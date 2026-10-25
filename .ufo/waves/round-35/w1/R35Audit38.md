# R35Audit38 — reviewer report (kaidoku round 35, wave 1)

Seat: `R35Audit38` (reviewer, leaf). Item: *Compare knowledge to QUALITY criteria — build evidence and first falsifications.*
Measured revision: HEAD `3ecf4298` (control-commit tip). Base `aa04633a`. Canonical freeze `2323d197` (first add of `claims-canonical.json`).
Constraints honored: lane read-only (git object reads + frozen-counter runs only, no `--json-out` into the lane), single lane write is this report, private `/tmp` only, no `/fast/scratch`, no delegation, no VCS mutation, no installs.

`Report: .ufo/waves/round-35/w1/R35Audit38.md`

---

## 1. Evidence executed (first-hand runs)

Frozen counters run read-only against the lane (`--freeze 2323d197…`, base `aa04633a…`; `python3 -I -B`):

| Run | Command tail | Exit | Output |
|---|---|---|---|
| C1 @ base (control) | `c1-coverage-counter.py --root . --freeze 2323d197… --rev aa04633a…` | 1 | `C1_FAIL:` entry_missing ×2, registry_row_missing S125/S129, province_missing ×2, readme_missing ×2 |
| C2 @ base (control) | `c2-calibration-counter.py --root . --base aa04633a… --freeze 2323d197… --rev aa04633a…` | 1 | `C2_FAIL:` D1_census_start_missing; D2_lesson_missing; D3_source_missing/verified_at/recheck/not_s106; D4 line1081 cells=4; D4_section_missing Round-34 run-6 |
| C1 @ HEAD | same, `--rev HEAD` | 1 | byte-identical 8 failures (data not landed) |
| C2 @ HEAD | same, `--rev HEAD` | 1 | `D1_no_sources_change_after_base` (+ same D2/D3/D4 set) |

Both base runs reproduce the committed red receipts `.ufo/waves/round-35/controls/c1-do-nothing.json` / `c2-do-nothing.json` exactly (same failing lists, exit 1). Do-nothing controls are real and fail as required.

Immutable-object pin verification (all match):

- Counter sha256 at HEAD = canonical `instruments` pins: C1 `e28792c7…`, C2 `576c14dd…`; blobs at freeze `2323d197` == HEAD blobs (`cbb4bcf0…`/`67dc8bf6…`).
- `plans/round-35-claims.md` sha256 `45b644a4…` == canonical pin; `claims-canonical.json` blob unchanged `2323d197`→HEAD.
- Census-start sha256 `b6ce2b17…` == `frozen_inputs` pin; content carries `rows=106`, `EXIT=0`, exactly 9 `W04` lines (S033/S047/S054/S062/S069/S083/S090/S092/S102).
- Base `corpus/SOURCES.md`: 106 unique rows (S001..S106), no S125/S129 → census base count accurate; S125/S129 genuinely new.
- Predicates byte-identical between `claims-canonical.json` and both counter constants (normalized string equality).
- `considerthese/` absent (0 hits) — plan line 14 prediction holds.

---

## 2. Findings by severity

### High

- **H1 — C2 D-1 is hostage to C1 (severability).** `c2-calibration-counter.py` fails `D1_no_sources_change_after_base` whenever no post-base `corpus/SOURCES.md` change exists; the only planned SOURCES writer this round is C1 (rows S125/S129). A C2-perfect state with C1 stalled still fails D-1 (current HEAD state). The plan's "do-nothing control cannot reach it" sizing is invalid for C2; the two claims are not separable. (Converges with `R35CriticClaims.md` F1.)
- **H2 — D-1/D-3 content checks are substring-only; frozen-input pin never enforced at score time.** D-1 accepts any census containing `rows=106`, `EXIT=0`, `W04` — no exact row count, no `9 W04` count, no re-hash against `frozen_inputs`; a fabricated one-line receipt scores CLEAN (sandbox-proven by `R35CriticClaims.md` F2 and `R35Audit32.md` F1/F2). D-3 matches `S106` as substring (accepts `S1060`); D-2's `AAdjacencyCite`/`31/32` are presence-only. No junk control was designed/committed for D-1/D-3 (plan controls cover only junk-row/settle/cell-count).
- **H3 — D-4 measures formatting, not the stated defect.** (a) False positive: the section scan from `### Round-32 instrument registry` swallows the *Residual witness registry* archive table (SKILL.md:1081-1084, 4 cells) before the `## Round-33` boundary, so `D4_not_eight_cells … line1081 cells=4` fires against an archived table that is not part of the round-32 instrument registry (whose own rows are already 8 cells). (b) The actual `### Round-34 run-6 instrument registry` section exists at SKILL.md:1209 but carries the suffix `— the shortcut-replay gate (stopped capability)`, so the counter's exact-equality heading lookup misses it (`D4_section_missing`); even if found, its data rows are 5 cells (1213-1219). Closing D-4 therefore requires rewriting archived/historical tables to raw 8-cell layout or inserting/removing headings merely to satisfy a pipe-count — a historiographic rewrite, not record-defect closure.

