#!/usr/bin/env python3
"""One Emoji, One Smile — writes exactly one emoji to /output/entry.txt.

Chosen emoji: U+1F917 HUGGING FACE (a hug offered to a stranger: the one
candidate that plainly aims to warm whoever reads it, reads the same way to
every age and background, and carries no irony, intimacy or flirtation).

The file is written as raw UTF-8 bytes with no trailing newline and no other
characters, so the payload is byte-identical on every run.
"""

import os
import sys

# Single code point: U+1F917 HUGGING FACE. 4 bytes in UTF-8, 1 code point.
EMOJI = "\U0001F917"
OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def build_payload() -> bytes:
    """Return the exact bytes to write: the emoji, nothing else."""
    payload = EMOJI.encode("utf-8")
    # Guard the gate contract before touching disk.
    if payload.decode("utf-8") != EMOJI:
        raise SystemExit("encoding round-trip failed")
    if len(EMOJI) != 1:
        raise SystemExit(f"expected 1 code point, got {len(EMOJI)}")
    if len(payload) > 8:
        raise SystemExit(f"payload is {len(payload)} bytes, gate allows 8")
    if any(ch.isspace() for ch in EMOJI):
        raise SystemExit("payload contains whitespace")
    return payload


def main() -> int:
    payload = build_payload()
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except OSError as exc:
        print(f"cannot create {OUTPUT_DIR}: {exc}", file=sys.stderr)
        return 1
    try:
        # Binary write: no newline translation, no BOM, no trailing bytes.
        with open(OUTPUT_PATH, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        print(f"cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 1
    # Read back and confirm the artifact on disk is exactly the payload.
    try:
        with open(OUTPUT_PATH, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        print(f"cannot read back {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 1
    if written != payload:
        print("verification failed: on-disk bytes differ from payload",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
