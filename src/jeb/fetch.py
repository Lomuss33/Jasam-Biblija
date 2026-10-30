"""Bounded, locked HTTPS acquisition; safe ZIP extraction when a future adapter needs it."""

from __future__ import annotations

import io
import re
import stat
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import PurePosixPath

from jeb.core import Project, atomic_write, read_bytes, require, sha256
from jeb.sources import admitted

MAX_DOWNLOAD = 32 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024
MAX_MEMBERS = 256


def https_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    require(
        parsed.scheme == "https"
        and bool(parsed.hostname)
        and not parsed.username
        and not parsed.password
        and not parsed.fragment
        and parsed.port in (None, 443),
        "Only credential-free HTTPS on port 443 is allowed",
    )


class AllowlistedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, urls: set[str]):
        self.urls = urls

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        https_url(newurl)
        require(newurl in self.urls, "Redirect URL is not explicitly allowlisted")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(
    url: str,
    allowed_urls: set[str],
    expected_size: int,
    expected_hash: str,
    *,
    opener=None,
    retries: int = 2,
    sleep=time.sleep,
) -> bytes:
    https_url(url)
    require(url in allowed_urls, "URL is not allowlisted")
    require(0 < expected_size <= MAX_DOWNLOAD, "Invalid locked download size")
    opener = opener or urllib.request.build_opener(AllowlistedRedirect(allowed_urls))
    payload = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "JEB/0.1 source-audit"})
            with opener.open(request, timeout=20) as response:
                require(response.getcode() == 200, "Unexpected HTTP status")
                require(response.geturl() in allowed_urls, "Unapproved final URL")
                content_type = response.headers.get("Content-Type", "").lower()
                require("html" not in content_type, "HTML response is not a source artifact")
                advertised = response.headers.get("Content-Length")
                require(
                    advertised is None or int(advertised) == expected_size,
                    "Server size differs from reviewed artifact",
                )
                output = io.BytesIO()
                while True:
                    chunk = response.read(min(65536, expected_size + 1 - output.tell()))
                    if not chunk:
                        break
                    output.write(chunk)
                    require(output.tell() <= expected_size, "Download exceeds locked size")
                payload = output.getvalue()
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if isinstance(exc, urllib.error.HTTPError) and exc.code < 500:
                raise ValueError(f"Download failed: HTTP {exc.code}") from exc
            if attempt == retries:
                raise ValueError(f"Download failed after {attempt + 1} attempts: {exc}") from exc
            sleep(0.1 * (attempt + 1))
    require(payload is not None and len(payload) == expected_size, "Incomplete source download")
    require(
        sha256(payload) == expected_hash, "Upstream hash changed; explicit re-evaluation required"
    )
    return payload


def archive_members(payload: bytes, *, max_expanded: int = MAX_EXPANDED) -> dict[str, bytes]:
    require(len(payload) <= MAX_DOWNLOAD, "Archive download too large")
    result = {}
    total = 0
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            require(len(archive.infolist()) <= MAX_MEMBERS, "Too many archive members")
            for member in archive.infolist():
                name = member.filename
                path = PurePosixPath(name)
                require(
                    not path.is_absolute()
                    and ".." not in path.parts
                    and "\\" not in name
                    and ":" not in name
                    and not any(re.search(r"[. ]$|[\x00-\x1f]", part) for part in path.parts),
                    f"Unsafe archive path: {name}",
                )
                require(
                    not any(
                        part.split(".")[0].upper()
                        in {
                            "CON",
                            "PRN",
                            "AUX",
                            "NUL",
                            *[f"COM{i}" for i in range(10)],
                            *[f"LPT{i}" for i in range(10)],
                        }
                        for part in path.parts
                    ),
                    f"Unsafe Windows archive name: {name}",
                )
                mode = member.external_attr >> 16
                require(
                    stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR),
                    "Archive link/device forbidden",
                )
                require(not member.flag_bits & 1, "Encrypted archive unsupported")
                require(
                    name.casefold() not in {n.casefold() for n in result}, "Duplicate archive path"
                )
                total += member.file_size
                require(total <= max_expanded, "Expanded archive size exceeded")
                if member.is_dir():
                    continue
                with archive.open(member) as stream:
                    data = stream.read(min(member.file_size, max_expanded) + 1)
                require(len(data) == member.file_size, "Archive member size mismatch")
                result[name] = data
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise ValueError(f"Invalid/unsupported ZIP: {exc}") from exc
    # Validate everything before the caller writes anything. No extractall() or filesystem paths.
    return result


def fetch(project: Project, source_id: str) -> dict:
    source, lock = admitted(project, source_id)
    require(
        not project.synthetic,
        "Synthetic fixtures are installed locally by jeb demo; never downloaded",
    )
    require(lock["format"] == "jeb-transcript-v1", "No audited adapter for this source format")
    path = project.path(f"data/raw/{source_id}/{lock['sha256']}.txt")
    if path.exists():
        data = read_bytes(path, MAX_DOWNLOAD)
        require(
            len(data) == lock["size_bytes"] and sha256(data) == lock["sha256"],
            "Cached source changed",
        )
        return {"source_id": source_id, "cached": True, "sha256": lock["sha256"]}
    data = download(
        lock["download_url"], set(source["download_urls"]), lock["size_bytes"], lock["sha256"]
    )
    require(
        data.startswith(b"JEB-TRANSCRIPT/1\n"), "Wrong source format; expected JEB-TRANSCRIPT/1"
    )
    atomic_write(path, data, replace=False)
    return {"source_id": source_id, "cached": False, "sha256": lock["sha256"]}
