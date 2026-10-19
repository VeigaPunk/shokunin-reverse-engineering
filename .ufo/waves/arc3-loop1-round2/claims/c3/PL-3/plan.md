# PL-3 — C3 plan: custody receipt v2 tool (capture pre|post + verify; v2 fields; v1 back-compat; live-attack design)

Seat PL-3 · chain c3 (planner) · wave arc3-loop1-round2 · 2026-10-19.
Repo HEAD at writing: `14b1682b1128d2e41085ebc79c9addeb8786d420` (read-only `git rev-parse`).
Frozen claim under this plan: `.ufo/waves/arc3-loop1-round2/claims-frozen.md:52-64` (C3 —
custody receipt v2: epoch times, inode/ctime pins, label fix; v1 back-compat; live
same-content-rewrite detection; live pre/post pair exit 0, 5/5).

This plan is **measurement-first**: the implementer's tool landed mid-wave (EX-31,
`.ufo/gates/custody-pair/custody-pair.py`, 39,157 B, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`), so this seat's job
became: ratify the landed interface as the C3 contract, reproduce every claim component
first-hand against it on read-only/scratch substrates, and name the gaps that remain.
All evidence: `claims/c3/PL-3/measurements.txt` (sha256
`57bdff92e954fc419a36878b5d28097e0d897e570c1f77f646d61d36133d9d92`; this identity
line was re-derived after the file's last append — C1 rule #14 applied to itself).

## 0. Headline — what is already true, measured (not asserted)

1. **Tool + selftest.** `.ufo/gates/custody-pair/custody-pair.py` exists (mtime
   09:05 local), selftest **15/15 CLEAN, exit 0** in 0.18 s (`selftest` run at
   12:06Z; scratch `/dev/shm`, never `/tmp`). Interface: `capture`, `verify`,
   `selftest`, `paths`.
2. **Declared exit map** (docstring + measured): `0` MATCH, `10` CONTENT-DRIFT,
   `11` REWRITE-DRIFT (same-content rewrite), `12` METADATA-DRIFT (mode/uid/gid/
   size/type, LABEL-DEFECT, EXTRA-PATH), `13` ABSENT, `2` USAGE, `3` SELFTEST-FAIL;
   capture exits `13` when a requested path is absent (receipt still written).
3. **v2 field set landed** (per path, exact order): `PATH, EXISTS, TYPE, SIZE,
   SHA256, MTIME_EPOCH, MTIME_NS, MTIME_UTC_RENDER, MTIME_LOCAL_RENDER,
   CTIME_EPOCH, CTIME_NS, CTIME_UTC_RENDER, CTIME_LOCAL_RENDER, INODE, MODE, UID,
   GID`; header carries `receipt-version: 2`, the tool's own sha256,
   `captured-utc`/`captured-local`, `repo-HEAD`, label/compare contracts.
4. **Label fix proven.** Fresh read-only capture (C10, 12:07:30Z, landed revision)
   renders `MTIME_UTC_RENDER` = `gmtime(epoch)` for all 5 paths and keeps the local
   render separately; round-1's defect (epoch `1792011200` = `20:53:20Z` printed as
   `17:53:20` under `MTIME_UTC`) is now (a) unrepresentable in v2 and (b) *detected
   and named* `LABEL-DEFECT` when a v1 receipt carries it (C7/C9).
5. **Same-content rewrite detected (the claim's core).** On `/var/tmp` synthetic
   replicas: control `0`; in-place same-bytes rewrite → `11` `moved=mtime_ns`
   (nano-second pin catches same-second rewrites) with `SHA256-CONTRACT: 2/2 paths
   agree on sha256`; replace-by-rename → `11` `moved=inode`; `cp --preserve=all`
   forgery over rename → `11` `moved=inode` (mtime restoration does not help);
   chmod-only → `12` `moved=mode,ctime_ns`; content flip → `10`; removed path →
   `13`; tampered receipt (sha nibble flipped) → `10`. The sha-only comparator is
   blind on the same states (`sha256sum -c` → `OK`, rc 0) — the before/after pair
   is one scratch state, two verdicts.
6. **v1 back-compat measured against the landed tool** (live, read-only):
   `sums-v1` (EX-02 form) → exit `0`, `MATCH-V1-PARTIAL 5/5`, `SHA256-CONTRACT
   5/5`; `v1-stanza` (CU-1 receipt) → exit `12`, `SHA256-CONTRACT 5/5` + per-path
   `LABEL-DEFECT`; `pipe-v1` (CU-1 metadata sidecar) → exit `12`, same,
   `compared=3/11`. Grading rule in §3.
7. **Gaps (see §6 for full list).** (a) The earlier wave-level pre-pair receipt
   `claims/c3/receipts/config-pre-pair-v2.txt` (sha256 `fa9706c6…`, captured
   12:04:06Z by EX-32) records `# tool: … sha256 4862f642…`, i.e. a revision that
   predates the landed tool (`112d01dc…`); **EX-31's own pair
   (`claims/c3/EX-31/capture-pre.txt` 12:06:26Z / `capture-post.txt`) is captured
   by the landed revision** (its `identity-rederivation.out` re-derives the
   embedded hash = fresh `sha256sum`), so the claim's "captured by the tool" is
   satisfied chain-internally; the EX-32 receipt should be re-captured or
   annotated with the revision mapping (my recon capture 12:07:30Z shows **all 11
   per-path fields ALL EQUAL** to EX-32's receipt → any re-capture is provably
   drift-free). (b) `REWRITE-DRIFT`'s `moved=` detail is
   partial (first branch only; ctime movement reported only when inode/mtime did
   not move) — class correct, detail understated. (c) Exit map deviates from the
   house 0/1/2 convention; the registry row must state it (§7 patch text).

