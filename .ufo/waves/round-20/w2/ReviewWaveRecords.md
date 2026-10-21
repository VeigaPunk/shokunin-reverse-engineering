FALSIFIED — W1 per-seat terminal/cause accounting at S is not QUALITY #22-complete: 98/100 reports reproduce, but the two missing seats have no retained cause records.

Axes: calibration (seat/report accounting), coverage (cited-seat reports), depth (per-seat outcome provenance). All revision-scoped observations below use committed Git objects at S=`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`, not the working tree.

## Recount

[Observation] `git -C "$R" show "$S:.ufo/waves/round-20/wave1-registry.json" | jq '{members:(.members|length),spawn:([.members[]|select(.kind == "spawn")]|length),agentIds:([.members[]|select((.agentId|type)=="string")]|length)}'` (EXIT 0) returned 100 members, 100 spawn, 100 agent IDs. The two reportless seats are assigned IDs at `wave1-registry.json:800-813`.

[Observation] `git -C "$R" show "$S:.ufo/waves/round-20/w1/swarm-registry.json" | jq '{members:(.members|length),assigned:([.members[]|select(.agentId != null)]|length),nullAgentIds:([.members[]|select(.agentId == null)]|length),spawn:([.members[]|select(.kind == "spawn")]|length)}'` (EXIT 0) returned `members=100, assigned=0, nullAgentIds=100, spawn=100`; the source rows show null agent IDs for both missing seats (`w1/swarm-registry.json:800-814`). Its creation time (`:3-6`) precedes the final registry and is the unassigned pre-record copy, not a contradicting final roster.

[Observation] `git -C "$R" ls-tree -r --name-only "$S" -- .ufo/waves/round-20/w1 | jq -R 'select(test("^\\.ufo/waves/round-20/w1/[^/]+\\.md$"))' | wc -l` (EXIT 0) returned 98. A Git-object set difference (EXIT 0; extras EXIT 0) returned only `ConnJjSelftests` and `ConnSiblingHarmony` as missing, no extra report basenames; an independent `git cat-file -s` check found all 98 report blobs nonempty (EXIT 0). Both absent report paths and both W1 registry rows were checked; the rows carry IDs `KaidokuR20.ConnSiblingHarmony-2` and `KaidokuR20.ConnJjSelftests-2`.

[Observation] `wave1-dispatch-attempts.json:1-12` records dispatch attempt one refused 100 and attempt two refused 0; `wave1-result-attempt1.txt:1` reports the background-job-limit refusal, while `wave1-result-attempt2.txt:1-102` records that 100 agents were spawned. The first refusal therefore does not explain the two missing reports after the retry. Separately, `SCORECARD.md:2575-2577` describes the top-level round attempt-1 watchdog and attempt-2 recovery; that is not a per-seat W1 outcome record.

## Missing causes — actionable finding

[Observation] `corpus/QUALITY.md:32` requires every reportless seat to have its retained terminal error line plus transcript/result pointer, or to be marked `cause unknown` with retrieval attempts; it also requires a cutoff and separation of terminal failures from seats still pending. At S, `git -C "$R" cat-file -e "$S:.ufo/waves/round-20/wave1-outcomes.json"` and checks for `.ufo/waves/round-20/evidence/wave-outcomes/w1-causes.json` and `w1-terminal.json` each exit 128 (path absent). The W1 report `w1/ReviewDeadSeatRecording.md:13-18` recommends those records and `:37` says no R20 outcome command was run in that advisory seat. The retained dispatch outputs show launch/refusal only, not per-seat terminal errors or transcript/result pointers.

[Observation / limitation] The assignment states the two transcripts end `aborted`; I could not independently retrieve them: `history://KaidokuR20.ConnSiblingHarmony-2` and `history://KaidokuR20.ConnJjSelftests-2` each returned `Unknown agent`. S contains no retained transcript pointer, terminal error line, cutoff snapshot, or `cause unknown` entry for either seat. [Inference] Their final terminal causes/status at the required observation cutoff are not reproducible from S, so the per-seat status claim fails QUALITY #22 even though the reported count and missing-seat identities are reproducible.

## Cited-seat coverage

