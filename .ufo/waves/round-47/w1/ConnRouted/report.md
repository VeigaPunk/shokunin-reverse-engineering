# ConnRouted — round 47: coverage of the round-46 routing

Lane `kaidoku-shokunin`, round 47. Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`.

**Two snapshots, because the lane moved while I worked.** S1 `caafeffa` (round-47 record commit,
my first pass), S2 `b1a058f32c6908a6b92248052f151d0b0e2c76b1` (tip at yield, 15:07:14). The round
declared freeze is now A6 `f54b3b6de9085d3db449ed5d0916296cb29c1f6d` and the claims are measured at
A7 `a07537869cf37963dff559fc75271dfa8fbb2542`. Every table row below is anchored to S2; the five
attacks were re-run at A7 after A5/A6 landed, and all five still pass.

I authored no round-47 byte. Receipts: `receipts.jsonl` (41 commands, each with exit code, stdout
sha256, UTC time), `exact-TIP.json`, `rec-TIP.json`, `exact-HEAD.json`, `rec-HEAD.json`,
`ctl-c1-5017-before.json`, `ctl-c1-A4-before.json`, `ctl-c1-A6-before.json`, `fz-5017e1f7.json`,
`probe*.py`, `probe*-results.json`, `probe3-results.txt`.

**Both counters at S2, re-measured by me:**

| counter | command | exit | key values |
|---|---|---|---|
| R47-C1 | `exact.py --root . --freeze f54b3b6d --rev b1a058f3` | 0 | `rule_blocks 24`, `rows 4`, `refs 9`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`, `frozen_path_changed []` |
| R47-C2 | `record.py --root . --rev b1a058f3` | 0 | `atoms 44`, `verified 43`, `corrections 2`, `exempted 1`, `corrections_bad []`, battery `3 / 0` |

## 1. Coverage of the routed defects — 21 rows

Legend — `closed` this round's bytes fail the defect's own forgery; `closed@46` closed in round 46 and
still holding at S2; **`partial`** the named check is met but the defect is only half bound; `open`
nothing closes it and the record says so; **`recurred`** round 47's own bytes reproduce the defect.
The last column also says whether another seat has already routed the residual (lesson `R47-CL*`).