## 1. Interface contract (ratified as landed — this is the C3 deliverable shape)

```
python3 .ufo/gates/custody-pair/custody-pair.py capture --out <path|-> [--label L] [--paths P...]
python3 .ufo/gates/custody-pair/custody-pair.py verify <receipt-a> [--live | <receipt-b>]
python3 .ufo/gates/custody-pair/custody-pair.py selftest [--scratch DIR]
python3 .ufo/gates/custody-pair/custody-pair.py paths
```

- `capture` = the pre|post pair primitive (the seat line's "capture pre|post"
  interface): same command for both phases, `--label` distinguishes them
  (round-1 precedent: labels `PRE-PAIR`/`post-pair` in the header). Default path
  set = the 5 canonical paths, fixed order devin/omp/kimi/bashrc/profile
  (`paths` prints them; order matches the SOP).
- `verify` has two modes: **receipt-vs-live** (`--live`, re-captures fields of the
  paths *named in the reference receipt*) and **receipt-vs-receipt** (pre vs post,
  or vs an independent capture). Same exit map; severity precedence
  `CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`.
- Structural guarantees: read-only over every inspected path (sha256 + stat only);
  refuses to write a receipt over a custody path (exit 2); warns on `/tmp` output;
  selftest scratch defaults `/dev/shm` then `/var/tmp`, refuses `/tmp`.
- `atime` is deliberately excluded (self-mutating on read) — declared in the
  docstring and the receipt's compare-contract.

**Ratification note:** this section freezes the *shape* (verbs, modes, exit map,
field names). It does not freeze the code bytes: any future revision must re-derive
the receipt's `# tool:` line in the same commit (C1 rule #14 discipline — the
receipt records its producer's identity, and this wave's own pre-pair is already a
live instance of that rule firing, gap 7a).

## 2. v2 receipt fields — semantics and render rules

| field | rule |
|---|---|
| `MTIME_EPOCH` / `CTIME_EPOCH` | integer seconds directly from `st_mtime`/`st_ctime` |
| `MTIME_NS` / `CTIME_NS` | `st_mtime_ns`/`st_ctime_ns` — the operative pins (a second-resolution ctime is blind to a same-second rewrite; measured: in-place rewrite with no sleep still lands `11` via `mtime_ns`) |
| `MTIME_UTC_RENDER` / `CTIME_UTC_RENDER` | `time.gmtime(epoch)` → `…Z`; TZ-independent by construction (the v1 label fix) |
| `MTIME_LOCAL_RENDER` / `CTIME_LOCAL_RENDER` | the same epoch rendered in the host TZ, explicitly labeled — kept for operator legibility, never compared as UTC |
| `INODE` | `st_ino` — moves on any rename-replace, including same-content (`cp --preserve=all` cannot restore it) |
| `SHA256` | content contract (unchanged from v1) |
| `TYPE`, `SIZE`, `MODE`, `UID`, `GID`, `EXISTS` | metadata class (METADATA-DRIFT axis) |
| header `# tool: … sha256 …` | producer identity; **capture-time** value — if the tool is revised, the receipt describes the superseded revision and a new capture (or a recorded revision mapping + field-level diff audit) is required for any live-pair claim |
| sidecar `<receipt>.sha256` | receipt-integrity helper (self-hash); forgery-proofness is NOT claimed (unsigned, lane-authored — named limit in §6) |

