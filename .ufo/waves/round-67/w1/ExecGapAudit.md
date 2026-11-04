# ExecGapAudit — R67-C1 per-carrier gap accounting (round-67 w1)

Seat: `ExecGapAudit`. Scope: independent re-derivation of the per-carrier gap disposition,
**without importing the round-67 wrapper** (`tools/round-67/avm-le-counter.py` was never
imported or executed by this seat). I apply the two frozen rules directly to the pinned
round-50 engine over the four committed round-50 envelopes.

Artifacts (my seat dir):

- `.ufo/waves/round-67/w1/ExecGapAudit/audit.json` — full machine record, 100 checks, all pass
- `.ufo/waves/round-67/w1/ExecGapAudit/rederive.py` — the derivation (stdlib + read-only git show)

## Method

Engine imported with `importlib.util.spec_from_file_location` from
`tools/round-50/c1-counter.py`; sha256 verified
`9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` (matches the spec pin).
Called the engine's own `parse_nonregular`, `subject_root`, `diagnostics`, `gaps`,
`gap_rule_model`, `disposition_check`, `published`, `nonregular_published`.

Then, per carrier × rule, an **independent recount** of the three families
(path-resolved gap via `extract_rel`; structural gap via `structural` allowance; removal via
`diagnostic_rel`; required/silent admission from the rule model), producing the full
undispositioned/missing lists. The recount's violation set was compared with the engine's own
`disposition_check` boolean on all 8 carrier×rule pairs: **all 8 agree**.

Rule models were loaded from bytes and pinned: round-50 `43f7c8d7…` (unchanged from the tree),
round-67 `e66ba022…` (matches spec). Both models parse with no problems.

Integrity: `carriers.json`, both gap rules, the four nonregular tables and the four
`after.json` envelopes have byte-identical blobs at the operative freeze
`3663e6b21dccf4c4957f459301156664d8b151d6` and at base
`a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`; each envelope's subject digest equals its
carrier pin. The envelopes were not re-measured here (see Limits).

## Results per carrier

| carrier | nonregular census | path gaps | structural | removals | silent (r50) | gaps_ok r50 | gaps_ok r67 |
|---|---|---|---|---|---|---|---|
| g7581 | 639 symlink, 349 dir, 13 char-dev | 636 unpublished-entry | 1 depth-limited (allow 1) | 3 symlink | 1 (dev/led) | **false** | **true** |
| g7582 | 639 symlink, 349 dir, 13 char-dev | 636 unpublished-entry | 1 depth-limited (allow 1) | 3 symlink | 1 (dev/led) | **false** | **true** |
| c6490 | 613 symlink, 300 dir, 1 char-dev | 612 unpublished-entry | 1 depth-limited (allow 1) | 1 symlink | 1 (dev/led) | true | **true** |
| c6430 | 568 symlink, 255 dir, 1 char-dev | 567 unpublished-entry | 1 depth-limited (allow 1) | 1 symlink | 1 (dev/led) | true | **true** |

Aggregate: **round-50 rule `gaps_ok` on 2 of 4; round-67 rule `gaps_ok` on 4 of 4** — this
reproduces the committed before-arm (`control-dryrun.json`: 2 and 4) exactly.

Every path gap resolves to exactly one non-regular row, zero unresolved; every removal
resolves to exactly one symlink row and is exclusive with gaps; every carrier has exactly one
`depth-limited` structural gap against an allowance of 1. All `unpublished-entry` gaps land on
symlinks. `nonregular_published` is empty on all four (no published regular file equals a
non-regular path under the extract root). `subject_root` is `firmware.bin_extract` from a
single `squashfs_v4_le` derivation edge on every envelope.

## Full undispositioned lists (no engine truncation)

Round-67 rule (`required.char-device: false`, no `silent`) — the undispositioned entry-class
set is **exactly the char-device class, 13/13/1/1**:

- g7581 (13): `dev/led` 247:0, `dev/pts/0..7` 136:0..7, `dev/tiatm` 230:0,
  `dev/ttyp0` 3:0, `dev/ttyp1` 3:1, `dev/ttyp2` 3:2
- g7582 (13): identical set
- c6490 (1): `dev/led` 247:0
- c6430 (1): `dev/led` 247:0

None of these is required under the round-67 rule, so `gaps_ok` is true and the class is
carried by the rule's `class_disposition` prose plus the oracle table / `nonregular_unpublished`
check.

