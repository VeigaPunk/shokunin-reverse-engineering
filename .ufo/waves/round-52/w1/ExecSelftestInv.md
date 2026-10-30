# ExecSelftestInv — R52-W1

Verdict: settled; inventory artifact ready for L1 verification.

- `cases.md` inventories v1 selftest `add()` cases and direct layout/spec/runner probes, with per-case assertion and port/adapt rationale; it also specifies fixture and expected result for each of the seven R52-required new cases.
- Primary adaptations: the R50 rule's device-gap expectations must not be carried over; R52 requires law-shape rejection of the all-thirteen whitelist, runtime non-regular census re-derivation, visible explicit prior-pin waiver, and depth-gap path/continuation evidence. Round-specific provenance/docs/frozen paths also change.
- Evidence: read `tools/round-50/c1-counter.py` selftest lines 2868–4594 and authoritative `plans/round-52-claims.md` lines 27–175. Disk guard status was run before the work; reported `/fast/scratch/hyaku` 46% used, 435.4G free. No counter tests, builds, lint, REA or data run executed.
- Artifact: `.ufo/waves/round-52/w1/ExecSelftestInv/cases.md`; status: `.ufo/waves/round-52/w1/ExecSelftestInv/status.json`.
- Risks: the table describes v1 cases and intended R52 disposition; it is an inventory for L1 to compare against the eventual v2 implementation, not evidence that v2 selftests exist or pass. Some v1 direct probes are not `add()` cases and are explicitly included as probe entries.
- Blockers: none.
