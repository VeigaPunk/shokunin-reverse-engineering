# R39W2C2TableReview — the SKILL.md SquashFS triage table (eight rows) against its cited sources

VERDICT: **DEFECTS FOUND** — every row's cause is true for the corpus shapes and the frozen table
labels all six spot-checked held-out envelopes correctly (the 20/20 counter verdict is consistent),
but two cells exclude wave-1-**measured** outcomes that three wave-1 seats explicitly required the
freeze to widen (row 5 `published files = 0`, row 8 `published files = >0`), two causes are wrong or
over-specific per the cited sources (row 6 omits the symlink-loop branch of `MaliciousSymlinkRemoved`;
row 7 claims symlink for a gap REA emits for every non-file entry, `kind` enum `["symlink","special"]`),
and row 4's action prescribes a PATH-wrapper mechanism that wave-1 itself recorded as untested
`[INFERENCE]` and that is unsafe if left installed.

## 0. Scope and method

Leaf seat, round 39 wave 2. Target: the eight table rows after `<!-- sqfs-triage-table v1 -->`
(`SKILL.md:333` marker, `:334` header, rows `:336`-`:343`) inside rule block "SquashFS
`extract-firmware` outcome triage (round 39)" (`SKILL.md:316-331`). For each row: is the
`cause -> action` true per the cited source; is any action wrong or unsafe; do the rule block's three
citations point at the paragraphs they claim. No frozen predicate, counter, carrier, oracle or table
was changed; the only writes are this report and `w2/artifacts/R39W2C2TableReview/`.

Method: read the pinned sources (installed copies, byte-identity re-verified below), read the frozen
interpreter `tools/round-39/sqfs-triage.py` (matching semantics: `rule_matches`/`classify` at
`:441-472`, features at `:341-421`), cross-check every row against the wave-1 measurement reports it
derives from, and run the **frozen** interpreter read-only on (a) six held-out envelopes and (b) four
minimal envelopes I constructed in scratch that reproduce wave-1-measured feature vectors the corpus
does not contain. Exact commands and outputs: `w2/artifacts/R39W2C2TableReview/demo-*.txt`.

## 1. Source identity (byte-identity re-verified, not assumed)

| source | installed copy | check | result |
|---|---|---|---|
| S112 | `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` | `cmp` vs `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | IDENTICAL |
| S118 | `…/unblob/extractor.py` | `cmp` vs tag 26.6.4 | IDENTICAL |
| S120 | `…/unblob/report.py`, `…/unblob/extractors/command.py` | `cmp` vs tag 26.6.4 | IDENTICAL |
| S119 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/{domain/firmware/firmwareAnalysis.js,firmware/FirmwarePublication.js,firmware/FirmwareReports.js}` | `cmp` vs `registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` (package.json `version: 6.5.0`) | IDENTICAL |
| S121 | fetched fresh: `onekey-sec/sasquatch` tag `sasquatch-v4.5.1-6` `squashfs-tools/unsquashfs.c` (4619 lines) and `debian/rules` (23 lines) | copies in artifacts dir | pinned source itself |

unblob dist-info: `unblob-26.6.4.dist-info`, `Version: 26.6.4`. The task's byte-identity premise
holds for every file this review cites.

## 2. Row-by-row review

### Row 1 — `no-squashfs-chunk` (`SKILL.md:336`) — cause TRUE, action safe

- "a non-4 `s_major`": true — the v4 patterns pin `s_major` only: BE `73 71 73 68 [24] 00 04`
  (S112:522), LE `68 73 71 73 [24] 04 00` (S112:463); a non-4 `s_major` matches no v4 pattern, so no
  chunk is created. Corroborated by the held-out generator's own note ("the v4 handler patterns pin
  `s_major` only, which is why s_minor 5 still matches and s_major 9 does not",
  `w1/R39C2HeldoutGen.md:135-136`).
