# RV-8 corrections — EX-30 patch-text clauses that the revised tool does not implement

Seat RV-8 · chain c2 · reviewer · wave `arc3-loop1-round3` · 2026-10-19.
Reviewed artifacts (patch texts only; EX-30 authored both) — **re-reviewed after
EX-30's re-emission** (rule #14); the two gaps below persist in the re-emitted
bytes (clause line numbers are in the current revision):

- `.ufo/waves/arc3-loop1-round3/claims/c2/EX-30/readme.patch.md`
  sha256 `07bff2086d6f7ec0c110fdbd2acb24c0a35edadee1ccc764678400c253a660ed`
  (earlier revision reviewed: `8941cbd91d5f11752ac9cb73…`; gap 1 at line 118,
  gap 2 at line 149 of the current bytes)
- `.ufo/waves/arc3-loop1-round3/claims/c2/EX-30/registry-row.patch.md`
  sha256 `153cc48c7ab3d01f7c7f6487f54655020b228dfd194d0f0e232816f311ebb591`
  (earlier revision reviewed: `9c5ff61a3933b1eda0ee3c2d…`)

Both re-emissions now pin instrument revision
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` — the
revision this review used. All identities in the re-emitted pair were
re-derived by this seat and reproduce exactly: `registry-row.diff` 8 lines
`dbd79a6377…` → SKILL `62de392295…`/390 lines; `readme.diff` 114 lines
`3a7e45dae8…` → README `a82d0071fe…`/180 lines
(`/var/tmp/rv8/ex30-apply-v2`; script `evidence/ex30-apply.sh`).

Instrument revision reviewed: `.ufo/gates/custody-pair/custody-pair.py`
sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`
(1155 lines; selftest `CLEAN cases=22 passed=22 failed=0 exit=0`).
Transcripts: `evidence/claims-run.txt` (this seat's dir). Every clause below was
run against that revision; the two failures were re-run against
`03bd6242…`, `89bfebec…` and `7cd19c3c…` — same result, so they are not
revision churn.

## Gap 1 — "without it, coverage is reported but not enforced" (readme.patch.md)

Claim (added `## Reference coverage` section, final sentence): *"The flag
applies to v1 and v2 references alike; without it, coverage is reported but not
enforced."*

Measured: without `--require-paths`, the tool prints **no** `REFERENCE-COVERAGE`
line — the call site is inside the flag branch (`custody-pair.py:677-687`;
`reference_coverage` has exactly one caller). A 1-of-5 reference vs live with no
flag reads `VERDICT: MATCH … exit=0` and 0 coverage lines
(`evidence/claims-run.txt` §C-3; with the flag: exit 2 + the line, §C-4; a v1
sums reference behaves the same, §C-5).

Correction (text, preferred — matches EX-21's landed phrasing):

> The flag applies to v1 and v2 references alike; without it, the comparison
> covers exactly the reference's paths and no coverage line is printed.

Correction (code, EX-21's target, if the sentence is to stay true): print
`reference_coverage(a_sections, len(CUSTODY_PATHS) or N)`'s line unconditionally
(after parsing the reference, before the flag branch) and keep the exit-2
enforcement inside the flag branch.

## Gap 2 — "receipt or sidecar" write-guard claim (readme.patch.md)

Claim (added `## Write scope` section, and the summary in §"Why the README must
change"): *"`capture` refuses (exit 2, `USAGE`) to write a receipt **or sidecar**
over any path it is measuring — including a hardlink alias".*

Measured: the guard checks only `out` (`custody-pair.py:648-649`, resolved path
+ `_same_file` inode arm); the sidecar path (`out.name + ".sha256"`,
`custody-pair.py:657`) is never checked. Probe: `capture --paths X.sha256
--out X` → exit 0, and the sidecar write **overwrites X.sha256, the file being
measured** (a measured path destroyed by a clean-exit run). The receipt write
itself and the hardlink arm are refused correctly (exit 2, file intact) —
`evidence/claims-run.txt` §C-6/§C-7/§C-8.

Correction (text, minimal): drop the two words "or sidecar" → *"refuses to
write its receipt over any path it is measuring — including a hardlink
alias"*. The `registry-row.patch.md` write-scope cell does not repeat the
sidecar claim and needs no edit.

Correction (code, EX-21's target, if the clause is to stay): compute
`sidecar = out.with_name(out.name + ".sha256")` before the guard and include it
in the guarded check, e.g.

```python
        sidecar = out.with_name(out.name + ".sha256")
        if (out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded)
                or sidecar.resolve() in {g.resolve() for g in guarded}
                or any(_same_file(sidecar, g) for g in guarded)):
```

## Wording nuance (no action required, recorded for precision)

`registry-row.patch.md` says a path that exists but cannot be evaluated "is
recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent". For the
stat-blocked (EACCES-on-parent) class the receipt line reads `EXISTS: no` with
`STAT-ERROR: …` alongside it (`evidence/claims-run.txt` §C-12) — the record is
not silent and the class is `UNEVALUABLE` (14), so the clause is defensible as
written; a reader who greps only `EXISTS` should know the `STAT-ERROR` line is
the discriminator.

## Identity note (rule #14)

The current pair pins instrument revision `7cd19c3c…`, which this seat reviewed.
EX-30's own header records the earlier chain inside one hour (`d164d49f…` →
`d9be407d…` → `57dffff1…` → `03bd6242…` → `7cd19c3c…`) — two of those
(`d164d49f`, `d9be407d`) fall between this seat's 60 s watcher samples, so they
are not independently evidenced here; they are historical, not the landing
revision. The landing must substitute the settled digest in the README revision
line and in the `registry-row.patch.md` token table. The base/patched/diff
digests for the HEAD bases were re-derived by this seat and are correct
(SKILL `62de3922…` 390 lines, README `a82d0071…` 180 lines, diffs `dbd79a63…`
and `3a7e45da…`).