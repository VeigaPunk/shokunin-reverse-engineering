# EX-15 — chain c2, executor — adjudication drafts (arc3-loop1-round4)

Seat line: `SEAT EX-15 | CHAIN c2 | ROLE executor | TASK: adjudication drafts:
every ADJUDICATE item gets a NO-CHANGE-with-cause text (or a repair) with
evidence. Artifact claims/c2/EX-15/adjudications.md.`

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (read-only `git rev-parse`; no git
mutation by this seat). Date 2026-10-19. Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback dispatch
(`claims-frozen.md:11-15`), not a lane signal. Baseline identity of the target:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. Scratch `/var/tmp/ex15/` (never `/tmp`, EDQUOT standing). Custody
paths never opened. No PROVINCE/SKILL/SCORECARD/corpus/README/LOG write — patch
texts only.

## 0. What this artifact is (and its unit boundary)

The chain claim requires that *every PROVINCE Frontier bullet and
surface-summary claim* be **census-checked** against the admitted corpus state,
and that every stale item be **repaired same-line** or **adjudicated
NO-CHANGE with cause**. This seat owns the adjudication half: a disposition per
item, each with its own re-derived evidence, and — where a repair is warranted —
a ready patch text in the wave's prose-patch format.

**Measured unit boundary (this seat's finding, load-bearing for the claim's
"census-checked" wording).** `.ufo/gates/c1-census-v10.py` cannot see any of the
items below. Its `SCOPE` table covers `PROVINCE.md` only at lines 8-13, 15-26,
40-43, 44, 45-62, 64-71, 119-131; the whole `## Frontier` section (73-93) and
the round-4 frontier block (133-162) are **outside every declared row**. The
instrument only raises `UNDECLARED` when a block carries a locus in its unit
(`rea-agents@x.y.z`, bare `6.x.y`, `~`/`/`-absolute `path:line`), and a
re-derivation confirms zero such loci in 73-93
(`sed -n '73,93p' PROVINCE.md | grep -nE 'rea-agents@|6\.[0-9]+\.[0-9]+|~/[^ ]*:[0-9]+|/home/[^ ]*:[0-9]+'` → no output). Census at HEAD reads
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 — **and
it would read PASS identically if every bullet below were deleted**. The
"census-checked" half of the claim is therefore *reviewer-adjudicated, not
instrument-enforced*, and this artifact is that reviewer record. This is a
statement about the instrument's declared unit, not a defect claim against it:
the r9 provenance block already names the boundary
(`.ufo/gates/c1-census-v10.py` — "SCOPE … an explicit declared table of
file:line ranges").

**Repair-shape constraint, measured by peer seats (adopted, not re-derived).**
EX-16's battery (`claims/c2/EX-16/interplay.md` §3-4) establishes: a same-line
rewrite of a Frontier bullet is safe under **both** instruments (probe
`clean 0/0`, census PASS, 162→162 lines); *growth* is not — `+1` line anywhere
above :119 fails the census (DATED marker at :119 moves), `+3` fails the probe
(`shonen-province-range` end 116). Every repair draft below is therefore
**line-count-neutral and line-number-neutral**: each rewrites exactly the bytes
of an existing line and never adds or removes one. That is also the frozen
claim's own required shape ("repaired same-line (line count held)").

**Repair drafts are validated, not asserted.** §4 records the scratch-tree run:
the eight-hunk landing set (A1-repair, A2, A3, A4, A5, A6b, B1, B2) applied to a
fresh `git archive` of HEAD, then graded by the census and by the citation-drift
probe in both modes; §4.5 does the same for the A6a variant. The A1-nocause text
is prose for the round record, not a hunk, and is not applied.

---

## 1. Dispositions

Verdicts: **REPAIR** (patch text drafted below) or **NO-CHANGE** (with cause).
Cross-reference: VZ-2's independent staleness census
(`claims/c2/VZ-2/evidence/province-staleness-census.py`) found 4 stale rows
(F1b, F5b, X1, R2) + 1 adjudicated (S5). This seat **concurs on all five** and
adds four further items that VZ-2's row set does not carry (A1 the `:3298`
pointer — VZ-2 carries it as its `S5` adjudicated row and this seat upgrades it
to a drafted repair; A2 the Ghidra feature count; A3 the absent-tool list; A4 the
crash-cap premise; C1 the pacman-pair clause). VZ-2's `F2` and this seat's A4
are the same bullet adjudicated differently, with the disagreement recorded in
A4 rather than smoothed.

### A1 — PROVINCE.md:18, the `config.toml:3298` pointer — **REPAIR** (or NO-CHANGE, see cause)

- **Item.** "`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3298` at the
  17:55:49Z receipt; value unchanged through 2026-10-18's rewrites — earlier
  pointers :2940 [16:57:35Z receipt] and :3227 [17:32Z rewrite] are historical)".
