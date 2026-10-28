# R46W1RevengerPlan — is round 46 attacking the right target?

Seat: revenger (bounded data-walk; the wave validator has no `planner` role).
Lane: `kaidoku-shokunin`. Freeze under review: `31820472784284727546808acc31b3ea1e73919b`.
Landed rev examined: `0425224756791b414454df28a9abf93dcdf154ce` (the rev the round's own green
receipts name) and `3182047` (the bytes the prompt calls frozen).
Read-only on the lane tree; every receipt below is under
`.ufo/waves/round-46/w1/R46W1RevengerPlan/receipts/`.

---

## Verdict

**The diagnosis is right; the target is half-right; the measure is not yet a measure.**

1. Round 45 measured *shape* and called it a measure. Round 46 measures shape more tightly and
   attaches 16 mutants, so it closes most of the 16 named defects. That is real progress (a
   44-line garbage-row artefact now fails; a six-fenced-row registry now fails).
2. But the family survives: I built a 13-row artefact whose every prose cell is the letter `x`,
   keeping only a routed id, one vocabulary token and a legal exit per row. It scores
   `met_target: true` end-to-end — `battery 9/9/0/1`, exit 0
   (`receipts/vacuous-rows-forgery.json`). That is R45-CL4's named class and a direct descendant
   of the round-45 "44-line artefact"; round 46 does not close it and no mutant covers it.
3. The pair cannot be scored at the freeze the prompt names. At `FREEZE=3182047`, `REV=0425224`,
   **both counters exit 2 `frozen_path_changed`** (`receipts/c1-at-stated-freeze.json`,
   `receipts/c2-at-stated-freeze.json`). The only green receipts in the tree are at
   `freeze == rev` (`c1-freeze-eq-rev.json`, `c2-freeze-eq-rev.json`), where the freeze arm is
   tautologically empty.

So: round 46 is worth landing *as a regression set over round 45's holes*, but the claim sentence
"a check that scores its own forgeries red" is still a proxy — it scores the forgeries its author
wrote, not the cheapest forgery that satisfies the artefact's shape.

---

## 0. What round 45 actually measured (reverse-engineered from committed bytes)

`tools/round-45/c1-counter.py` computes nine values; five of them are shape:

| clause | computed value | what it can prove |
|---|---|---|
| 1 | `rule_blocks == 22` via `re.split(r"(?m)^- \*\*")` | that 22 top-level bullets exist — not that 22 rules exist |
| 2 | `block22_present == 1` (marker in block, counted per block) | that some block contains a string |
| 3 | `rows >= 8`, header cells by substring, exit ∈ {0,1,2} | that a table of the right *shape* exists |
| 4 | refs by one regex over three trees, `path:line` resolves | that text shaped like a citation resolves |
| 5 | cites `S140` + interpreter path, interpreter present | that two substrings exist |
| 6 | interpreter at rev prints `PREFLIGHT_SELFTEST: cases=11 failures=0` | that *some* script prints that banner |

`c2-counter.py` is three values: `scope_size == 6` from a frozen list, first-cell `re.search` for
each scope path, and `\b0\b`/`\b1\b`/`\b2\b` anywhere in cell 2.

So round 45's claim — "a freeze-integrity decision table **whose arms are proven red**" — was
measured only at the level of: *a table of the right shape sits in SKILL.md, and a script at the
rev prints a banner*. The arms were never executed against the artefact. The round-45 report's
`met (instrument non-discriminating)` label was therefore honest about the result, and R45-CL13 /
R45-CL14 are precise: the predicate is a structural proxy (lesson `corpus/lessons/round-45.md:142`
and `:160`).

One consequence worth stating because it recurs in round 46: **a sha256 is the only clause in
round 45 that binds text to bytes, and it is the clause round 45 did not have.** Round 46 adds it
(clause 6) — but only for `attest.py`, not for `gate.py` or `registry.py`, which hold most of the
arms (F10 below).

---

## 1. (a) The sixteen named defects: what round 46 actually closes

