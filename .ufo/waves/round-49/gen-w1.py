#!/usr/bin/env python3
"""Generate the round-49 wave-1 spec (v1 policy, pre-freeze draft attack), validated dispatch, ready file."""
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-49")
BASE = "e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
WAVE = "r49-w1"
MILE = ("Round 49 wave 1 (pre-freeze): attack and verify the DRAFT claim instruments and plan, "
        "re-open sources, draft landing text; findings are folded in before the single freeze")
REPORT = ".ufo/waves/round-49/w1"
W = REPORT + "/"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r49/"
DRAFT = ROOT + "/.ufo/waves/round-49/draft"
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"

CTX = f"""# Target
kaidoku-shokunin round 49, wave 1 of 2 = the PRE-FREEZE attack: verify, attack and falsify the DRAFTS of the round's two claim instruments and plan, re-open sources, and draft landing text, BEFORE the single freeze and before any data run. Lane root (absolute): {ROOT}. L1 = KaidokuR49 (integration owner; it holds the section-3 planner seat \u2014 the validator rejects `planner` as a swarm role, so planning data-walks ride scout/connector/revenger seats). Base revision `{BASE}`.

# The two claims (the plan is the rule \u2014 read it, not this prompt)
- **R49-C1 coverage**: SquashFS v1/v2 (`squashfs_v1`, `squashfs_v2`, four frozen standard fixtures, both byte orders) Frontier -> Core through REA 6.5.0 `extract-firmware`, scored by `c1-counter.py` (the round-44 counter ported; round 44's claim stopped because plan text and counter disagreed about receipt provenance \u2014 this round states it once).
- **R49-C2 calibration**: nine round-48 self-assessment mismatches (atoms A1-A9, from the round-48 closure `{ROOT}/corpus/lessons/round-48-verifier-spotcheck.md` "Routed defects"), counted by `c2-mismatch.py`; target `mismatches 0` with an in-counter mutation battery; at the freeze it reads 9.
Plan draft: **`{DRAFT}/plans/round-49-claims.md`**. Counter/tool drafts: **`{DRAFT}/tools/round-49/`** (`c1-counter.py`, `c1-run.py`, `c1-run.sh`, `c1-controls.py`, `c1-oracle.py`, `carriers.json`, `c2-mismatch.py`). C1 landing-text drafts: `{ROOT}/.ufo/waves/round-49/w1/artifacts/R49C1Doc/` and `.../R49EntryDraft/`. Helpers: `{DRAFT}/mkclone.sh <dest>` builds a scratch clone at the base with the draft tools committed as a throwaway "dev freeze" (prints `DEV_FREEZE=<hash>`); `{DRAFT}/c2-after.py <clone>` builds the GREEN C2 fixture in it (prints `DEV_AFTER=<hash>`); `{DRAFT}/run-ctl.sh <clone> <workdir>` runs the C1 controls driver. Source snapshots: `{DRAFT}/snapshots/`. REA 6.5.0 package root: `{PKG}`. Read the plan in full before your first command.

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside `{ROOT}/{W}<YourSeatName>/` (create it) and your report file `{ROOT}/{W}<YourSeatName>.md`. Never edit the draft tools/plan/docs, `SKILL.md`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `plans/`, `tools/`, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command in the lane or fleet repo. Read-only git (`log`, `show`, `diff`, `ls-tree`, `rev-parse`, `cat-file`, `merge-base`) is fine.
- **Drafts are read-only.** To mutate, copy to scratch (use `mkclone.sh`). A finding that a draft clause is vacuous, satisfiable by a forgery, or disagrees with its plan sentence is the most valuable thing you can return: give the exact command, the differing value, and a fixture path.
- **Fixture repos**: `mkclone.sh` does it for you. Any other fixture repo: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, every later git call names `-C "$D"`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; set `user.name`/`user.email` in that clone only. Never run `git commit` with a throwaway identity anywhere else (run-6 incident: a seat's fixture commit landed on the FLEET repo and deleted 4,606 paths).
- **Scratch**: `S={SCRATCH}<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S" HYAKU_SCRATCH={SCRATCH.rstrip('/').rsplit('/', 1)[0]}`. Remove `$S` before you yield AFTER copying receipts into `{W}<YourSeatName>/`. Never write under `/tmp`; nothing under `/tmp` is citable. Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256 and UTC time. A check you did not run is not passed \u2014 say "not run". Never fabricate output.
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate. A 2 never counts toward a target.
- **Absolute paths**: your tools start at the fleet root, not the lane. The `Report:` trailer path in your prompt is relative to `{ROOT}` \u2014 write it at `{ROOT}/<that path>` (that is `{ROOT}/{W}<YourSeatName>.md`). A file written at a relative path lands in the FLEET repo and is a defect.
- **Tooling authorization (operator, 2026-10-19)**: you may install/upgrade tools that help the task; first read `/home/vgpnk/.omp/agent/RULES.md` (official channels, update-safety gate; record tool/version/channel/reason in your report). **pacman guard**: all pacman transactions are PAUSED host-wide \u2014 install only via `uv tool`/`npx`/an official binary in `~/.local/bin`, or nothing. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `/home/vgpnk/Projects/shokunin/.scratch/`, or the fleet repo. Never run `c1-run.sh --data-run` (the L1 runs data after the freeze).
- Return a final message of at most 8 lines: your verdict, the 1-3 most important findings, your report path.

# What the L1 does with your output
It reads every report, folds real defects into the drafts, then commits the ONE freeze (plan + tools + control fixtures), runs the data procedure, lands the evidence and docs, and dispatches wave 2 against the FROZEN bytes. Do not try to "fix" the drafts; report.
"""

