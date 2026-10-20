# ReviewProvenanceCorrections — R16-PROVENANCE corrections (falsify wave)

Seat: `KaidokuR17.ReviewProvenanceCorrections` (leaf, read-only advisory). Lane revision
`da64646adcb19c1ede7537b799b8c7d283fe43da`; baseline `b563c799d97774aae4351276fe43cb897311e349`.
No carrier executed, no REA analyze/search/decompile, no Ghidra/analyzeHeadless, no gate run beyond the
two round-17 tools' own `--selftest`; no installs or updates. Python invoked with `-B`; scratch under `/tmp`.
Only this file was written.

## Verdict

All four correction lines name a line that at `b563c79` really holds a temporal-stability claim, and the
correction's positive clause ("map matches committed source-revision blobs") is **observed, not assumed**:
the 20-entry map matches committed blobs 20/20. No in-class r16 producer/fixture-pin claim is left
uncorrected. Two calibration defects remain in the round-17 artifacts themselves: one MEDIUM overclaim
about the round's own mid-run pins (F1), one LOW stale tool-contract description (F2), plus one LOW
out-of-population r16 survivor (F3). Filed r16 bytes are unchanged.

## Findings (severity order)

### F1 — MEDIUM — "pins equal pre/mid/post" has no retained mid map; the mid equality exists only as absence of a failure field

