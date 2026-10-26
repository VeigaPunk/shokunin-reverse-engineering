# Gate cross-reference — `corpus/lessons/round-38.md` § Gate, resolved at `0fc61133`

Seat R38W2ScribeGateXref (leaf, advisory). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Target `0fc6113376a156fddc3ec385386d71c3a4a9f690`. All path existence checks are `git cat-file -e`
/ `git ls-tree` / `git show` against that commit; any live check is labelled.

**Verdict: DEFECTS FOUND (registration, not verdicts).** All 13 Gate decisions are represented —
each admitted source has a lane registry row with a `used-by`, each refusal has no lane row and a
staged row instead. Defects are in pointer registration: one lesson pointer does not resolve in-lane
(S147), two decisions rest on uncommitted host state, the scratch-mirror census gate certified an
S112 row that did not land, and registry row S113 registers only one of the two carrier digests it
scopes. No decision is overturned; no frozen predicate, counter, carrier or oracle was touched.

## 1. Sources S112–S116

| # | decision | registry row (lane `corpus/SOURCES.md`, 116 rows) | citing knowledge entry | evidence pointer in the lesson | resolves at `0fc61133`? |
|---|---|---|---|---|---|
| 1 | S112 unblob `squashfs.py` @26.6.4 — **admit** | **S112**, status `mined`, used-by `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (row 118) | BE entry (`source: S112 — … lines 24-70`) | none named; the row's own text: "`= S108 digest`" | **PARTIAL** — the digest `2d7b901b…9287` is committed in row S108 (row 114) and in `.ufo/waves/round-38/w1/R38ScoutUnblobHandler.md`; the L1's own re-open (03:43-03:00) has **no committed capture** |
| 2 | S113 unblob BE v4 fixtures — **admit** | **S113**, `mined`, used-by BE entry (row 119) | BE entry (`source: S113 — … fixture LFS oids`) | `.ufo/waves/round-38/w1/R38ScoutUnblobFixtures.md` | **YES** (file present; carries `oid sha256:a29ddc15…56ed / size 307`). See defect D4: the row's locator quotes only the nopad oid |
| 3 | S114 Freetz AVM-BE note — **admit (AVM marker only)** | **S114**, `mined`, used-by BE entry (row 120) | BE entry (`source: S114 — … mkfs_time == bytes_used`) | `.ufo/waves/round-38/w1/R38ScoutFreetzAvm.md`; `.ufo/waves/round-37/probes/avm.txt` | **YES**, byte-verified by this seat: `git show …:…/probes/avm.txt \| sha256sum` → `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`, 1496 B (matches the lesson) |
| 4 | S115 7-Zip 26.04 BE refusal — **reject (as oracle)** | **S115**, status `rejected`, used-by `—` (row 121) | none (rejected row; BE entry mentions the refusal as recorded-not-sourced) | `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt`; `…/R38ScribeLessonSkeleton/lesson.md` | **YES** — the artifact holds all four runs; `K1..K4` each `exit_code=2 "Cannot open the file as archive"` |
| 5 | S116 unblob.org formats matrix — **admit (via assimilation)** | **S116**, `mined`, used-by `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (row 122; digest `8f8c29af…bbc5` is in the row) | `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (`source: S116 …`, `source: S110 …`) | none named for the L1's re-open | **PARTIAL** — committed capture `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/sources-live.txt` (`http=200 bytes=216890`, `sha256 8f8c29af…bbc5`); independent refetch by this seat 2026-10-26: identical bytes/digest/counts. The L1's 03:44:24 fetch is **unrecorded** |

Registry deltas claimed by the lesson, checked: base `77091b49` has rows through S111 and 2 rows in
`S11[0-6]`; landed has 116 rows; `reg-ids` = 111 lines (`S001`..`S111`), `staged-ids` = 132
(`S106`..`S237`), `collisions` = 6 (`S106`..`S111`) — all present. **S110** edit verified:
status `mined` and recheck `on-release` are identical at base and landed; only scope and used-by
changed (used-by now lists both `2026-10-26-unblob-sasquatch-dependency.md` and
`2026-10-26-unblob-format-matrix.md`).

## 2. Assimilation decisions

| # | decision | registry row (or none) | citing knowledge entry | evidence pointer | resolves? |
|---|---|---|---|---|---|
| 6 | **ADMIT** `unblob-format-matrix` | rows **S116** (new) + **S110** (edited, used-by extended) | `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (committed; exists) | staged package `merge/kaidoku/knowledge/corpus/knowledge/unblob-format-matrix.md` (read-only, present) — cited in the entry as "Assimilated … (`merge/kaidoku/…`, staged 2026-10-23)" | **YES** (external, present). Corrections' arithmetic has **no committed capture** (D7); rechecked live by this seat: 97 `<h2 id=`, 3 × "more than 30 different", ten `SquashFS (…)` sections, `SquashFS (v4-broadcom)` ×3, 42 × `Vendor`, 1 × "Does not support encrypted ZIP files" — all as the entry states |
| 7 | **REFUSE** `sasquatch-unblob-compatibility-precondition` | **none** in lane (correct — refused); staged id **S165** = `SOURCES.append.md:66` | none (nothing appended) | staged entry `merge/kaidoku/knowledge/corpus/knowledge/sasquatch-unblob-compatibility-precondition.md` (present; its `source: S165 — lanes/kaidoku/round7/work/r7-local-measurements.tsv`); the repudiating half cites lane S110 line 49 and S112 | **YES** for the staged entry and the lane rows; the decisive *positive* fact ("`ls -la ~/.local/bin/sasquatch …` lists 382824 B and 436232 B") is an **uncommitted host observation**. Verified live by this seat: `382824` / `436232` B files and the `unblob` uv-tool link are present (D9) |
| 8 | **REFUSE** `sasquatch-unblob-avm-branch` | **none** in lane; staged **S189–S192** = `SOURCES.append.md:90-93` | none | staged entry `…/sasquatch-unblob-avm-branch.md` (present; `source: S189 — …/unblob/main/…`, S190/S191 `lanes/kaidoku/round9/work/lead2-avm-branch.tsv`, S192 Freetz) | **YES**, with a wording caveat (D9): the two campaign tsvs exist on this host and are *tracked in the shokuknow repo* (`git -C shokuknow ls-files --error-unmatch` exit 0 for both), so "the lane does not hold" is true for `kaidoku-shokunin` but the bytes are versioned elsewhere. S189's unpinned `/main/` URL and its "26.6.4" title are indeed inconsistent, as the refusal says |

