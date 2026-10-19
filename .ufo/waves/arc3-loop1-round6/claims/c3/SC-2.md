# SC-2 — c3 (depth): independent verification of SC-3's rule #15 — one citation CORRECTED

Seat SC-2, chain c3, wave arc3-loop1-round6, kaidoku-shokunin. Measured
2026-10-19 on this host. HEAD `c625d5de57e045188b5ce8cd450a57b349f90785`
(records; work `58c3db7` — `git log --oneline -3` re-read this seat). Every
number below is first-hand this session (lane rule #14); scratch was
`/var/tmp/sc2-arc3r6/`, evidence under `claims/c3/SC-2/`. Write scope honored:
only this artifact dir was created; SKILL.md, corpus, gates, PROVINCE.md and
LOG.md untouched; git read-only.

## 0. Deliverable in one line

SC-3's rule-#15 draft is substantively correct and its falsifiable metric
reproduces exactly (`rule_blocks` 14 → 15, `citation_resolved_rules` 14 → 15,
`depth_score` 10.0 at both revs) — **but as written it carries one
mis-anchored citation**: the tool-limitation quote is cited to
`2026-10-19-arc3-r4-evm-vyper-leg.md:34`, where line 34 is the `## Erratum`
header at both command-A revs (the phrase lives at `:29`, and `:34` did not
even exist before the erratum was appended). Command A's checker is
bounds-only, so the defect is invisible to the metric. **Correction:** one
token, `:34` → `:29`; corrected draft re-derived at 1,605 B / 23 lines /
sha256 `6967b1e3…`; simulated landing at both revs still reads 15/15, depth
10.0. Land the corrected text (patch in §8), not SC-3 §4 verbatim.

## 1. Baseline re-derivation — command A (SCORECARD.md:88-124)

The recipe was transcribed verbatim (one added `detail` array for the audit;
the recipe's nine printed keys are unchanged). Run against immutable Git
objects at both source revs:

```
$ python3 commandA.py 58c3db7
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [],
 "rule_blocks": 14, ...per-rule detail...}

$ python3 commandA.py c625d5d
  identical: citation_resolved_rules 14, coverage 10.0, depth 10.0,
  knowledge_files 84, mapped 84, missing [], dangling [], rule_blocks 14
```

Transcripts: `SC-2/commandA-before-58c3db7.json`,
`SC-2/commandA-before-c625d5d.json`. `git diff --stat 58c3db7 c625d5d --
SKILL.md corpus/` is empty; working-tree `SKILL.md` sha256
`8e56f3d9…88a68bf` equals `git show 58c3db7:SKILL.md` (re-measured).

Verdict: frozen-claim baseline (`rule_blocks=14`, 84/84, no missing/dangling)
— **REPRODUCED** first-hand at both revs.

## 2. Draft identity — SC-3's self-identity re-derived

The fenced block in `claims/c3/SC-3.md` §4, extracted byte-for-byte:

| convention | bytes | lines | sha256 |
|---|---|---|---|
| fenced block as-is (no final newline) | 1,604 | 23 | `f34846be…2fec47` |
| block + trailing newline (as a bullet in a file) | **1,605** | **23** | **`763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`** |

SC-3's claimed 1,605 B / 23 lines / `763c44b5…` — **REPRODUCED**, and the
convention is stated: the claim holds only with the bullet's final newline.
The block contains exactly one `^- \*\*` line start (its first line), so it
parses as exactly one craft rule. Extracted copy:
`SC-2/rule15-sc3.txt` (= `sha256sum` above); identity record:
`SC-2/draft-identity.txt`.

## 3. Simulated landing — the frozen falsifiable, both revs

Landing position reproduced per SC-3's spec: insert after rule #14's last line
("never a carried-over number.", `SKILL.md:255`) and before the blank lines
preceding `## Config custody` (`SKILL.md:260`).

| rev | state | rule_blocks | citation_resolved_rules | depth_score | coverage_score | 84/84 |
|---|---|---|---|---|---|---|
| `58c3db7` | before | 14 | 14 | 10.0 | 10.0 | yes |
| `58c3db7` | after (SC-3 text) | **15** | **15** | **10.0** | 10.0 | yes |
| `c625d5d` | before | 14 | 14 | 10.0 | 10.0 | yes |
| `c625d5d` | after (SC-3 text) | **15** | **15** | **10.0** | 10.0 | yes |
| `58c3db7` | after (corrected, §4) | **15** | **15** | **10.0** | 10.0 | yes |
| `c625d5d` | after (corrected, §4) | **15** | **15** | **10.0** | 10.0 | yes |

The 15th rule carries 8 command-A-pattern refs, all in bounds; the
non-pattern `corpus/QUALITY.md:21` reference is task-external to the metric
(row 11 exists, §4). Transcripts:
`SC-2/commandA-after-simulated-{sc3,corrected}-{58c3db7,c625d5d}.json`.

Insertion integrity (measured, not asserted): removing the inserted bullet +
its newline from the simulated `SKILL.md` reproduces the original byte-for-byte
(`sim.replace(bullet + "\n", "", 1) == orig` → True at both revs); rules 1-13
are byte-identical; rule #14 is unchanged modulo the split boundary's trailing
blank lines (`rstrip()` equal). The simulated file is 413 lines / 33,973 B
(390 + 23), sha256 `c4afd511…4be925a9` for the corrected text
(`SC-2/SKILL-c625d5d-simulated-corrected.md`). The patch in §8 applies cleanly
to `git show c625d5d:SKILL.md` and yields exactly that hash (measured:
`patch -s` rc=0, `cmp` identical).

Verdict: frozen falsifiable "rule_blocks 14 → 15 with the new rule's
citations resolving" — **REPRODUCED**; existing counters untouched —
**VERIFIED**.

## 4. Citation audit — bounds AND content (the correction)

Command A validates only `1 <= start <= end <= file-lines` (SCORECARD.md:109,
113-114). I additionally checked, for each citation, that the phrase SC-3 says
it evidences is present **inside the cited span** at both revs. Full
transcript: `SC-2/citation-audit.txt`.

| citation | span content re-derived | verdict |
|---|---|---|
| `…r1-evm-real-solc.md:24` | "0 functions", "parsed-and-empty" MATCH; **no containment token** — "byte-contain the full runtime" is at `:31` | ANCHOR NOTE (see below) |
| `…r1…:31` | "not byte-level absence", "embeds the runtime" MATCH | VERIFIED |
| `…r3-evm-optimizer-shapes.md:41-51` | "parsed-and-empty", "byte-exactly embedded", "not proof of byte absence" MATCH | VERIFIED |
| `…r4-evm-vyper-leg.md:39-46` | "parsed-and-empty", "creation probes parse empty while the runtime bytes are present verbatim", "offset +20" MATCH | VERIFIED |
| `…r4…:17` | "uniformly **parsed-and-empty**" MATCH | VERIFIED |
| `…r3…:27` | "0 functions", "probe-input trap, not a carrier defect" MATCH | VERIFIED |
| `…r4…:25` | "parsed-and-empty, the r1/r3 trap class" MATCH | VERIFIED |
| `…r4…:34` | **NO-MATCH** — line 34 is `## Erratum (arc3-loop1-round5 …)` | **CORRECTED → `:29`** |
| `corpus/QUALITY.md:21` | row 11: "Empty/zero findings must state whether the surface was parsed-and-empty or excluded-from-inventory" MATCH | VERIFIED |

**Correction, measured.** The phrase "empty results do not prove absence of
dispatch" is at `…r4-evm-vyper-leg.md:29` at **all four** relevant revs
(`40de383`: 29, `71668cc`: 29, `58c3db7`: 29, `c625d5d`: 29). At
`40de383`/`71668cc` the file had 32 lines, so `:34` did not exist at all; at
the two command-A revs `:34` is the erratum header. The draft's `:34` is a
line-number slip, not a corrupted quote. Corrected draft:
`SC-2/rule15-corrected.txt`, 1,605 B / 23 lines /
sha256 `6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`.

**Anchor note (not a blocker).** The draft's first sentence reads "The r1
creation legs probed 0 functions on blobs that byte-contain the full runtime
(`…:24`)". `:24` supports the 0-function half only; containment is `:31`'s
fact, cited in the next clause. The aggregate sentence is grounded, but the
`:24` placement invites the same over-claim the rule warns about. Optional
tightening: move the `:24` citation after "probed 0 functions" or cite
`:24,:31` together. Not required for landing.

**Why this matters beyond one token:** the draft at `:34` reads
`citation_resolved_rules = 15`, `depth_score = 10.0` — the metric cannot see
the slip. So "citations resolve" is a bounds statement, never a content
statement; the landing gate must include this manual anchor pass (the same
class as craft rule #14's "the written verify must itself reproduce").

## 5. Does the draft propagate the r3 erratum's dangling `:24` pointer?

RV-7 (peer artifact) found that the r3 erratum at `…r3…:41` claims to correct
`":24" "Creation blobs carry no runtime dispatch table"`, but that sentence
never existed in the r3 entry. I re-derived it first-hand
(`SC-2/r3-pointer-check.txt`):

- `git grep "Creation blobs" <rev> -- …r3…` → none at `c418be0` and
  `40de383`; only the erratum itself at `58c3db7`/`c625d5d` (`:41`).
- r3 `:24` is the "Observation (RESULT — Rv2TokenOpt @EX-07)" row at both
  `c418be0` and `c625d5d`.

SC-3's **rule text** cites the erratum only at `:41-51` and does not repeat
`:24` → **does not propagate** the dangling pointer (VERIFIED). SC-3's §6
provenance table does describe the erratum as "correcting r3 `:24`"; that
description inherits the erratum's own bad pointer but is not landing text.
For the record, RV-7's competing draft also avoids `:34` (grep: no `:34`
anchor; 6 command-A refs, 1,564 B / 23 lines), but I did not re-run its
simulated landing.

## 6. The rule's core instance — re-derived first-hand

The rule asserts parsed-and-empty ≠ byte-absence. Same carrier, both halves,
this seat (`SC-2/byte-census.txt`, `SC-2/probe-summary.txt`):

Byte census (retained r4 `EX-04/out/`, read-only):
- `creation.hex` decodes to **1,637 B**, sha256 `3c6673966d821d9d…94a226`;
  `creation.bin` identical. Input ASCII file sha256 `34f52280…3ccd92`.
- `runtime.bin` is **1,562 B**, sha256 `57d6fd0ae0da0019…91dae0`;
  `runtime.hex` decodes byte-identical to it.
- The full runtime occurs **once** inside the creation blob at **offset +20**,
  **55 trailing bytes** — byte-exact match to the r4 erratum (`:39-46`) and to
  SC-3's numbers.

Live probe (this seat, exit 0):
```
TMPDIR=/var/tmp/sc2-arc3r6 npx -y rea-agents@6.4.0 inspect-evm-interface \
  <repo>/.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex \
  hex --format json
→ functions = 0; bytecode.kind = "unknown"; bytecode.bytes = 1637;
  bytecode.sha256 = 3c667396…94a226; input sha256 = 34f52280…3ccd92;
  evidence_id ev_53732d0f8c67d15c…856bee13
```
The envelope's own limitation string says: "Empty results do not prove the
absence of callable dispatch." — the exact class the draft cites at r4:29.
The id equals SC-3's cited `ev_53732d0f…` because the request used the same
absolute path — same-path determinism (QUALITY row 15 / r3 `:30`), **not**
independent corroboration of the id. The independent corroboration is the
byte census above, which needs no REA.

Verdict: probe 0 functions vs bytes-verbatim-at-+20 — **VERIFIED** first-hand;
the r5-erratum numbers (1,637 / 1,562 / +20 / 55) — **REPRODUCED** byte-exact.

## 7. Frozen-scope checks (claims-frozen C3)

- "the lane's `SKILL.md` Queue-drain craft section holds 14 rules" —
  re-derived: 14 `^- \*\*` blocks inside `## Queue-drain craft ` at both revs
  (§1 detail array). **REPRODUCED.**
- Candidate (c) is the round-5 sweep's own framing of its biggest catch:
  `SCORECARD.md:1658-1659` (quote begins line 1658, within the cited
  1657-1660): "the r4 initcode-absence sentence (runtime IS byte-embedded in
  initcode at +20 — parsed-and-empty is the probe result, not byte absence)"
  — **VERIFIED** (path:line quoted).
- "rule_blocks 14 → 15 with the new rule's citations resolving under command
  A's pattern" — **REPRODUCED** (§3), with the content caveat (§4).

## 8. Corrected landing payload and recipe

Payload: `SC-2/rule15-corrected.txt` — SC-3 §4 bytes with the single
substitution `2026-10-19-arc3-r4-evm-vyper-leg.md:34` →
`…:29`. Identity: 1,605 B / 23 lines / sha256
`6967b1e3e7fbdb43492e191426399c0311ab3bf85ee307f1a181a3edd235511e`.
Patch: `SC-2/SKILL-rule15-corrected.patch` (against `SKILL.md`, +23/−0;
applies rc=0 to `git show c625d5d:SKILL.md`, result sha256
`c4afd511dff27fd08962c4f3db714ed533a824ce843e36d0a1d33f604be925a9`,
413 lines).

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch -p1 SKILL.md < .ufo/waves/arc3-loop1-round6/claims/c3/SC-2/SKILL-rule15-corrected.patch
sha256sum SKILL.md        # expect c4afd511dff27fd0…f604be925a9, 413 lines
# command A must then read rule_blocks=15, citation_resolved_rules=15,
# depth_score=10.0, knowledge_files=84, mapped=84, missing=[], dangling=[]
```

The integrator records the fresh landed identity in the landing receipt, not
inline (craft rule #14). If the wave prefers RV-7's wording instead, land
exactly one of the two drafts — both encode the same lesson and landing both
would duplicate it (rule #16 would be a near-restatement).

## 9. Per-item verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7`; `SKILL.md` identical at both, working tree clean for `SKILL.md`/`corpus/` | REPRODUCED |
| 2 | command A baseline at both revs: 14 rules, 14 resolved, 84/84, missing/dangling [], depth 10.0 | REPRODUCED |
| 3 | Draft self-identity 1,605 B / 23 lines / `763c44b5…` | REPRODUCED (trailing-newline convention stated) |
| 4 | Draft parses as exactly one rule block; 8 command-A refs | VERIFIED |
| 5 | Simulated landing: 14 → 15 blocks, 14 → 15 resolved, depth 10.0, all other counters unchanged | REPRODUCED (both revs) |
| 6 | Pure insertion (+23 lines; removal restores original bytes; rules 1-13 byte-identical) | VERIFIED |
| 7 | Citation `…r4-evm-vyper-leg.md:34` for the tool-limitation quote | **CORRECTED → `:29`** (phrase at :29 at all revs; :34 is the Erratum header; pre-erratum file had 32 lines) |
| 8 | Citation `…r1-evm-real-solc.md:24` for "blobs that byte-contain the full runtime" | ANCHOR NOTE — 0-function half is at :24, containment at :31 (same sentence cites :31); minor, non-blocking |
| 9 | Other 6 command-A citations + `QUALITY.md:21` content anchors | VERIFIED (all MATCH in-span) |
| 10 | r3 erratum's `:24` pointer is dangling; SC-3 rule text does not propagate it | VERIFIED (corroborates RV-7 F1) |
| 11 | Core instance: CarrierV creation 1,637 B `3c667396…`, runtime 1,562 B `57d6fd0a…` at +20, 55 trailing | REPRODUCED first-hand |
| 12 | Live probe: exit 0, 0 functions, kind unknown, decoded sha `3c667396…`, same-path id `ev_53732d0f…` | REPRODUCED first-hand |
| 13 | Frozen claim's falsifiable (14→15, citations resolving, depth 10.0) | REPRODUCED — with the §4 content caveat: command A is bounds-only, so this is not content verification |
| 14 | SC-3's claim that the draft is landable as-is | **CORRECTED** — land the §8 corrected text (or RV-7's), not §4 verbatim |

## 10. What I did NOT do / residuals

- Did not modify SKILL.md, corpus, gates, PROVINCE.md, LOG.md, SCORECARD.md, or
  any tracked file; git used read-only (`rev-parse`, `log`, `show`, `grep`,
  `diff`, `ls-files`). Simulated trees live only under `claims/c3/SC-2/` and
  `/var/tmp/sc2-arc3r6/`.
- Did not re-verify RV-7's alternative draft's metric run; I only grepped it
  for the `:34` anchor (absent) and counted its refs. If the parent lands
  RV-7's text, re-run command A against those bytes.
- Did not re-run the r3/r4 non-creation probe legs; the draft's core instance
  (creation-side) was re-derived first-hand (§6), and every other citation was
  content-anchored in the corpus text (§4).
- Residual for the integrator: after landing, re-derive the landed SKILL.md
  sha and re-run command A on the real tree; if a later append-only corpus
  edit shifts r4 line numbers, the `:29` anchor and every other line-number
  citation must be re-keyed (the lane's standing append-only discipline).
