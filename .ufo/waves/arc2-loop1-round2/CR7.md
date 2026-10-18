# CR7 (critic) — attack on smuggled claims and verdict inflation in round 2's three claims

Seat CR7, wave arc2-loop1-round2, 2026-10-18. Read-only on every repo and home
file; the only repo write is this report. Scratch: `/tmp/arc2-l2r2-CR7-sim/` and
`/tmp/arc2-l2r2-CR7-clone/` (a `git clone` of this repo, reset afterwards). Every
command and output below was run or read by this seat this session. State at every
command unless stated otherwise: HEAD `165057e36f558c95eb02bf24de4a874d559d6950`;
`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/` only.

## 1. Verdict

**TWO OF THE THREE "improved" VERDICTS ARE NOT SUPPORTED — C1 is unprovable as
written and its designated landing text is rejected by the round's own gate; C2 is
a trade in disguise whose "repair" lands a false sentence. C3's bracket is real and
verified by me, but its capability-row condition is unsatisfied at my read time.**

1. **C1 — unprovable as written (verdict inflation).** "Stale Kimi-pin statements
   N → 0" has no frozen N or counting command, and four round-2 seats measured four
   different before-values (R6: "6 vs 11"; S1: n=4; E22: 5; C2: 6 loci in target
   files). Independently, the designated PROVINCE landing block
   (`E7.md:245-279`, named as the landing text by `E24.md:205`) is **net +18 lines**
   and breaks seven landed `PROVINCE.md:114-116` citations (three in `LOG.md`,
   four elsewhere) plus `SCORECARD.md:593`→`PROVINCE.md:48` and
   `SKILL.md:231`→`PROVINCE.md:108-113`. **C3's own gate FAILS that block** (ran by
   me). No seat connected C3's own §4.1 anchor table to E7's actual block.
