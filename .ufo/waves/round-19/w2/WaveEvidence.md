# Wave 1 evidence review

Axes: calibration, freshness, depth. Scope: `wave1-spec.json`, `wave1-dispatch.json`, wave 1 registration/outcomes, report/cause records, and the follow-on wave 2 roster. Read-only review; this file is the only write.

## Findings

### P1 — The dispatched task strings are not identical to the spec prompts (90/90)

**Observation.** `wave1-spec.json` defines each task as `{name, role, prompt}` (`:11-15` is the first row); dispatch carries `{name, agent, task}` under `taskCall.tasks` (`wave1-dispatch.json:1026-1032`). The contexts match, all 90 names and role labels match, and each dispatched `task` starts with its spec `prompt`; however, exact string equality is **0/90**. Each dispatch task appends extra text after the spec prompt: lane-boundary text, `Judged on: calibration, freshness, depth`, and a per-seat `Report:` path. For example, the first spec prompt ends with its acceptance text at `wave1-spec.json:15`, while the corresponding dispatched task is at `wave1-dispatch.json:1032` and continues beyond that original text. The generator builds the spec prompt from the directive, task body, and acceptance text (`gen-wave1.py:25-40`); it does not put the later dispatch suffix in the spec item.

**Impact / inference.** If the validated payload is the `prompt` stored in the spec, the claim that it was dispatched unchanged is falsified for every seat. This is an append-only change, not a replacement of the core task; the added instructions may be useful, but the artifacts show no validation digest/receipt covering the resulting full dispatch strings. Treat the spec as the validated base prompt, not as an exact record of the full payload.

### P2 — The wave-1 cause summary over-attributes all 42 missing reports to the L1 exit

**Observation.** `claims.json:37` says the L1 session exit “killed 42 wave-1 seats.” The outcome record has 42 missing reports and 42 non-empty causes (`wave1-outcomes.json:15-19`), but cause text divides them into **33 parent-session aborts and 9 direct provider 429 errors**. The nine 429 entries are visible together in `evidence/wave-outcomes/w1-causes.json:24-32`; examples also appear in `wave1-outcomes.json:109-121`. The other entries describe aborted requests attributed to the L1 session exit (for example `wave1-outcomes.json:73`). A read-only check found the cited transcript line for each of the 42 entries in range; the 33 abort anchors carry an abort marker and all nine direct-429 anchors carry a 429 marker.

**Impact.** The 42 missing/no-report total is supported, but the single-cause wording is not: nine are recorded as request-level rate-limit errors rather than as tasks killed by the later L1 session exit. Preserve the distinction when describing failure cause.

## Observed invariants and limits

- **Seat count and roles:** spec, dispatch tasks, registration, registry snapshot, outcomes, and assignment map each contain 90 entries. Names are unique in each and the six name sets agree. Role labels agree across spec, dispatch, registration, and outcomes; no `planner` role is present. Distribution: scout 23, reviewer 18, executor 17, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2. Spec/dispatch set the lane ceiling to 100 and the dispatch spawns 90 (`wave1-spec.json:8-9`; `wave1-dispatch.json:4-19`): this is 90/100, not a saturated 100-seat wave.
- **Identity and replacement:** the post-dispatch `wave1-registration.json` has 90 distinct agent IDs; every ID matches `wave1-assignments.json` and the 90 IDs in the launch receipt. Dispatch records 90 spawns, zero resumes, and an empty `resumeSends` list (`wave1-dispatch.json:16-19,1481-1482`); every registered member is `kind: spawn`. None of the 42 missing wave-1 seat names occurs in the 72-name wave-2 spec. **No replacement is recorded in these artifacts.** This does not prove absence of an unrecorded out-of-band invocation.
- **Reports versus causes:** the 48 non-empty `.md` files in `w1/` match exactly the 48 outcomes marked `report_present`; the remaining 42 have non-empty cause text and `uncaused` is empty (`wave1-outcomes.json:10-19,20-64,68-609`). The registration and causes SHA-256 values in the outcome file match their current files (`wave1-outcomes.json:4,8`). This establishes accounting consistency, not 48 successful/complete reports: `wave-outcomes.py:170-176,318-353` defines report presence as a regular file with size greater than zero and considers any non-empty cause string sufficient.
- **Canonical receipt:** the dispatch contains one `taskCall` with 90 tasks (`wave1-dispatch.json:1026-1480`); `wave1-result.txt:1` records 90 spawned agents. Its captured progress contains 90 unique fully-qualified IDs matching the registration, each captured task starts with the dispatch task after the standard runner prefix, and all progress states are `pending` with `results=[]`. This is a spawn receipt, not proof of task completion. No second wave-1 call or replacement is represented here.

