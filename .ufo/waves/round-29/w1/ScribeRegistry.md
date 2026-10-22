# ScribeRegistry — round 29, wave 1: draft registry rows

Seat `KaidokuR29.ScribeRegistry`, leaf, read-only on the lane. Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`,
measured revision `18be864a528873b2b70d8c94e31f880290249e90` (`git rev-parse HEAD`, 2026-10-22T20:25:31Z,
`artifact` `runs/head.txt`). No tool install or update; no network fetch; no REA; no git or jj write in the
lane or the fleet repo; all verification ran in a sandbox clone.

## Behavior

Read `SKILL.md:948-955` (`### Round-27/28 measurement registry`, five columns: Name, Kind / owner,
Entry / verdict map, Self-invocation, Pinned values / write scope; four existing rows round27-C1,
round27-C2, round28-C1, round28-C2), then drafted four rows in that exact format for the round-29
tools. Each row's command and observed result is grounded in a committed receipt or the round's
working-tree receipt, and re-derived where the tool permits it (both counters, freeze-gate, the
prefile success path).

**Draft**: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeRegistry/draft.md`
sha256 `417894aa6fa1c2d026cade06a3b3b1d38ac0b508ce3b988116548022176cd90b`
(each row is one line, 5 cells, verified: line lengths 2649/1942/2374/1494 characters).

Row names chosen: `round29-C1`, `round29-C2` (claims), `round29-freeze`, `round29-prefile`
(hygiene, no claim row). The draft names the hygiene rows explicitly as hygiene and cites QUALITY
rows 46/47 and mistakes M29-2/M29-1. The draft also notes that the section heading still reads
"Round-27/28" and may need renaming when the rows land — the L1's call.

## Gates run by this seat (all in a clone at 18be864a, never the lane tree)

Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q <LANE> .../ScribeRegistry/clone`;
HEAD `18be864a…`, `git status --porcelain` 0 lines.

| command | exact result | exit | UTC |
|---|---|---|---|
| `python3 -I -B tools/round-29/c1-fresh-naming.py --root <clone> --rev 18be864a…` | `named 122, right 122, wrong 0, no_name 30`; `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` | 0 | 2026-10-22T20:22:43Z |
| `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <clone> --rev 18be864a…` | `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1` | 0 | 2026-10-22T20:22:43Z |
| `python3 -I -B tools/round-29/freeze-gate.py --root <clone> --rev 18be864a… --disclosures corpus/claim-freezes-v2.tsv` | `audited 19, clean 2`, flagged 17 keys, `ABSENT 12 / NONE 5 / PIN_MISMATCH 0 / REVISED 15 / UNPINNED 6 / UNRESOLVED 9`, `disclosures.exact 19 of 19, mismatched [], missing [], stray []` | 0 | 2026-10-22T20:22:50Z |
| `… freeze-gate.py … --require-clean round-14` | `required_failed ['round-14']` | 1 | 2026-10-22T20:23:17Z |
| `… freeze-gate.py … --disclosures corpus/claim-freezes.tsv` (pre-v2 ledger) | `mismatched ['round-28']`, `exact 15 of 19` | 1 | 2026-10-22T20:23:17Z |
| `… freeze-gate.py … --rev deadbeef` | `{"claim": "R29-freeze-gate", "error": "git_failed: rev-parse --verify --end-of-options", "finding": "unevaluable"}` | 2 | 2026-10-22T20:23:17Z |
| `GIT_OPTIONAL_LOCKS=0 sh tools/round-29/prefile-check.sh <clone>` | `prefile: clean` | 0 | 2026-10-22T20:22:50Z |
| `sh tools/round-29/prefile-check.sh` (no argument) | `usage: prefile-check.sh <lane-root>` | 2 | 2026-10-22T20:22:50Z |
| `python3 -I -B tools/round-29/c1-fresh-naming.py --selftest` | `selftest cases=22 failures=0` | 0 | 2026-10-22T20:25:52Z |
| `python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest` | `selftest cases=19 failures=0` | 0 | 2026-10-22T20:25:52Z |

Tool blob hashes at 18be864a (`git show 18be864a…:<path> | sha256sum`):

- `tools/round-29/c1-fresh-naming.py` `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda`
- `tools/round-29/c2-filtered-unseen.py` `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801`
- `tools/round-29/freeze-gate.py` `25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2`
- `tools/round-29/prefile-check.sh` `34edba0460cf9c5d3eb51e15367b3f54718da81bdd6b993d8cacc03379dd5672`

The first two equal the `instruments` pins in `.ufo/waves/round-29/claims.json`; observation, one
`sha256sum` per blob.

## Findings

F1 **observation** — five of the receipts the draft cites are untracked at the measured tip:
`.ufo/waves/round-29/after/{c1-at-18be864a.txt, c2-at-18be864a.txt, c1-selftest.txt, c2-selftest.txt,
freeze-gates-v2.txt}` are absent from `git ls-tree -r 18be864a -- .ufo/waves/round-29/` (which lists
`after/freeze-gates-at-dbd87cfa.txt`, `after/ledger-before-fix.txt`, `after/prefile-check-red-r28.txt`,
`after/r27-c2-xpin-selftest-patched.txt`, the `before/` receipts and `claims.json`). Their provenance is
the lane working tree (mtime 2026-10-22T20:16:37Z–20:16:39Z), not a Git blob. Their values are not
thereby weakened: every value line was re-derived identically in a clone at 18be864a (table above).
The L1 has to commit those five receipts with the report; until then a reader at 18be864a cannot see them.

