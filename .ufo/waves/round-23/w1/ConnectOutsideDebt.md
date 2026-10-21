# ConnectOutsideDebt — R23-C1 against the R20/R21 carried residual queue

Seat `KaidokuR23.ConnectOutsideDebt` (connector, leaf, author-side). Observation cutoff
`2026-10-21T14:43:59Z`. Lane HEAD `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
Frozen claim `.ufo/waves/round-23/claims.json` sha256
`249811d9d103960811025d5305422e97271877bec1f470c1601cadc1f40d1906`.

No REA producer, sigrok-cli, decoder, debugger, Frida, device, network or counter run was
performed by this seat. Machine work here was read-only: file reads, `git rev-parse`,
`sha256sum`, `stat`, `date`, and Python JSON/tar reads. Peer-produced records are marked as
such; where I did not independently re-run a peer's probe, that is stated.

The question is narrow: **does R23-C1 touch, preserve, or silently close any of the five
durable residuals left by R20/R21?** The answer is: it touches all five, closes none, and the
claim text itself names none of them. The risk is not a false closure in `claims.json`; it is
that the round's headline output (`k/6`) currently has no field that carries the debt.

---

## Verdict (bounded)

- **All five residuals remain open.** Their current disposition is stated in
  `corpus/lessons/round-21.md:31-35` and re-affirmed at `corpus/lessons/round-22.md:38`.
  Nothing in the frozen R23 claim or in the current R23 evidence changes those dispositions.
- **The claim is silent by name on all five, not preserving and not closing.** `claims.json`
  has one adjacent no-harm clause (`:61` `"source census exit0"`), one boundary clause (`:29`
  offline-only / adjacency unresolved, which covers only the no-execution half of ADJACENCY),
  and two falsifiers that could catch parts of SOURCE/ADJACENCY (`:36-37`). No clause names
  SOURCE, TIME, LINT-SANDBOX, CENSUS-GUARD or ADJACENCY.
- **The current counter can emit a green numerator without emitting any of the five.** At
  observed sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` its
  new-witness record is only `{entry, evidence_id, path}` (`count-c1.py:124`), and its result
  object (`:128-133`) has no residual or scope field. The envelope fields that would bound the
  claim (`authority`, `hardware_acquisition`, `provider`, `tool.sha256`) are present in the
  evidence and discarded by the count.
- **No silent closure has happened yet.** The concrete closure *shapes* are named below; none
  is observed in a retained R23 artifact as of the cutoff.

---

## Findings

### 0. What the claim actually freezes (observed)

- T1 six verbs, `before: 1`, `total: 6`, target `>=2/6`, exact k, incomplete unless 6/6
  (`claims.json:16-26`). The claim does not claim `6/6` or mastery (`:46-52`).
- `sourced` requires new knowledge to cite opened/mined **S058+** with exact used-by; historical
  R22 witnesses are preserved; new evidence only under `round-23/evidence/c1`
  (`claims.json:28`). This is an *additional* source gate over R22's S051+ rule.
- `boundary` excludes debugger/Frida live execution, says signal work is offline recording
  only, and says `inspect-dart-aot` is static parsing only (`claims.json:29`). "Adjacent
  ownership unresolved" is declared here, which is the correct ADJACENCY posture.
- `no_harm` says pre-round knowledge/source rows unchanged, LOG/SCORECARD prefixes preserved,
  prior admission criteria unchanged, R22 final `C1=1/6 C2=14/14`, map/citation rules
  preserved, source census exit0 (`claims.json:55-62`). None of these is a residual
  disposition.
- `inherited` concerns R22's 102 reportless seats (`:63`), not the R20/R21 residual queue.

**Observation:** the registry currently has 57 rows, S001-S057; no S058+ row exists yet.
`ReviewSourceCensus.md:5,9` independently recounts 57 rows (A51/B5/C1; mined55/rejected2) and
states no S058+ row. `corpus/SOURCES.md:57-63` ends at S057. A `grep -c S058
corpus/SOURCES.md` here returned `0`. Therefore the `sourced` clause is currently unsatisfied
for any new witness; the counter's S058+ gate (`count-c1.py:104-110`) will keep `new` empty
until a row lands.

### R20-SOURCE — rendered-quote caveats and unrowed `-c` anchors remain documentation debt

