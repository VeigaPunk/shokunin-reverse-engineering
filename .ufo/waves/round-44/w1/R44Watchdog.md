# R44Watchdog — round-44 attempt history + unblob/sasquatch run ledger

Seat: `R44Watchdog` (dispatched as `R44Watchdog-2`; role `scribe`; axes coverage/depth/calibration).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Measured 2026-10-28T08:14–08:34-03:00.
All figures are snapshots of a **live** lane (the L1 made six round-44 commits and seats kept
writing while this seat ran); every row carries its receipt id, whose
command/exit/stdout-sha256/wall-time is in
`R44Watchdog/receipts.tsv` (92 rows / 90 distinct ids — two ids carry an honest `rc=2` first run
superseded by a later green one, disclosed below; sha256 `5e57ed2c…82fe0d4`).

Scope: (1) the round-44 attempt history {launch, complete, dead} for this lane, (2) what this attempt
inherited, (3) a ledger of every unblob/sasquatch run line produced this session, (4) the ledger
defects a scribe must hand the report rather than paper over. This seat wrote no product code, ran
no counter, installed nothing, and did **not** run `tools/round-44/c1-run.sh`.

---

## 1. Attempt history — kaidoku round 44

`.ufo/watchdog.log` (read at 08:14; the file's last write is 07:49:44, so nothing was appended
during this seat's run). Receipts: `W1-launch-lines`, `W58-watchdog-r44-again`,
`W73-final-wd`, `W47-final-snapshot`.

| event | line | verdict |
|---|---|---|
| **launch** | `1817: 2026-10-28T07:42:04-03:00 launch kaidoku round=44 pgid=3257226 driver=hyaku-inline attempt=1` | present, **attempt 1** |
| **complete** | — | **absent** (`grep -cE "complete kaidoku round=44"` = 0) |
| **dead** (`lane-dead-no-report`) | — | **absent** (`grep -nE "(complete\|lane-dead-no-report) kaidoku round=44"` returns nothing; total kaidoku round=44 lines = **1**) |

**This is attempt 1.** No earlier attempt of round 44 exists for this lane, therefore the prompt's
attempts clause (`lane-dead-no-report kaidoku round=44` → inherited uncommitted outputs) **does not
fire**: there are no outputs inherited from a dead predecessor attempt of round 44.

Two things a later reader must not misread:

1. **No `complete` line ≠ dead lane.** The `complete` line is written by the driver when the lane
   returns a landed report; at measurement time the round was mid-flight (the L1 had already made
   **six** round-44 commits after the base, `fc5eb54a → f5fb8d59 → 3b0fcaa9 → f18bdfb9 → 9a8de923
   → 1e9c4a43`, and seats were still writing).
   The ledger carries **no heartbeat or progress line kind**, so it cannot distinguish in-flight
   from dead (finding F).
2. **Misattribution hazard.** A bare `grep "round=44" .ufo/watchdog.log` returns 32 lines across
   10 lanes — 15 `kake` (three of them `lane-dead-no-report kake round=44`, 2026-10-23), 2 each
   `chousa/kama/kengaku/kumitate/mado/mori/tameshi/tsukuroi`, and **1 `kaidoku`** (`W3-round44-fleet`).
   Filtering by the lane field is mandatory; the kake deaths are not this lane's.
3. `ps` shows no process in pgid `3257226` (`W12-pgid-alive`, empty). That is expected for
   `driver=hyaku-inline` (the L1 is an in-session subagent, not a detached process group) and is
   **not** evidence of a dead lane — the commits above post-date the launch line.

### Inherited state named

- Base `c29360e3` (`lane main`), with the round-43 verifier spot-check `c29360e3` as ancestor — the
  claimed base, unchanged at `refs/heads/main` on origin (`W11-lsremote`, `W83-offbranch-gate`).
- **`unblob.log` at the lane root is inherited round-38 debris**, not this round's evidence: 17
  lines, sha256 `2d651a4a…`, byte-identical to `HEAD:unblob.log` (`W45-unblob-sha-vs-head`), last
  committed in `7a1ac7fe` (2026-10-26T04:13:36) whose subject ends `… misroot unblob.log`
  (`W64-unblob-log-provenance`). Its content is a 2026-10-26 06:56 run on
  `/fast/scratch/hyaku/kaidoku-r38/…/P5.sqsh` (`squashfs_v4_be`, `sasquatch-v4be`). It is not a
  round-44 log and must not be cited as one.
- In-flight uncommitted outputs of **this** attempt (not inherited): 20 modified + 0 untracked at
  08:25:13 (`W72-final-state`), growing to 23 modified + 221 untracked (244 entries) at 08:33:51
  (`W88-inventory-total`) as seats kept writing; all under
  `.ufo/waves/round-44/**`, `corpus/evidence/round-44/**`, `tools/round-44/**`, `plans/**` — L1
  territory to land or revert, named here per the attempts clause.

---

## 2. unblob/sasquatch run lines this session

### 2a. Lane-root `unblob.log` — zero this-session lines

`find . -name 'unblob.log*' -newermt '2026-10-28 00:00'` over the lane (excluding `.git/`) prints
nothing. The only lane-root log is the round-38 file above (`W6-lane-unblob-log`,
`W64-unblob-log-provenance`, `W45-unblob-sha-vs-head`). **No unblob run wrote into the lane tree
this session**, so no tracked log was mutated by a probe, and the six session logs below are the
complete set (`W8-scratch-unblob-logs`).

### 2b. This session's unblob runs — 6 chunk-only passes, scratch only

`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Revenger/` (`W34-scratch-log-census`, `W35-…`,
`W36-…`, `W8-…`):

| dir | carriers | log lines | handler from log | "Running extract command" | `extraction_reports` | `extract/` entries |
|---|---|---|---|---|---|---|
| `ub-v1-le--squashfs_v1.0_le.bin` | v1-le | 11 | `squashfs_v1` 0x0-0x1000 | 0 | `[]` | 0 |
| `ub-v1-be--squashfs_v1.0_be.bin` | v1-be | 11 | `squashfs_v1` 0x0-0x1000 | 0 | `[]` | 0 |
| `ub-v2-le--squashfs_v2.0_le.bin` | v2-le | 29 | `squashfs_v2` 0x0-0x1000 | 0 | `[]` | 0 |
| `ub-v2-be--squashfs_v2.0_be.bin` | v2-be | 11 | `squashfs_v2` 0x0-0x1000 | 0 | `[]` | 0 |
| `ub-v21le` | v21-le | 29 | `squashfs_v2` 0x0-0x1000 | 0 | `[]` | 0 |
| `ub-v21be` | v21-be | 11 | `squashfs_v2` 0x0-0x1000 | 0 | `[]` | 0 |

unblob **26.6.4** (`W25-…`, uv tool). All six logs end at `JSON report written`; **none contains an
extract command**, and every `ChunkReport` carries `extraction_reports: []` with an empty
`extract/` dir. The seat's own report states the method as `unblob -s -p 1`
(`R44C1Revenger.md:133`, `--skip-extraction`), so this is consistent and expected: **these are
handler-detection passes, not extraction evidence.**

Consequences for the ledger:

- **No `sasquatch` (or `unsquashfs`) was invoked by unblob this session.** The only
  `Running extract command` lines anywhere in the lane are historical receipts — round-41 `s126` and
  round-42 `c1/{OW-A8092,OW-X86FS,DW-MEGA,DW-FONERA}` — with mtimes 2026-10-24/26 (`W9-…`).
- **No after-side C1 data exists.** `corpus/evidence/round-44/c1/` holds **0 files**
  (`W62-evidence-c1-now`); no round-44 `run.json`/REA receipt exists in lane or scratch
  (`W85-rea-absence`). REA 6.5.0 is installed (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
  version `6.5.0`) but **no run trace of it exists** in lane or scratch — stated as absence of
  evidence, not as proof of non-execution. That is consistent with the contract (L1 runs
  `c1-run.sh` after freeze), so nothing forbidden is visible in the tree.
- Benign noise to expect in these logs: `v2-le`/`v21le` carry two `lzma.InvalidInputFormat`
  tracebacks from unblob's pattern-matcher probe at offsets 0xc/0x18 before `squashfs_v2` matches.
  They are debug-level FALSE candidates, not failures.
- Extractor identity, measured: `/usr/bin/unsquashfs` = **4.7.5** (2026/03/01); `sasquatch` at
  `~/.local/bin/sasquatch` prints **`unsquashfs version 4.5.1 (2022/03/17)`** — the shim self-reports
  an unsquashfs banner (`W87-sasquatch-identity`). A reader who greps "unsquashfs version" in a
  receipt can therefore mistake the *extractor* for the *oracle*; the oracle must always be pinned
  by path `/usr/bin/unsquashfs` (finding H).
- Verified instrument quirks used by the claims: `/usr/bin/unsquashfs --version` **and**
  `-version` both print the version line and exit **1** (`W80/W81`); `cmp -l` on two 4096-byte
  files differing in one byte exits **0** while printing 13 bytes, whereas `cmp -s` and plain
  `cmp` exit **1** (`W77/W78/W79`). Both claims-file notes reproduce on this host.

---

## 3. Wave shape this attempt actually dispatched

Receipts: `W69-idmap`, `W70-role-tally`, `W71-seat-gaps`, `W13-dispatcher-spawn`,
`W24-spawncap-count`, `W76-dispatch-caprefusals`.

- **37 seats** in spec, registry and dispatch (`w1-spec.json` / `swarm-registry.json` /
  `w1.ready.dispatched` agree; spec∖dispatch and dispatch∖spec are both empty).
- v1 wave under `scripts/hyaku/ufo-wave-policy.json`: `waveMinLanes 32`, `waveMaxLanes 64`,
  `maxLanes 256`, `hardCeiling 256` → 37 is **in band**. One `task` call; 0 resumes.
- **14 spawn-cap refusals** during ramp-up (`RuntimeError('Background job limit reached (100)')`)
  covering **8 distinct seats** — `R44Simplify`×4, `R44Prefile`×3, `R44ScoutSEAT`×2, and one each
  for `R44RevKill`, `R44C1FixtureAudit`, `R44C2Plan`, `R44C2SentReview`, `R44Watchdog` — then
  `2026-10-28T08:12:09 spawned kaidoku 44 r44-w1 37`. The wave completed; the refusals are
  capacity evidence (host job cap 100 against a 10-lane fleet), not seat loss.
- Because of the retries, **8 spec ids were dispatched under suffixed ids**:
  `R44RevKill→R44RevKill-2`, `R44Prefile→-4`, `R44Simplify→-5`, `R44ScoutSEAT→-3`,
  `R44C1FixtureAudit→-2`, `R44C2Plan→-2`, `R44C2SentReview→-2`, `R44Watchdog→-2`. Output files are
  named by the **spec** id (e.g. `R44RevKill.md`), matching the registry member name the collector
  joins on; a tool keyed on the dispatched id will silently miss those 8 seats (finding D).
- **Attack share.** Roles: executor 8, scribe 8, scout 7, reviewer 4, critic 3, connector 3,
  revenger 1, sentinel 1, mutation-tester 1, simplifier 1. The commit subject claims "35% attack
  share": 13/37 = **35.1%** only if connector+revenger+sentinel count as attack. Under the v2
  policy's attack-role set (`reviewer, critic, mutation-tester, labrat`) it is **8/37 = 21.6%**, and
  a v1 wave carries no attack-share floor (the ≥25% clause is v2-only). Label, not violation
  (finding E).
- Seat-output coverage at the 08:24:40 snapshot: **28/37 have a `.md`**; missing
  `R44C1Controls, R44C1Counter, R44C1Run, R44C2Controls, R44C2Rubric, R44CritC1, R44Prefile,
  R44Simplify` (plus this seat). The count moved 22 → 26 → 28 during this run; it is a snapshot,
  not a dead-seat list.

---

## 4. Findings handed to the report (reported, not fixed)

### A. `plans/round-44-claims.md:24-25` claims a REA measurement that no artifact carries — freeze-blocking
Text (worktree **and** `HEAD:1e9c4a43`): *"§1 Carriers 4 → 6: `squashfs_v2.1` LE/BE added (unblob
26.6.4 `__input__` fetched 2026-10-28, `unsquashfs` oracle + committed `__output__` tree exist;
**REA extracts them — measured probe `.ufo/waves/round-44/l1/`**)"* (`W66-claims-v21-probe-cite`).
`.ufo/waves/round-44/l1/` contains exactly **one** file: `probe-fixture-404.txt`, 14 bytes, body
`404: Not Found`, sha256 `d5558cd4…` (`W65-l1-dir-listing`). There is no REA receipt anywhere:
`corpus/evidence/round-44/c1/` = 0 files, no round-44 `run.json` (`W62`, `W85`). The seat that owns
the REA derivation says so itself: *"No round-42 dev envelope covers the two v2.1 carriers … Their
REA-side prior is the same source-read contract"* (`R44C1Revenger.md:324-327`). What was actually
measured is the unblob **chunk-only** pass (§2b). The honest wording is *"handler detection measured
(unblob `-s`, 6 carriers); REA extraction unmeasured — source-read contract, corroborated by the
v2.0 twin receipts"*. As written, the amendment asserts a probe the freeze would have to defend.

