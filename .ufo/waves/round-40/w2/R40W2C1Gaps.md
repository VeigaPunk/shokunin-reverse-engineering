# R40W2C1Gaps — the frozen gap rule attacked against the four C1 receipts

**Verdict: DEFECTS FOUND** — in the rule as a standalone contract (two looseness families, two
over-tightness families, all latent on the frozen data); the four receipts themselves conform to the
rule on every dimension checked, and no wrong receipt passes the *full* clause set at the measured
revision, so the recorded C1 verdicts (3/4, honest stop at L2) stand.

Attacked: `.ufo/waves/round-40/c1/gap-rule.json` (bytes `421b3d1a1f74a098…`, identical at freeze
`7fce3086`, measured `42c10a58`, dispatch tip `4d62ee5a`, and the working tree — verified by
`git show <rev>:… | sha256sum`) against `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`,
using the counter's own frozen functions (`gap_rule_model`, `gap_check`, `same_rel`,
`parse_nonregular`, `nonregular_published`, `projection`, `projection_diff`) imported from
`tools/round-40/c1-counter.py` at the working tree, which is byte-identical to `42c10a58` for every
C1 path (`git diff --stat 42c10a58 -- <c1 paths>` empty).

## 1. The receipts conform to the rule (all seat checklist items)

Full inventory (recomputed from the committed `after.json` files, not from the L1 score; matches
`gaps_note` in `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` exactly):

| carrier | `unpublished-entry` | `depth-limited` (null path) | other kinds | total gaps | non-regular entries (symlink/dir/char-device) | published files |
|---|---|---|---|---|---|---|
| V1 | 263 | 1 | 0 | 264 | 381 (263/117/1) | 697 |
| V2 | 85 | 1 | 0 | 86 | 95 (85/9/1) | 8 |
| L1 | 2 | 1 | 0 | 3 | 13 (2/11/0) | 7 |
| L2 | 2 | 1 | 0 | 3 | 10 (2/8/0) | 6 |

- **Every path gap resolves to exactly one non-regular entry, and every `unpublished-entry` sits on a
  `symlink` row.** 0 unresolved, 0 multi-hit, 0 resolutions to dir/device rows; per-entry histogram is
  `{1: N}` on all four carriers — every symlink has exactly one gap, no entry has two, no symlink is
  gapless (the `required[symlink]=true` clause is satisfied everywhere).
- **`depth-limited` is structural and exactly one per receipt**: `relative_path: null`,
  `dependencies: []`, `handler: null`, `input_path: "$output/firmware.bin_extract"` (the carve dir) in
  all four. `unknown-chunk-handler` count 0.
- **Devices and directories are absent from the gap list.** V1/V2 each carry `dev/led char-device
  247:0` in the table; it produces no gap, no unpublished entry, no diagnostic (recon G7 behavior).
  All 117/9/11/8 dir rows are gapless.
- **No `MaliciousSymlinkRemoved` anywhere**: 0 in `normalized_result.diagnostics` and 0 occurrences in
  `raw_result` text, in all four `after.json` (and all four `run.json` records). Every symlink in all
  four images is retained in-tree — consistent with recon G8.
- Every gap path carries the `firmware.bin_extract/` carve prefix and is unique per entry;
  `unpublished_entries` mirrors the path gaps (263/85/2/2 rows, all `kind: symlink`).
- The counter's own `gap_check` returns `True` on all four ("264/86/3/3 gaps (1 structural) on
  381/95/13/10 non-regular entries") — matching the frozen score's `gaps_ok: true` per carrier.

## 2. Looseness — wrong receipts the rule alone accepts (constructed counterexamples)

All run through the frozen `gap_check` with the frozen model (artifact
`artifacts/R40W2C1Gaps/counterexamples-output.txt`; driver `cx.py`):

- **CX-A — no per-symlink cap.** Appending a second `unpublished-entry` on `bin/sh` to the honest L1
  gaps **passes** (`4 gaps (1 structural) on 13 non-regular entries`). The claim text says "one
  `unpublished-entry` per symlink"; the rule encodes only `required: ≥1` with `allowed` listing the
  kind — no upper bound, and no other counter clause counts gaps per entry. A receipt with 300 gaps on
  263 symlinks passes `gap_check`.
- **CX-B — suffix misattribution.** Rewriting the honest gap path `firmware.bin_extract/bin/sh` to the
  fabricated `deep/nested/bin/sh` **passes**: `same_rel` suffix-matches it onto the `bin/sh` symlink
  row, satisfies the required-gap clause, and the fabricated path corresponds to no real entry.
  `./bin/sh` (CX-C) passes the same way.
- **CX-S / CX-T — unchecked fields.** `gap_check` never reads `dependencies` (a structural gap with
  arbitrary dependencies passes) and never reads the `unpublished_entries` field (emptying it to `[]`
  while keeping the gaps passes); the gap's `handler`/`input_path` bookkeeping is likewise unread, and
  the `plus-extractor` projection does not include `input_path`/`handler` for gaps, so a depth-limited
  gap naming a bogus carve path projects *equal* to the fresh run.
- **CX-E — zero structural gaps passes** (consistent with the claim text "at most one", but it means
  the rule does not pin the truncation fact either).
- **Exact-duplicate gap objects** (CX family) pass when the kind is path-resolved.

