# Review — PROVINCE.md: where Go RTTI/bootstrap diagnosis lives

Seat: KaidokuR17.ReviewProvinceGo-3 (author-side advisory). Read-only; nothing written
outside this report. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution.
PROVINCE.md is unchanged from baseline `b563c799` (`git diff --stat b563c799 -- PROVINCE.md`
empty; only `.ufo/waves/round-17/` is untracked), so every anchor below is baseline text.

## Direct answer

**Go RTTI/bootstrap diagnosis sits in neither Core nor Frontier.** It exists only as a
subordinate clause inside one Core row's evidence cell:

- `PROVINCE.md:52` (Cross-version compare) — the row's last clause reads verbatim
  "precise old cause remains unknown, source-bootstrap diagnosis
  `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`; `REA_GHIDRA_STARTUP_TIMEOUT_MS`
  needed past ~40MB targets (r2-08)". This is the file's only Go-diagnostic reference.
- Core table `PROVINCE.md:42-62` (19 rows) has no Go/RTTI/bootstrap row.
- Frontier bullets `PROVINCE.md:82-93` (PE subtypes, crashes >32 MiB, alternate providers,
  macOS-only, EVM extended) and `PROVINCE.md:135-162` (RISC-V, >90MB PE closed, `.jsc`,
  sasquatch, adb, asar scale, cross-version residuals, operator-gated) contain no Go bullet.
- Frontier's own definition, `PROVINCE.md:75`: "Claimed in MINT.md, not yet held."
  MINT.md's frontier claim (`MINT.md:34-36`: IDA/Hopper, Android APK, runtime observation,
  firmware prerequisites, cross-version diffing) does not mention Go either.

## Frontier-ground consequence

**A real-carrier diagnosis moves no frontier ground and retires no frontier bullet.** The
Frontier→Core promotion rule at `PROVINCE.md:75-76` is one-way; there is no Go Frontier
bullet to promote, and none can be added without amending `MINT.md:34-36` (the map's own
precondition). What C2 can legitimately move:

1. The Core unknown at `PROVINCE.md:52` — the sentence "precise old cause remains unknown"
   is scoped to the historical `op` pair and is the only Go claim the map makes.
2. A new Core row (the capability C2 actually promises: retained REA Ghidra-session log
   capture), gated by `PROVINCE.md:30-32`: "ground moves to Core only after an end-to-end
   probe lands a `LOG.md` entry citing its `evidence_id` and subject sha256."

If L1 integrates round-17 text claiming frontier movement, that is unsupported by the map
as written. The honest classification is **Core-row/capability movement, not frontier**.

## Findings

### F1 (calibration, medium) — the only Go anchor is two rounds stale
`PROVINCE.md:52` cites only the r14 entry. The r15 and r16 Go entries are committed corpus
but referenced nowhere in PROVINCE.md: `grep -n '2026-10-20-r1[456]' PROVINCE.md` returns
only line 52 (r14). If C2 lands, `:52` is the exact amendment site; under the r16
append-only discipline the correction must be a named append citing
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, not a silent rewrite.

### F2 (depth, high) — the diagnosis cannot discriminate the two causes it is aimed at
OBSERVATION: the installed base snapshots cover exactly minors 1.15–1.25
(`.../data/typeinfo/golang` → `go1.15.0.json` … `go1.25.0.json`, 11 files; r15
`inventory.json` `base_json.count: 11`), and patch diffs cover 1.15–1.24 (123 files;
`patch_diff_histogram` has no 1.25 key). The declared range is `1.15-1.25`
(GoRttiMapper, r14 entry anchor). The two sets are co-extensive, so on this host
**out-of-range ⇔ missing base**: every carrier out of range also lacks a base, and every
in-range carrier has one.

OBSERVATION: L1's own carrier predictions already show the confound —
`.ufo/waves/round-17/w1/selection-1.27.0.json` and `selection-1.27.2.json` both
`status: missing_base`; `selection-1.20.12.json`/`selection-1.23.12.json` both `exact_diff`
with all five buckets present.

OBSERVATION: the pilot log fires both conditions on one carrier —
`.ufo/waves/round-17/pilot/shfmt-log/ghidra.log:83` `Untested Go version [1.27.0]`,
`:84` `Missing Go bootstrap type info`, then `:85`/`:89` both Go analyzers fail
("unable to get GoRttiMapper").

