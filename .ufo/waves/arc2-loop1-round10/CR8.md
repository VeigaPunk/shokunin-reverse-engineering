# CR8 — critic: provenance attack on the rerun envelopes (arc2-loop1-round10)

Seat: CR8 (critic) · 2026-10-18 · writes limited to this file; no repo edits, no git
mutations, no service signals (WATCH only), no config edits, no network. Scratch under
`/var/tmp/arc2-l10r10-CR8-work/`. Both live legs observed read-only; neither was signaled.

Axes: exclusivity (single writer / exclusive hold), binding (bytes ↔ invocation),
durability (surviving second copy), recipe identity (is the rerun the same experiment?).

## 1. Verdict

**SPLIT — one leg is decisive and re-derives; the other leg is not decisive at all and
must not be read as a refutation.**

**(a) Big leg — ID-STABILITY CONFIRMED, and the claim survives the single-writer attack.**
`arc2-r10-big` sealed an envelope **byte-identical** to the receipt committed at round 7:
sha256 `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`, 5204 B, 0 diff
lines against `.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json`. `evidence_id
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608` re-derives. The
analyze id is content+params-keyed at this scale point. The r6 CR8 hazard **reproduces**
(mode 0644, same-uid writable, no immutable bit, path published to 64 same-uid seats) but
is **defeated here** by two channels the file cannot fake: inode continuity with a
238-sample zero-byte series, and the root-owned systemd journal's resource record. Residual
named in §4, not waved away.

**(b) Mid leg — NOT a rerun of the r6 leg, and it produced no id. It can neither confirm
nor refute r6 id-stability.** `arc2-r10-mid` was kernel-OOM-killed at a **9 GiB `MemoryMax`
in 53.178 s**, sealing a typed `cancelled` envelope with **zero `ev_` occurrences**. More
importantly, the 9 GiB cap in the seat line is **not the r6 recipe**: the round-6 leg was a
plain bash runner with **no cgroup at all**, and its own record shows an 18.263 GiB peak
tree RSS at exit 0 — incompatible with any 9 GiB cap. The round-10 mid leg is therefore a
*different experiment* (containment and launcher both changed), and its failure is
cap-induced. Reporting it as "the r6 rerun failed" would be a **false refutation** of
`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md`.

**(c) C1's state model is too coarse and will mis-score.** C1 says "both legs sealed →
…; in-flight at close → the sealed leg(s) still land, unsealed leg(s) = named debt". The
mid leg is neither sealed nor in-flight: it is **terminal-unsealed** (typed error, no id)
**and off-recipe**. That is a third state, and a fourth qualifier (recipe-matched?) is
required before any leg may be counted as an id-stability data point. On the evidence, C1
lands at **one** scale point (91.6 MB), not two.

**(d) The recipe for the "exact r7 recipe" big leg is asserted, not artifact-sealed — the
same gap class as the mid leg's cap error.** `arc2-r7-pe.service` no longer exists
(`LoadState=not-found`), and the r7 journal line records no `MemoryMax` and no
`Environment`. The big leg's recipe identity is carried by outcome and by log-level
agreement (§2), not by a surviving unit file. Unlike the mid leg, the anchors here all
agree, so the recipe claim is sound — but it should be stated as reconstructed.

## 2. Evidence

All read-only. Local time −03. Snapshot cut 2026-10-18T21:58 −03.

### 2.1 Big leg — the decisive artifact

