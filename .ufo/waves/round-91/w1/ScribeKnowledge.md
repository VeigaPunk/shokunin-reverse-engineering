# ScribeKnowledge — round 91 knowledge draft (R91-C1, R91-C2 sources)

Seat: ScribeKnowledge (scribe). Lane `kaidoku-shokunin`, round 91, attempt 1. Declaration `deb2765a55fef0e4e81500a027dfe59951b69e87`.

## Output

- `.ufo/waves/round-91/w1/ScribeKnowledge/entry-draft.md` — new file, 97 lines. Not written under `corpus/`.

## Checks run (command, exit, result)

- `curl -sL -m 60 -o <scratch>/tmp/p_unix.cpp https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` → rc 0. `sha256sum` → `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`, 24181 bytes (matches S313).
- `sed -n '476p;485p;496p;504p' <p_unix.cpp>` → `unpackExtent` header, `fi->readx(&hdr, szb_info);`, `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)`, `fi->readx(ibuf+j, sz_cpr);`.
- `sha256sum` of `tools/round-91/upx-stop-boundary-repair.py`, `tools/round-91/stop-boundary-battery.py`, `tools/round-90/upx-later-block-battery.py` at the lane HEAD → match `claims.json` pins (`473bb3a9…`, `5998b6bd…`, `5462ef13…`). `tools/round-91/depth-blocks-v3.py` (`bcf6c4ea…`) and `record-cells.py` (`87ff5844…`) also match.
- `/usr/bin/upx --version` → `upx 5.2.0`; `sha256sum /usr/bin/upx` → `cf2f6e7c…c969` (matches pin).
- `git clone --shared` to `<scratch>/clone`, `git checkout -q deb2765a…` → `rev-parse --show-toplevel` printed the clone dir. Then `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` → `SELFTEST cases=4 failures=0`, rc 0.
- Read receipts (not re-run): `.ufo/waves/round-91/pre/c1-base-round90-repair.json` (label `refused 0 of 8; unsafe 2; intact 4 of 4`, exit 1); `.ufo/waves/round-91/l1/scores/c1-at-declaration.json` (label `refused 8 of 8; unsafe 0; intact 4 of 4`, exit 0, met true, per-cell `stored_total`); `.ufo/waves/round-91/l1/scores/c1-regression-at-declaration.json` (label `P1 6 of 6; P2 4 of 4; P3 4 of 4`, exit 0, all controls true).
- Frozen counters were not re-run. This seat drafts; it does not reproduce.

## Findings for the L1

1. The `stored_total` fields show the total cannot decide the class. On `jq`, `xxd`, `docker-init` the +7 walk equals `u_len`, the same as intact. On `libz` the intact and +7 walks both total 98,592. The −7 walks equal `u_len` on `xxd` and `docker-init` too, so the geometry test is not one-sided.
2. Geometry-only refusal, derived from those fields [INFERENCE]: refuses 3 of 8 tampered cells and the intact `libz`. The frozen label fails. The measured count is not in the lane.
3. **Existing corpus entry defect.** `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` (landed in `f7f5153b3`) cites `.ufo/waves/round-91/w1/ExecCandidate/` as the measured home of the cheap-rule counts. That directory does not exist; `swarm-registry.json` lists `ExecCandidate` with no output. It also says the regression receipt is "recorded in the round-91 lesson". `corpus/lessons/round-91.md` line 55 still says it is pending. The receipt does exist at `l1/scores/c1-regression-at-declaration.json`. The draft cites that path instead, and marks the cheap-rule count pending. The L1 should correct the landed entry by a new entry, per CORPUS.md's correction rule, not by rewriting it.
4. Source line ordering. The seat spec requires `source:`, `verified-at:`, `recheck:` as the first three lines. The draft does that. The existing corpus entries put a heading first. The L1 should choose one form when integrating.

## Out of scope

- No edits to the lane, `corpus/`, `SKILL.md`, `tools/`, `.ufo/state/`, or the fleet root.
- No installs. No pacman use.
- Scratch `/fast/scratch/hyaku/kaidoku-r91/ScribeKnowledge` removed before yield.

## Files written

- `.ufo/waves/round-91/w1/ScribeKnowledge/entry-draft.md`
- `.ufo/waves/round-91/w1/ScribeKnowledge.md` (this report)
