# RV-6 — c3 depth: independent verification of SC-3's rule #15, with two content defects and a corrected landing text

Seat RV-6, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19. Repo HEAD
`c625d5d` (work `58c3db7`). Every number below was re-derived first-hand this
seat (lane rule #14); no value is quoted from SC-3, RV-7, or an earlier round
without a fresh measurement. Scratch: `/var/tmp/rv6-c3/` (never `/tmp`).
Custody paths read-only; git read-only; writes only under
`.ufo/waves/arc3-loop1-round6/claims/c3/`. Evidence:
`claims/c3/RV-6/` (transcripts, draft bytes, probe envelope, checker script).

## 1. Baseline re-derivation (command A)

Ran the exact recipe at `SCORECARD.md:88-124` (git-object reads, not the
worktree) at both source commits. Full transcript:
`RV-6/commandA-transcript.txt`; checker: `RV-6/cmdA-sim.py`.

| rev | command A result |
|---|---|
| `58c3db7` | `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}` |
| `c625d5d` | identical (14/14, 84/84, depth 10.0) |

`git diff --stat c625d5d 58c3db7 -- SKILL.md` is empty (exit 0, no output):
the craft section is identical at both revs. SC-3's §1 baseline is
**REPRODUCED**.

## 2. SC-3 draft self-identity

Extraction: fenced `markdown` block from `claims/c3/SC-3.md:84-108`
(`RV-6/sc3-rule15-extract.txt`).

- Body as fenced (no terminator): **1,604 B**, 23 lines, sha256
  `f34846bec27af2ffd599d16a5b2be38667da79c4c503ff344f5172db952fec47`.
- Body + one `\n` terminator (the landing convention — a SKILL.md bullet is a
  newline-terminated line): **1,605 B**, 23 lines, sha256
  `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1` —
  exactly SC-3's stated identity.

Verdict: **REPRODUCED**, with the explicit convention noted. An integrator who
pastes the fenced block without a trailing newline would land 1,604 B /
`f34846be…`; the stated `763c44b5…` binds the newline-terminated form.

Parse properties: exactly one `^- \*\*` block start, 23 lines, 8
`corpus/knowledge/...` pattern refs (r1:24, r1:31, r3:41-51, r4:39-46, r4:17,
r3:27, r4:25, r4:34) — all in-bounds. **REPRODUCED**.

## 3. Citation content audit — two defects command A cannot see

Command A validates `1 ≤ start ≤ end ≤ line-count` only. It does not read the
cited line. Audit transcript: `RV-6/citation-audit.txt`.

| anchor | what the rule cites it for | cited line actually says | verdict |
|---|---|---|---|
| r1:24 | r1 creation legs probed 0 functions **on blobs that byte-contain the full runtime** | records 0 functions and `bytecode.kind:"unknown"`, then asserts "Creation blobs carry no runtime dispatch table" | **CORRECTED** (F2) |
| r1:31 | erratum: embedding measured, wording corrected to "not byte-level absence" | "measured false — `Rv2Token.creation.hex` (1,971 B) embeds the runtime … not byte-level absence" | ✓ |
| r3:41-51 | same correction re-landed on r3 | erratum: parsed-and-empty, not proof of byte absence, with embedded-runtime offsets | ✓ (facts; see F3) |
| r4:39-46 | "creation probes parse empty while the runtime bytes are present verbatim" | verbatim at `:46` | ✓ |
| r4:17 | entry had repeated the r1/r3 class | "uniformly parsed-and-empty … initcode carries no runtime dispatch table" | ✓ |
| r3:27 | raw-over-hex-text trap, not a carrier defect | "parsed-and-empty, a probe-input trap, not a carrier defect" | ✓ |
| r4:25 | same trap class on Vyper carriers | "raw-over-hextext exits 0 … parsed-and-empty, the r1/r3 trap class" | ✓ |
| r4:34 | tool limitation: "empty results do not prove absence of dispatch" | `## Erratum (arc3-loop1-round5 correctness sweep, append-only)` | **DISCREPANCY** (F1) |

**F1 — `r4:34` is the wrong line (DISCREPANCY).** The quoted limitation sits on
`r4:29` (the Limitations bullet); `r4:34` is the Erratum section header. This
does not change command A's count (34 ≤ 63), which is exactly the
reachability-vs-validity gap the rule is meant to police. Fix: `:34` → `:29`.

**F2 — `r1:24` is cited for a proposition it denies (CORRECTED).** The rule
sentence conjoins "probed 0 functions" (true at `:24`) with "blobs that
byte-contain the full runtime" (which `:24` asserts the opposite of; `:31`
measures it and calls the `:24` sentence measured false). The draft's own next
clause cites `:31`, but the first clause still attributes the containment to
`:24`. Fix: split the clause — probe result at `:24`, containment and
correction at `:31` (and scope the containment to `Rv2Token.creation.hex`,
which is what `:31(a)` measures).

