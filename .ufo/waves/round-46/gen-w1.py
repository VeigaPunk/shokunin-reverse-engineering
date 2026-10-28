#!/usr/bin/env python3
"""Generate the round-46 wave-1 spec, validated dispatch and ready file (L1 artifact)."""
import collections
import json
import sys
import os
import subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-46")
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
MILE = ("Round 46 wave 1: verify the frozen discriminating instruments, draft the landing "
        "evidence (rule block 23 and 38 registry rows), open the round's source and attack "
        "both claim predicates before data")
REPORT = ".ufo/waves/round-46/w1"
W = REPORT + "/"

CTX = f"""# Target
kaidoku-shokunin round 46, wave 1 = verification of the FROZEN instruments, drafting of the landing evidence, source opening, and attack of both claim predicates BEFORE data. Lane root (absolute): {ROOT}. L1 = KaidokuR46 (integration owner; it holds the canonical section-3 planner seat — the wave validator rejects `planner` as a swarm role, so bounded planning data-walks ride scout/connector/revenger seats; recorded in the round report). Freeze commit `{FREEZE}`; the frozen bytes are `plans/round-46-claims.md` and `tools/round-46/` (directory pathspec).

# What round 46 is fixing
Round 45 landed two artefacts and reported `met (instrument non-discriminating)`: a 44-line forged C1 artefact and a six-fenced-row C2 artefact each scored `met_target: true`. Round 46 replaces the measure: `tools/round-46/attest.py` (C1) and `tools/round-46/registry.py` (C2) must score their own forged copies red and the genuine artefact green. The forgeries are built by MUTATING the landed bytes, so the battery cannot drift from the artefact it defends.

# Read first
`{ROOT}/plans/round-46-claims.md` (both frozen predicates, clause by clause), then the instrument you are asked about. Do not re-derive the claims from this prompt: the claims file is the rule.

# Contract (binding on every seat)
- **You are read-only on the lane tree.** Write ONLY inside `{ROOT}/.ufo/waves/round-46/w1/<YourSeatName>/` (create it). Never edit `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command (no `git add/commit/checkout/reset/switch/pull/push`, no `jj commit/new/describe/squash/rebase/abandon/bookmark`). Read-only git is fine: `log`, `show`, `diff`, `diff-tree`, `ls-tree`, `cat-file`, `rev-parse`, `status --porcelain`.
- **Frozen means read-only.** `tools/round-46/` and `plans/round-46-claims.md` are byte-frozen at `{FREEZE}`. You may COPY them to scratch and mutate the copy; never mutate the originals.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, and every later git call names `-C "$D"`. Verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never run `git commit` with a throwaway identity anywhere else.
- **Scratch**: `S=/fast/scratch/hyaku/kaidoku-r46/<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S" HYAKU_SCRATCH="$S"`, pass explicit `--work`/`-p` dirs. Remove `$S` before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python) AFTER copying receipts into your report dir. Never write under `/tmp`. Nothing under `/tmp` is citable evidence.
- **Honest capture beats a pass.** Every receipt you write carries: the exact command, exit code, stdout sha256, UTC time. A check you did not run is not passed — say "not run".
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate. A 2 never counts toward a target.
- **`Report:` trailer**: every `Report: .ufo/waves/...` path in your prompt is relative to `{ROOT}` — write it at `{ROOT}/<that path>`.
- **Tooling**: read `/home/vgpnk/.omp/agent/RULES.md` before installing anything. All pacman transactions are PAUSED host-wide; use `uv tool`/`npx`/an official binary in `~/.local/bin`, or file nothing. Record any install (tool, version, channel, reason) in your report.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.

# What the L1 does with your output
It reads your report, reconciles disagreements, lands `SKILL.md` rule block 23 and the registry section, the release means you do or do not satisfy the claim you were asked about. A finding that the frozen instrument is wrong is valuable: report it with the exact command and the differing value; do not "fix" it. Registry-row seats: the L1 pastes your rows verbatim, so format them exactly.
"""

