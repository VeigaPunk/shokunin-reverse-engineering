# SEAT CU-1 — chain cross, role custody (arc3-loop1-round1)

Status: **DRAFT — post-pair section pending** (written at 2026-10-19T10:05Z; the wave's
post-pair capture lands at the end of this seat's run and is appended below).

## 1. Work performed (each bullet with an evidence pointer)

- **Pre-pair custody capture landed before the install/probe window closed.**
  `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
  (self sha256 `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776`,
  capture-utc **2026-10-19T09:57:18Z**, repo HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`).
  All 5 paths present; sha256 recorded per path (table in §3).
- **Attribution metadata captured** (inode/ctime/mtime/size/blocks per path):
  `claims/cross/receipts/config-pre-pair-metadata.txt`
  (self sha256 `85fa1860000bda4de57ffb17219e59fa0e553d505eb76815c4bcf542f6426a90`,
  2026-10-19T09:57:48Z).
- **Continuous-ish re-measurement during the wave**: `claims/cross/receipts/custody-snapshots.txt`
  — 25×60s checks, each a fresh 5-path sha256 vs the pre-pair, with a drift line per path
  (sha + size + mtime + ctime + inode) when a mismatch is seen.
- **Writer/attribution analysis material**: `claims/cross/receipts/writer-candidates.txt`
  — live processes, systemd services/timers, repo-side readers of the custody paths, and the
  pre-wave `config.toml` excursion analysis.
- **Adjacent-surface capture** (sibling configs + sidecars in the custody dirs):
  `claims/cross/receipts/sidecar-inventory-pre.txt`
  (self sha256 `4d55b758d6462c7e001583c61844e279c0fde8359baea53a9e39102d1710f93e`) and
  `claims/cross/receipts/adjacent-hashes-pre.txt`
  (self sha256 `f0ed35a2c1166d442ea78c16ecf9c0977e4e78e9469684e8f1d7e3c891f65b9b`).
- **Third-party corroboration collected** (not produced by this seat):
  seat EX-02's independent pre-pair `claims/c1/EX-02/custody-pre-pair.txt` and post-install
  `claims/c1/EX-02/custody-post-pair.txt` (diff EMPTY); seat EX-14's `claims/c1/receipts/MANIFEST.draft.txt`
  which re-checked my receipt by sha256 (`b8ed1936…`) and re-verified the 5 hashes live at
  09:59:40Z ("match (5/5)"); seat EX-15's `claims/c1/EX-15/custody-T0.txt` + cross-wave diff.

## 2. Proposed changes

- none (custody seat produces receipts/evidence only; no repo target is written or modified
  outside this seat's own report + `claims/cross/receipts/` artifacts).

## 3. Before → after measurement (the custody pair)

Pre-pair (2026-10-19T09:57:18Z), verbatim sha256:

| path | sha256 (pre) |
|---|---|
| ~/.config/devin/mcp_config.json | `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4` |
| ~/.omp/agent/mcp.json | `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b` |
| ~/.kimi-code/config.toml | `8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d` |
| ~/.bashrc | `7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598` |
| ~/.profile | `6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30` |

**Ordering evidence (pre-pair really is pre-install):** `tools/solc-prefix` (the only
authorized install target) has mtime `2026-10-19 06:57:25.61 -0300` = 09:57:25.6Z — **7.4 s
after** the pre-pair receipt was written (06:57:18.199 local). npm cache index entry for the
solc tarball is stamped 09:57:02Z (EX-02 install receipt §4), i.e. download began ~16 s
before the prefix existed; the receipt itself was written before any prefix file existed.

Post-pair: **pending** — appended below at wave close.

## 4. Attacks / refutations attempted

- **Attack: "the pre-pair is not pre-install."** Refuted with mtimes (§3): prefix 7.4 s after
  receipt; also EX-02 independently captured its own pre-pair at 09:57:0xZ, before running the
  install, and the two captures agree hash-for-hash (5/5).
- **Attack: "a single-seat capture could be stale or mis-transcribed."** Refuted by three
  independent captures agreeing on all 5 hashes (CU-1 pre-pair, EX-02 pre-pair, EX-15 T0),
  plus EX-14's manifest re-verification of my receipt's own sha256 and a live 5/5 match at
  09:59:40Z.
- **Attack: "sha256-only custody is blind to a same-content rewrite" (measurement-validity
  attack).** Confirmed as a real blind spot, empirically, on scratch in `/dev/shm`:
  rewriting a file with byte-identical content leaves `sha256` unchanged
  (`d49fa9ab…` both writes) while `ctime` advances (07:02:33 → 07:02:34). Mitigation applied:
  the metadata receipt pins inode/ctime, and the post-pair comparison checks **sha256, size,
  inode and ctime**, not sha256 alone.
- **Attack: "drift could be caused by a sidecar/sibling write rather than the 5 paths."**
  Partially addressed: sidecar inventory + adjacent hashes pin `~/.config/devin/config.json`,
  `~/.omp/agent/config.yml`, `~/.omp/agent/mcp.json`, `~/.kimi-code/mcp.json` and the newest
  `.bak`/`.backup` sidecars. Live writers observed inside the wave window on siblings:
  `~/.config/devin/config.json` (mtime 06:51, with `config.json.r34-backup` at 06:50) and
  `~/.omp/agent/agent.db{,-shm,-wal}` (07:00–07:02). **No custody path was touched by these.**
- **Attack: "an already-known excursion is being hidden."** Disclosed, not hidden: vs the
  arc2-loop1-round1 pre-pair, `~/.kimi-code/config.toml` differs
  (`3546e033…` → `8cbacd48…`). Its mtime is `2026-10-18 23:20:43` local = 07:20:43Z — about
  7.5 h **before** this wave's dir existed (06:49–06:56 local). Pre-wave, not attributable to
  this wave; independently observed by EX-15.
- **Attack: "the custody set is complete."** Not fully refuted: the 5 paths are the frozen
  set, but they exclude sidecars (`mcp.json.rea.backup`, `config.json.r34-backup`,
  `config.toml.<ts>.bak`) and sibling configs, all of which demonstrably receive writes.
  Recorded as a scope note for the parent, with the adjacent-surface baselines as the mitigation.

## 5. Blockers / environment caveats

- **`/tmp` is unusable this wave (fleet-wide).** `mount | grep ' /tmp '` →
  `tmpfs ... nr_inodes=1048576,inode64,huge=advise,usrquota`; user quota exhausted — even a
  4 KiB write yields `0 bytes copied` (0-byte file) and `2 MiB` fails the same way; `df -h /tmp`
  shows 16G/13G/3.1G but writes still fail (EDQUOT). Independently reported by EX-02
  (install receipt §8, errno -122). Consequence: this seat's watcher/scratch moved into
  `claims/cross/receipts/`; nothing was left under `/tmp` (`/dev/shm` remains writable and was
  used for the blind-spot demo, then cleaned).
- No custody-path drift observed so far; the pre-pair stands as the wave's baseline.
