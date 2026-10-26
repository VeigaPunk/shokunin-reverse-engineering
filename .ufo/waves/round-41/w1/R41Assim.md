# R41Assim — Assimilation candidate review (kaidoku round 41, wave 1, pre-freeze)

**Verdict: DONE — candidate A REJECT (duplicate ground), candidate B ADMIT with four repairs; id-collision guard re-proven (21 collisions, all positional drift); quarantine slice re-derived byte-identical to round 40 (5 rows, sha256 `7383a90e…8e6a`), with two slice rows refused and two adoptable.**

Scope: read-only review of the shokuknow package `/home/vgpnk/Projects/shokuknow/merge/kaidoku` (no campaign tool run there, nothing written there), plus the lane's own registry/coverage map at base `49096c7e6f226af0c750c4b003be58883cb6049f` and live source re-opens. No lane file was edited; this seat wrote only its report and its artifacts directory.

## 1. Behaviour (what was done, in order)

1. Read the package interface: `MERGE-REPORT.md` (132 rows, 77 entries, first staged id S106), the two candidate entries, their staged rows in `SOURCES.append.md`.
2. Read lane contract files at the base revision: `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md` `## Coverage map`, `corpus/SOURCES.md` registry + `## Leads (unopened)`.
3. Re-opened every cited source live today (4 fetches + 1 GitHub API call + 1 commit-pinned re-fetch), recording URL, UTC access instant, byte count, sha256, and ≤25-word contiguous located quotes with line and section — `artifacts/R41Assim/sources/source-reopens.md`.
4. Ran the §6 item 10 id-collision check verbatim into `artifacts/R41Assim/assimilation/` (`reg-ids`, `staged-ids`, `collisions`).
5. Proved the 0–3-space guard on a scratch indented fixture, then bounded its scope against the census parser itself.
6. Re-derived the quarantine slice with the §6 awk command, hashed it, and compared it byte-for-byte with the round-39 and round-40 slices; hand-checked all five slice rows live.
7. Validated a proposed normalized append row for the admitted candidate on a full scratch mirror of `corpus/` (green) and proved the campaign-style escaped-pipe variant red — `artifacts/R41Assim/census/`.

## 2. Gates