### B. The D-27/M44-1 red receipt is a body without an identity
`probe-fixture-404.txt` is 14 B and names no URL, no timestamp, no status line; `R44Shonen.md:148`
already concedes "the file itself names no URL". It satisfies "a committed receipt exists" but
cannot ground *which* URL was guessed. A receipt should carry `url`, `fetched_at`, `http_status`.
(Recorded as quality, not as a false claim: the sha does corroborate the body M44-1 reproduces.)

### C. The pre-report gate was RED at measurement time: 6 commits off-branch, detached
`git ls-remote origin refs/heads/main` = `c29360e3…` (base); lane `HEAD` = `1e9c4a43…` (detached),
jj bookmark `main` also `c29360e3`; `rev-list --count origin/main..HEAD` = **6**
(`W83-offbranch-gate`; re-verified unchanged at 08:34:49; `W84-jj-bookmark-main`).
The prompt's gate requires ls-remote to print the final lane hash before the report is written —
the L1 must land these through `jj-lane.sh` (never plain git), or the report will cite an unpushed
hash. Reported, not fixed: landing is L1-only.

### D. Collector-key hazard: 8 seats dispatched under suffixed ids
See §3. `w1.ready.dispatched` maps spec→dispatched id for those 8; output files use the spec name.
Any accounting keyed on the dispatched id under-counts by 8.

