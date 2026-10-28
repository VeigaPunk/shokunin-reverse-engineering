#!/usr/bin/env python3
"""Generate the round-49 wave-2 spec (v1 policy, post-landing falsification), validated dispatch, ready file."""
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-49")
BASE = "e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9"
FREEZE = "decc5697bfd4ec1e9de4a762ad199d9bd9c4230d"
REV = "29883d4ec35a31a8393c4ffb220888c44c0bb022"
DATA = "4aabb0b4bf716fb564c8406509c40b0a67457800"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
WAVE = "r49-w2"
MILE = ("Round 49 wave 2 (post-landing): re-run, attack and falsify the FROZEN counters and the landed "
        "bytes at the landing revision; every item names what it attacks")
REPORT = ".ufo/waves/round-49/w2"
W = REPORT + "/"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r49/"
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"

CTX = f"""# Target
kaidoku-shokunin round 49, wave 2 of 2 = POST-LANDING FALSIFICATION. The single freeze `{FREEZE}` (plan + `tools/round-49/**`) is committed; the C1 data run is committed at `{DATA}`; the landing (entry, PROVINCE/README rows, SOURCES, lesson, snapshots, QUALITY row 88, SCORECARD correction section) is committed; the landing revision is **`{REV}`** (lane `main`). Lane root (absolute): {ROOT}. L1 = KaidokuR49. The counters are FROZEN: a counter defect you find is a finding to report, never to patch. Read `{ROOT}/plans/round-49-claims.md` in full first.

# The two claims (the plan is the rule)
- **R49-C1 coverage** (SquashFS v1/v2 `squashfs_v1`/`squashfs_v2` Frontier -> Core through REA 6.5.0 `extract-firmware`, four frozen carriers): counting command `python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev {REV} --freeze {FREEZE} --pkg65 {PKG} --work <SCRATCH> --json-out <OUT>`. Expected at `{REV}`: exit 0, `carriers_matched 4`, every binding true, `frozen_path_changed []`. At the freeze: exit 1, `carriers_matched 0`.
- **R49-C2 calibration** (nine round-48 self-assessment atoms A1-A9): counting command `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev {REV} --freeze {FREEZE} --battery`. Expected at `{REV}`: exit 0, `atoms_total 9`, `mismatches 0`, `battery.failing []`, 16 mutations each red on exactly its own atom, do-nothing red x9. At the freeze: `mismatches 9`, exit 1.
Landed text under attack: `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, `PROVINCE.md` (`## Round-49 additions to Core` + the `Round-49 frontier note` line), `corpus/README.md` (coverage row, knowledge row, frontier line), `corpus/SOURCES.md` (S138/S139 used-by, S147-S149, search-log entries), `corpus/lessons/round-49.md`, `corpus/evidence/round-49/{{c1,c2}}/`, `corpus/QUALITY.md` row 88, `SCORECARD.md` `## Record corrections — round 49`. Wave-1 reports: `{ROOT}/.ufo/waves/round-49/w1/` (48 seats; the plan's "Wave-1 amendment record" says what was folded in).

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside `{ROOT}/{W}<YourSeatName>/` (create it) and your report `{ROOT}/{W}<YourSeatName>.md`. Never edit tools, plan, corpus, SKILL.md, LOG.md, SCORECARD.md, PROVINCE.md, SHONEN.md, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command in the lane or fleet repo. Read-only git (`log`, `show`, `diff`, `ls-tree`, `rev-parse`, `cat-file`, `merge-base`) is fine. Read from git objects at `{REV}` (`git -C {ROOT} show {REV}:<path>`), not from the worktree, which the L1 may be editing.
- **Frozen means frozen.** To mutate, copy to scratch. A finding that a frozen clause is vacuous, forgeable, or disagrees with its plan sentence is the most valuable thing you can return: exact command, differing value, fixture path.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q` (or `git clone --shared {ROOT} "$D"`), every later git call names `-C "$D"`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; set `user.name`/`user.email` in that clone only. Never run `git commit` with a throwaway identity anywhere else (run-6 incident).
- **Scratch**: `S={SCRATCH}<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku`. Remove `$S` before you yield AFTER copying receipts into `{W}<YourSeatName>/`. Never write under `/tmp`. Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass. Run every counter with `GIT_NO_REPLACE_OBJECTS=1`.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256 and UTC time. A check you did not run is not passed \u2014 say "not run". Never fabricate output.
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.
- **Absolute paths**: your tools start at the fleet root. The `Report:` trailer path in your prompt is relative to `{ROOT}` \u2014 write it at `{ROOT}/<that path>` (that is `{ROOT}/{W}<YourSeatName>.md`).
- **Tooling authorization (operator, 2026-10-19)**: you may install/upgrade tools that help the task; first read `/home/vgpnk/.omp/agent/RULES.md` (record tool/version/channel/reason). **pacman guard**: all pacman transactions are PAUSED host-wide \u2014 install only via `uv tool`/`npx`/an official binary in `~/.local/bin`, or nothing. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `/home/vgpnk/Projects/shokunin/.scratch/`, or the fleet repo. Never run `c1-run.sh --data-run` against the lane evidence root.
- Return a final message of at most 8 lines: verdict, the 1-3 most important findings, your report path.

# What the L1 does with your output
It reads every report, repairs defects in NON-frozen landed text (entry, PROVINCE/README rows, SOURCES, lesson, SCORECARD, LOG, QUALITY, SHONEN), re-measures both counters at the final revision, and reports every counter defect as a miss/limit without patching it.
"""