T = []


def add(name, agent, task):
    t = GODSPEED + task + (
        "\n\nWrite your findings to `<ROOT>/<W><SEAT>.md` (verdict first, then a findings table "
        "with exact commands, exit codes, sha256s); extra artifacts under `<ROOT>/<W><SEAT>/`.")
    T.append({"name": name, "agent": agent,
              "task": t.replace("<ROOT>", ROOT).replace("<W>", W).replace("<SEAT>", name)
              .replace("<DRAFT>", DRAFT).replace("<BASE>", BASE).replace("<PKG>", PKG)})


# ---------------------------------------------------------------- C1 instrument attacks
add("C1PortAudit", "reviewer",
    "R49-C1 port audit. Diff `<ROOT>/tools/round-44/{c1-counter.py,c1-run.py,c1-run.sh,c1-controls.py,c1-oracle.py,carriers.json}` "
    "against `<DRAFT>/tools/round-49/` of the same names. List EVERY delta and classify it mechanical (round 44 -> 49 token) or "
    "non-mechanical. Then find every remaining `44`/`r44`/`R44` token and decide whether it is an intended round-44 reference "
    "(oracle trees, carrier custody, history) or a stale one that would make a round-49 run read round-44 state. A stale one is a defect.")
add("C1ProvCritic", "critic",
    "Attack the receipt-provenance clause of R49-C1 (the clause round 44 stated two ways). Read the plan's P49-C1 sentence and the "
    "counter code that implements `parameters.output_directory` / evidence-id minting / `/kaidoku-r49/` segment / `provenance.json`. "
    "Questions: (1) does the plan sentence say exactly what the code checks? (2) can a receipt whose output_directory is inside "
    "`/kaidoku-r49/` but was produced by a fake REA satisfy it? (3) can the committed round-44 receipts, re-minted over a "
    "`/kaidoku-r49/` path, pass without a real run? Build the fixture for each in a scratch clone and score it with the draft counter.")
add("C1CtlDoNothing", "executor",
    "Run the do-nothing controls for R49-C1 on a scratch clone (`mkclone.sh`): (a) the counter at the dev freeze with no receipts "
    "(`--rev` = DEV_FREEZE): expect exit 1, `carriers_matched 0`; (b) the cheapest shortcut: copy the committed round-44 after-receipts "
    "`<ROOT>/corpus/evidence/round-44/c1/<id>/after.json` to `corpus/evidence/round-49/c1/<id>/after.json` in the clone, commit it, "
    "score it: expect non-zero. Record both receipts with the failing clause names. If (b) reaches `carriers_matched 4`, that is the "
    "kill rule: say so loudly with the exact command. Use `python3 -I -B tools/round-49/c1-counter.py --root <clone> --rev <rev> --freeze <DEV_FREEZE> --pkg65 <PKG> --work $S/work --json-out $S/out.json`.")
add("C1SelfTest", "executor",
    "Run `python3 -I -B <DRAFT>/tools/round-49/c1-counter.py --selftest --work $S/self` (offline). Record case count, failures, exit code, "
    "wall time. Then run `--selftest` three more times and show the output JSON is stable (digest equal modulo wall time). Then list the "
    "selftest cases by name and tell the L1 which frozen CLAUSES (the counter's `CLAUSES` and `BINDINGS` tuples) have NO selftest case that "
    "reds when that clause is false. Return that gap list.")
add("C1DevArmRepeat", "executor",
    "Run the positive development arm three times on a fresh `mkclone.sh` clone: `python3 -I -B tools/round-49/c1-counter.py --dev-arm --root <clone> --run-rea --pkg65 <PKG> --work $S/devarm<N> --json-out $S/devarm<N>.json` "
    "(real REA 6.5.0 `extract-firmware` on the four carriers, scratch only). Compare the three runs: dev_matched, per-carrier handler, "
    "published files, gap kinds, evidence ids. Report any run-to-run difference (that would make the counter-time rerun-projection clause flaky). Record wall times. "
    "Never write outside `$S`.")
add("C1OracleIndep", "executor",
    "Independent oracle re-derivation. For the four carriers named in `<DRAFT>/tools/round-49/carriers.json` (files under `<ROOT>/corpus/evidence/round-42/c2/fixtures/`): "
    "extract each with `/usr/bin/unsquashfs` and, if it reads them, `/usr/bin/7z`, into `$S`; compute member sha256/size/relative path; compare with the "
    "`oracle.census` in carriers.json and with the unblob `__output__` trees under `<ROOT>/corpus/evidence/round-44/oracle/`. Report every disagreement and "
    "whether `7z` agrees with `unsquashfs` (the counter treats unsquashfs as the oracle; say if 7z refuses and why).")