UTC-render acceptance test (portable): for every block, `date -u -d @$MTIME_EPOCH
+%Y-%m-%dT%H:%M:%SZ` must equal `MTIME_UTC_RENDER` (my C10 cross-check: 5/5 AGREE;
round-1 EX-01 used the same form).

## 3. Back-compat rules for v1 receipts (measured; the claim's last clause)

Three v1 shapes are parsed (auto-detected; `A format:` line echoes the class):

1. `sums-v1` — `sha256sum` output (SOP canonical form, `<64hex>  <path>`),
2. `v1-stanza` — CU-1 block form (`PATH:/EXISTS:/SIZE:/MTIME_UTC:/MODE: … UID: … GID:/SHA256:`),
3. `pipe-v1` — CU-1 metadata sidecar form (`path | inode | ctime | mtime | size | blocks | sha256`).

Rules (as landed, ratified):

- **sha256 is the graded contract.** The `SHA256-CONTRACT: n/n paths agree on
  sha256` line is the field-level verdict for every v1 input. Measured at HEAD:
  5/5 on all three shapes (C7/C8/C9).
- **`MATCH-V1-PARTIAL`** = every comparable field agrees; `compared=n/11` states
  exactly how many fields the v1 input made comparable. Missing v2 fields are
  **never back-filled from a live read** (that would make the receipt
  unfalsifiable) — the tool reports the reduced compare count instead.
- **The label defect is detected, not inherited.** When a v1 receipt carries a
  time string next to a known epoch, the tool renders the epoch both ways and
  emits `LABEL-DEFECT`; the path classes as METADATA-DRIFT → aggregate exit `12`
  (C7/C9). This is the *desired* fail-closed reading: a v1 receipt carrying the
  round-1 defect must not read as a clean PASS.