Supplementary Gate-block items:

| item | pointer | resolves? |
|---|---|---|
| Id-collision guard | `assimilation/{reg-ids,staged-ids,collisions}` + `R38ExecIdCollision/guard-proof.txt` | **YES** (all four present; counts 111/132/6 reproduced). D8: the map is a pre-append snapshot — staged **S112–S116 all exist** in `SOURCES.append.md`, so the append creates 5 collisions a future assimilation must renumber |
| Scratch-mirror census before append | `.ufo/waves/round-38/w1/R38ExecMirrorGate.md` (+ `artifacts/R38ExecMirrorGate/*`) | **YES** for the pre-append gate |
| "Attempt 2's registry … validates exit 0 in the real lane (end census in the report)" | **"the report"** — no L1 report exists at `0fc61133`; no post-append census receipt is committed | **NO** (D1/D2). Reproduced independently by this seat: full `git archive` of `0fc61133` to scratch, then `scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-26` → only `W04 S112 … across scopes`, **RC=0**. The claim is true; its receipt is missing, and the block the mirror gate certified is not the landed S112 row (D2) |

## 3. Quarantine slice (5 verdicts)

| # | verdict | registry row | citing entry | evidence pointer | resolves? |
|---|---|---|---|---|---|
| 9 | S150 — **REFUSE (fabrication class)** | staged **S150** (`SOURCES.append.md:51`); absent-defect register line 82 (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, present, 83,621 B) | none (no admitted entry cites it) | `assimilation/quarantine-slice`; `.ufo/waves/round-38/w1/R38ExecQuarantine.md`; `artifacts/R38ExecQuarantine/quarantine-verdicts.txt` (live 200, 174,088 B, sha `42d59c48…766e34`, heading count 0) | **YES** |
| 10 | staged S113 (adb) — **adopt-with-anchor, count corrected** | staged **S113** = `SOURCES.append.md:14` (its scope cell says 17 locales; register line 315) | none | same verdicts file: 22 `hreflang` = 21 locales + `x-default`, page sha `e6d50f92…8198` | **YES**. Note the id now collides with lane **S113** (BE fixtures) — the lesson labels it "S113 (staged)", and D8 applies |
| 11 | S117 — **unverifiable (not fabrication)** | staged **S117** = `:18`; register line 316 | none | verdicts file: IEEE HTTP 202, 0-byte body; dblp bot-challenge; Semantic Scholar 429 | **YES** |
| 12 | S136 — **adopt-with-anchor** | staged **S136** = `:37`; register line 317 | anchor is `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` (cited *as* the anchor, not citing) | `R38ExecQuarantine.md` §3.4 + verdicts file ("2 of 24 verbs are" ×1, line 8) | **YES**, byte-checked by this seat: heading line 3, `2 of 24 verbs are` at line 8 |
| 13 | S147 — **adopt-with-anchor; heading names in the row are wrong** | staged **S147** = `:48`; register line 318 | none | lesson: "`HOST-CONTRACT.md` line 41" | **NO as written** (D3): no `HOST-CONTRACT.md` exists anywhere in the lane tree (`git ls-tree \| grep -ci host.contract` → 0). The resolvable chain is: `.ufo/waves/round-35/w1/R35ReconQuarantine.md:174-178` (committed: `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`, 3,386 B, `sha256 ab36b310…58fe`, line 41 quote, line 46 heading) + the live host file (this seat: sha256 `ab36b310b285c0278bef2a62ccdc5effe9cdc2d232e4e684452c17be264b58fe`, 3,386 B, mtime 2026-10-22). The **bytes are not committed in round 38**, and the quote's `rea-agents@6.7.0` is contradicted by the lane's pinned package (`…/rea-agents/package.json` → `"version": "6.5.0"`), a caveat wave 1 raised and the lesson drops |