T = []


def add(name, agent, task):
    t = GODSPEED + task + (
        "\n\nWrite your findings to `<ROOT>/<W><SEAT>.md` (verdict first, then a findings table "
        "with exact commands, exit codes, sha256s); extra artifacts under `<ROOT>/<W><SEAT>/`.")
    T.append({"name": name, "agent": agent,
              "task": t.replace("<ROOT>", ROOT).replace("<W>", W).replace("<SEAT>", name)
              .replace("<REV>", REV).replace("<FREEZE>", FREEZE).replace("<DATA>", DATA)
              .replace("<BASE>", BASE).replace("<PKG>", PKG)})


# ---------------------------------------------------------------- attacks on C1 (frozen counter + landed bytes)
add("W2C1Rescore", "reviewer",
    "Attacks: the C1 before->after numbers. In a clean clone at `<REV>` (`git clone --shared <ROOT> $S/c && git -C $S/c checkout -q --detach <REV>`; set identity-free, no commits), run the C1 counting command at `--rev <REV>` and at `--rev <FREEZE>`; record exit code, `carriers_matched`, `failing`, `bindings_false`, stdout sha256. The L1's receipts: `<ROOT>/.ufo/waves/round-49/l1/scores/c1-at-landing.json` (read it, compare field by field). Report any difference.")
add("W2C1Reproduce", "executor",
    "Attacks: reproducibility of the committed C1 data. Run the data procedure into SCRATCH only: `bash <ROOT>/tools/round-49/c1-run.sh --lane-root <ROOT> --evidence-root $S/ev --scratch $S/scratch --freeze <FREEZE> --data-run` (the runner refuses an evidence root outside the lane evidence dir or scratch, so `$S/ev` under `/fast/scratch/hyaku/` is allowed; if it refuses, say exactly why and use `--dry-run` plus the counter's own `--dev-arm --run-rea`). Compare each produced `after.json` with `<ROOT>/corpus/evidence/round-49/c1/<id>/after.json`: handler, published files (path, sha256, size), gaps, unpublished entries, semantic projection (what differs: evidence ids and `output_directory` are expected to). Report every semantic difference.")
add("W2C1Receipts", "reviewer",
    "Attacks: the committed C1 evidence tree. For each of v1le/v1be/v2le/v2be under `corpus/evidence/round-49/c1/<id>/` at `<REV>`: `provenance.json`, `run.json`, `extract-env.json`, `extract-tree.tsv` vs the files actually committed under `firmware.bin_extract/` (path, size, sha256, symlinks, modes), vs the independent oracle (`tools/round-49/carriers.json` `oracle`), vs `after.json`. Check `run.json` `rev_at_run`/`freeze`, tool pins (unblob, sasquatch, npx rea-agents version), that no file in the tree is a symlink, and that `git ls-tree -r <REV> corpus/evidence/round-49/c1` lists every file on disk (the commit helper skips files over 1 MiB inside a directory). Report every disagreement.")
