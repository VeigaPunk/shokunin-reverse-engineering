#!/usr/bin/env python3
"""Generate the round-47 v2 wave spec, validated dispatch and ready file (L1 artifact)."""
import collections
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-47")
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
MILE = ("Round 47: verify, attack and falsify the two frozen counters (exactness over craft "
        "block 24; the self-assessment re-derivation) and draft the landing evidence before data")
REPORT = ".ufo/waves/round-47/w1"
W = REPORT + "/"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r47/"

CTX = f"""# Target
kaidoku-shokunin round 47, one v2 wave = verification, drafting and attack of the round's two FROZEN claim instruments, BEFORE any landing. Lane root (absolute): {ROOT}. L1 = KaidokuR47 (integration owner; it holds the canonical section-3 planner seat — the validator rejects `planner` as a swarm role, so bounded planning data-walks ride scout/connector/revenger seats; recorded in the round report). Freeze commit `{FREEZE}` (`plans/round-47-claims.md` + `tools/round-47/`, directory pathspec); base `{BASE}`.

# The two claims (read the claims file, not this prompt)
- R47-C1 depth: `SKILL.md` `## Queue-drain craft` rule block 24, marker `<!-- exactness-table v3 -->`, header `trigger | v2 hole | v3 arm | exit`, exactly four rows (one per R46-CL2, R46-CL3, R46-CL4, R46-CL6), exact arm tokens (`symbol`, `once`, `digest`, `order`), a `mutations_sha256` pin over the counter's own mutation list, a `interpreter_sha256` pin, and a flag-order clause over `tools/round-46/gate.py`. Counter: `tools/round-47/exact.py`.
- R47-C2 calibration: `tools/round-47/record.py` re-derives every machine-checkable atom of the last two `## Round N` sections of `SCORECARD.md` plus the current `## Owned axes` leading fractions, and requires zero mismatches with at least two re-derived corrections.
The claims file is the rule: **`{ROOT}/plans/round-47-claims.md`**. Read it in full before your first command.

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside `{ROOT}/{W}<YourSeatName>/` (create it). Never edit `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command (`add/commit/checkout/reset/switch/pull/push`, `jj commit/new/describe/squash/rebase/abandon/bookmark`). Read-only git is fine: `log`, `show`, `diff`, `diff-tree`, `ls-tree`, `cat-file`, `rev-parse`, `status --porcelain`.
- **Frozen means read-only.** `tools/round-47/` and `plans/round-47-claims.md` are byte-frozen at `{FREEZE}`. Copy to scratch to mutate the copy; never mutate the originals.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, and every later git call names `-C "$D"`. Verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never run `git commit` with a throwaway identity anywhere else.
- **Scratch**: `S={SCRATCH}<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S" HYAKU_SCRATCH="$S"`. Remove `$S` before you yield AFTER copying receipts into your report dir. Never write under `/tmp`; nothing under `/tmp` is citable evidence.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256 and UTC time. A check you did not run is not passed — say "not run".
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate. A 2 never counts toward a target.
- **`Report:` trailer**: the `Report: .ufo/waves/...` path in your prompt is relative to `{ROOT}` — write it at `{ROOT}/<that path>`.
- **Tooling**: read `/home/vgpnk/.omp/agent/RULES.md` before installing anything. **All pacman transactions are PAUSED host-wide** — install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or nothing. Record any install (tool, version, channel, reason) in your report.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, or the fleet repo.

# What the L1 does with your output
It reads your report, reconciles disagreements, lands `SKILL.md` block 24, the `SCORECARD.md` corrections and the record updates, then re-measures both counters at the landing revision. A finding that a FROZEN clause is wrong, vacuous, or satisfiable by a forgery is the most valuable thing you can return: give the exact command, the differing value, and a fixture path that shows it. Do not "fix" frozen bytes.
"""

T = []


def add(name, agent, task):
    T.append({"name": name, "agent": agent,
              "task": GODSPEED + task.replace("<ROOT>", ROOT).replace("<W>", W)
              .replace("<FREEZE>", FREEZE).replace("<BASE>", BASE)})


RUN = ("Run `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/<SEAT> python3 -I -B <ROOT>/tools/round-47/%s "
       "\\\n  --root <ROOT> %s --json-out <W><SEAT>/receipt.json` and record the exit code, the "
       "`failing` list and every value you quote. Write `<W><SEAT>/report.md` with a table.")

# --- C1 executors: clause-by-clause verification --------------------------------

