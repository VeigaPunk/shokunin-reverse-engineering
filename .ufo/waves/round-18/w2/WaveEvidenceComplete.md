HOLDS

# WaveEvidenceComplete — round 18 wave 2 (falsify): wave-1 evidence completeness

Seat `KaidokuR18.WaveEvidenceComplete` (scout, leaf, author-side advisory, not an outside review).
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (`git cat-file -t` → `commit`, EXIT=0; "round-18: carrier runs, corpus corrections, knowledge entry, registry and SOURCES (pre-falsify)", 2026-10-20 13:38:07 -0300).

- Lane writes: this file only.
- Installs/updates: none.
- Temporary files: C4 used one `mktemp -d /tmp/wec-XXXXXX` `git archive` export of REV and removed it in the same command. An earlier exploratory dir, `/tmp/wec-eooO6y`, was also removed.
- Labels: `[OBS]` means observed in command output; `[INF]` means inference.

## Verdict

**HOLDS**: all three asked items pass at REV.

| check | result at REV | anchor / command |
|---|---|---|
| dispatch task count | spawn 89, resume 0, total 89; `taskCall.tasks` = 89 entries, 89 unique names | `wave1-dispatch.json:16-20`; tasks `:1017-1461`; C1 |
| reports under `w1/` vs task names | 90 entries = 89 `.md` + `swarm-registry.json`. Missing `[]`, extra `[]`. Every task has exactly one `Report:` trailer, equal to `.ufo/waves/round-18/w1/<name>.md`. Smallest report is 3925 B. | C1 |
| registration recorded | `wave1-registration.json` covers 89/89 members, each agentId = `KaidokuR18.<name>`. It equals `wave1-assignments.json` and the 89 spawned ids in `wave1-result.txt:2`. Recorded 15:24:55.714Z, 17 s after the spawn call (`wave1-result.txt:1`, 12:24:38.6 -03:00). | `wave1-registration.json:2-7,979`; `wave1-assignments.json:2,90`; C2 |
| seats without reports | **none (0/89)** | C1; canonical collector `reportSummary {expected 89, present 89, missing []}` (C4) |

`LOG.md:2133-2134` says: "Wave 1: 89 seats in one validated `task` call (executor19/scout23/reviewer15/scribe10/connector8/critic6/revenger4/sentinel2/simplifier2), 89/89 reports". That holds, and the role mix matches the dispatch exactly (C1). `[OBS]`

Gaps G1–G3 below don't falsify any of these checks or the LOG line. They limit what the wave-1 record supports: the declared registry is still unfilled, there is no settled-outcome record, and one seat ended aborted.

## Gaps (non-breaking)

**G1 — the dispatch-declared registry was never filled; registration landed in a side copy.** `[OBS]`
- The dispatch declares `registry.path` = `.ufo/waves/round-18/w1/swarm-registry.json` (`wave1-dispatch.json:23`).
  - At REV that file still has 89/89 `agentId: null` (`w1/swarm-registry.json:10` and all other members).
  - Its `createdAt` equals its `updatedAt`, both 15:24:25.898Z (`:4-5`).
- `record` instead wrote `.ufo/waves/round-18/wave1-registry.json` (`wave1-registration.json:2`).
  - That file carries `"wave": null` (`wave1-registration.json:4`; `wave1-registry.json:3`) and createdAt == updatedAt == record time.
  - `wave1-registry.json` is JSON-equal (parsed comparison, not bytes) to the registration content minus `path` (C2).
