# R40MutR39 — mutation probe of the round-39 counters/interpreter before the round-40 freeze

**VERDICT: DEFECTS FOUND** — 47 of 51 single-logic mutants survive both of their detectors
(`--selftest` + the second detector: held-out labels for the triage interpreter, a real verdict run
at REV `8b9634ed` / FREEZE `8fcda41c` for both counters). All 32 survivors that round-39 wave 2
reported replicate 1:1; the 19 mutants I add on the clauses the round-40 successors keep
(gap clause, oracle match, handler, evidence id, seed==freeze, table byte-identity, first-match
order, set equality) surface **15 genuine missing selftest cases, 6 of them probe-proven on
constructed fixtures where pristine and mutant disagree on the verdict**. The single most
dangerous finding: **the C1 counter's oracle-coverage clause (`oracle_hits == oracle_files`) —
the heart of "publishes every regular file of the frozen oracle" — is pinned by zero selftest
cases**; a mutant deleting the conjunct passes the full 33-case selftest and scores `met` on the
real lane. Per the seat rules these are coverage findings for the round-40 successors' selftests,
not license to change any contract; no lane byte was modified.

## 1. Scope and method

- Attacked artifacts (scratch copies; lane files never written): `tools/round-39/sqfs-triage.py`
  (sha256 `ef4a8a8b…beacf2`), `tools/round-39/c2-counter.py` (`775766d8…e7f0e41`),
  `tools/round-39/c1-counter.py` (`efb4b526…577a91`). All three are **byte-identical at the
  round-39 freeze `8fcda41c`, at REV `8b9634ed`, and in the worktree** (verified via
  `git show <rev>:<path> | sha256sum` in a `--shared` clone), so every mutant attacks the frozen
  bytes exactly.
- Baselines (all green, before any mutation):
  - `sqfs-triage.py --selftest` → exit 0, `cases=35 pass=35 fail=0`; labeling the 20 committed
    held-out envelopes (`corpus/evidence/round-39/c2/heldout/`, manifest seed
    `8fcda41c…`) with the worktree `SKILL.md` (`f08b91d0…3059f`) → **20/20 agree**.
  - `c2-counter.py --selftest` → exit 0, `cases=27 pass=27 fail=0`; verdict
    `--root <shared clone> --rev 8b9634ed… --freeze 8fcda41c…` → **exit 0, met 20/20,
    bindings_false []**.
  - `c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` → exit 0,
    `cases=33 green_ok=1 red_ok=32`; verdict at the same revs → **exit 0, met, 6/6 matched,
    carriers_unchanged true**.
- Detector per mutant (each mutant = one minimal string edit, uniqueness-audited: every old-string
  occurs exactly once in its file, T13 twice with replace-all):
  1. the mutant's own `--selftest` (exit ≠ 0 ⇒ killed);
  2. second detector per tool — triage: label the 20 held-out envelopes and count agreements with
     `manifest.json` labels (<20 or run-crash ⇒ killed); c2-counter: the verdict run at
     REV `8b9634ed8253653e7eb994aad9860a624e3b0366` / FREEZE
     `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` (exit/payload ≠ baseline ⇒ killed);
     c1-counter: the same verdict run with `--pkg65` (c1 was never mutated in round 39 — all c1
     findings are new this wave).
- Survivor triage: for the load-bearing survivors, **differential fixtures** — one fixture repo per
  probe (mktemp + `git init`, toplevel verified, `user.name=fx` identity inside the fixture only),
  pristine `measure()` vs mutant `measure()` on identical bytes. A disagreement proves "missing
  test", not "unkillable mutant".

## 2. Full mutant table (51)

`selftest` = mutant's own `--selftest` exit (0 = pass). `2nd` = second detector (labels 20/20 or
verdict identical). Verdict classes: SURVIVED (both clean), KILLED-SELFTEST, KILLED-LABELS,
KILLED-VERDICT. Exact old→new pairs: `artifacts/R40MutR39/results.json`; machine table:
`artifacts/R40MutR39/mutants.tsv`.

### sqfs-triage.py — round-39 wave-2 survivors, replicated (18/18 agree with R39W2TriageMutants)