C1_CLAUSES = [
    ("C1Struct", "clauses 1-3", "marker_occurrences == 1, block_present == 1, block is last and "
     "titled `24. `, header exactly `trigger | v2 hole | v3 arm | exit`, rows == 4, 4 cells, "
     "exit cells in {0,1,2}"),
    ("C1Ids", "clause 4", "every row's trigger cell names exactly one `R46-CL<n>` id and the "
     "multiset over the rows is exactly the four ids once each"),
    ("C1Tokens", "clause 5", "every v3-arm cell is exactly one of `symbol`, `once`, `digest`, "
     "`order` — equality, not containment; the round-46 counter's substring hole is closed"),
    ("C1Digest", "clause 6", "`mutations_sha256` equals sha256 over \"\\n\".join(name for name, _ "
     "in the counter's MUTATIONS) and all four mutation names appear in the block"),
    ("C1Order", "clause 7", "`tools/round-46/gate.py` at the measured revision contains "
     "\"-m\", \"--diff-merges=first-parent\" exactly once and the reversed pair zero times"),
    ("C1Refs", "clause 8", "refs >= 3 with line selectors that resolve at --rev, "
     "`corpus/lessons/round-46.md` cited, and both sha256 pins matching the bytes at rev"),
]

for seat, label, text in C1_CLAUSES:
    add(seat, "executor",
        f"Verify R47-C1 {label} on the frozen counter `tools/round-47/exact.py` at freeze "
        f"`<FREEZE>`, then draft the block-24 row(s) that satisfy it.\n\nWhat the clause says: "
        f"{text}.\n\n1. Read `<ROOT>/plans/round-47-claims.md` R47-C1 and the clause in "
        f"`<ROOT>/tools/round-47/exact.py` that computes it; quote both.\n2. At the freeze the "
        f"counter exits 1 with `block_present 0` — record that, then build a CANDIDATE block 24 "
        f"in scratch (a copy of `SKILL.md` in a fixture repo) that satisfies your clause, and show "
        f"the counter's failing list shrinking to only the other clauses. Say exactly which "
        f"clauses remain red and why.\n3. Draft the ready-to-paste table row(s) for block 24 that "
        f"your clause governs into `<W><SEAT>/rows.md`, with the citation line selectors and "
        f"sha256 values you actually computed.\n\n"
        f"{RUN % ('exact.py', '--freeze <FREEZE> --rev <FREEZE>')}")


add("C1Battery", "executor",
    "Build and score the four R47-C1 battery forgeries independently, one row each, and prove the "
    "discrimination claim is not an artefact of the counter's own self-report.\n\n"
    "The four classes: `substring-arm` (a v3-arm cell containing but not equal to a vocabulary "
    "token), `duplicate-routed-id` (five rows, one id twice, all four ids still present), "
    "`stale-mutations-digest` (a digest computed over three of the four mutation names), "
    "`flag-order-drift` (the fixture's `gate.py` copy carries the reversed flag pair).\n\n"
    "For each: build a one-commit fixture repo in scratch from the landed block (copy of "
    "`SKILL.md` + the files its refs name), mutate only that class, and score the fixture with "
    "`--profile v2` and `--profile v3`. Expected: v2 exit 0 (the hole), v3 exit 1 (the fix). If a "
    "class scores differently, that is the finding: give the command and both receipts.\n\n"
    "Write `<W><SEAT>/report.md` with a 4-row table: class | v2 exit | v3 exit | failing clause.")


add("C1SelfTest", "executor",
    "Audit `tools/round-47/exact.py --selftest`: run it, count the cases the code registers "
    "(`case(`/`run(` invocations), and check every case is honest — does the named red case "
    "actually exercise the clause its name claims, and would it stay green if the clause were "
    "deleted? Copy the counter to scratch, delete ONE clause (your choice, name it), and show the "
    "selftest going red for the case that names it. A clause whose deletion no case notices is a "
    "finding.\n\n"
    "Record the banner (`EXACT_SELFTEST: cases=N failures=M`), the registered count, and the "
    "deleted-clause matrix in `<W><SEAT>/report.md`.\n\n"
    "Menu: `HYAKU_SCRATCH=... python3 -I -B <ROOT>/tools/round-47/exact.py --selftest --root "
    "<ROOT> --freeze <FREEZE> --rev <FREEZE>`.")


add("C1FreezeWindow", "executor",
    "Prove the frozen window is empty for the round's own paths: run "
    "`git -C <ROOT> log --name-status --format= -m --diff-merges=first-parent "
    "<FREEZE>..<FREEZE> -- tools/round-47 plans/round-47-claims.md` and, separately, "
    "`<FREEZE>..<tip>` at the current tip; report both outputs and the argument ORDER you used. "
    "Then reorder the flags the other way and report what changes on a two-parent merge fixture "
    "you build in scratch (that is R46-CL6's defect, measured). Write "
    "`<W><SEAT>/report.md` with the four commands, their exit codes and their byte counts.")


