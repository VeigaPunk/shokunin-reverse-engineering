# R39CL4FreezeRule — which freeze-drift verdict blocks a score (R38-CL4)

**Verdict: DONE — routed defect confirmed; rule text, counter embedding, and round-38 test verdicts delivered below.**

Routed defect R38-CL4 (`corpus/lessons/round-38-verifier-spotcheck.md` §5): `freeze-drift.py --freeze e059ca93 --rev 7a1ac7fe` is red (exit 1, three drift commits) while `ships_freeze_bytes` is true — correct history disclosure, but no round-39 rule says which verdict blocks a score. Confirmed by direct measurement this seat (receipts in `.ufo/waves/round-39/w1/artifacts/R39CL4FreezeRule/`, sha256s in `sha256sums.txt` there):

- At rev `7a1ac7fe`: `"drift"` = 3 commits (`79f69347`, `f1010f67`, `7a1ac7fe` itself restoring the bytes), `"net_changed": []`, `"ships_freeze_bytes": true`, **exit 1**.
- So the tool's redness is invisible to any consumer that reads only `ships_freeze_bytes` — the exact loophole M38-1 exploited (amend after scoring, restore later). Nothing in QUALITY 79/80 (`corpus/lessons/round-38.md:147`: 79 = first-freeze rule + freeze-drift.py, 80 = controls inside the freeze) states that a drift verdict blocks.

Prior art the rule re-unifies: `tools/round-31/freeze-integrity.py` (M31-2) already required the conjunction per pinned path — `ok = got == digest and not touched` (tools/round-31/freeze-integrity.py:50): history drift blocks **and** digest equality is required. Round-38 `freeze-drift.py` weakened this to disclosure (exit 1 informational + informational `ships_freeze_bytes`). The round-39 rule restores the round-31 semantics as a blocking gate, with the closure's verdict vocabulary.

## 1. Proposed rule text for `plans/round-39-claims.md`

Insert as a top-level section, referenced from both predicates (L1 integrates; paths re-checked against the final draft at freeze time):

```markdown
## Freeze-integrity rule (P39-FR — binding for R39-C1 and R39-C2)

The frozen rule for a claim is the bytes of its freeze commit `FREEZE` (QUALITY 79). A score
at measured revision `REV` is admissible only if the freeze-integrity check over the claim's
frozen path set returns verdict `clean`:

- `clean` — no commit in `FREEZE..REV` touches any frozen path, and every frozen path present
  at `FREEZE` has identical bytes at `REV`. Only `clean` admits a score.
- `frozen_path_changed` — some commit in `FREEZE..REV` touched a frozen path, or a frozen
  path's bytes at `REV` differ from `FREEZE` (or are absent). This blocks the score even when
  the final bytes equal the freeze bytes: a restore after drift does not un-block, because the
  drift commits remain evidence that the frozen rule was editable after the freeze.
  `ships_freeze_bytes` alone is never sufficient.
- `unevaluable` — the check cannot run (unknown revision, `FREEZE` not an ancestor of `REV`,
  or git failure). No score is admissible from an unevaluable check; fix the invocation.

Embedding: each round-39 counter runs this check itself, before any scoring, over its own
frozen path set (enumerated here; never a default inherited from another round), with
`--freeze` and `--rev` named explicitly (full hashes in the receipt). On
`frozen_path_changed` or `unevaluable` the counter exits **2** with
`freeze_integrity.verdict` = `frozen_path_changed` / `unevaluable`, records the drift commit
list, emits no per-carrier or per-envelope score fields, and never reports `met_target` true.
Exit 0/1 continue to mean met-target / target-not-met, only ever on `clean`. The verdict is
recomputed from git at whatever `REV` the receipt names; a later commit does not cure an
earlier block.

Frozen path sets (frozen at `FREEZE`):
- shared core: `plans/round-39-claims.md`, `tools/round-39/c1-counter.py`,
  `tools/round-39/c2-counter.py`, `tools/round-39/sqfs-triage.py`,
  `tools/round-39/heldout-gen.py`, `.ufo/waves/round-39/c1/carriers.json`;
- C1 adds: `corpus/evidence/round-39/c1/K*/oracle.tsv`,
  `corpus/evidence/round-39/c1/K*/symlinks.tsv`,
  `corpus/evidence/round-37/c1/K*/oracle.tsv`, `.ufo/waves/round-38/c1/carriers.json`;
- C2 adds: `SKILL.md` (whole file — the craft-section triage table cannot be path-isolated,
  so any post-freeze `SKILL.md` commit blocks C2 scoring; finish SKILL edits before the
  freeze).
Round-38 drift history (freeze `e059ca93`, revs `077e212b` and `7a1ac7fe`: both classify
`frozen_path_changed`) is the pinned red fixture at
`.ufo/waves/round-39/c1/freeze-drift-r38-red.json`.

Remedy: none after claim data exists. Before any claim data (and before C2 held-out
generation), the L1 may take a new freeze commit; the new freeze re-freezes the controls
(QUALITY 80), requires the controls re-scored under it, and resets the C2 held-out seed (the
new freeze hash). A blocking verdict after claim data exists is an honest stop for the claim.
```

