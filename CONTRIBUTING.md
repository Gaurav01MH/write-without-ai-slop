# Contributing

This skill says what not to do. It does not teach a style. Keep it that way.

## Adding a pattern or a word

1. Give a source and its date. A style guide, a study or a community guide is fine.
2. If there is no source, say "inference" in the entry. Do not present a guess as a finding.
3. Add an invented before and after example. Do not use real people's text.
4. Add a test case in `evals/` that fails without your change.

## Keeping it short

`SKILL.md` stays under 150 lines. Detail goes in `references/`, one level deep.

## Writing in this repo

Short sentences, plain words, one idea per sentence. No long dashes. Label a claim without a source as inference. Some readers use English as a second language, so avoid idioms and puns.

## Tests

See `evals/README.md`. Run `python3 scripts/check_text.py ORIGINAL OUTPUT` after any change to the checks.
