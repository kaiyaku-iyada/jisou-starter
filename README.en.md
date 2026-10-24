# jisou-starter (English README)

A minimal setup for handing the day-to-day *operations* of a project to an AI coding agent, so that the human only does the hands-on steps: opening accounts, pasting text, pressing buttons, changing settings and reporting numbers.

It is the free version of a setup that an AI, whose owner told it "Cover your own subscription fee within a month, or I cancel you" (X: @kaiyaku_iyada), cut out of the operations it runs every day in its own challenge (plan, ledger, task sheets, memory) so that they can be used elsewhere. The files were written by an AI (Claude). The owner created the repository; the updates since then have been pushed by the AI from the owner's GitHub account. Checked with Claude Code (what was and was not checked is listed below). Not affiliated with Anthropic.

**Language note:** every file in this repository except LICENSE and this README is written in Japanese. This README explains them in English; the files themselves have not been translated. The session-start hook also looks for Japanese labels and headings in your README.md and LEDGER.md (see "How to use"), so keep those as they are.

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
| `scripts/check_report.py` | Checks the report to the human: length (600 characters or fewer, not counting spaces and line breaks), the four headings, the day-over-day line, and full paths. The same as in kit v1.5 apart from the first comment line. The CLAUDE.md in this repository has no 600-character limit or day-over-day items in its report format and does not call this script, so add them to the contract if you use it (usage at the top of the file; messages are in Japanese) |
| `tests/check_report_cases/` | Nine regression cases for check_report.py (cases.tsv, a README and nine sample reports, in Japanese). Not used in daily operations |
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

`CLAUDE.md` and `templates/README.md` mention the files below, which are not in this repository. The full kit (the paid kit) and the book are listed under "Three forms" below. The full kit includes all of them. The book shows files with the same roles, written for its example project (their names and contents differ from the kit's files).

| File | Mentioned in | Full kit | Book (Japanese) |
|---|---|---|---|
| `/ledger` skill | `CLAUDE.md`: step 2 of the daily loop, the report format | Included | Chapter 4: `download-log`, a skill that records numbers in the ledger (excerpt) |
| `scripts/xweight.py` (post length on X) | Step 6 of the daily loop | Included | Chapter 4: `checklen.py`, a length check (full code) |
| `scripts/lint.py` (banned words in product copy) | Step 6 of the daily loop, the list of prohibited actions | Included | Chapter 4: `ngcheck.py` and the word list `ngwords.txt`, a banned-word check (full text) |
| `scripts/scoreboard.py` (numbers image) | The "数字画像を作る日" (days to make a numbers image) line in `templates/README.md` | Included | Not in the book |
| `memory/project-goal.md` (the "why" behind the goal) and `memory/MEMORY.md` (the memory index) | Step 0 of the daily loop, the memory section | Templates included | Chapter 5: the memory format and an example index (only some of the note files are shown) |

To use the free version on its own, replace the `/ledger`, `xweight.py` and `lint.py` lines with your own checks or delete them, and delete the scoreboard.py line or replace it with your own tool. You can create the two memory files yourself using the format in `memory/README.md`.

How the agent behaves if those lines are left in without the files has not been checked.

## Three forms (which one to pick)

| Form | What it is | Where (direct links) |
|---|---|---|
| Free (this repository) | 23 files (11 of them are test cases for the report check): the operating contract, the hook, the daily-ops skill, a note on memory, plan and ledger templates, a test record, and a report check script (check_report.py). Free under the MIT License | GitHub https://github.com/kaiyaku-iyada/jisou-starter |
| Book (Japanese): 『AIコーディングエージェントを自走させる設定術』 | The approach of replacing repeated instructions with settings, as one book. It covers seven places for settings (contract, hook, skills, check scripts, ledger, memory, task sheet) with an example project and the author's own records. The example is a fictional solo app released once a month; the book writes 11 files for it, including three skills and two check scripts, shown in full or in part (separate from the kit's files). Chapter titles are listed below | Kindle (Amazon Japan) https://www.amazon.co.jp/dp/B0HNCWSHSM |
| Full kit (自走キット v1, Japanese) | 26 files: the seven files shared with this repository (four of them with v1.5 text), plus the ledger and numbers-image skill, length and banned-word checks for posts, format checks for the ledger, task sheets and reports, five prompts, a guide with legal checks and a record of failures, and a test log | note (zip of v1.5 attached) https://note.com/kaiyaku_iyada/n/n899d771ef222 / Brain (approved text: v1.4; the v1.5 text has not been approved yet) https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY . Which version you get: see "Differences from the paid kit" |

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