"Wrong heading names": line 41 is a **bullet** under `## State as of this writing` (line 39), and the
second name the staged row gives ("§ Expected doctor output") matches line 46's heading
`## Expected \`doctor\` output on this host`. So one of the two names is wrong, not both — the
lesson's plural overstates by one.

## 4. Decisions with no committed evidence at `0fc61133`

1. **S147 anchor bytes** — only an inherited round-35 digest/size and a host file; nothing captured in
   round 38, and the lesson's pointer (`HOST-CONTRACT.md`) names no resolvable path.
2. **Assimilation REFUSE #1 positive fact** (binaries present) — an `ls -la` quoted in prose; no
   artifact. (True today when re-run by this seat.)
3. **The end census** ("validates exit 0 in the real lane … in the report") — no report and no receipt
   at the landing commit; reproduced by this seat instead (RC=0).
4. **The ADMIT's correction arithmetic** (42 `Vendor`, ten SquashFS sections, `v4-broadcom`,
   encrypted-ZIP sentence) — absent from `sources-live.txt`; rechecked live by this seat, all hold.
5. **S112's L1 re-open and S116's L1 re-open** — the L1's own fetches have no capture; byte
   identity is carried by earlier committed captures and by this seat's refetch.

## 5. Method / limits

- Read-only git only (`ls-tree`, `cat-file -e`, `show`, `grep`, `archive`); one `curl` of
  `https://unblob.org/formats/`; one run of the fleet census script on a **scratch** extraction of
  `0fc61133` (`/fast/scratch/hyaku/kaidoku-r38/R38W2ScribeGateXref`, removed). No lane file written
  except this artifact and the report; no VCS mutation; no REA run; no tool installed.
- Snapshots read-only, not judged as sources: the staged package `merge/kaidoku`, the absent-defect
  register, the shokuknow tsvs, and `~/.agents/.../HOST-CONTRACT.md`.
- [INFERENCE] The staged register and register line numbers are stable between 2026-10-24 and now —
  no digest was taken of them, only existence and content of the cited rows.
