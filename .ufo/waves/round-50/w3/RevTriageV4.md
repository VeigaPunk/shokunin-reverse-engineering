# RevTriageV4 — round 50 attempt 2, wave 3: the v4 table/evaluator contract, reversed for the v5 port

2026-10-29. Lane read-only; writes only under `.ufo/waves/round-50/w3/RevTriageV4*/`.
Base revision `f890bbead20ca2c549487167f56876ae47f1e1a4`; lane HEAD at read time
`03f852b9629c`; no REA run, no download, no tool install. Disk guard checked before the
heavy pass: `/fast/scratch/hyaku` 39% used, 495.6G free.

## Verdict

**Contract fully reconstructed and measured; the v4 defect is confirmed as a SHARED
table+evaluator defect, and two porting hazards for `sqfs-triage-v5.py` are new
findings.** `tools/round-42/sqfs-triage-v4.py` (2839 lines, read in full) plus
`SKILL.md` rule block 21 (marker line 526, vocabulary 527, header 528, separator 529,
15 rule rows 530–544) and the frozen evaluator `tools/round-42/indep-eval-v4.py` are
documented in **`RevTriageV4/v4-contract.md`** (marker/craft-section grammar; 13-column
order with the 9 scored / 2 output / 2 documentation columns; per-column cell grammars;
`fnmatch.fnmatchcase` glob semantics with the squashfs-prefix + KNOWN_HANDLERS liveness
guards; first-match-wins row precedence with HF→F fallback; the evaluator's 15-step
expected-label derivation with its tie-breaks; and pair-level mismatch semantics).

1. **All four v2ns `_ddefault` recon envelopes label `clean`/`none` today — measured on
   BOTH the frozen interpreter (rule 14, SKILL:543) and the frozen evaluator (step 14),
   exit 0 each.** They agree on the wrong pair, so the C3 do-nothing control and the
   before-run `pair_mismatches` can only fire against the **v5 evaluator's new
   precedence**; scoring the v4 table with `indep-eval-v4.py` at the base reads 0
   mismatches. v5 verdict for the four (claim precedence, claims file :74-83):
   **`clean-unverified` / `record-unverified`**, decided by F={`squashfs_v2_nonstandard`}
   (no-reader family), G=∅, P=4>0, behind an unchanged OP/PV domain guard; BE=n/a and
   the HF fallback are unconsulted on this arm.
2. **New hazard H1: the v4 docstring over-claims a refusal the code does not
   implement** — lines 130/154 promise "duplicate label **or handler glob**" is a
   malformed table, but only duplicate labels are refused (v4:455-459). The v5
   instrument must implement the glob-duplication refusal or drop the sentence;
   copying it would re-introduce a false guarantee.
3. **New hazard H2: the reader-backed v1–v3 legacy set {v1, v2, v3, v3_ddwrt} is NOT
   expressible as one validated v4 handler glob.** `squashfs_v[123]*` matches all 7
   legacy families (the F1 defect); `squashfs_v[123]` matches {v1,v2,v3} and silently
   drops `squashfs_v3_ddwrt`; the cell grammar has no alternation and duplicate labels
   are refused. Narrowing the `legacy-body-failure` cell therefore REQUIRES a v5
   grammar change (extra row under a distinct label, cell alternation, or matcher
   change) — a silent `squashfs_v[123]` swap is the exact failure mode to attack in
   the mutation battery.

Also verified: `SKILL.md` bytes differ between the C1 freeze `435d41fd` and the base
`f890bbe` by +12 lines, ALL instrument-registry rows (`git diff --stat` + hunk review);
the craft-section v4 table is byte-identical and lines 526–544 hold at the freeze, the
base, and HEAD (`f890bbe..HEAD` SKILL diff empty; worktree clean). `PR`→`PV` feature
rename between the R42 w1 artifacts and the frozen interpreter is documented so
before/after receipts stay comparable.

## Findings table

