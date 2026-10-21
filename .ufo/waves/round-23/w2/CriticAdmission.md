# CriticAdmission — R23-C1 final-producer architecture and source/frozen inputs

Seat: `KaidokuR23.CriticAdmission` (critic, leaf, source review only).
Candidate C=`2838351450ff1ee4baa620c962a1153450d53311`, B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
All bytes read with `git show <rev>:PATH`. No counter, selftest, verify.py, controls, census, build, or
test was executed by this seat. The only commands run were git object reads, `sha256sum` of git blobs,
and one byte-prefix comparison of four Markdown blobs. Nothing was installed.

Verdict for the attack target: the frozen k>=2 improvement is provable from the retained records, the
expected exits are written as literals rather than copied from the run, and the counter reads git
objects rather than the live worktree. All of that holds **at V=`6615aea`, not at C**. There are three
defects worth fixing: (1) the census record is labelled with a git revision even though it reads the
live worktree; (2) one frozen input gate, the S058+ threshold, has no control that tests it alone; (3)
the frozen counting command runs counter code from the live worktree. There are also two disclosed
tradeoffs that the judge must enforce: the count was measured at V rather than C, and the instrument
and its expectations come from the same author.

## Findings

### F1 — Measured revision is V=6615aea, not candidate C (observed; tradeoff, judge must enforce)
- Every child record has `source_rev: 6615aeae…`. The producer argv was `--rev 6615aeae…`
  (`.ufo/waves/round-23/verify-initial-producer.json`, `verify/initial/summary.json`). None was taken at C.
- `git diff --name-only 6615aea C` shows that C changes only `verify/initial/*`,
  `verify-initial-producer.json`, `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-23.md`.
  It leaves the counter's read set unchanged: `corpus/knowledge`, `corpus/SOURCES.md`, both evidence
  roots, the R20 catalog and the R22 tools.
- [INFERENCE] The deterministic git-only counter would return 4/6 at C too. That is not verified at C.
- No-harm at C is unmeasured, because `round-21/controls.py` was not run with `--after C`. I compared
  bytes directly: the B blob is a byte prefix of the C blob for LOG.md, SCORECARD.md, SKILL.md and
  PROVINCE.md, and the V blob is a byte prefix of each C blob. Map and citation integrity at C is
  unknown, since `corpus/lessons/round-23.md` changed in C.
- The narrative is honest about this. LOG/SCORECARD/lessons consistently say "Source V=6615aea…".
- Axes: coverage and calibration (admission provenance).
- Smallest safe correction: the judge admits 4/6 only "at V". To admit at C, it either runs the frozen
  counter once with `--rev C`, or records that `C\V` touches no counter input (the diff above) as the
  explicit basis for carrying the count forward.

### F2 — Expected exits are not self-derived (observed; holds)
- `verify.py:38-50` (C blob sha `59833006…`, identical at V) compares `r.returncode` to a literal
  `expected_exit`. The child's exit is never copied in as the expectation.
- The literals are: before-c1 = 1, after-c1 = 1, selftest = 0, frozen-input-red = 2, r22-c1 = 1,
  r22-c2 = 0, no-harm = 0, signal = 0, dart = 0, census = 0 (`verify.py:60-72,110`).
- `verify.py` was first committed at `2b40aec`. The only change before V is the
  `TMPDIR` child env (`diff 2b40aec 6615aea`). So the literals predate the retained run.
- Exit 1 for k=4 follows `count-c1.py:166` (0 only when k=6). That matches the claim frozen at
  `a3c92eb`, which says "incomplete unless k=6".
- Caveat (observed): the after-c1 predicate pins `t1_exercised_count==4` plus the exact verb list. That
  is stricter than the frozen `>=2`. It is an author expectation, not a frozen one. It can only add
  failures and cannot inflate the count.
- [UNKNOWN] Whether 4 was observed in an unretained earlier run before the literal was written.

### F3 — Self-derived selftest oracle revision (observed; disclosed tradeoff)
- `frozen/expected-v1.json` sets `old_source` to exit 1, count 1. `frozen/expected-v2.json`, the active
  oracle, sets it to exit 2, `unevaluable`. Both were added in the same commit `2b40aec`, together with
  the counter and the evidence.
- That commit is after the claim freeze `a3c92eb`, which contains no counter or oracle. The v2 hash
  `458b30d5…` is pinned only inside the counter itself (`count-c1.py:25`).
- `frozen/expected.json` is byte-identical to `expected-v1.json` (`ad1b4462…`). That is a dormant
  duplicate authority under the name that reads as canonical. LOG says v2 is active.
- `frozen-input-red` (`verify.py:63-67`) mutates only `fixture.json`. No control proves that a joint
  edit of `count-c1.py` and `expected-v2.json` is caught.
- Mitigation (observed): the `count-c1.py` blob is `f4b8d16a…` at 2b40aec, V and C. So the counter was
  not tuned between the evidence commit and the demonstration. `source-pins.json` records the same hash.
- Axes: calibration. This already falls under `not_claimed: independent non-author admission`. The
  judge must not read "frozen" as "pre-registered".

### F4 — S058+ threshold has no isolating control; mutation would survive (inferred from source; fixable defect)
- `count-c1.py:107` gates new-witness eligibility on `int(sid[1:]) >= 58`.
- The only control aimed at it, `old_source` (`counter-fixtures.py:77-78,85-86`), also appends ENTRY
  to the S051 row. That trips `historical_sources_changed` (`count-c1.py:72-73`) before line 107 is
  ever reached, which is why v2 expects exit 2.
