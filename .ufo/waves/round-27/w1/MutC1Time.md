# R27-C1 mutation probe: the counter's time and package gates

Seat: KaidokuR27.MutC1Time. Date 2026-10-22. Target: `tools/round-27/c1-rename-identity.py`
(pinned, sha256 `e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7`).

What I attacked: the two gates that are only labels plus one commit-time lookup, namely
`utc_start` versus the counter's own commit time, and `pkg_version` / `pkg_json_sha256`
versus the frozen 6.5.0 constants. I also asked whether a later rewrite of the counter or
a delete and re-add of an envelope can move the time anchor, and whether a run that really
happened before the counter commit can be exposed by any committed byte.

Verdict in one line: the label gates hold and the time anchor is anchored to the earliest
add commit, so neither a rewritten counter nor a re-added envelope can loosen them; but the
actual run time and the actual package identity are self-declared facts that no committed
byte can attest.

## How the probe ran

- Sandbox clone of the lane at `a4f674b3`: `/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Time/clone`.
- Green fixture built by the counter's own builder (`_build_green`, counter line 361) from the
  lane bytes of the counter and of `tools/round-26/recompute-ids.py`
  (sha256 `89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b`).
  Fixture timeline: base commit 2026-10-22T10:00:00Z, counter commit 11:00:00Z
  (epoch 1792666800), data commit 12:00:00Z; every `runs.tsv` row says `utc_start`
  2026-10-22T11:30:00Z; every envelope is first committed at 12:00:00Z.
- Baseline, command
  `python3 -I -B .../clone/tools/round-27/c1-rename-identity.py --root fix/green --rev HEAD --base b0a21e5e`:
  exit 0, `rows_complete=16/16 entry_ok=1`.
- Each mutant: clone the pristine green fixture, mutate one thing, commit with a fixed
  author and committer date, run the same counter command. Run at 2026-10-22T15:02Z
  (`results.json` field `utc_run`). The lane was only read; no lane file was written.

## Mutants

| mutant | expected detector | counter output excerpt | exit | verdict |
|---|---|---|---|---|
| m1 `utc_start` one second before the counter commit (`10:59:59Z`) | time gate | `INCOMPLETE jq analyze: base: utc_start 2026-10-22T10:59:59Z not after counter commit`, `rows_complete=15/16` | 1 | killed |
| m2 `utc_start` in local time with an offset (`13:30:00+02:00`) | time gate | `INCOMPLETE jq analyze: base: utc_start 2026-10-22T13:30:00+02:00 not after counter commit`, `rows_complete=15/16` | 1 | killed |
| m2b `utc_start` in this host's own local time (`08:30:00-03:00`) | time gate | `INCOMPLETE jq analyze: base: utc_start 2026-10-22T08:30:00-03:00 not after counter commit`, `rows_complete=15/16` | 1 | killed |
| m3 the counter file itself is rewritten after the data commit | time anchor must stay at the original add | `rows_complete=16/16 entry_ok=1`; `git log --diff-filter=A` for the counter path still returns only `1792666800` | 0 | survived (no effect, and none available) |
| m3b the counter file is deleted and re-added after the data commit | time anchor must stay at the original add | `rows_complete=16/16 entry_ok=1`; counter path add list `1792674000 1792666800`, the counter takes the last, so the anchor stays 1792666800 | 0 | survived (no effect) |
| m4 one envelope is deleted and re-added later | counter should notice the re-add | `rows_complete=16/16 entry_ok=1`; envelope add list `1792674000 1792670400` | 0 | survived (re-add is not visible, but cannot help either) |
| m4b a pre-counter envelope is deleted and re-added after the counter | time gate must catch the laundering | `INCOMPLETE jq analyze: base: envelope first committed before the counter`, `rows_complete=15/16`; envelope add list `1792674000 1792665000` | 1 | killed |
| m5 `pkg_version` = `6.5.0-beta` | package gate | `INCOMPLETE jq analyze: base: package 6.5.0-beta/a500302319c1 not the frozen 6.5.0`, `rows_complete=15/16` | 1 | killed |
| m6 `pkg_json_sha256` in upper case | package gate | `INCOMPLETE jq analyze: base: package 6.5.0/A500302319C1 not the frozen 6.5.0`, `rows_complete=15/16` | 1 | killed |
| m9 `pkg_json_sha256` of the installed 6.7.0 package | package gate | `INCOMPLETE jq analyze: base: package 6.5.0/3f6c47fb12c8 not the frozen 6.5.0`, `rows_complete=15/16` | 1 | killed |
| m7 the run really happened before the counter commit (envelope written at 10:30, committed only at 13:00) but `utc_start` claims 11:30 | nothing can see this | `rows_complete=16/16 entry_ok=1`; committed tree is byte-identical to green apart from the fixture's stray `.pyc` | 0 | survived |
| m8 `utc_start` exactly equal to the counter commit second (`11:00:00Z`) | boundary | `rows_complete=16/16 entry_ok=1` | 0 | survived (equality is accepted) |

