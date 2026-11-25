#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh (make.fun bounty).

Writes a single roast line about a smart fridge to /output/entry.txt
(or MAKEFUN_OUTPUT_DIR, falling back to ./output/entry.txt).

Deterministic: the same line is written on every run, no network,
no randomness, no dependencies beyond the Python standard library.
"""

import os
import sys

# The roast line, chosen after drafting five candidates and scoring them
# against the judge's five criteria (on-subject, punchline lands,
# smart-fridge-specific, tight wording, fresh angle). The winner:
# the touchscreen advertises milk that is already expiring inside it.
ROAST = (
    "My smart fridge's touchscreen shows me ads for milk "
    "while the milk expires two inches behind the glass."
)

MAX_CHARS = 200


def resolve_output_path() -> str:
    """Pick where entry.txt goes: /output, env override, or ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, "entry.txt")
    default_path = os.path.join(os.sep, "output", "entry.txt")
    try:
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        return default_path
    except OSError:
        return os.path.join("output", "entry.txt")


def main() -> int:
    line = ROAST.strip()
    if not line:
        print("error: roast line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: roast line is {len(line)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    path = resolve_output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Write exactly the line, no trailing newline: the file IS the entry.
    # If the primary location turns out unwritable at write time (e.g.
    # /output is read-only), fall back to ./output instead of crashing.
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
    except OSError:
        fallback = os.path.join("output", "entry.txt")
        if path == fallback:
            raise
        path = fallback
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)

    print(line)
    print(f"characters: {len(line)}")
    print(f"wrote: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
