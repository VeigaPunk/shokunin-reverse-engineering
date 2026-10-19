# SC-1 — c3 depth: independent verification of SC-3's rule #15 (parsed-and-empty ≠ byte-absence)

Seat SC-1, chain c3 (depth), wave `arc3-loop1-round6`, 2026-10-19.
Repo HEAD `c625d5d` (records; work `58c3db7`). Every number below was
re-derived first-hand this seat (lane rule #14); prior-seat values are only
compared against, never used as evidence. Evidence dir:
`.ufo/waves/arc3-loop1-round6/claims/c3/SC-1/`. Scratch: `/dev/shm/sc1/`
(command A + simulations), `/var/tmp/sc1-probe/` (live probe; never `/tmp`).
Write scope honored: only `claims/c3/SC-1.md` + `claims/c3/SC-1/` were
created; no git mutation; corpus, SKILL.md, gates, and peer artifacts read-only.

Verdict in one line: **SC-3's rule content is VERIFIED and command A measures
14 → 15 exactly as claimed, but the draft ships with two wrong citation
anchors (one major, one minor) that command A cannot see because its checker
validates line bounds only. A two-line corrected variant (§5) keeps the
content and measures 15/15 at both revs.**

## 1. Baseline re-derivation — command A, both revs (REPRODUCED)

Recipe run verbatim from `SCORECARD.md:88-124` at both source commits
(scratch `/dev/shm/sc1/cmdA_<rev>.json`; retained as
`SC-1/commandA-before.json`):

```
c625d5d {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}
58c3db7 {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}
```

`git diff --stat c625d5d 58c3db7 -- SKILL.md` prints nothing (exit 0) — the
craft section is identical at both revs. Mechanical section check at both
revs: craft header at `SKILL.md:81`, next `## ` heading at `:260`,
`rule_blocks=14`, rule 14's last line `:255` ends "never a carried-over
number." Cited-file line counts: r1 entry 46, r3 entry 57, r4 entry 63.

Verdict: the frozen "before" (`rule_blocks=14`, 84/84, `missing=[]`,
`dangling=[]`, depth 10.0) — **REPRODUCED** first-hand.

## 2. SC-3's draft identity and simulated landing (VERIFIED)

Extracted the fenced draft from `claims/c3/SC-3.md:84-108` (the `markdown`
fence) and measured both conventions:

- fenced block without trailing newline: 1,604 B, sha256 `f34846be…`;
- **as landed (trailing newline supplied by the line insertion): 1,605 B,
  23 lines, sha256
  `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`**
  — matches SC-3's claimed self-identity exactly (`SC-3.md:74-76`).

The convention is the ordinary one: every SKILL.md rule line ends in a
newline, so the landing bytes are the 1,605 B form. The block parses as
exactly one rule (one `^- \*\*` line start; no stray bullets inside).

Simulated landing: insert the draft after rule 14's last line
(`never a carried-over number.`) in `58c3db7:SKILL.md` and `c625d5d:SKILL.md`
in `/dev/shm`, then re-run command A's exact section-split, rule-split, and
citation checker against the corpus at the same rev
(`SC-1/commandA-after-simulated.txt`):

| draft | rev | rule_blocks | citation_resolved_rules | depth_score | new-rule refs | bad bounds |
|---|---|---|---|---|---|---|
| SC-3 verbatim 1,605 B `763c44b5…` | 58c3db7 | 14 → **15** | 14 → **15** | 10.0 | 8 | none |
| SC-3 verbatim | c625d5d | 14 → **15** | 14 → **15** | 10.0 | 8 | none |

All 14 pre-existing rules keep their resolved status; coverage counters are
untouched by a craft landing. Verdict: the frozen falsifiable — **REPRODUCED
on a scratch tree at both revs**.

## 3. The rule's earned facts, re-derived first-hand (VERIFIED/REPRODUCED)

### 3.1 CarrierV byte census (`SC-1/byte-census.txt`)

From the retained round-4 carrier (`…round4/claims/c1/EX-04/out/`):

- creation: 1,637 B, sha256 `3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226`;
- runtime: 1,562 B, sha256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`;
- `runtime.hex` decodes byte-identical to `runtime.bin`;
- the full runtime occurs exactly once inside the creation blob at **+20**,
  with **55 trailing bytes**.

These are byte-exact matches to the retained EX-08 census
(`…round4/claims/c1/EX-08/evidence-creation-embedding.txt`: same two
digests/sizes, `offset: 20`, `trailing bytes … 55`, trailer hex, and
`runtime round-trip byte-identical: True`) and to the r5 erratum's +20 /
1,637 B (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:43`). Verdict:
**REPRODUCED** byte-exact, with an independent file to compare against.

