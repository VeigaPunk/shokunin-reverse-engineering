# CriticSeparability: causal separability of R29-C1 and R29-C2 (round 29, wave 1)

Seat: KaidokuR29.CriticSeparability (critic, leaf). Lane read-only; every Git write was made in the sandbox clone
`/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticSeparability/clone`, with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset.
Lane commits examined: base `bacbe9cc`, freeze `dbd87cfa`, hygiene `7431096b`, data `4fcea978`, tip `18be864a`.
No network, no REA, no installs.

## Verdict

**Holds, with two fixable provenance defects and one unenforced boundary.**

- **Mechanical separability: holds** (observation). Neither counter reads the other claim's evidence directory, entry or
  SOURCES row. Each counter exits 0 on a sandbox revision where the other claim's data, entry, SOURCES row and Gate line
  are absent. Each still exits 0 when the other claim's frozen inputs are deleted as well.
- **Defect 1, circular attribution (fixable).** Each entry attributes the same fact ("0 of 199 entries filtered" on the
  152 shared selectors) to the *other* claim. No counter outputs that number. The fact is true in both databases.
- **Defect 2, wrong carrier in the C2 entry (fixable).** `factory()` (`0xc45a0155`) is in carrier n06 (UniV2Pair), not n08.
- **Unenforced boundary (a tradeoff for the judge, not a reject).** The claims.json `limits` text "C2 counts only its own
  fetch, never R29-C1's lookups" is enforced only by path. The C2 counter accepts R29-C1's lookup files and manifest
  entries copied into `c2/db` (exit 0). The off-lane collector logs indicate that the fetches really were separate (inference).

## Attack 1: does either counter read the other's data or entry?

**Static reading of the code (observation).** The path constants are disjoint except for the shared SOURCES and lesson files:

- `tools/round-29/c1-fresh-naming.py:56` `EVDIR = "corpus/evidence/round-29/c1"`, `:57` `ENTRY = ...r29-evm-fresh-selector-naming.md`,
  `:62` `CLAIM = {"row": "S088"}`, pins `:67-71` (resolver, c1/carriers.tsv, c1/heldout.tsv only).
- `tools/round-29/c2-filtered-unseen.py:53` `EVDIR = "corpus/evidence/round-29/c2"`, `:54` `ENTRY = ...r29-openchain-filtered-unseen.md`,
  `:59` `CLAIM = {"row": "S087"}`, pins `:61-64` (c2/selectors.tsv, c2/canonical-signatures.json only).
- Every C1 read goes through `EVDIR`, `RESOLVER`, `ENTRY`, `SOURCES` or `LESSON`: `:160`, `:186`, `:222`, `:234`, `:256-259`,
  `:323`, `:338-340`, `:357-362`, `:377`. Every C2 read likewise: `:120`, `:134-135`, `:150-153`, `:164`.
- The shared files are read per row only. In C1, `:345-351` requires only `CLAIM["row"]` (S088) to be cited, new since
  the base, mined, opened 2026-10-22 and in ## Gate. In C2, `:141-146` applies the same test to S087. Neither counter
  requires the other row to exist.

Command (2026-10-22T20:22:03Z, exit 0, inner greps exit 1 = no match):
`git show 18be864a:tools/round-29/c1-fresh-naming.py | grep -nE 'round-29/c2|R29-C2|S087|filtered-unseen|c2/'` → `rc=1`;
`git show 18be864a:tools/round-29/c2-filtered-unseen.py | grep -nE 'round-29/c1|R29-C1|S088|fresh-selector|c1/|heldout|tally'` → `rc=1`.

**Dynamic test (observation).** Script `build-isolated.sh` starts at `7431096b` (freeze plus hygiene, no data). For each
claim it checks out only that claim's evidence directory and entry, plus SOURCES and the lesson with the other claim's row
removed from the table and from ## Gate. Each counter then runs with `--base bacbe9cc`. Output is in `isolated-run.txt`.

| sandbox revision | contents | C1 counter | C2 counter |
|---|---|---|---|
| tip `18be864a` | both claims | `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` exit=0 (20:23:05Z) | `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1` exit=0 (20:23:06Z) |
| c1-only `5d2d8beb` | no c2/db, no C2 entry, S087 absent from SOURCES and lesson | same line as tip, exit=0 (20:23:08Z) | `responses_complete=0/178 ... entry_ok=0` exit=1 |
| c2-only `2b24a605` | no c1 data, no C1 entry, S088 absent | `runs_ok=0/16 rows_complete=0/152 tally_equal=0 entry_ok=0` exit=1 | same line as tip, exit=0 (20:23:09Z) |
| c1-only-purged `befcc269` | as c1-only, plus all of `corpus/evidence/round-29/c2` removed | exit=0, same line as tip (20:23:10Z) | `PIN pinned input absent: corpus/evidence/round-29/c2/selectors.tsv` exit=2 |
| c2-only-purged `815fa871` | as c2-only, plus all of `corpus/evidence/round-29/c1` removed | `PIN pinned input absent: corpus/evidence/round-29/c1/carriers.tsv` exit=2 | exit=0, same line as tip (20:23:11Z) |