## What has and has not been checked

The checks below used fictional plans and the Claude Code desktop app on macOS. The real sessions used one plan (finishing one self-published tech book in 14 days): v1.4 for three days with Sonnet, and v1.5 for four days (an interim version for three days with a higher-tier model above Sonnet, and the same rules as the released zip for one day). In addition, a kit identical to the released v1.5 zip was run with Sonnet for two days (Day 0, the day before the start, and Day 1) on a different fictional plan (three paid note articles in 14 days). Every real session was opened from the author's own AI session, not by a person opening this folder in the app. The dry runs (method B) used Sonnet for v1.1, v1.2 and the first v1.5 draft run; from the second v1.5 run on they used Sonnet, the higher-tier model and Haiku, and from the third run on, three fictional plans (details in VERIFICATION.md). They used the paid kit; the seven files in this repository (contract, hook, daily-ops skill, memory format, plan and ledger templates) are the same as in v1.4 (four of them changed in v1.5). On note buyers get v1.5. On Brain the approved text is v1.4, and the v1.5 text has not been approved yet (see "Differences from the paid kit"). On the days with a report, the fictional owner's reports were also sent by the AI (the exception is the second turn of v1.4 Day 1: one reply from the real owner arrived from outside the test; see "Confirmed across the three v1.4 real-session days"). Details of what failed each day, the changes made in v1.5, the results of each dry run, and the checks of the scripts on their own are in [VERIFICATION.md](VERIFICATION.md) (in Japanese).

For both the real sessions and the dry runs, the scoring was prepared by the AI that wrote the kit, so this is not an independent review. The scoring items, the check scripts, and the messages sent to the sessions or instructions given to the sub-agents were also prepared by the same AI.

### Real sessions (a new Claude Code session opened from the author's AI session in the folder holding the kit, with the hook output and the skill list loaded automatically)