### 3.2 Live probe — parsed-and-empty on the same blob

```
mkdir -p /var/tmp/sc1-probe
TMPDIR=/var/tmp/sc1-probe npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex hex --format json
→ exit 0
  evidence_id ev_53732d0f8c67d15c18110610cf228e550fb290537c87605706fc92a0856bee13
  functions 0 ; bytecode.kind "unknown"
  decoded bytecode.sha256 3c6673966d821d9d… (= the decoded creation's own sha above)
```

Raw envelope retained as `SC-1/probe-carrierv-creation.json`. The sealed
EX-06 envelope (`…round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`)
re-reads functions 0, kind unknown, same id; its `subject.local_path` is the
absolute resolved path, which explains why the relative invocation above
re-mints the same id. This is same-path determinism, not independent
corroboration — the independent leg is the byte census. The sealed r1
envelope (`…round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`,
`ev_c80379e1…`) also reads 0 functions. Verdict: **REPRODUCED** — probe says
0 functions on a blob whose bytes contain the full runtime at +20.

### 3.3 Two more carriers from the cited errata

- `VaultB` opt200 (`…round3/claims/c1/EX-10/out/`): creation 1,655 B,
  runtime 1,621 B, embedded at **+34**, 0 trailing — matches
  `…r3-evm-optimizer-shapes.md:46` ("1,621 B at offset +34 in 1,655 B").
- `Smoke` (`…round4/claims/c1/EX-02/smoke/Smoke.bytecode.hex` +
  `Smoke.runtime.hex`): creation 248 B, runtime 168 B, embedded at **+27**,
  53 trailing — matches `…r4-evm-vyper-leg.md:44`.

### 3.4 r1's "five EQ;PUSH2;JUMPI sites" — definition matters

`Rv2Token.creation.hex` at `…round1/claims/c1/RV-2/` decodes to 1,971 B
(sha256 `04e07f54…`); runtime 1,943 B (`c1081a56…`) embedded once at **+28**,
0 trailing. The literal 3-opcode pattern `14 61 .. 57` occurs **7×** in the
runtime (and 7× in the creation); exactly **5** are PUSH4-prefixed dispatch
sites (`63 <sel:4> 14 61 <target> 57`). So `…r1-evm-real-solc.md:31`'s
"its five `EQ;PUSH2;JUMPI` sites" holds for the **dispatch** sites; a loose
opcode scan over-counts by 2. This is a definitional caveat for any rule that
repeats the bare count, not a falsehood in the entry.

## 4. Citation anchor audit — 2 DISCREPANCIES in the draft

