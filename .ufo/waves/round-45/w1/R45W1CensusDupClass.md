# R45W1CensusDupClass — census W04 duplicate-URL classes

Seat: `R45W1CensusDupClass`. Read-only on the lane. No tool installed. SOURCES.md not edited.

**Class counts (14 warnings, 10 URL groups): (a) 14, (b) 0, (c) 0.**

Every current `W04` is the same first source-cell URL under a scope string that actually names a different claim. Four of them are rule-2 corrections (`teaches` opens `supersedes S0NN —`) whose scope was narrowed on purpose. None restates the earlier row's claim without that marker. None is the census keying an in-cell evidence pointer that the other row does not also use as its source URL.

The two strongest *candidates* for (b), which do not clear it, are **S112** (`corpus/SOURCES.md:118`) against **S108** (`:114`), then **S138** (`:144`) against **S130** (`:136`).

## Receipt

Command (lane not mutated):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

- UTC: `2026-10-28T15:39:15Z` (clock read immediately before the run).
- Exit: **0**.
- Stdout: 15 lines, 14 `W04` + `kaidoku ok`. Stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` (second invocation, same command; copy at `census-validate.stdout` in this directory).
- That sha is the round-44 end receipt's sha (`.ufo/waves/round-44/w2/R44W2ScribeCensus.md` records `9f32a8a8…` for 14 W04). It does **not** mean `SOURCES.md` is unchanged: validate prints only warnings and the `ok` path. Registry rows are now 141 (S140, S141 present). Neither new URL is in a duplicate group, so the W04 set is unchanged.

Partner rows were recomputed with the census `url_of` (`scripts/sources-census.sh:600-605`): first `https?://` token in the source cell, fragment and one trailing slash stripped, host lowercased. `W04` is `:644-645` (URL already seen, `(url, scope)` not seen). `E04` is `:646-649` (same URL and same scope, neither side rejected, `teaches` does not match `supersedes S[0-9]{3}`). This run printed no `E04`. CORPUS rule 2 is `CORPUS.md:116-118`: append-only except `status` / `recheck` / `used-by`; a correction is a new row whose `teaches` opens `supersedes S0NN —`. Rule 2 does not forbid a second claim on the same URL.

Axes used: coverage = all 14 warnings and both rows of each; depth = scope + teaches + supersedes, not the warning text alone; calibration = do not call a nested scope (b) or a punctuation artifact (c).

## Classes

| # | warning | line | first partner | partner line | normalized URL | class |
|---|---|---|---|---|---|---|
| 1 | S033 | 39 | S032 | 38 | `github.com/NationalSecurityAgency/ghidra/pull/9348` | (a) |
| 2 | S047 | 53 | S038 | 44 | `go.dev/dl/?mode=json&include=all`,` | (a) |
| 3 | S054 | 60 | S052 | 58 | `developer.android.com/ndk/guides/abis` | (a) |
| 4 | S062 | 68 | S058 | 64 | `raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1` | (a) |
| 5 | S069 | 75 | S065 | 71 | `www.wireshark.org/docs/man-pages/tshark.html` | (a) |
| 6 | S083 | 89 | S079 | 85 | `registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` | (a) |
| 7 | S090 | 96 | S079 | 85 | same tarball | (a) |
| 8 | S092 | 98 | S079 | 85 | same tarball | (a) |
| 9 | S102 | 108 | S100 | 106 | `learn.microsoft.com/en-us/windows/win32/debug/pe-format` | (a) |
| 10 | S112 | 118 | S108 | 114 | `…/unblob/26.6.4/…/squashfs.py` | (a) |
| 11 | S117 | 123 | S110 | 116 | `…/unblob/26.6.4/README.md` | (a) |
| 12 | S119 | 125 | S079 | 85 | same tarball | (a) |
| 13 | S123 | 129 | S079 | 85 | same tarball | (a) |
| 14 | S138 | 144 | S130 | 136 | `github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` | (a) |

Tarball group order (one URL, six rows, five warnings): S079 `:85`, then S083 `:89`, S090 `:96`, S092 `:98`, S119 `:125`, S123 `:129`. S080 is not in the group: its first URL is `registry.npmjs.org/rea-agents/6.5.0` (the version document), not the tarball.

## Why each is (a)

**Corrections that already follow rule 2** (not (b); the new row supersedes, and the scope change is the thing `W04` is measuring):

- S033 `:39` vs S032 `:38`. S033 `teaches` opens `supersedes S032 —` and says S032 keyed the PR on a rendered-page digest that does not reproduce. S032 scope (`:38`) is "Candidate mechanism for the aether symbol-markup EOF". S033 scope is "Same subject as S032 … a lead, not a mechanism proof". Same PR, retracted claim. The second URL in S033 (`.patch`) is not what `W04` keys; the first URL is the shared PR.
- S054 `:60` vs S052 `:58`. `teaches` opens `supersedes S052 —`. S052 teaches that ABI records describe the packaged library. S054 teaches only the `/lib/<abi>/lib<name>.so` convention and says the REA-record inference was the lane's, not the page's.
- S062 `:68` vs S058 `:64`. `supersedes S058 —`. S058 scope includes protocol-decoder options and teaches that samplerate is explicit in the exercised calls. S062 keeps file-input and format options and moves samplerate to S060's records.
- S069 `:75` vs S065 `:71`. `supersedes S065 —`. S065 scope names `-T fields`. S069 says the provider passes `-T json` and lists the options actually passed (`-n`, `-r`, `-T json`, `-2`, `-c`, `-Y`, `-d`, `-e`).

**Different claims, no correction owed:**

- S047 `:53` vs S038 `:44`. One JSON index, two entries. S038 is go1.25.0 and excludes the 1.26/1.27 train. S047 is go1.24.6 and excludes go1.25.0. Not the same claim.
- S102 `:108` vs S100 `:106`. S100 is `rejected`: CHPEMetadataPointer / 0xC8 / code-map tags are absent. S102 mines DOS/PE signature location and optional-header bounds, and its scope says S100 stays rejected for CHPE. Not a correction of a mined teaching, so no `supersedes` is required. `W04` has no rejected-row exemption (`:644-645`); the warning is still a real cross-scope pair.
- S117 `:123` vs S110 `:116`. Same README sha256 `6544d60f…`. S110 anchor is line 49 (sasquatch install). S117 anchor is lines 5 and 22 (`78+` format-count sentences). Scopes exclude each other's sentences.
- Tarball five: S079 evidence-id minting (`domain/evidence.js`); S083 Ghidra snapshot naming (local `binary-BVOr2mgE.js`, tarball cited as membership); S090 `inspect_rust_binary`; S092 `inspect_sqlite_database`; S119 gap kinds / `dependencies` / `unpublished_entries`; S123 envelope `operation` / `provider.id`, and its scope explicitly excludes S119's gap fields. Six claims, one package URL.

## Two strongest real-duplicate candidates

Both stay **(a)**. They are the only pairs whose later scope sits inside the earlier scope and whose `teaches` does **not** open `supersedes`.

### 1. S112 `:118` vs S108 `:114` — closest, still not (b)

Same file, same tag `26.6.4` = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`.

