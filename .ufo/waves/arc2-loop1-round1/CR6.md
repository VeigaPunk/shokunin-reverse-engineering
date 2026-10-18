# CR6 — critic: separability attack on C2 × C3 (one move wearing two hats?)

Seat CR6, wave arc2-loop1-round1, 2026-10-18. Read-only over the repo; the only
repo write is this report. All commands below were run by this seat this session
in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; scratch confined to
`/tmp/arc2-l1r1-CR6/`.

## 0. Verdict

**ONE-MOVE CHARGE REFUTED at draft level — but the refutation is textual, not
instrumental.** The strongest conflation case (single motivating defect; rule 10
prescribes exactly what C2 does; one state change resolves both) fails the
protocol's separability test in **both directions**: C2's acceptance test passes
with C3 unlanded (drift check rc=0, 3× OK, SKILL.md still at 9 rules), and C3's
acceptance test passes at revisions that predate this entire round (10/10 at
`18dc397d` and `40162fc`, 2026-10-16), with all three drafted rule texts free of
any this-round reference. **Residual weakness the charge does establish:** recipe
A is content-blind and path-blind — a rule that merely *restates C2* (including
one naming this round's receipt path in prose) also scores 10/10 — so C3's
separability from C2 rests on the landed rule text citing only pre-existing
loci, and the measurement cannot detect a violation. Landing guard in §4.

## 1. The strongest one-move case (steelman, as constructed)

1. **One defect, two ledger rows.** Both claims exist only because of a single
   defect — luna-round-8's missing pre-pair, recorded at `SCORECARD.md:544-545`,
   `LOG.md:856-858`, and `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`
   ("No config-drift pair."). C2 "closes" it; C3 "codifies" it.
2. **Same substance.** Rule 10's prescriptive content (freeze client-config
   sha256 pre-dispatch, re-verify post-battery, no pre-pair ⇒ claim void) is
   C2's custody procedure generalized — the E17/E18/P4 drafts describe the same
   act C2's receipts perform (E18.md:68-71; P4.md:18-25).
3. **The instrument cannot tell them apart.** Recipe A certifies "a 10th rule
   block carrying ≥1 in-bounds `corpus/knowledge` anchor" — nothing about
   content, and `.ufo/waves/...` mentions are invisible to its regex. So the
   depth delta 9→10 could be read as bookkeeping of C2's own act, and no
   measurement would object.
4. **Drafting-lane coupling.** C2's capability-row draft invokes C3's rule #10
   as its void-condition (`E14.md:76-79`); the two artifacts were written
   referencing each other, and the parent integrates the whole wave.
5. **One state change.** Executing the custody cycle (C2) and writing the rule
   (C3) could be narrated as one act recorded twice.

## 2. What refutes it — both counterfactuals, observed

**C2 is verifiable without C3 landed** (ran 2026-10-18T16:43:41Z, rule 10 not
landed — `grep -c '^- \*\*' SKILL.md` → `9`):

```
$ tail -n +2 .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt | sha256sum -c - ; echo rc=$?
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
rc=0
```

C2's acceptance test reads only the 3 config files + the receipt — never
SKILL.md. SKILL.md is byte-frozen since `638fb21` (luna-round-3):
`git diff 18dc397d HEAD -- SKILL.md | wc -l` → `0`; same vs `40162fc` → `0`.

**C3 is verifiable without C2's artifacts** — measured with each draft rule
inserted into a scratch copy of the worktree SKILL.md (all other reads via
`git show` at REV), through recipe A verbatim:

| variant | result |
|---|---|
| baseline, no rule | `rule_blocks 9, citation_resolved_rules 9, depth 10.0, 79/79` |
| E18 draft (12 lines) | `rule_blocks 10, citation_resolved_rules 10, depth 10.0, 79/79` |
| E17 draft (9 lines) | `rule_blocks 10, citation_resolved_rules 10, depth 10.0, 79/79` |
| P4 draft (8 lines) | `rule_blocks 10, citation_resolved_rules 10, depth 10.0, 79/79` |
| negative control (SCORECARD/LOG refs only) | `rule_blocks 10, citation_resolved_rules 9, depth 9.0` |
| C2-restatement rule + l8 anchor | `rule_blocks 10, citation_resolved_rules 10, depth 10.0` |
| neutral-topic rule + l8 anchor | `rule_blocks 10, citation_resolved_rules 10, depth 10.0` |

Same rule text, counterfactual revisions — commits from 2026-10-16, before this
round's receipts existed:

```
REV=18dc397d + E18 rule  → {"citation_resolved_rules": 10, "depth_score": 10.0, ..., "revision": "18dc397d", "rule_blocks": 10}
REV=40162fc + E18 rule  → {"citation_resolved_rules": 10, "depth_score": 10.0, ..., "revision": "40162fc", "rule_blocks": 10}
```

None of the three drafts references this round:
`grep -n "ufo\|receipt\|arc2" rule17.txt rule18.txt` → rc=1 (no hits);
same on the P4 draft → rc=1. C3's acceptance reads SKILL.md text + committed
`corpus/knowledge` line counts only.

**Independent failure surfaces** (the decisive point): C2 can fail — drift
detected → VOID per the drafted procedure (`E16.md:137`) — while rule 10 still
lands valid; C3 can fail — anchorless rule → 9/10, depth 9.0 (negative control
above) — while custody is perfect. Neither failure propagates to the other
claim. Distinct axes as declared (operability vs depth); the protocol test
(`AXES.md:31`, "each verifiable without the others having landed") is
verification-independence, and it holds in both directions.

## 3. The residual weakness the charge does establish