Conclusion (observation): each claim verifies with the other absent, and neither counter passes vacuously on the other's
data. Selftests in the sandbox at 2026-10-22T20:24:45Z: C1 `selftest cases=22 failures=0` exit=0; C2
`selftest cases=19 failures=0` exit=0.

## Attack 2: shared freeze and shared selectors

**Input dependence is fixed at freeze, not live (observation).** `tools/round-29/select-heldout.py:72-85` writes both
`c1/heldout.tsv` and `c2/selectors.tsv` in one run. The c1 set of selectors.tsv is the held-out list minus canonical keys
(`:79`). C2 then pins its own copy by sha256 (`c2-filtered-unseen.py:61-64`) and never opens heldout.tsv. A later
revision of C1's held-out list cannot change C2's input; the pin would refuse it (exit 2). Receipt
`.ufo/waves/round-29/before/select-heldout.txt:30`: `"c1_heldout": 152, ... "c2_selectors": 178, "c1_heldout_that_are_canonical": 0`.

**The 152 shared responses are byte-identical; their manifests differ (observation).** `analyze-shared.py` at
`4fcea978` (2026-10-22T20:23:47Z, exit 0): `"c1": {"selectors": 152, "entries": 199, "pred_true": 0, "obs_true": 0, ...
"c1_bytes_equal": 152, "c1_utc_equal": 1}`. The C2 manifest spans 20:03:21Z–20:06:17Z; the C1 openchain lookups span
20:03:40Z–20:08:52Z.

**C2's separation and both-branch target do not depend on the shared set (observation).** `analyze-alternatives.py`
at `4fcea978` (2026-10-22T20:25:22Z, exit 0) on the 26 canonical keys alone:
`"canonical": {"entries": 53, "altA_not_hvc_mismatches": 15, "altB_nonfirst_mismatches": 7}`. Both alternatives named in
claims.json R29-C2 `separation` (line 61) are refuted without the c1 set. On the canonical set alone, predicted_true=38 and
predicted_false=15, so both branches hold. The c1 set adds 199 of the 252 entries. All 199 are predicted false by
construction, because none of these selectors is a canonical key. Inference: C2's headline "0 of 252" is 79% trivial-branch
entries whose bytes equal C1's. The entry's per-set table discloses this, so it is a tradeoff, not a defect.

**Joint freeze, one ledger verdict (observation; tradeoff).** `tools/round-29/freeze-gate.py:97-138` (`audit_one`) gives
one verdict per claims file. `corpus/claim-freezes.tsv:17` and `corpus/claim-freezes-v2.tsv:20` each hold a single
`round-29 FLAGGED INSTRUMENT_UNPINNED` row for both claims. A finding against one claim's instrument would flag the shared
row; the counters themselves stay separable.

## Counterexample: C2 accepts R29-C1's lookups as its own fetch

