#!/usr/bin/env python3
"""One Emoji, One Smile — writes exactly one emoji to /output/entry.txt.

Final choice (revision round): U+1F917 HUGGING FACE.

Why this one, after weighing the alternatives again in criterion order:

* Criterion 1 (must plainly aim to warm a stranger). This is the cut that
  settles the list. A hug is addressed to the reader. Sunflower, rainbow,
  orange heart, sun-with-face, hatching chick and baby chick are moods,
  objects or creatures the stranger merely observes; a relieved face smiles
  inward; a melting face is irony. All of them lose here to a real gesture.
* Criterion 2 (warmth at first glance). Raising hands is "hooray", "praise"
  or "surrender" depending on the reader, so no single warm reading locks in.
* Criterion 3 (universality). Heart hands (U+1FAF6) is Unicode 14, added in
  2021: on older devices it does not render at all and shows as a blank box,
  and it also carries the Korean "finger heart" in-joke. A hug is Unicode 8
  (2015), renders everywhere, and is read the same way by every age.
* Criterion 5 (right for a stranger). Smiling face with hearts reads as
  affection or flirtation from someone unknown, which is the wrong note.

The two weaknesses of this emoji were weighed rather than ignored: some
readers see the hands as "jazz hands", and a hug offered to a stranger could
imply contact. The first is a minority reading against an overwhelming
convention of "sending hugs", and in messaging the hug is the sentiment at a
distance, not physical intimacy. Kept, because it is the only candidate that
is aimed at the stranger, supported on every device, and free of both irony
and flirtation at once.

The artifact is written as raw UTF-8 bytes: no trailing newline, no BOM, no
other characters, so the same bytes land on every run.
"""

import os
import sys

# One code point, U+1F917 HUGGING FACE, 4 bytes in UTF-8. Chosen over
# U+1FAF6 (heart hands) for font coverage and over the cheerful-object
# candidates for being aimed at the reader. Do not substitute a fallback:
# a variation selector or ZWJ would make this more than one code point.
EMOJI = "\U0001F917"
OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def build_payload() -> bytes:
    """Return the exact bytes to write: the emoji and nothing else."""
    payload = EMOJI.encode("utf-8")
    # Guard the published gate before anything touches the disk.
    if payload.decode("utf-8") != EMOJI:
        raise SystemExit("encoding round-trip failed")
    if len(EMOJI) != 1:
        raise SystemExit(f"expected 1 code point, got {len(EMOJI)}")
    if len(EMOJI) > 8:
        raise SystemExit(f"payload is {len(EMOJI)} characters, gate allows 8")
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
        # Report the real error rather than guessing at a cause.
        print(f"cannot create {OUTPUT_DIR}: {exc}", file=sys.stderr)
        return 1
    try:
        # Binary mode: no newline translation, no BOM, no trailing bytes.
        with open(OUTPUT_PATH, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        print(f"cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 1
    # Read the file back and refuse to claim success on a mismatch.
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
