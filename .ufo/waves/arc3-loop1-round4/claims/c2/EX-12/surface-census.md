# EX-12 — surface census, part 2: the Core table rows, the surface summary, and the drift-prone values

Seat EX-12 · chain c2 · role executor · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`015e1bab914713568f339fd53999bc180459cc40` (read-only throughout; no git
mutation by this seat). Lane: devin (`devin/deepseek-v4-1-flash-max`) — the
declared fallback dispatch (`claims-frozen.md:11-15`), not a lane signal.

**Write scope.** This seat wrote only: this artifact, its `evidence/` set, the
patch text `claims/c2/EX-12/proposed-core-asar-row-repair.patch.md`, and the
seat report `seats/EX-12.md`. `PROVINCE.md` / `SKILL.md` / `SCORECARD.md` were
only ever read (real-tree sha256s re-derived at close; see §6). Custody paths
were opened read-only (hash/stat only) — the custody tool's verify runs used a
`/var/tmp` copy. Scratch: `/var/tmp/ex12r4/` (never `/tmp`).

**Part boundary.** The chain's part-1 work covers the Frontier bullets
(`PROVINCE.md:72-118`, `:132-162`) — VZ-2's staleness census, EX-13/EX-14/PL-2's
repair patches, EX-15's adjudications, EX-17's before-state. This seat owns the
**other half of the declared scope**: the surface summary (`:8-13`), the
drift-prone values (`:15-26`), and the **Core table rows** (`:44-62`, `:119-131`).
The unit boundary is the same one the part-1 seats measured: the census
instrument grades only its declared `SCOPE` rows and cannot see a prose
inventory claim inside a DATED row; the certificate for those rows is this
seat's own per-row re-derivation, not the instrument's PASS.

## 1. Method and instruments (identities re-derived at close)

