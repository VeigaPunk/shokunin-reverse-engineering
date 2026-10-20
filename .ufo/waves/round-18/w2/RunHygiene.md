HOLDS

# RunHygiene: round-18 run leak review (wave 2, falsify)

- Seat: KaidokuR18.RunHygiene (sentinel, author-side advisory)
- REV: b2aad08ceeee8dd125ce0d316056d8bd766c7f94 (lane HEAD at review; `git rev-parse HEAD` exit 0)
- Scope: `.ufo/waves/round-18/runs/**` (248 blobs, 15 labels), `/tmp` residue, receipt env fields
- Read-only. This file is my only write. No installs. No REA, Ghidra or carrier execution.
- Severity: **none**. No leak found. N1–N4 are informational and need no fix for this round.
- LANE below means /home/vgpnk/Projects/shokunin/kaidoku-shokunin, and REV means the full hash above.

## Answers

| Question | Result | Kind |
|---|---|---|
| Was a session.json or bridge token copied under runs/? | **No.** No session/descriptor/ownership JSON exists anywhere in REV's 16,135 blobs. "token" appears 0 times. No 64-hex string sits outside a digest slot. No UUID-format string. | observation |
| Are /tmp/kr17-rea-* dirs left over? | **No.** None of the 15 recorded parents exist, none of the 15 session dirs exist, and no `/tmp/rea-ghidra-*` exists. | observation (state at ~13:45) |
| Do receipts record env (child_env_keys)? | **Keys only.** The same 10 keys appear in all 15 receipts. The only env *value* recorded is `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000`. TMPDIR equals `session_parent`. | observation |

## Attempted exploit paths and why they fail

1. **Descriptor copied into the lane.** The REA bridge token is `randomBytes(32).toString("hex")` (rea-agents 6.5.0 `dist/ghidra/GhidraClient.js:430`). It is written into `<runtime>/session.json` (`GhidraLauncher.js:95-98,447`), mode 0600 inside 0700 dirs (`:509,516`). On POSIX the bridge deletes the file right after reading it (`bridge/ghidra/ReaGhidraBridge.java:196-197`). The lane poller copies only `LOG_NAMES = ("ghidra.log","script.log")`, and only regular non-symlink files (REV `.ufo/waves/round-17/tools/carrier-run.py:42,223-228`).
   - Observed: every receipt's `retained_logs` names are exactly {ghidra.log, script.log}.
   - The 15 `session.json` hits are the Ghidra script-argument *path*, one per bound log, e.g. REV `runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:261`.
2. **Token in logs or stderr.** REA redacts the token from captured stderr (`GhidraLauncher.js:167`). All 45 `*.stderr` blobs at REV are 0 bytes.
   - The token is 64-hex, the same shape as a sha256. Every 64-hex string in runs/ sits in a digest slot (`sha256`, `digest`, `*_sha256`, the `tool_sha256` path map) or an `ev_` id. The residual regex has 0 hits (cmd 8).
3. **Host or agent secrets through env.** The child env is an allowlist plus `TMPDIR` and `NODE_DISABLE_COMPILE_CACHE` (REV `carrier-run.py:271-285`). Receipts store `sorted(child_env)` keys only (`:303,325`). Values are stored only for `REA_GHIDRA_*` (`:326-327`).
   - Observed: REV `runs/real-kimi-webbridge/receipt.json:11-22` lists the keys and `:1887-1889` the single value. All 15 receipts are identical here.
   - No socket or token key reached the child (e.g. PI_TOOL_BRIDGE_TOKEN, SSH_AUTH_SOCK).
   - I took the live values of this seat's secret-like env vars: 8 in the bash env (names withheld) plus PI_TOOL_BRIDGE_TOKEN in the eval env. None occurs in any of the 248 blobs (cmd 11).
4. **Residual session parent.** `mkdtemp(prefix="kr17-rea-", dir="/tmp")` creates the parent (`carrier-run.py:301`). It is removed with `rmdir` only when empty (`:410-417`); otherwise the run exits 2 (`:435-440`).
   - Observed: every receipt has `session_parent_leftovers: []`, `unbound_sessions: []` and `session_dir_baseline: []` (`real-kimi-webbridge/receipt.json:1914-1916,1998`; `s1246-swiss-nethttp/receipt.json:1914-1916,1989`).
   - Every label ends with `carrier-run=0 compare=0` (REV `runs/run-log.txt:3-31`).
   - Now: 0 of 15 parents exist and `ls` exits 2.