add("C1CarrierPins", "scout",
    "Carrier custody sweep. For each of the four carriers: sha256 of the committed fixture file, the pin in carriers.json, the pin in "
    "`<ROOT>/tools/round-42/fixtures.json` (if present), the committed copy under `<ROOT>/corpus/evidence/round-44/carriers/`, and the unblob 26.6.4 upstream fixture "
    "name. Open `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` (and the raw input blob URL for one carrier) and record the "
    "HTTP status and whether the committed bytes equal the upstream `__input__` bytes (sha256). Report mismatches only with evidence.")
add("C1S138Reopen", "scout",
    "Re-open source row S138 (`<ROOT>/corpus/SOURCES.md`) for the round-49 gate. Open its URL(s) today, record access date (UTC), HTTP status, and a <=25-word located quote "
    "from the page that grounds the row's `teaches`. Check the row's pinned sha256/manifest still describes what the committed oracle trees hold (`<ROOT>/corpus/evidence/round-44/oracle/manifest.json`). "
    "Give the exact text the lesson `## Gate` should carry for S138 (URL, date, quote with location). Do not edit the registry.")
add("C1S139Reopen", "scout",
    "Re-open source row S139 (`<ROOT>/corpus/SOURCES.md`): the squashfs-tools release page. Open it today, record access date (UTC), HTTP status, the `4.7.5` tag evidence with "
    "a <=25-word located quote, and `/usr/bin/unsquashfs` self-report (`unsquashfs -version` exits 1: parse stdout) plus its sha256 against the row/carriers.json pin. "
    "Give the exact text the lesson `## Gate` should carry for S139. Do not edit the registry.")
add("C1CounterMut", "mutation-tester",
    "Mutation-test the DRAFT `c1-counter.py` offline. In a `mkclone.sh` clone, mutate the counter source one clause at a time (at least 15 mutations: drop a clause from "
    "`CLAUSES`, make a comparison always true, widen a segment test, accept a gap, skip the rerun projection, ignore handler, skip superblock probe, drop the freeze-walk, etc.) and run "
    "`--selftest` for each. Report which mutations SURVIVE (selftest still exit 0). For each survivor say whether a red control (CTL-C1-0..5) would still catch it by running "
    "`<DRAFT>/run-ctl.sh` against a clone with the mutated counter committed as its dev freeze. A survivor no control catches is a finding.")
add("C1GoldForgery", "critic",
    "Gold-forgery attack on R49-C1: construct, in a scratch clone, the CHEAPEST input tree that makes the draft counter report `carriers_matched 4` with every binding true "
    "WITHOUT a genuine REA run (fabricated envelope re-minted by the package's own digest code, a copied round-44 receipt with the path rewritten, hollow PROVINCE/README/entry text, "
    "a scratch segment that is a directory name only). Score each attempt. If any reaches 4/4 + every binding true it is the kill rule: report the fixture and the exact command. "
    "Otherwise report which clause stopped each attempt (this is the evidence the claim cannot be met by a do-nothing).")
add("C1DocBindings", "critic",
    "Attack the five documentation bindings (`province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row`). For each, write the "
    "hollowest text that satisfies it (e.g. a PROVINCE row that names the two handlers and cites the entry path but says nothing true). Score with the draft counter in a clone "
    "that carries genuine scratch receipts (`--dev-arm` receipts planted via `<DRAFT>/run-ctl.sh`'s POS pipeline, or your own). Report which bindings are satisfiable by hollow text; "
    "the L1 will state that limit in the plan rather than claim it is closed.")
add("C1TmpScratch", "reviewer",
    "Scratch-discipline audit (operator directive 2026-10-25, section 7 of the round prompt). grep every file in `<DRAFT>/tools/round-49/` for `/tmp`, `tempfile`, `mkdtemp`, "
    "`gettempdir`, `TMPDIR`, `HYAKU_SCRATCH`, `/fast/scratch`. For each hit decide: honours `TMPDIR`/`--work`? hardcodes a path? writes outside the lane evidence root and the scratch segment? "
    "A tool that writes under `/tmp` regardless of TMPDIR is a routed defect. Also run each tool's `--help` (not `--data-run`) and confirm it makes no write.")
add("C1RunReview", "reviewer",
    "Review `<DRAFT>/tools/round-49/c1-run.py` and `c1-run.sh`. Run `c1-run.sh --dry-run` from a clone (use `--lane-root <clone>` and `--evidence-root $S/ev` so nothing is written into the lane) "
    "and show the four carrier ids, the output_directory it would use (must be inside `/kaidoku-r49/`), the evidence paths (`corpus/evidence/round-49/c1/<id>/`), the data-run guard "
    "(refuses without `--data-run`/`KAIDOKU_C1_DATA_RUN=1`), and `--force` semantics. List every way the data run could write outside `corpus/evidence/round-49/c1/` or the scratch segment. "
    "Do NOT run `--data-run`.")
