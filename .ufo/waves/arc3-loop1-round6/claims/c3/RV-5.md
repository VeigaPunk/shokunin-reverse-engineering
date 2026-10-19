# RV-5 — c3 verification: SC-3's rule #15 (parsed-and-empty ≠ byte-absence)

Seat RV-5, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19.
HEAD `c625d5d` (records), work `58c3db7`. Every number below was re-derived
first-hand this seat from Git objects, retained bytes, or a live probe; no
prior seat's value is used as evidence, only as a claim to test.

Write scope honored: only `.ufo/waves/arc3-loop1-round6/claims/c3/RV-5.md`
and `…/c3/RV-5/` were created. `SKILL.md`, `corpus/`, `.ufo/gates/`, and all
tracked files are untouched; `git status --porcelain SKILL.md corpus/` is
empty. Scratch: `/dev/shm/rv5/` and `/var/tmp/rv5-probe/` (never `/tmp`).

## 1. Baseline re-derivation (command A, SCORECARD.md:88-124)

Recipe run verbatim (scratch copy `/dev/shm/rv5/cmdA.py`, reads `git show`
objects only):

- `c625d5d` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "c625d5d", "rule_blocks": 14}`
- `58c3db7` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "58c3db7", "rule_blocks": 14}`

(`RV-5/cmdA-c625d5d.json`, `RV-5/cmdA-58c3db7.json`.) `git diff --stat
c625d5d 58c3db7 -- SKILL.md` is empty. The frozen "before" — 14 rules,
84/84 mapped, 14/14 resolved, depth 10.0 — **REPRODUCED** first-hand.

## 2. SC-3's draft: identity and parse (claims, re-derived)

Extracted the single fenced `markdown` block from `claims/c3/SC-3.md` §4 and
measured it:

| property | SC-3 claim | RV-5 measurement |
|---|---|---|
| bytes | 1,605 | **1,605** |
| lines | 23 | **23** |
| sha256 | `763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1` | **`763c44b5…6fd0d1`** (exact) |
| parses as one block | yes | **yes** — one line starts `- **`, no internal rule start |
| command-A refs | 8 | **8** |

Landing point: the craft section starts at `SKILL.md:81`; rule 14 ends at
`SKILL.md:255` ("never a carried-over number."); four blank lines precede
`## Config custody` at `:260`. Appending after `:255` yields the 15th/last
block. Draft identity — **VERIFIED** byte-exact.

## 3. Citation audit — 8 bounds pass, one content mis-point (CORRECTED)

All 8 `corpus/knowledge/<name>.md:<n>[-<m>]` refs resolve under command A's
bounds rule (files at `58c3db7`: r1 46 lines, r3 57, r4 63). Content anchors
were then checked line-by-line (`RV-5/citations.txt`):

| citation | content claim | verdict |
|---|---|---|
| `r1:24` | creation legs 0 functions, parsed-and-empty, not inventory exclusions | PASS |
| `r1:31` | erratum: 1,971 B creation embeds runtime; tool scope, "not byte-level absence" | PASS |
| `r3:41-51` | r5 erratum: parsed-and-empty; runtime embeddings listed | PASS |
| `r4:39-46` | "creation probes parse empty while the runtime bytes are present verbatim" | PASS |
| `r4:17` | original "initcode carries no runtime dispatch table" | PASS |
| `r3:27` | raw-on-hex-text trap, "not a carrier defect" | PASS |
| `r4:25` | same trap reproduced on Vyper carriers | PASS |
| `r4:34` | quoted "empty results do not prove absence of dispatch" | **FAIL — corrected** |

