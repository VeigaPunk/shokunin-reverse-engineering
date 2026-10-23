# ConnFleetOverlap2 — sibling-lane ground vs round-30 after data

Seat: `KaidokuR30.ConnFleetOverlap2`. Scope: does any sibling lane's committed
ground conflict with the round-30 entries on Rust metadata, uv binaries, or the
REA error-envelope shape (`invalid_request` + `details.issues`)?
Read-only on every lane; REA not run (item sets REA to none); no installs; no
subagents; no carrier or mutant opened.

**Verdict: no conflict on any of the five terms.** Three overlaps exist and all
three are cite-not-absorb. One of them is new relative to wave 1: **revenger's
committed REA 6.4.0 error records are independent, earlier ground for the exact
envelope shape that R30-C2's entry asserts**, so wave 1's blanket "no sibling
lane holds ground on the round-30 surface" holds for the Rust-reader surface
only, not for the envelope surface that the same entry also states.

## 1. Term-by-term result (committed trees, `git grep … HEAD`, one lane per call)

`[obs]` File counts per sibling; full table and commands in
`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ConnFleetOverlap2/scan-log.md`
(sha256 `9d29e1ba801e8682d2dc9512faab1cc0e7dacd3bf29dffeafb5ad7fa4cf4736b`).

| term | siblings with hits | reading |
|---|---|---|
| `details.issues` (dot-escaped) | none | zero in every sibling; the only relaxed `details…issues` hits across the 20 siblings are revenger 11 files, kake 1 (Telegram-API prose), kotoba 1 (omp strings dump) |
| `invalid_request` | kama 3, kengaku 9, kotoba 1, kotodama 1, kumitate 7, revenger 18 | **three different namespaces** (§4); only revenger's is REA |
| `inspect-rust-binary` / `inspect_rust_binary` | none | wave-1 verdict re-confirmed |
| `.dep-v0` / `dep-v0` | none | wave-1 verdict re-confirmed |
| `uv 0.13` | gd3d 1, kagi 3, kake 3, kama 16, kengaku 18, kotoba 4, kotodama 4, kumitate 2, mado 10, mori 2, revenger 8, tameshi 15, tsukuroi 5 | host-version and tooling records only (§5); no uv-binary provenance claim |

`[obs]` Instrument control, 2026-10-23T03:16:54Z: the same five terms on
`kaidoku-shokunin` HEAD return 14 / 296 / 272 / 99 / 28 files, so the search is
sensitive where the tokens exist. Zero-hit lanes return `git grep` exit 1 with an
empty list (audio lane receipt, all five terms, `rc=1`, container exit 0).

`[obs]` Method difference from wave 1: this scan is HEAD-restricted, so untracked
scratch and worktree drift cannot enter the counts. Committed sandbox twins still
can and do (kengaku, kotodama) — they are ground, but they are copies of the same
committed text, not independent witnesses, and nothing below cites them.

## 2. Overlap O1 — revenger's REA 6.4.0 error object matches the C2 envelope shape

`[obs]` Six committed files under revenger HEAD
`876630dbb4d630e016d7d8c32a19ea04c646cbae`, e.g.
`corpus/live/runs/round-31/attempt-invalid.json` (sha256
`b4a0af729a23430e8fce2b727a0daa7dc5f2e53a3d57511046c4b0ec45fd2db3`):

```
{"code":"invalid_request","category":"invalid_input",
 "message":"Analysis input is invalid. Check the arguments and try again.",
 "retryable":true,"remediation":{"action":"Correct the listed arguments and retry."},
 "details":{"operation":"inspect_pe_resources",
   "issues":[{"path":["path"],"reason":"invalid_format",
     "message":"Resource range leaves its section's virtual size."}]}}
```