add("C1ControlsReview", "reviewer",
    "Review `<DRAFT>/tools/round-49/c1-controls.py` and run `<DRAFT>/run-ctl.sh` on a fresh clone (work dir under your scratch). Confirm all seven controls print the expected verdict "
    "(CTL-C1-0..5 `as_expected` with exit 1, CTL-C1-POS exit 0). Then check: is CTL-C1-4 really the committed round-44 receipts of the same bytes relabelled (compare sha256 of the planted "
    "files with `<ROOT>/corpus/evidence/round-44/c1/<id>/after.json`)? Is each control's planted tree committed in the sandbox only? Does any control leave anything in the lane tree? "
    "(`git -C <ROOT> status --porcelain` must show nothing you caused.)")
add("C1RunMut", "mutation-tester",
    "Mutation-test the provenance part of `<DRAFT>/tools/round-49/c1-run.py` and the counter's provenance clause together. In a clone, apply 8+ single mutations to the RUNNER "
    "(use `--rea-outdir-mode evidence` so the receipt names the evidence path; drop `provenance.json`; copy a tree that is not byte-identical; record a wrong `rev_at_run`; "
    "point the scratch segment at `/kaidoku-r44/`) using the runner's `--fake-rea` option if present or its dry-run output, and score what the counter does with each resulting tree. "
    "Report mutations the counter ACCEPTS (a receipt produced the wrong way that still scores 4/4).")
add("C1Sentinel", "sentinel",
    "Security review of `<DRAFT>/tools/round-49/c1-run.py`/`c1-run.sh` and the unblob tee it generates: path traversal or symlink escape when it copies REA's produced tree verbatim "
    "into the evidence root (a symlink in an extracted tree pointing outside), privilege/exec surfaces (`REA_UNBLOB_COMMAND` tee, `npx -y rea-agents@6.5.0`), anything that could write "
    "outside the evidence root or scratch, anything that executes content from an extracted tree. Reproduce any finding on a fixture in scratch; do not run the data procedure.")
add("C1R44Revenge", "revenger",
    "Reverse-engineer why round 44's R44-C1 stopped, from bytes. Read `<ROOT>/plans/round-44-claims.md` R44-C1, `<ROOT>/corpus/lessons/round-44.md`, "
    "`<ROOT>/tools/round-44/c1-counter.py` and `<ROOT>/corpus/lessons/round-44-verifier-spotcheck.md` (if present). Build a clause-by-clause table: plan sentence fragment -> "
    "counter code (function, line) -> agrees / disagrees / unchecked. Do the same for `<DRAFT>/plans/round-49-claims.md` P49-C1 against the draft counter. Any fragment that is "
    "`disagrees` or `unchecked` in the round-49 table is a defect that would repeat round 44: list each.")

# ---------------------------------------------------------------- C1 landing-text drafts
add("C1ScribeEntry", "scribe",
    "Draft the round-49 knowledge entry text. Start from `<ROOT>/.ufo/waves/round-49/w1/artifacts/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` "
    "(the round-44 pre-stop draft, mechanically ported). Write `<ROOT>/<W><SEAT>/entry.md`: the full entry with `status:` stating the round-44 stop in one sentence (cite "
    "`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`), `source:` lines for S138/S139 (+S112), `verified-at:`, `recheck:`, and measured values left as "
    "`<MEASURED: name>` markers ONLY where they depend on the after-freeze data run. Every number must carry its command. List every marker at the end. Do not touch the repo entry path.")
add("C1ScribeProvince", "scribe",
    "Draft the three landing blocks and verify them against the draft counter's regexes: `## Round-49 additions to Core` section with one row naming `squashfs_v1` and "
    "`squashfs_v2` and citing `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` (counter: `province_core_row`, `SQFS12_TEXT_RE`); the one-line `Round-49 frontier note, 2026-10-28:` that "
    "carries the entry stem and a SquashFS v1/v2 token and says it supersedes the round-44 `measured, not promoted` note; the README `## Coverage map` row. Start from "
    "`<ROOT>/.ufo/waves/round-49/w1/artifacts/R49C1Doc/`. Write `<ROOT>/<W><SEAT>/block-a.md`, `block-b.md`, `block-c.md`; leave `<AFTER-DATA: ...>` markers only where the "
    "headline is the after-data receipt. Run the counter's own regex against each block in a scratch Python session and paste the match evidence.")
add("C1ScribeSources", "scribe",
    "Draft the SOURCES.md registry edits for C1 without touching the registry: for rows S138 and S139, the exact new `used-by` cell (append `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` "
    "to the existing cell; show old -> new), and confirm `opened` stays `2026-10-28` (the counter's `OPENED`). Draft the lesson `## Gate` rows for S138/S139 (URL, access date, <=25-word "
    "quote with location) from the re-open seats' reports if they exist at `<ROOT>/<W>C1S138Reopen.md` and `<ROOT>/<W>C1S139Reopen.md` (wait for them by reading; if absent, read the sources yourself). "
    "Run the census-shaped awk from `/home/vgpnk/Projects/shokunin/CORPUS.md` section SOURCES on a scratch copy with your edited rows and show NF=13 and no missing used-by path.")
