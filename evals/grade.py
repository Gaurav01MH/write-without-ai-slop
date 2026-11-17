#!/usr/bin/env python3
"""Run the exact checks on saved outputs and print a table.

Usage: python3 evals/grade.py RUN_DIR [EVAL_DIR]
EVAL_DIR defaults to evals/. Use evals/v2 for the second case set.
RUN_DIR holds one file per case, named with the case id, for example 02.md.
This covers only what a machine can check: the script checks from
scripts/check_text.py and a minimum similarity to the input where a case sets
one. Whether the voice is kept, a pattern is gone, or a claim is new still
needs a person or a second model to read.
"""

import difflib
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
if len(sys.argv) > 2:
    HERE = os.path.abspath(sys.argv[2])

from check_text import check  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(run_dir):
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as f:
        cases = json.load(f)
    rows = []
    for case in cases:
        matches = glob.glob(os.path.join(run_dir, case["id"] + "*"))
        if not matches:
            rows.append((case["id"], case["name"], "no output", ""))
            continue
        output = read(matches[0])
        # Facts given in the request count as given, so they are not "new".
        source = read(os.path.join(HERE, case["input"]))
        original = source + "\n" + case["request"]
        # Check the returned text only. The "Changed:" notes may name the
        # patterns they removed, and that must not count as a finding.
        body = output.split("\nChanged:")[0].split("\nLeft alone on purpose:")[0]
        notes = []
        if case["script"]:
            notes += check(original, body, quote_source=source)
        floor = case.get("similarity_min")
        if floor:
            ratio = difflib.SequenceMatcher(None, source.strip(), body.strip()).ratio()
            if ratio < floor:
                notes.append("similarity %.2f below %.2f" % (ratio, floor))
        rows.append((case["id"], case["name"], "fail" if notes else "pass", "; ".join(notes)))
    for row in rows:
        print("%s  %-28s %-9s %s" % row)
    failed = [r for r in rows if r[2] != "pass"]
    print("\n%d of %d pass the exact checks" % (len(rows) - len(failed), len(rows)))
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
