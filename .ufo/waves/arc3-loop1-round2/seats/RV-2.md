# SEAT RV-2 — wave arc3-loop1-round2, chain c1, role reviewer

Seat line: review the rule's citation set — every citation resolvable at HEAD, in
rule-#11 form (no bare line numbers into operator-mutable files).

Repo HEAD pinned at every sample: `14b1682b1128d2e41085ebc79c9addeb8786d420`
(`git rev-parse HEAD`). Writes: this report +
`.ufo/waves/arc3-loop1-round2/claims/c1/RV-2/` only. No git mutations in the lane
repo (the only `git init/commit` runs are in scratch fixture repos under
`/var/tmp/rv2/`, the committed-gate selftest pattern). No LOG/SCORECARD/SHONEN/
corpus/SKILL/README edits. Custody paths: one read-only capture
(`evidence/custody-readonly-capture.txt`), no byte written. Scratch: `/var/tmp/rv2`
(`/tmp` never used, standing EDQUOT record honored).

## VERDICT (citation set)

**CONDITIONAL PASS.**

- **Resolvable at HEAD — PASS for the landing text (EX-01 payload): 5/5**, and
  each cited range's content matches what the rule claims (`content-match.txt`).
  The 13 pre-existing rules: 54/54 in-repo citations resolve, 0 dead. Simulated
  work commit (full `git archive HEAD` tree + payload): 60 citation refs, 59
  in-repo resolved, 0 dead; the 60th is the path-only custody cite, out-of-repo.
- **Resolvable at HEAD — FAIL for the alternate v5 text (PL-1's block): 5/6**,
  one dead token `claims/c1/verdict.md` (absent from the repo root). If the
  integrator lands v5, it needs the one-token fix (`proposed-pl1-verdict-path.patch.md`,
  fixed form measured 6/6 dead 0).
- **PL-1's later `merged-rule-14-block.txt` (landed 12:19Z, after §1-4 were
  written) — PASSES BOTH CHECKS: 5/5 citations resolve, 0 dead, 0 form flags**
  (it cites SCORECARD/LOG by section key — the conforming form), command A 14/14
  in sim (`evidence/pl1-merged-audit.txt`). Two **text** defects, not citation
  defects, must be fixed before landing: the closing sentence occurs twice, and
  five continuation lines (15, 17-20) are unindented column-0 lines that would
  break the SKILL.md bullet they are meant to continue.