Sites: `corpus/lessons/round-17.md:26` ("8 receipts with one bound session each and pins equal
pre/mid/post") and `corpus/lessons/round-17.md:73` ("`tools/pins.py` (pre, 30 s mid-run and post maps
with timestamps) used by `carrier-run.py`").

Observed:

```
$ python3 -B -c 'import json;d=json.load(open(".ufo/waves/round-17/runs/pro-op/receipt.json"));print(list(d))'
['bound_sessions','carrier','label','log_capture_limit','orig_argv','pins_compare','pins_post','pins_pre',...,'steps','unbound_sessions']
$ ... print(list(d["pins_compare"]))
['changed','equal','errors','missing','post_taken_at_utc','pre_taken_at_utc']
$ grep -rln "pins_changed_during_run" .ufo/waves/round-17/runs/     # none
$ grep -n "pins_changed_during_run" .ufo/waves/round-17/tools/carrier-run.py
430:                    rec["pins_changed_during_run"] = {
```

`carrier-run.py:422-433` takes a throttled mid-run `pins.snapshot()` and compares it to the pre map, but
writes only `pins_changed_during_run` **on inequality**; the mid snapshot (which does carry `taken_at_utc`,
`pins.py:69`) and its timestamp are never stored. All eight receipts carry only `pins_pre`, `pins_post`,
`pins_compare`; my audit of `runs/*/receipt.json`: all 8 `equal=True`, changed/missing/errors 0, and a
pre/post pair per receipt (e.g. `pro-op` 13:55:55→14:00:05). So the receipt proves pre/post identity; the
mid instant has no digest and no named time. A mid equality is inferred from the absence of a field — the
absence-of-record shape the round's own QUALITY #19 rejects for `pins_unchanged_during_run`
(`corpus/QUALITY.md:29`: "records at named instants").

The admitted knowledge entry is correctly bounded, which confines the damage:
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:27-30` — "hashed before, every 30 s during, and
after … All eight pre/post compares are equal and no mid-run check differed. This shows identical bytes at
those instants, not continuity between them." Only the lesson's Gate justification and Mistakes row
overstate it.

Why it is in scope: this is the same claim class R16-PROVENANCE corrects, restated inside the corrective
lesson, and `temporal-sweep.py` cannot see it — `SITE_SOURCES` (`tools/temporal-sweep.py:37-43`) contains no
`corpus/lessons/round-17.md` (it is only a correction source, `:45-49`), and the pattern (`:55-59`) has no
`pre/mid/post` form.

Smallest fix (two lines, no schema change): reword `round-17.md:26` to "pins equal pre/post, and no mid-run
check differed (mid map not retained)" and `:73` to "pre/post maps with timestamps; a throttled mid-run
comparison whose mismatch would be recorded". If the stronger claim is wanted, persist the last mid map
per run in the receipt.

### F2 — LOW — `contract.md` still specifies the pre-widening temporal-sweep rule; the round's 4-site number is not reproducible from it

`contract.md:90-96` promises: sites in five files matching
`(?i)(unchanged during|remained unchanged during|stable throughout|pins_unchanged_during_run)`, and a site
`corrected` if *some* line contains the marker and the site's repo-relative path. The shipped tool at
`da64646` searches `corpus/knowledge/` too (`tools/temporal-sweep.py:37-44`), matches
`unchanged (during|across|throughout) (the )?(run|execution)` (`:55-59`), and requires the exact `file:line`
plus "temporal stability not evidenced" (`:62`, `:167`). `contract.md` is unchanged since the prediction
commit: `git diff 2711674 da64646 -- .ufo/waves/round-17/contract.md` is empty.

```
$ python3 -B <contract-rule reproduction over its five files at b563c79>
contract-rule sites at b563c799… = 2
corpus/lessons/round-16.md:154
.ufo/waves/round-16/verification.json:419
$ python3 -B .ufo/waves/round-17/tools/temporal-sweep.py --root . --rev b563c79 --sites-rev b563c79
{'corrected': 0, 'new_unqualified_at_rev': 0, 'sites': 4, 'unqualified': 4}
```

So a reader applying the written contract gets 2 sites, not the round's stated 4, and the contract's
path-coarse rule would accept the omnibus marker line the tool now (correctly) rejects. The lesson
discloses the undercount (`round-17.md:75`), so this is documentation lag, not a hidden divergence.
Smallest fix: append one line to the contract section — "superseded at `da64646` by
`.ufo/waves/round-17/tools/temporal-sweep.py:37-62` (widened source set/regex; exact `file:line` + required
phrase)" — or mark the section as dispatch-time text.

### F3 — LOW — one r16 temporal claim in the lane, outside the routed population, is uncorrected

`.ufo/waves/round-16/w2/FNoHarmCraft.md:11` — "| `.ufo/waves/round-16/controls.py` | `5f9fe949…` |
Unchanged across the review |"; `:12-13` add "Unchanged since 05:15:50/05:20:22".

```
$ git grep -n -i -E "unchanged (during|across|throughout)" b563c799… -- .ufo/waves/round-16/
b563c799…:.ufo/waves/round-16/verification.json:419:  "pins_unchanged_during_run": true,
b563c799…:.ufo/waves/round-16/w2/FNoHarmCraft.md:11:| `.ufo/waves/round-16/controls.py` | `5f9fe949…` | Unchanged across the review |
```

Subject and window differ from the routed defect (a review artifact across a review, not producer/fixture
pins during execution), so C1(a)'s population does not include it and no correction line names it. The
same table records sibling files "Changed … during review", so the claim is not obviously false — but it
has no retained before/after pair. Smallest fix, pick one: (a) add `- R16-PROVENANCE:
.ufo/waves/round-16/w2/FNoHarmCraft.md:11` with the required phrase; or (b) preferred, state the exclusion
boundary in the corrections header (seat review observations are per-seat and excluded), so the population
is explicit rather than implied. Under reading (b) there is no in-class survivor.

## Per-site verification of the four correction lines

Read at `b563c79` with `git show REV:path | awk 'NR==n'`:

| anchor | text at baseline | holds claim? | corrected_by |
|---|---|---|---|
| `LOG.md:2012` | `parameter. Producer/fixture hashes remain unchanged across execution.` | yes — "unchanged across execution" | `LOG.md:2059` |
| `corpus/lessons/round-16.md:154` | `All producer/fixture pins remained unchanged during execution.` | yes | `LOG.md:2060` |
| `.ufo/waves/round-16/verification.json:419` | `"pins_unchanged_during_run": true,` | yes — the predicate itself | `LOG.md:2061` |
| `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` | `not observed Java parity. Producer and fixture pins were unchanged during` (frame completes at `:96` "the run.") | yes — predicate on `:95` | `LOG.md:2062` |

The knowledge site's claim is hard-wrapped; the tool attributes a site to the line where the match starts
(`tools/temporal-sweep.py:116-129`) and the correction names that line. That is the only sensible single
line token, so I record it as correct, not a drift.

The four lines are byte-identical in both append points:
`diff <(sed -n '2059,2062p' LOG.md) <(sed -n '85,88p' corpus/lessons/round-17.md)` → empty.

### Positive clause verified

"map matches committed source-revision blobs" — recomputed SHA-256 for every path in
`producer_and_fixture_sha256` from `git show REV:path`:

```
entries 20 match 20 mismatch 0 absent 0   (REV = b563c79)
at 27b8fc1… match 20 other 0              (recorded verification.json source_revision)
```

So the replacement sentence is true at both the lane baseline and the receipt's own recorded revision.

## Append-only / filed bytes

```
$ git diff --stat b563c79 da64646 -- corpus/lessons/round-16.md .ufo/waves/round-16/
(empty)   # 0 bytes
$ git diff --stat … -- corpus/lessons/round-16-verifier-spotcheck.md corpus/knowledge/2026-10-20-r16-go-selection-preview.md
(empty)
$ LOG.md prefix: baseline 133860 bytes; sha256(first 133860 bytes of da64646:LOG.md) == baseline sha256 → YES
$ git show da64646:LOG.md | sed -n 2012p
  parameter. Producer/fixture hashes remain unchanged across execution.
```

No filed r16 byte was rewritten; the corrections live only in LOG and the round-17 lesson.

## Independent survivor sweep (bounded)

- Canonical pattern, whole tree at `b563c79` (`git grep -n -i -E "unchanged (during|across|throughout)|stable
  throughout|pins_unchanged_during_run"`): exactly the four lane sites above, plus
  `corpus/lessons/round-16-verifier-spotcheck.md:183` (the defect statement itself, marker-bearing) and
  `FNoHarmCraft.md:11` (window "the review", so the tool's run/execution regex excludes it).
- Adjacent "unchanged" claims read and excluded, with reasons:
  - `corpus/lessons/round-16.md:65` "Outside verifier files remain unchanged." — lane-start state; backed by
    `prior_verifiers_unchanged` in `verification.json`.
  - `corpus/lessons/round-16.md:142` "pointer table/expected pins unchanged" — that is the admitted
    "map matches committed blobs" form: both gate files are two of the 20 map entries (verified above).
  - `corpus/lessons/round-16.md:145-146` "126/126 … byte-identical; all four prior outside verifier files
    unchanged" — two-state output of `controls.py BASELINE SOURCE` with per-file digests retained.
  - `corpus/lessons/round-16-verifier-spotcheck.md:127` "original and supplemental baselines remain
    unchanged and digest-pinned" — r15 baselines, digest-pinned; not r16 pins.
  - `SCORECARD.md:2294-2306` (r16 block) — no temporal claim; it points at the receipt.
  - `SKILL.md`, `SHONEN.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `PROVINCE.md` at
    `b563c79` — canonical pattern yields no sites.
- Selftests (`able to fail` claims):
  - `python3 -B .ufo/waves/round-17/tools/pins.py --selftest` →
    `red case observed: compare exit 1 names /tmp/pins-selftest-…/a.txt` + `SELFTEST: CLEAN cases=7`, exit 0.
  - `python3 -B .ufo/waves/round-17/tools/temporal-sweep.py --selftest` → `SELFTEST: CLEAN cases=6`, exit 0;
    cases 2-3 exercise the exact-`file:line`+phrase rule and the deleted-site red case.
- End-state counts: baseline `4 sites / 0 corrected`; at `da64646` `4 / 4`, `new_unqualified_at_rev: 0`.

## Residual risk and verification gaps

- `temporal-sweep.py` is a wording census (its own docstring says so); a paraphrase outside its regex is
  invisible. F1 is a live instance: the claim is restated in the round-17 lesson, which is not a site
  source, so the counter that is supposed to discharge the defect cannot flag its own round's restatement.
  The w1 `ConnProvenanceRoutes.md` §2.2 self-exemption concern is only half-fixed: path-coarseness is fixed,
  self-exemption is not.
- No retained mid map exists for any run. If a future claim needs the mid instant, `carrier-run.py` must
  persist that snapshot (schema change), not only a failure flag.
- Pin values are taken from the receipts (I did not re-hash the host's installed Go data or the carriers);
  I verified receipt structure, timestamps, equality fields, and the 20-entry map against Git blobs.
- The `da64646` revision is pre-falsify: `w2/` is untracked in the worktree, so nothing in this wave's
  reports (including this one) is part of the measured revision yet.

Calibration read: 4/4 anchors and the 20/20 map clause verify, so the corrections themselves are
well-aimed; F1 is the only substantive miss and it is inside the round-17 lesson, not the corrections.
Depth read: the corrections add the warranted sentence, but the instrument still cannot see the round that
writes the corrections — the one change that would make the fix class-complete is adding
`corpus/lessons/round-17.md` to the site population (and a `pre/mid/post` alternative to the pattern).
