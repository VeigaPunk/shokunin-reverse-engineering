# SC-4 — c3 verification: SC-3's rule-15 draft, two anchor corrections, chain reconciliation

Seat SC-4, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19. Repo HEAD
`c625d5d` (records; work `58c3db7`). Every number below was re-derived
first-hand this seat (lane rule #14); no value is quoted from a prior seat or
round as evidence. Custody paths read-only; git read-only; the only writes are
this artifact and `SC-4/` under `.ufo/waves/arc3-loop1-round6/claims/c3/`.

Worktree state at seat: `git status --porcelain corpus/ SKILL.md` empty;
overall status shows only the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md`
(present before this seat's first read, untouched) and the untracked round-6
wave tree.

## 1. Baseline — REPRODUCED

Command A verbatim per `SCORECARD.md:88-124`, run against immutable Git objects
at both source commits (`SC-4/commandA-before.txt`):

```
c625d5d → {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
           "depth_score": 10.0, "knowledge_files": 84, "mapped": 84,
           "missing": [], "rule_blocks": 14}
58c3db7 → identical (14 / 84 / 84 / [] / [])
```

`git diff --stat c625d5d 58c3db7 -- SKILL.md` is empty — the craft section is
identical at both revs, so one landing text serves both measurements. The
`## Queue-drain craft` section splits into exactly 14 blocks; rule #14 ends
"never a carried-over number." at `SKILL.md:255`, followed by blank lines and
`## Config custody for live-probe rounds (SOP)` at `SKILL.md:260`.

## 2. SC-3's draft self-identity — REPRODUCED

The markdown block in `claims/c3/SC-3.md` §4 extracts (mechanically, between
the ```markdown fence) to exactly:

- **1,605 B, 23 lines, sha256 `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`**

matching SC-3 §4's stated self-identity byte-for-byte. The block contains no
stray `- **` line start (it parses as exactly one rule block) and carries
8 command-A-pattern citations.

## 3. Citation content audit — 7/8 VERIFIED, 1 CORRECTED, 1 precision re-anchor

Command A only bounds-checks (`1 <= start <= end <= line_count`), so it cannot
see a wrong-line anchor inside a long file. Each ref was therefore also checked
against its claimed content (`SC-4/citation-audit.txt`):

| ref | claim in draft | content check | verdict |
|---|---|---|---|
| r1 `:24` | creation legs probed 0 functions | "0 functions" present | VERIFIED for the probe half |
| r1 `:31` | erratum: tool scope, "not byte-level absence"; runtime embedded | both present | VERIFIED |
| r3 `:41-51` | same correction re-landed on r3 | erratum, parsed-and-empty + byte-embedded runtimes | VERIFIED |
| r4 `:39-46` | "creation probes parse empty while the runtime bytes are present verbatim" | quote at `:46` | VERIFIED |
| r4 `:17` | entry had repeated the r1/r3 class | "uniformly parsed-and-empty … initcode carries no runtime dispatch table" | VERIFIED |
| r3 `:27` | raw-over-hex-text trap, "not a carrier defect" | present | VERIFIED |
| r4 `:25` | Vyper repetition of the trap | "raw-over-hextext … parsed-and-empty" | VERIFIED |
| r4 `:34` | tool limitation quote "empty results do not prove absence of dispatch" | **quote absent; `:34` is `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`** | **CORRECTED → `:29`** |
| `corpus/QUALITY.md:21` (outside pattern) | empty/zero findings must state parsed-and-empty vs excluded-from-inventory | row 11 matches | VERIFIED |

**F-SC4-1 (CORRECTED).** The quoted limitation is at
`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29`
("…selectors/args/mutability are inferences; empty results do not prove absence
of dispatch…"). `:34` is the erratum heading. Command A still reads the rule as
resolved because 34 ≤ 63; this is instrument-green / content-red. Independently
found by EX-14 and EX-16 (see §7).

**F-SC4-2 (CORRECTED — precision).** The draft's compound sentence attributes
the containment clause to r1 `:24`:
"probed 0 functions **on blobs that byte-contain the full runtime**
(`…:24`)". Line 24 does contain the 0-function result, but it also asserts the
opposite of containment — "Creation blobs carry no runtime dispatch table" —
and does not contain "byte-contain" at all. The containment measurement is at
r1 `:31` ("…embeds the runtime and its five `EQ;PUSH2;JUMPI` sites"). The next
sentence does cite `:31`, but the immediate anchor misdescribes `:24`. Minimal
fix: attach `:24` to "0 functions" and let the following `:31` citation carry
the embedding. EX-14/EX-16 did not make this fix; the 1-line delta is shown in
§6.

## 4. The rule's core instance — REPRODUCED first-hand

Byte census of the retained CarrierV creation blob
(`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/`, read-only;
`SC-4/byte-census.txt`):

- `creation.hex` decodes to **1,637 B**, sha256
  `3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226`
  (matches r4 `:12` and the r5 erratum `:43-44`).
- `runtime.hex` decodes to **1,562 B**, sha256
  `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`;
  `runtime.bin` is byte-identical to the decode.
- The full runtime occurs **once**, at **offset +20**, with **55 trailing
  bytes** — byte-exact agreement with the retained EX-08 census
  (`…/EX-08/evidence-creation-embedding.txt`, same sizes, digests, offset,
  trailing count, `creation[:20]` wrapper and trailer hex).

Live probe re-run this seat (`SC-4/probe-run.txt`, envelope
`SC-4/probe-creation-6.4.0.json`):

```
TMPDIR=/var/tmp/sc4 npx -y rea-agents@6.4.0 inspect-evm-interface \
  …/EX-04/out/creation.hex hex --format json   → exit 0
evidence_id ev_53732d0f8c67d15c…, functions 0, bytecode.kind "unknown",
decoded bytecode.sha256 3c667396… (= the 1,637 B blob's own digest)
```

The id is byte-identical to the sealed round-4 envelope at the same absolute
path (`…round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`), which is
same-path determinism, not independent corroboration. The r1 sealed envelope
(`…round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`, `ev_c80379e1…`) also
reads 0 functions. So the two halves of the rule — probe says 0 functions;
bytes say the runtime is present verbatim — are both measured on one blob.

## 5. Falsifiable before → after — REPRODUCED on scratch trees

SKILL.md is outside this seat's write scope, so the landing was simulated:
craft section from `git show <rev>:SKILL.md`, candidate appended at the section
end, command A's exact split (`re.split(r'(?m)^- \*\*', craft)[1:]`) and
citation resolver, corpus read from the same rev (`SC-4/scratch-acceptance.txt`).

At **both** `c625d5d` and `58c3db7`: baseline 14 blocks / 14 resolved /
depth 10.0. After appending any candidate below: **15 blocks / 15 resolved /
depth 10.0**, with all other counters unchanged. New-rule refs (8 for the SC-3
lineage) all resolve in-bounds: r1 24≤46, r1 31≤46, r3 41-51≤57, r4 39-46≤63,
r4 17≤63, r3 27≤57, r4 25≤63, r4 29≤63. The frozen falsifiable
"`rule_blocks` 14 → 15 with the new rule's citations resolving" is satisfied.

## 6. Corrected landing text (recommended) and identities

Chain identities (same 23-line shape; `SC-4/citation-audit.txt`):

| candidate | bytes | sha256 | note |
|---|---|---|---|
| SC-3 as delivered | 1,605 | `763c44b5…` | F-SC4-1 and F-SC4-2 present |
| EX-14/EX-16 corrected (identical) | 1,605 | `6967b1e3…` | fixes F-SC4-1 only |
| **SC-4 corrected (recommended)** | **1,605** | **`a1bceb4074328d9d60d14ddf0789b9bcd18ca38936c217d78fc37b1091ec1789`** | fixes both; scratch 15/15 |
| RV-7 alternative rule | 1,565 | `ccbc5cdb…` | different wording; also 15/15 |

Land **exactly one** rule-15 bullet after `SKILL.md:255` (before the blank
lines preceding `## Config custody…`). Recommended bytes — the SC-3 rule with
both anchor corrections:

```markdown
- **A parsed-and-empty result is a statement about the parser's scope, never
  proof of byte absence — settle byte questions with a census (decode, locate,
  hash), not with the probe's function count.** The r1 creation legs probed
  0 functions (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`)
  on blobs that byte-contain the full runtime; the round-3
  byte census measured that embedding and the entry's append-only erratum
  corrected the wording to tool-scope parsed-and-empty, "not byte-level
  absence" (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31`). The
  same correction re-landed on the r3 entry
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

Re-derived identity of the block above: 1,605 B, 23 lines, sha256
`a1bceb40…` (the extractor must see the fence body only, as in §2; any edit
voids this hash). If the integrator prefers the two-peer consensus text,
`6967b1e3…` is also accepted by the same scratch run — it leaves F-SC4-2, a
precision issue only. Do not land SC-3's `763c44b5…` verbatim (F-SC4-1 is a
wrong-line quote) and do not land both this bullet and RV-7's `ccbc5cdb…`
(that would be rule #16 duplicating the lesson).

## 7. Peer reconciliation (read after their landing; independently re-measured)

- **EX-14 / EX-16** — both produced a corrected SC-3 draft with the
  `:34`→`:29` fix; their files are byte-identical (`6967b1e3…`). Their
  `commandA-after-corrected.jsonl` and `simulated-landing.txt` values
  (15/15, depth 10.0, both revs) were re-produced by my scratch run. Neither
  re-anchors the r1 `:24` compound (F-SC4-2).
- **RV-7** — independently worded rule-15 bullet (`ccbc5cdb…`, 6 refs) that
  avoids both problematic anchors; my scratch run reproduces its 15/15. Its F1
  (the r3 erratum's `:24` pointer is dangling) is independently re-derived in
  `SC-4/r3-pointer-check.txt`: at `c418be0`, `40de383`, `58c3db7` and
  `c625d5d`, r3 line 24 is the Rv2TokenOpt RESULT row; the quoted sentence
  "Creation blobs carry no runtime dispatch table" occurs in the r3 file only
  inside the erratum at `:41`, and occurs at r1 `:24`. This is pre-existing
  corpus debt, not SC-3's rule defect: SC-3 cites the r3 range `:41-51`, where
  the correction genuinely lives.
- **SC-3** — §1 baseline, §3 byte facts and §5 scratch numbers reproduced; §4
  draft identity exact. Its two content-anchor defects are F-SC4-1/-2 above.

## 8. Per-item verdicts

| Item | Verdict |
|---|---|
| Command A baseline (14 / 84-84 / [] / [], both revs) | REPRODUCED |
| Draft identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED |
| Draft parses as one block; 8 pattern refs | VERIFIED |
| Citation content, 7 of 8 refs | VERIFIED |
| r4 `:34` quote anchor | CORRECTED → `:29` (F-SC4-1) |
| r1 `:24` containment anchor | CORRECTED (precision, F-SC4-2) |
| CarrierV byte census (1,637 `3c667396…`; 1,562 `57d6fd0a…`; +20; 55 trailing, 1 occurrence) | REPRODUCED |
| EX-08 retained census agreement | REPRODUCED byte-exact |
| Live probe: exit 0, 0 functions, kind unknown, `ev_53732d0f…` | REPRODUCED / VERIFIED first-hand |
| `rule_blocks` 14 → 15 with all citations resolving (scratch, both revs) | REPRODUCED |
| r3 erratum's `:24` premise attribution | DISCREPANCY (pre-existing corpus debt; out of write scope) |

## 9. Evidence index and custody

`claims/c3/SC-4/`: `commandA-before.txt`, `scratch-acceptance.txt`,
`citation-audit.txt`, `byte-census.txt`, `probe-run.txt`,
`probe-creation-6.4.0.json`, `r3-pointer-check.txt`, `peer-reconcile.txt`.

Scratch: `/dev/shm/sc4/` (command-A JSONs, extracted/corrected drafts) and
`/var/tmp/sc4/` (probe TMPDIR; `/tmp` avoided — EDQUOT). No writes outside
this artifact dir; `git status` delta from seat start is only this wave's
untracked tree. Not done by design: landing into `SKILL.md` (integrator's
move), corpus correction of the r3 erratum pointer (out of scope), and
first-hand re-runs of the non-CarrierV legs cited by the rule (their retained
sealed envelopes were read, not re-executed).