- **Residual:** `corpus/lessons/round-20-verifier-spotcheck.md:182` — S041/S045/S046
  rendered-quote caveats and S043's unadded `-c` source anchors remain scoped documentation
  debt; a fresh superseding row, never an in-place rewrite. `corpus/lessons/round-21.md:34`
  repeats it. `corpus/lessons/round-22.md:38` keeps it open.
- **R23 touch (observed):** the round opens a new source frontier: libsigrokdecode 0.5.3 UART
  decoder and the sigrok binary input format. `w1/UartSemantics.md:18-21` records the fetched
  release tarball (`892783` bytes, sha256
  `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0`), the git tag peeled
  commit `97991a3919da6a07c4c87308ae66fb441bd512e3`, and `decoders/uart/pd.py` sha256
  `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62`; its proposed row at
  `:246` is a raw-code tier-A row with exact member/line scope. I read the same local tarball
  under `.ufo/waves/round-23/w1/_uart/` and confirmed the digest
  `c50814aa…83fc0`; I read `decoders/uart/pd.py:98,102,125,217,223,391` directly
  (channels/options/annotation classes/bit-width/stop-bit TODO). The tag/URL facts are peer
  observations; the local bytes and line text are my direct observations.
- **Competing R23 proposal (observed):** `w1/CoverageMap.md:209-234` proposes S058 as an
  **own-work** row whose location is the retained R23 envelopes and whose anchors are the
  envelopes' `ok:true`/`ev_` values; S059 is the AppImage tool pin. That row is honest about
  being own-work, but it is a *local outcome* row, not an independent semantics source. Under
  R20-SOURCE's rule and R20-EVIDENCE's distinction (`round-20-verifier-spotcheck.md:181`,
  "QUALITY25 token/path binding is not Evidence authentication"), an own-work row cannot
  substitute for the source that teaches the decoder's option/annotation semantics.
- **What stays open:** the assignment of S058+; whether the new row is raw or rendered; whether
  the knowledge entry distinguishes *what the upstream source teaches* from *what the local
  envelope observed*. The counter enforces append-only S001-S057 rows (`:69-73`) and an S058+
  gate on id/tier/status/opened/used-by (`:105-108`), but it does **not** check quote class,
  location pinning, or whether the row is independent of the evidence it is used to admit.
- **Silent-closure shape:** land S058 as the own-work evidence family and describe it as the
  source for signal semantics; or "fix" S043 by adding `-c` anchors in place. Both would make
  the count look sourced while repeating the R20 debt class. Neither is observed yet.