| id | defect (one line) | verdict | closer / non-closer at S2 |
|---|---|---|---|
| R46-CL1 | a `git merge --squash` tamper+restore is invisible to both freeze arms | `open` | no row in block 24 (`SKILL.md:636-639`); `grep -c squash tools/round-47/*.py` → 0; lesson routed list "Inherited, still open" |
| R46-CL2 | the arm-vocabulary check is a substring test (`blobberish` passes `blob`) | `closed` | `tools/round-47/exact.py:236-240` (`a not in VOCAB`); forgery `substring-arm` `v2_exit 0 / v3_exit 1` (`exact-TIP.json`) |
| R46-CL3 | a routed id need only appear in *some* row, so a row may claim an id it does not address | **`partial`** | exactly-once closed (`exact.py:219-231`); the *addresses* half and the id↔arm pairing are unbound — **F5** — now routed by another seat as **R47-CL6 / R47-CL10** |
| R46-CL4 | the mutation list has no digest, so a deletion changes the denominator silently | `closed` (residual stated) | `exact.py:92-96`, `:250-251`, `:279`; forgery red. Residual (behaviour edit keeping the names) = R47-CL4 |
| R46-CL5 | the registry `purpose` cell is never validated | `open` | `grep -c purpose tools/round-47/*.py` → 0; lesson "Inherited, still open" |
| R46-CL6 | `-m --diff-merges=first-parent` is order-sensitive and nothing enforces the order | **`partial`** | `exact.py:246-264` counts one literal spelling anywhere in `gate.py` (`:260`). The literal swap is caught; a line-wrapped semantic reorder with the literal kept in a comment exits 0 — **F4** — **not routed anywhere in the lesson** |
| R46-CL7 | the verdict-map clause binds the digits 0/1/2, not their meanings | `open` | block 24's refs say "routed again … this block does not reach it" (`SKILL.md:643`); lesson "Inherited, still open" |
| R46-CL8 | the plan states a stale `cases=11` and a non-runnable bare `--selftest` | `recurred` | `python3 tools/round-47/record.py --selftest` → **exit 2** (argparse requires `--root`, `--rev`); same for `exact.py` (`receipts.jsonl: bare_selftest_*`). Registry rows do print the runnable form (`SKILL.md:1748-1749`), so only the invocation half recurs — plus the stale count, V6 |
| R46-CL9 | `freeze_state` derived the frozen set at the measured revision | `closed@46` | `tools/round-46/gate.py:152-166` unions both ends; `attest.py:657` case; `exact.py:400` calls it (verified by reading, not by a new fixture) |
| R46-CL10 | counters execute from the worktree; no dirty arm although the claims promised one | `closed@46` for `freeze_state` callers, **not extended to R47-C2** | `gate.py:186-192`, `attest.py:658`; `grep -c freeze tools/round-47/record.py` → **0** and `record.py:472-484` has no `--freeze` — now routed as **R47-CL12** |
| R46-CL11 | block 23's R45-CL19 row advertised exit 2 while the gate returns 0 | `closed@46` | `SKILL.md:624` — arm `none: …`, exit `0` |
| R46-V1 | the record says 40 + 40 = 80 seats; wave 2 was never dispatched | **`recurred`, and now masked** | `SCORECARD.md:3606` still says `Waves: 40 + 40 = 80 seats.`; `LOG.md:3363-3365` still says 80 and cites `.ufo/waves/round-46/{w1,w2}-results.json`, of which **0** exist; the counter *verifies* the atom because `.ufo/waves/round-46/w2-dispatch.json` carries `counts.spawn 40` — added by `22fd0d6b`, whose subject says "the wave-2 spec **left undispatched**". No `w2.ready`; one file under `w2/`. **F3** is the mechanism; R47-CL10 covers only the tautology variant, not this one |
| R46-V2 | the "empty" window named a `<tip>` placeholder and was not empty | `closed` | corrections line 2; `git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` → 0 lines; the placeholder is the single `exempted` item (`rec-TIP.json`) |
| R46-V3 | the before cell was attributed to a revision where it is false | **`recurred`** | the before cell (`SCORECARD.md:3702`, claims `:121`) says "at the freeze exit 1, `block_present 0`, `rule_blocks 23`". At the declared freeze A6: exit 1 but `block_present 1`, `rule_blocks 24`, and the only failing clause is `interpreter sha256 pin does not match the bytes at rev` (`ctl-c1-A6-before.json`); at A4 it is already exit 0. The described state exists only at `5017e1f` (`ctl-c1-5017-before.json`), and that freeze against the tip exits 2 `frozen_path_changed` (`fz-5017e1f7.json`) — see C3 |
| R46-V4 | the wave settlement (32 of 40, dead set, attack seats) was false at its own cited tip | `open` | `LOG.md:3363-3365` unchanged; no correction appended for the round-46 settlement; the same entry cites a results file that does not exist |
| R46-V5 | the lane repo is dirty at closure and still growing | **`recurred`** | `git status --porcelain` → **217 entries at 18:04:20Z** (216 excluding this seat): 5 modified tracked, 212 untracked; `git ls-files --others --exclude-standard` → 2544, all under `.ufo/waves/`. It moved 158 → 202 → 217 in nine minutes while seats wrote — which *is* the defect |
| R46-V6 | stale self-test counts in `SKILL.md` and the report | **`recurred`** | `SKILL.md:1743` still says "15 cases … 16 from the F3 repair" while `attest.py` registers **18**; `SKILL.md:1749` says record.py "9 cases" while the selftest prints **`cases=10`** (`receipts.jsonl: record_selftest_cases`). The round's own registry row is stale by one |
| R46-V7 | receipt paths cited in the record do not exist | **`recurred`** | `plans/round-47-claims.md:125` cites `controls/ctl-c1-1-v2-profile.json`; `git ls-tree HEAD .ufo/waves/round-47/controls` lists four files and that is not one of them |
| R46-V8 | "9 line-selected citations" when it is 8 + 1 pinned interpreter | `open` (not re-introduced) | `SCORECARD.md:3610` still reads "9 line-selected citations"; round 47 does not repeat the phrasing (block 24 says `refs 9`, of which one is the self pin) and the claims require only `>= 3` |
| R46-V9 | the round's Gate recorded no rejected candidate | `closed` | `corpus/lessons/round-47.md` `## Gate` — S144 opened, **REJECTED** with a flip condition, plus the `Reject` bullet and census 142 → 144 |
| R46-V10 | a claim about an untracked file set that no committed artefact can attest | `open` (no recurrence) | no round-47 document makes an untracked-set claim; the underlying set is 212 untracked porcelain entries (2544 files) with no committed manifest |

