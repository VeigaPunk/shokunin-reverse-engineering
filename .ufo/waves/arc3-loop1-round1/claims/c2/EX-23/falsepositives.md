# EX-23 — false-positive census: honest in-flight edits vs the citation-drift frozen-run guard

Seat EX-23 | chain c2 | role executor | 2026-10-19 | HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`

C2 frozen claim under test (`claims-frozen.md:40-54`): *pin the sha256 of
`pointer-table.json` in `expected.json`; a tampered or absent table yields the
declared preflight could-not-evaluate class (exit 2), never silent findings.*

**Status of the guard under test.** EX-16's real-target write had **not landed**
at measurement time (poll log `harness/`; no `claims/c2/EX-16/`; gate file
mtimes pre-wave). The guard bytes measured here are this seat's **reference
implementation of the declared semantics**, built from the HEAD probe bytes
(sha256 `3067621a…`, byte-identical copy at `harness/head-citation-drift-probe.py`).
If EX-16 lands a different id/semantics, every row below re-runs with one
command (`python3 harness/census.py`, exit 0, results in
`harness/census-results.json`).

## 0. Method

Three probe variants are generated mechanically from the HEAD bytes:

| variant | guard block | id in `Findings.verdict()` CNE tuple | selftest per-case pin |
|---|---|---|---|
| `guardA` | yes | **no** (the "forgot the registry" variant) | no |
| `guardB` | yes | yes | no |
| `guardC` | yes | yes | yes (fixture run pins its own table) |

Guard block semantics (faithful to the declaration, in the file's own idiom):
read the bytes **at `--table`** (whatever table is actually loaded — closes
RV-6's attack 6 `--table` bypass), compare against
`expected["frozen_run"]["table_sha256"]`; mismatch → `pointer_table_tampered`
(detail carries **actual and pinned digest**); no pin → `unpinned_legacy`;
absent/unreadable/dir/binary → the existing `pointer_table_unreadable`. All four
ids are CNE classes. Each scenario is run under **probe semantics (default)**
and **`--strict`**; exit code, finding lines, verdict line and traceback
presence are captured.

## 1. Honest in-flight edits enumerated (the census proper)

Each row is a legitimate edit an operator makes mid-round, with its real
history instance where one exists. `guardB` result is the declared-class test.

| # | honest edit | real-history instance | guardB probe | guardB strict | finding id | clear string? |
|---|---|---|---|---|---|---|
| H1 | probe-table re-key (`line` 59→60 after a shift) | 6bc4c29 "census SCOPE re-key + probe re-pin coupled"; 110cc08 "log1005 pin to 1012" | **2** | **2** | `pointer_table_tampered` | yes |
| H2 | in-round needle fix (`must_match`) | 02c45d5 `readme175-sc1217` correction | 2 | 2 | `pointer_table_tampered` | yes |
| H3 | entry addition (13→31 extension) | dbae324 | 2 | 2 | `pointer_table_tampered` | yes |
| H4 | entry retirement (dead pointer removed) | r5 dispositions retiring rows | 2 | 2 | `pointer_table_tampered` | yes |
| H5 | quoted-array append (append-only record) | 085ca3c quoted LOG pins | 2 | 2 | `pointer_table_tampered` | yes |
| H6 | note-only edit (semantics unchanged) | note fields edited during re-keys | 2 | 2 | `pointer_table_tampered` | yes |
| H7 | exempt-list edit | exempt block authored/extended (3 rows at HEAD) | 2 | 2 | `pointer_table_tampered` | yes |
| H8 | pure reformat (indent 2→4) | editor auto-format class | 2 | 2 | `pointer_table_tampered` | yes |
| H9 | receipt-anchored update (new receipt stamp) | `sc59-receipt-stamp`, `prov18-stamp-named` re-anchoring (CR4's census precedent, `SCORECARD.md:815`) | 2 | 2 | `pointer_table_tampered` | yes |
| H10 | `_doc` extension note | the table's own `_doc` records each extension | 2 | 2 | `pointer_table_tampered` | yes |
| H11 | cross-revision replay (old table bytes vs current pin) | r5 audit's `git archive` re-derivations at cited commits | 2 | 2 | `pointer_table_tampered` | yes |

Verbatim representative (H1, `guardB`):

```
CITATION_DRIFT: pointer_table_tampered entry=pointer-table.json sha256 4a5d96cc4c5ed5a02a456f90b48ffee5bf792cead01bbb7dafba2173de9789be != pinned 738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

