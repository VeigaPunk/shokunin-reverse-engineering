# CR7 (critic) — attack on round-4's claims: smuggled work in C2's base, verdict inflation in C1/C2/C3, and the C2 honest-stop path

Seat CR7, wave `arc2-loop1-round4`, 2026-10-18. Read-only on the repo; **this
report is my only write**. Scratch: `/var/tmp/arc2-l4r4-CR7/` (moved off `/tmp`
after a real `Disk quota exceeded` at 19:06Z; `/tmp` was 13G/16G at 84% inode
use — independently hit by round-4 seat E4, `E4.md:§2.5`). No git mutation, no
config edits, no installs, no network. The live PE analyze was observed
read-only via `pgrep`; never signalled. HEAD at my start
`158a96611f22afdfa723131f3ec27f39138020e8`; HEAD moved mid-leg to
`1692acbe48ce0eac3b7c87698be59d8a04f46a08` ("rule 11", author `v <v@x>`,
19:09:10Z) — every measurement below names its revision.

**Pre-pair receipt (my leg):** `.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt`
verified **5/5** (`sha256sum -c` rc=0, five OK lines), self-hash
`231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62`, shape
6/5/1 — my own run, before any probe of mine (I ran none; my only executions
are Python stdlib and `git show`).

## 1. Verdict

**ATTACK SUSTAINED IN PART — the round's declared measurables are real but two
of its premises are false and three wordings are inflated.**

1. **C2's base is a lineage that does not exist.** The claim says "Base: E15's
   proven implementation + R3's F1-F3 fixes + R6's defect fixes". R3's F1-F3
   were written against **C3.md's** `verify-citations.py` (sha `0a3e7480…`,
   `R3.md:36-40`); R6's fixes against **E23's** `c2-census.py` (sha
   `cf5d65b6…`, `R6.md:123-131`). E15's gate (`citation-drift-gate.py`, sha
   `0c5350b1…` — re-verified by me this session) **does not contain** those
   fixes: its R3-F1-class defect is live (a table row missing `"file"` →
   uncaught `KeyError`, rc=1, the *declared "failed" code* for a configuration
   error — measured, §2.3), and R6's anchor-fragility defect is live in two
   entries that are now **false-dead on round-3's own landed repairs**
   (`province-18-kimi-pin`, `scorecard-59-pin-receipted` — §2.2).
2. **C2 smuggles four entry classes and a schema merge as if already "base".**
   E16's landed table (`e16-table.json`, sha `89eddae0…`, 51 rows) uses key
   `"pointers"` and kinds `line|symbol` plus BASELINE/QUOTED/EXTERNAL
   semantics; E15's gate reads key `"entries"` and knows only
   `anchor|exact|extracted`. **Measured: E15's gate run with E16's table
   returns `clean findings=0 exit=0`** — a silent no-op, not an error
   (`table.get("entries", [])`, `citation-drift-gate.py:252`). `kind:"line"`
   rows exit 2 (`pointer_table_unreadable`); `kind:"symbol"` rows exit 1
   (`citation_out_of_range`). No implementation of the claimed artifact
   exists.
3. **"kind=probe … gates nothing" contradicts the named artifact.** PROTOCOL
   defines a probe as *"a tool that cannot fail"* (`PROTOCOL.md:363-364`).
   E15's gate **can fail** (exit 1 on findings, exit 2 on config error,
   verdict map `clean/failed/could-not-evaluate`). Landing it unchanged makes
   it a **gate**, binding every Gate-standard clause; landing it with the exit
   neutralized makes it a probe but discards the "reports drift" teeth the
   claim also wants. The round must pick one, and the registry row's
   `gate|probe` field must match the artifact, not the intent.
4. **Verdict inflation, each measured:** "craft otherwise byte-identical" —
   the pre-existing craft bytes are identical (`cmp` of `SKILL.md:81-206`,
   sim1 vs sim2 → identical) but the insert shifts `SKILL.md:207+` and flips
   **one of the gate's own rows red** (`skill-registry-row`, `SKILL.md:336` →
   `:340`; findings 10 → 11 in my simulation). "Conformant frozen snapshot" —
   the digest pin is real and verified, but the committed expected verdict
   (`expected.json` `frozen_run`) is **never read by the script**
   (`grep -c 'frozen_run\|exempt'` → 0), so the Two-evidences clause's
   "contradicts the frozen run" mechanism is inert; and the pinned verdict
   (`failed findings=10 @679af5d`) will not match any run at the work commit.