| id | clause | mutation (one edit) | selftest | 2nd | verdict |
|----|--------|---------------------|----------|-----|---------|
| T01 | handler | H filter `startswith('squashfs')` → `'squash'` | 0 | 20/20 | SURVIVED |
| T02 | handler | drop the squashfs-prefix filter | 0 | 20/20 | SURVIVED |
| T03 | handler | case-insensitive H filter | 0 | 20/20 | SURVIVED |
| T04 | gap clause | drop `isinstance(kind, str)` guard on gap kinds | 0 | 20/20 | SURVIVED |
| T05 | gap clause | drop `isinstance(dep, str)` guard on dependencies | 0 | 20/20 | SURVIVED |
| T06 | handler/BE | BE scans `commands[:1]` only | 0 | 20/20 | SURVIVED |
| T07 | handler/BE | BE any-command → all-commands | 0 | 20/20 | SURVIVED |
| T08 | handler/BE | drop command dedup | 0 | 20/20 | SURVIVED |
| T09 | handler | only `sasquatch-v4be` counts (plain sasquatch dropped) | 0 | 20/20 | SURVIVED |
| T10 | handler | basename test → `'sasquatch' in token` | 0 | 20/20 | SURVIVED |
| T11 | handler | drop `rsplit('/', 1)` basename strip | 0 | 20/20 | SURVIVED |
| T12 | symlink | drop the diagnostics SR scan (raw_result only) | 0 | 20/20 | SURVIVED |
| T13 | symlink | typename equality → substring (both sites) | 0 | 20/20 | SURVIVED |
| T14 | files | `P = len(files)` → `bool(files)` | 0 | 20/20 | SURVIVED |
| T15 | files | `P += len(unpublished_entries)` | 0 | 20/20 | SURVIVED |
| T16 | set/fnmatch | `fnmatchcase` → `fnmatch` | 0 | 20/20 | SURVIVED |
| T17 | files boundary | `>0` rejects only P<0 (accepts P=0) | 0 | 20/20 | SURVIVED |
| T18 | files boundary | `0` rejects only P<0 (accepts P>0) | 0 | 20/20 | SURVIVED |

### sqfs-triage.py — new this wave (6)

| id | clause | mutation | selftest | 2nd | verdict |
|----|--------|----------|----------|-----|---------|
| N-T1 | gap clause | `gap_kinds.add(kind)` → `add(kind.lower())` | 0 | 20/20 | SURVIVED |
| N-T2 | set equality | `none` cell → matches everything (`return True`) | 0 | 20/20 | SURVIVED |
| N-T3 | set equality | exact set → nonempty intersection | 1 | — | **KILLED-SELFTEST** (exact-gap-miss, exact-gap-superset, exact-dep-superset) |
| N-T4 | handler | handler-pattern `any` → `all` | 0 | 20/20 | SURVIVED |
| N-T5 | first-match order | first match wins → last match wins | 1 | — | **KILLED-SELFTEST** (c_first_match_order) |

### c2-counter.py — round-39 wave-2 survivors, replicated at the round-39 tip (14/14 agree with R39W2C2Mutants)

| id | clause | mutation | selftest | verdict@8b9634ed | verdict class |
|----|--------|----------|----------|------------------|---------------|
| M01 | seed==freeze | drop `.lower()` on the manifest seed | 0 | met 20/20 | SURVIVED |
| M03 | seed==freeze | regen seed compared to *declared* seed | 0 | met 20/20 | SURVIVED (masked) |
| M04 | byte-identity | drop regen `label` conjunct | 0 | met 20/20 | SURVIVED |
| M05 | byte-identity | drop regen `arm` conjunct | 0 | met 20/20 | SURVIVED |
| M06 | byte-identity | `regen_sha == msha` → `regen_sha != ''` | 0 | met 20/20 | SURVIVED |
| M12 | first-add | drop `is_ancestor(freeze, ma)` | 0 | met 20/20 | SURVIVED |
| M13 | first-add | `manifest_before_envelopes` all→any | 0 | met 20/20 | SURVIVED |
| M16 | table byte-identity | drop both `is not None` guards | 0 | met 20/20 | SURVIVED (masked) |
| M21 | set equality | `per.get(k)` → `per.get(k, 2)` | 0 | met 20/20 | SURVIVED (masked) |
| M22 | met formula | `consistent = True` | 0 | met 20/20 | SURVIVED (vacuous) |
| M23 | met formula | `if not consistent:` → `if False:` | 0 | met 20/20 | SURVIVED (vacuous) |
| M27 | freeze descent | freeze-ancestor precheck → `if False:` | 0 | met 20/20 | SURVIVED |
| M28 | first-add | drop `--reverse` (latest add wins) | 0 | met 20/20 | SURVIVED |
| M29 | byte-identity | `carriers_regenerated` all→any | 0 | met 20/20 | SURVIVED |

