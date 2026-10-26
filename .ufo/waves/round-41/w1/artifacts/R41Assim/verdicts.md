# R41Assim — verdicts (round 41, wave 1, pre-freeze)

Lane base read: `49096c7e6f226af0c750c4b003be58883cb6049f` (`KaidokuR41`).
`corpus/SOURCES.md` in the working tree is byte-identical to that base:
sha256 `a61bb2486352ba452ac08c6002bae5b600ede3ae3d6afd64d38b21236ca49e5e`, `git status --porcelain -- corpus/SOURCES.md corpus/knowledge` empty.
Baseline census: `sources-census.sh validate --file corpus/SOURCES.md` → **exit 0**, 13 × W04 duplicate-URL warnings, last line `file ok …/corpus/SOURCES.md`.
Lane registry size at measurement: **126 rows** (S001–S126). Staged package: **132 rows** (S106–S237).

## Candidate A — `knowledge/corpus/knowledge/unblob-sasquatch-dependency.md`

**Verdict: REJECT (duplicate ground; no expansion credit).**

1. **Coverage-map overlap (hard).** The lane already holds this exact ground twice over:
   - knowledge entry `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (round 36 assimilation, same staged source file);
   - `corpus/README.md` coverage row `| unblob's sasquatch dependency (round 36, assimilated) | 2026-10-26-unblob-sasquatch-dependency | held as producer contract … re-grounded from the shokuknow package with three corrections |`.
2. **Both cited documents are already registry rows, with tighter pins than the staged text.**
   - unblob README: lane **S110** pinned at tag 26.6.4 (commit `1fcc7a0a…`), sha256 `6544d60f…3716`; staged S106 uses a floating `HEAD`.
   - devttys0 sasquatch README: lane **S111**, sha256 `f09961ee…1fef`; staged S107 identical content, no pin.
   Today's fetches reproduce both hashes exactly (`sources/source-reopens.md` A1–A3), so nothing moved that could justify a new row.
3. **The staged text is stale where it is not duplicate.** Its host-state sentence ("sasquatch absence on this host") was true at the 2026-10-23 package snapshot and is false since round 36 (`~/.local/bin/sasquatch` sha256 `ad02d27a…4754`; lane entry §3 records this explicitly).
4. PROVINCE scope: passes (firmware/archives are Core). QUALITY bar: passes as producer contract. Axis fit: fails — no new ground, so it cannot move coverage or depth.

**Flip condition:** (a) the lane entry `2026-10-26-unblob-sasquatch-dependency.md` is withdrawn or superseded, **or** (b) the staged file is shown to carry a claim the lane entry lacks. Checked now: it does not — the lane entry is a superset carrying the three corrections (pin-by-document, inference labels, dropped "fork" wording), and its S110/S111 anchors are the same two documents.

## Candidate B — `knowledge/corpus/knowledge/firmware-region-vocabulary.md` (content = binwalk v3)

**Verdict: ADMIT with four repairs (the staged file must not be appended as-is).**

- **PROVINCE check — pass.** binwalk is a named Core surface: `PROVINCE.md` § "Round-4 additions to Core" row *Firmware regions + extract* (`REA_BINWALK_COMMAND=/usr/bin/binwalk` 3.1.0, probe `inspect-firmware-regions`/`extract-firmware`). A producer contract about that tool is in-province.
- **QUALITY bar — pass after repairs.**
  - #1 resolvable source: yes, re-opened today (`sources/source-reopens.md` C; sha256 `87b8277e…11d4`, 1 470 B).
  - #2 falsifiable: yes — "binwalk v3 is a Rust rewrite" is checkable in one sentence.
  - #3 domain-specific: yes (firmware region inspection), not generic advice.
  - #5 labels: the "Why this matters" paragraph asserts a cross-reference to *the lane's own REA wrapper docs* — that is inference and needs an [INFERENCE] label plus a corpus pointer, or deletion.
  - #7 not-examined: present and honest (the Wiki catalogue is declared unopened) — keep verbatim.
  - #8/#17/#42: **fail as staged** → repairs 1–2 below.