# --- C2 executors ---------------------------------------------------------------

C2_KINDS = [
    ("C2Atoms", "enumerate and independently re-derive every atom",
     "Enumerate all atoms `record.py` extracts at `<BASE>` (`--json-out` gives `atoms`, "
     "`atoms_by_class`). For each class pick two atoms and re-derive its value with a command you "
     "write yourself (not the counter's code): dispatch `counts.spawn`, the round-46 window, a "
     "`.ufo/waves/` path, a backticked commit, the coverage map count and command A's citation "
     "count. Report disagreements only; then confirm the counter's four mismatches."),
    ("C2Mismatch", "verify the four before-mismatches are real",
     "For each of the four mismatches the counter reports at `<BASE>` (round-45 seat atom, "
     "round-46 window atom, coverage row, depth row) re-derive the truth with your own commands "
     "and say whether the counter is right. A false mismatch is a finding: name the command and "
     "the value."),
    ("C2Corrections", "draft the correction lines",
     "Draft the `## Record corrections — round 47` section text: a `seats` correction stating the "
     "correct wave count and seat total for round 45, a `window` correction stating a concrete "
     "window you have run yourself and found empty for the round-46 paths, plus the one-line "
     "statement for each of the coverage and depth rows' current values (those rows are updated in "
     "place, so state them as facts with their counting command). Imitate the exact grammar the "
     "counter parses (`- corrects seats <round>: <n> waves, <total> seats total`; "
     "`- corrects window <round>: empty in <a>..<b> -- <paths>`) and prove each line re-derives by "
     "building a scratch copy of `SCORECARD.md` with your section appended and running the counter "
     "on it."),
    ("C2Vacuity", "prove the exemption mechanism cannot be abused",
     "Try to reach `met_target: true` without doing the work: exempt every atom, then correct "
     "nothing; exempt an atom that does not exist; state a seats total the dispatch files "
     "contradict; state a window that is not empty; exempt a window atom with a correction naming "
     "a different window. Run each on a scratch copy of `SCORECARD.md` and report the counter's "
     "exit and failing list. Any attempt that reaches exit 0 is a HIGH finding."),
]

for seat, what, detail in C2_KINDS:
    add(seat, "executor",
        f"R47-C2 verification: {what}.\n\n{detail}\n\n"
        f"{RUN % ('record.py', '--rev <BASE>')}")


add("C2CorrGrammar", "executor",
    "Check the counter/correction grammar agreement end to end: write a scratch `SCORECARD.md` "
    "copy whose corrections section is written by somebody else's wording (the round-46 appendix "
    "style: 'Wave 1: 40 seats; wave 2: not dispatched'), run `record.py` on it, and report what it "
    "refuses and why. Then write the minimal correct line for each class and show it accepted. "
    "Write `<W><SEAT>/report.md` with both texts and both receipts; this tells the L1 exactly "
    "which wording to paste.")


add("C2SelfTest", "executor",
    "Audit `tools/round-47/record.py --selftest`: run it, count registered cases, and delete ONE "
    "clause at a time in a scratch copy to show which case goes red. Name any clause whose "
    "deletion no case notices. Also verify the battery (`correction_forgeries == 3`, "
    "`forgeries_green == 0`) by running it on a scratch copy with a deliberately truthful section "
    "and a deliberately forged one. Receipt in `<W><SEAT>/report.md`.")


# --- scribes: drafting ----------------------------------------------------------

add("ScribeBlock24", "scribe",
    "Draft the final prose for craft rule block 24 in `<W><SEAT>/block24.md`: the lead sentence "
    "(what the round-46 block left only as substrings, counts and conventions), the four-row table "
    "in the frozen house shape, the citation line with 3+ line-selected refs including "
    "`corpus/lessons/round-46.md`, the `interpreter_sha256:` value you compute from "
    "`tools/round-47/exact.py` at the freeze, and the `mutations_sha256:` value. Do not invent a "
    "citation: run `git -C <ROOT> show <FREEZE>:<path> | wc -l` for every line range you cite. "
    "Mark every value you could not compute as `NOT COMPUTED` rather than guessing.")


add("ScribeCorrections", "scribe",
    "Draft the `## Record corrections — round 47` section for `SCORECARD.md` in "
    "`<W><SEAT>/corrections.md`, in the exact grammar `tools/round-47/record.py` parses. Each line "
    "carries: the class and key, the corrected statement, and the evidence pointer (path or "
    "command). Cover: round-45 seat counts, the round-46 empty window, and a note that the "
    "`## Owned axes` coverage and depth rows are updated in place to their current observables. "
    "Keep it append-only in tone: the original text is quoted, the correction supersedes it, "
    "nothing is rewritten.")