Tally, non-overlapping: **closed this round 4** (CL2, CL4, V2, V9) · **closed at 46 and verified 3**
(CL9, CL10-core, CL11) · **partial 2** (CL3, CL6) · **open 12** (CL1, CL5, CL7, CL8, V1, V3, V4, V5,
V6, V7, V8, V10), of which **6 recur inside round 47's own bytes** (CL8, V1, V3, V5, V6, V7).

The round's own routed list names four inherited items (CL1, CL5, CL7, CL8) and I agree on all four.
It does **not** carry the two the round-47 landing reproduces: **V1/V4 (the seat settlement)** and
**V3 (the before-cell revision)**.

## 2. Five attacks on the frozen instruments

Fixtures, not edits: originals read from git objects, altered bytes committed only in throwaway repos
under my scratch root. All five were re-run at A7 (`a0753786`) after A5/A6; none was fixed by them.

### F1 — `record.py` has no frozen-byte arm — **routed at S2 as R47-CL12**
Claims `:11`: "a change makes both counters exit 2 `frozen_path_changed`". Measured:
`grep -c freeze tools/round-47/record.py` → 0; no `--freeze` in `record.py:472-484`; the exit-2 set in
`SKILL.md:1749` does not name it. `exact.py --freeze 5017e1f --rev b1a058f3` → exit 2
`frozen_path_changed`, `restored ['tools/round-47/record.py']`; `record.py --rev b1a058f3` → exit 0.

### F2 — the `axes` correction class is unparseable — **routed at S2 as R47-CL14, and the record now says so**
`record.py:50` — `CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` — omits
`axes`, so an `axes` correction is never parsed, counted or re-derived; `corrects()`'s `axes` branch
(`:280`) is unreachable and a second, dead branch at `:292-297` dereferences `atom["axis"]`, undefined
there. Measured at A7 (`probe-results.json`):

| card | exit | `corrections` | `corrections_bad` |
|---|---|---|---|
| real card | 0 | 2 | [] |
| `- corrects axes coverage: 999/999` | **0** | 2 | [] |
| `- corrects axes depth: 999/999` | **0** | 2 | [] |
| `- corrects axes speed: 999/999` (ghost axis) | **0** | 2 | [] |
| `- corrects seats round-46: 2 waves, 80 seats total` (true) | 0 | 3 | [] |
| `- corrects seats round-46: 3 waves, 81 seats total` (false) | 1 | 3 | `claimed [3,81] derived [2,80]` |

The parser discriminates `seats` and is blind to `axes`. The landed corrections section has since
moved to "repaired **in place**, not by a correction line" and names the inertness — the right
repair; the frozen clause (`claims:166-169`, "an `axes` correction must state `<resolved>/<total>`")
remains unsatisfiable-in-principle, which is why it belongs in the round-48 list rather than the
record.

### F3 — the `seats` atom is satisfied by a dispatch *plan*, not by a dispatch — **not routed as such**
`record.py:65-83` reads `counts.spawn`. Fixture (`probe2-results.json`), card atom
`Waves: 40 + 40 = 80 seats`:

| fixture state | `mismatches` | derived |
|---|---|---|
| only `w1-dispatch.json` (spawn 40) | 1 | `claimed [40,40,80] derived [40,0,40]` |
| plus `w2-dispatch.json` (spawn 40) | **0** | atom verified |

An 11-line JSON file turns a false record sentence true. The real repo is in exactly this state (V1):
the wave-2 dispatch file exists, the wave did not, and the commit that added the file says so. R47-CL10
routes the *tautology* (a record that omits its claims); this is the complement — a record that states
a claim the counter certifies from an intent file.

### F4 — the flag-order clause binds a spelling, not the argv order — **not routed**
`exact.py:260` counts the literal and its literal reverse anywhere in `gate.py`. Fixture
(`probe2-results.json`): live call rewritten as `git(root, "log", "--diff-merges=first-parent",\n "-m", …)`
with the correct literal kept in a comment; the file still compiles.