add("W2C1Entry", "critic",
    "Attacks: the landed knowledge entry `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` at `<REV>`. Extract every checkable statement (numbers, hashes, line citations `:NN-MM` into S112/unblob source, command receipts, 'receipt X', paths) and verify each: resolve every cited path/line, recompute every digest you can, check every receipt id named in the entry exists in `<ROOT>/.ufo/waves/round-49/w1/C1ScribeEntry/receipts.tsv`, check each statement against QUALITY rows 1-12 and 18/34 (no floating 'this round', no placeholders). Table: claim | resolves? | evidence. Every false or unresolvable item is a defect the L1 will repair in the entry.")
add("W2C1Province", "critic",
    "Attacks: the landed PROVINCE/README text. At `<REV>` read the `## Round-49 additions to Core` section of `PROVINCE.md`, the `Round-49 frontier note` line, and the three `corpus/README.md` additions (coverage row, knowledge row, frontier line). Find: any statement contradicted by the receipts or the counter (e.g. 'Core' claimed beyond the four carriers), any earlier PROVINCE/README/SKILL/SHONEN line that now contradicts the promotion (grep `SquashFS v1/v2`, `squashfs_v1`, `squashfs_v2`, `Frontier` across `<ROOT>` tracked files) and is not marked superseded, and hollow text a counter binding would accept. Table with file:line for each.")
add("W2C1Sources", "scout",
    "Attacks: the sources behind the C1 entry. Independently re-open S112 (raw `squashfs.py` at 26.6.4), S138 and S139 today and check every citation the entry makes against the live bytes: the S112 line ranges (`:24-69`, `:101-155`, `:158-196`, the `EXTRACTOR` and argv decision lines), the unblob tag commit, the S139 release facts, the sasquatch/unsquashfs identity lines. Report each citation: holds / drifted / wrong, with the live quote and the entry's claim side by side.")
add("W2C1Controls", "reviewer",
    "Attacks: the committed control ledger. Re-run the controls at the freeze from a clean clone: `python3 -I -B tools/round-49/c1-controls.py --root <clone-at-<REV>> --freeze <FREEZE> --counter <clone>/tools/round-49/c1-counter.py --pkg65 <PKG> --work $S/w --out $S/o --json-out $S/summary.json --doc-dir <ROOT>/.ufo/waves/round-49/w1/artifacts --from-fixtures` and compare with `<ROOT>/.ufo/waves/round-49/controls/summary.json` (verdicts, exit codes, stdout sha256). Report every control whose verdict or exit differs, and any control whose planted tree is not the committed fixture bytes.")
add("W2C1Fixtures", "executor",
    "Attacks: control-fixture integrity. Rebuild the control inputs (`c1-controls.py --build-only` into scratch, no `--from-fixtures`) and diff against the committed `tools/round-49/control-fixtures/**` at `<FREEZE>`: which fixtures are byte-identical, which differ and why (REA run-unique values are expected to differ in the POS capture; the verbatim round-44 copy in CTL-C1-4 must be byte-identical to `corpus/evidence/round-44/c1/<id>/after.json`). Also confirm `tools/round-49/control-fixtures/**` has no file that no control reads.")
add("W2C1Forge", "critic",
    "Attacks: the FROZEN C1 counter at `<REV>`. Wave 1 found that a relabelled replay (round-44 receipts, `output_directory` rewritten under `/fast/scratch/hyaku/kaidoku-r49/`, evidence id re-minted) and an oracle-complete fabrication score `carriers_matched 4`; the plan discloses that. Verify the disclosure is exact: build both on scratch clones of `<REV>` (the tree at `<DATA>` + landing), score them, and confirm exit/`carriers_matched`. Then look for forgeries the plan does NOT disclose: a receipt that passes while `gaps`/`unpublished_entries` are non-empty, a symlink or extra file in the committed tree, a wrong handler on a v2 carrier, a copied receipt with the carrier subject digest changed. Any green that the plan does not name is a finding.")