5. **C3's premise and fix are confirmed and refined:** census at HEAD is
   `FAIL undeclared=2` (§2.5, my run); the declared *single-step* scope-table
   re-key clears `undeclared` but exposes `G11 ['SCORECARD.md:731']` → still
   FAIL; PASS is reachable by three measured variants (mine: DATED re-key +
   `tools_sha256` accepted by the receipt regex → PASS). The claim says
   "currently FAIL undeclared=2 … census PASS at the work commit" without
   naming the second half — that half is load-bearing and is a semantic
   decision.
6. **The C2 honest-stop path stays open — with two conditions.** §3 gives the
   wording; the structural reasons are `AXES.md:34-36` (a round is admitted
   only if every claim verifies and no axis is harmed; report every verdict),
   the round-3 precedent (`SCORECARD.md:832-833`, "unprovable (honest stop —
   not harmed)" / "not verified (honest stop)"), and `PROTOCOL.md:397-402`
   (a red gate is a recorded conformance defect, status-neutral; the
   integrator verifies committed evidence and **does not execute a sibling's
   gate**). No C1 or C3 measurable depends on C2 landing.

## 2. Evidence — exact commands and observed output (all run by me this session)

### 2.1 The receipt and the two artifacts I grade

```
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62  …config-pre-pair.txt

$ sha256sum /tmp/arc2-l3r3-E15/citation-drift-gate.py /tmp/arc2-l3r3-E15/pointer-table.json \
            /tmp/arc2-l3r3-E15/expected.json /tmp/arc2-l3r3-E15/config-toml-landmarks
0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f  citation-drift-gate.py
d7bf0eb340a652950fb49a5cb5e62adc4c3e7097376bdd45dbaa0ecd23db059b  pointer-table.json
6ebada28259262da835c8371b9bfccfcebe4500c22fdd19716933a62fbca1beb  expected.json
387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154  config-toml-landmarks
```

All four match `E15.md`'s §5.7 pins, so I graded the exact artifact E15
delivered, not a paraphrase. The redaction still holds: 3322 lines, 7
non-blank, `grep -icE 'token|key|secret|oauth|password|api'` → **0**.

### 2.2 E15's gate at HEAD: selftest green, live run red — and two false-deads on round-3's repairs

```
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --selftest --expected /tmp/arc2-l3r3-E15/expected.json
CITATION_DRIFT_SELFTEST: CLEAN cases=10 passed=10 failed=0 exit=0        (rc=0)

$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev HEAD \
    --table /tmp/arc2-l3r3-E15/pointer-table.json \
    --expected /tmp/arc2-l3r3-E15/expected.json --snapshot-dir /tmp/arc2-l3r3-E15
CITATION_DRIFT: citation_dead entry=scorecard-270-readme-bullet SCORECARD.md:270 cites corpus/README.md:157-157 …
CITATION_DRIFT: citation_dead entry=scorecard-270-readme-head-claim SCORECARD.md:270 cites corpus/README.md:160-160 …
CITATION_DRIFT: citation_dead entry=province-18-kimi-pin PROVINCE.md:18 states no resolvable pointer (pattern 'relocated it to :([0-9]+)' absent)
CITATION_DRIFT: citation_dead entry=scorecard-698-live-pin SCORECARD.md:698 cites @config-toml-landmarks:2940-2940, …
CITATION_DRIFT: citation_dead entry=scorecard-59-pin-receipted SCORECARD.md:59 states no resolvable pointer (pattern 'config\.toml:([0-9]+)' absent)
… (5 more @config-toml-landmarks rows) …
CITATION_DRIFT_VERDICT: failed findings=10 exit=1
```

