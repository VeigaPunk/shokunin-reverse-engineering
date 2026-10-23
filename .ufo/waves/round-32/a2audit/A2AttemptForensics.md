# Round 32 W1 attempt-1 dispatch/dead-seat forensics

**Report UTC:** 2026-10-23T06:53:22Z (captured immediately before writing).  
**Axes:** dispatch provenance; seat-outcome certainty; freeze-ledger conformance.

## Finding

The W1 dispatch plan contains 36 spawn tasks and no resumes, but does not establish 36 actual starts. The registry was created and last updated at 06:13:05.241Z before the recorded 06:13:39Z dispatch, and all 36 `agentId` fields remain `null`. The refusal log corrects the initial apparent starts as parser errors: the initial full request and the three 12-seat chunks were refused for the background-job limit. A later first chunk did start 12 seats at 06:17:19Z; the only exact accepted runtime ID preserved in the refusal-log response head is `KaidokuR32-10.CtlC1DoNothing-6`. The next chunk was refused repeatedly. The W1 report directory contains only `swarm-registry.json`; there are no seat reports to use.

The 06:19:06Z `omp SIGSEGV` watchdog death is supplied by the assignment context, not recorded in the inspected W1 files. It is attributable to the started attempt-1 batch at group level; individual attribution beyond the one returned ID is not independently recoverable from the registry or truncated response heads. I did not retry or replace W1 work. Scratch content is untrusted: I inventoried names and SHA-256 hashes only and did not use scratch contents as claim evidence.

## Freeze and dispatch chronology

| UTC | Observation and provenance |
|---|---|
| 06:03Z | R32-C1 freeze `9a73680a` is recorded in the W1 dispatch context and `corpus/claim-freezes.tsv:20`. |
| 06:09:57Z / 06:10Z | `claims-v3.json:supersedes.at` is `2026-10-23T06:09:57Z`; the W1 dispatch context and v2 ledger record C2 v3 freeze `f382e3b7` at 06:10Z. The file states that v1/v2 were superseded before dispatch or data; C1 remains frozen in `claims.json`. |
| 06:13:05.241Z | W1 registry `createdAt` and `updatedAt`; all member IDs are null. |
| 06:13:39Z | `w1-dispatched-at.txt:1`. This follows both operative freeze times. |
| 06:14:20Z | `w1-refusals.txt:1`: full 36-seat call refused, `Background job limit reached (100)`. |
| 06:14:28Z / 06:16Z | Lines 2–4 initially say three chunks started; line 5 explicitly corrects them: all were refused because retry IDs had `-2` suffixes the refusal parser missed, and no W1 seat had started by then. |
| 06:15:18Z–06:16:38Z | Lines 6–8: first 12-seat chunk retries 1–3 each report `started 0 refused 12`, naming `CtlC1DoNothing-3`, `-4`, and `-5` in the response heads. |
| 06:17:19Z | Line 9: retry 4 reports `started 12 refused 0`; the response head records `KaidokuR32-10.CtlC1DoNothing-6`. The remaining returned IDs are truncated. |
| 06:17:20Z, 06:18:00Z, 06:18:40Z | Lines 10–12: next 12-seat chunk retries 5–7 each report `started 0 refused 12`; response heads name `MutOracle-3`, `-4`, `-5` and the background-job-limit refusal. |
| 06:19:06Z | Watchdog death time and `omp SIGSEGV` cause are supplied in the assignment context. No local W1 artifact inspected here records that event. |

`w1-dispatch.json` says `spawn: 36`, `resume: 0`, `total: 36`; this is planned count, not a start receipt. Its roster/task array supplies the ordered seat names below. The refusal-log response starts with `CtlC1DoNothing` for the accepted chunk and with `MutOracle` for the refused next chunk; assigning the rest of each 12-seat group by task-array order is an inference, not a recorded per-seat `agentId` map.

## Roster and cause certainty