### Medium

- **M1 — C1 counter leniencies.** Trio presence is checked anywhere (not "opens with"), no key order/adjacency, row citation is raw substring (`S1250` passes), used-by is substring containment (trailing noise survives), PROVINCE/README are whole-file substrings (no Core-table/coverage-map placement — QUALITY 54 unenforced). Additionally the README check demands the `.md`-suffixed filename while lane README house style omits `.md` → a convention-conformant row would false-fail and a misplaced mention would false-pass. Implementer must write the literal forms (dated stems in a Round-35 additions-to-Core table; `.md` filenames in the coverage map) to satisfy the frozen machine check. (Converges with `R35Audit05.md` A/B/C, `R35Audit08.md` 1-3, `R35Audit11.md` M6.)
- **M2 — Freeze-path hygiene incomplete.** No CLEAN `freeze-integrity` receipt exists for the canonical `2323d197` snapshot anywhere under `.ufo/waves/round-35/`; the only documented gate run failed at `f1ea3a6d` (`freeze-status.md`), and `corpus/claim-freezes.tsv` row round-35 still reads `FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED`. `instrument_supersessions` lists `a85ca674`, but the final counter bytes again differ at `2323d197` — the commit that itself first adds `claims-canonical.json` — without a separate supersession ledger entry (disclosed only via pins/note). Counters were committed before data (conf), but "instruments before claims file" holds only in the first-introduced sense; the finalization landed in the freeze commit.
- **M3 — Receipt shape.** C1 receipt `checks` map uses constant labels that never equal the failure ids, so every `c1_N` is always `true` even when the invariant fails (non-informative; `failing` is the reliable channel). C2 receipt has no `checks` map (asymmetric).
- **M4 — D-1 ordering uses `%cI` committer wall-clock**, not topology; equal-second commits (d2729cba family) pass ties, skew can invert verdicts.

### Low

- **L1 — Wave artifacts currently untracked:** `corpus/lessons/round-35.md` (draft lesson incl. M35-1..4 + Gate source decisions), `census-end.txt`, and `w1-settle.json` are untracked in the worktree → invisible to the git-object counters at any measured revision until committed. `w1-settle.json` contains a duplicate key `"spawned": 2` then `"spawned": 7` (ambiguous JSON; last-wins parses to 7) — malformed before it can feed D-2.
- **L2 — Plan does not carry the verbatim P35 sentence** (no `P35-c1`/`P35-c2` occurrence in `plans/round-35-claims.md`), while the plan's own claim-discipline line asserts byte-identity "in this plan"; predicate identity does hold across claims/counter/receipt (QUALITY 68 core satisfied; plan omission is a doc-governance gap).

---

## 3. QUALITY-criteria mapping (advisory)

- #52/#61/#66: do not cite "gate-clean" for the canonical snapshot without a committed receipt — none exists; current lesson draft wording should not assert it.
- #33/#38/#55: instruments before data ✓; finalization-in-freeze-commit disclosed but not ledgered; freeze-gate pin discipline not re-run on canonical snapshot.
- #45: `claim_row` present; counter enforces row mined/opened/used-by; newness rests on verified base absence; word-boundary weakness (S1250).
- #54: PROVINCE/README placement not machine-verified (H/M1).
- #1/#4/#5/#7: S125/S129 live reopen evidence (R35Audit01/17/18) HOLDS — captures byte-identical, anchors present, 677 releases complete/authentic; entry drafting must pin fetch SHA-256, quote raw lines, and keep the "Electron works / Node may fail" boundary.

---

## 4. Verification gaps / residual risk

- Neither claim's final green has been exercised against real corpus data (none landed); only synthetic green/red fixtures and base controls.
- D-2 cannot be assessed until settle receipts (w1 clean + w2) and the lesson are committed; w1-settle JSON needs the duplicate key fixed.
- A clean C1 or C2 pass under the frozen counters is not reachable without either (a) data written to the exact literal forms the counters demand (including README `.md` suffixes and Core-table stems), and (b) for C2, accepting the counter's over/under-matched D-4 semantics or rewriting historical tables — the latter conflicts with preserve-history governance. Recommendation (advisory): both claims are in honest-stop territory under the frozen kill rules; never re-freeze/relabel; record the stop with the M35 ledger.

## 5. Limits

Read-only lane; git object reads + frozen-counter executions only; no scoring/verdict authority — advisory evidence only; no network, no `/fast/scratch`, no delegation; nothing installed.
