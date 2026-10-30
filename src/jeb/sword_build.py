"""Optional offline build of the pinned, synthetic-only SWORD diagnostic profile."""

from __future__ import annotations

import difflib
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

from jeb.core import Project, read_bytes, read_json, require, sha256, write_json
from jeb.sword_diagnostic import SOURCE_HASH, TOOL_NAMES, check_tool_lock


def build(
    project: Project, archive: Path, output: str, compiler: str, c_compiler: str, cmake: str
) -> dict:
    archive_bytes = read_bytes(archive, 8 * 1024 * 1024)
    require(
        len(archive_bytes) == 2606652 and sha256(archive_bytes) == SOURCE_HASH,
        "Software archive is not the reviewed SWORD 1.9.0 release",
    )
    destination = project.path(output)
    require(not destination.exists(), "Build output exists; preserve it and choose a fresh path")
    destination.mkdir(parents=True)
    resources = project.path("toolchains/sword-1.9.0")
    source = destination / "sword-1.9.0"
    commands = []

    def run(arguments: list[str], label: str, timeout: int = 300) -> bytes:
        with (
            (destination / f"{label}.stdout").open("wb") as stdout,
            (destination / f"{label}.stderr").open("wb") as stderr,
        ):
            process = subprocess.run(
                arguments, stdout=stdout, stderr=stderr, timeout=timeout, check=False
            )
        commands.append({"label": label, "arguments": arguments, "returncode": process.returncode})
        write_json(destination / "commands.json", commands)
        require(process.returncode == 0, f"Native {label} failed; inspect {output}/{label}.stderr")
        return read_bytes(destination / f"{label}.stdout", 8 * 1024 * 1024)

    try:
        omitted = []
        with tarfile.open(archive, "r:gz") as bundle:
            members = bundle.getmembers()
            require(
                len(members) <= 2000 and sum(m.size for m in members) <= 32 * 1024 * 1024,
                "Software archive exceeds reviewed extraction bounds",
            )
            regular = []
            for member in members:
                require(
                    member.name.startswith("sword-1.9.0/") or member.name == "sword-1.9.0",
                    "Unexpected software archive prefix",
                )
                if member.issym():
                    require(
                        member.name.startswith("sword-1.9.0/bindings/Android/"),
                        "Unexpected software archive symlink",
                    )
                    omitted.append(member.name)
                    continue
                require(
                    member.isfile() or member.isdir(), "Unsupported software archive special member"
                )
                regular.append(member)
            require(len(omitted) == 7, "Software source symlink inventory changed")
            # Preserve the upstream archive and omit its known Android symlinks; never materialize links.
            bundle.extractall(destination, members=regular, filter="data")
        write_json(destination / "omitted-android-symlinks.json", omitted)
        patches = []
        for name in ("rawstr4-win64", "pointer-key-win64", "offline-no-ftp"):
            descriptor = read_json(resources / f"{name}.json")
            records = descriptor.get("changes", [descriptor])
            computed_patch = []
            for record in records:
                target = (source / record["file"]).resolve()
                require(
                    target.is_relative_to(source.resolve()) and not target.is_symlink(),
                    "Unsafe patch target",
                )
                before = read_bytes(target)
                require(
                    sha256(before) == record["before_sha256"], "Upstream patch preimage changed"
                )
                if name == "rawstr4-win64":
                    after = before.replace(b"(unsigned long)datfd > 0", b"datfd != 0").replace(
                        b"(unsigned long)idxfd > 0", b"idxfd != 0"
                    )
                elif name == "pointer-key-win64":
                    after = before.replace(
                        b"(unsigned long)key", b"reinterpret_cast<std::uintptr_t>(key)"
                    )
                    index = after.index(b"#include")
                    after = after[:index] + b"#include <cstdint>\n" + after[index:]
                else:
                    after = before.replace(
                        b"SET(sword_SOURCES ${sword_SOURCES} ${sword_curl_nofound_SOURCES})",
                        b"# JEB offline diagnostic build: omit the legacy FTP transport implementation.",
                    )
                require(
                    sha256(after) == record["after_sha256"],
                    "Patch output differs from reviewed result",
                )
                computed_patch.extend(
                    difflib.diff_bytes(
                        difflib.unified_diff,
                        before.splitlines(keepends=True),
                        after.splitlines(keepends=True),
                        fromfile=("a/" + record["file"]).encode(),
                        tofile=("b/" + record["file"]).encode(),
                        n=2 if name == "pointer-key-win64" else 3,
                    )
                )
                target.write_bytes(after)
            patch = resources / f"{name}.patch"
            require(
                b"".join(computed_patch) == read_bytes(patch), "Patch diff and descriptor disagree"
            )
            patches.append(
                {
                    "path": patch.relative_to(project.root).as_posix(),
                    "sha256": sha256(read_bytes(patch)),
                }
            )
        cpp = shutil.which(compiler)
        cc = shutil.which(c_compiler)
        cmake_command = shutil.which(cmake)
        require(
            cpp is not None and cc is not None and cmake_command is not None,
            "A C++ compiler, C compiler and CMake must already be installed",
        )
        native_build = destination / "build"
        flags = [
            "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_CXX_STANDARD=11",
            "-DLIBSWORD_LIBRARY_TYPE=Static",
            "-DSWORD_NO_CURL=Yes",
            "-DSWORD_NO_ICU=Yes",
            "-DSWORD_NO_BZIP2=Yes",
            "-DSWORD_NO_XZ=Yes",
            "-DSWORD_NO_CLUCENE=Yes",
            "-DSWORD_USE_INTERNAL_ZLIB=Yes",
            "-DCMAKE_DISABLE_FIND_PACKAGE_Regex=TRUE",
            "-DSWORD_BUILD_TESTS=OFF",
            "-DSWORD_BUILD_EXAMPLES=No",
            "-DSWORD_BUILD_UTILS=Yes",
            "-DCMAKE_C_FLAGS=-DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1",
        ]
        cpp_version = (
            run([cpp, "--version"], "compiler-version")
            .decode("utf-8", errors="replace")
            .splitlines()[0]
        )
        cmake_version = (
            run([cmake_command, "--version"], "cmake-version")
            .decode("utf-8", errors="replace")
            .splitlines()[0]
        )
        run(
            [
                cmake_command,
                "-S",
                str(source),
                "-B",
                str(native_build),
                "-G",
                "Ninja",
                f"-DCMAKE_CXX_COMPILER={cpp}",
                f"-DCMAKE_C_COMPILER={cc}",
                f"-DCMAKE_INSTALL_PREFIX={destination / 'unused-install'}",
                *flags,
            ],
            "configure",
        )
        run(
            [
                cmake_command,
                "--build",
                str(native_build),
                "--parallel",
                "4",
                "--target",
                "imp2vs",
                "mod2imp",
                "mod2osis",
            ],
            "build",
        )
        windows = os.name == "nt"
        suffix = ".exe" if windows else ""
        tools = native_build / "utilities"
        probe_source = resources / "synthetic_probe.cpp"
        arguments = [
            cpp,
            "-std=c++11",
            "-O2",
            "-I" + str(source / "include"),
            "-I" + str(native_build / "include"),
            str(probe_source),
            str(native_build / "libsword.a"),
        ]
        if windows:
            arguments.append("-lws2_32")
        run([*arguments, "-o", str(tools / ("jeb-synthetic-probe" + suffix))], "build-probe")
        lock = {
            "schema_version": "1.0",
            "toolchain_id": "sword-1.9.0-jeb-offline-v1",
            "purpose": "synthetic_diagnostic_only",
            "platform": "windows" if windows else "linux",
            "source": {
                "url": "https://www.crosswire.org/ftpmirror/pub/sword/source/v1.9/sword-1.9.0.tar.gz",
                "sha256": SOURCE_HASH,
                "size_bytes": len(archive_bytes),
            },
            "patches": patches,
            "probe_source_sha256": sha256(read_bytes(probe_source)),
            "compiler": {
                "command": cpp,
                "version": cpp_version,
                "sha256": sha256(read_bytes(Path(cpp), 64 * 1024 * 1024)),
            },
            "cmake_version": cmake_version,
            "build_flags": flags,
            "executables": {
                name: {
                    "filename": name + suffix,
                    "size_bytes": (tools / (name + suffix)).stat().st_size,
                    "sha256": sha256(read_bytes(tools / (name + suffix), 32 * 1024 * 1024)),
                }
                for name in TOOL_NAMES
            },
        }
        check_tool_lock(lock, tools)
        write_json(destination / "toolchain.lock.json", lock, replace=False)
        return {
            "output": output,
            "lock": f"{output}/toolchain.lock.json",
            "synthetic_only": True,
            "tools": tools.relative_to(project.root).as_posix(),
            "source_sha256": SOURCE_HASH,
        }
    except (ValueError, OSError, subprocess.SubprocessError, tarfile.TarError) as exc:
        write_json(destination / "failure.json", {"error": str(exc), "commands": commands})
        raise ValueError(f"Optional SWORD build failed: {exc}") from exc