`[obs]` Round-30's committed C2 refusal `corpus/evidence/round-30/c2/envelopes/r-empty.json`
carries the **same error object field-for-field**, byte-identical in every generic
field (`code`, `category`, `message`, `retryable`, `remediation.action`), with
`details.operation` = `inspect_rust_binary`, the reader text in
`details.issues[0].message`, and an outer `{"ok":false,…,"meta":{"command":…,"duration":…}}`
wrapper. The reader text differs, as it must.

`[obs]` Differences, stated so they are not smoothed away:
- Pin: revenger's records are `rea-agents@6.4.0` (`corpus/live/runs/round-31/LEDGER.md:7`,
  `reviewer.md:95`); round-30 is 6.5.0.
- Operation: `inspect_pe_resources`, not `inspect_rust_binary`.
- Artifact class: revenger preserved the bare error object (no `ok` wrapper, no
  `meta`); round-30's counter stores the full CLI JSON. `[unk]` whether the 6.4.0
  CLI emitted a `meta` block that was dropped, or never emitted one for that
  command; revenger's LEDGER treats the file as the failed invocation record.
- Status: revenger calls it a failed, unscored attempt with no Evidence ID
  (`reviewer.md:95`).

`[inf]` The shape is therefore not a 6.5.0 discovery: two pins (6.4.0, 6.5.0),
two operations, and an identical generic message string. `[obs]` is limited to
what the two records show; stability across other operations and pins is not
measured.

**Cite-not-absorb (O1).** Cite these six files only as prior fleet ground for
the *envelope shape* and the generic-message hazard that C2's entry states at
line 43. Do **not** cite them as evidence for any of the 19 mutant outcomes, for
P2-match, for the 6.5.0 gate order, for the `resource_constraint` /
`unsupported_target` code family, or as a substitute for a live run. `[obs]` The
six attempt records carry only `invalid_request`; revenger's whole committed
`corpus/` has 0 occurrences of `resource_constraint` or `unsupported_target`
(space-tolerant `"code": ?"…"` search), while it does carry unrelated codes
(`executable_missing` ×4, `capability_unavailable`, `not_configured` ×3,
`provider_unavailable`, `version_unresolved`, `artifact_operation_failed`).

**Why wave 1 missed it.** `[obs]` Wave 1's patterns were
`dep-v0|cargo-auditable|inspect[-_]rust[-_]binary`, then
`auditable_metadata|RustBinaryImage|uvx|uv 0\.13`; `invalid_request` and
`details.issues` were never searched. Its verdict stands for the Rust-reader
surface and needs the §2 qualification for the envelope surface.

## 3. Overlap O2 — the fleet has no single REA pin

`[obs]` Committed sibling records: `rea-agents@6.4.0` (revenger live runs and
knowledge), `@6.5.0` (tameshi round-17 dispatch, mado round-19/20, kumitate
round-35/36 evidence), `@6.7.0` (kotoba round-47 pins, kumitate round-44 controls,
mado round-19 `AtkInstallsRecord.md:108`). Revenger's readiness checklist
re-verification of 2026-10-19 (`corpus/knowledge/2026-10-12-rea-readiness-checklist.md`,
K02/K03 rows) records `npm view rea-agents version` → `6.7.0`, "the skill's
current pin is `rea-agents@6.7.0`", and the omp MCP server registered at `6.5.0`.

**Cite-not-absorb (O2).** This does not conflict with the frozen claims (both are
explicitly 6.5.0) and must not be read as one. It does mean the C2 table is a
*pinned* table, not current-release behavior: a reader who knows 6.7.0 exists can
mistake the table for stale. Cite the 6.7.0 rows as the reason the pin sentence
must be explicit, never as a version at which any row was checked.

## 4. Overlap O3 — `invalid_request` is a three-way homonym in this fleet

`[obs]` Distinct denotations in committed ground:

1. **REA API error `code`** — revenger's six envelopes (§2); round-30's C2 envelopes.
2. **omp/UFO failure class** — kumitate `corpus/knowledge/native-admission-detail.md:110`
   (`FAILURE_RULES`, `invalid_request/400`, first-match-wins),
   `SKILL.md:438` (`400→invalid_request`), `failure-telemetry.md:92`,
   `reconcile-and-cycle.md:28`, `route-probe-cluster.md:225,509`.