Predicate edits in the same file:

- P39-C1, final clause: replace "and no frozen C1 path changed after the freeze" with
  "and the freeze-integrity check (P39-FR) over the frozen C1 path set returns `clean` at the measured revision".
- P39-C2: after "and the triage table bytes at the measured revision equal those at the freeze" add
  ", and the freeze-integrity check (P39-FR) over the frozen C2 path set returns `clean` at the measured revision".

`clean` implies `ships_freeze_bytes` true; the converse is false (proven at `7a1ac7fe`), so P39-FR strictly subsumes both draft net-bytes bindings.

## 2. Counter embedding (round-39 c1-counter.py / c2-counter.py)

Algorithm (git objects only, no worktree reads):

1. Resolve `FREEZE` and `REV` to full hashes (`cat-file -e HASH^{commit}`); failure → `unevaluable`.
2. `merge-base --is-ancestor FREEZE REV`; failure → `unevaluable` ("freeze is not an ancestor of rev").
3. History half: `git log --format=%H%x09%cI%x09%s --name-only --no-renames FREEZE..REV -- ':(glob)<each frozen path>'`. Any commit line → `frozen_path_changed`, reason `history_drift`, with the parsed commit list.
4. Digest half: for each non-glob frozen path, `git show REV:<path>` sha256 vs `git show FREEZE:<path>` sha256; mismatch/absent → `frozen_path_changed`, reason `digest_mismatch`.
5. Verdict `clean` → proceed to scoring; receipt records `freeze_integrity` either way.

