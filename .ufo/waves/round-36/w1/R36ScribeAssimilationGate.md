# R36ScribeAssimilationGate — assimilation `## Gate` block draft (kaidoku round 36, wave 1)

Seat: scribe, leaf. Advisory: this file is the only lane write.
Observation cutoff: **2026-10-26T04:40Z**. Lane HEAD read: `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`
(`corpus/lessons/` holds no `round-36*` file at that revision — `git ls-files corpus/lessons | grep -c 36` → 0,
so the block below is a draft for a file that does not yet exist).
Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ScribeAssimilationGate` (removed at exit; every artifact cited
here is a lane file, a package file, or a value reproduced in this report).
No VCS mutation, no subagents, no REA calls, no campaign tool run in `/home/vgpnk/Projects/shokuknow`
(read-only), no tool installed or upgraded, no pacman transaction.

## 1. Inputs and their identity

| input | sha256 | notes |
|---|---|---|
| `merge/kaidoku/SOURCES.append.md` | `b82d1276d837867d3a39f56e57a255249802b9d0665b230f1bc87c9424510449` | 132 staged rows (ids S106–S237) |
| `…/unblob-sasquatch-dependency.md` | `032c97a822b89c4606bb6988ec32e2eeec1963277f4eae100a60b0085923ca78` | cites staged S106, S107 |
| `…/sasquatch-prebuilt-package-inventory.md` | `ed1158292578ffe99b38177183244789063dc1d44e09736dfde303f2ca1003ec` | cites staged S130 |
| `…/sasquatch-unblob-compatibility.md` | `f646e611027f8d9d4bb0c019e68748b8e6a4dd8a44cc60c56c0b604d3a445bb1` | cites staged S183–S186 |
| `…/sasquatch-unblob-compatibility-precondition.md` | `6f5708e3a02333ab2e8b5586a68cd5340710c0b88889844e9263f63f0b6fe0f9` | cites staged S165 |
| `.ufo/waves/round-36/assimilation/reg-ids` | `4673ae892be3e6ac8bed9e1a703da118d16c9698490f316e27dd5bf11a168162` | 106 ids |
| `.ufo/waves/round-36/assimilation/staged-ids` | `93841167c73394fa7f15835b802caa9964757971a654c0d0837ec166c5da089b` | 132 ids |
| `.ufo/waves/round-36/assimilation/collisions` | `68f990a0364372e14b15ac23901aad0a44b2ead9f0ac7b464f64da0a440e206b` | `S106` |
| `.ufo/waves/round-36/assimilation/quarantine-slice` | `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` | 5 rows: S150, S113, S117, S136, S147 |
| `id-guard-proof/{fixture-registry.md,fixture-staged.md,collisions}` | `0b811b2b…bd9`, `0b08b320…4e4`, `f8d01e56…828` | fixture contains `  | S002 |`; collisions = `S002` |

## 2. Re-verification performed by this seat (first-hand)

### 2.1 Id-collision check — reproduced exactly

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' lane/corpus/SOURCES.md      | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' pkg/SOURCES.append.md       | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```
Result: `reg=106 staged=132 collisions=1`, file content `S106`; all three files `diff`-identical to the
committed evidence (`reg_same`, `staged_same`, `coll_same`). Registry ids are contiguous `S001`–`S106`
(no gaps; `106 1 106 []`).

**Collision is a document collision, not a re-use.** Lane `S106` is the GNU binutils readelf version-needs
row (`corpus/SOURCES.md:112`, sourceware URL); staged `S106` is the unblob upstream README. The staged row
must therefore take a *new* lane id by document (map in §3).

### 2.2 Guard proof — reproduced (the guard is not broken)

Scratch fixture with an indented row (`| S001 | a |` then `  | S002 | b |`), staged set `S002`, `S900`:
- column-zero pattern `^\|…` → `collisions-col0` **empty** (false green),
- 0–3-space pattern `^ {0,3}\|…` → `collisions` = **`S002`** (matches the committed proof).

So the 0–3-space extractor is the only one that catches an indented collision, and the committed
`id-guard-proof` set is consistent with a working guard.

### 2.3 Source re-open (my access date, my hashes)

