# ScoutRecord — PROVINCE.md pointer cells under a strict exact-token rule

Seat: `ScoutRecord` (scout, read-only recon). Wave `r80-w1`, round 80.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base blob: `16dfa009bf143080dfcdfc5f9ec34bd359536d90` (`PROVINCE.md` 643 lines, 85848 bytes,
sha256 `99d29a00ecabf492afee5ec1e393455761bf2947bac6ec1e25e14951b8752ca0`).
Declaration guard for `plans/round-80-claims.md`: `84d68e90f8a1ea3a3a7f94a208695c21023c0472`
(`git log -1 --format=%H -- plans/round-80-claims.md`).
Frozen rule under test (claims file): a pointer binds only when every declared token occurs in the
pointed lines as a **delimited token** — start/end of line, or a character outside
`[A-Za-z0-9._-]` on each side.

Evidence: `w1/ScoutRecord/receipt.json` (machine receipt), `w1/ScoutRecord/probe.json` (raw probe),
`w1/ScoutRecord/round79-live-at-base.json` (round-79 binder, live arm at base).
No lane production file was touched.

## 1. The five pointer cells

Extracted from the base blob with the same regexes the round-79 binder uses
(`RE_PIN`, `RE_GHIDRA_PTR`+`RE_GHIDRA_VALUE`, `RE_BASHRC_PTR`); `record_line` is the
pointer-bearing line, `span` the full regex match (the client label for the three pin cells sits at
the **end of the preceding line**, so the match crosses a newline).