### c2-counter.py — new this wave (4)

| id | clause | mutation | selftest | verdict | class |
|----|--------|----------|----------|---------|-------|
| N-M1 | seed==freeze | full-hash equality → `startswith(freeze[:8])` | 0 | met 20/20 | SURVIVED |
| N-M2 | table byte-identity | `blk_rev == blk_fr` → `.strip()` equality | 0 | met 20/20 | SURVIVED |
| N-M5 | domain guard (R39-CL1 successor) | `operation == 'extract_firmware'` → substring `in str(...)` | 0 | met 20/20 | SURVIVED |
| N-M6 | evidence digest | drop `and bool(msha)` guard | 0 | met 20/20 | SURVIVED (masked) |

### c1-counter.py — new this wave (10; c1 was never mutated in round 39)

| id | clause | mutation | selftest | verdict@8b9634ed | class |
|----|--------|----------|----------|------------------|-------|
| N-C1 | oracle match | `same_rel` drops the exact-equality alternative | 0 | met 6/6 | SURVIVED |
| N-C2 | oracle match | hit test `sha == fs and same_rel(...)` → `or` | 0 | met 6/6 | SURVIVED |
| N-C3 | handler | `HANDLER in chunk_handlers` → substring over tokens | 0 | met 6/6 | SURVIVED |
| N-C4 | evidence id | drop `startswith('ev_')` conjunct | 0 | met 6/6 | SURVIVED (equivalent) |
| N-C5 | evidence id | stored-vs-recomputed equality → case-insensitive | 0 | met 6/6 | SURVIVED |
| N-C6 | gap clause | drop the final `sorted(seen) != sorted(in_tree)` cardinality check | 1 | — | **KILLED-SELFTEST** ('materialised in-tree symlink', 'missing gap for an in-tree symlink') |
| N-C7 | gap clause | gap-kind whitelist widened to accept `extractor-failure` | 0 | met 6/6 | SURVIVED |
| N-C8 | first-add | drop `add != freeze` (receipt added at the freeze passes) | 1 | — | **KILLED-SELFTEST** ('receipt added at freeze') |
| N-C9 | oracle match | drop `oracle_hits == oracle_files` from the matched conjunction | 0 | met 6/6 | **SURVIVED — headline** |
| N-C10 | first-add | `first_add` returns earliest add instead of latest | 0 | met 6/6 | SURVIVED |

**Totals: 51 mutants — 47 SURVIVED, 4 KILLED-SELFTEST, 0 killed by the second detector alone.**
The second detector (held-out labels / real verdict) killed nothing that the selftest did not —
every kill came from `--selftest`.

## 3. Differential fixtures — survivors proven to be missing tests

Fixture repos built in scratch (`mktemp -d` + `git init`, toplevel asserted, `user.name=fx` inside
the fixture); pristine and mutant `measure()`/`classify()` run on identical bytes.
Full outputs: `artifacts/R40MutR39/probe-c1-results.json`, `probe-c2-results.json`,
`probe-t-results.json`.

### c1-counter (the round-40 C1 counter keeps every one of these clauses)

