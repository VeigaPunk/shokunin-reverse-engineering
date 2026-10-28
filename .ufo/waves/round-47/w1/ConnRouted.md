# ConnRouted — round 47: coverage of the round-46 routing

Lane `kaidoku-shokunin`, round 47. Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. Measured at
`caafeffa330a15e59412bc037591f6942b51e5aa` (round-47 record commit), declared freeze
`1e2c3102952dc636650095643c1963c833859019` (A4), first freeze `5017e1f7299c3a812e87e7950148f54313dd279e`.

I did not author any round-47 byte. I re-ran both frozen counters at HEAD and at the declared freeze,
re-derived each routed defect's own measurement from committed objects, and built five fixture attacks
on the two claims. Receipts: `receipts.jsonl` (33 commands, each with exit code, stdout sha256, UTC
time), `rec-HEAD.json`, `exact-HEAD.json`, `ctl-c1-A4-before.json`, `ctl-c2-A4.json`,
`fz-5017e1f7.json`, `fz-9018c53b.json`, `probe*.py`, `probe*-results.json`, `probe3-results.txt`. Every path below is
relative to this seat directory unless it names a lane path.

**Counters at HEAD, re-measured by me (not read from a receipt):**

| counter | command | exit | key values |
|---|---|---|---|
| R47-C1 | `python3 -I -B tools/round-47/exact.py --root . --freeze 1e2c310295 --rev caafeffa` | 0 | `rule_blocks 24`, `rows 4`, `refs 8`, `arm_tokens [symbol,once,digest,order]`, battery `4/4/0/1/0` |
| R47-C2 | `python3 -I -B tools/round-47/record.py --root . --rev caafeffa` | 0 | `atoms 41`, `verified 40`, `corrections 2`, `exempted 1`, `corrections_bad []`, battery `3/0` |

## 1. Coverage of the routed defects — 21 rows

Legend — `closed` this round's bytes fail the defect's own forgery; `closed@46` closed in round 46 and
still holding at HEAD; **`partial`** the named check is met but the defect is only half bound;
`open` nothing in this round closes it and the record says so; **`recurred`** round 47's own bytes
reproduce the defect.