**Verdict: 11/11 honest edits land in the declared exit-2 class, both
semantics, with a clear finding string and no traceback.** The guard cannot
distinguish intent (by construction: the C2-tamper control produces the same
class and the same string shape) — exit 2 is the correct non-accusatory class;
an exit-1 class would false-fail every honest edit.

### Finding-string clarity, criterion by criterion (guardB)

| criterion | measured |
|---|---|
| stable typed finding id (not `internal_error`, not a traceback) | yes, `pointer_table_tampered` / `unpinned_legacy` / `pointer_table_unreadable` |
| names the graded artifact | yes (`entry=pointer-table.json`; full path in the `CITATION_DRIFT_TABLE:` header) |
| prints actual **and** pinned digest (mismatch class) | yes |
| verdict line states label + count + exit | yes, `could-not-evaluate findings=1 exit=2` |
| exit 2 in **both** semantics | yes (guardB) |
| remediation hint in the detail | **no** — proposed (optional): append `(re-pin expected.json frozen_run.table_sha256 in the same commit if this edit is yours)`; the operator currently has to know the re-pin ritual |

## 2. Defects measured (both are landing conditions, not opinions)

**D1 — the CNE registration is load-bearing.** `verdict()` has a hardcoded CNE
tuple (`citation-drift-probe.py:72-75`). A new finding id that is not added
there returns `CLEAN` in probe semantics and `FAILED` under `--strict`:

| | probe | strict |
|---|---|---|
| `guardA` (id unregistered), all H1-H11 | `reported findings=1 exit=0` — declared class NOT achieved | `failed findings=1 exit=1` — **false failure on an honest edit** |
| `guardB` (id registered) | `could-not-evaluate findings=1 exit=2` | `could-not-evaluate findings=1 exit=2` |

**D2 — the guard breaks the probe's own selftest unless the fixture run pins
its table.** With `guardB`, 9 of the 11 existing cases fail (`exit=2` where
0/1 is expected) because the selftest's per-case `expected.json` is
`{"snapshots": …}` with no `frozen_run`:

```
CITATION_DRIFT_SELFTEST: FAILED cases=11 passed=2 failed=9 exit=1
```

`guardC` (the selftest writes the sha256 of the fixture table it just built
into that case's expected, and the two new cases deliberately break the pin /
omit the file) reaches the claim's target:

```
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

The recipe is in `guard-recipe.patch.md`; the two new case rows measured are
`table_tampered` (exit 2, `pointer_table_tampered`) and `table_absent`
(exit 2, `pointer_table_unreadable`). 6/6 repetitions per variant are
deterministic (`harness/selftest-flake.log`); one transient traceback was seen
once in ~10 earlier selftest runs under wave load and did not reproduce in 6
dedicated reps — recorded, not claimed either way.

## 3. Workflow-impact classes (adjacent false-positive surface)

**W1 — the lane's established scratch-table harness shape flips to exit 2.**
EX-25 and RV-6 grade scratch tables with the *real* `expected.json`:

```
python3 <probe> --root . --rev HEAD --table claims/c2/EX-25/scratch/table-tampered.json \
        --expected .ufo/gates/citation-drift/expected.json
