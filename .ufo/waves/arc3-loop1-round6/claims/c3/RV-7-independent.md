# RV-7 (independent verification dispatch) — c3 depth: SC-3's rule #15 re-derived, one wrong citation corrected

Seat: RV-7, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19.
Repo HEAD `c625d5d` (records; work `58c3db7`), both re-measured this seat.
Evidence: `…/claims/c3/RV-7-independent/`; scratch `/var/tmp/rv7-verify/`
(never `/tmp`). Write scope honored: only this artifact dir; `SKILL.md`,
`corpus/`, gates and all tracked files read-only; git untouched.

**Path-collision note (for the parent).** A concurrent dispatch already wrote
`claims/c3/RV-7.md` (mtime 2026-10-19 13:32) with its own rule-15 draft and
F1 finding. I did not overwrite or edit it; this file is the independent
verification artifact for the same seat name. Both should be read together:
the peer's artifact is `claims/c3/RV-7.md`, mine is this one.

## 1. Baseline — command A at both revs

Recipe verbatim from `SCORECARD.md:88-124` (`/var/tmp/rv7-verify/cmdA.py`):

| rev | rule_blocks | citation_resolved_rules | depth_score | knowledge_files | mapped | missing | dangling | coverage |
|---|---|---|---|---|---|---|---|---|
| `c625d5d` | 14 | 14 | 10.0 | 84 | 84 | [] | [] | 10.0 |
| `58c3db7` | 14 | 14 | 10.0 | 84 | 84 | [] | [] | 10.0 |

