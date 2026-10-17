## CLAIM
r9-02:215-216 reconciliation: draft the minimal append-only erratum for `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md` (or adjudicate none needed), given README:53's round-4 "inferred not evidenced in results".

## METHOD
Read-only at HEAD `cfc84c2` (worktree = HEAD; `git status` shows only untracked `.ufo/`): r9-02 `:7-8`, `:50-55`, `:78-85`, `:108-124`, `:184-216`, `:294-309`, `:321-345`, EOF `:375`; README `:53`/`:122`; round-4 V12b/R03/C04; LOG.md:749. Wave drafts (VB5/D5/DB5) and gates (C4 matcher, X1 guard) read after the primary pass. No probes, no network.

## FINDINGS
- Overclaim confirmed in three places: `:7-8` ("all four verification statuses observed live"), `:215-216`, `:326-334` ("four distinct typed statuses"). The union (`:50-55`) has four variants; results record three — `verified` (`:120-121`, run 11), `contradicted` (`:112`, run 10), `unresolved` under both bases (`:82-84` run 9; `:194-196` run 13) — plus the refusal (`:198-203`, run 7). `inferred:0` (`:83`) is the sole explicit count; the `:205-207`/`:243-244` `inferred` strings are envelope confidence. Erratum needed: round-4 named the file-side reconciliation debt (V12b.md:11; LOG.md:749).
- Draft for EOF append (after `:375`), C4-shaped (heading prefix + tokens, truthfully embedded), X1-guarded, append-only. Keep the token lines unbroken when appending.

```
## Errata (round 5 freshness reconciliation, r9-02)

- **Status-taxonomy qualifier (:7-8, :215-216, :326-334).** "All four
  verification statuses observed live" / "the four statuses … complete row
  13's observable behavior surface" overstate this record. The schema union
  defines four variants (:50-55); the runs demonstrate three — `verified`
  /`exact-function-name` (run 11), `contradicted`/`module-mismatch` (run
  10), `unresolved` under both bases (`no-native-candidate`, runs 9-10;
  `unsupported-native-evidence`, run 13) — across separate runs, plus the
  typed refusal (run 7). The single queued-pairing gtk run's summary (sole
  explicit count) reads 0 verified, 0 inferred, 39 unresolved, 0 contradicted
  (:82-84); `inferred`/`decorated-name-candidate` is not evidenced in any
  recorded run (`confidence:"inferred"` at :205-207, :243-244 is envelope
  metadata). This record does not establish `inferred` is unreachable.
  Earlier observations stand as written.
```

- Converges with VB5/D5/DB5; closes the heading/token gaps RB3/CB9 flagged in DB5. Parent-owned spill, outside this draft: README:122, LOG.md:286-289.

## THREATS
Text-only, no re-probes; corpus evidence cannot show whether an unrecorded run produced `inferred` — the draft says "not evidenced", never unreachable. My write scope is this seat file; the append is the parent's.

## VERDICT
FINDING: r9-02 overstates observed statuses at :7-8/:215-216/:326-334 — minimal integration-shaped EOF erratum drafted above (3 of 4 variants evidenced; `inferred` schema-only, not unreachable).
