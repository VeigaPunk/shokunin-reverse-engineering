# SourceRizinDocs — rizin 0.8.x `iI`, `iS`, `ie`, `-N`, `-q`, `-c`

Seat: KaidokuR20.SourceRizinDocs-2 (leaf, read-only; report only). Access date: 2026-10-20 (`date -Iseconds` at fetch: 2026-10-20T17:47:11-03:00 to 17:48:50-03:00).

## Sources opened

| # | URL / object | Fetched | sha256 (full) | Revision |
|---|---|---|---|---|
| D1 | https://book.rizin.re/ (index) | 2026-10-20T17:46:55-03:00 | 6e18709460c0240ec999e8b6b0d6f74f5146043ff07485ec26c56fdacc05c089 | unversioned (no release stamp in page) |
| D2 | https://book.rizin.re/src/first_steps/commandline_options.html | 2026-10-20T17:47:11-03:00 | 5c30b9f6c7afbc80bd57192cc79ef3a600305c29ced2053e1c28766002dedfeb | unversioned |
| D3 | https://book.rizin.re/src/refcard/intro.html | 2026-10-20T17:47:11-03:00 | 5c16fc96aa8d9a3340f89187cdb223fca06f1ef3708ddd216eaac56dd72c7f4d | unversioned |
| D4 | https://book.rizin.re/src/basic_commands/sections.html | 2026-10-20T17:47:11-03:00 | fc78aef2f90fea2e9be96c21c1f0de490b56f57f2239d369025eff7c0a261875 | unversioned |
| D5 | https://github.com/rizinorg/rizin/releases/tag/v0.8.2 | 2026-10-20T17:46:55-03:00 | 1862edfe34424fc1eed84387d0c14dcc7ddf9da96cefaf0e08f002d8ea24ca7c | tag v0.8.2 (release body: security + Haiku notes only; no command/flag docs) |
| S1 | rizinorg/rizin `git clone --depth 1 --branch v0.8.2` (system tmp, removed after use) | 2026-10-20T17:47:52-03:00 | librz/main/rizin.c `046219f7a2bbe245d1533461e8b53a2fb8feb36620e91540722ca12056c349c6`; librz/core/cmd_descs/cmd_descs.c `2cbea72050b3a6f55cd6440ea7ae81bc8470a2f724f4cfda8f996d7be1942943`; librz/core/cmd/cmd_info.c `2330263be18921437af24d49f8993fc9a9b2d6b1397926d49be8398c8913bfc3` | tag v0.8.2 = commit `5a611eee2999d312317ff90d600e37dde0f58992`, committed 2026-02-01T21:52:21+04:00 |
| L1 | local `/usr/bin/rizin` 0.8.2 (`rizin -h`, `rizin -N -q -c '<cmd>?'`) | 2026-10-20T17:47–17:48 | n/a | observed binary, `rizin 0.8.2 @ linux-x86-64` |

No installs or updates were performed; `curl`, `git`, and the pre-existing `/usr/bin/rizin` were used as-is.

## Quote (one contiguous quote, located)

> "Quiet mode (no prompt) and quit after -i and -c" (9 words)

- Located: D2, §7 "Shell Command-line Options", usage block, `-q` line (converted text line 204 of the fetched HTML). Matches local `rizin -h` (L1) and source `librz/main/rizin.c:130`.

Supporting quotes (verbatim, for the Draft row only):
- D3, §136.5 "Information" (converted text line 259): "The i command uses the RzBin API and allows us to the same things rz-bin does." (16 words)
- S1, `librz/main/rizin.c:128`: "Do not load user settings and scripts" (`-N` help string)
- S1, `librz/core/cmd_descs/cmd_descs.c:12956`: `.summary = "Show binary info"` (iI)
- S1, `librz/core/cmd_descs/cmd_descs.c:12897`: `.summary = "List entrypoints"` (ie)
- S1, `librz/core/cmd_descs/cmd_descs.c:13086`: `.summary = "List sections"` (iS)

## Findings

Observations (O) and inferences (I) are labelled.