`2026-10-26T04:36:42Z` → `04:36:44Z`:

| source | http | bytes | lines | sha256 |
|---|---|---|---|---|
| `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | 200 | 7580 | 235 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` |
| `https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md` | 200 | 7580 | 235 | same bytes (`cmp` exit 0) |
| `https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | 200 | 1050 | 30 | `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` |

Tag pin: `git ls-remote https://github.com/onekey-sec/unblob refs/tags/26.6.4` →
`1fcc7a0a584a70a96c31f5a276c20944d199a089  refs/tags/26.6.4` (the GitHub API `git/ref` call returned 403,
rate-limited — `ls-remote` is the first-hand substitute used here).

Located quotes (contiguous, ≤25 words):
- unblob README line 49 — `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):`
- unblob README line 43 — `Then install the required external extractor tools. On Ubuntu/Debian:` (scopes the deb block)
- sasquatch README line 12 — `Very beta.`
- sasquatch README line 17 — `You need a C/C++ compiler, plus the liblzma, liblzo and zlib development libraries:`
- sasquatch README line 26 — `The included build.sh script will download squashfs-tools v4.3, patch the source, then build and install sasquatch:`

Note on locators: the staged **row** `S107` anchor (`§ "Prerequisites"` and `§ "Installation"`) is *correct* —
those setext headings exist at lines 14 and 23. It is the **entry's** source line (`§ "sasquatch"`) that
names a heading that does not exist. Row and entry are corrected differently (see §3, decisions 1 and 2).

### 2.4 Host state (first-hand, 2026-10-26)

```
~/.local/bin/unblob --version                     -> 26.6.4
~/.local/bin/unblob --show-external-dependencies   -> "sasquatch ✓", "sasquatch-v4be ✓"
~/.local/bin/sasquatch -version                    -> unsquashfs version 4.5.1 (2022/03/17)
sha256sum ~/.local/bin/sasquatch                   -> ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754 (382824 B, mtime Oct 26 01:22)
sha256sum ~/.local/bin/sasquatch-v4be              -> fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6 (436232 B)
```

`corpus/evidence/round-36/c1/K{1..4}/after-run.json` each record `sasquatch` path + sha256 `ad02d27a…` +
`unsquashfs version 4.5.1 (2022/03/17)`, `exit 0`; the four `after.json` files carry an empty
`extraction_gaps`. The sasquatch-on-PATH pairing is therefore already observed **in the lane** this round.

### 2.5 Append gate on a scratch mirror (§10 rule, run before any append)

Mirror = lane root copied into scratch (`corpus/` + top-level files + `tools/`), the two normalized rows
inserted after `S106`, and the admitted entry placed at
`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (staged bytes, rename only):

```
scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md --today 2026-10-26   -> exit 0
```
Findings: the same 9 pre-existing `W04` duplicate-URL warnings as the untouched lane registry
(`validate --file lane/corpus/SOURCES.md` → exit 0, findings identical apart from the printed path),
and **no** `E01/E03/E04/E11` for the appended rows. Both rows split to **11 cells** (the staged rows split to
12 — see finding F2). Row text in Appendix A.

## 3. Deliverable — draft `## Gate` block for `corpus/lessons/round-36.md`

Everything between the markers is the block; it is written to be inserted verbatim under the lesson's
`## Gate` heading by the integration owner.

<!-- BEGIN GATE BLOCK -->

### Assimilation theme — sasquatch / unblob, package `merge/kaidoku`

Theme: the four staged sasquatch/unblob entries, evaluated against `PROVINCE.md` scope and the
`corpus/QUALITY.md` admission bar. Package identity: `SOURCES.append.md` sha256 `b82d1276…0449`, 132 staged
rows; lane registry at `d2e46ef5…b8be` holds 106 rows `S001`–`S106`.

**Id-collision check (scratch, read-only, re-run 2026-10-26).** 0–3-leading-space extractor over
`corpus/SOURCES.md` → **106** ids; over `merge/kaidoku/SOURCES.append.md` → **132** ids; `comm -12` →
**1 collision: `S106`**. The guard was proven first on a fixture whose registry carries an indented
`  | S002 |`: the column-zero pattern yields an empty `collisions` (false green) while the 0–3-space pattern
yields `S002`. Evidence: `.ufo/waves/round-36/assimilation/{reg-ids,staged-ids,collisions}` and
`…/id-guard-proof/`. The single collision is a *different document*: lane `S106` is the binutils readelf
row, staged `S106` is the unblob README — so the staged row is renumbered by document, not merged.