[Observation] The exact member-key scan over `corpus/lessons/round-20.md`, the Round-20 section of `SCORECARD.md`, and the five round-20 knowledge entries returned 36 distinct cited W1 seat names and zero cited names without a nonempty W1 report (EXIT 0). The Round-20 scorecard section (`SCORECARD.md:2569-2598`) cites no W1 seat name. The complete cited set is: `CustodySelftestFix`, `HeadRevNested`, `WasmInspectLeg`, `WasmCompareLeg`, `WasmRefusalLeg`, `RizinLeg`, `RizinPeLeg`, `HarmonyLeg`, `ScoutLaneScratchWriters`, `ScoutTimestampOracle`, `ScoutCarrierExecPaths`, `ScoutSandboxPrimitives`, `ScoutWasmSchema`, `ScoutRizinSchema`, `ScoutWasmCarriers`, `ScoutGo1246Carriers`, `ScoutGhidraVariadic`, `ScoutGo1273Exposure`, `ReviewClaimsC2`, `ReviewCensusGate`, `RevWasmVerb`, `ConnSiblingRizin`, `ConnSandboxPatterns`, `SourceWabtRelease`, `SourceRizinDocs`, `SourceHarmonyDocs`, `SourceWasmSpec`, `SourceGo1246`, `SourceObjdumpDocs`, `CriticC2`, `CriticC3`, `CriticGuardSufficiency`, `CriticCensusRekey`, `SentinelRevexec`, `SimplifyC1Tools`, `SimplifyC3Pipeline`. Lesson citations are at `round-20.md:32-37,52-53,100-107,113-120`; knowledge references include Go `:1,15`, Rizin `:2,41-43`, and WASM `:2,30,34`. Neither reportless seat is cited.

## Command evidence (read-only; all inputs from Git objects at S)

```sh
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9
git -C "$R" show "$S:.ufo/waves/round-20/wave1-registry.json" | jq '{members:(.members|length),spawn:([.members[]|select(.kind == "spawn")]|length),agentIds:([.members[]|select((.agentId|type)=="string")]|length)}'
# EXIT 0; members=100, spawn=100, agentIds=100
git -C "$R" show "$S:.ufo/waves/round-20/w1/swarm-registry.json" | jq '{members:(.members|length),assigned:([.members[]|select(.agentId != null)]|length),nullAgentIds:([.members[]|select(.agentId == null)]|length),spawn:([.members[]|select(.kind == "spawn")]|length)}'
# EXIT 0; members=100, assigned=0, nullAgentIds=100, spawn=100
git -C "$R" ls-tree -r --name-only "$S" -- .ufo/waves/round-20/w1 | jq -R 'select(test("^\\.ufo/waves/round-20/w1/[^/]+\\.md$"))' | wc -l
# EXIT 0; 98
comm -23 <(git -C "$R" show "$S:.ufo/waves/round-20/wave1-registry.json" | jq -r '.members|keys[]') <(git -C "$R" ls-tree -r --name-only "$S" -- .ufo/waves/round-20/w1 | jq -Rr 'select(test("^\\.ufo/waves/round-20/w1/[^/]+\\.md$"))|sub(".*/";"")|sub("\\.md$";"")')
# EXIT 0; ConnJjSelftests, ConnSiblingHarmony
comm -13 <(git -C "$R" show "$S:.ufo/waves/round-20/wave1-registry.json" | jq -r '.members|keys[]') <(git -C "$R" ls-tree -r --name-only "$S" -- .ufo/waves/round-20/w1 | jq -Rr 'select(test("^\\.ufo/waves/round-20/w1/[^/]+\\.md$"))|sub(".*/";"")|sub("\\.md$";"")')
# EXIT 0; no extra reports
git -C "$R" show "$S:.ufo/waves/round-20/wave1-dispatch-attempts.json"
# EXIT 0; attempts record refused=100 then refused=0
git -C "$R" show "$S:.ufo/waves/round-20/wave1-result-attempt1.txt"
# EXIT 0; line 1 reports background-job-limit refusal
git -C "$R" show "$S:.ufo/waves/round-20/wave1-result-attempt2.txt"
# EXIT 0; line 1 reports 100 spawned
git -C "$R" cat-file -e "$S:.ufo/waves/round-20/wave1-outcomes.json"; printf 'EXIT:%s\n' "$?"
# EXIT 128; absent
git -C "$R" cat-file -e "$S:.ufo/waves/round-20/evidence/wave-outcomes/w1-causes.json"; printf 'EXIT:%s\n' "$?"
# EXIT 128; absent
git -C "$R" cat-file -e "$S:.ufo/waves/round-20/evidence/wave-outcomes/w1-terminal.json"; printf 'EXIT:%s\n' "$?"
# EXIT 128; absent
node -e 'const c=require("node:child_process"),p="/home/vgpnk/Projects/shokunin/kaidoku-shokunin",r="5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9",d=".ufo/waves/round-20/w1";const a=c.execFileSync("git",["-C",p,"ls-tree","-r","--name-only",r,"--",d],{encoding:"utf8"}).trim().split("\n").filter(x=>x.startsWith(d+"/")&&!x.slice(d.length+1).includes("/")&&x.endsWith(".md"));const ok=a.every(x=>Number(c.execFileSync("git",["-C",p,"cat-file","-s",r+":"+x],{encoding:"utf8"}))>0);console.log(JSON.stringify({reports:a.length,allNonempty:ok}));'
# EXIT 0; {"reports":98,"allNonempty":true}
```

Residual risk: without retained per-seat transcript/result pointers, the two `aborted` tails cannot establish the terminal error or cutoff state.