add("C1DocCheck", "executor",
    "Doc-binding dry run. Build a clone (`mkclone.sh`), run `<DRAFT>/run-ctl.sh <clone> $S/w` and confirm CTL-C1-POS exits 0 with every documentation binding true (it plants the R49C1Doc blocks, "
    "the R49EntryDraft entry and the S138/S139 used-by append). Then mutate ONE doc at a time in your own copy of the doc dir (point `--doc-dir`... via the run-ctl.sh extra args): remove the "
    "heading, drop `squashfs_v2` from the row, drop the entry path, drop the frontier-note stem, drop S139 from the entry's `source:`, drop the README row; show each flips exactly its own "
    "binding red and exit non-zero.")

# ---------------------------------------------------------------- C2 attacks
add("C2RederiveA", "executor",
    "Independent re-derivation of atoms A1-A3 (do NOT import the counter). From read-only git objects of `<ROOT>` (`git show <BASE>:<path>`): A1 the freeze the SCORECARD `## Round 48` "
    "declares vs the one `corpus/lessons/round-48.md` names in its header (and the A1-A8 rows the lesson itself lists); A2 whether `663f30ee7516942a0120e7de68fe88356e680822` is a commit and "
    "which commit shares its 8-hex prefix; A3 the full set of LOG.md line numbers (at base) naming `2e785632`, `33f65a91`, `577a02a5`, `8847042a`. Write your own derivation script and "
    "compare its numbers with the draft lesson lines produced by `<DRAFT>/c2-after.py` (read that script). Report every disagreement.")
add("C2RederiveB", "executor",
    "Independent re-derivation of atoms A4-A6 (do NOT import the counter). A4 from `<ROOT>/.ufo/waves/round-48/r48-w1-results.json` and the committed `.ufo/waves/round-48/w1/` tree at base: seats, "
    "seats with a report artifact (a `.md` at `w1/<seat>.md` or under `w1/<seat>/`), the seats without. Cross-check against the closure's own count (72/75; missing C1Meaning, C1Battery, ScribeReportNumbers) "
    "in `<ROOT>/corpus/lessons/round-48-verifier-spotcheck.md`. A5 raw and newline-stripped sha256 of `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json` and `c2-final-33f65a91.json`, and which digests "
    "the round-48 fleet report quoted (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md`, read-only). A6 open the committed snapshot `<DRAFT>/snapshots/popper.html` and "
    "locate the quote \"falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific\" and the h2/h3 heading above it. Report disagreements with the draft.")
add("C2RederiveC", "executor",
    "Independent re-derivation of atoms A7-A9 (do NOT import the counter). A7 open `<DRAFT>/snapshots/sysexits.html`, confirm `EX_USAGE 64` and the 22-word quote "
    "\"The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, bad syntax in a parameter, or whatever.\" are present after tag stripping, and fetch "
    "`https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` today to compare sha256 with the snapshot. A8 derive, from `git show` of `corpus/SOURCES.md` at "
    "`61b87d742032e65fca9c38267d7d6ed7e555edad`, `8847042a140b044dbf335210c965bf7b06b09b4f` and `<BASE>`, the registry row counts and the new-id included/excluded split. A9 confirm "
    "`corpus/lessons/round-48-verifier-spotcheck.md` states `rejected-harmed` and a `| calibration | harmed |` axis row. Report disagreements with `c2-after.py`.")
add("C2CounterMut", "mutation-tester",
    "Mutation-test `<DRAFT>/tools/round-49/c2-mismatch.py` beyond its built-in battery. Build the green fixture (`mkclone.sh` + `c2-after.py`). Apply at least 20 mutations to the COUNTER source "
    "(delete a check inside an atom, weaken a comparison, swap `and`/`or`, skip the append-only blob compare, drop the freeze walk, accept an absent lesson line) and run the counter with `--battery` against "
    "the green fixture for each. A mutation is KILLED when the genuine run or the battery goes red; report every SURVIVOR with the exact diff. Also try 10 fixture-side forgeries (right strings, wrong facts) "
    "and report which atoms accept them.")
add("C2GoldForgery", "critic",
    "Gold-forgery attack on R49-C2: find the cheapest repository state that makes the draft counter report `mismatches 0` and `battery.failing []` while the underlying facts are wrong "
    "(e.g. a correction line whose numbers are re-derived from a file the forger also edited, an overlay-based do-nothing that is vacuous, snapshots whose bytes were edited and re-pinned, "
    "search-log entries that match derived counts of a different range). Build each on a scratch clone and score it. Anything green is a finding with the fixture and command.")
add("C2PlanMatch", "reviewer",
    "R49-C2 plan <-> counter match (the round-44 failure class: claim text and counter disagreeing). Table each sentence of P49-C2 and of the atom list in the plan against the "
    "docstring and the code of `<DRAFT>/tools/round-49/c2-mismatch.py` (function, line): agrees / disagrees / unchecked. Include the numbers (9 atoms, 11 mutations, `mismatches 9` at the freeze). "
    "Run the counter at DEV_FREEZE from a clone and show the observed `mismatches` and exit code. Every `disagrees`/`unchecked` is a defect to fix before the freeze.")