`copy-attack.sh 2b24a605` (2026-10-22T20:23:48Z, exit 0) starts from the c2-only sandbox revision. It replaces the 152
c1-set manifest entries in `c2/db/manifest.json` with R29-C1's entries from `c1/db/manifest.json`, and copies R29-C1's
files over C2's. Output: `replaced 152 c2 manifest entries and files with R29-C1's`, `file bytes changed vs c2-only: 1`
(only manifest.json, because the bodies are identical), and then from the C2 counter:
`responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`, exit=0.

Why it passes: `c2-filtered-unseen.py:60` uses the same URL string as `c1-fresh-naming.py:228-229`. The checks at
`:168-179` (url, status, utc after the counter commit, sha256, first commit after the counter) are all satisfied by
R29-C1's entries. Nothing records which collector produced a file. Impact: the claims.json R29-C2 `limits` line
"C2 counts only its own fetch, never R29-C1's lookups" is enforced by directory only.

**Mitigating evidence (observation; separate fetches are an inference).** The off-lane L1 logs, which are not committed:

- `/fast/scratch/hyaku/kaidoku-r29/l1/tmp/c2-fetch.log`: sha256 `5f7730b1725315f7872d2ad33f6ffc6c7afec0f2847deeeb5f590ae8340e14ed`,
  178 lines, birth 17:03:21.168 -0300 (20:03:21Z), mtime 20:06:17.028Z, first line `01ffc9a7 200 1`.
- `/fast/scratch/hyaku/kaidoku-r29/l1/tmp/c1-lookups.log`: sha256 `cc72991c2559aa0886c96aa60c917d835439bf486a710e7b0cab9459b041cee3`,
  152 lines, birth 20:03:38.673Z, mtime 20:08:52.764Z.

These spans match each manifest's utc range, and 151 of 152 manifest timestamps differ. Command: `stat`/`sha256sum`
(2026-10-22T20:24:13Z, exit 0).

## Defect 1: circular attribution of "0 of 199"

- C1 entry `corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md:68-69` (at `18be864a`):
  "`filtered: false` (S084, S087; R29-C2 observed 0 of 199 entries on these selectors marked filtered)".
  Its source: line (`:1`) also cites "S084/S087 for the `filtered` flag".
- C2 entry `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md:65`:
  "The round-25 naming rules' filter step is inert for any selector outside the 36 keys (R29-C1:
  0 of 199 entries filtered on its 152 rows)".
- No counter outputs this figure. The C1 counter never counts `filtered` (`rule_outputs` `:141-156` only consumes it).
  The C2 counter prints totals only (`:216-218`).
- The fact itself is true in each claim's own bytes. `analyze-shared.py` gives `from c1/db only: selectors=152 entries=199
  filtered_true=0`, and the c2/db c1 set gives `entries 199, obs_true 0` (observation).

Impact: if either claim were retracted, the other entry would cite a nonexistent observation (false provenance; the
coverage and depth axes keep their text). This is not a counter failure.

## Defect 2: wrong carrier for `factory()` in the C2 entry

C2 entry `:60`: "`factory()`, the function R29-C1 carrier n08 holds under that selector". In
`corpus/evidence/round-29/c1/carriers.tsv:9`, n08 is `UniV2Factory`; `factory()` appears only in
`compiled/UniV2Pair.abi.json` (carrier n06, `carriers.tsv:7`; `src/UniV2Pair.sol:17` `function factory() external`).
`before/select-heldout.txt:25`: `EXCLUDE c45a0155 factory() name_seen`. Command `git show 18be864a:...` greps,
2026-10-22T20:25:04Z, exit 0. Impact: a false reference to C1's frozen inputs inside C2's entry. No counter checks it.

## Smallest safe corrections (for the L1; this seat edits nothing)

1. Both entries should cite their own bytes for "0 of 199".
   - C1 entry `:68-69`: "0 of the 199 openchain entries in `corpus/evidence/round-29/c1/db` are filtered (L1 reading, not a
     counter output)".
   - C2 entry `:65`: "(c1 set above: 0 of 199)".
2. C2 entry `:60`: change "carrier n08" to "carrier n06 (UniV2Pair)".
3. Make the boundary honest without changing any counter:
   - Reword the R29-C2 limits in the entry to say "C2 counts only files under `c2/db`; the counter cannot tell a copy of
     R29-C1's lookups from its own fetch".
   - Commit the two collector logs with the sha256 values above as fetch receipts.
   - An `instrument_supersessions` change to a frozen counter is not needed and would cost the freeze.

## Impacted axes

- C1, coverage: not affected by the counter. Its entry prose has a provenance defect (Defect 1).
- C2, depth: the counter verdict stands and its separation holds on the canonical set alone. Its entry prose has
  Defects 1 and 2, and the fetch-provenance boundary is unenforced.

## Seat artifacts (`/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticSeparability/`)

| file | sha256 |
|---|---|
| build-isolated.sh | `7ba4d3ed073a51bd3fb5d7ff2940e037b897827173645ffe25f93b359e5a9d91` |
| isolated-run.txt | `62c3dcee06414d42406e5cf19f007a6af1a8a1cbf3418d4f23369d2205d53206` |
| analyze-shared.py | `84479f8464cd23cc19020174f344d2b393237aa3134ea5a3787fabff565d0d92` |
| analyze-shared.txt | `e86cdfa920b88dae7048a5ecf3fd13f6a75c224590a7f9a872ad1018ee7a2706` |
| copy-attack.sh | `94c5b87fda25f61cc1a6858bb26e26bfa6adddd44f8e1e3693862038e17e1ea6` |
| copy-attack.txt | `b18cbf905c4292dd8889d7869e7ed31efad7d18ffabc8ea1721fc57e8b38802f` |
| analyze-alternatives.py | `7b833e79494d4acf5057cd68629efe12e798554c475a85dfdac68a796c2f28c5` |
| analyze-alternatives.txt | `25f65784aba9bb42d95aca410781b2063b4bd55d963bb10c6fb40b24dac125f2` |

Sandbox clone `clone/` holds these revisions: c1-only `5d2d8beb`, c2-only `2b24a605`, c1-only-purged `befcc269`,
c2-only-purged `815fa871` and copy-attack `4cd3f9d4`. `tmp/c1db/` holds the R29-C1 db extracted with `git archive`.
Installs: none.