- S108 scope: names and invokes sasquatch and sasquatch-v4be, LE/BE argv, and the AVM test. Anchor already cites lines 24-26 (`V4BE_EXECUTABLE`) and 68-69 (`get_dependencies`). Teaches: a SquashFS chunk's missing-extractor gap names sasquatch, and which argv recursion uses.
- S112 scope: v4 BE extractor dependency and argv only. Anchor quotes `case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE` and `get_dependencies()` returning `sasquatch` + `sasquatch-v4be` (lines 24-70, inside the file S108 already digests, sha256 `2d7b901b…`). Teaches: treat sasquatch-v4be as structural for standard BE v4 before diagnosing image properties.

Inference: S108's scope mentions v4be, but its `teaches` does not state S112's proposition. S112 does not correct S108 (no retracted sentence). Rule 2's supersede form is for a correction, which this is not. Nested scope without a shared claim is why `W04` exists. It would become (b) if S112's `teaches` only repeated the gap-name sentence.

### 2. S138 `:144` vs S130 `:136` — second

Same first URL (the parent `squashfs` tree). Both also carry the same second URL (`media.githubusercontent.com/.../squashfs`), which `url_of` ignores.

- S130 scope: fixture bytes and expected member trees for the whole handler family (v1 through v4-Broadcom), for a round-42 C2 generator. Teaches: pin URL plus LFS oid; a fixture path is not a handler label (two of 58 sit under DD-WRT/Broadcom but are plain v3).
- S138 scope: v1 and v2 expected trees only, both byte orders, as the R44-C1 cross-check oracle (4 trees, 22 files). Teaches: those trees are unblob's own regression set, not an independent producer; `unsquashfs` 4.7.5 agrees path-for-path and sha256-for-sha256; pin LFS oid, not the pointer-blob sha.

Inference: "expected member trees" and "pin the oid" overlap S130. The independence claim and the unsquashfs/7-Zip agreement do not. S138 is a second claim about a subset of the same tree, not a restatement and not a correction. S113 `:119` is a deeper `__input__` URL and is not in this warning.

## Considered for (c) and rejected

(c) would be a warning whose shared URL is an evidence pointer the census lifted out of a cell, not the row's source identity.

- S047's displayed URL ends in a backtick and a comma (`go.dev/dl/?mode=json&include=all`,`). Both source cells wrap the URL in backticks and a comma (`SOURCES.md:44` and `:53`). `url_of`'s token is `https?://` then any non-space non-pipe (`sources-census.sh:601`), so the closing backtick and comma stick. Stripping that tail still leaves one shared endpoint. The pair is real; the warning text is cosmetically dirty. Not (c).
- S083's only URL sits after local paths, as "members of the tarball". That is still the package identity the other five rows use as their first URL, and the scopes differ. The census cannot see a non-URL primary locator. That does not invent the duplicate.
- S033's `.patch` URL and S130/S138's LFS base are second URLs. `W04` keys the first URL on both sides.

## Not run / unknowns

- Live re-fetch of the ten URLs: not run. Classification uses the committed cells only.
- Whether a later reader would rather have had S112 or S138 supersede: not a census fact. The cells do not open `supersedes`, and the `teaches` sentences differ, so they are not class (b) on rule 2 as written.