## Residual risks and verification gaps

- The dispatch's declared registry path is `w1/swarm-registry.json` (`wave1-dispatch.json:21-25`), whose 90 members still have `agentId: null` (`w1/swarm-registry.json:8-12` and the count command below). The later registration snapshot has the populated, verified mapping, but its `wave` is null (`wave1-registration.json:2-7`); `wave1-outcomes.json` also has `wave: null` (`:9`). I found no wrong identity in the populated mapping, but a consumer following only the dispatch registry path cannot resolve agent IDs from that file; joining relies on the separate registration/assignment artifacts.
- Cause text contains transcript paths outside the round-19 tree; `cause_sources` is empty (`wave1-outcomes.json:67`) because the causes file stores plain strings rather than structured source fields. The underlying line anchors were checked for existence/range, but the cause validator itself only checks non-emptiness. The retained wave-19 artifacts therefore do not form a fully self-contained, machine-verifiable source bundle for all causes.
- LSP was unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list had no LSP device. These targets are JSON/text artifacts; no caller/definition/diagnostics request could be made, and literal anchor searches were not treated as semantic proof. No builds or tests were run.

## Commands and exit codes

Commands below were run from `.../.ufo/waves/round-19`; every shell command shown returned the listed status.

1. Artifact counts and exact prompt comparison — **exit 0**:

```sh
python3 -c 'import json,os,hashlib,collections; S=json.load(open("wave1-spec.json")); D=json.load(open("wave1-dispatch.json")); R=json.load(open("wave1-registration.json")); G=json.load(open("wave1-registry.json")); O=json.load(open("wave1-outcomes.json")); A=json.load(open("wave1-assignments.json")); I={x["name"]:x for x in S["items"]}; T={x["name"]:x for x in D["taskCall"]["tasks"]}; M=R["members"]; X={x["name"]:x for x in O["seats"]}; F={p[:-3] for p in os.listdir("w1") if p.endswith(".md") and os.path.isfile(os.path.join("w1",p)) and os.path.getsize(os.path.join("w1",p))>0}; miss={n for n,x in X.items() if not x["report_present"]}; print("items/tasks/registration/snapshot/outcomes/assignments",len(I),len(T),len(M),len(G["members"]),len(X),len(A)); print("roles",dict(sorted(collections.Counter(x["role"] for x in I.values()).items()))); print("name_sets_equal",all(set(I)==set(x) for x in [T,M,G["members"],X,A]),"IDs_unique",len({v["agentId"] for v in M.values()}),"assignment_IDs_match",all(M[n]["agentId"]==A[n] for n in M)); print("task_roles_match",all(I[n]["role"]==T[n]["agent"] for n in I),"exact_prompt_matches",sum(I[n]["prompt"]==T[n]["task"] for n in I),"prompt_prefix_matches",sum(T[n]["task"].startswith(I[n]["prompt"]) for n in I),"context_match",S["context"]==D["taskCall"]["context"]); print("reports",len(F),"outcome_report_names_match",F=={n for n,x in X.items() if x["report_present"]},"missing/uncaused/causes",len(miss),len(O["uncaused"]),sum(bool(X[n]["cause"] and X[n]["cause"].strip()) for n in X)); print("cause_classes",dict(collections.Counter("parent-exit" if "killed when the L1 session" in X[n]["cause"] else "provider-429" if "rate_limit_error" in X[n]["cause"] else "other" for n in miss))); print("dispatch_spawn_resume_sends",D["counts"]["spawn"],D["counts"]["resume"],len(D["resumeSends"])); print("hashes_match",hashlib.sha256(open("wave1-registration.json","rb").read()).hexdigest()==O["registration_sha256"],hashlib.sha256(open("evidence/wave-outcomes/w1-causes.json","rb").read()).hexdigest()==O["causes_sha256"]); print("wave_ids",S["wave"],D["wave"],R.get("wave"),O.get("wave"))'
```

Output: 90 entries at each stage; 90 unique IDs; 0 exact prompt matches / 90 prefix matches; 48 reports, 42 missing, 0 uncaused; causes 33 parent-exit / 9 provider-429; spawn 90 / resume 0; both hashes match. **Exit 0.**