- **Grading rule for the claim clause** ("v1 receipts remain verifiable against
  the tool's sha256 fields"): grade on `SHA256-CONTRACT 5/5` plus per-path class —
  `sums-v1` at exit `0`; time-carrying v1 forms at exit `12` **with** 5/5 on the
  sha256 contract and `LABEL-DEFECT` attributed to the receipt's defect, never to
  custody drift. A verifier that reports the v1 stanza as a clean pass is
  **wrong**; a verifier that refuses to compare sha256 at all is also wrong.
- **Absent live path against a v1 reference → `ABSENT` (13)**, never a skip
  (round-1 H1 lesson applied to receipts; EX-35's fixture `v1-absent-path.txt`
  expects exit 2 in its adapter proposal — under the landed tool the same case
  lands 13 via `verify --live`; reconcile when EX-35 runs against the landed tool).
- **Fixtures to use**: EX-35's `fixtures/v1-synth.txt`(+sidecar),
  `v1-corrupt-sha.txt`, `v1-absent-path.txt`, plus the real round-1 samples
  (paths+digests in my `measurements.txt` C7-C9 and EX-35 `backcompat.md`).
- **Supersession note**: EX-35's `proposed-v1-verify-adapter.patch.md` proposed a
  `--verify/--sidecar/--v1-tz` CLI and a 0/1/2 exit map. The landed tool covers
  the same cases with `verify <receipt> --live` and the 10/11/12/13 map; the patch
  text is **superseded as an interface** but stands as the v1 field-mapping table
  (its mapping matches the landed parser: sha/size/mode/uid/gid native, inode/
  ctime via pipe-v1 only, mtime_epoch never assumed UTC).

## 4. Live-attack design (for EX-33; scratch only — never a real custody path)

Substrate: `/var/tmp/pl3-r2/L` (synthetic replicas; the round-2 variant of round-1
VZ-3's scratch method). A byte copy of a custody path is **not** required and was
not used by this seat; if EX-33 wants one, it must copy (never rewrite) and say so.
Each attack is: fresh `capture --out <scratch>/pre.txt --paths <replicas>` →
mutation → `verify <scratch>/pre.txt --live`; record raw verdict lines + exit.

| # | attack | declared/measured class (landed tool) |
|---|---|---|
| A0 | control, no touch | exit `0`, `MATCH n/n compared=11/11` |
| A1 | in-place same-content rewrite (`read+write same bytes`, no sleep) | exit `11` `REWRITE-DRIFT moved=mtime_ns`; sha contract n/n agree |
| A1b | in-place same-content rewrite **with mtime restored** (`os.utime` back) | exit `11` `moved=ctime_ns` (EX-31 A1, `attacks.out`; ctime is the last witness) |
| A2 | replace-by-rename, same content | exit `11` `moved=inode`(+`mtime_ns`) |
| A3 | chmod-only (metadata, no content) | exit `12` `METADATA-DRIFT moved=mode,ctime_ns` |
| A4 | content flip (1 byte) | exit `10` `CONTENT-DRIFT moved=sha256` |
| A5 | path removed | exit `13` `ABSENT moved=exists` (severity: content-drift on another path outranks — declare which case asserts what) |
| A6 | receipt tamper away from live (flip a sha nibble in a scratch copy) | exit `10` `CONTENT-DRIFT` (my C6) |
| A6b | receipt tamper **to match live** (EX-33 J) | `verify --live` returns `MATCH exit 0` — the tool does not authenticate receipts; the capture-written sidecar (`sha256sum -c <receipt>.sha256`) is the available out-of-band check (EX-33 §4.1; named limit §6.4) |
| A7 | `cp --preserve=all` over rename (mtime restored) | exit `11` `moved=inode` — the mtime-restoration forgery fails on identity pins |
| A8 | v1 fixtures through `verify --live` | `sums-v1` → `0`; `v1-stanza`/`pipe-v1` → `12` + `LABEL-DEFECT`; never a clean pass |
| A9 | v1 label specimen (synthetic stanza with local render under `MTIME_UTC`) | exit `12`, `LABEL-DEFECT` printed with both renders — the defect is *reported*, the fix is *not retroactive* |

Report format for EX-33: per case, the exact command, the `VERDICT:` line, the exit,
and `sha256sum` of tool + receipt. An unrun case is not a passed case.

**Detection falsifiability (the one-state pair, use in the report):**
```
same scratch state, two comparators
sha256sum -c  → OK rc=0         (v1 method: BLIND)
custody-pair.py verify --live → REWRITE-DRIFT exit 11  (v2 method: DETECTED)
```
Measured in `measurements.txt` C1 (sha contract 2/2 agree *and* rewrite flagged).

## 5. Claim mapping (frozen component → measured status → owner)

| claim component (`claims-frozen.md:52-64`) | status at plan time | evidence / owner |
|---|---|---|
| `.ufo/gates/custody-pair/` exists as a committed tool | directory + tool landed (untracked: `?? .ufo/gates/custody-pair/`); commit is parent-side | EX-31; `git status` snapshot in `measurements.txt` |
| v2 receipt per path: sha256 + mtime epoch (UTC-rendered, correctly labeled) + inode + ctime | landed + measured (C10; field keys; UTC renders 5/5 AGREE) | EX-31 / this plan §2 |
| label defect gone | v2 cannot express it; v1 defect detected as `LABEL-DEFECT` | C7/C9/C10; EX-01 A4 (round 1) |
| live same-content rewrite detected (inode/ctime movement) | measured: `11` on in-place (mtime_ns), rename (inode), preserve-all forgery (inode) | this plan §4 A1/A2/A7 |
| v1 receipts remain verifiable against sha256 fields | measured: 5/5 sha contract on all three shapes; exit 0 (sums) / 12 (time-carrying, label defect reported) | C7/C8/C9; rule in §3 |
| the round's own live pre/post pair (exit 0, 5/5) captured by the tool | **EX-31's pair satisfies it** (`capture-pre.txt` 12:06:26Z / `capture-post.txt`, landed revision, `identity-rederivation.out` OK; pre↔post and pre↔live `MATCH 5/5 exit=0`); EX-32's earlier 12:04:06Z wave receipt carries the superseded tool sha — annotate or re-capture | EX-31 artifacts; EX-32 receipt; my C10 diff (all 11 fields equal) |

## 6. Residuals / named limits (for the records; none blocks the claim)

1. **Revision staleness on EX-32's wave-level receipt** (gap 7a) — its `# tool:`
   sha is `4862f642…`, predating the landed `112d01dc…`; EX-31's pair is on the
   landed revision. Annotate with the mapping + field-level diff (all equal) or
   re-capture (cheap, provably drift-free).
2. **`moved=` detail is partial** under REWRITE-DRIFT (first branch wins; ctime
   movement is listed only when inode/mtime did not move). Class correct; if the
   records quote `moved=`, quote it as "at least these fields".
3. **Exit map ≠ house 0/1/2** — extended 10-13 classes are deliberate; the
   registry row (§7) must carry the map so future consumers do not read `10` as a
   convention breach or `12` as a pass.
4. **Receipt authenticity is not claimed**: receipts are unsigned, lane-authored;
   an actor who can rewrite the receipt can make it match live — measured: a
   tamper-to-match receipt passes `verify --live` with exit 0 (EX-33 case J,
   `attack-rewrite.md:104-112`), while a tamper away from live is caught as
   CONTENT-DRIFT (my C6). The capture-written sidecar is the available
   out-of-band integrity check (`sha256sum -c <receipt>.sha256`); recommend the
   parent's records mandate it wherever a receipt's pristine bytes matter. The
   tool detects on-disk custody drift and receipt-vs-live mismatch, not
   adversarial inference about a co-resident writer (luna-round-9/10 precedent:
   a hash proves custody, not authorship). Sidecar = integrity helper, not a
   signature.
5. **TOCTOU**: capture and verify each read the path once; a write between the
   stat and the open is out of scope (single-machine operator configs; no claim).
6. **v1 receipts cannot retro-detect** a same-content rewrite that happened before
   the v1 capture (no pins); the tool says so by `compared=n/11`.
7. **`verify --live` trusts the reference receipt's path list** — a receipt edited
   to point elsewhere is compared at the pointed paths (A6 detects field forgery
   only when the live file disagrees; a consistent forgery is out of scope, §6.4).
8. `__pycache__/` re-created under `.ufo/gates/` and `.ufo/gates/custody-pair/` by
   module-import audits (hygiene note; exclude from any commit — round-1 SC-2
   precedent).

## 7. Proposed changes (patch text, not landed by this seat)

- `registry-row.patch.md` — SKILL.md "Local round-evidence gate registry" row for
  `custody-pair` (entry map incl. the 10-13 classes, self-invocation `selftest`,
  pinned values / write scope).
- `sop-amendment.patch.md` — the custody SOP v2 amendment (capture/verify
  invocations, v2 receipt as the primary artifact, v1 receipts verified-not-edited,
  label-defect rule, pair re-capture rule on tool revision).
- Records-side one-liner (for the parent's SCORECARD/LOG entry, not a patch file):
  "C3 operability — custody receipt v2: `.ufo/gates/custody-pair/custody-pair.py`
  (sha `112d01dc…`, selftest 15/15) emits sha256+epoch/NS+inode/ctime with UTC
  renders; same-content rewrites detected (exit 11 — three attack shapes measured);
  v1 receipts verify on the sha256 contract (5/5, three shapes; label defect
  reported as LABEL-DEFECT exit 12); live pre/post pair 5/5 (pre re-captured by the
  landed revision)."

## 8. Constraints honored

- Custody paths: hash/stat reads only (`capture`, `verify --live`, `stat`); no
  bytes of any custody path were copied, rewritten, or moved. All mutations ran on
  synthetic files under `/var/tmp/pl3-r2`.
- No git mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/README writes; artifacts
  written only under `claims/c3/PL-3/` and the seat report.
- No census scope change, no pointer-table widening (this chain touches neither).