- **Coverage-map overlap — none.** `git grep -c -E 'ReFirmLabs|binwalk v3|binwalk-3|Rust rewrite' 49096c7e -- PROVINCE.md SKILL.md corpus/` → **0 hits**; `corpus/SOURCES.md` has **0** occurrences of `ReFirmLabs`; its single `binwalk` occurrence sits inside S123's scope cell (`rea-agents` provider/operation assignment), not as a binwalk-upstream row. Existing binwalk ground (`2026-10-13-r2-firmware-probe.md`, 15 hits) is about REA's *version gate and provider gating* on binwalk 3.1.0 — it never states the upstream identity or the catalogue's location. The candidate adds the producer's own statement.

**Repairs required before append (all verified in scratch):**

1. **Pin by document.** Staged `HEAD` → commit `26713972e3f9f52dc37d4a421c4554b0bd9e82ef` (2026-08-11T15:27:26Z). The bytes at that commit are identical to today's `HEAD` (`cmp` exit 0), so the pin is free, not a rewrite.
2. **Anchor correction.** The Rust-rewrite sentence is line 3 in the document lead, **not** § "What does it do?"; line 9 is the one inside that section. Both quotes are ≤25 words and contiguous.
3. **Recheck cell normalization.** Staged `180d — \`curl … \| grep -c …\` -> 1` is campaign schema and fails the lane census: the escaped pipe splits the row (`E01 fields=12`), and the prose+cadence fails `E09`. Normalized cell is a bare `180d`, with the recheck command moved into the round lesson's Gate block. Verified: with `180d` the full-mirror census is **exit 0** (`census/validate-green.txt`); with the staged escaped-pipe cell it is **exit 1**, E01 + E11 (`census/validate-red-escaped-pipe.txt`).
4. **File name / title.** The staged file is named `firmware-region-vocabulary.md` while its content is binwalk-v3 identity; land it under a title-matching name (suggested `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md`), and set `used-by` to that path (the census `E11` check resolves `used-by` on disk).

**Renumber by document (not arithmetic).** Staged **S109** names `raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md`; lane **S109** is the neovim v0.12.6 release — different document. The lane holds **no row** for the binwalk README (`grep -c ReFirmLabs corpus/SOURCES.md` → 0), so the document takes the registry's next free id **S127**. Proposed normalized row (11 columns, validated): `census/proposed-row-S127.txt`.

**Flip condition (to reject):** the README's line 3 no longer says the tool is a Rust rewrite, or the signature catalogue becomes part of the README itself (then the catalogue-outside-the-README claim dies), or an existing lane entry is found to already state binwalk v3's upstream identity.

## Id-collision check — `assimilation/`

Exact §6 item 10 command, `A=<this dir>/assimilation`:

```sh
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md            | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <pkg>/merge/kaidoku/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

- `reg-ids` **126** (S001…S126), `staged-ids` **132** (S106…S237), `collisions` **21** (S106…S126) — file `assimilation/collisions`.
- **Every one of the 21 is positional drift, not a shared document** (`assimilation/collision-documents.tsv`, 21/21 `same_document = no`). Examples: staged S106 (unblob README) = lane S110; staged S107 (devttys0 README) = lane S111; staged S109 (binwalk README) = lane S109 **neovim release**.
- **Guard proof** (`assimilation/guard-proof.txt`, fixtures `assimilation/registry-indented.md`, `assimilation/staged.md`): registry row `  | S002 |` + staged S002 → column-zero-only pattern sees 1 id / 1 collision (misses S002); the specified ` {0,3}` pattern sees 2 ids / **2 collisions**. Guard is live.
- **Guard scope equals the parser's scope**: the census awk accepts a row only on `line !~ /^ {0,3}\|/` (`scripts/sources-census.sh:615`; selftest loops `for indent_width in 0 1 2 3`, `:287`). A tab-indented row is invisible to the census itself — a registry silent-loss risk, not an append collision risk. Stated as a limit, not claimed as clean.

## Quarantine slice — `assimilation/quarantine-slice`

Exact awk from §6 item 10, `R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`:

- **5 rows**, sha256 **`7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`** — byte-identical to round 40's `7383a90e…28e6a`: `cmp` against `.ufo/waves/round-40/w1/artifacts/R40Quarantine/quarantine-slice` → 0, and against `.ufo/waves/round-39/w1/artifacts/R39Quarantine/quarantine-slice` → 0.
- Register itself unchanged: sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (same as round 40's cited `5afe1810…d833`).
- The slice ids are **package-id space** (`| kaidoku | roundN | Sxxx`), not lane-id space; the same numerals name different documents in the lane registry.

Row-by-row verdicts (hand-checked live today, 2026-10-26T20:23Z window):

| pkg id | class in register | document | live check (command + outcome) | verdict |
|---|---|---|---|---|
| S113 | unreachable (source unfetchable) | https://developer.android.com/tools/adb?hl=en | `curl -fsSL -A 'Mozilla/5.0'` exit 0, 368 059 B; `grep -o 'hreflang="[a-zA-Z-]*"' \| sort -u \| wc -l` → **21** values = `ar bn de en fa fr he hi id it ja ko pl pt-BR ru th tr vi x-default zh-Hans zh-Hant` (20 locales + `x-default`) | **REFUSE as written**: the row claims "served in 17 locales"; observed 20 + x-default. Re-anchor and re-count before any append. (Staged quote itself is present, so it is a count defect, not fabrication.) |
| S117 | unreachable | https://doi.org/10.1109/SP46214.2022.9833799 | `curl -fsSL` on the DOI → exit 0, **0 bytes** (publisher gate); `api.semanticscholar.org/graph/v1/paper/DOI:10.1109/SP46214.2022.9833799?fields=…` → title `SoK: Demystifying Binary Lifters Through the Lens of Downstream Applications`, venue `IEEE Symposium on Security and Privacy 2022`, abstract contains `252,063` = **True** | **ADOPT WITH ANCHOR** = the Semantic Scholar abstract record (not the DOI page). This flips the lane's own `SOURCES.md:220` lead line "the primary paper and an anchorable quote remain unopened" — the reversal must be recorded (QUALITY #35/#36). |
| S136 | named no locator | own-work `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` | `grep -c '2 of 24 verbs are' <file>` → **1**; heading located at `:3` (`# kaidoku-r4u / 06 — ADB surface: client present, zero devices`) | **ADOPT** (locator located and reproduces). Lane holds no other row for this document (0 hits), so it needs a new lane id (next free after S127). |
| S147 | named no locator | `$HOME/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` | file exists (3 386 B, mtime 2026-10-22); `grep -c '207 tools'` → **1** | **ADOPT** (locator located and reproduces); also needs a new lane id. |
| S150 | payload-absent | https://zenn.dev/yasu01/articles/7370bd5d414ec4 | page `curl` exit 0, 174 088 B; quoted heading `シンボルがない場合のヒント` → **0 occurrences** (live, today); body present: `objdump` ×42, `PLT` ×8, `AArch64` ×6, `x86-64` ×2, `逆アセンブル` ×18; served H-tags are the article title + site navigation only | **REFUSE the row**: the anchor heading is absent from the served bytes (fabrication class). The *substance* exists in the body under other anchors; re-authoring from a located body passage is a new row, never this one. |

## Carried-disposition conflict, reported verbatim for the judge

Round 40 carried: *"S113 adopt-with-anchor with the count corrected to 21 locales"* (`.ufo/waves/round-40/w1/artifacts/R40CL6Receipts/r39-w2-status.json` and `R40Quarantine.md:3`). Today's live measurement on the same URL gives **21 hreflang values total**, i.e. **20 locales + `x-default`**, and the staged row's own claim is **17 locales**. All three numbers differ. I did not adopt any of them; the re-count must be declared before the row is written.