```
- today (unguarded): `citation_dead … ; reported findings=1 exit=0`
- with the guard, pre-pin expected: `unpinned_legacy … exit=2`
- with the guard, pinned expected: `pointer_table_tampered … exit=2`

By the declared semantics this is correct (a different table is not the pinned
one), but every such harness must now carry its **own** `expected.json` with the
pin of the table it grades — exactly how this seat's harness does it. Three c2
seats run this shape this round; the parent should name it in the round record.

**W2 — pre-pin revisions read `unpinned_legacy` exit 2.** Any revision whose
`expected.json` lacks the pin (including current HEAD, and any extracted
archive of a pre-pin commit) yields exit 2 for *every* run. Consequence: the
guard code and the pin **must land in the same commit**, else HEAD goes
permanently CNE. (Measured: C5 control.)

**W3 — the pin's referent is the landing-commit table, not the frozen
revision's.** `frozen_run.revision` is `679af5d…`, where the table did not
exist: `git show 679af5d:.ufo/gates/citation-drift/pointer-table.json` → `fatal:
path … exists on disk, but not in '679af5d…'`; `git diff --stat 679af5d HEAD`
→ 331 insertions (file added after). Pinning the frozen revision's digest would
be impossible; pinning the landing-commit digest is the only coherent reading
and matches "findings = 0 at HEAD". RV-6's attack 10 independently confirms the
same fact.

## 4. Controls (all as declared)

| control | guardB probe/strict | finding |
|---|---|---|
| C0 clean tree, pin matches | 0 / 0 | none (`findings=0`) |
| C1 honest edit + same-commit re-pin | 0 / 0 | none — the intended workflow clears |
| C2 semantic tamper, no re-pin | 2 / 2 | `pointer_table_tampered` (byte-indistinguishable from H1) |
| C3 table absent | 2 / 2 | `pointer_table_unreadable` (`[Errno 2] …`) |
| C4 table invalid JSON | 2 / 2 | `pointer_table_unreadable` |
| C5 expected.json without pin | 2 / 2 | `unpinned_legacy` |
| C6 expected.json absent | 2 / 2 | `pointer_table_unreadable` + `unpinned_legacy` (2 findings) |
| C7 pin malformed (`deadbeef`) | 2 / 2 | `pointer_table_tampered` (`… != pinned deadbeef`) |
| C8 `--table` is a directory | 2 / 2 | `pointer_table_unreadable` (`[Errno 21] Is a directory`) |
| C9 table bytes not UTF-8 | 2 / 2 | `pointer_table_unreadable` (`'utf-8' codec …`) |
| C10 pin matches but bytes are invalid JSON | 2 / 2 | `pointer_table_unreadable` — the pre-existing class still fires |

No bare crash on any path: zero tracebacks across 84 runs (21 scenarios × 2
variants × 2 semantics), including dir/binary/malformed/absent inputs.

## 5. Attacks / refutations attempted

1. **"Honest re-key is distinguishable from a tamper."** REFUTED — C2 and H1
   produce identical classes and string shapes. The guard's exit 2 is the right
   class precisely because it does not accuse; the operator dispositions by
   comparing the actual digest to their own edit.
2. **"The guard can be bypassed by passing a custom `--table`."** REFUTED for
   the pin class — the guard hashes the file actually loaded. (RV-6 attack 6
   named this bypass for the *unguarded* probe; the reference implementation
   closes it.)
3. **"A semantic no-op write trips the guard."** REFUTED — writing the same
   value leaves the digest unchanged (H2's first harness attempt was such a
   no-op and did not trip; recorded as a harness bug, then re-measured with a
   real edit).
4. **"The guard yields silent findings."** PARTIALLY CONFIRMED for the
   unregistered-id variant: the finding line still prints, but probe exit is 0
   and strict exit is 1 — the declared class fails and strict false-fails.
   REFUTED for the registered variant (exit 2 both modes).
5. **"The guard can be tripped by the probe's own fixtures."** CONFIRMED (D2) —
   and the per-case-pin recipe fixes it (13/13 exit 0).
6. **"Pin/mismatch classes can crash on hostile inputs."** REFUTED — see §4;
   every hostile input lands on a typed CNE finding.
7. **Residual, named not weaponized: TOCTOU.** The reference block hashes
   `open(table_path,"rb").read()` and the existing code then re-reads the file
   with `json.load(open(table_path))`; a swap between the two reads would grade
   bytes other than the hashed ones. Cheap hardening: parse the bytes that were
   hashed (`table = json.loads(table_bytes)`), which also removes the second
   read. Microsecond window, honest-operator threat model — recorded for the
   implementer.

## 6. Before→after measurement (chain C2's claim)

| | before (HEAD `e845c2b`, measured) | after (reference recipe, measured) |
|---|---|---|
| selftest | `CLEAN cases=11 passed=11 failed=0 exit=0` (6/6 reps) | `CLEAN cases=13 passed=13 failed=0 exit=0` (6/6 reps) |
| table digest pinned in expected.json | none (keys `_doc, frozen_run, snapshots, selftest`; EX-25's `before-digest-check.txt` → `NO-PIN`) | `frozen_run.table_sha256 = 738b3a56…` |
| honest in-flight edit (any of H1-H11) | graded normally (e.g. scratch table → `citation_dead … exit=0`) | `pointer_table_tampered … exit=2` (both semantics) |
| tampered table, no re-pin | `reported findings=1 exit=0` (silent suppression, RV-6 attack 4) | `could-not-evaluate exit=2` |
| clean tree | `findings=0 exit=0` | `findings=0 exit=0` (unchanged) |
| coupled re-pin | n/a | `findings=0 exit=0` (workflow preserved) |

## 7. Blockers / gaps

- **EX-16's implementation did not land in this seat's window.** All rows test
  the declared semantics via the reference implementation, not EX-16's bytes.
  If EX-16 lands different ids or placement, re-run `harness/census.py` (one
  command, exit 0) and diff `census-results.json`.
- `/tmp` is quota-blocked this wave (`echo > /tmp/... ` → `Disk quota
  exceeded`); scratch was relocated to `~/.cache/kaidoku-scratch/ex23` (deleted
  at close) and the harness copied into this seat's artifact dir. Same hazard
  RV-6 recorded.
- No write was made to `.ufo/gates/` by this seat: the guard bytes exist only as
  patch text (`guard-recipe.patch.md`) and as harness variants under this seat
  dir.

## 8. Evidence index

Harness (all under `claims/c2/EX-23/harness/`): `census.py` (318 lines,
sha256 `d87cea3b99115165b12c7bd442ae7fa493d3721ad9b66d214f402b2f79414b97`,
delivered form, re-run in place), `selftest-proof.py` (`ed598cf8…`),
`selftest-flake.py` (`998eec53…`), `name-alignment.py` (`5ac09959…`),
`head-citation-drift-probe.py` = HEAD probe
`3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f`,
`head-pointer-table.json` = `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`,
`head-expected.json` = `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33`,
`guardA/B/C.py` (generated variants), `guardP.py` (PL-2 naming),
`expected-13.json`, `guard-recipe.diff` (`ccea662a…`), `census-results.json`
(`61d74e57…`, 84-run matrix), `census-run-inplace.log`, `selftest-proof.log`,
`selftest-flake.log`, `name-alignment.log`.

Cross-checks used: `git show 265e1aa:…pointer-table.json | sha256sum` →
`edaa4e59…` (H11's old-table digest, exact match); EX-25
`logs/before-digest-check.txt` (`NO-PIN`); RV-6 report §4 attacks 4/5/6/10
(convergent: silent-rc-0 class, `--table` bypass, frozen-rev predates the
table).

## 9. Name-alignment check (PL-2's planned naming)

PL-2's plan (`claims/c2/PL-2/plan.md:47-65`) lands a different pin key and
unpinned id than this seat's reference block: pin
`expected["pointer_table"]["sha256"]`, unpinned `pointer_table_unpinned` (new,
registered in the CNE tuple alongside the retained `unpinned_legacy`),
`pointer_table_tampered` and `pointer_table_unreadable` as here, and the same
per-case selftest pin. The census rows therefore re-ran under that naming
(`harness/name-alignment.py`, log `harness/name-alignment.log`):

| row | PL-2-naming probe | PL-2-naming strict |
|---|---|---|
| H1 honest re-key | 2 `pointer_table_tampered` | 2 `pointer_table_tampered` |
| C0 clean | 0 | 0 |
| C1 edit + coupled re-pin | 0 | 0 |
| C3 absent table | 2 `pointer_table_unreadable` | 2 `pointer_table_unreadable` |
| C5 no pin | 2 `pointer_table_unpinned` | 2 `pointer_table_unpinned` |
| C7 malformed pin (`deadbeef`) | 2 `pointer_table_unpinned` | 2 `pointer_table_unpinned` |

All census verdicts hold under either naming; only the pin-key lookup and the
unpinned id's spelling change. The D1 landing condition applies identically to
`pointer_table_unpinned` and `pointer_table_tampered`: an id absent from
`verdict()`'s CNE tuple silently degrades to probe-0 / strict-1. PL-2's patch
text registers both (its diff adds them to the tuple), so D1 is already
addressed in the plan of record; this census supplies the counterfactual
measurement and the honest-edit surface that the plan's own rows do not cover.

