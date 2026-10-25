# R35Audit12 — C1 wrong-section token mutation

## Scope and evidence
Read the frozen plan (`plans/round-35-claims.md`, C1 at lines 16–32), canonical claims (`.ufo/waves/round-35/claims-canonical.json`, C1 predicate), and the frozen C1 counter (`tools/round-35/c1-coverage-counter.py`). No lane production or source-tree files were changed. All mutation fixtures were created in private `/tmp` temporary Git repositories and scored with the lane counter in immutable-Git-object mode.

Counter integrity: SHA-256 of `tools/round-35/c1-coverage-counter.py` was `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220`, matching the canonical instrument digest. Instrument selftest output: `C1_SELFTEST: ok` / `green=0 red=1` (exit 0).

## Commands and results
Fixture score command (one invocation per mutation):

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-35/c1-coverage-counter.py --root <private-temp-git-repo> --rev HEAD --freeze <fixture-green-commit>
```

| Fixture mutation | Result |
|---|---|
| Green baseline with both correct entries, rows, README and PROVINCE tokens | `C1_CLEAN revision=HEAD` (exit 0; observed in initial baseline run) |
| Mapper entry cites S129 instead of S125 | Reject, `row_citation_missing:...mapper-contract.md:S125` (exit 1) |
| S125/S129 `used-by` values swapped | Reject, both `registry_usedby_missing` failures (exit 1) |
| Both filenames present in README coverage map but under unrelated section label | **Accepted**: `C1_CLEAN revision=HEAD` (exit 0) |
| Both stems present in PROVINCE.md but only under `## Older notes`, not Round-35 Core additions | **Accepted**: `C1_CLEAN revision=HEAD` (exit 0) |
| Mapper cites S1250 and a matching S1250 SOURCES row is added, while required S125 row remains | **Accepted**: `C1_CLEAN revision=HEAD` (exit 0) |
| Both entries cite S125 | Reject, release-inventory row citation missing S129 (exit 1) |
| Mapper has heading/body before otherwise valid provenance trio | **Accepted**: `C1_CLEAN revision=HEAD` (exit 0) |

Note: the standalone rerun's nominal M0 no-op mutation could not commit because its tree was clean (`nothing to commit`); baseline green acceptance was observed in the initial successful fixture run before that rerun. The other mutation fixtures each committed and ran independently.

## Findings / limits
The frozen counter detects wrong per-entry source rows, swapped registry `used-by`, and a missing distinct S129 citation. It does not enforce the declared section placement: README filenames can be in an unrelated section and PROVINCE stems can be in a non-Core section. Its row citation is an unbounded regex substring, so `S1250` satisfies the S125 token check when an S1250 registry row exists. It checks that provenance keys occur somewhere, not that the trio opens the entry; a heading/body before the trio passes. These are observed false accepts relative to the plan's section/“opens with provenance trio” language and the specific-row requirement. This is advisory evidence only; frozen predicates/scope were not changed.

Report: `.ufo/waves/round-35/w1/R35Audit12.md`
