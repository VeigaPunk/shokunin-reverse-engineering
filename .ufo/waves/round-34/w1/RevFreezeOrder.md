# RevFreezeOrder — read-only freeze/order/pins audit (round 34, attempt 1)

| Field | Value |
|---|---|
| Seat | `KaidokuR34.RevFreezeOrder` (reviewer, Godspeed) |
| Sandbox | `/fast/scratch/hyaku/kaidoku-r34/w1/RevFreezeOrder` (branch `seat-r34-RevFreezeOrder`, base `54a87a51…`) |
| Lane root | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| Audit | First-add commit order (counter/reader/red fixtures), independent manifest/source/table, claims freeze, current before-receipt and control outputs, no production data, frozen_inputs pin coverage, expected-author independence |
| Mode | Read-only; no repo tool executed (no parser, no counter, no producer). Evidence: git object reads, `sha256sum`, JSON structural analysis, grep. |

## 1. Commit order (names, axes)

Git parent chain (equal in sandbox and production):
`ec3125ad` (round-33 base) ← `8897a67f` (*round-34: source-backed ELF reader and admissible prefreeze inputs*) ← `54a87a51` (*round-34: freeze ELF version-needs predicate before adversarial controls*) ← `d52e2404` (production HEAD, *retain baseline and validated isolated control dispatch*).

- **Every instrument first appears in the same single commit `8897a67f`**: `tools/round-34/version-needs-counter.py`, `tools/round-34/elf-version-needs.py`, `tools/round-34/freeze-integrity.py`, `.ufo/waves/round-34/prep/R34Expected-files/author_expected.py`, `.ufo/waves/round-34/expected.json`, and `corpus/evidence/round-34/elf/e01.bin…e12.bin`. There is no inter-artifact ordering — the first-add is atomic for all of them, and it precedes the claims freeze.
- The freeze commit `54a87a51` adds only `.ufo/waves/round-34/claims.json` and updates `corpus/claim-freezes.tsv` / `claim-freezes-v2.tsv`. No instrument or fixture changed after first-add.
- Red fixtures are not separate files: the negative fixture cases are **inline text fixtures** in the counter's `--selftest` (`version-needs-counter.py` lines 228–266: `red-junk`, `red-all-false`, `red-duplicate-json`, `red-exit`, `red-documents`, `red-boolean-schema`, `red-pin`, `red-manifest-count`, `red-replay`; plus `green-empty`/`green-translated`). They share the same first-add commit `8897a67f`.

## 2. Pin coverage — every declared hash verified

All digests below confirmed with `sha256sum` against the production worktree and `git show` against freeze/instruments commits.

