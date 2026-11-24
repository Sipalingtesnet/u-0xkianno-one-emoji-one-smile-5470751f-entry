#!/usr/bin/env python3
"""One Emoji, One Smile - writes exactly one emoji to /output/entry.txt.

Final choice after the revision round: U+1F917 HUGGING FACE.

The choice was reopened and the two strongest rivals were argued against it
in criterion order, not defended by default:

* U+1F917 vs U+1F423 (hatching chick). The chick is a genuine rival: Unicode
  6.0, so it renders everywhere, no flirtation, no irony, and gently funny,
  which criterion 2 explicitly allows. It loses on criterion 1 all the same.
  The brief says the entry "loses to any emoji that plainly aims to warm a
  stranger", and a chick is a creature the reader observes, not a gesture
  addressed to them. Criterion 1 is listed first and is the first place the
  two differ, so it decides.
* U+1F917 vs U+1FAF6 (heart hands). Heart hands does aim at the reader, so it
  clears criterion 1 alongside the hug, then loses on criterion 3 for a
  checkable reason: it is Unicode 14 (2021), so on older devices it does not
  render and shows a blank box, and a stranger reads nothing at all. It also
  carries the Korean finger-heart in-joke, the shared-context reading
  criterion 3 forbids. Under criterion 4 it is spent: the round brief notes
  it already appears in other entries' titles.

The pick's own weakness was weighed rather than hidden: some readers see the
hands as "jazz hands" and read it as performative or sarcastic. That is a
minority reading against the convention that fixes this emoji as "sending
hugs" - comfort offered at a distance, which is the brief's target - and
against it being Unicode 8 (2015), rendered everywhere. The finger-heart and
blank-box problems are failures, not minority readings, so they decide.

The artifact is written as raw UTF-8 bytes: no trailing newline, no BOM and no
other characters, so the same bytes land on every run. The file is read back
and compared before success is reported, because /output is a shared path that
other processes on this host also write to.
"""

import os
import sys

# One code point, U+1F917 HUGGING FACE, 4 bytes in UTF-8.
# Rejected here: U+1FAF6 (no glyph on older devices), U+1F423 (not aimed at
# the reader), U+1F970 (reads as flirtation from a stranger). Do not append a
# variation selector or ZWJ: that would make the payload more than one code
# point and break the single-emoji gate.
EMOJI = "\U0001F917"
OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def build_payload() -> bytes:
    """Return the exact bytes to write: the emoji and nothing else."""
    payload = EMOJI.encode("utf-8")
    # Hold the payload to the published gate before anything touches disk.
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
        # Report the real error; never guess at a cause.
        print(f"cannot create {OUTPUT_DIR}: {exc}", file=sys.stderr)
        return 1
    try:
        # Binary mode: no newline translation, no BOM, no trailing bytes.
        with open(OUTPUT_PATH, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        print(f"cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 1
    # Read straight back and refuse to report success on a mismatch.
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