add("ScribeAxesRow", "scribe",
    "Draft the replacement text for the `coverage` and `depth` cells of the `## Owned axes` table "
    "so their leading fraction equals the observable at the landing revision (coverage: mapped / "
    "knowledge files; depth: resolved / total craft rule blocks, with block 24 counted). Keep the "
    "historical chain of values in the cell (append the new value at the head, do not delete the "
    "old ones) and give each value its counting command and revision. Write `<W><SEAT>/axes.md` "
    "with the exact cell text.")


add("ScribeLesson", "scribe",
    "Draft `corpus/lessons/round-47.md` in `<W><SEAT>/lesson.md`: the `## Mistakes` table (class, "
    "evidence pointer, captured-by, fix-shown-able-to-fail) mining at least one mistake from this "
    "round or an earlier one — start from `corpus/lessons/round-46.md` `## Routed defects` and the "
    "round-46 non-author spot-check's V1–V10, and say which of them this round closes, which it "
    "routes again, and why; the `## Gate` section recording every source row opened this round "
    "(URL, access date, ≤25-word located quote), at least one admit and at least one reject with "
    "flip condition; and the census before→after line. Do not invent quotes: open every URL you "
    "cite and record its byte count and sha256.")


add("ScribeQuality", "scribe",
    "Draft up to two new `corpus/QUALITY.md` criteria from this round's findings in "
    "`<W><SEAT>/quality.md`: each as a numbered row in the file's own shape, each with a "
    "red-before demonstration the criterion would have caught (name the round and the receipt). "
    "Read `<ROOT>/corpus/QUALITY.md` first; do not duplicate an existing row — quote the row "
    "numbers you checked.")


add("ScribeSources", "scribe",
    "Draft `<W><SEAT>/sources.md`: candidate `corpus/SOURCES.md` rows opened this round, in the "
    "contract's 11-column shape. Candidates: the Python `re` documentation anchored on "
    "`re.fullmatch` (for the exact-token clause) and the git-log documentation's `--diff-merges` "
    "entry (already S142: do not duplicate — check the registry first). Open each URL yourself, "
    "record HTTP status, byte count and sha256, and a ≤25-word located quote. Write the row in the "
    "lane's own id sequence (next free id after the current registry maximum) and say what it "
    "teaches. One reject with reason and flip condition if you find a candidate that does not earn "
    "a row.")


add("ScribeReport", "scribe",
    "Read `.ufo/waves/round-47/{w1}-results.json` when it exists and draft the round report's "
    "**Work performed** and **Landed changes** bullets in `<W><SEAT>/report-draft.md` from the "
    "seat reports in `<ROOT>/.ufo/waves/round-47/w1/*/report.md` — one bullet per work item with "
    "its evidence pointer. Never state a result a seat did not report; mark gaps. This is "
    "drafting for the L1, not the report.")


add("ScribeShonen", "scribe",
    "Read `<ROOT>/SHONEN.md` and draft one line per box for the round report's **SHONEN** section "
    "in `<W><SEAT>/shonen.md`: the box text, the evidence pointer that would justify `[~]`, and "
    "whether a named non-author verifier exists for `[x]` (do not award `[x]`). Check each "
    "`stated:` cell you lean on against the repo and flag stale counts.")


# --- scouts ---------------------------------------------------------------------

