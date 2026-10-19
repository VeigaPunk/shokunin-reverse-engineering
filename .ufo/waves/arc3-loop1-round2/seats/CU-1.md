# SEAT CU-1 — chain cross, role custody (arc3-loop1-round2)

Task (seat line): corroborate the v2 custody pair (poll for EX-32's receipt):
recompute the 5 paths' sha256 + stat independently and compare; also corroborate
the round-1 v1 receipt's digests still match live.

Status at seat close (2026-10-19T12:33Z): **COMPLETE.** EX-32's authoritative
PRE-PAIR (12:04:06Z) corroborated; round-1 v1 digests corroborated live;
POST-PAIR captured by CU-1 at 12:31:44Z (EX-32's own post never landed in
`claims/c3/receipts/` — 21 polls, 12:11–12:31Z) and the pair verified by the
tool **MATCH 5/5 drift=0 exit 0** and independently graded **60/60** field cells
against a locally derived ledger. Zero custody drift across the 27.6-minute
window.

## 1. Work performed (evidence pointers)

All CU-1 artifacts: `.ufo/waves/arc3-loop1-round2/claims/cross/CU-1/`.
Read-only discipline: hash/stat only on the 5 custody paths; no byte copies of
custody content; scratch in `/var/tmp/cu1-r2`; no git mutations.

- **Independent live capture of the 5 custody paths** (three hash
  implementations + GNU stat + epoch↔UTC/local renders):
  `capture-1201Z.txt` (12:01:26Z, sha256 coreutils = openssl = python hashlib
  on all 5; LSTAT inode/mode/uid/gid/size; MTIME/CTIME with epoch + both
  renders).
- **Round-1 v1 receipt corroboration** — receipt bytes stable, digests still
  match live: `compare-v1-vs-live.txt`, driven by `expected-ledger.txt`.
  - `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
    recomputes to `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776`
    (matches round-1 seat claim, unchanged).
  - `…-metadata.txt` recomputes to
    `85fa1860000bda4de57ffb17219e59fa0e553d505eb76815c4bcf542f6426a90` (unchanged).
- **Label-defect reproduction (independent of the tool)**: my own epoch→render
  arithmetic, `label-defect-and-v1-vs-live.txt` — v1's `MTIME_UTC` fields are
  local (-03) renders; gmtime renders are +3 h.
- **Tool verification battery** against revision
  `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
  (`verify-battery-1206Z.txt`): selftest 15/15 CLEAN; `capture` 5/5 exit 0;
  `verify --live` MATCH 5/5 drift=0 exit 0; v1 stanza/pipe receipts vs live.
- **Self-integrity, TZ-independence, read-only and write-guard probes**:
  `tz-and-selfchecks.txt` (B5–B8).
- **EX-32 pre-pair receipt corroboration**: `corroboration-summary.txt`,
  `tool-capture-T0/T1/T2.txt` (+ tool sidecars), `tool-revisions.txt`.
- **Pair corroboration incl. EX-31's gate pair** (`claims/c3/EX-31/capture-pre.txt`
  / `capture-post.txt`) and the frozen gate identity (tool `112d01dc…`,
  `README.md` `fa484d57…`, 889 lines re-derived independently): §3c.
- **Wave-close post-pair capture + pair verification**: `config-post-pair-v2.txt`
  (12:31:44Z, `0443484d…`), `post-capture.out`, `pair-verification.txt` (§3d).
- **Handoff grader** (`grade-receipt.py` in this artifact dir) — grades any v2
  receipt against `expected-ledger.txt` (12 field classes × 5 paths incl. ns via
  `--ns`); selftest: EX-32 pre → `ALL FIELDS MATCH` exit 0; mutated scratch copy
  → `MISMATCH` exit 1. Usable by the parent to grade any replacement post-pair.
- Poll log: `poll-log.txt` (21 checks, 12:11–12:31Z).

## 2. Proposed changes

- **none** (custody seat writes no repo target; no patch text — the C3 target
  `.ufo/gates/custody-pair/custody-pair.py` is EX-31's and was under active
  revision during this seat's run: 4 observed revisions, so patch text from
  here would race). Three measured notes for EX-31/parent, all with file:line
  anchors in §4: (A6) exit-channel ambiguity on v1 references, (A7) write-guard
  scope under `--paths`, (A9) cwd-derived `repo-HEAD` provenance.