- Real bypass shape (observed preconditions): at B, S051–S057 are all `A | mined | 2026-10-21`.
  Their used-by already names `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` or
  `…-r22-flutter-positive-dart-refusal.md`.
- Counterexample: a later commit edits that R22 entry to cite a round-23 `.json` envelope plus its
  evidence id. That needs no SOURCES row change. With line 107's `>=58` deleted, the counter would
  credit it, and [INFERENCE] all 21 selftest cases would still pass.
- Today the only thing catching it is the separate no-harm control (`round-21/controls.py`, "prior
  files unchanged"). The counter itself has no defense.
- The current C count does not depend on this: the new entries cite S058/S059/S060 and S061, whose
  rows list exactly those entries.
- Axes: coverage (falsifiers "new source relevance or ownership unsupported" and "inherited identify
  lost").
- Smallest safe correction: add one case to a v3 manifest that edits the existing R22 entry named in
  S051's used-by, leaves SOURCES.md untouched, and expects exit 1, count 1. A mutation seat should
  confirm that deleting `>= 58` turns that case red.

### F5 — Source census is a live-worktree observation labelled with a git revision (observed; fixable defect)
- `verify.py:110` runs `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kaidoku`. It runs outside and after the snapshot-clone block.
- That script lives in the parent repo and is not pinned. Its header says it reads lane
  `corpus/SOURCES.md` from disk, checks `E11 used-by path missing on disk`, and flags `W04` across
  sibling scopes.
- `record()` still writes `source_rev: rev` (`verify.py:46-47`), so `verify/initial/source-census.json`
  claims `6615aea` for a live, fleet-dependent result.
- The no-harm item "source census exit0" is therefore false provenance as labelled.
  - [INFERENCE] SOURCES.md is the same at V and C, so the verdict is probably the same.
  - It is not reproducible from C, and it depends on siblings' live SOURCES state and the parent
    script's live bytes.
- Axes: calibration and no-harm (false provenance).
- Smallest safe correction: run the census inside the clone block against the snapshot (`--file
  <clone>/corpus/SOURCES.md`, or a lane dir inside the clone), and record the script's sha256. Or label
  the record `source: live_worktree` instead of `source_rev`.

### F6 — Frozen counting command executes live-worktree code (observed; fixable at judge side)
- `claims.json` `counting_command` is `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE>
  --rev <REV>`, which is a cwd-relative path. Run as written, it measures `<REV>` git data with whatever
  counter bytes the moving worktree holds.
- `measure()` itself is snapshot-pure: every input is `git show rev:…` (`count-c1.py:60-124`), and
  `HELPER_SHA256` pins the R22 helpers (R22 `count-c1.py:50-66`).
- `--selftest` reads `root/rel` live files (`count-c1.py:138-146`). It is only snapshot-safe because
  `verify.py:53-59` points `--root` at a checked-out clone.
- `verify.py` itself ran from the live path (`verify-initial-producer.json` argv[3]). Its recorded
  `producer_source_sha256` `59833006…` equals the V and C blobs. However, `verify.py` does not write
  that wrapper file, so who wrote the wrapper record is [UNKNOWN].
- Smallest safe correction: the judge materializes `git show REV:.ufo/waves/round-23/tools/count-c1.py`,
  or uses a clone at REV, and asserts sha `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`
  before counting.

### F7 — An incomplete current count does not make the frozen improvement unprovable (observed; holds)
- The counter's exit encodes completeness only. k comes from the `t1_exercised_count` field in stdout.
- The same counter blob (`f4b8d16a…`) recorded:
  - at B: count 1, `['identify-flutter-build']` (`verify/initial/before-c1.json`);
  - at V: count 4 (`verify/initial/after-c1.json`). The held targets:
    - identify (historical R22 `identify-flutter-build-saber`, `identify-godot`);
    - inspect-dart-aot (`inspect-dart-legacy-saber.envelope.json`);
    - inspect-signal-decoders (`inventory.envelope.json`);
    - decode-signal-recording (`decode-official-uart`, `decode-uart-hi`).
- The refusal `decode-invalid-decoder` is not counted.
- The baseline of 1 was also recorded before the new counter existed, by the reviewed R22 counter at
  freeze time (`before-r22-c1.json`: `['identify-flutter-build']`, 1). So the baseline is not authored
  by the new instrument.
- 4 >= 2, and both exits are 1. "Incomplete" and "improved" are therefore separable and consistent.
  This holds at V, and at C only under F1.
- Tradeoff (inferred): `bind_new` (`count-c1.py:42-56`) rejects any nested dict anywhere with
  `ok != true`. That can falsely refuse real envelopes that carry per-item `ok:false` subresults, for
  example future gdb/rizin envelopes. This direction only undercounts, so it does no harm to this claim.

## Produced files and hashes
- `.ufo/waves/round-23/w2/CriticAdmission.md` (this file; sha256 not self-embeddable; L1 should hash it on intake).

## Installs
None.

## Open risks
- [UNKNOWN] Whether global git config (hooks, for example `core.hooksPath`) affected `git clone`/`checkout` in
  `verify.py:55-56` or `counter-fixtures.py:31-35`. Only `GIT_*` env is stripped. HOME config was not
  read, per the contract.
- S060 and S061 cite the author's own REA envelopes as sources. Relevance and ownership stay manual and
  belong to other seats.
- F4's mutation survival is inferred from source and has not been executed. A designated mutation seat
  is required to call it observed.