Command A's checker evaluates only `file exists && 1 ≤ start ≤ end ≤ line
count` (`SCORECARD.md:105-117`). I additionally checked that each cited line
range actually carries the claim attached to it (`SC-1/anchor-audit.txt`;
cited text read at `58c3db7`, identical at `c625d5d`):

| ref in draft | attached claim | bounds | content anchor | verdict |
|---|---|---|---|---|
| `…r1-evm-real-solc.md:24` | "probed 0 functions on blobs that byte-contain the full runtime" | 24 ≤ 46 ✓ | line supports "0 functions"; it asserts the **opposite** of byte-containment ("Creation blobs carry no runtime dispatch table"); the embed fact is at `:31` | **D1 — mis-scoped citation (minor)** |
| `…r1-evm-real-solc.md:31` | correction, "not byte-level absence" | 31 ≤ 46 ✓ | "measured false … embeds the runtime … not byte-level absence" | PASS |
| `…r3-evm-optimizer-shapes.md:41-51` | "the same correction re-landed on the r3 entry" | 41-51 ≤ 57 ✓ | "corrected", "parsed-and-empty", "runtimes are byte-exactly embedded" | PASS (but see F1) |
| `…r4-evm-vyper-leg.md:39-46` | verbatim corrected statement | 39-46 ≤ 63 ✓ | the quoted sentence is at `:46` | PASS |
| `…r4-evm-vyper-leg.md:17` | original claim repeated | 17 ≤ 63 ✓ | "uniformly parsed-and-empty … initcode carries no runtime dispatch table" | PASS |
| `…r3-evm-optimizer-shapes.md:27` | raw-over-hex-text trap | 27 ≤ 57 ✓ | "parsed-and-empty, a probe-input trap, not a carrier defect" | PASS |
| `…r4-evm-vyper-leg.md:25` | Vyper repetition of the trap | 25 ≤ 63 ✓ | "raw-over-hextext exits 0 … the r1/r3 trap class" | PASS |
| `…r4-evm-vyper-leg.md:34` | tool limitation "empty results do not prove absence of dispatch" | 34 ≤ 63 ✓ | **phrase absent**; line 34 is `## Erratum (arc3-loop1-round5 correctness sweep, append-only)`. The phrase is at **`:29`** (Limitations bullet) | **D2 — mis-citation (major)** |

