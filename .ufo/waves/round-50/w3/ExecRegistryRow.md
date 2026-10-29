# ExecRegistryRow — R50-C3 instrument-registry v2 row + B9 coupling verification

**VERDICT: the row is drafted and validated green, but my seat prompt named the wrong landing
path.** The instrument must land at `tools/round-50-c3/sqfs-triage-v5.py`, not
`tools/round-50/sqfs-triage-v5.py`. Measured on a fixture clone against the two frozen
round-50 counters' own derivations: the in-tree path makes **both** `c1-counter.py` and
`c2-record.py` exit **2** (`frozen_path_changed` / `frozen_drift`) at the C3 landing revision;
the out-of-tree path leaves both green. The plan
(`plans/round-50-attempt2-claims.md:63-71`) already chose the out-of-tree path and its path
rule is correct. **B9 coupling: no dangling path; the row below keeps it green either way.**

Artifacts: `registry-row.md` (the row + cell derivation), `row-final.txt` (the row bytes),
`receipts.md` (every command, exit code, sha256), `receipt-*.json` (the raw receipts).

**Tip state at yield:** the lane moved under me mid-wave. The L1 committed `03f852b9`
("C3 instrument path moved outside the frozen `tools/round-50` walk (seat-measured
frozen_drift)") at 17:38, which edits `plans/round-50-attempt2-claims.md` to name
`tools/round-50-c3/sqfs-triage-v5.py`. **My independent measurement reached that same path
from the frozen counters' own derivations** (F1 below), so the two agree. The C1 freeze
`435d41fd4ad9211d1579fc447936fb33d2b74467` is still byte-unchanged
(`git diff --stat 435d41fd HEAD -- tools/round-50 plans/round-50-claims.md` is empty), and
`c2-record.py --rev HEAD --freeze 435d41fd` at the new tip `03f852b9` is **exit 0,
`mismatches 0`, 11/11 atoms green including B9**. The registry region still holds **54** rows,
no duplicates and no `tools/round-50-c3/` row — **the row below is still to be landed.**