```sh
systemctl --user cat arc2-r10-big.service
# [Service]
# MemoryMax=9663676416
# MemorySwapMax=1073741824
# StandardOutput=file:/var/tmp/arc2-l10r10-big/stdout.json
# StandardError=file:/var/tmp/arc2-l10r10-big/stderr.log
# Environment="REA_GHIDRA_DISABLED_ANALYZERS=Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis" \
#   "REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000" "GHIDRA_HEADLESS_MAXMEM=6G" \
#   "TMPDIR=/var/tmp/arc2-l10r10-big" "GHIDRA_INSTALL_DIR=.../ghidra_12.1.4_PUBLIC" \
#   "JAVA_HOME=/usr/lib/jvm/java-21-openjdk"
# ExecStart="/home/vgpnk/.local/share/mise/installs/node/latest/bin/npx" "-y" "rea-agents@6.5.0" "analyze" ".../windows_release_arm64.exe"

journalctl --user -u arc2-r10-big.service --no-pager -o short-iso | tail -2
# 2026-10-18T20:56:25-03:00 Started [systemd-run] .../npx -y rea-agents@6.5.0 analyze .../windows_release_arm64.exe.
# 2026-10-18T21:20:23-03:00 arc2-r10-big.service: Consumed 42min 43.809s CPU time over
#   23min 58.082s wall clock time, 7.8G memory peak, 769.1M memory swap peak.

stat -c '%n mode=%a owner=%U ino=%i size=%s birth=%w mtime=%y ctime=%z' /var/tmp/arc2-l10r10-big/stdout.json
# /var/tmp/arc2-l10r10-big/stdout.json mode=644 owner=vgpnk ino=2840144 size=5204
#   birth=2026-10-18 20:56:25.385370723 -0300 mtime=2026-10-18 21:20:23.388139992 -0300 ctime=<same>

sha256sum /var/tmp/arc2-l10r10-big/stdout.json
# a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a   (== r7 receipt sha256)
diff /var/tmp/arc2-l10r10-CR8-work/big-envelope-copy.json \
     .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json && echo BYTE-IDENTICAL
# BYTE-IDENTICAL to r7 receipt
head -1 /var/tmp/arc2-l10r10-CR8-work/big-envelope-copy.json
# evidence_id: ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
```

Binding to *this* run (the check r6 CR8 could not perform):

```sh
grep -c "size=0" /var/tmp/arc2-l10r10-CR8-work/watch-big.log        # 238
grep -o "ino=[0-9]*" .../watch-big.log | sort -u                    # ino=2840144  (single inode)
# 238 consecutive 5-s samples 21:00:33→21:20:19 all size=0 ino=2840144;
# first non-zero observation is the terminal snapshot at 21:20:24, size=5204.
# i.e. the file was empty for the whole 20-minute window I watched and became
# 5204 bytes at mtime 21:20:23.388139992 — the same second as the journal's
# completion line (the journal records whole seconds, so it cannot order the two).
```

Writer set (exclusivity axis):

```sh
# full /proc/<pid>/fd scan at 21:00:04, all arc2-l10r10-* targets:
# pid=622317 comm="npm exec rea-ag"  fd=1 -> /var/tmp/arc2-l10r10-big/stdout.json
# pid=622423 comm=node-MainThread   fd=1 -> /var/tmp/arc2-l10r10-big/stdout.json
# pid=622629 comm=java fd=157 -> .../rea-ghidra-JpFr4i/ghidra.log ; fd=158 -> .../script.log
# (no other holder of the envelope path; java does NOT inherit fd 1 onto it)
python3 -c "import os;p='/var/tmp/arc2-l10r10-big/stdout.json';print(os.access(p,os.W_OK),os.getuid())"
# True 1000
lsattr /var/tmp/arc2-l10r10-big/stdout.json
# ----------------------   (no immutable bit)
```

Recipe-identity anchors (the r7 unit file is gone, so identity is carried by these):

```sh
systemctl --user show arc2-r7-pe.service -p LoadState,MemoryMax
# LoadState=not-found
# MemoryMax=infinity          <-- the not-found default, NOT r7's actual cap
sed -n '276,279p' /var/tmp/arc2-l10r10-big/rea-ghidra-JpFr4i/ghidra.log   # preserved copy, §2.3
# 276 REPORT: Execute script: .../ReaGhidraAnalysisOptions.java 'Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis'
# 277 SCRIPT:   .../ReaGhidraAnalysisOptions.java
# 278 ANALYZING all memory and code: file:///.../target-7a2ccd688f6c.exe
# 279 Skipping PDB processing: missing PDB information in program metadata
grep -c "Call Convention ID" <preserved log>     # 1  (argument line only; no activity line)
```