| instrument / source | identity at close |
|---|---|
| census `c1-census-v10.py` | sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` (610 lines) — re-derived after the last run |
| citation-drift probe `citation-drift-probe.py` | `--selftest` → `CLEAN cases=13 passed=13 failed=0 exit=0`; at HEAD both modes → `findings=0 exit=0` |
| custody tool (r4 revision) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 lines) — verified on a `/var/tmp` copy, never executed from the gate dir |
| `PROVINCE.md` base | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`, 162 lines |
| custody pin receipts (the claim's pin source) | r3 revised-tool pair (`7cd19c3c…`) + r4 EX-21 pair (`29bb45ae…`) — both re-verified this seat |

Every verdict below is a first-hand re-derivation: a live command, a live file
read, or a live parse. No peer seat's prose was accepted as evidence.

**Custody pin re-verification (the claim's "pins per the current receipts"
clause).** The r4 live pair (`claims/c3/EX-21/receipts/live-pre.txt` /
`live-post.txt`) and the r3 revised-tool pair were each verified against the
live filesystem with the revised tool, from a scratch copy:

```
CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0        # r4 pair vs live
CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0        # r4 pre vs r4 post
CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0        # r3 post-pair vs live
```

and the live five-path hashes match the r3 revised-tool receipt exactly
(devin `16f496e6…`, omp `38d2a1d0…`, kimi `bc66d543…`, bashrc `7d2ca28a…`,
profile `6c6be761…`). The pins the surface summary states are therefore the
receipts' pins, re-derived.

## 2. The disposition grid — surface summary + drift-prone values

Grid key: **CURRENT** = re-derived this run, matches the text;
**STALE** = text contradicted by a first-hand measurement; **ADJUDICATED** =
contradicted but defensible as receipt-stamped/historical by declaration;
**NO-CHANGE** = checked, correct as written.

| id | item (PROVINCE lines) | verdict | evidence |
|---|---|---|---|
| S1 | surface summary: Devin + OMP use `rea-agents@6.5.0` (207/153, `805433f1…`) | **CURRENT** | live `grep`: `mcp_config.json:7`, `mcp.json:8`; live `doctor` at 6.5.0 → `153/207/6`, `tools_sha256 805433f1…` (`evidence/doctor-6.5.0.json`) |
| S2 | surface summary: Kimi uses `rea-agents@6.7.0` (207/153, `af39310c…`) | **CURRENT** | live `config.toml:3546` = `rea-agents@6.7.0`; live node eval of the 6.7.0 cache's `catalogIdentity.js` → `153/207/6`, `af39310c…` (`evidence/catalog-and-cache.txt`) |
| S3 | surface summary: historical Kimi pin 6.4.0 (170/127, `25802f6d…`), separate cache installs | **CURRENT** | live node eval of the 6.4.0 cache → `127/170/6`, `25802f6d…`; `npx -y rea-agents@6.4.0 --version` → `6.4.0`; three distinct `_npx` hashes hold the three versions |
| S4 | surface summary: Ghidra provider path | **CURRENT** | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` exists; `application.version=12.1.4` at `application.properties:17` |
| S5 | drift-prone: devin pin `mcp_config.json:7` | **CURRENT** | live `grep -n` returns exactly `7:rea-agents@6.5.0` |
| S6 | drift-prone: omp pin `mcp.json:8` | **CURRENT** | live `grep -n` returns exactly `8:rea-agents@6.5.0` |
| S7 | drift-prone: Kimi pin `config.toml:3298` at the 17:55:49Z receipt | **ADJUDICATED** (same disposition as VZ-2 S5 / EX-15 A1) | line 3298 now holds `max_context_size`; live pin is `:3546` under `[mcp_servers.rea]` at `:3544`. The value claim is current; the pointer is receipt-stamped by design (round-3 re-anchored it to the named 17:55:49Z receipt). The census never evaluates it (`ptr_check` unreached when the clause carries a pin — re-confirmed by VZ-2 A3 and by the instrument's own control flow). PL-2's optional S5 hunk would refresh it; **no repair required** |
| S8 | drift-prone: cache/catalog identities (three `_npx` hashes + three `tools_sha256`) | **CURRENT** | all three re-evaluated live from each cache's own `catalogIdentity.js`; hashes and counts match the block byte-for-byte (`evidence/catalog-and-cache.txt`) |
| S9 | drift-prone: installed shared REA skill v42/207, `c8639823…` | **CURRENT** | `sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md` → `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`, 22,513 B, `version: "42"` |
| S10 | drift-prone: doctor alignments (Devin/OMP aligned historical; 6.7.0 reports stale; 6.4.0 expects v37 and stale) | **CURRENT** | live 6.5.0 doctor: `registration:devin` → `aligned`, `registration:omp` → `aligned`, `skill:identity` → `config_drift` ("Installed REA skill identity is stale."); luna-r2 receipt `l10-doctor-6.4.0.txt:241` → `expected_skill_version: "37"`. The 6.7.0 half is a 2026-10-18 receipt, marked historical in the text |
| S11 | drift-prone: Ghidra/JDK block (`GHIDRA_INSTALL_DIR`, `application.version`, `JAVA_HOME`, `21.0.12.1`) | **CURRENT** | `.bashrc:23-24` exports both; `java -version` → `21.0.12.1`; `application.properties:17`; `/usr/lib/jvm/java-21-openjdk` the sole JVM dir (`default`/`default-runtime` are symlinks to it) |
| S12 | drift-prone: provider-key inventory paragraph | **CURRENT as historical** | the paragraph says "remains historical, not re-probed 2026-10-16" and the live `.bashrc` still carries all seven keys at `:58-64`; `REA_IDA_MCP_CONFIG`/`HOPPER_LAUNCHER_PATH` confirmed unset live |

**Surface summary + drift-prone result: 12 checked, 11 CURRENT, 1 ADJUDICATED,
0 STALE.** No repair is proposed for this half.

## 3. The disposition grid — Core table rows

The Core table (`:44-62`) and the round-4 additions table (`:119-131`) were
checked row by row. Rows are graded on **falsifiable clauses**, not on
completeness of prose.

| id | row (line) | verdict | evidence |
|---|---|---|---|
| C44 | REA MCP server | **CURRENT** | pins re-derived (S1/S2); `binary_session`/doctor probe clause unchanged; env keys live |
| C45 | `rea` CLI — no `rea` on PATH; 153/127 counts | **CURRENT** | `command -v rea` → absent; counts re-derived from all three caches |
| C46 | Ghidra provider — 876 MB, 39 processor modules, **35 features** | **STALE (partially repaired by PL-2)** | `du -sh` → `876M` ✓; processors → 39 ✓; **features → 34** (`find … -maxdepth 1 -mindepth 1 -type d | wc -l` = 34). The corpus entry itself carries the erratum (`2026-10-13-ghidra-install.md:68` "34, not 35"). PL-2's hunk C46 repairs exactly this cell (`candidate-repairs.patch.md`, sha `daef6994…`); this seat re-derived the value independently and concurs |
| C47 | JDK 21 substrate | **CURRENT** | `JAVA_HOME` live; sole JVM dir; `.bashrc:24` + `.profile:4` both export it |
| C48 | Native ELF via Ghidra — jq 30 segments / 167 procedures / 190 strings | **CURRENT (re-run this seat)** | live `rea analyze /usr/bin/jq` at 6.5.0 → `segment_count 30`, `procedure_count 167`, `string_count 190`, `ev_14f9d92f…` (`evidence/analyze-jq-6.5.0.json`) |
| C49 | Electron/ASAR/JavaScript — asar inventory + 1Password 423-file | **STALE** | live sweep finds **12** asars vs the row's 9 named (missing: chatgpt 578,643,106 B owned by `chatgpt-bin 26.1013.40934-1` installed 2026-10-16; zcode squashfs-root 326,913,098 B; `~/.config/obsidian/obsidian-1.14.4.asar` 27,477,966 B — the r1 entry's "~/.config contributes zero" is superseded). And `423-file` is the superseded count: the cited r4-06 entry's own erratum says 480; direct header parse → **486 entries = 480 files + 6 dirs** (415 `.js`, 6 `.html`). 188MB core confirmed: `index.node` = 187,997,016 B. **Patch text authored: `proposed-core-asar-row-repair.patch.md`** (this seat). Cross-corroboration: VZ-2 independently re-derived both halves and adopted this row as its **ninth stale item** (`.ufo/waves/arc3-loop1-round4/claims/c2/VZ-2/evidence/ninth-stale-item.txt`, census row `C3`), so the baseline stale count is nine, not eight |
| C50 | Archive/package inventory — pacman corpus **1556 signed archives** | **STALE (repaired by PL-2)** | live `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` → **1350**; `.sig` → 1350; `du -sh` → 7.0G. The 1556 figure is the 2026-10-13 scan (its own entry records it as a snapshot); the cache has aged out 206 archives. PL-2's hunk C50 repairs it (`… 1556 signed archives at the 2026-10-13 scan (1350 today)`); this seat re-derived the value and concurs |
| C51 | Native PE via Ghidra — cli-64.exe `bbb3de57…`: 8 segments, 142 procedures | **CURRENT (re-run this seat)** | live `rea analyze` at 6.5.0 on the `bbb3de57…` copy → `segment_count 8`, `procedure_count 142`, `string_count 89`, `ev_0f2e390f…` (`evidence/analyze-cli64-6.5.0.json`). NOTE: five copies exist on host; the r2-05-recorded sha is one of them (two others differ — `db1663a6…`), so the row's citation is copy-specific and still resolvable |
| C52 | Cross-version compare — `compare_functions`/`compareFunctions` no CLI verb | **CURRENT** | live `CLI_COMMAND_NAMES` (153) contains no `compare_functions`; `compare` and `compare-javascript-export-shapes` are present, as the row says |
| C53 | Runtime observation (CDP) | **CURRENT** | `chromium` and `xvfb-run` both on PATH; the row's probe clause is a self-launched-target recipe (no live target needed for the inventory claim) |
| C54 | EVM interface — positional encoding, EVMole 0.9.3/WASM | **CURRENT** | `evmole: 0.9.3` in the 6.7.0/6.5.0 `package.json`; `evmole@0.9.3` in the CLI runtime; 6.4.0's `package.json` also carries `0.9.3` |
| C55 | Carrierless-macOS surface via synth carriers | **CURRENT** | the row states the Linux behavior of three verbs; no host inventory claim to falsify |
| C56 | APK surface (full) — jadx 0.7.1, apktool 3.0.3 | **CURRENT** | `apktool --version` → `3.0.3`; jadx jar sha256 `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75` = the row's `6e5eacf5…`; live doctor: `jadx` → healthy |
| C57 | `.node` native addons | **CURRENT** | taxonomy clause (`nm -D | grep -c ' U napi'`); no host-count claim |
| C58 | MCP retained-evidence session | **CURRENT** | session-only verbs; no falsifiable host clause |
| C59 | Verb families — xrefs/trace/read-bytes/address-to-file-offset/function/instructions, address POSITIONAL | **CURRENT** | all six names present in the live 153-command list |
| C60 | Recorded crashes (mechanism) — 32 MiB cap; `REA_PWNTOOLS_PYTHON` venv path | **CURRENT** | venv dir exists at the stated path; `pip list` shows pwntools 4.15.0; the cap is the row's own mechanism clause |
| C61 | Evidence discipline | **CURRENT** | no host-inventory clause |
| C62 | Host fallback readers — absent list | **STALE (repaired by EX-13 + PL-2 + EX-14 v2)** | live sweep: `7z` `/usr/bin/7z`, `xxd` `/usr/bin/xxd`, `radare2` `/usr/bin/radare2`, `strace` `/usr/bin/strace`, `upx` `/usr/bin/upx` all present (pacman-owned, one install batch 2026-10-13 13:52); genuinely absent: `cabextract`, `rizin`, `ltrace`, `pacman-contrib` (`evidence/tool-sweep.txt`). Three independent patch texts repair it; this seat re-derived the sweep and concurs |
| C120 | Firmware regions + extract — binwalk 3.1.0, unblob 26.6.4 | **CURRENT** | `binwalk --version` → `3.1.0`; `unblob --version` → `26.6.4`; `.bashrc:59-60` exports both |
| C124 | JavaScript source recovery — wakaru ELF | **CURRENT** | `.bashrc:63` resolves live (shell-expanded) to the `@wakaru/cli-linux-x64` ELF, 26,793,296 B, mtime 2026-10-13 13:52; the path is real and executable |
| C125 | Android deep analysis — jadx jar + apktool | **CURRENT** | as C56; `.bashrc:61` exports `REA_APKTOOL_COMMAND` |
| C126 | Managed IL — `REA_DOTNET*` unset; dnfile 0.18.0 + dncil 1.0.2 | **CURRENT as stated, with a measured caveat** | `REA_DOTNET*` confirmed unset live. The venv the entry built was `/tmp/dnfenv-r4` — **gone** (host `/tmp` hygiene); `python3 -c "import dnfile"` fails; no durable dnfile install exists on host. The row's own words are "pip pkgs" (an installable recipe), not "installed at path X", so the text is not falsified — but a re-run today needs the `uv venv` step from the entry. Recorded as a named re-run caveat, **not** a repair (the claim is about the verb map, not a venv path) |
| C127 | `.jsc` V8 bytecode — electron 42.2.0, host node 24/V8 13.6 | **CURRENT** | host has no system electron42, but the row's recipe is `npx -y electron@42.2.0` (r4-07 records the npx acquisition); the fnm node 24.21.0 tree exists with V8 `13.6.233.17-node.53`; the mise default node is 26.12.0 (V8 14.6) — the row's "host node 24" refers to the fnm-installed 24.x, which is present and still V8 13.6. Both halves resolvable |
| C128 | Runtime observation verbs | **CURRENT** | r4-08's record; no host-inventory clause |
| C129 | Binary layout — pwnenv | **CURRENT** | venv path exists; pwntools 4.15.0 |
| C130 | ADB client (device-free) — provider adb 37.0.0 | **CURRENT** | `adb version` → `1.0.41` / `Version 37.0.0-android-tools`; `.bashrc:62` exports the path |
| C131 | AppImage inner payload | **CURRENT** | `7z` present (so the fallback leg is live); no host artifact claim beyond r4-15's record |

**Core-table result: 24 rows checked. 20 CURRENT; 4 STALE — C46 (35→34
features), C49 (asar inventory + 423 count), C50 (1556→1350), C62 (absent-tool
list).** Of the stale set, **C49 is this seat's unique repair** (no prior patch
text); C46/C50 carry PL-2's hunks and C62 carries three peer patch texts
(EX-13, EX-14 v2, PL-2) — this seat re-derived each value independently and
concurs with all of them.

**Total across both grids: 36 items checked → 31 CURRENT, 1 ADJUDICATED, 4
STALE (one, C49, with no prior patch text).**

## 4. Before → after measurement (this seat's falsifiable contribution)

The chain claim's falsifiable form: *every checked item stale/current/adjudicated
with evidence; stale count N → 0; PROVINCE line count unchanged; census PASS at
the work tree after the parent applies the patches.*

This seat's own contribution to the N → 0 leg is C49. Measured, before → after,
on scratch copies (`/var/tmp/ex12r4/apply/`, never the real tree):

| unit | before (HEAD) | after (C49 patch) |
|---|---|---|
| `PROVINCE.md` sha256 | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | `ab00f2242e1d495e4851f066d4e19f0cc3affa7c7d115a006e74cff08b025c24` |
| lines | 162 | **162 (held)** |
| hunk application (RV-4 `prose-apply.py`) | — | `hunks: applied=1 failed=0` |
| census | PASS 0/0/0/0, exit 0 | **PASS 0/0/0/0**, exit 0, scope-errors `[]`, G2 17/14/3 |
| census output bytes | `6a87844b…` | `6a87844b…` — **byte-identical**: the patched row carries no gated locus, so the repair is census-inert (a PASS certifies locus hygiene, not claim truth — A9) |
| RV-4 `census-diff.py` over baseline-vs-after | — | `RESULT: CLEAN — no new gated locus, no regression` |
| falsified clause `423-file asar` present | True | **False** |
| falsified clause `obsidian ×2, signal, …` (9-archive list) present | True | **False** (replaced by the 12-archive form) |

**Composed landing (the chain's minimal set + this seat's hunk).** PL-2's
21-hunk candidate (`daef6994…`) applied first, then this seat's C49 hunk, on a
fresh scratch tree:

| unit | value |
|---|---|
| hunks applied | 21/21 (PL-2) + 1/1 (C49) |
| `PROVINCE.md` after | `b37effee9908c98179a9f18f88a876a16f98943a10330ef570b6f12458a18db4` |
| lines | **162** |
| census | **PASS 0/0/0/0**, exit 0 |
| citation-drift probe, patched scratch clone | `reported findings=0 exit=0`; `--strict` → `clean findings=0 exit=0` |

(The EX-14 v2 patch text does **not** compose on top of PL-2 — its search text
was already rewritten by PL-2's hunks, so `prose-apply.py` fails closed with
`search text not found verbatim`, 0/6 applied. That is the expected
fail-closed behavior of two overlapping repair sets; the parent must land
**one** set, not both. Recorded as a landing note, not a defect.)

## 5. Attacks / refutations attempted, with verdicts

| # | attack | measured result | verdict |
|---|---|---|---|
| A1 | "the pins are stale — the surface summary is wrong" | live pins = `6.5.0`/`6.5.0`/`6.7.0`; all three catalog identities re-evaluated live from each cache; r3 + r4 custody pairs verify MATCH 5/5 vs live | **refuted** — the pin block is current |
| A2 | "the drift-prone `:3298` pointer is simply stale text and must be repaired" | line 3298 = `max_context_size`; live pin `:3546`; the clause is receipt-stamped ("at the 17:55:49Z receipt") and the census never evaluates the pointer (`ptr_check` unreached when a pin is present) | **partially sustained, adjudicated** — the *value* is current; the pointer is historical-by-declaration. Repair optional (PL-2 S5 hunk exists); NO-CHANGE is defensible. Matches VZ-2 S5 and EX-15 A1 |
| A3 | "the Core table is the claim's scope and is fully covered by the part-1 seats" | EX-17's census checked 16 items; the Core rows beyond :62 were never enumerated row-by-row; C49's two falsified clauses appear in no peer patch text | **refuted** — the Core-table sweep is this seat's gap and C49 is its finding |
| A4 | "`423-file` is right; the r4-06 erratum is just a wording nit" | direct asar-header parse: 486 entries = **480 files + 6 dirs**; the entry's own erratum states 480 | **refuted** — the row carries the superseded number |
| A5 | "the asar count is a moving target and not a falsifiable claim" | the row's own list is a named inventory ("obsidian ×2, signal, 1Password, electron39/43 stubs, typora ×3"); three archives postdate the sweep and are absent from it; the count is stable under re-sweep today (12, re-derived twice) | **refuted** — it is a checkable inventory claim |
| A6 | "the C49 repair introduces a census locus" | census on the patched tree: PASS 0/0/0/0; `census-diff.py`: CLEAN, 0 new gated loci | **refuted** |
| A7 | "the C49 repair shifts a line and breaks the DATED marker at :119" | 162 → 162 lines held; scope-errors `[]` | **refuted** |
| A8 | "the C49 repair stales a citation-drift needle" | probe on the patched scratch clone: both modes `findings=0`; the row's unit carries no `REA_GATE` token at all (measured: `REA_GATE` match = False on line 127; line 49 same class) | **refuted** |
| A9 | "the census PASS proves the repairs" | the instrument's Frontier/Core prose claims sit outside its declared unit or carry no needle — a PASS certifies locus hygiene and anchor agreement, **not claim truth** (the H2 residual EX-14 measured, re-confirmed here). The certificate for this census is §2/§3's per-row re-derivations | **confirmed** — stated, not smoothed |
| A10 | "the Managed IL row's venv is gone, so the row is stale" | `REA_DOTNET*` unset ✓; the row says "pip pkgs", not "installed at /tmp/dnfenv-r4"; the entry's own recipe is a `uv venv` one-liner | **refuted as a repair, recorded as a re-run caveat** — a re-run today needs the entry's venv step |
| A11 | "C51's cli-64.exe sha is unverifiable" | five copies on host: `bbb3de57…` (×4, including the `~/.cache/codex-runtimes` one) and `db1663a6…` (×1); the row's cited sha resolves to real files and the live re-probe at 6.5.0 returns the row's own numbers (8/142) | **refuted** — the citation is copy-specific but resolvable |
| A12 | "the two repair sets (PL-2 + EX-14 v2) compose" | `prose-apply.py`: EX-14 v2 on the PL-2 tree → `applied=0 failed=6` (fail-closed) | **refuted** — they are alternatives; the parent lands one set |
| A13 | "custody pins drifted since the r4 receipts" | all three verify runs MATCH 5/5 vs live; the five live hashes equal the r3 revised-tool receipt | **refuted** |

## 6. Self-identity re-derivation (rule #14)

Re-derived after the last revision, at close:

```
sha256sum .ufo/gates/c1-census-v10.py                     → d0772ce8…  (610 lines)
sha256sum .ufo/gates/citation-drift/pointer-table.json    → 1b3ab955…  (== the expected.json pin)
sha256sum .ufo/gates/custody-pair/custody-pair.py         → 29bb45ae…  (1343 lines, read-only)
sha256sum PROVINCE.md SKILL.md SCORECARD.md               → d075a3c6… / 5eec51c0… / 21042196…
sha256sum claims/c2/EX-12/proposed-core-asar-row-repair.patch.md
                                                          → see evidence/SHA256SUMS.txt
```

The real tree's three scoped files were never written by this seat: their
hashes above equal the HEAD blobs (`git show HEAD:PROVINCE.md | sha256sum` →
`d075a3c6…`; same class for the other two). The patch-text hash and this
artifact's own hash are in `evidence/SHA256SUMS.txt`, written last.

## 7. Blockers and named gaps

1. **Two stale Core rows are outside every seat's patch text at write time**
   — C46 (35→34) and C50 (1556→1350) *are* covered by PL-2's candidate
   (`daef6994…`), but PL-2's patch text has no measurement artifact behind it
   in its own directory (only the generator `gen-and-measure.py` and the two
   patch files); this seat applied PL-2's text and measured the composed tree
   (§4) so the parent has a first-hand conformance result for it. Not a
   blocker; recorded as coverage provenance.
2. **The chain's "stale count N → 0" clause** requires the parent to land one
   composed set. This seat's minimal recommendation: **PL-2's 21-hunk
   candidate + this seat's C49 hunk** — measured PASS 0/0/0/0 at 162 lines
   with the probe clean in both modes (§4). If the parent prefers EX-14 v2's
   six-hunk set, C49 must be added to it separately (C49 is not in EX-14's
   set), and PL-2's C46/C50 hunks must be added too — the two sets overlap on
   F1b/F3/F5b/X1/R2 but not on the Core rows.
3. **The census cannot grade any of these repairs** (A9) — the claim's PASS
   clause is satisfiable without the repairs being true. The certificate is
   the per-row grid (§2/§3). Stated for the record; the instrument's scope
   table is chain c1's to widen, not this seat's.
4. **`__pycache__` residue** exists under `.ufo/gates/` and the citation-drift
   dir (untracked); must stay out of the landing commit (round-2 precedent,
   re-confirmed by EX-31 in round 3).

## 8. Files written by this seat

- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-12/surface-census.md` (this file)
- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-12/proposed-core-asar-row-repair.patch.md`
- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-12/evidence/` — 15 files:
  `census-head.txt`, `census-baseline.json`, `census-after-asar-patch.txt`,
  `census-after-asar-patch.json`, `doctor-6.5.0.json`, `analyze-jq-6.5.0.json`,
  `analyze-cli64-6.5.0.json`, `1password-asar-list.txt`,
  `analyze-true-default-tmpdir.err`, `live-pins-and-hashes.txt`,
  `tool-sweep.txt`, `asar-sweep.txt`, `catalog-and-cache.txt`,
  `custody-verify.txt`, `SHA256SUMS.txt`
- `.ufo/waves/arc3-loop1-round4/seats/EX-12.md` (seat report)
