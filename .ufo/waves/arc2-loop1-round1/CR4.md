# CR4 (critic) — C3 attack: is rule-10 generic agent advice violating "specialize, don't generalize"?

Seat CR4, wave arc2-loop1-round1, 2026-10-18. Repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at HEAD
`4b806e14db22ea44cc57729f5fa3f7b46b616178`; `git status --porcelain` → only
`?? .ufo/waves/arc2-loop1-round1/` (worktree == HEAD for every tracked file).
No repo file was modified; this report is my only repo-side write. Scratch is
confined to `/tmp/arc2-l1r1-CR4/` (my namespace only).

## Verdict

**NO VIOLATION.** Rule-10 as drafted by E17, E18 and P4 — and a hardened
11-line variant measured below — is in-class with the nine existing
queue-drain rules under the "specialize, don't generalize" invariant (fleet
`PROTOCOL.md:439`, restated `SKILL.md:189-190` in the fleet skill;
`corpus/QUALITY.md:13`). The attack's only landing ground is a **legibility
gradient**: rule-10 is the first queue-drain rule whose specificity is
pointer-carried rather than token-carried — zero REA entity tokens in its
body, where all nine existing rules carry at least one (census in §3). That
gradient does not make the text generic agent advice (test in §4), and it is
removable at zero measurement cost (§5 hardened variant: 10/10 resolvable,
depth 10.0, pure +11/−0 insertion — same measurement as all three drafts).

## 1. The invariant, read first-hand

- Fleet: `/home/vgpnk/.kimi-code/skills/shokunin/protocol/PROTOCOL.md:439`
  — "Specialize, don't generalize: a shokunin's `SKILL.md` contains *cited,
  verifiable* knowledge of its domain — never generic agent advice."
  (restated at `/home/vgpnk/.kimi-code/skills/shokunin/SKILL.md:189-190`).
- Repo admission criterion: `corpus/QUALITY.md:13` — "Domain-specific — no
  generic agent advice | PROTOCOL.md invariants".
- The test therefore decomposes into: (a) cited, (b) verifiable, (c) of its
  domain, (d) not generic agent advice. §4 applies it item by item.

## 2. Measurements (all run this session)

**2.1 Command A — baseline and independent draft sims.** Script extracted
from `SCORECARD.md:93-123` (the recipe A fence, `SCORECARD.md:92-124`);
sims replace only `get('SKILL.md')` with the worktree copy plus the report's
fenced block inserted after `SKILL.md:195` (blank line :196 and
`## Checklists` :197 preserved); every `corpus/knowledge` read still
`git show` at HEAD, `REV=4b806e14db22ea44cc57729f5fa3f7b46b616178`.

Baseline at HEAD:

```console
$ REV=$(git rev-parse HEAD); bash /tmp/arc2-l1r1-CR4/cmdA.sh
{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "4b806e14db22ea44cc57729f5fa3f7b46b616178", "rule_blocks": 9}
```

Draft blocks extracted mechanically from the reports (`sed` over the fences:
E17.md:60-68, 9 lines; E18.md:68-79, 12 lines; P4.md:18-25, 8 lines) and
re-measured:

```console
E17 sim (260 lines): {"citation_resolved_rules": 10, ..., "depth_score": 10.0, "rule_blocks": 10}
E18 sim (263 lines): {"citation_resolved_rules": 10, ..., "depth_score": 10.0, "rule_blocks": 10}
P4  sim (259 lines): {"citation_resolved_rules": 10, ..., "depth_score": 10.0, "rule_blocks": 10}
```

So C3's measurement (rules 9→10, 10/10 resolvable) reproduces independently
for all three drafts. Negative control (P4 block with its
`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15` citation
stripped):

```console
{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 9.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "4b806e14...", "rule_blocks": 10}
```

— reproduces P4.md:57-58's trap and confirms the corpus citation is both the
specificity anchor and the measurement anchor.

**2.2 The citations every draft rests on** (each read this session):

- `SCORECARD.md:544-545` → "Measured: command A 79/79, 9/9, 10.0/10.0 at
  `18dc397d`; config hashes / match the round-6 baseline (no round-8
  pre-pair — recorded)."
- `LOG.md:856-858` → "…zero / config drift closed against the round-6
  baseline (no round-8 pre-pair — / carried debt); six-of-37 scope stated
  in the entry's limitations."
- `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15` (17-line
  file) → "No config-drift pair."

## 3. Domain-specificity census — nine rules vs three drafts

