# SC2 (scout) — round-4 read-only config pin corroboration: pre-pair receipt 5/5, pin unchanged, churn bounded, PE wall OOM-killed

Wave arc2-loop1-round4 · Seat SC2 · 2026-10-18 · read-only corroboration (only write: this report). Versions, key names, line numbers and hashes only — no secret values printed anywhere.

## Verdict

**CONFIRMED — the round-4 pre-pair receipt (`.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt`, `2026-10-18T19:03:02Z`, 6-line/5-path, self-hash `231edd7d…`) verifies 5/5 (`sha256sum -c` rc=0), and its five payload lines are byte-identical to the round-3 post-pair receipt (18:57:18Z, self-hash `a023e3b0…`), so the custody bracket closed clean. The current rea pin is unchanged: Kimi `rea-agents@6.7.0` at `/home/vgpnk/.kimi-code/config.toml:3298` with stanza anchor `[mcp_servers.rea]` at `:3296` (env table `:3301`), Devin `rea-agents@6.5.0` at `/home/vgpnk/.config/devin/mcp_config.json:7`, OMP `rea-agents@6.5.0` at `/home/vgpnk/.omp/agent/mcp.json:8`.** Since 17:55Z exactly one custody-path churn episode occurred — the already-recorded mutate-revert of config.toml (backup born 18:01:33Z, rewrite 18:01:40Z, `cp -p` restore 18:02:33Z, ctime witness survives) — and the file has been byte-stable at `bd5a78d1…` through four captures spanning 19:05:22Z→19:08:37Z. Two non-custody directory touches landed after the receipt (npx cache dirs, mtime-only). **Separately: the round-4 PE wall infrastructure died — OOM-kill at 19:07:45Z (exit=1); see §7.**

## Evidence — exact commands run this session with observed output

Capture stamps (`date -u`): `19:04:34Z`, `19:05:22Z`, `19:06:03Z`, `19:06:22Z`, `19:06:47Z`, `19:07:05Z`, `19:07:58Z`, `19:08:37Z`.

### 1. Round-4 pre-pair receipt — shape and integrity

```
$ R=.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
$ wc -l < $R  → 6 ;  grep -cE '^[0-9a-f]{64}  /' → 5 ;  grep -cE '^[0-9]{4}-…Z$' → 1
$ tail -n +2 $R | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum $R
231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62
```
**5/5 verified before my leg** (receipt is the round-2/3 6-line 5-path form; mtime `2026-10-18 16:03:02.799 -0300` = 19:03:02Z).

### 2. Receipt lineage — round-3 post-pair vs round-4 pre-pair

```
$ diff <(tail -n +2 …round3/receipts/config-post-pair.txt) <(tail -n +2 …round4/receipts/config-pre-pair.txt)
IDENTICAL payloads (5/5)
$ sha256sum .ufo/waves/arc2-loop1-round3/receipts/{config-pre-pair,config-post-pair}.txt
3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553   (r3 pre-pair, 17:55:49Z)
a023e3b0b5b623d1373e9af9efe31690311e2019cb1ebac9c49130baaf569606   (r3 post-pair, 18:57:18Z)
$ tail -n +2 …round3/receipts/config-post-pair.txt | sha256sum -c -  → 5× OK, rc=0
```
The four intervening hours produced **zero net change on all five custody paths** — the round-3 in-window excursion (§4) was fully reverted before the post-pair capture.

### 3. Pin census (three clients) — values unchanged

```
$ grep -n 'rea-agents' /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml
/home/vgpnk/.config/devin/mcp_config.json:7:        "rea-agents@6.5.0",
/home/vgpnk/.omp/agent/mcp.json:8:        "rea-agents@6.5.0",
/home/vgpnk/.kimi-code/config.toml:3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ grep -n 'rea-agents\|mcp_servers\.rea' /home/vgpnk/.kimi-code/config.toml
3296:[mcp_servers.rea]
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
3301:[mcp_servers.rea.env]
$ grep -nE '(^|[^a-z])rea([^a-z]|$)' /home/vgpnk/.kimi-code/config.toml | grep -v reasoning
3296:[mcp_servers.rea]
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
3301:[mcp_servers.rea.env]
```
Word-boundary sweep returns **only** the same three lines — the file's entire `rea` footprint is the one MCP table (3322 lines total). Neighborhood (key names only; values redacted): `:3297 command`, `:3298 args`, `:3299 startup_timeout_sec`, `:3302 GHIDRA_INSTALL_DIR`, `:3303 JAVA_HOME`. Bonus: `~/.grok/config.toml:30` still `"rea-agents@6.5.0"`; `~/.codex/config.toml` has 0 `rea-agents` matches.

