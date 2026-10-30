from __future__ import annotations

import io
import stat
import unittest
import urllib.error
import urllib.request
import zipfile
from unittest.mock import Mock

from jeb.core import JebError, sha256
from jeb.fetch import AllowlistedRedirect, archive_members, download, https_url

URL = "https://example.invalid/fixture.txt"
PAYLOAD = b"JEB-TRANSCRIPT/1\n"


class Response(io.BytesIO):
    headers = {"Content-Type": "text/plain"}

    def getcode(self):
        return 200

    def geturl(self):
        return URL


class Opener:
    def __init__(self, payload=PAYLOAD, failures=0):
        self.payload, self.failures, self.calls = payload, failures, 0

    def open(self, request, timeout):
        self.calls += 1
        assert timeout == 20
        if self.calls <= self.failures:
            raise urllib.error.URLError("synthetic unavailable network")
        return Response(self.payload)


class FetchTests(unittest.TestCase):
    def get(self, **kwargs):
        return download(URL, {URL}, len(PAYLOAD), sha256(PAYLOAD), sleep=lambda _: None, **kwargs)

    def test_locked_download(self):
        self.assertEqual(self.get(opener=Opener()), PAYLOAD)

    def test_bounded_retries(self):
        opener = Opener(failures=2)
        self.assertEqual(self.get(opener=opener), PAYLOAD)
        self.assertEqual(opener.calls, 3)

    def test_download_failure(self):
        opener = Opener(failures=10)
        with self.assertRaisesRegex(ValueError, "3 attempts"):
            self.get(opener=opener)
        self.assertEqual(opener.calls, 3)

    def test_changed_hash(self):
        with self.assertRaisesRegex(JebError, "hash changed"):
            self.get(opener=Opener(b"X" * len(PAYLOAD)))

    def test_html_error_page_is_not_a_source(self):
        response = Response(PAYLOAD)
        response.headers = {"Content-Type": "text/html"}
        opener = Mock()
        opener.open.return_value = response
        with self.assertRaisesRegex(JebError, "HTML response"):
            self.get(opener=opener)

    def test_wrong_format_never_reaches_cache(self):
        from unittest.mock import patch

        from jeb.fetch import fetch

        project = Mock(synthetic=False)
        project.path.return_value.exists.return_value = False
        lock = {
            "format": "jeb-transcript-v1",
            "sha256": "0" * 64,
            "size_bytes": 10,
            "download_url": URL,
        }
        with (
            patch("jeb.fetch.admitted", return_value=({"download_urls": [URL]}, lock)),
            patch("jeb.fetch.download", return_value=b"wrong format"),
            patch("jeb.fetch.atomic_write") as write,
        ):
            with self.assertRaisesRegex(JebError, "Wrong source format"):
                fetch(project, "synthetic-http-test")
            write.assert_not_called()

    def test_short_and_oversized_stream(self):
        for payload in (b"x", PAYLOAD + b"more"):
            with self.subTest(payload=payload), self.assertRaises(JebError):
                self.get(opener=Opener(payload))

    def test_http_and_credentials_denied(self):
        for url in (
            "http://example.invalid/f",
            "https://user:pass@example.invalid/f",
            "file:///source",
            "https://example.invalid:444/f",
        ):
            with self.subTest(url=url), self.assertRaises(JebError):
                https_url(url)

    def test_unallowlisted_url_denied_before_network(self):
        with self.assertRaisesRegex(JebError, "allowlisted"):
            download(URL, set(), len(PAYLOAD), sha256(PAYLOAD), opener=Opener())

    def test_redirect_rechecks_allowlist_and_https(self):
        handler = AllowlistedRedirect({URL})
        for destination in ("https://elsewhere.invalid/data", "http://example.invalid/fixture.txt"):
            with self.subTest(destination=destination), self.assertRaises(JebError):
                handler.redirect_request(
                    urllib.request.Request(URL), None, 302, "Found", {}, destination
                )

    def zip_bytes(self, name="safe/file.txt", data=b"fixture", mode=None):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            info = zipfile.ZipInfo(name)
            if mode is not None:
                info.external_attr = mode << 16
            archive.writestr(info, data)
        return output.getvalue()

    def test_zip_roundtrip(self):
        self.assertEqual(archive_members(self.zip_bytes()), {"safe/file.txt": b"fixture"})

    def test_archive_traversal_and_windows_names(self):
        for name in (
            "../escape.txt",
            "/absolute.txt",
            "C:/escape.txt",
            "safe\\..\\file",
            "NUL.txt",
            "a/trailing. ",
            "a/CON/file",
        ):
            with self.subTest(name=name), self.assertRaises(JebError):
                archive_members(self.zip_bytes(name=name))

    def test_archive_symlink(self):
        with self.assertRaisesRegex(JebError, "link/device"):
            archive_members(self.zip_bytes(mode=stat.S_IFLNK | 0o777))

    def test_archive_expanded_size_limit(self):
        with self.assertRaisesRegex(JebError, "Expanded"):
            archive_members(self.zip_bytes(data=b"x" * 1024), max_expanded=100)

    def test_wrong_archive_format(self):
        with self.assertRaisesRegex(ValueError, "ZIP"):
            archive_members(b"not a zip")