- "a `bytes_used` past the end" / truncated: true — unblob's finder drops the chunk silently:
  `finder.py:106-108` `if chunk.end_offset > context.file_size: logger.debug("Chunk overflows file"…);
  return Scan.Continue` — debug log, no report. Measured: `TT-be-trunc` (H=∅, G=∅, P=0,
  coverage `complete`, `w1/R39C2ReconMarker.md` §5.1) and `full-not-squashfs` (`w1/R39C2ReconDep.md` §2).
- Action ("check the magic and superblock before rerunning; an empty envelope is not an empty
  filesystem") matches the knowledge paragraph it cites (`:50-54` → content at 50-53). ✓

### Row 2 — `dep-missing-be` (`SKILL.md:337`) — cause TRUE, action safe; one citation gap (D7)

- Cause true: BE v4 selects `sasquatch-v4be` (S112:41,48-50); the handler-level
  `get_dependencies()` lists both binaries (S112:68-69) but the **gap** names only the executable the
  chosen `Command` needed — `Command.get_dependencies()` returns `[self._executable]`
  (S120 `command.py:101-102`) and the report is built in the `FileNotFoundError` handler
  (`command.py:69-77`). Measured: every stripped-PATH BE run has `D={sasquatch-v4be}` exactly
  (`w1/R39C2ReconDep.md` §2/§3; round-38 `K1/before.json`).
- Action safe and complete: "rerun into a fresh output directory" matches REA's schema requirement
  ("Absolute, absent output directory; parent must exist", S119 `firmwareAnalysis.js:20-24`);
  "the image is unmeasured, not unreadable" is right — no command ran, so no argv/stderr exists
  (BE=`n/a` measured, ReconDep §3).
- `published files = *` is **required**, not loose: the AppImage before-arm publishes 2 files beside
  the same gap (round-36 `K3/before.json`, see row 3); the delivered dev table's `0` cell was
  correctly broadened (`w1/R39C2TableDraft.md:131-133`).
- **D7 (low, citation gap):** the row's gap-kind string `missing-extractor-dependency` is minted by
  REA, not by either cited source — S119 `FirmwarePublication.js:165-205` (three gap emitters) and
  `FirmwareReports.js:333-334` (`kind: dependencies === null ? "extractor-failure" :
  "missing-extractor-dependency"`). The source cell cites only S112/S120.

### Row 3 — `dep-missing-le` (`SKILL.md:338`) — cause TRUE including the AppImage claim; same citation gap (D7)

- The AppImage claim is verified against the receipt of the same shape: round-36
  `corpus/evidence/round-36/c1/K3/before.json` → `H=[elf64, squashfs_v4_le, elf64]`,
  `G=[missing-extractor-dependency]`, `D=[[sasquatch]]`, `P=2`, files =
  `firmware.bin_extract/0-944632.elf64_extract/carved.elf` (the ELF prefix) and
  `firmware.bin_extract/944632-11454968.squashfs_v4_le` (the opaque container range). Exactly what the
  row asserts, and exactly why the `*` cell is needed.
- "sasquatch-v4be alone does not satisfy this gap": true — the LE `Command`'s executable is the name
  `sasquatch` (S112:25,37; S120 `command.py:101-102`); a differently-named binary on the PATH does not
  resolve it, so the `FileNotFoundError` (and the gap) persist.

### Row 4 — `avm-marker-be-dropped` (`SKILL.md:339`) — cause TRUE; action's flag fix measured, wrapper delivery untested and unscoped (D5)

- Cause true: `is_avm = header.bytes_used == header.mkfs_time; if not is_avm:
  commands_args.append("-be")` (S112:48-50) — the drop is exactly the equality. S121 explains the
  failure: the `-be` option (unsquashfs.c:4389-4395) forces `swap = 1` on a little-endian host, while
  the `FIX_BE` auto-detect inversion (unsquashfs.c:2262-2282: "different endianess" branch →
  `swap = 0`) leaves the metadata-block headers unswapped; the measured stderr
  ("SquashFS version [1024.0] / inode count [150994944] suggests a SquashFS image of a different
  endianess" — message at unsquashfs.c:2267-2268, present in the installed binary's strings) and
  exit 1 match. Measured 6/6 AVM runs `BE=no, P=0` plus the direct matrix (no flag → exit 1, `-be` →
  exit 0): `w1/R39C2ReconMarker.md` §1-§4.
- "(REA has no flag passthrough)": true — `extract_firmware` input is a `strictObject` of
  input / output_directory / range / max_depth only (S119 `firmwareAnalysis.js:18-31`; unknown keys
  are rejected by construction); wave-1's `--help` check agrees (`w1/R39C2TableDraft.md:145-146`).
- **D5a (medium-low, untested mechanism):** the action's delivery vehicle — "a PATH wrapper named
  `sasquatch-v4be` that appends `-be`" — was never built or run. Wave-1's own record:
  `w1/R39C2TableDraft.md:143-146` "the *flag* is the fix; the *wrapper* mechanism … is [INFERENCE] —
  I did not build or test one", and `w1/r39-w1-results.json:154` ("the PATH-wrapper mechanism is
  [INFERENCE]"). A grep of `.ufo/waves/round-39/` finds no wrapper exercise in any wave-1 or wave-2
  artifact. The mechanism is plausible (S120 `command.py:52-58` runs `subprocess.run(cmd)` with
  argv[0] resolved on the child PATH; the dependency check is only the `FileNotFoundError` handler at
  `:69-77`, so an earlier PATH hit satisfies it) — but the table states it as the fix, not as an
  untested hypothesis.
- **D5b (medium-low, unsafe if followed literally):** the action gives no scope-or-remove
  instruction. A wrapper named `sasquatch-v4be` left on the child PATH re-adds `-be` exactly when
  unblob deliberately omits it (the `is_avm` branch, S112:48-50). Per S121:4389-4395 `-be` forces
  `swap = 1`, the reading the no-`-be` path exists to avoid for AVM-layout images — so every later
  **genuine AVM-BE** extraction through that PATH fails and is then mislabeled
  `body-extractor-failure` ("the image body or header is damaged", row 5). Row 2's action (install the
  real binary) is safe to leave installed; row 4's is not, and the row does not say so.
- Minor: row 4 omits "fresh output directory" (row 2 has it). REA refuses a pre-existing outdir
  (`firmwareAnalysis.js:20-24`), so a rerun needs one regardless — the omission cannot cause a wrong
  result, only an incomplete instruction.

### Row 5 — `body-extractor-failure` (`SKILL.md:340`) — action TRUE/safe; cells exclude a measured outcome (D1, the strongest finding); cause narrowed (D6)

- **D1 (medium): `published files = 0` contradicts wave-1's own measurement and explicit freeze
  requirement.** Measured counterexample (`w1/R39C2ReconDep.md` §2, `full-be1-xz`):
  `H={squashfs_v4_be}`, `G={extractor-failure}` (exactly one kind), `D=∅`, `BE=yes`, `SR=no`,
  **P=6** — an xz body failure publishes six files beside the failed chunk. ReconDep §5.3:
  "**`published files` for `body-extractor-failure` must allow `>0`.** … A `0`-only cell misses
  them." `w1/R39C2LabMixed.md` §4: "a `0`-only body cell … is wrong." `w1/R39C2ReconMarker.md` §5.2:
  the cell "MUST be `*` (not `>0`)". Three wave-1 seats converge on `*`; the committed row uses `0`.
  Demonstrated live (artifacts `demo-constructed.json-out.txt`): that exact feature vector →
  **`unclassified`** (rule None) under the committed table. The narrowing buys nothing — rows 6-8 are
  disjoint from row 5 on `symlink removed`/`gap kinds`/`-be`, so `*` would shadow nothing — and the
  shape is covered by neither the claim's "Not claimed" list (`plans/round-39-claims.md` R39-C2:
  AVM-BE bodies, LE body damage, unknown-chunk-handler/encrypted-chunk/depth-limited, mixed-symlink
  images, extracted programs) nor the knowledge entry's limits (`:55-58`). The 20/20 counter passes
  only because the held-out generator has no partial-publish body-failure class.