| probe | fixture (one defect on an otherwise green 6-carrier lane) | pristine | mutant | missing test |
|-------|-----------------------------------------------------------|----------|--------|--------------|
| N-C9 | K2 receipt omits one oracle file (`space name.txt`) | exit 1, K2 oracle-coverage deficit | **exit 0, met 6/6** | **No selftest case exercises a receipt that fails to publish an oracle file.** The oracle-coverage conjunct is the predicate's core and is pinned by nothing. Required case: drop one published file that an oracle row needs → not met. |
| N-C2 | K2 publishes `a/run.sh` with sha256 `f·64` (wrong sha, right path) | exit 1 | **exit 0, met** | The sha half of the oracle match is unpinned: a wrong-sha file at a matching path counts as a hit under the mutant. Required case: published path matches an oracle row but sha256 differs → oracle_hits < oracle_files → not met. |
| N-C3 | K6 chunk handler `xsquashfs_v4_bey` | exit 1, handler_ok false | **exit 0, met** | handler_ok is exact-token in pristine but nothing pins exactness. Required case: near-miss handler token must fail handler_ok. |
| N-C7 | K3 gap kind → `extractor-failure` **with** a relative_path matching an in-tree symlink | exit 1, gaps_ok false | **exit 0, met** | The existing 'extra gap kind' case uses `relative_path: None`, which the path check rejects regardless of kind — it masks the kind whitelist. Required case: a non-`unpublished-entry` gap kind carrying a valid in-tree relative_path → gaps_ok false. |
| N-C5 | K2 stored evidence id uppercased (`EV_…`) | exit 1, evidence_id_ok false | **exit 0, met** | Evidence-id equality is never exercised for case. Required case: stored id differing from the recomputed id in case only → evidence_id_ok false. |
| N-C10 | K2 receipt added at the freeze commit, deleted, re-added after the freeze | exit 1, K2 receipt_fresh false | **exit 0, met** | No fixture re-adds a receipt; `first_add`'s earliest-add semantics (git log newest-first, `lines[-1]`) is unpinned. Required case: receipt added at freeze → deleted → re-added must stay not-met. |
| N-C1 | K2 publishes a file at exactly the oracle rel (`a/run.sh`, no dir prefix) | exit 0, met | exit 1 (stricter) | False-negative direction: the equality branch of `same_rel` is load-bearing for green but unpinned. Required case: exact-path publication must still count as a hit (or the contract declares suffix-only and drops the branch). |

### c2-counter (the round-40 C2 counter keeps all of these)

| probe | fixture | pristine | mutant | missing test |
|-------|---------|----------|--------|--------------|
| P-N-M5 | H03 envelope operation `xextract_firmwarey` | exit 1, envelopes_valid false | **exit 0, met** | The domain guard (R39-CL1 successor clause) is pinned only against a full flip (`analyze`); a substring-relaxed operation passes. Required case: operation containing but not equal to `extract_firmware` → envelopes_valid false. |
| P-N-M1 | manifest seed = `freeze[:8] + 'a'·32` | exit 1, seed_matches_freeze false | **exit 0, met** | seed==freeze is never exercised beyond exact equality. Required case: a seed sharing the freeze's 8-char prefix must fail. |
| P-N-M2 | rev table = freeze table + one trailing space on the last row | exit 1, triage_table_identical false | **exit 0, met** | Byte-identity is never exercised for whitespace. Required case: a whitespace-only table edit must break `triage_table_identical`. |
| P-M06+M29 | H01 committed body = regen body + `X`, manifest sha = sha(committed), envelope digest consistent | exit 1, carriers_regenerated false | **M06 exit 0 met; M29 exit 0 met** | Byte-identical regeneration (`regen_sha == msha`) and the all-quantifier are both unpinned — the only regeneration fixture corrupts the committed file, which trips `carriers_committed` instead. Required case: committed bytes match the manifest sha but diverge from regeneration → carriers_regenerated false. |
| P-M04 | H05 committed label `clean`, envelope stub_class `clean`, regen label `dep-missing-be` | exit 1, carriers_regenerated false | **exit 0, met** | Regenerated label/arm drift vs the committed entry is invisible while the interpreter agrees with the committed entry. Required case: regen label ≠ committed label → carriers_regenerated false. |

### sqfs-triage (in-process classify differentials)

| probe | table + envelope | pristine | mutant | missing test |
|-------|------------------|----------|--------|--------------|
| N-T1 | row keyed `unpublished-entry`; envelope gap kind `Unpublished-Entry` | unclassified | **`dep`** | Gap kinds are matched case-exactly but nothing pins case. Required case: uppercase gap kind → unclassified. |
| N-T2 | two-row table, `none`-gapped row first; envelope G=`{unpublished-entry}` | `correct` (row 2) | **`early`** (row 1 swallows) | The `none` cell's rejecting semantics is unpinned when a `none` row precedes the matching row. Required case: none-celled row first + nonempty-G envelope → the later row must win. |
| N-T4 | row pattern `squashfs_v4_be`; envelope H=`[squashfs_v4_be, squashfs_v4_le]` | `be-only` | **unclassified** | No held-out envelope has two squashfs handlers (V1-style containers have both BE and LE members). Required case: multi-handler envelope vs an exact-handler row. |