2. Non-empty report-file count — **48, exit 0**:

```sh
find w1 -maxdepth 1 -type f -name '*.md' -size +0c -printf '%f\n' | sort | wc -l
```

3. Transcript anchor existence and cause markers — **42 in-range anchors, 33 abort markers, 9 direct-429 markers; exit 0**. The script emitted counts only, not transcript content:

```sh
python3 -c 'import json,re,os,collections; o=json.load(open("wave1-outcomes.json")); c=collections.Counter(); bad=[]
for x in o["seats"]:
 if x["report_present"]: continue
 m=re.search(r"transcript (/.+\.jsonl):(\d+)$",x["cause"] or "")
 if not m: bad.append(x["name"]); continue
 with open(m.group(1),encoding="utf-8",errors="replace") as f: line=next((v for i,v in enumerate(f,1) if i==int(m.group(2))),"")
 raw=x["cause"] or ""
 if "rate_limit_error" in raw: c["reported-429"]+=1; c["source-line-has-429"]+=int("429" in line or "rate_limit_error" in line)
 elif "killed when the L1 session" in raw: c["reported-parent-exit"]+=1; c["source-line-has-abort-marker"]+=int(any(q in line.lower() for q in ["abort","kill","parent","exit"]))
 else: c["other"]+=1
print("cause/provenance counts",dict(c),"bad refs",bad)'
```

4. Launch receipt name/ID binding and recorded task inclusion — **90/90, all pending, zero result records; exit 0**:

```sh
python3 -c 'import ast,json; z=ast.literal_eval(open("wave1-result.txt").read()); p=z["details"]["progress"]; r=json.load(open("wave1-registration.json"))["members"]; d={x["name"]:x["task"] for x in json.load(open("wave1-dispatch.json"))["taskCall"]["tasks"]}; n=lambda x:x["id"].removeprefix("KaidokuR19."); prefix="Complete assignment thoroughly:"+chr(10)*2; print("progress entries",len(p),"identity exact",all(x["id"]==r[n(x)]["agentId"] for x in p)); print("dispatch tasks embedded after wrapper",sum(x["task"].startswith(prefix+d[n(x)]) for x in p)); print("statuses",sorted({x["status"] for x in p}),"result records",len(z["details"]["results"]))'
```

5. Declared registry-path identity check — **90 null agent IDs in the dispatched registry file; exit 0**:

```sh
python3 -c 'import json,collections; d=json.load(open("w1/swarm-registry.json")); m=d["members"]; c=collections.Counter(v.get("agentId") for v in m.values()); print("keys",sorted(d)); print("wave/report",d.get("wave"),d.get("reportDir")); print("agentId values",c); print("sample",[(n,m[n].get("kind"),m[n].get("agentId"),m[n].get("role")) for n in list(m)[:5]]); print("unique roles",dict(collections.Counter(v.get("role") for v in m.values()))); print("all agent IDs null",all(v.get("agentId") is None for v in m.values()))'
```

6. Missing wave-1 names versus the wave-2 roster — **no same-name overlap; exit 0**:

```sh
python3 -c 'import json,collections; a=json.load(open("wave1-spec.json")); o=json.load(open("wave1-outcomes.json")); b=json.load(open("wave2-spec.json")); d=json.load(open("wave2-dispatch.json")); old={x["name"]:x for x in a["items"]}; dead={x["name"]:x for x in o["seats"] if not x["report_present"]}; nxt={x["name"]:x for x in b.get("items",[])}; tasks={x["name"]:x for x in d["taskCall"]["tasks"]}; print("wave2 spec/tasks",len(nxt),len(tasks)); print("name overlap with missing wave1",sorted(set(dead)&set(nxt))); print("same-name exact original prompt",[(n,old[n]["prompt"]==nxt[n].get("prompt"),old[n]["prompt"]==tasks.get(n,{}).get("task")) for n in sorted(set(dead)&set(nxt))]); print("wave2 roles",dict(sorted(collections.Counter(x["role"] for x in nxt.values()).items())))'
```


An exploratory receipt parse keyed the fully-qualified receipt ID as a bare seat name and exited 1 (`KeyError`); I corrected the join by stripping the `KaidokuR19.` prefix, as in command 4. No artifact issue was inferred from that parser error.