# Round 30 — `inspect-rust-binary` positive class on three containers; refusal signatures predicted from code

Author: kaidoku L1, round 30, attempt 1 (in-session hyaku lane subagent). Lane-round base
`d210fb8fa62d2af04d009cfa0c65a4e8137dc742`. Instruments at `0dbabf78`; both claims frozen at `4ee65c67`
(`.ufo/waves/round-30/claims.json`, 02:35:13Z) before any REA run on a carrier or mutant. Pre-data control
wave `w1` (39 seats) dispatched 02:41:55Z; control receipts committed at `f39f4530` (`.ufo/waves/round-30/controls/`)
before the data commit `24da3459`.

Repair first. The outside decision on round 29 (`corpus/lessons/round-29-verifier-spotcheck.md`) is
`rejected-honest-stop` for axis misfit: R29-C1 re-scored a held rule on new author-built inputs and the trivial
baseline also met its target. This round leaves EVM naming and evidence-ID identity (the rejected streak) and
works a surface the lane had not governed: the positive input class of `inspect_rust_binary`.

## Claims

- R30-C1, coverage (surface: PROVINCE Core gains `inspect-rust-binary` on images that carry a cargo-auditable
  `.dep-v0` section; at the base PROVINCE names the verb 0 times and every lane run of it returned
  `auditable_metadata: null`). Counter `tools/round-30/c1-rust-positive.py`; target
  `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0. Entry
  `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` (S089, S091).
- R30-C2, depth (surface: a SKILL.md decision table of the reader's refusal signatures, predicted from the
  6.5.0 code). Counter `tools/round-30/c2-rust-refusals.py`; target
  `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`, exit 0. Entry
  `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (S090).

## Gate

New SOURCES rows (all opened 2026-10-23 by wave-1 scribes; the L1 re-read each report and copied the row):

| row | URL | access | sha256 | located quote (≤25 words) | decision |
|---|---|---|---|---|---|
| S089 | https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/README.md (+ PARSING.md, cargo-auditable.schema.json at the same commit) | 2026-10-23 | README `ccca48d9…`; PARSING `39e35b88…`; schema `c6ac9399…` | `README.md:95`: "The JSON is Zlib-compressed and placed in a linker section named `.dep-v0`." | admit, mined (`SrcCargoAuditable.md`) |
| S090 | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz (metadata https://registry.npmjs.org/rea-agents/6.5.0) | 2026-10-23 | tarball `531717a0…e699`; `RustAuditableReader.js` `1f3748c9…`, byte-identical to the installed copy | `package/dist/rust/RustAuditableReader.js:7`: "export const RUST_SECTION_BYTES = 1024 * 1024;" | admit, mined (`SrcReaPackage.md`); W04 duplicate URL with S083 (same tarball, different scope), kept |
| S091 | https://pypi.org/pypi/uv/0.13.0/json | 2026-10-23 | `2eaed6c8…b4c` (byte-identical to the committed copy) | line 1: `"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"` | admit, mined (`SrcPypiUv.md`); kind `dataset` (the draft's `registry` is not in the enum, E05) |

Rejected: a second row for the master copy of the cargo-auditable docs (not opened separately; the pinned commit
is the source); a row for `llvm-readobj`/`objdump` (host readers used as cross-checks, not learning sources).
Row changes old→new: none to existing rows; S089–S091 new (status `mined`, used-by the two round-30 entries). S090 anchor corrected after wave-2 `ReopenS090.md`: `cli.js` → `dist/cli-runtime/cli.js` (a different `dist/cli.js` exists) and `:5176-5217` → `:5176-5218` (the 1 MiB message is on line 5218).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail?) |
|---|---|---|---|---|
| M30-1 | A re-score of an already-held rule on new author-built inputs was labelled coverage, and its completeness-only target was also met by the trivial baseline (round 29). | `corpus/lessons/round-29-verifier-spotcheck.md:44,50-56,123-124` | outside verifier (routed defects 1–2); no lane rule | QUALITY row 48 and `tools/round-30/axis-fit-gate.py`: coverage/depth claims need `surface` and `unmoved_command`, and control receipts committed before the first envelope. Shown able to fail: round 29 exits 1 (`SURFACE_MISSING`, `UNMOVED_COMMAND_MISSING`, `RECEIPTS_ABSENT`; `.ufo/waves/round-30/w1/ExecAxisFitGate.md`); round 30 exited 1 at the freeze (receipts absent, `ExecAxisFitGate.md`) and 0 after `f39f4530` (`.ufo/waves/round-30/controls/axis-fit-gate-before-data.txt`). The gate checks presence and order only (QUALITY row 50): it does not catch the round-29 mistake if filler fields are written, so the content review of the controls stays the real check. |
| M30-2 | Shared frozen inputs were writable during a wave: seat `RevOracleVsReadobj` ran `llvm-objcopy --dump-section` without an output file, which rewrites the input, and altered 4 carriers at 02:42:35Z and 02:43:14Z. | `.ufo/waves/round-30/w1/RevOracleVsReadobj.md`; `CtlC1DoNothing.md` (first run `PIN carrier elf-x86_64-uvx absent or altered`, exit 2) | the C1 counter's per-run sha256 pin (QUALITY row 39 family) | Carriers restored from the verified wheel members and set `chattr +i` at 02:44:00Z (inode ctime); QUALITY row 49, narrowed for regenerated mutants by row 51. Shown able to fail: four control seats' first counter runs (CtlC1AllFalse, CtlC1DoNothing, CtlC1NoReader, CtlC1JunkRow) exited 2 on the altered bytes before any REA call; CtlC1ShortcutIds made one construction-only REA call on an altered carrier at 02:42:42Z and re-seeded on restored bytes. The `+i` copy refuses `llvm-objcopy` with "Operation not permitted" (wave-2 `ReviewQuality4849.md`). No measurement used altered bytes (data collected 02:59:33Z on sha-verified carriers). |
| M30-3 | A counter clause the L1 wrote is weaker than its sentence suggests: for predicted refusals, P2's committed-record check compares only the `ok` flag, so fabricated refusal records pass it. | `.ufo/waves/round-30/w1/CtlC2Sequence.md` (control `predictions-copied-as-observations`: matches 16 of 19), `RevPredicateIdentity.md`, `CriticTargetsControls.md` | the pre-data control wave (QUALITY row 48) | Disclosed, not repaired: the frozen counter is not edited. The live re-run remains the authority; a future counter compares the full refusal envelope. Not yet shown able to fail. |
| M30-4 | The first after-measurement (`24da3459`) printed `skill_ok=0`: the SKILL section named the entry and the verb on different lines. | `.ufo/waves/round-30/after/c2-rust-refusals-at-24da3459.txt` (exit 1) | the C2 counter's `skill_ok` | The decision-table lead line now names both; re-measured at `92b1dd2d` (`after/c2-rust-refusals-at-92b1dd2d.txt`, exit 0); later commits change no file the counters read, and the final tip is re-measured before filing. The receipt at `24da3459` is kept. |
| M30-5 | Round-29 carriers were called "published" although 15 of 16 lists were written from memory. | `corpus/lessons/round-29-verifier-spotcheck.md:127` (routed defect 5) | outside verifier | Appended correction lines at PROVINCE.md, the round-29 entry, corpus/README.md, SCORECARD.md and LOG.md (`ScribeR29Provenance.md`). |