SCOUTS = [
    ("ScoutCraftTail", "Map `SKILL.md` at `<FREEZE>`: total lines, the `## Queue-drain craft ` "
     "heading line, every `^- \\*\\*` block start with its first 60 characters, the last block's "
     "line range, the next `## ` heading, and the exact insertion point for block 24 (line number "
     "plus the two neighbouring lines). Also give the registry markers `<!-- instrument-registry "
     "v2 -->` / `<!-- /instrument-registry -->` line numbers."),
    ("ScoutSources", "Map `corpus/SOURCES.md` at `<FREEZE>`: row count, highest id, tier and "
     "status histograms, every row whose `used-by` names `corpus/lessons/round-46.md`, and the "
     "lines the next row must be appended after. Run the census command from `CORPUS.md` and "
     "record its exit code."),
    ("ScoutAxes", "Map the `## Owned axes` table of `SCORECARD.md` at `<FREEZE>`: the exact text of "
     "the coverage and depth rows, the leading fractions, and every historical fraction the cells "
     "carry. Independently compute the coverage observable (mapped/knowledge files) and command A's "
     "citation count at the freeze."),
    ("ScoutRounds", "Map the last two `## Round N` sections of `SCORECARD.md` at `<FREEZE>`: every "
     "`Wave`/`Waves` sentence with its dispatch files' `counts.spawn`, every `is empty` sentence, "
     "every `.ufo/waves/` path token, and every backticked commit. Say which are verifiable and "
     "which are not, with the command."),
    ("ScoutDispatch", "Inventory `.ufo/waves/round-4[3-7]/`: every `*-dispatch.json` with its "
     "`counts`, every `*-results.json`, every `.ready`/`.ready.dispatched`, and which of them are "
     "tracked at `<FREEZE>` (`git cat-file -e`). This is the ground truth for the seats atoms."),
    ("ScoutCraftBlocks", "Enumerate every craft rule block in `SKILL.md` at `<FREEZE>`: number, "
     "title, whether it carries a marker, and whether every citation resolves (write the resolver "
     "yourself). Report which blocks would break block 24's `block_is_last` clause and where "
     "`## Config custody` begins."),
    ("ScoutTools", "Inventory `tools/round-47/`: both counters' CLI surface (`--help`), their "
     "exit constants, their selftest case counts from source, and the digests of their bytes at "
     "`<FREEZE>`. Compare with what `plans/round-47-claims.md` says and list discrepancies."),
    ("ScoutState", "Describe the lane's working state: `jj-lane.sh state`, `git status "
     "--porcelain` counts by path prefix, and whether `tools/round-47/__pycache__` is ignored. "
     "Name every inherited uncommitted path that belongs to this round versus an earlier one. Do "
     "not delete anything."),
]
for seat, body in SCOUTS:
    add(seat, "scout", body + "\n\nWrite `<W><SEAT>/report.md` with a table of every measurement "
        "and the command that produced it.")

# --- reviewers ----------------------------------------------------------------

REVIEWS = [
    ("RevC1Before", "Attack the C1 before-state: re-run the do-nothing control at `<FREEZE>` "
     "yourself and check that `block_present 0` is true for the right reason (block 24 absent, not "
     "a parser accident). Try a `## Queue-drain craft ` heading variant and a block with a column-"
     "zero `- **24. ` line inside a body; report whether the parser could be fooled."),
    ("RevC1Ids", "Attack clause 4: build fixtures where a row names two ids, none, an id not in "
     "the frozen set, the same id twice across two rows, and an id in the v2-hole column instead "
     "of the trigger column. Which reach exit 0?"),
    ("RevC1Tokens", "Attack clause 5: `order`, `order-ish`, ` order `, `` `order` ``, `order,once`, "
     "`ORDER`, an empty cell. Which reach exit 0 under `--profile v3`? Then the same six under "
     "`--profile v2` — the difference is the claim."),
    ("RevC1Digest", "Attack clause 6: is the digest over the *names* sufficient? Reorder the "
     "`MUTATIONS` list in a scratch copy and re-run: what happens to the block's pin and to the "
     "battery denominators? Is a reorder detectable, and does the claim depend on it?"),
    ("RevC1Order", "Attack clause 7: does the literal check survive a reformatted `gate.py` that "
     "keeps the order (line break inside the tuple, double spaces, a kwarg)? Does it catch the "
     "reversed pair written across lines? Report the exact rewrites you tried and the exit."),
    ("RevC1Refs", "Attack clause 8: citations that resolve but are off-topic, a path prefix that "
     "is a prefix of the allowlist (`corpus/lessons-evil/`), a line range that ends exactly at the "
     "last line, a pin computed over a *copy* of the counter. Which reach exit 0?"),
    ("RevC1Last", "Attack the `block_is_last` and title clauses: a block 24 followed by a "
     "comment-only `^- **` line, a block 25 that is really block 24's text, `24.` without the "
     "space, `24. ` inside a fenced code block. Report the exit for each."),
    ("RevC1Battery", "Attack the battery's honesty: are the four forgeries built from the LANDED "
     "block (not a hand-written one)? Mutate `MUTATIONS` in a copy so the battery's own list shrinks "
     "and show what the claim would then report. Is `forgeries_total == 4` a real denominator?"),
    ("RevC2Before", "Attack the C2 before-state: re-run `record.py` at `<BASE>` and independently "
     "verify each of the four mismatches with a command of your own. Then check the verifier's "
     "blind spots: an atom class with zero atoms, a section with no atoms, a `Waves:` sentence "
     "inside a fenced code block, a `## Round` heading in a code fence."),
    ("RevC2Scope", "Attack the section scoping: which `## Round N` headings does the counter "
     "select (last two in file order) and can an amendment appended AFTER the last section hide a "
     "false atom? Build a scratch card where an appended `## Round 47` section carries no atoms and "
     "shows the previous two rounds dropping out of scope — is that a real hole for the claim's "
     "own landing?"),
    ("RevC2Exempt", "Attack the exemption path: with `<= 3` exemptions allowed, can a round exempt "
     "the atoms it falsified without ever correcting them? Try a corrections section that exempts "
     "the two seat atoms and one window atom with true statements but leaves a fourth false atom. "
     "Report the exit and the failing list."),
    ("RevC2Window", "Attack the window class: a window with abbreviated hashes, a window on a path "
     "that does not exist, a window whose `--` pathspec is empty, a window claimed empty for a "
     "range that contains only a rename. Which are detected and which pass?"),
    ("RevC2Axes", "Attack the axes class: are the two fractions the *headline* of the row (they "
     "must be the current claim, not history)? What happens when the row is reflowed across lines, "
     "or when the coverage map is stale but the file count matches? Re-derive both observables "
     "yourself at `<FREEZE>`."),
    ("RevC2Dispatch", "Attack the seats derivation: a round with no dispatch file, a dispatch with "
     "`counts.spawn` absent, a `w1`/`w2` gap (w1 and w3), a results file that contradicts the "
     "dispatch. Report what the counter does for each (exit 1 vs 2) and whether a `2` could be "
     "mistaken for a pass."),
]
for seat, body in REVIEWS:
    add(seat, "reviewer", body + "\n\nEvery finding needs: the fixture path, the command, the exit "
        "code, and what the claim would have to say. Write `<W><SEAT>/report.md`.")

