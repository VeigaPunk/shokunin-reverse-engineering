# CriticGuardSufficiency — is clearing exec bits (D3) enforcement or theatre?

Seat: KaidokuR20.CriticGuardSufficiency-2 (read-only; no Go binary executed; no REA/Ghidra; no git writes; no installs).
Verdict up front: **enforcement for exactly one channel — non-root direct `execve` of the armed inodes — and theatre (undetectable) for every execution channel that leaves the guarded inode untouched.** The `check` side is currently **armed-but-never-checked**, and the draft QUALITY row under-declares the bypass classes.

## 1. What is actually enforced (OBSERVATION)

- `manual-arm.json` records 20 carriers (`bin/go`, `bin/gofmt`, 18 `pkg/tool/linux_amd64/*`), each `mode_before 0o755 → mode_after 0o644`, committed in `d1d981d` ("carrier exec bits cleared"; `git log --format='%H %cI %s' -1 -- <file>` → `d1d981d2… 2026-10-20T17:43:06-03:00`, exit 0).
- Live re-verification: `stat -c '%a'` on all 20 paths → `644` (exit 0); `os.access(p, os.X_OK)` → `False` for all 20 (command in §5, exit 0). `exec_probe` (`manual-arm.json:166-170`) records `PermissionError`/errno 13 on `bin/go` — consistent with my stat, but it is a self-reported probe covering 1 of 20 paths, not an independent measurement.
- Coverage of the ELF surface is complete: my own walk found 73 ELFs under `go-1.24.6`; all non-manifest ones are `testdata`/`*.syso` objects — corroborating `ScoutGo1246Carriers.md:20-24` (`carriers=20 extra_elf=53`, none executable). Direct `execve` refusal confirmed on a non-Go fixture: `cp /usr/bin/true t644; chmod 644 t644; ./t644` → `Permission denied`, exit 126.
- So: the round-19 violation class (mistake row 5, `corpus/lessons/round-19.md:90` — an honest `bin/go version` invocation) is genuinely blocked. As a tripwire/accident guard it works.

## 2. Bypasses — execution channels that leave `check` green (OBSERVATION unless marked)

All demonstrated this session on a `/usr/bin/true` fixture in a `mkdtemp` dir (never on a Go carrier), all leaving the armed inode's mode/ctime/content untouched:

| # | channel | command | exit |
|---|---|---|---|
| B1 | copy+chmod+exec (same-owner read ⇒ copy ⇒ run) | `cp t644 t755 && chmod 755 t755 && ./t755` | 0 |
| B2 | loader-mapped exec (declared limit, contract.md:51-52) | `/lib64/ld-linux-x86-64.so.2 ./t644` | 0 |
| B3 | memfd+fexecve on copied bytes | `os.memfd_create` + `os.execve(fd,…)` (Python snippet, §5) | child exit 0 |
| B4 | unprivileged userns bind-mount of an executable copy **at the guarded path itself** | `unshare -rm sh -c 'mount --bind $PWD/x755 $PWD/t644 && $PWD/t644'` | inner 0 |
| B5 | sibling installs (contract also bans them) | `stat` → `go-1.25.0/bin/go`, `go-1.27.3/bin/go` still `0755`, `X_OK=True` | — |

Notes: `fexecve` on the armed inode itself fails (`PermissionError(13)` — exec-bit check is per-inode, so an open fd is not a bypass). `findmnt -T /home/vgpnk/.local/opt/go-1.24.6` → `rw,noatime` (exit 0); `/tmp` (xfs) and `/dev/shm` (tmpfs) are **not** `noexec`, so B1/B3/B4 run anywhere the seat can write. `unshare -rm` worked empirically; `user.max_user_namespaces=122865`. `[INFERENCE]` B4 means even "the exact guarded path was executed" cannot be inferred from a failed direct exec: a seat can run `go` at its real path inside a private mount ns while `check` stays green. `[INFERENCE]` `noatime` removes even the weak atime tripwire — a loader-mapped run is byte-identical to a permitted `readelf` read.

## 3. False greens of `check` (contract.md:46-52 semantics; implementation absent at review)

The tool is not yet landed (`git ls-tree -r 14f0260 --name-only | grep carrier` → none under `tools/`; `ls .ufo/waves/round-20/tools/` → ENOENT, exit 2). Per the contract spec plus `gen-wave1.py:267-269` (runner runs `check` before each label):