| Pin | Declared | Verified |
|---|---|---|
| `expected.json` (manifest) | `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` | yes, at freeze and worktree |
| knowledge doc `2026-10-23-r34-elf-version-needs.md` | `d721189c9df0a267c22dd566d488deb3c19e3b1365f1e1f8cfaf0ba2092aa639` | yes |
| `approved-skill-section.txt` | `c156effc825c46930bc08309888102a47e7011c5b589a453dceb2e961c8d2ba6` | yes |
| source `lsb-symversion.html` | `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91` | yes |
| source `glibc-elf.h` | `fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f` | yes |
| carriers e01…e12 (12) | each in `frozen_inputs` | all 12 yes |
| counter | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` | yes at `8897a67f`, at `54a87a51`, and in worktree |
| reader | `ac7d24a546022c7cc8295450a2692c51c07099e42a1aa02fb69c29455dae3f33` | yes at `8897a67f` and worktree |
| freeze-integrity | `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138` | yes at `8897a67f` and worktree |
| author_expected.py | `916e066964ebe09c1015ed641621f9ec51354c1399eef65263537cbaf8b9c797` | yes at `8897a67f` and worktree |
| claims.json | — | byte-identical at `54a87a51`, `d52e2404`, worktree: `bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4` — no post-freeze amendment |

Source cite spans spot-checked in the captured bytes: `glibc-elf.h:459` defines `SHT_GNU_verneed 0x6ffffffe`; lines 1124–1161 contain `Elf64_Verneed` (ends 1133), `VER_NEED_CURRENT` (1138), `Elf64_Vernaux` (ends 1161). `lsb-symversion.html` contains the `Elfxx_Verneed`/`Elfxx_Vernaux` structure blocks at ~644–677 and ~833–845 (claim quotes 615–677, 717, 839–845, 937). Both source files are present with the pinned hashes.

## 3. Independent manifest/source/table

- Production `.ufo/waves/round-34/expected.json` is byte-identical to the independent-expected seat's artifact `.ufo/waves/round-34/prep/R34Expected-files/manifest.json` (same sha `f22e7e3b…`); `MANIFEST.sha256` lists the same value. `selection.json` records the prefreeze e11 swap and dev-selftest exclusions.
- Manifest structure: `{schema:1, carriers:12}`; totals **107 `needed` records / 339 `Vernaux` records** — exactly the claim's width. Per-carrier counts and `.dynstr` (`string_table` offset/size) match the prep tables; every `string_table` offset+size lies within the carrier file; every carrier size+sha256 verified against the files on disk.
- `e12` (static `sln`) has `needed: []` and `string_table: null` — the absent-section/empty control, matching the claim's `empty_control`.
- The counter validates the manifest schema (`validate_manifest`), requires `string_table {offset,size}` for every nonempty carrier, and pins the manifest blob to `manifest_sha256` at the freeze revision (`measure()`).

## 4. Expected-author independence

- `version-needs-counter.py` contains **no reference** to `author_expected.py`, `author_challenge.py`, or the challenge schedule (grep over the file). The `input-transfer.json` note is accurate: the challeng `challenge/` artifacts are retained as bounded independent-author evidence only.
- The production counter's schedule-1 rename is generated in-process by `renamed()`: a Sattolo single-cycle shuffle of the 64-character ASCII alphabet (`secrets.randbelow`, unpredictable per run, no fixed points) applied byte-wise to the linked `.dynstr` slice; the prediction is derived in-process from the manifest expectation by the same bijection. Same-length, ASCII, and non-identity by construction. This is not the frozen author schedule.

## 5. Two schedules per carrier

`score()` runs two schedules per carrier: schedule 0 = original bytes vs manifest expectation; schedule 1 = renamed candidate vs in-process prediction; a carrier matches only if **both** attempts match (`all(a["matched"]…)`). For `e12` (null `string_table`) schedule 1 repeats the empty record against the unchanged bytes — no `.dynstr` is invented. Output is compared under canonical JSON (`object_pairs_hook` duplicate-key rejection, strict schema).

## 6. Before receipt and controls — honest, no production data

- `before/c1-at-base.json`: `--freeze 54a87a51… --rev ec3125ad…` → exit 1, `finding: reader_absent`, `matched: 0`, `met_target: false`, scope "Base reader absent; no production reader invoked." Correct: the reader only exists from `8897a67f` onward, so at base revision nothing could be scored.
- Selftest control chain (all `--selftest`, exit 0, 11 cases, text-only isolated fixtures, no ELF scoring):
  - `counter-selftest.json` (initial, unlabelled findings) — instrument `859f2fbd…`
  - `counter-selftest-stable-findings.json` (supersedes initial) — instrument `80aa26d6…`
  - `counter-selftest-final-prefreeze.json` (supersedes both; stable finding labels, nonidentity Sattolo permutation, selected-revision source pin checks, explicit empty-requirement branch) — instrument `d7f0a8cf…` = frozen digest
  - `counter-selftest-at-instruments.json` — same frozen digest `d7f0a8cf…`
- Production tree after freeze contains only wave-dispatch metadata: `before/c1-at-base.json`, `w1-dispatch.json`, `w1-sandboxes.json`, `w1-spec.json`, `w1-submitted.json`, `w1-validator-stderr.txt`, `w1/swarm-registry.json`. `corpus/evidence/round-34/elf/` contains exactly `e01.bin…e12.bin`. No score envelopes, no result JSON, no `elf-meta` copies, no parser products anywhere in production. **No production data exists.**

## 7. Findings by severity

No blockers or actionable defects found.

- **Info — atomic first-add.** All instruments/fixtures/manifest landed together in `8897a67f`, before the claims freeze `54a87a51`; freeze commit touched only `claims.json` + TSV rows. Order is as claimed and stable.
- **Info — pins all hold.** Every `frozen_inputs`/`instruments`/`documents`/`sources` hash verified at the declared revisions and in the worktree; `claims.json` unmodified since freeze.
- **Info — independence holds.** Counter never reads the author schedule; unpredictability comes from in-process Sattolo/`secrets`; author challenge artifacts are inert evidence.
- **Info — width matches.** 12 carriers, 107/339 records, e12 empty; string-table bounds sane.
- **Info — honest controls.** `c1-at-base` is a genuine pre-data miss (`reader_absent`); selftest supersession chain is documented and converges on the frozen instrument digest.

## 8. Residual risk / verification gaps

- Read-only role: the counter/parser/selftests were **not executed** here; runtime behavior rests on the committed control receipts, code inspection, and hash verification. The reader's FINDINGS decision-table self-test and the counter's `SKILL.md`-section / `SOURCES.md`-row checks at the measured revision are declared in code but were not re-run (would require executing the counter).
- Manifest counts/values were read from the frozen `expected.json` and cross-checked against the prep report's dual-path readelf methodology; expected records were not re-derived from carrier bytes in this seat.
- Host volatility (documented in R34Expected §8.5): pins are to the copies, not host paths; a host package change would invalidate digests, not the frozen copies.

## 9. Evidence retained

`RevFreezeOrder-files/evidence.txt` — commands and digests. No production files were modified; no git/jj writes; no tool installs.
