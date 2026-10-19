# SC-3 — c3 depth rule: rule #15 draft (parsed-and-empty ≠ byte-absence)

Seat: SC-3, chain c3 (depth), wave arc3-loop1-round6, 2026-10-19.
Repo HEAD at seat time: `c625d5d` (records; work `58c3db7`). All numbers
below re-derived first-hand this seat (lane rule #14); no value quoted from a
prior seat or round without re-derivation. Write scope honored: only this
artifact dir was created; git untouched; SKILL.md, corpus, gates read-only.

## 1. Baseline re-derivation (command A, SCORECARD.md:88-124)

Run verbatim per the recipe at both source commits (scratch:
`/dev/shm/sc3/cmdA_c625d5d.json`, `/dev/shm/sc3/cmdA_58c3db7.json`):

- `c625d5d` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}`
- `58c3db7` → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "rule_blocks": 14}`

Verdict: frozen-claim "before" values (`rule_blocks=14`, `knowledge_files=84`,
`mapped=84`, `missing=[]`, `dangling=[]`) — **REPRODUCED** first-hand at both
revs. `git diff --stat c625d5d 58c3db7 -- SKILL.md` is empty (craft section
identical at both revs).

## 2. Candidate chosen: (c) parsed-and-empty ≠ byte-absence

Chose candidate (c) over (a) census-checked-vs-instrument-graded and (b)
coupled-landing discipline because (c) is the only one whose full evidence
chain lives in corpus/knowledge entries with citable, in-bounds lines (the
command-A citation pattern), and it is the round-5 sweep's own framing of its
biggest catch: SCORECARD.md:1657-1660 (round-5 C2 section) — "the r4
initcode-absence sentence (runtime IS byte-embedded in initcode at +20 —
parsed-and-empty is the probe result, not byte absence)". Candidates (a)/(b)
are real lessons but their earning evidence sits mostly in `.ufo/waves/`
artifacts, which the command-A pattern does not resolve.

## 3. First-hand evidence for the rule's content (this seat's own runs)

Carrier: `CarrierV` creation blob from retained round-4 evidence
(`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/`, read-only).

Byte census (this seat, /dev/shm scratch script):

- `creation.hex` decodes to 1,637 B, sha256 `3c6673966d821d9d…` (= r4 entry
  `:12` "creation 1,637 B `3c667396…`").
