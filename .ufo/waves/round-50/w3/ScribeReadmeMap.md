# ScribeReadmeMap — round-50 attempt 2, wave 3 (build)

**VERDICT: DRAFTED AND OFFLINE-VERIFIED — three paste-ready `corpus/README.md` bindings exist
(`## Coverage map` row, `## Frontier` edit, `## Knowledge` index row) and pass the FROZEN counter's
own binding code on a scratch clone. NOT LANDED by me (read-only seat). One critical defect found
outside my draft: the entry stem named in this seat's dispatch text — and in the L1's two landing
scripts — is stale; the frozen counter pins a third stem, and the landing scripts would write the
README rows with the wrong one, turning four C1 documentation bindings red.**

Draft: `.ufo/waves/round-50/w3/ScribeReadmeMap/readme.md` (paste-ready, with the conditionality
note and the §4 landing-script hazard).

## Behavior (what the drafts do)

| surface | edit | placement | binding it must satisfy |
|---|---|---|---|
| `corpus/README.md` `## Coverage map` | new row, section `SquashFS LE AVM members (round 50)`, stem `` `2026-10-28-r50-avm-le-squashfs-core` ``, state `**Core** — on four pinned vendor carriers, bounded: …`, ending with the supersession note for the round-49 note's LE-AVM clause | after the round-49 coverage row (base line 105), last row of the table | `tools/round-50/c1-counter.py:2479-2482` `b:coverage_map_row`; `tools/round-50/c2-record.py:496-517` atom **B1** (knowledge file mapped) |
| `corpus/README.md` `## Frontier` | (2a) new dated line `sasquatch — 2026-10-29 round 50: …` naming the superseding entry, superseding the round-49 line's LE-AVM clause and keeping the `~13k`-file clause; (2b) optional in-place removal of `LE AVM members (\`hsqs\`)` from the round-49 line with a forward pointer | 2a as the last bullet of the section; 2b on the round-49 bullet | none (documentation only); the counter reads no README `## Frontier` binding |
| `corpus/README.md` `## Knowledge` | new index row: stem, topic, source `S243, S244, S245, S249; receipts \`corpus/evidence/round-50/c1/\`; counter \`tools/round-50/c1-counter.py\``, verified-at `{{DATA_COMMIT_CI}}` (substitute the data commit's `%cI`) | after the round-49 knowledge row (base line 226), last row of the table | house style (4 cells); the counter reads no `## Knowledge` binding |

## Findings

| # | finding | evidence | severity |
|---|---|---|---|
| F1 | **The entry stem in this seat's dispatch text (`2026-10-29-r50-le-avm-hsqs-core`) is stale.** The FROZEN counter pins `STEM = '2026-10-28-r50-avm-le-squashfs-core'`, `ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'`. A row keyed to the dispatch stem leaves `b:coverage_map_row` red and B1 unmapped. The L1 already corrected `plans/round-50-attempt2-claims.md` in commit `6f4aba63` ("the counter, not this file, is the rule"). | `git show 435d41fd:tools/round-50/c1-counter.py` → lines 377-378; counter sha256 `9820811b…` identical at HEAD and at the freeze | critical (blocks C1) |
| F2 | **The L1's landing scripts carry a third stale stem and would write the README rows with it**: `land_c1.py:17` and `land_sources.py:11` both set `STEM = '2026-10-28-r50-le-avm-members-core'`; `land_c1.py` writes the entry, the coverage-map row, the Knowledge row and the Frontier line from that stem → `b:entry_present`, `b:coverage_map_row`, `b:frontier_note` (PROVINCE) red. `land_sources.py` also filters S243/S244/S245/S249 out (`S = {k: S[k] for k in ('S246','S247','S248')}`) → `b:sourced` red. `land_c1.py`'s Knowledge row is written with an empty `verified-at` cell; its PROVINCE Core row does not embed the entry path, which `c1-counter.py:2447-2451` requires. | `grep -n "r50-le-avm-members-core" .ufo/waves/round-50/l1/land_c1.py .ufo/waves/round-50/l1/land_sources.py`; `sed -n '139,153p' .ufo/waves/round-50/l1/land_c1.py` | critical (blocks C1) |
| F3 | The `**Core**` coverage row asserts `carriers_matched 4`, but the R50-C1 data run has not been executed (L1-only, after this wave). The row must land **only if** the counter exits 0 with `carriers_matched 4`; otherwise it becomes a *measured, not promoted* row (house style of the round-44 row) and the Frontier edit is dropped. | `plans/round-50-attempt2-claims.md` → "Landing order" step 3; no REA run this wave | high (honesty gate) |
| F4 | Frontier edit has a genuine style fork: the lane's habit is "a correction is a new line, never a rewrite" (C2 B3/B4/B5/B11). Option **2a-only** (append) leaves the round-49 bullet's `LE AVM members (\`hsqs\`)` text in place but explicitly supersedes it; option **2a+2b** removes the clause from that bullet (residue: the round-41 dated bullet still carries it). Both drafts are supplied and both pass the checks; the choice is the L1's. | `receipts.primary.log` vs `receipts.appendonly.log`; patched copies and diffs | medium (reviewer judgment) |
| F5 | `verified-at` in the `## Knowledge` row must equal the entry's own `verified-at:` (the data commit's `%cI`, per `ScribeEntryC1` / QUALITY 23). The dispatch text's `2026-10-29` is a fallback only. No counter binding reads this column. | `ScribeEntryC1` message; `c1-counter.py:393` `OPENED_DATES` applies to the SOURCES `opened` cell | medium |

## Verification (offline; no REA — forbidden this wave)

All commands ran on a scratch clone (`git clone --shared` → `checkout --detach 6f4aba63`) under
`/fast/scratch/hyaku/kaidoku-r50/w3-ScribeReadmeMap`; the lane tree was never written
(receipt `lane-clean`: empty `git status --porcelain` over `corpus/README.md SKILL.md PROVINCE.md
SCORECARD.md LOG.md corpus/SOURCES.md corpus/knowledge tools plans`). Receipts with command, exit
code, stdout sha256 and UTC time: `.ufo/waves/round-50/w3/ScribeReadmeMap/receipts/receipts.tsv`
(9 receipts, all rc=0).

| command | rc | stdout sha256 | UTC |
|---|---|---|---|
| `git -C <lane> rev-parse HEAD` → `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f` | 0 | `863f27ba40a7d473fc171fd4351b3873da3990fc3bbcb99c278b574b624a7eab` | 2026-10-29T20:36:40Z |
| `sha256sum <lane>/corpus/README.md` (README bytes: `a702bfdd6a32b89427d672b4522878742810e21dbe3f6db2b36c60268e1d2274`) | 0 | `c05049e3b2b833f7db4b004ca12af136298657c702435a9754fb5aa781747041` | 2026-10-29T20:36:40Z |
| `git -C <lane> show 435d41fd:tools/round-50/c1-counter.py` (counter bytes `9820811b…`, `STEM`/`ENTRY` at lines 377-378) | 0 | `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` | 2026-10-29T20:36:40Z |
| `sha256sum <lane>/tools/round-50/c1-counter.py` (identical to the freeze blob) | 0 | `22be8fa4e9ce41af0d68707d5609aca3e4d666db409c766604f93559141d7a3f` | 2026-10-29T20:36:40Z |
| `git -C <lane> grep -n r50-le-avm-hsqs-core` (hit only in the L1's correction note) | 0 | `bc36a9b2d71c9e5a305206196fdcff7dc36685662f42334f44bc28c72322e23a` | 2026-10-29T20:36:41Z |
| `git -C <lane> status --porcelain -- corpus/README.md SKILL.md PROVINCE.md SCORECARD.md LOG.md corpus/SOURCES.md corpus/knowledge tools plans` (empty) | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-29T20:36:41Z |
| `python3 -I -B patch_readme.py primary` (patch + all binding checks, variant 2a+2b) | 0 | `8c01c5fb361aa0f1e4258b2bca6c003580ce6402c1e108b592c7e548078dc659` | 2026-10-29T20:36:41Z |
| `python3 -I -B patch_readme.py appendonly` (variant 2a only) | 0 | `09170a79ffc60b2b72fd9865ec0f0e2e80cb1c5bf4d090227ca28e967364dd62` | 2026-10-29T20:36:41Z |
| `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (`/fast/scratch/hyaku` 39 % used, 494.6 G free) | 0 | `2e5ce8a5e6472db66e8c3a36b27c6771d99e1bb7f80d214faf291464cbfd7ea3` | 2026-10-29T20:37:16Z |

Binding checks executed **against the frozen instruments' own code** (read-only `importlib` load of
`tools/round-50/c1-counter.py` and `tools/round-50/c2-record.py` from the clone), for both variants:

- counter `STEM` == drafted stem → **True**; `section(readme,'## Coverage map')` contains exactly **1** row naming the stem, and the counter's own `coverage_map_row` expression evaluates **True**.
- `unique_section` for `## Coverage map`, `## Knowledge`, `## Frontier` → unique / unique / unique.
- `map_token(STEM)` matches the `## Coverage map` section → **True**.
- B1 mapping simulation: 139 knowledge files at HEAD → **0 unmapped**; with the landing entry present (140) → **0 unmapped**.
- drafted row shape: coverage row 3 cells, Knowledge row 4 cells, Frontier line contains no pipe.
- `## Frontier` after the edit: last bullet is the round-50 line; contains the `~13k` clause; names the entry. Residue after 2b: only the round-41 dated bullet.

**Not run:** REA (forbidden this wave), `c1-counter.py --rev` scoring (needs the data run + carrier
cache; L1's job), `c1-counter.py --selftest` (not needed for a documentation-binding draft; the
counter's bytes were not modified — sha256 unchanged at HEAD).

## Gates

| gate | state |
|---|---|
| lane tree read-only | **met** — no write outside `.ufo/waves/round-50/w3/ScribeReadmeMap{,.*}`; `lane-clean` receipt empty |
| no REA this wave | **met** — no `npx rea-agents` / `rea` invocation |
| no vendor firmware bytes | **met** — no download at all; no carrier bytes in the lane |
| fixture clone discipline | **met** — `git clone --shared` into scratch, `checkout --detach`, `rev-parse --show-toplevel` asserted to the clone path; no commit, no identity set |
| scratch hygiene | **met** — scratch removed after receipts were copied (see artifact list) |
| exit-code semantics | rc 0 = met for every check above; no check was reported that was not run |

## Touched surfaces

Written (this seat only): `.ufo/waves/round-50/w3/ScribeReadmeMap.md` (this report),
`.ufo/waves/round-50/w3/ScribeReadmeMap/readme.md` (paste-ready drafts),
`.ufo/waves/round-50/w3/ScribeReadmeMap/{patch_readme.py, receipts.*.log, readme.*.patched.md,
readme.*.diff, receipts/}`.
Peer messages sent: `ScribeEntryC1` and `ScribeRowsSources` (stem correction + `used-by` cell).
Nothing else in the lane, the fleet repo or `.ufo/state/` was touched; no git mutation was run.

## Out of scope (not mine, flagged for their owners)

- the PROVINCE `## Round-50 additions to Core` row and the `Round-50 frontier note` line (`ScribeProvinceBinding`);
- the entry file itself (`ScribeEntryC1`) and the SOURCES rows `S243/S244/S245/S249` (`ScribeRowsSources`);
- the L1's `land_c1.py` / `land_sources.py` stem fix (F2) — I cannot write under `.ufo/waves/round-50/l1/`;
- the C1 data run and the counter scoring (L1 only, after this wave).

## Artifacts

- `.ufo/waves/round-50/w3/ScribeReadmeMap/readme.md` — paste-ready drafts (§0 stem, §1 coverage row, §2 frontier edit, §3 knowledge row, §4 landing-script hazard, §5 verification)
- `.ufo/waves/round-50/w3/ScribeReadmeMap/patch_readme.py` — the patch + verification driver (offline; applies only to the scratch clone)
- `.ufo/waves/round-50/w3/ScribeReadmeMap/receipts.primary.log`, `receipts.appendonly.log` — verification stdout (both rc=0)
- `.ufo/waves/round-50/w3/ScribeReadmeMap/readme.primary.patched.md` (sha256 `297a5310…`), `readme.appendonly.patched.md` (sha256 `c1bdaa48…`) — patched README copies (scratch only, never in the lane tree)
- `.ufo/waves/round-50/w3/ScribeReadmeMap/readme.primary.diff` (sha256 `62329926…`), `readme.appendonly.diff` (sha256 `b736c73d…`)
- `.ufo/waves/round-50/w3/ScribeReadmeMap/receipts/receipts.tsv` + `receipts/*.out|err` — 9 receipts (command, rc, stdout sha256, UTC)

Tools installed/updated this seat: **none** (no package, binary or service was installed; the
task needed only read-only git, `python3` and `sha256sum`).