Both defects pass command A because the bounds are valid. They are exactly
the class the rule is about: a check that finds the right *shape* (path +
line) is not proof that the cited clause says what the rule claims. This is
also a live datum for frozen candidate (a) ("census-checked vs
instrument-graded"): command A reads 15/15 on a draft with two mis-anchored
citations.

### F1 — the r3 erratum's own `:24` pointer is dangling (independently confirmed)

`…r3-evm-optimizer-shapes.md:41` says "`:24` 'Creation blobs carry no runtime
dispatch table' — corrected." But at `58c3db7` r3's line 24 is the
Rv2TokenOpt RESULT row. `git grep` at `c418be0`, `40de383`, `58c3db7` finds
that sentence in `corpus/knowledge/` only in **r1's** entry at `:24` and
inside r3's own erratum at `:41`. So the r3 erratum's byte facts are true but
its `:24` attribution is wrong (the sentence it quotes is r1's). SC-3's draft
does not repeat the `:24` pointer — it cites the range `:41-51` — so the draft
does not propagate the defect, but the range it cites contains it. Suggested
append-only disposition for a later corpus pass: re-point the r3 erratum's
quote to r1 `:24`, or drop the pointer (outside this seat's write scope).

## 5. Corrected landing variant — command-A clean with anchors fixed

Minimal two-edit variant of SC-3's own text (content unchanged, authorship
SC-3; edits are mine):

1. move the `r1:24` citation so it attaches to the probe result it supports:
   "0 functions" (`…r1…:24`) "on blobs that byte-contain the full runtime;"
2. `…r4-evm-vyper-leg.md:34` → `:29` for the tool-limitation quote.

Bytes: **1,605 B, 23 lines, sha256
`a8aef40eb1fd825d4c3cc4b1d35965751cc2b14a7e5ee5370027e6d5b54ae0d1`**
(retained verbatim at `SC-1/rule15-sc3-corrected.md`; the diff against the
SC-3 block is exactly these two edits plus the trailing newline that landing
supplies). Simulated landing measures
`rule_blocks=15`, `citation_resolved_rules=15`, `depth_score=10.0`, 8 refs,
no bad bounds at both revs, and all eight anchors now pass the content check
(`SC-1/commandA-after-simulated.txt`, `SC-1/anchor-audit.txt`).

**Recommendation:** land the corrected 1,605 B variant (or RV-7's independent
draft, §6), not SC-3's verbatim text. If the integrator prefers to land SC-3
verbatim, the two anchors should at least be queued as a follow-up erratum —
a craft rule about evidence discipline should not itself ship mis-anchored.

## 6. Peer reconciliation (brief — VZ/CN own the full reconcile)

RV-7's competing bullet (`claims/c3/RV-7/rule15-bullet.md`) measured first-hand
this seat: 1,565 B, 23 lines, sha256 `ccbc5cdb…`; simulated landing gives
`rule_blocks=15`, `citation_resolved_rules=15`, `depth_score=10.0`, 6
pattern refs, no bad bounds at both revs. Its anchors spot-check clean
(`r1:24` for the original claim + `:31` for the correction, `r3:41-51`,
`r4:39-46`, `r4:17`, `r3:27`, `r4:25`). One wording caveat: its §5
"creation carries exactly 5 compare-site patterns" is true only for
PUSH4-prefixed **dispatch** sites; the loose `EQ;PUSH2;JUMPI` pattern is 7×
in both runtime and creation (§3.4). Not a blocker, but do not repeat the
bare "5" without the dispatch qualifier.

Both drafts are independently command-A-clean; the choice between them is
editorial. The corrected SC-3 variant preserves SC-3's structure and the
SC-3 self-identity record; RV-7's is shorter and already avoids both anchors.

## 7. Per-item verdicts

| Item | Verdict |
|---|---|
| command A baseline (`rule_blocks=14`, 14 resolved, 84/84, `missing=[]`, `dangling=[]`, depth 10.0) at `c625d5d` + `58c3db7` | **REPRODUCED** (§1) |
| `git diff --stat … -- SKILL.md` empty; craft section `:81-259`; 14 rules; rule 14 ends `:255` | **VERIFIED** (§1) |
| SC-3 draft self-identity 1,605 B / 23 lines / `763c44b5…` | **VERIFIED** (§2) |
| rule_blocks 14 → 15, citation_resolved_rules 14 → 15, depth 10.0, 8 refs in bounds | **REPRODUCED** on scratch at both revs (§2) |
| CarrierV 1,637 B `3c667396…` / 1,562 B `57d6fd0a…` / +20 / 55 trailing; runtime.hex ≡ runtime.bin | **REPRODUCED**; EX-08 census agrees byte-exact (§3.1) |
| Live probe: exit 0, 0 functions, kind unknown, decoded sha `3c667396…`, id `ev_53732d0f…` | **REPRODUCED** (§3.2) |
| Sealed r1 `ev_c80379e1…` and EX-06 `ev_53732d0f…` creation envelopes: 0 functions | **VERIFIED** by re-reading sealed JSON (§3.2) |
| VaultB opt200 1,621 B at +34 in 1,655 B; Smoke 168 B at +27 in 248 B | **REPRODUCED** (§3.3) |
| r1:31 "five EQ;PUSH2;JUMPI sites" | **VERIFIED** for the 5 dispatch sites; loose pattern is 7× — definitional caveat (§3.4) |
| r1:24 anchor for "byte-contain the full runtime" | **DISCREPANCY D1** — line asserts the opposite; embed fact is `r1:31` (§4) |
| r4:34 anchor for the tool-limitation quote | **DISCREPANCY D2** — line 34 is the Erratum header; phrase is at `r4:29` (§4) |
| r3 erratum `:24` attribution | **DISCREPANCY F1** (corpus defect; not propagated by the draft) (§4) |
| Corrected 1,605 B variant `a8aef40e…`: 15/15, all anchors pass | **REPRODUCED** (§5) |
| RV-7 peer bullet 1,565 B `ccbc5cdb…`: 15/15, 6 refs, anchors clean | **REPRODUCED** (§6) |
| Frozen C3 falsifiable ("rule_blocks 14 → 15 with citations resolving") | **SATISFIED** by SC-3 verbatim, corrected variant, and RV-7 variant — but command A alone does not certify citation content |

## 8. Scratch and custody

- Scratch: `/dev/shm/sc1/` (command-A JSONs, draft extracts, simulations),
  `/var/tmp/sc1-probe/` (live-probe TMPDIR; `/tmp` avoided — EDQUOT).
- Writes: only `claims/c3/SC-1.md` and `claims/c3/SC-1/` (this artifact).
  No git mutation; corpus, `SKILL.md`, `.ufo/gates/`, `LOG.md`, `SCORECARD.md`,
  `PROVINCE.md`, and all peer artifacts read-only.
- `git status --porcelain` at seat end shows the pre-existing
  ` M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked
  `.ufo/waves/arc3-loop1-round6/` tree; neither is a write of this seat.
- Not done here (by design): landing the rule into `SKILL.md` (integrator's
  move); the r3 erratum pointer fix and any corpus append (outside seat
  scope; queue for a corpus round).