add("W2C1Mutate", "mutation-tester",
    "Attacks: the new C1 clauses. In scratch clones of `<REV>` mutate the frozen counter copy (never the original) at the five edits wave 1 forced: `provenance_ok` (prefix -> substring; drop the `..` test), the quiet-carrier rule in `nonregular_unpublished_ok`, the `frozen_drift` added-file branch, `core.quotePath=false`, the `Round-49` heading/mark constants. Run `--selftest` and the C1 score for each mutant and report which mutants SURVIVE (selftest exit 0). A survivor no control catches is a witness gap to disclose.")
add("W2C1Drift", "reviewer",
    "Attacks: freeze integrity at `<REV>`. Run: `git -C <ROOT> log -m --diff-merges=first-parent --name-status --format=%H <FREEZE>..<REV> -- tools/round-49 plans/round-49-claims.md` (must be empty); `git diff --stat <FREEZE> <REV> -- tools/round-49 plans/round-49-claims.md` (empty); sha256 of `tools/round-49/c1-counter.py` and `c2-mismatch.py` at `<FREEZE>` and at `<REV>` and in the worktree; confirm `<FREEZE>` is an ancestor of `<DATA>` and `<REV>`; list every commit in `<FREEZE>..<REV>` with author, committer, files; check none touched a frozen C1 path (`tools/round-42/*`, `tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`, `corpus/evidence/round-44/oracle/**`). Also confirm the receipts' first-add commit is `<DATA>`-descended (the counter's `receipt_fresh`).")
add("W2C1Superblock", "executor",
    "Attacks: the entry's superblock table and the carriers.json pins. Write your OWN parser for the v1/v2 packed 32-byte superblock (magic, inodes, bytes_used, uid_start, guid_start, inode_table_start, directory_table_start, s_major, s_minor) and decode the four committed carriers (`corpus/evidence/round-42/c2/fixtures/`); compare every value with the entry's table and `tools/round-49/carriers.json` `superblock`; also locate the zlib stream offsets (`0x78da`) the entry cites. Report any value that differs.")
add("W2C1Stale", "scout",
    "Attacks: stale statements elsewhere in the lane. `git -C <ROOT> grep -n -i -E 'squashfs[_ ]v1|squashfs[_ ]v2|SquashFS v1/v2|v1/v2' <REV> -- ':!.ufo' ':!corpus/evidence' ':!corpus/lessons'` and read each hit: list every sentence that still says v1/v2 is Frontier, 'measured, not promoted', or 'remains Frontier' without a dated supersession note (SKILL.md, SHONEN.md, SCORECARD.md, PROVINCE.md, README, knowledge entries, LOG.md). LOG/lessons/older entries are append-only history: report them but mark `history, no repair`. Table: file:line | sentence | repair needed?")
add("W2C1Selftest", "executor",
    "Attacks: the numbers the landed text quotes about the instruments. Run `python3 -I -B tools/round-49/c1-counter.py --selftest --work $S/s` (the lane text says 52 cases, 0 failures), `python3 -I -B tools/round-49/c1-controls.py --selftest ...` (11 passed), `python3 -I -B tools/round-49/c2-mismatch.py --help`; compare with every place the plan, lesson, entry and wave-1 reports quote them. Report any quoted number that does not reproduce.")
add("W2C1Rea", "scout",
    "Attacks: toolchain claims. From `corpus/evidence/round-49/c1/<id>/extract-env.json` and `run.json` at `<REV>` read the recorded unblob, sasquatch, npx and rea-agents identities; verify against the live host (`unblob --version`, `sasquatch -v`, `npx -y rea-agents@6.5.0 --version`, `sha256sum` of each binary), against `tools/round-42/rea-pkg.json` and `prior-pins.json`, and against what the entry states (sasquatch 4.5.1, unblob 26.6.4, rea-agents 6.5.0). Report any recorded identity that no longer matches the host (drift) and any statement in the entry that the receipts do not support.")

