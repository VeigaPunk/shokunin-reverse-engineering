# R25 a3 wave 1 — C1 rerun at three revisions (seat C1Rerun)

Date: 2026-10-22. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (HEAD 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76, `git rev-parse HEAD`; `git status --porcelain` on the instrument: clean).

## Verdict

| Attack | Result |
|---|---|
| Instrument digest at 3 revs equals claims.json pin | holds |
| Before rev: items 5, mismatches 5, exit 1 | holds (matches frozen a2 receipt byte for byte) |
| L1 C1 rev 0e333eb: items 5, mismatches 0, exit 0 | holds |
| Lane tip 08c7a72: items 5, mismatches 0, exit 0 | holds |

## Instrument digest vs pin

Pin (claims.json `instruments["tools/round-25/a2/c1-calibration.py"]`):
`4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee`

Command per rev: `git -C <lane> show <REV>:tools/round-25/a2/c1-calibration.py | sha256sum` (exit 0 each).

| Rev | sha256 | Equal to pin |
|---|---|---|
| 9dcd11ecb412fe4828f274580018039b8edbc05a | 4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee | yes |
| 0e333eb2fc25f538a99058761f379845f2534c42 | 4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee | yes |
| 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76 | 4378af84fa8e036f62e85e81a07d21d0ed899a34b56f790a4682f0c965356eee | yes |

Working-tree file also hashes to the same value (observation), so the executed script is the pinned blob. Ancestry observed: 9dcd11e is ancestor of 0e333eb (`git merge-base --is-ancestor`, echo 0), and 0e333eb of 08c7a72 (echo 0).

## Runs

Command: `python3 -I -B <lane>/tools/round-25/a2/c1-calibration.py --root <lane> --rev <REV>`.

| Rev | items | mismatches | exit | UTC |
|---|---|---|---|---|
| 9dcd11e (before) | 5 | 5 | 1 | 2026-10-22T10:43:59Z |
| 0e333eb (L1 C1) | 5 | 0 | 0 | 2026-10-22T10:43:59Z |
| 08c7a72 (tip) | 5 | 0 | 0 | 2026-10-22T10:43:59Z |

Excerpts (observation): before `"items": 5, "mismatches": 5`; both after revs `"items": 5, "mismatches": 0` with all five detail items `"match": true`. Per-item before mismatches: I1 false, I2 false, I3 false, I4 stated 78/78 vs observed 107, I5 stated 88-116 vs observed 95-266.

**Before=5 and after=0: hold (observation).** Exit codes 1/0/0 observed on bare runs with stdout to /dev/null; the first trio piped through `tee` and my `EXIT=$?` captured tee's status (0), a capture flaw in my harness, corrected by the bare reruns. JSON bodies from the first trio are the saved evidence below.

## Cross-checks

- Frozen receipt corpus/evidence/round-25/a2/before/c1-calibration.json is byte-identical to my fresh before output (`cat`, same JSON; observation).
- I4's observed knowledge counts (107 at 0e333eb, 108 at tip) agree with the C2 claim numbers 107 before / 108 after (observation; consistency, not proof).
- Instrument read-only verified by reading its source: reads blobs via `git cat-file --no-replace-objects`, prints one JSON object, writes no files; safe to run inside the read-only lane.

## Artifacts (scratch, sha256)

- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C1Rerun/out/c1-9dcd11e.json — 24c295c2377ff46bebec02325aaa82d1360c08b890a0569af30319a1c8affb53
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C1Rerun/out/c1-0e333eb.json — 38fe3dc869a240f2327077c902cf0e59a7c8d1e102aae8ef6d4aa659e686064a
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C1Rerun/out/c1-08c7a72.json — d6be83a566570f0abd6ad8b0dbc38bc83cea7bbd6e2c095e697426229ba91591

Tooling directive: no tools installed or upgraded; existing python3/git used. No pacman, uv, or npx activity.

## Residual risk and verification gaps

- I ran and hashed the pinned instrument and read its logic, but did not independently re-derive items I1-I5 from the raw blobs; item truth rests on the instrument once its pin is confirmed (inference from pin equality, not a second counter).
- Exit codes observed on a second run after the tee flaw; single-run exit evidence for the exact tee-piped invocations is not retained (unknown, immaterial: stdout JSON identical across runs).
- `--rev` variants beyond the three assigned revs not probed (out of scope).