- O1: Book help for `-q`, `-N`, `-NN`, `-c` (D2 lines ~185–205) matches rizin 0.8.2 usage text byte-for-byte as printed by local `rizin -h`, and the source help strings at `librz/main/rizin.c:128-130`.
- O2: `iI` is `rz_cmd_info_binary_handler` → `rz_core_bin_info_print` (`librz/core/cmd/cmd_info.c:421-423`). `ie` → `rz_core_bin_entries_print` (`cmd_info.c:192-194`). `iS` → `rz_core_bin_sections_print` with optional digest arguments (`cmd_info.c:242-248`; help `iS[jqt] [<digests1> <digests2> ...]`, observed in L1 `i?`). All three use the RzBin object (I: consistent with D3's "uses the RzBin API").
- O3: Each of `iI`, `iS`, `ie` requires an opened binary: `rizin -N -q -c 'ie' --` printed `ERROR: No binary object currently selected.` (L1).
- O4: That error case exited 0 under `-q` (L1: `rc=0` from `timeout`/rizin; the shell pipeline reported the timeout rc). Inference: under `-q -c`, a failed info command does not change process exit status in this build, so a REA caller cannot rely on exit code alone to detect a failed `iI`/`iS`/`ie`. Stdout/stderr text must be checked.
- O5: `-N` side effects not in the book: `librz/main/rizin.c:678-683` sets `run_rc=false`; `librz/main/rizin.c:930-933` then skips `rz_core_parse_rizinrc` and sets `scr.utf8=false`. Observed: `rizin -N -q -c 'e scr.utf8' /usr/bin/true` → `false`; without `-N` → `true` (L1).
- O6: `-NN` (second `-N`) sets `load_l=false` (`rizin.c:682`), i.e. plugins are not loaded; the book's "Do not load any script or plugin" (D2) agrees.
- O7: `-q` sets `scr.interactive`, `scr.prompt`, `cfg.fortunes` to false (`rizin.c:688-691`) and a second `-q` sets `forcequit` (`rizin.c:692-694`); the book's "quit after -i and -c" (D2) describes the exit behavior. `run_commands` (`rizin.c:332-365`) runs `-i` files then each `-c` via `rz_core_cmd_lines`, then returns for quiet runs with commands.
- O8: Multiple `-c` flags execute in order (`run_commands`, `rizin.c:354-357`); L1 `rizin -N -q -c 'iI' -c 'ie' /usr/bin/true` produced 42 lines on stdout (I: both ran; not separately checked).
- O9: Book §Sections (D4 line 202) says "To list all created sections use iS (or iSj to get the json format)" and "The iS= will show the region bars" — consistent with `iS[jqt]` and the `iS=` section-bars subcommand in local help.
- O10: Book is unversioned: D1–D4 carry no version string, and the refcard's `iI`/`ie`/`iS` lines (D3 §136.5) are one-line summaries only ("Info on binary", "Display entrypoint", "Display sections"). Inference: the book supports meaning, not 0.8.x-specific behavior; the tag source (S1) is the version-pinned evidence.
- O11: Local observed `iS` output on `/usr/bin/true` (L1) matches the column layout of D4's sample (paddr/size/vaddr/vsize/align/perm/name/type/flags).
- O12: The release page (D5) documents only security fixes (CVE-2026-22780, mach0 chained fixups) and a Haiku note. It does not document the commands or flags in scope.
- O13: Book `rz-bin -I` (D2-adjacent page `tools/rz-bin/file_identification`) is `rz-bin`'s file-identification command, not rizin's `iI`. The two are different commands; `iI` is the rizin-command route. Do not conflate them in REA routing text.

## Limits

- Book pages are unversioned; claims about the book are for the fetch on 2026-10-20 only.
- S1 covers the tag v0.8.2 only. Behavior on later 0.8.x or master is not checked.
- O4/O5/O7 are one local build (linux-x86-64, rizin 0.8.2 at /usr/bin/rizin); not verified on other platforms.
- No version-specific `iI` output schema was read beyond the handler call path.

## Draft

SOURCES.md rows (11-column contract shape; status `queued`; ids are placeholders for L1 to assign).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | rizin Handbook — https://book.rizin.re/ (`src/first_steps/commandline_options.html` §7; `src/refcard/intro.html` §136.5) | docs | B | Meaning of rizin `iI`, `iS`, `ie`, `-N`, `-q`, `-c` in rizin 0.8.x, as unversioned book text only | unversioned; fetched 2026-10-20T17:47:11-03:00; sha256 `5c30b9f6c7afbc80bd57192cc79ef3a600305c29ced2053e1c28766002dedfeb` (commandline_options), `5c16fc96aa8d9a3340f89187cdb223fca06f1ef3708ddd216eaac56dd72c7f4d` (refcard); `-q` line; `The i command uses the RzBin API` | Gives the user-facing meaning of `-q` (quit after -i and -c), `-N` (no user settings and scripts), and the `i` info family; does not pin the 0.8.x behavior of `iI`/`iS`/`ie`. | queued | 2026-10-20 | on-release | — |
| S0NN | rizin v0.8.2 source at tag — https://github.com/rizinorg/rizin/tree/v0.8.2 (commit `5a611eee2999d312317ff90d600e37dde0f58992`) | code | A | Behavior and help text of rizin 0.8.2 only for `iI`, `iS`, `ie`, `-N`, `-q`, `-c`; not later 0.8.x or master | v0.8.2 / `5a611eee2999d312317ff90d600e37dde0f58992`, 2026-02-01T21:52:21+04:00; `librz/main/rizin.c:128` (`-N` help), `:678-697` (`-N`/`-q`), `:930-933` (`scr.utf8`); `librz/core/cmd_descs/cmd_descs.c:12896-12897`, `:12955-12956`, `:13085-13086` (summaries); `librz/core/cmd/cmd_info.c:192-194`, `:242-248`, `:421-423` (handlers); sha256 `046219f7…c349c6`, `2cbea720…42943`, `2330263b…bfc3` | Version-pinned meaning of the four REA-executed info commands and flags, including that `-N` skips the rc file and sets `scr.utf8=false`, and that `-q` forces `scr.interactive`/`scr.prompt` off, which the book does not state. | queued | 2026-10-20 | on-release | — |

Rejected candidates: the release page (D5) is REJECTED for this scope: it documents only the v0.8.2 security and Haiku notes, no commands or flags (O12).

## Tooling

No installs or updates. Scratch clone and fetch files live under the system temp dir and were removed after reading.
