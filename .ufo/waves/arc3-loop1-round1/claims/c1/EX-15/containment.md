# EX-15 — containment corroboration (chain c1, role executor)

Wave: arc3-loop1-round1 | Repo HEAD at capture: `e845c2b524ad2e59871e004c51a1386e192a74ab`
Host: plazir27 | user: vgpnk | kernel: Linux 7.2.3-arch1-3 | boot: 2026-10-19 00:34:33 -03
Wave window used throughout: **2026-10-19 06:49:00 -03 → capture time** (wave dir created 06:49;
`claims-frozen.md` written 06:52).

Scope of this artifact: the three requested containment checks —
(a) no writes under any custody path, (b) no stray processes/fds from probe runs,
(c) journalctl for OOM/containment events in the wave window — plus two leaks found
while running them. All checks below were actually executed; commands and outputs are cited.

---

## 1. Verdict summary

| # | Check | Verdict |
|---|-------|---------|
| a | Custody writes (5 paths) | **CLEAN** — zero drift across T0→T1, corroborated by CU-1 |
| b | Stray processes / fds from probes | **CLEAN** — no leftover probe procs, no custody fds, no new zombies |
| c | OOM / kill / cgroup events | **NONE** — no OOM, no process kills, no cgroup containment events |
| c' | *Containment mechanism* events | **FOUND** — per-UID 12.1G tmpfs quota on `/tmp` is saturated (see §4) |
| + | Repo writes outside authorized paths | **LEAK, RECURRING** — created 06:58:37, removed 07:03 by EX-26, **recreated 07:04:16, live at close** (see §5) |
| + | `/tmp` scratch integrity wave-wide | **DEGRADED** — 147 zero-byte files in window (see §4.4) |

Net: custody and process containment held. The wave's *scratch* surface did not.

---

## 2. (a) Custody — no writes under any custody path

### 2.1 Captures taken

- `custody-T0.txt` — captured 2026-10-19T06:58:40-03 (this seat)
- `custody-T1.txt` — captured 2026-10-19T07:01:16-03 (this seat, closure)
- `custody-crosswave-diff.txt` — cross-wave comparison vs the arc2 pre-pair receipt
- Independent third-party capture: `claims/cross/receipts/config-pre-pair.txt` (SEAT CU-1,
  2026-10-19T09:57:18Z = 06:57:18 -03) and its `config-pre-pair-metadata.txt` (06:57:48)

### 2.2 T0 vs T1 — byte-identical on all 5 paths

| Path | sha256 (T0 = T1 = CU-1) | mtime | ctime | size |
|---|---|---|---|---|
| `~/.config/devin/mcp_config.json` | `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4` | 2026-10-14 17:53:20 | 2026-10-14 17:53:20 | 406 |
| `~/.omp/agent/mcp.json` | `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b` | 2026-10-14 17:53:20 | 2026-10-14 17:53:20 | 429 |
| `~/.kimi-code/config.toml` | `8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d` | 2026-10-18 23:20:43 | 2026-10-18 23:20:43 | 114434 |
| `~/.bashrc` | `7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598` | 2026-10-16 13:33:16 | 2026-10-16 13:33:16 | 3601 |
| `~/.profile` | `6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30` | 2026-10-15 03:12:07 | 2026-10-15 03:12:07 | 736 |

Three independent captures agree on all five hashes. No `mtime`/`ctime` advanced anywhere.

### 2.3 Filesystem-level argument (stronger than a capture pair)

Every custody path's **mtime and ctime predate the wave window**:

- latest custody mtime = `~/.kimi-code/config.toml` @ **2026-10-18 23:20:43**, i.e. **~7.5 h before**
  the wave window opened at 2026-10-19 06:49:00. The remaining four predate by 2.5–4.5 days.

Since `mtime` cannot move without a write and `ctime` moves on any metadata change
(chmod/chown/link), a write to any custody path during the window would be visible in the
T1 capture. None is. Verdict: **no writes under any custody path in the wave window.**

