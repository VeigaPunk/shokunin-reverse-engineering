DEFECTS FOUND — the R42LocalSrc pack's *bytes* are verified correct and landable, but FIX-FIRST on two
claim/procedure points before landing: (1) P43-C2's "every copy's digest re-verifies against the live host
object" is unreachable as written — two host sources named by the map are GONE today (go-1.24.6, go-1.25.0
toolchain dirs) and a third never existed (rea-agents 6.7.0 npx dir); (2) gate exit-0 alone is provably not
sufficient for P43-C2 — the gate greens a stub pack on all 18 rows (none carries a URL-cell pin), so the
landing needs the structural lint I wrote, not just the gate.

Seat: R43RevLocalsrc (adversarial review of `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/` before it lands).
Base probed: `6b9e64fe7e0de202d9383baad5792fbfe039a743`; lane HEAD during review `d22686e1`.
Gate rev pinned by the pack's receipts: `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (129-row SOURCES.md).
Copy destination: `corpus/evidence/round-42/local-sources/` (per L1 correction 2026-10-27; the prepared map's
own `copy` fields). All scratch under `/fast/scratch/hyaku/kaidoku-r43/w1-R43RevLocalsrc` (removed at exit).

## (1) Artifacts dir vs git — every byte present and digest-identical

```
git -C <lane> ls-tree -r 6b9e64fe… -- .ufo/waves/round-42/w1/artifacts/R42LocalSrc | wc -l   → 35
find <same dir> -type f | wc -l                                                            → 35
find <same dir> -type l | wc -l                                                            → 0  (no symlinks)
git log 6b9e64fe..HEAD -- <dir>                                                            → empty
git status --porcelain -- <dir>                                                            → empty
```
Per-file `git hash-object` vs tree blob: **35/35 identical, zero mismatches** (script: for each `ls-tree` row,
`git hash-object "$path"`; output ended "digest check done" with no MISMATCH lines). Git modes: 32×100644,
3×100755 (the three build scripts). No commits since the base touched the dir.

## (2) sandbox-gate.sh re-run today — green, modulo one crashed helper

`bash …/build/sandbox-gate.sh <A> $S $S/receipts/rerun` — clone+place only, no lane writes, no commits.
Receipts in `artifacts/R43RevLocalsrc/receipts/sandbox-gate-rerun/`:

| step | script label | exit | meaning |
|---|---|---|---|
| A | gate-pristine | 1 | no copies → 18 rows fail (negative control) |
| B | gate-with-copies `--rev c4a38ea` | **0** | the claim's green state |
| C | gate working tree | 0 | same, unpinned table |
| D | verify-copies.py | **1** | **CRASH — see defect F2** |
| E | one corrupted copy | 1 | `copy-digest-mismatch` on S056 |
| F | one dropped map entry | 1 | `no-copy-named` on S007 |
| G | restored | 0 | green again |

Every receipt identical in shape to the pack's own committed `build/receipts/` (exit codes, rows_failed,
rows_total=129 all equal). Gate tool itself proven frozen: sha256 of
`tools/round-41/local-source-gate.py` = `cafe232a196dd8…` identical at first commit `d764389e` (round-41
freeze), HEAD, and disk.

## (3) Round-38 stub attacks — constructed in a sandbox clone, gate exit measured

Attack clone `git clone --shared <lane>` + `cp -a <pack>/corpus/. clone/corpus/`; gate run with
`--rev c4a38ea --json`. Driver `artifacts/R43RevLocalsrc/bin/attacks.sh`; per-attack JSON receipts in
`receipts/attacks/`; summary `receipts/attack-summary.tsv`.