# --- critics ------------------------------------------------------------------

CRITICS = [
    ("CritC1Predicate", "Falsify R47-C1's predicate as written: is `exactness` the right axis and "
     "the right surface for depth? Could the same clauses be satisfied by a block that teaches "
     "nothing (four rows of filler with the right tokens and pins)? Construct that block and score "
     "it. If it reaches exit 0, say so plainly — that is the claim's sharpest limit."),
    ("CritC1Sizing", "Falsify the C1 target: `failing == []` with the battery. Is `rows == 4` "
     "large enough to be a matrix or is it four restatements? Compare against the round-46 block's "
     "13 rows and say what the claim buys. Attack the `mutations_sha256` clause for self-reference: "
     "does the pin prove anything beyond 'the file I ran is the file I cite'?"),
    ("CritC1Order", "Falsify the flag-order clause: what exactly does it protect, and what does it "
     "NOT protect (a `git log` call added elsewhere, a wrapper that reorders at runtime, the "
     "`--format=` position)? Build the case that the clause is decorative if it can be satisfied "
     "without the arm working, and say what would close it."),
    ("CritC2Calibration", "Falsify R47-C2 as calibration: does zero mismatches across 50 atoms "
     "measure self-assessment quality or just bookkeeping? Name the atom classes an honest lane "
     "would need and are missing (e.g. the report's own claims, PROVINCE.md, LOG.md). Then test "
     "whether the counter can be satisfied while a routed record defect (R46-V4, V5, V6, V7) stays "
     "open — list which stay open."),
    ("CritC2Corrections", "Falsify the correction mechanism: the sanctioned repair route is to "
     "append an exemption. Show the cheapest false-but-passing card (e.g. append a correction that "
     "restates a claim already true, exempt the false one) and say whether the `corrections >= 2` "
     "and `exempted <= 3` floors stop it. Give the exact text and the exit."),
    ("CritC2Axes", "Falsify the axes atoms: the coverage row's headline is a *fraction*, but the "
     "axis score is the 0–10 number. Can the counter read `138/138` while the score column still "
     "says `9.72 → 10.0`? Say whether the calibration claim overstates what it verifies, and what "
     "the SCORECARD contract would require instead."),
    ("CritC2Scope", "Falsify the scope claim: 'the last two round sections plus the Owned axes "
     "table'. Compute how much of `SCORECARD.md` (in lines and atoms) that covers, and what the "
     "rest contains. Is `sections == 2` a boundary the round can move to dodge an atom?"),
    ("CritBattery", "Falsify both batteries: for each of the 7 forgeries (4 C1 + 3 C2) decide "
     "whether it is 'the artefact with one defect' or 'a different artefact'. For any that is "
     "merely different, propose the mutation that keeps the class honest, and score your proposal "
     "against the frozen counter."),
    ("CritDigest", "Attack the mutation digest's stability: the digest is over names only. Show a "
     "mutation-list change that keeps the digest identical but changes behaviour, and a name edit "
     "that changes the digest without changing behaviour. Say what the clause should have hashed."),
    ("CritGold", "Construct the gold-plated forgery: the cheapest artefact that reaches "
     "`met_target: true` for BOTH claims without any of the round's real work — e.g. four marker "
     "rows with correct tokens and a truthful corrections section that exempts the mismatches it "
     "created. Score it. If it passes, that is the round's honest-stop evidence."),
]
for seat, body in CRITICS:
    add(seat, "critic", body + "\n\nWrite `<W><SEAT>/report.md`: the fixture, the command, the "
        "exit, and a one-line verdict (`predicate holds` / `predicate too weak, here is what "
        "closes it`).")

