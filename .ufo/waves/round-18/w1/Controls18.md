# Controls18 — round-18 `controls.py` (wave 1)

Files changed: `.ufo/waves/round-18/controls.py` (new, only file written).

## Deliverable

Adapted `.ufo/waves/round-17/controls.py` into `.ufo/waves/round-18/controls.py`
per `contract.md:142-145` ("Shared outputs" — `W18/controls.py BEFORE AFTER`):
LOG/SCORECARD old-prefix, prior knowledge/lesson/verifier files byte-identical
(old-prefix for the one appended r17 knowledge entry), QUALITY rows 1–20
identical, SOURCES S001–S032 identical except status/recheck/used-by, W17
predictions identical except the restored SHA256SUMS line, SKILL.md deleted
lines listed. `--selftest` builds fixture repos under `tempfile.mkdtemp()`,
removes them, prints `SELFTEST: CLEAN cases=N`, exits 0/1 (r17 pattern kept;
fixture commits are the only git writes and they land in the temp dir, never
LANE — `controls.py:605-608`).

## Design deltas over r17 (path:line anchors are in `.ufo/waves/round-18/controls.py`)

- `APPEND_ONLY` widened to LOG.md + SCORECARD.md (`:50`) — C1 corrections are
  appended to both (`contract.md:35,40`).
- `corpus_text_report` (`:238`) tightens lessons/knowledge from r17's
  old-prefix to byte-identical, with `APPENDABLE_KNOWLEDGE` (`:52`) naming the
  single contracted exception, `corpus/knowledge/2026-10-20-r17-go-carrier-
  diagnostics.md`, which keeps the old-prefix rule (C1 appends discharge lines
  there only). Per-file `mode` names which rule applied; `violations` lists
  offenders. Verifier spotchecks stay byte-identical via the same path.
- `quality_registry` (`:357`) keeps all-BEFORE-rows-identical and adds
  `rows_1_20_present_at_before` / `rows_1_20_identical` for the contract's
  literal 1–20 facet.
- `sources_registry` (`:388`) widens mutable cells from used-by (11) to
  `MUTABLE_SOURCE_COLUMNS = {8: status, 10: recheck, 11: used-by}` (`:76`) —
  `opened` (9) and all other cells immutable; per-column `allowed_deltas`
  named by column, not the r17 single `used_by_deltas`.
- `frozen_report` (`:316`) carves `CONTRACTED_MODIFICATIONS` (`:57`) — the six
  contract-named in-place fixes: `round-17/verify.py`,
  `round-17/tools/{carrier-run,compare,log-extract,receipt-validate}.py`, and
  `round-17/predictions/SHA256SUMS` — out of the byte-identical `files` set and
  reports them under `contracted_modifications` with `byte_identical` flags.
- `r17_sums_report` (`:271`) implements the restored-line rule exactly:
  `restored_ok` iff byte-identical, or exactly one added line
  `<sha256(carriers.tsv blob at AFTER)>  predictions/carriers.tsv` and zero
  removed lines. Wrong sha → red; any removed line → red; other added lines →
  red.
- `skill_diff` (`:423`) lists SKILL.md `deleted_lines`/`added_lines` (capped at
  64 each, `truncated` flag) — reported, not judged, per contract wording.
- Observation: `.ufo/gates/` edits (citation-drift probe, custody-pair) fall
  outside `FROZEN_PREFIXES` scope — no carve-out needed there.

## Verification (commands actually run; all read-only on LANE git)

- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/controls.py --selftest` → exit 0, last line exactly:
  `SELFTEST: CLEAN cases=23`
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/controls.py 9011581d84527ba34c675f9cf912e54d2e72d470 9011581d84527ba34c675f9cf912e54d2e72d470` → exit 0; zero harm (baseline vs itself):
  `old_prefix` both `prefix_preserved: true`; lessons 22/22 and knowledge 95/95
  ok; frozen 15517/15517 unchanged, `quote_script_unchanged: true`,
  `r17_sums_restored_line.restored_ok: true` (byte-identical branch); QUALITY
  `rows_1_20_present_at_before: 20`, `rows_1_20_identical: true`; SKILL
  `byte_identical: true`; SOURCES 32→32 rows, `immutable_cells_unchanged:
  true`; all 6 verifier spotchecks unchanged; all six contracted modifications
  enumerated.
- Baseline facts gathered read-only for calibration: `git show
  refs/heads/main:.ufo/waves/round-17/predictions/SHA256SUMS` lacks the
  `predictions/carriers.tsv` line; `carriers.tsv` sha256 at baseline is
  `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5`; QUALITY
  has exactly 20 numbered admission rows; SOURCES has 32 rows.
- Other read-only commands (exit 0): `git ls-tree --name-only` on
  knowledge/lessons/predictions/tools dirs; `git show` of `corpus/SOURCES.md`
  and `corpus/QUALITY.md` headers/row count; `grep -n` on the new file for
  anchors. One grep pipeline exited 1 on a miscounted awk slice (superseded by
  the correct count of 20 above).

## Selftest coverage

23 checks. Clean case: LOG+SCORECARD appends, S033 added with S001
status/used-by edits (recorded as allowed deltas), QUALITY row 3 appended,
SHA256SUMS restored line, in-scope `compare.py` edit, appendable r17 knowledge
append, SKILL line substitution listed. Six sequential red mutations, each
asserted detected on its facet: rewritten LOG line; edited QUALITY row 1
(`row_text_changed`, `rows_1_20_identical: false`); changed S001 teaches cell
→ `immutable_violations {S001: [7]}`; tampered non-appendable knowledge file;
SHA256SUMS restored line with a wrong sha → `restored_ok: false`; mutated
frozen `.ufo/waves/` blob named in `files`.

## Risks / limits

- `restored_ok` accepts a byte-identical SHA256SUMS (carriers.tsv line absent
  at AFTER) — a no-change case is zero-harm; the line's presence at the
  delivered revision is the routed-defects R17-SUMS-RUNLOG check, not a
  no-harm concern. [INFERENCE: contract splits these the same way.]
- `skill_diff` deletion listing is unjudged; if L1 wants a cap on allowed
  deletions it is a report field away.
- Git inherits caller environment (GIT_* could redirect object reads) —
  same recorded limitation as r17.
- No tools installed; Python 3 stdlib only.
