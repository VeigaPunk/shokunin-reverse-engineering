# EX-18 (arc3-loop1-round2) — control injection: absent `PROVINCE.md`

Seat EX-18 · chain c2 · role executor · task: confirm the absent-`PROVINCE.md`
FAIL class still reproduces at round-2 HEAD with the same or a clearer class,
and capture it.

**Headline: CONFIRMED, and upgraded — the class now names the file and the
cause.** An absent `PROVINCE.md` FAILs exit 1 on both the pre-round-2
instrument and the **landed** C2 instrument (EX-16's edit, measured at
`82fb807e…`), where the declared class becomes
`UNREADABLE (could-not-evaluate): ['PROVINCE.md: FileNotFoundError']` +
`DECLARED FAIL CLASSES: ['UNREADABLE']`, carried in `--json` as
`unreadable` / `declared_fail_classes`, alongside the pre-existing
`SCOPE-ERRORS … marker uncheckable` class. Six unreadable shapes (absent,
0-byte, truncated, directory, dangling symlink, chmod 000) and a
binary-garbage shape all land in the same declared class, exit 1. Two
findings from the pre-landing pass are recorded because they bound the claim:
the pre-landing FAIL was **incidental** — delete-around-able (§6.1) — and the
H1-only candidate's class was **JSON-invisible** (§6.2); the landed instrument
closes both (§7).

Timeline / identity (HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`
throughout; no repo file written by this seat):

- pre-landing instrument `.ufo/gates/c1-census-v10.py`
  sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`
  — measured 12:03–12:15Z (§3, §4).
- EX-16 landed during this seat's run (`59975ae0…` observed 12:16Z, complete
  `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` from
  12:17Z, stable through the end of capture), frozen to
  `scripts/landed-82fb807e79963f6d.py` — all §7 numbers are against the frozen
  copy, not the live path.
- scoped files: `PROVINCE.md` `d075a3c6…` (162 lines), `SKILL.md` `483b0eba…`
  (371 lines), `SCORECARD.md` `a7c72950…` (1417 lines); live anchors
  re-derived `{devin: 6.5.0, omp: 6.5.0, kimi: 6.7.0}`.
- landed SCOPE table is **identical** to the pre-landing table (21 rows,
  checked programmatically) — before/after numbers are comparable.

Scratch only under `/dev/shm/ex18-r2/` (disk-backed per the frozen rule; `/tmp`
avoided). Every log referenced below is copied into `logs/`, every candidate
instrument into `scripts/`.

## 1. What was run

Baseline and per-shape injection runs, each captured as full text + `--json`:

```
python3 <instrument> --root <scratch-root>
python3 <instrument> --root <scratch-root> --json
```

`fresh(root)` = copy of the three scoped files from the repo; the injection is
the single named mutation of `PROVINCE.md` (or the named contrast file);
everything else pristine. Candidate instruments built mechanically from the
frozen round-1 patch texts (`scripts/apply-h1.py`, `scripts/apply-h1h3.py`;
each anchor must match exactly once or the build fails):

| candidate (scratch) | sha256 | content |
|---|---|---|
| `census-h1-candidate.py` | `8b1a2079…` | v10 + RV-11's H1 patch text (3 hunks) |
| `census-h1h3-candidate.py` | `a81893fc…` | v10 + H1 + CR-5's H3 patch text (5 hunks) |
| `census-province-all-current.py` | `f32725bf…` | v10 with PROVINCE's 3 DATED rows re-classed CURRENT (probe, §6.1) |

## 2. Baseline (instrument healthy, both revisions)

- `B0`/`L0` census at the repo root: **PASS exit 0**,
  `stale=0 ambiguous=0 undeclared=0 unresolved=0`, `SCOPE-ERRORS []`
  (`logs/B0.out`, `logs/L0.out`).
- `S0`/`L1` intact scratch root: **PASS exit 0**; pre-landing `B0.out` ≡
  `S0.out` byte-identical (`cmp`) — the scratch root reproduces HEAD, so the
  injections isolate the single mutation.
- Landed JSON on the intact root: `verdict=PASS declared_fail_classes=[]`
  (`logs/L1.json`).

## 3. Injection matrix — pre-landing instrument (v10 as committed)