| attack | gate exit | rows_failed / reason | verdict |
|---|---|---|---|
| baseline (pack as-is) | **0** | none | — |
| A. copy file deleted (S007) | 1 | `copy-missing` | gate catches it |
| B1. symlink→wrong in-lane file | 1 | `copy-digest-mismatch` | catches (via digest) |
| B2. symlink→in-lane file, right digest | **0** | none | **PASSES — defect F3** |
| B3. symlink→**out-of-lane** host source | **0** | none | **PASSES — worst case: "copy" IS the source** |
| B4. dangling symlink | 1 | `copy-missing` | catches |
| C1. copy at `tools/stub-copy.bin` (in-lane, wrong dir) | **0** | none | passes — dir is convention-only for the gate |
| C2. copy inside `.git/` | **0** | none | passes — uncommittable path still greens the gate |
| D1. pinned row S126, stub copy, row digest kept | 1 | `copy-digest-mismatch` | pinned rows are safe |
| D2. pinned row S126, map sha := stub digest | 1 | `row-pin-conflict` | pinned rows are safe |
| D3. **unpinned** row S007, stub copy + map sha := stub | **0** | none | **PASSES — the whole 18-row class, see F4** |
| E. alias: S040 entry → S056's copy+digest | **0** | none | passes — alias not checked |
| F. duplicate JSON key (stub first, good second) | **0** | none | passes — `json.load` keeps LAST; undetectable in the parsed map |
| G. copy is a directory | 1 | `copy-not-a-regular-file` | catches |
| H1. `../..` escape | 1 | `copy-outside-lane` | catches |
| H2. absolute copy | 1 | `copy-outside-lane` | catches |
| H3. copy := the external path | 1 | `copy-outside-lane` | catches |
| I1. orphan entry (unreferenced key) | 0 | none | harmless |
| I2. unknown key inside entry | 2 | GateError | catches (whitelist) |
| I3. map absent | 1 | all 19 `map-missing` | catches |

**Why D3 matters: zero of the 18 new rows carries a URL-cell digest pin** (extracted with the gate's own
`external_paths`/`digests_in`; only S126 pins, in its URL cell). For all 18 rows the map's `sha256` field is a
self-assertion: a 21-byte stub file plus `sha256=<digest of that stub>` exits 0. The gate is a *consistency*
check between map and bytes, not a *provenance* check — except where `source_sha256` happens to fire, and it
only fires on file-kind sources that still exist (see F2). This is exactly the round-38 lesson's stub class
(M38-6: a green counter that cannot tell real evidence from a stub) — dischargeable, but only by a
landing-time verifier, which is what the pack's `verify-copies.py` was for and what now crashes.

## (4) Map ↔ rows binding audit — exactly-one-copy holds

`artifacts/R43RevLocalsrc/bin/probe.py` drives the frozen gate's own parser over SOURCES.md (working tree and
base rev): 19 out-of-lane host paths across 19 rows (S035×2 paths, S082×3, plus S066/S070 sharing one path and
S048/S079/S090/S092 sharing the dist dir). The prepared map has **18 keys — set-equal to the path set**
(`missing=[] extra=[]`), `version: 1`, **no duplicate keys at any level** (object_pairs_hook scan), **all 18
`copy` strings unique** (no aliases), **every copy under `corpus/evidence/round-42/local-sources/`** except the
preserved S126 copy `corpus/evidence/round-41/s126/lead1-avm-image.tsv` (already committed in-lane, digest
`f205807d…` verified). All 20 copy paths resolve to regular files with map-matching sha256.

## (5) Size bound and content class — clean

Largest copy: `S048/rea-agents-6.5.0-dist-cited-members.tar` 2,048,000 B < 5 MiB; all others ≤ 719 KiB.
Content sniff over all 18 pack files + every tar member: markdown/JS/Go/Java/pacman-desc/JSON only — **no
SquashFS magic, no ELF, no firmware bytes anywhere** (the lane's own 4 KiB `avm-be.squashfs` dev fixture lives
beside the S126 dir, is not part of this pack, and is not named by any row). All 6 tars deterministic: sorted
member order, mtime=0, uid=gid=0, empty uname, GNU format — matching the map's notes.

## (6) Fresh re-verification of copies vs sources — all proven, but not the way the claim says

`artifacts/R43RevLocalsrc/verify-copies-r43.py` (hardened port of the pack's verifier; writes nothing to the
lane; run: `--root <attack-clone> --rev c4a38ea --upstream-dir $S/dl/go --tarball $S/dl/rea6.7.0.tgz`):
**130 checks, 0 failures** — full receipt `receipts/verify-r43.tsv`.