The last two findings are the round-3 **repairs** biting back: round-3
re-anchored `PROVINCE.md:18` and `SCORECARD.md:59` to content-anchor form
(`PROVINCE.md:18` now reads "`config.toml:3298` at the 17:55:49Z receipt …
earlier pointers :2940 … :3227 … are historical"; `SCORECARD.md:59` now names
`[mcp_servers.rea]`), and E15's `extracted` patterns are pinned to the
*pre-repair wording* (`relocated it to :N`, `config.toml:N`). This is exactly
R6's finding 3 class ("the clause is gated on the literal … a detector whose
activation condition is drafter wording", `R6.md:43-49`) — **unfixed in the
artifact the round-4 claim names as its base**. Under the claim's own
ruling ("in-repo pinneable citations only, content-anchor form") these two
entries must be re-patterned or dropped, or the probe ships red on two
citations round-3's record calls "improved" (`SCORECARD.md:792`).

### 2.3 E15's gate fails open and mis-maps errors (R3-F1-class, live)

```
$ # E16's landed table (key "pointers", kinds line|symbol) handed to E15's gate
$ python3 …/citation-drift-gate.py --root . --rev HEAD --table e16-table.json \
      --expected …/expected.json --snapshot-dir …/  →  CITATION_DRIFT_VERDICT: clean findings=0 exit=0   rc=0

$ # unknown kind (E16's "line") through the same gate
$ python3 … --table <{"entries":[{"id":"e16-style","kind":"line",…}]}>  →  pointer_table_unreadable … exit=2  rc=2

$ # a row missing "file" (config error)
$ python3 … --table <{"entries":[{"id":"x","kind":"exact","must_match":"y"}]}>
Traceback … File "…/citation-drift-gate.py", line 158, in check_entry
    target = entry["file"]
KeyError: 'file'                                                       rc=1   # the declared "failed" code

$ # nonexistent --rev, nonexistent --root, empty entries: all silent clean
$ python3 … --rev deadbeef …        → CITATION_DRIFT_VERDICT: clean findings=0 exit=0   rc=0
$ python3 … --root /var/tmp/arc2-l4r4-CR7/nope … → clean findings=0 exit=0             rc=0
$ python3 … --table <{"entries":[]}>            → clean findings=0 exit=0              rc=0

$ # a ~/... row through the same gate (git show of an untracked path)
$ python3 … --table <{"entries":[{"id":"live","kind":"exact","file":"~/.kimi-code/config.toml","line":1,…}]}> → clean exit=0
```

Three defects, all measured: (a) **wrong-schema table = silent clean** — the
`table.get("entries", [])` default (`citation-drift-gate.py:252`) converts a
schema mismatch into "nothing to check, all good"; (b) **config errors borrow
the "failed" code** (`KeyError` → rc=1) and print no `VERDICT` line — the
R3-F1 class R3 raised against `verify-citations.py:93-99`; (c) a
`citation_file_absent` finding for a git-absent *citing* file is written at
`:164` but is **unreachable for git-resolved targets**, because
`Tree.lines` adds every failed target to `self.reported` at
`citation-drift-gate.py:121` and `check_entry` then suppresses the finding
(`:163-164`) — so `citation_file_absent` fires only for snapshot targets.
I could not construct a table that produces it for a repo path.

Notably, the gate's own negative controls are *honest*: missing
`--snapshot-dir` → exit 2, tampered snapshot → exit 2 (both re-verified via
the selftest cases), and `--selftest` with a missing `expected.json` →
`SELFTEST_FAILED … exit=1 finding=selftest_table_unreadable` — declared, not
silent. The selftest also passed 10/10 under `TMPDIR=/tmp`,
`TMPDIR=/nonexistent`, and an unset TMPDIR (tempfile falls back to
`/var/tmp`), so **selftest failure at landing time is not the realistic
risk** — the realistic landing-time failures are §2.2/§2.3.

### 2.4 E16's table, landed: schema, classes, and what it does to each checker

`e16-table.json` landed at the repo root in `1692acbe` (sha `89eddae0…`,
361/362 lines, byte-identical to `/tmp/arc2-l3r3-E16/e16-table.json` — my
`sha256sum` of both). `git show --stat 1692acbe` → the commit adds
`e16-table.json` + round-4 reports + the receipt and touches no `SKILL.md`
(`git diff 679af5d 158a966 -- SKILL.md` → empty; the commit subject "rule 11"
is inaccurate — round-4 seat E20 measured the same, `E20.md:§2.9`).