F2 **observation** — `tools/round-29/c1-fresh-naming.py` docstring lines 14 and 27 still describe
`corpus/evidence/round-28/c1/carriers.tsv` and `corpus/evidence/round-28/c1/tally.json`, while the code's
`EVDIR` is `corpus/evidence/round-29/c1` (line 50). Docstring-only staleness, no verdict effect; the
drafted row states the code's behaviour. Worth a two-line fix by the L1 (a change to the counter, though,
would need a new pin and a supersession note, so a docstring edit at filing is not free — leaving it is
the safer option this round).

F3 **observation** — `prefile-check.sh` takes no `--rev` and has no receipt against the lane; both
receipts are at the scratch clone `242b0d8b…` (clean → exit 0; with seat ExecR27SelftestFix's post-stop
bytes → ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md`, `prefile: NOT CLEAN (1 paths)`, exit 1,
restamped 2026-10-22T20:21:57Z in `prefile-check-red-r28-v2.txt`). The clean clone-at-18be864a run is a
fixture result (a fresh checkout is clean by construction) and the draft says so instead of implying the
lane was clean at 18be864a — it was not, because the F1 receipts were untracked. QUALITY row 47's
filing-time run against the lane remains the L1's to take.

F4 **observation** — `freeze-gate.py` has no `--selftest` and no pins of its own, so the row's
"Self-invocation" cell records green runs at `dbd87cfa` (stamp 20:06:07Z, exit 0) and at `18be864a`
(exit 0) plus the three red shapes this seat exercised (exit 1 require-clean, exit 1 ledger disagreement,
exit 2 unevaluable). `grep -n selftest tools/round-29/freeze-gate.py tools/round-29/prefile-check.sh`
returned no match (exit 1).

F5 **observation** — the pre-v2 ledger `corpus/claim-freezes.tsv` is detected as disagreeing with the v2
gate at exactly `round-28` (`exact 15/19`): its round-28 row still carries
`INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED`, which is the round-24 gate's pin-key behaviour, while v2
reads `producers_not_counters` and reports only `INSTRUMENT_UNRESOLVED`; the other four absent rows are
the two `claims-review.json` files and `round-28/claims-c2.json`. This is consistent with the disclosed
M29-2 corrections and is why the round-29 report must use `claim-freezes-v2.tsv`.

F6 **observation** — `clean=2` at 18be864a is `.ufo/waves/round-24/claims.json` and
`.ufo/waves/round-28/claims-c2.json` (from the audit JSON's `freezes` array), not the two round-29 claims.

F7 **inference from source, not run** — the counters' `entry_ok` requires the entry's `source:` line to
cite the claim's own new row (S088 for C1, S087 for C2) and forbids another valid new row; both selftests
carry the red case `red-cites-other-new-row` and both exit 1 on it (observed in the receipts and in this
seat's selftest re-runs).

## Touched surfaces

- Written: this report and
  `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeRegistry/{draft.md, runs/*, clone/}`.
- Lane: only `.ufo/waves/round-29/w1/ScribeRegistry.md` (this file). No lane file edited; `SKILL.md`
  not modified.

## Out of scope / not done

- `SKILL.md` was not edited (the draft is paste-ready for the L1).
- `prefile-check.sh` was not run against the live lane: 150+ seats were writing into it during this
  seat's window, so any result would be a transient snapshot, not the filing-time check QUALITY row 47
  prescribes.
- No network lookups (4byte.directory, openchain, Sourcify, ERC repos) and no REA call; none was needed
  to draft the rows.
- No review of the round-29 evidence data beyond what the counters read: the counters' own checks
  (`runs_ok`, `rows_complete`, `tally_equal`, `responses_complete`, `mismatches`) are reported as their
  observed output, not re-audited by hand.

## Artifacts (sha256)

| path (under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeRegistry/`) | sha256 |
|---|---|
| `draft.md` | `417894aa6fa1c2d026cade06a3b3b1d38ac0b508ce3b988116548022176cd90b` |
| `runs/c1.txt` | `2afa79b052dea2c04f9a9d3b2a9e9b124c312750aca704d7cfd694cac7ca5748` |
| `runs/c2.txt` | `ab4d6875a13c50ab66537952046af667948dbfc33abce3e4088a6993beaf6be8` |
| `runs/c1-selftest.txt` | `f384b3e5b15f1e8bcd5f9e15f22c7ae6025abd8aba9225eefcbd6b94d6292b18` |
| `runs/c2-selftest.txt` | `f3a6ef424faf285273b977a2a1bedbd46f1f41c2689f32508f534cc6d93a7ba4` |
| `runs/freeze-gate.json` | `217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c` |
| `runs/freeze-gate.txt` | `691cb506560995c3b9e4bb7bc2c64b09bd7a8d9970fcd845653f20d340512a69` |
| `runs/freeze-gate.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `runs/freeze-gate-red-require.txt` | `b2b727e70797677ecf7478d6a07943768af96a85ccddc98b3e17b3f258dd93db` |
| `runs/freeze-gate-red-disclose.txt` | `0efc34cb2f376da70ac7f5e7eaf5ceca86c729a4c972b545ee8258595db6acde` |
| `runs/fg-oldledger.json` | `ba47d0d9732cd9a8b29b5d17a7e55b94214c0135428bee013bb6fe679bad56cc` |
| `runs/fg-badrev.json` | `5cf7b9bb2ebf1f1a70c0ba786a2d0276e9b53ef9626628359e03e95da08bdf0a` |
| `runs/prefile-clean.txt` | `cae2bff3bddb21e81387945542b33c4df2279699267c045492386296115ab39d` |
| `runs/head.txt` | `84b370fc495ab4afdfd50b90dda93f19f0362e1549489f28b51a287639b4348b` |

Sandbox clone `clone/` is scratch and not listed (regenerable with the clone command above). This report's
own sha256 cannot be stated inside itself; the L1 can hash it after commit.