- **Unknown:** whether L1 will land one row or three (raw source / own-work evidence / tool
  pin); whether the final `sources-census.sh validate` E11 (`used-by` path must exist on disk)
  passes for the entry path. E11 is an ordering constraint: row and entry must land in the
  same measured revision (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:27-33`).

### R20-TIME — new binary carriers enlarge the skip population; green text scan is not timeliness

- **Residual:** `corpus/lessons/round-20-verifier-spotcheck.md:178` — keep the two 2030
  fixture/diagnostic allowances separately visible; binary skips, zoneless timestamps and
  lexical limits are exclusions, not evidence of full-tree timeliness; freeze any future
  completeness claim's scanned population. `corpus/lessons/round-21.md:31` repeats it.
- **R23 touch (observed):** new tracked-or-trackable binaries:
  - `evidence/c1/uart-hi.bin`, 2500 bytes, sha256
    `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727` — the synthetic UART
    carrier. It contains NUL bytes and is classified `binary` by
    `.ufo/waves/round-20/tools/evidence-timestamps.py:208-209`.
  - `w1/_uart/libsigrokdecode-0.5.3.tar.gz`, 892783 bytes, sha256 `c50814aa…83fc0` — currently
    under the report directory and untracked; if committed it is a second binary skip.
  - `runtime/squashfs-root/` is gitignored (`.ufo/waves/round-23/.gitignore:1`), so it is
    outside a Git-revision scan; it is not a skip, it is absent from the population.
- **Comparator (peer-produced, read by me):** R22 final `evidence-timestamps.json` scanned
  `.ufo/waves/round-22` at `e9db7e2…`, `files_scanned:174`, `files_skipped:1`
  (`evidence/c2/empty.pcap`, binary), `finding_count:0`, `unexempted_finding_count:0`. That is
  the shape a R23 scan will take, with a larger skip list.
- **What stays open:** no R23 timestamp scan has been run or retained at the cutoff. The
  counter emits no `files_scanned`/`files_skipped` field, so its green numerator says nothing
  about the text scan, and nothing at all about the binary carrier's bytes. The counter's
  `.json`-only citation filter (`count-c1.py:113-114`) separately keeps the `.bin` out of the
  evidence binder; that is correct, but it also means the count cannot be asked to bound the
  carrier's timestamps.
- **Silent-closure shape:** report "round-23 evidence timestamps verified (strict, exit0)"
  without the `skipped` list; or let a no-harm clause imply the binary carrier was checked.
  The scanner's own rule says every skip "needs review"
  (`evidence-timestamps.py:251-261`); a skip is not a pass.
- **Unknown:** whether `_uart/*.tar.gz` will be committed; whether the final scan's `skipped`
  list is reported verbatim.

### R20-LINT-SANDBOX — no isolation boundary exists in the counter or the sigrok launcher

- **Residual:** `corpus/lessons/round-20-verifier-spotcheck.md:179` — D6a duplicate-name
  nested-read miss and D6b `--host-home`/AF_UNIX exposure remain; `revexec` is not a security
  boundary; do not inspect private HOME as proof. `corpus/lessons/round-21.md:32` repeats it.
  The residual trust is explicit in `.ufo/waves/round-20/tools/revexec.py:4-14` (same uid,
  AF_UNIX reachable, kernel bugs, not a boundary against root).
- **R23 touch (observed):**
  - The counter loads revision-extracted legacy code and executes it in-process:
    `count-c1.py:36-40` (`exec(compile(path.read_bytes(), …))`), after a byte pin at
    `:22-23,62-63`.
    Digest identity is not isolation. The temp file is written under
    `.ufo/waves/round-23/runtime` (`:50-55`), which is gitignored; the process runs as the
    caller's uid with the caller's network/AF_UNIX namespace. This is a fresh instance of the
    same trust family, not a revexec run and not a sandbox.
  - The sigrok launcher is **not** sandbox-local: `tools/sigrok-cli.sh:9-12` sets
    `LD_LIBRARY_PATH` to the extracted AppDir but preloads the **host**
    `/usr/lib/libgmodule-2.0.so.0`; `setup-sigrok.py:30` executes the AppImage with
    `--appimage-extract`. `w1/AppImageLibraries.md:22` observes the AppImage `.sha256_sig` and
    `.sig_key` sections are **all zero (unsigned)**, and `:45,53` observe the payload is
    missing `libglib-2.0.so.0`, `libgio-2.0.so.0`, `libgobject-2.0.so.0`, `libusb-1.0.so.0`,
    `libexpat.so.1` and requires the host for them. `:57-65` predicts the bundled gmodule /
    host libgio collision that the launcher's `LD_PRELOAD` works around. I did not re-run the
    signature byte scan; that fact is peer-observed.
  - The decoder run is resource-limited, not isolated: the retained envelope carries
    `normalized_result.resource_limiter = {configured_path: "/usr/bin/prlimit", args:
    ["--as=1073741824:1073741824","--fsize=67108864:67108864","--cpu=30:30","--core=0:0", …]}`.
    `prlimit` bounds address space/filesize/CPU/core; it does not create a filesystem, network
    or uid boundary.
- **What stays open:** D6a/D6b are untouched; no private HOME inspection occurred; the new
  in-process `exec` of revision code is an additional same-uid trust surface; the sigrok
  toolchain requires host libraries and an unsigned AppImage. No sandbox/security certification
  is warranted.
- **Silent-closure shape:** call the private worktree a "sandbox" and infer isolation; call the
  SHA-pinned AppImage "trusted" as if the pin were authentication; cite `prlimit` as an inode
  or execution guard. QUALITY24 already separates offline decoder **tool execution** from
  **carrier execution**; that separation must be stated, not assumed.
- **Unknown:** whether the `.sha256_sig`/`.sig_key` zero bytes prove the AppImage is unsigned
  under the AppImage spec (peer inference from zero bytes; I did not verify the spec); whether
  a future launcher can avoid the host preload.

### R20-CENSUS-GUARD — `sources-census exit0` is a different instrument and an instant attestation

- **Residual:** `corpus/lessons/round-20-verifier-spotcheck.md:180` — DATED shelter/same-line
  laundering and loader/copy/memfd/same-owner carrier-guard bypasses stay open; guard green
  attests bytes/modes at instants, never continuous non-execution.
  `corpus/lessons/round-21.md:33` repeats it.
- **Two distinct instruments (observed):**
  - `sources-census.sh` parses `corpus/SOURCES.md`, exits 0 on clean **or warnings**
    (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:16`), and W04 is "same URL across
    scopes; warnings do not affect clean lanes" (`:33`). R23 start-census
    (`.ufo/waves/round-23/start-census.json`, sha256 `26175ded…ba1e6`) records exit0 plus W04
    for **S033, S047, S054** — the same three warnings as R22 final
    (`round-22/verify/final/sources-census.json`). `ReviewSourceCensus.md:7` independently
    reconciles this and notes the R22 **start** snapshot had only S033/S047; the final added
    S054. So the R23 start set is consistent with R22 final, not with R22 start.
  - `c1-census-v10.py` is the SCORECARD/SKILL scope-table instrument. Its own header says H2
    same-line inline-marker excusal and t5 DATED-shelter are "still named, NOT closed here (no
    silent widening)" (`.ufo/gates/c1-census-v10.py:82-87`). It was **not** run in R23.
  - `carrier-guard.py` is only a mode-bit guard: it does not prevent loader-mapped execution,
    root/privileged restore, or execution of a separate copy
    (`.ufo/waves/round-20/tools/carrier-guard.py:15-18`). No arm/check record exists for
    `uart-hi.bin`; it is a synthetic fixture (mode 644), not a manifest carrier, and was never
    guarded.
- **What stays open:** the DATED/same-line classes, all loader/copy/memfd/same-owner bypasses,
  and the distinction between "`sources-census.sh validate` exit0 with W04" and "the c1-census
  gate passed". The claim's `no_harm: "source census exit0"` (`claims.json:61`) is true of the
  former only.
- **Silent-closure shape:** cite `source census exit0` as CENSUS-GUARD closure, or cite
  "carrier-guard not triggered" as non-execution proof. Neither is observed in the claim yet,
  but the clause is the hook a final report could misuse.
- **Unknown:** the final census after S058+ rows (new W04s, E11 ordering); whether L1 will run
  `c1-census-v10.py` at all this round.

### R20-ADJACENCY — new REA signal verbs expand a local surface map, not a province

- **Residual:** `corpus/lessons/round-20-verifier-spotcheck.md:183` — REA province overlap with
  revenger remains unresolved and reported; no silent ownership ruling.
  `corpus/lessons/round-21.md:35` repeats it. R21's `w1/ConnProvince.md:5-20` separates
  Kaidoku's REA-local tool/surface map from revenger's domain ledger and historical receipt;
  the broader adjacency remains unadjudicated.
- **R23 touch (observed):** two previously zero-mention REA verbs are now exercised offline:
  `inspect_signal_decoders` (`inventory.envelope.json`, ev_940c…, 110 decoders; `uart-help`
  ev_4be1…, 81 help lines) and `decode_signal_recording` (`decode-uart-hi.envelope.json`,
  ev_bcad…, annotations `300-1100 uart-1: 48` / `1300-2100 uart-1: 69`). The runs use
  `REA_SIGROK_COMMAND=<lane>/tools/sigrok-cli.sh` (`*.run.json` `env_overrides`). The envelopes
  declare `authority: "shipped-artifact"`, `hardware_acquisition: "not-performed"`,
  `provider: {id:"sigrok-recording", version:"sigrok-cli@0.7.2"}`. `w1/CriticScope.md:14-25`
  finds the device-control falsifier fails (REA argv cannot reach scan/acquisition) and the
  domain-bleed falsifier partly holds unless the entry/PROVINCE wording is corrected.
- **What stays open:** the REA-local surface map grows; that is not a province ruling, not
  dynamic signal ownership, and not provider availability over time (`claims.json:49` already
  disclaims the last). The offline file decode says nothing about hardware, device control or
  revenger's ledger.
- **Silent-closure shape:** present the new entries as held "signal analysis" or "UART/protocol
  ground"; or treat `REA_SIGROK_COMMAND` working once as provider stability. `CriticScope`'s
  wording correction is the compatible guard: name the entry as an REA verb envelope on this
  host for an offline file, not as domain capability.
- **Unknown:** whether the operator's live 6.7.0 registration changes availability (the claim
  pins the 6.5.0 CLI; S037 pins the 6.7.0 npm record; the installed cache used here is 6.5.0;
  no 6.7.0 run). That is a version-pin question, not an adjacency ruling.

### Cross-cutting observation: the count drops the fields that carry the debt

`count-c1.py` at the observed sha256
`f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` (the file changed during
the wave; line cites are to this sha; re-read before patching) does the following:

- Loads legacy R22 source from Git, pins its sha (`:22-23,62-63`), executes it (`:36-40`), and
  uses it only for the historical R22 root (`:81-83`). This answers `CriticGate.md:16-42`'s F1.
- Enforces that the historical R22 evidence tree and the S001-S057 source rows are unchanged:
  the old root tree hash must match baseline (`:66-68`) and the old source rows must be a
  prefix of the new rows (`:69-73`), else `historical_evidence_changed` /
  `historical_sources_changed`. This is the mechanical form of the R20-SOURCE append-only rule.
- Scans new-root entries itself, with an anchored citation regex (`:97`) — answering
  `CriticGate.md:43-63`'s F2 — and rejects non-JSON evidence citations (`:113-114`). The latter
  is correct for the binder but means the `.bin` carrier is cited provenance, not Evidence.
- Emits new witnesses as `{entry, evidence_id, path}` (`:124`) and drops the eligible source
  row id (`sid` is tested at `:105-108` but not stored), the envelope's `authority`,
  `hardware_acquisition`, `provider`, `tool.sha256`, and the resource-limiter kind. The result
  object (`:128-133`) has `limit` prose but no machine field for any of the five residuals.

So the current output can say `k=3/6` while a reader cannot tell from it whether the new
witness is raw-source-backed or own-work-backed, whether the envelope claims offline
acquisition, or which of the five debts the round touched. That is the gap this connector's
one move addresses. The append-only checks above are real and should be credited; they do not
substitute for a residual field.

---

## Affected axes

| Axis | Effect of the proposed move | Why |
|---|---|---|
| coverage (worked axis) | **protected, not inflated** | The move adds no verb and changes no k. It keeps a nominal `k=3/6` from being inadmissible on SOURCE/scope grounds by making the provenance and debt visible in the same record. |
| calibration | **improved in accuracy, no numeric proxy claim** | The claim's limits become machine-visible (`authority`, `hardware_acquisition`, `provider`, source media) instead of prose that a later reader can drop. |
| depth | **unchanged** | No depth claim or measurement is added. |

No axis is harmed: the historical R22 witness path, the six-verb denominator, the exit 0/1
semantics for 6/6 and incomplete, and the R22 files are untouched. The only new exit-2 case
is the already-declared "unevaluable" class in the BuildCounter spec.

---

## Proposed move (one, bounded)

**Carry the five residual IDs and the envelope's own scope fields into the R23 counter's
new-witness record, and fail closed when a new witness exists without them.**

This is a single additive change to `.ufo/waves/round-23/tools/count-c1.py`; it does not edit
`corpus/`, does not land source rows, and does not decide any residual.

### Exact shape

1. At the eligibility loop (`:104-110`), retain the qualifying `sid` (e.g. `source_row = sid`)
   instead of only `eligible = True`.
2. At the new-witness append (`:124`), replace the three-field dict with:
   ```json
   {
     "entry": "<knowledge path>",
     "source_row": "S058",
     "evidence_id": "ev_…",
     "path": ".ufo/waves/round-23/evidence/c1/<envelope>.json",
     "scope": {
       "authority": "<data.authority or null>",
       "hardware_acquisition": "<data.normalized_result.hardware_acquisition or null>",
       "provider": "<data.provider.id>@<data.provider.version>",
       "tool_sha256": "<data.normalized_result.tool.sha256 or null>",
       "source_media_hint": "own-work|live-url|local-artifact"
     },
     "trust": "digest identity only; not authentication; not an isolation boundary"
   }
   ```
   Read these by re-decoding the same `blob` with the already-imported `r21.decode`; do not
   re-run `bind_cli` and do not add a second JSON parser. `source_media_hint` is derived from
   the row cells only: `cells[3] == "own-work"` → `own-work`; `"http" in cells[2]` →
   `live-url`; otherwise `local-artifact`. It is a hint, not quote verification.
3. After the target loop (`:125-126`), build a top-level block:
   ```json
   "residual_carry": {
     "declaration_only": true,
     "ref": "corpus/lessons/round-21.md:31-35",
     "R20-SOURCE":        {"status":"open","touched_by":["corpus/SOURCES.md S058+","w1/UartSemantics.md:18-21,246"],"limit":"raw over rendered; superseding row only; no in-place rewrite of S041/S043/S045/S046"},
     "R20-TIME":          {"status":"open","touched_by":["evidence/c1/uart-hi.bin","w1/_uart/libsigrokdecode-0.5.3.tar.gz"],"limit":"binary skips are exclusions, not timeliness"},
     "R20-LINT-SANDBOX":  {"status":"open","touched_by":["tools/count-c1.py:36-40,62-63","tools/sigrok-cli.sh:9-12","tools/setup-sigrok.py:14,30"],"limit":"same-uid exec and host preload; unsigned tool; no sandbox/security claim"},
     "R20-CENSUS-GUARD":  {"status":"open","touched_by":["start-census.json"],"limit":"sources-census exit0 with W04; c1-census-v10 DATED/same-line and carrier-guard bypasses not closed"},
     "R20-ADJACENCY":     {"status":"open","touched_by":["evidence/c1/*.envelope.json","claims.json:29"],"limit":"REA-local surface only; revenger overlap unresolved"}
   }
   ```
   Add `"source_policy": {"round22":"S051+ mined 2026-10-21 (legacy)","round23":"S058+ mined 2026-10-21, exact used-by (R23)"}` so the asymmetry is explicit.
4. Enforcement, only when at least one `targets[verb].new` exists:
   - all five keys present, each `status == "open"`, each `touched_by` non-empty, else
     `raise ValueError("residual_carry_incomplete")` (the existing `main()` maps `ValueError`
     to exit2);
   - if a signal witness has a present `scope.hardware_acquisition` that is not
     `"not-performed"`, `raise ValueError("scope_conflict")`;
   - if a field is absent, emit `null` and a `scope_missing` list; do not infer a value.
   At baseline (no new witness) the block is emitted but not enforced, so the measured
   `k=1` exit1 is unchanged.

### What the move does and does not do

- It does **not** close any residual; `status:"open"` and `declaration_only:true` are literal.
- It does **not** decide source relevance or domain admission; those stay manual, as the
  counter's `limit` already says.
- It does **not** add a verb, change the denominator, or alter the historical R22 witness.
- It makes the `sourced` clause auditable: the witness record now names the exact row id and
  the media hint, so an own-work row masquerading as semantics is visible to the reader.

---

## Risks

1. **New exit-2 can block the round** if L1 does not populate the five-key block. Mitigation:
   the block is five literal `"open"` entries with refs; enforcement applies only when a new
   witness exists; baseline is unaffected.
2. **Scope-field absence in non-signal envelopes.** Dart/Flutter envelopes may not carry
   `normalized_result.hardware_acquisition`. Mitigation: `null` + `scope_missing`, fail only on
   a present contradictory value, not on absence.
3. **`source_media_hint` is a heuristic**, not a quote verifier. A local HTML snapshot would be
   labeled `local-artifact`; a raw code path and a copied rendered page are not distinguished
   by location alone. It must not be reported as source authentication.
4. **The counter is a moving target.** Its sha changed at least three times during the wave
   (`7c356b97…` → `f4b8d16a…`); line cites are to the latter. If BuildCounter/L1 rewrites it
   before integration, the edit points must be re-read, not patched blind.
5. **The residual ref `round-21.md:31-35` can drift** if lessons are renumbered. The literal
   IDs are stable; the line ref is advisory and should be treated as a pointer, not a digest.
6. **S058/S059 ordering is unresolved.** If CoverageMap's own-work S058 lands and
   UartSemantics' raw row becomes S059, the counter's `source_row` will say `S058` and the
   media hint will say `own-work`; that is visible, not fatal. The recommended assignment is
   S058 = raw upstream decoder source, S059 = own-work R23 evidence family, S060 = AppImage
   tool pin, so the primary source is independent of the evidence it admits. This is a
   recommendation, not a registry edit by this seat.
7. **No-harm wording tension, now resolved in code.** `claims.json:56` says "all pre-round
   knowledge and source rows unchanged"; `:28` requires new S058+ rows. The consistent reading
   is "S001-S057 byte-identical; S058+ appended", which is the R22 `source-rows.json` pattern
   (`old_rows_identical:true`, `before:50`, `after:57`) and is now enforced by
   `count-c1.py:69-73` (`historical_sources_changed`). The final report should still state the
   append explicitly, not "source rows unchanged" without qualification.

---

## Verification (author-side; not run here)

These are the checks L1 should run after integration; none was run by this seat.

1. **Baseline counter, unchanged:** `python3 -I -B .ufo/waves/round-23/tools/count-c1.py
   --root <LANE> --rev a3c92eb6bc70984e90ae5b895412de978840b2c5` → exit1, k=1,
   `historical` identify present, `new` empty, `residual_carry` emitted (not enforced).
   Peer-retained baseline from an earlier counter revision: `w1/.tmp-counter/r23-out.json`
   (k=1, 135/153 mentions, 18 zero); re-run at the current sha rather than assume it.
2. **Post-landing counter:** after S058/S059 + the knowledge entry at a measured revision →
   k=3, `targets["inspect-signal-decoders"].new[0]` and `targets["decode-signal-recording"].new[0]`
   each carry `source_row`, `scope.authority=="shipped-artifact"`,
   `scope.hardware_acquisition=="not-performed"`, `scope.provider=="sigrok-recording@sigrok-cli@0.7.2"`,
   and the five-key `residual_carry`.
3. **Fail-closed controls (new):** remove `R20-CENSUS-GUARD` from a copied output/input →
   exit2 `residual_carry_incomplete`; set a copied envelope's `hardware_acquisition` to
   `"performed"` → exit2 `scope_conflict`; cite an absolute/sandbox evidence path → no count
   (CriticGate F2 control).
4. **Census:** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` after
   the rows and entry land → exit0; record the full W04 set verbatim (expected to still include
   S033/S047/S054 unless a new duplicate URL lands); do not cite it as c1-census.
5. **Timestamps:** `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root
   <LANE> --rev <REV> --path .ufo/waves/round-23 --strict` after commit → record
   `files_scanned`, `files_skipped` (expect `evidence/c1/uart-hi.bin`, plus
   `w1/_uart/*.tar.gz` if tracked), `findings`, `unexempted_finding_count`; do not treat
   `skipped` as scanned.
6. **Source row identity:** `git diff --stat <baseline>..<rev> -- corpus/SOURCES.md` → only
   appended S058+ rows; `git show <baseline>:corpus/SOURCES.md` vs the same file at `<rev>` for
   S001-S057 → byte-identical (the R22 `source-rows.json` check, repeated for R23).
7. **No-execution scope:** confirm the only processes executed are the offline decoder
   (sigrok-cli via the lane adapter under `prlimit`) and the counter's Git/Python reads; no
   debugger, Frida, attach, device, or APK execution. The envelopes' `hardware_acquisition`
   field is the machine witness for the decoder runs; it is not a proof about other processes.

---

## Produced files

- This report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ConnectOutsideDebt.md`
  — SHA-256 reported in the final handoff (self-hash is not embedded; writing it would change
  the digest).

No other files were created or modified by this seat. No production lane file, registry row,
claim, counter, fixture, or sibling report was edited.

## Installs

None. No package, tool, AppImage, Python module, or npm package was installed or upgraded by
this seat. The sigrok AppImage extraction and the `_uart` tarball are peer-produced artifacts
already present in the wave; I only read them.

## Open risks

- **Unknown:** whether L1 lands the raw-source row (UartSemantics) before or after the own-work
  evidence row (CoverageMap); the S058/S059/S060 assignment is a recommendation, not a
  decision.
- **Unknown:** whether the final R23 timestamp scan and census are run at the delivered
  revision, and whether their full outputs (including `skipped` and W04) are retained. Without
  them, TIME and CENSUS-GUARD remain prose-only dispositions.
- **Unknown:** whether `c1-census-v10.py` is run at all this round; its DATED/same-line classes
  cannot be closed by `sources-census.sh`.
- **Unknown:** whether the AppImage's zero signature sections mean "unsigned" under the
  AppImage specification; that is a peer observation, not a spec-verified fact.
- **Inference:** the R23 evidence's `authority:"shipped-artifact"` plus
  `hardware_acquisition:"not-performed"` supports the claim's offline boundary for these two
  signal verbs; it does not support any hardware, device-control or dynamic-ownership claim.
- **Inference:** the current counter's anchored citation regex (`:97`) closes the specific
  absolute/sandbox-path hole CriticGate F2 demonstrated; it does not close the source-media or
  scope gaps above.
- **Not claimed:** any residual is addressed, reduced, or closed by this round. The five remain
  open at `corpus/lessons/round-21.md:31-35`.

Report: `.ufo/waves/round-23/w1/ConnectOutsideDebt.md`