Citation-stripped bodies (parenthetical `` `…` `` citations and bare
`corpus/knowledge/...` refs removed), REA-surface token regex over verb
names, typed refusals, env keys, provider names, carriers, authority-grade
names, and lane artifact names. First pass omitted backticked grade names
(rule 4 read as empty); corrected pass:

| rule | SKILL.md line | REA-surface tokens remaining in body |
|---|---|---|
| 1 | :86 | mkdtemp |
| 2 | :108 | DYN, ELF, Ghidra, PIE, glibc, jq, libgtk, libjq, outside-memory, vaddr |
| 3 | :118 | REA_BROWSER_EXECUTABLE, VALIDATION_ERROR, capability_unavailable, invalid_request, provider_unavailable |
| 4 | :137 | observed, inferred, shipped-artifact, analyst-inference, historical-reference, controlled-replay |
| 5 | :151 | createEvidenceBundle, inspect_artifact |
| 6 | :162 | analyze_function, glibc |
| 7 | :170 | trace-web-source-location |
| 8 | :175 | Queue-B |
| 9 | :187 | chromium, har-schema, netlog, pwntools, setuptools |
| E17 draft | insert after :195 | — (none) |
| E18 draft | insert after :195 | — (none) |
| P4 draft | insert after :195 | — (none; "6.4.0" only, not labeled as the REA pin) |

Nine rules: ≥1 token each. Three drafts: 0 each. That is the attack's real
edge, and it is real — recorded here as an observation, not dismissed.

## 4. Why zero tokens ≠ generic agent advice (the verdict's reasoning)

- **(c) Of its domain.** The operative term "drift-sensitive client
  configs" is an in-file defined lane term: `SKILL.md:22-26` — "Drift-
  sensitive values: `GHIDRA_INSTALL_DIR`, `JAVA_HOME` in the three client
  configs (devin/omp/kimi), the per-client REA pin (see current inventory
  above), the installed skill version." The pointer chain from rule-10's
  body resolves to REA-specific surfaces ~60 lines above the insertion
  point. "Custody" likewise has lane usage history (`SCORECARD.md:497`
  "custody defects recorded"; `LOG.md:807` "(custody; current bytes
  hash-match)").
- **(a)(b) Cited, verifiable.** Three citations, all resolving (§2.2), all
  recording *this lane's own* luna-round-8 defect. The section's declared
  admission rule is exactly this: `SKILL.md:83-84` — "each bullet is
  bounded by the lines it cites." Rule-10 conforms.
- **(d) Not generic agent advice.** Transplant test: move rule-10 into
  another lane's SKILL.md unchanged — "client configs" has no referent
  there without re-deriving this lane's surfaces (the three named configs,
  the env keys, the per-client pin). Generic advice survives transplant by
  definition; rule-10 does not. It also carries a falsifiable void
  condition ("a zero-drift claim without its own pre-pair is void") — none
  of the generic formulations ("always verify your environment") has one.
- **Species check.** The nine already mix empirical laws (1, 2, 4, 5, 6, 7)
  with process discipline distilled from recorded defects (3, 8, 9 —
  refusal families, census rows, provisioning hints). Rule-10 is process
  discipline of the same species: a custody requirement distilled from a
  recorded lane defect.