**F3 — r3 erratum's `:24` pointer is dangling (CONFIRMED independently).** At
`c418be0`, `40de383`, and `58c3db7`, `arc3-r3…:24` is the Rv2TokenOpt RESULT
row and the phrase "Creation blobs carry no runtime dispatch table" occurs
zero times outside the HEAD erratum (one occurrence at `:41`). This confirms
RV-7's F1. SC-3's landable rule body does **not** repeat the quote or the
`:24` pointer — but SC-3's §6 table describes the r3 erratum as "correcting r3
`:24`", so the claim text (not the draft) propagates the false attribution.

Net: 6/8 anchors fully correct; 1 wrong line (F1); 1 attribution conflation
that `:31` already repairs in the next clause (F2).

## 4. Mechanical falsifiable — REPRODUCED, with the caveat above

Simulated landing: insert the draft after the SKILL.md anchor
`never a carried-over number.` in the git object for each rev, then run the
exact command-A checker (`RV-6/commandA-transcript.txt`).

| rev | before | after SC-3 draft | after RV-6 corrected (§6) |
|---|---|---|---|
| `58c3db7` | 14 rules / 14 resolved / depth 10.0 | **15 / 15 / 10.0** | **15 / 15 / 10.0** |
| `c625d5d` | 14 / 14 / 10.0 | **15 / 15 / 10.0** | **15 / 15 / 10.0** |

All existing counters unchanged in every arm: `knowledge_files=84`,
`mapped=84`, `missing=[]`, `dangling=[]`, `coverage_score=10.0`. The frozen
C3 falsifiable is **REPRODUCED**. Note that SC-3's verbatim draft passes this
test *despite* F1/F2, because the checker is bounds-only — the corrected text
is justified by the content audit in §3, not by command A.

## 5. First-hand evidence for the rule's core instance

CarrierV bytes (`RV-6/census-and-probe-transcript.txt`), decoded first-hand
from `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/`:

- `creation.hex` file: 3,274 B, sha256 `34f52280d3cdc740…` (= r4:12's
  recorded creation-hex digest `34f52280…`); decoded creation: **1,637 B**,
  sha256 `3c6673966d821d9d…` (= r4:12).
- `runtime.bin`: **1,562 B**, sha256 `57d6fd0ae0da0019…` (= r4:12);
  `runtime.hex` decodes byte-identically to `runtime.bin`.
- The runtime occurs exactly **once** in the creation, at **offset +20**, with
  **55 trailing bytes** (= r4:43-44's r5 erratum, reproduced byte-exact).
- Retained EX-08 census
  (`…/round4/claims/c1/EX-08/evidence-creation-embedding.txt`) carries the
  same sizes, digests, +20 offset and 55 trailing bytes.

Live probe, first-hand (`RV-6/probe-CarrierV-creation-6.4.0.json`):

```
TMPDIR=/var/tmp/rv6-c3/probe npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex hex --format json
→ exit 0; evidence_id ev_53732d0f8c67d15c…; functions: 0;
  bytecode.kind: "unknown"; decoded bytecode.sha256 3c667396…;
  subject.digest.sha256 34f52280… (the hex-text file)
```

That id is byte-identical to EX-06's sealed envelope at the same absolute
path (`…/round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`, also 0
functions) — same-path determinism, **not** independent corroboration, as
SC-3 itself states. Independent corroboration is the byte census above and the
r1 sealed envelope (`…/round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`,
`ev_c80379e1…`, 0 functions). The pair "probe says 0 functions / bytes contain
the full runtime at +20" is re-derived on one blob: **VERIFIED**.

Round-5 attribution: `SCORECARD.md:1658-1659` contains the quoted r4
initcode-absence correction (SC-3 cites the enclosing range 1657-1660):
**VERIFIED**.

## 6. Corrected landing text (RV-6 candidate)

Two surgical edits to SC-3 §4, nothing else: (F2) split the r1 clause so
`:24` carries only the 0-function result and `:31` carries the measured
containment/correction; (F1) re-point `:34` to `:29`. Byte-exact source:
`RV-6/rv6-corrected-rule15.txt`.

Self-identity: **1,574 B, 23 lines**, sha256
`38f850706b07ebe868d0d9d9c166aca45f0d2bcc421d939fe1fb8f339b3bfe6d`
(re-derive after any edit; the file is newline-terminated). Max line length
78. Exactly one block start; 8 pattern refs, every one content-checked at the
cited line (`RV-6/citation-audit.txt`): r1:24 "0 functions", r1:31 "1,971 B",
r3:41-51 "parsed-and-empty", r4:39-46 "present verbatim", r4:17
"parsed-and-empty", r3:27 "probe-input trap", r4:25 "trap class", r4:29
"empty results do not prove absence".

```markdown
- **A parsed-and-empty result is a statement about the parser's scope, never
  proof of byte absence — settle byte questions with a census (decode, locate,
  hash), not with the probe's function count.** The r1 creation legs probed
  0 functions (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`), and
  the entry's own erratum measured `Rv2Token.creation.hex` (1,971 B) embedding
  the runtime and corrected the wording to tool-scope parsed-and-empty, "not
  byte-level absence"
  (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31`). The same
  correction re-landed on the r3 entry
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51`) and on
  r4's initcode legs — "creation probes parse empty while the runtime bytes
  are present verbatim"
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46`) — after the
  entry had repeated the r1/r3 class
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`). The trap legs
  are the second face of the same mistake: raw-over-hex-text reads exit 0 /
  0 functions on ASCII bytes — a probe-input trap, not a carrier defect
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:27`;
  Vyper repetition `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:25`).
  The tool's own limitation says it: "empty results do not prove absence of
  dispatch" (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29`). Word
  zero-findings at their class (parsed-and-empty vs excluded-from-inventory,
  `corpus/QUALITY.md:21`) and only then claim or deny byte presence.