- **D6 (low): the cause dropped an alternative the dev table carried.** The interpreter's own dev
  table (`sqfs-triage.py:130` `TABLE_BLOCK`) says "the fault is in the image body **or the extractor
  build**"; the committed cause asserts damage only. An intact image whose compressor the sasquatch
  build lacks also fails under `-be`. The action's stderr-keeping mitigates; the cause still
  overclaims.
- Action TRUE and safe: `ExtractCommandFailedReport` carries `command`/`stdout`/`stderr`/`exit_code`
  (S120 `report.py:91-98`, built at `command.py:59-68` on non-zero exit) and REA copies it verbatim
  into diagnostics (S119 `FirmwareReports.js:255,287`) — "keep the failing command and stderr from
  diagnostics" is executable advice; "never patch the envelope into a success" is safe. (The draft's
  "do not retry, do not install anything, and drop or quarantine the carrier"
  (`w1/R39C2TableDraft` skill-craft-block.md) was softened to evidence-keeping — noted, not a defect.)
- Citations ✓: `S120 report.py:91-98` (class at 91-98) and `knowledge entry :29-40` (AVM paragraph
  29-39) both point where claimed.

### Row 6 — `escaping-symlink-removed` (`SKILL.md:341`) — action TRUE/safe; cause incomplete (D3)