HOUSE = ("| `{path}` | {purpose} | 0={z}; 1={o}; 2={t} | {selftest} | {pinned} | {scope} | kaidoku |")
REG_RULE = (
    "Write ONE markdown table row per instrument, in this EXACT 7-column house format "
    "(one line each, no wrapping, NO literal `|` inside any cell, no backticks around "
    "anything except cell 1's path):\n\n"
    "`| \\`<repo-relative path>\\` | <one-line purpose> | 0=<meaning>; 1=<meaning>; 2=<meaning> | <self-test command> | <pinned-value path, or none> | <write scope, or none> | kaidoku |`\n\n"
    "Rules the frozen counter enforces: cell 1 is exactly the backticked path AND nothing "
    "else; cell 3 (the verdict map) must bind each of 0, 1 and 2 to a meaning with `=`; the "
    "row has exactly 7 cells. Read the tool's source at the freeze to derive the exit "
    "meanings — never guess. If the tool takes an exit code outside {0,1,2}, say so in your "
    "report (not in the row). If the tool has no selftest, write `none`. Verify at least one "
    "claim in each row with a command you actually ran (e.g. `--help`, `--selftest`, a bad-argument probe) and record the command plus exit code.")


def T(name, agent, task):
    task = task.replace("<ROOT>", ROOT).replace("<FREEZE>", FREEZE).replace("<W>", W)
    return {"name": name, "agent": agent, "task": GODSPEED + task}


def reg_seat(name, paths, tag):
    rows = "\n".join("- `%s`" % p for p in paths)
    return T(name, "executor",
             "Produce three READY-TO-PASTE SKILL.md instrument-registry rows for the instruments "
             "below (round-46 C2 census, tag `%s`).\n\n%s\n\n%s\n\nFor each instrument open "
             "`<ROOT>/<path>` AT THE FREEZE (`git -C <ROOT> show <FREEZE>:<path>`) and read its "
             "argparse/CLI surface and its exit paths. Write `<W>%s/rows.md` containing exactly "
             "three rows in the required format, then re-read your own file and check: 7 cells "
             "per row, cell 1 exactly the backticked path, cell 3 binds 0=, 1= and 2=. Record "
             "each command you ran and its exit code in `<W>%s/receipt.md`."
             % (tag, rows, REG_RULE, name, name))