# ---------------------------------------------------------------- attacks on C2
add("W2C2Rescore", "reviewer",
    "Attacks: the C2 before->after numbers. In a clean clone at `<REV>`, run the C2 counting command at `--rev <FREEZE>` (expect `mismatches 9`, exit 1) and at `--rev <REV> --battery` (expect exit 0, `mismatches 0`, 16 mutations each exactly their atom, do-nothing red x9); compare with `<ROOT>/.ufo/waves/round-49/l1/scores/c2-at-landing.json` and `<ROOT>/.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json` field by field (stdout sha256 of the printed JSON, `counter_sha256` vs `counter_sha256_at_freeze`).")
add("W2C2Mutate", "mutation-tester",
    "Attacks: the nine atoms on the LANDED fixture (not wave 1's dev fixture). In scratch clones of `<REV>` write 30 NEW single mutations of the committed record (not of the counter): lesson line values, SOURCES rows S147/S148/S149 and the search log, SCORECARD A9 line, snapshot bytes, the round-48 inputs at the base (those must be immune: edit them at REV and show the atom stays as at base), duplicate headings. Score each with the frozen C2 counter. Report every mutation that leaves all nine atoms green (an undetected change to the record) and every mutation that turns a different atom red than you expected.")
add("W2C2Forge", "critic",
    "Attacks: the FROZEN C2 counter at `<REV>`. Re-run wave 1's gold forgeries (`<ROOT>/.ufo/waves/round-49/w1/C2GoldForgery.md` F01-F14, `C2CounterMut.md`, `C2MutAtoms.md` M-list, `C2PlanMatch.md` forgery table) against the frozen counter on scratch clones of `<REV>` and report which still score `mismatches 0`. Then find new ones. For each green forgery say whether the plan's disclosed limits cover it (snapshots are consistency, identified is asserted, prose not judged).")
add("W2C2Sources", "scout",
    "Attacks: rows S147/S148/S149 and the snapshots. Re-fetch today `https://plato.stanford.edu/entries/popper/`, `https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` and `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3`; compare sha256 and bytes with `corpus/evidence/round-49/c2/{popper,sysexits,freebsd-sysexits}.html` at `<REV>`; locate every quote the three rows carry (S147: two quotes, S148: one, S149: one) in the live page body and the heading above each; check each stated word count; check the HTTP status and byte counts the rows/lesson state. Table per row.")
add("W2C2Log", "reviewer",
    "Attacks: atoms A3, A4, A5 on the landed lesson. Re-derive from git objects at `<BASE>` (not at `<REV>`) every number on lesson lines A3/A4/A5 with your own code (no counter import): the LOG.md line sets for `2e785632`, `33f65a91`, `c093e798`, the commits LOG never names (`577a02a5`, `8847042a`, `7fe11332`), the 75/72 seat accounting from `r48-w1-results.json` and the `w1/` tree, the raw and newline-stripped digests of both round-48 receipts. Then read `corpus/lessons/round-49.md` prose around the lines and flag any sentence that misstates them (e.g. the closure's own wording).")
add("W2C2SearchLog", "reviewer",
    "Attacks: atom A8 and the registry diff. (1) Derive row counts and the new-id included/excluded split for `61b87d74 -> 8847042a` and `<BASE> -> <REV>` yourself. (2) Diff `corpus/SOURCES.md` `<BASE>` vs `<REV>`: the ONLY changes must be rows S147-S149, the two search-log entries and the S138/S139 `used-by` appends; per-status tallies (mined/queued/rejected) base vs REV; census-shaped awk from `/home/vgpnk/Projects/shokunin/CORPUS.md` (NF=13, enums, duplicate ids, used-by paths exist); `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit code and final line (run it on a clone checkout if the worktree differs from `<REV>`). (3) Check the two search-log entries against CORPUS.md rule 5. Report every deviation.")
add("W2C2Lesson", "critic",
    "Attacks: `corpus/lessons/round-49.md` at `<REV>`. Verify every pointer and claim: each `w1/...` and `.ufo/...` path resolves at `<REV>`, each hash is a commit/blob that exists, each number carries a resolvable command, the M49-1..M49-3 rows' evidence pointers say what the lesson says they say (open them), the Gate rows' quotes are present in the cited pages (use `corpus/evidence/round-49/c2/` snapshots where applicable), the 'registry diff, verified' bullet is true, and the prose after the A-lines does not contradict them. Table: statement | resolves/true? | evidence.")