| W1 roster entries | Outcome / cause | Certainty and ID limits |
|---|---|---|
| `CtlC1DoNothing` | In the accepted 12-seat response; the supplied watchdog event says started attempt-1 seats died by `omp SIGSEGV` at 06:19:06Z. | Exact returned ID `KaidokuR32-10.CtlC1DoNothing-6`; death event is assignment-supplied, not locally logged. |
| `CtlC1JunkRow`, `CtlC1AllFalse`, `CtlC1NoReader`, `CtlC1Placement`, `CtlC1NonHybrid`, `CtlC1EcCount`, `CtlC1IdRotated`, `CtlC1WriteMode`, `CtlC2Junk`, `CtlC2Shortcut`, `MutC1Counter` | First accepted 12-seat group; under the supplied watchdog event, the started group died by `omp SIGSEGV`. | Membership is inferred from the ordered payload and 12-seat chunk boundary; their exact runtime IDs and individual death records are absent. |
| `MutOracle`, `MutC2Counter`, `ExecPefileWitness`, `ExecCitedRuns`, `ExecFleetGuard`, `RevCarrierBuild`, `RevPredicateC1`, `RevPredicateC2`, `RevFreezeChain`, `CriticAxisFitC1`, `CriticAxisFitC2`, `CriticSeparability` | Next 12-seat chunk refused: 0 started/12 refused at each logged retry; no death for a process that did not start is evidenced. Cause recorded as background-job limit. | `MutOracle-3` is the first refused ID in the response head; the other IDs are not preserved. Group membership follows the ordered payload and chunk boundary. |
| `RevengerInspectPE`, `ScoutPublishedArm64x`, `ConnSiblings`, `SentinelContainment`, `ScribeSrcS099`, `ScribeSrcS098`, `ScribeSrcS100`, `ScribeSrcS101`, `ScribeD1Row56`, `ScribeD3Skill1038`, `ScribeR31Lesson`, `ScribeCapRows` | The correction records that the initial third chunk was refused. No later start for this chunk appears in `w1-refusals.txt`; no death cause can be assigned from the inspected records. | Later disposition and per-seat IDs are unknown. Do not label these seats as dead based solely on the watchdog signal for started seats. |

The roster has 36 planned members; only the first 12-seat group has an observed successful start count. No post-watchdog W1 retry or replacement is recorded in these artifacts, and none was initiated by this seat. Earlier scheduler retries above are historical launch attempts, not evidence of a replacement after the crash.

## Round-32 freeze-ledger conformance needs

Read `tools/round-29/prefile-check.sh` (lines 2–14, 20–45); **no prefile or freeze gate was run for this report**. Before filing the integrated round report, after all seats settle and the last lane commit lands:

1. At the final lane HEAD, `GIT_OPTIONAL_LOCKS=0 git -C <lane> status --porcelain` must be empty. The prefile script also resolves that HEAD.
2. Run the round-24 gate at that HEAD with `--disclosures corpus/claim-freezes.tsv`; prefile requires exit 0.
3. Because `corpus/claim-freezes-v2.tsv` exists, run the round-29 gate at the same HEAD with `--disclosures corpus/claim-freezes-v2.tsv`; prefile requires exit 0.
4. Record the live session/job listing separately: the script explicitly cannot tell whether dispatched seats are still running.
5. Preserve the actual C1 freeze (`9a73680a`) and the operative C2 v3 freeze (`f382e3b7`), including the superseded C2 v1/v2 records (`9a73680a`, `9d54070b`). Do not mistake the v1 ledger's `round-32 CLEAN` row for C2 v3 admission: its pointer says it concerns C1 and superseded C2 v1 instrument custody.
6. Reconcile the v2 ledger's `round-32/claims-v3.json` row (`FLAGGED / INSTRUMENT_UNPINNED`) against the round-29 gate's actual output and exact disclosure schema. The current row explains that the historical evidence-anchor paths are parsed as unpinned even though they are evidence pointers, not C2-executed tools. The gate's `--require-clean` option defaults to empty and is not passed by prefile; therefore this flag alone does not establish a prefile failure, but the disclosure must exactly match the gate output, with no missing, mismatched, or stray rows. This is a source-based requirement, not a verified pass.

## Commands, hashes, and provenance

Read-only source paths used: `.ufo/waves/round-32/{w1-dispatch.json,w1-payload.json,w1-spec.json,w1-dispatch.err,w1-dispatched-at.txt,w1-refusals.txt,w1/swarm-registry.json,claims.json,claims-v2.json,claims-v3.json}`, both freeze ledgers, both freeze-gate scripts, and `tools/round-29/prefile-check.sh`. Their relevant excerpts are cited above. `w1-dispatch.err` is empty. The registry output showed `agentId: null` for all 36 members. No Git/JJ command, test, build, REA invocation, or external-source fetch was performed. No private sandbox clone was created; revisions below are those recorded in the W1/claim/ledger sources, not independently revalidated from Git history.