**Second tip move:** the L1 has since committed `d71829bf` ("C3 pre-freeze amendments from
wave-3 attacks"). Re-verified at that tip: `c2-record.py --rev HEAD --freeze 435d41fd` is
**exit 0, `mismatches 0`, 11/11 atoms green including B9**; the C1 freeze `435d41fd` is still
byte-unchanged; the registry region still holds **54** rows with no duplicates and no
`tools/round-50-c3/` row; and my row still validates against the amended `SKILL.md` (7 cells,
kind ok, entry ok, self-test spelling ok, meaning map no-error). The stub at
`tools/round-50-c3/sqfs-triage-v5.py` is still present and still **untracked**.

**Late finding (F8-F10, raised to the L1 at 20:5xZ):** while this seat was finishing, the L1's
misroot sweep copied the **49-byte stub** into the lane at the C3 instrument path, not the
real 90,837-byte instrument (which lives in the `ExecTriageV5` seat dir, sha256 `c444f7ee…`).
The stub **fake-greens**: `--selftest` exits 0 with empty stdout and the full predicate command
exits 0 while writing **no receipt** — a do-nothing green, exactly the control the claim
requires to be red. It is still untracked, so nothing is committed; the L1 has been told to
replace it with the real bytes and to require the `--json-out` receipt to exist rather than
trusting a zero exit. See F8.

## Findings

| # | finding | evidence | severity |
|---|---|---|---|
| F1 | **The in-tree path breaks both frozen counters.** `c1-counter.py` freezes `tools/round-50/` as a prefix family (`FROZEN_PREFIXES`, line 425) and `c2-record.py` freezes the whole `tools/round-50` tree (`FROZEN`, line 123); an `A` status under either is drift. Measured at the simulated C3 landing with freeze `435d41fd`: C1 `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` → exit 2; C2 `freeze_check = ('frozen path touched in FREEZE..REV: … A tools/round-50/sqfs-triage-v5.py', 'frozen_path_changed')` → exit 2. The out-of-tree path gives `[]` and `(None, None)`. | `receipt-sim-paths.json`, `receipt-c2-oldfreeze-intree.json` | **blocker for the path choice** |
| F2 | **The row is drafted and passes every frozen rule.** Seven cells; cell 0 exactly `tools/round-50-c3/sqfs-triage-v5.py`; cell 1 opens `gate` and its entry command names the path; cell 2 binds 0/1/2 to meanings under **both** the original round-48 rule (`{"0":"success","1":"not-met","2":"unevaluable"}`) and its port in `c2-record.py` (no error); cell 3 is the `--selftest` spelling; cell 4 names the git-tracked envelopes manifest; no duplicate cell-0 in the 54-row region; all 54 existing rows still parse. | `receipt-validate-row.json` | draft ready |
| F3 | **B9 stays green at the C3 landing.** `c2-record.py --rev <C3 landing> --freeze 435d41fd` → exit **0**, `mismatches 0`, 11/11 atoms green including B9. Simulation arms against the frozen `b9()`: file in-tree **without** the row → `no registry row` (red); file in-tree **with** the row → green; row for the out-of-tree path → green with the census unchanged at 12. **No path dangles**: the six attempt-1 `tools/round-50/**` rows plus the new one cover every census path; `oracle/**` and `control-fixtures/**` hold no `.py`/`.sh`. | `receipt-c2-c3landing.json`, `receipt-sim-b9.json` | green |
| F4 | **Coupling the L1 must respect: no further `.py`/`.sh` may land under `tools/round-50/`.** The census prefix is `tools/round-50`, so any new helper there needs its own registry row *and* re-trips the C1 freeze-drift arm. A C3 helper belongs under `tools/round-50-c3/` (invisible to the census: `git ls-tree -- tools/round-50` returns 0 hits for `round-50-c3`). | `receipt-sim-paths.json` (`instrument_visible_to_census_prefix: false`) | constraint |
| F5 | **The R48 `registry_extra` failure is pre-existing, not caused by this row.** `tools/round-48/meanings.py` is already exit 1 at HEAD with 12 rows outside `tools/round-48/census2.json` (which covers rounds 41-48 only); the new row makes 13. Disclosed at `plans/round-50-claims.md:34-38`. R46 `registry.py` and R45 `c2-counter.py` stay green; R49 `c2-mismatch.py`'s A8 is red at HEAD with **identical** numbers at the C3 landing rev (A8 counts `corpus/SOURCES.md` rows, not registry rows). | `receipts.md` R7 | no action |
| F6 | **The v5 rule's reach is wider than the claim's "four `v2ns *_ddefault` rows".** Confirmed in the committed manifest: the four `squashfs_v2_nonstandard *_ddefault` rows are present and all `clean`/`none`, but `squashfs_v3_broadcom` carries 7 and `squashfs_v3_nonstandard` carries 8 further `clean`/`none` `_ddefault` rows. The C3 after-run receipt should count all of them, not just the four. | `receipts.md` R8 | disclosure for the L1 |
| F7 | **Cell 3 deliberately states the spelling, not a case count.** The attempt-1 rows cite a count and a date ("29 cases, exit 0 on 2026-10-28"); the v5 instrument does not exist yet, so the draft says "the case count and the exit code are recorded in the freeze receipt". The L1 must replace that with the measured values after the selftest runs — not with invented ones. | `registry-row.md` §2 | edit after the selftest |
| F8 | **The lane's C3 instrument path currently holds a 49-byte DO-NOTHING STUB, not the real instrument.** `tools/round-50-c3/sqfs-triage-v5.py` = 49 bytes, sha256 `af1b22ba…`, content `#!/usr/bin/env python3` + `# simulated C3 instrument` — the L1's misroot sweep copied the fleet stray rather than the real file. The real 90,837-byte instrument (sha256 `c444f7ee…`) is in the `ExecTriageV5` seat dir. **The stub fake-greens**: `--selftest` → rc 0 with 0 bytes of stdout; the full predicate command → rc 0 while writing **no receipt** (a 2-line file with no `main()` just runs and exits). The real instrument at the same path → `--selftest` rc 0 with "selftest: 13 cases, pass 13, fail 0", and the predicate command → rc 1 with a receipt carrying `pair_mismatches 19`, `evaluator_missing 0` and all four `squashfs_v2_nonstandard *_ddefault` rows among the mismatches (the claim's before-state). Only the real bytes can reproduce the before-state. Still untracked (`?? tools/round-50-c3/`) — nothing committed. L1 told: replace with the real bytes, and require the `--json-out` receipt to exist and parse rather than trusting a zero exit. | `receipts.md` R11-R13 | **blocker before the C3 freeze** |
| F9 | **The sibling's competing registry row fails B9's frozen self-test spelling; mine passes.** `ExecTriageV5`'s landing-draft cell 3 is `` `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest` (13 cases, …) `` — it opens with a backtick, so `re.match` against B9's rule `<interpreter> <path> … --selftest` fails (and the `none — <reason>` alternative also fails): `selftest_cell_ok = False`. Both rows are 7 cells with a valid 0/1/2 meaning map, so the difference is the self-test cell alone. Today it is inert under B9 only because `tools/round-50-c3/` is outside B9's census, but the spelling should still be right. L1 told to use my row. | `receipts.md` R14 | reconciliation |
| F10 | **The misroot's true origin is a second instance of MY seat, not the sibling.** The stray's exact literal is at `/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2/final-landing.py:64`; that scratch dir belongs to `ExecRegistryRow-2`, which also holds `validate-peer-row.py`, `registry-couplings.py` and `drift-extension.py` — all written from a *peer* seat's perspective ("the peer seat's registry row"). `ExecTriageV5` reached the same conclusion independently and the L1 has been told to attribute the misroot to my seat family. The fleet tree is clean again (`git status` there shows no `?? tools/`). | `receipts.md` R15 | attribution correction |

## Row (verbatim, one line)

```
| `tools/round-50-c3/sqfs-triage-v5.py` | gate — R50-C3 depth: the SKILL rule block 22 triage table v5 scored against the frozen independent evaluator over the round-42 recon envelope corpus (table label and action against evaluator label and action, pair_mismatches, evaluator_missing, the committed mutation battery), run as `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root LANE --rev REV --freeze FREEZE --envelopes DIR --json-out OUT` | 0=met, every envelope's table label and action equal the evaluator's, pair_mismatches 0 and evaluator_missing 0 at --rev, and the committed mutation battery green; 1=not met, a named envelope pair mismatch or a false binding, the receipt still written; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, an absent envelopes directory or a refusal | python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest — the committed mutation battery; the case count and the exit code are recorded in the freeze receipt | .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json (the R42C2ReconLegacy envelope manifest) and .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ (the frozen held-out envelope set) | --json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r50/c3; never the lane | kaidoku |
```

Paste immediately before `<!-- /instrument-registry -->` in `SKILL.md`. Same bytes as
`row-final.txt` (sha256 `3cce072798d598511393f3b84c6c19b99eeecda317e43a09e6c147cc5f88f64e`).

## Boundary kept

Read-only on the lane tree: the only lane files I wrote are under
`.ufo/waves/round-50/w3/ExecRegistryRow/` and this report. No REA was run, no `--data-run`,
no commit/push/stage/stash or other mutating git in the lane or fleet repo (all fixture
commits were in the scratch clone, with `user.name`/`user.email` set in that clone only, and
`git -C "$S/clone" rev-parse --show-toplevel` verified before the first commit). Nothing was
downloaded. Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow` was removed after the
receipts were copied into the seat directory. The disk guard was consulted before the clone
work (exit 0).

One correction to note for the record: my first `write` of the simulation script landed at
`/home/vgpnk/Projects/shokunin/kaidoku-r50/…` — a typo for `kaidoku-shokunin` — creating an
untracked directory in the fleet repo. It was moved to scratch and the stray directory
removed within the same turn; `git status --porcelain` in the fleet repo afterwards shows
only the pre-existing `M .scratch/goal-20261029-hyaku-run12.md` and no `kaidoku-r50/`
entry.

## Not run (stated, not claimed)

`tools/round-50/c1-counter.py` was not run end-to-end (it needs REA and the vendor carriers);
its frozen `frozen_drift()` derivation was exercised directly instead — that is the arm that
decides the path question. The v5 instrument was not built and its selftest was not run.
`tools/round-42/sqfs-triage-v4.py --selftest` was not run. No tool was installed or upgraded.