### 2.4 Cross-wave delta (context, not a violation)

`custody-crosswave-diff.txt` compares against the arc2-loop1-round1 pre-pair receipt
(2026-10-18T14:49:13Z):

- `devin/mcp_config.json` → **IDENTICAL** to the arc2 capture
- `omp/agent/mcp.json` → **IDENTICAL** to the arc2 capture
- `kimi-code/config.toml` → **CHANGED** (`3546e033…` → `8cbacd48…`)

The `config.toml` change is **pre-wave, not wave-induced**: its ctime/mtime is
2026-10-18 23:20:43, which is after the arc2 capture (2026-10-18 11:49 -03) but ~7.5 h
*before* this wave's window. The frozen C1 prediction "no config.toml drift" is a
statement about the wave window and is not falsified. Recorded so the parent does not
mistake the cross-wave delta for a containment failure.

### 2.5 Open-file-descriptor scan

Scanned `/proc/<pid>/fd/*` for every live process, matching against all 5 custody paths
(and the repo root). Result: **no process holds any custody path open** (empty output).
No deleted-but-open files under the repo or wave dir either.

---

## 3. (b) No stray processes / fds from the probe runs

### 3.1 Process snapshots

- T0 snapshot 06:56:58 (`ps -eo pid,ppid,etime,stat,rss,cmd --sort=-rss`): top consumers were
  pre-existing desktop processes (obsidian/electron, kimi, 1Password, Hyprland, oauth-shim).
  No orphaned probe processes.
- In-flight at 06:57–06:58 (expected, not stray): a c1 probe running
  `npm view solc version` / `npx -y rea-agents@6.7.0 --version`, and an EX-05 retry loop.
- Final snapshot 07:01:35: `ps | grep -iE "npm|npx|solcjs|rea-agents|inspect-evm"` →
  **empty**. Every probe process exited; nothing was left behind.

### 3.2 Zombies

Four `<defunct> [uwsm-app]` zombies (PIDs 1748/1753/1757/1760) with elapsed time
**06:26:58** — i.e. from login at 00:34, ~6.4 h before the wave. **Pre-existing, unrelated
to the wave.** No new zombies from any probe run.

### 3.3 FDs

Covered in §2.5: no probe (or any process) holds a custody path open. No `deleted` entries
under the repo or wave dir were found in `/proc/*/fd`.

---

## 4. (c) journalctl — OOM / containment events in the wave window

### 4.1 No OOM, no kills, no cgroup events

```
$ journalctl --no-pager --since "2026-10-19 00:34:00" -p warning \
    | grep -iE "oom|killed process|out of memory|cgroup|contain|memory pressure|invoked oom"
(no output)
$ journalctl -k --no-pager --since "2026-10-19 00:34:00" \
    | grep -iE "oom|out of memory|killed|quota|cgroup|contain"
kernel: VFS: Disk quotas dquot_6.6.0
(pci BAR "no space" lines are boot-time firmware noise, unrelated)
$ systemctl --user --failed ; systemctl --failed
0 loaded units listed   (both scopes)
```

Verdict: **no OOM events, no process kills, no cgroup containment events, no failed units**
anywhere from boot through the wave window. Memory pressure was real but never fatal:
`free -h` at 07:00 showed 30Gi RAM with 3.2Gi free / 11Gi available, swap 34Gi with 7.9Gi used.

### 4.2 The one containment-relevant event that *is* in the journal

```
Oct 19 00:34:53 plazir27 systemd-user-runtime-dir[1456]:
    Successfully configured disk quota for UID 1000 on /tmp to 12.1G
Oct 19 00:34:53 plazir27 systemd-user-runtime-dir[1456]:
    Successfully configured disk quota for UID 1000 on /dev/shm to 12.1G
```

This is a **deliberate per-user containment quota** on `/tmp`, applied at login by
`systemd-user-runtime-dir`. `/tmp` is mounted with `usrquota`:

```
$ findmnt -no OPTIONS /tmp
rw,nosuid,nodev,nr_inodes=1048576,inode64,huge=advise,usrquota
$ systemctl show tmp.mount -p Options
Options=rw,nosuid,nodev,nr_inodes=1048576,inode64,huge=advise,usrquota
```

### 4.3 That quota is now saturated — every byte-write to /tmp fails

`/tmp` usage exceeds the 12.1G quota:

```
$ df -h /tmp | tail -1
tmpfs            16G   13G  3.1G  80% /tmp
$ du -sh /tmp
13G	/tmp
```

Directly measured write behaviour (repeated at 06:57, 06:58, 07:01 — stable, not transient):

```
touch0:           OK   size=0      (0-byte create succeeds)
one (1 byte):     FAILED errno=122 Disk quota exceeded
kb (1024 bytes):  FAILED errno=122 Disk quota exceeded
append-existing:  FAILED errno=122 Disk quota exceeded
mkdir:            OK
```

Re-tested at 07:01:16 — still `EDQUOT` on both a 1-byte and an 11-byte write. The
discriminator is exact: **inode allocation succeeds, block allocation fails** → this is the
*space* quota, not the inode quota (`df -i`: 155422 inodes free).

Attribution of the 13G: `find /tmp -maxdepth 1 -mindepth 1 -user vgpnk | wc -l` → 1427
entries (only small root-owned `systemd-private-*` dirs are foreign), so essentially all of
it is UID 1000's. Of that, **~7.2G is 24 stale pre-wave directories** (see §4.5).

**Causal status — stated honestly.** The quota *limit* (12.1G) is read from the journal; the
usage (13G) is measured with `du`/`df`; the failure (errno 122) is measured directly. The
inference "usage ≥ limit ⇒ EDQUOT" is consistent with all three and is the only mechanism
found. I could not read the kernel's live quota counter directly (that needs root/`quotactl`),
so the limit figure is journal-sourced rather than counter-sourced. No alternative cause was
found: `df` reports 3.1G still free on the tmpfs, and `mkdir`/0-byte creates still succeed,
which rules out filesystem-full and inode exhaustion.

### 4.4 Consequence — silent zero-byte evidence across all three chains

Because shell redirection **creates** the file and then fails the write, a seat's scratch
file can appear to exist while containing nothing, with no error surfaced in the seat's
tool output. Measured casualty census (`tmp-quota-casualties.txt`, window ≥ 06:49):

- **Tier A — defensible casualties (63 files):** 0-byte files whose extension implies
  non-empty content (`.sol .py .sh .json .hex .bin .lines .toml .md`). Examples:
  `/tmp/ex06/KdxToken.sol`, `/tmp/ex07/Selftest.sol`, `/tmp/rv1/keccak_ref.py`,
  `/tmp/ex30/recipeA.py`, `/tmp/rv3/cmdA-worktree.py`, `/tmp/rv2-c1/Rv2Token.sol`,
  `/tmp/ex05-work/recon.hex`, `/tmp/cr3/old-table-265e1aa.json`,
  `/tmp/ex18-absent/gate/pointer-table.json`, `/tmp/vz2-base/citation-drift/pointer-table.json`.
- **Tier B — ambiguous (84 files):** 0-byte `.txt/.err/.out/.log`, which can be legitimately
  empty (e.g. a clean stderr), plus CLI-owned `/tmp/devin-overflows-1000/**`.

**Total 147 zero-byte files created in the wave window.** Tier A spans c1 (`ex05/ex06/ex07/
pl1/rv1/rv2/rv3`), c2 (`ex18/ex20/ex21/ex24/cr3/sc5/vz2`), c3 (`ex27/ex29/ex30/rv10/rv11/
vz3`) and cross (`cu1/cr5`).

Two independent live corroborations that these are real losses, not empty-by-design:

1. **EX-05's own retry loop**, caught in the process table at 06:57:56:
   `for i in $(seq 1 12); do if printf '6001600101' > recon.hex 2>/dev/null; then ok=1; …; fi; sleep 5; done`
   — a seat visibly fighting the failure and retrying a 5-byte write 12 times. Its
   `/tmp/ex05-work/recon.hex` is still 0 bytes.
2. **Seat self-reports.** Both landed c1 reports independently name the same condition:
   - `seats/EX-02.md` §5: "`/tmp` scratch is unusable for this user (tmpfs usrquota
     exhausted → EDQUOT on any write)", with attack #1 ("Independent tarball capture via
     `npm pack` to /tmp → FAILED: errno -122 EDQUOT").
   - `seats/EX-11.md` §5: "/tmp … intermittently returns `OSError: [Errno 122] Disk quota
     exceeded` on scratch writes; two scratch attempts failed mid-run."

   **Two corrections to EX-11's characterization**, from direct measurement: the condition is
   *not intermittent* (it failed on every byte-write across three probes spanning 06:57–07:01),
   and it is *not* attributable to "the 64-seat wave" filling `/tmp` — the dominant consumers
   predate the wave (§4.5). EX-11's own numbers were unaffected (their recipe is read-only
   against Git objects), so this correction does not change their result.

### 4.5 The saturation is pre-existing, not wave-induced

`/tmp`'s 24 largest directories all have mtimes **01:28–04:58**, before the 06:49 wave start:

```
/tmp/d23          2.2G   mtime 2026-10-19 02:08:14
/tmp/P1           484M   mtime 2026-10-19 01:28:45
/tmp/p6           443M   mtime 2026-10-19 01:30:04
/tmp/c1           348M   mtime 2026-10-19 04:48:13
/tmp/m1h24        294M   mtime 2026-10-19 02:36:50
/tmp/f2           268M   mtime 2026-10-19 04:42:57
  … 18 more, 105M–258M, mtimes 01:28–04:58
sum of the 24:   7223152 KB ≈ 6.9G
```

So the wave inherited a `/tmp` that was already over quota. The wave did not cause it, but
it *did* absorb the damage: 147 zero-byte artifacts. **Nothing was deleted by this seat** —
the stale directories are other sessions' state and removing them is the operator's call,
not a seat's. Note that `du -sc` of those 24 dirs ≈ 6.9G, comfortably more than the ~1G
needed to get back under the 12.1G quota.

### 4.6 Where the wave's own writes *did* work

Everything written under the wave dir succeeded, because the wave dir lives on `/home`
(`/dev/mapper/root`, 930G, 703G avail) — not on the quota-limited tmpfs. Verified:
EX-02's `tools/solc-prefix/` install (soljson.js 9237611 B, sha256 `221d7a6673…`),
EX-02's compiled `Smoke_sol_Smoke.bin`, RV-2's `Rv2Token.creation.hex` (3942 B),
EX-13's `README.patched` (45229 B). The install authorization ("isolated prefix under the
wave dir") is therefore also the containment-correct choice.

---

## 5. Additional leak found (recurring) — unauthorized repo path `.ufo/gates/__pycache__/`

Not one of the three requested checks, but squarely a containment finding, so recorded.
**Summary: created 06:58:37 in-window, removed 07:03 by EX-26, recreated 07:04:16, live at
this seat's close 07:05:27 (both creations verified by inode).**

```
$ git status --porcelain          # observed 2026-10-19T07:00-07:02
 M .ufo/waves/arc2-loop1-round10/C3.md
?? .ufo/gates/__pycache__/
?? .ufo/waves/arc3-loop1-round1/
```

- `.ufo/waves/arc3-loop1-round1/` — the authorized wave dir. Expected.
- `.ufo/waves/arc2-loop1-round10/C3.md` — modified **2026-10-18 23:01:44**, i.e. **pre-wave**.
  Pre-existing, also noted independently by EX-11. Not a wave write.
- `.ufo/gates/__pycache__/` — **created inside the wave window.** Pinned exactly:

```
$ stat -c '%n | mtime=%y | ctime=%z | inode=%i' .ufo/gates/__pycache__ \
    .ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc
.ufo/gates/__pycache__          | mtime=2026-10-19 06:58:37.715331109 | ctime=2026-10-19 06:58:37.715331109 | inode=36440714
.ufo/gates/__pycache__/…pyc     | mtime=2026-10-19 06:58:37.715331109 | ctime=2026-10-19 06:58:37.715331109 | inode=36440715

$ stat -c '%n mtime=%y ctime=%z' .ufo/gates
.ufo/gates mtime=2026-10-19 06:58:37.713506697 ctime=2026-10-19 06:58:37.713506697
```

The parent `.ufo/gates` directory's own mtime/ctime moved to 06:58:37.713 — i.e. **a new
directory entry was added to `.ufo/gates` at 06:58:37**, inside the window. Both directory
and file are new (ctime == mtime), so neither existed before.

Provenance proof that it came from the census instrument:

```
$ python3 -c "…read pyc header…"
magic 0xa0d0e2b flags 0
embedded source mtime 2026-10-18 20:31:48
embedded source size  20256
actual c1-census-v10.py size   20256
actual c1-census-v10.py mtime  2026-10-18 20:31:48.836774
```

The pyc embeds the census source's exact mtime **and** size — it is the compiled form of
`.ufo/gates/c1-census-v10.py`. It was produced by a C3 seat *importing* the instrument
(Python writes `__pycache__` on import/`runpy`, not on `python3 script.py`); C3 census runs
landed at 06:57 (EX-26, RV-11) and 06:58 (SC-6), matching the 06:58:37 timestamp.

Note the instrument itself was **not** modified — `c1-census-v10.py` still shows
mtime 2026-10-18 20:31:48. Only the incidental `__pycache__` appeared.

**Why this matters:** `.ufo/gates/__pycache__/` is outside every authorized write path, and
it is **not gitignored** (`git check-ignore` → no rule; `.gitignore` contains no `__pycache__`
pattern). It therefore shows up as untracked noise that the parent could sweep into the
integration commit.

**Remediation (verified):** the leak was self-caught and reversed. EX-26's report states the
`__pycache__` was "created 06:58:37, absent from the 06:57 `git status`" and "Removed with
the now-empty directory at 07:03" (`seats/EX-26.md` §5). This seat re-checked at
**2026-10-19T07:03:42**:

```
$ ls -la .ufo/gates/__pycache__/
ls: cannot access '.ufo/gates/__pycache__/': No such file or directory
$ git status --porcelain
 M .ufo/waves/arc2-loop1-round10/C3.md