- **FG1 (structural): any channel that does not mutate the armed inode.** B1–B5 above. `check` verifies "modes still exec-free, ctime and content unchanged" — true while the seat ran `go version` via `ld-linux` on the real file a minute earlier. Green ⇒ at most "inode state preserved", never "not executed".
- **FG2 (provenance): `check` re-baselines whatever record you hand it.** The interface takes `--record DIR` with no binding to the committed `manual-arm.json`. A seat can `chmod +x` a carrier, run it, `chmod` back, `arm --record <own-tmp-dir>` (fresh ctime_ns baseline), then `check` green. Detectable only if a *separate* gate pins the record dir to the committed lane path and the committed bytes — `gen-wave1.py:69-71` does require a check record at REV "whose carrier set equals predictions/carriers.tsv", which constrains the *integrated* evidence but not records produced mid-wave outside the lane. `[INFERENCE]` for the mid-wave case.
- **FG3 (green-by-absence): no check has ever run.** `ls .ufo/waves/round-20/evidence/carrier-guard/` → `manual-arm.json` only (exit 0). A state where arm exists and no `check-*.json` exists is currently the whole deployment — matching `DraftQualityRows.md:17`'s "arm without check is not evidence of non-execution". D3's substance criterion (`gen-wave1.py:70-71`) demands `arm.json` + ≥1 exit-0 check record, so today's state fails it; `adopt --from manual-arm.json` (gen-wave1.py:107) converts naming but does not run a check.
- **FG4 (TOCTOU): check→launch is not atomic.** The runner checks *before each label* (`gen-wave1.py:267-269`); anything between check and exec — including a same-owner `chmod` — is invisible. SentinelCarrierGuard.md:9 covers this; I confirm independently.
- **FG5 (manifest completeness):** `check` verifies only manifest rows. The manifest covers the 20 go-1.24.6 ELFs; it does not cover `go-1.25.0`/`go-1.27.3`, which the contract *policy* also bans (contract.md:90) — a guard green is silent on the policy's full forbidden set.
- **FG6 (record authenticity):** `manual-arm.json` is plain JSON; carrier SHA-256 authenticates the carrier, not the record or who probed (SentinelCarrierGuard.md:11). Its integrity today derives solely from being git-tracked + `git status` clean — a seat writing it violates a convention, not a filesystem boundary. `[INFERENCE]` detection depends on integration-time git diffs, i.e., post-hoc.
- **FG7 (small):** `exec_probe` probes 1/20 paths (observation, §1); a record showing 19 armed files is a weaker claim than the probe suggests.
- **FG8 (small, spec-level):** nothing in the declared interface makes `check` fail-closed on a vanished carrier or a manifest row pointing at a symlink — the implementation review can't confirm until the tool lands. `[INFERENCE]`

## 4. What enforcement would actually be, and what wording is safe

Real prevention needs an OS boundary the lane hasn't used: `noexec` mount on the carrier dir, a seat sandbox without exec/write rights to the install (the D6b revexec sandbox *could* mount carriers read-only/noexec — that would close B1–B4 for revexec'd tools only), or removal of read permission. Cleared exec bits + same-owner UID + write access + unprivileged userns cannot reach that.

The draft QUALITY row (`DraftQualityRows.md:26`, row 24) has the right skeleton — record `arm`+`check`+`disarm`, declare limits, "instructed, not enforced" without a record, "arm without a check is not evidence of non-execution". Two fixes needed so it does not overclaim:

1. **Bypass list "at minimum loader-mapped execution and root" is materially incomplete.** The admitted row must enumerate at least: executing a copied/memfd-carried image; unprivileged userns bind-mount over the guarded path (exec at the real pathname); same-owner chmod between check instants; executables outside the manifest set (sibling installs 1.25.0/1.27.3); and record provenance — green attests only the record dir presented, so the row should require the check record to name the committed arm record it verified (path + sha256), not a caller-supplied DIR.
2. **Define "enforced" as a narrow predicate, never as "execution prevented".** Safe form: "direct `execve` of the manifest paths is refused (EACCES) for non-root processes; a `check` exit 0 attests inode state at the check instant only and is consistent with execution via every non-inode channel." Any knowledge/QUALITY phrasing of the form "carrier execution is enforced/blocked/prevented/impossible" is an overclaim and fails the contract's own declared limit.

Suggested row text (minimal, admitting only what is demonstrated): "A no-execution contract is stated as *tripwire-enforced for direct execve of the manifest paths* only when (a) exec bits are cleared and the armed set is re-verified exec-free (e.g. `access(X_OK)` per path), (b) a retained `check` record (exit code) names the committed arm record it verifies, and (c) the record declares its bypass classes: loader-mapped exec (`ld-linux …`), copy/memfd-of-bytes exec, userns bind-mount over the path, same-owner chmod between check instants, out-of-manifest executables, and root. A green check is attested state at one instant, never non-execution. Absent (a)+(b) the contract is 'instructed, not enforced'."

## 5. Commands run (exit codes)

- `ls -la /home/vgpnk/.local/opt/go-1.24.6/{bin,pkg/tool/linux_amd64}; stat -c '%a %U %s %n' …/bin/*` → exit 0 (20 files 644).
- `stat -c '%a %n' go-*/bin/*` → exit 0 (1.25.0, 1.27.3 still 755); `findmnt -T …` → exit 0 (`rw,noatime`, no `noexec`); `findmnt /tmp /dev/shm` + `/proc/mounts` → exit 0.
- `find go-1.24.6 -type f -perm /111` → exit 0, 42 hits, all scripts/testdata (wasm exec helpers, `src/*.bash`, `mk*.pl`); Python ELF walk → 73 ELFs, manifest-complete.
- Fixture bypass demo in `mkdtemp` (commands verbatim in §2): `./t644` exit 126 EACCES; ld-linux exit 0; copy+chmod exit 0; memfd child exit 0; fexecve-on-644 `PermissionError(13)`; `unshare -rm` bind-mount exec exit 0.
- `os.access(X_OK)` over all 20 manifest paths → all False, exit 0.
- `git --no-optional-locks log -1 --format='%H %cI %s' -- …/manual-arm.json` → `d1d981d2…` exit 0; `git status --porcelain` on the evidence dir → clean.
- Reads: contract.md:46-52,88-92; gen-wave1.py:69-71,105-108,267-269; QUALITY.md admission rows; round-19.md:90; SentinelCarrierGuard.md; DraftQualityRows.md:12-29; ScoutGo1246Carriers.md:9-24.

Impacted axes: calibration (what the "D3 closed" claim may assert), coverage (the bypass/FG classes the row must enumerate), depth (B4 userns mount + record re-baseline are the non-obvious holes).
Report: .ufo/waves/round-20/w1/CriticGuardSufficiency.md
