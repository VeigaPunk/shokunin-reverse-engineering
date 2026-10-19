# RV-8 — c3 verification: SC-3's rule #15 (parsed-and-empty ≠ byte-absence)

Seat RV-8, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19. Measured at
HEAD `c625d5d` (work `58c3db7`). Every number below is re-derived first-hand
this seat (lane rule #14); no value is quoted from SC-3, RV-7, or a prior
round without an independent measurement. Scratch: `/dev/shm/rv8/` and
`/var/tmp/rv8-probe/` (never `/tmp`). Custody paths read-only; git untouched;
the only writes are `…/claims/c3/RV-8.md` and `…/claims/c3/RV-8/`. Evidence
files are listed in §9.

Task: independently verify SC-3's delivered rule #15 draft, or propose a
different rule. Verdict up front: **SC-3's draft VERIFIES** — bytes, citations,
earned facts, and the frozen falsifiable all reproduce. Two non-blocking
attribution/wording nits and one peer-reconciliation conflict (SC-3 vs RV-7
both filling slot #15) are recorded in §6–§7.

## 1. Baseline command A (SCORECARD.md:88-124) — REPRODUCED

Run verbatim from `SCORECARD.md:93-123` at both source commits
(`RV-8/commandA-before.txt`):

- `58c3db7` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}`
- `c625d5d` → identical (`rule_blocks=14`, 14/14 resolved, 84/84, `missing []`, `dangling []`).

`git diff --stat c625d5d 58c3db7 -- SKILL.md` is empty. The frozen-claim
"before" values are **REPRODUCED** first-hand.

## 2. Draft self-identity — VERIFIED

Extracted the fenced `markdown` block under `SC-3.md:84-108` byte-for-byte
(`RV-8/draft-identity.txt`):

```
bytes=1605 lines=23 sha256=763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1 ends_with_lf=True
bullet-line starts (^"- **"): [1]
corpus/knowledge refs: 8
```

SC-3's §4 self-identity (1,605 B, 23 lines, `763c44b5…`) — **VERIFIED**. The
block parses as exactly one craft bullet, and the only `^- \*\*` line is the
first. The byte-exact landing copy is preserved at
`RV-8/rule15-sc3-1605b.txt` (1,605 B, sha256 `763c44b5…`).

## 3. Citation audit — 8/8 resolve in-bounds, content anchors verified

Command A's pattern `corpus/knowledge/<name>.md:<n>[-<m>]` was applied by the
simulation in §5; each anchor was also read at `58c3db7` (bounds = file line
counts: r1 46, r3 57, r4 63):

| Citation in the draft | Bound | Content anchor re-derived (this seat) |
|---|---|---|
| `…arc3-r1-evm-real-solc.md:24` | 24 ≤ 46 | r1:24 = creation-code observation: `Rv2Token.creation.hex` `ev_c80379e1…` → 0 functions, kind `unknown`; Smoke `.bin` `ev_f875e21e…` → 0 functions |
| `…r1…:31` | 31 ≤ 46 | erratum: Rv2Token creation "embeds the runtime and its five `EQ;PUSH2;JUMPI` sites"; 0-function result is "tool scope (parsed-and-empty), not byte-level absence" |
| `…arc3-r3-evm-optimizer-shapes.md:41-51` | 41 ≤ 51 ≤ 57 | round-5 erratum: creation probes are parsed-and-empty; runtimes byte-exactly embedded (VaultB opt200 1,621 B at +34 in 1,655 B, etc.) |
| `…r3…:27` | 27 ≤ 57 | raw-over-hex-text trap: exit 0 / 0 functions, decoded sha = hex text file's own sha — "a probe-input trap, not a carrier defect" |
| `…arc3-r4-evm-vyper-leg.md:39-46` | 39 ≤ 46 ≤ 63 | round-5 erratum: "creation probes parse empty while the runtime bytes are present verbatim"; CarrierV at +20 in 1,637 B |
| `…r4…:17` | 17 ≤ 63 | original claim the erratum corrects: creation legs "uniformly parsed-and-empty (exit 0, 0 functions)" |
| `…r4…:25` | 25 ≤ 63 | raw-over-hextext reproduced on Vyper carriers, "the r1/r3 trap class" |
| `…r4…:34` | 34 ≤ 63 | tool limitation: "empty results do not prove absence of dispatch" |

The draft's extra non-pattern reference `corpus/QUALITY.md:21` was checked:
line 21 is gate row 11, "Empty/zero findings must state whether the surface was
parsed-and-empty or excluded-from-inventory". It is outside command A's
pattern and does not affect resolution either way. **8/8 pattern refs resolve;
all content anchors hold.**

Attribution nit **N1** (non-blocking): in the first sentence, "probed 0
functions on blobs that byte-contain the full runtime (`…r1…:24`)" attaches the
embedding half to `:24`, but embedding is recorded at `:31`. The next clause
cites `:31` for exactly that fact, so the paragraph as a whole is accurate; a
re-point would read `probe result (:24), embedding (:31)`. Any edit voids the
recorded hash and requires re-derivation.

## 4. The rule's earned facts, re-derived first-hand — REPRODUCED

Byte census on the retained CarrierV artifacts
(`…/arc3-loop1-round4/claims/c1/EX-04/out/`, read-only;
`RV-8/byte-census.txt`):

```
creation.hex file: 3274 B sha256 34f52280d3cdc740…
decoded creation : 1637 B sha256 3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226
runtime.bin      : 1562 B sha256 57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
runtime.hex decode == runtime.bin: True
occurrences of full runtime in creation: [20]   trailing bytes: [55]
```

`creation.bin` equals the decoded hex (1,637 B, same sha). This matches SC-3 §3
and the r5 erratum (`…r4…:43-44`: "CarrierV runtime at offset +20 in its
1,637 B creation"), and EX-08's retained census
(`…round4/claims/c1/EX-08/evidence-creation-embedding.txt`: same sizes,
digests, offset, 55 trailing bytes). **REPRODUCED byte-exact.**

Live probe (first-hand, this seat; `RV-8/probe-CarrierV-creation-6.4.0.json`,
stderr empty):

```
TMPDIR=/var/tmp/rv8-probe npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex hex --format json
→ exit 0; evidence_id ev_53732d0f8c67d15c…; functions: 0; kind: "unknown";
  decoded sha256 3c667396… (= the 1,637 B creation's own sha);
  subject.digest.sha256 34f52280… (= the hex text file)
```

The same id and payload are the sealed round-4 envelope EX-06 recorded at the
same absolute path (`…round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`,
`ev_53732d0f…`, 0 functions). Per the lane's own id-domain finding (`…r4…:26`)
this is same-path determinism, **not** independent corroboration; the
independent corroboration is the byte census above. The probe says 0 functions
on bytes that verbatim contain the 1,562 B dispatcher — both halves of the
rule measured on one blob. **REPRODUCED.**

r1 sealed envelope re-read: `…round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`
→ `ev_c80379e1…`, 0 functions, kind `unknown` (r1:24). **VERIFIED.**

Additional first-hand check of the rule's **plural** ("the r1 creation leg**s**
… byte-contain the full runtime"): r1's second creation leg, the 685 B
`Smoke_sol_Smoke.bin` (decoded sha `08299f31…`, the r1:43-44 decoded domain),
declares `CODECOPY` of **657 B from +28** at pc 16, and 28+657=685 = EOF; the
extracted 657 B tail begins `608060405260043610610049` (solc dispatcher
prologue), sha `f6c2de73…`. So both r1 creation legs embed their complete
runtime. This extends the corpus record (r1:31 names only Rv2Token) but does
not contradict it; the rule's plural is factually sound.

## 5. Falsifiable before → after on a scratch tree — REPRODUCED

SKILL.md is outside this seat's write scope, so the landing was simulated on
`git show <rev>:SKILL.md`: insert the exact `RV-8/rule15-sc3-1605b.txt` bytes
after rule #14's final line (`SKILL.md:255`, "never a carried-over number."),
before the blank lines preceding `## Config custody` (`SKILL.md:260`), then run
command A's exact split (`re.split(r'(?m)^- \*\*', craft)[1:]`) and
citation-resolution logic with corpus files read from the same rev
(`RV-8/landing-simulation.txt`):

| rev | state | rule_blocks | citation_resolved_rules | depth_score | knowledge/mapped/missing/dangling |
|---|---|---|---|---|---|
| `58c3db7` | before | 14 | 14 | 10.0 | 84 / 84 / [] / [] |
| `58c3db7` | after | **15** | **15** | 10.0 | 84 / 84 / [] / [] |
| `c625d5d` | before | 14 | 14 | 10.0 | 84 / 84 / [] / [] |
| `c625d5d` | after | **15** | **15** | 10.0 | 84 / 84 / [] / [] |

The diff is a pure insertion (`added_lines=23, removed_lines=0`); the last
block carries 8 refs, all valid; no existing SCOPE/counter is touched because
only the craft section changes. The frozen falsifiable ("`rule_blocks` 14 → 15
with the new rule's citations resolving under command A's pattern") is
**REPRODUCED** at both revs. SC-3's §5 numbers are correct.

## 6. Peer reconciliation — RV-7's F1 CONFIRMED; one duplicate-draft conflict

**RV-7 F1 (r3 erratum's `:24` pointer is dangling) — CONFIRMED first-hand**
(`RV-8/f1-r3-pointer.txt`). At `c418be0`, `40de383`, `58c3db7`, and `c625d5d`,
`…r3…:24` is the "Observation (RESULT — Rv2TokenOpt @EX-07)" line, and the
string "Creation blobs" occurs only at `:41`, inside the erratum itself. The
quoted sentence is r1's `:24`. So the r3 erratum's byte facts are true but its
relative `:24` pointer resolves to the wrong line in its own file. SC-3's draft
cites only `r3:41-51` and does **not** propagate the pointer. Disposition for a
later append-only pass: re-point to `r1:24` or drop the `:24` token.

**Duplicate-draft conflict (for VZ/CN).** RV-7's alternative bullet
(`RV-7/rule15-bullet.md`, 1,565 B, 23 lines, sha256 `ccbc5cdb…`) also simulates
to `rule_blocks=15, citation_resolved_rules=15, depth_score=10.0` (6 refs, all
resolve; measured this seat). Both drafts are sound, but there is **one** rule
slot. Landing both was measured this seat (`rule_blocks=16`,
`citation_resolved_rules=16`, depth 10.0), which fails the frozen claim's
literal 14 → 15. Land exactly one. Recommendation: **SC-3's verbatim**
(it is the assigned c3 deliverable and this seat hash-verified it);
RV-7's is a valid substitute if the richer measured numbers (VaultB +34/1,655 B
etc.) are preferred.

**Minor correction to SC-3 §2's rationale.** SC-3 says candidates (a)/(b)
"mostly" lack command-A-resolvable corpus evidence. That is true for (a), but
not for (b): coupled-landing discipline has corpus anchors at
`corpus/knowledge/2026-10-13-ghidra-install.md:72-76` ("repaired to 34 in the
same commit as this erratum … coupled PROVINCE repair") and
`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` ("superseded at
the same commit … `PROVINCE.md:91-93`"). (b) was landable-thin, not unlandable.
The choice of (c) still stands on evidence depth; this note does not touch the
rule text.

Wording nit **N2** (non-blocking): "Word zero-findings at their class" is
awkward; "State zero-findings at their class" would read better. Editing voids
the recorded hash.

## 7. Per-item verdicts

| Item | Verdict | Evidence |
|---|---|---|
| Command A baseline at `c625d5d`/`58c3db7` (`rule_blocks=14`, 84/84, `missing []`, `dangling []`) | REPRODUCED | §1, `RV-8/commandA-before.txt` |
| SC-3 draft self-identity 1,605 B / 23 lines / `763c44b5…` | VERIFIED | §2, `RV-8/draft-identity.txt`, `RV-8/rule15-sc3-1605b.txt` |
| Draft parses as exactly one craft block; 8 pattern refs all resolve | VERIFIED | §2, §3, §5 |
| Citation content anchors (r1:24/:31, r3:27/:41-51, r4:17/:25/:34/:39-46, QUALITY.md:21) | VERIFIED | §3 table |
| r1:24 attribution of the embedding half (N1) | VERIFIED with non-blocking nit | §3 |
| CarrierV byte facts (1,637 B `3c667396…`; 1,562 B `57d6fd0a…`; +20; 55 trailing; one occurrence) | REPRODUCED byte-exact | §4, `RV-8/byte-census.txt` |
| Live creation probe: exit 0, 0 functions, kind `unknown`, `ev_53732d0f…` | REPRODUCED | §4, probe JSON |
| r1 sealed envelope `ev_c80379e1…` / 0 functions | VERIFIED | §4 |
| Rule's plural (r1's Smoke creation leg embeds its full runtime) | VERIFIED first-hand (new derivation: 657 B at +28 in 685 B) | §4, `RV-8/byte-census.txt` |
| Scratch-tree landing: `rule_blocks` 14→15, 15/15 resolve, depth 10.0, other counters unchanged | REPRODUCED at both revs | §5, `RV-8/landing-simulation.txt` |
| RV-7 F1 (r3 erratum `:24` dangling) | CONFIRMED | §6, `RV-8/f1-r3-pointer.txt` |
| RV-7 alternate bullet also reads 15/15 | CONFIRMED; duplicate-slot conflict | §6 |
| SC-3 §2 claim that candidate (b) lacks corpus grounding | CORRECTED (minor; does not affect the rule) | §6 |

No item is UNVERIFIABLE. No DISCREPANCY was found in SC-3's numbers.

## 8. Landing spec for the integrator

1. Append the exact bytes of `RV-8/rule15-sc3-1605b.txt` (1,605 B, sha256
   `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`) after
   `SKILL.md:255`, before the blank lines preceding `## Config custody`
   (`SKILL.md:260`). Do not reflow, re-indent, or re-wrap — the hash binds the
   bytes.
2. Do **not** also land RV-7's bullet; one rule per slot.
3. Expected command A at the landing commit: `rule_blocks=15`,
   `citation_resolved_rules=15`, `depth_score=10.0`, `knowledge_files=84`,
   `mapped=84`, `missing=[]`, `dangling=[]`, `coverage_score=10.0`.
4. Optional follow-ups (not this seat's write scope): an append-only re-point
   of the r3 erratum's `:24` token (F1); optionally fix N1/N2 in a later
   revision, re-hashing the draft.

## 9. Evidence files (`…/claims/c3/RV-8/`)

- `commandA-before.txt` — command A at `c625d5d` and `58c3db7` (verbatim).
- `draft-identity.txt` — draft byte count, line count, sha256, bullet parse, ref count.
- `rule15-sc3-1605b.txt` — the exact 1,605 B landing copy (sha256 `763c44b5…`).
- `landing-simulation.txt` — before/after counters at both revs, pure insertion.
- `byte-census.txt` — CarrierV decode/embedding + r1 Smoke preamble derivation.
- `probe-CarrierV-creation-6.4.0.json` — live 6.4.0 probe envelope (exit 0).
- `probe-creation.stderr.txt` — empty.
- `f1-r3-pointer.txt` — `:24` line + "Creation blobs" hits at four revisions.

## 10. Custody

`git status --porcelain` after this seat shows ` M .ufo/waves/arc2-loop1-round10/C3.md`
(a file this seat did not touch or write) and `?? .ufo/waves/arc3-loop1-round6/`
(the wave tree). No tracked file, corpus entry, gate, PROVINCE/SKILL/SCORECARD/
LOG, or git object was modified. Scratch remains under `/dev/shm/rv8/` and
`/var/tmp/rv8-probe/`.