#### Decision 1 — `unblob-sasquatch-dependency` — **ADMIT** (bounded; land only with corrections c1–c3)

- **PROVINCE scope: in.** This is the producer contract of the surface C1 moves — `PROVINCE.md:149`
  (Frontier bullet *sasquatch — unblob's squashfs recursion extractor*), the Core row `PROVINCE.md:125`
  (`Firmware regions + extract`) and `corpus/README.md:44` (Firmware, "recursion blocked by missing
  sasquatch"). Domain-specific, not generic tool advice (QUALITY #3).
- **Re-opened this round, own access date 2026-10-26T04:36:42Z.** unblob README tag `26.6.4` = commit
  `1fcc7a0a584a70a96c31f5a276c20944d199a089`, 235 lines, sha256 `6544d60f…3716`, byte-identical to HEAD
  that day; sasquatch README (`master`), 30 lines, sha256 `f09961ee…1fef`.
- **Located quotes (≤25 words, contiguous).** `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):`
  (unblob README line 49); `Very beta.` (sasquatch README line 12); `You need a C/C++ compiler, plus the liblzma, liblzo and zlib development libraries:`
  (sasquatch README line 17).
- **QUALITY.** #1/#2/#3 hold on the re-opened bytes. #4/#8 fail as staged (no commit, hash, or version pin;
  "HEAD as fetched" is a floating ref) → **c1**. #5 fails as staged (two reasoning steps unlabelled, and
  the "(a) sasquatch absent on this host" sentence is now false) → **c2**. #42 fails as staged (the entry's
  S107 source line cites `§ "sasquatch"`, a heading that does not exist) → **c3**.