**F1 (this seat): the tool-limitation quote is at `r4:29`, not `r4:34`.**
`58c3db7:corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29` reads
"…empty results do not prove absence of dispatch…"; `:34` is the
`## Erratum` heading (`sed -n '29p;34p'` shows both). The draft's `:34`
still bounds-resolves (34 ≤ 63), so the defect is content-level and score-
invisible — exactly the class rule #15 itself warns about. Minimal fix:
`…-vyper-leg.md:34` → `…-vyper-leg.md:29`. The corrected draft is byte- and
line-identical in length, 1,605 B / 23 lines, sha256
`6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`
(`RV-5/rule15-corrected.md`). SC-3's §6 table repeats the same mis-point
("`r4:34` … tool limitation") and should be read with this correction.

Minor note (not a defect): the draft's phrase "probed 0 functions on blobs
that byte-contain the full runtime (`r1:24`)" is supported in two parts —
0-functions at `r1:24`, byte containment at `r1:31`; the continuation
citation carries the second half.

## 4. The rule's core instance, re-derived first-hand

CarrierV from retained round-4 evidence
(`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/`, custody read-only;
`RV-5/byte-census.txt`):

- `creation.bin` 1,637 B sha256 `3c6673966d821d9d3366283ab2501c4e32167798ae89d92a21143f560994a226`; `creation.hex` decodes byte-identical.
- `runtime.bin` 1,562 B sha256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; `runtime.hex` decodes byte-identical.
- The runtime occurs in the creation blob at **offset +20, exactly once, 55 trailing bytes**.

Live probe this seat (exit 0):

```
TMPDIR=/var/tmp/rv5-probe npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex hex --format json
→ functions 0; bytecode.kind "unknown";
  decoded bytecode.sha256 3c667396… (= the 1,637 B creation blob's own sha)
  subject.digest.sha256 34f52280… (the hex-text carrier)
  evidence_id ev_53732d0f8c67d15c18110610cf228e550fb290537c87605706fc92a0856bee13
```

So one measurement pair on one blob: the probe parses **0 functions** while
the same bytes verbatim contain the full runtime — the rule's two halves.
The probe envelope is byte-identical (sha256 `0da3f5cd…`,
`RV-5/probe-CarrierV-creation-6.4.0.json`) to the sealed round-4 EX-06
envelope at the same absolute path: same-path determinism, not independent
corroboration; the independent leg is the byte census above. The r1 sealed
envelope re-read (`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`)
is `ev_c80379e1…`, 0 functions, kind `unknown` — agrees.

`corpus/QUALITY.md:21` is row 11, verbatim: "Empty/zero findings must state
whether the surface was parsed-and-empty or excluded-from-inventory…". The
draft cites it correctly; it sits outside command A's pattern and does not
affect resolution.

## 5. Peer-adjudication (RV-7's findings, re-derived independently)

- **RV-7 F1 (r3 erratum's `:24` pointer is dangling) — CONFIRMED.**
  `RV-5/erratum-pointer.txt`: at `c418be0`, `40de383` and `58c3db7`, r3 line
  24 is the Rv2TokenOpt RESULT row; r3 contains zero "Creation blobs"
  occurrences before `58c3db7`, and at `58c3db7` the only occurrence is the
  erratum's own quote at `:41`. The quoted sentence lives in the r1 entry at
  `:24`. SC-3's draft does not propagate the bad pointer (it cites only
  `r3:41-51` as "the same correction re-landed", which is true).
