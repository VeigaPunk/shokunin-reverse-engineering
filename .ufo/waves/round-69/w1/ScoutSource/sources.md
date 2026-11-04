# Sources — the packer-identity row for R69-C2 (ScoutSource, r69-w1)

Assigned question: which source at the pinned tag grounds a **PACKER-IDENTITY** row for the round-69
route's `--version` / sha256-pin arms (A3/A4/A6) — the `--version` description, the ELF format
section, and any statement about the packer's version banner — without restating S269's byte-identity
scope; and which two candidates must be rejected.

Fetched with `curl -sSL -o` (no `-f`, so a 4xx would still be recorded as bytes); every figure below
is measured on the fetched bytes in `fetch/` and pinned by `SHA256SUMS` and `fetches.json`.
Access clock: **2026-11-04T02:37–02:40Z**, i.e. 2026-11-03 23:37–23:40 local (−0300). Rows record
`opened 2026-11-03` per the round date and the S269/S270 convention; this note is the reason.
No tool was installed or upgraded for this seat (no pacman transaction, no npx, no npm).

## 0. What the tree already contains (observation)

`corpus/SOURCES.md` is dirty (`git status`: `M corpus/SOURCES.md`, `+2` lines) and line 187 already
holds **S270 = `doc/upx.1`** (kind `docs`, 40077 B, sha256 `09552b3c…`, quote line 164), cited by
`corpus/knowledge/2026-11-03-r69-packed-route-contract.md`, `PROVINCE.md` and `corpus/README.md`.
`corpus/lessons/round-69.md` `## Gate` (line 19) instead records the **code** source
`src/help.cpp` + `src/main.cpp` as **ADMIT — S270** and (line 20) `doc/upx.1` as **not a row**, "a
secondary locator inside S270's anchor cell".

So two staged artifacts disagree about what S270 *is*. Both are uncommitted at `3f3d20fc`, so either
can still be made consistent. §4 gives the exact row both ways; §6 gives the required companion edits.

## 1. Answer

The doc side of the claim is already registered twice and does **not** need a third row: the sentence
`--version: print the version of UPX` is byte-identical in `doc/upx-doc.txt:99` (S269's bytes) and
`doc/upx.1:164` (the staged S270). What no manual states — and what A3/A6 actually test — is the
**composition of the banner**: only `src/help.cpp` and `src/main.cpp` at the tag show that
`--version` and `-V` both reach `show_version()`, whose first stdout line is `upx %s` fed with
`UPX_VERSION_STRING` (with `-git-<rev>` / git-describe variants). That is the row to land, and the
lesson's `## Gate` already says so. `doc/upx-doc.txt` itself contains **no** `5.2.0` string (0
occurrences), **no** `-V`, and no banner statement.

## 2. Candidates