add("C1PlanMatch", "reviewer",
    "R49-C1 plan <-> counter match (the round-44 failure class). Table each clause of P49-C1 and each control/target sentence in `<DRAFT>/plans/round-49-claims.md` against "
    "`<DRAFT>/tools/round-49/c1-counter.py` (function, line, the `CLAUSES`/`BINDINGS` name it maps to): agrees / disagrees / unchecked. Especially: the provenance sentence, the "
    "`Round-49 frontier note` mark, `opened 2026-10-28`, `used-by`, the controls list vs `c1-controls.py`. Every `disagrees`/`unchecked` is a defect to fix before the freeze.")
add("C2LogPtr", "reviewer",
    "Review atoms A3 and A4 against the closure's text. Read `<ROOT>/corpus/lessons/round-48-verifier-spotcheck.md` \"Step-1 conformance\" and \"Routed defects\" 7 and 8. For each statement the closure makes "
    "about LOG.md pointers and the 72/75 wave accounting, re-derive it from git at base. Then check the draft counter encodes the SAME definition (report artifact = `.md` at `w1/<seat>.md` or under "
    "`w1/<seat>/`; LOG line sets from the base blob). Find any definition under which the closure and the counter would disagree, and any lines the closure cited that the counter does not cover.")
add("C2SourcesReopen", "scout",
    "Re-open the two sources behind rows S147/S148 independently. Fetch `https://plato.stanford.edu/entries/popper/` and `https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` today; record "
    "HTTP status, byte count, sha256 (compare with `<DRAFT>/snapshots/*.html`: equal or different, and if different diff the quoted passages), the section heading above the Popper quote, and the "
    "`EX_USAGE` definition lines. Also search the Popper page for the text after the quote (the clause that says the criterion's verdict, `is unscientific`) and tell the L1 whether a <=25-word quote can carry it. "
    "Return exact locator strings for the registry rows.")
add("C2FleetSweep", "scout",
    "Read-only sweep of the round-48 fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md`: extract every 40-hex hash, every LOG.md line pointer, every file path, every "
    "sha256; resolve each against `<ROOT>` at `8847042a140b044dbf335210c965bf7b06b09b4f` (`git cat-file -e`, `git show`, line grep). Table: citation | resolves? | note. The closure found 15/16 hashes "
    "resolving; confirm, and list any further defect the closure did not name. This is a sweep with its command and output, not an opinion.")
add("C2SelfAssess", "scout",
    "Self-assessment sweep (routing only, no fixes). Compare what `<ROOT>/SCORECARD.md` (Owned axes table and the Round 48 section), `<ROOT>/SHONEN.md` and `<ROOT>/LOG.md` (round 48 entry) "
    "SAY about round 48 against observed state: the closure verdict (rejected-harmed), the calibration score cell, wave counts, 'dead seats 0', SHONEN pointers. List up to 12 additional "
    "mismatches beyond atoms A1-A9, each with both quotes (file:line) and the command that shows the disagreement. These are candidates for next round; do not rank them as claims.")
add("C2SearchLog", "reviewer",
    "Review atom A8 (search log). Read `<ROOT>/corpus/SOURCES.md` `## Search log` entries (format; last entry round 33) and the contract in `/home/vgpnk/Projects/shokunin/CORPUS.md` rule 5. "
    "Check the draft entries produced by `<DRAFT>/c2-after.py` for rounds 48 (late) and 49 meet the contract (question, where searched, date, identified/screened/included/excluded, exclusion "
    "reasons, stop rationale), and that the counter derives `rows B -> A` and included/excluded from git. Check the derived numbers for round 48 yourself: rows at `61b87d74` vs `8847042a`. "
    "List contract elements the counter does not check and the L1 must write by hand.")
add("C2ScribeCorrections", "scribe",
    "Draft the C2 landing text in full, real values, no markers: `<ROOT>/<W><SEAT>/lesson-corrections.md` (the `## Corrections to round 48` section with lines A1-A7 in the exact "
    "`- A<n> key=value` format the counter parses; read `<DRAFT>/c2-after.py` for the shape and re-derive every value from git yourself), `scorecard-section.md` (the `## Record corrections — round 49` "
    "section with the A9 line plus 3 sentences of honest prose: calibration was harmed at round 48 per the closure, what the corrections repair, what stays routed), and `search-log.md` (the two "
    "search-log entries, contract-complete). Run `<DRAFT>/c2-after.py`-style verification: build a clone, apply your text, run the draft counter with `--battery` and paste the result.")