```
$ python3 /tmp/arc2-l3r3-E16/pointers.py --root <1692acbe tree> --baseline-root <repo>
OK   M1-M8, S1-S7, C1-C5, X1-X13 …
RED   X14 SCORECARD.md:270       [STALE, repair pending] '`:157` pointer (at `:177`'
ADVISORY   E1-E4 (external rows)
rows=47 BASELINE=1 EXTERNAL=4 INREPO=35 QUOTED=1 STALE=1 XREF=5
VERDICT: failed
```

E16's own checker works (its 47-row form has a `BASELINE` class whose target
is graded at `6645585` and an `EXTERNAL` advisory class — the two classes
that make it *not* red on sanctioned citations). E15's gate has neither
class. So "Base: E15's proven implementation … pointer table = … E16's
BASELINE/QUOTED/SYMBOL classes" describes a merge no measured artifact
performs; `E16.md:299-337` itself says "the gate must honor" those classes,
i.e. they are *requested* semantics, not implemented ones. Landing E15's
gate against E16's table as-is yields §2.3's silent clean; landing E16's
table's semantics requires new code in E15's gate.

### 2.5 C3's census: premise confirmed, fix is two-part (three variants measured)

Instrument extracted byte-identically from `E22.md:264-692` (fenced block) →
`/var/tmp/arc2-l4r4-CR7/c1-census-v9.py`, 429 lines, sha
`213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c` — matches
`E22.md:698`.

