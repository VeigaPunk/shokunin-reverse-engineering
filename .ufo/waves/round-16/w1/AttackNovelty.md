# AttackNovelty — C1 advisory

**Axes:** depth and calibration. Source/data review only; no execution, admission, score, or target-capability finding.

## Counterexample to an overstated novelty claim

The answer “1.24.7 falls back to the 1.24.6 diff” is not new knowledge. The prior record already supplies that inference and all its inputs:

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:17-23,61-74` records the same-minor base law, closest-lower single-diff law, ordered architecture law, and requested 1.24.7 with diffs through 1.24.6.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/inventory.json:7338-7375,7394-7398,7689-7732` already pins the 1.24 base, the 1.24.6 diff identity, every base bucket, and that request's missing exact diff. Reprinting those identities, or calculating the minor's maximum patch, does not establish the proposed selector computation.

However, the old executable does **not** compute that relation: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py:351-388` emits all minor diffs and exact-file presence, not a selected diff; `:403-417` takes no GOOS/GOARCH. Thus the narrow C1 before-state in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/claims.json:4-8` is distinguishable from “no prior selection knowledge.”

## Exact computation that must be newly demonstrated

The delta must be a request/platform-specific **join**, not a new filename census: select the mandatory base, choose the greatest *positive patch no greater than the request* within that same minor, bind the chosen file's identity, and filter base buckets into source search order.

Strongest local contrast, **[INFERENCE: source-model expectations, not executed outputs]**, holding the installed root and linux/amd64 constant:

| Request | Required selection | Selected diff identity already pinned in round 15 |
|---|---|---|
| 1.24.5 | `exact_diff`, patch 5 — despite patch 6 being installed | `go1.24.5.json.diff`; size 106091; SHA-256 `5743f4335615fdc5aa8d7e3c2516a8223a3eb769ffd306b3344b79bef4ea7053` |
| 1.24.7 | `fallback_diff`, patch 6 | `go1.24.6.json.diff`; size 118810; SHA-256 `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6` |

Pins: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/inventory.json:7300-7375`. This pair defeats an implementation that merely reports the installed minor maximum while looking correct on the old 1.24.7 example.

For both requests the computed unpatched-base matches must be `[linux-amd64, linux, unix, amd64, all]`, not the inventory's alphabetic list and not cgo variants. Changing only GOOS to windows must give search order `[windows-amd64, windows, "", amd64, all]` and matches `[windows-amd64, windows, amd64, all]`. Base-key evidence: the same inventory `:7693-7721`; current installed base keys were also reopened read-only.

Source authority: S003, `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`, member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:108-109,122-145,148-166,177-178,205-239`. These establish search order, base-before-diff, bounded descending selection, UNIX membership, and ordered bucket retention. Source applies the chosen diff before reading buckets; the proposed preview does not, so its matches must remain explicitly **unpatched-base** matches with `patch_applied:false` and `evidence_class:'source_model'`.

## Missing evidence and smallest safe correction

This review inspected the proposal and prior evidence, not a retained round-16 selector invocation/result. The exact missing demonstration is the computed relation above, tied to the delivered implementation and its producing argv; expected values in this report are not that evidence.

Keep C1 bounded to **materializing the previously prose-inferred relation as a source-grounded computation**, and retain a contrasting request/platform result rather than counting copied hashes or filenames as new facts. This is a fixable novelty/evidence gap, not an observed axis tradeoff. Depth depends on the new computation; calibration depends on preserving the old knowledge baseline and the unpatched/source-model limits. No builds, tests, checks, target/source execution, or tool installs/updates were performed.