3. **OpenAI-compatible error `type` `invalid_request_error`** — kama
   `README.md:2292,2387` and `server-common.cpp:96` (llama.cpp), kengaku
   `corpus/evidence/probe-r19-shim-ds-run.log:125`
   (`{"error":{"code":"invalid_request_error","message":"bad shape"}}`), kotoba
   omp strings dump.

`[obs]` The naive substring `invalid_request` matches all three; the
discriminating form `invalid_request([^_]|$)` drops namespaces 2 and 3 except the
omp rows, which use the bare class name.

**Cite-not-absorb (O3).** Never quote the C2 refusal table into omp telemetry or
route-health work (kumitate): REA's `invalid_request` means the *analysis input*
is invalid, not that a model or tool leg failed. Conversely, kumitate's
`FAILURE_RULES` rows are not REA envelope evidence and say nothing about
`details.issues`.

## 5. `uv 0.13` — records agree; three different objects share the version

`[obs]` Host records: `uv 0.13.0 (x86_64-unknown-linux-gnu)` at
`/home/vgpnk/.local/bin/uv` — game-dev-3d `reports/round-106/glb-unity-regression.md:20`,
mado `.ufo/waves/round-19/w2/reports/AtkInstallsRecord.md:42`, and the same
version as a tooling record in kagi, kake, kama, kengaku, kotoba, kotodama,
kumitate, mori, revenger, tameshi, tsukuroi. `[obs]` No sibling line matched by
the `uv 0.13` pattern asserts a different host uv version, and none asserts that
host uv differs from the manylinux x86_64 wheel member.

`[obs]` Different objects, same version string: tsukuroi's pacman repository rows
`uv 0.13.1-1` / `0.13.4-1` / `0.13.5-1` (round-24 mirror listings; wave 1 §2
already established they are sync-database entries, not installed packages), and
mado's upstream `uv 0.13.4` source test `tool_run_args`
(`.ufo/waves/round-21/w1/reports/OracleUvPackageHelp.md:12`).

**Cite-not-absorb (uv).** Cite the host-version records as consistent context for
the "host `uv` is the x86_64 wheel member" premise, never as provenance for the
frozen wheels (S091 is) and never the pacman/upstream-0.13.4 rows as carriers.

## 6. Rust metadata axis

`[obs]` Zero sibling committed ground on `.dep-v0`, `inspect-rust-binary`,
`auditable_metadata`, or any Rust reader symbol. The only string-level adjacency
remains tsukuroi's three `cargo-auditable 0.7.7-1` package-name rows
(wave 1 §2; re-counted here: `cargo.?auditable` → tsukuroi 3, all other 19 lanes 0).
No conflict, no support: the round-30 entries are the fleet's first ground on that
surface, as they claim.

## 7. Affected axes

- **R30-C1 (coverage): untouched.** No sibling ground names a carrier, a wheel
  digest, a section, a package list, or P1. Nothing to absorb; nothing to rebut.
- **R30-C2 (depth): the only axis with overlap.** C2's entry already states the
  envelope-shape observation as "not predicted and not scored" (line 43). O1
  supplies an earlier, operation-different witness to that same observation, and
  O2 supplies the reason its pin boundary needs to be said out loud. Neither
  changes a predicted outcome, the target line, or the confidence of any of the
  19 matches.
- **Substrate / readability:** O3 is the live hazard. The fleet's ops vocabulary
  already uses `invalid_request` as a failure class; the round-30 SKILL table adds
  a second denotation to the same token. That is a documentation collision, not a
  correctness defect, and it is resolved by one clause.

## 8. Proposed move (one, bounded)

**Append one short "Sibling overlap" paragraph to
`corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`, immediately after
the existing shape observation (line 43), before `## Limits`.** Current entry
sha256 `bb0518484e01386116d00fa9415fb129368ca0ef6bc68ba8acf2e11c1f6be4a3`.
Content, four clauses:

1. At 6.4.0 and on `inspect_pe_resources`, revenger's committed
   `corpus/live/runs/round-31/attempt-invalid.json` (+ rounds 35, 36, 51, 52)
   carries the same `invalid_request` error object, including
   `details.issues[0].{path,reason,message}` and the same generic `message`;
   cite the six paths and one sha256. State that it is a record of the shape,
   not of any mutant outcome.
2. The table is 6.5.0-only; the published `rea-agents` version recorded in fleet
   ground on 2026-10-19 is 6.7.0 (revenger readiness re-verification), and 6.4.0
   is in committed use as well.
3. `invalid_request` here is the REA API error code for invalid analysis input;
   it is not omp's `invalid_request` failure class
   (kumitate `native-admission-detail.md:110`) nor the OpenAI-shim
   `invalid_request_error` type.
4. No sibling artifact is used as evidence for P2-match or as a substitute for a
   live run.

Why this is safe against the freeze and the instruments: `entry_ok`
(`tools/round-30/c2-rust-refusals.py:258-271`) reads only the entry's first
`source:` line (must contain `S090`), the `| S090 |` row in `corpus/SOURCES.md:96`,
and the same row's absence at the base revision; `skill_ok` (`:273-277`) reads
`SKILL.md` only. An appended section touches neither, and no counter, predicate,
label, target, carrier, mutant, envelope, or PROVINCE row changes.

## 9. Risks

- **R1 — frozen-claim misreading.** The claims freeze forbids amending
  predicates, targets, carriers, predictions. This move is provenance prose in
  the entry. If the L1 judges any post-data entry edit as touching a frozen
  claim, keep these notes in this wave-2 report only and change nothing.
- **R2 — absorption.** A later reader may cite revenger's 6.4.0 record as P2
  evidence. Clause 4 is the guard; the absence of that clause is the failure mode.
- **R3 — pin overreach.** Do not extend the stability inference to 6.7.0. The
  observed stability is 6.4.0 → 6.5.0, two operations; 6.7.0 was not read.
- **R4 — verification ownership.** The C2 counter rewrites the shared mutants, so
  only seat `ReRunC2` may run it; this seat cannot verify the edit and did not try.
  An unrun check has not passed.
- **R5 — path coupling.** `skill_ok` requires a SKILL.md line naming
  `inspect-rust-binary` *and* this entry path. Do not rename or move the entry.
- **R6 — the artifact-class mismatch** (§2: bare error object vs full CLI JSON)
  must be stated as observed, not explained; the reason is `[unk]`.

## 10. Verification (for the owner, not run here)

1. After the edit, seat `ReRunC2` runs
   `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <post-edit REV>`
   → expect `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`, exit 0.
2. Text-only checks anyone may run read-only:
   `git show <REV>:corpus/SOURCES.md | grep -c '^| S090 |'` → 1;
   `git show <REV>:corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md | grep -c 'error.details.issues'` → 1 (the line-43 sentence survives);
   `git diff <pre-edit> <post-edit> -- tools/ .ufo/waves/round-30/claims.json corpus/evidence/` → empty.
3. C1 is unaffected: `python3 -I -B tools/round-30/c1-rust-positive.py …` need not
   be rerun for this move; if the L1 wants a no-harm receipt, the C1 target line
   must be unchanged (`carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`).

## Evidence ledger

`[obs]` All producing commands, per-lane counts, exit codes and the clock read
`2026-10-23T03:16:54Z` are in the scratch log named in §1; revenger HEAD
`876630db…`; the six envelope hashes are listed there and quoted in §2; worktree
bytes equal committed bytes for all six (`same`, 2026-10-23T03:15Z).
`[obs]` Round-30 entry hash `bb051848…`, C1 entry hash `e7927256…` (both
`sha256sum`, exit 0). `[obs]` No lane file was edited except this report; no
script outside scratch; no REA run; no process left running.