These `:276/:277/:278` line numbers are exactly the ones r7's own disable proof cites
(`.ufo/waves/arc2-loop1-round7/E3.md:74`: "pre-script `ReaGhidraAnalysisOptions.java`
executed with exactly those names at ghidra.log:276 … before `ANALYZING` at :278"). The
npx cache resolves to the same directory in both rounds (`.../.npm/_npx/ad9a3fdbcad992c6/`,
seen in the live argv and in the journal form), and the imported target inside the runtime
root is `target-7a2ccd688f6c.exe`, 91,662,336 B — the pinned artifact. Resolving pointers:
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7,11,13,15`.

### 2.2 Mid leg — terminal-unsealed, and not the r6 experiment

```sh
systemctl --user show arc2-r10-mid.service \
  -p Result,ExecMainStatus,MemoryPeak,MemoryMax,MemorySwapPeak,MemorySwapMax,ActiveEnterTimestamp,ActiveExitTimestamp,NRestarts
# Result=oom-kill
# ExecMainStatus=1
# MemoryPeak=9663676416        <-- byte-equal the cap (constraint-kill signature)
# MemoryMax=9663676416
# MemorySwapPeak=1073741824 ; MemorySwapMax=1073741824
# ActiveEnterTimestamp=Sun 2026-10-18 20:56:25 -03
# ActiveExitTimestamp=Sun 2026-10-18 20:57:18 -03        (duration 53.178 s)
# NRestarts=0
journalctl --user -u arc2-r10-mid.service --no-pager -o short-iso | tail -3
# arc2-r10-mid.service: The kernel OOM killer killed some processes in this unit.
# arc2-r10-mid.service: Failed with result 'oom-kill'.
# arc2-r10-mid.service: Consumed 4min 14.200s CPU time over 53.602s wall clock time, 9G memory peak, 1G memory swap peak.
grep -o "ev_[0-9a-f]\{64\}" /var/tmp/arc2-l10r10-mid/stdout.json | sort -u
# (empty — zero evidence ids)
grep -n "code:\|category:\|operation:\|failure_message\|target_sha256\|profile_digest\|run_id" /var/tmp/arc2-l10r10-mid/stdout.json
# 2:code: cancelled   3:category: cancelled   9:  operation: list_documents
# 13: target_sha256: a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786   (= r6 target)
# 16: profile_digest: 59e0d37bce87c1b8ccb70c6062be2383648a35642f5a6c85b1db0939164d5e55   (= r6 ghidra profile)
# 17: run_id: c6b1b41b-f0bf-47ce-ba1c-4f1706396e48    18: runtime_root: /var/tmp/arc2-l10r10-mid/rea-ghidra-FSLOSS
# 39: failure_message: Ghidra startup was cancelled
stat -c '%n ino=%i size=%s birth=%w mtime=%y' /var/tmp/arc2-l10r10-mid/stdout.json
# ino=2840146 size=315462 birth=2026-10-18 20:56:25.387370727 mtime=2026-10-18 20:57:18.810446698
sha256sum /var/tmp/arc2-l10r10-mid/stdout.json
# 56e87061869d8928c84a4c0926c5cd5e17c1ce56a0c0166f48ddafa9e4bb0981
```

The envelope is a legitimate artifact of *that* unit (inode born 20:56:25.387, mtime
20:57:18.810 matching the unit's 20:57:18 exit; `process_id: 622553` is in the same launch
batch as the big leg's 622317/622423/622629 and is now dead). It is simply not the r6
experiment and it carries no id.

**The r6 recipe, from r6's own surviving artifacts:**

```sh
cat /var/tmp/arc2-l6r6-E9-mid/run-leg.sh
# plain bash; sets REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G
#   GHIDRA_INSTALL_DIR=... TMPDIR=$SCRATCH/tmp ; then
# /usr/bin/timeout -k 60 5400 node "$REA_JS" analyze "$BIN" --format json > stdout.json
# NO systemd-run, NO MemoryMax, NO cgroup of any kind.
cat /var/tmp/arc2-l6r6-E9-mid/meta.txt
# exit_code=0   wall_s=2479   stdout_bytes=5660   stderr_bytes=0
# peak_tree_rss_kb=19149984        <-- 18.263 GiB
# peak_java_rss_kb=2884192
```

`.ufo/waves/arc2-loop1-round6/E9.md:66` names that peak: "Peak tree 19,149,984 kB
(18.263 GiB) was the decompiler swarm (10 `decompile` children observed, one ~4.1 GB
RSS)". `:77` records the launcher: "An outer `timeout -k 60 5400` was a backstop and did
not fire." **An 18.263 GiB peak tree RSS at exit 0 is incompatible with a 9 GiB
`MemoryMax`.** The two runs are therefore different experiments, differing in cgroup
containment (none → 9 G + 1 G) and launcher (direct bash → transient service). Both of
those changes are *upgrades* owed to the r7 lesson; they are simply not the r6 recipe.

### 2.3 Durability

`arc2-r10-big`'s runtime root was deleted at close — `/var/tmp/arc2-l10r10-big/` now holds
only `node-compile-cache/`, `stderr.log` (0 B) and `stdout.json`. Same as r7, where
`ghidra.log` was lost and E3 had to work from a partial snapshot. This seat's watcher
retained copies, which the parent can seal (this seat does not write repo files):

```
/var/tmp/arc2-l10r10-CR8-work/big-envelope-copy.json   5204 B  sha256 a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a
/var/tmp/arc2-l10r10-CR8-work/big-ghidra-log-latest.log  39580 B / 511 lines  sha256 81ba3b5a61adbe82b1bdfd64d059ce8ecca2c52040185043eb9a97dcfd0b32c2
/var/tmp/arc2-l10r10-CR8-work/big-seal-snapshot.txt    sha256 50ff3b02ac72996f5cb7cca50911716179263f826706e595dccb36fc4a6b6c74
/var/tmp/arc2-l10r10-CR8-work/watch-big.log            sha256 164b3c816e587af1a89c5060a81c0e79fe6022afa0bfa412b2805c8d1a35ca7a
```

The preserved log runs `:276` (pre-script) through `:511` (`REA no-return fix:
cleared=0 sites=0 refit=0` at 21:20:16, then `ReaGhidraBridge.java` at 21:20:16) — i.e. it
covers the whole analysis, including the disable proof, and is the only surviving copy.
It is a stronger receipt than anything r7 could keep.

### 2.4 Custody (scope adjacency)

```sh
awk 'NR>1{print $1"  "$2}' .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt > rec
sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
          /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile > now
diff rec now && echo "CUSTODY 5/5 MATCH"
# CUSTODY 5/5 MATCH
```

Receipt timestamp `.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt:1` =
`2026-10-18T23:56:25Z`, the same second as both units' `ActiveEnterTimestamp`
(20:56:25 −03). Point-in-time pre-pair only; not a post-pair or zero-drift result.

## 3. Verbatim-landable text

Draft append-only erratum for `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` (closes the
entry's `:7` and `:19` "rerun id-stability UNKNOWN"):

```markdown
Erratum (arc2-loop1-round10, 2026-10-18, append-only): rerun id-stability
RESOLVED — analyze ids re-derive. User service `arc2-r10-big` re-ran this
entry's recipe (transient unit, 9G `MemoryMax` + 1G swap, 7200s deadline, 6G
heap, the same three disabled analyzers, `TMPDIR=/var/tmp/arc2-l10r10-big`) and
sealed an envelope BYTE-IDENTICAL to the receipt committed at round 7:
sha256 `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`,
5204 B, `evidence_id
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608` (0 diff
lines). Wall 23min 58.082s (vs 1424.663s), 7.8G peak (vs 7.9G), `Result=success`,
journal `Consumed 42min 43.809s CPU over 23min 58.082s`. Binding: the envelope
kept one inode (2840144, birth 20:56:25.385370723) and read 0 bytes across 238
consecutive 5-second samples before becoming 5204 bytes at mtime
21:20:23.388139992, in the same second as the journal's completion line (the
journal records whole seconds, so it cannot order the two); the preserved
`ghidra.log` shows the disable pre-script at :276-278 and the bridge script at
:510-511. Therefore at this scale point the same request bytes re-derive both
the id and the bytes: content+params keying is confirmed, not merely asserted.
Scope: ONE scale point (91.6MB), one host, one date. The 17.7MB leg of the same
round is not a second scale point — it ran a different experiment and produced
no id (see the r6 entry's erratum). Residual, recorded not resolved: the
envelope path is a mode-0644 same-uid-writable regular file whose path was
published to 64 same-uid seats, and a sub-second overwrite between the genuine
write and the seal snapshot is not excluded by the file channel; the claim
rests on the systemd journal channel, which is root-owned and mode 0640 and so
cannot be written by uid 1000. Recipe caveat: `arc2-r7-pe.service` no longer
exists (`LoadState=not-found`), so this entry's cap and env are reconstructed
from prose and from the outcome identity below, not from a surviving unit file.
(arc2-loop1-round10)
```

Draft append-only erratum for `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md` (its
recheck line says "expect exit 0"; it omits the cap):

```markdown
Erratum (arc2-loop1-round10, 2026-10-18, append-only): this entry's hold is NOT
reproducible under a 9G cgroup cap, and the recheck line above omits the cap.
The round-10 mid leg ran the same target with this entry's recorded env
(`REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`, `GHIDRA_HEADLESS_MAXMEM=6G`, no
disabled analyzers, same npx cache `ad9a3fdbcad992c6`) inside a transient
service with `MemoryMax=9663676416` and `MemorySwapMax=1073741824`, and was
kernel-OOM-killed in 53.178s (`Result=oom-kill`, `MemoryPeak` byte-equal the
cap, 9G + 1G swap peak; typed `cancelled` envelope, `operation:
list_documents`, no `evidence_id`). The original round-6 leg ran UNCAPPED:
`/var/tmp/arc2-l6r6-E9-mid/run-leg.sh` is a plain bash runner using
`/usr/bin/timeout -k 60 5400` with no systemd unit, and its `meta.txt` records
`peak_tree_rss_kb=19149984` (18.263 GiB) at `exit_code=0` — incompatible with
any 9 GiB cap. The two runs are different experiments: this entry's hold needs
an uncapped host and is caller-coupled, which the round-7
caller-independent-services rule forbids. Rerun id-stability for this entry
therefore REMAINS UNKNOWN — the round-10 leg produced no id. Do not read it as
a refutation of this entry's hold. Corollary datum: the natural unmitigated
17.7MB analyze OOM-kills at 9G in 53.178s, extending the round-8 "no natural
hold at this cap" finding to a smaller target. (arc2-loop1-round10)
```

Draft claim-state wording for C1 (replaces the sealed/in-flight binary):

```markdown
Leg states are three, plus a recipe qualifier. SEALED = a result envelope with
an `evidence_id`, which alone may be counted as an id-stability data point.
TERMINAL-UNSEALED = the unit reached a terminal state without an `evidence_id`
(typed `cancelled`/`execution_failure`, or a cap kill) — a named debt, and NOT
the same as in-flight. IN-FLIGHT = no terminal state at close. A leg may be
counted only if SEALED *and* recipe-matched against the entry it re-runs;
recipe match means the same target digest, the same heap/deadline env, the same
analyzer preset, *and* the same containment (cgroup caps and launcher). Round
10: big leg SEALED + recipe-matched → one scale point, id-stability confirmed;
mid leg TERMINAL-UNSEALED + NOT recipe-matched (r6 ran uncapped) → no scale
point, r6's unknown stays open.
```

## 4. Observation / inference / unknown

- **OBSERVATION** — every `systemctl`/`journalctl`/`stat`/`sha256sum`/`diff`/`grep`/`lsattr`
  output quoted above; the 238-sample zero-byte series; the two-holder fd scan; the
  byte-identity with the round-7 receipt; the mid leg's `oom-kill` and zero `ev_`
  occurrences; the r6 `run-leg.sh`/`meta.txt` contents; custody 5/5; `LoadState=not-found`
  for `arc2-r7-pe`; the journal file mode `0640 root:systemd-journal`.
- **INFERENCE** — that the mid leg's 53.178 s kill is cap-bound rather than analysis-bound
  (from `MemoryPeak` byte-equal the cap, the memcg OOM journal line, and 53 s being far
  short of even the old ~900 s deadline); that the big leg's envelope was written by this
  run rather than placed (from inode continuity + the zero-byte series + the journal's
  resource record); that the big leg's recipe matches r7's (from journal argv form, npx
  cache path, `ghidra.log:276-278` agreement with E3's record, target digest, and the
  byte-identical envelope) — this is outcome-level identity, not a surviving unit file.
- **UNKNOWN** — whether the round-10 mid leg's 53.178 s kill time is stable (single run);
  whether a same-uid process overwrote `/var/tmp/arc2-l10r10-big/stdout.json` inside the
  ≤0.6 s window between the genuine write (21:20:23.388) and this seat's seal snapshot
  (21:20:24) — not excluded by the file channel, excluded only by the journal channel, so
  it is a named residual and not a clean bill; r7's actual `MemoryMax` (unit gone, journal
  silent — 9G is inferred from the family default and the 7.9G observed peak, not read);
  which in-unit process the kernel killed in the mid leg (java presumed, not captured); the
  r6 leg's rerun id-stability, which stays open.
- **NOT DONE / NOT MINE** — no repo file was edited; no seat counted the round-10 roster
  against the dispatch items array; no post-pair custody was taken; the C2 citation-drift
  and C3 hyper-lane census are other seats' scopes. The round-10 roster receipt
  (`.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt`) asserts 64 seats and is
  claimed pre-dispatch this round; I did not verify it against the dispatch items array.