5. **Process or HOME residue.**
   - No `java`, `rea-ghidra` or `analyzeHeadless` processes are running.
   - The only REA process is pid 3221 `npm exec rea-agents@6.5.0 mcp`. It started at 09:57:31, before the run window of 13:24:07–13:32:10 (`run-log.txt:2,31`). [INFERENCE: it is the harness MCP server, not residue from the runs.]
   - No REA, Ghidra or npm path under `$HOME` changed during 13:24–13:33. This matches REA moving HOME, TMPDIR, XDG_* and java.io.tmpdir/user.home into its runtime root (`GhidraLauncher.js:518-543`).

Calibration: the token *values* cannot be recovered because the descriptor is deleted and the runtime root removed. The REA-token check therefore relies on the token's format, the absence of the word "token", and the code path; it is not an exact value match. For PI_TOOL_BRIDGE_TOKEN I could only match exact values for this seat's own token. The UUID check (0 hits) covers that format for any seat's token.

## Informational notes (not findings)

- **N1 (latent):** two rules cover any name starting `REA_GHIDRA_`. `carrier-run.py:326-327` records the value of every such parent variable, and `:282` passes any such variable to the child. REA 6.5.0 reads only six of them: COMPILER_SPEC_ID, DISABLED_ANALYZERS, LANGUAGE_ID, NATIVEAOT_JAR, SEED_FILE and STARTUP_TIMEOUT_MS. These are ids, paths and a timeout, not secrets, so nothing leaks today. Smallest hardening: record values only for an explicit name tuple.
- **N2 (TOCTOU):** the check at `:226` is followed by an `open()` at `:228` that follows symlinks. Exploiting it needs same-uid write access inside a 0700 private root, so no boundary is crossed. O_NOFOLLOW would close it.
- **N3 (host fingerprint, not secret):** receipts commit absolute paths, the username, and the real carrier's install path plus md5/sha256 (`real-kimi-webbridge/receipt.json:5-10`). Its `analyze.json` is 5,744 B of counts and segments, with no binary strings.
- **N4:** `/tmp/kr18-runlog.txt` (13:32) is a byte-identical copy of `runs/run-log.txt` (cmp exit 0). It is a harmless operator copy, not a kr17-rea dir.
- **Adjacent, outside my scope:** `~/.zcode/cli/config.json.rea.backup` and `~/.zcode/skills/reverse-engineer-anything/**` have mtime 13:32:28.05. That is 18 s after the last run ended (`run-log.txt:31`). The `*.rea.backup` writers sit in REA's client-configuration modules (SetupHost, SetupClientConfiguration, SetupSkill, Uninstall); `dist/cli-runtime/cli.js:10075-10081` loads SetupHost from `runSetupCommand`. The runs called only `analyze` and `inspect-go-binary` (all 15 receipts). [INFERENCE from timing and code path: these files do not come from the runs.] I did not open the file because it may hold credentials. If a seat ran `rea setup`/`update`/`uninstall`, that changed client routing; route it to the orchestrator.

## Commands (exit codes observed)

