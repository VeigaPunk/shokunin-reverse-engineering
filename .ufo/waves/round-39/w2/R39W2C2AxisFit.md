# R39W2C2AxisFit — R39-C2 attacked as a DEPTH claim

**VERDICT: DEFECTS FOUND.** R39-C2 is *true as scored* (I reproduced `matched 20/20`, exit 0, 21/21
bindings true, `frozen_paths_changed []` at `6fdaf4f1`), and its table does sit in the craft section
with rule blocks `17 -> 18`, all resolved. It is **not** a measured *depth increment*: the axis's own
counting recipe is saturated at 10.00 before the landing, ~5 of the 8 rows are pre-held at the base,
the "20/20" is 9 distinct predicate decisions, the cause→action column the claim advertises is
**0% scored** (an 8-row nonsense-cause mutant still scores 20/20), the table's own round labels 2 of
this round's 6 frozen C1 carriers with a lossy action, and the interpreter silently mislabels a
non-firmware REA envelope as SquashFS triage. No claim byte was changed; all work is scratch + a
read-only clone.

Seat: leaf, no subagents, no background jobs. Tooling: **nothing installed, upgraded or removed**.

## 1. Command A at both revisions (the exact recipe, `SCORECARD.md:92-124`)

Ran verbatim at `a2f64e1da78afcf8cc39287106604dbcc270844c`, `52b0eb2907c704ed5f184c47b14c723208e5cbbc`
and (extra) `6fdaf4f162aff156fcef0e52998a5469c64fd6f0`:

| REV | knowledge files | mapped | dangling | rule blocks | resolved | coverage | **depth** |
|---|---|---|---|---|---|---|---|
| `a2f64e1d` (base) | 126 | 126 | [] | **17** | 17 | 10.00 | **10.00** |
| `52b0eb29` | 128 | 128 | [] | **18** | 18 | 10.00 | **10.00** |
| `6fdaf4f1` (measured) | 128 | 128 | [] | 18 | 18 | 10.00 | **10.00** |

So the expected `17 -> 18` holds and every block resolves at both revisions. **The new block is in
the craft section**: `## Queue-drain craft` spans `SKILL.md:81-347` at head (base `:81-318`), the
marker `<!-- sqfs-triage-table v1 -->` is at `SKILL.md:333`, the table runs `:334-346`, and the next
`## ` heading is `:348`. Craft grew 238 → 267 lines; rules 1-17 are byte-identical to base and block
18 is appended.

**QUALITY 75 finding (the decisive one).** Row 75 (`corpus/QUALITY.md:130`) says the depth surface is
"the SKILL/corpus craft section **and its counting recipe**" and an axis label is "checked against
those bytes". The bytes moved; **the recipe's number did not move and cannot** — `depth_score` is
`10*resolved/rules`, and every earlier block already resolved, so any added rule that cites a
≥1-line file resolves and the score is pinned at 10.00. The depth axis had **zero headroom at the
base**, so `17 -> 18` is a count of blocks, not a measurement of depth. Every depth claim that lands
after `a2f64e1d` is admitted by construction on this proxy. (Consistent with base saturation: the
same recipe reports 10.00/10.00 for coverage and depth at the round-38 tip.)

## 2. Fraction of the table already held at `a2f64e1d`