2. **C2 — trade in disguise (the "repair" would make the clause false).**
   `SCORECARD.md:68`'s defect is not a pointer offset: the clause asserts content
   ("`:160` **still lists already-held** … as frontier") that was **discharged at
   `7125dd4`** — `:177` now reads "**held, not frontier**". A bare re-point (the
   wording `E19.md:209` proposes: "repaired to `:177`") yields the false sentence
   "`:177` still lists already-held … as frontier". Same for `:128`→`:138`: `:138`
   already reads "2 fixes applied at integration", the very correction the clause
   demands. The measurable is also mis-stated: the drifted-pointer class has **three**
   readings (`:160`, `:128`, `SCORECARD.md:270`'s `:157`), not one.
3. **C3 — real but conditional, not "improved" yet.** Pre-pair verified 6/5/1, 5/5
   OK, self-hash `4097ec77…`; zero drift re-confirmed at 17:12:30Z. But
   `receipts/` holds only `config-pre-pair.txt`, `git ls-files` on the wave dir → 0,
   and the post-pair exists only in seat scratch. The row's entry condition
   (zero drift **+ committed receipts**) is unmet; the SOP still says "three" paths
   (`SKILL.md:218`), contradicting the landed 6-line receipt.

## 2. Evidence — commands run THIS session with observed output

### 2.1 C2: the clause's content is discharged; a re-point makes it false

```
$ sed -n '68,70p' SCORECARD.md
- **Other stale summaries:** `corpus/README.md:160` still lists already-held
  process/managed/call-target operations as frontier; `:128` says four r13
  nits fixed although `LOG.md:395-401` corrects integration fixes to two.

$ sed -n '177p' corpus/README.md | grep -o 'held, not frontier'
held, not frontier
$ sed -n '138p' corpus/README.md | grep -o '2 fixes applied at integration'
2 fixes applied at integration
$ sed -n '68p' SCORECARD.md | grep -o 'still lists already-held'
still lists already-held
```

Observation: the clause's two content assertions are both **false at HEAD**
(`:177` says held-not-frontier; `:138` already carries the correction) and both were
discharged at `7125dd4` (`E9.md:108-109` measured the same two hunks). A re-point
therefore does not repair a claim about content — it re-asserts it against text that
contradicts it. `E19.md:209` proposes exactly that ("repaired to `:177`");
`E24.md:229-234`'s candidate block does it correctly by rewriting. Which text lands
is unresolved across seats.

```
$ grep -n ':157' SCORECARD.md | head -2
270:  `:157` pointer (at `:160` in HEAD, per seat C7) is recorded as named debt,
```
Third pointer-reading, same class (`V5.md:7` found it; `V5.md:114` counts
"**3 pointer-readings → 0**"). The claim's "drifted pointer 1 → 0" is wrong as a
before-value (`R6.md:10` independently).

### 2.2 C1: four different before-values, no command

```
$ sed -n '9p' .ufo/waves/arc2-loop1-round2/R6.md
1. **C1 has no counting command at all.** … I measured the before-value two ways and they disagree (6 vs 11 loci) …
$ sed -n '17p' .ufo/waves/arc2-loop1-round2/S1.md
   **n = 4** (paragraph-level, §2.1). Six sites reach **n = 0**.
$ sed -n '13p' .ufo/waves/arc2-loop1-round2/E22.md
**5 stale loci in CURRENT scope at HEAD** — adding `PROVINCE.md:44`,
```
Observation: "stale N → 0" cannot be adjudicated from the round's own record. This
is the round-1 R1 defect class (`SCORECARD.md:318-325` records the same caution),
repeating.

### 2.3 C1: the designated landing block breaks citations (my simulation)

Block under test: `E7.md:245-279` — designated as "PROVINCE.md:8-25 replacement" by
`E24.md:205` ("`.ufo/waves/arc2-loop1-round2/E7.md:244-280`"). E7's own preamble
(`E7.md:235-238`) says it replaces `:8-24`, keeps `:25`.

```
$ mkdir -p /tmp/arc2-l2r2-CR7-clone && git clone -q . /tmp/arc2-l2r2-CR7-clone
$ cd /tmp/arc2-l2r2-CR7-clone && git checkout -q 165057e36f558c95eb02bf24de4a874d559d6950
$ python3 -c "… replace PROVINCE.md:8-24 with E7.md lines 245-279 …"
wrote PROVINCE.md: 180 lines (was 162)
$ git diff --numstat HEAD -- PROVINCE.md
31	13	PROVINCE.md
$ grep -n 'Quality/safety verdicts on findings' PROVINCE.md
132:- **Quality/safety verdicts on findings** — the lane answers "what does this   # was :114
$ grep -n 'Provider-key inventory remains historical' PROVINCE.md
44:Provider-key inventory remains historical, … (`HEAD:PROVINCE.md:19-26`) …      # was :26
$ sed -n '48p' PROVINCE.md | cut -c1-70
provider candidates); a catalog-listed tool is *available*, not *held*          # was "| Native ELF via Ghidra |"
$ sed -n '114,116p' PROVINCE.md | cut -c1-50
                                                                               # (blank)
Ground the lane refuses or defers — reported to the orchestrator, neve
absorbed.
```

Observation: the block is 35 lines replacing 17 → **net +18**, not line-neutral.
Blast radius, all measured above and all outside the round's declared edit
envelope: `PROVINCE.md:114-116` (six landed citations: `LOG.md:872,:958,:985`;
`SCORECARD.md:656`; `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`;
`corpus/knowledge/2026-10-13-r3-jq-provenance.md:141`;
`corpus/lessons/2026-10-15-round-1.md:175`), `PROVINCE.md:48`
(`SCORECARD.md:593`), `PROVINCE.md:108-113` (`SKILL.md:231`), and `PROVINCE.md:26`'s
self-citation. `C3.md:112-116` tabulates every one of these anchors — but no seat
joined that table to E7's block. `E24.md:130` warns only about `:26`'s self-citation
(and cites S1's measurement `:26 → :33`, which is a *different* landing text from
E7's `:26 → :44`).

### 2.4 C1: the round's own gate rejects the block

Gate extracted verbatim from `C3.md:299-487` (`sed -n '299,487p' … > /tmp/arc2-l2r2-CR7-gate.py`):

```
$ python3 /tmp/arc2-l2r2-CR7-gate.py 165057e36f558c95eb02bf24de4a874d559d6950 --selftest
OK   PROVINCE.md pre_blob 8a1cec88b50f0e9aa928b0c042354a017217ad47
OK   SKILL.md pre_blob 4518e3fc2b3f996ca4de226dbf84882af97b1957
OK   SCORECARD.md pre_blob 187988469d47ea18b26b8aea54533e7752836b83
OK   corpus/README.md pre_blob 5efb202a7b0aecdf182695fb8849050044e65ac9
OK   LOG.md pre_blob 5ee14144235835547eeb5b41e49f7719ed6daac8
selftest PASS variant A

$ git add PROVINCE.md && python3 /tmp/arc2-l2r2-CR7-gate.py 165057e36f558c95eb02bf24de4a874d559d6950
FAIL PROVINCE.md: +31 -13 hunks=4 @@ -8,6 +8,15 @@ -15,1 +24,1 @@ -18,6 +27,13 @@ -24,0 +41,2
      insert/append hunk not allowed @@ -24,0 +41,2
OK   SKILL.md: untouched
```

Observation: the gate (selftest PASS on the real base) rejects the designated C1
landing text. The gate's `allow=[[8, 13], [15, 26], [44, 44]]`, `inserts=[]`,
`del_budget=16` (`C3.md:342`) assume a **line-neutral** repair; E7's block is +18.
Also note the block's own `:25` Ghidra/JDK sentence is **not** in the block
(`E7.md:236-238` says "keep `:25` unchanged"), so a parent applying
`E24.md:205`'s "`:8-25` replacement" reading must delete it — my variant-2 simulation
(with `:25` retained) still measured `:114 → :132`, i.e. the harm is not avoidable by
reading the range differently.

Cleanup (verified): `git reset -q HEAD -- PROVINCE.md; git checkout -q -- PROVINCE.md`
→ 162 lines; the lane repo was never written to.

### 2.5 C3: bracket verified; entry condition unmet; SOP contradiction live

```
$ cat .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt   # 501 B, 2026-10-18T16:57:35Z
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile
$ wc -l < receipt → 6 ; grep -cE '^[0-9a-f]{64}  /' → 5 ; timestamp-regex → 1
$ sha256sum receipt → 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245
$ tail -n +2 receipt | sha256sum -c -    # at 17:12:30Z, live files
…/mcp_config.json: OK   …/mcp.json: OK   …/config.toml: OK   …/.bashrc: OK   …/.profile: OK   rc=0
$ git ls-files .ufo/waves/arc2-loop1-round2/ | wc -l
0
$ ls .ufo/waves/arc2-loop1-round2/receipts/
config-pre-pair.txt
$ ps -eo pid,args --no-headers | grep -E 'rea\.mjs|rea-agents' | grep -v grep    # 17:20:07Z
(no output)
$ sed -n '218p;224,225p' SKILL.md
  unpaired round.** Hash exactly the three drift-sensitive client configs,
  absent. Then gate the receipt's shape: `wc -l` = 4,
  `grep -cE '^[0-9a-f]{64}  /'` = 3, one timestamp line
```

Observations: the pre-pair is real and self-consistent (I reproduced shape, self-hash
and a 5/5 `-c` at 17:12:30Z); zero REA residue at 17:20:07Z. But the receipts are
untracked, the post-pair is absent from the repo, and the binding SOP still mandates
the 3-path/4-line form that the landed 6-line receipt violates — a live normative
contradiction that only E21's amendment (`E21.md:180-245`) closes. `R7.md:7`
independently holds the row "NOT-YET-QUALIFYING at this snapshot".

Soft point on the claim's own wording: "bracketing a 2-leg battery on the unprobed
6.7.0 cache" — the pair brackets the five **config/shell files**, not the cache. The
6.7.0 cache **directory** mtime moved during the round (`2026-10-18 14:09:58 -0300`;
`E2.md:112` attributes it to `npm exec` dir bumps and reports no file changes). No
seat hashed the cache package into custody, so the pair cannot falsify a cache
mutation; E14's own threat note (`E14.md:180`) concedes this for the package.

### 2.6 C3/C1 side-note: the "no network" wording is inaccurate

```
$ grep -hE 'http fetch GET|http cache' /home/vgpnk/.npm/_logs/2026-10-18T17_09_58_*.log
14 http fetch GET 200 https://registry.npmjs.org/rea-agents 5ms (cache stale)   # rea-agents@6.7.0 --version
14 http fetch GET 200 https://registry.npmjs.org/rea-agents 5ms (cache stale)   # rea-agents@6.5.0 --version
$ sed -n '10p' .ufo/waves/arc2-loop1-round2/E14.md
- `node scripts/rea.mjs --version` → `6.7.0` … **No network fetch**: the package was served from the local npx cache …
```

Observation: plain `npx` performs a registry revalidation (`GET 200`, "cache stale")
even when the payload is served from cache. `E13.md:7` and `SC1.md:7` recorded this
nuance correctly; `E14.md:10` and `:178` ("no network fetches") do not. Not a
falsification of the census — but the LOG entry and round report must not inherit
"no network fetch" verbatim.

## 3. Text the parent should land VERBATIM (only if it chooses to record this attack)

```text
CR7 attack record (arc2-loop1-round2, read-only seat):

C1 — NOT PROVABLE AS WRITTEN. "Stale Kimi-pin statements N → 0" has no frozen N or
counting command; four seats measured four before-values (R6 "6 vs 11"; S1 n=4;
E22 5; C2 6). Independently, the designated PROVINCE landing block (E7.md:245-279,
per E24.md:205) is net +18 lines, not line-neutral: measured in a scratch clone it
moves the safety-refusal bullet PROVINCE.md:114 → :132 and the provider-key
self-reference :26 → :44, leaving PROVINCE.md:114-116 blank/refusal-text and
PROVINCE.md:48 wrong. That breaks six landed citations of PROVINCE.md:114-116
(LOG.md:872,:958,:985; SCORECARD.md:656; corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244;
corpus/knowledge/2026-10-13-r3-jq-provenance.md:141; corpus/lessons/2026-10-15-round-1.md:175),
plus SCORECARD.md:593 → PROVINCE.md:48 and SKILL.md:231 → PROVINCE.md:108-113.
C3's own gate (C3.md:299-487) FAILS the block: "FAIL PROVINCE.md: +31 -13 hunks=4
… insert/append hunk not allowed @@ -24,0 +41,2". Either land a genuinely
line-neutral PROVINCE repair inside C3's envelope, or re-point every affected
citation in the same commit and record the blast radius; do not land E7's block
under the current envelope.

C2 — TRADE IN DISGUISE. SCORECARD.md:68-69 asserts content, not just pointers:
":160 still lists already-held … as frontier" and ":128 says four r13 nits fixed
although LOG.md:395-401 corrects integration fixes to two". Both content claims are
already discharged at 7125dd4 — corpus/README.md:177 reads "held, not frontier" and
:138 reads "2 fixes applied at integration". A bare re-point to :177/:138 (the
wording E19.md:209 proposes) lands the false sentence "`:177` still lists
already-held … as frontier". The bullet must be rewritten as a record of a
discharged debt (E24.md:229-234's form), not re-pointed. Also, the drifted-pointer
class has three readings, not one: :68's :160, :69's :128, and SCORECARD.md:270's
:157 — "drifted pointer 1 → 0" is false as a before-value.

C3 — CONDITIONAL. Pre-pair verified this session (6/5/1 shape, 5/5 sha256sum -c OK,
self-hash 4097ec77…, 501 B, 2026-10-18T16:57:35Z; live re-check 5/5 OK at
17:12:30Z; no REA residue at 17:20:07Z). But receipts/ holds only
config-pre-pair.txt and git ls-files on the wave dir returns 0 — the row's entry
condition (zero drift + committed receipts) is unmet until the parent copies the
post-pair and both leg artifacts and commits them. The SOP still reads "three
drift-sensitive client configs" with a 4/3/1 shape gate (SKILL.md:218,:224-225),
contradicting the landed 6-line receipt; the amendment must land in the same commit
or the round leaves a normative contradiction. Note the pair brackets the five
config/shell files, not the 6.7.0 cache (whose directory mtime moved during the
round, 14:09:58 -0300) — no cache-mutation claim is supported by it.

Wording: E14.md:10/:178's "No network fetch" is inaccurate — npm logs show
"http fetch GET 200 https://registry.npmjs.org/rea-agents 5ms (cache stale)" on
both --version runs. The payload was cache-served; the metadata request was not.
Do not inherit "no network fetch" into the LOG entry or report.
```

## 4. Conclusions by label

**Observations** (run/read this session): §2.1 the two discharged content claims and
their contradiction with a bare re-point; §2.2 the four before-values; §2.3 the +18
line block, its four measured anchor breaks, and the reset clone; §2.4 the extracted
gate's selftest PASS and its FAIL on E7's block; §2.5 the receipt's shape/self-hash/5-5
`-c`, `git ls-files` = 0, the SOP's 3-path text, and the cache dir mtime; §2.6 the
npm `GET 200` lines.

**Inferences**: (1) C1's landing as currently designated **harms** the same class of
citation it claims to repair — this is a cross-claim trade, not an improvement, and
under `AXES.md:29-33` ("no axis is harmed — a trade anywhere is not an improvement")
it must be re-worked or the blast radius explicitly re-pointed and recorded.
(2) C2's "improved" verdict is unsupported: the clause is a content claim whose
content is discharged; re-pointing converts it into a false statement while booking
a "1 → 0" improvement. (3) C3's operability move is genuine but its row entry is
conditional and unmet at my read time; recording it as "improved" before the
post-pair lands would be pre-claiming (`AXES.md:62-64`). (4) The three-in-a-row
"improved" pattern is inflated 2 of 3.

**Unknowns**: (a) which SCORECARD:68 text the parent lands — E19's re-point phrasing
vs E24's rewrite (if E24's, C2's defect reduces to the "1 → 0" mis-count only);
(b) whether the parent applies E7's PROVINCE block verbatim (gate-FAIL) or a
line-neutral variant; (c) whether the post-pair lands in-repo before the records
commit; (d) whether `SCORECARD.md:270` is inside the frozen 2026-10-15 scope
(`LOG.md:884` names only `:79`); (e) whether any cache-mutation custody is intended
(none exists today).

## 5. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
sed -n '68,70p;270p' SCORECARD.md; sed -n '138p;177p' corpus/README.md
sed -n '9p' .ufo/waves/arc2-loop1-round2/R6.md; sed -n '17p' …/S1.md; sed -n '13p' …/E22.md
# C1 blast-radius simulation (scratch clone only):
rm -rf /tmp/arc2-l2r2-CR7-clone && git clone -q . /tmp/arc2-l2r2-CR7-clone
cd /tmp/arc2-l2r2-CR7-clone && git checkout -q 165057e36f558c95eb02bf24de4a874d559d6950
python3 -c "…replace PROVINCE.md:8-24 with E7.md lines 245-279…"
git diff --numstat HEAD -- PROVINCE.md        # 31 13
grep -n 'Quality/safety verdicts on findings' PROVINCE.md   # 132 (was 114)
# C3's gate against the same block:
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && sed -n '299,487p' .ufo/waves/arc2-loop1-round2/C3.md > /tmp/arc2-l2r2-CR7-gate.py
cd /tmp/arc2-l2r2-CR7-clone && git add PROVINCE.md && python3 /tmp/arc2-l2r2-CR7-gate.py 165057e36f558c95eb02bf24de4a874d559d6950
# C3 bracket re-verification:
tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
git ls-files .ufo/waves/arc2-loop1-round2/ | wc -l     # 0
grep -hE 'http fetch GET' /home/vgpnk/.npm/_logs/2026-10-18T17_09_58_*.log
```