| ID | Attacks | Command (cwd = lane root) | Exit | stdout sha256 (receipt here) | Finding |
|---|---|---|---|---|---|
| M1 | v4 parser/table vs lane SKILL.md | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only` | 0 | `65abca784fbaafc0318df5d05eee97036081f8a1a6aff96d38b5c2cbc76c510f` (`table-only-v4.out`) | Parses clean: 15 rules, marker line 526, actions line 527, 15-token vocabulary. |
| M2 | v4 labels on the four v2ns `_ddefault` envelopes | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --json <4 envelope.json paths>` | 0 | `3120ebb94f41d17b66ee373a7cb7fd940ff960c08ae8097127115e140ec07909` (`v4-v2ns-ddefault.json`) | All four → `clean`/`none`, rule 14; features F={v2ns}, HF fallback {v2ns}, G=∅, D=∅, BE=n/a, SR=no, P=4. |
| M3 | frozen evaluator selftest | `python3 -I -B tools/round-42/indep-eval-v4.py --selftest` | 0 | `b8971b6aaf22a93a962522b29da4e5a377c81329d7a0e6fcd333a7f801703040` (`indep-eval-v4-selftest.out`) | 45/45 pass; every step 1-15 and every (label, action) pair exercised; selftest pins the v2ns→`legacy-body-failure` mis-route as expected (eval:564-567). |
| M4 | frozen evaluator on the full recon corpus | `python3 -I -B tools/round-42/indep-eval-v4.py --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --out <scratch>/indep-eval-v4-recon.json` | 0 | `a36149a030ed18aaeee56e1f549933e88563affdb405a2d40c476f17029d0425` (`indep-eval-v4-recon.json`) | n=126, skipped=[]; the four v2ns `_ddefault` ids → `clean`/`none`/step 14 — evaluator agrees with the table on the defect. |
| M5 | freeze/base/HEAD SKILL bytes | `git show 435d41fd:SKILL.md \| sha256sum`; `git show f890bbe:SKILL.md \| sha256sum`; `git diff --stat 435d41fd f890bbe -- SKILL.md`; `git diff --stat f890bbe HEAD -- SKILL.md` | 0 | — | freeze `04a3a865…`, base=worktree `19046cf2…`; delta = +12 registry rows only; craft table byte-identical; no HEAD drift. |
| M6 | docstring-vs-code (H1) | `grep -n 'duplicate' tools/round-42/sqfs-triage-v4.py` | 0 | — | Claim at v4:130/154; enforcement only at v4:455-459 (labels). No glob-duplicate check exists; no selftest case covers it. |
| M7 | legacy-glob expressiveness (H2) | fnmatch analysis over `KNOWN_HANDLERS` (v4:226-240) + cases v4:1339-1371 | — | — | `squashfs_v[123]*`→7 families; `squashfs_v[123]`→3 (drops v3_ddwrt); no single-glob narrowing to the 4 reader-backed families exists. |
| M8 | evaluator provenance | `diff preview-precedence.py tools/round-42/indep-eval-v4.py` | 1 | — | Files differ (1477 lines): frozen is a typed rewrite with `LEGACY_HANDLER = re.compile(r"squashfs_v[123]($|_)")` (still matches v2ns/v3_broadcom/v3_nonstandard) and widened D/SR/BE/H sources — §7 of the contract lists each. |

## Inputs (sha256)

- `tools/round-42/sqfs-triage-v4.py` `497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9` (read in full, 2839 lines)
- `tools/round-42/indep-eval-v4.py` `7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301`
- `.ufo/waves/round-42/w1/artifacts/R42C2ControlTables/preview-precedence.py` `47a6bed5c3d49c2bf3c6b0603c57c79f9198a850f80326beb7e76ce04a6517b1`
- `tools/round-42/c2-controls.py` `09b3c013b84d2488c6e160ae8087ce37df9a97a8ea88f26e189e5134c1c57e07`
- `SKILL.md` (worktree = base) `19046cf204ce999e5dccb1ebe86eebe9921e84ded8443dd87abc5a693fd8c974`
- the four `envelope.json` files: `636f84f5…`, `6f21e6ad…`, `55375dca…`, `57bb013f…` (full hashes in `RevTriageV4/v4-contract.md` §9)

## Deliverables

- `RevTriageV4/v4-contract.md` — the full contract (11 sections, line citations) + receipts R1-R4 copied here.
- `RevTriageV4/` — `table-only-v4.out/.err`, `v4-v2ns-ddefault.json/.err`,
  `indep-eval-v4-selftest.out`, `indep-eval-v4-recon.json`.

## Limits

- M2/M4 measure labels, not REA behaviour; no REA run this wave (contract).
- "UTC time" per receipt = file mtime of the captured output (stat in `RevTriageV4/`), session date 2026-10-29; per-command wall times were not otherwise recorded.
- The v5 evaluator verdicts in contract §9 are derived from the frozen claim text
  (`plans/round-50-attempt2-claims.md:74-83`), not from a v5 binary — none exists yet.
- Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-RevTriageV4` removed after receipts were copied.