| seq | source | kind | tier | accessed (UTC) | HTTP / bytes / sha256 | located quote (≤25 words; line, byte offset) | verdict |
|---|---|---|---|---|---|---|---|
| 1 | `doc/upx-doc.txt` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt | docs | A | 2026-11-04T02:37:09Z | 200 / 37208 / `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` | `--version: print the version of UPX` (6 words) — line 99, offset 3657; `Linux/elf386 is automatically selected for Linux ELF executables.` (8 words) — line 439, offset 18892; S269's round-trip sentence lines 441-442 (10 words) | **not a new row** — its identity sentence is already S270's subject (identical text at `doc/upx.1:164`); id-less corroboration only |
| 2 | `src/help.cpp` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp | code | A | 2026-11-04T02:37:09Z | 200 / 27279 / `0b893ca8299c061a8e1961ddbc1fa85cd8d77f3f043cba9a478a697e5d363c79` | `fprintf(f, "upx %s\n", UPX_VERSION_STRING);` (4 words) — line 469, offset 17406; gitrev variants lines 465 (offset 17237) and 467 (offset 17325); `show_version` line 460; usage `[-123456789dlthVL]` line 123 | **ADMIT** — the only source stating the banner composition and the `-V` alias |
| 3 | `src/main.cpp` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/src/main.cpp | code | A | 2026-11-04T02:37:09Z | 200 / 41889 / `a02c7cba2939708e2af4c25119fe20a5a7594b7225b189848196280b03dea82c` | `{"version", 0, N, 'V' + 256},  // display version number` (10 words) — line 834, offset 23702; `case 'V': set_cmd(CMD_VERSION);` lines 418-419; dispatch lines 421-430; pre-scan `strcmp(argv[i], "--version")` line 1174 | **ADMIT** (co-source of the same row) — grounds the option-to-command mapping |
| 4 | `doc/upx.1` at tag `v5.2.0` — https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.1 | docs | A | 2026-11-04T02:38:18Z | 200 / 40077 / `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25` | `--version: print the version of UPX` (6 words) — line 164; `a checksum of both the compressed and uncompressed file is maintained internally` (14 words) — lines 112-114 | **verified**, then **not a row** — identical claim text to seq 1; kept as the row's secondary locator |
| 5 | tag ref + tag object — https://api.github.com/repos/upx/upx/git/ref/tags/v5.2.0 and …/git/tags/bc521d8d825298cffd342d6de8ec0bc397ad6849 | dataset | A | 2026-11-04T02:37:09Z / 02:37:10Z | 200 / 356 / `8d6c2aca…`; 200 / 757 / `b945f9df…` | `"ref": "refs/tags/v5.2.0"` → tag object `bc521d8d825298cffd342d6de8ec0bc397ad6849` → commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce` | supporting: revision identity of every `v5.2.0` raw URL above |
| 6 | `https://upx.github.io/` | docs | C | 2026-11-04T02:37:10Z | 200 / 5059 / `f07678bd16df1e713cac0c04bd2eb0b3d2accfb98c589f6f63911d6f32ad1fa7` | `Download latest release` (3 words) — offset 1223; `grep -c '5\.2\.0'` = 0, `grep -c -- '--version'` = 0, `grep -ci version` = 0 | **REJECT** (R1) |
| 7 | `https://manpages.debian.org/bookworm/upx-ucl/upx.1.en.html` → effective `…/trixie/upx-ucl/upx.1.en.html` | docs | C | 2026-11-04T02:37:10Z | 200 / 61235 / `59f2f4a0c6fc997827717fb0d9f0bce24b92b5096b2d1e33d7962fbac30b521b` | renders `upx 4.2.4` (offset 60209) and the version chip `upx-ucl/4.2.4-1.1`, while the page still contains `--version: print the version of UPX` (1 occurrence) | **REJECT** (R2) — a true quote from the wrong revision |
| 8 | `https://man.archlinux.org/man/upx.1.en` | docs | B | 2026-11-04T02:37:12Z | 200 / 47791 / `aed1c12a62e54bbe04f718e9184b3c912dbf254fc98233771809e8536143ea04` | `upx 5.2.0` (offset 44709); `--version`: `print the version of UPX` (HTML line 149) | **supporting only, not a row** — version-matched but a derived rendering of seq 4; adds no claim |
| 9 | v5.3.0 cross-version — https://raw.githubusercontent.com/upx/upx/v5.3.0/doc/upx-doc.txt and …/v5.3.0/src/help.cpp | docs + code | A | 2026-11-04T02:40:37Z | 200 / 39224 / `9b980dcab21e1220e9d6e4bb41a36c2b25392891934a998af4fe71cd750d3c35`; 200 / 30497 / `b2a36017c042a157aa5ab79afdcc1b1a66d69f0f3f9135c86256673ba21fcf8f` | doc quote still line 99, offset 3657 (unchanged); `fprintf(f, "upx %s` still at help.cpp lines 485/487/489 (`show_version` line 480) | stability observation, not a row |

## 3. Rejections (two, each with its flip)