Legend — **closed**: a v2 clause *and* a red case (battery mutant or selftest case) fail the
artefact; **closed by check**: a v2 clause computes it but no mutant isolates it; **partial**:
the clause catches the literal shape but not the class; **open**: nothing in the landed bytes
fails it.

| defect | round-46 closure | status | residual / evidence |
|---|---|---|---|
| 13a no sha256 pin on the interpreter (a 4-line stub passes) | C1 cl.6: block's `sha256:` must equal sha256 of `attest.py` at `--rev`; mutant `stub-pin` | **closed** | pin binds `attest.py` only (F10) |
| 13b bare / off-topic / self-citation resolves and counts | C1 cl.5: line selector required, path inside the allow-set, `corpus/lessons/round-45.md` mandatory; mutants `lineless-refs`, `self-refs` | **partial** | off-topic *inside* the allow-set still counts (`plans/round-1-claims.md:1` passes); a citation outside the regex prefix (`SKILL.md:9999`, `LOG.md:9999`) is invisible — `HARD_REF` requires `corpus|plans|tools` (F9); `self-refs` is red only because the mandatory round-45 citation is lost, not because self-reference is forbidden (F8) |
| 13c header cells matched by substring | C1 cl.2 `header == ["trigger","v1 hole","v2 arm","exit"]`; mutant `header-substring` | **closed** | — |
| 13d marker counted once per block, two markers pass | C1 cl.1 `marker_occurrences == 1`; mutant `two-markers`; selftest `red-two-markers` | **closed** | — |
| 13e `rule_blocks` inflated by a bullet inside a body (false negative too) | v2 has **no** block-count clause; the block is identified by marker + `23. ` title + "is last" | **closed as a pass condition, root cause open** | `craft_blocks` still splits on `^- \*\*`; a legal top-level bullet inside block 23 now yields rows 0 → a *false negative* for a valid artefact |
| 13f malformed heading → IndexError, exit 1, empty stdout | `Malformed` → exit 2; selftest `red-malformed-heading-is-exit-2` | **closed in code, unverifiable as documented** | the whole selftest is unreachable with the published command (F5): `attest.py --selftest` exits 2 with empty stdout and a usage error |
| 14a rows in a fence / HTML comment / under any heading register | C2 cl.1 marker-bound section, fence- and comment-aware; mutants `fenced`, `html-comment`, `off-section`; selftest cases for each | **closed** | — |
| 14b `re.search` on cell 0 lets "see \`path\` (wrapper)" register | C2 cl.3 exact backticked cell equality; mutant `substring-cell` | **closed** | a duplicate row inside the section still first-wins (`by_path.setdefault`), so an honest thin row can be shadowed by an earlier good duplicate |
| 14c first-wins dedupe: a fenced good row shadows a thin honest row | mutant `first-wins-shadow` (fenced good row above the thin row) | **closed for the fenced case** | in-section duplicate ordering is not covered |
| 14d no header validation; any cell containing 0,1,2 passes | cl.2 exact header; cl.4 `EXITMAP = \b([012])\s*[=:]`; mutants `no-header`, `prose-exit`; selftest `red-prose-exit` | **closed against prose, header schema is wrong** | the "house schema" the clause enforces is 7 cells without `entry command`; `PROTOCOL.md:402-403` names eight row fields *including* `entry command` (F7) |
| 14e a scope path that exists at no revision registers | C2 cl.5 `absent_at_rev`; selftest `red-absent-at-rev` | **closed by check** | no mutant isolates it (the seven mutants all mutate shape, none mutates presence) |
| 14f freeze arm prints met for a merge-introduced touch | `gate.history_touched` uses `-m --diff-merges=first-parent --name-status -z` | **closed, verified** | probe: a merge whose own resolution adds `tools/round-46/z.py` → `touched` includes it, exit 2 (`receipts/merge-resolution.json`) |

**Tally over the sixteen:** 10 closed, 3 closed-against-the-literal-shape-with-a-named-residual,
2 partial (13b, 13e), 1 closed in code but not evidenceable (13f). None of the residuals is
covered by the 9 C1 mutants, because every mutant is a *shape* mutation and every residual is a
*semantic* one.

