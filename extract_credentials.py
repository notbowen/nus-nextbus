#!/usr/bin/env python3
"""Extract NUS NextBus API credentials from a decompiled app directory."""

import base64
import json
import re
import sys
from pathlib import Path
from typing import Optional


def find_build_config(app_dir: Path) -> Optional[Path]:
    for path in app_dir.rglob("BuildConfig.java"):
        if "NNEXTBUS_API_KEY" in path.read_text():
            return path
    return None


def extract_credentials(app_dir: Path) -> dict:
    build_config = find_build_config(app_dir)
    if build_config is None:
        raise FileNotFoundError("BuildConfig.java not found under " + str(app_dir))

    text = build_config.read_text()

    url_match = re.search(r'NNEXTBUS_API_URL\s*=\s*"([^"]+)"', text)
    key_match = re.search(r'NNEXTBUS_API_KEY\s*=\s*"((?:[^"\\]|\\.)*)"', text)

    if not url_match or not key_match:
        raise ValueError("Could not find NNEXTBUS_API_URL or NNEXTBUS_API_KEY in " + str(build_config))

    api_url = url_match.group(1)
    api_key = key_match.group(1).replace('\\"', '"')
    auth_header = "Basic " + base64.b64encode(api_key.encode()).decode()

    return {
        "api_url": api_url,
        "api_key": api_key,
        "auth_header": auth_header,
        "source": str(build_config),
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <app_dir>", file=sys.stderr)
        sys.exit(1)

    app_dir = Path(sys.argv[1])
    if not app_dir.is_dir():
        print(f"Error: {app_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    creds = extract_credentials(app_dir)
    print(json.dumps(creds, indent=2))


if __name__ == "__main__":
    main()