- The validator contract (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`, HEAD `31c465f15669`, working tree clean for this file):
  - `run` persists the registry at `reportDir/swarm-registry.json` with null ids, and "`record` fills them … so a later wave's resume lanes can name members" (`:53-58`).
  - `record` requires the file to exist (`:1602`), writes back to the same path (`:1741`) and emits `{path, …doc}` (`:1744`).
  - It preserves `wave`/`createdAt` from the loaded doc (`:1735-1736`), defaulting them to `null`/now (`:620-621`).
- `[INF]` The side file was therefore created before `record` without `wave`/`createdAt` keys. That is consistent with a copy of the dispatch's inline `registry` object (`wave1-dispatch.json:21-24`: schema/path/reportDir/members).
- Effect, observed with the canonical collector on a REV export (C4). Its default registry is the wave record's `registry.path` (`ufo-swarm-collect.mjs:26-31`).
  - Default run: `reportSummary {89, 89, []}`, but **0/89** entries carry an agentId.
  - With `--registry .ufo/waves/round-18/wave1-registry.json`: 89/89.
- Trend `[OBS]` (C3), declared-registry nulls by round:
  - r14 0/32, r15 0/32, and r16 0/64 (r16's registration path is the declared registry, i.e. it was filled in place).
  - r17 78/78 null.
  - r18 89/89 null, side file.
- `[INF]` A later wave whose `priorRegistry` names the declared path could not resolve these members (`resume_unknown_member`). There is no realized harm yet. `[OBS]` (C12) The post-REV, untracked `wave2-spec.json` has no `priorRegistry` and no resume items, and `wave2-*` follows the same side-file pattern (`w2/swarm-registry.json` 98/98 null; `wave2-registration.path` = `wave2-registry.json`).

**G2 — no settled-outcome record for wave 1 at REV.** `[OBS]`
- `wave1-result.txt` is only the spawn acknowledgement:
  - one line, `attempt1 … 12:24:38.609 -> 12:24:38.624` (`:1`);
  - `progress` statuses `{pending: 89}`, `details.results` = 0 (C2).
- No round-18 outcomes file exists. Rounds 16 and 17 kept them (`round-16/wave1-outcomes.json`, `round-16/wave2-outcomes.json`, `round-17/wave-outcomes.json`; C3).
- `SCORECARD.md:2398-2405` reports r17 per-wave completions and deaths and lists "Records: `wave-outcomes.json`, `wave*-registration.json`".
- The round-18 SCORECARD section (`SCORECARD.md:2428`) has no Waves subsection yet; its only headings are `:2428` and `:2436` (C12). So this is pending for the round close, not a broken claim. `LOG.md:2134` claims reports, not completions, which is accurate as written.

**G3 — 88/89 seats ended normally; `SwissMisreadTool` ended aborted.**
- Seat transcripts are outside the lane: `~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/`. They are not agent.db or credential files, and no credential fields were printed.
- C5 `[OBS]`:
  - all 89 transcripts exist;
  - final assistant `stopReason` is `stop` for 88 seats and `aborted` for 1;
  - 9 seats had at least one `error` turn and continued afterwards; every one of them except SwissMisreadTool ended `stop`;
  - in 89/89 transcripts, the seat's own write/edit/bash calls touch its own `w1/<name>.md`, so every report was seat-authored.
- C7 timeline `[OBS]` (times in Z):

  | time | event |
  |---|---|
  | 16:02:25.929 | L1 sends "please land what you have within ~10 minutes" |
  | 16:04:49.784 | seat writes its report |
  | 16:05:55.256 | seat's last report edit |
  | 16:06:02.891 | final assistant turn `aborted`, "Request was aborted"; no yield message |
  | 16:13:02.902 | `session_exit dispose` |

- The REV bytes are that final edit (C1b: worktree == REV, `git diff --quiet` exit 0; file mtime 13:05:55 -03:00, C12).
- Cause of the abort is unresolved. The L1 transcript shows no kill or `proc://` write naming the seat (C9) `[OBS]`.
- Related `[OBS]` (C9, C10): the L1's only read of this report was at 16:05:06Z, before the seat's last two modifications. The read differs from REV at `w1/SwissMisreadTool.md:90` (an mcount cell) and `:97` (an added `ghidra_uncommon` sentence), both in §4 (`:80-112`).
- `[INF]` No effect on the knowledge entry: it cites this report at `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:119`, pointing at §5 (`:113-129`), which the late edits did not touch (C10).

## Checked and consistent (no finding)

- **One task call, payload as validated** `[OBS]` (C8):
  - one `attempt1` line;
  - each of the 89 spawn texts is `"Complete assignment thoroughly:\n\n"` + the dispatch `task` + one identical suffix (`# Tooling directive — operator, 2026-10-19 …`). `[INF]` The prefix and suffix are injected by the host or operator; the lane did not rewrite the tasks.
  - `wave1-spec.json` prompts appear verbatim in the dispatch tasks (89/89), roles match (89/89) and the context is identical.
- **Timing** `[OBS]` (C8): the reports' worktree mtimes are metadata, and their bytes equal REV.
  - The cited reports behind the contract amendments (`contract.md:148`, "~12:40 -03:00") were last written by 12:35:54 -03:00, before `contract.md` (12:37:59).
  - All 89 reports were last written between 12:25:52 and 13:05:55 -03:00, with 15 after 12:40.
  - All of them landed before commit `eb6c266` (13:23:55 -0300). That is the only commit touching `w1/` through REV (C1b) and it added all 90 entries. They also predate the claims amendment (`claims.json:35`, 13:25 -03:00).
- **No misplaced or degenerate reports** `[OBS]` (C12):
  - No seat-named `.md` files exist outside `round-18/w1/` except prior-round namesakes (`round-17/w1/ConnSiblingOverlap.md`, `round-17/w2/CriticSourcedClaim.md`).
  - The fleet repo has no `.ufo/waves/round-18`.
  - No report has a blocked, stub or placeholder marker in its first 6 lines, and there are no duplicate blobs.

## Remaining unknowns

- Why the last SwissMisreadTool turn was aborted (host-side cause not observable from the lane or the L1 tool calls).
- Whether the round close will add a wave-1 outcomes record that shows 88 `stop` + 1 aborted-after-landing (G2/G3), and whether `record` will be pointed at the declared registry (G1).

## Commands (verbatim; exit codes as observed)

C1 — dispatch vs reports (cwd: lane root)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; python3 -I -B -c '
import json,subprocess as sp,sys,collections
R=sys.argv[1]; B=".ufo/waves/round-18/"
g=lambda p: sp.run(["git","show",R+":"+B+p],capture_output=True,text=True,check=True).stdout
d=json.loads(g("wave1-dispatch.json")); t=d["taskCall"]["tasks"]; names={x["name"] for x in t}
ok=all([l for l in x["task"].splitlines() if l.startswith("Report:")]==["Report: write your scoped findings to "+B+"w1/"+x["name"]+".md"] for x in t)
files=sp.run(["git","ls-tree","-l",R,B+"w1/"],capture_output=True,text=True,check=True).stdout.splitlines()
md={l.split("\t")[1].rsplit("/",1)[1][:-3]:int(l.split()[3]) for l in files if l.endswith(".md")}
print("counts",d["counts"],"| tasks",len(t),"unique",len(names),"| one Report: trailer = w1/<name>.md:",ok)
print("roles",dict(collections.Counter(x["agent"] for x in t).most_common()))
print("w1 entries",len(files),"| .md",len(md),"| missing",sorted(names-set(md)),"| extra",sorted(set(md)-names),"| min bytes",min(md.values()))
' "$REV"; echo EXIT=$?
```
```
counts {'spawn': 89, 'resume': 0, 'total': 89} | tasks 89 unique 89 | one Report: trailer = w1/<name>.md: True
roles {'scout': 23, 'executor': 19, 'reviewer': 15, 'scribe': 10, 'connector': 8, 'critic': 6, 'revenger': 4, 'sentinel': 2, 'simplifier': 2}
w1 entries 90 | .md 89 | missing [] | extra [] | min bytes 3925
EXIT=0
```

C1b — w1 history and worktree identity (cwd: lane root)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; git log --format='%h %ci %s' "$REV" -- .ufo/waves/round-18/w1; echo EXIT=$?; git diff --quiet "$REV" -- .ufo/waves/round-18/w1; echo DIFF_EXIT=$?
```
```
eb6c266 2026-10-20 13:23:55 -0300 round-18: frozen C3 predictions and decision rule, wave-1 tools and evidence (pre-run)
EXIT=0
DIFF_EXIT=0
```

C2 — registration chain (cwd: lane root)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; python3 -I -B -c '
import json,subprocess as sp,sys,ast,re,collections
R=sys.argv[1]; B=".ufo/waves/round-18/"
g=lambda p: sp.run(["git","show",R+":"+B+p],capture_output=True,text=True,check=True).stdout
names=[x["name"] for x in json.loads(g("wave1-dispatch.json"))["taskCall"]["tasks"]]
reg=json.loads(g("wave1-registration.json")); rg=json.loads(g("wave1-registry.json")); sw=json.loads(g("w1/swarm-registry.json")); asg=json.loads(g("wave1-assignments.json"))
ids=lambda o: {k:v["agentId"] for k,v in o["members"].items()}
print("registration: path",reg["path"],"wave",reg["wave"],"created",reg["createdAt"],"members",len(reg["members"]),"filled",sum(v is not None for v in ids(reg).values()),"all==KaidokuR18.<name>",all(v=="KaidokuR18."+k for k,v in ids(reg).items()),"set==dispatch",set(reg["members"])==set(names))
print("wave1-registry.json == registration minus path:",{k:v for k,v in reg.items() if k!="path"}==rg)
print("assignments: n",len(asg),"== registration ids:",asg==ids(reg))
print("declared w1/swarm-registry.json: wave",sw["wave"],"created",sw["createdAt"],"updated",sw["updatedAt"],"null agentIds",sum(v is None for v in ids(sw).values()),"/",len(sw["members"]))
L=g("wave1-result.txt").split("\n"); r=ast.literal_eval(L[1]); P=r["details"]["progress"]
sp_ids=re.findall(r"`(KaidokuR18\.\w+)` \(job",r["text"])
print("result:",L[0],"| spawned",len(sp_ids),"== assignments",set(sp_ids)==set(asg.values()),"| progress status",dict(collections.Counter(p["status"] for p in P)),"| details.results",len(r["details"]["results"]))
' "$REV"; echo EXIT=$?
```
```
registration: path .ufo/waves/round-18/wave1-registry.json wave None created 2026-10-20T15:24:55.714Z members 89 filled 89 all==KaidokuR18.<name> True set==dispatch True
wave1-registry.json == registration minus path: True
assignments: n 89 == registration ids: True
declared w1/swarm-registry.json: wave kaidoku-r18-w1 created 2026-10-20T15:24:25.898Z updated 2026-10-20T15:24:25.898Z null agentIds 89 / 89
result: attempt1 2026-10-20T12:24:38.609054-03:00 -> 2026-10-20T12:24:38.624704-03:00 | spawned 89 == assignments True | progress status {'pending': 89} | details.results 0
EXIT=0
```

C3 — cross-round registry fill and outcome records (cwd: lane root)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; python3 -I -B -c '
import json,subprocess as sp,sys
R=sys.argv[1]
def j(p):
    r=sp.run(["git","show",R+":"+p],capture_output=True,text=True); return json.loads(r.stdout) if r.returncode==0 else None
for n in (14,15,16,17,18):
    sw=j(".ufo/waves/round-%d/w1/swarm-registry.json"%n); reg=j(".ufo/waves/round-%d/wave1-registration.json"%n)
    print("r%d w1/swarm-registry null agentIds %d/%d | wave1-registration.path %s" % (n,sum(v["agentId"] is None for v in sw["members"].values()),len(sw["members"]),(reg or {}).get("path","<absent file>" if reg is None else "<no path key>")))
fs=sp.run(["git","ls-tree","-r","--name-only",R,".ufo/waves/round-16/",".ufo/waves/round-17/",".ufo/waves/round-18/"],capture_output=True,text=True,check=True).stdout.split()
print("outcome records:",[f for f in fs if "outcomes" in f])
' "$REV"; echo EXIT=$?
```
```
r14 w1/swarm-registry null agentIds 0/32 | wave1-registration.path <absent file>
r15 w1/swarm-registry null agentIds 0/32 | wave1-registration.path <absent file>
r16 w1/swarm-registry null agentIds 0/64 | wave1-registration.path .ufo/waves/round-16/w1/swarm-registry.json
r17 w1/swarm-registry null agentIds 78/78 | wave1-registration.path <no path key>
r18 w1/swarm-registry null agentIds 89/89 | wave1-registration.path .ufo/waves/round-18/wave1-registry.json
outcome records: ['.ufo/waves/round-16/wave1-outcomes.json', '.ufo/waves/round-16/wave2-outcomes.json', '.ufo/waves/round-17/wave-outcomes.json']
EXIT=0
```

C4 — canonical collector on a `git archive` export of REV (cwd: lane root; writes only under the temp dir, which is removed). The results file is a **synthetic driver**: its `status: completed` rows are placeholders the collector requires. Only `reportSummary` and agentId attribution are read from the output; collector `outcome` fields are not evidence.
```
rm -rf /tmp/wec-eooO6y; REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; T=$(mktemp -d /tmp/wec-XXXXXX) && git archive "$REV" .ufo/waves/round-18 | tar -x -C "$T" && cd "$T" && python3 -I -B -c 'import json; a=json.load(open(".ufo/waves/round-18/wave1-assignments.json")); json.dump({"schema":"ufo-swarm-results-v1","members":[{"name":n,"status":"completed"} for n in a]},open("synthetic-results.json","w"))' && C=/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-collect.mjs && W=.ufo/waves/round-18/wave1-dispatch.json && UFO_PROJECT_ROOT="$T" node "$C" collect --wave "$W" --results synthetic-results.json --runId wec-probe --sessionId wec-probe > a.json; echo "collect(default registry) EXIT=$?"; UFO_PROJECT_ROOT="$T" node "$C" collect --wave "$W" --results synthetic-results.json --registry .ufo/waves/round-18/wave1-registry.json --runId wec-probe --sessionId wec-probe > b.json; echo "collect(--registry wave1-registry.json) EXIT=$?"; python3 -I -B -c '
import json
for f,lbl in (("a.json","default=dispatch registry.path"),("b.json","--registry wave1-registry.json")):
    d=json.load(open(f)); s=d["subagents"]
    print(lbl,"| reportSummary",d["reportSummary"],"| entries with agentId",sum("agentId" in e for e in s),"/",len(s))
'; echo "summary EXIT=$?"; cd / && rm -rf "$T"; echo "cleanup EXIT=$?"
```
```
collect(default registry) EXIT=0
collect(--registry wave1-registry.json) EXIT=0
default=dispatch registry.path | reportSummary {'expected': 89, 'present': 89, 'missing': []} | entries with agentId 0 / 89
--registry wave1-registry.json | reportSummary {'expected': 89, 'present': 89, 'missing': []} | entries with agentId 89 / 89
summary EXIT=0
cleanup EXIT=0
```

C5 — seat transcripts: final state and self-authorship (cwd: the session dir `…/01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18`)
```
python3 -I -B -c '
import json,subprocess as sp,collections,os
R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
names=list(json.loads(sp.run(["git","-C","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","show",R+":.ufo/waves/round-18/wave1-assignments.json"],capture_output=True,text=True,check=True).stdout))
fin=collections.Counter(); odd=[]; selfw=0; errs=0
for n in names:
    recs=[json.loads(l) for l in open("KaidokuR18.%s.jsonl"%n) if l.strip()]
    A=[r for r in recs if r.get("type")=="message" and r["message"].get("role")=="assistant"]
    sr=A[-1]["message"].get("stopReason"); fin[sr]+=1
    if sr!="stop": odd.append((n,sr,A[-1]["timestamp"],A[-1]["message"].get("errorMessage")))
    errs+=any(a["message"].get("stopReason")=="error" for a in A)
    tgt="w1/%s.md"%n
    selfw+=any(c.get("type")=="toolCall" and tgt in json.dumps(c.get("arguments") or {}) and c.get("name") in ("write","edit","bash") for a in A for c in (a["message"].get("content") or []) if isinstance(c,dict))
    ex=[r for r in recs if r.get("customType")=="session_exit"]
print("transcripts",sum(os.path.exists("KaidokuR18.%s.jsonl"%n) for n in names),"/",len(names),"| final stopReason",dict(fin),"| seats with >=1 error turn",errs,"| seats whose own calls touch own report path",selfw)
print("non-stop finals:",odd)
' ; echo EXIT=$?
```
```
transcripts 89 / 89 | final stopReason {'stop': 88, 'aborted': 1} | seats with >=1 error turn 9 | seats whose own calls touch own report path 89
non-stop finals: [('SwissMisreadTool', 'aborted', '2026-10-20T16:06:02.891Z', 'Request was aborted')]
EXIT=0
```

C6 — anchor lines at REV (cwd: lane root). The `for` loop prints `LOG.md:2133-2134`, `SCORECARD.md:2398-2405`, `contract.md:148`, `wave1-dispatch.json:16-24`, `wave1-registration.json:2-7` and `w1/swarm-registry.json:3-10`, all quoted above. EXIT=0.
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; for spec in LOG.md:2133-2134 SCORECARD.md:2398-2405 .ufo/waves/round-18/contract.md:148-148 .ufo/waves/round-18/wave1-dispatch.json:16-24 .ufo/waves/round-18/wave1-registration.json:2-7 .ufo/waves/round-18/w1/swarm-registry.json:3-10; do f=${spec%%:*}; r=${spec#*:}; git show "$REV:$f" | python3 -I -B -c 'import sys; a,b=map(int,sys.argv[2].split("-")); L=sys.stdin.read().splitlines(); [print(sys.argv[1]+":"+str(i), L[i-1][:170]) for i in range(a,b+1)]' "$f" "$r"; done; echo EXIT=$?
```

C7 — SwissMisreadTool end-of-run timeline (cwd: the C5 session dir)
```
python3 -I -B -c '
import json
for l in open("KaidokuR18.SwissMisreadTool.jsonl"):
    r=json.loads(l); ts=r.get("timestamp",""); m=r.get("message") if isinstance(r.get("message"),dict) else {}
    if ts<"2026-10-20T16:02": continue
    if m.get("role")=="user": c=m["content"]; t=c if isinstance(c,str) else " ".join(x.get("text","") for x in c if isinstance(x,dict)); i=t.find("L1:"); print(ts,"user(irc)",t[i:i+60])
    elif m.get("role")=="assistant":
        calls=[(c.get("name"),(c.get("arguments") or {}).get("i")) for c in (m.get("content") or []) if isinstance(c,dict) and c.get("type")=="toolCall"]
        if m.get("stopReason")!="toolUse" or any(n in ("write","edit") for n,_ in calls): print(ts,"assistant",m.get("stopReason"),m.get("errorMessage") or "",calls)
    elif r.get("customType")=="session_exit": print(ts,"session_exit",r.get("data",{}).get("reason"))
'; echo EXIT=$?
```
```
2026-10-20T16:02:25.929Z user(irc) L1: please land what you have within ~10 minutes. Also emit 
2026-10-20T16:04:49.784Z assistant toolUse  [('write', 'Writing SwissMisreadTool report')]
2026-10-20T16:05:55.256Z assistant toolUse  [('edit', 'Fixing report sentence')]
2026-10-20T16:06:02.891Z assistant aborted Request was aborted []
2026-10-20T16:13:02.902Z session_exit dispose
EXIT=0
```

C8 — spawn-payload fidelity and timing (cwd: lane root; mtimes are worktree metadata, and C1b shows the bytes equal REV)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; python3 -I -B -c '
import json,subprocess as sp,sys,ast,os,datetime,glob
R=sys.argv[1]; B=".ufo/waves/round-18/"
g=lambda p: sp.run(["git","show",R+":"+B+p],capture_output=True,text=True,check=True).stdout
d=json.loads(g("wave1-dispatch.json")); T={x["name"]:x for x in d["taskCall"]["tasks"]}; s=json.loads(g("wave1-spec.json"))
P=ast.literal_eval(g("wave1-result.txt").split("\n")[1])["details"]["progress"]; pre="Complete assignment thoroughly:\n\n"
suf={p["task"][len(pre+T[p["id"].split(".",1)[1]]["task"]):] for p in P if p["task"].startswith(pre+T[p["id"].split(".",1)[1]]["task"])}
print("spawn text = prefix+dispatch task+suffix:",sum(p["task"].startswith(pre+T[p["id"].split(".",1)[1]]["task"]) for p in P),"/",len(P),"| distinct suffixes",len(suf),"| suffix starts",[x[:60] for x in suf])
print("spec prompt verbatim in task",sum(i["prompt"] in T[i["name"]]["task"] for i in s["items"]),"/",len(s["items"]),"| role==agent",sum(i["role"]==T[i["name"]]["agent"] for i in s["items"]),"| context equal",s["context"]==d["taskCall"]["context"])
tz=datetime.timezone(datetime.timedelta(hours=-3)); mt=lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(B+p),tz).strftime("%H:%M:%S")
cited=["CriticC1","CriticC2","CriticC3","ConnSiblingOverlap","ScoutLaneGitSitesNow","RevGhidraMapTypeRead","ScoutGhidraGoStructMapping","SentinelSandbox"]+sorted(os.path.basename(p)[:-3] for p in glob.glob(B+"w1/RevBase*.md"))
print("contract.md:148 cited reports, latest mtime",max(mt("w1/%s.md"%n) for n in cited),"| contract.md mtime",mt("contract.md"))
allm=sorted(mt("w1/%s.md"%n) for n in T); print("all 89 report mtimes: first",allm[0],"last",allm[-1],"| after 12:40:00",sum(x>"12:40:00" for x in allm))
' "$REV"; echo EXIT=$?
```
```
spawn text = prefix+dispatch task+suffix: 89 / 89 | distinct suffixes 1 | suffix starts ['\n\n# Tooling directive — operator, 2026-10-19 (always on, eve']
spec prompt verbatim in task 89 / 89 | role==agent 89 | context equal True
contract.md:148 cited reports, latest mtime 12:35:54 | contract.md mtime 12:37:59
all 89 report mtimes: first 12:25:52 last 13:05:55 | after 12:40:00 15
EXIT=0
```

C9 — L1 calls naming the seat (cwd: the session dir `…/01a15963-70c3-7390-a1b4-7911b9506d07`). Output shows no kill or `proc://` write; the only read of the report is at 16:05:06.
```
python3 -I -B -c '
import json
for l in open("KaidokuR18.jsonl"):
    if "SwissMisreadTool" not in l: continue
    r=json.loads(l); m=r.get("message") if isinstance(r.get("message"),dict) else {}
    if m.get("role")!="assistant": continue
    for c in m.get("content") or []:
        if isinstance(c,dict) and c.get("type")=="toolCall":
            a=c.get("arguments") or {}; s=json.dumps(a)
            if "SwissMisreadTool" in s: print(r["timestamp"][:19],c.get("name"),a.get("i"),"|",(a.get("path") or a.get("command") or "")[:150].replace(chr(10)," "))
'; echo EXIT=$?
```
```
2026-10-20T15:24:16 write Writing wave-1 spec generator | …/round-18/gen-wave1.py
2026-10-20T15:37:36 write C3 cross-seat findings for emulator | agent://KaidokuR18.SwissMisreadTool
2026-10-20T15:41:16 bash Waiting for key tool seats | cd …/round-18/w1; for i in $(seq 1 60); do …
2026-10-20T16:02:09 write Status and failure-kind request | agent://KaidokuR18.SwissMisreadTool
2026-10-20T16:04:01 bash Checking swiss-misread status | … ls -la tools/ w1/SwissMisreadTool.md …
2026-10-20T16:05:01 bash Waiting for swiss-misread report | for i in $(seq 1 40); do [ -f …/w1/SwissMisreadTool.md ] && break; sleep 15; done; …
2026-10-20T16:05:06 bash Reading swiss-misread report | cd …/round-18 && sed -n 1,200p w1/SwissMisreadTool.md | cut -c1-400
2026-10-20T16:34:04 write Writing C3 knowledge entry | …/corpus/knowledge/2026-10-20-r18-swiss-map-replay.md
EXIT=0
```
(The paths in the C9 output are shortened with `…` for width; the command prints them in full.)

C10 — what the L1 read at 16:05:06Z vs REV, and where the difference sits (cwd: C9 session dir, then lane root)
```
python3 -I -B -c '
import json,subprocess as sp,difflib
R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
recs=[json.loads(l) for l in open("KaidokuR18.jsonl") if l.strip()]
cid=None
for r in recs:
    m=r.get("message") if isinstance(r.get("message"),dict) else {}
    if m.get("role")=="assistant" and r.get("timestamp","").startswith("2026-10-20T16:05:06"):
        for c in m.get("content") or []:
            if isinstance(c,dict) and c.get("type")=="toolCall" and "SwissMisreadTool.md" in json.dumps(c.get("arguments")): cid=c.get("id"); cmd=c["arguments"].get("command")
res=[r for r in recs if isinstance(r.get("message"),dict) and r["message"].get("role")=="toolResult" and r["message"].get("toolCallId")==cid]
txt="".join(x.get("text","") for x in res[0]["message"]["content"] if isinstance(x,dict)) if res else None
print("call",cid is not None,"| cmd:",cmd,"| result at",res[0]["timestamp"] if res else None)
rev=sp.run(["git","-C","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","show",R+":.ufo/waves/round-18/w1/SwissMisreadTool.md"],capture_output=True,text=True,check=True).stdout
exp="\n".join(l[:400] for l in rev.splitlines()[:200])
a=[l.rstrip() for l in txt.strip().splitlines()]; b=[l.rstrip() for l in exp.strip().splitlines()]
d=[x for x in difflib.unified_diff(a,b,"L1-read-16:05:06Z","REV",n=0,lineterm="") if not x.startswith(("---","+++"))]
print("L1-read lines",len(a),"| REV lines (first 200, cut 400)",len(b),"| identical",a==b,"| differing hunks/lines",len(d))
for x in d[:12]: print("  ",x[:200])
'; echo EXIT=$?
```
```
call True | cmd: cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18 && sed -n 1,200p w1/SwissMisreadTool.md | cut -c1-400 | result at 2026-10-20T16:05:06.109Z
L1-read lines 178 | REV lines (first 200, cut 400) 179 | identical False | differing hunks/lines 7
   @@ -90 +90 @@
   -| `*http.Header` | 40 | 40 / 0 | **past_eof same pair** | (real mcount 13) | silent |
   +| `*http.Header` | 40 | 40 / 0 | **past_eof same pair** | 20987 / 13 | silent |
   @@ -97 +97,2 @@
   -name, tag `a`, pkgPath `0x780100`; `types+0x780100` = `0x10D4120`, whose LEB128 name length is 111,938,854
   +name, tag `a`, pkgPath `0x780100`. The emitted `per_type[].h1.ghidra_uncommon` for the three failing maps is `{pkg_path: 40, mcount: 0, moff: 16}`; H0 emits `{55036, 5}`, `{16493, 6}`, `{20987, 13}`.
   +`types+0x780100` = `0x10D4120`, whose LEB128 name length is 111,938,854
EXIT=0
```
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; git show "$REV:.ufo/waves/round-18/w1/SwissMisreadTool.md" | python3 -I -B -c 'import sys; [print("SwissMisreadTool.md:%d"%i,l[:70]) for i,l in enumerate(sys.stdin.read().splitlines(),1) if l.startswith("## 4") or l.startswith("## 5") or l.startswith("## 6") or i in (90,97)]'; echo EXIT=$?; git show "$REV:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md" | python3 -I -B -c 'import sys; L=sys.stdin.read().splitlines(); print("lines",len(L)); print("knowledge:119",L[118])'; echo EXIT=$?
```
```
SwissMisreadTool.md:80 ## 4. Aether per-type map-path evidence (h1 vs h0)
SwissMisreadTool.md:90 | `*http.Header` | 40 | 40 / 0 | **past_eof same pair** | 20987 / 13 |
SwissMisreadTool.md:97 name, tag `a`, pkgPath `0x780100`. The emitted `per_type[].h1.ghidra_u
SwissMisreadTool.md:113 ## 5. Reconciliation with peers
SwissMisreadTool.md:130 ## 6. Anchors (Base-src.zip members; read in this session)
EXIT=0
lines 119
knowledge:119   from the log by 3 of ~5927 (w1 `SwissMisreadTool.md` §5).
EXIT=0
```

C11 — the validator source cited in G1 is unmodified at its HEAD (cwd: `/home/vgpnk/Projects/ufo-fsd-alpha`)
```
git rev-parse --short=12 HEAD; git diff --quiet HEAD -- scripts/ufo-swarm-wave.mjs scripts/ufo-swarm-collect.mjs; echo DIFF_EXIT=$?
```
```
31c465f15669
DIFF_EXIT=0
```

C12 — residual consistency checks (cwd: lane root; the `wave2-*`/`w2/` reads are post-REV untracked worktree files, as `git status` shows)
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; python3 -I -B -c '
import json,subprocess as sp,sys,re,collections,os,datetime
R=sys.argv[1]; B=".ufo/waves/round-18/"
g=lambda p: sp.run(["git","show",R+":"+p],capture_output=True,text=True,check=True).stdout
names=list(json.loads(g(B+"wave1-assignments.json")))
allf=sp.run(["git","ls-tree","-r","--name-only",R],capture_output=True,text=True,check=True).stdout.splitlines()
print("seat-named .md outside round-18/w1:",[f for f in allf if f.endswith(".md") and f.rsplit("/",1)[-1][:-3] in names and not f.startswith(B+"w1/")])
print("fleet repo .ufo/waves/round-18 exists:",os.path.exists("/home/vgpnk/Projects/shokunin/.ufo/waves/round-18"))
pat=re.compile(r"\b(BLOCKED|blocked|could not complete|did not (finish|complete)|incomplete|placeholder|TODO|stub|timed out|rate limit|aborted)\b")
print("marker hits in first 6 lines:",[n for n in names if pat.search("\n".join(g(B+"w1/%s.md"%n).splitlines()[:6]))])
blobs=[l.split()[2] for l in sp.run(["git","ls-tree",R,B+"w1/"],capture_output=True,text=True,check=True).stdout.splitlines()]
print("duplicate blobs in w1:",[k for k,v in collections.Counter(blobs).items() if v>1])
L=g("SCORECARD.md").splitlines(); print("SCORECARD headings from :2428:",[(i,L[i-1][:60]) for i in range(2428,len(L)+1) if L[i-1].startswith("#")],"| last line",len(L))
tz=datetime.timezone(datetime.timedelta(hours=-3)); print("SwissMisreadTool.md mtime",datetime.datetime.fromtimestamp(os.path.getmtime(B+"w1/SwissMisreadTool.md"),tz).isoformat(timespec="seconds"))
s=json.load(open(B+"wave2-spec.json")); sw=json.load(open(B+"w2/swarm-registry.json")); rg=json.load(open(B+"wave2-registration.json"))
print("post-REV worktree: wave2-spec priorRegistry",s.get("priorRegistry"),"| resume items",sum("resume" in i for i in s["items"]),"| w2/swarm-registry null",sum(v["agentId"] is None for v in sw["members"].values()),"/",len(sw["members"]),"| wave2-registration.path",rg.get("path"))
' "$REV"; echo EXIT=$?; git status --porcelain -- .ufo/waves/round-18/wave2-spec.json .ufo/waves/round-18/w2/swarm-registry.json; echo EXIT=$?
```
```
seat-named .md outside round-18/w1: ['.ufo/waves/round-17/w1/ConnSiblingOverlap.md', '.ufo/waves/round-17/w2/CriticSourcedClaim.md']
fleet repo .ufo/waves/round-18 exists: False
marker hits in first 6 lines: []
duplicate blobs in w1: []
SCORECARD headings from :2428: [(2428, '## Round 18 — routed r17 defects, jj-safe revision pins, Swi'), (2436, '### Routed r17 corrections (append-only)')] | last line 2440
SwissMisreadTool.md mtime 2026-10-20T13:05:55-03:00
post-REV worktree: wave2-spec priorRegistry None | resume items 0 | w2/swarm-registry null 98 / 98 | wave2-registration.path .ufo/waves/round-18/wave2-registry.json
EXIT=0
?? .ufo/waves/round-18/w2/swarm-registry.json
?? .ufo/waves/round-18/wave2-spec.json
EXIT=0
```

## Checks for the integrating seat

- Re-run C1, C2 and C4 against the final round commit if `w1/` or the `wave1-*` files change after REV.
- If an outcomes record is added at close, it should show 88 `stop` + 1 aborted (`SwissMisreadTool`) per C5.
