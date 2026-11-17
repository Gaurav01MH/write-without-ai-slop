# write-without-ai-slop

**Stop your AI agent from writing like every other AI.**

AI text looks, feels and reads the same, and readers notice. This skill lists what not to do. It does not teach a style, so your agent keeps its own voice, or yours. No setup, and it does not ask questions mid-task. It is an agent skill: a folder with a SKILL.md file that agents read.

## See it work

Before:

```
Here's the thing: shipping fast isn't just about speed, it's about trust.

Last month our team cut the checkout bug backlog from 42 to 9 in two weeks. Not just a win for engineering, but a win for customers, for the business, and for the future.

Agree? What's your biggest lesson?
```

After:

```
Shipping fast builds trust.

Last month our team cut the checkout bug backlog from 42 to 9 in two weeks.
```

The numbers stayed. The setup line, the "not just X" contrast, the group of three and the bait question went. More in [examples](examples/before-after.md). All examples are invented.

## Install

One line, for agents that support the skills installer:

```
npx skills add nocodeanish/write-without-ai-slop
```

In Claude Code 2.1.275 or later:

```
/plugin install write-without-ai-slop --marketplace nocodeanish/write-without-ai-slop
```

Or copy the folder into your agent's skills folder. For example, in Claude Code:

```
cp -r write-without-ai-slop ~/.claude/skills/
```

## How it works

- **Check:** ask it to check a draft. You get a list of problems, each with the quoted line and a short fix. Nothing is rewritten.
- **Rewrite:** give it a draft. You get the smallest edit that removes the problems, and a short list of what changed. Say the text will be pasted as it is, and you get only the text.
- **Write:** an agent that is about to write follows the rules while it writes.

## What it catches

- Invented facts, numbers, quotes and names.
- Chatbot leftovers such as "Certainly!", "I hope this helps" and unfilled placeholders.
- Sameness: five posts that open or end the same way.
- Patterns that matter in combination: "not X, but Y", groups of three, setups before the point, fake meaning at the end of a sentence, stacked fragments, piled-up hedges, vague sources, and more.

It has short pages for LinkedIn, X, email, website copy, docs and Slack.

## What it does not do

- It does not teach good writing or a house style.
- It does not detect AI. Detectors are unreliable: in one study, seven of them flagged 61% of essays by non-native English writers as AI, though people wrote them. This skill never says who wrote a text.
- One pattern proves nothing. It acts on combinations, and leaves a text alone when only one shows up.
- It works on English. For other languages it checks only for invented facts, padding and sameness.

## Something went wrong?

Open a [bad output report](https://github.com/nocodeanish/write-without-ai-slop/issues/new?template=bad-output.yml). Paste your request, the text and the answer. Use invented text or text you are free to share.

To add a pattern or fix a page, see [CONTRIBUTING.md](CONTRIBUTING.md). Small first tasks carry the `good first issue` label.

## Your own voice

Give your agent a voice file or a short sample with your request. The skill keeps your phrasing and adds no voice of its own.

## Tests and sources

Test cases and results are in [evals/](evals/). Where each rule comes from is in [docs/sources.md](docs/sources.md). Versions are in the [changelog](CHANGELOG.md).

## License

MIT. Created by Anish Gandhi. See `LICENSE`.

If this saved you an edit, a star helps other people find it.