Round-50 rule (`required.char-device: true`, `silent.char-device = ["247:0"]`) — 12/12/0/0:

- g7581 (12, the FALSE carrier): `dev/pts/0` 136:0, `dev/pts/1` 136:1, `dev/pts/2` 136:2,
  `dev/pts/3` 136:3, `dev/pts/4` 136:4, `dev/pts/5` 136:5, `dev/pts/6` 136:6,
  `dev/pts/7` 136:7, `dev/tiatm` 230:0, `dev/ttyp0` 3:0, `dev/ttyp1` 3:1,
  `dev/ttyp2` 3:2
- g7582 (12, the FALSE carrier): identical set
- c6490 (0): `dev/led` 247:0 admitted by the per-row silent label
- c6430 (0): same

The engine's failure string truncates to `sorted(missing)[:8]` (`c1-counter.py:1564`); on
g7581/g7582 it therefore shows only `dev/pts/0..7`. The 12-row lists above are the complete
sets. A path I could not explain — any undispositioned row outside the char-device entry
class, or any undispositioned symlink — would be a blocking finding; there are none.

## Rule delta (byte-level, per model)

- `allowed`, `structural`, `removed.diagnostic`, `removed.kinds`, `removed.disposition`:
  **identical** between round-50 and round-67.
- `required.char-device`: **true → false** — the only behavioral delta.
- `removed.silent`: `{char-device: ["247:0"]}` → **absent** (transparency, not scoring: the
  engine consults `silent` only for rows where `need` is true — `c1-counter.py:1552-1557` — so
  with `required.char-device: false` the silent label is dead code for these carriers).
- `class_disposition` is prose only: `gap_rule_model` ignores unknown keys and does not read
  it; `round`/`supersedes` are likewise ignored, and the round-67 rule carries no `claim` key
  (round-50 has `"claim": "R50-C1"`). None of these is a defect — the model tolerates an
  absent claim (`c1-counter.py:791`) — but the rule's semantics live entirely in
  `required`/`removed`; the prose is the audit trail, not an enforced check. Stated so the
  clause review does not attribute behavioral force to the class narrative.

Empty-list classes (`block-device`, `fifo`, `socket`, `dir`) are outside the disposition
accounting by construction (`allowed == []`, `required == false`). Verified: no block-device,
fifo or socket rows exist on any carrier (the rule prose's "no block-device row exists on
these four carriers" holds), and zero dir rows are gapped or removed. The raw "no per-row
disposition" set including `dir` is 349/349/300/255 — the 13/13/1/1 statement is scoped to
entry classes (kinds with a non-empty `allowed` list), which is what a disposition rule can
ever ask about.

## Symlinks

639/639/613/568 symlinks, disposed exactly as 636+3 / 636+3 / 612+1 / 567+1
(gap + removal). **No symlink is undispositioned under either rule**, and no symlink is both
gapped and removed.

## Verdict

- g7581: round-50 FAIL (12 required char-device rows undisposed); round-67 PASS (0 required undisposed, 13 char-device rows undispositioned as a non-required class); symlinks 636 gap + 3 removal.
- g7582: round-50 FAIL (12); round-67 PASS (13 class rows); symlinks 636 + 3.
- c6490: round-50 PASS (dev/led silent-admitted); round-67 PASS (1 class row); symlinks 612 + 1.
- c6430: round-50 PASS; round-67 PASS (1 class row); symlinks 567 + 1.

No blocking findings. The gap-accounting half of R67-C1's predicate is confirmed on the
frozen data: 4 of 4 under the round-67 rule, 2 of 4 under the round-50 rule.

## Limits / honest boundaries

- I did **not** run the four carrier data runs, the `measure()` documentation bindings, or the
  reruns; `carriers_matched 4 of 4`, `met_target`, and `exit 0` are the L1's data run, not
  asserted here.
- I did **not** re-derive oracle tables from carrier bytes with `unsquashfs` (carrier cache is
  another seat's/L1's working state); the committed table bytes are pinned at freeze/base and
  the engine's own `oracle_rederived_ok` in the data run is the byte-level check.
- This audit reads the committed round-50 envelopes, not a fresh measurement of the base
  revision.
- Scratch `/fast/scratch/hyaku/kaidoku-r67/ExecGapAudit` was created for TMPDIR and deleted;
  no writes outside my seat dir and this report. No tools installed.
