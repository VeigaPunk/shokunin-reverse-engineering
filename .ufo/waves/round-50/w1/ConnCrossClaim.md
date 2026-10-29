# ConnCrossClaim — round 50 wave 1: cross-claim pattern scan (R50-C1 × R50-C2)

Seat: `ConnCrossClaim` (leaf connector, no dispatch). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (read-only). Round-49 freeze referenced by the frozen round-49 counters: `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` (ancestor of base; the round-49 C2 counter's freeze walk passes at base). Receipts: `.ufo/waves/round-50/w1/ConnCrossClaim/receipts/` (`SHA256SUMS`, 26 files). Matrix: `.ufo/waves/round-50/w1/ConnCrossClaim/conflict-matrix.tsv`. Fixture commits were made only in a `git clone --shared` under scratch, with the toplevel asserted before each commit and a clone-local identity. Nothing in the lane or fleet repo was staged, committed, stashed or written. Scratch removed after the receipts were copied.

## Verdict

**Separable on the verdict, not separable on the read set. Do not freeze the draft as written.**

1. **Landing text is one-way separable.** Doc-only edits (PROVINCE and README lines) leave the C2 counter green (overlay B, exit 0). The round-49 `ConnSeparability` measured the same two-claim file set: neither landing flips the other's verdict. The round-50 C1 counter does not exist yet, so the C1 side for the new rows S152–S154 is `[INFERENCE]`.
2. **Coupled, measured:** any added SOURCES registry row flips the **frozen round-49 C2 counter** to exit 1 at any REV after round 50 (its A8 counts every row added since `e4f2cfa5`). That counter cannot be patched; the consequence must be disclosed or routed.
3. **Coupled, by plan text:** round-50 C2 atom B1 (coverage fraction) reads C1's knowledge entry and coverage-map row; atom B9 (registry census) reads C1's instrument rows if its scope includes `tools/round-50/c1-*`; both claims would write the same `## Owned axes` coverage row. That row is already stale at base (states 138/138; base has 139 knowledge files, all stems mapped).
4. **Defect in the C1 port draft (pre-freeze fix required):** `frozen_drift` runs an unpathspec'd, non-merge-aware `git log --name-only --no-renames FREEZE..REV`. A frozen-path edit made inside a merge commit is invisible to it; the plan's rule (`-m --diff-merges=first-parent`, pathspec) sees it.

Before the single freeze commit: (a) fix the C1 walk; (b) reserve S150–S154 by name; (c) list frozen paths per claim, not `tools/round-50/` as a whole; (d) move B1 and B9 off the other claim's writes; (e) pin or disclose the REV-read inputs listed below; (f) record the round-49 A8 flip as a known REV property of a frozen counter.

## Findings table

Exit codes are the commands' own. Receipts are under `.ufo/waves/round-50/w1/ConnCrossClaim/receipts/`.

| # | Finding | Command (abridged) | Exit | Key result | sha256 / receipt |
|---|---|---|---|---|---|
| F1 | Base is clean and the frozen round-49 C2 counter is green at base | `git clone --shared` + `checkout --detach 7c678ae6`; `python3 -I -B c2-mismatch.py --root <clone> --rev 7c678ae6 --freeze decc5697 --json-out …` (counter taken from `git show decc5697:tools/round-49/c2-mismatch.py` into scratch) | **0** | `mismatches 0`, `atoms_total 9`, `counter_sha256 == counter_sha256_at_freeze` = `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` | stdout `488524a4f02852a0721a7eb421157348b0c281c2fff1edad181ad095f6127b5c`; `receipts/c2-base-nobattery.json` |
| F2 | An added registry row flips the frozen round-49 counter (A8). Verified with two synthetic C1-shaped rows S150/S151 (11 cells, used-by to an existing file) in clone commit `38e1ebcb` | same command, `--rev 38e1ebcb` | **1** | `A8: round 49: rows 146 -> 149, derived 146 -> 151`; `included/excluded 2/1, derived 4/1`; `mismatches 1` | `receipts/c2-overlayA.json` `c7642a5e2b08ae50aee336f30421ae711e37036d34797c33864cb75c42a2ce50` |
| F3 | Doc-only edits (PROVINCE and README lines) do not flip C2 (control) | same command, `--rev a761fa0f` (overlay B on base) | **0** | `mismatches 0`, `atoms_total 9` | `receipts/c2-overlayB.json` `ea06cf885b065e21700e82ac498753d8c2c4b946da960268ce8c4e7087023831` |
| F4 | Fleet registry validator, lane-root form, base | `bash sources-census.sh validate --today 2026-10-28 --root <croot> <croot>/kaidoku-shokunin` (copy of `scripts/sources-census.sh`, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, in scratch) | **0** | `ok` with 15 W04 cross-scope duplicate-URL warnings (warnings, not errors) | `receipts/census-base.stdout` `250e12e9b122f2564a4154ecab141b493ae0d18b1a6f17f4fca6d4845e4bc551` |
| F5 | Same validator with overlay A (two rows whose `used-by` names a missing file) | same, at `38e1ebcb` | **1** | `E11 S151 missing used-by corpus/knowledge/x.md` | `receipts/census-overlayA.stdout` `1215a93a4eae46a806414407ee5316c8c0231f8f14dea3a64485b784d6542ce7` |
| F6 | `--file` mode does not validate `used-by` (artifact, not a registry finding) | `validate --today 2026-10-28 --file corpus/SOURCES.md` at base | **1** | 241 E11 on base; every `used-by` path reported missing [INFERENCE: resolved relative to the given file's directory] | `receipts/census-src-base.md.stdout` `8c70387aa0ec1c5703021d13360f87829429c1fb3a029996fd0491a69e78fbc7` |
| F7 | E04 duplicate-URL behaviour for a correction row that reuses a URL. A same-URL row duplicating **rejected** S149 passes both with and without a `supersedes S149` marker; the code exempts `teaches` containing `supersedes S###` (lines 648–649) | row copy of S149 with a new id, teaches with and without the marker | **0 / 0** | both pass because S149 is `rejected`; the `supersedes` exemption was **not** isolated against a `mined` original | `receipts/census-v-super-teaches.stdout`, `receipts/census-v-nosuper-sameurl.stdout` (both `250e12e9…c551`) |
| F8 | Merge-commit blind spot in the freeze walk. A merge commit hand-edits a frozen file. The C1 draft walk (`git log --pretty=format: --name-only --no-renames B..M`) lists only the side and main files. The plan-rule walk (`git log -m --diff-merges=first-parent --name-status -- tools/round-50 plans/round-50-claims.md`) lists the edit | probe in scratch clone; merge `0572b9c776d916918ce55e80cc6eeccf39a4e857`; draft walk at `.ufo/waves/round-50/w1/C1CounterPort/tools/round-50/c1-counter.py:1199-1200` | — | draft: `main.txt side.txt`; rule: `0572b9c7 M tools/round-50/frozen-probe.txt` | `receipts/probe-merge-sha.txt` `23b072603b06018498936f13c7289b99a775cdba3d23c36aad8e1c61a8ae6642` |
| F9 | `tools/round-49` `.py`/`.sh` paths at base (B9 scope) | `git ls-tree -r --name-only 7c678ae6 -- tools/round-49 \| grep -E '\.(py\|sh)$'` | 0 | 6 paths: `c1-controls.py c1-counter.py c1-oracle.py c1-run.py c1-run.sh c2-mismatch.py` | — |
| F10 | The SKILL registry section that B9 names holds 4 data rows and no round-49/50 path; a different path-keyed counter table (round-42..45 rows, near SKILL.md:1742) exists | `sed -n 772,787p SKILL.md`; `grep -c 'round-49/' SKILL.md` | 0 | 4 data rows (`interactive-r1-recovery`, `citation-drift`, `custody-pair`, `quote-fidelity`); 0 `round-49/` hits | — |
| F11 | Owned-axes coverage row is stale at base; B1 is already red at base | `sed -n 19,25p SCORECARD.md`; `git ls-tree -r --name-only 7c678ae6 -- corpus/knowledge \| grep -c '\.md$'`; substring check of every knowledge stem in `corpus/README.md` at base | — | row reads `138/138 … round-47 landing`; knowledge files **139**; stems substring-mapped **139/139** (a substring test, not the lane's own counting command) | — |
| F12 | Round-49 search-log matcher is a prefix test on `- 2026-10-28 round 49`; round-50 entries must not start with that prefix (or with a round-50 prefix shared by two claims) unless tagged | read of `tools/round-49/c2-mismatch.py` `a8()`: `l.startswith('- %s %s' % (ROUND_DATE, tag))` | — | a second matching entry makes the count 2 and reds A8 | — |
| F13 | Round-49 A9 section is bounded by the next `##` heading; a round-50 correction placed under `## Record corrections — round 49` would change A9's input | read of `c2-mismatch.py` `sections(…, '## Record corrections \u2014 round 49')`; SCORECARD heading list (line 3768 is the last `##`) | — | exactly one such heading required at REV | — |
| F14 | Pointer hygiene for round-49 score artifacts cited by round-50 text | `git ls-tree -r --name-only 7c678ae6 -- .ufo/waves/round-49/l1/scores` | 0 | 7 files at base, including `c1-final.json` and `c2-final.json` (the round-49 wave-2 D1 finding does not hold at base) | — |
| F15 | Read-set inventory of both round-49 counters | `grep` for `show(` / `r.show(` / SOURCES, PROVINCE, README, SCORECARD, SKILL, LOG, lessons, knowledge across `tools/round-49/c1-counter.py` and `tools/round-49/c2-mismatch.py`; cross-checked with round-49 `ConnSeparability.md` traces | — | C1: PROVINCE (core heading, frontier line), README `## Coverage map`, entry, SOURCES S138/S139 (whole-file parse), `tools/round-27/xpin-attribute.mjs`, `tools/round-39/gen-squashfs.py`, round-42 pins. C2: SCORECARD (`## Round 48` at base; `## Record corrections — round 49` at REV), LOG (base and REV), lessons 48 and 49, SOURCES (all IDs, S145–S149, search log), `.ufo/waves/round-48/**` at base, `tools/round-49/**` names. Neither reads SHONEN, QUALITY, LEARNING, MANIFEST, claim-freezes, or any round-50 lesson | — | see matrix | — |
| F16 | Round-49 `ConnSeparability` measured two read-set violations in round 49: C2 battery do-nothing reads C1 landing content; C1 `frozen_drift` names C2's paths. Both verdict-neutral there | `.ufo/waves/round-49/w1/ConnSeparability.md` F3, F4 | — | cited, not re-run | — |

Not run: the round-50 C1 and C2 counters (drafts still in flight in sibling seats; the C1 port was read, not run), REA reruns, controls, and any `--data-run`.

## Conflict matrix (summary; full table in `conflict-matrix.tsv`)

| shared path | written by | read by | flip direction (verified or inferred) | disposition for the freeze |
|---|---|---|---|---|
| `corpus/SOURCES.md` | C1 (S150, S151, S112/S114 re-open, search log); C2 (S152–S154, search log) | C1 (S112, S114, S150, S151, entry-cited rows); C2 (all IDs, S138, S145–S149, search log) | **C1 rows flip the frozen round-49 C2 A8 (F2, verified).** C2 rows: same mechanism [INFERENCE from F2]. A `used-by` naming a missing file reds the validator (F5) | Not a frozen file. Freeze lists blob pins for S112, S114, S138, S139, S145–S149 (base), reserves S150–S154, and states the round-49 A8 consequence |
| `corpus/README.md` `## Coverage map` | C1 (entry row, knowledge row, frontier line) | C1 (stem binding); C2 B1 (count) | C1 → C2, one way: B1 count = 139 + C1 entry (F11 baseline) | Not frozen. C2 B1 reads base count plus a separate C1 mapping check, or is ordered after C1 |
| `PROVINCE.md` | C1 only | C1 only (C2 never reads) | none (F3 control) | Not frozen; C1-only |
| `SCORECARD.md` `## Owned axes` coverage row | C1 (if it touches the row) and C2 (B1) | C2 (B1, B2); round-49 A9 reads the round-49 correction section | **double write of one cell (conflict)**; A9 section boundary (F13) | Single writer: C2, after C1 lands. Correction heading `## Record corrections — round 50` (own `##`) |
| `SKILL.md` `## Local round-evidence gate registry` | C2 (B9 rows: round-49 six paths plus round-50 c2 instruments); C1 if it writes rows for c1 instruments | C2 (B9) | B9 at REV depends on C1's rows if the scope includes `tools/round-50/c1-*` (F9, F10) | Single writer (C2 landing commit). B9 scope = round-49 paths plus `tools/round-50/c2-*`. C1 instrument rows land in the same commit as B9 |
| `LOG.md` | L1 (freeze line, landing, data run); both claims' lines | C2 (base prefix rule, B11 freeze agreement) | EOF append collisions (textual) only | L1 writes the freeze line first; claim lines in landing order |
| `corpus/lessons/round-50.md` | L1 | none | none | Must exist before any registry row whose `used-by` names it (E11, F5) |
| `corpus/lessons/round-49.md` | none | C2 B11 (REV) | a later edit flips B11 with no freeze walk | Pin the base blob (round-49 rule: round-49 outputs read at base) or disclose |
| `corpus/knowledge/*` (C1 entry) | C1 | C2 B1 (count) | C1 → C2, one way | C1 first |
| `corpus/evidence/round-50/c1/**` | C1 data run (L1) | none (C2 do-nothing deletes names only, per plan) | none for the verdict; the battery reads names and content (round-49 F3) | Not frozen; restrict the battery restore to C2-read paths, or disclose |
| `tools/round-50/` | both | both freeze walks | **whole-directory freeze couples the walks**: a post-freeze edit to one trips the other (exit 2 `frozen_path_changed`) | Per-claim frozen lists (below), same freeze commit |
| `tools/round-49/**` | none | C2 B9 (names) | none | Byte-frozen, not edited |
| `SHONEN.md`, `corpus/QUALITY.md`, `LEARNING.md` | none planned | none (grep: 0 hits in both round-49 counters) | none | Not frozen |

## Frozen vs not frozen (proposed for the plan's `## Frozen paths`)

**Frozen (byte, at the single freeze commit), listed per claim:**
- Both: `plans/round-50-claims.md`.
- C1: `tools/round-50/c1-counter.py`, `tools/round-50/c1-run.sh` (and `c1-run.py` / `c1-controls.py` if added), `tools/round-50/carriers.json`, `tools/round-50/control-fixtures/c1/**`, `tools/round-41/sqfs-list.py`, `tools/round-41/fetch-vendor.py`, `tools/round-27/xpin-attribute.mjs`, and any other C1 carried input the port imports.
- C2: `tools/round-50/c2-record.py`, `tools/round-50/selftest-r49-c2.py`, `tools/round-50/control-fixtures/c2/**`.
- Round-49 (already frozen, unchanged): `tools/round-49/**`, `corpus/evidence/round-49/c2/{popper,sysexits,freebsd-sysexits}.html`.

**Not frozen (read at REV or written by a claim; each counter binds or discloses what it reads):** `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` (row-pinned as above), `SCORECARD.md`, `SKILL.md` (registry section), `LOG.md`, `corpus/lessons/*` (except the round-49 lesson pin proposed above), `corpus/knowledge/*`, `corpus/evidence/round-50/**`.

## Safe landing order (text only; tools are frozen before any of this)

1. C1: knowledge entry and its `used-by` targets first; then the PROVINCE section and frontier line; README Knowledge and Coverage-map rows; S150 and S151 rows; S112/S114 re-open; search-log entry tagged `round 50 C1`.
2. C2 (one writer for SCORECARD `## Owned axes` and the SKILL registry): `corpus/lessons/round-50.md` (exists before any row cites it); S152–S154 rows; search-log entry tagged `round 50 C2`; SKILL registry rows (B9), including C1 instrument rows; SCORECARD `## Owned axes` coverage (B1, computed at REV after step 1) and calibration (B2) rows; `## Record corrections — round 50` as its own heading.
3. L1: freeze-hash and landing lines in LOG.md; round-50 SCORECARD section last.
4. Then run the frozen C1 and C2 counters at the landing REV. `c2-mismatch.py` for round 49 at the round-50 REV is expected to report A8 (F2). The round-50 record must state that as a known consequence of a frozen counter, not as a record error.

## Freeze-blocking items (ranked)

| # | item | evidence | fix before freeze |
|---|---|---|---|
| 1 | C1 port `frozen_drift` misses merge-commit edits and names unrelated paths | F8; `C1CounterPort/.../c1-counter.py:1199-1200` | add `-m --diff-merges=first-parent --name-status`, `core.quotePath=false`, pathspec = the C1 frozen list; keep the blob backstop |
| 2 | Round-49 A8 flips on any registry row added after base | F2 | decide and write into the round-50 record: round-49 counter red at round-50 REV by design; do not patch round-49 |
| 3 | B1 reads a C1 product; Owned-axes coverage row is double-written; B1 is red at base | F11; matrix | B1 counts base (139) plus a separate C1 mapping check; C2 is the single writer of that row |
| 4 | B9 scope includes C1's rows; two registry-like tables in SKILL.md | F9, F10 | B9 scope = `tools/round-49/**` plus `tools/round-50/c2-*`; single writer; name the section by its exact heading |
| 5 | ID reservation absent from the plan text (no S150–S154 anywhere in `round-50-claims.md`); the Frontier step names three source families, the prompt names two new rows | `grep -o 'S1[5-9][0-9]'` on the draft: 0 hits | reserve S150–S151 (C1) and S152–S154 (C2) in the plan; each counter asserts its IDs |
| 6 | Whole-directory freeze of `tools/round-50/` couples the walks | matrix | per-claim frozen lists (above) |
| 7 | Search-log matchers are prefix tests; round-50 tags could collide | F12 | distinct claim tags; C2 matcher requires its own tag |
| 8 | Landing order vs validator E11 | F5 | knowledge entry, lesson and `used-by` targets land before the rows that cite them |
| 9 | C2 battery do-nothing reads names and content of C1 landing paths (round-49 F3), violating the plan sentence unless restricted | round-49 `ConnSeparability` F3 | restrict the restore set to C2-read paths, or amend the sentence (before freeze only) |
| 10 | B11 reads the round-49 lesson at REV while `corpus/lessons/*` is unfrozen | matrix | pin the base blob or disclose |
| 11 | E04 correction-row URL reuse: exempt for rejected originals (tested) or `supersedes` in teaches (code read; not isolated against a `mined` original) | F7 | write C2 correction rows with `supersedes S###` in teaches; do not rely on the rejected exemption |

## Disclosures

- Measured: F1–F5, F7 (rejected-original branch), F8, F9–F14. Read-only: F10–F13, F15, F16.
- `[INFERENCE]`: C1 is unaffected by C2 rows S152–S154 because C1 reads only its own IDs and `used-by` targets (the C1 counter is not yet written; round-49 `ConnSeparability` row 4 measured the analogue for round 49).
- `[INFERENCE]`: `corpus/README.md` will map the new entry stem (the C1 binding requires it).
- The census validator's `--file` mode is not a valid check of `used-by` (F6); the `--root` form was used.
- Not measured: round-50 C1 and C2 counters, REA reruns, controls, data runs.

## Tools and installs

No tool was installed, upgraded or removed. The host guard was read (`/home/vgpnk/.omp/agent/RULES.md`); no pacman transaction was run. `disk-guard.sh status` was run before the first pass (no action needed; `/fast/scratch/hyaku` 555G free).

## Artifacts

- `.ufo/waves/round-50/w1/ConnCrossClaim/conflict-matrix.tsv`: full matrix (path × writer × reader × verified flip × freeze disposition × landing order).
- `.ufo/waves/round-50/w1/ConnCrossClaim/receipts/`: c2 runs (base, overlay A, overlay B), validator runs (base, overlay A, dup-URL and teaches variants, `--file` form), merge probe SHA, counter and validator sha256 pins, `SHA256SUMS`.
- `.ufo/waves/round-50/w1/ConnCrossClaim/census-fixtures/sources-census.sh`: copy of the fleet validator (sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`), for reproduction.
