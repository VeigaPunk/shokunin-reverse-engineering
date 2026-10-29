# ExecCounterSelftest — round 50, attempt 2, wave 3 (BUILD)

**Seat:** `ExecCounterSelftest` (leaf; no dispatch performed, no subagent spawned)
**Target:** run the four frozen round-50 instruments' **offline** selftests at base and record receipts.
**Verdict:** **PASS — all four frozen instruments are green at base (169 / 20 / 29 / 40 cases, zero failures).**
**But the dispatch's own command text is defective for two of the four instruments** (F1): both exit 2
(usage error = *could-not-evaluate*), so a receipt taken from the dispatch spelling would record a
usage error, not a verdict. Use the SKILL.md **instrument-registry v2** spellings instead (table below).
**No REA was run, no carrier was fetched, no network was used, no lane file was written or modified.**

---

## 1. Environment and frozen bytes

| item | value |
|---|---|
| interpreter | `python3 --version` → `Python 3.14.8` (`/usr/bin/python3`); every run used `python3 -I -B` |
| host | Linux 7.2.11-arch1-1 (x86_64) |
| lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| lane HEAD at run time | `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f` ("attempt-2 claims corrected") |
| freeze commit (C1) | `435d41fd4ad9211d1579fc447936fb33d2b74467` — **committed, ancestor of HEAD, byte-unchanged** (`git merge-base --is-ancestor` → yes) |
| dispatch base rev | `f890bbead20ca2c549487167f56876ae47f1e1a4` (one commit behind HEAD; see F4) |
| scratch | `/fast/scratch/hyaku/kaidoku-r50/w3-ExecCounterSelftest` (`TMPDIR` set to it; removed after receipts were copied) |
| disk guard | `scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku` 39% used, 495.2G free (pass) |
| tools installed | **none** — no install, upgrade or PATH change was needed or performed |

Frozen instrument bytes — **identical** in the work tree, at HEAD (`6f4aba63`) and at the dispatch base
(`f890bbea`), so every result below is base-independent:

| instrument | sha256 (work tree = HEAD = f890bbea) |
|---|---|
| `tools/round-50/c1-counter.py` | `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` |
| `tools/round-50/c1-controls.py` | `bca264c1b385559290d649b7f7fbee4f7bbc343b4b280aa14ba0f6da557f5bfb` |
| `tools/round-50/c2-record.py` | `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285` |
| `tools/round-50/selftest-r49-c2.py` | `7d0523ab6b80c0b570f36e682eb0f446ffdd455d48e84d50399876b79a3e7fbc` |
| `tools/round-50/selftest-r49-c2.expected.json` | `0a9ddec8dc917f835a609352218854f41b6038a17418962b3047dfc5b033c36f` |

Lane tree after all runs: `git status --porcelain --untracked-files=no` → empty; `git diff --stat HEAD` →
empty; `git status --porcelain tools plans corpus SKILL.md PROVINCE.md LOG.md SCORECARD.md` → empty.
**The selftests wrote nothing into the lane tree.**

---

## 2. Receipts

Every row: exact argv, cwd `$S` (scratch), `TMPDIR=$S`, UTC start, wall seconds, exit code,
stdout sha256, canonical sha256 (scratch paths / timings / per-case child digests masked).
Machine-readable copies: `.ufo/waves/round-50/w3/ExecCounterSelftest/receipts.json`, `runs.json`,
`runs/*.out`, `runs/*.err`; runner `run-selftests.sh`; collector `collect-receipts.py`.

### 2.1 Registry-pinned spellings — the runs that count

| # | command (cwd `$S`) | exit | wall (s) | UTC start | stdout sha256 | canonical sha256 | result |
|---|---|---|---|---|---|---|---|
| R1 | `python3 -I -B $LANE/tools/round-50/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $S/wk-c1` | **0** | 43.891 | 2026-10-29T20:44:37Z | `3273afd2a900f6ac…` | `40d1fc569d924b97b082…` | **169 cases, 0 failures** (17 green + 152 red; 57 probes = 6 path (3 discriminating) + 8 root + 43 spec) |
| R2 | `python3 -I -B $LANE/tools/round-50/c1-controls.py selftest --work $S/wk-ctrl` | **0** | 0.561 | 2026-10-29T20:45:21Z | `643f230f57ae81f8…` | `643f230f57ae81f8…` | **20 cases, 20 passed, 0 failed** |
| R3 | `python3 -I -B $LANE/tools/round-50/c2-record.py --selftest --root $LANE --work $S/wk-c2` | **0** | 15.034 | 2026-10-29T20:45:22Z | `9d5b96431bf9599e…` | `9d5b96431bf9599e…` | **29 cases, 0 failures** |
| R4 | `python3 -I -B $LANE/tools/round-50/selftest-r49-c2.py --lane $LANE --work $S/wk-49` | **0** | 30.969 | 2026-10-29T20:45:37Z | `c43739696d7afa10…` | `ed2475c0461013d700da…` | **40 cases, 40 passed, 0 failures** (base `7c678ae6…`, freeze `decc5697…`, counter sha `9b80b3b0…`) |