add("C2ScribeSources", "scribe",
    "Draft registry rows S147 and S148 (supersedes S145 / S146) to the house schema (11 cells, no `|` inside a cell), with sha256-pinned snapshots under "
    "`corpus/evidence/round-49/c2/`, from `<DRAFT>/snapshots/` and the exact locators the re-open seats find (`<ROOT>/<W>C2SourcesReopen.md` if present; else open the pages yourself). "
    "The quote must be <=25 words and present in the snapshot after tag stripping; the anchor names the heading above it. S148 `teaches` must state EX_USAGE is 64 and that the lane's 0/1/2 meanings are its own convention. "
    "Also draft the lesson `## Gate` block (S147 admit, S148 admit, S145/S146 left untouched; the round-48 closure's spot-check disagreements recorded; at least one reject from this round's candidates with reason and flip). "
    "Write `rows.md` and `gate.md`. Verify with a scratch registry copy and the census awk lines.")

# ---------------------------------------------------------------- cross
add("ConnSibling", "connector",
    "Sibling-overlap scan. Does another shokunin lane's PROVINCE/knowledge hold SquashFS, unblob, sasquatch, firmware-extraction or REA material that overlaps R49-C1, or source-curation "
    "/ self-assessment-calibration tooling that overlaps R49-C2? Search `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` and `corpus/knowledge/` read-only (grep SquashFS|unblob|sasquatch|firmware). "
    "Table: lane | path:line | overlap | verdict (adjacent: report, not absorb / none). Also name the one place this lane's C2 counter and another lane's instrument do the same job, if any.")
add("ConnSeparability", "connector",
    "Prove or break causal separability of R49-C1 and R49-C2. Build two scratch clones: X carries ONLY the C1 landing (POS tree from `<DRAFT>/run-ctl.sh`'s pos output + docs) and Y carries ONLY the C2 landing "
    "(`c2-after.py`). Score C1 on X and on Y, C2 on X and on Y (each at its own dev freeze). C1 must be green on X only, C2 green on Y only, and neither counter may read a path the other claim's landing writes "
    "(list each counter's read set by tracing its `show`/`git show` paths). Report any shared path (SOURCES.md is expected: confirm which rows each reads).")
add("CritFreeze", "critic",
    "Attack the freeze-integrity rule. The freeze commit will contain `plans/round-49-claims.md` and `tools/round-49/**`. After it, the L1 runs `c1-run.sh --data-run` (writes `corpus/evidence/round-49/c1/**`), "
    "lands docs and runs both counters. In a clone, try: touching a tools file after the freeze and restoring it (merge-aware walk must still refuse), adding a new file under `tools/round-49/`, "
    "editing `carriers.json` in a merge commit, a rename. Score both counters on each (C1 walk vs C2 walk). Report any manoeuvre one counter refuses and the other accepts, or any that neither catches.")
add("ScoutPriorClosures", "scout",
    "Read the last three closures (`<ROOT>/corpus/lessons/round-46-verifier-spotcheck.md`, `round-47-...`, `round-48-...`). For every routed defect/recommendation in each, decide against the repo at `<BASE>`: "
    "fixed / still open / declined, with the evidence pointer. Output a table: closure | defect id | status | evidence. The L1 needs the list of still-open ones to decide what round 49 repairs and what it "
    "routes (the plan already repairs round-48 defects 1-4, 7, 8 and routes 5-6).")
add("ScoutAssimilation", "scout",
    "Read-only look at the assimilation package for this lane: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (`MERGE-REPORT.md`, `SOURCES.append.md`, knowledge entries) and "
    "`<ROOT>/considerthese/` (expected absent). Never run any campaign tool there. Report: is there a theme/entry that matches the lane's PROVINCE and could be adopted in a round that is "
    "not an assimilation round? List the staged entries, their target paths and whether any overlaps SquashFS/firmware. The L1 plans `Assimilation: none` unless you find an entry that is cheap, in-province, and not already held.")
add("ReviewerQuality", "reviewer",
    "QUALITY-bar review. Read `<ROOT>/corpus/QUALITY.md` (rows 70-79 especially) and apply the rows that bind a new knowledge entry, a SOURCES row and a lesson to the round-49 drafts "
    "(`R49EntryDraft`, the S147/S148 rows `c2-after.py` writes). List each applicable criterion, whether the draft meets it, and propose the exact text of ONE new QUALITY row for the round-49 "
    "mined mistake M49-1 (reference-drift: the round-48 lesson header named an amended-away freeze; captured-by none; the fix is atom A1 + its mutation).")
add("ExecFreezeDry", "executor",
    "Full freeze dry run. Build a clone (`mkclone.sh`), then: (1) score C1 and C2 at DEV_FREEZE (expect C1 exit 1 `carriers_matched 0`; C2 exit 1 `mismatches 9`); (2) `<DRAFT>/run-ctl.sh` (expect 7/7 as expected); "
    "(3) `c2-after.py` then C2 with `--battery` (expect exit 0, 11 mutations killed, do-nothing red x9); (4) `c1-run.sh --dry-run` against the clone. Record every command, exit code, stdout sha256 in a table. "
    "Anything that differs from the expectation is a defect; list the L1 steps that would be needed to commit the freeze (which paths must be in the freeze commit: tools, plan, control-fixtures, controls receipts).")
