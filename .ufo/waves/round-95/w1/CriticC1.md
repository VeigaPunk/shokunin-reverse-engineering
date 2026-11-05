# CriticC1 — attack on R95-C1 (receipt world-binding), round 95 attempt 1

Frozen at 4bda1d1dd3788973f10e61212b70df18b3b14ea0. Full record: `w1/CriticC1/attacks.md`.
Scope: attack only R95-C1. R95-C2 (craft block 34) was not in this item and was not attacked.

## Result

The strengthened instrument binds a receipt to the frozen label, its own revision string, the stdout/rc pair, and the verdict and counter pins. It does NOT bind it to the measured tree, the repair/imported pins, the unlabelled counts, or the public leg. The v5 self-verification is also skipped on the public CLI whenever `--json-out` is omitted, and that path exits 0. Four of these gaps are NOT covered by any named limit in `plans/round-95-claims.md`.

## Attacks (v2 `--root <clone> --rev 4bda1d1d…`, exit codes observed)

| id | forged | v2 exit | reasons | covered by named limit? |
|---|---|---|---|---|
| A1 | counts + label copied from identity donor; pins/rev honest; met False | 0 | [] | yes (provenance limit) |
| A1b | unlabelled counts (`silent 10`) from donor; `repaired 12 + silent 10 > scored 12` | 0 | [] | **no** |
| B1 | counts altered, label recomputed, met False | 0 | [] | yes (refusal labels free-form) |
| B1ctl | same, met True | 1 | label-not-frozen | refused |
| C1 | receipt met False, stdout says frozen met True | 1 | stdout-disagree | refused |
| D1 | separate writer, never ran a repair, honest pins | 0 | [] | yes (wholly re-authored) |
| E1 | revision = other commit with identical tool bytes, verifier `--rev` 4bda | 1 | revision-not-bound | refused |
| E1' | same, verifier `--rev` = other commit | 0 | [] | **no** (measured tree) |
| E2 (live) | v5 run with HEAD 5ad4c96d, `--rev 4bda`, selfverify ok=True | 0 (v5) / 0 (v2) | [] | **no** (measured tree) |
| F1x | `repair_sha256` = identity bytes | 0 | [] | **no** |
| G1x | `imported_r92_battery_sha256`/`imported_v2_sha256` forged | 0 | [] | **no** |
| H1x | `public_met false` inside a met-True receipt | 0 | [] | **no** |

Honest control (H) accepted, exit 0. Short `--rev` control accepted (v2 resolves it), `--rev` set to another commit refused, exit 1.

## v5 self-verification (`stop-boundary-repair-battery-v5.py`)

- Honest run with `--json-out`: exit 0, `selfverify ok=True reasons=0`.
- **Honest repair, no `--json-out`: exit 0, `selfverify ok=None reasons=0`, no receipt written.** The check is skipped; no named limit covers this, and the kill rule does not reach it because it checks only runs that pass `--json-out`.
- `--json-out` to `/dev/null`, a directory, or a missing parent directory: exit 1 by exception, before verification. These fail closed.
- Short `--rev` with `--json-out`: exit 1, `revision-not-bound`. `--rev` omitted with `--json-out`: exit 1, `revision-unresolvable`. `--rev` omitted without `--json-out`: exit 0 with no revision check.
- Answer: a repair command cannot skip verification itself, since it has no channel to `args.json_out`. The skip is reachable only by the caller omitting `--json-out`. I did not find a `--json-out` path that writes but cannot be re-read.

## Named-limit verdict

Limit quoted from the plan: "they do not authenticate provenance — a wholly re-authored triple whose stdout/rc/pins/revision/label all consistently describe the honest world at the honest revision is indistinguishable from an honest capture at the byte level". This covers A1, B1 (via the refusal-label limit) and D1.

Not covered: A1b (unlabelled counts and internal count consistency), E1'/E2 (revision is a verifier-supplied string, HEAD and the measured tree are never checked; the claim surface says "the measured tree"), F1x/G1x (claim lists the frozen r92 repair pin; v2 `pins-not-bound` checks only verdict and counter), H1x (`public_met` not bound), and the nojson skip.

## Named files

- `w1/CriticC1/attacks.md` (record and classification)
- `w1/CriticC1/attacks/ATK-{H,A1-F1,A1b,B1,B1ctl,C1,D1,E1,E2,F1x,G1x,H1x}-*.{json,stdout,rc}`, `attacks/d1-separate-writer.py`, `attacks/ref-*`, `attacks/v5-runs/*`
- `w1/CriticC1/scores/v2-ATK-*.{json,out}` (v2 outputs; `v2-ATK-E1-revC2.*` for the second E1 verifier revision)
- `w1/CriticC1.md` (this report)

Scratch `$S` (clone, probes, receipts) removed before yield. Clone HEAD was `4bda1d1d` at start; a same-tool-bytes commit `5ad4c96d` was created in the clone only, not the lane. No lane file was edited. No pacman, sysctl or host change was made.