Source-file SHA-256 values (captured by `sha256sum`; tool output did not separately expose numeric shell exit codes):

| File | SHA-256 |
|---|---|
| `.ufo/waves/round-32/w1-dispatch.json` | `70ad2ee7b79e239c6801c94a7158764aaf8abb3edae333b344459b97acdfd469` |
| `.ufo/waves/round-32/w1-payload.json` | `16ae8dfd1e01176ea8d5d14f0e688c7ab57ed4fe82b2376be29d85183353a0f8` |
| `.ufo/waves/round-32/w1-spec.json` | `1c623c75dcc6c37640ff85baa7d765e44be2784a6ee84131ac9bd50b878007f1` |
| `.ufo/waves/round-32/w1-dispatch.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/waves/round-32/w1-dispatched-at.txt` | `01d502a844cffefc59b39fed28be952249e78dc373c345880813007f3c393252` |
| `.ufo/waves/round-32/w1-refusals.txt` | `320d4ce5ecccfc4b417bea18de16b802460fe33a4e201ef8d6d21a977d890d98` |
| `.ufo/waves/round-32/w1/swarm-registry.json` | `99b2da215c59fce5d7e61effe8ea1ca2d7eeaacd800cac4778beb804e345761b` |
| `.ufo/waves/round-32/claims.json` | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |
| `.ufo/waves/round-32/claims-v2.json` | `805a05146515580d644074792db3d84a241307e65fbd9c54b916b762d82e5609` |
| `.ufo/waves/round-32/claims-v3.json` | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| `corpus/claim-freezes.tsv` | `b02cc6858a4f29612330bf455ef9d6e3770d43f13343693ea1beb520ede74ec9` |
| `corpus/claim-freezes-v2.tsv` | `cc19f7c84dc9e553ac256e2b1317801675f2a60fc6bf1169acb2bc5689c731b3` |
| `tools/round-29/prefile-check.sh` | `5c3586b277e16b7c43ae32a4160643442f6b9612b7e2d74cd6e76c12c688cdd9` |
| `tools/round-29/freeze-gate.py` | `25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2` |
| `.ufo/waves/round-24/tools/freeze-gate.py` | `8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329` |

Recorded source revisions: base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`; C1 freeze `9a73680a`; C2 v2 freeze `9d54070b`; C2 v3 freeze and recorded lane tip `f382e3b7978e6091a19ca93277c15a75c0016b43`.

Scratch inventory commands and outputs:

- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated /fast/scratch/hyaku/kaidoku-r32/seats/w1/MutC1Counter -type f ! -path '*/.git/*' -printf '%p\n' | wc -l` → `20336`.
- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated/clone/.git -type f -printf '%p\n' | wc -l` → `11094`.
- Full per-file hash stdout is retained at `artifact://779` (20,336 regular worktree-file hashes, `.git` excluded) and `artifact://1165` (11,094 regular `.git` metadata-file hashes). The commands and counts are also in the index file below. The regular-file hash commands completed at 06:48:03Z–06:48:05Z and 06:49:47Z–06:49:48Z respectively.
- Symlink inventory at 06:51:05Z found two broken links in `CtlC1DoNothing/clone/.ufo/waves/arc3-loop1-round4/claims/c3/EX-25/fixtures/scratch/`: `alias-1.conf` and `alias-2.conf`, both targeting `/var/tmp/ex25-r4/fixtures/scratch/aliased-real.conf`. `sha256sum` of each target failed with `No such file or directory`; SHA-256 of each link-target string (not target bytes) is `9ea4b025c81b582b8791685c97452f34d82bf996289eccbc205d9918355d9d91`.
- Scratch index: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2AttemptForensics/w1-discard-sha256-index.txt`, SHA-256 `e4a25c09d24f88656de9ead24fe3444a206c50be512fe88890a63ad356edf711` (hash command output at 06:52:59Z). It records the complete inventory artifact paths, counts, broken links, and limits. No scratch file body was read or used to infer a seat result.

**Touched surfaces:** this report only in the lane; one inventory index in this seat's assigned scratch directory. No lane claim, ledger, code, report, or Git/JJ state otherwise changed.  
**Out of scope / not verified:** no prefile or freeze gate execution, no process-list check, no independent Git-history verification, no scratch-content review, and no claim/predicate judgment. The watchdog event remains assignment-supplied.

Report: `.ufo/waves/round-32/a2audit/A2AttemptForensics.md`