| fixture | exit | `gate_order_literal` / `_reversed` |
|---|---|---|
| live literal swapped (the counter's own mutation) | 1 | 0 / 1 |
| line-wrapped reorder + clause residue in a comment | **0** | **1 / 0** |
| reversed literal + comment | 1 | 1 / 1 |

`E6` confirms the premise on git 2.56.0: the correct order prints the merge once, the reversed order
**twice**. A semantically blinded arm passes clause 7.

### F5 — the `v3 arm` column binds a multiset, not an assignment — **routed at S2 as R47-CL6 / R47-CL10**
`exact.py:224-243` binds ids (clause 4) and tokens (clause 5) separately; nothing binds the pair.
Fixture (`probe3-results.txt`): `order` moved onto `R46-CL2`, `symbol` onto `R46-CL6` → **exit 0**,
`arm_tokens [order, once, digest, symbol]`, all four ids still exactly once.

## 3. Contradictions, stated rather than smoothed

- **C1.** Claims `:11` ("both counters exit 2 `frozen_path_changed`") vs `record.py` having no freeze
  concept — F1, routed as R47-CL12.
- **C2.** `SCORECARD.md:3685` ("all before any claim verdict") and `LOG.md:3419` ("Four amendments
  before verdict") vs the claims' own A2 paragraph (`plans/round-47-claims.md:36`: "The first
  **after-data run** … at the landing `e856beb5` failed clause 6") and vs the timestamps: landing
  `e856beb5` 14:51:02 → A2 14:51:50 → A3 14:52:38 → A4 14:53:05 → A5 14:56 → A6 14:58. A2–A6 are
  post-data by the round's own account. (The A1-vs-A6 freeze contradiction is separately routed as
  R47-CL11.)
- **C3.** Before cell (`SCORECARD.md:3702`, claims `:121`) vs the declared freeze A6, where the
  counter exits 1 for a **pin** reason with `block_present 1`, `rule_blocks 24`, and vs A4, where it
  is already exit 0. The described before-state exists only at `5017e1f`, and that freeze against the
  tip exits 2 `frozen_path_changed`. "Before" and "freeze" are not simultaneously measurable for C1
  in this round. This is R46-V3's class, reproduced.
- **C4.** `SKILL.md:1749` "9 cases" vs `RECORD_SELFTEST: cases=10 failures=0`; `SKILL.md:1743`
  "15/16" vs 18 case registrations.
- **C5.** Claims `:125` cites `controls/ctl-c1-1-v2-profile.json`, absent at S2 (four control files,
  that one not among them). R47-CL9 describes what that control *runs*; the receipt is still missing.
- **C6.** The claims' C2 scope excludes `LOG.md`, yet the most-falsified sentences of the routed list
  live there (`LOG.md:3363-3365`). No counter reads the file the spot-check told the lane to correct.

Checked and **not** a defect: the kill rule "a block that reuses block 23's text relabelled `24. `
fails clauses 2–6" holds — block 23's header is `trigger | v1 hole | v2 arm | exit` (`SKILL.md:614`),
block 24's is `trigger | v2 hole | v3 arm | exit`.

## 4. What remains unaddressed at S2 — bounded

Already routed by other seats, so not repeated here as work: F1 (CL12), F2 (CL14), F5 (CL6/CL10), the
A1-vs-A6 freeze naming (CL11), the tautology hole (CL10), the `--profile` battery coupling (CL9).

Still needing a decision or a routing line:

1. **F4** — the flag-order clause is textual. Minimal closure: assert the live `git(...)` argument
   vector, not a file substring, or state in the block that clause 7 binds one spelling.
2. **F3 + V1/V4** — a dispatch `counts.spawn` is intent, not evidence. Either derive seats from
   `w2/*.ready` + results, or correct the round-46 settlement sentence and say the atom is a plan
   check.
3. **V3 / C3** — name the revision the before cell was measured at (`5017e1f`), in the SCORECARD row
   and in the claims' "Before" paragraph.
4. **V6 / C5** — the two stale case counts and the missing `ctl-c1-1-v2-profile.json` citation.
5. **V5 / V10** — 217 dirty entries and 2544 untracked files with no committed manifest; land the wave
   evidence under a named commit or state the set by count and name.

## 5. Honest capture and limits

- Every value in §1–§3 comes from a command in `receipts.jsonl` or a fixture in this directory. Nothing
  is quoted from another seat's report; where a finding coincides with an `R47-CL*` line I say so and
  leave the credit there.
- **Not run:** no fixture exercises R46-CL9/CL10 (I read `gate.py:152-192` and the two selftest case
  registrations instead); the `path`, `rev` and `window` classes were not attacked beyond F2's ghost
  path case; no attempt was made to break `record.py`'s `sections()` window.
- **Defect of my own capture:** two scratch captures were briefly written under `/tmp` and removed;
  nothing under `/tmp` is cited. All cited evidence is under this directory.
- Fixtures live under `/fast/scratch/hyaku/kaidoku-r47/ConnRouted` and are removed after the copies
  here; the drivers (`probe*.py`, `receipts*.sh`) rebuild them deterministically from git objects at
  the revision named in `PROBE_REV`.
- No tool was installed. No lane byte outside this directory was written; every git call was read-only.