| gate | command | result |
|---|---|---|
| Lane registry revision | `git show 49096c7e:corpus/SOURCES.md \| sha256sum` vs working tree | both `a61bb2486352ba452ac08c6002bae5b600ede3ae3d6afd64d38b21236ca49e5e`; `git status --porcelain -- corpus/SOURCES.md corpus/knowledge` empty |
| Baseline census | `scripts/sources-census.sh validate --file corpus/SOURCES.md` | **exit 0**, 13 × W04 (warnings), `file ok …` |
| Scope check, candidate A / B | `PROVINCE.md` Core surfaces | A pass (firmware/archives); B pass (binwalk = Core firmware-region surface, Round-4 additions) |
| QUALITY bar, candidate A | `corpus/QUALITY.md` | passes as producer contract; fails axis fit (no new ground) |
| QUALITY bar, candidate B | `corpus/QUALITY.md` #1,2,3,5,7,8,17,42 | pass after repairs 1–4 (§4) |
| Id-collision | §6 item 10 grep/comm pair | 126 reg / 132 staged / **21 collisions** |
| Guard proof | scratch `  \| S002 \|` fixture | old pattern 1 id/1 collision; ` {0,3}` pattern 2 ids/**2** collisions |
| Quarantine slice | §6 awk + `sha256sum` + `cmp` | 5 rows, `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`, `cmp` 0 vs round 40 and round 39 |
| Proposed append row (S127) | `sources-census.sh validate --file` on a full scratch mirror | **exit 0** (`census/validate-green.txt`); same row with the staged escaped-pipe recheck cell → **exit 1**, `E01 fields=12` + `E11` (`census/validate-red-escaped-pipe.txt`) |

## 3. Candidate A — `unblob-sasquatch-dependency.md`: REJECT

The staged entry re-derives ground the lane has held since round 36, twice over:

- knowledge entry `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (same staged source file, admitted in round 36);
- coverage-map row `unblob's sasquatch dependency (round 36, assimilated)` in `corpus/README.md`, "held as producer contract … re-grounded from the shokuknow package with three corrections".

Both documents it cites are already registry rows with **stronger** pins than the staged text: unblob README = lane **S110** (tag 26.6.4, commit `1fcc7a0a…`, sha256 `6544d60f…3716`) versus staged S106 on a floating `HEAD`; devttys0 sasquatch README = lane **S111** (sha256 `f09961ee…1fef`) versus staged S107. Today's fetches reproduce both hashes byte-exactly, so no drift justifies a second row. Its host-state sentence ("sasquatch absent") is also stale as of round 36 (`~/.local/bin/sasquatch`, sha256 `ad02d27a…4754`).

**Flip condition:** the lane entry is withdrawn/superseded, or the staged file is shown to carry a claim the lane entry lacks. Checked: it does not — the lane entry is a superset (pin-by-document, inference labels, dropped "fork" wording).

## 4. Candidate B — binwalk v3 entry (staged as `firmware-region-vocabulary.md`): ADMIT with repairs

Novelty sweep (QUALITY #57 spellings, at base): `git grep -c -E 'ReFirmLabs|binwalk v3|binwalk-3|Rust rewrite' 49096c7e -- PROVINCE.md SKILL.md corpus/` → **0 hits**; `ReFirmLabs` in `corpus/SOURCES.md` → **0**. The lane's existing binwalk ground (`2026-10-13-r2-firmware-probe.md`) is REA-side version gating, never the upstream identity. The candidate adds a producer contract on a Core tool, which is in-province.

The staged text must not be appended as-is; four repairs, each verified in scratch:

1. **Pin the document.** `HEAD` → commit `26713972e3f9f52dc37d4a421c4554b0bd9e82ef` (committer date 2026-08-11T15:27:26Z, GitHub API). The commit-pinned README is byte-identical to today's `HEAD` (`cmp` exit 0), so the pin costs nothing.
2. **Anchor correction.** The Rust-rewrite sentence is line 3, in the document lead under `# Binwalk v3`; only the "identify, and optionally extract…" sentence (line 9) is inside `## What does it do?`. The staged entry attributes both to that section.
3. **Recheck cell normalization.** Staged `180d — \`curl … \| grep -c …\` -> 1` fails the lane census: escaped pipe → `E01 fields=12`, prose+cadence → `E09`. Use bare `180d` and move the recheck command to the round lesson's Gate block. The normalized row validates **exit 0**; the staged form is **exit 1**.
4. **Name/title and used-by.** The staged file name (`firmware-region-vocabulary.md`) does not match its content (binwalk v3 identity); land it under a matching name (suggested `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md`) and set `used-by` to that path — the census `E11` check resolves `used-by` on disk.

**Renumber by document:** staged **S109** names the ReFirmLabs binwalk README; lane S109 is the neovim v0.12.6 release — different document. The lane holds no row for the binwalk README, so the document takes the next free registry id, **S127**. Ready-to-append row (11 columns, validated): `artifacts/R41Assim/census/proposed-row-S127.txt`. The Rust-rewrite quote is `This is an updated version of the Binwalk firmware analysis tool, re-written in Rust for speed and accuracy.` (line 3, 20 words).

## 5. Id-collision check (§6 item 10, exact commands)

`reg-ids` **126** (S001…S126) · `staged-ids` **132** (S106…S237) · `collisions` **21** (S106…S126).
`assimilation/collision-documents.tsv` resolves every collision by document: **21/21 are positional drift, not shared documents** (e.g. staged S106 unblob README = lane S110; staged S107 devttys0 README = lane S111; staged S109 binwalk README = lane S109 neovim). No arithmetic shift is admissible.

**Guard proof** (`assimilation/guard-proof.txt`): a scratch registry carrying `  | S002 |` plus a staged set containing S002 yields, under the column-zero-only pattern, 1 id / 1 collision (S002 missed) — a false green; under the specified `^ {0,3}\|…` pattern, 2 ids / 2 collisions.

**Guard scope limit (stated, not overclaimed):** the census awk accepts a row only when `line !~ /^ {0,3}\|/` (`scripts/sources-census.sh:615`; its selftest loops indent widths 0–3, `:287`), so the guard's scope equals the parser's. A **tab**-indented row is invisible to the census itself: a registry silent-loss risk to report, but not an append-collision risk.

## 6. Quarantine slice (§6 awk, `R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`)

- **5 rows**, sha256 **`7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`** — byte-identical to round 40's `7383a90e…28e6a` (`cmp` 0 against `.ufo/waves/round-40/w1/artifacts/R40Quarantine/quarantine-slice`) and to round 39's. Register unchanged: `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`.
- Slice ids are **package-id space**, not lane-id space; the same numerals name different documents in the lane registry.

| pkg id | live check (2026-10-26T20:23Z window) | verdict |
|---|---|---|
| S113 adb `?hl=en` | 368 059 B; 21 `hreflang` values = 20 locales + `x-default` (`ar bn de en fa fr he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant x-default`) | **REFUSE as written** — the row claims "17 locales"; observed 20 + x-default. Count defect, not fabrication; re-anchor and re-count before append |
| S117 SoK binary lifters (DOI) | DOI `curl` → 0 bytes (publisher gate); Semantic Scholar abstract: title/venue match, contains `252,063` = True | **ADOPT WITH ANCHOR** = the Semantic Scholar abstract; this flips the lane's own lead at `corpus/SOURCES.md:220` ("the primary paper and an anchorable quote remain unopened") — the reversal must be recorded per QUALITY #35/#36 |
| S136 own-work `2026-10-13-r4u-06-adb-surface.md` | `grep -c '2 of 24 verbs are'` → 1; heading at `:3` | **ADOPT** (locator found, reproduces); needs a new lane id |
| S147 `HOST-CONTRACT.md` | file present (3 386 B, mtime 2026-10-22); `grep -c '207 tools'` → 1 | **ADOPT**; needs a new lane id |
| S150 Zenn no-symbols article | 174 088 B; quoted heading `シンボルがない場合のヒント` → **0 occurrences**; body: `objdump` ×42, `PLT` ×8, `AArch64` ×6 | **REFUSE the row** — anchor heading absent from served bytes (fabrication class); re-authoring from a located body passage is a new row |

**Conflict reported verbatim for the canonical judge.** Round 40 carried *"S113 adopt-with-anchor with the count corrected to 21 locales"* (`.ufo/waves/round-40/w1/artifacts/R40CL6Receipts/r39-w2-status.json`, `R40Quarantine.md:3`). Today's live page yields 21 `hreflang` **values** = 20 locales + `x-default`, and the staged row says 17 locales. Three different numbers; I adopted none of them.

## 7. Touched surfaces

- Written: `.ufo/waves/round-41/w1/R41Assim.md` (this report) and `.ufo/waves/round-41/w1/artifacts/R41Assim/` only.
- Read-only: lane `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `corpus/knowledge/*` (`git show`/`grep`), `scripts/sources-census.sh`; shokuknow `merge/kaidoku/*` and `.ufo/waves/corpus-expansion-1/absent-defect-register.md`; round-39/40 wave artifacts for the slice `cmp`.
- No lane file edited, nothing appended, no VCS mutation, no campaign tool run in shokuknow, no extractor/REA run (no carrier touched).

## 8. Out of scope (deliberately not done)

- No append to `corpus/SOURCES.md`, no knowledge-file landing, no `used-by` rewriting — L1 integration only (this seat is read-only on the lane corpus).
- No `renumber-staged.py` / `merge-plan.py` / `quote-lint.py` execution (campaign tools write into shokuknow).
- No round-end `validate --root … kaidoku` (the L1's conformance gate); the scratch `--file` run is the proxy and is labelled as such.
- No re-adjudication of round-40's AVM-theme entries; not this seat's item.

## 9. Findings (ranked)

1. **A** is a duplicate of a round-36 held entry and would have cost a row without moving the coverage map; it also carries a stale host-state sentence.
2. **B**'s campaign-schema recheck cell is not appendable: escaped pipes split the row (`E01 fields=12`) and prose cadence fails `E09`. Any package row with the same shape needs the same normalization; the kengaku precedent in §6 item 10 is not a one-off.
3. Package ids S106–S237 collide with lane S106–S126 across **21** ids, all different documents — proving the drift is positional and that only per-document renumbering is safe.
4. **S150**'s quoted heading never existed on the live page: a `payload-absent` row whose body substance is real — the register is right to quarantine it, and it must not be repaired by swapping in a different heading without a new anchor.
5. **S113** count drift across three sources (17 staged / 21 round-40 / 20+x-default measured today) — a re-count must precede any append.
6. **S117** is genuinely adoptable through the Semantic Scholar record and would retire an open lead; this needs the QUALITY #35/#36 reversal record.
7. Guard scope equals census parser scope (` {0,3}` spaces); tab-indented registry rows are invisible to the census — a registry-integrity note for the L1, not a gate failure.

## 10. Artifacts

- `artifacts/R41Assim/verdicts.md` — full verdicts, repair list, guard proof narrative, slice table.
- `artifacts/R41Assim/sources/source-reopens.md` — URLs, UTC access instants, sizes, sha256, located ≤25-word quotes with lines/sections, fetch commands.
- `artifacts/R41Assim/assimilation/reg-ids`, `staged-ids`, `collisions` — the exact §6 item 10 outputs (126/132/21).
- `artifacts/R41Assim/assimilation/collision-documents.tsv` — 21 collisions resolved by document (21/21 different).
- `artifacts/R41Assim/assimilation/guard-proof.txt`, `registry-indented.md`, `staged.md` — 0–3-space guard proof fixture and output.
- `artifacts/R41Assim/assimilation/quarantine-slice` — the re-derived slice (sha256 `7383a90e…8e6a`).
- `artifacts/R41Assim/census/proposed-row-S127.txt`, `validate-green.txt`, `validate-red-escaped-pipe.txt` — normalized append row and its green/red census receipts.

Scratch `/fast/scratch/hyaku/kaidoku-r41/R41Assim` (47 MB mirror + fetches) is removed at seat exit; every cited number is reproducible from the commands recorded in the artifacts. Tool installs: none.