# --- mutation testers ---------------------------------------------------------

MUTS = [
    ("MutExactClauses", "Delete one clause at a time from a scratch copy of "
     "`tools/round-47/exact.py` (clauses 1–9) and report which selftest cases and which battery "
     "forgeries go red for each deletion. A clause whose deletion changes nothing is dead weight."),
    ("MutRecordClauses", "Delete one clause at a time from a scratch copy of "
     "`tools/round-47/record.py` (each `failing.append` guard) and report which selftest case "
     "catches it. Name any unguarded clause."),
    ("MutBlock24", "Mutate a candidate block 24 row by row (13 mutations: token, id, cells, exit, "
     "title, marker, header, digest, pin, refs) and report the exit for each under v3 and v2. This "
     "is the landing's own discrimination table."),
    ("MutRecordAtoms", "Mutate a scratch `SCORECARD.md`: change one digit in each of four atoms "
     "(seat count, window hash, path segment, commit hash) and report whether `record.py` catches "
     "each. A silent digit is a finding."),
    ("MutCorrections", "Mutate corrections: correct the wrong round, state a total that matches a "
     "different round, exempt a non-existent path, name a window pair that exists but is not in "
     "scope, add a duplicate correction. Report the exit for each."),
    ("MutGate", "Mutate a scratch copy of `tools/round-46/gate.py` in ten ways (flag order, "
     "`--format=`, `-z`, `--name-status`, `-m`, the `--` separator, the pathspec join, the status "
     "regex, the decode, the return) and report which mutation `exact.py` clause 7 catches and "
     "which it does not."),
    ("MutScratch", "Probe the scratch discipline of both counters: run them with `TMPDIR=/tmp`, "
     "with no `HYAKU_SCRATCH`, with a relative `--json-out`, with `--json-out` pointing at a "
     "graded surface (`SKILL.md`). Report each exit and reason. A counter that writes under `/tmp` "
     "is a routed defect."),
    ("MutExitCodes", "Probe exit-code semantics: run both counters with unknown revisions, a "
     "non-ancestor freeze, a malformed claims file (scratch copy), an unreadable SCORECARD, and a "
     "crash injected into a scratch copy. Every one must be exit 2 and never 0. Report the matrix."),
]
for seat, body in MUTS:
    add(seat, "mutation-tester", body + "\n\nWrite `<W><SEAT>/report.md` with a mutation table "
        "(mutation | exit | detected by) and the command you ran.")

# --- connector / sentinel / revenger / labrat / simplifier ---------------------

CONN = [
    ("ConnSeparability", "Test causal separability between the two claims: revert each landing "
     "surface in a scratch clone (block 24 out; corrections out) and score BOTH counters at each "
     "state. Report the 2×2 matrix of exits — each claim must score without the other."),
    ("ConnRouted", "Map the round-46 routed defects (R46-CL1..CL11 plus the spot-check's V1–V10) "
     "onto what this round actually closes. For each: closed, routed again, or not addressed, with "
     "the file/line that closes it. This is the round's coverage-of-routing table."),
    ("ConnSiblings", "Look for overlap with sibling lanes' surfaces: does any other shokunin repo "
     "carry an `exactness`/`record-consistency` counter or a `corrects <class>` grammar this lane "
     "would be duplicating? Search read-only under `/home/vgpnk/Projects/shokunin/*-shokunin/` "
     "(`grep -rn 'corrects .*seats\\|mutations_sha256\\|exactness-table'`). Report hits and whether "
     "the lane should cite rather than reinvent."),
    ("ConnCraft", "Trace the craft-block lineage: block 22 (round 45) → block 23 (round 46) → "
     "block 24 (this round). For each routed defect, name the block that first stated it and the "
     "block that made it checkable. Say whether block 24 repeats a lesson already stated (dead "
     "weight) or closes a hole (real move)."),
]
for seat, body in CONN:
    add(seat, "connector", body + "\n\nWrite `<W><SEAT>/report.md` with the matrix/table.")