- **Corrections that must land with it.**
  - **c1 — pin by document.** Source lines become `source: S107 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md`
    and `source: S108 — https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md`, each with the
    sha256 and the access date above; the unblob pin names commit `1fcc7a0a…` and *tag* `26.6.4`, not HEAD.
  - **c2 — labels and host-state scope.** Mark the "failed SquashFS extraction cannot be read as *no
    SquashFS*" step and the packaging-route consequence as inference; re-scope "(a) sasquatch absence on
    this host" to the 2026-10-23 snapshot, because on 2026-10-26 both executables are installed
    (`unblob --show-external-dependencies` → `sasquatch ✓`, `sasquatch-v4be ✓`; `~/.local/bin/sasquatch`
    sha256 `ad02d27a…4754`) and the round-36 C1 after-receipts record a sasquatch-enabled run.
  - **c3 — drop the unsupported provenance claim.** Neither cited README calls the onekey package a
    "fork"; the wave-1 API read of `onekey-sec/sasquatch` returned `"fork": false` (second-hand: this
    seat's own API call was rate-limited, 403). What the sources support is a base-version difference
    (devttys0 `build.sh` pulls squashfs-tools **4.3**, line 26; the packaged binary reports **4.5.1**), so
    that is the wording to keep.
- **Row / file map.** Staged `S106` → lane **`S107`**; staged `S107` → lane **`S108`** (map by document,
  below). Entry lands at `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` — the package's
  undated stem is renamed because all 122 existing knowledge stems are date-prefixed and C2's coverage
  count only recognises `2026-MM-DD-…` stems (`tools/round-36/c2-counter.py:126`).
- **Flip to refuse.** Any of c1–c3 not applied at landing; or the re-opened README hashes differ from the
  values above; or the appended rows fail `sources-census.sh validate` (E01/E03/E04/E11).

#### Decision 2 — `sasquatch-prebuilt-package-inventory` — **REFUSE as staged**

- **PROVINCE scope: in** (same packaging surface, `PROVINCE.md:149`); refused on the QUALITY bar, not on scope.
- **QUALITY #1/#2 fail on two claims.** (i) "each carrying a Debian package per architecture" is false as
  written: release `sasquatch-v1.0` (2022-02-26) has **amd64 only**. (ii) "the release body shows the
  packaged upstream version (`4.5.1`) against the package version (`1.0`)" is not sourced: the
  `sasquatch-v4.5.1-6` body names PRs only; `4.5.1` appears in the tag name and the `-1` body, `1.0` in the
  asset names and deb control. Both findings are the wave-1 scout's, re-read here against the entry text.
- **The row's own recheck does not reproduce.** Stored: `grep -c 'sasquatch-v4.5.1-6'` → `12`. Re-run by
  this seat at 2026-10-26T04:38:58Z on the same URL: `grep -c` → **13**, `grep -o … | wc -l` → **18**. The
  release page is dynamic, so a line count over it cannot be the row's recheck.
- **Flip to admit.** Correct (i) to "7 of 8 releases; `sasquatch-v1.0` is amd64-only", (ii) to attribute
  `4.5.1`/`1.0` to the tag name, the deb control and `sasquatch -version`, and (iii) replace the recheck
  with the API form (`jq length`, per-tag asset counts) at a stated date. Row `S130` is not appended.

#### Decision 3 — `sasquatch-unblob-compatibility` — **REFUSE as staged**

- **PROVINCE scope: in**; refused on QUALITY #1 (resolvable source).
- **The four cited rows do not resolve at the lane.** Staged `S184`–`S186` cite
  `lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv`, and `S183` names the lane copy
  `lanes/kaidoku/round8/work/unblob-squashfs-upstream.py`. The lane has no `lanes/` directory
  (`ls lane/lanes` → absent) and the file exists only under the read-only sibling root
  `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round8/work/`. A pointer that resolves only outside the
  lane revision is not a repo path for this lane's registry, and the lane cannot acquire it by copying out
  of a read-only root under this round's bounds.
- **The ground is already being claimed in-lane this round.** `corpus/evidence/round-36/c1/K{1..4}/after-run.json`
  record the sasquatch-enabled run (sha256 `ad02d27a…4754`, `unsquashfs version 4.5.1`), exit 0, empty
  `extraction_gaps`. Admitting this entry unchanged would double-claim C1's own ground with evidence the
  registry cannot point at.
- **Flip to admit.** Re-point `S183`–`S186` to lane-retained bytes — either copies inside
  `corpus/evidence/` or the round-36 C1 receipts plus carrier paths — then re-open in a later round.
  Rows `S183`–`S186` are not appended.

#### Decision 4 — `sasquatch-unblob-compatibility-precondition` — **REFUSE**

- The entry's load-bearing claim — "Neither tool is present on the lane host … the compatibility question
  is permanently operator-side" — is **false on the measured host**: `unblob --show-external-dependencies`
  reports `sasquatch ✓` and `sasquatch-v4be ✓`; `~/.local/bin/sasquatch` is the release binary
  (sha256 `ad02d27a…4754`, `unsquashfs version 4.5.1 (2022/03/17)`); and four C1 after-receipts record the
  pairing running. QUALITY #1/#2 fail (a falsifiable claim, falsified by this round's own evidence) and #5
  fails (the installation inference is stated as observation).
- **Flip.** None under the current host state. It becomes admissible only as an explicit *superseded
  historical record*: the entry and row `S165` re-scoped to a dated 2026-10-24 host snapshot, naming this
  refusal by path and line and the admitting row naming the reversal (QUALITY #35/#36). Not this round;
  `S165` is not appended.

#### Renumber map — by document (staged id → lane id)

| staged id | document (URL is the evidence; the id follows it) | lane id | used-by |
|---|---|---|---|
| `S106` | unblob README, tag `26.6.4` — `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | **`S107`** | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` |
| `S107` | devttys0/sasquatch README, `master` — `https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | **`S108`** | same entry |

The other 130 staged ids are untouched; campaign ids keep their campaign meaning — **staged `S107` is not
lane `S107`**. If the C1 knowledge entry cites the same unblob README document, it must cite lane `S107`
and be appended to that row's `used-by` list; it must not mint a second row for the same URL (census `E04`).

#### Normalisation applied to the two appended rows (§10 scratch transformation)

- Both staged rows split into **12** cells because their `recheck` cells carry an escaped `\|` inside a
  command. The appended rows carry `180d` in `recheck` (valid cadence, E09-clean); the stripped verify
  commands are recorded here: staged `S106` → `curl -fsSL …/unblob/HEAD/README.md`, then `grep -c 'sasquatch'`
  → 3 (reproduced today, on the tag URL); staged `S107` → `curl -fsSL …/devttys0/sasquatch/master/README.md`,
  then `grep -c 'vendor-specific SquashFS'` → 1.
- `opened` is `2026-10-26` (this round's access date, not the campaign's `2026-10-23`); `status` is `mined`;
  `used-by` lists exactly the admitted entry. `anchor` and `teaches` cells are rewritten without any
  literal or escaped `|`.
- Append gate: on a scratch mirror of the lane (`corpus/` + append block + the admitted entry at its lane
  path) `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26` exits
  **0**, with only the 9 pre-existing `W04` warnings of the base registry and no new finding.

#### Quarantine slice (5 rows) — verdicts, none appended

| row | class | verdict this round |
|---|---|---|
| `S150` | payload-absent | **RECORDED** as a fabrication-class refusal (cited heading absent from both served HTML and the Zenn API body); verdict recorded, not re-derivation of the wave-1 scout's finding |
| `S113` | unreachable | **RECORDED** as locatable with a `teaches` count defect (row says 17 locales; served bytes carry 21 + `x-default`) — verdict recorded from the wave-1 check |
| `S117` | unreachable | **RECORDED** as unverifiable at the cited source (publisher wall) with a mirror-consistent abstract |
| `S136` | named no locator | **RECORDED** as locatable |
| `S147` | named no locator | **RECORDED** as locatable with a heading mismatch (`§ "REA release"` is a bullet under `§ "State as of this writing"`) |

None of the five is cited by an admitted entry, so none is appendable this round; the verdicts are the
wave-1 seat's (`.ufo/waves/round-36/w1/R36ScoutQuarantine.md`) and this Gate records them rather than
re-running them.

<!-- END GATE BLOCK -->

## 4. Findings for the integration owner

- **F1 — Collision is by document, and the naive fix breaks a citation.** Re-pointing *by arithmetic*
  (staged `S106` → `S107` and staged `S107` → `S108`) happens to produce the same numbers here, but the map
  is written per document so the C1 entry and the adopted entry converge on **one** row for the unblob
  README (`S107`). Two rows for one URL would trip census `E04`.
- **F2 — The staged rows are not appendable as-is.** `S106`, `S107` and `S130` each split into **12** cells
  on an escaped `\|` inside the `recheck` command. Only `S106`/`S107` matter this round (the other is
  refused); both are normalised per §10.
- **F3 — Adoption forces a calibration edit (C2 coupling).** Command A (`c2-counter.py:119-140`) computes
  `mapped = files ∩ stems-found-in-README-coverage-map` over `2026-MM-DD-…` stems. Measured on the mirror
  with the entry present and no README row: **knowledge_files 123, mapped 122** → a SCORECARD
  `N/N` statement would mismatch. Adoption must land with (i) a `corpus/README.md` coverage-map row naming
  the dated stem (Firmware row area, `corpus/README.md:44`) and (ii) the SCORECARD owned-axes coverage count
  restated to the new observed value at the same revision C2 is re-measured on.
- **F4 — Naming.** All 122 current `corpus/knowledge/*.md` stems are date-prefixed. The package's undated
  target path (`corpus/knowledge/unblob-sasquatch-dependency.md`) would be invisible to C2's `mapped` set,
  so the entry is renamed to `2026-10-26-unblob-sasquatch-dependency.md` at adoption.
- **F5 — Row anchor vs entry locator are two different defects.** Staged `S107`'s anchor (`§ "Prerequisites"`,
  `§ "Installation"`) is correct; the *entry's* source line (`§ "sasquatch"`) is the wrong one. Fixing the
  package's suggested correction blindly would "repair" a correct row.
- **F6 — `S130`'s recheck is unstable.** `grep -c 'sasquatch-v4.5.1-6'` on the GitHub releases HTML returned
  12 at ~04:27Z (wave-1 scout) and **13** at 04:38:58Z (this seat), with 18 occurrences. A dynamic page
  cannot carry a fixed count in a registry cell; the API form is the replacement.
- **F7 — The theme's remaining two entries are refuted, not merely weak.** `sasquatch-unblob-compatibility-precondition`
  asserts a host state that four in-lane receipts contradict; if the round needs that entry at all it is as
  a superseded record under QUALITY #35/#36.
- **F8 — Scope check passes for all four entries.** Nothing here is sibling-domain: every entry concerns
  unblob/sasquatch on the firmware-extraction surface the lane already owns (`PROVINCE.md:125,149`;
  `corpus/README.md:44`). The refusals are QUALITY-bar and evidence-pointer failures, so they cannot be
  waved through as "not our domain".
- **F9 — One admit, three refuses** meets the round's `≥1 admit and ≥1 reject` requirement without
  padding: the admitted entry is bounded to producer-contract ground the lane does not hold (the packaged
  install route and the upstream self-description); its compatibility sibling is left to C1's own receipts.

## 5. Commands run (exact) and outcomes

| # | command (cwd = scratch unless noted) | outcome |
|---|---|---|
| 1 | `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/corpus/SOURCES.md \| grep -oE 'S[0-9]+' \| sort` | 106 ids, contiguous S001–S106 |
| 2 | same over `merge/kaidoku/SOURCES.append.md` | 132 ids, S106–S237 |
| 3 | `comm -12 reg-ids staged-ids` | `S106` (1 line); `diff` vs committed = identical |
| 4 | fixture guard (col0 vs 0–3-space patterns) | `[]` vs `[S002]` — guard sound |
| 5 | `curl -sS -o … https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` (+ HEAD, sasquatch master) | 200 / 7580 B, 200 / 7580 B, 200 / 1050 B; `cmp` tag≡HEAD exit 0 |
| 6 | `git ls-remote https://github.com/onekey-sec/unblob refs/tags/26.6.4` | `1fcc7a0a…a089` |
| 7 | `curl -sS https://api.github.com/repos/onekey-sec/unblob/git/ref/tags/26.6.4` | **403** (rate limit) — value taken from `ls-remote` instead |
| 8 | `curl -fsSL 'https://github.com/onekey-sec/sasquatch/releases' \| grep -c 'sasquatch-v4.5.1-6'` | **13** (stored value is 12) |
| 9 | `~/.local/bin/unblob --show-external-dependencies \| grep -i sasq` | `sasquatch ✓`, `sasquatch-v4be ✓` |
| 10 | `sha256sum ~/.local/bin/sasquatch ~/.local/bin/sasquatch-v4be` | `ad02d27a…4754`, `fac88740…14c6` |
| 11 | `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26` | **exit 0**, 9 `W04` (identical to base), no E-code for the appended rows |
| 12 | `scripts/sources-census.sh validate --file lane/corpus/SOURCES.md --today 2026-10-26` (read-only base control) | exit 0, same 9 `W04` |
| 13 | python replication of `c2-counter.command_a` on the mirror | `knowledge_files 123, mapped 122` (F3) |

## 6. Limits and what this seat did not do

- The block is a **draft**; no lane file other than this report was written, so nothing here is an
  admission until the integration owner lands the rows, the entry and the README/SCORECARD companion edits.
- `onekey-sec/sasquatch` repository metadata (`fork: false`) and the 8-release API count are **second-hand**
  from `.ufo/waves/round-36/w1/R36ScoutUnblobReadme.md` / `R36ScoutPrebuiltInventory.md`; this seat's own
  GitHub API calls were rate-limited (403) at 04:36–04:39Z.
- The quarantine verdicts are likewise the wave-1 seat's, recorded here — not re-fetched by this seat.
- No REA run, no carrier extraction, no `.deb` unpacking by this seat; C1's receipts were read, not
  re-executed. Whether C1 meets its own target is not this seat's judgement.
- The scratch mirror validated row schema and pointer resolution only: it does not establish that the
  corrected entry text reads well, that the SCORECARD restatement is numerically right at the landing
  revision, or that the final-tip C2 re-measure passes.
- Scratch removed at exit; nothing cited above lives under `/tmp` or scratch.

## Appendix A — normalized append rows (as validated, 11 cells)

```
| S107 | unblob upstream README, tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | docs | A | unblob's own producer contract: the format set it claims, its recursion-depth default, and the delegation of SquashFS support to an external sasquatch extractor — a capability statement about the producer, not evidence about any firmware image | README.md § "Installation" (lines 35-60); tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089, 235 lines, sha256 6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716, byte-identical to HEAD fetched 2026-10-26 | Which formats unblob claims, that recursion defaults to 10 levels, and that SquashFS support requires an external sasquatch install published as a prebuilt `.deb` for Ubuntu/Debian | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md |
| S108 | sasquatch upstream README — https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md | docs | A | what sasquatch itself claims to cover (vendor-modified SquashFS headers and LZMA customisations) and the build prerequisites that explain a source-only install path — a tool's self-description, not proof that any image was extracted | README.md § "About" (line 12), § "Prerequisites" (lines 14-20) and § "Installation" (lines 23-26); branch `master`, 30 lines, sha256 f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef, fetched 2026-10-26 | That sasquatch is a patch set over `unsquashfs` (squashfs-tools 4.3) that brute-forces vendor LZMA customisations, needs a C/C++ compiler plus liblzma/liblzo2/zlib development libraries, is self-described as very beta, and builds by downloading then patching squashfs-tools v4.3 | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md |
```

## Appendix B — id lists (§10 requires both lists pasted)

**Registry (106, `corpus/SOURCES.md` at `d2e46ef5`)**

S001, S002, S003, S004, S005, S006, S007, S008, S009, S010, S011, S012, S013, S014, S015, S016, S017, S018
S019, S020, S021, S022, S023, S024, S025, S026, S027, S028, S029, S030, S031, S032, S033, S034, S035, S036
S037, S038, S039, S040, S041, S042, S043, S044, S045, S046, S047, S048, S049, S050, S051, S052, S053, S054
S055, S056, S057, S058, S059, S060, S061, S062, S063, S064, S065, S066, S067, S068, S069, S070, S071, S072
S073, S074, S075, S076, S077, S078, S079, S080, S081, S082, S083, S084, S085, S086, S087, S088, S089, S090
S091, S092, S093, S094, S095, S096, S097, S098, S099, S100, S101, S102, S103, S104, S105, S106

**Staged (132, `merge/kaidoku/SOURCES.append.md`)**

S106, S107, S108, S109, S110, S111, S112, S113, S114, S115, S116, S117, S118, S119, S120, S121, S122, S123
S124, S125, S126, S127, S128, S129, S130, S131, S132, S133, S134, S135, S136, S137, S138, S139, S140, S141
S142, S143, S144, S145, S146, S147, S148, S149, S150, S151, S152, S153, S154, S155, S156, S157, S158, S159
S160, S161, S162, S163, S164, S165, S166, S167, S168, S169, S170, S171, S172, S173, S174, S175, S176, S177
S178, S179, S180, S181, S182, S183, S184, S185, S186, S187, S188, S189, S190, S191, S192, S193, S194, S195
S196, S197, S198, S199, S200, S201, S202, S203, S204, S205, S206, S207, S208, S209, S210, S211, S212, S213
S214, S215, S216, S217, S218, S219, S220, S221, S222, S223, S224, S225, S226, S227, S228, S229, S230, S231
S232, S233, S234, S235, S236, S237

**Collision count: 1 — `S106`** (lane binutils readelf row vs staged unblob README row; different documents).

## Appendix C — verdict summary

| entry | scope | quality | decision | rows | file |
|---|---|---|---|---|---|
| `unblob-sasquatch-dependency` | in | passes with c1–c3 | **ADMIT (bounded)** | S107, S108 | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` |
| `sasquatch-prebuilt-package-inventory` | in | #1/#2 fail on two claims; recheck unstable | **REFUSE** | none | — |
| `sasquatch-unblob-compatibility` | in | #1 fails (cited rows unresolvable in-lane) | **REFUSE** | none | — |
| `sasquatch-unblob-compatibility-precondition` | in | #1/#2/#5 fail (host state refuted) | **REFUSE** | none | — |