## 3. Before → after measurement

### 3a. v1 receipt digests vs live (task item 2) — 5/5 still match

Commands: `bash capture.sh` (read-only) at 12:01:26Z, then
`python3 compare-v1.py capture-1.txt`; output `compare-v1-vs-live.txt`.

| path | v1 sha256 | live sha256 (3 impls) | size/mode/uid/gid | inode (v1 meta) | ctime/mtime |
|---|---|---|---|---|---|
| ~/.config/devin/mcp_config.json | `16f496e6…263a4` | identical | match | 11341318 = live | match (local render) |
| ~/.omp/agent/mcp.json | `38d2a1d0…b926b` | identical | match | 11341316 = live | match |
| ~/.kimi-code/config.toml | `8cbacd48…73c38d` | identical | match | 34530637 = live | match |
| ~/.bashrc | `7d2ca28a…a26598` | identical | match | 25991953 = live | match |
| ~/.profile | `6c6be761…db4f30` | identical | match | 40274 = live | match |

`SUMMARY: inode eq 5/5; ctime==local 5/5; mtime==local 5/5` — i.e. not merely
same-content: the v1 pins for inode/ctime/mtime re-derive from the live
filesystem 2 h 4 min after capture, so no write (not even a same-content
rewrite, which would move inode/ctime) has touched any of the 5 paths.

### 3b. v2 pre-pair corroboration (task item 1) — 5/5 paths, 50/50 field cells

EX-32's receipt
`.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt`:
recomputed sha256 `fa9706c6f036e882ee1fe9e8589c4aa9fa7e60de65c6eaf4e2c8ac0949eba1c9`
= its tool-written sidecar = EX-32's report claim. Captured-utc 12:04:06Z,
repo-HEAD `14b1682b…`, embedded tool sha256 `4862f642…` (the revision live at
that instant).

Against my independently derived `expected-ledger.txt` (my own sha256sum/stat,
not the tool): **10 field classes × 5 paths = 50/50 match** (SHA256, SIZE,
INODE, MTIME_EPOCH, CTIME_EPOCH, MODE, UID, GID, MTIME_UTC_RENDER,
CTIME_UTC_RENDER), plus **MTIME_NS/CTIME_NS 5/5 + 5/5** against GNU stat's
nanosecond renders (`corroboration-summary.txt`).

Byte-level cross-checks (normalized = minus `# tool/captured-*/capture-label`
header lines):
- F1: EX-32 pre (rev `4862f642`, 12:04:06Z) vs my `tool-capture-T2.txt`
  (rev `112d01dc`, 12:08:12Z, cwd = repo root): **diff EMPTY**.
- F2: same vs my `tool-capture-T1.txt` (12:06:53Z): **diff EMPTY**.
- F3 provenance replay: I hold rev `4862f642`'s bytes (copied 12:04:11Z,
  `/var/tmp/cu1-r2/custody-pair.py`); re-running that revision at 12:09Z
  reproduces EX-32's receipt body exactly (**diff EMPTY**) — its embedded tool
  identity is verified, not just asserted.
- F4 capture determinism across rev A→B: **diff EMPTY**.

Also independent agreement at 12:01Z from peer captures: RV-12
(`claims/c3/RV-12/independent-pre.txt`) and VZ-3
(`claims/c3/VZ-3/live-baseline-1201Z.txt`) epoch/inode/sha values = mine.

### 3c. The v2 pair, as landed — all captures agree with the ledger

Every live capture on disk at 12:20Z, graded against my independent ledger
(`40/40` field cells each, i.e. 8 field classes × 5 paths):

| capture | written | tool rev (embedded) | sha256 | vs my ledger |
|---|---|---|---|---|
| EX-32 authoritative PRE-PAIR (`claims/c3/receipts/config-pre-pair-v2.txt`) | 12:04:06Z | `4862f642` | `fa9706c6…` | 40/40 |
| EX-31 `capture-pre.txt` | 12:06:26Z | `112d01dc` | `3f3db73e…` | 40/40 |
| EX-31 `capture-post.txt` | 12:06:26Z | `112d01dc` | `c0674f99…` | 40/40 |
| CU-1 `tool-capture-T1/T2` (third-party) | 12:06:53Z / 12:08:12Z | `112d01dc` | see files | 40/40 |