| id | record_line | cell_text (paths/pins only) | pointed line(s) | token required | whole token |
|---|---|---|---|---|---|
| devin-pin | 16 (span 15–16) | ``Devin `rea-agents@6.7.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`)`` | `        "rea-agents@6.7.0",` | `rea-agents@6.7.0` | **yes** |
| omp-pin | 17 (span 16–17) | ``OMP `rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:12`)`` | `        "rea-agents@6.7.0",` | `rea-agents@6.7.0` | **yes** |
| kimi-pin | 18 (span 17–18) | ``Kimi `rea-agents@6.7.0` (`~/.kimi-code/config.toml:4722`)`` | `args = [ "-y", "rea-agents@6.7.0", "mcp" ]` | `rea-agents@6.7.0` | **yes** |
| ghidra-version | 27 | `` `application.version=12.1.4` (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties:17`) `` | `application.version=12.1.4` | `application.version=12.1.4` | **yes** |
| bashrc-exports | 27 | `` `/home/vgpnk/.bashrc:28-29` `` | `export GHIDRA_INSTALL_DIR="$HOME/.local/opt/ghidra_12.1.4_PUBLIC"` / `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk` | `GHIDRA_INSTALL_DIR=` **and** `JAVA_HOME=` | **yes** (both) |

Delimiter evidence (immediate neighbours of the occurrence; class = `[A-Za-z0-9._-]`):

| id | token | line | left | right | whole |
|---|---|---|---|---|---|
| devin-pin | `rea-agents@6.7.0` | 7 | `"` | `"` | yes |
| omp-pin | `rea-agents@6.7.0` | 12 | `"` | `"` | yes |
| kimi-pin | `rea-agents@6.7.0` | 4722 | `"` | `"` | yes |
| ghidra-version | `application.version=12.1.4` | 17 | start of line | end of line (`\n`) | yes |
| bashrc-exports | `GHIDRA_INSTALL_DIR=` | 28 | space | `"` | yes |
| bashrc-exports | `JAVA_HOME=` | 29 | space | `/` | yes |

Each token occurs exactly once in its pointed lines (one occurrence per line; the bashrc range
carries one token per line). Every pointed file also contains the declared pin exactly once at the
whole-file level (devin 1, omp 1, kimi 1), so no live longer token competes with a declared pin.

**shape hazard for the round-80 candidate (finding).** The three client cells do not read
`Devin `rea-agents@...`` on one line: the record is `... are Devin\n`rea-agents@6.7.0` (...)`.
A same-line cell regex would parse **0** pin cells and fail the live arm (`checks_total 5`).
The round-79 `RE_PIN` uses `\s+`, which crosses the newline; the strict binder must keep that.
The frozen fixture `record_template` writes each client cell on one line, so the fixtures alone do
not catch a same-line regression — only the live arm does.

**second shape finding.** The bashrc cell requires **two** tokens over a two-line range, one per
line. The rule must be "every declared token occurs somewhere in the pointed lines", not "all
tokens on one line"; the green fixture `gr02` exercises a token on the second line of a range.

## 2. Pointed-line digests and byte offsets

`line_sha256` is the round-79-compatible digest: sha256 over the pointed lines joined as read
(line endings preserved, i.e. `sha256sum` of `sed -n '<range>p' <file>`). Cross-checked with the
shell. Byte offsets are 0-based file offsets of the first pointed line (`grep -bn`).

| id | live path | line range | byte offset | pointed bytes | line_sha256 |
|---|---|---|---|---|---|
| devin-pin | `/home/vgpnk/.config/devin/mcp_config.json` | 7 | 87 | 28 | `d62ab8dad36380a4fd6fb3a90ee070feee0e34866f6f0bcebffb7133f6326a5d` |
| omp-pin | `/home/vgpnk/.omp/agent/mcp.json` | 12 | 269 | 28 | `d62ab8dad36380a4fd6fb3a90ee070feee0e34866f6f0bcebffb7133f6326a5d` |
| kimi-pin | `/home/vgpnk/.kimi-code/config.toml` | 4722 | 154109 | 43 | `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675` |
| ghidra-version | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties` | 17 | 632 | 27 | `e655d6c552eb40758474dfbc79dcbf290e71dc3974df4782fcf7c2ac57e9d512` |
| bashrc-exports | `/home/vgpnk/.bashrc` | 28-29 | 1426 | 112 | `db162b4cbfd4a0cd2033e63c095b25f2155f3d165b190935da338faf490c9ac4` |

Devin and OMP digests coincide because the two pointed lines are byte-identical
(`        "rea-agents@6.7.0",`); the paths and files differ.

## 3. Over-refusal check (strict rule vs. the record's other occurrences)

Prompt names lines 9, 12, 47; the base blob carries **eight** non-cell `rea-agents@` occurrences on
seven lines. All are whole-token occurrences and none parses as a client cell:

| line | token | context (truncated) | delimiters | whole |
|---|---|---|---|---|
| 9 | `rea-agents@6.7.0` | ``and Kimi all pin `rea-agents@6.7.0` (207 MCP tools + 153 CLI commands;`` | backtick/backtick | yes |
| 12 | `rea-agents@6.5.0` | ``... superseded client pin `rea-agents@6.5.0` (same 207/153 counts; ...`` | backtick/backtick | yes |
| 12 | `rea-agents@6.4.0` | ``Historical: Kimi resolved `rea-agents@6.4.0` (historical ...`` | backtick/backtick | yes |
| 47 | `rea-agents@6.4.0` | `` `npx -y rea-agents@6.4.0 --version` → `6.4.0` `` | space/space | yes |
| 322 | `rea-agents@6.5.0` | ``- Native reader evidence-ID identity at `rea-agents@6.5.0` now rests ...`` | backtick/backtick | yes |
| 345 | `rea-agents@6.5.0` | ``... provider-free); `rea-agents@6.5.0` \| `inspect-rust-binary ...`` | backtick/backtick | yes |
| 358 | `rea-agents@6.5.0` | ``... provider-free); `rea-agents@6.5.0` \| `inspect-sqlite-database ...`` | backtick/backtick | yes |
| 438 | `rea-agents@6.5.0` | ``... `REA_UNBLOB_COMMAND` = unblob 26.6.4. **Use:** `npx -y rea-agents@6.5.0 extract-firmware ...`` | space/space | yes |

`RE_PIN` finds **exactly three** matches in the base blob (record lines 15–16, 16–17, 17–18, one per
client); lines 9, 12, 47 (and 322/345/358/438) do not match
``(Devin|OMP|Kimi)\s+`rea-agents@...` (`<pointer>`)``, so they can neither displace nor duplicate a
cell. `RE_BASHRC_PTR.search` and `RE_GHIDRA_PTR.search` return the line-27 pointers
(`.bashrc:28-29`, `...application.properties:17`) as first matches; the later `.bashrc:63-69/:34/:66/:29/
:63/:61` mentions never win.

**Verdict: no cell is newly refused by the strict rule.**
Grounds, each verified:

1. The rule checks tokens on each cell's **pointed lines** only; the record's prose occurrences are
   never the token source (round-79 `bind()` reads the pointer target file; `PROVINCE.md` is not
   consulted for token matching). The eight non-cell occurrences cannot enter a cell's verdict.
2. All eight non-cell occurrences are themselves whole-token occurrences (previous table), so even
   a hypothetical whole-record strictness scan refuses nothing.
3. Each pointed line's declared token is whole (section 1), including the two bashrc exports and
   the Ghidra property.
4. No pointed file holds a longer token that the declared pin is a prefix of (`rea-agents@` occurs
   exactly once per client config; `GHIDRA_INSTALL_DIR=` / `JAVA_HOME=` do not collide with any
   longer same-prefix variable on lines 28–29).