## Forgery classes that no committed byte can expose

1. **When the run really happened.** `utc_start` is a free string in `runs.tsv`; the counter
   only parses it (counter line 105, strict `%Y-%m-%dT%H:%M:%SZ`, only the `Z` form parses) and
   compares it with the counter's commit time (line 245). Nothing else in the repository records
   an execution time: a real REA envelope carries `meta` with only `command` and `duration`
   (checked at `corpus/evidence/round-26/c1/envelopes/analyze-base.json`), the hashed projection
   in `tools/round-26/recompute-ids.py` has no time field, and Git records commit times, not file
   creation or run times. So a run made at 10:30 and committed at 13:00 with a label of 11:30 is
   indistinguishable from a genuine run: mutant m7 exits 0 with 16 of 16. The only hard constraint
   is that the evidence was committed after the counter, not that it was produced after it.
2. **Which package really ran.** `pkg_version` and `pkg_json_sha256` are self-declared strings
   compared against constants (counter line 247). The counter never opens the installed
   `package.json`; it cannot tell 6.5.0 from 6.7.0 behind correct labels. The evidence id covers
   subject, parameters and results, not the tool version, and the 6.5.0 id rule is public, so a
   6.7.0-produced payload can be given a 6.5.0-shaped id. Mutants m5, m6 and m9 kill wrong labels
   only, never a wrong reality behind a right label.

Both classes are the same defect in kind: the claim is a label in a table, with no attested ground
truth in the repository. Only an external attestation (a signed run log, or a stamp the tool itself
signs) could close them.

## Other findings

- **The time anchor is the earliest add commit, which is the strict side.** `first_commit_time`
  (counter lines 98 to 100) takes the last entry of `git log --diff-filter=A`, which is the oldest
  add commit. Therefore m3b (counter deleted and re-added) and m4 (envelope deleted and re-added)
  cannot move the anchor later, and m4b shows that a pre-counter envelope re-added after the counter
  is still caught. Raising the anchor would require rewriting the history that holds the original
  add commit, which the lane's frozen commit pin forbids. Observation, verified by the probes above.
- **The gate is "not earlier than", not "strictly after".** m8 is accepted: a label equal to the
  counter's commit second passes, while the reason text says "not after counter commit". The wording
  overstates the rule. In the lane the counter was added by commit `a4f674b3` at epoch 1792680683
  (2026-10-22T14:51:23Z), so a label of `2026-10-22T14:51:23Z` or later passes.
- **The counter never checks its own bytes at the revision.** It hashes the envelope, the table and
  the recomputed id, but not `tools/round-27/c1-rename-identity.py` at the revision. A rewrite of
  that path in the revision (m3) is invisible to the counter. The executed file is the pinned
  working-tree copy, so the rewrite cannot change the verdict, and the lane's pin on the frozen
  tree is the only defence. Observation.
- **Not executed, outside this card:** `load_recompute` (counter line 111) reads
  `tools/round-26/recompute-ids.py` from the revision, not from the working tree, so the id rule in
  force is the one in the revision tree. I did not probe that; it is flagged for another seat.

## Restoration and lane safety

- Every mutant ran in its own clone of the pristine green fixture, so the fixture was never
  mutated. After all 12 cases the green fixture tree manifest sha256 is
  `c77d23eedec1d83cac623709541ed017dbca077a48a5bf6fe7bd827af1685ce6`, the same value as before
  the run, and `git status --porcelain` in it is empty.
- The lane was read only: `git clone` into the seat, then read-only `git log`, `git show`,
  `git ls-tree` in the lane. Lane `HEAD` is still `a4f674b343d8564e21f7eb8984630a95089c82d6`.
  No commit, add, checkout or reset was run in the lane, and no `jj` command was run.

## Artefacts (all under `/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Time/`)

- `c2d24d093a571773aee77fdb18366249205890d22b2be60378cab266abada824`  mutate.py (driver)
- `d2a7d8dd666659f29479632240ccc30a2cc94cce5f079232ebca50720516e071`  results.json
- `00dfbfe2f46b561fbcad6308705c532bb060c5904eed65e130a14d6f6f904965`  run.log (raw stdout)
- `74f6d191e70f667a438b2265093500b64dce1b83a741bbb40ae40f34d2cc7768`  manifest.txt (sha256 of
  each file and of each fixture tree) and `fix/` with the green fixture and the 12 mutant clones.

Conclusion labels: every row of the table is an observation (an executed command with the quoted
output). The statement that no committed byte can expose classes 1 and 2 is an inference from the
observed probes m7 and m5/m6/m9 plus the read code and the read envelope; the one untested item
is marked as such above.