```
$ python3 c1-census-v9.py --quiet      # at HEAD (worktree, and on a 1692acbe materialization)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)      rc=1
  -- UNDECLARED (2) --  SCORECARD.md block 731-737 ; SCORECARD.md block 747-766
     (round-2's own records blocks; the hardcoded SCOPE table ends at 635-701, c1-census-v9.py:103)

$ # variant A: re-key only — add ("SCORECARD.md", 703, 767, "DATED", 703, r"2026-10-18")
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   G11 … ['SCORECARD.md:731']

$ # variant B: same row declared CURRENT
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   ambiguous=1

$ # variant C: re-key + RECEIPT regex accepts tools_sha256 (c1-census-v9.py:112)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

`SCORECARD.md:731` is `- Battery (REA 6.7.0, local npx cache; one registry
packument revalidation` — current-ok, no receipt word in its own block
(`RECEIPT.search` over 731-737 → False; `tools_sha256` is present at :735).
Round-4 seats E22 (`E22.md:216-252`) and S1 (`S1.md:§2.6`) reached the same
conclusion independently (re-key alone → FAIL; a second, semantic change
needed for PASS) — I ran my variants before reading their reports; the
convergence is three-source. The claim's "census PASS at the work commit"
is reachable but is **not** the single-step re-key it names; the parent must
name the second half and why it is not a relaxation-for-green.

### 2.6 C1's rule 11: measurable confirmed, collateral measured

Simulated the insert in a scratch clone (`sim1` = 1692acbe materialized;
`sim2` = sim1 + a 4-line rule inserted before the SOP heading):

```
$ command A at sim2 HEAD
{"citation_resolved_rules": 11, "coverage_score": 10.0, "depth_score": 10.0,
 "rule_blocks": 11, "knowledge_files": 79, "mapped": 79, "missing": [], "dangling": []}
$ cmp <(sed -n '81,206p' sim1/SKILL.md) <(sed -n '81,206p' sim2/SKILL.md)   # pre-existing craft bytes
CRAFT-81-206 IDENTICAL
$ diff <(git -C sim1 show HEAD:SKILL.md) <(git -C sim2 show HEAD:SKILL.md)
206a207,210   > - **Operator-mutable citations anchor by stanza key + receipt, never bare …
$ python3 …/citation-drift-gate.py --root sim1 … | grep -c CITATION_DRIFT:   → 10
$ python3 …/citation-drift-gate.py --root sim2 … | grep -c CITATION_DRIFT:   → 11
$ # the extra finding:
CITATION_DRIFT: citation_dead entry=skill-registry-row SKILL.md:336 lacks 'interactive-r1-recovery \| gate / kaidoku'
$ grep -n '^## Config custody' sim2/SKILL.md → 212   (was 208; the registry row moved :336 → :340)
```

So: rules 10→11, 11/11 resolvable, depth 10.0 — **confirmed**. "Craft
otherwise byte-identical" — **true for the existing craft bytes, false for
the file's citations**: `corpus/lessons/2026-10-15-round-1.md:37`'s
`SKILL.md:207-210` and `LOG.md:685`'s `SKILL.md:211-214` now land on the new
rule's own text (I read both lines and the shifted region), and any landed
table row pinning `SKILL.md:336` (E15's `skill-registry-row` does) goes red.
S1 measured the same class of collateral (`S1.md:19-24`, `:204`, `:434`,
`:610`) with an 8-line variant; my 4-line variant shows the effect is
structural, not a property of the exact wording. If C2's table lands before
C1's insert, **C1 turns the probe red** — a sequencing constraint the round
text does not carry.

### 2.7 C3's `lessons:82` locus, read directly

```
$ sed -n '82p' corpus/lessons/2026-10-15-round-1.md
`~/.kimi-code/config.toml:1287` still pins 6.4.0. Installed shared skill
$ sed -n '1287p' /home/vgpnk/.kimi-code/config.toml
[models."opencode-go-3/grok-4.7"]
$ wc -l < corpus/lessons/2026-10-15-round-1.md  → 188
```

Both halves of the claim's statement are false at HEAD (dead line, stale
version), the append route is the file's own precedent (`:162`'s
"Pointer refresh" section), and round-4 seat E4 has a verified draft
(`E4.md:§2.5`: block sha `e6ccdd45…`, post-append 210 lines, sha
`91df9b37…`, prefix-identical). Nothing in my seat contradicts it; noted so
the parent's C3 landing has a second, independent reading of the locus.

## 3. Text for the parent to land VERBATIM (if used)

### 3a — the C2 landing conditions (my seat's requested confirmation)

```text
CR7 (round-4 critic) — C2 landing conditions, measured at HEAD 1692acbe:

1. BASE LINEAGE IS NOT AS DECLARED. E15's gate (sha 0c5350b1…) does NOT contain
   R3's F1-F3 fixes (written against C3.md's verify-citations.py 0a3e7480…) nor
   R6's defect fixes (written against E23's c2-census.py cf5d65b6…). Measured in
   0c5350b1…: a table row missing "file" raises an uncaught KeyError with rc=1
   (the declared "failed" code for a configuration error); two entries
   (province-18-kimi-pin, scorecard-59-pin-receipted) are false-dead on
   round-3's own content-anchor repairs because their patterns pin the
   pre-repair wording (R6's anchor-fragility class). If C2 lands 0c5350b1…
   unchanged, the round ships a probe that is red on two citations round-3
   adjudicated correct and that cannot distinguish "wrong schema" from "clean"
   (table.get("entries", []) at :252).

2. PROBE vs GATE MUST MATCH THE ARTIFACT. PROTOCOL.md:363-364 defines a probe
   as "a tool that cannot fail". 0c5350b1… can fail (exit 1 findings, exit 2
   config error). Land it as a gate — then the Gate standard binds (registry
   row fields, self-test, Two evidences with a committed expected verdict, and
   the frozen run must be re-pinned at the work commit, because
   expected.json's frozen_run (failed, 10 findings @679af5d) matches no run on
   the work tree) — or neutralize the exit so it cannot fail, and register it
   as a probe. Do not register "probe" while shipping gate exits.

3. SCHEMA. E16's landed table (e16-table.json, sha 89eddae0…, key "pointers",
   kinds line|symbol + BASELINE/QUOTED/EXTERNAL semantics) is a silent no-op
   under 0c5350b1… (clean exit 0, measured). "E15 base + E16 classes" requires
   an adapter and four new entry classes; none exists today. If the round
   lands E16's table as the contract, the gate must implement it (or the
   round must declare the merge as the work, not the base).

4. SEQUENCING. C1's rule insert shifts SKILL.md:207+ (my 4-line variant: SOP
   heading :208→:212, registry row :336→:340) and flips
   0c5350b1…'s skill-registry-row red (findings 10 → 11). Land the table
   AFTER C1 with the row re-pinned to the new line, or drop that row.

