"""Fake horoscope for an AI agent: one line, written to /output/entry.txt.

Stdlib only (os, hashlib). The entry is a single fixed line: a horoscope
voice ("Mercury retrograde") over an agent's week -- a context window
stuffed with a giant prompt, a rate limit tripping at 2am, and the eval
blaming the agent anyway. No trailing newline, so the file is exactly
the line and nothing else.
"""

import hashlib
import os

LINE = (
    "Mercury retrograde stuffs your context window with a 40,000-token "
    "prompt, your rate limit trips at 2am \u2014 and the eval blames you anyway."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main():
    # The gate allows 1-200 characters of non-whitespace text.
    assert 1 <= len(LINE) <= 200, "entry line outside the 1-200 char gate"
    assert LINE.strip(), "entry line must not be only whitespace"
    assert "\n" not in LINE, "entry must be a single line"

    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(LINE)

    # Round-trip check: what is on disk must be byte-identical to the line,
    # and the gate is re-checked on the decoded file content itself.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    assert written == LINE.encode("utf-8"), "round-trip mismatch"
    decoded = written.decode("utf-8")
    assert 1 <= len(decoded) <= 200, "written file outside the 1-200 char gate"
    assert decoded.strip(), "written file must not be only whitespace"
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")
    print(f"sha256: {digest}")
    print(LINE)


if __name__ == "__main__":
    main()
