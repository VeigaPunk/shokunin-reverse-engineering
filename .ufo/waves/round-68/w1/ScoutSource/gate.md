# ScoutSource — round-68 w1 source gate: R68-C2 identity rule

Question (one): which primary source grounds R68-C2's identity rule — *a packed executable is
restored by unpacking to its original bytes; the unpacked file is the original program, not a
reconstruction* — and which candidate must the lane reject.

Opened 2026-11-03 by plain HTTP fetch (`curl -sSL`, user agent `kaidoku-shokunin/r68-scoutsource`),
no browser. Every fetched copy is committed beside this file under `fetch/`; `SHA256SUMS` is the
manifest. Line numbers below are **fetched-bytes** line numbers of the copy named in the row; byte
offsets are counted from file offset 0.

## Candidate table

| # | candidate | HTTP | bytes | sha256 (fetched bytes) | located quote (<= 25 words) | location | decision |
|---|---|---|---|---|---|---|---|
| a1 | UPX front page — https://upx.github.io/ | 200 | 5056 | `f07678bd16df1e713cac0c04bd2eb0b3d2accfb98c589f6f63911d6f32ad1fa7` | none for this rule — prose only: "you can list, test and **unpack** your executables" and "a checksum of both the compressed and uncompressed file is maintained internally" (`unpack` 1, `-d ` 0, `original` 0, `byte-identical` 0) | `fetch/upx-github-io.html`, `safe` bullet of the Overview list; quotes at byte offset 3152 (line 69) and 3221 (line 70) | **REJECT as a rule source**: a landing page; it names list/test/unpack in prose and a checksum, but states no `-d` switch and no restoration of the original file, and it links no manual page (`upx-doc` 0 occurrences) |
| a2 | UPX manual page the brief assumed — https://upx.github.io/upx-doc.html | 404 | 9379 | `b620507312c5e97566a3c6cfaf99144fefc18a0da7d941401dfa0f5f58fb0368` | none — GitHub Pages body: `Page not found &middot; GitHub Pages` | `fetch/upx-github-io-upx-doc.html.404`, `<title>` at byte offset 254 (line 6) | **REJECT**: URL absent (HTTP 404). The manual is not served from the project site; it ships in the repository as `doc/upx-doc.html` / `.txt` / `.pod` / `upx.1` |
| b | UPX 5.2.0 manual, `doc/upx-doc.txt` at tag `v5.2.0` (commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`) — https://raw.githubusercontent.com/upx/upx/034b6d0d81c53998c07ad6f34bfead6f5c5445ce/doc/upx-doc.txt | 200 | 37208 | `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (identical on a second fetch) | "Packed programs will be byte-identical to the original after uncompression." (11 words) | `fetch/upx-v5.2.0-doc-upx-doc.txt` lines **441-442**, byte offset **18963**, section `NOTES FOR LINUX/ELF386` (heading line 433, preceded by "Linux/elf386 is automatically selected for Linux ELF executables." at line 439); one occurrence in that section | **ACCEPT** → row S270 |
| c | Debian manpages mirror — https://manpages.debian.org/unstable/upx-ucl/upx.1.en.html | 200 | 61251 | `40e69ca34c2ceac37273eaf1c8dff82a00b9e46bade9e9dcdd0ed273427afbb8` | "Packed programs will be byte-identical to the original after uncompression." (same sentence, 11 words) | `fetch/reject-debian-upx-ucl-4.2.4-2.html`, rendered body; page header `upx(1) — upx-ucl — Debian unstable`, footer `upx-ucl 4.2.4-2`, synopsis `upx 4.2.4` | **REJECT**: it renders the **4.2.4** manual of the `upx-ucl` package, not the 5.2.0 packer the route runs (`/usr/bin/upx` = upx 5.2.0-1, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`); quoting it would attribute a 4.2-era sentence to the 5.2.0 binary |
| c2 | ManKier mirror — https://www.mankier.com/1/upx | 200 | 48794 | `ba8b23d74ef28337499f414ac64d5e1e27b9bc99be8edf5e8d80d7bd41687b06` | "Packed programs will be byte-identical to the original after uncompression." (same sentence, 11 words) | `fetch/reject-mankier-upx.html`, rendered body | **REJECT**: no revision, tag or commit pin (`revision` 0, `commit` 0, `tag ` 0); the rendered text is upstream-tip, so a quote cannot be tied to the 5.2.0 packer |

## Why b and not S269

S269 already registers this rule from `doc/upx.pod` at the same tag, quoting the
`=head2 NOTES FOR LINUX [general]` passage ("UPX keeps your original program untouched. This means
that after decompression you will have a byte-identical version"), pod lines 459-460. That passage is
a **general** Linux claim about the packer leaving the input alone.

The anchor this seat pins is the **format-scoped** sentence in `NOTES FOR LINUX/ELF386` — the format
both R68-C2 carriers are. The two are different statements in the same 5.2.0 manual: the general
section does not say the ELF format round-trips, and the ELF386 section does. Hence a second row with
a distinct anchor rather than a duplicate of S269's value. If the L1 prefers one row per source
family, fold the ELF386 line into S269's anchor cell and drop S270; nothing else changes.

## Facts the row must not overstate

- **Observation**: the manual asserts byte identity per format, and for linux/elf386 asserts it
  without qualification (lines 441-442). The PS1/EXE section carries a qualifier the ELF386 one does
  not: "uncompression, until further notice." (line 595).
- **Observation**: the same manual bounds the guarantee elsewhere — `--exact` "require[s] to be able
  to get a byte-identical file after decompression with option `-d`. [NOTE: this is work in progress
  and is not supported for all formats yet.]" (lines 101-105). So byte identity is the documented
  intent and a per-format property, not a promise to test against.
- **Inference (not a quote)**: "the unpacked file is the original program, not a reconstruction"
  follows from byte identity by definition of identity. The manual never uses the word
  "reconstruction"; the source grounds *byte equality*, and the route's `identity_ok` arm measures
  exactly that (unpacked sha256 == carrier pin).
- **Observation**: the installed packer is upx **5.2.0-1** (`pacman -Qo /usr/bin/upx`), which is why
  the row pins tag `v5.2.0` rather than the newest tag `v5.3.0` (`7c7bea44146c7ad6e17cb2d0bb9566805b44a91a`).
  The sentence is unchanged at 5.3.0 — `fetch/upx-v5.3.0-doc-upx-doc.txt` line 484, sha256
  `9b980dcab21e1220e9d6e4bb41a36c2b25392891934a998af4fe71cd750d3c35` — recorded as stability, not as the pin.
- **Unknown**: whether `upx.github.io` ever served a rendered manual page at `upx-doc.html`; no
  archive was opened this round, so the 404 is a fact about 2026-11-03 only.