### 2.2 The dispatch's own spellings (as literally written in the seat prompt) — both fail to evaluate

| # | command | exit | UTC start | stdout sha256 | stderr (verbatim, trimmed) |
|---|---|---|---|---|---|
| D1 | `python3 -I -B $LANE/tools/round-50/c2-record.py --selftest` | **2** | 2026-10-29T20:44:37Z | `e3b0c44298fc1c14…` (empty) | `c2-record.py: error: the following arguments are required: --root` |
| D2 | `python3 -I -B $LANE/tools/round-50/selftest-r49-c2.py --root $LANE` | **2** | 2026-10-29T20:44:37Z | `e3b0c44298fc1c14…` (empty) | `selftest-r49-c2.py: error: unrecognized arguments: --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |

Exit 2 = *could-not-evaluate* under the lane's exit-code semantics: neither a pass nor a failure of the
instrument. The two instruments are fine; the dispatch spelling is wrong.

### 2.3 Calibration attack on the C1 counter's selftest (is it a rubber stamp?)

| # | command | exit | UTC start | stdout sha256 | stderr (verbatim) |
|---|---|---|---|---|---|
| A1 | `python3 -I -B $LANE/tools/round-50/c1-counter.py --selftest --pkg65 /nonexistent/pkg --work $S/wk-bogus` | **1** | 2026-10-29T20:46:08Z | `e3b0c44298fc1c14…` (empty) | `xpin mint failed: xpin-attribute: 6.5.0: cannot read package files under /nonexistent/pkg: Cannot find module '/nonexistent/pkg/dist/domain/canonicalDigest.js' imported from …/tools/round-27/xpin-attribute.mjs` |

A wrong REA package pin makes the selftest **red (exit 1)** in 0.088 s — the selftest discriminates on
the package pin and is not a no-op.

### 2.4 Repeat runs (determinism / flakiness)

Five `c1-counter --selftest` runs (2 without `--pkg65`, 3 with) → **all** canonical sha
`40d1fc569d924b97b082…`, 169 cases, 0 failures. Five `selftest-r49-c2.py --lane` runs → **all**
canonical sha `ed2475c0461013d700da…`, 40/40. Three `c2-record --selftest` runs → **byte-identical**
stdout `9d5b96431bf9599e…` (both spellings, with and without `--work`). Three `c1-controls selftest`
runs → **byte-identical** stdout `643f230f57ae81f8…`.
**No flakiness observed; no verdict changed between repeats.**

---

## 3. Findings

### F1 — the dispatch's command text is wrong for two of the four instruments (exit 2). *(highest impact for the L1)*
`c2-record.py --selftest` requires `--root LANE`; `selftest-r49-c2.py` takes `--lane LANE` and rejects
`--root` outright. The frozen **SKILL.md `instrument-registry v2` rows** pin the correct spellings and
the correct case counts, and my runs match them exactly:

| registry row (SKILL.md) | pinned selftest spelling | pinned count | measured now |
|---|---|---|---|
| `tools/round-50/c1-counter.py` (SKILL.md:1768) | `… c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` | 169 cases, exit 0 on 2026-10-28 | **169, exit 0** ✓ |
| `tools/round-50/c1-controls.py` (SKILL.md:1770) | `… c1-controls.py selftest --work DIR` (positional; no `--selftest` flag) | 20 cases, exit 0 on 2026-10-28 | **20, exit 0** ✓ |
| `tools/round-50/c2-record.py` (SKILL.md:1772) | `… c2-record.py --selftest --root .` | 29 cases, exit 0 on 2026-10-28 | **29, exit 0** ✓ |
| `tools/round-50/selftest-r49-c2.py` (SKILL.md:1773) | `… selftest-r49-c2.py --lane LANE` | 40 cases | **40, exit 0** ✓ |

**Action for the L1:** when the quiet-window controls are run, use the registry spellings (table above),
not the dispatch text; and when the new C3 instrument gets its registry row, pin the **same** spelling
that the instrument actually accepts (the two disagreeing spellings in this wave are exactly the
recurrence risk).

### F2 — two of the four selftests are semantically deterministic but **not byte-stable**; receipts must not quote their raw stdout sha256 as a "bytes unchanged" pin.
`c1-counter --selftest` and `selftest-r49-c2.py --lane` embed `mktemp` scratch names in their stdout
(e.g. `…/c1-selftest-work.gyiks68g/stubs/unblob-26.6.3`, `…/c1-emptypath.xhfhh97b`) and per-case child
digests + `sec`/`wall_sec` timings, so the same command yields a different stdout sha256 every run
(`3273afd2…` vs `7341d7fa…` vs `5385dfe2…` vs `a5bd310f…` vs `feb3d44a…`). Masking paths and timings
gives one stable canonical digest per instrument (`40d1fc56…` / `ed2475c0…`), and the verdicts are
identical across all repeats. `c2-record` and `c1-controls` are byte-stable.
**Action:** cite case count + `failures []` + the canonical (path-masked) digest in the L1's receipts;
quoting the raw stdout sha for the two path-bearing selftests would raise a false "frozen bytes moved"
alarm between the before-run and after-run receipts.

### F3 — the C1 counter's `--selftest` is offline but **package-dependent**; pass `--pkg65` explicitly.
Without `--pkg65`, `c1-counter.py` auto-discovers the REA package in the npm npx cache
(`find_rea_pkg()` → `~/.npm/_npx/*/node_modules/rea-agents`, version must be 6.5.0) and mints evidence
ids by running `node tools/round-27/xpin-attribute.mjs` against it. No REA extract-firmware run occurs
(the docstring says so, and the run is a simulated runner inside `selftest()`); the REA CLI itself is
never invoked. A wrong pin is red (A1 above). **Action:** use the registry spelling with an explicit
`--pkg65` and record the package root + `package.json` version in the receipt, so the receipt is
reproducible on a machine whose npx cache differs.

### F4 — base-revision discrepancy (dispatch vs lane) — benign for the instruments, material for the landing text.
The dispatch names base `f890bbea`; lane HEAD is `6f4aba63`, whose only change is
`plans/round-50-attempt2-claims.md` (the C1 entry stem corrected from
`2026-10-29-r50-le-avm-hsqs-core` to the stem the **frozen counter pins**,
`2026-10-28-r50-avm-le-squashfs-core`). The four instruments are byte-identical at `f890bbea`, at HEAD
and at the freeze `435d41fd`, so every measurement in this report is base-independent.
**Action for the L1:** the C1 landing text must use the stem the counter pins
(`2026-10-28-r50-avm-le-squashfs-core`), not the draft stem in the earlier commit; the counter, not the
plan prose, is the rule.

### F5 — scratch hygiene: `c1-counter --selftest` defaults its work dir to the **shared** lane scratch, not `$S`.
Without `--work`, the counter used `/fast/scratch/hyaku/kaidoku-r50/counter/c1-selftest-work.*` (the
lane-wide `$HYAKU_SCRATCH/kaidoku-r50/counter` default) and left temp dirs there; with `--work $S/...`
everything lands under the seat scratch. Nothing was written inside the lane tree either way.

### F6 — the C3 instrument does not exist yet; two CLI conventions must be reconciled before the C3 freeze.
`tools/round-50/sqfs-triage-v5.py` is absent at base. The frozen v4 precedent
(`tools/round-42/sqfs-triage-v4.py`) exposes `--selftest` (plus `--skill`, `--json`, `--table-only`,
positional envelopes), while the R50-C3 predicate command is
`--root <LANE> --rev <REV> --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>`; the claim also requires
"`selftest` green (every committed mutation flips ≥1 pair, none a no-op or cross-flip, do-nothing red)".
**Action:** the v5 instrument must accept the predicate spelling *and* a `--selftest` flag, and its
registry row (B9 coupling — currently no v5 row exists) must pin the spelling that works.

### F7 — `selftest-r49-c2.py` is pinned to **round 49**, not round 50 — do not read it as a round-50-wide check.
It judges the frozen round-49 counter (`c2-mismatch.py`, sha256
`9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` as printed in
`runs/registry-r49-selftest.out`) against base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`
and freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`, with 40 cases
(25 single-defect, 6 refusal, 3 cli, 2 green, 2 known-blind, 1 battery, 1 do-nothing). It therefore stays
green whatever round 50 lands — it is a hermetic re-test of the **r49** counter, not a round-50 verdict.
It also carries a `--mutant-counter PATH` mode that judges a mutant counter and exits 1 when it is
caught (useful for the mutation-testing lane).

---

## 4. What the L1 can rely on / what to do

- **Rely on:** all four frozen instruments are green at base with the registry-pinned spellings
  (169 / 20 / 29 / 40 cases, zero failures, no flakiness over 3–5 repeats each); the freeze commit
  `435d41fd` is committed, an ancestor of HEAD and byte-unchanged; the selftests leave the lane tree clean.
- **Do:** run the controls with the registry spellings (F1); record case count + `failures []` +
  canonical digest, not raw stdout sha, for `c1-counter` and `selftest-r49-c2` (F2); pass `--pkg65`
  explicitly and pin the package root (F3); land the C1 entry under the stem the counter pins (F4);
  require the v5 instrument to carry both CLI conventions before its registry row (F6).
- **Not run here (out of scope by contract):** any REA run, any `--data-run`, any carrier fetch, any
  C3 scoring, any C1 controls scoring — those are the L1's, in the quiet window.

**Artifacts:** `.ufo/waves/round-50/w3/ExecCounterSelftest/` — `receipts.json`, `runs.json`,
`runs/<label>.out|err` (7 runs), `run-selftests.sh`, `collect-receipts.py`.
Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ExecCounterSelftest` removed after the receipts were copied.

**Sibling observation (not my artifact, not touched):** at 2026-10-29T20:46Z a sibling seat wrote
`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (untracked; it appeared during this wave).
Its filename is the stem the **frozen counter pins** (F4), so the C1 landing text is already on the
counter's stem rather than the corrected-claims draft stem. It also names the counter's four source
rows S243/S244/S245/S249 — consistent with the claim text. I did not read it further, edit it, or write
anywhere in `corpus/`.
