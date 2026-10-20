# ControlsRerun — round-18 no-harm controls replay

**Verdict: HOLDS** (with two coverage caveats, F1/F2, neither exercised by this diff)

Author-side advisory rerun of `.ufo/waves/round-18/controls.py` at lane revision
`b2aad08ceeee8dd125ce0d316056d8bd766c7f94` vs baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.

## Commands

- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/controls.py 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94` → **exit 0** (reporter: `conformance_gate` is hardcoded `false`, controls.py:497; verdict is read from the JSON).
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/controls.py --selftest` → **exit 0**, stdout `SELFTEST: CLEAN cases=23`.
- `git diff --name-status 9011581… b2aad08…` → 437 entries: 15 `M`, 422 `A`, 0 `D`/`R` (read-only, exit 0).

## Report summary (observation, all from the emitted JSON)

| Check | Result |
|---|---|
| `old_prefix` LOG.md | `prefix_preserved: true`, appended 3459 B — no prefix break |
| `old_prefix` SCORECARD.md | `prefix_preserved: true`, appended 1197 B — no prefix break |
| `prior_corpus_text` | lessons 22/22 byte-identical; knowledge 95/95 ok (94 identical + 1 `appendable_knowledge` `2026-10-20-r17-go-carrier-diagnostics.md`, +1917 B, prefix preserved); `violations: []` both |
| `prior_verifiers_unchanged` | all 6 `*-verifier-spotcheck.md` unchanged |
| `prior_wave_evidence_blobs` | 15517 checked, 15517 unchanged; `quote_script_unchanged: true` |
| `r17_sums_restored_line` | `restored_ok: true`; sole added line `8ac38afe…d3eb5  predictions/carriers.tsv`, none removed |
| `quality_admission_rows` | rows 1–20 byte-identical, `added_rows: ["21"]`, `violations: {}` |
| `sources_registry` | `immutable_cells_unchanged: true`, `immutable_violations: {}`; added S033–S036; `allowed_deltas: {}` (no mutable-cell edits) |
| `skill_md_diff` | 6 deleted / 53 added lines, `truncated: false` (listed, not judged) |
| `craft` | `craft_sha256` identical at both revs; 17 rule blocks / 17 resolved citations |

## Changed blobs vs the contracted set

`CONTRACTED_MODIFICATIONS` (controls.py:57-64) = the six r17 files. Every `M` under
`.ufo/waves/` was exactly one of those six — all six changed (`byte_identical: false`), and
**no changed blob outside the contracted set exists inside the frozen prefixes** (15517/15517).

Non-frozen `M` blobs, unmonitored by controls.py (observation; all contract-authorized):
- `.ufo/gates/citation-drift/citation-drift-probe.py` and `.ufo/gates/custody-pair/custody-pair.py` —
  the contracted in-place fixes (contract.md:73-86); `.ufo/gates/` is outside `FROZEN_PREFIXES`
  (controls.py:56), so controls.py neither flags nor scopes these edits. Spot check: probe diff
  adds `resolve_rev`, `rev_resolved`, `head_not_branch_tip` — consistent with the contract.
- `LOG.md`, `SCORECARD.md` — append-only, verified above.
- `SKILL.md` — contracted registry update (line delta listed).
- `corpus/QUALITY.md` — row 21 added, rows 1–20 identical.
- `corpus/SOURCES.md` — S033–S036 rows, no immutable-cell change.
- `corpus/README.md` — one row edited to name `2026-10-20-r18-swiss-map-replay`; README is not
  covered by any controls.py check (blind spot, matches `prior_wave_evidence_blobs` scope being
  `.ufo/waves/` + `evidence/` only).
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` — the one contracted
  `APPENDABLE_KNOWLEDGE` append (controls.py:52-54).

Additions (`A`, 422): all under `.ufo/waves/round-18/` plus the two new corpus files
(`2026-10-20-r18-swiss-map-replay.md`, `lessons/round-18.md`). None under `.ufo/waves/round-1…17`,
`.ufo/waves/round-18/` predating the run, or `evidence/` — verified via
`git diff --name-status … | grep -v round-18` returning empty for `A` under frozen prefixes.

## Findings / caveats

- **F1 (coverage blind spot, not exercised):** `frozen_report` iterates `before.blobs` only
  (controls.py:323-328), and `corpus_text_report` likewise (controls.py:244-248). A file *added* at
  AFTER under `.ufo/waves/round-1…17/`, `evidence/`, or `corpus/lessons|knowledge/` would be
  invisible. This run adds nothing there, so the control's positive result is honest; the blind
  spot is structural. Reproduce scope:
  `git diff --name-status B AFTER | awk '$1=="A" && ($2~/^\.ufo\/waves\/round-1[0-7]/ || $2~/^evidence\//)'`
  → empty.
- **F2 (duplicate-line blind spot, not exercised):** `r17_sums_report` uses `set()` line
  differences (controls.py:292-295); re-adding a duplicate of an existing SHA256SUMS line would
  leave `added == []` and `restored_ok: true`. Current AFTER differs by exactly the one expected
  line, so no impact.
- **`conformance_gate: false` is by design** (controls.py:497) — reporter semantics, exit 0 means
  "report emitted", not "all checks passed". This report read the JSON checks individually.
- Selftest `cases=23` covers the docstring's "one clean append case, six red mutations"
  (controls.py:610): 16 clean-case assertions + 7 red assertions, all passing.

## Tooling

No installs. Commands used: `python3` (`/usr/bin/python3`), `git` read-only
(`diff --name-status`, `show`, `diff --stat`); zero writes to the lane.

## Evidence

- Full controls JSON retained in this session's output artifact (15517 unchanged entries elided in
  console display; totals and `contracted_modifications` read verbatim).
- Key line anchors at REV `b2aad08…`: `controls.py:50-77` (scope constants), `:316-354`
  (frozen_report), `:609-791` (selftest), `contract.md:72-86` (gates in-place fixes),
  `contract.md:148-151` (amendments).
