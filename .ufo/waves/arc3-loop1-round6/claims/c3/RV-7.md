# RV-7 — c3 chain (depth): rule #15 draft + citation list, all numbers re-derived first-hand

Seat: RV-7, wave arc3-loop1-round6, kaidoku-shokunin. Measured 2026-10-19 at
HEAD `c625d5d` / work `58c3db7` (both re-measured this seat; working tree clean
for `corpus/` and `SKILL.md` — `git status --porcelain corpus/ SKILL.md` empty).
Evidence: `…/claims/c3/RV-7/` (this dir; scratch work under `/var/tmp/rv7-c3/`).

## 1. Baseline re-derivation (first-hand, both revs)

Command A (SCORECARD.md:88-124 recipe, run verbatim via `git show` objects):

- `58c3db7` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}` — `RV-7/commandA-before.txt`
- `c625d5d` → identical numbers (`rule_blocks=14`, 84/84, depth 10.0).

14 rules enumerated mechanically at `58c3db7:SKILL.md` (split `^- \*\*` inside
`## Queue-drain craft`, section starting SKILL.md:81): 1 evidence-id
content-addressing, 2 vaddr +0x100000 shift, 3 refusal families, 4 authority
grades, 5 shape-gated input contracts, 6 caller-attested module attribution,
7 tool acceptance ≠ correctness, 8 census rows can be defects, 9 verify the
gate not the hint, 10 stanza-key+receipt citations, 11 config pre/post-pair,
12 Ghidra runs as user services, 13 natural control, 14 byte-identity
re-derivation (ends :255). → frozen claim "rules #1-14" VERIFIED.

## 2. Candidate evaluation (why (c))

- **(a) census-checked vs instrument-graded — UNLANDABLE this round.** Zero
  corpus grounding: `grep -rni "instrument|clause-level|blind spot"
  corpus/knowledge/` returns only REA-verb-census / doctor-blind-spot senses,
  none about the C1 gate. A rule with no `corpus/knowledge/` ref is invalid
  under command A's checker (`valid = bool(refs)`), so landing (a) today moves
  `rule_blocks` 14→15 but `citation_resolved_rules` stays 14 → depth_score
  10·14/15 = **9.33, a regression** against the claim's own falsifiable
  ("citations resolving under command A's pattern"). It needs a corpus entry
  first (C2 territory).
