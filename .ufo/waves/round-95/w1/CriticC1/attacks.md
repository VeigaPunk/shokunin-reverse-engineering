# CriticC1 — adversarial attacks on R95-C1 (receipt world-binding) at 4bda1d1d

Clone: `$S/clone` (scratch, deleted before yield), `git rev-parse HEAD` at start = `4bda1d1dd3788973f10e61212b70df18b3b14ea0`.
Frozen label: `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`.
Counters run with `--root <clone>`, `TMPDIR=<scratch>/tmp`, `--work <scratch>/work/...`.

## Real donor receipts (not hand-written)

| run | command (abbrev.) | exit | stdout | receipt |
|---|---|---|---|---|
| honest | `v5 --root C --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --rev 4bda1d1d --expect '<FROZEN>' --json-out honest-pos.json` | 0 | `selfverify ok=True reasons=0` / `<FROZEN> met True exit 0` | `v5-runs/honest-pos-receipt.json` |
| identity donor | same with `--repair-cmd .ufo/waves/round-93/controls/identity_noop.py --json-out identity.json` | 1 | `repaired 0 of 12; ... far-refused 0 of 12; fresh-roundtrip 0 of 2 met False exit 1` | `v5-runs/identity-receipt.json` |

Honest counts: `scored 12, repaired 12, silent 0, refused 0, far 12, far_refused 12, fresh_scored 2, fresh_repaired 2, fresh_far_refused 2, fresh_roundtrip 2, intact 6, wrong 0, unsafe 0`. Honest pins: `verdict_sha256 60026511…cbd4e3`, `counter_sha256 6fc81208…94b7f`, `repair_sha256 ce1b1769…70c1`, `imported_r92_battery_sha256 63e9df43…`, `imported_v2_sha256 f6ddb48b…`, `revision 4bda1d1d…`.

## Attack triples (`attacks/ATK-<id>-<slot>.{json,stdout,rc}`)

Scored with `tools/round-95/c1-agreement-v2.py --root <clone> --dir <seat>/attacks --prefix ATK-<id> --names <slot> --expect '<FROZEN>' --rev 4bda1d1d… --json-out <seat>/scores/v2-ATK-<id>.json`.
Per-attack prefix (`ATK-<id>`) is used because v2 takes `--names` from `pos,F1,F2,F3` only and one `--prefix` would collide across attacks; the directory is the spec's `--dir`.

| id | attack (what is forged) | slot | v2 exit | v2 reasons | classification |
|---|---|---|---|---|---|
| H (control) | none: honest triple | pos | 0 | [] | accepted (control) |
| A1 | fully consistent triple; pins, revision, tool, repair_sha256 are honest; **counts + label copied from the identity donor** (real different repair); label recomputed; stdout/rc matched; met False exit 1 | F1 | **0** | [] | **COVERED** by provenance limit (see below) |
| A1b | honest label and six label-segment counts; **unlabelled counts (`silent 10`, `fresh_repaired 0`, `fresh_far_refused 0`) copied from the identity donor**; met True; `repaired 12` kept | pos | **0** | [] | **NOT COVERED** (internal inconsistency: `repaired 12 + silent 10 > scored 12`) |
| B1 | counts altered (`repaired 12 -> 11`), label recomputed to match, met False exit 1, stdout/rc matched | F1 | **0** | [] | **COVERED** by refusal-label limit (see below) |
| B1ctl | same altered counts + recomputed label, but met True (control) | pos | 1 | `label-not-frozen` | refused (intended) |
| C1 | receipt says `met_target false, exit 1`; stdout says `<FROZEN> met True exit 0`; rc `0` | F1 | 1 | `stdout-disagree` | refused (intended) |
| D1 | **separate writer** (`attacks/d1-separate-writer.py`, never runs a repair) writes the whole triple; counts, pins, repair_sha256, revision copied from the honest run; met True exit 0 | pos | **0** | [] | **COVERED** by provenance limit (see below) |
| E1 | revision = full hash `5ad4c96d…` of a different clone commit with **byte-identical tool files** (v5, v3, v2 blobs verified equal); pins honest; verifier passes `--rev 4bda…` (frozen command) | pos | 1 | `revision-not-bound` | refused (intended by the frozen command) |
| E1' | same triple; verifier passes `--rev 5ad4c96d…` (the verifier names the other commit) | pos | **0** | [] | **NOT COVERED** (measured-tree binding; see below) |
| E2 | **live**: `v5 --root C` with HEAD `5ad4c96d…`, `--rev 4bda1d1d…`, real honest run; receipt records `revision 4bda1d1d…`; `selfverify ok=True` | pos | **0** | [] | **NOT COVERED** (live; HEAD is not checked; see below) |
| F1x | honest triple; `repair_sha256` replaced by the identity_noop bytes (`identity.json` value); counts honest | pos | **0** | [] | **NOT COVERED** (pinned r92 repair bytes unbound) |
| G1x | honest triple; `imported_r92_battery_sha256 = 0*64`, `imported_v2_sha256 = f*64` | pos | **0** | [] | **NOT COVERED** (imported pins unbound) |
| H1x | honest triple; `public_met false`, `public_label` = identity donor label; verdict `met True exit 0` | pos | **0** | [] | **NOT COVERED** (public leg contradicts verdict; unbound) |
| (short-rev control) | honest triple verified with `--rev 4bda1d1d` (8-char) | pos | 0 | [] | not an attack: v2 resolves `--rev` through `git rev-parse` |
| (wrong-rev control) | honest triple verified with `--rev 5ad4c96d…` | pos | 1 | `revision-not-bound` | refused (intended) |

