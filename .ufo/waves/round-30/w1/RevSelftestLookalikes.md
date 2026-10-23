# RevSelftestLookalikes — R30 selftest look-alike and control-class coverage review

Seat: `KaidokuR30.RevSelftestLookalikes` (reviewer, wave 1). Lane read-only; no lane file
modified. All times UTC, 2026-10-23.

**Question.** Do the R30 selftests carry green look-alike cases for every refusal the
counters make (QUALITY.md row #40) and red cases for each control class named in
`.ufo/waves/round-30/claims.json` (`controls_required_before_data`)?

**Verdict.** Both selftests pass and every *written* case is honest (no green-labelled
case fails). But coverage is partial: green look-alikes are missing for three clauses the
counters exercise (shared-document carrier pair, duplicate-identical
`auditable_metadata`, refusal message on stderr only), and red coverage of the named
control classes is partial (`all-false` committed-envelope shapes in C1; the
`junk-row` linkage checks are unreachable from either selftest). Findings F1–F7 below.

## Evidence — selftest runs (observation)

```
$ python3 -I -B tools/round-30/c1-rust-positive.py --selftest     # 2026-10-23T02:44Z, exit 0
ok green-exact got=P1-pass (packages=2 edges=1)
ok green-reordered-indices got=P1-pass (packages=2 edges=1)
ok red-do-nothing got=P1-fail (envelope not ok)
ok red-nonzero-exit got=P1-fail (exit 1)
ok red-not-ok got=P1-fail (envelope not ok)
ok red-other-operation got=P1-fail (operation 'inspect_go_binary')
ok red-subject-mismatch got=P1-fail (subject sha256 'x')
ok red-null-metadata got=P1-fail (auditable_metadata count 1 or null)
ok red-empty-packages got=P1-fail (package multiset differs (rea 0, oracle 2))
ok red-empty-oracle got=P1-fail (oracle list empty)
ok red-version-differs got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-edge-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-kind-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-root-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-duplicate-package got=P1-fail (package multiset differs (rea 3, oracle 2))
ok red-offset-differs got=P1-fail (file_offset 101 != 100)
ok red-size-differs got=P1-fail (compressed_bytes 49 != 50)
ok green-committed-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-same-commit-as-freeze got=False (committed envelope absent or not added after the freeze)
ok red-no-freeze-commit got=False (no freeze commit)
ok red-committed-id-differs got=False (committed evidence_id 'ev_2' != live 'ev_1')
ok red-committed-packages-differ got=False (committed metadata shape)
ok red-entry-lacks-id got=False (entry does not name ev_1)
selftest cases=25 failures=0

$ python3 -I -B tools/round-30/c2-rust-refusals.py --selftest      # 2026-10-23T02:44Z, exit 0
ok green-refusal-matches got=P2-match (refused with predicted message)
ok green-acceptance-matches got=P2-match (accepted, packages=1)
ok red-do-nothing got=P2-miss (predicted message absent)
ok red-accepted-when-refusal-predicted got=P2-miss (accepted, refusal predicted)
ok red-other-message got=P2-miss (predicted message absent)
ok red-empty-predicted-message got=P2-miss (predicted message absent)
ok red-refused-when-acceptance-predicted got=P2-miss (not accepted (exit 1))
ok red-accept-wrong-packages got=P2-miss (package multiset differs)
ok red-accept-wrong-offset got=P2-miss (offset/size differ)
ok red-accept-wrong-subject got=P2-miss (subject sha256)
ok green-committed-agrees got=True (ok)
ok green-committed-refusal-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-ok-differs got=False (committed ok False != live ok True)
ok red-committed-id-differs got=False (committed evidence_id differs)
selftest cases=16 failures=0
```

Working-tree instruments are byte-identical to the freeze (`git show 0dbabf78:<f> | sha256sum`
equals `sha256sum <f>` and equals the `instruments` pins in claims.json for all three
files); selftest cases were present at the instrument commit. Probes below import those
exact files (`probe-gaps.py`, artifact listed at end) — observations, not patches.

## Case map — clause each case exercises

### C1 `judge` (c1-rust-positive.py:94-122) — P1 clauses

| case | P1 clause exercised |
|---|---|
| green-exact | all acceptance clauses positive: exit 0, `ok`, operation, subject sha256, exactly one metadata dict, non-empty oracle, multiset equality, file_offset, compressed_bytes |
| green-reordered-indices | **look-alike**: package order swapped with dependency indices remapped → same tuple multiset → pass (multiset clause, index indirection) |
| red-do-nothing | `env` not a dict → "envelope not ok" (do-nothing control) |
| red-nonzero-exit | `exit_code != 0` |
| red-not-ok | `env.ok is not True` |
| red-other-operation | `operation != inspect_rust_binary` |
| red-subject-mismatch | subject sha256 ≠ carrier sha256 |
| red-null-metadata | metadata count/clause, `null` variant |
| red-empty-packages | multiset differs (rea 0 vs oracle 2) |
| red-empty-oracle | `oracle_tuples` empty → "oracle list empty" |
| red-version-differs | multiset, version field |
| red-edge-dropped | multiset, dependency set |
| red-kind-dropped | multiset, kind field |
| red-root-dropped | multiset, root field |
| red-duplicate-package | multiset, duplicate member counted |
| red-offset-differs | `file_offset` clause |
| red-size-differs | `compressed_bytes` clause |

### C1 `committed_check` (:182-204) — "committed envelope agrees" half of P1

| case | clause |
|---|---|
| green-committed-agrees | all: added > freeze, committed ok, cid==lid truthy, committed multiset == oracle tuples, entry names cid |
| red-committed-absent | `env_added is None` |
| red-committed-before-freeze | `env_added < freeze_ct` |
| red-committed-same-commit-as-freeze | `env_added == freeze_ct` boundary (`<=`) |
| red-no-freeze-commit | `freeze_ct is None` |
| red-committed-id-differs | `cid != lid` |
| red-committed-packages-differ | committed multiset ≠ oracle tuples |
| red-entry-lacks-id | `cid not in entry_text` |

### C2 `judge` (c2-rust-refusals.py:200-228) — P2 clauses

| case | clause |
|---|---|
| green-refusal-matches | refusal arm: not-ok envelope + frozen message verbatim in stdout |
| green-acceptance-matches | acceptance arm: exit 0, ok, operation, subject, single metadata, multiset, offset/size |
| red-do-nothing | env None + no message → miss (do-nothing control) |
| red-accepted-when-refusal-predicted | `env.ok is True` under refuse prediction |
| red-other-message | not-ok envelope but message absent from both streams |
| red-empty-predicted-message | `not message` guard (vacuous prediction can't match) |
| red-refused-when-acceptance-predicted | acceptance arm `code != 0 / not ok` |
| red-accept-wrong-packages | multiset clause |
| red-accept-wrong-offset | offset/size clause |
| red-accept-wrong-subject | subject sha256 clause |

### C2 `committed_agrees` (:246-255)

| case | clause |
|---|---|
| green-committed-agrees | ok pair, added > freeze, ids equal |
| green-committed-refusal-agrees | refusal pair (committed `ok:false` agrees with live refusal) — a look-alike green |
| red-committed-absent | `added is None` |
| red-committed-before-freeze | `added <= freeze_ct` |
| red-committed-ok-differs | `c_ok != l_ok` |
| red-committed-id-differs | `evidence_id` differs under live-ok |

## claims.json `controls_required_before_data` → selftest coverage

| control class | C1 coverage | C2 coverage |
|---|---|---|
| do-nothing | red-do-nothing ✔ | red-do-nothing ✔ |
| junk-row (entry + PROVINCE/SKILL lines without envelopes) | **partial**: committed-absent + entry-lacks-id cover the envelope/id halves; `entry_ok`/`province_ok` (SOURCES row, base-diff checks) unexercised — see F5 | **partial**: same envelope-side only; `entry_ok`/`skill_ok` unexercised |
| all-false (committed refusal or null-metadata envelopes) | **partial**: committed-absent only; no `ok:false` committed, no null-metadata committed, no shape-exc committed — F3 | **partial**: red-committed-ok-differs covers the refusal variant; null-metadata not checked by `committed_agrees` (predicate scope) — untested either way |
| no-reader (oracle-fabricated envelopes) | **partial**: committed-vs-live disagreement covered (packages-differ); a fabricated envelope that agrees with live passes by design — the real guard is live-run-then-compare | same |
| shortcut keyed on ids/labels | ✔ committed-id-differs, entry-lacks-id, subject-mismatch | ✔ committed-id-differs, accept-wrong-subject, other-message |

## Findings

**F1 (moderate) — no green look-alike for the shared-document carrier pair.**
QUALITY.md row #40 wants a green selftest case for the legitimate look-alike a
duplicate-refusing gate could refuse — "two genuine runs whose envelopes are
byte-identical." C1's frozen input class contains exactly this shape: claims.json C1
`limits` states "uv and uvx of one wheel carry the same dependency document" (the
carriers.tsv pairs `elf-x86_64-uv`/`elf-x86_64-uvx`, etc. — same package list, different
subject sha256, different file). The selftest has no case feeding the same oracle tuples
under two different subject digests. Probe: `judge(env(sha="AAAA"), "AAAA", ...)` and
`judge(env(sha="BBBB"), "BBBB", ...)` both → `P1-pass` — the clause behaves; the case is
simply absent. The C1 selftest carries **zero** duplicate-related green cases.

**F2 (moderate) — no green look-alike for duplicate-identical `auditable_metadata`.**
`find_metadata` (c1:65-82) dedups identical values, so an envelope carrying the same
metadata object twice is the closest in-envelope analog of "identical evidence, still
legitimate." Probe → `P1-pass`; the twin failure shape (two *distinct* metadata blocks →
"auditable_metadata count 2 or null") is likewise unexercised in red. The multiplicity
axis of the "auditable_metadata count 1 or null" refusal has no selftest case at all —
only the `null` variant is tested.

**F3 (moderate) — C2: refusal-message-on-stderr-only green case missing.**
P2's clause is "the frozen message appears verbatim in the run's stdout **or stderr**";
every refusal selftest case passes `err_t=""` with the message in stdout. Probes:
`judge(R, refusal_env, "", "Dependency section is empty", 1, "h", None)` → `P2-match`,
and `judge(R, None, "", "<msg>", 1, ...)` → `P2-match`. Also untested: the permissive
MATCH when no JSON envelope exists at all but the message is in stdout
(`judge(R, None, "<msg>", "", 1, ...)` → `P2-match`) — worth pinning as an explicit
case since "the envelope is not ok" for an absent envelope is an interpretation the
selftest should make visible.

**F4 (moderate) — `all-false` committed-envelope shapes untested in C1.**
claims.json names the class verbatim: "committed refusal or null-metadata envelopes."
`committed_check` refuses committed `ok:false` ("committed envelope not ok", :188),
missing metadata ("committed metadata missing", :195) and malformed metadata
("committed metadata shape", :200); probes confirm all three fire — no selftest case
reaches any of them. Also unexercised: committed envelope with no `evidence_id`
(`cid` falsy → fails, probed). C2 covers the refusal variant
(red-committed-ok-differs) but the same asymmetry items appear at F6.

**F5 (low) — `junk-row` linkage checks unreachable from selftest.**
`entry_ok`, `province_ok` (C1:142-166) and `entry_ok`, `skill_ok` (C2:258-277) — the
clauses that fail a junk row *with* envelopes — are git-dependent and never invoked by
either selftest. Their sub-clauses (entry absent, missing `source:` row, row present at
base, PROVINCE/SKILL line absent or unchanged at base) have zero coverage. A junk row
carrying a committed envelope would fail only on paths with no demonstration.

**F6 (low) — acceptance-arm refusals unexercised (both counters).**
C2 `judge` miss reasons with no case: `operation %r` (probe → MISS), `metadata missing`
incl. >1-distinct-metadata (→ MISS), `oracle empty` (→ MISS), `metadata shape`
exception (→ MISS), `committed_agrees` no-freeze variant (→ False). C1 `judge`:
`metadata shape` exception path (probe → `P1-fail`), non-dict non-None env
(list → `P1-fail`). Each probes correctly; none is demonstrated.

**F7 (low) — committed-side agreement checks weaker than the selftest suggests.**
Probes on the pinned code:
- `committed_agrees` (C2) lacks C1's `if not cid` presence guard: a live-ok run with
  **no** `evidence_id` plus a committed envelope with none → `True` (probe). C1 refuses
  this shape. Predicate letter ("agrees … on ok and evidence_id") is arguably met, but
  the guard asymmetry is a live `None == None` pass.
- `committed_agrees(None, refusal, 200, 100)` → `True`: a committed file containing
  JSON `null` "agrees" with a refusal run (only `ok` parity is compared).
- `committed_check` (C1) never compares the committed envelope's **subject sha256**:
  a committed envelope with a different subject but the right evidence_id and multiset
  → `True` (probe). Within the predicate letter ("same evidence_id and package
  multiset") but not demonstrated, and adjacent to the "shortcut keyed on ids" class.

## Residual risk / verification gaps (observations, not defects)

- predictions.tsv reuses identical frozen messages across mutants built through
  different code paths (r-empty/r-nobits "not file-backed"; r-not-zlib/r-trailing-bytes
  "not a complete zlib stream"; r-extra-field/r-kind-dev "package schema"). Judging is
  per-mutant so no cross-match occurs, but a mutant refusing for the *wrong* reason
  with the *same* message still MATCHes; the `code_pointer` column is frozen but unused
  by `judge`. A green pair exercising this look-alike is also absent from the selftest.
- The C2 builder's determinism is pinned only at measure time (`do_build` sha check);
  the selftest comment (:430) states this. `build_mutants` output is otherwise
  unselftested.
- All measure-level aggregation paths (per-carrier loop, `--write-evidence`, exit-1/2
  branches) are outside selftest reach by design; the exit-2 PIN paths have no
  demonstration.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r30/seats/w1/RevSelftestLookalikes/)

| file | sha256 |
|---|---|
| `c1-selftest.txt` (full stdout + `c1 exit=0`) | `eb3b2b909eebd581c58ec59645c21b202df241fc9410dbed36d3beb9fc39032d` |
| `c2-selftest.txt` (full stdout + `c2 exit=0`) | `3068d56e7b54d1f4f40036f3c02733d3a3109c157ec04c12be0751fe0f62adf1` |
| `probe-gaps.py` (imports pinned counters, feeds proposed cases) | `2689097cb7b1604fd2be24789f5c347538b5ae98727916cf19ad1f96248761a8` |
| `probe-gaps.txt` (probe stdout, exit 0, 2026-10-23T02:47Z) | `dfe45277acc4756aa34396aee1b194af509332a85e8135e266c142a92188ad30` |

Exit codes: C1 selftest 0 (25 cases, 0 failures); C2 selftest 0 (16 cases, 0 failures);
probe script 0.

No REA runs, no carrier/mutant execution (selftest and judge-only probes run no
subprocess), no tool installs (host python3 sufficed), no messages sent, no lane writes
other than this report.