5. THE C2 HONEST-STOP PATH IS OPEN AND STAYS OPEN. No C1/C3 measurable
   depends on C2: command A's 10→11/11/11 and depth 10.0 are C1's, and the
   census PASS is C3's. If the probe's selftest fails at landing time (my
   runs: 10/10 under TMPDIR=/tmp, TMPDIR=/nonexistent, and unset TMPDIR — so
   selftest failure is not the realistic risk; the realistic failures are
   items 1-4), then per AXES.md:34-36 and PROTOCOL.md:397-402 record C2 as
   "not verified (honest stop)" in the round section, do NOT enter a
   capability row (AXES.md:62: rows enter only through a round that
   demonstrates the capability running), and route the probe as named debt —
   exactly the round-3 disposition of C3 (SCORECARD.md:833). A red probe
   recorded in the round notes is a conformance defect, status-neutral; it is
   not a trade and it does not fail the round.
```

### 3b — the one-line correction for the round record's C1 row

```text
C1 (depth, owned): rule 11 landed — command A 10→11 rule blocks, 11/11
resolvable, depth 10.0 at the work commit (CR7 simulation, 4-line variant;
S1's 8-line variant agrees). Collateral, measured: the insert shifts
SKILL.md:207+ (SOP heading, registry row), so the round record must NOT say
"craft otherwise byte-identical" without the qualifier "existing craft bytes
identical; SKILL.md:207+ citations re-anchored in the same commit" — the two
live citations into that region are corpus/lessons/2026-10-15-round-1.md:37
(`SKILL.md:207-210`) and LOG.md:685 (`SKILL.md:211-214`), and any pinned row
on SKILL.md:336 flips red until re-pinned.
```

## 4. Conclusions, labeled

**OBSERVATIONS** (run or read by me this session):

- Round-4 pre-pair verified 5/5 rc=0, self-hash `231edd7d…`, shape 6/5/1.
- E15's four deliverables hash exactly to `E15.md`'s pins (`0c5350b1…`,
  `d7bf0eb3…`, `6ebada28…`, `387e1f08…`); the redaction retains 0 secret-ish
  matches.
- E15's selftest is 10/10 at exit 0; its live run at HEAD is
  `failed findings=10 exit=1`, of which two are false-deads minted by
  round-3's content-anchor repairs (`province-18-kimi-pin`,
  `scorecard-59-pin-receipted`).
- E15's gate returns `clean exit=0` for: E16's landed table (wrong schema),
  `--rev deadbeef`, a nonexistent `--root`, an empty `entries` list, and a
  `~/…` file row; it returns exit 2 for an unknown kind and exit 1
  (uncaught KeyError) for a row missing `"file"`.
- `citation_file_absent` is unreachable for git-resolved citing files
  (`citation-drift-gate.py:121` vs `:163-164`).
- `expected.json`'s `frozen_run` and `pointer-table.json`'s `exempt` are never
  read by the script (`grep -c` → 0); only `snapshots` and the selftest table
  are consumed.
- E16's landed `e16-table.json` (sha `89eddae0…`) is byte-identical to the
  round-3 scratch file; E16's own checker reports `rows=47 … VERDICT: failed`
  with `X14` the single RED.
- Census instrument extracted at sha `213fe679…` (429 lines); at HEAD
  `FAIL undeclared=2` (blocks 731-737, 747-766); re-key alone → FAIL with
  `G11 ['SCORECARD.md:731']`; re-key + `tools_sha256` accepted → PASS.
- Command A at a rule-11 simulation: `11/11`, `depth_score 10.0`,
  `rule_blocks 11`; pre-existing craft bytes `cmp`-identical; the insert
  shifts SKILL.md:207+ and flips E15's `skill-registry-row` red.
- `corpus/lessons/2026-10-15-round-1.md:82` is doubly false at HEAD
  (`:1287` = `[models."opencode-go-3/grok-4.7"]`; live pin 6.7.0); file 188
  lines; no `frozen` root exists under `.ufo`; `.ufo/gates/` does not exist
  and is not git-ignored.
- HEAD moved 158a966 → 1692acbe mid-leg (commit "rule 11" adds
  `e16-table.json` + reports + receipt; touches no `SKILL.md`).
- Repo untouched by me: `git status --porcelain` shows only
  `?? .ufo/waves/arc2-loop1-round4/*` (other seats' reports + mine);
  `git rev-parse HEAD` = `1692acb` at my close.

**INFERENCES:**

- The round-4 C2 claim, as worded, is not landable as a single artifact: its
  base lineage is false, its probe/gate category is unresolved, and its
  pointer table's classes do not exist in the implementation it names. The
  honest landing is a reduced scope with an explicit adapter step, or the
  honest stop.
- The two false-deads on round-3's repairs are the round's own thesis turned
  on itself: a detector whose activation condition is drafter wording
  (`R6.md:43-49`) fires on the repair, not the defect. Any landed table must
  pattern-match the *current* citing text, and re-derive it at the work
  commit.
- The census PASS is a two-part change; shipping the claim's single-step
  phrasing and then reporting PASS would be a measurable that does not match
  its own description.
- The C2 honest-stop is structurally safe: C1 and C3 carry the round's
  admissible measurables, and the round-3 precedent shows an honest stop is
  recorded, not punished.

**UNKNOWNS:**

- Whether the parent lands E15's gate at `.ufo/gates/` (the round's stated
  layout; the directory does not exist yet) and with which schema; whether an
  adapter is written this round or the table is reduced.
- Which of the three PASS variants the parent chooses for the census, and
  whether it is recorded as a semantic decision (it should be).
- Whether the round-4 C2 knowledge/record will claim "probe registered" while
  the artifact exits 1/2 — the one wording I would refuse.
- The post-battery closing state of the five custody paths (my receipt check
  is mid-battery; the parent's post-pair owns the close).
- Whether `1692acbe`'s root-level `e16-table.json` is intended as a
  deliverable (it is a scratch artifact by provenance) or is cruft to be
  relocated in the work commit.

## 5. Reproduction

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD; git status --porcelain
tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
sha256sum /tmp/arc2-l3r3-E15/{citation-drift-gate.py,pointer-table.json,expected.json,config-toml-landmarks}

# E15 gate: selftest, live, and the four fail-open paths
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --selftest --expected /tmp/arc2-l3r3-E15/expected.json
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev HEAD \
  --table /tmp/arc2-l3r3-E15/pointer-table.json --expected /tmp/arc2-l3r3-E15/expected.json \
  --snapshot-dir /tmp/arc2-l3r3-E15                      # failed findings=10 exit=1
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev HEAD \
  --table e16-table.json --expected /tmp/arc2-l3r3-E15/expected.json \
  --snapshot-dir /tmp/arc2-l3r3-E15                      # clean exit=0 (schema no-op)
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev deadbeef \
  --table /tmp/arc2-l3r3-E15/pointer-table.json --expected /tmp/arc2-l3r3-E15/expected.json \
  --snapshot-dir /tmp/arc2-l3r3-E15                      # clean exit=0

# census (extract from E22.md's fence, lines 264-692) — variants in /var/tmp/arc2-l4r4-CR7/
python3 /var/tmp/arc2-l4r4-CR7/c1-census-v9.py --quiet      # FAIL undeclared=2
python3 /var/tmp/arc2-l4r4-CR7/c1-census-rekey.py --quiet   # FAIL g11 ['SCORECARD.md:731']
python3 /var/tmp/arc2-l4r4-CR7/rekey-receiptfix.py --quiet  # PASS

# rule 11 simulation (sim1 = 1692acbe tree; sim2 = sim1 + 4-line insert)
python3 /var/tmp/arc2-l4r4-CR7/sim2 -c …  # see §2.6; command A recipe from SCORECARD.md:92-123
```

Scratch inventory (`/var/tmp/arc2-l4r4-CR7/`, 163M): the extracted census +
three re-key variants, `sim1`/`sim2` (rule-11 simulation repos), `head158`,
`emptyrepo`/`emptytree` (negative controls), and the small tables used in
§2.3. `/tmp/arc2-l4r4-CR7*` removed (the earlier scratch there was wiped after
the quota error; nothing of mine remains on `/tmp`). No process of mine was
left running; the PE analyze (another seat's, already OOM-killed at 19:07:45Z
per round-4 E13/SC2) was only observed.