```
1  ls -la /tmp/kr17-rea-*                                                    -> exit 2 (No such file)
2  ls -d /tmp/kr17-rea-* /tmp/rea-ghidra-*                                   -> exit 2
3  cd LANE && diff <(find .ufo/waves/round-18/runs -mindepth 1 \( -type f -o -type l \) | sort) \
     <(git --no-optional-locks ls-tree -r --name-only REV -- .ufo/waves/round-18/runs | sort)   -> exit 0
   git --no-optional-locks status --porcelain --ignored --untracked-files=all -- .ufo/waves/round-18/runs -> exit 0, empty
4  git --no-optional-locks -C LANE ls-tree -r --name-only REV | python3 -I -B -c 'import sys,re; n=sys.stdin.read().split(); print(len(n),"blobs in REV;", [x for x in n if re.search(r"(^|/)(session[^/]*|ownership|descriptor[^/]*)\.json$",x)])'
                                                                             -> "16135 blobs in REV; []", exit 0
5  git --no-optional-locks -C LANE grep -a -c 'session\.json' REV -- .ufo/waves/round-18/runs
                                                                             -> 15 lines, each logs/rea-ghidra-*/ghidra.log:1, exit 0
6  git --no-optional-locks -C LANE show REV:.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log | sed -n 261p
                                                                             -> "...ReaGhidraBridge.java '/tmp/kr17-rea-0wd781s_/rea-ghidra-ZSUHpG/session.json'", exit 0
7  git --no-optional-locks -C LANE grep -a -c -i token REV -- .ufo/waves/round-18/runs                -> exit 1 (no match)
8  git --no-optional-locks -C LANE grep -a -c -P '(?<!": ")(?<!":")(?<!ev_)(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])' REV -- .ufo/waves/round-18/runs -> exit 1
9  git --no-optional-locks -C LANE grep -a -c -i -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' REV -- .ufo/waves/round-18/runs -> exit 1
10 git --no-optional-locks -C LANE grep -a -c -i -E 'bearer|authorization|passw(or)?d|api[_-]?key|BEGIN [A-Z ]*PRIVATE KEY|SSH_AUTH_SOCK|DBUS_SESSION_BUS_ADDRESS|/run/user/|ANTHROPIC|OPENAI|GITHUB_TOKEN|NPM_TOKEN|_authToken|\.npmrc|\.netrc|\.ssh/|agent\.db|endpoint_path|run_id|ownership\.json' REV -- .ufo/waves/round-18/runs -> exit 1
11 python3 -I -B -c 'import os,re,subprocess as s;R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94";L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin";ns=s.run(["git","-C",L,"ls-tree","-r","--name-only",R,"--",".ufo/waves/round-18/runs"],capture_output=True,text=True,check=True).stdout.split();bl=[s.run(["git","-C",L,"show",R+":"+n],capture_output=True,check=True).stdout for n in ns];c=[(k,v) for k,v in os.environ.items() if re.search("(?i)token|secret|key|pass|auth|cookie|credential|sock",k) and len(v)>=12];print(len(ns),"blobs;",{k:sum(v.encode() in b for b in bl) for k,v in c})'
                                                                             -> "248 blobs; {<8 names withheld>: 0 each}", exit 0
12 python3 -I -B -c 'import json,os,subprocess as s;R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94";L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin";g=lambda *a:s.run(["git","--no-optional-locks","-C",L,*a],capture_output=True,text=True,check=True).stdout;ns=[n for n in g("ls-tree","-r","--name-only",R,"--",".ufo/waves/round-18/runs").split() if n.endswith("/receipt.json")];rs=[json.loads(g("show",R+":"+n)) for n in ns];print(len(rs),"receipts");print("child_env_keys variants:",{tuple(r["child_env_keys"]) for r in rs});print("rea_ghidra_env variants:",{json.dumps(r["rea_ghidra_env"]) for r in rs});print("leftovers:",{json.dumps(r["session_parent_leftovers"]) for r in rs},"unbound:",{json.dumps(r["unbound_sessions"]) for r in rs},"bound per receipt:",{len(r["bound_sessions"]) for r in rs});print("parents existing now:",[r["session_parent"] for r in rs if os.path.exists(r["session_parent"])]);print("retained file names:",{k for r in rs for e in r["retained_logs"] for k in e["files"]});print("step argv verbs:",{st["argv"][3] for r in rs for st in r["steps"].values()})'
                                                                             -> 15 receipts; 1 key variant (10 keys); {"REA_GHIDRA_STARTUP_TIMEOUT_MS": "900000"}; leftovers {[]}; unbound {[]};
                                                                                bound {1}; parents existing now []; {ghidra.log, script.log}; {inspect-go-binary, analyze}; exit 0
13 git --no-optional-locks -C LANE show REV:.ufo/waves/round-17/tools/carrier-run.py | cat -n | sed -n '42,43p;223,228p;271,285p;301,305p;324,327p;410,417p;435,440p' -> exit 0
14 pgrep -a java -> exit 1;  pgrep -af 'kr17-rea|rea-ghidra|analyzeHeadless' -> exit 1;  ps -o pid,lstart,args -p 3221 -> 09:57:31 start, exit 0
15 find "$HOME" -xdev -maxdepth 5 \( -path "$HOME/Projects" -o -path "$HOME/.omp" -o -path "$HOME/.local/share/Trash" -o -path "$HOME/.cache/mozilla" \) -prune \
     -o -newermt '2026-10-20 13:24:00' ! -newermt '2026-10-20 13:33:00' -printf '%TH:%TM %y %p\n' -> exit 0; no REA/Ghidra/npm paths
16 git --no-optional-locks -C LANE show REV:.ufo/waves/round-18/runs/run-log.txt | cmp - /tmp/kr18-runlog.txt -> exit 0
17 stat -c '%y %s %n' ~/.zcode/cli/config.json.rea.backup               -> 13:32:28.051 963 B, exit 0
18 (REA 6.5.0 at ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents) grep -nE 'tmpdir|TMPDIR|java\.io\.tmpdir|user\.home|token|0o6|0o7|session\.json' dist/ghidra/GhidraLauncher.js -> exit 0;
   grep -nE 'deleteIfExists\(descriptorPath\)' bridge/ghidra/ReaGhidraBridge.java -> 197, exit 0;  grep -rhoE 'REA_GHIDRA_[A-Z0-9_]+' dist | sort | uniq -c -> 6 names, exit 0
```

Cmd 11 prints only env names and counts, never values; the names are withheld from this file. Every git command is read-only against REV objects.