def main():
    census = json.load(open(os.path.join(ROOT, "tools/round-46/census.json")))["paths"]
    groups = [census[i::13] for i in range(13)]
    tags = list("ABCDEFGHIJKLM")
    tasks = []
    for i, g in enumerate(groups):
        tasks.append(reg_seat("R46W1Reg" + tags[i], g, "reg-" + tags[i].lower()))

    tasks += [
        T("R46W1ScoutCraftTail", "scout",
          "Map the tail of `<ROOT>/SKILL.md` at `<FREEZE>` for the round-46 landing. Report: "
          "total lines; the `## Queue-drain craft ` heading line; every `^- \\*\\*` block start "
          "line and its first 60 characters; the LAST block's line range and its last line; "
          "the next `## ` heading after it and its line; and the exact insertion point (line "
          "number and the two neighbouring lines) where new rule block 24 would begin. Also "
          "report the line number where the file's registry sections (`### Round-40 instrument "
          "registry`, `### Round-44/45 instrument registry`) sit and what follows the last "
          "registry table. Write `<W>R46W1ScoutCraftTail/report.md`."),
        T("R46W1ScoutFixtures", "scout",
          "Inventory what round 45 committed as forgery evidence, so round 46 knows what it can "
          "re-run instead of rebuild. `git -C <ROOT> ls-tree -r --name-only <FREEZE> -- "
          ".ufo/waves/round-45 | grep -i fixture`. Open the round-45 seat reports "
          "`R45W1CritC1/report.md`, `R45W1CritC2/report.md`, `R45W2ReviewC2/report.md` and the "
          "committed fixtures under `R45W2ReviewC2/evidence/fixtures/`. For each committed "
          "fixture file report: path, what defect class it encodes, and whether a round-46 "
          "counter could score it directly (it is a `SKILL.md` body) or would need a repo "
          "around it. Report the cheapest-green artefact sha256 that R45-CL13 names and whether "
          "that exact artefact is committed. Write `<W>R46W1ScoutFixtures/report.md`."),
        T("R46W1ScoutCensus", "scout",
          "Independently re-derive the C2 census WITHOUT running `tools/round-46/census.py`, so "
          "the counter's scope rests on a second reading. Read `plans/round-41-claims.md` .. "
          "`plans/round-46-claims.md` at `<FREEZE>` and extract every path matching "
          "`tools/round-4[1-6]/**.{py,sh}`. Then `python3 -c` or `grep -oE` your own list, sort "
          "it, and diff it against `tools/round-46/census.json` (`jq -r '.paths[]'`). Report: "
          "the count you derived, the count in the JSON, the exact symmetric difference, and "
          "for each difference whether the path exists at `<FREEZE>`. Also report whether every "
          "census path is a tracked file at `<FREEZE>` (`git cat-file -e`). Write "
          "`<W>R46W1ScoutCensus/report.md`."),
        T("R46W1ScoutSiblingReg", "scout",
          "Sibling-overlap scan: do other lanes already own an instrument registry or a "
          "freeze-integrity counter, and what row format do they use? Grep sibling lanes' "
          "`SKILL.md` (read-only) under `/home/vgpnk/Projects/shokunin/*-shokunin/` for "
          "`instrument registry`, `verdict map`, `exit codes`, and for tools named like "
          "`*counter.py`/`*attest*`. Report: which lanes have a registry section, ONE verbatim "
          "example row from another lane with its path:line, whether any sibling has a "
          "discrimination battery (does any counter score forgeries?), and whether this lane's "
          "7-column shape conflicts with the fleet's `PROTOCOL.md` house schema (quote the "
          "schema line). Write `<W>R46W1ScoutSiblingReg/report.md`."),
        T("R46W1ExecFidelity", "executor",
          "Verify both frozen counters' fidelity and selftests FROM THE FREEZE BYTES. Extract "
          "`git show <FREEZE>:tools/round-46/attest.py` and `registry.py` and `gate.py` into "
          "scratch; run `python3 -I -B <copy> --root <ROOT> --freeze <FREEZE> --rev <FREEZE> "
          "--selftest` for each and record exit, the `*_SELFTEST: cases=N failures=M` line, and "
          "stdout sha256. Then re-run both fidelity receipts: `attest.py --spec r45 --profile v1 "
          "--no-battery --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev "
          "f59565b782c18b0eb691bec12f52d2f80d9f5032` and the same for `registry.py`; record every "
          "receipt field and compare with round 45's recorded values (`rule_blocks 22`, "
          "`block22_rows 10`, `block22_refs 8`, `registry_rows 45`, `scope_size 6`). State "
          "plainly whether the v1 profile is a faithful port or a straw man. Write "
          "<W>R46W1ExecFidelity/report.md`."),
        T("R46W1ExecGap", "executor",
          "Measure the round-45 discrimination gap LIVE, on committed bytes, so the report's "
          "before value is not just a quoted receipt. (1) Find the cheapest-green C1 forgery "
          "round 45 recorded: `R45W1CritC1/receipts.json` entry whose label contains "
          "`cheapest` or `a6`, plus `R45W2Lesson/fx-a6-SKILL.md`. (2) Build a fixture repo "
          "containing that SKILL text, a `plans/round-45-claims.md` with the round-45 frozen "
          "paths, and the real `tools/round-45/frozen-path-preflight.py`, then score it with the "
          "FROZEN round-45 counter `tools/round-45/c1-counter.py` copied from `<FREEZE>`: record "
          "exit and `met_target`. (3) Score the same text with `tools/round-46/attest.py --spec "
          "r45 --profile v1`: record exit. Report whether a forgery round 45 accepted is still "
          "accepted by the round-46 v1 profile (it must be — that is the hole C1 closes). "
          "Write `<W>R46W1ExecGap/report.md` with both receipts."),
        T("R46W1ScribeSource", "scribe",
          "Open SOURCES row candidate S142 live and produce the row plus its Gate block. Fetch "
          "`https://git-scm.com/docs/git-log` (record HTTP status, byte size, sha256, UTC access "
          "time) and locate the `--diff-merges` section: the value `first-parent` and the "
          "sentence saying it shows the diff against the first parent only. Record a located "
          "quote of at most 25 words and the anchor name. Write the lane's 11-column registry "
          "row (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, "
          "used-by) with `used-by` naming `corpus/lessons/round-46.md`, and a 3-line Gate block "
          "(URL, access date, quote). Prove the quote is present in your saved copy. If the "
          "page does not contain it, say so and write no row. Write `<W>R46W1ScribeSource/row.md`."),
        T("R46W1ScribeBlock23", "scribe",
          "Draft the prose for `SKILL.md` rule block 23 so the L1 can land it. Read "
          "`plans/round-46-claims.md` R46-C1 and `corpus/lessons/round-45.md` R45-CL13 and "
          "R45-CL14 (both lists of named defects are the row sources). Produce: (a) the block's "
          "title line beginning `- **23. ` and at most 40 words; (b) a markdown table with the "
          "exact header `| trigger | v1 hole | v2 arm | exit |` and THIRTEEN data rows, one per "
          "routed id R45-CL2, CL6, CL7, CL9, CL13, CL14, CL15, CL18, CL19, CL20, CL22, CL23, "
          "CL24 — each row's trigger cell names its id, its v2 arm cell names one token from "
          "commit/blob/restored/dirty/pathspec/merge/marker/header/rows/refs/pin/battery/output/"
          "presence, its exit cell is 1 or 2; (c) a `Refs:` paragraph of at least six "
          "`path:line` or `path:first-last` citations inside `corpus/lessons/`, "
          "`corpus/knowledge/`, `plans/` or `tools/round-46/`, with "
          "`corpus/lessons/round-45.md` among them, each line range VERIFIED to exist at "
          "`<FREEZE>`; (d) the sentence carrying `S142`, the path "
          "`tools/round-46/attest.py` and `sha256:<64 hex>` (compute it with `git -C <ROOT> show "
          "<FREEZE>:tools/round-46/attest.py | sha256sum`). No cell may contain a literal `|`. "
          "Write `<W>R46W1ScribeBlock23/block.md`."),
        T("R46W1ScribeLesson", "scribe",
          "Draft the round-46 lesson's prose so the L1 can land it. Read "
          "`corpus/lessons/round-45.md` (Mistakes table shape, Gate table shape, Routed defects "
          "list) and `corpus/lessons/round-45-verifier-spotcheck.md`. Produce: (1) `## Mistakes` "
          "rows for these classes — (M46-1) `control-named-a-measurement-that-cannot-exist-at-"
          "the-freeze` (the claims plan named `ctl-c1-1-v1-profile` 'at the freeze', but the "
          "battery mutates the landed artefact, so the receipt can only exist after landing; "
          "captured-by: the satisfiability preflight, which should have asked 'when does this "
          "value exist'; fix: the v1-gap receipt is produced post-landing and the plan says so); "
          "(M46-2) `plan-contradicted-its-own-instrument` if you find one by comparing "
          "`plans/round-46-claims.md` clause by clause with `tools/round-46/attest.py` and "
          "`registry.py`; (M46-3) any mismatch you find between the claims text and the code. "
          "(2) A `## Gate` draft shaped like round 45's: the source table (S142 once the scribe "
          "row exists), an admit and a reject from the assimilation set (`Assimilation: none` "
          "with the reason if nothing applies), and the census before/after line. Do not invent "
          "numbers — leave `<L1 fills>` where a measurement is needed. Write "
          "<W>R46W1ScribeLesson/lesson.md`."),
        T("R46W1RevGateMerge", "reviewer",
          "Attack the round-46 freeze core's merge arm, which exists to close R45-CL6. Read "
          "`<ROOT>/tools/round-46/gate.py` (`history_touched`, `blob_changed`, `freeze_state`). "
          "In a scratch fixture repo: (a) create two branches, edit a frozen path on a side "
          "branch, merge with a conflict and resolve it by restoring the original bytes (a "
          "resolution edit on the merge) — does the history arm still see the path? (b) the same "
          "but the merge's resolution keeps the edit — does `freeze_state` exit 2? (c) a squash "
          "merge that folds a tamper+restore away — record what the gate reports and whether the "
          "table's stated limit matches. (d) a plain fast-forward merge with no conflict. Report "
          "each as {shape, expected by the claims file, observed exit, `touched`/`blob_changed`/"
          "`restored`}. Write `<W>R46W1RevGateMerge/report.md` with the fixture scripts."),
        T("R46W1RevRestoredUnion", "reviewer",
          "Verify that R45-CL18 cannot re-enter: the round-45 gate never listed a path named "
          "only by `--freeze-path`, so tamper+restore read `clean`. Round 46 derives ONE frozen "
          "set from the claims file. Build a scratch fixture whose claims file lists a FILE and "
          "a DIRECTORY, tamper with the file, commit, restore the bytes, commit again, then call "
          "`gate.freeze_state` (import it from a copy in scratch with `sys.path` set) — record "
          "exit, `touched`, `blob_changed`, `restored`. Then do the same for a path inside the "
          "frozen directory. Report whether a restore-only history now yields `restored` "
          "non-empty (it must) and exit 2. Also test: a commit that only ADDS a file inside the "
          "frozen directory. Write `<W>R46W1RevRestoredUnion/report.md`."),
        T("R46W1RevOutputGuard", "reviewer",
          "Attack `gate.out_path` (the R45-CL22 fix). Try, against a scratch COPY of the lane "
          "layout (never the real lane): `--json-out SKILL.md`, `--json-out ../../SKILL.md`, "
          "`--json-out plans/round-46-claims.md`, `--json-out corpus/SOURCES.md`, "
          "`--json-out tools/round-46/gate.py`, an absolute path inside the lane, a path outside "
          "the lane root, a symlink inside the lane pointing at SKILL.md, and a normal "
          "`.ufo/waves/...` path. Report each as {target, expected, exit, whether any byte of a "
          "graded file changed (`sha256sum` before/after)}. Also check whether the counters "
          "write the file BEFORE the verdict is computed (a `--json-out` onto a frozen path must "
          "never write). Write `<W>R46W1RevOutputGuard/report.md`."),
        T("R46W1RevScratch", "reviewer",
          "Attack the scratch policy (R45-CL20). Read `gate.scratch`. Test: `HYAKU_SCRATCH` "
          "unset with `TMPDIR` unset; `HYAKU_SCRATCH=/tmp`; `TMPDIR=/tmp/x`; "
          "`HYAKU_SCRATCH=/var/tmp`; `HYAKU_SCRATCH` set to a real fast path; `HYAKU_SCRATCH` "
          "set to a relative path; a read-only `HYAKU_SCRATCH` dir. Report each as {env, "
          "expected, observed, whether anything was created under /tmp (`find /tmp -newermt` "
          "around your run)}. Then state whether both counters still reach exit 1/0 (not 2) "
          "with a normal scratch root. Write `<W>R46W1RevScratch/report.md`."),
        T("R46W1RevRound45Recheck", "reviewer",
          "Re-check the round-45 report's central sentences against committed bytes now, since "
          "round 46 supersedes them. Open `.ufo/reports/round-45/kaidoku.md` (fleet root, "
          "read-only) and `corpus/lessons/round-45.md`. For each of these, state supported / "
          "unsupported with the command you ran: (a) 'both counters are shown non-discriminating "
          "by wave 1' — is the artefacts named there really scored green?; (b) the recorded "
          "`block22_refs` sequence 6/7/8/8; (c) 'no seat falsified either claim predicate'; (d) "
          "the wave sizes 40/36 and the 15 dead seats. Report any sentence round 46 must not "
          "repeat. Write `<W>R46W1RevRound45Recheck/report.md`."),
        T("R46W1CritC1", "critic",
          "Falsify R46-C1 before data. Read `plans/round-46-claims.md` R46-C1 and "
          "`tools/round-46/attest.py`. At least SIX attacks, each {attack, expected if the "
          "claim is sound, observed}: (1) can a block satisfy every clause while carrying no "
          "actionable content — e.g. thirteen rows that name the routed ids and the arm "
          "vocabulary but whose 'v1 hole' cell is lorem ipsum? Is that a defect or acceptable? "
          "(2) is `marker_occurrences == 1` checkable when the marker also appears in another "
          "section? (3) can the `sha256` pin be satisfied by a file the forger controls (does "
          "the pin bind the BYTES at `--rev` or just a hex string)? (4) does the arm-vocabulary "
          "check pass a row whose arm cell contains 'blob' as a substring of 'blobberish'? (5) "
          "is `refs >= 6` gameable by six citations to the same file? (6) does the routed-id "
          "check require the id to be the WHOLE trigger or just present? Name the cheapest "
          "artefact that would score green and is not the intended table. Write "
          "<W>R46W1CritC1/report.md`."),
        T("R46W1CritC2", "critic",
          "Falsify R46-C2 before data. Read `plans/round-46-claims.md` R46-C2 and "
          "`tools/round-46/registry.py`. At least SIX attacks {attack, expected, observed}: (1) "
          "can a row satisfy a census path while describing a different tool (is exact cell-0 "
          "equality enough when the purpose cell lies)? (2) can the verdict-map cell be "
          "`0=x; 1=y; 2=z; <garbage>`? (3) does the section parser handle a `|` inside a cell "
          "or an unclosed fence? (4) can a row register twice and shadow? (5) is "
          "`absent_at_rev` computed from the census or from the row (i.e. can a ghost pass)? "
          "(6) what happens when `census.json` lists a path twice? Report the cheapest artefact "
          "that scores green without being the intended registry. Write <W>R46W1CritC2/report.md`."),
        T("R46W1CritBattery", "critic",
          "Attack the battery itself — the round's central novelty. Read "
          "`tools/round-46/attest.py` `MUTATIONS`/`run_battery` and `registry.py` "
          "`MUTATIONS`/`run_battery`. Questions to answer with a probe each: (a) can a mutation "
          "silently become a no-op (the code counts a no-op as `v2_green += 1` — when does that "
          "happen and can a forger force it)? (b) is a mutation that BOTH fails v1 and v2 "
          "counted in the denominator (the claim requires `v1_green == 9`)? (c) does the fixture "
          "repo copy every file the refs name, and what happens when one is missing at `--rev`? "
          "(d) can the battery be made to pass by weakening the artefact so every mutation is a "
          "no-op? (e) does the battery leave any scratch behind? Write "
          "<W>R46W1CritBattery/report.md` with the exact commands."),
        T("R46W1CritDenominator", "critic",
          "Interrogate the denominators. `forgeries_total == 9` (C1) and `== 7` (C2) are fixed "
          "numbers, but the mutations are code. Answer: (1) if someone deletes a mutation from "
          "`MUTATIONS`, what breaks and where? (2) does `v1_green == 9` measure the forgery's "
          "quality or the port's looseness — what would a stricter v1 port do to the claim? (3) "
          "is 'the nine round-45 defect classes' the right denominator, or does the routed list "
          "name more classes that the mutations omit (compare R45-CL13 a-f and R45-CL14 a-f to "
          "the nine mutation names and list every omission)? (4) is `genuine_green == 1` a real "
          "guard against a counter that rejects everything? Write "
          "<W>R46W1CritDenominator/report.md`."),
        T("R46W1MutC1Checks", "mutation-tester",
          "Mutate `tools/round-46/attest.py` and find survivors in its 15-case selftest. Copy "
          "it (and `gate.py`) to scratch; produce at least EIGHT mutants, one per check: (m1) "
          "`marker_occurrences != 1` → `>= 1`; (m2) drop the is-last-block check; (m3) header "
          "prefix match instead of equality; (m4) `rows >= 13` → `>= 8`; (m5) drop the exit-cell "
          "check; (m6) drop the routed-id check; (m7) substring arm vocabulary; (m8) pin "
          "compared by length only. For each run `--selftest` and name the case that goes red; a "
          "survivor is a hole — report the case that SHOULD have caught it. Write "
          "<W>R46W1MutC1Checks/report.md`."),
        T("R46W1MutC2Checks", "mutation-tester",
          "Mutate `tools/round-46/registry.py` and find survivors in its 12-case selftest. Copy "
          "it (and `gate.py`) to scratch; at least SIX mutants: (m1) `re.search` on cell 1 "
          "instead of equality; (m2) fence-blind parse; (m3) drop the header check; (m4) drop "
          "`absent_at_rev`; (m5) `EXITMAP` back to `\\b[012]\\b`; (m6) accept rows outside the "
          "marker section. For each run `--selftest`, name the red case or report the survivor. "
          "Write <W>R46W1MutC2Checks/report.md`."),
        T("R46W1MutGate", "mutation-tester",
          "Mutate `tools/round-46/gate.py` and find survivors, using the two counters' selftests "
          "as the harness. Copy `gate.py` into a scratch copy of `tools/round-46/`; at least SIX "
          "mutants: (m1) drop `--diff-merges=first-parent`; (m2) drop the blob arm; (m3) frozen "
          "set from a hard-coded list instead of the claims file; (m4) `dirty` replaces rather "
          "than unions (call it directly); (m5) `out_path` returns the path unchanged; (m6) "
          "scratch allows `/tmp`. For each run both `--selftest`s and report which case catches "
          "it or that it survives. Note: the selftests cover the counters, not gate's CLI, so a "
          "survivor here may be a coverage hole rather than a bug — say which. Write "
          "<W>R46W1MutGate/report.md`."),
        T("R46W1SentTools", "sentinel",
          "Adversarial security review of `tools/round-46/{gate,attest,registry,census}.py`. "
          "Hunt: (a) command injection (any shell string built from git output, a claims file or "
          "a SKILL row); (b) path traversal in `--root`, `--json-out`, fixture paths; (c) a "
          "hostile `SKILL.md` or `census.json` that makes a counter report `met_target true` "
          "without the work; (d) writes outside scratch (does the battery clean up? does "
          "`fixture_repo` ever leave a repo behind?); (e) `git` invocation with attacker-"
          "controlled refs (can `--freeze`/`--rev` start with `-`?); (f) `subprocess` without a "
          "timeout on a hostile repo. For each: exact input, code line, exploitable yes/no. "
          "Write <W>R46W1SentTools/report.md`."),
        T("R46W1RevengerPlan", "revenger",
          "Is the round-46 target the right one? Reverse-engineer what round 45 actually "
          "measured versus what it claimed, from committed bytes only: read "
          "`plans/round-45-claims.md`, `tools/round-45/{c1-counter,c2-counter}.py`, the round-45 "
          "lesson's R45-CL13/CL14, and `.ufo/reports/round-45/kaidoku.md`. Answer: (a) which of "
          "the sixteen named defects (R45-CL13 a-f, R45-CL14 a-f) does the round-46 pair of "
          "instruments actually close, and which does it leave open? (b) which of the remaining "
          "routed items (R45-CL1..CL24) does round 46 close by construction, by a check, or not "
          "at all? Give a table. (c) Is 'the counter must score its own forgeries red' the "
          "cheapest honest way to make the measure a discriminator, or is there a smaller "
          "move? Write <W>R46W1RevengerPlan/report.md`."),
        T("R46W1SimplInstruments", "simplifier",
          "YAGNI review of `tools/round-46/` before it is used as evidence. For each of gate.py, "
          "attest.py, registry.py, census.py, name code no clause of "
          "`plans/round-46-claims.md` needs and whose removal keeps both selftests green. Test "
          "each proposed deletion in a scratch copy and report `selftest after deletion` "
          "(cases/failures). Candidates to examine: unused receipt fields, `SPECS['r45']` "
          "fields, `m_*` functions no mutation list uses, `census.py`'s `per_claims_file` "
          "detail. A deletion that breaks a red case is not dead weight. Write "
          "<W>R46W1SimplInstruments/report.md`."),
        T("R46W1ProbeTmp", "executor",
          "One falsifiable hypothesis: 'the round-46 battery writes nothing outside the scratch "
          "root it is given'. Test it with a filesystem diff: snapshot `find /tmp /var/tmp "
          "-maxdepth 2 -newermt '-5 minutes'` before, run `attest.py --selftest` and "
          "`--no-battery` and a full run with `HYAKU_SCRATCH=/fast/scratch/hyaku/<seat>`, then "
          "snapshot again; also list every path the run created under the scratch root and "
          "check it is removed at exit. Report the hypothesis verdict (falsified/not falsified), "
          "the exact commands, and any leftover path with its mtime. Write "
          "<W>R46W1LabratTmp/report.md`."),
        T("R46W1ProbeCost", "executor",
          "One falsifiable hypothesis: 'a full C1 + C2 run costs under 60 s and under 50 MB of "
          "scratch'. Measure: `time` and peak RSS (`/usr/bin/time -v`) for "
          "`attest.py --root <ROOT> --freeze <FREEZE> --rev <FREEZE>` and the same for "
          "`registry.py`; report wall time, max RSS, and the peak size of the scratch root "
          "during the run (`du -s` sampled or `inotifywait` if available). Then state whether "
          "the battery is cheap enough for a closure to re-run it, and what dominates the cost. "
          "Write <W>R46W1LabratBatteryCost/report.md`."),
        T("R46W1ConnFleet", "connector",
          "Cross-claim and cross-source pattern scan for round 46. (1) Read-only, open "
          "`/home/vgpnk/Projects/shokunin/scripts/hyaku/{jj-lane.sh,fleet-commit.sh,inline.sh}` "
          "and report every freeze/dirty-path/output guard they already enforce — does any of "
          "them run a lane-side gate before a commit or a sweep (R45-CL1)? (2) Report which of "
          "the round's two instruments duplicate an existing fleet mechanism (so the registry "
          "row says so) and which are genuinely lane-local. (3) Grep the fleet's "
          "`templates/round-prompt.md` and `MISSION.md` for a rule the round-46 claims should "
          "cite; quote it with path:line. Write <W>R46W1ConnFleet/report.md`."),
    ]

    os.makedirs(WAVE_DIR, exist_ok=True)
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES}
             for t in tasks]
    spec = {"wave": "r46-w1", "milestone": MILE, "reportDir": REPORT,
            "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path],
                          capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s"
                         % (proc.returncode, proc.stdout[:600], proc.stderr[:600]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {}
    for t in wave_tasks:
        members[t["name"]] = {"kind": "spawn", "agentId": None, "role": t["agent"],
                              "item": None, "axes": AXES, "milestone": MILE}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": "r46-w1",
        "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1",
                     "path": ".ufo/waves/round-46/w1/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None,
                                              "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0,
                                              "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": ("Issue exactly one batched task call with taskCall ({context, tasks}); "
                 "never split a wave into multiple task calls (one-swarm-per-wave)."),
    }
    with open(os.path.join(WAVE_DIR, "w1-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w1"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w1/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": "r46-w1",
                   "reportDir": REPORT, "members": members}, f, indent=1)
    ready_path = os.path.join(WAVE_DIR, "w1.ready")
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
        print("wrote", len(wave_tasks), "seats;",
              dict(collections.Counter(t["agent"] for t in wave_tasks)))
        print("counts", plan["counts"])
        return
    with open(ready_path, "w") as f:
        json.dump({"lane": "kaidoku", "round": 46, "wave": "r46-w1",
                   "dispatch": os.path.join(WAVE_DIR, "w1-dispatch.json"),
                   "l1": "KaidokuR46"}, f)
    print("wrote", len(wave_tasks), "seats;",
          dict(collections.Counter(t["agent"] for t in wave_tasks)))
    print("counts", plan["counts"])


if __name__ == "__main__":
    main()