## 4. Equivalent / masked survivors (no test can or needs to kill; proofs)

- **N-C4 (ev_ prefix drop):** `xpin-attribute.mjs:210` returns `` `ev_${digest}` `` unconditionally,
  so the recomputed id always starts with `ev_`; `stored == recomputed` then implies the prefix.
  Equivalent by construction.
- **N-M6 (digest `bool(msha)` guard):** the guard differs from pristine only when `msha == ''`;
  then `commit_ok = (committed_sha == '')` is false, `carriers_committed` is false, and `met` is
  false under both. Masked by a sibling binding.
- **M03:** under `seed_matches_freeze` (declared seed == freeze), "regen seed == declared seed" ⟺
  "regen seed == freeze". Masked by construction (the counter itself invokes the generator with
  `--seed freeze`).
- **M16:** differs only when the table is absent at both REV and freeze; then
  `triage_table_present` is false and `met` is false either way.
- **M21:** `per.get(k, 2) == 2` fails only for a declared class with zero carriers; then
  `n_equals_twice_classes` is false regardless. Masked by a sibling binding.
- **M22/M23 (consistency guard):** `met` and `recomputed` are the same expression over the same
  dict, so `consistent` is true by construction and the raise is unreachable;
  `met_target_consistent: true` in every receipt is guaranteed, not evidence. Same corollary and
  fix as R39W2C2 §5: make `recomputed` independent or drop the guard.
- **T14 (P→bool) / T15 (P += unpublished):** equivalent **under the v1 files-cell vocabulary**
  (`*`/`0`/`>0` consume only zero-vs-nonzero; `bool` is 0/1 and `+unpublished` only inflates a
  nonzero P). They become killable exactly when v2's `clean-empty` / `partial-body-failure` work
  introduces a count-sensitive cell — the required case is then: files=0 with one unpublished
  entry → P must remain 0 (T15), and an exact-count/`>1` cell must reject P=2-as-bool (T14).
- **T16 (`fnmatch` vs `fnmatchcase`):** `posixpath.normcase` is identity, so the two are
  behaviorally identical on Linux — platform-equivalent, not killable by any fixture on this host.
  If v2 wants case-exact handler patterns, keep `fnmatchcase` and say so in prose.
- **T17/T18 (files-boundary exclusions):** the exclusion directions are masked by rule order on
  every existing envelope. Required v2 case: place the `>0` row FIRST with a P=0 envelope (must
  fall through to a later row), and a `0` row first with P=1.

## 5. The selftest cases a round-40 successor must add (consolidated)

For **sqfs-triage-v2.py** (block 19 interpreter), in `--selftest`:
1. non-squashfs handler chunk (e.g. `cpio`) beside a squashfs chunk → H excludes it (kills T01/T02/T03);
2. non-string gap kind / dependency (123, None) → excluded from G/D (T04/T05);
3. two sasquatch commands, only the later with `-be` → BE `yes` (T06/T07); same command recorded
   twice → `commands` length 1 (T08);
4. path-prefixed `/usr/bin/sasquatch-v4be` counts; plain `sasquatch -be` counts; token
   `xsasquatchy` does not (T09/T10/T11);
5. MaliciousSymlinkRemoved only in diagnostics → SR `yes`; typename `MaliciousSymlinkRemovedX` → no (T12/T13);
6. files=0 with one unpublished entry → P stays 0; a count-sensitive cell (if v2 adds one) rejects bool/inflated P (T14/T15);
7. boundary rows placed FIRST: `>0` row vs P=0 envelope falls through; `0` row vs P=1 falls through (T17/T18);
8. uppercase gap kind → unclassified (N-T1); `none`-celled row before the matching row must not swallow (N-T2);
   two-squashfs-handler envelope vs an exact-handler row (N-T4).