| case | shape of `PROVINCE.md` | exit | verdict | declared class (text) | JSON class visible? |
|---|---|---|---|---|---|
| S1 | **absent** | 1 | FAIL | `SCOPE-ERRORS … ['PROVINCE.md:40', ':45', ':119' marker uncheckable (file unreadable)]` | yes (`scope_errors`, 3) |
| S2 | 0-byte | 1 | FAIL | output **byte-identical to S1** | yes |
| S4 | directory | 1 | FAIL | byte-identical to S1 (`IsADirectoryError ⊂ OSError`) | yes |
| S5 | dangling symlink | 1 | FAIL | byte-identical to S1 | yes |
| S9 | chmod 000 | 1 | FAIL | byte-identical to S1 (`PermissionError`) | yes |
| S3 | truncated to 30 lines | 1 | FAIL | `marker '…' absent from '<beyond EOF>'` ×3; `lines=30 loci=2` | yes |
| S8 | 200 B binary garbage | 1 | FAIL | 3× `marker … absent from '<beyond EOF>'`; `lines=8 loci=0` | yes |
| S10b | symlink → `7125dd4:PROVINCE.md` (pre-6.7.0) | 1 | FAIL | `STALE` ×3 (`:10`, `:18`, `:44`) + `AMBIGUOUS` ×1 (`:67`) | yes |
| S11b | copy of `7125dd4:PROVINCE.md` | 1 | FAIL | same as S10b | yes |

`cmp` results: S2/S4/S5/S9 outputs byte-identical to S1
(`logs/identity-notes.txt`). Contrast cases, same instrument: `S6`
**`SKILL.md` absent → PASS exit 0** (silent `lines=0 loci=0` — the H1
fail-open reproduced at round-2 HEAD); `S7` `SCORECARD.md` absent → FAIL exit 1,
10× marker uncheckable.

**Round-1 → pre-landing round-2 class comparison.** Round-1 capture
(`.ufo/waves/arc3-loop1-round1/claims/c3/RV-11/scratch/atk-no-province.out:6`):
`['PROVINCE.md:40 …', 'PROVINCE.md:40 …', 'PROVINCE.md:119 …']` — same class
string `marker uncheckable (file unreadable)`, same exit 1, `:40` listed twice
from the pre-re-key table. Post-re-key: `:40`, `:45`, `:119` — the two
PROVINCE DATED rows now name their own markers. **Same class, marker list
sharpened by the G18 re-key; no regression.**

## 4. H1 / H1+H3 scratch candidates