add("ExecRunbook", "executor",
    "Write the L1 runbook for the after-freeze phase as an EXECUTABLE script `<ROOT>/<W><SEAT>/after-freeze.sh` (not run by you, except with `--dry-run` where supported): "
    "(a) pre-checks (`jj-lane.sh state`, freeze is ancestor of HEAD, tools frozen blobs unchanged); (b) `tools/round-49/c1-run.sh --data-run` with scratch under `/fast/scratch/hyaku/kaidoku-r49/l1`; "
    "(c) the exact counting commands for C1 and C2 with `--json-out` into `.ufo/waves/round-49/l1/scores/`; (d) the census command before/after; (e) the misroot sweep. "
    "Verify the C1 commands by running each with `--dry-run`/`--help` or on a clone; paste the resolved argv. Flag any step that would write outside the lane evidence root, the wave dir or scratch.")
add("C1ScribeLesson", "scribe",
    "Draft the round-49 lesson skeleton `<ROOT>/<W><SEAT>/lesson-skeleton.md` for `corpus/lessons/round-49.md`: header (base, FREEZE placeholder `<FREEZE>` to be filled by the L1 after the freeze commit exists, "
    "stating the freeze is ONE commit and there is no amendment series), `## Mistakes` with M49-1 (class `reference-drift`; evidence `corpus/lessons/round-48.md:4` vs `SCORECARD.md` Round 48 declared freeze; captured-by none; fix atom A1 with "
    "mutation `A1 swap declared/stale` shown red) and a second row for any further mistake the seats' reports surface (leave a marker), `## Gate` (assimilation none with the sweep command; considerthese absent), "
    "`## Corrections to round 48` placeholder pointing at `C2ScribeCorrections`, `## Census before -> after` with the round-start census output already recorded at "
    "`<ROOT>/.ufo/waves/round-49/l1/sources-census-start.txt` (read it and paste exit code and the final line), `## Routed defects` (round-48 defects 5 and 6 declined with reasons: round-48 claims stay frozen).")
add("C1Simplify", "simplifier",
    "YAGNI check on the round-49 instrument set. Is every file in `<DRAFT>/tools/round-49/` needed by a claim, a control or the data run? Is `c1-oracle.py` needed at score time or only to build "
    "carriers.json (then it is evidence, not an instrument)? Is any dead code path in `c2-mismatch.py` (e.g. the `Overlay.ls` branch, unused helpers) unexercised by the battery? List removals that would NOT change "
    "any verdict (prove by running both counters on the green fixture with the removal) and anything that is unreachable. Do not edit the drafts.")
add("C2MutAtoms", "mutation-tester",
    "Fixture-side mutation test of the nine atoms on the GREEN fixture (`mkclone.sh` + `c2-after.py`). For each atom write 3 distinct fixture mutations of the committed bytes (not the counter): "
    "change a number, move a pointer, swap two ids, truncate a quote, rewrite a hash by one hex digit, re-pin a snapshot, delete a row, reorder sections. Score each with the draft counter. Report every "
    "mutation that stays green (an undetected change to the record) with the exact diff. Target: 27 mutations.")
add("C1Frontier", "scout",
    "Frontier read for the round-49 report: from `<ROOT>/PROVINCE.md` Frontier and `<ROOT>/corpus/README.md` `## Frontier`, list the sasquatch/SquashFS items still Frontier AFTER this round's promotion "
    "(`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3, v4 Broadcom, LE AVM, AVM kernels, nested sub-images below depth 1) with the one cheapest next probe for each (a "
    "tool/fixture that exists on this host or upstream under unblob 26.6.4 `tests/integration/filesystem/squashfs`). Verify each named fixture exists upstream by opening the listing; do not run extractions.")


def main():
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES} for t in T]
    spec = {"wave": WAVE, "milestone": MILE, "reportDir": REPORT, "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path], capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s" % (proc.returncode, proc.stdout[:1200], proc.stderr[:1200]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {t["name"]: {"kind": "spawn", "agentId": None, "role": t["agent"], "item": None,
                           "axes": AXES, "milestone": MILE} for t in wave_tasks}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": WAVE, "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1", "path": ".ufo/waves/round-49/w1/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None, "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0, "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": "Issue exactly one batched task call with taskCall ({context, tasks}); never split a wave.",
    }
    with open(os.path.join(WAVE_DIR, "w1-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w1"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w1/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": WAVE, "reportDir": REPORT, "members": members}, f, indent=1)
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
    else:
        with open(os.path.join(WAVE_DIR, "w1.ready"), "w") as f:
            json.dump({"lane": "kaidoku", "round": 49, "wave": WAVE,
                       "dispatch": os.path.join(WAVE_DIR, "w1-dispatch.json"), "l1": "KaidokuR49"}, f)
        print("ready written:", os.path.join(WAVE_DIR, "w1.ready"))
    print(json.dumps({"items": len(items), "counts": plan["counts"],
                      "roles": {r: sum(1 for t in T if t["agent"] == r) for r in sorted({t["agent"] for t in T})}}, indent=1))


if __name__ == "__main__":
    main()
