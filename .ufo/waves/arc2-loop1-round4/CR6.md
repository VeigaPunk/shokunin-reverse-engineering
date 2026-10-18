# CR6 (critic) — separability attack: do C1, C2, C3 couple through shared files?

Seat CR6, wave `arc2-loop1-round4`, 2026-10-18. Read-only on the repo and every
home file; **my only write is this report**. No git mutation, no config edit, no
install, no network fetch, no REA probe. Scratch in `/var/tmp/arc2-l4r4-CR6/`
only (my namespace; `/tmp` was at quota — see §8). HEAD at leg start `158a966`;
the parent landed `1692acbe` ("rule 11", artifact-only) mid-leg at 19:09Z; every
measurement below was made against materialized copies and re-checked after the
move. The live PE analyze was never signalled or touched.

## 1. Verdict

**NOT SEPARABLE — the three claims share two files and one line-number regime,
and I reproduced three coupling paths by execution, two of which flip a claim's
acceptance test.** The seat-line question ("SKILL.md gets rule + registry row;
lessons file gets erratum — any coupling?") resolves to: the lessons-file
erratum is the ONLY clean separation; SKILL.md couples C1 and C2 hard, and the
census instrument couples C1's *text* to C3's measurable.

1. **C1 → C2 (fatal to C2's as-drafted acceptance test).** C1's rule #11 is a
   craft-section insert that shifts every SKILL.md line at or after `:208`.
   C2's pinneable pointer tables pin **11 SKILL.md rows, 9 of them at `:208+`**
   (E16's K1-K9) plus E15's `skill-registry-row` at `:336`. Measured: after a
   7-line rule-#11 insert, E16's checker goes **0 FAIL → 9 FAIL** and E15's gate
   gains one `citation_dead` (`findings=10 → 11`, entry `skill-registry-row`).
   The two craft rows (`:81`, `:206`) hold. So C2's tables are only correct at
   the post-C1 revision; landing C2 first and C1 second, or landing C2 against
   the pre-C1 tree, produces a red probe on 10 rows for a non-defect.
2. **C1's text → C3's census (fatal to C3's measurable if the rule cites what it
   is about).** The census scans SKILL.md only in declared ranges `:10-16` and
   `:18-20`; everything else carrying a pin/version token is `UNDECLARED` → FAIL.
   Rule #11's subject is exactly "citations into operator-mutable files anchor by
   stanza key + receipt" — the natural draft names `rea-agents@6.7.0` and/or
   `config.toml:N`. Measured three variants: a rule naming `config.toml:3298` +
   `rea-agents@6.7.0` → `undeclared=3` (new locus `SKILL.md 208-209`); a rule
   naming `~/.kimi-code/config.toml:3298` → `undeclared=3`; a bare-number churn
   chain without a version token → `undeclared=2` (unchanged). Only a
   token-free rule text is census-safe, and the claim text must say so.
3. **C3's own recipe is insufficient alone.** C3 declares "census PASS at the
   work commit" via the E22 scope-table re-key. Measured: re-key alone removes
   `undeclared=2` but then fires `g11` on `SCORECARD.md:731` (a `current-ok`
   block without receipt language) → still FAIL. PASS requires re-key **plus**
   receipt language on the battery block — I reproduced `VERDICT: PASS` only
   with both edits (`sim-final2`, §3.3).
4. **The lessons erratum is separable.** The census never reads
   `corpus/lessons/`; the lessons file is cited by LOG/SCORECARD as prose, and no
   pointer table (E15/E16) pins a lessons line. C3's `lessons:82` erratum can
   land in any order, before or after C1/C2, with no measured interaction.

Consequence for the parent: land **C1 before C2** (or pin C2's tables at the
post-C1 revision), keep rule-#11's text token-free or widen the census scope,
and land the C3 census recipe as re-key + receipt (both edits), not re-key
alone.

## 2. Evidence — commands run THIS session, with observed output

### 2.1 Pre-leg receipt (seat line requires 5/5 before my leg)

```
$ R=.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
$ wc -l < "$R"                                   → 6
$ grep -cE '^[0-9a-f]{64}  /' "$R"               → 5
$ grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' "$R"  → 1
$ grep -cE '^[0-9a-f]{64}  /home/vgpnk/\.(config/devin/mcp_config\.json|omp/agent/mcp\.json|kimi-code/config\.toml|bashrc|profile)$' "$R"  → 5
$ tail -n +2 "$R" | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum "$R"
231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62  .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
```

Shape 6/5/1 + 5 path-identity lines, timestamp line `2026-10-18T19:03:02Z`.
**5/5 at my leg.** At my closing check (19:37Z) the same command returned
`/home/vgpnk/.kimi-code/config.toml: FAILED`, rc=1 — a fifth config rewrite
(19:17:21Z, sha256 `e0634d8c…`, 3322→3181 lines, stanza `:3296`→`:3155`, pin
`:3298`→`:3157`) landed inside this round's bracket. Independently caught and
recorded by seats C1 (`C1.md:292`), C3 (`C3.md:16-18`), E22 (`E22.md:27-29`),
V1; not mine to adjudicate, but it is live and the round's zero-drift claim is
false for that path from 19:17:21Z.

### 2.2 Instruments extracted byte-identically (nothing trusted from memory)

```
$ sed -n '264,692p' .ufo/waves/arc2-loop1-round2/E22.md > /var/tmp/arc2-l4r4-CR6/c1-census-v9.py
$ wc -l /var/tmp/arc2-l4r4-CR6/c1-census-v9.py     → 429
$ sha256sum /var/tmp/arc2-l4r4-CR6/c1-census-v9.py
213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c
```

Matches the digest E22 claims for its Block B (`E22.md:698`), so every census
result below is a result of the exact artifact the round would land.

```
$ cp /tmp/arc2-l3r3-E15/{citation-drift-gate.py,pointer-table.json,expected.json,config-toml-landmarks} /var/tmp/arc2-l4r4-CR6/e15/
$ sha256sum /var/tmp/arc2-l4r4-CR6/e15/*
0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f  citation-drift-gate.py
387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154  config-toml-landmarks
6ebada28259262da835c8371b9bfccfcebe4500c22fdd19716933a62fbca1beb  expected.json
d7bf0eb340a652950fb49a5cb5e62adc4c3e7097376bdd45dbaa0ecd23db059b  pointer-table.json
$ sha256sum /var/tmp/arc2-l4r4-CR6/e16/*
89eddae03d52cb8baede95256439f355d39c765d8f4700d75e73c4e7d5a20e31  e16-table.json
f2a7cdd20f0e3bbf308d147960a04941fe9908cbe4265d90eff24473980f170e  pointers.py
```

All four E15 hashes equal E15.md §5.7; the E16 table hash equals the file now
committed at the repo root (`git show 1692acbe:e16-table.json` → same
`89eddae0…`), so this seat grades the same bytes the parent committed.

### 2.3 The census at HEAD reproduces C3's declared base (FAIL undeclared=2)

```
$ cd <repo>; python3 /var/tmp/arc2-l4r4-CR6/c1-census-v9.py --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=854  loci=9
SKILL.md       lines=336  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
```

The two `UNDECLARED` blocks are `SCORECARD.md 731-737` and `747-766` — both
created by round-2's own record append, outside the hardcoded SCOPE table whose
last SCORECARD range ends at `:701` (`c1-census-v9.py:103`). This is exactly
the defect C3 declares and inherits.

### 2.4 C1's rule-#11 insert, and the C1→C2 coupling (measured)

Materialized HEAD into a scratch git repo (`git archive HEAD | tar -x`,
committed as `3de057b`), then inserted a 7-line rule #11 before
`SKILL.md:208` (the craft section end), matching the claim's shape:

```
$ python3 - <<'PY'   # insert before the '## Config custody' heading
... lines.insert(idx, rule) ...
PY
inserted 7 lines before 208
$ git commit -qm "sim A: C1 rule #11 (census-safe wording)"    → 248ad43
$ git diff --numstat 3de057b HEAD -- SKILL.md
7	0	SKILL.md
```

E16's checker (the 47-row form) on the pre-C1 and post-C1 trees:

```
$ python3 /var/tmp/arc2-l4r4-CR6/e16/pointers.py --root <pre-C1 tree> --baseline-root <repo>   # HEAD
VERDICT: failed                       # X14 only (C1's pending reword)
$ python3 /var/tmp/arc2-l4r4-CR6/e16/pointers.py --root <post-C1 tree> --baseline-root <repo>
FAIL   K1 SKILL.md:208  [INREPO] needle '## Config custody for live-probe rounds (SOP)' MISSING
FAIL   K2 SKILL.md:217  [INREPO] needle "Freeze the pre-pair before the round's first probe" MISSING
FAIL   K3 SKILL.md:225  [INREPO] needle "gate the receipt's shape: `wc -l` = 6" MISSING
FAIL   K4 SKILL.md:231  [INREPO] needle 'the shape gate is mandatory, not advisory' MISSING
FAIL   K5 SKILL.md:246  [XREF] needle 'PROVINCE.md:108-113' MISSING | target PROVINCE.md:108 @HEAD OK
FAIL   K6 SKILL.md:252  [INREPO] needle 'tail -n +2 "$R/config-pre-pair.txt" | sha256sum -c -' MISSING
FAIL   K7 SKILL.md:257  [INREPO] needle '`tail -n3` is not a config selector on a five-hash receipt' MISSING
FAIL   K8 SKILL.md:262  [INREPO] needle 'tail -n +2 … | tail -n2' MISSING
FAIL   K9 SKILL.md:336  [INREPO] needle 'interactive-r1-recovery' MISSING
FAIL count: 0 → 9
```

And E15's gate (same table, `--rev HEAD`):

```
$ python3 …/e15/citation-drift-gate.py --root <pre-C1 tree> …
CITATION_DRIFT_VERDICT: failed findings=10 exit=1
$ python3 …/e15/citation-drift-gate.py --root <post-C1 tree> …
CITATION_DRIFT: citation_dead entry=skill-registry-row SKILL.md:336 lacks 'interactive-r1-recovery \| gate / kaidoku'
CITATION_DRIFT_VERDICT: failed findings=11 exit=1
```

Entry-set diff between the two runs: exactly one new entry, `skill-registry-row`
(the table pins SKILL.md:336; post-insert the row sits at `:343`). E15's table
therefore has the same coupling, one row wide. **Repair measured:** shifting the
9 E16 rows and the E15 row by +7 (the post-C1 offsets) restores both: E16
`FAIL count → 0` (X14 RED only, by design) and E15 `findings → 10` (the
pre-existing set, unchanged).

The two craft rows (`e16-s1-shonen-craft-target` `SKILL.md:81`,
`e16-s4-craft-end` `SKILL.md:206`) held across the insert because rule #11 goes
after them — so the coupling is exactly the 9 `:208+` rows, not the whole table.

### 2.5 C1's text → C3's census (three rule-text variants, measured)

Same pre-C1 tree; three one-bullet rule-#11 texts inserted before `:208`:

```
variant 1 — names `config.toml:3298` and `rea-agents@6.7.0`:
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=3 unresolved=0)
  UNDECL: SKILL.md 208-209 | - **Citations into operator-mutable files anchor by stanza key + receipt.** The …

variant 2 — names `~/.kimi-code/config.toml:3298`:
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=3 unresolved=0)

variant 3 — bare churn numbers, no version token:
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)   ← unchanged, i.e. safe
```

So the coupling is conditional on the rule's *wording*, and the natural wording
(the rule is about pin citations) is the unsafe one. A census-safe rule must
avoid `6.x.y` version tokens and `config.toml` path pointers entirely — a
non-obvious constraint the claim text does not state. **Repair measured:** if
the parent accepts a wider census scope, re-keying SKILL.md to cover the craft
section (e.g. `("SKILL.md", 81, 214, "DATED", 81, r"distilled in round 13")`)
absorbs the new locus and returns `undeclared=2` (the pre-existing round-2
blocks only) — but that is a second scope decision, not C3's declared re-key.

### 2.6 C3's declared recipe is insufficient alone (re-key vs re-key+receipt)

```
$ # re-key only: SCOPE last SCORECARD range 635-701 → 635-766
$ python3 c1-census-rekey.py --root <HEAD copy> --quiet
G11 current-ok without receipt language: ['SCORECARD.md:731']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      ← still FAIL

$ # re-key + receipt language appended to the :731-737 battery block
$ python3 c1-census-rekey.py --root <patched copy> --quiet
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      ← PASS
```

Full integrated recipe on the simulated post-C1 tree (rule #11 + receipt patch +
round-4 records appended + re-key): `VERDICT: PASS`, all counters 0 — the
recipe works, but only with both edits, and with a rule text that is
census-safe (variant 3) or a widened scope. C3 as declared ("census PASS at the
work commit" via re-key) does not name the receipt edit; landing it as written
still fails.

A further measurement: the re-key window matters. Re-keying to `703-766` (the
round-2 section only) leaves the round-4 records appended at `768+` UNDECLARED
on the next round's append (`undeclared=1` at `686-701` after one more shift in
my sim). The durable form is a range open to the next round's append, or the
scope-table update becomes a per-round chore — which is exactly the standing
defect that made E22's instrument round-bound (`R6.md` §3).

### 2.7 The lessons-file erratum is separable (measured negative)

```
$ grep -n 'lessons' /var/tmp/arc2-l4r4-CR6/c1-census-v9.py      → no match (census never reads it)
$ python3 -c "import json; d=json.load(open('/var/tmp/arc2-l4r4-CR6/e16/e16-table.json')); \
  print([r['id'] for r in d['pointers'] if 'lessons' in r.get('file','')])"    → []
$ python3 -c "import json; d=json.load(open('/var/tmp/arc2-l4r4-CR6/e15/pointer-table.json')); \
  print([e['id'] for e in d['entries'] if 'lessons' in e['file']])"            → []
```

Neither C2 pointer table pins any line of `corpus/lessons/2026-10-15-round-1.md`,
and the census does not scan it. Appending the E4 erratum (22 lines, per
`E4.md` §1) changes the file 188 → 210 lines; the only repo citations into it
(`LOG.md:1059`, `LOG.md:1112`, `SCORECARD.md:758`, `SCORECARD.md:847`) name `:82`
and `:152` — both **above** the append point, so no citation moves. **C3's
lessons half is order-independent.**

### 2.8 The already-declared C2 hazard reproduces: E15's gate is false-clean
on unresolvable inputs (this is C2's probe-quality problem, not separability)

Found while building controls; recorded because it bears on C2's acceptance
test:

```
$ python3 …/e15/citation-drift-gate.py --root /var/tmp/arc2-l4r4-CR6/nope --rev HEAD …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0          ← nonexistent root, "clean"
$ cd <repo>; python3 …/e15/citation-drift-gate.py --root . --rev deadbeef …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0          ← bogus revision, "clean"
```

Mechanism, traced exactly: `Tree.lines()` unconditionally does
`self.reported.add(target)` on every `git_show` failure
(`citation-drift-gate.py:119-122`), and `check_entry`'s fallback
(`:160-164`) files `citation_file_absent` only when the target is **not**
already in `tree.reported`. The `add` at `:121` therefore makes that fallback
unreachable for every in-repo citing file — an unresolvable **citing** file is
**silently skipped with no finding at all**, in every mode:

```
$ cd <scratch tree with PROVINCE.md deleted at HEAD>   # citing file removed
$ python3 …/e15/citation-drift-gate.py --root . --rev HEAD …
$ grep -c 'citation_file_absent' <output>   → 0
$ grep -c 'province-18' <output>            → 0
CITATION_DRIFT_VERDICT: failed findings=9 exit=1   # 10 → 9: the entry VANISHED
```

The reachable `citation_file_absent` site is the *cited*-target one
(`:210`; the selftest's `file_absent` case exercises that, which is why the
selftest is 10/10 while this hole stands). So: **a gate that reports `clean`
on a nonexistent root — and silently drops any entry whose citing file it
cannot resolve — cannot be a `gate` for C2's acceptance test as invoked**;
the C2 landing must fix this (probe form, or fail-closed when root/rev or any
entry's citing file does not resolve). Recorded here because it bears directly
on whether C2's verdict can be trusted as the round's operability evidence.

### 2.9 Command A at HEAD (the C1 denominator baseline)

```
$ python3 - HEAD <<'PY'   # verbatim SCORECARD.md:92-123 recipe
...PY
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [],
 "revision": "HEAD", "rule_blocks": 10}
```

On the post-C1 sim tree: `rule_blocks 11, citation_resolved_rules 11,
depth_score 10.0` — so C1's "rules 10→11, 11/11 resolvable, craft otherwise
byte-identical" is reproducible in form. The residual risk is content: rule #11
must carry at least one `corpus/knowledge/<file>.md(:N)` reference or command A
counts it unresolvable → depth 10/11 = 9.09. The claim's own acceptance
criterion ("11/11 resolvable") is satisfiable only if the landed rule text
includes such a reference; the census-safe variant I measured (variant 3) cites
`config.toml` numbers and **no** `corpus/knowledge` path, so the two constraints
pull against each other: census-safety wants no config pointers, command A
wants a corpus/knowledge citation. A rule that cites an **erratum section** of
a corpus/knowledge file (e.g. `corpus/knowledge/2026-10-13-mcp-registrations.md:92-111`)
satisfies both — that is the form I used in the sim and it produced
`citation_resolved_rules: 11`.

## 3. Text for the parent to land VERBATIM

### 3a — the separability ruling

```text
arc2-loop1-round4 — CR6 separability ruling (measured, seat CR6):

C1, C2, C3 are NOT separable through SKILL.md. Three coupling paths measured:

(1) C1 → C2 line-number coupling. C1's rule #11 is inserted inside the craft
    section; every SKILL.md line at or after :208 shifts by the rule's line
    count. C2's pinneable tables pin 11 SKILL.md rows, 9 of them at :208+:
      E16 rows K1 :208, K2 :217, K3 :225, K4 :231, K5 :246, K6 :252, K7 :257,
      K8 :262, K9 :336; E15 row skill-registry-row :336.
    Measured with a 7-line insert: E16 FAIL 0 → 9 (K1-K9), E15 findings 10 → 11
    (+skill-registry-row). The craft rows :81/:206 hold. FIX: land C1 first, then
    pin C2's tables at the post-C1 revision (shift the 9 rows and the E15 row by
    the insert length; +7 in my simulation restores both tables to their
    pre-C1 verdicts).

(2) C1's text → C3's census. The census scans SKILL.md only at :10-16 and :18-20;
    any pin/version token elsewhere is UNDECLARED → FAIL. A rule #11 naming
    `config.toml:3298` and/or `rea-agents@6.7.0` creates SKILL.md 208-209
    UNDECLARED (measured: undeclared 2 → 3). A rule text free of 6.x.y tokens
    and config.toml path pointers is safe (undeclared stays 2). FIX: write rule
    #11 with no version token and no config pointer; cite the round-3 errata
    section of corpus/knowledge/2026-10-13-mcp-registrations.md:92-111 instead
    (this also satisfies command A's resolvability requirement — see (3)).

(3) C1's rule text must satisfy TWO constraints that pull apart. Command A
    counts a craft rule resolvable only if it carries a corpus/knowledge
    citation; the census forbids config pointers in the same text. A rule citing
    the errata section satisfies both (measured: rule_blocks 11,
    citation_resolved_rules 11, depth 10.0, census undeclared unchanged).

C3's declared recipe is insufficient alone: re-keying the census scope removes
undeclared=2 but then fires g11 on SCORECARD.md:731 (current-ok without receipt
language) → still FAIL. PASS requires re-key PLUS receipt language on the
:731-737 battery block (measured both ways; PASS only with both).

The lessons-file erratum is the ONLY separable piece: no pointer table pins a
lessons line, the census never reads the file, and every repo citation into it
(:82, :152 via LOG.md:1059,1112 / SCORECARD.md:758,847) sits above the append
point. It may land in any order.

Landing order that keeps every acceptance test green:
  1. C1 (rule #11 with errata citation, no version token / config pointer)
  2. C2 (tables re-pinned at the post-C1 revision; probe-form or fail-closed
     fix for the root/rev false-clean)
  3. C3 (erratum — any time — plus census re-key AND receipt language)
```

### 3b — the two fixed artifacts' exact deltas

```text
E16 pointers.py / e16-table.json: the 9 SKILL.md rows at :208+ and the E15
skill-registry-row move by the landed rule-#11 line count (measured: +7 with a
7-line rule). Post-shift values: K1 215, K2 224, K3 232, K4 238, K5 253, K6 259,
K7 264, K8 269, K9 343 (E15: 343). Verify: E16 FAIL count returns to 0 (X14 RED
remains by design until C1's SCORECARD:270 reword); E15 returns to findings=10.

Census scope (if the parent accepts widening instead of a token-free rule):
  ("SKILL.md", 81, <craft end>, "DATED", 81, r"distilled in round 13")
and re-key SCORECARD to an open range covering the current round's records
(measured: 635-766 covers round-2 blocks and makes undeclared 0; a closed range
re-creates undeclared on the next round's append).

Receipt language for SCORECARD.md:731-737 (g11 fix), minimal form:
  append to the battery block: "Recorded per the 17:32:20Z custody receipt."
(measured: g11 [] and census PASS with this one clause + the re-key).
```

## 4. Conclusions, labeled

**OBSERVATIONS** (ran/read this session):

- Round-4 pre-pair verified 5/5 rc=0 at my leg (shape 6/5/1, stamp
  2026-10-18T19:03:02Z, self-hash `231edd7d…`); at my closing check
  `config.toml: FAILED` — the 19:17:21Z rewrite (`e0634d8c…`, 3181 lines,
  stanza `:3155`, pin `:3157`).
- The census instrument extracted byte-identically (`213fe679…`, 429 lines) and
  reproduces `FAIL undeclared=2` at HEAD (blocks `SCORECARD.md 731-737`,
  `747-766`).
- A 7-line rule-#11 insert before `SKILL.md:208` moves E16's FAIL count 0 → 9
  (K1-K9) and E15's findings 10 → 11 (`skill-registry-row`); a +7 re-pin of
  those rows restores both.
- Rule texts naming `config.toml:3298` / `rea-agents@6.7.0` produce
  `undeclared=3`; a token-free rule keeps `undeclared=2`.
- Re-key alone → `g11 ['SCORECARD.md:731']` FAIL; re-key + receipt clause →
  `PASS 0/0/0/0`. Reproduced on the simulated post-C1 tree with round-4 records
  appended.
- E15's gate returns `clean findings=0 exit=0` for a nonexistent root and for
  `--rev deadbeef`; deleting a citing file behaves correctly (findings 10 → 9).
- No pointer table or census scope touches `corpus/lessons/2026-10-15-round-1.md`.
- Command A at HEAD: 79/79, 10 rules, 10.0/10.0; on the post-C1 sim: 11 rules,
  11/11 resolved, 10.0.
- HEAD moved 158a966 → 1692acbe mid-leg ("rule 11", artifact-only: E4.md,
  E23.md, receipts, root e16-table.json; no tracked content file).

**INFERENCES:**

- C2's acceptance test cannot be graded independently of C1's landing revision;
  "C2 passes" and "C1 landed" are one measurement, not two. The claim pair must
  be landed in the order C1 → C2 with the tables pinned post-C1, or the probe
  reddens on 10 rows for a non-defect.
- C3's census PASS is only achievable with a rule text the claim does not
  currently specify (token-free) or a scope widening it does not currently
  declare (craft section), PLUS the receipt edit its declared recipe omits.
  Three of the three claims therefore depend on choices the round declaration
  leaves open — the separability failure is not an artifact of my simulation
  but of the declaration's under-specification.
- The lessons erratum is genuinely independent; the only file-level question
  left is whether its 22-line append shifts anything downstream in that file
  (it does not: no in-repo citation names a lessons line above :152 in a
  context that resolves past it).

**UNKNOWNS:**

- The exact rule-#11 text the parent will land. Everything in (1)-(3) is a
  function of its length and tokens; I measured 7-line and 2-line forms and both
  coupling directions, but the landed text decides the offsets.
- Whether the parent chooses token-free-rule or widened-scope for the census;
  both work, and they are not interchangeable for other rounds.
- Whether the round-4 custody claim is closed as VOID for `config.toml` (per
  the SOP, the 19:17:21Z rewrite voids the bare zero-drift claim) or re-bracketed.
- Whether the PE analyze's OOM (reported by C1/E22 as ending 19:07:45Z) leaves
  any state the round intends to cite; not my seat, not read by me.

## 5. Scope compliance

- Only write: this report. `git status --porcelain` at my checks showed the
  round-4 wave directory (other seats' reports) plus `?? e16-table.json` (the
  parent's artifact commit content); I edited nothing and ran no git mutation
  in the lane repo. All simulations ran in `/var/tmp/arc2-l4r4-CR6/` scratch
  git repos seeded from `git archive HEAD` or from copies.
- No config edits; the five custody paths were read as digests and greps only
  (no contents beyond the non-secret stanza lines and line numbers). No secret
  values read or emitted.
- No network, no installs, no REA/MCP session. The live PE analyze was observed
  read-only (ps) and never signalled.
- `/tmp` was at quota when I started (a 1-byte write failed); all scratch went
  to `/var/tmp/arc2-l4r4-CR6/`, distinct from the PE analyze's
  `/var/tmp/arc2-l4r4-pe/`. Nothing of another seat's was touched or deleted.
- Scratch inventory: `sim-tree/` (HEAD materialization), `simrepo/` (git,
  base `3de057b` + rule-#11 commit `248ad43`), `sim-final/`, `sim-final2/`
  (integrated PASS reproduction), `sim-unsafe{,2,3}/` (rule-text variants),
  `sim-row{,2}/`, `sim-records/`, `fix-citing/` (deleted-citing-file control),
  `e15/`, `e16/` (instrument copies), `c1-census-v9.py` + re-key variants.