Row-by-row against the base prose table (`SKILL.md:1231-1243` at base, the round-36 "Decision table —
REA envelope signal to action") and `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`:

| new row | discriminant | held at base? | evidence |
|---|---|---|---|
| `dep-missing-le` | gap kind + `["sasquatch"]` | **yes, verbatim** | base `SKILL.md:1233-1235` names exactly this gap, dependency and handler |
| `in-tree-symlink-metadata` | `unpublished-entry` per kept link | **yes, verbatim** | base `SKILL.md:1239-1241`; r38 entry §Symlinks |
| `clean` | no gap, regular files published | **yes** | base `SKILL.md:1236-1237` |
| `escaping-symlink-removed` | `MaliciousSymlinkRemoved`, no gap | **yes** (BE) | r38 entry: K1 escaping link removed, "no gap is recorded" |
| `dep-missing-be` | `["sasquatch-v4be"]` on the BE handler | **yes** | r38 entry table row `before` on K1-K4 |
| `avm-marker-be-dropped` | BE=no separates it from damage | **half** | the cause (`-be` dropped when `bytes_used == mkfs_time`, S114) is in the r38 entry; the *outcome* (`extractor-failure`, 0 files) and the separation from damage were measured in round-39 **wave 1**, not at base |
| `body-extractor-failure` | `extractor-failure`, 0 files, BE=yes | **no** | `git grep -c -F extractor-failure a2f64e1d -- …` = **0** |
| `no-squashfs-chunk` | no `squashfs*` chunk at all | **no** | `s_major` = **0**, `s_minor` = **0** hits at base |

Base token counts (PROVINCE, SKILL, corpus/README, corpus/knowledge, corpus/SOURCES at `a2f64e1d`):
`sasquatch-v4be` 31, `unpublished-entry` 17, `missing-extractor-dependency` 8, `bytes_used` 6,
`squashfs_v4_be` 5, `mkfs_time` 4, `MaliciousSymlinkRemoved` 1, **`extractor-failure` 0**,
**`s_major` 0**, **`s_minor` 0**.

**Fraction:** 5 of 8 rows are pre-held (fully stated at base), 1 is half-held, **2 of 8 are new
decision content (~25%; ~19% if row 4 counts half)**. The machine-readable form is new for all 8, but
the *decision knowledge* is largely transcription, which is what the claim's own controls say too:
CTL-C2-5 (round-36 table transcribed) scores 8/20 and CTL-C2-6 (best table without `-be` and without
`MaliciousSymlinkRemoved`) scores 12/20 (`.ufo/waves/round-39/controls/ctl-c2-dev-scores.json`), i.e.
the round-39-specific discriminants decide 8 of 20 envelopes — matching my row count.

## 3. Is scoring 20 self-generated envelopes a real measurement of the table? (structure vs shape, r32/r34)

Partly, and less than the number claims.

**(a) What it does measure — real, not r32/r34.** The 20 envelopes are genuine REA `data` objects
(`evidence_id ev_…`, `operation extract_firmware`, `provider.id unblob 26.6.4`; e.g.
`corpus/evidence/round-39/c2/heldout/H01/envelope.json`), not hand-built JSON, and the labels were
fixed by the generator before the run. The controls show a feature-blind table cannot reach the
target (catch-all 4/20, gap-count 6/20, gap-kind 10/20, published-only 6/20, no-BE-no-SR 12/20), so
this is **not** the round-32 "text presence" or round-34 "size-keyed fixed-slice replay" family: the
scored reader parses REA-named fields, not fixture identity. `--json` on a scratch SKILL copy with
`clean` renamed to `zz-clean` returned `zz-clean` ×4 (`labels-rename.json`), so the labels do come
from the SKILL bytes and not from constants in the tool.

**(b) The 20 is 9.** Coarsening `P` to the table's own `0/>0` threshold, the 20 envelopes carry
**9 distinct predicate tuples**, one per class, and `body-extractor-failure` and
`version-minor-mismatch` collapse onto **one tuple covering 4 envelopes** (H15, H16, H19, H20):

```
H01,H02 clean-be            (squashfs_v4_be) () () n/a no >0
H03,H04 clean-le            (squashfs_v4_le) () () n/a no >0
H05,H06 escaping-…          (squashfs_v4_be) () () n/a yes >0
H07,H08 in-tree-…           (squashfs_v4_be) (unpublished-entry) () n/a no >0
H09,H10 dep-missing-be      … (missing-extractor-dependency) (sasquatch-v4be) n/a no 0
H11,H12 dep-missing-le      … (missing-extractor-dependency) (sasquatch) n/a no 0
H13,H14 avm-marker-be-…     … (extractor-failure) () no no 0
H15,H16,H19,H20 body-…      … (extractor-failure) () yes no 0
H17,H18 no-squashfs-chunk   () () () n/a no 0
```

The counter's own bindings make N structural: `classes_two_each` and `n_equals_twice_classes` both
true. Two replicates per class differ only in file contents/compression draw, never in a predicate
cell, so `matched == 20` is **9 of 9 decisions**, and one of the nine is decided by 4 replicates.
The claim states the sample size as 20; the score carries the weight of 9.

**(c) The cause→action column — the depth content — is 0% scored.** `sqfs-triage.py`'s docstring
declares `cause -> action` and `source` "Documentation only", and the counter compares only
`label == expected_label` (`class_match`, `c2-counter.py:389-390`; no rule index, no row text). I
replaced **all 8** cause cells with `THIS CAUSE IS DELIBERATELY WRONG -> DO THE OPPOSITE; ignore the
evidence` in a scratch copy: the interpreter exits 0 and returns **byte-identical labels for all 20**
(`labels-cause.json`). The header cell was excluded so the mutant stays a valid table (the header
check refuses a mutated header, exit 2 — a real grammar guard, but not a content guard). The claim's
own headline is "signature → cause → action"; only `signature → label` is measured.

**(d) Precedence is untested and inert.** Rows 6 and 7 each pin `symlink removed` (`yes` / `no`), and
rows 2/3 pin gap kind + dependency, so no held-out envelope can match two rows; "rows are tried top
to bottom, the first match wins" is stated in the block and never exercised. The one multi-signal
shape the round actually produced (below) resolves by `SR`, not by order.

**(e) Seed = freeze hash.** It prevents the author from *seeing* the instances (the hash cannot exist
before `8fcda41c`), and the regeneration binding is true. It does not make the shapes held out: the
8-row table and the 10-class generator (with its class → label map) were authored into the **same**
freeze commit `8fcda41c`, and the class list appears verbatim in the frozen claims. What the score
can and did falsify is that REA behaves as the recipes assumed — a real but narrow claim.

## 4. Counterexamples from the lane's own bytes

**(C1) The table mislabels 2 of this round's 6 frozen Core carriers.** Labelling every committed
`round-3[6789]/c1/K*/{before,after}.json` with the frozen interpreter (`real-envelope-labels.txt`):

```
round-39/c1/K5/after.json  escaping-symlink-removed  r=6  G=[unpublished-entry] SR=yes P=10
round-39/c1/K6/after.json  escaping-symlink-removed  r=6  G=[unpublished-entry] SR=yes P=8
```

K5 holds 2 in-tree + 1 escaping link, K6 1 in-tree + 2 escaping (frozen symlink tables,
`plans/round-39-claims.md`). The table returns the escaping label whose action is "expect the path to
be **absent**; never materialise the link" — while the same envelope carries `unpublished-entry`
gaps, i.e. two (K5) / one (K6) in-tree links are recorded present and the label's action tells the
reader to ignore them. 2 of 6 promoted carriers get a lossy action. The claims *disclose* the label
("images holding both symlink kinds … labelled `escaping-symlink-removed` by row order; no held-out
class"), so this is a routed defect, not a predicate failure — but it is a shape the round's own
carriers exhibit at 33% frequency and the held-out set deliberately excludes.

**(C2) Undisclosed domain overreach: a non-firmware envelope is labelled SquashFS triage.**
`corpus/evidence/round-27/c1/envelopes/jq-function-base.json` and
`corpus/evidence/round-26/c1/envelopes/function-base.json` are `operation analyze_function`,
`provider.id ghidra`. Both exit 0 with label **`no-squashfs-chunk`** and the cause "unblob's finder
dropped a truncated image, a `bytes_used` past the end or a non-4 `s_major`" (rule 1: handler `none`,
every other cell `*`). The base prose table has exactly the guard the executable table dropped —
`SKILL.md:1242-1243` "`operation` ≠ `extract_firmware`, or `provider.id` ≠ `unblob` … the receipt is
not comparable … do not relabel". The interpreter reads no verb and no provider, and the registry row
says it "labels REA envelopes" without a precondition, so the statement is over-broad as written.

**(C3) Two registered kill controls were not scoreable when frozen.** `CTL-C2-5-round36-le-transcribed`
and `CTL-C2-6-no-be-no-sr` as authored exit **2** with "cause -> action cell has no `->` separator";
the recorded 8/20 and 12/20 come from `….formatfix.md` first added at `72359309`, **after** the freeze
`8fcda41c` (`git cat-file -e 8fcda41c:…/tables/CTL-C2-5….formatfix.md` → absent). Both the broken
(input at freeze) and the fixed table are retained and both outcomes are in `ctl-c2-dev-scores.json`,
so this is not concealment; it is the QUALITY 80 pattern (a control input repaired post-freeze, so the
scored value certifies bytes the freeze never held) at its mildest — a format repair, not a weakened
shortcut. The claims' own ordering rule ("receipts land in their own commit before the first data
commit") holds.

## 5. Impacted axes

- **depth (primary).** The claim's attribution is defective on four measurable counts: (i) the
  recipe is saturated (`10.00` at base and at every later REV), so no depth delta is measurable;
  (ii) ~25% of the rows are new decision content, 5/8 pre-held at base; (iii) the depth-bearing
  columns are unscored (nonsense-cause mutant 20/20); (iv) `20/20` is 9 distinct decisions.
- **coverage (secondary, coupled).** C2 adds no coverage surface, but C1's K5/K6 receipts are the
  evidence that the triage table's mixed-signal label is lossy; if C1's symlink rule were ever
  revised, C2's rows 6-7 move with it (the w1 seat's shared-premise finding stands unresolved:
  both rows restate C1's rule).
- **calibration.** The interpreter's label is a statement about one envelope, and it now also fires
  outside its verb/provider domain (C2 above); unchanged by this landing, but the registry row's
  scope sentence is false as written.

## 6. Smallest safe correction (not applied — everything here is frozen)

1. **Guard the domain** in `sqfs-triage.py`: exit 2 (or a distinct `out-of-domain` label) unless
   `operation == extract_firmware` and `provider.id == unblob`. Restores the guard the prose table
   already states at `SKILL.md:1242-1243`; costs no claim byte, fixes (C2).
2. **Score the cause column**: have the counter assert the matched **rule index** (and one intended
   row per class) instead of `label` only — `body-extractor-failure` and `version-minor-mismatch`
   currently share rule 5 and any row with the right label passes.
3. **State the sample honestly**: N = 9 distinct predicate tuples (2 replicates per class, 4 for the
   shared tuple), or make the two replicates differ in one predicate cell so 20 is 20.
4. **Add the mixed-signal class** (one in-tree + one escaping link) to the table and to the held-out
   set: it is the shape 2 of 6 of this round's own carriers exhibit, and today it receives an action
   that contradicts its own gap list.
5. **Validate control-table format at freeze** (`sqfs-triage.py --table-only` over every registered
   control) so no kill control is unevaluable after the freeze (C3).

## 7. Evidence (commands, exit codes)

```
# command A, verbatim from SCORECARD.md:92-124, three REVs, cwd=<lane>
python3 - "$REV" <<'PY' … PY     -> depth 10.00/10.00/10.00; rule_blocks 17/18/18; exit 0

# counter at the measured revision (read-only --shared clone in $S)
git clone -q --shared <lane> "$S/clone"
python3 -I -B "$S/clone/tools/round-39/c2-counter.py" --root "$S/clone" \
  --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out "$S/c2-at-6fdaf4f1.json"
  -> rc 0, n 20, matched 20, met_target true, met_target_consistent true,
     bindings_false [], frozen_paths_changed []      [artifact c2-at-6fdaf4f1.json]

# held-out features (frozen interpreter, frozen SKILL)
python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json corpus/evidence/round-39/c2/heldout/H*/envelope.json
  -> rc 0, 20 results, 9 predicate-relevant tuples          [heldout-features.json]

# every committed round-36/37/38/39 C1 envelope (22 files)
python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json <22 paths>
  -> rc 0; K5/K6 = escaping-symlink-removed             [real-features.json, real-envelope-labels.txt]

# non-firmware envelopes
python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json \
  corpus/evidence/round-27/c1/envelopes/jq-function-base.json corpus/evidence/round-26/c1/envelopes/function-base.json
  -> rc 0, label no-squashfs-chunk on operation=analyze_function, provider=ghidra

# label-provenance mutant (scratch SKILL copy, clean -> zz-clean): rc 0, labels zz-clean x4
# cause mutant (all 8 cause cells replaced): rc 0, labels byte-identical to the frozen table (20/20)
```

Controls read, not re-run: `.ufo/waves/round-39/controls/ctl-c2-dev-scores.json`
(CTL-C2-0 exit 2; catch-all 4; gap-count 6; gap-kind 10; published-only 6; round-36-transcribed 8;
no-BE-no-SR 12; freeze table 20). Repos: all git calls read-only; the only `git init/clone` work is
the `--shared` clone under `$S` (removed).

**Limits of this report [INFERENCE where marked].** I did not re-run REA on any held-out or C1
carrier (provenance of the 20 envelopes is taken from their own `ev_ …`/`operation`/`provider`
fields, not re-derived). The "effective sample size = 9" count uses the table's own `0/>0`
`published files` threshold; under a stricter reading of `P` the tuples are 16 but the table cannot
distinguish them, so the scored decisions remain 9. QUALITY 75's exact remedy (whether a claim must
show a *score delta* or only that the counted surface moved) is [INFERENCE] from row 75's wording;
the score-neutral fact — `10.00` at the base — is observed.
