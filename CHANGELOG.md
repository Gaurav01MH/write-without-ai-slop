# Changelog

## Unreleased

- `scripts/check_consistency.py` checks that the version, test counts, links and skill format agree across files. A GitHub Action runs it on every push and pull request.
- README: added a "Does it work?" section with the test results and their limits, and a "Privacy" section.
- CONTRIBUTING: run the consistency check before a pull request; contributors are named in the changelog.
- README art: a banner, an animated before and after, and a page on what each way returns. They are SVG files under `.github/readme/` (15 KB in total), built by `make_art.py`. The README keeps the same example as text in a collapsed block.
- README: status, license and release badges; a note that editors call leaving a text alone *stet*.
- The consistency check now also checks the README art: alt text, missing or unused files, a size limit, and the install command in the demo. CI rebuilds the art and fails if the files differ.

## 0.5.0 (2026-11-17)

First public version.

- Rules for check, rewrite and write, with pages for LinkedIn, X, email, website copy, docs and Slack.
- When the request says the text will be pasted as it is, only the text comes back.
- A text with one tell and otherwise specific content is left unchanged.
- Check findings quote a line and name the pattern, and end with one sentence.
- Missing names become a marker such as "[your name]". No invented senders or closers.
- Test cases and a script for exact checks. See `evals/README.md`.