All five bodies are byte-identical to each other outside header lines
(normalized diff EMPTY) — including across tool revisions A→B.

**Measured caveat on EX-31's pair (my finding, not EX-31's claim):** the two
receipts carry the *same* `captured-utc: 2026-10-19T12:06:26Z`; their file
mtimes are `09:06:26.272851874` and `09:06:26.336717134` local — i.e. the pair
was two real runs **64 ms apart**. It exercises the pair mechanics (two
captures, `verify` MATCH 5/5 exit 0, diff = label line only — I re-diffed
independently, and the shipped `capture-pre-vs-post.diff` matches my byte diff)
but it brackets a 64 ms window, so it is not evidence that the 5 paths were
untouched across any working window. The window-bracketing capture for this
round is the EX-32-pre / CU-1-post pair in §3d. Whoever records the pair should
say which of the two readings of "the round's live pre/post pair" is claimed.

### 3d. v2 post-pair — captured by CU-1, pair verified (task item 1 complete)

EX-32's post never landed in `claims/c3/receipts/` (21 polls, 12:11–12:31Z;
`poll-log.txt`). At wave close (all 64 seat reports present) CU-1 captured the
post into its own chain dir (CU-1's write scope):

- `config-post-pair-v2.txt` — captured-utc **12:31:44Z**, tool `112d01dc…`,
  `repo-HEAD 14b1682…`, **exit 0, 5/5**, receipt sha256
  `0443484dd87bec7d8c8e90c871959ddd0744a02ea7b9ab1b1e1ba31f946439ad`
  (= its tool-written sidecar), label states it is the wave-close capture.
- `pair-verification.txt` (all commands + outputs):
  - P1 `verify <EX-32 PRE> --live` → MATCH 5/5, drift=0, **exit 0**.
  - P2 `verify <EX-32 PRE> <CU-1 POST>` → **MATCH 5/5, drift=0, exit 0** — the
    pair, verified by the tool.
  - P3 CU-1 grader on POST, 12 field classes × 5 paths incl. ns → **60/60,
    exit 0**.
  - P4 normalized byte diff PRE vs POST → **EMPTY**: zero drift across the
    27.6-minute window (12:04:06Z → 12:31:44Z), which spans the whole wave.
  - P5 digests: PRE `fa9706c6…`, POST `0443484d…`.

So the C3 claim component "the round's own live pre/post pair (exit 0, 5/5) is
captured by the tool" holds on an *independent-captor* pair (EX-32 pre + CU-1
post, both tool-produced), not merely on EX-31's 64 ms demonstration pair (§3c).

## 4. Attacks / refutations attempted (verdicts)

- **A1 "the round-1 v1 receipt was edited since round 1"** — REFUTED:
  self-digests recompute to the round-1 values (`b8ed1936…`, `85fa1860…`).
- **A2 "v1-vs-live digest match is a same-content-rewrite false negative"** —
  REFUTED: inode, ctime (and mtime) re-derive equal, not just sha256.
- **A3 "three 'independent' hashes are one implementation"** — avoided by
  construction: GNU coreutils 9.11 `sha256sum`, OpenSSL 3.6.4 `dgst`, Python
  3.14 `hashlib` — three engines, all equal on 5/5.
- **A4 "EX-32's receipt matches because it was copied from my capture"** —
  REFUTED on ordering + independence: EX-32 wrote at 12:04:06Z, before my first
  capture (12:04:39Z); RV-12 (12:01:12Z), VZ-3 (12:01Z) and EX-32's own lstat
  ground truth (12:01:48Z) independently agree.
- **A5 "the receipt could have been produced by a doctored tool"** — REFUTED by
  the F3 replay: the receipt's body is exactly what the revision whose sha it
  embeds produces on the live paths.