- **Re-derived.** `wc -l ~/.kimi-code/config.toml` → **3570** lines (the r3
  receipt's snapshot was shorter). `grep -n 'rea-agents@' ~/.kimi-code/config.toml`
  → exactly one occurrence, at **:3546** (`args = [ "-y", "rea-agents@6.7.0", "mcp" ]`).
  `sed -n '3298p'` → `max_context_size = 1048576` — an unrelated Copilot model
  block. The cited line holds no pin.
- **The value claim survives.** Live pins re-read: devin `rea-agents@6.5.0`
  (`~/.config/devin/mcp_config.json:7`), omp `rea-agents@6.5.0`
  (`~/.omp/agent/mcp.json:8`), kimi `rea-agents@6.7.0` (`:3546`). The named
  receipt exists and is tracked: `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`
  line 1 is `2026-10-18T17:55:49Z` (verified by `git ls-files --error-unmatch`,
  rc 0). So `prov18-stamp-named` and `prov18-receipt-exists` in the citation
  table both hold — **the citation is receipt-stamped, and the receipt is the
  in-repo terminus of the chain** (`pointer-table.json` entry
  `prov18-receipt-exists` says exactly this). What is dead is the *live-line*
  reading of `:3298`.
- **Why the census misses it.** `classify()` collects pointer loci only
  `if not occ` — i.e. only when a block carries no `@`-pin and no bare version.
  Line 18 carries a pin (`rea-agents@6.7.0`), so the `PTR` branch never runs.
  Direct call, for the record:
  `ptr_check('~/.kimi-code/config.toml', 3298, {'kimi':'6.7.0'})` →
  `('stale', "line holds no rea-agents pin: 'max_context_size = 1048576'")`;
  `ptr_check(..., 3546, ...)` → `('ok', 'pins 6.7.0')`. The staleness is real
  and *detectable by the instrument's own checker* — it is simply not reached.
- **Disposition.** **REPAIR** — the line is outside every census row's
  marker-bearing text? No: :18 sits inside the CURRENT row 15-26 and carries no
  marker itself, so a same-line rewrite is census-neutral (EX-16 measured a
  same-line rewrite of a *surface-summary* line: `clean 0/0`, PASS). **A
  NO-CHANGE adjudication is also defensible** and is the honest alternative: the
  sentence already declares itself a receipt-time pointer ("at the 17:55:49Z
  receipt") and already carries a supersession chain (:2940 → :3227 → :3298),
  so a fourth re-anchor preserves the same perishable form and will die the same
  way. Both texts are drafted in §2 (A1-repair and A1-nocause); the parent
  picks one. This seat's recommendation: **A1-repair**, because the bullet's own
  style re-anchors rather than accumulates, and because a dead pointer is the
  one class here that a reader can trip over silently.
- **Note on rule #11.** The replacement text below contains `config.toml:3546`
  — a `path:line` token. Inside the *census* unit that is harmless (`PTR`
  requires a `~`/`/`-absolute path and a `.json|toml|yaml` suffix — this text
  uses a bare basename, so it is not a locus; verified by the post-apply census
  in §4). But PROVINCE's own convention writes the full `~/.kimi-code/...`
  form; the draft keeps the full path to match house style, and §4 measures the
  consequence rather than assuming it.

### A2 — PROVINCE.md:46, "35 features incl. PyGhidra/BSim" — **REPAIR**

- **Item.** Ghidra provider row: "…39 processor modules; **35 features** incl.
  PyGhidra/BSim…".
- **Re-derived.** `find …/Ghidra/Features -maxdepth 1 -mindepth 1` → **34**
  entries, all directories (34 dirs, 0 files). `ls -1` verbatim gives: Base,
  BSim, BSimFeatureVisualizer, BytePatterns, ByteViewer, CodeCompare, DataGraph,
  DebugUtils, Decompiler, DecompilerDependent, FileFormats, FunctionGraph,
  FunctionGraphDecompilerExtension, FunctionID, GhidraGo, GhidraServer,
  GnuDemangler, GraphFunctionCalls, GraphServices, MicrosoftCodeAnalyzer,
  MicrosoftDemangler, MicrosoftDmang, PDB, ProgramDiff, ProgramGraph, PyGhidra,
  Recognizers, Sarif, SourceCodeLookup, SwiftDemangler, SystemEmulation,
  VersionTracking, VersionTrackingBSim, WildcardAssembler.
- **The corpus is self-inconsistent, which is why this was easy to miss.** The
  r1 entry's *claim line* says "35 modules" but its own *enumerated list* has
  **34** entries; a mechanical comparison of that list against the live
  directory returns zero differences in both directions
  (`in list not on disk: []`, `on disk not in list: []`). The "35" is a miscount
  of the entry's own list, propagated into PROVINCE. The row is therefore stale
  against the very evidence it cites.
- **Disposition.** **REPAIR** — one word, `35` → `34`, same line, byte-length
  differs by zero. Line 46 is inside the DATED row 45-62 (marker at :45, the
  literal `2026-10-13`); the marker is on line 45 and is untouched, so the
  DATED row keeps its marker and the census keeps its PASS (§4 measures it).
- **Adjacent, adjudicated NO-CHANGE:** the same row's "39 processor modules" is
  correct (`find …/Processors -maxdepth 1 -mindepth 1` → 39) and "876 MB
  install" is correct within rounding (`du -sb` → 863.9 MiB = 906 MB SI; the
  corpus entry and the row agree on "876M" as a `du -sh` reading). Neither is
  touched.

### A3 — PROVINCE.md:62, the absent-tool list — **REPAIR**

- **Item.** Host fallback readers row: "absent: `7z`, `cabextract`, `xxd`,
  radare2/rizin, strace/ltrace, upx, pacman-contrib".
- **Re-derived** (`command -v`, per tool): **present now** — `7z` `/usr/bin/7z`,
  `xxd` `/usr/bin/xxd`, `radare2` `/usr/bin/radare2` (and `r2`),
  `strace` `/usr/bin/strace`, `upx` `/usr/bin/upx`. **Still absent** —
  `cabextract`, `rizin`, `ltrace`, and the pacman-contrib verbs (`paccheck`,
  `pactree`, `pacfiles`).
- **Cause of the drift, dated.** `pacman -Qo` and `pacman -Qi` put every one of
  the newly-present tools at **Install Date: Tue 13 Oct 2026 01:52:22 PM -03**
  (7zip 26.03-1, radare2 6.2.0-1, strace 7.0-1, upx 5.2.0-1, tinyxxd 1.3.16-1
  owning `/usr/bin/xxd`). The row landed in `a43d442` (2026-10-13 12:16:39
  -0300) — roughly 12 hours *earlier*, when the sweep was true. This is a
  same-day host change, not a citation error; the row simply has no refresh
  mechanism.
- **Corroborated by the corpus, in the direction of the repair.** Two entries
  already rely on the present tools and say so: `2026-10-13-r4u-03-unblob-extract.md`
  ("`7z` is installed and reads unblob's carved squashfs directly — a working
  carve-then-7z pipeline"; `7z 26.03`), and `2026-10-13-r3-appimage.md` ("`7z`
  reads the carved image"). `2026-10-13-r3-evm-interface.md:122` still carries
  the older "`xxd` absent on this host" — that is a *corpus* line, outside this
  seat's scope, named here as a cross-artifact residual for the parent.
- **Disposition.** **REPAIR** — drop the five now-present names, keep the four
  that are still absent. Line 62 is the last line of the DATED row 45-62;
  the repair is same-line and the row's marker (:45) is untouched.

### A4 — PROVINCE.md:82-83, "Reserve: 91MB Godot ARM64 template" — **REPAIR**

- **Item.** PE-subtypes bullet: "…Reserve: 91MB Godot ARM64 template, ARM64X
  hybrids."
- **Re-derived.** The exact artifact is on disk and **byte-identical to the one
  arc2-r7 held**: `sha256sum …/godot/export_templates/4.7.2.stable/windows_release_arm64.exe`
  → `7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292`, which is
  the sha256 printed in `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` (line 11)
  as the target of the successful 75,218-procedure hold. The corpus already
  treats this as closed: `corpus/README.md`'s Frontier section reads ">90MB PE
  scale — **CLOSED, not frontier**". PROVINCE still lists the same target as a
  *reserve*, i.e. as not-yet-claimed.
- **Disposition.** **REPAIR** — the honest residual is ARM64X hybrids alone;
  the 91MB template moved to held. (VZ-2 independently found this row stale,
  `F1b`.) Note the two bullets A4 and B1 below are the *same* closure seen from
  two sections; both need the edit, or the document contradicts itself.

### A5 — PROVINCE.md:84-86, "Recorded crashes >32 MiB" — **REPAIR**

- **Item.** "…mechanism held (Core); **all 3 organic cores exceed the cap**
  (waybar 434MB). Needs a cap-raising knob or partial-core intake — neither
  exists. Retention decays oldest-first."
- **Re-derived — the premise is false as written.** `coredumpctl list` now
  reports **1537** entries and the host holds **1465** `godot` cores plus
  `Hyprland`, `git`, `chrome_crashpad`, and an `UnrealEditor-Cmd` record.
  Dumping and measuring four of them (`coredumpctl dump <pid> -o …`, then
  `ls -l`):
  - PID 1857 `chrome_crashpad_handler` → **17,608,704 B** decompressed.
  - PID 1214442 `git` → 36,360,192 B.
  - PID 1700 `Hyprland` → 172,793,856 B.
  - PID 590432 `godot` → 349,663,232 B.
  The 17.6 MB core is **under the 33,554,432-byte cap**, and it is an *organic*
  core in the sense the bullet means (a real application crash of a real
  program — the Grok Bot / Electron 42.1.0 crashpad handler, `SIGBUS`,
  `BUS_ADRERR`), not a deliberate self-kill. The count "3 organic cores" is a
  round-1 census of a 175-entry list; the list is now 1537 entries.
- **And the tool runs on it — end-to-end, first-hand.** `TMPDIR=/var/tmp/ex15/tmp
  npx -y rea-agents@6.4.0 inspect-recorded-crash /var/tmp/ex15/cores/c-1857 --format json`
  → **exit 0**, `evidence_id ev_2cef7d1131ed4a4b07840e889d56bca54a149a8411e107dac9dd8d3d43adb386`,
  `subject.digest.sha256 0d444cf0f3a130a9270223d00348179b906797134a33b14f05d9372012be0c53`,
  provider `pwntools-elf`, `normalized_result.format: "elf-core"`,
  `architecture: "x86_64-little-endian"`, **3 threads × 27 registers**,
  **53 segments**, 7 `limitations[]`. The same command on the over-cap 172.8 MB
  core returns the declared refusal (exit 1, `invalid_request` /
  `out_of_range`, "Selected artifact exceeds 33554432 bytes") — so the cap is
  still real and the *sub-cap* class is now reachable.
- **Independent corroboration.** Peer seat EX-17 probed the same core and
  landed `claims/c2/EX-17/evidence/crashpad-probe.json` with the same subject
  digest `0d444cf0…` and the same 3 threads / 53 segments; EX-11 probed the
  oversize `git` core and landed the same `out_of_range` refusal
  (`claims/c2/EX-11/evidence/oversize-refusal-33554432.json`). Three seats,
  same bytes, same classes.
- **Disposition.** **REPAIR** — but the *correct* repair is not "delete the
  bullet". What is false is the universal ("all organic cores exceed the cap")
  and the count; what remains true is the *coverage* statement that matters for
  a frontier: organic cores **in the multi-hundred-MB class** still exceed the
  cap and the knob still does not exist. The draft narrows the quantifier and
  keeps the frontier. (VZ-2 marked this row `current` by matching the
  "no flag to raise the cap" substring; that substring is indeed still true —
  the row is stale in its *premise*, which is why a substring census and a
  semantic one can disagree. Recorded, not smoothed.)

### A6 — PROVINCE.md:91-93, the EVM bullet — **REPAIR**

- **Item.** "…selectors held on synthetic dispatcher (Core, r3-07); **real
  solc/vyper-compiled bytecode untested**; selectors stay bare hashes…".
- **Re-derived.** The `solc` half is **doubly** stale: `arc3-r1` landed a
  real-solc-0.8.37 entry (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`:
  K/K on 5/5, 6/6, 11/11, per-function mutability and argument tuples), and
  `arc3-r3` extended it to optimizer-on/off shapes
  (`2026-10-19-arc3-r3-evm-optimizer-shapes.md`: 13/13, 11/11, 8/8, 5/5 across
  two pins). The r3 wave named this exact staleness in its own seat records
  (`arc3-loop1-round3/seats/SC-2.md` §"Named, not proposed as patch text":
  "the stale `PROVINCE.md:91-93` EVM frontier bullet — doubly stale after r1 and
  r3"), and the arc3-r3 round report carries it as named debt.
- **The `vyper` half is stale *as of this round*.** The round's authorized
  vyper install landed (`claims/c1/EX-02/install-receipt.txt`; venv at
  `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`, `vyper 0.4.3`), and the
  Vyper carrier was probed: `claims/c1/EX-05/planted-vs-probe.txt` shows
  **15/15 planted selectors recovered, zero missing, zero extra** on hex
  @6.4.0, hex @6.7.0 and raw @6.4.0, `dispatch:"abi"`, decoded
  `bytecode.sha256 57d6fd0a…`. So on the round's own work commit the sentence
  "vyper-compiled bytecode untested" becomes false.
- **Timing caveat, stated.** EX-05's probe legs are the *evidence*; whether the
  c1 chain's corpus entry and the `vyper` clause land in the same commit as
  C2's patches is a **parent-side sequencing decision**, not something this
  seat can settle. The draft therefore offers **two** texts (§2, A6a/A6b):
  A6b names only the solc leg (true at HEAD and independent of c1's landing);
  A6a names both legs (true only once c1's entry lands). This is the one place
  in this artifact where a repair's truth depends on another chain, and it is
  flagged rather than assumed.
- **Disposition.** **REPAIR** (A6b unconditionally; A6a if c1 lands first).
  VZ-2's `F5b` is the same row.
- **Adjudicated NO-CHANGE within the same bullet:** "selectors stay bare hashes
  (no signature DB → no name resolution)" remains true — no corpus entry claims
  a signature DB or name resolution (`grep` over `corpus/knowledge/*.md` finds
  none), and every probe envelope's `limitations[]` carries the
  upstream-inference caveat. Untouched.

### B1 — PROVINCE.md:139-144, ">90 MB PE scale wall" — **REPAIR**

- **Item.** "…**Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to ~3.6Ms +
  `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a 2-5MB PE."
- **Re-derived.** The wall is closed, and the corpus says so twice over:
  `arc2-r7` held the exact 91.6 MB target (`ev_a4aa9b0d…`, 75,218 procedures,
  1424.663 s, 7.9G peak under a 9G cap, zero OOM) with three registry-validated
  analyzers disabled; the append-only erratum in the same entry records
  `arc2-r8`'s natural control — no analyzers disabled, identical caps — being
  **kernel-OOM-killed at 9G in 4m42.945s**. `corpus/README.md`'s Frontier reads
  ">90MB PE scale — CLOSED, not frontier". The "Next:" remediation is
  pre-r7 text and now points at a mechanism the round already superseded.
- **Disposition.** **REPAIR** — replace the open "Next:" remediation with the
  closure and the one genuine residual (rerun id-stability remains UNKNOWN;
  natural unmitigated hold does not exist at this cap). VZ-2's `R2` is the same
  row.

### B2 — PROVINCE.md:157-160, "compare-application-versions still probe-refused since r2" — **REPAIR**

- **Item.** Cross-version residuals: "`compare-application-versions` still
  probe-refused since r2; multi-version pacman pairs beyond expac unexercised".
- **Re-derived (first clause).** The r2 refusal was one *input class*
  (native records), not the verb: `2026-10-13-r2-version-diff-compare.md` records
  `invalid_request`/`invalid_input` for a native-record input, and the r4-16
  census cell (line 203) already reads "two JS-graph/managed evidences — now
  self-provisionable; only the refusal datum is held". The success path landed
  in r12-02 on **both** classes: `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md`
  records `ev_7a8d0ec4…`/`javc_efb02d28…` (obsidian 1.12.7→1.13.7 JS graphs:
  218 items, `{changed:10, unknown:208}`, byte-identical re-run) and
  `ev_b5fc998f…` (Pinta managed graphs: all-unknown non-verdict, 4,114 items),
  with the negative ladder (`{}` → `missing_argument`; same-evidence-id →
  superRefine "must be distinct"). The r4-16 rescan carries the discharge as an
  append-only erratum.
- **Disposition.** **REPAIR** — the verb's refusal-era wording is superseded;
  keep the genuinely open half. VZ-2's `X1` is the same row.

### C1 — PROVINCE.md:157-160, "multi-version pacman pairs beyond expac unexercised" — **REPAIR** (this seat's addition; VZ-2 marked it current)

- **Item.** Same bullet, second clause.
- **Re-derived.** `2026-10-13-r4-10-real-version-pair.md` is titled "Real
  cross-version binary compare: 1password-cli `op` 2.34.1 → 2.40.0" and its
  target section is headed "**Targets — cached pacman pairs (`uniq -d` walk:
  354 duplicated pkgbases)**", listing two pairs (`1password-cli` 2.34.1-1 →
  2.40.0-2, member `usr/bin/op`, 41,210,040 → 43,475,106 B; and `qpdf`
  12.3.2-2 → 12.4.1-1 as a control). Both members were extracted from the
  pacman cache with `tar -xOf <pkg> usr/bin/<name>`, and the entry states the
  hashes reproduce round 2's `op` values. The cache still holds the 2.40.0
  member (`/var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst`);
  the 2.34.1 member has since been evicted by cache churn (recorded as an
  honest limit — the *entry* is the evidence, and it is corpus-admitted).
- **Why VZ-2 marked it current:** its row `X2` tests the substring
  "multi-version pacman pairs beyond expac unexercised" against
  `corpus_has("expac")`, which trivially matches the r2 entry that *defines* the
  expac baseline. The test confirms the bullet's *text* exists; it does not test
  the *claim*. Recorded as a unit-boundary observation about substring censuses,
  not as a fault in VZ-2's instrument (which declares its own method).
- **Disposition.** **REPAIR** — fold both clauses into the superseded
  statement. Same line count.

### D1 — PROVINCE.md:87-88, "Alternate providers — IDA …, Hopper (absent), JEB (unprobed)" — **NO-CHANGE with cause**

- **Cause, re-derived now.** `REA_IDA_MCP_CONFIG` unset in env and absent from
  `~/.bashrc`; `HOPPER_LAUNCHER_PATH` likewise unset/absent; `REA_JEB_MCP_URL`
  unset (`env | grep -c '^REA_JEB_MCP_URL='` → 0). A live probe at the round's
  newest pin returns the declared typed class:
  `npx -y rea-agents@6.7.0 inspect-jeb-client` → `capability_unavailable`
  (`claims/c2/EX-17/evidence/jeb-probe-6.7.0.json`). The corpus agrees at the
  same level of detail (`2026-10-13-r2-frontier-prereqs.md`: "Fully absent.
  `REA_JEB_MCP_URL` unset; no JEB install …").
- **One word is arguable and adjudicated, not repaired.** "JEB (unprobed)" is
  loose: the verb *has* been probed (r2's `inspect-jeb-client` refusal is
  recorded, and EX-17 re-probed it this round) — what is unprobed is a *JEB
  installation*. The parenthetical is a shorthand for "no JEB surface is held",
  which is true, and the r4-16 census carries the same wording. Repairing one
  word of a true-in-substance clause costs a patch and buys nothing a reader
  needs. **NO-CHANGE.**
- Adjacent, adjudicated NO-CHANGE: the "Operator-gated, still absent" bullet
  (:161-162) is the same content and is likewise correct.

### D2 — PROVINCE.md:89-90, "macOS-only surfaces … report `unsupported_host` on Linux" — **NO-CHANGE with cause**

- **Cause.** The refusal class is corpus-held and specific:
  `2026-10-13-r3-keyed-archive-carriers.md` records `inspect-plist` →
  `unsupported_host` ("Native macOS utilities require macOS") while the three
  carrier-based macOS *formats* (`inspect-keyed-archive`,
  `decode-interface-builder`, `trace-dylib-resolution`) work on Linux. The
  bullet says exactly the narrow thing — the *ops* report `unsupported_host`,
  and the lane "never claims them" — and the corpus's summary table agrees
  (`| inspect_plist | false (unsupported_host) |`). No drift found.
  **NO-CHANGE.**

### D3 — PROVINCE.md:50, "pacman `.pkg.tar.zst` corpus 1556 signed archives" — **NO-CHANGE with cause**

- **Cause.** The live cache holds **1350** archives and 1350 `.sig` files
  (`ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l`), down from the corpus's
  measured 1556 — pacman cache eviction, i.e. the number is a *retention-varying
  inventory*, not a capability claim. The row's load-bearing content is the
  pipeline (`inspect_artifact`/`extract_artifact`, `.MTREE` per-file sha256,
  `pacman -Qkk`) and its verified instance: `sha256sum /usr/bin/jq` →
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, and
  `tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum`
  → the **same** digest; `pacman -Qkk jq` → "25 total files, 0 altered files".
  Re-derived this run, both halves hold.
- **Why NO-CHANGE rather than a repair:** the row is a Core surface row, not a
  Frontier bullet, and the count is inside a CURRENT census row (40-43) that is
  clean. Editing a correct-as-of-its-receipt inventory count inside a CURRENT
  row would (a) be an unforced change to a PASSing row and (b) re-introduce the
  same perishability at a new number. If the parent wants the count refreshed,
  the correct move is a dated re-receipt of the row, which is a calibration
  action, not this round's repair. **NO-CHANGE** — recorded so the discrepancy is
  on the record rather than silently absorbed.

### D4 — PROVINCE.md:8-13 and :15-26, surface summary + drift-prone block — **NO-CHANGE with cause** (except A1)

- **Cause, re-derived per value.** The three pins, the three cache identities
  and the doctor states all hold at HEAD: live pins devin/omp `6.5.0`,
  kimi `6.7.0` (as above); cache `~/.npm/_npx/a1722018f28f9df2` → 6.7.0,
  `ad9a3fdbcad992c6` → 6.5.0, `dea9475797100b20` → 6.4.0 (`package.json`
  versions); and a live doctor sweep this run returns, for 6.7.0 and 6.5.0,
  `counts {cli_commands:153, mcp_tools:207, mcp_prompts:6}` with
  `tools_sha256 af39310c…` / `805433f1…`, and for 6.4.0
  `{127,170,6}` with `25802f6d…` — matching every digest the document states.
  The "Devin/OMP 6.5.0 doctor reported aligned at luna-round-2 (historical);
  the 2026-10-18 6.7.0 doctor reports those registrations stale" sentence is
  also still true: a 6.7.0 doctor run this round reports
  `identity.registrations[*].state == "stale"` on five entries and
  `identity.skill.state == "stale"`.
- **Exception:** A1 above (`:18`'s line pointer) is the only defect in these
  two blocks. **NO-CHANGE** for the rest.

### D5 — PROVINCE.md:75-80 and :161-162 — **NO-CHANGE with cause**

- **Cause.** The Frontier preamble's `[r5-audit C1: …]` annotation is a
  historical audit marker describing a past pruning; the six named bullets are
  indeed in "Round-4 additions to Core" below it (spot-checked: firmware,
  JavaScript source recovery, Android deep analysis, managed IL, `.jsc`,
  runtime observation verbs, binary layout, ADB, AppImage — 9 rows present).
  The "Operator-gated, still absent" bullet (:161-162) duplicates D1's content
  and is likewise correct. **NO-CHANGE.**

---

## 2. Patch texts (prose-patch format; parent applies, seats never write PROVINCE)

Format matches `claims/c2/RV-4/prose-apply.py` (fenced block, `-` search lines,
`+` replacement lines, target named by a backticked path on the introducing
line). Every hunk is **same-line**: the `-` and `+` groups have equal line
counts, so the file stays at 162 lines and every later line keeps its number.

### A1-repair — re-anchor the dead `config.toml:3298` pointer

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18,1 +18,1 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3298` at the 17:55:49Z receipt; value unchanged through 2026-10-18's rewrites — earlier pointers :2940 [16:57:35Z receipt] and :3227 [17:32Z rewrite] are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

### A1-nocause — the alternative NO-CHANGE text (parent picks ONE of A1-repair / A1-nocause)

If the parent prefers not to churn the pointer, land **no** patch and record
this cause in the round report instead (verbatim text for the record):

> **PROVINCE.md:18 — ADJUDICATED NO-CHANGE.** The pointer
> `~/.kimi-code/config.toml:3298` no longer names a pin line: `config.toml` is
> now 3570 lines and its only `rea-agents@` occurrence is at :3546; :3298 holds
> `max_context_size = 1048576`. The clause is explicitly receipt-stamped
> ("at the 17:55:49Z receipt") and names its own supersession chain
> (:2940 → :3227 → :3298), and that receipt is tracked in-repo
> (`.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`, line 1 =
> `2026-10-18T17:55:49Z`) — so the *value* claim and the *citation terminus*
> both hold; only the live-line reading is dead, and the clause does not claim
> one. The census gate cannot see this class: `classify()` collects pointer loci
> only when a block carries no `@`-pin, so `ptr_check` never runs on :18
> (direct call: `ptr_check('~/.kimi-code/config.toml', 3298, {'kimi':'6.7.0'})`
> → `('stale', …)`). Named as a *reviewer-enforced* residual: PROVINCE's
> drift-prone block re-anchors rather than accumulating, and the next round
> that touches this line should re-anchor it then.

### A2 — Ghidra feature count

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -46,1 +46,1 @@
-| Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 35 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
+| Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 34 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
```

### A3 — host fallback readers: absent-tool list

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -62,1 +62,1 @@
-| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |
+| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx, plus `7z`, `xxd`, `radare2`, `strace`, `upx` (host-installed 2026-10-13, after this row's sweep) | `command -v <tool>` | absent: `cabextract`, `rizin`, `ltrace`, pacman-contrib |
```

### A4 — PE-subtypes reserve

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -82,2 +82,2 @@
-- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
-  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
+- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
+  procedures via Ghidra). Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7).
```

### A5 — recorded crashes: the universal is false

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -84,3 +84,3 @@
-- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
-  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
-  intake — neither exists. Retention decays oldest-first.
+- **Recorded crashes >32 MiB** — mechanism held (Core), and a sub-cap organic
+  core is now reachable (chrome_crashpad 17.6MB, probed exit 0); the huge
+  organic cores still exceed the cap; no cap-raising knob exists. Retention decays oldest-first.
```

### A6a — EVM bullet, both legs named (land only if c1's vyper entry lands first)

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -91,3 +91,3 @@
-- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
+  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
+  carrier (arc3-r4); selectors stay bare hashes (no signature DB → no name resolution).
```

### A6b — EVM bullet, solc leg only (true at HEAD, independent of c1)

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -91,3 +91,3 @@
-- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
+  (Core, r3-07) and real solc-0.8.37 carriers (Core, arc3-r1/r3); vyper-compiled
+  bytecode untested; selectors stay bare hashes (no signature DB → no name resolution).
```

### B1 — >90 MB PE scale wall closure

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -139,6 +139,6 @@
-- **>90 MB PE scale wall** — 91.6 MB Godot ARM64 PE hits REA's ~900s internal
-  session deadline (`provider_timeout`, GhidraClient.js:607), still progressing
-  at kill (r4-12) [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs
-  -Xmx2G headroom exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to
-  ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a
-  2-5MB PE.
+- **>90 MB PE scale wall** — CLOSED (arc2-r7: the same 91.6 MB Godot ARM64 PE
+  held, 75,218 procedures, 7.9G/9G peak, zero OOM, three validated analyzers
+  disabled; arc2-r8's no-disable control OOM-killed at 9G in 4m42.945s; not
+  OOM at this cap, RSS ~2.36GB vs -Xmx2G headroom). Residual: rerun id-stability
+  UNKNOWN; no natural unmitigated hold exists at this cap. The pre-r7 "Next:"
+  remediation is superseded by the validated analyzer-disable recipe.
```

### B2 — cross-version residuals

`PROVINCE.md`

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -157,4 +157,4 @@
-- **Cross-version residuals** — `compare-application-versions` still
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+- **Cross-version residuals** — `compare-application-versions` is EXERCISED on
+  both input classes (r12-02: JS-graph diff + managed all-unknown non-verdict) and
+  multi-version pacman pairs beyond expac are exercised (r4-10: op 2.34.1→2.40.0, qpdf
+  control) [r5-audit C1: merged from the pruned Frontier bullet — its `compare_javascript_export_shapes` item is now held (Core, r4-09)].
```

**Combined landing recipe (parent).** Apply A1-repair, A2, A3, A4, A5, A6a-or-A6b,
B1, B2 to `PROVINCE.md`; expect **162 → 162 lines** and a single changed-line
set (10 lines across 7 hunks). Then re-run, at the landing commit:

```bash
python3 .ufo/gates/c1-census-v10.py --root .            # expect PASS 0/0/0/0, exit 0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .           # expect findings=0 exit=0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict  # expect clean findings=0 exit=0
```

---

## 3. Before → after measurement for the chain's claim

The chain claim's falsifiable pair is: *staleness census (each checked bullet:
stale / current / adjudicated, with evidence) → stale count N → 0; PROVINCE line
count unchanged; census PASS at the work tree after the parent applies the
patches.*

| quantity | before (HEAD `015e1ba`) | after (patch set applied on scratch) | how measured |
|---|---|---|---|
| PROVINCE.md lines | 162 | **162** | `wc -l` on the scratch tree (§4.1) |
| PROVINCE.md sha256 | `d075a3c6…` | **`dce736cd…`** (A6b) / `feec841b…` (A6a) | `sha256sum` (§4.1, §4.5) |
| items adjudicated by this seat | — | **13** (8 REPAIR, of which 1 is a two-text fork; 5 NO-CHANGE) | §1 |
| items this seat marks stale | **8** (:18, :46, :62, :82-83, :84-86, :91-93, :139-144, :157-160) | **0** after patch application | §1 + §4.4 |
| lines changed | — | **16** across 6 hunks, all `replace`, zero insert/delete | §4.4 |
| census verdict | PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0` exit 0 | PASS, same counts, same locus floors (17/14/3) | §4.2 |
| citation probe (default) | `findings=0 exit=0` | `findings=0 exit=0` | §4.3 |
| citation probe (`--strict`) | `clean findings=0 exit=0` | `clean findings=0 exit=0` | §4.3 |
| patch hunks applied | — | **8/8**, each `applied=1 failed=0` | §4.1 |

**The honest reading of this table.** The census verdict is *unchanged before
and after* — because the instrument cannot see any of the items (§0). That is
not a defect in the measurement; it is the measurement. The freshness movement
this chain claims lives in the **adjudication ledger** (stale 8 → 0) and in the
two instruments' continued PASS, not in a census number that could not have
moved. A census-only before→after would read `PASS → PASS` and would be
indistinguishable from "nothing was checked" — which is precisely why this seat
exists in the roster and why the claim's own wording says "census-checked …
or adjudicated NO-CHANGE with cause".

---

## 4. Verification performed (scratch-tree, read-only on the real tree)

Fresh extraction of HEAD into `/var/tmp/ex15/scratch/final` (`git archive HEAD |
tar -x`), byte-identical to the repo (`PROVINCE.md` `d075a3c6…`, 162 lines).
Patch texts extracted mechanically from §2 into `/var/tmp/ex15/patches4/` and
applied with the wave's own applier (`claims/c2/RV-4/prose-apply.py`, the
chain's declared format), then graded by both instruments. **Nothing in the repo
tree was modified by this seat** (`git status --porcelain` shows only the
untracked round-4 wave directory).

### 4.1 Apply report

Fresh extraction of HEAD into `/var/tmp/ex15/scratch/final` (`git archive HEAD |
tar -x`), pre-apply identity re-derived as `PROVINCE.md`
`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`, 162 lines.
Patch texts extracted mechanically from §2 (fenced `-`/`+` groups) into
`/var/tmp/ex15/patches4/` and applied with the wave's own applier. Run, verbatim
(A6b variant; A6a re-run separately in §4.5):

```
=== pre-apply (must be d075a3c6… / 162) ===
d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad  PROVINCE.md
162 PROVINCE.md
=== apply set (A6b variant) ===
--- a1-repair-re-anchor-the-dead-config-toml-3298-pointer.patch.md
  hunk 1 [PROVINCE.md]: applied (1 - / 1 +)
hunks: applied=1 failed=0
--- a2-ghidra-feature-count.patch.md
  hunk 1 [PROVINCE.md]: applied (1 - / 1 +)
hunks: applied=1 failed=0
--- a3-host-fallback-readers-absent-tool-list.patch.md
  hunk 1 [PROVINCE.md]: applied (1 - / 1 +)
hunks: applied=1 failed=0
--- a4-pe-subtypes-reserve.patch.md
  hunk 1 [PROVINCE.md]: applied (2 - / 2 +)
hunks: applied=1 failed=0
--- a5-recorded-crashes-the-universal-is-false.patch.md
  hunk 1 [PROVINCE.md]: applied (3 - / 3 +)
hunks: applied=1 failed=0
--- a6b-evm-bullet-solc-leg-only-true-at-head-independent-of-c1.patch.md
  hunk 1 [PROVINCE.md]: applied (3 - / 3 +)
hunks: applied=1 failed=0
--- b1-90-mb-pe-scale-wall-closure.patch.md
  hunk 1 [PROVINCE.md]: applied (6 - / 6 +)
hunks: applied=1 failed=0
--- b2-cross-version-residuals.patch.md
  hunk 1 [PROVINCE.md]: applied (4 - / 4 +)
hunks: applied=1 failed=0
=== post-apply ===
dce736cd1dba288cb5cd80f49035a3e594a4da50603cc1ef24f31a9e4b0f5c9c  PROVINCE.md
162 PROVINCE.md
```

**Every hunk's search text matched verbatim and exactly once** (`prose-apply.py`
refuses on ambiguity). Post-apply line count **162** — the same as pre-apply.
Post-apply sha256 `dce736cd1dba288cb5cd80f49035a3e594a4da50603cc1ef24f31a9e4b0f5c9c`.

> **A defect this seat caught in its own artifact, recorded rather than
> smoothed.** The first extraction of §2 produced three hunks (A5, B1, B2) whose
> `+` groups were one line longer than their `-` groups; applied, they took the
> file to **163** lines — breaking the claim's own "line count held" clause.
> The measured count is what caught it, not a review of the prose. All three
> were re-tightened to equal-length groups and the set re-extracted; the table
> above is the corrected run. A patch-text author who trusted the prose would
> have shipped a 163-line "line-neutral" patch.

### 4.2 Census on the patched tree

```
$ cd /var/tmp/ex15/scratch/final && python3 .ufo/gates/c1-census-v10.py --root .
…
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit 0
```

**PASS, and identical in every counter to the HEAD run** (§0). The census does
not move because the patched lines are outside its declared unit — which is the
point of §0 and §3, not a failure of the run. What the run *does* prove is that
the repairs did **not** disturb the unit the census does cover: PROVINCE's
current-ok locus count stays 17, the DATED markers at :40/:45/:119 still assert,
no `SCOPE-ERROR`, no `UNREADABLE`, no `UNDECLARED`. That is the "repairs must
stay pin-conformant" clause, measured.

### 4.3 Citation probe, both modes

The probe requires a readable Git work tree (`git rev-parse --git-dir`), so the
patched `PROVINCE.md` was copied into a **scratch clone** of the repo at
`/var/tmp/ex15/scratch/repo` and committed there (`3a7e4fee…`); the real repo was
never written.

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

**Both modes clean**, matching the HEAD baseline
(`claims/c2/EX-16/evidence/probe-head-both-modes.txt`: `reported findings=0
exit=0` / `clean findings=0 exit=0`). In particular `prov18-pin-value`
(`rea-agents@6\.7\.0` on line 18) and `prov18-stamp-named` (`17:55:49Z
receipt` on line 18) both still hold — the A1-repair text keeps the pin verbatim
and keeps the receipt stamp, moving only the line pointer. This is the check
EX-16 flagged as the one that binds hardest, since line 18 is the only
line-pinned PROVINCE target in the table.

### 4.4 Diff audit (the patch touched only what it claims)

`diff -u <HEAD:PROVINCE.md> <patched PROVINCE.md>`, opcode-level:

```
base lines: 163  final lines: 163          (split('\n') count; = 162 lines of text)
('replace', 18, 18, 18, 18)
('replace', 46, 46, 46, 46)
('replace', 62, 62, 62, 62)
('replace', 83, 86, 83, 86)
('replace', 92, 93, 92, 93)
('replace', 139, 144, 139, 144)
('replace', 157, 160, 157, 160)
```

Six `replace` opcodes, **zero** `insert`/`delete` opcodes — no line was added,
removed, or moved. Every replaced range maps to a claimed target:

| diff range | claimed target | disposition |
|---|---|---|
| 18 | A1 | REPAIR (pointer re-anchor) |
| 46 | A2 | REPAIR (feature count) |
| 62 | A3 | REPAIR (absent-tool list) |
| 83-86 | A4 + A5 | REPAIR ×2 (PE reserve; crash universal) |
| 92-93 | A6b | REPAIR (EVM solc leg) |
| 139-144 | B1 | REPAIR (>90MB wall closure) |
| 157-160 | B2 | REPAIR (cross-version residuals) |

The A4 and A5 hunks merge into one opcode because they are adjacent
(83-86 spans both bullets); the other five map one-to-one. **Nothing outside
these ranges changed** — the five NO-CHANGE items (D1-D5) are untouched, which
is the observable form of "adjudicated, not repaired".

### 4.5 The A6a variant

Re-run on a second fresh extraction (`/var/tmp/ex15/scratch/a6a`), same seven
hunks with A6a substituted for A6b: all eight applied cleanly, post-apply
`162` lines, sha256 `feec841b9a5c4ba7304e407fd7ac1dbffb4e665152ba510642b41eca4e20d41c`,
census `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. Both
variants are mechanically landable; the difference is **truth**, not
applicability (A6a's vyper clause depends on c1's entry landing in the same
commit).

---

## 5. Attacks / refutations attempted, with verdicts

| # | attack | expected if true | observed | verdict |
|---|---|---|---|---|
| 1 | "The census already covers the Frontier bullets — the claim's census half is instrument-satisfied." | a Frontier-line mutation reddens the census | `SCOPE` has no row covering 73-93 or 133-162; the region carries zero loci in the instrument's unit; census PASSes identically with the region intact | **REFUTED** — the region is outside the declared unit (§0) |
| 2 | "`ptr_check` would catch the `:3298` pointer if it ran." | direct call returns stale | `ptr_check(…, 3298, …)` → `('stale', "line holds no rea-agents pin: 'max_context_size = 1048576'")`; `…, 3546, …` → `('ok', 'pins 6.7.0')` | **CONFIRMED** — the checker is correct; it is simply not reached (`if not occ`) |
| 3 | "The `35 features` count is right and the directory listing is what's short." | `ls` shows 35 | `find -maxdepth 1 -mindepth 1` → 34 (34 dirs, 0 files); the corpus entry's own enumerated list has exactly 34 names, matching disk with zero diff in either direction | **REFUTED** — the number is a miscount of its own list |
| 4 | "The absent-tool list drifted because the row was written before those packages existed." | install dates after the row | all five installed `2026-10-13 13:52`; the row landed in `a43d442` at `2026-10-13 12:16:39 -0300` | **CONFIRMED** — same-day host change, ~1.6 h after the sweep |
| 5 | "The >32 MiB bullet is right: no organic core fits the cap." | every organic core > 33,554,432 B | 17,608,704 B crashpad core dumps; `inspect-recorded-crash` on it → exit 0, `ev_2cef7d11…`, 3 threads, 53 segments | **REFUTED** — a sub-cap organic core exists *and* the verb completes on it |
| 6 | "The same bullet's refusal is gone (cap raised)." | over-cap input now succeeds | 172,793,856 B core → exit 1, `invalid_request`/`out_of_range`, "exceeds 33554432 bytes" | **REFUTED** — the cap is intact; only the universal is false |
| 7 | "A sub-cap core must be a synthetic self-kill, not organic." | `crash-godot`/bash self-kill | `coredumpctl info 1857`: `chrome_crashpad_handler`, Grok Bot 0.71.2, Electron 42.1.0, `SIGBUS`/`BUS_ADRERR`, real stack frames | **REFUTED** — it is a real application crash |
| 8 | "`compare-application-versions` is still refused, so :157 stands." | no success record in corpus | r12-02 records two success legs with byte-identical re-runs and a negative ladder | **REFUTED** |
| 9 | "No second pacman pair was exercised, so :158's second clause stands." | corpus shows only expac | r4-10's target section is "cached pacman pairs (`uniq -d` walk: 354 duplicated pkgbases)" with `op` + a `qpdf` control, both extracted `tar -xOf` from the cache | **REFUTED** — this seat's addition; VZ-2's substring test read it as current |
| 10 | "The >90MB wall bullet is fine because it is only a *record*." | wording reads as closed | it ends in "Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`…", a remediation, and the corpus/README both say CLOSED | **REFUTED** — an open remediation for a closed wall |
| 11 | "The :18 pointer is genuinely dead but harmless, so NO-CHANGE is right." | value claim depends on the line | the receipt is tracked in-repo and the clause is receipt-stamped; the value re-derives live | **CONFIRMED as defensible** — hence two texts in §2; parent picks |
| 12 | "A same-line repair will break the DATED marker at :45 or the probe needle at :18." | marker/needle reddens | measured in §4.2-4.3 (census PASS, probe 0/0 both modes after the patch set) | **REFUTED** (measured, not assumed) |
| 13 | "My own patch texts are stale relative to HEAD." | search text not found | §4.1 apply report — every hunk's search text matched verbatim, exactly once | **REFUTED** (measured) |
| 14 | "This seat's artifact self-identifies a hash it has since invalidated (rule #14)." | a stale self-hash | this artifact pins no hash of itself; every hash it prints belongs to a *target* file and was re-derived after the final write | **REFUTED** — §7 |

**Not attacked, and named as such:** the *cause* of the `config.toml` churn
(operator-side interactive-session edits) is not re-derived here; the r3 receipt
and the live file are both read-only evidence and the drift is stated as a
fact, not attributed. Likewise, whether c1's vyper entry lands in the same
commit as these patches is a parent decision (A6a/A6b).

---

## 6. Blockers

None for the seat task. Named gaps and hand-offs for the parent:

1. **A1 is a genuine fork** — two texts, one decision. This seat recommends
   A1-repair; either is defensible and both are written to be landable as-is.
2. **A6a/A6b sequencing** — A6a's truth depends on c1's vyper entry landing in
   the same commit. A6b is unconditionally true at HEAD. Do not land A6a alone.
3. **Cross-artifact residual (out of this seat's write scope):**
   `corpus/knowledge/2026-10-13-r3-evm-interface.md:122` still reads "`xxd`
   absent on this host; node used instead" — the same A3 drift, in a corpus
   file this seat may not write. Named for the parent / a future corpus round.
4. **Instrument boundary, named not repaired:** the census's `PTR` branch is
   unreachable whenever a clause carries a pin (attack 2). Closing that would
   be an instrument edit; it is outside this chain's scope and would itself
   need the external scope audit (H4). Recorded for a future instrument round.
5. **Count refresh is calibration, not freshness:** `PROVINCE.md:50`'s "1556
   signed archives" now reads 1350 (cache eviction). Adjudicated NO-CHANGE
   (D3) with the reasoning; a re-receipt is a calibration action.
6. **Not re-measured by this seat:** the `## Core` table's other rows
   (lines 44-62) were read and adjudicated only where a defect was found;
   a full Core-table re-receipt is the calibration round's job, not this
   chain's, and the census's CURRENT rows 8-13/15-26/40-43/44/64-71 cover
   their version/pin unit.
7. **Delivery:** this artifact is the seat's complete output; no other file in
   the repo was written.

---

## 7. Identity discipline (rule #14)

Every byte-identity this artifact claims is a **target** identity, re-derived
after this artifact's final write, and re-checked in the §4 run:

- `PROVINCE.md` (repo, pre-patch): `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
  162 lines — re-derived with `sha256sum` and `wc -l` immediately before the
  patch run.
- Scratch base extraction: byte-identical to the repo copy (same sha256, same
  line count) — `git archive HEAD | tar -x`, verified by the same two commands.
- Patched scratch tree: sha256 and line count are printed in §4.1/§4.4 from the
  run itself.
- The four corpus entries, the r3 receipt, the r3 round-3 seat records and the
  peer seats' evidence files cited above are cited by path; their hashes were
  not re-derived by this seat and are not claimed.

This artifact records **no hash of itself** — a file that prints its own digest
is stale by construction on the next write (the r2 rule-#14 form-fix). Its
identity is whatever `sha256sum` returns at the parent's landing; the parent
re-derives it there.
