# R39-C1 pre-freeze controls

Ten controls for the DRAFT `P39-C1` (six-carrier standard big-endian SquashFS v4
→ Core) in `plans/round-39-claims.md`. They are designed to be applied on top of
the base `a2f64e1da78afcf8cc39287106604dbcc270844c` in a scratch clone, after
(or, for CTL-C1-5, inside) the round-39 freeze commit, and scored with the
round-39 counter. Nothing here is a claim, a counter, or lane content; the L1
integrates.

## Layout

| path | what |
|---|---|
| `CTL-C1-*/control.json` | exact overlay list, generated K5/K6 mode, doc blocks, commit order, expected verdict |
| `CTL-C1-*/overlay/` | static files mirroring lane paths (K1–K4 `after.json`; all doc blocks are generated from `_shared/`) |
| `CTL-C1-*/generated-manifest.json` | evidence ids of the static K1–K4 receipts |
| `_shared/` | exact added blocks: Core section, frontier note, two SOURCES rows, README row, knowledge entry |
| `_harness/fabricate_receipts.py` | builds after-receipts from frozen metadata only (no REA); modes `copy38`, `forge-old`, `forge-remint`, `materialise`, `wrong-gap-kind`, `escaping-gap`, `extra-gap`, `failed-chunk` |
| `_harness/apply_control.py` | applies one control in a scratch clone and runs the counter |
| `_harness/receipt_probe_NOT_COUNTER.py` | receipt-only reference probe (not the counter); used to score the controls below |
| `_harness/example-carriers.json`, `_harness/example-symlinks/` | dry-run metadata. K1–K4 real; **K5/K6 are fixtures** |
| `evidence/` | live-vs-fabricated run, xpin verdicts, probe receipts, suite summary |

`xpin-attribute.mjs` requires both `--pkg65` and `--pkg67`; this host has no 6.7.0 root, so both
flags point at the 6.5.0 root and the tool's 6.7.0 column is vacuous. Both harness scripts print
that disclosure at startup (and warn if `--pkg65`'s `package.json` version is not 6.5.0); only
the 6.5.0 column is used anywhere.

## Applying

```bash
S=$(mktemp -d /fast/scratch/hyaku/r39ctl.XXXX)
git clone -q <LANE> "$S/clone"          # scratch only; never the lane
# ... author the freeze commit in "$S/clone" (carriers.json, counter, xpin, oracles,
#     symlinks.tsv per carrier) and export FREEZE=$(git -C "$S/clone" rev-parse HEAD)

# post-freeze controls
python3 _harness/apply_control.py --control CTL-C1-3 --clone "$S/clone" \
  --freeze "$FREEZE" --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --receipt-dir "$S/receipts"

# CTL-C1-5: stage the complete freeze content in the working tree first, then
python3 _harness/apply_control.py --control CTL-C1-5 --clone "$S/clone" \
  --mode in-freeze --pkg65 <REA650_PKG_ROOT> --receipt-dir "$S/receipts"
```

The applier substitutes `{{ENTRY}}`, `{{STEM}}`, `{{SID}}`, `{{SID2}}` and
inserts the SOURCES row after the `## Registry` table and the README row after
the `## Coverage map` table. Default entry
`corpus/knowledge/2026-10-26-r39-sasquatch-be-squashfs-promotion.md` — freeze the
counter with this constant or pass `--entry`.

Static overlays carry `subject.local_path` under
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/...`; the predicate checks the
subject **digest** against the frozen pin, not the path.

## Commit order

| control | order relative to the freeze |
|---|---|
| CTL-C1-0 | none; measured rev = freeze |
| CTL-C1-1 | commit 1 receipts, commit 2 docs |
| CTL-C1-2 / 3 / 4 / 6 / 7 / 8 / 9 | commit 1 receipts, commit 2 docs |
| CTL-C1-5 | receipts and docs **in the freeze commit**; measured rev = freeze |

## Controls and required verdicts

`carriers_matched` is what a correct counter must report at the measured rev.
"Defeats" means the control is ranked by how likely it is to make a receipt-only
counter exit 0.

| rank | control | shortcut | required verdict | refusing binding | defeats? |
|---|---|---|---|---|---|
| 1 | **CTL-C1-3** | six fabricated receipts, ids re-minted by xpin | **exit 0, 6/6** as drafted — no receipt-only counter can refuse it | none; needs a non-receipt binding (see report) | certain |
| 2 | CTL-C1-5 | green bytes committed in the freeze commit itself | exit 1, 0/6 | first add strictly descends from the freeze (`add != freeze`) | high if ancestry is non-strict |
| 3 | CTL-C1-4 | in-tree symlink materialised as a file, gap dropped | exit 1; K2 (+ in-tree K5) fail | gap set equality, not subset | medium |
| 4 | CTL-C1-7 | escaping symlink kept as a gap | exit 1; K1 (+ escaping K6) fail | no gap on an escaping path | medium |
| 5 | CTL-C1-6 | in-tree gap kind rewritten | exit 1; K2 (+ K5) fail | gap kind equality | medium-low |
| 6 | CTL-C1-9 | handler named, chunk `extraction_failed: true` | exit 1, 0/6 | no failed chunk | low-medium |
| 7 | CTL-C1-8 | extra gap on a published regular file | exit 1, 0/6 | gap path set equality | low-medium |
| 8 | CTL-C1-2 | fabricated receipts keeping stale ids | exit 1, 0/6 | xpin 6.5.0 recomputation == stored id | low |
| 9 | CTL-C1-1 | round-38 receipts copied, K5/K6 absent | exit 1, 4/6 | `carriers_matched == 6` | very low |
| 10 | CTL-C1-0 | do nothing | exit 1, 0/6 | receipts absent | none |

Each `control.json` carries the per-carrier expectation and the isolated
binding.

## Observed dry run

Against `receipt_probe_NOT_COUNTER.py` on a fixture freeze (six carriers; K5/K6
metadata fixtures): every control scored exactly as its `control.json` says, and
**only CTL-C1-3 passed (exit 0, 6/6)**. See `evidence/suite-summary.md` and
`evidence/suite-receipts/`.

## The finding that matters

A fabricated receipt matches a real REA run on every field P39-C1 names; the
evidence ids still differ, because they embed per-run paths
(`evidence/live-vs-fabricated.md`). Therefore:

- a receipt-only counter cannot refuse CTL-C1-3 — and neither can a counter that
  re-runs REA and accepts when the committed receipt *agrees* with the run;
- the smallest safe correction is to move the run into the counter and score
  from the counter's own envelope (normalized fields only), so the committed
  JSON is no longer the evidence;
- if the claim wants the committed receipt to remain evidence, it must add an
  unforgeable provenance binding, which repo content alone cannot supply.