```

Simulated landing at both revs: **15 rules / 15 resolved / depth 10.0**, all
other counters unchanged (§4 table; `RV-6/commandA-transcript.txt`).

## 7. Adjudication with RV-7 and recommendation

RV-7's delivered bullet (`claims/c3/RV-7/rule15-bullet.md`) was re-measured
here: **1,565 B, 23 lines**, sha256
`ccbc5cdbbefc86081393cd4d60ef9c85606c3dd1c98ed76d63520da1da0b67e7`, 6
pattern refs (r4:39-46 occurs twice), simulated landing **15/15, depth 10.0 at
both revs** (first-hand, `RV-6/commandA-transcript.txt`). It is content-clean
on F1/F2: it does not cite `:34`, and its r1 clause attributes the
correction to `:31` explicitly. Its bullet does carry the same r3 erratum that
has the dangling internal pointer (F3), but it does not repeat the pointer.

Both candidate texts land the frozen falsifiable. **Recommendation: land
exactly one of** `RV-6/rv6-corrected-rule15.txt` or RV-7's bullet; do not land
both (they would create rules #15 and #16 with duplicate content), and do not
land SC-3 §4 verbatim (it ships F1 and F2; its mechanical pass is a
bounds-only artifact). This seat's preference is the §6 corrected text because
it preserves SC-3's teaching sequence with the two defects repaired and all 8
anchors content-audited; RV-7's bullet is an equally valid, shorter-citation
alternative already delivered by its seat. The integrator must record the
fresh landing identity of whichever text is inserted.

## 8. Per-item verdicts

| item | verdict |
|---|---|
| Baseline command A at `58c3db7` and `c625d5d` (14/14, 84/84, depth 10.0) | **REPRODUCED** |
| SC-3 draft identity 1,605 B / 23 lines / sha `763c44b5…` | **REPRODUCED** (newline-terminated; 1,604 B / `f34846be…` without terminator) |
| SC-3 draft parses as one rule block, 8 in-bounds refs | **REPRODUCED** |
| C3 falsifiable: 14 → 15 rules, 15/15 citations, depth 10.0 at both revs | **REPRODUCED** (also true of verbatim SC-3 despite §3) |
| `r4:34` content anchor | **DISCREPANCY** — limitation phrase is at `r4:29`; `:34` is the Erratum header |
| `r1:24` content anchor | **CORRECTED** — `:24` records 0 functions but denies runtime presence; containment is measured at `:31` |
| Other 6 of 8 anchors (r1:31, r3:41-51, r4:39-46, r4:17, r3:27, r4:25) | **VERIFIED** at cited lines |
| SC-3 §6 row describing r3:41-51 as correcting r3 `:24` | **DISCREPANCY** (F3, independently confirmed; not in the landable rule body) |
| CarrierV census: 1,637 B `3c667396…`; runtime 1,562 B `57d6fd0a…`; +20; 55 trailing | **REPRODUCED** byte-exact (and agrees with EX-08's retained census) |
| Live creation probe: exit 0, 0 functions, kind unknown, decoded `3c667396…`, `ev_53732d0f…` | **REPRODUCED**; identical to EX-06 sealed envelope (same-path determinism) |
| Round-5 sweep attribution | **VERIFIED** (`SCORECARD.md:1658-1659`) |
| Corrected text (§6): 1,574 B / sha `38f85070…`, 8/8 anchors content-checked, 15/15 at both revs | **VERIFIED** |
| RV-7 bullet: 1,565 B / sha `ccbc5cdb…`, 6 refs, 15/15 at both revs, content-clean | **VERIFIED** (first-hand re-measurement) |

## 9. Scratch and custody

Scratch `/var/tmp/rv6-c3/` (checker, extracted/edited draft bytes, probe
output); never `/tmp`. Evidence committed to this seat's dir:
`commandA-transcript.txt`, `census-and-probe-transcript.txt`,
`citation-audit.txt`, `sc3-rule15-extract.txt`,
`rv6-corrected-rule15.txt`, `probe-CarrierV-creation-6.4.0.json`,
`cmdA-sim.py`. No writes outside
`.ufo/waves/arc3-loop1-round6/claims/c3/`; no git mutation; SKILL.md, corpus,
and `.ufo/gates/` untouched.