### 4. Churn events since 17:55Z, with timestamps

**(a) config.toml mutate-revert — the only custody-path churn (already recorded by round 3):**

```
$ stat -c 'birth=%w  mtime=%y  ino=%i  size=%s  %n' /home/vgpnk/.kimi-code/config.toml.20261018-150133.bak
birth=2026-10-18 15:01:33.132180403 -0300  mtime=2026-10-18 14:50:34.896343019 -0300  ino=30149532  size=107496  config.toml.20261018-150133.bak
$ cmp /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.kimi-code/config.toml.20261018-150133.bak ; echo rc=$?
rc=0
$ stat -c 'mtime=%y ctime=%z ino=%i %n' config.toml
mtime=2026-10-18 14:50:34.896343019 -0300  ctime=2026-10-18 15:02:33.462921932 -0300  ino=29670088  config.toml
```
Timeline (UTC): **18:01:33.132Z** backup born (a *new* artifact vs round-3's SC2 report, which listed 5 config states; this is the 6th) → **18:01:40.77Z** rewrite to `9ac8023b…` (108208 B, 3336 lines, stanza transiently `:3310`) → **18:02:33.46Z** restore via `cp -p` (mtime+inode restored; ctime survives at 15:02:33.462 -0300). Verbatim in `.ufo/waves/arc2-loop1-round3/receipts/drift-config-toml-mutate-revert-20261018T180140Z.txt`, `LOG.md:1105-1110`, and `E19.md:131` (the 108208-byte transient). Zero churn on this path after 18:02:33Z.

**(b) Non-custody directory touches after the round-4 receipt (mtime-only, no file content changed):**

```
$ ls -la --time-style=full-iso /home/vgpnk/.npm/_npx/
drwxr-xr-x … 2026-10-18 16:05:46.066941075 -0300 a1722018f28f9df2   (6.7.0 cache dir; 19:05:46Z)
drwxr-xr-x … 2026-10-18 16:03:03.048298571 -0300 ad9a3fdbcad992c6   (6.5.0 cache dir; 19:03:03Z)
$ find …/a1722018f28f9df2 -newermt '2026-10-18T19:05:00Z' → only the dir itself
$ for e in …/a1722018f28f9df2/*; do stat …; done
ctime=mtime=2026-10-18 08:24:02 -0300  node_modules / package.json / package-lock.json
```
The 6.5.0 dir touch at 19:03:03Z is the PE launch resolving its cache (`/tmp/arc2-l4r4-pe-launch.sh` runs `npx -y rea-agents@6.5.0`); the 6.7.0 touch at 19:05:46Z has no corresponding live process in `ps` and changed no file inside. Both are npx dir-metadata events, not pin drift. Neither path is a custody path.

**(c) Repo churn:** `git log --since=2026-10-18T17:55:00Z` → three commits, all round-3 (`fd30b9c` 18:59:25Z, `dbba2dd` 18:59:48Z, `158a966` 19:01:13Z), HEAD still `158a966`. Working tree: `?? .ufo/waves/arc2-loop1-round4/` and `?? e16-table.json` (an untracked 8206-byte seat artifact born 19:05:44Z — **not mine**; I only read its head to identify it).

**(d) `~/.kimi-code` session churn since 19:03Z:** the 64-seat wave's own wire logs/agent task dirs under `sessions/wd_shokunin_…/agents/agent-*/` (expected), plus `credentials/kimi-code-env-0e4f99c69cc27850.json` at 19:03:45Z (client auth-refresh event; **not read — name/mtime only**).

### 5. Pin-line and stanza byte-identity across all six known config states

```
$ for f in *.085645.bak *.114557.bak *.143236.bak *.145016.bak *.150133.bak config.toml; do printf '%s  ' "$(grep -h 'rea-agents' $f | sha256sum | cut -c1-16)"; done
eb1c7da74fc5f870  ×6   (one rea-agents line each)
$ for f in …; do sed -n '/\[mcp_servers.rea\]/,/^$/p' "$f" | sha256sum | cut -c1-16; done
3751281c2a379b04  ×6
```
Pin line numbers and file lengths: `:2915` (2939) → `:2932` (2956) → `:2940` (2964) → `:3227` (3251) → `:3298` (3322) → `:3298` (3322). Stanza anchors: `:2913/:2918` → `:2930/:2935` → `:2938/:2943` → `:3225/:3230` → `:3296/:3301` → `:3296/:3301`. **The stanza's content digest is identical in all six states**, which is exactly the round-3 E22 fence's recipe (`.ufo/waves/arc2-loop1-round3/E22.md` tail block) reproducing `3751281c2a379b04` as documented.

### 6. Live drift re-check inside this leg (four captures)

```
19:05:22Z  bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  config.toml
19:06:03Z  bd5a78d1…  (all five paths captured; 5/5 match the round-4 receipt)
19:06:22Z  bd5a78d1…
19:06:47Z  bd5a78d1…
19:07:05Z  bd5a78d1…  (5/5 match)
19:07:58Z  bd5a78d1…
19:08:37Z  bd5a78d1…  (leg close)
```
Devin/omp mtimes remain `2026-10-14 17:53:20 -0300` with ctime identical (no churn possible); `.bashrc` mtime `2026-10-16 13:33:16`, `.profile` `2026-10-15 03:12:07`, both with matching ctime.

### 7. ROUND INFRASTRUCTURE EVENT — PE wall OOM-killed at 19:07:45Z (observed, not touched)

```
$ systemctl --user status run-p4175743-i29293759.scope
× arc2-pe-wall
     Active: failed (Result: oom-kill) since Sun 2026-10-18 16:07:45 -03
   Duration: 4min 42.282s
     Mem peak: 7G (swap: 1G)
        CPU: 9min 2.497s
Oct 18 16:07:45 …: The kernel OOM killer killed some processes in this unit.
Oct 18 16:07:45 …: Failed with result 'oom-kill'.

$ journalctl -k --since '19:07:00Z'
… oom-kill:constraint=CONSTRAINT_MEMCG, oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.s…
… Memory cgroup out of memory: Killed process 4181543 (java) total-vm:10168632kB, anon-rss:3353140kB …
   (Ghidra decompile worker threads, 200 each, ~80–116MB × N)

$ cat /var/tmp/arc2-l4r4-pe/exit.txt
exit=1 wall_utc=2026-10-18T19:07:45Z
$ ls /var/tmp/arc2-l4r4-pe/rea-ghidra-1Uwcai/ → No such file or directory  (runtime_root cleaned up)
$ head -c 1200 /var/tmp/arc2-l4r4-pe/stdout.json
error: Analysis failed / code: cancelled / message: Analysis was cancelled…
   operation: list_documents | cleanup: complete | provider_version: 12.1.4
   run_id: 4cd20f34-c1de-4b2b-87c2-a4726302ee4b
   target_sha256: 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
   failure_kind: cancelled / failure_message: Ghidra startup was cancelled
   (stdout tail shows Ghidra decompile WARN spam — "Unable to resolve constructor … (DecompileCallback)" —
    immediately before the kill; 20093 B total; not valid JSON, it is REA's error renderer output)
```
Observed, no action taken: I did not kill, renice, restart, or modify anything; I only ran `systemctl --user status/show`, `journalctl -k`, `ps`, and `cat`/`head` on the run dir. The scope is now `failed` and the java/node/npm processes are gone; `/var/tmp/arc2-l4r4-pe/` retains `stdout.json`, `exit.txt`, empty `stderr.log`, and `node-compile-cache`. Memory cap was `MemoryMax=7516192768` (7G, confirmed via `systemctl --user show … -p MemoryMax`), and the peak hit it exactly — i.e. the wall was the containment cap, and Ghidra's decompile phase outgrew it.

## Text for parent to land VERBATIM

```text
REA pin corroboration, round 4 (read-only, SC2 scout, 2026-10-18): round-4 pre-pair receipt (.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt, 2026-10-18T19:03:02Z, 501 B, self-hash 231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62) verified 6/5/1 shape, 5x sha256sum -c OK, rc=0 — 5/5 before the leg; zero drift during it (four captures 19:05:22Z-19:08:37Z, all bd5a78d1…). Its five payload lines are byte-identical to the round-3 post-pair receipt (18:57:18Z, self-hash a023e3b0b5b623d1373e9af9efe31690311e2019cb1ebac9c49130baaf569606, 5x OK) — the round-3 in-window excursion was fully reverted before bracket end. Pin values UNCHANGED: Devin rea-agents@6.5.0 (/home/vgpnk/.config/devin/mcp_config.json:7, 16f496e6…), OMP rea-agents@6.5.0 (/home/vgpnk/.omp/agent/mcp.json:8, 38d2a1d0…), Kimi rea-agents@6.7.0 at /home/vgpnk/.kimi-code/config.toml:3298 (file 3322 lines, sha256 bd5a78d1…; stanza [mcp_servers.rea] :3296, env :3301; word-boundary sweep shows the file's whole rea footprint is these 3 lines). CHURN SINCE 17:55Z, with timestamps: (1) the single custody-path event is the already-recorded config.toml mutate-revert — backup config.toml.20261018-150133.bak born 18:01:33.132Z (ino 30149532, byte-identical to live, cmp rc=0), rewrite 18:01:40.77Z to 9ac8023b… (108208 B, 3336 lines, stanza transiently :3310), cp -p restore 18:02:33.46Z (mtime 14:50:34.896 -0300 + ino 29670088 restored; ctime 15:02:33.462 -0300 survives); verbatim in arc2-loop1-round3/receipts/drift-config-toml-mutate-revert-20261018T180140Z.txt and LOG.md:1105-1110; (2) two non-custody npx cache DIR mtime touches after the receipt — /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6 (6.5.0, 19:03:03Z = the PE launch's cache resolution) and /home/vgpnk/.npm/_npx/a1722018f28f9df2 (6.7.0, 19:05:46Z, no live process, no file inside changed); (3) repo: three round-3 commits (fd30b9c 18:59:25Z, dbba2dd 18:59:48Z, 158a966 19:01:13Z), HEAD 158a966 unchanged, untracked ?? e16-table.json (8206 B, born 19:05:44Z, not SC2's) + ?? .ufo/waves/arc2-loop1-round4/; (4) ~/.kimi-code: wave session wire logs + credentials/kimi-code-env-0e4f99c69cc27850.json touched 19:03:45Z (auth refresh; name/mtime only, never read). Stanza-content digest (sed -n '/\[mcp_servers.rea\]/,/^$/p' | sha256sum) is 3751281c2a379b04… IDENTICAL across all six known config states (5 backups + live) — the E22 fence recipe reproduces. Pin line numbers :2915 -> :2932 -> :2940 -> :3227 -> :3298 -> :3298 (file 2939/2956/2964/3251/3322/3322). ROUND INFRASTRUCTURE: the contained 91.6MB PE analyze (scope arc2-pe-wall) was OOM-KILLED at 2026-10-18T19:07:45Z — systemd result 'oom-kill', mem peak 7G (swap 1G) against MemoryMax=7G, kernel cgroup OOM killed java pid 4181543 (anon-rss 3353140kB) during Ghidra decompile; exit.txt "exit=1 wall_utc=2026-10-18T19:07:45Z", stdout.json = REA "Analysis failed / cancelled" envelope (run_id 4cd20f34-c1de-4b2b-87c2-a4726302ee4b, target_sha256 7a2ccd688f6c…), runtime_root cleaned. SC2 took NO action on it (observation only: status/journalctl/ps/cat).
```

## Conclusions by label

- **Observation** — (a) round-4 pre-pair receipt 6/5/1, 5× OK rc=0, self-hash `231edd7d…`, timestamp `2026-10-18T19:03:02Z`, mtime 19:03:02.799Z; (b) its payload is byte-identical to round-3's post-pair (5/5); (c) Kimi pin `rea-agents@6.7.0` at live `config.toml:3298`, the file's only rea occurrence, stanza `:3296`, env `:3301`, file 3322 lines, sha `bd5a78d1…`; (d) Devin/OMP `6.5.0` at `:7`/`:8`, both files mtime+ctime `2026-10-14 17:53:20`; (e) the pin line and the whole `[mcp_servers.rea]` stanza block are byte-identical across all six known config states (`eb1c7da7…`, `3751281c2a379b04…`), line numbers `:2915→:2932→:2940→:3227→:3298`; (f) live hash re-checked 4× inside the leg (19:05:22Z–19:08:37Z), identical each time; (g) the only custody-path churn in the window is the 18:01:33Z→18:02:33Z mutate-revert, whose ctime witness (15:02:33.462 -0300) is present on the live file; (h) two npx cache dir touches at 19:03:03Z / 19:05:46Z with no inner-file changes; (i) PE scope `arc2-pe-wall` failed with `Result: oom-kill` at 19:07:45Z, Mem peak 7G, kernel CONSTRAINT_MEMCG kill of java 4181543, `exit=1`; (j) `SCORECARD.md:698` still carries `config.toml:2940` as a live-pin pointer (line reads `capabilities = [ "thinking", "tool_use" ]` today) while `PROVINCE.md:18` carries the receipt-scoped `:3298` form.
- **Inference** — The round-4 pre-pair correctly re-baselines the post-revert state, so this round's custody bracket starts clean; the receipt-pair equality (r3-post == r4-pre) means the intervening 6 minutes introduced no change at all. The 6.7.0 npx dir touch with no live process is consistent with npx metadata/cache bookkeeping (e.g. a `npx` version-check or lock refresh from one of the 64 seats) rather than a reinstall — no file inside changed, and the 6.7.0 pin's package identity was already established. The PE OOM is consistent with the Ghidra decompile phase exceeding the 7G containment cap (the round-3 `91.6MB cancelled envelope` precedent): the wall as configured cannot complete this target's decompile, so a future attempt needs either a higher cap (operator decision) or a narrower operation (`list_documents` alone, which is what the error envelope shows as the active operation). `PROVINCE.md:18`'s receipt-scoped wording survives this window's churn intact; `SCORECARD.md:698`'s bare `:2940` remains a live-scope dead pointer (it is explicitly labeled "SC2-refuted", so it may be intentional history — the parent should decide; it is *not* one of the C1 loci named in the round declaration).
- **Unknown** — (a) whether any config rewrite lands between this leg's close (19:08:37Z) and the round-4 post-pair capture (cadence today was ~2/hour before 18:00Z, then zero for 66 minutes — cannot extrapolate); (b) what triggered the 19:05:46Z 6.7.0 npx dir touch (no process observed at 19:07Z); (c) whether the parent re-runs the PE wall with a different cap or operation (out of my scope — I only report the OOM); (d) whether the Kimi client actually *loads* the config.toml pin at runtime (configured ≠ held — unchanged standing question); (e) whether `SCORECARD.md:698`'s `:2940` will be treated as a stale pointer or intentional history this round.

## Scope compliance

Read-only on every repo and home file except this report. No repo file edited; no git mutations (no commit/checkout/reset; `git log`/`status`/`rev-parse`/`reflog` only); no config edits; no installs; no network commands; no secret values read or emitted (only versions, key names, line numbers, hashes; neighborhood printed with `sed -E 's/=(.*)$/= <redacted>/'`). The OOM'd PE process was **not** touched — observation only (`systemctl --user status/show`, `journalctl -k`, `ps`, `cat`/`head` on its output files, `ls` on its run dir); I did not kill, renice, restart, or modify it or its scope. I read the *name and mtime* of `credentials/kimi-code-env-…json` but never its contents. Scratch: none — no `/tmp/arc2-l4r4-SC2-*` files created or left (`ls -d /tmp/arc2-l4r4-SC2*` → no such file). Threats: all observations are point-in-time; the "no inner-file change" claim for the npx dirs rests on `find -newermt` mtime/ctime scans, not content hashing of the cache trees; `e16-table.json` was identified by its first ~300 bytes only (a seat artifact, not mine).