?? .ufo/waves/arc3-loop1-round1/
```

So the artifact existed for **~4.5 minutes (06:58:37 → 07:03)** and is now gone; `git status`
is back to the two pre-wave entries. EX-26's remediation claim is **CONFIRMED, not merely
asserted** — this seat observed the artifact present at 07:02 and absent at 07:03:42, which
independently brackets the removal.

**The leak then recurred — measured, not predicted.** A second creation appeared at
**2026-10-19 07:04:16** (new inode, so genuinely a second `mkdir`, not the same directory):

```
$ stat -c '%n mtime=%y ctime=%z inode=%i' .ufo/gates/__pycache__ .ufo/gates/__pycache__/*
.ufo/gates/__pycache__        | mtime=2026-10-19 07:04:16.701181610 | inode=36522168
.ufo/gates/__pycache__/…pyc   | mtime=2026-10-19 07:04:16.701181610 | inode=36522169
$ stat -c '%n mtime=%y' .ufo/gates
.ufo/gates mtime=2026-10-19 07:04:16.699420639
$ git status --porcelain        # 2026-10-19T07:05:27
 M .ufo/waves/arc2-loop1-round10/C3.md
?? .ufo/gates/__pycache__/
?? .ufo/waves/arc3-loop1-round1/
```

(Inode 36522168 vs the first occurrence's 36440714; same pyc size 23796 B.) So a C3 seat
imported the census instrument again ~1 minute after EX-26 cleaned up. **Per-seat cleanup
does not hold across the roster** — this is now a measured recurrence, not a hypothetical.
This is the direct justification for the `.gitignore` proposal at
`claims/c1/EX-15/proposed-gitignore-pycache.patch.md`.

Three caveats for the parent:

- The remediation was itself a write outside the authorized paths (a deletion under
  `.ufo/gates/`). It restored the pre-wave state and was self-reported, so it is the right
  outcome, but strictly it is a second out-of-path action. The parent may prefer an explicit
  "self-caught side effect may be reversed by the causing seat" clause in the next freeze.
- **Three reports mischaracterize this artifact.** `seats/EX-01.md:36`, `seats/EX-30.md:25`
  and `seats/EX-11.md:25` all list `?? .ufo/gates/__pycache__/` among pre-existing `git status`
  entries. It was created *in-window* at 06:58:37; those characterizations are wrong, though
  harmless since all three seats only used the list to show they were not the writer.
- **The leak is live at this seat's close.** The directory exists as of 07:05:27. This seat
  did not remove it: the removal would be a write outside the authorized paths, the parent
  needs to see the recurrence, and any cleanup that does not also add the `.gitignore` rule
  will simply recur.
- **Residual risk:** any future C3 census run that imports the instrument will recreate this
  directory. A `.gitignore` rule for `__pycache__/` (proposed as patch text, not applied —
  see the seat report §2) would neutralize it permanently.

---

## 6. Attacks / refutations attempted

1. **"The custody captures are too late to prove anything"** (T0 was taken at 06:58, nine
   minutes after the wave opened) → **partially conceded, then refuted by other means.**
   The capture pair alone would not cover 06:49–06:58. But every custody path's mtime/ctime
   predates the window by 7.5 h to 4.5 days (§2.3), and CU-1's independent 06:57:18 capture
   agrees with T0 and T1 on all five hashes. Verdict: the window is covered by filesystem
   timestamps, not just by the capture pair.
2. **"Maybe /tmp writes are only intermittently failing"** (EX-11's characterization) →
   **REFUTED.** Three probes at 06:57, 06:58 and 07:01 each failed a 1-byte write with
   errno 122 while 0-byte creates succeeded. Verdict: deterministic and persistent, not
   intermittent.
3. **"Maybe the wave's 64 seats filled /tmp"** (EX-11's attribution) → **REFUTED.** The 24
   largest `/tmp` dirs (≈6.9G) have mtimes 01:28–04:58, before the 06:49 wave start.
   Verdict: pre-existing saturation inherited by the wave.
4. **"Maybe it is inode exhaustion, not space quota"** → **REFUTED.** `touch` (0-byte create,
   needs an inode) succeeds; any ≥1-byte write fails; `df -i` shows 155422 free inodes.
   Verdict: space quota.
5. **"Maybe it is just the tmpfs being full"** → **REFUTED.** `df` reports 3.1G still
   available on the tmpfs while writes fail. Verdict: per-UID quota, not filesystem size.
6. **"Maybe probe processes are still running / leaked"** → **REFUTED** at 07:01:35 — the
   npm/npx/solc/rea process scan is empty, and the only zombies are 6.4 h old and from login.
   Verdict: no stray processes or fds.
7. **"Maybe `.ufo/gates/__pycache__/` predates the wave"** (EX-11 `:25`, EX-01 `:36` and
   EX-30 `:25` all list it among pre-existing `git status` entries) → **REFUTED.** dir and
   file ctime == mtime == 06:58:37, and the parent `.ufo/gates` mtime moved at 06:58:37.713.
   Verdict: created in-window by a C3 census run; the three reports mischaracterize it as
   pre-existing.
8. **"Maybe the C3 seat modified the census instrument"** → **REFUTED.** `c1-census-v10.py`
   mtime/ctime unchanged at 2026-10-18 20:31:48. Only `__pycache__` appeared.
9. **"Maybe EX-26's remediation claim is just an assertion"** → **CONFIRMED by observation,
   not taken on trust.** This seat saw the directory present at 07:02 and absent at
   07:03:42, bracketing the removal EX-26 reports at 07:03. Verdict: remediation real.
10. **"Maybe the cleanup is durable — one seat cleaned up, so the class is closed"** →
    **REFUTED.** The directory reappeared at **07:04:16** with a new inode (36522168), ~1 min
    after EX-26's removal. Verdict: per-seat cleanup does not hold; the `.gitignore` proposal
    is the durable fix.
11. **"Maybe EX-02's solc install leaked outside its prefix"** → **not a full check by this
    seat**, but supporting evidence exists: `git status` shows no stray tracked/untracked
    files besides those in §5, and EX-02's own pre/post custody pair is empty. The npm cache
    (`~/.npm`) is explicitly outside the custody set per the frozen rules, so its writes are
    authorized by definition. Verdict: no observable leak; EX-02's receipt is the
    authoritative record.
12. **"Maybe the wave wrote into other seats' chain dirs or the repo outside the wave dir"** →
    **REFUTED** by `git status --porcelain` at 07:03:42 (2 entries: the pre-wave
    `arc2-loop1-round10/C3.md` and the authorized wave dir) and again at 07:05:27 (3 entries —
    the third being the recurred `__pycache__`, i.e. the only stray path, and the only one
    §5 discusses).

---

## 7. Evidence index (files in this directory)

| File | What it is |
|---|---|
| `containment.md` | this artifact |
| `custody-T0.txt` | 5-path sha256+mtime+ctime+size, 2026-10-19T06:58:40-03 |
| `custody-T1.txt` | same, closure capture 2026-10-19T07:01:16-03 |
| `custody-crosswave-diff.txt` | T0 vs arc2-loop1-round1 pre-pair receipt |
| `tmp-quota-casualties.txt` | zero-byte casualty census (Tier A 63 / Tier B 84) |
| `_writecheck.txt` | wave-dir write sanity check (the /home path works) |

Read-only cross-references used: `claims/cross/receipts/config-pre-pair.txt` and
`config-pre-pair-metadata.txt` (CU-1), `claims/c1/EX-02/install-receipt.txt`,
`seats/EX-02.md`, `seats/EX-11.md`, `claims/c1/EX-14/MANIFEST.draft.txt`.

## 8. Blockers / limits of this seat

- **This seat's own scratch was impaired.** The mandated `/tmp` scratch location was
  unusable, so all captures were written directly to this artifact directory (on `/home`).
  `/tmp/ex15-scratch/` was created and cleaned; its contents were all 0 bytes anyway.
- **No live quota-counter read.** The 12.1G limit is journal-sourced; reading the live
  counter needs root/`quotactl`. The EDQUOT failure itself is directly measured.
- **No post-close capture of custody beyond T1 (07:01:16).** Probes were still finishing
  when T1 was taken. A parent-side post-pair capture at integration is still warranted;
  CU-1's post-pair receipt is the designated closure artifact.
- **Casualty tiers are heuristic.** Tier B (84 files) includes files that may be
  legitimately empty; only Tier A (63) is defended. Wave-dir 0-byte files were deliberately
  *excluded* from the census — e.g. `claims/c1/EX-14/MANIFEST.draft.check.sha256` is 0 bytes
  because it is the sha256 of the empty string with 0 entries, and
  `claims/c1/RV-2/solc-out.err` is 0 bytes because the compile emitted no errors. Neither is
  a quota casualty, and conflating them would have inflated the count.