For **the round-40 C2 counter**: uppercase-seeded green case (M01); regen label/arm drift with the
interpreter agreeing with the committed entry (M04/M05); committed bytes = manifest sha but ≠ regen
(R39W2C2's m06/m29 fixture — re-proven here) (M06/M29); manifest first-added on a non-descending
branch via merge plumbing (M12); mixed envelope ordering around the manifest commit (M13); held-out
file added → deleted → re-added (M28); orphan REV expecting exit 2 `freeze_not_ancestor_of_rev`
(M27); seed = freeze-prefix-but-not-freeze (N-M1); whitespace-only table edit (N-M2); operation
`xextract_firmwarey` (N-M5). Make `recomputed` independent or drop the consistency guard (M22/M23).

For **the round-40 C1 counter** (all new — c1 was never mutated before): receipt omitting one
oracle file → not met (**N-C9, the headline gap**); wrong-sha published file at a matching path →
not met (N-C2); near-miss handler token `xsquashfs_v4_bey` → handler_ok false (N-C3);
`extractor-failure` gap WITH a matching in-tree relative_path → gaps_ok false (N-C7); uppercase
stored evidence id → evidence_id_ok false (N-C5); receipt added at freeze → deleted → re-added →
not met (N-C10); exact-path oracle publication stays a hit or the contract declares suffix-only
(N-C1).

## 6. Which kept clauses have teeth today, and which do not

| clause family (round-40 keeps) | pinned today by | unpinned direction (survivors) |
|---|---|---|
| gap clause | exact singleton values, `none`/`*` cells (R39 kills), c1 per-gap path check (N-C6 killed) | str-guards (T04/T05), case (N-T1), kind whitelist vs path-masked extra kinds (N-C7), c1 cardinality is pinned only via the two named cases |
| oracle match | nothing in c1's selftest for coverage or sha (**N-C2, N-C9**) | everything except the happy path |
| handler | be/le discrimination + handler-`none` reject (R39 kills), c1 exact token vs LE (R39 kill) | filter precision (T01–T03), name forms (T09–T11), aggregation (T06–T08), c1 near-miss tokens (N-C3) |
| evidence id | stored≠recomputed red cases (R39 kills) | case (N-C5), ev_-prefix is implied (N-C4 equivalent) |
| seed==freeze | wrong-seed red case (R39 kill) | case-normalisation direction (M01), prefix-only (N-M1), regen-vs-declared (M03 masked) |
| table byte-identity | content edits at rev (R39 kill) | None-guards (M16 masked), whitespace (N-M2) |
| first-match order | triage selftest c_first_match_order (N-T5 killed) | c2/c1 first-add latest-vs-earliest (M28, N-C10) |
| set equality | exact hit/miss/superset selftest cases (N-T3 killed) | `none`→any under row order (N-T2), intersection direction unpinned beyond R39's two subset flips, case-insensitive per-class counting (M21 masked) |

## 7. Bounds, restoration, tooling

- **Restoration evidence:** lane `tools/round-39/{c1-counter,c2-counter,sqfs-triage}.py` and
  `SKILL.md` sha256 before and after the whole campaign identical (`artifacts/R40MutR39/restoration.txt`):
  `efb4b526…`, `775766d8…`, `ef4a8a8b…`, `f08b91d0…`. All mutants lived and died in
  `$S=/fast/scratch/hyaku/kaidoku-r40/R40MutR39` (removed at finish). No VCS mutation: lane git
  usage read-only (`clone --shared` into scratch, `show`/`cat-file`/`rev-parse`/`log` inside the
  counters); the only `git init`/commit calls are inside mktemp fixture repos with the toplevel
  assertion. Nothing written outside this report and `artifacts/R40MutR39/`.
- **Tooling:** nothing installed or upgraded (python3 stdlib, git, node v24.21.0 already present);
  no pacman transactions; sasquatch/unblob untouched and never run (no carrier was opened — this
  seat runs no REA/unblob at all).
- **Limits:** hand-picked mutant set (51) over the tasked clause families — not an exhaustive
  statement-level sweep. The verdict arm ran each counter mutant once at the single
  (REV `8b9634ed`, FREEZE `8fcda41c`) pair. Equivalent/masked classifications are proofs by
  reasoning over the code (no fixture can demonstrate them — that is the classification).
  [INFERENCE] Severity of the c1 oracle-coverage gap: highest, because R40-C1's rerun binding
  compares a *semantic projection* of a fresh run against the committed receipt — if the
  projection fields are fixed in the freeze the way P40-C1 drafts them, the rerun clause will
  cover publication; until then the oracle-coverage conjunct is the only publication gate, and it
  has no selftest pin.
