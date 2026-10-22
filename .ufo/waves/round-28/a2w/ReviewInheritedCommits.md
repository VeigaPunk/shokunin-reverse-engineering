# ReviewInheritedCommits — attempt-1 inherited commits, round 28 attempt 2

Seat: KaidokuR28a2.ReviewInheritedCommits. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Reviewed: 87d3dfb6, 86fa8526, ca4069a4, cb8d495e, a2673116 over base 935c3660.
Method: read-only git (show -s --format=fuller, --stat, diff-tree, log, archive) plus jq on
extracted blobs. No lane writes except this report. All commands run 18:28:58Z-18:44:22Z UTC,
2026-10-22; every command exited 0 unless noted. HEAD at review time: 071270b5… (tip has moved
past a2673116 during attempt 2; observation).

## Chain
`git log 935c3660..a2673116` lists exactly the five target commits, linear, newest first:
a2673116 -> cb8d495e -> ca4069a4 -> 86fa8526 -> 87d3dfb6 -> 935c3660. Observation.

## Per-commit verdict (git show --stat --format=fuller)
Author and Committer of all five: `kaidoku-shokunin <kaidoku@shokunin.local>`. Single parent each.

- 87d3dfb6 (AuthorDate 13:14:11Z, CommitDate 14:17:16Z): "freeze R28-C1". 9 files, +1188:
  claims.json, c1-heldout-naming.py (623), collect-c1.py, select-heldout.py, carriers.tsv (62),
  heldout.tsv (188), 3 before receipts. Verdict: HOLDS (observation).
- 86fa8526 (AuthorDate 14:17:16Z, CommitDate 14:21:55Z): "freeze R28-C2". 7 files, +813:
  claims-c2.json, c2-filtered-flag.py (343), collect-c2.py, canonical-signatures.json,
  selectors.tsv (231), 2 before receipts. Verdict: HOLDS.
- ca4069a4 (AuthorDate 14:21:55Z, CommitDate 14:22:32Z): "C1 REA runs on 61 carriers". 62 files:
  envelopes h01-h61 + runs.tsv; message records h09 refusal. Verdict: HOLDS.
- cb8d495e (AuthorDate 14:22:32Z, CommitDate 14:25:49Z): "C1 lookups and tally". 376 files:
  187 4byte + 187 openchain responses + manifest.json (2620) + tally.json (2683). Verdict: HOLDS.
- a2673116 (AuthorDate 14:25:49Z, CommitDate 14:45:05Z): "C2 openchain fetch + inherited w1".
  234 files: 230 openchain responses + c2 manifest (1612) + w1-spec.json, w1-dispatch.json,
  w1/swarm-registry.json. Verdict: HOLDS.

## Later edits to frozen files
`git log --format='%H %ad %an %s' 935c3660..a2673116 -- <path>` per path (18:28:58Z, exit 0):
- .ufo/waves/round-28/claims.json: only 87d3dfb6.
- .ufo/waves/round-28/claims-c2.json: only 86fa8526.
- tools/round-28/c1-heldout-naming.py: only 87d3dfb6.
- tools/round-28/c2-filtered-flag.py: only 86fa8526.
Supplementary check `git log a2673116..HEAD -- <same four paths>`: empty (18:31:27Z, exit 0).
Verdict: no commit after either freeze edits any frozen file, up to current tip. Observation.

## W1 spec / dispatch / registry in a2673116 (agentId check)
Files extracted via `git archive a2673116 <paths>` into the seat scratch dir; jq queries below.
- w1-spec.json: keys context/items/maxLanes/reportDir/wave; items = 33 seats {name, role,
  prompt}; contains zero agentId fields (plan stage only). `jq '[paths(scalars) as $p |
  select($p[-1]=="agentId")]|length'` -> 0 (exit 0).
- w1-dispatch.json: schema ufo-swarm-wave-dispatch-v1; counts {spawn:33, resume:0, total:33};
  resumeSends []; compaction.applied false; taskCall.tasks = 33; embedded registry.members each
  {kind:"spawn", agentId:null, role, item:null}. `jq '[..|objects|select(has("agentId"))|
  .agentId]|unique'` -> `[null]`; member count by value -> [{"value": null, "count": 33}].
- w1/swarm-registry.json: schema ufo-swarm-registry-v1; createdAt/updatedAt
  2026-10-22T17:24:26.636Z; members = 33, each {kind:"spawn", agentId:null, role, item:null};
  `jq '[.members[]|.agentId]|group_by(.)|map({value:.[0],count:length})'` -> [{"value":null,
  "count":33}]; member keys unique -> [["agentId","item","kind","role"]].
- Cross-file: spec item names == registry members == dispatch registry members == taskCall
  task names (all four sets equal, jq comparison -> true/true/true).
Verdict: HOLDS — the committed w1 artifacts show no dispatched seat; every agentId is null and
every member kind is spawn. Observation. Runtime dispatch state outside git objects is out of
scope for this seat.

## Findings
None. No defect in the five inherited commits; no later edit to a frozen file.

## Residual risk / verification gaps
- Frozen-file byte equality against the sha256 pins inside claims.json / claims-c2.json was not
  rechecked here (other seats recount); this review covers commit authorship and edit history.
- HEAD already contains attempt-2 commits beyond a2673116; only frozen-path history was checked
  through HEAD, other post-a2673116 content is out of scope.

## Tooling
No installs; git and jq already present.

## Artifacts (under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewInheritedCommits/)
sha256:
- b8c3b9353789e4a1b2ef270be9787610c5e129d5d09d5c63d98af32246439e6b  git-show-87d3dfb6.txt
- 690eabc82e6ecd784373ab285f5b934a8c6469b858f93b80ccc9b2aa35d5cd2e  git-show-86fa8526.txt
- b6bacff2733bf18c62ca9836204371a3bc37310ec56b1e0d9bee8a2e94ee6b8e  git-show-ca4069a4.txt
- a0c753efd50e53795f46c9a5c07f96a2136e17b97b1f60313ebce1b70885be7c  git-show-cb8d495e.txt
- f74cc51351638357f275cca4ea32e0aa7b3bd8e47d1635fa7eb091eff56bdcf7  git-show-a2673116.txt
- a325c5f3088809e1a96ba883637863502b46f9f16a648e173cf72ca15f1477fc  frozen-paths-log.txt
- 2db325460c1d004d5cd01bd1ac9ce966bdb51ad767aee450fdec5881fb8ca74f  .ufo/waves/round-28/w1-spec.json
- eb3a4d4ef73191c2e49878e80af3ab047a8021f47eb16e25a0be94778ae40ae9  .ufo/waves/round-28/w1-dispatch.json
- 945f78f77ff33a049c84ff2cd3d1b39d55255c9bcf14b396c0c4c760a8cfaaea  .ufo/waves/round-28/w1/swarm-registry.json

Report: .ufo/waves/round-28/a2w/ReviewInheritedCommits.md
