#!/usr/bin/env python3
"""Build evals/prompts.md from cases.json and the input files.

The prompts file holds only the request and the text for each case. It does
not hold the pass checks, so a model under test cannot read them there.
Usage: python3 evals/make_prompts.py [EVAL_DIR]
EVAL_DIR defaults to evals/. Use evals/v2 for the second case set.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
if len(__import__("sys").argv) > 1:
    HERE = os.path.abspath(__import__("sys").argv[1])


def main():
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as f:
        cases = json.load(f)
    parts = []
    for case in cases:
        with open(os.path.join(HERE, case["input"]), encoding="utf-8") as f:
            text = f.read()
        parts.append("## Case %s\n\nRequest: %s\n\nText:\n\n<<<\n%s\n>>>\n" % (case["id"], case["request"], text))
    with open(os.path.join(HERE, "prompts.md"), "w", encoding="utf-8") as f:
        f.write("# Prompts\n\nEach case is independent.\n\n" + "\n".join(parts))
    print("wrote prompts.md with %d cases" % len(cases))


if __name__ == "__main__":
    main()