- **Precedent, read this session.** The fleet already treats "does rule X
  overgeneralize beyond its citations?" as a per-rule audit class:
  `.ufo/rounds/interactive-r1/wave-spec.json:66` (AddressSpace seat,
  targeting the +0x100000 rule: "Check whether the stated universal ELF
  PIE/DYN +0x100000 rule overgeneralizes beyond the concrete cited
  jq/libjq/glibc/libgtk imports … return a bounded finding, not a global
  correctness verdict"). Where the fleet did find true overgeneralization,
  the remedy was scoping *empirical* claims down to cited evidence:
  luna-round-3 `.ufo/waves/luna-round-3/M5.md:2` ("M2's
  'operation-family-specific' opener generalizes beyond the cited
  `analyze_function` family") and `C5.md:11` ("Keep the scope specifically
  `analyze_function`; do not generalize to all evidence-ID families"),
  landed as `QUALITY.md:25` (#15 supersedes #14). Rule-10 makes no
  empirical generalization — it prescribes a forward custody practice — so
  that remedy class does not apply.
- **Cross-check, read this session.** R4.md:75-87 reached the same
  in-class conclusion by a style/vocabulary route ("rule 10 is the same
  species (process discipline with a concrete threshold and a recorded
  prior defect), not generic agent advice (QUALITY.md criterion 3)"), and
  flagged the both-fences scenario (E17+E18 → 11 rules, 11/11, breaking
  the 9→10 claim). My §2 sims independently reproduce the 10/10 result
  that conclusion rests on.

## 5. Per-draft detail and the optional hardening

- **E17 (9 lines):** NO VIOLATION. "drift-sensitive" is in-file defined
  (`SKILL.md:22`); closest to rule 1's shape (bold claim, evidence
  sentences, prescriptive close).
- **E18 (12 lines):** NO VIOLATION; weakest on legibility — its key term
  "live-probe" resolves at `SCORECARD.md:461` ("remaining queue is
  live-probe re-verification of stale-held surfaces") but is not defined
  in SKILL.md; 12 lines is the longest rule in the section. R4.md:75-77
  made the same observation.
- **P4 (8 lines):** NO VIOLATION; note the scope wording — "pre/post-paired
  for every live-probe round" is a slightly broader forward commitment
  than the claim text ("required for any live-probe round's zero-drift
  claim"); it prescribes future practice rather than asserting past
  facts, so it is not an evidence-overgeneralization, but the parent owns
  the wording choice.
- **Hardened variant (mine, 11 lines, measured):** closes the legibility
  gradient by naming the lane surfaces inline; command A gives
  `{"citation_resolved_rules": 10, "rule_blocks": 10, "depth_score": 10.0}`
  and `git diff --no-index --numstat SKILL.md /tmp/arc2-l1r1-CR4/skill-CR4f.md`
  → `11  0` (pure insertion).

## 6. Verbatim text for the parent (optional; land INSTEAD of, never alongside, E17/E18/P4)

If landed: insert after `SKILL.md:195`, keeping the blank line before
`## Checklists` (:197). Landing this **and** any draft fence together gives
11 rule blocks and breaks the 9→10 claim (R4.md:84-87, corroborated by
E19.md). Exact bytes also at `/tmp/arc2-l1r1-CR4/rule10-final.txt`:

```markdown
- **Config custody is a pre/post-pair — a zero-drift claim without its own
  pre-pair is void.** luna-round-8 closed zero config drift against the
  round-6 baseline with no round-8 pre-pair — recorded as carried debt
  (`SCORECARD.md:544-545`; `LOG.md:856-858`) and stated as a limitation in
  the battery entry itself, "No config-drift pair"
  (`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`). Freeze
  the sha256 of the drift-sensitive client configs — the devin/omp/kimi
  client configs carrying `GHIDRA_INSTALL_DIR`/`JAVA_HOME` and the
  per-client REA pin — before dispatch and re-verify after the battery;
  only the bracketing pair supports a zero-drift claim — a post-only
  comparison is void, not a weaker grade.
```

## 7. Conclusions

- **Observation (ran/read this session):** command A at HEAD = 9 rules,
  9/9, depth 10.0 (§2.1); all three draft blocks measured independently →
  10 rules, 10/10, depth 10.0; negative control → 9/10, depth 9.0; the
  three cited defect sites resolve verbatim (§2.2); the token census of §3
  (nine rules ≥1 token, three drafts 0); `SKILL.md:22-26` defines
  "drift-sensitive"; `QUALITY.md:13` and `PROTOCOL.md:439` carry the
  invariant; `wave-spec.json:66` and luna-round-3 M5/C5 show the audit and
  remedy precedents; R4.md:75-87 read for cross-check; worktree == HEAD
  (no tracked file modified).
- **Inference:** rule-10 as drafted satisfies (a)-(d) of §4; its only
  measurable gap against the nine is token-carried specificity, which the
  §6 variant closes while preserving the exact 10/10/10.0 measurement. The
  C3 claim survives the attack in all four wordings; choosing a wording is
  a parent adjudication, not a claim defect.
- **Unknown:** (a) the AddressSpace seat's report under
  `.ufo/rounds/interactive-r1/` is not present in that directory (listing
  read this session — no `specialists/` subdir), so the fleet's own prior
  verdict on an analogous overgeneralization attack could not be cited;
  (b) the parent's final wording pick (E17/E18/P4/§6) and whether the
  `SKILL.md:83-84` header is amended in the same commit (E18.md:95-99
  flagged; outside C3's measurement); (c) whether "live-probe" needs an
  in-file definition if E18 is chosen.