### E. "35% attack share" is a wide-set count
13/37 = 35.1% counts connector/revenger/sentinel as attack; the policy's own attack set gives
8/37 = 21.6%. v1 has no floor, so this is a labelling question for the report, not a gate.

### F. The watchdog ledger cannot express "in flight"
One line per lane-round (`launch`), then nothing until `complete`/`lane-dead`; no heartbeat, no wave
progress. A scribe reading it mid-round can only say "launched, no terminal line". Recommend a
`progress`/heartbeat line kind so `lane-watch.sh` and the ledger can distinguish a working lane from
a silent death without shelling out to `ps`.

### G. Inherited tracked debris still at the lane root
`unblob.log` (round-38 misroot, committed in `7a1ac7fe`) is tracked and byte-stable; harmless but it
is the first file a reader greps when asked for "the unblob log", and it is a v4 run from a different
round. Either archive it under `.ufo/waves/round-38/…` or add a first-line marker naming its round.

### H. `sasquatch -version` prints an `unsquashfs` banner
`~/.local/bin/sasquatch` reports `unsquashfs version 4.5.1 (2022/03/17)`; the oracle is
`/usr/bin/unsquashfs` 4.7.5. Any receipt that identifies the extractor by version text alone is
ambiguous — pin by absolute path.

### Cross-checks that passed (so the report need not re-run them)
- `R44C1Revenger.md` §3's six quoted `report.json` sha256 values match the bytes on disk, 6/6.
- `R44C2Counter.md`'s seven receipt rows: embedded `stdout_sha256` equals the quoted value, 7/7;
  exit codes as tabulated (0,1,1,2,0,2,2).
