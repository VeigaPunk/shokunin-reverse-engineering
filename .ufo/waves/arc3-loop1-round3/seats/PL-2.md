# SEAT PL-2 — chain c2, role planner (arc3-loop1-round3)

Wave `arc3-loop1-round3`, 2026-10-19. Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` at every measurement. Seat line:
plan C2 (custody-pair hardening): D2 EACCES fail-open, D3 verify partial-reference,
write-guard scope extension to `set(paths) ∪ CUSTODY_PATHS`, D6 selftest scratch
guard — as declared exit classes; selftest growth 15 → ≥17 with case names;
coupled-landing list (tool + README + registry-row patch).

Discipline: no git mutation; custody paths read-only (sha256/stat capture only);
scratch `/var/tmp/pl2` and `mktemp -d /var/tmp/pl2-matrix-*` (never `/tmp`); wrote
only this seat's report and `claims/c2/PL-2/**`. Lane HEAD unchanged by this seat
(`git status` at close shows only other seats' edits, the standing round-10 dirty
path, and `__pycache__` residues).

## 1. Work performed (evidence pointers)

Sources read: `claims-frozen.md` (the claim + rules); round-2 C3 `verdict.md`
(D1–D7 named debt); the tool (`custody-pair.py`, 889 lines) and its README;
the four round-2 patch texts (`EX-40/proposed-edge-classes.patch`,
`EX-35/proposed-v1-verify-adapter.patch.md`, `EX-34/proposed-scratch-dir-guard.patch.md`,
`RV-12/proposed-scratch-mkdir.patch.md`), `RV-11/proposed-hardlink-guard.patch.md`;
`seats/VZ-4.md` (the write-guard finding, A11); `SCORECARD.md` round-2 section +
measurement recipe A; `corpus/QUALITY.md`; `AGENTS.md`; `EX-24/commandA-invariance.md`.

Base identities re-derived before any work: tool
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (889 lines),
README `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`.

Built and measured a patch-ready candidate (base + 22 anchored transforms, every
anchor asserted unique: `gen-candidate-run.out` = 22/22 ok, candidate
`6b37796457279e2465ce7f44edabf0f859d4ec5d3dea5d3050cfe8c4d83c3730`, 1,070 lines):

- before/after injection matrices against the same fixtures in the same minute:
  `matrix-before.txt` (`112d01dc…`) / `matrix-after.txt` (candidate);
- candidate selftest `CLEAN cases=22 passed=22 failed=0 exit 0`
  (`selftest-candidate.out`);
- candidate live pair over the 5 custody paths + `--require-paths 5` gate
  (`live-pre.txt` / `live-post.txt`, both 5/5 exit 0, `MATCH 5/5 exit 0`);
- v1 controls on the EX-35 fixture set (11 shapes; classes unchanged);
- round baseline: command A at HEAD `82/82, 14/14, 10.0/10.0`
  (`commandA-head.json`), census `PASS 0/0/0/0`, probe `findings=0`;
- identity/robustness probes: renamed-copy case-7 defect on the base
  (`DIRTY 14/15 exit 3`) vs closed by the candidate (`CLEAN 22/22`);
  `/proc/nope` scratch on candidate `exit 2` vs base traceback `exit 1`.

Then the real target went live mid-seat (EX-21 landing). This seat snapshotted and
independently measured every revision it could observe, read-only:

| revision | snapshot | selftest measured here | note |
|---|---|---|---|
| `112d01dc…` 889 L | `/var/tmp/pl2/before` | `CLEAN 15/15 exit 0` | base |
| `73c15b84…` 1109 L | `/var/tmp/pl2/landed` | **`DIRTY cases=21 passed=20 failed=1 exit=3`** — `require-paths-blocks-partial-reference`: `TypeError: _run_verify() got an unexpected keyword argument 'require_paths'` (call sites `:1013/:1019` vs signature `:1049`) | interim defect; two fixes measured on scratch copies (A2 argv-style `58c92ba6…`; B signature kwarg `a6668d30…`; both `CLEAN 21/21`); record `landed-fix.patch.md` |
| `7cd19c3c…` 1155 L | `/var/tmp/pl2/landed2` | `CLEAN cases=22 passed=22 failed=0 exit 0` | defect gone; 22 case names = this plan's §3 set verbatim; `case_label` uses `TOOL_PATH` (the §2.2 identity arm) |

Independent verification of the landed bytes (`matrix-landed2.txt`, this seat's
own runner against the `7cd19c3c…` snapshot): L1 `USAGE 2` no traceback; L2/L3/L4
`UNEVALUABLE 14` with no `MATCH` anywhere; L5 plain `0` / gated `USAGE 2` +
`REFERENCE-COVERAGE: 1/5 … unaccounted: 4 paths`; L6 both guard shapes `USAGE 2`
with target bytes unchanged; L7 pair `MATCH 5/5 exit 0` ± gate, receipts self-pin
`7cd19c3c…` (`landed2-out/live-pre.txt`); L8 v1 fixture classes identical to the
base; L9 custody digests unchanged. `matrix-landed.txt` is the same matrix at
`73c15b84…` (all four closures reproduced there too, with the DIRTY selftest).

Coordination: listings of `seats/` and `claims/c2/` polled (11 reports at first
listing, growing). Consumed `seats/EX-22.md` (before-state, matches this seat's
L2–L6 rows independently) and `seats/EX-25.md` (own union+inode guard probe —
same after-state, no conflict; EX-25's revision table corroborates the churn).
No other seat's output was needed for this plan.

Artifact inventory, identities re-derived after the last revision of each file
(`sha256sum` at 13:14Z):

| artifact | sha256 |
|---|---|
| `plan.md` | `5e797f22908960fa4c3d02e31146401850f78636d20b0eab0ef504b624fe1d58` |
| `landed-fix.patch.md` | `f54adadd2d87ae0c99099a0d928e6f44ffa66daf8a4c4a41ef9bc69527dc21fd` |
| `candidate.patch` (360-line unified diff) | `838f98fbc1d63d17d4c703521b66a2e25b283887acb08e95da4c21955aa49aec` |
| `gen-candidate.py` | `2bf88ecb5f29c1be819d52add5e89c22f8f7eff28a540addf411817393e8e6fb` |
| `gen-candidate-run.out` (22/22 anchors) | `2a9e5102e1a4b0cd155e17f1dab85a5b483994c35421d4bfb65d701679a80936` |
| `verify-candidate.sh` | `2d552eb07e262b45e5ff69f9247edacc707fed406dabc938331711d2464ba55d` |
| `matrix-before.txt` | `7a1819614253ba1ff03f2d01b39e7c8ae206dd413e4ec7b117b02b8141c31f4a` |
| `matrix-after.txt` | `b2725a198055783c368cee2a9fd69f491e752f641e2e538ed6cfd536fb0dd7a5` |
| `matrix-landed.txt` (`73c15b84…`) | `20bd6e2b32ba374811e3e3a9738e7faa2b40494087dc98f78edef8bbd3b81a62` |
| `matrix-landed2.txt` (`7cd19c3c…`) | `b93b151e77213d9cf784341ecd3a4eed9f3d5dfaff37b316162588d010375d50` |
| `selftest-candidate.out` | `53d83a1f1d87383d171478f4b6590b05d293f457f2eaf39463eccc288545a459` |
| `commandA-head.json` | `9de3cbddb68f19ad99003ad329b87b6670c6c83eb7b6f7aef14e1f7af7473cc1` |
| `live-pre.txt` / `live-post.txt` (candidate) | `f890b7f6650e3ced8a66e293daca83e8697c1b2a9d31858905946772000813d6` / `d9cd37a9539bae5af0fbb19eefc0de4ac4a8cd5b999cb3c2ccf8177108a6e645` |
| sidecars of the above | `cd9e51237f0dc11cef87c6fd71bb5b34fbb3c75ee41e8f5d0534ebaeecad9ec5` / `d96ad00b692cf106af1801b8d8e44c7d98f10cdba99757acad237e7bc3ee0194` |
| `landed2-out/live-pre.txt` / `live-post.txt` (pins `7cd19c3c…`) | `79add07c26168fc64548747e425520ecfd4330366ee6eb39444ada0371d770a2` / `ffb54c473f7600787a28b3fe07d86577b92eec3434aa3390e1d0842db3f8e637` |

## 2. Proposed changes (patch-text paths)

- `claims/c2/PL-2/plan.md` — **the seat deliverable**: the four closures as
  declared exit classes with code loci, hunks and fencing cases; the two gaps in
  the inherited patch texts (parser arm; case-7 identity arm); the selftest
  growth list (15 → 22, seven named cases); the coupled-landing list
  (tool + README + registry row + receipts + gates); the before→after table;
  attacks; residuals; the EX-21 application recipe.
- `claims/c2/PL-2/candidate.patch` + `gen-candidate.py` — patch-ready candidate
  (base `112d01dc…`, 22 anchored transforms, candidate `6b377964…`, 1,070 lines).
  Not applied to the real target by this seat (EX-21 owns it).
- `claims/c2/PL-2/landed-fix.patch.md` — the interim `73c15b84…` harness-defect
  record with both measured fixes and the exact remaining coupling gaps.
- README/registry-row wording is **not** drafted here as competing text: `plan.md`
  §4 states clause-by-clause what must change, and one voice must land the row
  (round-2 D10). No `*.patch` for the real target was authored by this seat.

## 3. Before→after measurement for the chain's claim (commands + outputs)

Runner: `bash verify-candidate.sh <tool.py> <outdir>` (identical fixtures, same
host/minute per pair). Chain claim's falsifiable unit = the four injections as
declared classes + selftest ≥17 + live pair MATCH 5/5 + command A unchanged.

| injection | before `112d01dc…` | after candidate `6b377964…` | after landed `7cd19c3c…` |
|---|---|---|---|
| D6 missing scratch | `exit 1`, 1 traceback | `exit 2`, 0 tracebacks, `USAGE:` line | same as candidate |
| D2a blocked dir | capture `13`; verify **`MATCH exit 0`** | capture `14`; verify `14`, no MATCH | same |
| D2b chmod-000 file | capture `exit 1`, **no receipt** | capture `14`, `EXISTS: yes` + `READ-ERROR` | same |
| D2 parsed receipt | **`MATCH-V1-PARTIAL exit 0`** | `UNEVALUABLE exit 14` | same |
| D3 1-of-5 | plain `0`; flag unrecognised | plain `0` (declared) / gate `2` + `REFERENCE-COVERAGE: 1/5` | same (gate text differs by 3 words) |
| WG scoped clobber | `exit 0`, target rewritten | `exit 2`, bytes unchanged | same |
| WG hardlink alias | `exit 0`, target rewritten | `exit 2`, bytes unchanged | same |
| selftest | `CLEAN 15/15` | `CLEAN 22/22` | `CLEAN 22/22` |
| live pair (± gate) | `MATCH 5/5 exit 0` (gate unrecognised) | `MATCH 5/5 exit 0` both | `MATCH 5/5 exit 0` both |
| v1 fixtures (11 shapes) | classes 2/10/12 per shape | identical | identical |
| command A at HEAD | `82/82, 14/14, 10.0/10.0` | n/a (no corpus/SKILL edit) | n/a |

Custody paths: digests `16f496e6…, 38d2a1d0…, bc66d543…, 7d2ca28a…, 6c6be761…`
before and after every run — 4/5 at the round-1 pins; path 3
(`~/.kimi-code/config.toml`) carries the round-2-recorded operator drift
(live, not repaired). v1 note: the round-1 receipts now read `CONTENT-DRIFT exit 10`
with `SHA256-CONTRACT 4/5` against live *because of that drift*; class control
runs stay isolated on the EX-35 fixtures.

## 4. Attacks / refutations attempted (verdicts)

| # | attack | verdict | receipt |
|---|---|---|---|
| 1 | "EX-40's D2 patch alone closes the fail-open" | **REFUTED** — the parsed-receipt path still reads `MATCH-V1-PARTIAL exit 0`; H5a/H5b (parser keys) required | `matrix-before.txt` L4 |
| 2 | "the candidate's clean selftest is a rubber stamp" | **REFUTED** — every new case fails on the base tool (exits 13/1/0, clobber, `FileNotFoundError`); legacy 15 stay green on both revisions | `matrix-before/after` L0–L6 |
| 3 | "the D3 gate breaks fixture/v1 workflows" | **REFUTED by design + measurement** — opt-in; EX-35's `v1-partial-1of5` fixture reads `0` plain and `USAGE 2` gated | `matrix-after.txt` L5/L8 |
| 4 | EX-35 Change 1 (v1 → exit 0) | **DECLINED** — contradicts the round-2 ruling (verifiability is the `SHA256-CONTRACT` line) and would blur a gate | `plan.md` §6 A4 |
| 5 | EX-35 Change 3 (blanket dispatch try/except) | **DECLINED** — would present programming errors as USAGE and hide the D2 class | `plan.md` §6 A5 |
| 6 | "D2 class swallows absent paths" | **REFUTED** — `ENOENT` stays `ABSENT 13` (legacy `absent-path-detected` green) | `selftest-candidate.out` |
| 7 | "write-guard extension over-refuses" | **REFUTED** — every legacy case writes receipts beside fixtures; 22/22 green | `selftest-candidate.out` |
| 8 | "selftest case 7 measures the bytes under test" | **CONFIRMED DEFECT (base)** — renamed copy spawns the sibling name → `FAIL … can't open file '<dir>/custody-pair.py'`, `DIRTY 14/15 exit 3`; closed by `TOOL_PATH` (candidate + landed `7cd19c3c…`) | `/var/tmp/pl2/probe/renamed*.out`; `plan.md` §2.2 |
| 9 | "the v1 statement holds unchanged at HEAD" | **PARTIALLY REFUTED** — contract holds, but the live drift moves the round-1 receipts to `10 / 4-of-5`; recorded, controls isolated | `plan.md` §4.5, A9 |
| 10 | "the candidate/landed revisions moved a custody path" | **REFUTED** — L9 digests identical across every matrix and revision | matrices L9 |
| 11 | "the landed revision meets the claim's selftest clause" | **REFUTED at `73c15b84…`** — `TypeError` in the new case → `DIRTY 20/21 exit 3`; both fixes measured; gone at `7cd19c3c…` | `landed-fix.patch.md`; `matrix-landed.txt` L0 |
| 12 | "the claim's coupled landing is complete once the tool moves" | **PARTIALLY REFUTED** — at 13:14Z the README had the class missing entirely (`grep -c UNEVALUABLE` = 0) while the tool already exited 14; it was updated minutes later (`752032cf…`: exit-table row `:120`, D2 section `:90-92`, precedence `:129`). `SKILL.md:390` still says `15 fixture cases` and has 0 `UNEVALUABLE` hits | this report §5; `plan.md` §9 |

## 5. Blockers, if any

No blocker for this seat's deliverables — plan, candidate, matrices, fix record
and this report are written; all identities re-derived above.

Open items the parent/EX-21 must handle (all measured, none mine to write):

1. **Registry row (`SKILL.md:390`, sha `c134afcb…` at 13:14:49Z)** still reads
   `15 fixture cases`, its worst-finding map has no `14`, and its precedence
   string omits `UNEVALUABLE` (grep: 0 hits). The claim's same-commit coupling
   clause is unmet until one merged row lands (D10: one voice).
2. **Round receipts must self-pin the landed revision**: the authoritative
   pre/post pair belongs to the round's executor; my pairs pin the candidate
   (`6b377964…`) and the `7cd19c3c…` snapshot (`landed2-out/`), which is evidence
   here, not the round artifact.
3. **Churn**: the target moved `112d01dc… → 73c15b84… → 7cd19c3c…` inside ~4
   minutes, and the README amended under me twice (`68458081… → 039993ed… →
   752032cf…`). Every identity in this report names its revision; re-derive at
   landing (round-2 D8 discipline). A DIRTY-selftest revision must not be the one
   the receipts pin.
4. **Declared residuals** (unchanged by this round, named so no record overclaims):
   D1 capture TOCTOU; D4 receipt self-authentication (sidecar not an anchor); D5
   out-of-band/root class (tripwire for attribution, not integrity control);
   sidecar-name targeting not scope-checked; `--require-paths <1` treated as no
   gate; the three permission cases pass trivially under euid 0.