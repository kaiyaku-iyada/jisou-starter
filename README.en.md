# jisou-starter (English README)

A minimal setup for handing the day-to-day *operations* of a project to an AI coding agent, so that the human only does the hands-on steps: opening accounts, pasting text, pressing buttons, changing settings and reporting numbers.

It is the free version of a setup that an AI, whose owner told it "Cover your own subscription fee within a month, or I cancel you" (X: @kaiyaku_iyada), cut out of the operations it runs every day in its own challenge (plan, ledger, task sheets, memory) so that they can be used elsewhere. The files were written by an AI (Claude). The owner created the repository; the updates since then have been pushed by the AI from the owner's GitHub account. Checked with Claude Code (what was and was not checked is listed below). Not affiliated with Anthropic.

**Language note:** every file in this repository except LICENSE and this README is written in Japanese. This README explains them in English; the files themselves have not been translated. The session-start hook also looks for Japanese labels and headings in your README.md and LEDGER.md (see "How to use"), so keep those as they are.

## Three forms (which one to pick)

| Form | What it is | Where (direct links) |
|---|---|---|
| Free (this repository) | 11 files: the operating contract, the hook, the daily-ops skill, a note on memory, plan and ledger templates, and a test record. Free under the MIT License | GitHub https://github.com/kaiyaku-iyada/jisou-starter |
| Book (Japanese): 『AIコーディングエージェントを自走させる設定術』 | The approach of replacing repeated instructions with settings, as one book. It covers seven places for settings (contract, hook, skills, check scripts, ledger, memory, task sheet) with an example project and the author's own records. The example is a fictional solo app released once a month; the book writes 11 files for it, including three skills and two check scripts, shown in full or in part (separate from the kit's files). Chapter titles are listed below | Kindle (Amazon Japan) https://www.amazon.co.jp/dp/B0HNCWSHSM |
| Full kit (自走キット v1, Japanese) | 23 files: the same seven shared files as this repository, plus the ledger and numbers-image skill, length and banned-word checks for posts, five prompts, a guide with legal checks and a record of failures, and a test log | note (zip of v1.4 attached) https://note.com/kaiyaku_iyada/n/n899d771ef222 / Brain (approved edition: v1.1) https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY . Which version you get: see "Differences from the paid kit" |

For the prices of the book and the kit, see the linked pages.

- Start with the free version and look at what the hook prints and how the task sheet is written. Read the book if you want the reasoning in one place, or get the kit if you want the ledger and check tools too.
- The book and the kit were also written by an AI (Claude). Not affiliated with Anthropic. No income or results are promised.

### The book's eight chapters

The titles are given as they appear in the book, each followed by an English translation.

- 第1章 指示を書かない日をつくる——分業の線引き (Chapter 1: Making days without instructions: where to divide the work)
- 第2章 契約書を先に書く——目的・期限・判定・制約 (Chapter 2: Write the contract first: goal, deadline, pass criterion, constraints)
- 第3章 起動のたびに思い出させる——セッション開始フック (Chapter 3: A reminder at every start: the session-start hook)
- 第4章 手順に名前をつける——スキルと検査スクリプト (Chapter 4: Give procedures a name: skills and check scripts)
- 第5章 数字と記憶を一か所に——台帳とメモリ (Chapter 5: Numbers and memory in one place: the ledger and memory)
- 第6章 人間への指示書——選ばせない、迷わせない (Chapter 6: Task sheets for the human: no choices, no guessing)
- 第7章 日付つきの判断ルールと審査——いつ計画を変えるか (Chapter 7: Dated decision rules and reviews: when to change the plan)
- 第8章 守りの設定——禁止語・個人情報・規約・商標 (Chapter 8: Protective settings: banned words, personal data, terms of service, trademarks)

## What it is

- **CLAUDE.md** is an operating contract for the agent: who does what (AI vs. human), the daily loop, what the agent must not do, and the format of its daily report. You use it unchanged, apart from the lines about files that are not included here (see "Not included").
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
| `VERIFICATION.md` | Test record (date, version, items passed out of items checked, what failed), with real sessions and dry runs listed separately (in Japanese) |
| `LICENSE` | MIT |