Mutation sanity (the detector is not vacuous): `  "rea-agents@6.7.05",` contains
`rea-agents@6.7.0` non-whole (right neighbour `5`), and `xGHIDRA_INSTALL_DIR=` is non-whole (left
neighbour `x`); both correctly fail the delimited test (independent `grep -P` lookarounds, 0 hits).

## 4. File lengths (line ranges cross-check)

`wc -l` and byte length of every pointed file (three client configs exist; the prompt's "two" is a
subset — all are reported). Full-file digests are recorded for the client configs as digests only;
no `env` block or token value is copied.

| key | path | lines | bytes | sha256 (whole file) |
|---|---|---|---|---|
| devin | `/home/vgpnk/.config/devin/mcp_config.json` | 17 | 406 | `9159ca91487a34daf86d203f04bf747143e750f3508d0f912179e00d8a5f1c39` |
| omp | `/home/vgpnk/.omp/agent/mcp.json` | 104 | 2909 | `fa3517758a5ae4596ac53dfb679b3236b49c88570ab3e099e2ef862251057ab6` |
| kimi | `/home/vgpnk/.kimi-code/config.toml` | 4746 | 154754 | `f4c98c23269c07ed25bb2f8247c52f9c6466af4782712e083305ec2bed237be4` |
| bashrc | `/home/vgpnk/.bashrc` | 102 | 4544 | `7c430e1e4d9261c7297255a9d1956a1bd63b7320e0c1db8bb82a382c85f922ae` |
| ghidra_properties | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties` | 17 | 659 | `e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67` |

Cross-checks: kimi pointer `:4722` is inside 4746 lines; bashrc range `28-29` inside 102;
application.properties `:17` is its last line (632 + 27 = 659 bytes); devin `:7` inside 17;
omp `:12` inside 104.

## 5. Live arm at base (baseline the strict binder must not regress)

`python3 -I -B tools/round-79/pointer-bind.py --root . --rev 16dfa009... --json-out <evidence>`
exits 0 with `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`, `ok true`;
`--validate` reports `{"defects": [], "checks": 5, "matched": 5}`. Instrument sha256
`40905d396245313bedb7d0ae25b63f322b39e8e877371630e84d7616f12cb877`. The five per-cell digests in
that receipt equal section 2 exactly, and every `path_is_declared` is true. A strict candidate on
the same measured rev must reproduce 5/5 with these same digests.

## Findings

1. All five cells bind **5/5 as whole tokens** on their pointed live lines; none depends on a
   substring occurrence. The frozen red fixtures are synthetic (`@6.7.05`, `@6.7.00`), not copies
   of live state — the live state contains no substring trap.
2. Strict rule causes **zero over-refusals**: the eight other `rea-agents@` occurrences are all
   whole and none parses as a cell; exactly three `RE_PIN` matches exist.
3. Record-shape hazard: the three client labels sit on the **preceding** line; a same-line cell
   regex parses 0 cells and fails the live arm. Keep `\s+` (newline-crossing) semantics.
4. The bashrc cell is a **two-token, two-line** range (`GHIDRA_INSTALL_DIR=` on 28, `JAVA_HOME=` on
   29); token matching must scan the whole range, not one line.
5. Ghidra and bashrc cells share record line 27; first-match extraction order yields
   `application.properties:17` and `.bashrc:28-29` — the later `.bashrc:` mentions are inert.
6. Base round-79 live arm is 5/5 and validate-clean; the strict binder must preserve the five line
   digests in section 2.

## Limits

- Live host files were read once at recon time; their bytes can drift after this receipt. The
  digests pin the observed state, not a guarantee.
- Whole-token verdicts were computed by a Python boundary test and independently by PCRE
  lookarounds; both formulations agree, but a candidate with a different tokenisation (e.g.
  maximal-run) should be re-scored by the frozen strictness battery.
- No git fixture repo was created. The only writes outside the evidence dir were under the
  scratch root `/fast/scratch/hyaku/kaidoku-r80/ScoutRecord/`, removed before yield; no `/tmp`
  or other scratch write occurred.

## Evidence files

- `.ufo/waves/round-80/w1/ScoutRecord/receipt.json` — acceptance receipt (`cells`,
  `over_refusal_check`, `file_lengths`).
- `.ufo/waves/round-80/w1/ScoutRecord/probe.json` — raw probe (extraction, occurrences, offsets).
- `.ufo/waves/round-80/w1/ScoutRecord/round79-live-at-base.json` — round-79 live arm at base.
