# Contributing

This skill says what not to do. It does not teach a style. Keep it that way.

## Adding a pattern or a word

1. Give a source and its date. A style guide, a study or a community guide is fine.
2. If there is no source, say "inference" in the entry. Do not present a guess as a finding.
3. Add an invented before and after example. Do not use real people's text.
4. Add a test case in `evals/` that fails without your change.

## Reporting a bad output

Use the [bad output form](https://github.com/nocodeanish/write-without-ai-slop/issues/new?template=bad-output.yml). Copy the request, the text you gave and the answer you got.

## First tasks

Issues with the `good first issue` label are small and list their steps. Say in a comment that you are taking one, then open a pull request.

## Keeping it short

`SKILL.md` stays under 150 lines. Detail goes in `references/`, one level deep.

## Writing in this repo

Short sentences, plain words, one idea per sentence. No long dashes. Label a claim without a source as inference. Some readers use English as a second language, so avoid idioms and puns.

## Tests

See `evals/README.md`. Run `python3 scripts/check_text.py ORIGINAL OUTPUT` after any change to the checks.

Run `python3 scripts/check_consistency.py` before you open a pull request. It checks that the version, the test counts and the links agree across files, and the same check runs on every pull request. If you add a test case, update the counts in `evals/README.md`.

## README art

The images in `.github/readme/` are built by `.github/readme/make_art.py`. Change the script, run it, and commit the SVG files with it. CI runs `make_art.py --check` and fails if they differ. The art holds no version or test counts, so those never go stale in it. Keep every image's alt text in the README, and keep the total under 250 KB. The motion is plain CSS, so it plays on GitHub without scripts, and every file shows its finished picture when a reader prefers reduced motion.

## Credit

Contributors are named in the changelog entry for their change, unless they ask to stay out.