add("SentScope", "sentinel",
    "Security and scope review of the frozen instruments: can either counter write outside the "
    "lane? Check `--json-out` handling, the fixture-repo creation (does it verify the toplevel?), "
    "the scratch-root refusal, symlink handling in `gate.show`, and whether a crafted `SCORECARD.md` "
    "or `SKILL.md` could make the counter execute something. Report each as pass/fail with the "
    "command. Write `<W><SEAT>/report.md`.")
add("SentFixtures", "sentinel",
    "Fixture hygiene: build five fixtures (merge with conflict resolution, rename, symlink, "
    "submodule, bare repo) and report whether either counter can be pointed at one and whether the "
    "fixture's identity lands anywhere outside scratch. Confirm no `git commit` runs with a "
    "throwaway identity in the lane tree. Write `<W><SEAT>/report.md`.")
add("RevIntent", "revenger",
    "Reconstruct the original intent of R46-CL6: read the round-46 lesson, the gate source at the "
    "freeze, and the git-log documentation, then decide whether clause 7 protects the arm the "
    "lesson describes, or only its spelling. Give the historical evidence (quoted lines) and a "
    "verdict. Write `<W><SEAT>/report.md`.")
add("RevHistory", "revenger",
    "Reconstruct why the round-46 record claimed 40 + 40 seats and an empty window: read the "
    "dispatches, the ready files' timestamps, the results file, and the SCORECARD amendments. "
    "Decide which claim was true when written and which became false later, so the correction says "
    "the right thing. Write `<W><SEAT>/report.md`.")
add("LabOrderProbe", "executor",
    "Falsifiable probe: on a deterministic two-parent merge fixture, run `git log -m "
    "--diff-merges=first-parent --name-status -z --format= A..B` and the same with the two flags "
    "swapped; report the exact byte counts and whether the merge appears once or twice. That is the "
    "single fact clause 7 rests on. Write `<W><SEAT>/report.md` with both outputs' sha256.")
add("LabWindowProbe", "executor",
    "Falsifiable probe: at the freeze, is there ANY concrete A..B window over the round-46 paths "
    "that is empty and plausibly the one the round-46 record meant? Test `332f4884..58eb04b6`, "
    "`0425224..58eb04b6`, `58eb04b6..58eb04b6` and `332f4884..332f4884`, with and without "
    "`--diff-merges`. Report each byte count; the correction must name a window that is really "
    "empty. Write `<W><SEAT>/report.md`.")
add("SimplC1", "simplifier",
    "YAGNI pass on `tools/round-47/exact.py`: which checks are load-bearing for the claim and "
    "which are decoration? For each function/flag, name the claim clause it serves or argue for "
    "its deletion. Do not edit; write `<W><SEAT>/report.md` with a keep/cut table and the selftest "
    "case that would catch each cut.")
add("SimplC2", "simplifier",
    "YAGNI pass on `tools/round-47/record.py`: same treatment. Specifically: is the `axes` class "
    "necessary for the calibration claim, and is `CORR_MIN = 2` a real floor or a formality? "
    "Write `<W><SEAT>/report.md` with a keep/cut table.")


def main():
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES}
             for t in T]
    spec = {"wave": "r47-w1", "milestone": MILE, "reportDir": REPORT,
            "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path],
                          capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s"
                         % (proc.returncode, proc.stdout[:800], proc.stderr[:800]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {t["name"]: {"kind": "spawn", "agentId": None, "role": t["agent"],
                           "item": None, "axes": AXES, "milestone": MILE}
               for t in wave_tasks}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": "r47-w1",
        "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1",
                     "path": ".ufo/waves/round-47/w1/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None,
                                              "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0,
                                              "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": ("Issue exactly one batched task call with taskCall ({context, tasks}); never "
                 "split a wave into multiple task calls (one-swarm-per-wave)."),
    }
    with open(os.path.join(WAVE_DIR, "w1-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w1"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w1/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": "r47-w1",
                   "reportDir": REPORT, "members": members}, f, indent=1)
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
    else:
        with open(os.path.join(WAVE_DIR, "w1.ready"), "w") as f:
            json.dump({"lane": "kaidoku", "round": 47, "wave": "r47-w1",
                       "dispatch": os.path.join(WAVE_DIR, "w1-dispatch.json"),
                       "l1": "KaidokuR47"}, f)
    print("wrote", len(wave_tasks), "seats;",
          dict(collections.Counter(t["agent"] for t in wave_tasks)))
    print("counts", plan["counts"])


if __name__ == "__main__":
    main()