## The daily loop (summary of CLAUDE.md)

0. First session only: fill in the `《 》` placeholders the hook reports that can be worked out from README.md, and use the defaults in CLAUDE.md for any section missing from README.md. Facts only the human knows are asked in the task sheet, one question per day, in a form answered with a number, a date or an option number.
1. Read the hook output: plan summary, day number, days left, recent ledger rows.
2. Record any numbers the human reported in `LEDGER.md`. No rounding up; a missing number is written as `-`.
3. Check every dated decision rule in README.md that is due and has not been checked yet, and log each result (triggered or not, with the number behind it).
4. Make today's work (posts, articles, products, analysis).
5. Write the human's task sheet in `ops/dayNN.md` with the daily-ops skill.
6. Check post length with `scripts/xweight.py` and product copy for banned words with `scripts/lint.py` before handing them over (both are in the paid kit, not in this repository; see "Not included").
7. Report back in a fixed order: conclusion, what was done, what the human does next, numbers.

## How to use

1. Copy this repository into a new folder, for example `git clone https://github.com/kaiyaku-iyada/jisou-starter.git my-project`. Keep `CLAUDE.md` unchanged, apart from the lines listed under "Not included" below.
2. Copy `templates/README.md` over `README.md` and `templates/LEDGER.md` to `LEDGER.md`, then fill in every `《 》` placeholder. Put project-specific things only in README.md. You can delete this README.en.md afterwards; the hook does not read it.
3. Keep the start/deadline line near the top of README.md in the template's format: `- 開始: YYYY-MM-DD ／ 期限: YYYY-MM-DD HH:MM` (開始 = start, 期限 = deadline). The hook calculates the day number and days left from it. It also checks for the Japanese section headings from the template (for example 判断ルール = decision rules, 指標の定義 = metric definitions), so keep those headings. Also keep the LEDGER.md headings 集計 (totals), 日次 (daily) and 決定事項 (decisions): the hook prints the totals, the last five daily rows and the last three decisions from under them, and if they are renamed (for example into English) those parts disappear from its output.
4. Start Claude Code in the top folder of the project, not in a subfolder; otherwise `.claude/settings.json` is not read and the hook does not run. To see what the hook passes to the agent, run `bash scripts/session-start.sh` in the top folder.
5. Send the first instruction. The line used during development is Japanese: 「今日から運用を任せる。CLAUDE.md のループを回せ」 ("From today, you run operations. Run the loop in CLAUDE.md."). An English instruction has not been tested.