- **D3 (low-medium): `MaliciousSymlinkRemoved` has a second cause the row omits.** S118 emits it from
  TWO branches: the unsafe-target removal (`extractor.py:81-86`, inside the cited `:79-91`) and the
  **recursive-link** removal (`extractor.py:58-63`, *outside* the cited range — `is_recursive_link` →
  report + unlink). A loop image produces the identical vector (`SR=yes`, no gap, `P>0`) and is
  labeled `escaping-symlink-removed` with a false cause ("a symlink target resolved outside the
  extraction root" — a loop never resolves at all). Demonstrated live (`demo-constructed.json-out.txt`):
  loop vector → rule 6. Wave-1 knew: `w1/R39C2Triage.md` §5.6 "a symlink loop is reported and removed
  (`extractor.py:57-65`), so it looks exactly like class 6"; `w1/R39C2ReconMarker.md` §5.7 (the TE
  tree's self-loop; "SR is `yes` only for `E-be-gzip` (relative `../outside.txt` + self-loop)").
  The action ("expect the path to be absent; never materialise the link") happens to be right for a
  loop too, so the harm is a wrong mechanism story, not a wrong instruction.
- Action TRUE: a removed link leaves no gap — REA publishes/records only entries present in the tree
  (S119 `FirmwarePublication.js:69-75`); measured round-38 `K1/after.json`: 0 gaps + exactly one
  `MaliciousSymlinkRemoved`.
- Related caveat (not a separate defect): an **empty-target** link is removed with *no* report
  (`extractor.py:68-71`) → `SR=no`, no gap → such an image labels `clean` (row 8) while a path is
  absent. Wave-1 knew ("invisible to the table", `w1/R39C2Triage.md` §5.6); neither the row nor the
  knowledge entry records it. The clean action's oracle match surfaces the absence downstream, so the
  loss is contained.

### Row 7 — `in-tree-symlink-metadata` (`SKILL.md:342`) — action TRUE; cause over-specific (D4)

- **D4a (low-medium): the gap is not symlink-specific.** REA records an `unpublished-entry` gap for
  **every** non-file entry (S119 `FirmwarePublication.js:69-75` `if (entry.kind !== "file")`), and the
  normalized kind enum is `["symlink", "special"]` (S119 `firmwareAnalysis.js:137-140`). A FIFO or
  device node (`kind: "special"`) yields the identical `G={unpublished-entry}` vector and is labeled
  `in-tree-symlink-metadata` under a cause that says "a symlink target resolved inside the extraction
  root". Demonstrated live: special-entry vector → rule 7. The action ("expected, not a failure; count
  one gap per in-tree link and publish nothing for it") survives — one gap per entry
  (`FirmwarePublication.js:301-308`) and nothing published for it — but the cause names the wrong
  entry kind for that case.
- **D4b (low): absolute targets are kept by re-rooting, not because they "resolve inside".**
  `fix_symlink` strips the leading `/` and re-roots under outdir (`extractor.py:74-75`), and
  `is_safe_path` joins outdir first (`file_utils.py:34-39`
  `basedir.joinpath(path).resolve().relative_to(basedir.resolve())`); measured: `-> /etc/passwd` is
  kept with rewritten `link_target "etc/passwd"` (`w1/R39C2Triage.md` §5.3/§5.5;
  `w1/R39C2ReconMarker.md` §6). The label and action hold; the cause's mechanism description is wrong
  for that half of the class.
- Citation ✓: `S119 FirmwarePublication.js:68-75,301-308` — the non-file push is at 69-75, the
  one-gap-per-entry map at 301-308.

### Row 8 — `clean` (`SKILL.md:343`) — action TRUE/safe; cells exclude a measured outcome (D2)

- **D2 (medium): `published files = >0` contradicts a measured clean shape.** Measured
  (`w1/R39C2ReconDep.md` §2/§5.4, `full-be-dirempty-gzip`): an image whose tree is one empty directory
  extracts with `chunks[].extraction_failed == false`, `G=∅`, `SR=no`, coverage `complete`, **P=0**.
  ReconDep §5.4: "**`published files` for `clean` must allow `0`.** … A `>0` cell makes it
  `unclassified`, and it is also the shape a *real* clean carrier takes when the tree yields no
  regular files. `*` is the safe cell; `no-squashfs-chunk` is still separable because it is keyed on
  `handler == none`." `w1/R39C2LabMixed.md` §4: "a `>0`-only clean cell is wrong." Demonstrated live:
  the dirempty vector → **`unclassified`**. The cause ("every regular file was published, no gap was
  recorded and no symlink was removed") is vacuously true at P=0 — which is exactly why the `>0` cell
  is unjustified.
- Action TRUE and safe: REA throws if any reported regular file is absent from the materialized output
  (S119 `FirmwarePublication.js:60-65`) and hashes every published file (`:76-90`), so
  suffix+sha256 oracle matching is the right check; the one silent-loss shape (empty-target link, see
  row 6 caveat) is caught by that same oracle match.

## 3. Rule-block citation check (`SKILL.md:322`, `:326`, `:329`) — all three PASS

Knowledge entry `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` paragraph map (verified by
line-numbered read): title 1; sources 3-7; verified-at 8; recheck 9; **Features 11-18** (the six
fields H/G/D/BE/SR/P); **Dependency misses 20-27** (the `sasquatch-v4be`/`sasquatch` naming and the
one-gap suppression); **AVM marker 29-39**; **Symlinks 41-48**; **No SquashFS chunk 50-53**; Status
and limits 55-58.

| rule-block citation | claims | points at | verdict |
|---|---|---|---|
| `:11-28` (`SKILL.md:322`) | six fields; a miss names `sasquatch-v4be`/`sasquatch` | Features 11-18 + Dependency misses 20-27 | ✓ both claims inside |
| `:29-40` (`SKILL.md:326`) | AVM-marked and damaged both `extractor-failure`/zero files; only `-be` separates; drop iff `bytes_used == mkfs_time` | AVM paragraph 29-39 | ✓ |
| `:41-54` (`SKILL.md:329`) | in-tree link = one gap; escaping = removed with report, no gap; missing chunk = silent empty envelope | Symlinks 41-48 + No-chunk 50-53 | ✓ |

Row-level citations: S112 "lines 44-50" ✓ (`is_avm` 48, append 50), "68-69" ✓; S118 "79-91" ✓ for the
escaping branch (but it excludes the loop branch 58-63 — consistent with D3's omission), "73-77" ✓
(absolute strip/re-root); S119 `FirmwarePublication.js:68-75` ✓, `:241` ✓ (`dependencyChunkKeys`, the
suppression the knowledge entry cites), `:301-308` ✓, `FirmwareReports.js:254-255` ✓, `:284` ✓
(`extractionFailed` derivation); S120 `report.py:91-98` ✓, `118-122` ✓, `133-138` ✓,
`command.py:59-77` ✓, `:101-102` ✓; S121 `debian/rules` "15-18" ✓ (`CFLAGS=-DFIX_BE dh_auto_build`
at 17, `cp … sasquatch-v4be` at 18). Only defect: D7 (rows 2/3 omit S119 for the gap-kind string).

## 4. Defect list (severity-ordered)

| # | sev | where | defect |
|---|---|---|---|
| D1 | medium | `SKILL.md:340` (row 5, `published files = 0`) | Excludes the measured `full-be1-xz` vector (`G` exactly `{extractor-failure}`, `BE=yes`, `P=6`, `w1/R39C2ReconDep.md` §2) → `unclassified`; ReconDep §5.3 / LabMixed §4 / ReconMarker §5.2 all required `*` before the freeze; narrowing buys no separation; shape absent from the claim's "Not claimed" list and the knowledge entry's limits. Demonstrated live. |
| D2 | medium | `SKILL.md:343` (row 8, `published files = >0`) | Excludes the measured `full-be-dirempty-gzip` vector (clean extraction, `P=0`) → `unclassified`; ReconDep §5.4 required `*`. Demonstrated live. |
| D5a | medium-low | `SKILL.md:339` (row 4 action) | Prescribes the PATH-wrapper mechanism wave-1 recorded as untested `[INFERENCE]` (`w1/R39C2TableDraft.md:143-146`, `w1/r39-w1-results.json:154`); no artifact exercises a wrapper through REA. |
| D5b | medium-low | `SKILL.md:339` (row 4 action) | No scope/remove caveat: a persistent `sasquatch-v4be` wrapper re-adds `-be` exactly when unblob omits it (S112:48-50), so later genuine AVM-BE extractions fail (S121:4389-4395 forces `swap=1`) and get mislabeled `body-extractor-failure`. |
| D3 | low-medium | `SKILL.md:341` (row 6 cause) | Omits the symlink-loop branch of `MaliciousSymlinkRemoved` (S118 `extractor.py:58-63`, outside the cited 79-91); a loop image gets the label under a false cause. Demonstrated live. |
| D4a | low-medium | `SKILL.md:342` (row 7 cause) | `unpublished-entry` is emitted for every non-file entry (`kind` enum `["symlink","special"]`, S119 `firmwareAnalysis.js:137-140`); a FIFO/device gets the symlink-only cause. Demonstrated live. |
| D4b | low | `SKILL.md:342` (row 7 cause) | Absolute targets are kept by `lstrip`+re-root (S118:74-75, `file_utils.py:34-39`), not because they "resolve inside"; measured `-> /etc/passwd` kept. |
| D6 | low | `SKILL.md:340` (row 5 cause) | Drops the dev table's "or the extractor build" alternative (`sqfs-triage.py:130` TABLE_BLOCK); an unsupported compressor also fails under `-be`. |
| D7 | low | `SKILL.md:337-338` (rows 2/3 source cell) | The gap-kind string `missing-extractor-dependency` is minted by REA (S119 `FirmwarePublication.js:165-205`, `FirmwareReports.js:333-334`); the cited S112/S120 do not contain it. |
| D8 | observation | `tools/round-39/sqfs-triage.py:130` | The interpreter's embedded `TABLE_BLOCK` is the round-38 dev table (dep rows `0`, rows 6-8 handler `squashfs_v4_be`, different causes/sources), not the committed SKILL.md table; `--print-table` prints the stale block. Runtime reads SKILL.md (verified: marker line 333, table line 334, rules: 8), so scoring is unaffected — operator-facing staleness only. |

## 5. Demonstrations (frozen interpreter, read-only; artifacts `demo-*.txt`)

`python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json …` on four minimal envelopes
constructed in scratch from wave-1-measured vectors:

| envelope | vector (H/G/D/BE/SR/P) | committed-table label |
|---|---|---|
| `xz-shape.json` (= measured `full-be1-xz`) | `squashfs_v4_be` / `{extractor-failure}` / ∅ / yes / no / 6 | **unclassified** (D1) |
| `dirempty-shape.json` (= measured `full-be-dirempty-gzip`) | `squashfs_v4_be` / ∅ / ∅ / n/a / no / 0 | **unclassified** (D2) |
| `loop-shape.json` (loop removal, S118:58-63) | `squashfs_v4_be` / ∅ / ∅ / n/a / yes / 1 | `escaping-symlink-removed` rule 6, false cause (D3) |
| `special-shape.json` (`kind: "special"`) | `squashfs_v4_be` / `{unpublished-entry}` / ∅ / n/a / no / 1 | `in-tree-symlink-metadata` rule 7, false cause (D4a) |

Corpus spot-check (six held-out envelopes, labels read from the frozen table): H01→`clean` (8),
H05→`escaping-symlink-removed` (6), H13→`avm-marker-be-dropped` (4), H15→`body-extractor-failure`
(5), H17→`no-squashfs-chunk` (1), H19→`body-extractor-failure` (5) — all equal to the manifest's
frozen labels. The P39-C2 predicate (20/20 on the held-out set) is consistent with its scoring; the
defects above are craft-quality gaps in the table the claim installed, not counter failures.

## 6. Residual risks and non-defects

- **Timeout corner:** `ExtractorTimedOut` records `cmd`, not `command` (S120 `report.py:125-131`), so
  the interpreter's BE scan misses it → a timed-out failure with `SR=yes`, `P>0` would match row 6
  (`-be = n/a`). Exotic (12 h timeout, `command.py:20`); unmeasured.
- **Compound envelopes:** a dep-miss cannot co-occur with `SR=yes` for the same chunk (nothing was
  extracted, so no link was materialised — measured, ReconDep §3 masking), but a *second* chunk's
  removal plus a squashfs dep-miss would fall past rows 2/3 (`SR=no`) to row 6 and hide the
  dependency from the label. Unreachable for the single-squashfs carrier family; noted for
  future multi-chunk inputs.
- **Row 4's cause asserts "standard-BE body":** a damaged *genuine* AVM image would land here and the
  wrapper advice would be wrong for it; out of corpus (knowledge limits: "AVM-BE bodies" not covered).
- **Broadcom handler** (`squashfs_v4_broadcom`, S112:548-569) matches rows 6-8's `squashfs_v4_*` but
  not rows 2-5; a broadcom dep-miss → `unclassified`. Out of corpus.
- Row 5's softened action (the draft's "do not retry" became "never patch the envelope into a
  success") is a deliberate, safe weakening — not a defect.
- Row 1's position (first) is harmless: `H=∅` fails every other row's handler check, so it cannot
  shadow; row 4 before row 5 (`-be` no before yes) and row 6 (SR=yes) before rows 7/8 (SR=no) match
  the load-bearing order wave-1 pinned (`w1/R39C2ReconDep.md` §5, `w1/R39C2LabMixed.md` §4.4).

## 7. Tooling record

No tool was installed, upgraded, moved or removed (operator authorization 2026-10-19 read; nothing
needed). `curl` (pre-installed) fetched the pinned upstream sources into scratch solely for the
byte-identity checks of §1; the fetched copies of `unsquashfs.c`, `debian/rules` and
`rea-agents-6.5.0.tgz` are preserved in the artifacts dir. No pacman transaction; no VCS mutation
(read-only `git show` on the freeze commit only); scratch
`/fast/scratch/hyaku/kaidoku-r39/R39W2C2TableReview` removed after copying the cited artifacts.