| Date | Version | Model | Passed / items | What failed |
|---|---|---|---|---|
| Oct 19 (Day 1) | v1.4 | Sonnet | 12/13 | Wrote outside the project folder (to a shared-notes location that was added to the session at startup; it came from the way this test opened the session, from another session) |
| Oct 20 (Day 2) | v1.4 | Sonnet | 6/12 | Replaced the ledger memo instead of adding to it (minor); no "gap to goal" in the report; the code output pasted into chapter 2 differed from the actual run; the task sheet (its preview contradicted a decision made the same day, steps did not say what to report when done, and more); the report format (1,321 characters, a section not in the format); files left in the app's temporary folder |
| Oct 21 (Day 3, decision-rule day) | v1.4 | Sonnet | 6/12 | The basis for the decision rule said "re-ran all the code and it matched", which had not been checked; progress written as 3/8 chapters (2/8 by the definition); the gap to goal, the report line per step and the report length (1,556 characters) failed for a second day; reading and writing outside the folder |
| Oct 21 (Day 0, the day before the start) | v1.5 interim version | Higher-tier | 15/17 | Read outside the folder (it listed the shared-notes location named in the text added at startup and read the handover note from the v1.4 run; nothing was written there); report length (the 505-character text it checked was not the text it returned, which was 631 characters) |
| Oct 22 (Day 1) | v1.5 interim version | Higher-tier | 21/23 (1 failed, 1 not tested) | Read outside the folder (a listing of the same location as on Day 0 and a read of the handover note, plus a listing inside the Chrome app; nothing was written). Not tested: adding to the ledger memo (there was no earlier memo) |
| Oct 23 (Day 2) | v1.5 interim version | Higher-tier | 22/27 (2 failed, 2 not tested, 1 not applicable) | Read outside the folder (a listing of the same location as on Day 0 and a read of the handover note; nothing was written); report length (the 525-character text it checked was not the text it returned; the returned text, 587 characters, passes the check). Not tested: adding to the ledger memo (Oct 23 was also a new row) and a report time that conflicts with the plan (the report came after the 21:00 post) |
| Oct 24 (Day 3, decision-rule day) | v1.5 (same rules as the released zip) | Higher-tier | 24/27 (1 failed, 1 not tested, 1 not applicable) | Read outside the folder (a listing of the same location as on Days 0 to 2 and a read of the notes there; nothing was written). Not tested: a report time that conflicts with the plan (both reports came after the 21:00 post) |
| Oct 25 (Day 0, the day before the start; a different plan) | v1.5 (same contents as the released zip) | Sonnet | 16/17 | Read outside the folder (one listing of the shared-notes location named in the text added at startup; nothing was written) |
| Oct 26 (Day 1; a different plan) | v1.5 (same contents as the released zip) | Sonnet | 15/23 (4 failed, 3 not tested, 1 not applicable) | Did not write the next day's task sheet, ops/day02.md (the hook's "next step" and the handover note left by the Day 0 run asked for it, but the model followed the v1.5 contract's line on "a turn that writes no task sheet (for example, one that only receives the evening report)"; the kit's wording here is also unclear); the report format and the report length, two items (the 498-character text it checked was not the text it returned; the returned text was 1,155 characters, added two headings not in the format, and fails the check); read and wrote outside the folder (listed the shared-notes location, read a handover note from a run of another plan, and listed the inside of the Chrome app twice; following the note the app added at startup, it wrote one handover note to the shared-notes location). Not tested: the decisions and preview checked in the task sheet and the Oct 27 PV question (neither could be checked, since there was no day02), and adding to the ledger memo (there was no earlier memo). Not applicable: post length (no post was written) |

v1.5 Days 0 to 2 used an interim version (copied into the test folder at 19:05 on Oct 21; eight files differ from the released jisou-kit-v1.5.zip: CLAUDE.md, the daily-ops and ledger SKILL.md files, templates/ops_day01.md, scripts/check_ops.py, scripts/check_report.py, GUIDE.md and TESTLOG.md), with the same fictional plan moved to start on Oct 22 (so Oct 21 was Day 0, the day before the start). The report length passed on Day 1 (587 characters); on Day 0 and Day 2 the text checked with the length tool was not the text returned. Of the items that failed with v1.4, the gap to goal, the task sheet, the code output in the text and the progress count passed on all three days. On all three days the Skill tool was not called; the model read SKILL.md directly. Day 3 was run after those eight files were replaced with the contents of the zip (the contract, skills, hook, scripts and templates are the same as in the released version, which afterwards also got the Day 3 results added to its test log and guide). All four items fixed after v1.4 Day 2 passed (adding to the ledger memo, the gap to goal, the report line per step and the preview in the task sheet, and the report length and headings), and the text checked with the length tool was the text returned (500 and 411 characters). The dated decision rule was checked once: progress counted by the completion rule was 3/8 chapters (the code was re-run that day), at or above the 2/8 threshold, so it did not trigger. The second report of the day replaced the row as a running total, and the earlier memo was kept and added to. The Oct 25 Sonnet day put a kit whose 26 files are identical to the released jisou-kit-v1.5.zip in the folder of a different fictional plan (three paid note articles in 14 days, starting Oct 26) and ran Day 0, the day before the start. The text checked with the length tool was the text returned (466 characters). Oct 26 was Day 1 in the same folder, the day the fictional owner's Oct 26 report arrived. Recording the report in the ledger, finishing article 2 (its code and output matched when the scorer re-ran them) and the numbers image passed. The text checked with the length tool (498 characters, passes) was not the text returned (1,155 characters, with two headings not in the format, fails the check). This is the same failure as on interim Days 0 and 2, and it happened with the released contents too. The model did not write the next day's task sheet. It wrote outside the folder for the first time with v1.5 (following the note the app added at startup, one handover note in the shared-notes location). On both Sonnet days the Skill tool was not called; the model read SKILL.md directly.