- `runtime.bin` is 1,562 B, sha256 `57d6fd0ae0da0019…` (= `:12` "runtime
  1,562 B `57d6fd0a…`"); `runtime.hex` decodes byte-identical to `runtime.bin`.
- The full runtime occurs inside the creation blob at **offset +20**, 55
  trailing bytes after it — byte-exact match to the r5 erratum
  (`2026-10-19-arc3-r4-evm-vyper-leg.md:43-44`) and to the earlier EX-08
  census (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-08/evidence-creation-embedding.txt`,
  same sizes, same digests, same offset +20, same 55 trailing bytes).

Live probe (this seat): `mkdir -p /var/tmp/sc3-recheck && TMPDIR=/var/tmp/sc3-recheck
npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex hex --format json`
→ **exit 0, `functions` = 0, `bytecode.kind` = "unknown"**, evidence id
`ev_53732d0f…`. That id is byte-identical to the sealed round-4 envelope
EX-06 recorded at the same absolute path
(`.ufo/waves/arc3-loop1-round4/claims/c1/EX-06/probe/CarrierV-creation-6.4.0.json`,
same id, also 0 functions) — same-path determinism, consistent with the r4
entry's `:26` id-domain finding; not independent corroboration, which is what
the byte census above provides.

Cross-pin: the r1 sealed envelope
(`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json`,
`ev_c80379e1…`) also reads 0 functions — the r1 entry `:24` result, re-read
from the sealed bytes.

Together: the probe says **0 functions** on a blob whose bytes verbatim
contain the full runtime dispatch table — the two halves of the rule, both
re-derived at this seat on the same blob. Verdict: the distinction —
**VERIFIED** (first-hand), and the r4/r5 erratum numbers — **REPRODUCED**
byte-exact (+20 / 1,637 / 1,562 / 55).

## 4. Rule #15 draft (exact proposed SKILL.md text)

Self-identity of the draft bytes below: 1,605 B, 23 lines, sha256
`763c44b504f9964d970a741ef56a8331d85e7a362a191d09025e38d14a6fd0d1`
(re-derive after any edit; per craft rule about self-identity, a mismatching
hash voids the validation in §5).

Landing spec: append as the next bullet at the end of the `## Queue-drain
craft` section (after the current rule #14 bullet ending "never a carried-over
number.", before the blank lines preceding `## Config custody for live-probe
rounds (SOP)`).

```markdown
- **A parsed-and-empty result is a statement about the parser's scope, never
  proof of byte absence — settle byte questions with a census (decode, locate,
  hash), not with the probe's function count.** The r1 creation legs probed
  0 functions on blobs that byte-contain the full runtime
  (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`); the round-3
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
  dispatch" (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34`). Word
  zero-findings at their class (parsed-and-empty vs excluded-from-inventory,
  `corpus/QUALITY.md:21`) and only then claim or deny byte presence.
```

## 5. Falsifiable before → after, demonstrated on a scratch tree

SKILL.md is outside this seat's write scope, so the "after" was demonstrated
by appending the §4 bytes to the craft section extracted from
`git show <rev>:SKILL.md` in /dev/shm and running command A's exact rule-split
(`re.split(r'(?m)^- \*\*', craft)[1:]`) and citation-resolution logic
(corpus files read from the same rev via `git show`):

| rev | rule_blocks | citation_resolved_rules | depth_score |
|---|---|---|---|
| `58c3db7` before | 14 | 14 | 10.0 |
| `58c3db7` after | **15** | **15** | 10.0 |
| `c625d5d` before | 14 | 14 | 10.0 |
| `c625d5d` after | **15** | **15** | 10.0 |

The new rule parses as exactly one block (no stray `- **` line starts), is
the 15th/last block, and carries 8 pattern citations, all resolving in-bounds
(§6). Verdict: the frozen falsifiable "rule_blocks 14 → 15 with the new
rule's citations resolving under command A's pattern" — **REPRODUCED** on the
scratch tree at both revs. The integrator lands §4 verbatim; command A then
reads the same numbers on the real tree.

## 6. Citation list (each re-checked for existence + line bounds this seat)

| citation | what it evidences | resolves |
|---|---|---|
| `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24` | r1 creation legs 0 functions / parsed-and-empty, not excluded | yes (file 46 lines) |
| `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31` | r1 erratum: 0-function result is tool scope, "not byte-level absence"; runtime embedded in blob | yes |
| `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51` | r5 erratum correcting r3 `:24` "creation blobs carry no runtime dispatch table"; runtime embeddings measured | yes (file 57 lines) |
| `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46` | r5 erratum: "creation probes parse empty while the runtime bytes are present verbatim"; CarrierV at +20 | yes (file 63 lines) |
| `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17` | r4 initcode legs uniformly parsed-and-empty (the sentence later corrected) | yes |
| `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:27` | raw-on-hex-text trap: exit 0 / 0 functions, "a probe-input trap, not a carrier defect" | yes |
| `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:25` | same trap class reproduced on Vyper carriers | yes |
| `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:34` | tool limitation: "empty results do not prove absence of dispatch" | yes |

Non-pattern context inside the rule (`corpus/QUALITY.md:21`, the
parsed-and-empty/excluded-from-inventory row) is outside command A's
`corpus/knowledge/` pattern — verified present at `corpus/QUALITY.md:21`
(grep) and it does not affect resolution either way.

## 7. Per-item verdict summary

- Baseline command A (`rule_blocks=14`, `knowledge_files=84`, `mapped=84`,
  `missing=[]`, `dangling=[]`) at `c625d5d` and `58c3db7` — **REPRODUCED**
  (first-hand, §1).
- Frozen-claim scope: craft section holds 14 rules, each bounded by corpus
  citations; 14/14 resolve — **REPRODUCED** (§1, §5 "before" rows).
- parsed-and-empty ≠ byte-absence (probe: 0 functions vs bytes: runtime
  verbatim at +20) — **VERIFIED** first-hand on CarrierV creation (§3); r1
  sealed envelope re-read agrees (`ev_c80379e1…`, 0 functions).
- r5-erratum measured numbers (1,637 B creation `3c667396…`; 1,562 B runtime
  `57d6fd0a…`; offset +20; 55 trailing) — **REPRODUCED** byte-exact, and
  independently agree with EX-08's retained census (§3).
- Round-5 sweep attribution of the catch (SCORECARD.md:1657-1660) —
  **VERIFIED** (path:line, quoted in §2).
- Rule #15 draft lands the frozen falsifiable (rule_blocks 14 → 15, all
  citations resolve) — **REPRODUCED** on scratch trees at both revs (§5).
- Not done here (by design): landing the rule into SKILL.md (integrator's
  move), and first-hand re-runs of the r3/r4 non-creation legs — the draft
  cites them at line level and the r5 audit already re-derived them; this
  seat re-derived the rule's core instance only.

## 8. Scratch and custody notes

Scratch: `/dev/shm/sc3/` (command-A JSONs, `rule15.txt`),
`/var/tmp/sc3-recheck/` (probe output). No writes outside
`.ufo/waves/arc3-loop1-round6/claims/c3/`; no git mutation; custody paths
read-only. `git status` delta from seat start: only this wave's untracked
artifact tree.