---

## 2. (b) The remaining routed items R45-CL1..CL24

Close modes: **by construction** = the mechanism that produced the defect is gone; **by check** =
a v2 clause computes it; **by mutant** = a named forgery class fails it; **partial**; **not at all**.

| id | close mode | status | evidence / residual |
|---|---|---|---|
| CL1 preflight is a lane-side gate; needs placement in the fleet sweep | — | **not closed** | `grep -rln 'round-46' scripts/hyaku` → nothing; the lane cannot write there (operator request) |
| CL2 registry row names a tool absent at every revision | check (C2 cl.5) + selftest case | **closed** | `absent_at_rev` computed from `gate.show` |
| CL3 widen the scope to rounds 41–43 | construction (generated census) | **closed** | `census.py --rev 0425224` regenerates `census.json` byte-equal; 38 paths; `named_but_absent []` (`receipts/census-regen.json` vs committed) |
| CL4 structurally valid, semantically empty rows pass | — | **not closed** | `receipts/vacuous-rows-forgery.json`: 13 rows of `\| R45-CLn \| x \| commit \| <exit> \|` → `met_target true`, battery 9/9/0/1 |
| CL5 r44 counters exit 2 on the eight sweep-committed fixtures | — | **not addressed** | record, correctly not rewritten |
| CL6 merge-blind log arm | construction + probe | **closed** | `-m --diff-merges=first-parent`; probe exit 2 on the resolution edit |
| CL7 c1 selftest holes (no 23-block fixture, no two-marker case) | construction + mutant | **partial** | the block-count clause is gone, `two-markers` is red; but the new selftest cannot be run as documented (F5) |
| CL8 c2 selftest holes (suffix path, cell-contains-path) | construction + mutant | **closed** | exact equality kills the suffix; `substring-cell` is red |
| CL9 A1 citation regex invisible paths | — | **partial** | `HARD_REF` now sees `corpus/**`, `plans/**`, `tools/**` and rejects outside-allowlist paths; bare-root names (`SKILL.md:9999`, `LOG.md:9999`) match nothing and are still silently ignored (the docstring's "Every path-like citation is seen" is false) |
| CL9 A2 `craft_blocks` splits on `^- \*\*` | — | **open** | unchanged; see 13e |
| CL9 A3 rows under any heading | check (C2 cl.1) | **closed** | marker-bound section |
| CL9 A4 `re.search` cell 0 | check (C2 cl.3) | **closed** | exact equality |
| CL9 A5 `scope_size` without de-duplication | construction | **closed** | `load_scope` does `dict.fromkeys`; and r46 has no `scope_size` clause |
| CL9 A6 `\b0\b`/`\b1\b`/`\b2\b` anywhere in the exit cell | check (C2 cl.4) | **closed** | `EXITMAP` requires `0=`/`1=`/`2=` |
| CL10 published gate invocation missed the claims file; gate exit 1 where counters exit 2; blob oid could name a subtree | construction | **closed** | `frozen_set()` derives both paths from the claims file; `gate.py` is a library with no CLI exit to disagree; `blob_changed` handles dir entries explicitly |
| CL11 preflight docstring says `-z`, code is plain | — | **not closed** | the round-45 bytes are untouched; block 22 already states the plain form |
| CL12 a github.com HTML sha256 is not a page identity | rule, not an instrument | **honoured** | S142 cites a located quote + a page sha256; no HTML digest is claimed as identity |
| CL13 a–f | see §1 | **4 closed, 1 partial, 1 closed-as-pass-condition** | — |
| CL14 a–f | see §1 | **5 closed, 1 wrong-schema** | — |
| CL15 dirty scope replaced instead of unioned; arms not isolating | — | **open** | `gate.dirty(pathspecs)` passes the caller's list through verbatim: a dirty frozen file with `["other.txt"]` reads `[]` (`receipts/dirty-union.json`). No counter calls `dirty`; neither selftest has a dirty case. Block 23's CL15 row claims the union and a red case that names it — both false |
| CL16 registry row misdescribed `c1-run.sh` | — | **not addressed** | record |
| CL17 scope wording over-attributes "instrument" | partial | **partial** | the new census sentence is honest ("every tools/round-4[1-6]/… named by …"); the frozen r45 sentence stays |
| CL18 pathspec boundary / freeze-path not in the log scope | construction | **closed (verdict), label wrong** | one derived set feeds both arms → the verdict is right; but `restored` mislabels every touched file under a directory freeze (F2) |
| CL19 squash-folded tamper+restore | stated limit | **open, and contradicted by the artefact** | claims file `:185` says "no table row claims otherwise"; block 23 row 9 *does* claim it (exit 2, blob arm covers it). Measured: exit 0 (`receipts/squash-fold.json`) |
| CL20 (a) scratch falls back to `/tmp` | check | **closed** | `gate.scratch` returns could-not-evaluate for any root under `/tmp`, `/var/tmp` |
| CL20 (b) registry 7 columns vs the protocol's 8 (`entry command` absent) | — | **open** | `registry.HOUSE` is 7 and the claim calls it "the house schema"; `PROTOCOL.md:402-403` includes `entry command` (F7) |
| CL21 record corrections | fixed in r45 | **n/a** | — |
| CL22 `--json-out` can overwrite a graded surface | check | **closed** | `out_path` refuses graded surfaces and paths outside the lane root; caveat: it resolves **relative** paths against the process cwd, so `--json-out .ufo/…/out.json` run from the lane root is refused as "outside the lane root" — `<OUT>` must be absolute (F11) |
| CL23 newline/tab path recorded C-quoted | construction | **closed** | `--name-status -z` + NUL split, `surrogateescape` |
| CL24 (a) record; (b) block 22 empty-range wording; (c) S140/S141 anchors lack a revision token; (d) r44 row command untested | — | **partial** | (a) fixed in r45; (b) unchanged; (c) S142 has a fetch stamp and a page sha256 but **no revision token** either (`corpus/SOURCES.md:148`) — same class, reopened; (d) unchanged |

**Counts:** 11 closed, 1 closed-with-a-wrong-label, 6 partial, 6 not closed/not addressed, plus
the CL13/CL14 ranges above.

---

## 3. (c) Is "the counter must score its own forgeries red" the cheapest honest discriminator?

**No — it is neither the cheapest nor, on its own, a discriminator.** Three measured reasons.

**(i) It is a regression set, not a discriminator.** Every one of the nine C1 mutants is killed by
a *shape* clause (rows/header/marker/pin/ids/vocabulary). The cheapest artefact that satisfies
those clauses scores green with the full battery still 9/9/0/1:
`receipts/vacuous-rows-forgery.json` — 13 rows, `| R45-CLn | x | commit | <exit> |`, `failing []`,
`met_target true`. The battery's fixed point is the author's imagination: it can only prove that
the defects someone named are caught.

**(ii) The v1 control is not the round-45 clause set, so half the battery proves nothing about
round 45.** `run_battery` scores the mutants with `spec_name="r46", profile="v1"` — the *r46 spec
under loose semantics*, which still requires `S142`, the pinned interpreter path and `refs >= 6`.
`battery.v1_green == 9` therefore says "a looser variant of v2 accepts these nine shapes", not
"the round-45 counter accepts them". The claim's sentence "This is the round-45 clause set's hole,
measured" is an overstatement; the actual round-45 port is the separate `--spec r45 --profile v1`
fidelity receipt, which clause 7 does not require. *(Inference from the code path
`run_battery` → `score(..., spec_name, "v1", ...)`; the frozen audit trail shows the v1 port
needed three post-freeze commits — `50862e4`, `65678df0`, `0425224` — to stop being stricter than
round 45, and `c2-at-781e19ae` failed `battery v1_green 0 != 7` before the last one.)*

**(iii) The battery costs more than the artefact it defends.** `attest.py` 630 + `registry.py` 534
+ `gate.py` 225 + `census.py` 79 ≈ 1,470 lines, of which the mutation harness and the v1 profile
are the majority, to defend a 13-row table.

### Ranked alternatives

| option | size | what it closes | what it costs |
|---|---|---|---|
| **A. Executable table** — each row *is* a test case: the row's trigger names a fixture, the counter materialises it, runs the named arm and compares the observed exit to the row's exit cell; rows that are not executable are marked `prose` and do not count toward the row floor | ~150–250 lines + one small fixture per executable row (the fixtures are already expressible through `gate`'s API) | CL4 and the vacuous-rows family **by construction** (a vacuous row cannot reproduce an exit); no mutant harness, no v1 profile; the artefact is the battery, so it cannot drift | every row must be runnable; the prose residue must be split out honestly (a "23." block with 13 executable rows and a short prose note) |
| **B. Add one `vacuous-rows` mutant now** — rewrite each row to `id + one token + original exit` and require v2 red on it | ~10 lines in `MUTATIONS` | names the F6 class; keeps round 46's numbers (battery becomes 10) | still only the named class; a different vacuous shape survives |
| **C. Drop the artefact, grade the instrument's own case set** — the claim surface becomes "the gate reproduces N named behavioural cases", block 23 a one-paragraph pointer, sha-pinned | smallest of all (delete `craft_blocks`/`table`/mutants ≈ −400 lines) | discrimination is definitional: the artefact *is* a passing run | loses the craft prose the depth axis is supposed to carry; the next round's measure inherits the same fixed point one level up |
| **D. Freeze the artefact's sha** | ~5 lines | nothing a forgery could not copy | tautological; makes SKILL.md immutable per round |

**Recommendation.** Land round 46 as a regression set over the sixteen defects (that is genuine and
verified), but do **not** fund another round of mutants. Take **A** in round 47 and **B** in this
round's residue list: A is the smaller move that actually makes the measure a measure, and it
retires `battery.v1_green` along with the 16 fixture repos.

---

## 4. Divergences found in the landed pair (all with commands)

**F1 — the stated freeze makes both counters exit 2 at the landed rev; every green receipt is at
`freeze == rev`.** `git log --format=%H -1 -- plans/round-46-claims.md` → `3182047…` (still; the
claims file was written once). `tools/round-46/` was then rewritten three times
(`50862e4`, `65678df0`, `0425224`), and `50862e4`'s message *declares* a re-freeze
("the first freeze commit did not carry the final bytes"). The frozen claims file defines the
freeze as "the commit that **first contains** this file and `tools/round-46/`" — a later commit
message cannot move it. Measured:

```
python3 -I -B tools/round-46/attest.py   --root . --freeze 3182047 --rev 0425224 --no-battery   → exit 2 frozen_path_changed
python3 -I -B tools/round-46/registry.py --root . --freeze 3182047 --rev 0425224 --no-battery   → exit 2 frozen_path_changed
python3 -I -B tools/round-46/attest.py   --root . --freeze 0425224 --rev 0425224                → exit 0, battery 9/9/0/1/0
python3 -I -B tools/round-46/registry.py --root . --freeze 0425224 --rev 0425224                → exit 0, 38/38, battery 7/7/0/1
```

`frozen_path_changed` names `tools/round-46/attest.py`, `gate.py`, `registry.py` and the directory.
This is the freeze-integrity class the round exists to close, re-entering through the freeze
*definition*: a freeze you may re-declare when the bytes do not satisfy is not a freeze. The L1
must either (a) score against `3182047` and accept exit 2 as the honest verdict for the landed rev,
or (b) record the re-freeze as an amendment to the claims file — which the frozen bytes forbid.

**F2 — `restored` mislabels every touched file under a directory freeze.** `blob_changed` returns
the *directory* (`tools/round-46/`), and `restored = [p for p in touched if p.rstrip("/") not in
changed]` compares file paths with a directory path, so no file ever matches and *all* touched
files are called restored. Live receipt (`c1-at-stated-freeze.json`): `restored` names all three
tools, one of which is a genuine change. Fixture receipt
(`receipts/restored-granularity.json`): `x.py` (really restored) and `y.py` (really changed) are
both `restored`. The verdict is still exit 2 (from `touched`), so the *verdict* is right and the
*label* is wrong — but block 23's CL18 row asserts "one frozen set … feeds both arms, so the sets
cannot differ"; they differ in granularity. Fix is one line (compare per-file blobs when the
entry is a directory), not a redesign.

**F3 — block 23's CL19 row contradicts the claim's own stated limit.** Claims `:185`: "a
tamper+restore committed and folded away with `git merge --squash` leaves nothing … no table row
claims otherwise." Block 23 row 9 (`SKILL.md:624`) claims exit `2` and "the blob arm still compares
the two revisions". Measured on a squash-folded tamper+restore: `gate.freeze_state` → **exit 0**,
`touched []`, `blob_changed []` (`receipts/squash-fold.json`). The row must be rewritten to state
the limit (exit 0, no arm can see it) before the L1 pastes block 23.

**F4 — block 23's CL15 row is false against the bytes.** Row 7 (`SKILL.md:622`) claims "the dirty scope is the
union of the pathspecs, and each arm has a red case that names it". `gate.dirty()` unions nothing
(it forwards the caller's list); neither counter calls it; neither selftest contains a dirty case
(attest: 16 cases, none named dirty; registry: 12, none). `receipts/dirty-union.json`: a dirty
frozen file with `["other.txt"]` → `[]`.

**F5 — `--selftest` is unreachable as documented, and the claimed case counts are stale.**
`--root/--freeze/--rev` are `required=True`, so `attest.py --selftest` exits **2 with empty stdout
and a usage error** (`receipts/selftest-attest-documented.txt`, 0 bytes; same for registry). With
dummy args the selftests run: `cases=16 failures=0` and `cases=12 failures=0`
(`selftest-attest-reachable.txt`, `selftest-registry-reachable.txt`). The claims' Satisfiability
preflight (`:192–194`) says `cases=15` and `cases=11` — both wrong at the scored rev, and the
command that would prove them cannot run. Round 45's counters had optional args and checked
`--selftest` first; round 46 regressed this.

**F6 — a vacuous artefact scores `met_target: true` end-to-end** (`vacuous-rows-forgery.json`,
battery 9/9/0/1/0, exit 0). See §3(i).

**F7 — C2 enforces a 7-cell "house schema" that is not the protocol's.** `PROTOCOL.md:402-403`:
"Row fields: name, `gate|probe`, **entry command**, verdict map (code → class), self-test command
and spelling, pinned-value path, write scope, owner" — eight fields. `registry.HOUSE` is seven and
has no `entry command`. R45-CL20(b) named exactly this; round 46 codified it as the target.

**F8 — the `self-refs` mutant does not isolate self-reference.** `m_self_refs` rewrites the Refs
line to `plans/round-46-claims.md:1..6`; v2 fails it because `must_cite_refs` loses
`corpus/lessons/round-45.md`, not because citing the claims file is wrong. A self-citation added
*beside* the required refs passes.

**F9 — `HARD_REF` still cannot see bare-root citations.** The regex requires a
`corpus|plans|tools` prefix, so `SKILL.md:99999` and `LOG.md:9999` are neither counted nor
rejected — the A2 defect is narrowed, not closed (the comment above the regex says otherwise).

**F10 — the pin protects one of four files.** Clause 6 pins `attest.py`. `gate.py` (merge,
restored, dirty, output, -z arms) and `registry.py` (the whole C2 instrument) are unpinned, and
block 23's CL24 row claims "a prose claim and the bytes it describes cannot diverge silently".
They can: `gate.py` changed after the freeze and a row about it would not notice.

**F11 — `out_path` resolves relative paths against the process cwd, not the root.** From the lane
root, `--json-out .ufo/waves/…/out.json` is refused as "outside the lane root"; only absolute
paths inside the lane work. Harmless for the L1 (its receipts use absolute paths) but the
docstring and the claims' `<OUT>` placeholder do not say so.

---

## 5. Calibration

**Run (all receipts committed beside this report):** both counters at the stated freeze and at
`freeze == rev`; both selftests in the documented and the reachable form; census regeneration
(byte-equal, 38 paths); the merge-resolution, squash-fold, dirty-pathspec and restored-granularity
gate probes; the vacuous-rows forgery end-to-end including the battery; the interpreter pin
(`sha256 e6c44d2d…` at `0425224` equals block 23's cell); the block-23 text and the
PROTOCOL/SOURCES/lesson anchors read directly.

**Not run:** the round-45 counters themselves (I read their bytes; their receipts are round-45
evidence, not mine); the claim's `--spec r45 --profile v1` fidelity replay; the control receipts
under `.ufo/waves/round-46/controls/`; an end-to-end forged *registry* (I read the seven mutants
and the scope instead); the round-45 forgery fixtures (`fx-a6-cheapest-green`). Those are "not
run", not "passed".

**Inference, marked:** §3(ii) (the v1 profile is the r46 spec under loose semantics) is from the
code path and the three post-freeze port commits, not from executing `--profile v1` on a
round-45 artefact. §1's "13e false negative" is from reading `craft_blocks` and `skill_text`,
not from a fixture.

**What this seat does not decide:** whether the L1 should land block 23 at all. It should not land
rows 7 and 9 as written (F3, F4), and it should record F1 before writing `met` for either claim.

---

## 6. Receipts

| file | sha256 (first 16) | exit | command |
|---|---|---|---|
| `c1-at-stated-freeze.json` | `18d2c32fe78ff294` | 2 | `attest.py --root . --freeze 3182047 --rev 0425224 --no-battery` |
| `c2-at-stated-freeze.json` | `2f6a9035929498ab` | 2 | `registry.py --root . --freeze 3182047 --rev 0425224 --no-battery` |
| `c1-freeze-eq-rev.json` | `5811bfe0d6e439c9` | 0 | `attest.py --root . --freeze 0425224 --rev 0425224` |
| `c2-freeze-eq-rev.json` | `d3869553edf79e57` | 0 | `registry.py --root . --freeze 0425224 --rev 0425224` |
| `selftest-attest-documented.txt` | `e3b0c44298fc1c14` (empty) | 2 | `attest.py --selftest` |
| `selftest-attest-reachable.txt` | `0bf8f4c6ae0e46a0` | 0 | `attest.py --root . --freeze 0425224 --rev 0425224 --selftest` → `cases=16` |
| `selftest-registry-documented.txt` | `e3b0c44298fc1c14` (empty) | 2 | `registry.py --selftest` |
| `selftest-registry-reachable.txt` | `0fa8c31a6419905f` | 0 | `registry.py --root . --freeze 0425224 --rev 0425224 --selftest` → `cases=12` |
| `census-regen.json` | `573ec008fc3f9173` | 0 | `census.py --root . --rev 0425224 --out …` (equal to the committed file) |
| `vacuous-rows-forgery.json` | `48dd843067bf8a8d` | 0 | fixture repo, `attest.evaluate(..., with_battery=True)` on the gutted block |
| `squash-fold.json` | `1af8cdfff659f4e4` | 0 | `gate.freeze_state` on a squash-folded tamper+restore fixture |
| `dirty-union.json` | `ec956a70da8819ae` | — | `gate.dirty(d, ["other.txt"])` vs the union |
| `restored-granularity.json` | `f4fb5cdb38a21e6e` | 2 | `gate.freeze_state` on one restored + one changed file under a dir freeze |
| `merge-resolution.json` | `876a446f941f15a4` | 2 | `gate.freeze_state` on a merge whose own resolution edit adds `z.py` (`touched` names it; `restored` also names both files — F2) |
| `manifest.json` | `6cf66b077bdccdaa` | — | per-receipt: command, cwd, exit, stdout sha256, UTC window |

UTC window for the receipt batch: 2026-10-28T14:0x–14:1xZ (per-receipt stamps in `manifest.json`).
Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RevengerPlan` was removed after the receipts were
copied here. No install was made (no `pacman`, no `uv tool`, no `npx`); nothing was written outside
this seat directory.