- 7 file copies `byte-identical` vs live host (S001,S002,S006,S007,S040,S056,S066,S083,S082×2) + S126.
- `source_sha256` re-verified against live host where recorded: S003 zip, S023 json, S082 extra.db, S126 tsv — all equal.
- S023 gzip decodes to the row-pinned digest `54d10162…`.
- All 30 member-pins from the rows' anchor cells reproduce inside the tars.
- S003 tar == live `Base-src.zip` (2 members); S048 tar == live rea-agents 6.5.0 `dist/` (23 members);
  S082 tar member == live `extra.db` member (1246 B).
- **S035: both host dirs are GONE** (`/home/vgpnk/.local/opt/go-1.24.6` and `go-1.25.0` do not exist; the host
  now has only `go1.27.3`). Proven instead against upstream: all 28 members of each tar byte-equal
  `raw.githubusercontent.com/golang/go/{go1.25.0,go1.24.6}/src/internal/abi/…` (56 fetches, manifest
  `receipts/go-upstream-sha256.tsv`).
- **S081: host npx dir never existed** (the map's note already says so). Proven against the official tarball
  `rea-agents-6.7.0.tgz` sha256 `20958a66…` (== the row's own pin; all 3 members byte-equal).

## Findings

- **F1 (claim text, medium):** P43-C2's clause "every copy's digest re-verifies against the live host object
  it copies (fresh row-pin audit, this round)" is **unreachable for S035×2 and S081** — those live host
  objects are absent today. Substitute re-verification exists and is stronger (upstream tags + pinned npm
  tarball, proven above). Fix: amend the clause to "re-verifies against the live host object where it exists,
  else against the published pinned artifact the row itself cites", or re-install the two Go toolchains
  before the freeze. The R42-built `verify-copies.py` also crashes hard (FileNotFoundError, traceback) on an
  absent host source — it must not be re-used as the landing check; `verify-copies-r43.py` in my artifacts
  tolerates absence and falls back to upstream/published artifacts.
- **F2 (procedure, medium):** the sandbox-gate receipt's step D has masked this since round 42 —
  `verify-copies.py` exits 1 by *crash*, and `sandbox-gate.sh` still exits 0 (it only echoes the exit).
  Today's re-run of the script reproduces the crash verbatim (receipt `sandbox-gate-rerun/verify-clone.tsv`).
- **F3 (predicate gap, medium):** the gate passes a `copy` that is a **symlink** — including a symlink *out
  of the lane to the source file itself* (B3) — and a copy living outside the stated dir or inside `.git`
  (C1/C2). git commits symlinks, so a landed pack could technically contain one and still green. P43-C2's
  "in-lane regular-file copy under …/local-sources/" therefore requires the structural lint (lstat, dir
  prefix, uniqueness, dup-key scan) my verifier implements; gate exit-0 alone does not state it. The pack as
  committed contains zero symlinks and all copies are in the stated dir — verified.
- **F4 (predicate gap, medium):** with no URL-cell pins on the 18 rows, the gate cannot distinguish the real
  pack from a stub pack (D3=exit 0, E=exit 0, F=exit 0). CTL-C2-1's "map entry whose copy is absent or
  digest-mismatched keeps the gate red" is proven (01, 08, 09 all exit 1) — but the *landing* predicate must
  cite the verifier, not the gate, for copy authenticity; the claim's counting command remains correct as a
  counting command.

No defect in the pack's bytes, map shape, digests, determinism, or coverage of the 18 rows. The pack is the
right pack; the claim needs the two wording/procedure fixes so the freeze means what it says.

## Limits

- Upstream substitution for S035 rests on GitHub serving the true tag contents (transport-verified fetches;
  member digests recorded in `receipts/go-upstream-sha256.tsv`). [INFERENCE: golang/go tag immutability is
  assumed, not re-proven.]
- The gate `--rev` reads SOURCES.md at `c4a38ea` (129 rows) for the pack receipts and at base `6b9e64fe` (134
  rows) for the freeze prediction; both give exactly the 18 rows on `rows_failed`, so the row-count delta is
  benign (`rows_total ≥ 129` holds either way).
- Pacman `extra.db` on this host is frozen by the host-wide transaction pause, so its `source_sha256` still
  verifies; if it ever rolls, that row re-rends red *advisory* only (gate exit unaffected — disclosed limit).
- Installs this round: none (curl/npx/git/python3 already present; tarball fetched per channel rules into
  scratch only). Tooling directive read at `~/.omp/agent/RULES.md`.