Recipe A certifies anchor presence, not content: a rule that merely restates
C2 — even one whose prose names
`.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt` — scores 10/10
(observed; the receipt path is invisible to the recipe's
`corpus/knowledge/([a-z0-9-]+\.md)` regex). If the *landed* rule 10 text were to
embed this round's receipt, the one-move charge would convert from refuted to
sustained (the rule would then be C2's record wearing the depth hat) and the
measurement would still read 10/10. The three existing drafts avoid this
(§2); the guard below makes the landed text checkable.

**Timing context (observed):** pre-pair receipt mtime `2026-10-18 11:49:13
-0300` (= `14:49:13Z`, matching its content timestamp); battery leg 1 ran
`11:51:50 -0300` (`E24.md:11`); leg 2 server `started_at`
`2026-10-18T14:53:21.522Z` (`E25.md:5`). The pre-pair predates both legs, so
"pre-dispatch" is satisfied for the two completed legs — leg 3 pending.
Receipt artifact sha256 reproduced this session:
`7369fbcb3bfd91cf5bdf48d0871ae670bce133d5d091a35e8fd7826c0cef04e4` (328 B),
matching `E11.md:76` / `V5.md:67`. C2's "receipts committed" clause is still
pending: `git ls-tree -r HEAD -- .ufo/waves/arc2-loop1-round1 | wc -l` → `0`;
`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round1/`.

**Transient hazard observed:** during this session `git status --porcelain`
briefly showed `?? corpus/knowledge/.r3-sim-tmp.md` (another seat's scratch,
gone by 16:44:58Z). Untracked files are invisible to recipe A (which reads
committed trees via `git ls-tree`), but if an integration commit swept such a
file, coverage would move 79→80 and the recorded numbers would break. Commit
named paths only.

## 4. Text for the parent — VERBATIM

```text
CR6 separability adjudication (C2 × C3) — one-move charge REFUTED at draft level; conditional on the landed rule text.
Both directions of the protocol's separability test (AXES.md:31) were exercised 2026-10-18:
- C2 without C3: `tail -n +2 .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt | sha256sum -c -` → 3× OK, rc 0 at 16:43:41Z while SKILL.md still carried 9 rule blocks (SKILL.md byte-frozen since 638fb21).
- C3 without C2: each of the E17/E18/P4 rule-10 drafts measures rule_blocks 10, citation_resolved_rules 10, depth 10.0 through recipe A; the same text scores 10/10 at revisions 18dc397d and 40162fc (2026-10-16), which predate this round's receipts; none of the three drafts references this round's artifacts.
Residual: recipe A is content-blind — a rule that merely restates C2 with the same l8-01:15 anchor also scores 10/10, and a `.ufo/waves/...` mention is invisible to its regex. C3's separability therefore rests on the landed rule text citing only pre-existing loci, not on the measurement.

Integration guard (run after committing rule 10; <REV> = that commit):
  git show <REV>:SKILL.md | awk '/^## Queue-drain craft/,/^## Checklists/' | grep -n "arc2\|receipt\|2026-10-18"   # must be empty — no this-round path in the landed rule
  REV=<REV> python3 - <<'PY' ... recipe A verbatim (SCORECARD.md:92-124) ... PY   # expect rule_blocks 10, citation_resolved_rules 10, depth_score 10.0, 79/79
  git status --porcelain   # commit named paths only — no stray files (one transient `?? corpus/knowledge/.r3-sim-tmp.md` was observed mid-wave)
```

## 5. Conclusions, labeled

- **Observation:** every number and byte in §2–§3 — recipe A at HEAD (`9/9,
  10.0, 79/79`) via the official recipe run verbatim and via an independent
  transcription (identical outputs); the six simulation variants; the two
  counterfactual-revision runs; the C2 drift check with rule 10 absent; the
  zero-hit greps on all three drafts; receipt hash/mtime; E24/E25 timestamps;
  the untracked wave dir; the transient stray file. Pointers verified by direct
  read this session: `SCORECARD.md:544-545`, `LOG.md:856-858`,
  `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15` (17-line
  file), `SKILL.md:81,86,108,118,137,151,162,170,175,187,197`,
  `E17.md:59-69`, `E18.md:67-80`, `P4.md:17-26`, `E14.md:76-79`, `E16.md:137`,
  `E24.md:11`, `E25.md:5`, `AXES.md:31` (fleet path, read-only).
- **Observation (concurrency):** `E16.md` was rewritten by its seat mid-wave
  (131 → 166 lines, mtime 13:42:15 -0300; the VOID clause moved from `:106` to
  `:137-139`). Its pointer in this report was re-resolved after the rewrite;
  the other seat files cited here were mtime-stable throughout. Cross-report
  pointers into live seat files are unstable until the wave closes.
- **Inference:** the one-move charge fails because the two claims have disjoint
  acceptance tests, disjoint landing artifacts (receipts + capability row vs
  SKILL.md insert), and independent failure modes; the shared subject and
  shared motivating defect are not the protocol's test. The charge survives
  only as a *landing-text* condition (§3), enforceable by the §4 guard.
- **Unknown:** whether the parent lands rule 10 and the C2 capability row in
  one commit (commit granularity does not affect separability, but one bad
  commit could void both); whether C2's post-battery drift check will hold at
  leg-3 time (this seat observed zero drift only through 16:43:41Z); the final
  chosen draft text (E17/E18/P4 differ in wording; all three measure 10/10).
- **Scope compliance:** no repo file edited except this report; no git
  mutations; no config reads beyond `sha256sum`/`stat`; no network; scratch
  confined to `/tmp/arc2-l1r1-CR6/`.