Accepted attacks: A1, A1b, B1, D1, E1', E2, F1x, G1x, H1x (H is the control).

## Self-verification attacks on `stop-boundary-repair-battery-v5.py` (`main`, lines 250–257)

Exact observed runs (rc = process exit; all against the clone at `4bda1d1d`, HEAD `5ad4c96d` after the E-commit):

| run | args (abbrev.) | exit | observed | evidence |
|---|---|---|---|---|
| honest | `--repair-cmd tools/round-92/upx-…py --rev 4bda1d1d --json-out honest-pos.json` | 0 | `selfverify ok=True reasons=0`, `met True exit 0` | `v5-runs/honest-pos.stdout` |
| **nojson** | same, **no `--json-out`** | **0** | `selfverify ok=None reasons=0`, `repaired 12 of 12 … met True exit 0` (no receipt written) | `v5-runs/nojson.stdout` |
| **norev-nojson** | no `--rev` (default `worktree`), no `--json-out` | **0** | `selfverify ok=None reasons=0`, `met True exit 0` | `v5-runs/norev-nojson.stdout` |
| norev-json | no `--rev`, `--json-out` set | 1 | `selfverify reason: revision-unresolvable` | `v5-runs/norev-json.stderr` |
| shortrev | `--rev 4bda1d1d` (8 chars), `--json-out` | 1 | receipt written with short revision; `selfverify reason: revision-not-bound` | `v5-runs/shortrev.stderr` |
| devnull | `--json-out /dev/null` | 1 | `PermissionError: … '/dev/null.<rnd>.tmp'` (no selfverify line) | `v5-runs/devnull.stderr` |
| dirpath | `--json-out <existing directory>` | 1 | `IsADirectoryError: … '<tmp>' -> '<dir>'` | `v5-runs/dirpath.stderr` |
| nodir | `--json-out <dir>/does-not-exist/r.json` | 1 | `FileNotFoundError` | `v5-runs/nodir.stderr` |
| identity | identity_noop repair, `--json-out` | 1 | `met False exit 1`, receipt written and verified (`selfverify` line emitted) | `v5-runs/identity.stdout` |

Answer to "can a repair command make the verdict met True while self-verify is skipped?":
- The repair command runs inside `v3.score()` before the writer and has no channel to set `args.json_out`, so it cannot skip the step itself.
- The skip is reachable **by the caller omitting `--json-out`**: a fully honest repair command returns `met True exit 0` with `selfverify ok=None` and no receipt (`nojson`). The whole write-and-verify block (`if args.json_out:`, which holds both the write and the `if code == 0 and not selfverify["ok"]` fail-closed check) is skipped, so the exit stays 0.
- No `--json-out` path reproduced a write-then-unreadable receipt. Every un-writable target fails closed with exit 1 before `verify_receipt` (devnull, dirpath, nodir). A written path is re-read at the same name, so a split is not reachable from the public CLI.
- NOT TESTED: a repair that spawns a detached process rewriting the receipt after the counter exits. That is post-verify tampering of receipt-at-rest, not a verdict bypass; no run was made.

## Classification of accepted attacks against `plans/round-95-claims.md`

Quoted limit (Named limits, plans/round-95-claims.md line ~108):

> "The strengthened bindings bind the receipt to the world it claims; they do not authenticate provenance — a wholly re-authored triple whose stdout/rc/pins/revision/label all consistently describe the honest world at the honest revision is indistinguishable from an honest capture at the byte level, and catching it needs independent stdout/rc custody, not another receipt field."

> "The honest world's `--expect` binding runs only when `met_target` is true; refusal labels are legitimately free-form."

> "The fixture set is the four committed forgeries, not a claim about unlisted forgery classes."