- **RV-7 F2 (r1's 1,971 B is the decoded-byte domain) — CONFIRMED.**
  `RV-2/Rv2Token.creation.hex` is 3,942 B of `0x`-prefixed ASCII; decoding
  gives 1,971 B, sha256 `04e07f54…`; the text file's own sha is
  `e6517fb7…`.
- **RV-7 F3 (candidate (a) without a corpus entry regresses depth) —
  CONFIRMED.** A counterfactual rule citing only `.ufo/gates/` and
  `.ufo/waves/` artifacts measures `rule_blocks=15,
  citation_resolved_rules=14, depth_score=9.33` (below).

## 6. Simulated landing (frozen falsifiable)

`SKILL.md` parked in `/dev/shm/rv5/`, corpus read from `git show 58c3db7`;
command A's exact split and citation logic (`RV-5/simulated-landing.txt`):

| variant | rule_blocks | resolved | depth | other counters |
|---|---|---|---|---|
| before (`58c3db7`) | 14 | 14 | 10.0 | 84/84, missing [], dangling [] |
| SC-3 draft as delivered | **15** | **15** | **10.0** | unchanged |
| RV-5 corrected (`:34`→`:29`) | **15** | **15** | **10.0** | unchanged |
| counterfactual no-corpus-refs rule | 15 | 14 | 9.33 | unchanged |

Verdict: the frozen falsifiable "rule_blocks 14 → 15 with the new rule's
citations resolving" — **REPRODUCED** at `58c3db7` (and structurally at
`c625d5d`, whose `SKILL.md` is identical). No existing rule changed (rules
1–14 compare equal before/after).

## 7. Per-item verdicts

| Item | Verdict |
|---|---|
| Baseline command A 14 rules / 84 files / mapped 84 / 14 resolved / depth 10.0 | **REPRODUCED** (both revs, §1) |
| Draft self-identity 1,605 B / 23 lines / sha `763c44b5…` | **VERIFIED** (exact, §2) |
| Draft parses as exactly one block; 8 refs; all bounds-resolve | **VERIFIED** (§2, §3) |
| Citation content anchors (`r1:24`, `r1:31`, `r3:27`, `r3:41-51`, `r4:17`, `r4:25`, `r4:39-46`, `QUALITY.md:21`) | **VERIFIED** (§3) |
| Citation `r4:34` for the tool-limitation quote | **CORRECTED** → `r4:29` (F1, §3) |
| CarrierV 1,637 B `3c667396…` / 1,562 B `57d6fd0a…` / +20 / 55 trailing / 1 occurrence | **REPRODUCED** first-hand (§4) |
| Probe says 0 functions on bytes containing the runtime (exit 0, kind unknown) | **REPRODUCED** live first-hand (§4) |
| r3 erratum `:24` pointer dangling (RV-7 F1) | **CONFIRMED** independently (§5) |
| r1 "1,971 B" decoded-domain note (RV-7 F2) | **CONFIRMED** (§5) |
| Candidate (a) unlandable without a corpus entry (RV-7 F3) | **CONFIRMED** (9.33 counterfactual, §6) |
| Rule #15 lands the frozen falsifiable | **REPRODUCED** on scratch tree (§6) |

## 8. Handoff

Land the **corrected** draft (`RV-5/rule15-corrected.md`, sha256
`6967b1e3…`, 1,605 B / 23 lines) after `SKILL.md:255` — the as-delivered
SC-3 text differs by one token (`r4:34` → `r4:29`) and is otherwise
identical. Command A should then read `rule_blocks=15,
citation_resolved_rules=15, depth_score=10.0` with 84/84 mapping unchanged.
Queue the r3 erratum pointer repair (`:24` → `r1:24`, or drop the pointer)
as an append-only corpus correction in a later round — this seat did not
touch `corpus/`. If the wave prefers SC-3's text verbatim, the only cost is
one content-mis-pointed (though bounds-valid) citation; the rule's substance
and citations are otherwise sound.

## 9. Evidence index

- `RV-5/cmdA-c625d5d.json`, `RV-5/cmdA-58c3db7.json` — baseline command A.
- `RV-5/draft-identity.txt` — draft bytes/lines/sha; corrected identity.
- `RV-5/citations.txt` — per-citation bounds + content anchors.
- `RV-5/byte-census.txt` — CarrierV sizes, digests, offset, probe summary.
- `RV-5/probe-CarrierV-creation-6.4.0.json` — live probe envelope.
- `RV-5/simulated-landing.txt` — before/after/counterfactual command A runs.
- `RV-5/erratum-pointer.txt` — r3 `:24` adjudication across three revs.
- `RV-5/rule15-corrected.md` — landing candidate (corrected draft, verbatim).