- **(b) coupled-landing discipline — feasible but thin.** Corpus grounding is
  two spots: `corpus/knowledge/2026-10-13-ghidra-install.md:74-76` ("repaired
  to 34 in the same commit as this erratum … coupled PROVINCE repair") and
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` ("superseded at
  the same commit … landing commit `40de383` writes `Core, arc3-r1/r3` … into
  `PROVINCE.md:91-93`"). Real, but a one-fact rule.
- **(c) parsed-and-empty ≠ byte-absence — CHOSEN.** Three-round lineage with
  original claim + append-only correction in each entry, plus the QUALITY gate
  row, plus this seat's first-hand re-derivation of every byte fact (§4). The
  claims-frozen names it "the sweep's biggest catch".

## 3. Rule #15 draft (patch TEXT — parent lands; SKILL.md untouched by this seat)

Insert after rule 14's final line (current SKILL.md:255), before the `## Config
custody` section. Unified diff of the simulated landing:
`RV-7/rule15-landing.patch.txt`; bullet text: `RV-7/rule15-bullet.md`.

```markdown
- **Parsed-and-empty is not byte-absence: a 0-function probe result is a
  parser-scope statement, and "absent" may be written only after a byte search
  of the same input locates nothing.** The class earned its keep across the
  EVM rounds: r1 recorded creation-code probes as 0 functions and wrote
  "creation blobs carry no runtime dispatch table", corrected append-only once
  a byte census found the runtime and its five compare sites embedded in the
  initcode (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`,
  corrected at :31); round 5 re-derived the same facts for the r3/r4 carriers
  — each runtime sits byte-exactly inside its initcode blob (VaultB opt200
  1,621 B at +34 in 1,655 B; CarrierV 1,562 B at +20 in 1,637 B) while every
  creation-code probe still reads exit 0 / 0 functions
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51`;
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46`, original claim
  :17). The corrected form is "creation probes parse empty while the runtime
  bytes are present verbatim"
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46`); the same
  discipline separates a probe-input trap (raw-over-hextext: exit 0, decoded
  sha = the hex *text* file's own sha — a costume, not a carrier) from a
  carrier defect
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:27`,
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:25`), per the entry
  gate that an empty/zero finding must state which of the two it is
  (`corpus/QUALITY.md:21`, row 11).
```

The rule deliberately does NOT repeat the r3 erratum's `:24` attribution —
that pointer is dangling (§6, finding F1).

## 4. Citation list — each anchor verified first-hand at `58c3db7`

Command A pattern `corpus/knowledge/<name>.md:<n>[-<m>]`; bounds = 1 ≤ start ≤
end ≤ line count (r1 file = 46 lines, r3 = 57, r4 = 63); content anchors
grepped at the measured rev (all match=1):

| Citation | Bounds | Content anchor re-derived |
|---|---|---|
| `2026-10-19-arc3-r1-evm-real-solc.md:24` | 24≤46 ✓ | "Creation blobs carry no runtime dispatch table" verbatim |
| `…r1…:31` (continuation) | 31≤46 ✓ | "(a) … is measured false — `Rv2Token.creation.hex` (1,971 B) embeds the runtime and its five `EQ;PUSH2;JUMPI` sites" |
| `2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51` | 41≤51≤57 ✓ | erratum "corrected … parsed-and-empty … runtimes byte-exactly embedded" |
| `…r3…:27` | 27≤57 ✓ | "parsed-and-empty, a probe-input trap, not a carrier defect" |
| `2026-10-19-arc3-r4-evm-vyper-leg.md:39-46` | 39≤46≤63 ✓ | erratum "corrected … 'creation probes parse empty while the runtime bytes are present verbatim'" |
| `…r4…:17` (continuation) | 17≤63 ✓ | original "uniformly **parsed-and-empty** (exit 0, 0 functions)" |
| `…r4…:25` | 25≤63 ✓ | "raw-over-hextext exits 0 … parsed-and-empty, the r1/r3 trap class" |
| `corpus/QUALITY.md:21` (gate row 11) | n/a — outside command A's pattern, provenance only | "Empty/zero findings must state whether the surface was parsed-and-empty or excluded-from-inventory" |

## 5. The rule's earned facts re-derived first-hand (no prior-seat values quoted)

`RV-7/byte-embed-derivation.txt` — python `bytes.find` over the retained
artifacts (unhexlified where stored as text):

- CarrierV: creation 1,637 B sha256`3c667396…`; runtime 1,562 B `57d6fd0a…`
  embedded at **+20**, 1 occurrence (r4:39-46's +20/1,637 — VERIFIED).
- VaultB opt200: 1,621 B `b24a0115…` at **+34** in 1,655 B (r3:41-51 — VERIFIED).
- VaultB nopt: 3,163 B `bcdf64ab…` at **+80** in 3,243 B (VERIFIED).
- CarrierB: 1,469 B `b9c70178…` at **+91** in 1,560 B `6794c3a2…` (VERIFIED).
- Smoke @r4: 168 B `415e6b1b…` at **+27** in 248 B (VERIFIED).
- Rv2Token @r1: 1,943 B `c1081a56…` at **+28** in a 1,971 B creation, and the
  creation carries exactly **5** compare-site patterns — r1:31(a)'s "1,971 B
  embeds the runtime and its five EQ;PUSH2;JUMPI sites" VERIFIED (note: the
  RV-2 retained files carry `0x` prefixes; stripped before decode).

Live probe re-deriving the parsed-and-empty leg (first-hand this seat,
`RV-7/probe-CarrierV-creation-6.4.0.json`):

```
TMPDIR=/var/tmp/rv7-c3 npx -y rea-agents@6.4.0 inspect-evm-interface \
  /var/tmp/rv7-c3/CarrierV.creation.hex hex --format json   → exit 0
functions: 0; bytecode.kind "unknown"; decoded bytecode.sha256 3c6673966d821d9d…
(= the decoded 1,637 B creation's own sha re-derived above); input file sha256
34f52280d3cdc740… (= r4:12's recorded creation hex carrier); evidence_id
ev_7a8403967a6e1e1a…
```

The same input carries the 1,562 B runtime at +20 (above): probe says 0
functions, bytes say present — the distinction, proven in one measurement pair.

## 6. Review findings

- **F1 (DISCREPANCY — r3 erratum's `:24` pointer is dangling).** The r3
  erratum at `…r3…:41` claims to correct "`:24` 'Creation blobs carry no
  runtime dispatch table'". That sentence never existed in the r3 entry at any
  revision: greps at `c418be0` (round-3 landing), `40de383`, `58c3db7` find
  "Creation blobs" only inside the erratum itself; r3's line 24 is the
  Rv2TokenOpt RESULT row at every revision; r3's "creation" occurrences are
  file-path contexts (:5, :12-14, :37). The quoted sentence is r1's (r1:24),
  already corrected at r1:31(a) in round 3. The erratum's byte facts are true
  (re-derived §5); only the attribution is wrong. Evidence:
  `RV-7/r3-erratum-dangling-pointer.txt`. Suggested disposition for the next
  append-only pass: re-point the quote to r1:24 or drop the `:24` pointer.
  The rule text in §3 avoids propagating it.
- **F2 (VERIFIED with a serialization note).** r1:31(a)'s "1,971 B" is the
  decoded-byte domain; the retained `Rv2Token.creation.hex` file is ASCII-hex
  text (`0x`-prefixed). Both domains re-derived (`04e07f54…` decoded; file
  text sha256 recorded in byte-embed-derivation.txt) — consistent with the
  lane's two-byte-domains discipline (cf. the r1:39-46 Smoke erratum).
- **F3 (choice constraint, for CN/VZ).** Landing candidate (a) before a corpus
  entry exists would drop depth_score to 9.33; if the wave wants (a) too, the
  corpus entry must land first (same-commit coupling — candidate (b)'s own
  lesson).

## 7. Falsifiable before → after (demonstrated on a scratch tree)

- BEFORE (`RV-7/commandA-before.txt`): `rule_blocks=14`,
  `citation_resolved_rules=14`, `depth_score=10.0` at `58c3db7` and `c625d5d`.
- AFTER (simulated landing — rule 15 appended to `58c3db7:SKILL.md` in
  `/var/tmp/rv7-c3/SKILL.simulated.md`, same checker logic, corpus untouched;
  `RV-7/commandA-after-simulated.txt`): `rule_blocks=15`,
  `citation_resolved_rules=15`, `depth_score=10.0`. All 6 rule-15 corpus refs
  resolve in-bounds; no existing rule or counter altered (the patch only
  inserts; `RV-7/rule15-landing.patch.txt`, +24/−2 blank-line normalization).

## 8. Per-item verdicts

| Item | Verdict |
|---|---|
| `rule_blocks=14` baseline (claim text) | VERIFIED (both revs, first-hand) |
| knowledge_files 84 / mapped 84 / missing [] / dangling [] | VERIFIED (both revs) |
| Rules #1-14 enumeration, craft section SKILL.md:81-255 | VERIFIED |
| Candidate (c) corpus lineage (r1:24/:31, r3:27/:41-51, r4:17/:25/:39-46, QUALITY.md:21) | VERIFIED (bounds + content anchors, §4) |
| r3/r4/r1 erratum byte-embedding facts (7 measurements) | REPRODUCED first-hand (§5) |
| Parsed-and-empty live behavior (exit 0, 0 functions, kind unknown) | REPRODUCED first-hand (§5 probe) |
| r3 erratum's `:24` premise attribution | DISCREPANCY (F1) |
| Candidate (a) landability this round | CORRECTED — unlandable without a corpus entry (F3) |
| rule_blocks 14 → 15 with all citations resolving | REPRODUCED on scratch tree (§7) |

## 9. Handoff to parent

Land §3's bullet after SKILL.md:255 (see `rule15-landing.patch.txt`), then
command A should read `rule_blocks=15, citation_resolved_rules=15,
depth_score=10.0`, all other counters unchanged. Consider queueing F1 as an
append-only pointer erratum for the r3 entry in a later round (this seat did
not touch the corpus). Scratch artifacts live under `/var/tmp/rv7-c3/` (not
`/tmp` — EDQUOT).
