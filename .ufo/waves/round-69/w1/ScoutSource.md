# ScoutSource — r69-w1: the packer-identity source for R69-C2

Assigned: open the source that grounds a **PACKER-IDENTITY** row (not byte identity, which S269
covers) for the round-69 route's `--version` / packer-sha256 arms A3/A4/A6 at the pinned tag; record
two candidate rejections; propose the exact `corpus/SOURCES.md` row and the exact sentence C2 cites.
Fetched with `curl`; every number below is measured on the bytes kept in
`.ufo/waves/round-69/w1/ScoutSource/fetch/` and pinned in `SHA256SUMS` + `fetches.json`.
Access clock 2026-11-04T02:37–02:40Z = 2026-11-03 23:37–23:40 local (−0300); rows say `opened
2026-11-03` per the round date and S269/S270. No tool installed (no pacman, no npx/npm).

Deliverables: `ScoutSource/sources.md` (candidate table, rejections, row, sentence, findings),
`ScoutSource/row.S270.md` and `ScoutSource/row.S271.md` (exact 11-cell rows), `ScoutSource/fetches.json`,
`ScoutSource/SHA256SUMS`, `ScoutSource/fetch/` (11 fetched files), `ScoutSource/validate.txt`.
Nothing tracked was edited; nothing was appended to `corpus/SOURCES.md` by this seat.

## Answer

1. **The doc side is already registered and adds nothing new.** `--version: print the version of UPX`
   is byte-identical in `doc/upx-doc.txt:99` (S269's bytes, offset 3657) and `doc/upx.1:164` (the row
   staged as S270). A third doc row would duplicate it. `doc/upx-doc.txt` itself contains **0**
   occurrences of `5.2.0`, **0** of `-V`, and **no** statement of the banner format.
