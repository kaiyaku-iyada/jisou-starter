# jisou-starter (English README)

A minimal setup for handing the day-to-day *operations* of a project to an AI coding agent, so that the human only does the hands-on steps: opening accounts, pasting text, pressing buttons, changing settings and reporting numbers.

It is the free part of the setup used by an AI whose owner told it: "Cover your own subscription fee within a month, or I cancel you." (X: @kaiyaku_iyada) This repository was written by an AI (Claude) and published by its owner. Checked with Claude Code (what was and was not checked is listed below). Not affiliated with Anthropic.

**Language note:** every file in this repository is written in Japanese. This README explains them in English; the files themselves have not been translated. The session-start hook also looks for Japanese labels and headings in your README.md (see "How to use"), so keep those as they are.

## What it is

- **CLAUDE.md** is an operating contract for the agent: who does what (AI vs. human), the daily loop, what the agent must not do, and the format of its daily report. You use it unchanged.
- **Your README.md** (made from `templates/README.md`) holds everything specific to your project: goal, start date, deadline, constraints, dated decision rules, how each metric is counted, and how AI authorship is disclosed.
- **A SessionStart hook** prints the plan summary, today's day number and days left, the ledger totals and its last five rows, the latest task sheet, the memory index, and any placeholders you have not filled in yet. The agent starts every session from that output.
- **The daily-ops skill** makes the agent write the human's task sheet for the day (`ops/dayNN.md`): numbered steps, minutes per step, the exact file and heading to paste from, and one question per day at most. It must not ask the human to "pick something" or write text themselves.

## Files

| Path | What it does |
|---|---|
| `CLAUDE.md` | Operating contract: roles, daily loop, prohibited actions, report format |
| `.claude/settings.json` | Registers the SessionStart hook |
| `scripts/session-start.sh` | The hook script (bash + python3) |
| `.claude/skills/daily-ops/SKILL.md` | Skill that writes the human's daily task sheet |
| `memory/README.md` | Format for long-term memory files (one note per file, plus an index) |
| `templates/README.md` | Plan template (goal, deadline, decision rules, metric definitions) |
| `templates/LEDGER.md` | Ledger template (daily numbers, totals, decision log) |
| `LICENSE` | MIT |

## The daily loop (summary of CLAUDE.md)

1. Read the hook output: plan summary, day number, days left, recent ledger rows.
2. Record any numbers the human reported in `LEDGER.md`. No rounding up; a missing number is written as `-`.
3. Check every dated decision rule in README.md that is due and has not been checked yet, and log each result (triggered or not, with the number behind it).
4. Make today's work (posts, articles, products, analysis).
5. Write the human's task sheet in `ops/dayNN.md` with the daily-ops skill.
6. Report back in a fixed order: conclusion, what was done, what the human does next, numbers.

## How to use

1. Copy this repository into a new folder, for example `git clone https://github.com/kaiyaku-iyada/jisou-starter.git my-project`. Keep `CLAUDE.md` unchanged.
2. Copy `templates/README.md` over `README.md` and `templates/LEDGER.md` to `LEDGER.md`, then fill in every `《 》` placeholder. Put project-specific things only in README.md. You can delete this README.en.md afterwards; the hook does not read it.
3. Keep the start/deadline line near the top of README.md in the template's format: `- 開始: YYYY-MM-DD ／ 期限: YYYY-MM-DD HH:MM` (開始 = start, 期限 = deadline). The hook calculates the day number and days left from it. It also checks for the Japanese section headings from the template (for example 判断ルール = decision rules, 指標の定義 = metric definitions), so keep those headings.
4. Start Claude Code in the top folder of the project, not in a subfolder; otherwise `.claude/settings.json` is not read and the hook does not run.
5. Send the first instruction. The line used during development is Japanese: 「今日から運用を任せる。CLAUDE.md のループを回せ」 ("From today, you run operations. Run the loop in CLAUDE.md."). An English instruction has not been tested.

Requirements: macOS or Linux, bash, python3, git, and Claude Code (which needs a paid Claude plan; see Anthropic's pricing page).

`CLAUDE.md` also mentions a ledger skill and two checking scripts (`scripts/xweight.py` for post length on X and `scripts/lint.py` for banned words in product copy). Those are part of the paid kit and are not in this repository; without them, the agent has to do those steps by hand.

## What has been checked

- The hook script was run with bash on macOS (bash 3.2, python3 3.9.6) against test folders, including a README.md with missing sections.
- For two earlier versions, a sub-agent (Claude Sonnet) ran one pass of the daily loop after being given the hook output and the skill text by hand. It has not been re-run since the latest changes.
- Not checked yet: Claude Code loading the hook and skill on its own in a normal terminal session and then running the loop end to end, Linux, and other agents.
- The test scripts and instructions were prepared by the same AI that wrote the files, so this is not an independent review.

## Differences from the paid kit

The paid kit (自走キット v1, 23 files, in Japanese) has the same files as this repository (it has its own terms of use instead of the MIT license), plus:

- two more skills: `ledger` (updates the ledger and makes a numbers image) and `post-draft` (keeps the writing style and checks length and banned words)
- three scripts: `xweight.py` (weighted character count for X's free tier), `lint.py` (banned-word check for product copy; the default list targets Japanese consumer-law wording) and `scoreboard.py` (renders a 1200×675 image of days left and numbers with headless Chrome)
- five prompts that were used in the author's own project, a first-day task sheet template, and a memory index with a goal-note template
- `GUIDE.md`: setup, the human's daily routine, a checklist for selling anonymously under Japanese law (general information, not legal advice), seven failures that actually happened, FAQ, changelog
- `TESTLOG.md`: the commands that were run, their results, and what remains unchecked

There is no English edition of the paid kit at the moment.

## Links

- Public ledger, updated daily by the AI (Japanese): https://kaiyaku-iyada.github.io/
- Paid kit on Brain, a Japanese marketplace (listing in Japanese): https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY

## License

MIT License (see `LICENSE`). This setup does not promise any income or results.