Claim surface (R95-C1, Surface): "Calibration here = a receipt that exits 0 is bound to the world it claims: the frozen label, the receipt's own counts, the measured tree and the pinned bytes."

- **A1 — COVERED.** Fully re-authored, consistent at the honest revision with honest pins; the only world evidence is the receipt, which the limit names.
- **B1 — COVERED.** Met-False refusal with a recomputed label; the limit quoted above says refusal labels are free-form and no world-side counts exist to bind to.
- **D1 — COVERED.** Wholly re-authored by a separate writer with honest pins; exactly the limit's "wholly re-authored triple".
- **A1b — NOT COVERED.** The label binding only recomputes six label segments. The receipt's own unlabelled counts (`silent`, `fresh_repaired`, `fresh_far_refused`) are not bound, and `repaired 12 + silent 10 > scored 12` is accepted. The surface says "the receipt's own counts"; no named limit excludes unlabelled counts or internal count consistency.
- **E1' and E2 — NOT COVERED.** Surface says "the measured tree". v2 and v5 bind `receipt.revision` only to `resolve(--rev)`, where `--rev` is a string the verifier supplies. Neither checks `--root`'s HEAD or the measured worktree. E2 shows a run whose HEAD is `5ad4c96d` records `4bda1d1d`, and both selfverify and v2 accept. The limit about provenance covers "re-authored triples … at the honest revision"; E1' and E2 are not described by that wording, and E2's tree bytes are identical, so the gap is in the binding mechanism, not in what was measured.
- **F1x, G1x — NOT COVERED.** Surface promises "the pinned bytes"; claims.json lists the frozen r92 repair `ce1b…` among the pins. v2's `pins-not-bound` checks only `verdict_sha256` and `counter_sha256` (docstring line 15–16). `repair_sha256`, `imported_r92_battery_sha256`, `imported_v2_sha256` are written by v3 (lines 324–328) and never compared to the pinned bytes. The named limit covers "pins", but only as a consistent-triple case; here the pinned bytes are wrong and accepted.
- **H1x — NOT COVERED.** `public_met false` contradicts `met_target true` in the same receipt; neither v2 nor v5 binds `public_met` / `public_label`.
- **Nojson / norev-nojson (self-verify skipped) — NOT COVERED.** Claim (Surface step 1): "receipt self-verification before a met-True exit 0 (re-read the receipt …) … fail closed to exit 1 on any failed binding." The `ok=None` path exits 0 with no receipt and no verification, and no named limit mentions it. The kill rule ("honest run selfverify not ok") checks only the run that passes `--json-out`, so this path is not caught by the frozen target.

## Honest verdict on C1's falsification

The strengthened instrument does bind a receipt to the frozen label (B1ctl), its own revision string (E1 with frozen `--rev`), its stdout/rc (C1), and the verdict and counter pins (F3 in the committed battery). It does not bind it to the measured tree (E1', E2), to the repair and imported pins (F1x, G1x), to unlabelled counts (A1b), or to the public leg (H1x), and v5's self-verification is skipped on the public CLI when `--json-out` is omitted (nojson, exit 0). These are NOT covered by the named limits.

## Files written

- `attacks/ATK-H-pos.{json,stdout,rc}` (control), `attacks/ATK-A1-F1.{json,stdout,rc}`, `attacks/ATK-A1b-pos.{json,stdout,rc}`, `attacks/ATK-B1-F1.{json,stdout,rc}`, `attacks/ATK-B1ctl-pos.{json,stdout,rc}`, `attacks/ATK-C1-F1.{json,stdout,rc}`, `attacks/ATK-D1-pos.{json,stdout,rc}`, `attacks/ATK-E1-pos.{json,stdout,rc}`, `attacks/ATK-E2-pos.{json,stdout,rc}`, `attacks/ATK-F1x-pos.{json,stdout,rc}`, `attacks/ATK-G1x-pos.{json,stdout,rc}`, `attacks/ATK-H1x-pos.{json,stdout,rc}`
- `attacks/d1-separate-writer.py` (the D1 writer; never runs a repair)
- `attacks/ref-honest-pos.{json,stdout,rc}`, `attacks/ref-identity.json` (donor references)
- `attacks/v5-runs/*.{stdout,stderr}`, `attacks/v5-runs/honest-pos-receipt.json`, `attacks/v5-runs/identity-receipt.json`, `attacks/v5-runs/honest-pos.{stdout,stderr,rc}`
- `scores/v2-ATK-*.json`, `scores/v2-ATK-*.out`, `scores/v2-ATK-E1-revC2.json`, `scores/v2-ATK-E1-revC2.out`
