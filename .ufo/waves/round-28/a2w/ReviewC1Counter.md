# R28-C1 counter review — ReviewC1Counter

Scope: tools/round-28/c1-heldout-naming.py vs .ufo/waves/round-28/claims.json (R28-C1).
Reviewed at lane tip a267311678309fd17772407e8afa122ec3219289 on 2026-10-22. Counter sha256 at
tip = 29c2b571…b27c, identical to claims.json instruments pin (observed). Selftest run:
21 cases, 0 failures, exit 0 (artifact selftest.txt). Counter run at tip exit 1:
runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=0 (artifact counter-at-tip.txt).

## Findings (numbered, severity ordered)

1. c1-heldout-naming.py:225 (severity low) — HOLDS but with a provenance gap: the manifest url
   check `if url is None and i == 0` only assigns the expected 4byte page-0 url to the first
   file, so manifest entries for 4byte pages p>=1 pass with any or no url, while p0 and
   openchain are url-bound. Weakens the record's own provenance statement only; cannot elevate
   a pass because every manifest field is producer-recorded anyway and bytes are sha-bound.
   Unexercised on real data: zero p>=1 files exist at tip.

2. c1-heldout-naming.py:187,242 (severity low) — HOLDS with a same-commit edge: the commit-time
   rule is `added < counter_time` => refuse, so a data file committed in the counter's own
   commit (added == counter_time) satisfies it; recorded times (utc_start/manifest utc, lines
   177,237) still require strictly-after. Matches the literal freeze wording ("first committed
   ... before its own commit"); unexploited: the freeze commit 87d3dfb contains only
   carriers.tsv and heldout.tsv (observed via git ls-tree).

3. c1-heldout-naming.py:208, resolver resolve-selectors.py:174-175,183-184 (severity low) —
   HOLDS as refusal but fails cleanly: a hash-consistent malformed counted record raises an
   uncaught exception instead of a FAIL line. Demonstrated: db row missing "text_signature" ->
   KeyError; non-JSON body -> JSONDecodeError; envelope function missing "selector" at line 208
   (outside the try that ends line ~206) -> KeyError. Exit code is still nonzero (crash), so no
   record passes; the counter just refuses by traceback rather than reason.

4. c1-heldout-naming.py:175-182,229-241 (severity informational) — HOLDS, bounded: utc_start and
   manifest utc are producer-recorded; only commit-time ordering is independently enforced, and
   envelope evidence_id is unchecked, so a fabricated-but-well-formed run record committed after
   the counter would pass. This is the counter's design limit (it counts committed records, not
   ground truth of execution); the claim's freeze_kind states exactly this mechanism. Cross-
   carrier envelope replay IS refused (subject digest+local_path bound to pinned carriers.tsv,
   selftest red-envelope-of-other-carrier green).

5. c1-heldout-naming.py:97-103 (severity informational) — HOLDS, conservative: first_commit_time
   returns the OLDEST add time (out[-1]); a file added, deleted, re-added is measured by its
   earliest add, which can refuse a legitimate re-addition. Not present in the real history.

## Verified holds against the claim

6. Pins: PINS (lines 61-66) covers exactly the code file (resolve-selectors.py) and frozen inputs
   (carriers.tsv, heldout.tsv); sha256 of all three at tip equal claims.json loaded_by_counter
   values (observed). Every other load via show()/ls() is counted data (runs.tsv, envelopes/,
   db/, tally.json) or checked artifacts (ENTRY, SOURCES, LESSON), matching pin_note.

7. Rule identity: rule_outputs (135-151) and RULES (68-74) are line-for-line identical to
   tools/round-25/a3/tally-resolution.py lines 24-48 (compared; observed).

8. Scoring unit and not-recovered: one row per heldout.tsv row (187 rows, 187 distinct
   selectors, observed); recompute line 258 sets recovered = sel in fns and line 272 forces all
   rule outputs to None when not recovered, so no_name counts it, matching the claim.

9. Time checks use the counter's own commit: line 353 counter_time = first_commit_time of
   COUNTER_PATH; all run/lookup/file time checks compare to it (177,187,237,242). Observed:
   counter added 1792689436; runs.tsv added 1792689752; db added 1792689949 (artifact
   commit-times.txt).

10. Byte-identical lookup bodies accepted: no cross-file byte comparison exists; selftest
    green-identical-4byte-bodies-across-selectors passes (observed exit 0). Records are keyed by
    manifest entry + file sha256 + commit time, not by content uniqueness.

11. No legitimate record refused beyond claim semantics: exactly-one run record per carrier
    (162-165) matches "one REA call per carrier"; exit!=0 refused (173), which correctly counts
    h09's genuine exit-1 run invalid (observed FAIL line at tip; h09 carries exactly 1 heldout
    row 395c1d44, hence 186/187).

12. Forgery gates present: runs.tsv argv must equal the pinned REA argv with the carrier's frozen
    runtime path; pkg version/sha pinned (175); envelope sha bound to file bytes (184), first-
    commit >= counter (187), operation/provider/subject digest/subject path all checked;
    tally.json must equal a full recompute over committed bytes (375-381, observed tally_equal=1
    at tip); entry requires source:/verified-at:/recheck:, the recomputed primary triple, and an
    S row new since base, status mined, opened 2026-10-22, in ## Gate (336-344; SOURCES.md header
    confirms column indices 7/8 = status/opened). At tip entry is absent => entry_ok=0, honest.

13. Pin refusal: any pinned file differing exits 2 (observed: selftest red-pin-refusal exit 2).

## Residual risk

The counter counts committed records whose producer-recorded fields (utc_start, manifest
url/utc/status) it cannot independently verify; commit-time ordering is the only hard ordering.
No lane-resident flaw found that would let a forged record flip the claim's exit code, or refuse
a record the claim requires.

## Artifacts (sha256)
- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewC1Counter/counter-at-tip.txt sha256 7414d1c38b86bbf76a0e88060799f9e680a4ba69b6d56ee7baf0b2f8aad16211
- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewC1Counter/selftest.txt sha256 33971d993bc2fe528cb09b4baeb324fb3d5db8774caa8fc5d8316dbfe1d1f9fb
- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewC1Counter/commit-times.txt sha256 5bde645bd4ca6bf8610f8edda908c1485eec165eb83d843b250fa643d92a37ee

No installs or updates performed. Report: .ufo/waves/round-28/a2w/ReviewC1Counter.md