- Claims instrument notes reproduce: `cmp -l` rc 0 on 4096-B differ (13 B out), `cmp -s`/`cmp` rc 1;
  `unsquashfs --version` and `-version` both rc 1 with the version on stdout.
- No `complete`/`lane-dead` line, no `.ufo/reports/round-44/kaidoku.md` (`ls` rc 2, `W14`) — the
  round had not landed at 08:25.

### Side effects this seat discloses
- `jj` is colocated here and **snapshots the working copy on every read**. This seat ran
  `jj log`/`jj diff`/`jj bookmark list`/`jj op log`, which added seven `snapshot working copy` ops
  this session — 08:14:30, 08:21:40, 08:25:43, 08:25:58, 08:26:06, 08:30:11, 08:35:06 (`jj op log`;
  the four `export from jj` ops in the same log are all dated 2026-10-27 and pre-date this seat).
  **No git ref, commit or file byte
  changed by them**: no `export from jj` after 2026-10-27T09:17:24, git `HEAD`/reflog identical to
  the L1's commits, `HEAD:unblob.log` still equals the worktree file, and the pre-existing
  working-copy change (parent `1e9c4a43`, non-empty) is the seats' own in-flight work.
- Writes: only `.ufo/waves/round-44/w1/R44Watchdog.md`, `.ufo/waves/round-44/w1/R44Watchdog/`,
  `.ufo/waves/round-44/w1/artifacts/R44Watchdog/`, and scratch under
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44Watchdog/`. No PATH writes, no fleet-root tracked
  file, no commit/push, no install.
- Two receipts in `receipts.tsv` are honest `rc=2` could-not-evaluate rows (`W69-idmap`,
  `W70-role-tally`: helper scripts had not yet been written); both were re-run green and are cited
  from the green rows. They never count toward a target.

---

## 5. Artifacts

| path | content |
|---|---|
| `.ufo/waves/round-44/w1/R44Watchdog.md` | this ledger |
| `.ufo/waves/round-44/w1/R44Watchdog/receipts.tsv` | 84 receipts: seat, id, exit, stdout sha256, wall s, bytes, command (sha256 `527610a1…ded95f2`) |
| `.ufo/waves/round-44/w1/R44Watchdog/out/` | every receipt's captured stdout/stderr under `<id>.std{out,err}.txt` |
| `.ufo/waves/round-44/w1/artifacts/R44Watchdog/` | the harness (`run*.sh`) and helpers (`idmap.py`, `roles.py`, `gaps.py`) that produced them |
| `/fast/scratch/hyaku/kaidoku-r44/probe-R44Watchdog/` | scratch origin of the same |