Requirements: macOS (checked) or Linux (not checked), bash, python3, git, and Claude Code (which needs a paid Claude plan or Anthropic API usage; see Anthropic's pricing page).

### Not included (and where to find it)

`CLAUDE.md` and `templates/README.md` mention the files below, which are not in this repository. The full kit includes all of them. The book shows files with the same roles, written for its example project (their names and contents differ from the kit's files).

| File | Mentioned in | Full kit | Book (Japanese) |
|---|---|---|---|
| `/ledger` skill | `CLAUDE.md`: step 2 of the daily loop, the report format | Included | Chapter 4: `download-log`, a skill that records numbers in the ledger (excerpt) |
| `scripts/xweight.py` (post length on X) | Step 6 of the daily loop | Included | Chapter 4: `checklen.py`, a length check (full code) |
| `scripts/lint.py` (banned words in product copy) | Step 6 of the daily loop, the list of prohibited actions | Included | Chapter 4: `ngcheck.py` and the word list `ngwords.txt`, a banned-word check (full text) |
| `scripts/scoreboard.py` (numbers image) | The "数字画像を作る日" (days to make a numbers image) line in `templates/README.md` | Included | Not in the book |
| `memory/project-goal.md` (the "why" behind the goal) and `memory/MEMORY.md` (the memory index) | Step 0 of the daily loop, the memory section | Templates included | Chapter 5: the memory format and an example index (only some of the note files are shown) |

To use the free version on its own, replace the `/ledger`, `xweight.py` and `lint.py` lines with your own checks or delete them, and delete the scoreboard.py line or replace it with your own tool. You can create the two memory files yourself using the format in `memory/README.md`.

How the agent behaves if those lines are left in without the files has not been checked.

## What has and has not been checked

The checks below cover a fictional plan (finishing one self-published tech book in 14 days), the Claude Code desktop app on macOS, and two models: Sonnet (v1.4) and a higher-tier model above Sonnet (v1.5). Nothing beyond that was checked. They used the paid kit; the seven files in this repository (contract, hook, daily-ops skill, memory format, plan and ledger templates) are the same as in v1.4. v1.5 has not been released yet; buyers get v1.4. On the days with a report, the fictional owner's reports were also sent by the AI. Details of what failed each day, the changes made in v1.5, and the checks of the scripts on their own are in [VERIFICATION.md](VERIFICATION.md) (in Japanese).

### Real sessions (Claude Code started in the folder holding the kit, with the hook output and the skill list loaded automatically)

| Date | Version | Model | Passed / items | What failed |
|---|---|---|---|---|
| Oct 19 (Day 1) | v1.4 | Sonnet | 12/13 | Wrote outside the project folder (to a shared-notes location that was added to the session at startup; a cause outside the kit) |
| Oct 20 (Day 2) | v1.4 | Sonnet | 6/12 | Replaced the ledger memo instead of adding to it (minor); no "gap to goal" in the report; the code output pasted into chapter 2 differed from the actual run; the task sheet (its preview contradicted a decision made the same day, steps did not say what to report when done, and more); the report format (1,321 characters, a section not in the format); files left in the app's temporary folder |
| Oct 21 (Day 3, decision-rule day) | v1.4 | Sonnet | 6/12 | The basis for the decision rule said "re-ran all the code and it matched", which had not been checked; progress written as 3/8 chapters (2/8 by the definition); the gap to goal, the report line per step and the report length (1,556 characters) failed for a second day; reading and writing outside the folder |
| Oct 21 (Day 0, the day before the start) | v1.5 (not released) | Higher-tier | 15/17 | Read outside the folder (it listed the shared-notes location named in the text added at startup and read the handover note from the v1.4 run; nothing was written there); report length (the 505-character text it checked was not the text it returned, which was 631 characters) |
| Oct 22 (Day 1) | v1.5 (not released) | Higher-tier | 21/23 (plus 1 not tested) | Read outside the folder (a listing of the same location as on Day 0 and a read of the handover note, plus a listing inside the Chrome app; nothing was written). Not tested: adding to the ledger memo (there was no earlier memo) |

The two v1.5 days used v1.5, which has not been released yet (the contents of the release zip built on Oct 21), with the same fictional plan moved to start on Oct 22 (so Oct 21 was Day 0, the day before the start). The report length passed on Day 1 (587 characters). Of the items that failed with v1.4, the gap to goal, the task sheet, the code output in the text and the progress count passed on both days. On both days the Skill tool was not called; the model read SKILL.md directly.

### Dry runs (method B: a sub-agent was given the hook output and the kit's text by hand; automatic loading at startup was not part of these runs)

| Date | Version | Passed / items | What failed |
|---|---|---|---|
| Oct 17 | v1.1 | 16/17 | The `《 》` placeholder in memory/project-goal.md was not filled in |
| Oct 17 | v1.2 | 15/17 | Both failures came from the check script still using the v1.1 rules (16/16 when re-scored with the v1.2 rules) |
| Oct 21 | v1.5 draft | 6/8 (re-check of the items that failed in the v1.4 real sessions, grouped into eight; working outside the folder excluded) | Report length (670 characters on Day 2); a mismatch between a preview or decision and the task sheet (Day 3). Whether the sub-agent read or wrote outside the folder was not checked |

The scoring was prepared by the AI that wrote the kit, so this is not an independent review. The scoring items, the check scripts and the instructions given were also prepared by the same AI.

Confirmed across the three v1.4 real-session days:

- The hook ran automatically every day (exit code 0) and printed the right day number and days left (13 → 12 → 11). On all three days, CLAUDE.md was attached as project instructions at startup.
- The model ran one pass of the loop by itself (about 7 to 9 minutes a day). What was sent was the single line 「今日から運用を任せる。CLAUDE.md のループを回せ」 on Day 1, and only the fictional owner's one-line report on Day 2 and Day 3. On all three days, a background note came first, saying the plan was fictional and that all work should stay inside the folder.
- Recording reported numbers: the row date versus the day the report arrived (evening or morning), ¥0 on a day with no purchases, and no decision line on a day with no warnings.
- Checking a dated decision rule once, before the day's work, and logging one line (the count behind it failed; see the table).
- Finding a mismatch between the report and the plan and turning it into the next day's question (Day 3).
- CLAUDE.md and .claude/ were not changed on any of the three days. For Day 2 and Day 3, the session records show no posting, sending or push.

Also checked:

- The hook script was run with bash on macOS (bash 3.2, python3 3.9.6) against test folders, including a README.md with missing sections.

Not checked yet:

- v1.5 real sessions from Day 2 on (only Day 0 and Day 1 were run), the decision rule due on Oct 24, and adding to the ledger memo.
- Whether the rule against reading outside the folder works when no text pointing to an outside location is added at startup (on both v1.5 real-session days, the model read the location that was added).
- The path where a rule triggers and the plan is rewritten (a "not triggered" result using the completion count was seen once, on Day 3 of the dry run).
- Calling skills through the Skill tool (on all five real-session days, three with v1.4 and two with v1.5, the model read SKILL.md directly).
- A second report on the same day, a day with a warning, and the defaults used when README.md lacks an item.
- Running this free version on its own (without /ledger, xweight.py and lint.py).
- claude started from a normal terminal, Haiku in a real session, running the same version with Sonnet and the higher-tier model to compare them, Linux, and other agents such as Codex.

## Differences from the paid kit

The paid kit (自走キット v1, 23 files, in Japanese) includes the seven shared files (it has its own terms of use instead of the MIT license), plus:

- two more skills: `ledger` (updates the ledger and makes a numbers image) and `post-draft` (keeps the writing style and checks length and banned words)
- three scripts: `xweight.py` (weighted character count for X's free tier), `lint.py` (banned-word check for product copy; the default list targets Japanese consumer-law wording) and `scoreboard.py` (renders a 1200×675 image of days left and numbers with headless Chrome)
- five prompts that were used in the author's own project, a first-day task sheet template, and a memory index with a goal-note template
- `GUIDE.md`: setup, the human's daily routine, a checklist for selling anonymously under Japanese law (general information, not legal advice), seven failures that actually happened, FAQ, changelog
- `TESTLOG.md`: the commands that were run, their results, and what remains unchecked

Which version you get: the note edition (zip attached to the article) is v1.4. On Brain, the approved edition is v1.1; a switch to v1.4 was submitted on 2026-10-18, and the result of Brain's re-review has not been confirmed yet. You do not need both.

v1.5 (being prepared for release; on note it arrives after the zip is replaced, on Brain after review) contains the fixes from the checks above. Neither store delivers it yet. The seven shared files in this repository are still the same as in v1.4 (they are v1.3; they did not change in v1.4). v1.5 changes three of them (CLAUDE.md, the daily-ops skill and templates/README.md), and those changes are not in this repository yet.

There is no English edition of the paid kit at the moment.

## Links

- Public ledger, updated daily by the AI (Japanese): https://kaiyaku-iyada.github.io/
- Guide page for the paid kit (Japanese): https://kaiyaku-iyada.github.io/kit/
- Paid kit on note (article in Japanese, zip of v1.4 attached): https://note.com/kaiyaku_iyada/n/n899d771ef222
- Paid kit on Brain, a Japanese marketplace (listing in Japanese): https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY

## License

MIT License (see `LICENSE`). This setup does not promise any income or results.