- **A6 "'v1 receipts remain verifiable against the tool's sha256 fields' (C3
  claim) holds cleanly"** — **PARTIAL; the strong reading fails.** The
  sha256-contract channel verifies (both v1 forms print
  `SHA256-CONTRACT: 5/5 paths agree on sha256`), but the *verdict* channel for a
  faithful v1 receipt compared against live or a v2 receipt is
  `VERDICT: METADATA-DRIFT … exit=12` — driven by `_label_audit` escalation
  (`custody-pair.py:470`) reproducing the round-1 label defect. So exit 12
  conflates "the paths drifted" with "the reference is a v1 receipt (label
  defect)". Measured on the real round-1 receipt (stanza form) **and** its
  metadata sidecar (pipe form), `verify-battery-1206Z.txt` §B3/§B4; EX-32's
  `battery-B1-B2.log` §B2 measures the same. Consequence for the claim text or
  for a caller: a script keying on exit 0 reads a faithful v1 baseline as
  drift. Nothing in the tool is wrong for the *v2 pair*; the gap is the v1
  verdict class.
- **A7 "the write-guard covers any path being captured"** — REFUTED for
  `--paths` overrides: the guard compares `--out` only against the canonical
  `CUSTODY_PATHS` (`custody-pair.py:563-565`). Measured: with
  `--paths X --out X` the tool overwrote X (scratch file, `tz-and-selfchecks.txt`
  §B8, exit 0 instead of USAGE). For the frozen 5-path contract the guard holds
  (selftest case 12 exercises it on `CUSTODY_PATHS[3]`, `custody-pair.py:816-824`).
- **A8 "the label fix is itself TZ-dependent"** — REFUTED: `MTIME_UTC_RENDER`/
  `CTIME_UTC_RENDER` byte-identical under `TZ=UTC`, `TZ=Asia/Tokyo`,
  `TZ=America/New_York`; the local renders differ correctly
  (`tz-and-selfchecks.txt` §B5).
- **A9 "repo-HEAD in the receipt is reliable provenance"** — REFUTED as
  run-order-sensitive: the stamp is `git rev-parse` of the cwd's enclosing repo.
  My `tool-capture-T1.txt` (run from `/home/vgpnk/Projects/shokunin`) recorded
  `repo-HEAD 553afae8…` (the outer fleet repo), not kaidoku's `14b1682…`; T2
  (run from the repo root) records `14b1682b…`, matching EX-32's receipt. Any
  post-pair capture must be run from the repo root (or the field ignored).
- **A10 "the tool churned mid-battery, so the numbers are mixed"** — handled,
  not refuted: every artifact carries the revision sha used; the battery ran
  wholly under rev `112d01dc`; the capture path is byte-stable across rev A→B
  (F4), and EX-32 documented a transient broken rev (`b10ad1c8`, `KeyError:
  'sha_agree'`, 12:04:40Z) that is not the revision any of my numbers come from.
- **A11 "read-only capture could still touch the paths"** — bounded: canary
  capture leaves mtime/ctime unchanged; atime advances (atime is deliberately
  not captured by the tool, `custody-pair.py:246-247`) — `tz-and-selfchecks.txt`
  §B7.

## 5. Blockers / gaps

- **EX-32's post-pair was never landed by its own seat** — gap closed by CU-1's
  own wave-close capture (§3d), which the parent can adopt or replace; if the
  parent prefers EX-32's, it must be captured after 12:31:44Z and graded with
  `grade-receipt.py`.
- **Tool revision churn** (4 revisions observed; EX-32 F1/F2): the pre-pair was
  produced by `4862f642` and my post by `112d01dc`. Capture bodies compare
  cleanly across revisions (F4), and each receipt self-records the revision that
  produced it; the pair's records should quote both embedded tool shas.
- **No custody-path drift observed at any capture** (12:01:26Z, 12:04:06Z,
  12:06:53Z, 12:08:12Z, 12:31:44Z): sha256/inode/mtime/ctime all equal from the
  first to the last; the pair's normalized diff is empty.
- **A6 exit-channel ambiguity** (v1 reference → exit 12 on unmoved paths) and
  **A7 write-guard scope** (`--paths` overrides bypass it) remain as named
  operability notes for any future revision of the instrument; neither affects
  this round's v2 pair, which verifies exit 0.