| id | defect (one line) | verdict | closer / non-closer |
|---|---|---|---|
| R46-CL1 | a `git merge --squash` tamper+restore is invisible to both freeze arms | `open` | stated, not closed: block 24 has four rows, none of them this one (`SKILL.md:636-639`); `grep -c squash tools/round-47/*.py` → 0; claims `:53-56`; lesson `:80` |
| R46-CL2 | arm-vocabulary check is a substring test (`blobberish` passes `blob`) | `closed` | `tools/round-47/exact.py:236-240` binds `a not in VOCAB` after stripping backticks/spaces; forgery `substring-arm` scores `v2_exit 0 / v3_exit 1` (`exact-HEAD.json`) |
| R46-CL3 | a routed id need only appear in *some* row, so a row may claim an id it does not address | **`partial`** | exactly-once is closed (`exact.py:219-231`, per-row `len(ids) != 1` at `:225`, cardinality at `:229`; forgery `duplicate-routed-id` red). The *addresses* half is not bound by anything, and neither is the id↔arm assignment — see **F5**: permuting `order` onto `R46-CL2` and `symbol` onto `R46-CL6` exits 0 |
| R46-CL4 | the mutation list has no digest, so a deletion changes the denominator silently | `closed` (residual stated) | `exact.py:92-96` (`MUTATIONS`, `MUT_DIGEST`), digest compared at `:250-251`, `forgeries_total == 4` at `:279`; forgery `stale-mutations-digest` red. Residual (a behaviour edit that keeps the names) is stated as R47-CL4, lesson `:74-76` |
| R46-CL5 | registry `purpose` cell is never validated | `open` | `grep -c purpose tools/round-47/*.py` → 0; block 24 rows exclude it; lesson `:80-81` |
| R46-CL6 | `-m --diff-merges=first-parent` is order-sensitive and nothing enforces the order | **`partial`** | `exact.py:246-264` counts one literal spelling anywhere in `gate.py` (`:260`). The literal swap is caught; a line-wrapped semantic reorder with the literal kept in a comment exits 0 — **F4**, and git 2.56.0 really does print the merge twice when reversed (**E6**) |
| R46-CL7 | the verdict-map clause binds the digits 0/1/2, not their meanings | `open`, re-routed in the landed bytes | block 24's own refs say "routed again, because a verdict map is a registry concern and this block does not reach it` (`SKILL.md:643`); `grep -c verdict tools/round-47/*.py` → 0; lesson `:81` |
| R46-CL8 | plan states a stale `cases=11` and a non-runnable bare `--selftest` | `recurred` | `python3 tools/round-47/record.py --selftest` → **exit 2** (argparse: `--root`, `--rev` required); same for `exact.py` (`receipts.jsonl: bare_selftest_*`). The registry rows do print the runnable form (`SKILL.md:1748-1749`), so only the invocation half recurs — plus the stale count, see V6 |
| R46-CL9 | `freeze_state` derived the frozen set at the measured revision | `closed@46` | `tools/round-46/gate.py:152-166` unions both ends; `attest.py:657` case `red-frozen-section-shrink-is-exit-2`; `exact.py:400` calls it. Verified by reading, not by a new fixture |
| R46-CL10 | counters execute from the worktree; no dirty arm although the claims promised one | `closed@46` for `freeze_state` callers, **not extended to R47-C2** | `gate.py:186-192` refuses a dirty frozen path; `attest.py:658` case. `grep -c freeze tools/round-47/record.py` → **0**, and `record.py:472-484` has no `--freeze`: the C2 counter has no frozen or dirty arm at all. See contradiction C1 |
| R46-CL11 | block 23's R45-CL19 row advertised exit 2 while the gate returns 0 | `closed@46` | `SKILL.md:624` — arm cell reads `none: …`, exit cell `0` |
| R46-V1 | the record says 40 + 40 = 80 seats; wave 2 was never dispatched | **`recurred`, and now masked** | `SCORECARD.md:3606` still says `Waves: 40 + 40 = 80 seats.`; `LOG.md:3363-3365` still says 80 and cites `.ufo/waves/round-46/{w1,w2}-results.json`, of which **0** exist at HEAD; the C2 counter *verifies* the atom because `.ufo/waves/round-46/w2-dispatch.json` carries `counts.spawn 40` — the file added by `22fd0d6b`, whose subject line reads "the wave-2 spec **left undispatched**". No `w2.ready` (only `w1.ready`, `w1.ready.dispatched`), one file under `w2/`. **F3** shows any written dispatch file flips the atom green |
| R46-V2 | the "empty" window named a `<tip>` placeholder and was not empty | `closed` | corrections line 2 states `332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md`; I re-ran `git log --name-status --format=` over it → 0 lines (`receipts.jsonl: window_332f_58eb_empty`); `corrections_bad []`, and the placeholder atom is the one item in `exempted` (`rec-HEAD.json`) |
| R46-V3 | the before cell was attributed to a revision where it is false | **`recurred` at the top level of round 47** | round-47's before cell ("at the freeze exit 1, `block_present 0`, `rule_blocks 23`") is **false at the declared freeze A4**: `exact.py --freeze 1e2c310295 --rev 1e2c310295` → exit 0, `block_present 1`, `rule_blocks 24` (`ctl-c1-A4-before.json`). It is true only at `5017e1f`. See contradiction C2 |
| R46-V4 | the wave settlement (32 of 40, dead set, attack seats) was false at its own cited tip | `open` | `LOG.md:3363-3365` unchanged; no correction appended for the round-46 settlement; the same entry cites a results file that does not exist (V1 above) |
| R46-V5 | the lane repo is dirty at closure and still growing | **`recurred`** | `git status --porcelain` → **217 entries at 18:04:20Z** (216 excluding this seat's own directory): 5 modified tracked, 212 untracked; `git ls-files --others --exclude-standard` → 2544, all under `.ufo/waves/`. The count moved 158 → 202 → 217 in nine minutes while seats were still writing — which *is* the defect |
| R46-V6 | stale self-test counts in `SKILL.md` and the report | **`recurred`** | `SKILL.md:1743` (attest.py) still says "15 cases … 16 from the F3 repair", while the code registers **18** (`attest_case_registrations` → 18); `SKILL.md:1749` says record.py "9 cases", the selftest prints **`cases=10`** (`receipts.jsonl: record_selftest_cases`). The round's own registry row is stale by one, one round after the defect was routed |
| R46-V7 | four receipt paths cited in the record do not exist | **`recurred`** | `plans/round-47-claims.md:125` cites `controls/ctl-c1-1-v2-profile.json`; `git ls-tree HEAD .ufo/waves/round-47/controls` lists four files and that is not one of them |
| R46-V8 | "9 line-selected citations" when it is 8 + 1 pinned interpreter | `open` (not re-introduced) | `SCORECARD.md:3610` still reads "9 line-selected citations"; round 47 does not repeat the phrasing (block 24 prose says `refs 8`) and the claims require only `>= 3` |
| R46-V9 | the round's Gate recorded no rejected candidate | `closed` | `corpus/lessons/round-47.md:43,55` — S144 opened, **REJECTED** with a flip condition, plus the `Reject` bullet and census 142 → 144 |
| R46-V10 | a claim about an untracked file set that no committed artefact can attest | `open` (no recurrence) | no round-47 document makes an untracked-set claim; the underlying set is 197 untracked files at HEAD with no committed manifest |

Tally, non-overlapping: **closed this round 4** (CL2, CL4, V2, V9) · **closed at 46 and verified 3**
(CL9, CL10-core, CL11) · **partial 2** (CL3, CL6) · **open 12** (CL1, CL5, CL7, CL8, V1, V3, V4, V5,
V6, V7, V8, V10) of which **6 recur inside round 47's own bytes** (CL8, V1, V3, V5, V6, V7).

The round's own `## Routed defects (for round 48)` list (lesson `:79-81`) names four inherited items
(CL1, CL5, CL7, CL8). My table agrees on those four and adds the two the list does not carry: **V1/V4
(the seat settlement) and V3 (the before-cell revision)**, both of which the round-47 landing
reproduces rather than inherits.

## 2. Five attacks on the frozen instruments

Each attack is a fixture, not an edit: the originals were read from git objects and the altered bytes
were committed only inside a throwaway repo under my scratch root. Scripts and outputs are in this
directory.

### F1 — `record.py` has no frozen-byte arm, so the claims' "both counters" sentence is false
Claims `:11`: "a change makes both counters exit 2 `frozen_path_changed`". Measured:
`grep -c freeze tools/round-47/record.py` → **0**; `record.py:472-484` declares no `--freeze`; the
exit-2 set in the registry row (`SKILL.md:1749`) does not include `frozen_path_changed`.
`exact.py --freeze 5017e1f --rev HEAD` → exit 2 `frozen_path_changed` with
`restored ['tools/round-47/record.py']`; `record.py --rev HEAD` → exit 0. One counter's frozen scope is
enforced; the other has none.

### F2 — the `axes` correction class is unparseable, so C2 clause 3 is vacuous for it
Claims `:166-169` require that "an `axes` correction must state `<resolved>/<total>`" and that "every
correction line itself re-derives". `record.py:50`:
`CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` — **`axes` is absent**, so
the two `axes` lines in `SCORECARD.md`'s corrections section are never parsed, never counted and never
re-derived; `corrects()`'s `axes` branch (`record.py:280`) is unreachable, and a second, dead `axes`
branch at `:292-297` dereferences `atom["axis"]`, which is undefined in that scope.

Measured (`probe.py`, `probe-results.json`):

| card | exit | `corrections` | `corrections_bad` |
|---|---|---|---|
| real card | 0 | 2 | [] |
| `- corrects axes coverage: 999/999` | **0** | 2 | [] |
| `- corrects axes depth: 999/999` | **0** | 2 | [] |
| `- corrects axes speed: 999/999` (ghost axis) | **0** | 2 | [] |
| `- corrects seats round-46: 2 waves, 80 seats total` (true) | 0 | 3 | [] |
| `- corrects seats round-46: 3 waves, 81 seats total` (false) | 1 | 3 | `claimed [3,81] derived [2,80]` |

So the parser discriminates `seats` and is blind to `axes`: two of the four landed correction lines
cannot fail, and the landed corrections section's own sentence ("each `corrects` line below …
is itself re-derived by the counter") is false for exactly those two. The three-forgery battery
(`record.py:400-455`) never forges an `axes` line, so this class is also outside the battery.

### F3 — the `seats` atom is satisfied by a dispatch *plan*, not by a dispatch
`record.py:65-83` reads `counts.spawn` from `w1-dispatch.json`/`w2-dispatch.json`. Fixture
(`probe2.py`, `probe2-results.json`): a card whose only seat atom is `Waves: 40 + 40 = 80 seats`.

| fixture state | exit | `mismatches` | derived |
|---|---|---|---|
| only `w1-dispatch.json` (spawn 40) | 1 | 1 | `claimed [40,40,80] derived [40,0,40]` |
| plus `w2-dispatch.json` (spawn 40), a file that does not prove a dispatch | 1 (only `corrections 0 < 2`) | **0** | atom verified |

An 11-line JSON file with `{"counts":{"spawn":40}}` turns a false record sentence true. The real
repo is in exactly this state: the wave-2 dispatch file exists, the wave did not (one file under
`w2/`, no `w2.ready`, zero `results.json`), and the commit that added the file says
"the wave-2 spec left undispatched". R46-V1 asked for the SCORECARD sentence to be amended; the
counter now certifies it instead.

### F4 — the flag-order clause binds a spelling, not the argv order
`exact.py:260` counts `'\"-m\", \"--diff-merges=first-parent\"'` and its literal reverse anywhere in
`gate.py`. Fixture (`probe2.py`): the live call rewritten as
`git(root, "log", "--diff-merges=first-parent",\n            "-m", ...)` with the correct literal kept
in a comment; the file still compiles.

| fixture | exit | `gate_order_literal` / `_reversed` |
|---|---|---|
| live literal swapped (the counter's own mutation) | 1 | 0 / 1 |
| line-wrapped reorder + clause residue in a comment | **0** | **1 / 0** |
| reversed literal + comment | 1 | 1 / 1 |

`E6` confirms the premise on git 2.56.0: `git log -m --diff-merges=first-parent …` prints the merge
once, the reversed order prints it **twice**. So a semantically blinded arm passes clause 7. This is
the narrowest kind of closure — the one-sentence rewrite is caught, the defect ("one argument reorder
silently undoes the arm") is not.

### F5 — the `v3 arm` column binds a multiset of tokens, not an assignment to the routed defect
`exact.py:224-243` binds ids (clause 4) and tokens (clause 5) separately; nothing binds the pair.
Fixture (`probe3.py`): block 24 with `order` moved onto `R46-CL2` and `symbol` onto `R46-CL6`.

| block | exit | `arm_tokens` |
|---|---|---|
| landed | 0 | `[symbol, once, digest, order]` |
| arms permuted across ids | **0** | `[order, once, digest, symbol]` |

The matrix could claim that the flag-order arm closes the substring hole and still score met. Since
block 24's whole claim is that the *binding* is exact, this is the sharpest residual in C1, and it is
not in the round's routed list (R47-CL4 covers mutation bodies only).

## 3. Contradictions, stated rather than smoothed

- **C1.** Claims `:11` ("both counters exit 2 `frozen_path_changed`") vs `record.py` having no freeze
  concept (0 hits, no `--freeze`) — F1.
- **C2.** `SCORECARD.md:3683` ("commits, **all before any claim verdict**") and `LOG.md:3419` ("Four
  amendments before verdict") vs the claims' own A2 paragraph (`plans/round-47-claims.md:36`: "The
  first **after-data run** of R47-C2 at the landing `e856beb5` failed clause 6") and vs the
  timestamps: landing `e856beb5` 14:51:02 → A2 `62e33f7d` 14:51:50 → A3 14:52:38 → A4 14:53:05. A2,
  A3 and A4 are post-data by the round's own account.
- **C3.** Before cell `SCORECARD.md:3702` / claims `:121` ("at the freeze exit 1, `block_present 0`,
  `rule_blocks 23`") vs the declared freeze A4, where the counter is already green
  (`ctl-c1-A4-before.json`). The only freeze under which the before cell is true is `5017e1f`, and
  under that freeze the counter at HEAD exits 2 `frozen_path_changed` (`fz-5017e1f7.json`) — so
  "before" and "freeze" are not simultaneously measurable for C1 in this round. This is R46-V3's
  class, reproduced by the round that claims to re-derive its record.
- **C4.** Corrections section: "each `corrects` line below … is itself re-derived by the counter" vs
  `corrections 2` over four lines, with forged `axes` lines passing — F2.
- **C5.** `SKILL.md:1749` "9 cases" vs `RECORD_SELFTEST: cases=10 failures=0`.
- **C6.** Claims `:125` cites `controls/ctl-c1-1-v2-profile.json`, absent at HEAD (R46-V7's class).
- **C7.** The claims' C2 scope excludes `LOG.md`, yet R46-V1/V4's most-falsified sentences live there
  (`LOG.md:3363-3365`). The counter cannot see the file the spot-check told the lane to correct.

Checked and **not** a defect: the claims' kill rule "a block that reuses block 23's text relabelled
`24. ` fails clauses 2–6" holds — block 23's header is `trigger | v1 hole | v2 arm | exit`
(`SKILL.md:614`), block 24's is `trigger | v2 hole | v3 arm | exit`.

## 4. What this means for landing

Landable as-is, on my evidence: block 24 as a *literal* matrix (C1 exit 0, four forgeries red under
v3 and green under v2), the `seats`/`window` corrections, and the `window` closure of V2.

Before the round's own record can claim what it claims, five things need a decision by the L1 — none
of them a rewrite of frozen bytes, all of them record or routed-list edits:

1. **Name the before revision.** Either say "at `5017e1f`" in the SCORECARD/LOG before cell and in the
   C1 "Before" paragraph (the receipt already carries `freeze = rev = 5017e1f`), or move the freeze
   back before the landing and accept that clause 7 and the record clause then read a different
   instrument. C2/C3 cannot both be true as written.
2. **Drop or fix the "all before any claim verdict" sentence** in `SCORECARD.md` and `LOG.md`; the
   round's own A2 paragraph is the counter-evidence.
3. **Correct the round-46 seat settlement** (V1/V4) or state that the counter's `counts.spawn`
   derivation means a *plan* file is evidence. As it stands the record's 80-seat sentence is certified
   by the file whose own commit says the wave was never dispatched.
4. **Route F2, F4, F5** into the round-48 list: the `axes` correction class is unparseable, the
   flag-order clause is textual, and the arm column is a multiset. Each is a frozen-clause gap the
   record currently does not state, unlike R47-CL4.
5. **Fix the two stale case counts** (`SKILL.md:1743` 15/16 vs 18; `:1749` 9 vs 10) and land
   `controls/ctl-c1-1-v2-profile.json` or drop the citation — V6 and V7, one round after both were
   routed.

## 5. Honest capture and limits

- Every value in §1–§3 comes from a command in `receipts.jsonl` or a fixture in this directory; the
  two counter runs are in `rec-HEAD.json` and `exact-HEAD.json`. Nothing is quoted from another seat's
  report.
- **Not run:** no fixture exercises R46-CL9 or R46-CL10 (I read `gate.py:152-192` and the two selftest
  case registrations instead); no attempt was made to bypass `record.py`'s window arm beyond the
  `axes` class; the `path` and `rev` classes were not attacked.
- **Defect of my own capture:** two scratch captures were briefly written under `/tmp` and removed;
  nothing under `/tmp` is cited here. All cited evidence is under this directory.
- Fixtures live under `/fast/scratch/hyaku/kaidoku-r47/ConnRouted` and were removed after the copies
  here were made; the fixture drivers (`probe*.py`) rebuild them deterministically from git objects at
  `caafeffa`.
- No tool was installed. No lane byte outside this directory was written; all git calls were read-only.