**R1 — the project front page, `https://upx.github.io/` (200, 5059 B, sha256 `f07678bd…`).**
Observation: the page carries no revision identity at all — `5.2.0` 0 occurrences, `--version` 0,
case-insensitive `version` 0; its only related element is the button `Download latest release`
(offset 1223). A "latest" landing page cannot ground an identity claim about a pinned build.
Tier C; kind docs.
*Flip:* the page gains a version-pinned statement of the identity probe (or an anchored section
naming the banner/`--version` contract) at that version.

**R2 — a distro rendering of another revision, `https://manpages.debian.org/bookworm/upx-ucl/upx.1.en.html`
(200, effective `…/trixie/upx-ucl/upx.1.en.html`, 61235 B, sha256 `59f2f4a0…`).**
Observation: the page *does* contain the exact quote (`--version: print the version of UPX`, 1
occurrence) yet renders `upx 4.2.4` (offset 60209) and the chip `upx-ucl/4.2.4-1.1` — the text is
right and the revision is wrong, which is the failure mode a text grep cannot catch. Quoting it would
attribute 4.2-era text to the 5.2.0 binary the pin enforces. Tier C; kind docs.
*Flip:* a Debian rendering of `upx-ucl` at 5.2.0 (or the tag's own `doc/upx.1`, which R2 is a
rendering of).
Note: `corpus/lessons/round-69.md:22` already rejects the **unstable** rendering (61251 B, sha256
`40e69ca3…`, chips 4.2.4-1.1 / 4.2.4-2) for the same reason; R2 is the independently measured trixie
rendering of the same class, not a new argument.

**Not a rejection, recorded so it is not mistaken for one:** seq 8 (Arch, 5.2.0-1) is version-matched;
it is refused a *row* because it is a derived rendering of seq 4 and adds no claim, not because it is
wrong. If a rendering were ever the only copy, it would be admissible as tier B.

## 4. The row (exact; 11 cells, no `|` inside)