INFERENCE: a real-carrier run therefore supports "EMPTY snapshot is sufficient and
co-occurs with the advisory range warning"; it cannot separate the advisory range check
from the missing-base branch, which is the distinction the r14 entry draws at source level.
The discriminating control (base present + out-of-range version, or base missing +
in-range version) does not exist in the installed data without mutating the Ghidra data
directory. L1's integration and the C2 knowledge entry should say this; claiming the run
"resolves which cause" would overclaim. `PROVINCE.md:52`'s "unknown" can be narrowed to
the direction of the effect, not to a separated cause.

### F3 (calibration, medium) — promotion bar has no evidence_id for the log itself
`PROVINCE.md:30-32` requires an `evidence_id` + subject sha256 for Core promotion; the
evidence-discipline row `PROVINCE.md:61` requires every Core probe to emit
`evidence_id` + `limitations[]`/`unknowns[]`. The promised capability retains the Ghidra
log by polling copy after REA deletes its runtime root, and the contract admits lossiness
(`contract.md` `log_capture_limit`; `pilot/README.txt` — "The last copy can miss lines
written after the final poll"). The log has no REA `evidence_id` of its own: the receipt
pins it by sha256. A Core row for it must put receipt/log sha256 in the evidence cell and
the polling gap in the limitations cell, or it fails the file's own convention. Also the
pilot is explicitly "NOT the final measured runs" and recorded no pre/post pins, so it is
not admissible promotion evidence under `:30-32`; only the contract's `carrier-run.py`
receipts are.

### F4 (depth, low) — the pilot already answers the map's question in direction
`pilot/esbuild-0.25.12-log/ghidra.log:63-76`: in-range go1.23.12 loads the snapshot,
discovers 4,881 types, fixes 2,248 + 2,055 signatures; analyzer cost 15.728 s (`:104`).
`pilot/shfmt-log/ghidra.log:106-107`: out-of-range go1.27.0 burns 0.002 s / 0.007 s on the
Go analyzers. So the province must not present "cause unknown" as unchanged after C2 — but
it also must not amend the map from the pilot (pilot README disclaims finality). The
correct sequence is final receipts → LOG entry → `:52` append.

## Residual risk and gaps

- I did not execute any REA verb or Ghidra; log readings inherit the pilot's polling-copy
  gap. Evidence ids in the pilot (`shfmt` `ev_2b29a1dd…`, `esbuild` `ev_391dbfe6…`) cover
  the analyze step, not the retained log.
- The per-build `op` mapping (2.34.1=go1.25.7→33,060; 2.40.0=go1.26.8→11,595) is
  [INFERENCE] from `LOG.md:99` and `PROVINCE.md:52` arrows; neither states it per build.
  The C2 carrier set (1.27.x / 1.23.12 / 1.20.12) contains no 1.26.8 carrier, so the
  historical `op` cause stays consistent-not-proved.
- Bounded search recorded: case-sensitive `grep -n 'Go' PROVINCE.md` → 5 hits (4 are
  "Godot", lines 56/125/139; the fifth is line 52); `git log -S'Go RTTI' -- PROVINCE.md`
  → empty; `git log -S'bootstrap' -- PROVINCE.md` → only `3e99fbd` (round-14).
- Tooling: no installs or upgrades. Executed read-only `python3 -I .ufo/waves/round-16/selection.py`
  (r16 source model) for `1.26.8` → `missing_base`, evidence class `source_model`.

## Recommendations to L1 (decision-ready)

1. Do not claim frontier ground moved for C2; the map has no Go Frontier bullet.
2. On validated final receipts, append to `PROVINCE.md:52` an r17 correction scoped to what
   was observed (out-of-range ⇒ `Untested Go version` + missing RTTI bootstrap; in-range ⇒
   snapshot load), citing the new knowledge entry and the carrier sha256/evidence id.
3. If instead a new Core row is preferred, fill it per `:30-32` with receipt/log sha256
   (no evidence_id exists for the log) and state the polling-copy limitation.
4. If a Frontier bullet is still wanted, amend `MINT.md:34-36` in the same commit, or the
   `PROVINCE.md:75` precondition is violated.