Receipt shape (exit 2 = blocked; discriminated by `verdict`, matching the round-38 counter's existing convention where 2 already meant Unevaluable):

```json
{"tool": "round-39-c1-counter", "freeze": "<full>", "rev": "<full>",
 "freeze_integrity": {"verdict": "clean|frozen_path_changed|unevaluable",
                      "reasons": ["history_drift"| "digest_mismatch"| "<unevaluable reason>"],
                      "drift": [{"commit": "...", "committed": "...", "subject": "...", "paths": [...]}],
                      "ships_freeze_bytes": true},
 "blocked": "frozen_path_changed", "met_target": false}
```

On a blocked verdict: exit 2, no per-carrier/per-envelope fields, `met_target` hard-false. On `clean`: exit 0/1 exactly as the round-38 counters did.

Selftest (mandatory; closes the R38-CL2 unregistered-gate class for the new gate) — five cases, fixtures built in tmpdirs with the lane's fixture-repo discipline, plus one pinned lane case:

| case | fixture | expected |
|---|---|---|
| `clean` | freeze → unrelated-file commit | verdict clean, scoring proceeds |
| `drift-unrestored` | freeze → amend frozen file | exit 2 `frozen_path_changed`, ships false |
| `drift-restored` | freeze → amend → restore bytes | exit 2 `frozen_path_changed`, ships **true** (the decisive case) |
| `unevaluable` | rev not descending from freeze | exit 2 `unevaluable` |
| `r38-history-red` | lane repo, freeze `e059ca93`, rev `7a1ac7fe` | exit 2 `frozen_path_changed` (pinned receipt at `.ufo/waves/round-39/c1/freeze-drift-r38-red.json`) |

Mutation targets a wave-2 seat should kill: drop the merge-base check; invert the drift-list emptiness test; check net bytes only (survives the restore case — must not); fall back to the round-38 DEFAULT path set when the claim set is empty; emit `met_target` computed anyway on a blocked verdict. The embedded gate gets a SKILL.md round-39 registry row (entry command, verdict map 0/1/2, selftest command, pinned-value path) at the freeze.

## 3. Test on round-38 history — verdicts the rule gives

All rows measured this seat with `python3 tools/round-38/freeze-drift.py --root <LANE> --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --rev <REV>` (exit codes re-recorded without pipes; JSON receipts in the artifacts dir):

| freeze | rev | observed tool verdict / drift commits | ships_freeze_bytes | exit | **P39-FR verdict** |
|---|---|---|---|---|---|
| e059ca93 | 077e212b (attempt-1 tip) | drift: `79f69347` (claims+c1-counter), `f1010f67` (c1-counter) | false | 1 | **frozen_path_changed — blocks** |
| e059ca93 | 3b960fe5 (attempt-2 claim data) | drift: `79f69347`, `f1010f67` | false | 1 | **frozen_path_changed — blocks** |
| e059ca93 | 7a1ac7fe (attempt-2 final; bytes restored) | drift: `79f69347`, `f1010f67`, `7a1ac7fe` (restore) | **true** | 1 | **frozen_path_changed — blocks; `ships_freeze_bytes` does not rescue** |
| e059ca93 | e059ca93 (freeze itself) | clean, 0 drift | true | 0 | clean — scoring admissible |
| e059ca93 | 676328449 (pre-freeze) | unevaluable: "freeze is not an ancestor of rev" | n/a | 2 | unevaluable — no score |

Answer to the routed question, stated plainly: under P39-FR the round-38 rule test gives **`frozen_path_changed` (score blocked)** for every measured revision after the freeze — including the final receipts at `7a1ac7fe`, whose restored bytes would have passed a `ships_freeze_bytes`-only rule. The only admissible scoring revision under freeze `e059ca93` was `e059ca93` itself. Retroactively this voids round-38's final receipts as *scores* (the honest-stop verdict stands; the v1-at-final met_target becomes inadmissible by procedure, not merely disclosed). That is the intended strictness: it forecloses amend-then-restore, which is precisely the M38-1 shape. For round-39 the rule binds prospectively from the round-39 freeze.

Fixture corroboration (scratch, lane fixture discipline; receipt `fx-restore.json`): synthesized freeze → drift A → drift B → restore reproduces the real shape — exit 1, 3 drift commits, `ships_freeze_bytes: true`; clean control (freeze → unrelated commit) exit 0. Independent `git diff --name-only` over the frozen paths at `e059ca93..7a1ac7fe` is empty, confirming the restore.

## 4. Residual risks and limits

- Path granularity for C2 is deliberately coarse (whole `SKILL.md` frozen post-freeze). Finer region bindings add parser surface to a frozen tool; not recommended for round-39.
- Round-38 `freeze-drift.py` parses `--format=%H%x09%cI%x09%s --name-only` textually; a filename containing a tab would confuse it (pathological, unobserved in lane history). The round-39 embedding should use NUL/`%x00`-separated output or `-z`.
- Merge commits in `FREEZE..REV` were never exercised (round-38 history and fixtures are linear); `git log --name-only` traversal over merges is standard but untested here [INFERENCE].
- Receipts must record resolved full hashes, not argv symbols (`HEAD` worked in the fixture but is not a stable receipt value).
- The rule binds `FREEZE..REV` only; commits after `REV` are out of scope by design — the score is bound to `REV`, and a later restore never retro-validates.
- `freeze-drift.py` itself remains an unregistered round-38 probe (R38-CL2, prior-round frozen bytes — out of my scope to edit); the round-39 embedded gate must carry its own registry row.
- Draft drift: K5/K6 paths and tool names above follow the DRAFT claims file; L1 re-verifies the enumeration against the final draft at the freeze.

Tools installed: none (no new tooling needed; pacman untouched).