Recommended landing — **one row, S270, the code source** (what `round-69.md` `## Gate` line 19
already decides; `doc/upx.1` becomes the anchor's secondary locator, as line 20 says). The exact line
is `row.S270.md`:

```
| S270 | UPX 5.2.0 packer source at tag `v5.2.0`, the identity banner and `--version` option — https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp and https://raw.githubusercontent.com/upx/upx/v5.2.0/src/main.cpp | code | A | The composition of the identity banner a caller reads before packing — `--version` and `-V` both reach `show_version()`, whose first stdout line is `upx <UPX_VERSION_STRING>` (git-describe and `-git-<rev>` variants on a gitrev build); not the manual's probe description, not byte identity (S269), not sha256 pinning of the packer binary, not any carrier | Tag `v5.2.0` object `bc521d8d825298cffd342d6de8ec0bc397ad6849` → commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`; `src/help.cpp` fetched 2026-11-03, HTTP 200, 27279 bytes, sha256 `0b893ca8299c061a8e1961ddbc1fa85cd8d77f3f043cba9a478a697e5d363c79`, `show_version` at `:460`, plain banner `:469`, gitrev variants `:465` and `:467`, usage `:123`; `src/main.cpp` HTTP 200, 41889 bytes, sha256 `a02c7cba2939708e2af4c25119fe20a5a7594b7225b189848196280b03dea82c`, option row `:834`, dispatch `:421-430` and `:1294-1296`; secondary locator `doc/upx.1:164` (40077 bytes, sha256 `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25`) renders `--version: print the version of UPX` | The route reads the packer's own first banner line and can refuse a different packer before it packs; a `-git-<rev>` build prints a longer first line, so an exact-string version pin is stricter than accepting the release number. | mined | 2026-11-03 | 180d | corpus/knowledge/2026-11-03-r69-packed-route-contract.md |
```

Alternative landing — **append S271 and leave S270 = `doc/upx.1` as staged**. Then the same 11 cells
with only the id cell changed to `S271`; the `(S269)` clause stays, because it names a real neighbour
(S269's byte-identity scope) rather than S271's own subject. The exact variant line is `row.S271.md`;
it validated clean (§7). Do **not** land both: the two rows would carry the same claim (a duplicate by
subject, even though the URL check would stay silent because the URLs differ).

Row-id observation: the registry's max id at `3f3d20fc` is S270 (176 → 177 rows when the staged row is
counted; `grep -c '^| S'` = 176 before it). S270 is free in `HEAD`; in the working tree it is taken by
`doc/upx.1`, so "replace S270" and "append S271" are the only two consistent options.

## 5. The sentence R69-C2's A3/A4/A6 arms cite (exact, recommended landing)

> At tag `v5.2.0` the packer source maps `--version` and `-V` to `show_version()`, whose first stdout
> line is `upx <UPX_VERSION_STRING>` — `upx <…>-git-<rev>` on a gitrev build — (S270,
> `src/help.cpp:460-470`, `src/main.cpp:418-430,834`), and the same tag's manual renders `--version`
> as `print the version of UPX` (`doc/upx.1:164`) and states that a checksum of both the compressed
> and uncompressed file is maintained internally (`doc/upx.1:112-114`), so A3, A4 and A6 exercise a
> first-line `--version` test, a packer-binary sha256, and an exact-string version pin, not an
> "is 5.2.0" test.

Option-B variant (S270 = manual, S271 = code): replace the parenthetical `(S270, `src/help.cpp…`)`
with `(S271, `src/help.cpp…`)` and prefix the two manual references with `S270, `.

Deliberate limits of the sentence: the manual's checksum sentence is about **compressed and
uncompressed files**, not the packer binary, so it is cited for what it says; the packer-binary
sha256 in A4/A6 is **route policy** (`tools/round-69/packed-elf.py:64-65,257-259`), not a source
claim. No sentence should say the source grounds sha256 pinning of `upx` itself.

## 6. Required companion edits (only for the recommended landing)

1. `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` lines 1-4 currently read
   `source: S270 — UPX 5.2.0 generated manual page, doc/upx.1` with 40077 B / `09552b3c…` / line 164.
   Under the recommended landing they must read: `source: S270 — UPX 5.2.0 packer source at tag
   v5.2.0, src/help.cpp + src/main.cpp` with 27279 B / `0b893ca8…` and 41889 B / `a02c7cba…`, located
   at `help.cpp:469` (and `main.cpp:834`), with the manual's line 164 kept as the secondary locator.
   Otherwise the entry's citation and the registry row name different sources.
2. `corpus/lessons/round-69.md:19` quotes `help.cpp:465` (the `UPX_VERSION_GIT_DESCRIBE` branch) as
   the located quote. For a non-git build the emitted line is `:469` (`UPX_VERSION_STRING`); `:465` /
   `:467` are the variant branches. Prefer `:469` as the quote and keep `:465`/`:467` as the
   variant list, or the Gate's quote reads as the always-taken path when it is not.
3. `PROVINCE.md` and `corpus/README.md` cite `S270` without naming the file, so they need no edit —
   they stay true under either landing.

## 7. Validator run (green and red)

`scripts/sources-census.sh validate --today 2026-11-03 --file <candidate> <lane>`, with the lane's
`corpus/{knowledge,lessons,QUALITY.md,…}`, `plans/`, `tools/`, `SKILL.md` symlinked into a scratch
fixture so E11 resolves exactly as it will in the lane (transcript: `validate.txt`).

| candidate | new findings vs the staged file | exit |
|---|---|---|
| staged `corpus/SOURCES.md` (S270 = `doc/upx.1`) | baseline: 19 pre-existing W04, no E | 0 |
| replace S270 with the code row (`row.S270.md`) | none — finding lines identical | 0 |
| append the code row as S271 (`row.S271.md`) | none — finding lines identical | 0 |
| **control A**: same row with the `doc/upx-doc.txt` URL as first URL | `W04 S271 duplicate url …/doc/upx-doc.txt across scopes` | 0 |
| **control B**: same row with a non-existent `used-by` | `E11 S271 missing used-by corpus/lessons/round-69-does-not-exist.md` | 1 |

Control A proves the duplicate check is live (so "no W04" for the proposed row is a fact, not a dead
check); control B proves E11 would catch a dangling `used-by` (so the row's cited
`corpus/knowledge/2026-11-03-r69-packed-route-contract.md` was checked to exist). The first URL in a
`source` cell is the one the checker keys on (`url_of()` takes the first `https?://` match), which is
why the code URL must stay first.

## 8. Findings

- **[observation] F1 — the two staged artifacts disagree about S270.** `corpus/SOURCES.md:187` holds
  S270 = `doc/upx.1` (docs), while `corpus/lessons/round-69.md:19-20` holds S270 = `help.cpp` +
  `main.cpp` (code) and calls `doc/upx.1` "not a row". One of them must change before the landing.
  This seat's row is the code source; the lesson's Gate is the artifact that already decided it.
- **[observation] F2 — the staged S270 row's `teaches` cell over-claims.** It says "a sha256 pin
  covers the bytes the banner cannot". The manual's sentence (lines 112-114) is that "a checksum of
  both the compressed and uncompressed file is maintained internally" — it concerns packed and
  unpacked *files*, and says nothing about pinning the packer binary's bytes. Pin semantics are
  `packed-elf.py:257-259`; the proposed row keeps that in `scope` as a negation.
- **[observation] F3 — no manual at the tag states the banner composition.** Both manual forms give
  only `--version: print the version of UPX`; `doc/upx-doc.txt` has 0 occurrences of `5.2.0` and 0 of
  `-V`. The banner text lives only in `help.cpp:460-470`; the `-V` alias only in `main.cpp:418-419`
  and the usage string `help.cpp:123`. A cite sentence that claims the banner format from "the
  documentation" would be unsupported.
- **[observation] F4 — the pin is an exact-string test with a real refusal path.** `preflight()` takes
  `upx --version` stdout, `.strip().splitlines()[0]`, and compares it to `"upx 5.2.0"`
  (`tools/round-69/packed-elf.py:253-256`). A git-describe or `-git-<rev>` upstream build prints a
  longer first line (`help.cpp:465,467`) and would be refused as `packer_mismatch`. The installed
  Arch `upx 5.2.0-1` prints exactly `upx 5.2.0` ([observation], `/usr/bin/upx`, sha256
  `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` = the route's `UPX_SHA256_PIN`).
- **[observation] F5 — the claim is stable across the next release.** v5.3.0 keeps the doc sentence at
  the same line 99 / offset 3657 and the same three `fprintf` branches (`help.cpp:485-489`), so the
  identity channel is not a 5.2.0 artefact; the pin stays 5.2.0 because that is the installed packer.
- **[inference] F6** — the round's plan says "a new row ... for the pin/`--version` surface" and "at
  least one claim names it"; the recommended landing satisfies both with one row, and it is the row
  the Gate already names. Landing S271 *as well* would give the round two rows for one claim.
- **[unknown]** who staged S270/`doc/upx.1` and the knowledge entry before this seat ran (the wave
  registry lists no sources scribe besides `ScoutSource`; the L1 is exempt from the no-tracked-edit
  rule). **[unknown]** whether the L1 prefers replace-S270 or append-S271 — both are given exactly.
- **[unknown]** whether upstream ever builds a release binary with `UPX_VERSION_GITREV` defined; not
  established here (only that the code path exists). It does not change the row, only F4's scope.

## 9. Deliverables in this directory

| path | contents |
|---|---|
| `row.S270.md` | the exact recommended row line (11 cells) |
| `row.S271.md` | the exact append-variant row line (11 cells) |
| `fetches.json` | 11 fetch records: URL, effective URL, UTC time, HTTP, bytes, sha256, local copy, verdict |
| `SHA256SUMS` | `sha256sum *` of `fetch/` |
| `fetch/` | the fetched bytes: 2×v5.2.0 code, 2 manuals, tag ref + tag object, 2 rejections, 1 supporting rendering, 2×v5.3.0 stability |
| `validate.txt` | validator transcripts for baseline, replace, append, and both controls |