add("W2C2Scorecard", "reviewer",
    "Attacks: `SCORECARD.md` `## Record corrections — round 49` and the round-48 section it sits beside. Is the A9 line exact (counter requires exactly one, equal to the contract line)? Does the prose say anything false about round 48 (check against `corpus/lessons/round-48-verifier-spotcheck.md`)? Does the SCORECARD still carry any round-48 statement the closure contradicts and no correction (list them with file:line; these are routed, not repaired this round)? Report calibration-axis implications honestly: what the owned-axes table says about calibration vs the closure verdict.")
add("W2C2Registry", "executor",
    "Attacks: the registry and snapshots as bytes. Run the `CORPUS.md` census awk lines and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` against a clean checkout of `<REV>` (clone to scratch; the script takes `--file <path>/corpus/SOURCES.md` too); paste exit codes and outputs; sha256 the three snapshots and compare with the pins in rows S147/S148/S149; confirm each row has NF=13 and no `|` inside a cell; confirm S145 and S146 lines are byte-identical to `<BASE>`.")
add("W2C2Quality", "reviewer",
    "Attacks: QUALITY row 88 and the discernment trend. Read `corpus/QUALITY.md` row 88 at `<REV>`: do its evidence pointers resolve (the swap mutation `A1 swap declared/stale` is red in `.ufo/waves/round-49/l1/scores/c2-at-landing.json`; the 9-mismatch control file)? Does the row name the lesson M49-1 and the criteria it sharpens (33, 68, 79 exist and say what the row says they do)? Is any wave-1 finding that became a lane mistake (M49-2, M49-3) lacking a QUALITY criterion that should exist? Propose exact row text only if a criterion is missing; do not edit.")

# ---------------------------------------------------------------- cross-cutting
add("W2Consistency", "connector",
    "Attacks: cross-document consistency. Read at `<REV>`: the plan, the lesson, the entry, PROVINCE, README, SOURCES search log, SCORECARD correction section, QUALITY row 88. Build a table of every number, hash, count and name that appears in two or more of them (rows 146 -> 149, 48 wave-1 seats, 16 mutations, 52 selftest cases, 40-of-75 mutants, 3/3/4/4 members, the freeze hash, the data commit hash, the counters' sha256s) and mark each pair agree/disagree with file:line on both sides. Every disagree is a defect.")
add("W2Plan", "reviewer",
    "Attacks: the plan against the frozen bytes. For every row of the plan's 'Wave-1 amendment record' table, verify its disposition is TRUE in the frozen tools at `<FREEZE>` (e.g. the id regex in `c1-run.py`, the evidence-root write-scope guard, `outdir_mode` default, the C2 base-reads, the A3 exact sets, the 16-mutation battery, `counter_not_frozen`). Then trace every sentence of P49-C1 and P49-C2 to the counter code (function, line) once more at `<FREEZE>`: agrees / disagrees / unchecked. Any `disagrees` or `unchecked` is a repeat of the round-44 failure class and must be reported even though the plan cannot be edited.")
add("W2Misroot", "scout",
    "Attacks: seat write hygiene. Read-only: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (fleet root) and list every untracked/modified path whose content or name mentions `kaidoku` or `round-49` or whose mtime falls within the last 6 hours and which is NOT under `.scratch/`, `.ufo/state/` or another lane's directory; for each, read its head and decide whether a kaidoku round-49 seat wrote it (misroot). List the paths exactly; do not move or delete anything. Also list any file under `<ROOT>` written outside `.ufo/waves/round-49/`, the lane's own corpus/tools/plans/PROVINCE/SCORECARD/LOG paths this round (`git -C <ROOT> diff --name-only <BASE> <REV>`), flagging any unexpected path.")
add("W2Scratch", "scout",
    "Attacks: scratch discipline (round-prompt section 7). `ls -la /fast/scratch/hyaku/kaidoku-r49/` and `du -sh` each entry; `find /tmp -maxdepth 2 -newer <ROOT>/.ufo/waves/round-49/gen-w1.py -user $(id -un) 2>/dev/null | head -50` for round-49 leftovers; run `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`. Table: path | size | owner seat (from the name) | live process? (`pgrep -af` for the path) | safe-to-delete? Do NOT delete anything: the L1 removes `/fast/scratch/hyaku/kaidoku-r49` after landing.")