| case | instrument | exit | result |
|---|---|---|---|
| P0 | H1 | 0 | intact root PASS |
| P1 | H1 | 1 | FAIL — marker class + `UNREADABLE … ['PROVINCE.md: FileNotFoundError']` |
| P2 | H1 | 1 | `SKILL.md` absent → FAIL `UNREADABLE ['SKILL.md: FileNotFoundError']` (debt closed); **JSON blind** — `verdict=FAIL, scope_errors=[], no unreadable key` (§6.2) |
| P3 | H1 | 1 | `SCORECARD.md` absent → FAIL both classes |
| Q0 | H1+H3 | 0 | intact root PASS; `G2 … ok (current-ok loci=5, total loci=17)` |
| Q1 | H1+H3 | 1 | PROVINCE absent → FAIL both classes |
| Q2/Q3 | H1+H3 | 1 | SKILL / SCORECARD absent → FAIL; G2 stays `ok` — no false H3 firing |
| Q4/Q5 | H1+H3 | 1 | truncated / 0-byte PROVINCE → FAIL via marker class only; `unreadable=[]` (the patch texts' H1 covers OSError, not short reads) |

## 5. Attacks / refutations (verdicts)

| attack | verdict |
|---|---|
| absent (deleted) `PROVINCE.md` | **class holds** — FAIL exit 1, same class as pre-round-1 (§3) |
| 0-byte / directory / dangling symlink / chmod 000 / binary garbage | **all FAIL exit 1**, same or marker-class family (§3) |
| delete-around: re-class PROVINCE rows CURRENT, then delete the file | **pre-landing REFUTED the class's robustness** — FAIL→**PASS exit 0** (`T1`); post-landing the same shape FAILs (T2/L-checks, §7) |
| stale replacement (older PROVINCE with stale statements) | **not silent** — FAIL exit 1 via STALE, pre- and post-landing (S10b/S11b/L11) |
| absent `SKILL.md` (the pure H1 case) | pre-landing **REFUTED — silent PASS exit 0** (S6); landed **FAIL exit 1 `UNREADABLE ['SKILL.md: FileNotFoundError']`** (L9) |
| JSON consumer sees the cause | pre-landing H1 candidate **REFUTED — cause invisible in `--json`** (P2.json); landed **holds — `unreadable` + `declared_fail_classes` keys** (L2.json/L9.json) |

## 6. Findings that bound the claim (pre-landing)

### 6.1 The pre-H1 FAIL is *incidental*, and absence is delete-around-able

The FAIL fires from `assert_markers` (`c1-census-v10.py:255-272`) — a side
effect of PROVINCE's **DATED rows**, not an absent-file rule. Measured: with
the three PROVINCE DATED rows re-classed CURRENT in a scratch variant
(`census-province-all-current.py`, `f32725bf…`), removing `PROVINCE.md` turns
the run from FAIL to **PASS exit 0** (`T1`) — a removed file contributes no
loci and nothing else in the verdict keys on presence. Same shape: at HEAD,
`SKILL.md` is already free to delete (S6, PASS). **Deleting a scoped file could
convert FAIL → PASS under v10.** Landed status: closed — the guard is
row-class-independent by construction and measured (T2, §7).

### 6.2 The H1-only class was text/exit-only; `--json` stayed blind

`P2.json` (SKILL absent, H1 candidate): `verdict=FAIL`, `scope_errors=[]`, key
set identical to the unpatched instrument — no field named the unreadable
file. Proposal recorded: `proposed-json-unreadable-field.patch.md`. Landed
status: **addressed** — the landed instrument carries `unreadable` and
`declared_fail_classes` in `--json` (§7, L2/L9). The proposal remains as the
rationale receipt; no further action needed.

### 6.3 Residual, out of this instrument's unit: identity-blindness

The census is a **statement** census: a same-content (or statement-equal)
replacement of a scoped file is invisible here. The stale-replacement attack
fails because the stale *statements* contradict live anchors (`STALE` ×3), not
because identity moved. Identity/rewrite detection belongs to C3's custody v2
receipt (sha256 + inode + ctime) — named boundary, not claimed coverage.

## 7. Landed-instrument re-run (EX-16's edit, sha256 `82fb807e…`, frozen copy)

| case | shape | exit | declared class | JSON |
|---|---|---|---|---|
| L0 | repo root | 0 | PASS 0/0/0/0; `classes=[]` | `PASS` |
| L1 | intact scratch | 0 | PASS; `UNREADABLE []` | `PASS classes=[]` |
| L2 | **PROVINCE absent** | 1 | `UNREADABLE ['PROVINCE.md: FileNotFoundError']` **+** marker ×3 | `FAIL classes=['UNREADABLE'] scope_errors=3` |
| L3 | 0-byte | 1 | `['PROVINCE.md: 0 lines < declared max 131 (rows beyond EOF)']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L4 | truncated 30 | 1 | `['PROVINCE.md: 30 lines < declared max 131 …']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L5 | directory | 1 | `['PROVINCE.md: IsADirectoryError']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L6 | dangling symlink | 1 | `['PROVINCE.md: FileNotFoundError']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L7 | chmod 000 | 1 | `['PROVINCE.md: PermissionError']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L8 | binary garbage | 1 | `['PROVINCE.md: 8 lines < declared max 131 …']` + marker ×3 | `FAIL ['UNREADABLE']` |
| L9 | SKILL absent | 1 | `['SKILL.md: FileNotFoundError']` (no marker class) | `FAIL ['UNREADABLE'] scope_errors=0` |
| L10 | SCORECARD absent | 1 | `['SCORECARD.md: FileNotFoundError']` + marker ×10 | `FAIL ['UNREADABLE']` |
| L11 | stale `7125dd4` PROVINCE | 1 | STALE ×3 + AMBIGUOUS ×1 + 1 marker scope-error (`:45` marker drift vs the older revision) | `FAIL classes=[]` |

T2 (structural check): landed semantics + PROVINCE-rows-all-CURRENT variant +
absent PROVINCE → FAIL `UNREADABLE ['PROVINCE.md: FileNotFoundError']`. The
delete-around hole of §6.1 is closed; the class is structural, not incidental.

Re-run protocol for any later revision of the instrument:

```
bash recheck-against-landed.sh [REPO_ROOT]      # costs ~2 s; read-only on the repo
```

It re-hashes the instrument, re-runs L0/L2/L9/L10 on `/dev/shm` copies and
prints the verdict + declared-class table; scratch at `/dev/shm/ex18-r2/recheck/`.

## 8. Blockers

- None standing. The one honest gap at first capture — EX-16 had not landed,
  so the "after" column was measured on scratch candidates built from the
  frozen patch texts — was resolved in-wave: the landed instrument
  (`82fb807e…`, stable at close) was re-measured and the results above are
  from the frozen copy of the landed bytes, not from a candidate.
- `/dev/shm` writable (16 G, 13 M used at capture); `/tmp` not used.
