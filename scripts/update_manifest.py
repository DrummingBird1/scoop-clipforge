"""Point bucket/clipforge.json at the latest ClipForge release.

The zip is downloaded and hashed, and the result has to match the release's
SHA256SUMS.txt. Nothing is written when any check fails. Standard library only.
"""

import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

APP_REPO = "DrummingBird1/clipforge-app"
MANIFEST = Path(__file__).resolve().parent.parent / "bucket" / "clipforge.json"


def fetch(url, token=None):
    headers = {"User-Agent": "scoop-clipforge-updater"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120)


def version_tuple(version):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(f"Unexpected version format: {version!r}")
    return tuple(int(part) for part in version.split("."))


def listed_hash(sums, name):
    """The hash that SHA256SUMS.txt gives for exactly this file name."""
    found = []
    for line in sums.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].lstrip("*") == name:
            found.append(parts[0].lower())
    if len(found) != 1 or not re.fullmatch(r"[0-9a-f]{64}", found[0]):
        raise SystemExit(f"SHA256SUMS.txt has no single valid line for {name}")
    return found[0]


def sha256_of(url):
    digest = hashlib.sha256()
    with fetch(url) as response:
        while chunk := response.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def output(**values):
    """Hand values to the next workflow steps (printed when run locally)."""
    lines = "".join(f"{key}={value}\n" for key, value in values.items())
    print(lines, end="")
    if path := os.environ.get("GITHUB_OUTPUT"):
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(lines)


def main():
    text = MANIFEST.read_text(encoding="utf-8")
    manifest = json.loads(text)
    current = manifest["version"]

    # "latest" never returns a draft or a pre-release.
    api = f"https://api.github.com/repos/{APP_REPO}/releases/latest"
    with fetch(api, os.environ.get("GH_TOKEN")) as response:
        release = json.load(response)
    version = release["tag_name"].removeprefix("v")

    if version_tuple(version) <= version_tuple(current):
        print(f"The manifest has {current}, the latest release is {version}: nothing to do.")
        output(changed="false")
        return

    zip_name = f"ClipForge-{version}-win64.zip"
    base = f"https://github.com/{APP_REPO}/releases/download/v{version}"
    with fetch(f"{base}/SHA256SUMS.txt") as response:
        expected = listed_hash(response.read().decode("utf-8-sig"), zip_name)
    actual = sha256_of(f"{base}/{zip_name}")
    if actual != expected:
        raise SystemExit(f"Hash mismatch for {zip_name}: SHA256SUMS.txt {expected}, download {actual}")

    new_values = {
        "version": version,
        "url": f"{base}/{zip_name}",
        "hash": expected,
        "extract_dir": f"ClipForge-{version}-win64",
    }
    # Replace only the value text, so the rest of the file stays byte for byte.
    # count=1 picks the top-level key, which comes before the one in "autoupdate".
    for key, value in new_values.items():
        old = f'"{key}": {json.dumps(manifest[key])}'
        if old not in text:
            raise SystemExit(f"Could not find the {key!r} line in the manifest")
        text = text.replace(old, f'"{key}": {json.dumps(value)}', 1)

    if json.loads(text) != {**manifest, **new_values}:
        raise SystemExit("The edited manifest is not what was expected; nothing was written")

    MANIFEST.write_bytes(text.encode("utf-8"))
    output(changed="true", version=version, hash=expected)


if __name__ == "__main__":
    sys.exit(main())