add("W2Shonen", "reviewer",
    "Attacks: the SHONEN boxes. Read `<ROOT>/SHONEN.md` (4 boxes) and the lane's evidence at `<REV>`; for each box say what round 49 changed (e.g. a new end-to-end domain task: REA `extract-firmware` on four fixtures at `<DATA>`; executable instructions; province boundary) and propose one honest report line per box: `[~]` with a resolvable evidence pointer, or `[ ]` if untouched. A box may be `[x]` only with a named non-author verifier: none exists this round, so no `[x]`. Flag any SHONEN sentence the round makes false.")
add("W2Chronology", "critic",
    "Attacks: the chronology the plan and lesson assert. Using `git -C <ROOT> log --format='%H %ad %cd %s' --date=iso <BASE>..<REV>` and the wave dispatch markers (`<ROOT>/.ufo/waves/round-49/w1.ready.dispatched`, `w1-dispatch.json`), establish: freeze commit time vs the last wave-1 seat report mtime (the plan says wave 1 attacked DRAFTS before the freeze; was any seat still writing after it, and did any seat's output change a frozen byte?); data commit after the freeze; controls scored at the freeze; no C1 receipt committed before the freeze (`git log --diff-filter=A --format=%H -- corpus/evidence/round-49/c1`). Any claim in the plan/lesson ('before any data run', 'no amendment series') that the git history contradicts is a defect.")
add("W2Sentinel", "sentinel",
    "Attacks: sensitive-content and write-scope sweep of everything this round added. `git -C <ROOT> diff --name-only <BASE> <REV>` -> for each path scan for credential material (tokens, `op://`, session ids, cookies, private keys, `Authorization`), for private/operator paths that should not be public, for symlinks (`git ls-tree` mode 120000), for files over 1 MiB, and for secrets inside the three HTML snapshots and the REA receipts (env dumps in `run.json`/`extract-env.json`, `PATH`, home paths are acceptable; secrets are not). Report each hit with file:line and a verdict; CORPUS.md rule 6 applies.")
add("W2CleanClone", "executor",
    "Attacks: 'commands runnable verbatim'. In a fresh `git clone --shared <ROOT>` checked out at `<REV>` (scratch), run exactly the commands the L1 will paste into the report: both counting commands (before at the freeze, after at `<REV>`), `sources-census.sh validate`, `grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`, `git ls-tree -r --name-only <REV> corpus/knowledge | grep -c '\\.md$'` (base vs REV, expect +1), the `GIT_NO_REPLACE_OBJECTS=1` form. Record exit codes and outputs; report any command that fails or prints something other than the plan/lesson say.")
add("W2Gate", "critic",
    "Attacks: the lesson `## Gate` (discernment). The gate admits S147/S148, rejects S149, keeps S138/S139, records two closure disagreements, and says `Assimilation: none`. Re-decide each from the sources: would you admit S147/S148 at tier A? Is the S149 rejection reason honest and its flip condition one that could change the verdict (CORPUS.md rule 1 and the `teaches` shape `REJECTED: <reason>; flip: <what would change the verdict>`)? Does the Gate record at least one admit and one reject, with URL, date and a <=25-word located quote each? Is any decision taken on a source you could not reopen? Return agree/disagree per row with the reason. You are a lane seat: your answer is input to the L1, not the non-author spot-check.")
add("W2Coverage", "scout",
    "Attacks: the coverage claim's boundary. List what the landed text says is Core now and what stays Frontier, then test the boundary with evidence on this host (no extraction runs): for `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, gzip v3, v4 Broadcom, LE AVM, which fixture exists upstream under unblob 26.6.4 `tests/integration/filesystem/squashfs` (open the listing), which reader reads it (`unsquashfs -s`, `7z l`, exit codes), and what the cheapest next claim would be. Check the landed README/PROVINCE Frontier lines name the same residual list. Report any residual the text omits or any Core overreach.")
