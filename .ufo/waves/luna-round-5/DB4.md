## CLAIM
2nd opinion (DB4) on VB4.md's README item: concur — both statements are stale at tracked HEAD cfc84c2, the current targets are `corpus/README.md:131` and `:163`, and VB4's two minimal fixes are correct. One wording precision suggested, and `SCORECARD.md:68-72` itself becomes stale once README is fixed.

## METHOD
VB4.md read as the assigned source; every claim re-checked against primary sources at HEAD cfc84c2 (`git rev-parse HEAD`; tree clean, only untracked `.ufo/`): `git show HEAD:corpus/README.md | sed -n '128p;131p;160p;163p'`; drift lineage by grepping the two target strings (`round-13-distillation`, `Runtime-obs extended`) across `git show {a3f2e1b,2abd30f,638fb21,6a71cd5}:corpus/README.md`; SCORECARD.md:62-75; LOG.md:388-401; r5-02:18,:53,:175-194; r9-02:321-350; r11-01:316-317,:351-360; r4-16:262-266. No probes. Disclosure: before VB4.md existed I read Lane-A V4.md solely to identify my target; all content verification is primary-source.

## FINDINGS
- Positions/drift exact: HEAD :131 = `lessons/round-13-distillation` row ending `verify-lane VERIFIED, 4 nits fixed`; :163 = `Runtime-obs extended… (~26 self-provisionable)` bullet. Lineage: a3f2e1b :128/:160 → :130/:162 (2abd30f) → :131/:163 (6a71cd5 = HEAD), i.e. +3 total. SCORECARD.md:68-70 cites the pre-drift :160/:128 — VB4's claim 2 exact.
- :163 removal correct: all three named families held — call targets (r5-02:181-192, 3/3 resolved; README:47), managed verify/project (r9-02:323-345; README:53), process-capture pair (r11-01:316-317 exit-0 runs, :351-360; README:56); "~26 self-provisionable" is r4-16:262's pre-drain census.
- :131 fix correct; wording suggestion (attribution-complete): `4 nits (2 fixed at integration, 1 already self-corrected by the distill lane pre-landing, 1 accepted)`. LOG.md:396-398 attributes the pre-landing correction to the distill lane (the verify lane read a pre-correction cut); "4 nits fixed" was never true even before the tail correction (LOG.md:389-390: 3 fixed, 1 accepted).
- VB4 claims 1, 3, 4 verified as stated. Follow-up: SCORECARD.md:68-72 is the debt entry that spawned this round; after the README fix it needs retiring or a pointer update, else it becomes the next drift.

## THREATS
Documentation-only; no runtime re-probes. Read scope: VB4.md (assigned) plus V4.md (target identification, pre-VB4); P0 not read. :159 spot-checked consistent (capture-electron-scenario refusal re-verified, r10-02:33); Frontier lines beyond :163 not re-audited.

## VERDICT
CLEAN — VB4's README claims reproduce at HEAD under independent primary-source checks; both fixes are right as drafted (one wording tweak, one SCORECARD follow-up flagged).