Exact JSON: `RV-7-independent/cmdA-c625d5d-before.json`,
`…/cmdA-58c3db7-before.json`. Verdict: frozen "before" values **REPRODUCED**
first-hand at both revs. `git diff --stat c625d5d 58c3db7 -- SKILL.md` is
empty; the craft section ends at `SKILL.md:255` ("never a carried-over
number."), before four blank lines and `## Config custody …`.

## 2. SC-3's draft — identity and structural parse

Extracted from the ` ```markdown ` fence in `claims/c3/SC-3.md` §4:

```
1605 bytes, 23 lines, sha256 763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1
```

- 1 rule-block start (`^- \*\*`), 8 `corpus/knowledge/` refs — **VERIFIED**.
- Insertion after the unique anchor `never a carried-over number.\n` adds
  exactly +23 lines (390 → 413) and nothing else
  (`RV-7-independent/skill-landing.diff`, `SKILL-*-simulated.md`).
- The draft's own self-identity claim (1,605 B / 23 lines / `763c44b5…`) is
  byte-exact — **VERIFIED**.

## 3. Scratch landing and sensitivity

SKILL.md is outside this seat's write scope, so "after" was measured by
appending `rule15-sc3.txt` to `git show <rev>:SKILL.md` in `/var/tmp` and
running command A's exact split/citation logic (corpus files still read from
the rev via `git show`):

| rev | before (blocks/resolved/depth) | after (blocks/resolved/depth) |
|---|---|---|
| `c625d5d` | 14 / 14 / 10.0 | **15 / 15 / 10.0** |
| `58c3db7` | 14 / 14 / 10.0 | **15 / 15 / 10.0** |

Per-rule ref counts after landing: `10,4,8,5,4,2,1,6,3,1,1,2,2,1` for rules
1–14 (identical to before) plus `8` for rule 15. All other counters
unchanged (`84/84`, `missing []`, `dangling []`, `coverage 10.0`).
Verdict: the frozen falsifiable "rule_blocks 14 → 15 with the new rule's
citations resolving" — **REPRODUCED** at both revs.

Fault arm (`RV-7-independent/fault-arm.txt`): an out-of-bounds citation
(`r4:39-46` → `:39-64`, file is 63 lines) drops to **15 blocks / 14
resolved / 9.33**; a missing file does the same. The arm is sensitive — the
"after" 15/15 is not vacuous.

## 4. F1 — one citation is content-wrong (CORRECTED)

All 8 pattern citations resolve **by bounds** (8/8); the audit is in
`RV-7-independent/citation-audit.txt`. Content anchors:

| citation | anchor | verdict |
|---|---|---|
| `…r1-evm-real-solc.md:24` | "Creation blobs carry no runtime dispatch table" | present (original-claim locus) |
| `…r1…:31` | "not byte-level absence" | present |
| `…r3-evm-optimizer-shapes.md:41-51` | "byte-exactly embedded" | present |
| `…r4-evm-vyper-leg.md:39-46` | "creation probes parse empty while the runtime bytes are present verbatim" | present (:46) |
| `…r4…:17` | "uniformly **parsed-and-empty**" | present |
| `…r3…:27` | "a probe-input trap, not a carrier defect" | present |
| `…r4…:25` | "parsed-and-empty, the r1/r3 trap class" | present |
| `…r4…:34` | "empty results do not prove absence of dispatch" | **ABSENT — quote is at `:29`** |

`r4:34` is the `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`
header. The quoted sentence sits at `r4:29` (the Limitations line). This is a
real defect in the text that would land in SKILL.md; it survives command A
because the checker validates bounds only (§6). The non-pattern
`corpus/QUALITY.md:21` citation (row 11) is exact — **VERIFIED**.

**Corrected variant delivered**:
`RV-7-independent/rule15-sc3-corrected.txt` — the same draft with only
`…r4-evm-vyper-leg.md:34` → `…:29`. Fresh identity (craft rule 14: a revision
re-derives its own identity): **1,605 B, 23 lines, sha256
`6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`**; it
lands 15/15/10.0 on scratch. Landing the original instead leaves a wrong
line pointer inside SKILL.md until an append-only correction, and that
correction mints yet another identity.

## 5. The rule's earned facts — first-hand

`RV-7-independent/byte-embedding.txt`:

- **CarrierV** (r4 EX-04/out): creation 1,637 B sha `3c667396…`; runtime
  1,562 B sha `57d6fd0a…`; `runtime.hex` decodes byte-identical to
  `runtime.bin`; runtime occurs once at **+20**, 55 trailing bytes —
  **REPRODUCED** (SC-3 §3 and `r4:43-44`).
- **Live probe** (CarrierV creation, 6.4.0, disk-backed TMPDIR): rc 0,
  functions **0**, `kind "unknown"`, decoded sha `3c667396…`, subject
  `34f52280…`, evidence `ev_53732d0f8c67d15c…` — **REPRODUCED exactly**,
  including the id SC-3 reported (relative vs absolute path resolve to the
  same absolute file).
- Sealed corroboration: `EX-06/probe/CarrierV-creation-6.4.0.json` has the
  same id and 0 functions; `r1 RV-2/probe-creation-hex-6.4.0.json` is
  `ev_c80379e1…`, 0 functions. These are same-path re-reads, not independent
  corroboration; the byte census is the independent half.
- **The rule's plural "r1 creation legs … byte-contain the full runtime"**:
  verified for both legs. Rv2Token creation 1,971 B = 28 B initcode + 1,943 B
  runtime at +28 (one occurrence, 0 trailing); the r1 **Smoke** creation is
  685 B decoded and its own initcode is
  `PUSH2 0x0291; DUP1; PUSH2 0x001c; PUSH0; CODECOPY; PUSH0; RETURN` —
  copies `code[28:28+657]`, and 28+657 = 685 = file length, so the 657 B
  runtime is byte-embedded at +28. Its probe is `ev_f875e21e…`, 0 functions.
- **"five EQ;PUSH2;JUMPI sites"** (r1:31(a)): 5 *dispatcher* compares
  (`80; PUSH4 <sel>; EQ; PUSH2 <dest>; JUMPI`) with selectors
  `095ea7b3, 18160ddd, 23b872dd, 70a08231, a9059cbb` and destinations
  `0x59/0x89/0xa7/0xd7/0x107` (= the probe offsets 89/137/167/215/263).
  A loose `14 61 xx xx 57` scan finds **7** — the two extra at runtime
  +1384/+1435 are non-dispatch EQ-based guards outside the five-compare
  dispatcher chain. The five-site claim is correct under the dispatcher
  definition; a loose scan would overcount.

## 6. The checker is bounds-only — demonstrated, and it matters here

Fault-arm cross-check (`RV-7-independent/fault-arm.txt`):

| variant | rule_blocks | resolved | depth |
|---|---|---|---|
| clean | 15 | 15 | 10.0 |
| out-of-bounds `r4:39-64` | 15 | 14 | 9.33 |
| missing file | 15 | 14 | 9.33 |
| content-wrong `:34` | 15 | **15** | 10.0 |
| content-correct `:29` | 15 | **15** | 10.0 |

Command A cannot distinguish `:34` from `:29`: the wrong pointer passes the
frozen falsifiable. This is the same census-checked-vs-instrument-graded gap
the round's candidate (a) names, encountered inside the verification of
candidate (c) — a bounds-resolving citation is not a content-correct one.
Candidate (a)'s landability arithmetic is also confirmed: a rule with no
corpus citation lands as a 15th block that resolves invalid
(`RV-7-independent/candidate-a.txt`): **15 blocks / 14 resolved / 9.33**,
and the targeted C1-gate vocabulary grep over `corpus/knowledge/` is empty —
**VERIFIED**, as SC-3 argued.

## 7. Cross-checks against the concurrent peer RV-7 artifact

- **Peer F1 — r3 erratum's `:24` pointer is dangling: VERIFIED.** The phrase
  "Creation blobs carry no runtime dispatch table" is absent from the r3
  entry at `c418be0` and `40de383`, and at `58c3db7` occurs only inside the
  erratum itself (:41). r3's line 24 is the Rv2TokenOpt RESULT row at every
  rev; the quoted sentence is r1:24. The erratum's byte facts are true; its
  pointer is unqualified/wrong (`RV-7-independent/r3-pointer-audit.txt`).
- **Peer §5 byte table: REPRODUCED 5/5**
  (`RV-7-independent/peer-embedding-table.txt`): VaultB opt200 1,621 B
  `b24a0115…` at +34 in 1,655 B; VaultB nopt 3,163 B `bcdf64ab…` at +80 in
  3,243 B; CarrierB 1,469 B `b9c70178…` at +91 in 1,560 B; Smoke@r4 168 B
  `415e6b1b…` at +27 in 248 B (53 trailing); Rv2Token 1,943 B `c1081a56…`
  at +28 in 1,971 B.
- **SC-3 §6 table row** describes the r3 erratum as "correcting r3 `:24`" —
  that repeats the dangling pointer as if it were r3's own line. SC-3's
  *rule text* deliberately says only "re-landed on the r3 entry", so the
  landing artifact is unaffected; the table row should not be copied into
  any record that needs the pointer.
- Rule 15 does not duplicate rules 7–9 (tool acceptance ≠ correctness;
  census rows can be defects; verify the gate, not the hint): it is the
  parsed-and-empty-vs-byte-absence distinction, and it is consistent with
  them. **VERIFIED.**

## 8. Per-item verdicts

| Item | Verdict |
|---|---|
| Baseline command A at `c625d5d` and `58c3db7` (14/14/10.0; 84/84; missing/dangling []) | REPRODUCED |
| Craft section 14 rules, ends `SKILL.md:255`; revs identical | VERIFIED |
| Draft identity 1,605 B / 23 lines / `763c44b5…` | VERIFIED |
| Draft parses as one block; 8 knowledge refs | VERIFIED |
| Scratch landing 14 → 15 blocks, 15/15, depth 10.0, other counters unchanged | REPRODUCED |
| Fault arm catches out-of-bounds and missing-file citations | REPRODUCED |
| Citation bounds 8/8 | VERIFIED |
| Citation content | **CORRECTED** — `r4:34` quote is at `:29` |
| `corpus/QUALITY.md:21` row 11 | VERIFIED |
| CarrierV 1,637/1,562/+20/55 byte facts | REPRODUCED |
| CarrierV live probe (0 functions, kind unknown, `ev_53732d0f…`) | REPRODUCED |
| EX-06 same-id envelope; r1 sealed `ev_c80379e1…` | VERIFIED (same-path determinism) |
| r1 Smoke creation embeds its 657 B runtime at +28 via its own CODECOPY | VERIFIED |
| Rv2Token "five" dispatching compares; loose scan 7 | VERIFIED (definition caveat) |
| Peer RV-7 §5 byte table | REPRODUCED 5/5 |
| Peer RV-7 F1 (r3 `:24` pointer) | VERIFIED |
| SC-3 §6 table's r3-`:24` description | CORRECTED (rule text unaffected) |
| Candidate (a) ref-less rule → 9.33 | VERIFIED |
| Rule non-duplication / consistency with rules 7–9 | VERIFIED |
| SC-3's SCORECARD.md:1657-1660 attribution | VERIFIED |

## 9. Landing recommendation (parent)

1. Land rule 15, because its content is earned and verified. **Land the
   corrected variant** (`RV-7-independent/rule15-sc3-corrected.txt`), not the
   original: one line pointer changes (`:34` → `:29`), identity re-derives to
   **1,605 B / 23 lines / `6967b1e3…`**.
2. If the wave requires landing the seat's draft verbatim, land
   `763c44b5…` and queue an append-only pointer correction; but SKILL.md then
   carries a wrong line number until that lands, and the correction changes
   the rule bytes again. Either way, record the fresh landed identity — a
   stale self-identity voids the verification block (craft rule 14).
3. After landing, command A should read
   `rule_blocks=15, citation_resolved_rules=15, depth_score=10.0,
   knowledge_files=84, mapped=84, missing=[], dangling=[], coverage=10.0`.
   Do not land the rule twice (original + corrected); one block only.
4. Queue F1 (r3 erratum `:24` pointer) as an append-only corpus correction in
   a later round: re-point it to r1:24 or qualify it. This seat did not touch
   the corpus.

## 10. Custody / scratch

- Scratch: `/var/tmp/rv7-verify/` (command-A script, simulated SKILLs,
  probes, evidence staging). No `/tmp` use.
- Custody paths read-only throughout: `SKILL.md`, `corpus/`, `.ufo/gates/`.
- Git: read-only (`show`, `log`, `rev-parse`, `status`); no mutation.
- Files written: this artifact and `RV-7-independent/` only. The existing
  `claims/c3/RV-7.md` and `claims/c3/RV-7/` (concurrent peer) were left
  untouched.