- **Rule-#11 form (no bare line numbers into operator-mutable files) — PASS for
  the custody class, 1 named soft flag.** No rule in the 14-rule set carries a
  line number into any of the 5 custody paths; the only custody mention is
  rule #11's own path-only `~/.kimi-code/config.toml` + stanza key + receipt
  (conforming). Flag: rule #14's `SCORECARD.md:1366-1368` — a bare line range
  into a file whose **head is rewritten in place** (pre-existing same-class flag:
  rule #12's `SCORECARD.md:544-545`). Measured: both ranges resolve at HEAD, the
  cited content matches, and SCORECARD.md's observed cadence is tail-append with
  line-neutral head rewrites (below). Under the strict reading of rule #11's
  escape clause ("a line number may appear only inside an append-only record that
  names its capture stamp") they are non-conforming; a one-sentence conforming
  rewrite is proposed in `proposed-rule14-citation-form.patch.md`. This flag does
  not affect command A, the census, or the probe.

## 1. Work performed (evidence pointers)

- Read the frozen wave claims (`claims-frozen.md:20-33,66-83`), the queue-drain
  rule block at HEAD (`SKILL.md:81-241`, 13 rules), rule #11's text
  (`SKILL.md:196-206`) and its landing record (`SCORECARD.md:865-880`), the
  round-4 boundary critique of rule #11 (`arc2-loop1-round4/CR1.md:10-60,190-262`),
  the committed citation instruments (`.ufo/gates/citation-drift/pointer-table.json`
  — 31 rows: exact 15 / extracted 11 / anchor 5; `expected.json`; `SCORECARD.md:88-124`
  recipe A), and the round-1 incident records read directly (CR-2 F2, VZ-1 D9,
  `SCORECARD.md:1366-1368`, `LOG.md:1411-1412`).
- **Built the seat's instrument** `claims/c1/RV-2/rule-citation-audit.py`
  (reads SKILL.md as a Git object; splits the craft section into rule blocks;
  extracts every `path[:line[-line]]` token including `~`-rooted and `/`-rooted
  paths; resolves each against the named revision; classifies targets by
  write-cadence — in-place-rewritten / append-only record / external-custody;
  flags bare line numbers into in-place/operator-mutable targets; `--block` mode
  audits a not-yet-landed draft against the tree; out-of-repo targets are
  stat/line-count captured read-only). Selftest builds isolated scratch fixture
  repos and requires the auditor to catch an injected dead line and an injected
  bare in-place line — `SELFTEST PASS` (`evidence/selftest.txt`).
- Baseline at HEAD: `audit-head-summary.txt` / `audit-head.json` —
  **13 rules, 55 citation tokens (54 in-repo + 1 custody), 54/54 in-repo
  resolved, 0 dead, 1 form flag** (rule #12 `SCORECARD.md:544-545`). Independent
  cross-enumeration (a second regex over the same section) returned the same
  token set, and command A agrees at 13/13, 82/82 (below).
- Rule #14 candidates audited before/at landing: CR-1 T1/T2/T3, EX-05 fallback,
  EX-01 payload, PL-1 v5, PL-1 merged (`evidence/candidate-verdicts.txt`,
  `evidence/pl1-merged-audit.txt`) — each against HEAD in `--block` mode.
- **Work-commit simulation**: `git archive HEAD` → `/var/tmp/rv2/full`, EX-01's
  payload inserted after `SKILL.md:239`; post-image **385 lines, sha256
  `19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90`** — byte-equal
  to EX-01's `identity-final.txt` claim (the rule's own identity discipline
  checked against its own artifact; the payload block between the markers is
  896 B, sha256 `a47dc38d…`, also byte-equal). Full-set audit there:
  `audit-work-sim-summary.txt` / `audit-work-sim.json` (60 refs, 0 dead, the two
  named form flags); prefix check `cmp` → first 239 lines byte-identical
  (`commandA-sim-work-commit.txt`).
- Read-only custody capture (`evidence/custody-readonly-capture.txt`):
  `~/.kimi-code/config.toml` sha256 `8cbacd48…73c38d`, inode 34530637, mtime/ctime
  2026-10-18 23:20:43 -0300; `[mcp_servers.rea]` at line 3544, pin `rea-agents@6.7.0`
  unchanged. No write/chmod/touch.

## 2. Proposed changes (patch text, none applied)

- `claims/c1/RV-2/proposed-rule14-citation-form.patch.md` — one-sentence
  conforming rewrite of the payload's `SCORECARD.md:1366-1368` citation to the
  section-key form (rule #11 form), plus the alternative of recording the
  adjudication if the bare range is kept. Command-A-neutral; content anchor and
  LOG.md citation unchanged.
- `claims/c1/RV-2/proposed-pl1-verdict-path.patch.md` — one-token fix for PL-1's
  v5 block: `claims/c1/verdict.md` → `.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md`;
  fixed form measured `citations 6 | resolved 6 | dead 0`.
- No repo edit is proposed against SKILL.md itself by this seat (the rule text is
  EX-01/PL-1's; the integrator applies one of them).

## 3. Before → after measurement for chain c1's claim

| Check | Before (HEAD `14b1682b…`) | After (simulated work commit `bcf158b3…` = full HEAD tree + EX-01 payload) |
|---|---|---|
| command A (recipe `SCORECARD.md:88-124`) | `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "HEAD", "rule_blocks": 13}` | `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "HEAD", "rule_blocks": 14}` (`commandA-sim-work-commit.txt`) |
| rule-citation audit (this seat) | 13 rules, 55 refs, 54 resolved, 0 dead, 1 form flag | 14 rules, 60 refs, 59 resolved, 0 dead, 2 form flags (`audit-work-sim-summary.txt`) |
| prior-13 byte-identity | — | first 239 lines byte-identical (`cmp` exit 0); pure insertion after rule #13 |
| needle scan (EX-05's tool, payload diff) | — | `added_lines=14 needle_hits=0`, exit 0 (`needle-scan.txt`) |
| citation content match (all 5 new refs) | — | every cited line holds the claimed fact: entry `:7` = recheck line; CR-2 `:86-89` = 8,316 B/`f95c5a05…` vs 8,598 B/`d8d85949…`; VZ-1 `:115` = `9,513 B ≠ claimed 8,316 B`; SCORECARD `:1366-1368` = "fresh identity recorded (10,225 B, sha256 `dd986f56…`"; LOG `:1411-1412` = same identity (`content-match.txt`) |
| SCORECARD write-cadence (form evidence) | — | every hunk `a280e07→14b1682` is either line-neutral (`-53,11 +53,11`, `-65,11 +65,11`) or a tail append (`-557,3 +557,861`, `-1334,3 +1334,84`); landmark `:544` held across all 8 recorded revisions while the file grew 1095→1417 lines; `## Measurement recipes` held at `:86` (`scorcard-cadence.txt`) |
| candidate texts | T1: 3 refs, 0 dead, 0 flags, **0 corpus refs** → command A 13/14, depth 9.29 (measured in sim `784ad32`) · EX-05 fallback: 1 ref, 0 dead, 0 flags → 14/14 (`c882e6f`) · EX-01 payload: 5 refs, 0 dead, 1 flag → 14/14 · PL-1 v5: 6 refs, **1 dead**, 0 flags · PL-1 merged: 5 refs, 0 dead, 0 flags → 14/14 (`29b60de`), 2 text defects (`candidate-verdicts.txt`, `pl1-merged-audit.txt`) | — |

## 4. Attacks / refutations attempted (verdicts)

| # | Attack | Method | Verdict |
|---|---|---|---|
| A1 | "the citation set only resolves because nobody applied it yet" | applied EX-01's payload to a full `git archive HEAD` tree and re-ran both the audit and command A there | **refuted** — 59/60 in-repo refs resolve in the patched tree; the landing is a pure tail insertion, so no pre-existing cited target changes |
| A2 | "the new rule's citations are line numbers that will drift like config.toml" | classified every token by target write-cadence; scanned for custody-path line numbers in all 14 rules | **refuted for the churner class** — zero line numbers into any custody path; **sustained for SCORECARD.md** (2 soft flags, named) |
| A3 | "resolving line numbers is enough; content could be stale" | read all 5 cited ranges at HEAD and matched them against the rule's claims | **refuted** — all five match exactly (incl. both stale hashes and the landed `dd986f56…`) |
| A4 | "a corpus citation is decoration — T2/T3 pass without evidencing the incident" | measured all candidates under command A in scratch sims (fresh reset per candidate) | **partially sustained** (CR-1's T3 argument reproduced): command A cannot discriminate craft from decoration; T1's incident-only text scores 9.29 while a content-free text scores 10.0. Recommended the incident-anchored corpus citation (the landed entry, `:5-7` or `:7`) so the counted citation is the incident's own record, not an adjacent file |
| A5 | "the payload's own self-identity is stale (the rule's own failure mode)" | re-derived payload bytes (896 B / `a47dc38d…`) and the post-image (385 lines / `19057c13…`) from the artifact | **refuted** — byte-exact; EX-01's identity block is fresh |
| A6 | "the SCORECARD line range is dead or soon-dead" | hunk analysis + landmark history across every recorded SCORECARD revision | **refuted on measurement** (the range is live and the writer has never inserted above it) — **but the form guarantee is absent**, hence the flag and the proposed rewrite, not a dead-citation verdict |
| A7 | "my checker only proves what I coded" | selftest injects a dead line and a bare in-place line into fixture repos; two independent enumerations (two regexes) and command A agree on the baseline set | **refuted** — `SELFTEST PASS`; enumerations agree set-for-set (55 tokens) |
| A8 | "PL-1 v5 (the alternate text) is equivalent on citations" | audited v5 and ran the literal path check | **sustained as a defect** — `claims/c1/verdict.md` resolves nowhere from the repo root; fix proposed and re-measured 6/6 |
| A9 | "the merged block is quote-ready because its citations pass" | audited PL-1's `merged-rule-14-block.txt` and flattened its text | **sustained as a text defect** — closing sentence duplicated (2 occurrences); continuation lines 15, 17-20 sit at column 0 and would break the bullet; citation set itself is clean (5/5, 0 flags) |

## 5. Blockers / named gaps

- No seat blocked on me; no blocker on this seat. The chain's candidate choice
  (EX-01 payload vs PL-1 v5 vs PL-1 merged) is the integrator's; this report
  gives the citation verdict for all three. **Recommended landing:** PL-1's
  merged block (only candidate scoring 5/5 resolved with 0 form flags and a
  resolving corpus citation) after fixing its two text defects; EX-01's payload
  is equally resolvable and carries the corpus/verdict chain differently, but
  needs either the one-sentence form rewrite or an explicitly recorded
  adjudication for `SCORECARD.md:1366-1368`.
- Named gaps at this write: CR-1's and SC-1's seat reports had not landed
  (`seats/` polled from 12:00Z: RV-1, EX-01, CU-1 present; VZ-1's C1 convergence
  verdict absent). My checks did not depend on them; RV-1's independent
  measurements (T1 9.29 / T2 14/14) agree with mine.
- Boundary of claim: "resolvable at HEAD" is measured against the pinned
  revision and against my scratch work-commit simulation; the literal
  work-commit rerun after the integrator lands remains owed by the round's
  records (precedent: round-1 VZ-1 E7).
- One measurement discrepancy noted in a peer artifact, not mine: EX-02's
  `citation-range-check.txt` prints the entry as "file lines=34"; at HEAD it is
  33 lines under `splitlines()` (`wc -l` 33, worktree 33), which is command A's
  own counting method. No verdict changes — but a range check should use the
  instrument's counting method.
