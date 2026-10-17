# kaidoku luna-round-8 — operability: REA 6.4.0 symmetry battery

Date: 2026-10-16. Axis: **operability** (fleet axis, unowned proxy).
Fourth 128-seat two-lane wave. Predictions frozen pre-dispatch.

## Work performed

- 10-leg battery on the Kimi-resolved 6.4.0 pin: L1 version exact; L2
  tools/list = 170 names (full list retained); L3–L8 the six 6.5-only
  verbs (`inspect_go_binary`, `inspect_rust_binary`,
  `inspect_electron_fuses`, `inspect_sqlite_database`, `search_bytes`,
  `inspect_with_objdump`) each TYPED-REFUSAL (`-32602 Tool <name> not
  found`) on real carriers; L9 six exact absences from the 170-name list;
  L10 control RESULT (`inspect_binary_layout` on jq; the literal `analyze`
  verb is absent from 6.4.0 — the fallback is recorded in the receipt).
- Cross-lane verification: PB0 re-derived every hash and confirmed 10/10;
  QB gates admitted the consolidated entry; ZB2's disposition list
  adjudicated every defect.

## Landed changes

- `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` +
  map/Knowledge rows — commit `18dc397d` (lane identity), denominator
  78 → 79.
- Round-8 receipt bundle committed TRACKED (round-6 durability precedent):
  `receipts/leg-1..10.md`, `leg-2-tools.txt`, `MANIFEST.txt`,
  `census-pre.txt` (+ three RV3 replay files).
- Bookkeeping commit (below).

## Before → after measurements

- Score: **10/10** frozen predictions matched (CA6 census; PB0 independent
  re-verification with recomputed hashes; refusal taxonomy VB7: all six
  uniform `-32602`).
- Command A at `18dc397d`: `knowledge_files 79, mapped 79, missing [],
  dangling [], citation_resolved_rules 9/9, coverage 10.0, depth 10.0`.
- Config hashes match the round-6 baseline (SB2); no round-8 pre-pair —
  carried debt.

## Defects & adjudications (ZB2's list, condensed)

leg-3 display-hash defect self-repaired during the wave (current bytes =
claim = raw /tmp stdout; the pre-repair generation survives in /tmp for
audit). leg-10 append-only supersession: head-59 hash preserved, MANIFEST
annotated. Eleven stale early-snapshot verdicts (PS/RV/RE seats reading
before receipts landed) — superseded by CA6's late census, recorded as
timing artifacts. mtime-ordering unsound as evidence (hashes unaffected).
MANIFEST leg-10 row predates the append — annotation, not repair.
Six-of-37 scope stated in the entry's limitations (CA9/CB6/CA6).
Zero config drift closed against the round-6 baseline; a per-round
pre-pair remains carried debt.

## SHONEN

- [~] ×4 unchanged (RE4/SH1/RB7).

## Verdicts

- operability: **improved** — both pins now live-evidenced; the six
  round-7 entries' 6.5-only scope corroborated per-name.
- coverage / depth / calibration / freshness: **unchanged** (measured;
  the +1 entry is this round's expansion side-effect, recorded under
  coverage as denominator growth).
- Learning: expansion +1; quality improved (tracked receipts standard,
  stale-verdict adjudication); discernment unchanged.
- Admitted: yes — one axis improved, none harmed.