add("W2Honesty", "critic",
    "Attacks: honesty of the claim packaging. Read the plan's disclosed limits and the landed entry's 'Limits' and 'Observation, inference, unknown' sections. Is every disclosed limit backed by a receipt that resolves at `<REV>`? Is any limit understated (compare with wave-1 findings in `<ROOT>/.ufo/waves/round-49/w1/` — especially `C1ProvCritic`, `C1GoldForgery`, `C1DocBindings`, `C1CounterMut`, `C2GoldForgery`, `CritFreeze`)? Is there any sentence in the landed text that says or implies the committed receipt proves who/when/which round produced it, that the documentation bindings prove truth, or that C2 judges prose? List each overreach with file:line and the correct wording.")
add("W2Jj", "reviewer",
    "Attacks: VCS hygiene. `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state <ROOT>` (read-only) and `git -C <ROOT> log --format='%H %an <%ae> | %cn <%ce> | %s' <BASE>..<REV>`: every round commit authored and committed by `kaidoku-shokunin <kaidoku@shokunin.local>`; no commit contains a path outside the allowed scope (`git diff-tree --no-commit-id --name-status -r` per commit: only `.ufo/waves/round-49/**`, `plans/`, `tools/round-49/`, `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`); no deletions; the remote tip equals local (`git -C <ROOT> ls-remote origin refs/heads/main`). Report anything else.")
add("W2Rea", "scout",
    "Attacks: the REA/domain claim. Using only committed receipts at `<REV>` plus a fresh `npx -y rea-agents@6.5.0 extract-firmware --help` (no extraction), state what REA 6.5.0 verbs/refusals the entry relies on, whether `extract-firmware --max-depth` default and `--full-output` are as the runner used them (read `c1-run.py` argv in `run.json`), and whether any statement in the entry about REA behaviour (typed gaps, `missing-extractor-dependency`, `coverage complete`) is unsupported by the four committed `after.json` envelopes. Report unsupported statements with file:line.")
add("W2Skill", "reviewer",
    "Attacks: SKILL.md and the decision table. At `<REV>` read `SKILL.md` decision table and the queue-drain craft section: does any row (Firmware blob, SquashFS, `extract-firmware`) now mislead given the promotion (e.g. say v1/v2 needs 7z fallback or is Frontier)? Does PROVINCE Core row `squashfs_v1`/`squashfs_v2` give a decision a reader can act on (command, expected result, refusal signature)? List SKILL.md lines that need a dated supersession note and propose the wording; do not edit.")
add("W2Wave", "scout",
    "Attacks: wave accounting. Read `<ROOT>/.ufo/waves/round-49/w1-dispatch.json`, `w1/swarm-registry.json`, `w1-spec.json` and the 48 seat reports: seats spawned (48), seats with a report `.md` (list the ones without), role mix (executor 10, reviewer 9, scout 9, scribe 6, critic 5, mutation-tester 4, connector 2, revenger 1, sentinel 1, simplifier 1), attack share (reviewer+critic+mutation-tester = 18/48), the dead/unsettled seats (`C2SourcesReopen` had no report at the freeze; say whether it ever reported and when). The L1 will quote these numbers; verify each from the files.")


def main():
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES} for t in T]
    spec = {"wave": WAVE, "milestone": MILE, "reportDir": REPORT, "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w2-spec.json")
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
        "registry": {"schema": "ufo-swarm-registry-v1", "path": ".ufo/waves/round-49/w2/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None, "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0, "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": "Issue exactly one batched task call with taskCall ({context, tasks}); never split a wave.",
    }
    with open(os.path.join(WAVE_DIR, "w2-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w2"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w2/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": WAVE, "reportDir": REPORT, "members": members}, f, indent=1)
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
    else:
        with open(os.path.join(WAVE_DIR, "w2.ready"), "w") as f:
            json.dump({"lane": "kaidoku", "round": 49, "wave": WAVE,
                       "dispatch": os.path.join(WAVE_DIR, "w2-dispatch.json"), "l1": "KaidokuR49"}, f)
        print("ready written:", os.path.join(WAVE_DIR, "w2.ready"))
    print(json.dumps({"items": len(items), "counts": plan["counts"],
                      "roles": {r: sum(1 for t in T if t["agent"] == r) for r in sorted({t["agent"] for t in T})}}, indent=1))


if __name__ == "__main__":
    main()