**Composite closure at the measured revision.** Every hole above is closed by a sibling clause, which
I demonstrated rather than inferred: `projection_diff` (profile `plus-extractor`) between the honest
L1 receipt and each mutated one reports `extraction_gaps` / `unpublished_entries`
differences (CX-A, CX-B, CX-E, CX-T all `projection_equal=False`), CX-D (symlink materialised as a
regular file with its gap kept) is caught by `nonregular_published` → `nonregular_unpublished_ok`,
and a missing oracle file is caught by `oracle_hits_ok`. Since `projection_ok` requires equality with
a fresh REA run of the pinned carrier bytes made at scoring time, no wrong receipt passes the full
clause set at `42c10a58` — the only accepted receipts are those projecting equal to the real run,
which is the disclosed by-design limit. **The looseness is therefore latent: it would become
exploitable only if the fresh run itself emitted the loose shape** (e.g. duplicate gaps per symlink),
which the four receipts show does not happen (histogram all exactly 1).

## 3. Over-tightness — honest shapes the rule rejects

- **CX-U/CX-V — the escaping-symlink class is unrepresentable.** With a table containing symlink
  `bin/escape` and the receipt recording no gap for it (unblob removes an escaping link with a
  `MaliciousSymlinkRemoved` report and, per the corpus's own measured behavior, **no gap** — recon
  `R40C1ReconGaps.md` §4 G3: "`#unpublished-entry == #links − #escaping`", t1: 5→4+1 MSR, t2: 4→3+1,
  t2b: 5→3+2; same semantics in the C2 triage table's `escaping-symlink-removed` and `mixed-symlinks`
  rows), `gap_check` returns **False** with `required gap absent on ['bin/escape']`. `required:
  {symlink: true}` demands a gap for *every* symlink row, and `gap_check` takes no diagnostics input,
  so the rule cannot express "removed with diagnostic, no gap". The frozen rule is valid only for
  carriers with zero escaping links — true for V1/V2/L1/L2 (0 MSR), so no honest receipt was rejected
  this round, but the rule contradicts the recon measurements it was derived from and the triage
  table's own mixed class.
- **CX-O — suffix-collision multi-hit rejects honest gaps.** An honest gap on a symlink at
  `usr/lib` would suffix-match both the `usr/lib` and `lib` rows of L1's table (`len(hits)=2`) and be
  rejected. V1's table already contains four such dir-dir collision pairs (`lib`⊂`lib/modules/…/lib`,
  `bin`⊂`usr/bin`, `lib`⊂`usr/lib`, `sbin`⊂`usr/sbin`); none involves a symlink, so no real gap trips
  it, but any future carrier with a symlink whose path suffix-contains another entry's path cannot
  pass. Likewise the structural cap `depth-limited: 1` assumes exactly one carve dir at depth 1 (recon
  G5) — a carrier with two depth-1 carves would be rejected.

## 4. The L2 stop is a `same_rel` false positive — confirmed from data, and it is the same matcher

L2's image contains symlink `bin/busy → /usr/bin/busy` **and** regular file `usr/bin/busy`
(`oracle.tsv` row `usr/bin/busy e28f81fc… 40000`). The receipt publishes the regular file
(`firmware.bin_extract/usr/bin/busy`, sha `e28f81fc…` = the oracle row) and records the symlink's
required gap (`firmware.bin_extract/bin/busy`). `nonregular_published` fires only because
`'…/usr/bin/busy'.endswith('/bin/busy')` — the published path is the genuine oracle regular file, not
a materialised link, and every other L2 clause including `projection_ok` is true in the frozen score.
So the L1's "path-suffix false positive" reading is correct, and the root cause is the same
`same_rel` suffix matcher that `gap_check` itself relies on: it makes the combined gate reject an
honest receipt (L2) while under-constraining gap paths (CX-B/CX-C). One direction is a false positive
that decided the C1 honest stop; the mirror-image false negative is closed only by the projection
clause.

## 5. Calibration summary

- Rule vs claim text: "one `unpublished-entry` per symlink" is **not encoded** (no cap); "none for
  directories or devices", "at most one `depth-limited`", "no `unknown-chunk-handler`" **are encoded**
  and hold (N1–N11 all correctly reject: path-carrying structural gaps, null-path
  `unpublished-entry`, dir/device gaps, unmatched paths, dropped required gaps, unknown gap kinds,
  unknown structural kinds, over-cap structural counts).
- The `allowed` keys exactly cover the reader's kind vocabulary (`sqfs-list.py` emits
  `dir|symlink|block-device|char-device|fifo|socket`); `gap_rule_uncovered_kinds` is empty. The
  `fifo`/`socket` allowances are dead on the frozen data (no such rows) — harmless.
- No end-to-end wrong receipt exists at the measured revision; the defects are latent rule-contract
  defects (missing multiplicity cap, unchecked gap bookkeeping, unrepresentable escaping class,
  suffix-collision fragility), plus the live `same_rel` false positive that produced the L2 stop.

**Residual risk / verification gaps:** I did not re-run REA myself (the counter's fresh-run clause at
scoring time is the closure I relied on; its output is recorded in the frozen score, and the
`run.json` records confirm gap counts 264/86/3/3 with the same kind sequence). The
`rel_suffix`-normalization tolerance (a receipt using a differently-named carve dir, e.g.
`zzz_extract/bin/sh`, projects equal to the fresh run) is by design per the counter docstring and
shares the disclosed "receipt equal to a real run on the projection is accepted" limit; I flag it as
the boundary of that limit, not a new hole.

Evidence artifacts: `artifacts/R40W2C1Gaps/{gapaudit-output.txt,counterexamples-output.txt,gapaudit.py,cx.py}`.
Tooling: none installed or upgraded (stdlib Python only); scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1Gaps` removed after copying the artifacts.