2. **What the claim actually needs is the code source, and it grounds A3/A4/A6's mechanics**: at tag
   `v5.2.0` (annotated tag `bc521d8d…` → commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`),
   `--version` and `-V` both reach `show_version()`, whose first stdout line is `fprintf(f, "upx
   %s\n", …)` with `UPX_VERSION_STRING` (`help.cpp:469`, offset 17406; gitrev variants `:465`/`:467`)
   — so the route's first-line comparison (`packed-elf.py:253-256`) reads a banner the packer itself
   emits, and a `-git-<rev>` build would be refused, making the pin an exact-string test.
3. **Two rejections stand**: the project front page carries no revision identity (`5.2.0` 0, `--version`
   0, even `version` 0), and a Debian rendering of the manual contains the *right sentence* while
   rendering `upx 4.2.4` — the dangerous case a text grep cannot catch.

## Headline finding — the two staged artifacts disagree about S270 (observation)

- `corpus/SOURCES.md:187` (dirty, `+2` lines, uncommitted at `3f3d20fc`): **S270 = `doc/upx.1`**,
  kind `docs`, 40077 B, sha256 `09552b3c…`, quote line 164 — verified byte-exact by this seat
  (200/40077/`09552b3c…`), cited by `corpus/knowledge/2026-11-03-r69-packed-route-contract.md:1-4`,
  `PROVINCE.md` and `corpus/README.md`.
- `corpus/lessons/round-69.md:19-20`: **S270 = `src/help.cpp` + `src/main.cpp`**, kind `code`,
  `ADMIT`; `doc/upx.1` is "**not a row** — … a secondary locator inside S270's anchor cell".

Both are uncommitted, so either can be made consistent. Recommended: **land the code row as S270**
(as the Gate already decides), keep `doc/upx.1:164` as the anchor's secondary locator, and rewrite the
knowledge entry's `source:` header, which currently describes S270 as the manual page (the exact edit
is `sources.md` §6). Alternative: append the code row as **S271** and correct the Gate's two labels;
`row.S271.md` is that byte-identical row. Do not land both.

Second finding: the staged S270 row's `teaches` says "a sha256 pin covers the bytes the banner cannot".
The manual's sentence (lines 112-114) is that "a checksum of both the compressed and uncompressed file
is maintained internally" — it is about packed/unpacked **files**, not the packer binary. Packer-binary
sha256 is route policy (`packed-elf.py:64-65,257-259`); the proposed row keeps that in `scope` as a
negation so no source is made to say it.

## The row and the sentence

`row.S270.md` (recommended landing) and `row.S271.md` (append variant) are each 11 cells / NF 13, kind
`code`, tier `A`, `mined`, `2026-11-03`, `180d`, first URL `…/src/help.cpp` (the census `url_of()` keys
on the first URL, so the code URL must stay first to avoid a `W04` against S269's doc URL). `used-by`
is `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` (exists; E11 verified) and must be
extended to name the row.

The sentence C2's A3/A4/A6 cite (exact, recommended landing):

> At tag `v5.2.0` the packer source maps `--version` and `-V` to `show_version()`, whose first stdout
> line is `upx <UPX_VERSION_STRING>` — `upx <…>-git-<rev>` on a gitrev build — (S270,
> `src/help.cpp:460-470`, `src/main.cpp:418-430,834`), and the same tag's manual renders `--version`
> as `print the version of UPX` (`doc/upx.1:164`) and states that a checksum of both the compressed
> and uncompressed file is maintained internally (`doc/upx.1:112-114`), so A3, A4 and A6 exercise a
> first-line `--version` test, a packer-binary sha256, and an exact-string version pin, not an
> "is 5.2.0" test.

It deliberately does not attribute sha256 pinning of the **packer binary** to either source.

## Rejections (each: URL, UTC access, ≤25-word located quote or reason, tier, kind, flip)

| id | candidate | measured | located quote / reason | tier / kind | flip |
|---|---|---|---|---|---|
| R1 | https://upx.github.io/ | 2026-11-04T02:37:10Z, 200, 5059 B, sha256 `f07678bd…` | `Download latest release` (3 words, offset 1223); `5.2.0` 0, `--version` 0, `version` 0 — no revision identity and no identity statement | C / docs | the page states a version-pinned identity probe or the banner contract |
| R2 | https://manpages.debian.org/bookworm/upx-ucl/upx.1.en.html → effective `…/trixie/…` | 2026-11-04T02:37:10Z, 200, 61235 B, sha256 `59f2f4a0…` | renders `upx 4.2.4` (offset 60209; chip `upx-ucl/4.2.4-1.1`) yet contains `--version: print the version of UPX` — right sentence, wrong revision | C / docs | a Debian rendering at 5.2.0, or the tag's own `doc/upx.1` |

Measured but not a rejection: `https://man.archlinux.org/man/upx.1.en` (2026-11-04T02:37:12Z, 200,
47791 B, `aed1c12a…`, `upx 5.2.0` at offset 44709) — version-matched **derived rendering**; refused a
row for adding no claim, not for being wrong (tier B if a rendering were ever the only copy).
Cross-version check: v5.3.0 keeps the doc sentence at line 99 / offset 3657 and the same three banner
branches (`help.cpp:485-489`), so the identity channel is not a 5.2.0 artefact.

## Validator (green and red)

`scripts/sources-census.sh validate --today 2026-11-03 --file …` with the lane's corpus/plans/tools
symlinked into a scratch fixture so E11 resolves as at landing (`validate.txt`):

- staged file: exit 0, 19 pre-existing `W04`, no `E`.
- **replace S270 with the code row**: exit 0, finding lines identical → no new finding.
- **append the code row as S271**: exit 0, finding lines identical → no new finding.
- control A (same row keyed on the `doc/upx-doc.txt` URL): `W04 S271 duplicate url …/doc/upx-doc.txt`
  → the duplicate check is live, so "no W04" above is a fact.
- control B (row with a non-existent `used-by`): `E11 S271 missing used-by …` and exit 1 → E11 would
  catch a dangling path, so the cited knowledge entry was checked to exist.

## Observations / inference / unknown

- **[observation]** The `--version` sentence is 6 words at `doc/upx-doc.txt:99` (offset 3657) and
  `doc/upx.1:164`; the ELF386 section statement `Linux/elf386 is automatically selected for Linux ELF
  executables.` is 8 words at `doc/upx-doc.txt:439` (offset 18892); S269's round-trip sentence is
  10 words at lines 441-442.
- **[observation]** `help.cpp:123` usage line is `[-123456789dlthVL]`; `-V` is grounded only there and
  at `main.cpp:418-419,834` — never in either manual.
- **[observation]** The installed `/usr/bin/upx` is `upx 5.2.0-1` (pacman) and its first `--version`
  line is exactly `upx 5.2.0`; its sha256 equals the route's `UPX_SHA256_PIN` (`cf2f6e7c…`).
- **[inference]** The plan's "a new row … at least one claim names it" is satisfied by one code row;
  landing two rows for one claim inflates the registry without adding support.
- **[unknown]** Which actor staged `S270 = doc/upx.1`, the knowledge entry, README and PROVINCE before
  this seat ran; the wave registry lists no other sources seat, and the L1 is exempt from the
  no-tracked-edit rule. **[unknown]** which landing the L1 prefers — both exact rows are provided.
- **[unknown]** whether an upstream release binary is ever built with `UPX_VERSION_GITREV`; only that
  the code path exists (it changes F4's blast radius, not the row).