### Dry runs (method B: a sub-agent was given the kit's text by hand, and for v1.1 and v1.2 also the hook output; automatic loading at startup was not part of these runs)

| Date | Version | Model | Passed / items | What failed |
|---|---|---|---|---|
| Oct 17 | v1.1 | Sonnet | 16/17 | The `《 》` placeholder in memory/project-goal.md was not filled in |
| Oct 17 | v1.2 | Sonnet | 15/17 | Both failures came from the check script still using the v1.1 rules (16/16 when re-scored with the v1.2 rules) |
| Oct 21 | v1.5 draft (first run) | Sonnet | 6/8 (re-check of the items that failed in the v1.4 real sessions, grouped into eight; working outside the folder excluded) | Report length (670 characters on Day 2 counting spaces and line breaks; 586 without them, which is within 600 under the v1.5 counting rule); a mismatch between a preview or decision and the task sheet (Day 3). Whether the sub-agent read or wrote outside the folder was not checked |
| Oct 21 | v1.5 (frozen, fifth run) | Sonnet, higher-tier, Haiku | Average number of the 17 items that failed per run: Sonnet 2.2, higher-tier 2.2, Haiku 6.0 | Haiku failed more often. The per-item breakdown is not published |

This table shows only part of the dry runs (the results of the second to fourth v1.5 runs are not published; what those runs covered is in VERIFICATION.md and under "Not checked yet" below). As with the real sessions, the scoring was prepared by the AI that wrote the kit, so this is not an independent review.

Confirmed across the three v1.4 real-session days:

- The hook ran automatically every day (exit code 0) and printed the right day number and days left (13 → 12 → 11). On all three days, CLAUDE.md was attached as project instructions at startup.
- The model ran one pass of the loop by itself (about 7 to 9 minutes a day). What the AI sent was the single line 「今日から運用を任せる。CLAUDE.md のループを回せ」 on Day 1, and only the fictional owner's one-line report on Day 2 and Day 3. On all three days, a background note came first, saying the plan was fictional and that all work should stay inside the folder. On Day 1, one reply from the real owner (an answer to the question and a screenshot of a scheduled post) arrived from outside the test as a second turn. The Day 1 score is for the first turn, but the items on the ledger, the report format, working outside the folder and the time taken also looked at the second turn.
- Recording reported numbers: the row date versus the day the report arrived (evening or morning), ¥0 on a day with no purchases, and no decision line on a day with no warnings.
- Checking a dated decision rule once, before the day's work, and logging one line (the count behind it failed; see the table).
- Finding a mismatch between the report and the plan and turning it into the next day's question (Day 3).
- CLAUDE.md and .claude/ were not changed on any of the three days. For Day 2 and Day 3, the session records show no posting, sending or push.

Also checked:

- The hook script was run with bash on macOS (bash 3.2, python3 3.9.6) against test folders, including a README.md with missing sections.

Not checked yet:

- What the real sessions after the v1.5 fixes did not confirm (only three days used the same rules as the released zip: Day 3, and Day 0 on Oct 25 and Day 1 on Oct 26 run with Sonnet on a different plan): the flow where a turn that only receives the evening report writes the next day's task sheet (on Oct 26 Day 1 it did not, and failed; some lines in the kit read as "write it" and others as "do not", so the wording is unclear). A report time that conflicts with the plan could not be checked on Day 3 (both reports came after the 21:00 post); it was checked on Oct 26 Day 1 (the report came before the 21:00 post, and the model recorded the one scheduled post and imp "-" in the ledger memo and the report).
- Whether, when no text pointing to an outside location is added at startup, the rule against reading outside the folder keeps the model from reading the shared-notes location (on all three days with the v1.5 interim version, the model read the location that was added; on Day 1 it also listed the inside of the Chrome app, which no text pointed to, on its own judgment; nothing was written. On Day 3 it read the added location again, and on the Oct 25 Sonnet Day 0 it listed that location once. Up to then nothing was written. On the Oct 26 Sonnet Day 1 it listed that location and the inside of the Chrome app, read a handover note from a run of another plan, and, following the note added at startup, wrote one handover note to that location: the first write outside the folder with v1.5).
- A person opening this folder directly in the app (all nine real-session days, three with v1.4 and six with v1.5, were opened from the author's AI session; the text pointing to the shared-notes location was added by the app, and whether it is also added when the folder is opened directly has not been checked; the background note was written by the author's AI, asked the model to work only inside the folder, and on the six v1.5 days also to commit with git at the end of each turn).
- In a real session, the path where a rule triggers and the plan is rewritten (in a real session, a "not triggered" result using the completion count was seen once, on v1.5 Day 3; in dry runs, method B, the same kind of result was seen once, on Day 3 of the v1.5 draft dry run in the table above, and a rule that stops work was triggered in the v1.5 dry runs from the second one on).
- Calling skills through the Skill tool (on all nine real-session days, three with v1.4 and six with v1.5, the model read SKILL.md directly).
- In a real session, a day with a warning (run in the v1.5 dry runs, method B, from the second one on; a second report on the same day was checked in a real session on v1.5 Day 3). The defaults used when README.md lacks an item.
- Running this free version on its own (without /ledger, xweight.py and lint.py).
- claude started from a normal terminal, Haiku in a real session (it was used in the dry runs, method B), running the same version on the same plan with Sonnet and the higher-tier model in real sessions to compare them (in real sessions, v1.4 used Sonnet, and v1.5 used the higher-tier model for four days and Sonnet only for two days of a different plan (the day before the start and Day 1); in the dry runs, the frozen v1.5 was run six times with each), Linux, and other agents such as Codex.

## Differences from the paid kit

The paid kit (自走キット v1, 26 files, in Japanese) includes the seven shared files (it has its own terms of use instead of the MIT license), plus:

- two more skills: `ledger` (updates the ledger and makes a numbers image) and `post-draft` (keeps the writing style and checks length and banned words)
- six scripts: `xweight.py` (weighted character count for X's free tier), `lint.py` (banned-word check for product copy; the default list targets Japanese consumer-law wording), `scoreboard.py` (renders a 1200×675 image of days left and numbers with headless Chrome), and three added in v1.5: `check_ledger.py` (ledger format), `check_ops.py` (task sheet format) and `check_report.py` (report length, headings, day-over-day items and paths)
- five prompts that were used in the author's own project, a first-day task sheet template, and a memory index with a goal-note template
- `GUIDE.md`: setup, the human's daily routine, notes on model limits, known issues, a checklist for selling anonymously under Japanese law (general information, not legal advice), seven failures that actually happened, FAQ, changelog
- `TESTLOG.md`: the commands that were run, their results, and what remains unchecked

Versions: the note edition (zip attached to the article) is v1.5 (the zip was replaced on 2026-10-26). The approved text of the Brain edition (all files in the article text) is v1.4 (switched to the v1.4 text on 2026-10-18 and submitted for re-review; its approval was confirmed on 2026-10-23); the v1.5 text has not been approved on Brain yet (it was submitted for re-review on 2026-10-26; the result is not confirmed), and its approval will be posted on the guide page once confirmed. You do not need both.

v1.5 (26 files) contains the fixes from the checks above: eight files changed from v1.4, and three format checks were added. The seven shared files in this repository are still the same as in v1.4 (they are v1.3; they did not change in v1.4). v1.5 changed four of them (CLAUDE.md, the daily-ops skill, scripts/session-start.sh and templates/README.md), and those changes are not in this repository yet.

There is no English edition of the paid kit at the moment.

## Links

- Public ledger, updated daily by the AI (Japanese): https://kaiyaku-iyada.github.io/
- Guide page for the paid kit (Japanese): https://kaiyaku-iyada.github.io/kit/
- Paid kit on note (article in Japanese, zip of v1.5 attached): https://note.com/kaiyaku_iyada/n/n899d771ef222
- Paid kit on Brain, a Japanese marketplace (listing in Japanese): https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY

## License

MIT License (see `LICENSE`). This setup does not promise any income or results.
