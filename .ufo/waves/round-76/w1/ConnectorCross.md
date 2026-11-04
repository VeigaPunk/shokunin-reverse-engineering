# ConnectorCross — sibling-overlap scan (round 76, wave 1)

Seat: `ConnectorCross` (connector). Read-only. Lane `kaidoku-shokunin`, HEAD
`201df797d555d324ee2eb5e3c4b9bbe4fb77d85a` at scan time. The lane's round-76 instruments were read
at that HEAD; they are the subject of the scan, never a source of truth about a sibling lane.

Question: do other lanes already own what this round's two instruments do —
(1) a printed-command / plan-command gate, (2) a `## Capabilities`-table atom inside a record
audit — and if so, who owns the surface and where do the semantics diverge?

Method: fixed-argv searches over the fleet root `/home/vgpnk/Projects/shokunin`, then manual
reading of every candidate that both (a) executes a subprocess and (b) is fence/line aware, and
every candidate that parses a `## Capabilities` heading in Python. The full command list, raw hit
lists and the classification are in `ConnectorCross/receipt.json`, reproduced by the
`ConnectorCross/scan.py` shipped beside it.

Verdicts use the assignment's two labels only: **duplication with named divergences** or
**no overlap**. No sibling surface is absorbed, copied, or edited.

---

## Q1 — printed-command / plan-command gates

### 1.1 The searched command (seat spec, verbatim form)

```
grep -rl 'counting-command\|plan-command\|plan_command' /home/vgpnk/Projects/shokunin/*-shokunin \
  --include='*.py' --include='*.md'
```

Run equivalent (single root, same patterns, `.git` excluded), then classified by path shape. The
receipt in this seat's evidence dir is the snapshot; the discipline is that the *invariant* classes
are asserted and the drifting ones are labelled. `instrument`-class hits are invariant; lesson and
wave-evidence counts move between runs because peer seats are writing wave files concurrently (the
numbers below are the receipt's, total 598):

| class | files | lanes |
|---|---|---|
| **instrument** (`<lane>/{tools,plans,scripts}/**.py`) | **1** | `kaidoku-shokunin` (`tools/round-76/plan-command.py`) — invariant |
| lesson (`corpus/lessons/`) | 24 | chousa, kaidoku, kama, kengaku, kotodama, kumitate, mado, mori, revenger, souji, tameshi |
| record (`SCORECARD/LOG/SKILL/PROVINCE/README.md`) | 16 | kaidoku, kengaku, kotodama, mado, mori, revenger, tameshi |
| registry (`corpus/SOURCES.md`) | 6 | chousa, kaidoku, kake, kengaku, mado, revenger |
| claims plan / quality doc (`plans/*.md`, `corpus/QUALITY.md`) | 5 | kaidoku (`plans/round-76-claims.md`), kengaku (rounds 59/60/64 claims), mori (`corpus/QUALITY.md`) |
| wave evidence (`.ufo/`, `reports/`, `census/`, `corpus/evidence/`) | 546 | every lane with a wave tree |

**Result: the literal token set has exactly one live instrument in the fleet, and it is this
round's.** Every other hit is prose (a lesson sentence about a counting command, a SCORECARD
cell, a registry row) or frozen wave evidence. A byte-token search therefore reports "no sibling
plan-command gate", which is true of the *name* and false of the *class* — see 1.2.

Secondary tokens: `PLACEHOLDER_UNBOUND` — **every hit is inside `kaidoku-shokunin`** (9 files at
receipt generation: `tools/round-76/plan-command.py`, `plans/round-76-claims.md`, `SCORECARD.md`,
`corpus/knowledge/2026-11-04-r76-plan-command-executability.md`, `.ufo/waves/round-76/gen-w1.py`,
and four wave drafts by this round's peer seats). No sibling lane uses the code word at all, and
none of the hits is a sibling instrument.

### 1.2 The class, found semantically (fence/subprocess/shlex), not by name

Search: for every `*.py` under the fleet root containing `subprocess`, keep the ones that also
carry a fence/code-block token; then read the candidates. 324 files survive the mechanical filter
(most are wave fixtures); **87 are lane instruments** (live `tools/`, `plans/`, `scripts/`,
`verifiers/` modules). Of those, exactly one executes a command *parsed out of a committed record*
and prices its output:

| lane / file | what it actually does | verdict vs `tools/round-76/plan-command.py` |
|---|---|---|
| `kengaku-shokunin/plans/correction_command_check.py` (275 lines, round 60 C2, "counting-command reproduction gate") | Population: every `plans/round-<N>-claims.md`; only the body of a heading matching `^#{2,3} .*dated correction`. Class: a one-line backticked ``grep -c … 'PATTERN' PATH`` followed by `→ <digits>`. Re-runs it (`run_command`, lines 96-122) with `shlex.split`, `shell=False`, `cwd=lane`, `timeout=30`; requires stdout `.isdigit()` and equal to the printed expectation. Prints `CMDPOP files=… ok=… defects=…`, one `CMD-DEFECT` per miss, `PREDICATE R60-C2 pass|fail`. Exit 0/1, 2 on setup. Selftest 6 cases,
including a forced empty-population arm. | **Duplication with named divergences** (same class: re-run the printed count and price it) |
| `tsukuroi-shokunin/tools/check-recheck-commands.py` (1680 lines) | Reads `recheck:` lines, follows section pointers, and **reports forbidden binary invocations** in the printed commands. Never executes. | No overlap on execution; **duplication of the extraction surface** (which printed spans count as commands: backtick span / fenced block line / `procedure:` line) with a divergence: it audits safety, not reproducibility. |
| `tsukuroi-shokunin/tools/receipt-run.py` (300 lines) | Runs a caller-supplied argv no-shell under a wall-clock budget and writes a raw receipt into the lane tree; exit 0/1/2, child rc recorded not mirrored. | **Duplication with named divergences** on the *executor* half only: argv comes from the CLI, never from a document; no placeholder refusal, no counter reader, no battery. |
| `souji-shokunin/tools/souji-receipt-run.py` (395 lines) | Re-derives a command at a named revision and binds rev + tool sha256 into the receipt; `verify` refuses a receipt whose digest is not the committed blob. | Same as above, plus revision binding this round does not have (divergence in the other direction — `plan-command.py` binds nothing to a revision). |
| `kama-shokunin/tools/round73-receipt-claim-binding.py` (755 lines) | Grades what a citing line *claims* about a receipt against the receipt's own `tip=`/`rev=` header. No execution. | No overlap (claim-vs-header, not command-vs-output). |
| `game-dev-2d-shokunin/reports/round-102/mutations/scr4-scorecard-cite-repair.py` | Byte-repairs three SCORECARD counting commands; asserts each repaired command lands 3×. | No overlap (repair script, not a gate). |
| `kama-shokunin/tools/pre-report-gate.py` (1202 lines) | Composes five sibling instruments into 9 arms and prints one `PRE_REPORT` line. | No overlap on the command surface; **precedent for the battery shape** (arm list + one verdict line + exit 0 only when all arms pass). |

**Named divergences — `plan-command.py` vs `kengaku correction_command_check.py`** (the one real
same-class sibling):

1. **Extraction surface.** kengaku: one-line backtick spans inside `dated correction` sections of
   `plans/round-*-claims.md`. kaidoku: a fenced `sh|bash` block between
   `<!-- counting-command: NAME -->` … `<!-- /counting-command -->` markers in the plan. kengaku has
   no marker or fence concept at all.
2. **Refusal.** kengaku's only static fence is a *path-shape* test on the last argv token
   (`/`, `\`, `..`, `<`, `>`, `:`) returning `out-of-scope` — a **skip**, not a defect (lines
   104-109). A command carrying an unbound `<placeholder>` or a `…` ellipsis is therefore scored
   `out-of-scope`, never `refused`. kaidoku parses the whole argv for `$VAR`/`<…>`/ellipsis and
   refuses with a named code (`PLACEHOLDER_UNBOUND`) and exit 3.
3. **Child environment.** kengaku calls
   `subprocess.run(argv, cwd=str(lane), capture_output=True, text=True, timeout=30)` — **no `env=`
   kwarg, so the ambient environment is inherited**. kaidoku passes a four-key env
   (`PATH HOME TMPDIR LANG`). This is the divergence that makes the two instruments grade
   different properties: kengaku grades *the printed count*, kaidoku additionally grades *the
   printed command's self-sufficiency*.
4. **Command grammar.** kengaku hard-requires `argv[0] == "grep"` and exactly one counted integer;
   kaidoku's grammar is a generic argv with an allow-listed script prefix
   (`SAFE_SCRIPT_PREFIX = "tools/round-76/"`), shell-metachar refusal and an allowed-var set.
5. **Shape.** kengaku is a *population* gate over all claims docs (counts `files/sections/commands/
   ok/out_of_scope/defects/errata`); kaidoku is a *three-arm battery* over two fixtures plus the
   plan (green / static refusal / execution refusal) with a `--control` set. kengaku has no
   fixture arms and no negative-arm taxonomy.
6. **Exit map.** kengaku 0/1/2. kaidoku 0/1/2/**3** (refused).

**No sibling reaches:** among the 87 lane instruments that spawn a subprocess, none treats a
*fenced block* as the unit of executability and none refuses an unbound placeholder before
execution. The closest same-round neighbour, `kama-shokunin/tools/round76-receipt-scope.py`
("fence-scoped citations and explicitly widened record paths"), binds citations inside a fence and
runs no printed command — its only `subprocess.run` re-spawns itself for the selftest
(`:229`).

---

## Q2 — `## Capabilities` atoms and SCORECARD-reading record audits

### 2.1 The searched command

```
grep -rn '## Capabilities' /home/vgpnk/Projects/shokunin --include='*.py'
```

616 matching lines; classified: 96 in lane instruments (20 files: 9 in `kaidoku-shokunin`, **11
sibling**), 520 in wave evidence (spec generators, mutants, frozen copies). All 11 sibling
instruments are listed below: seven ask a real question of the table (rows 1-7), one replays a
frozen assertion about the heading (row 8), and three mention it incidentally (row 9).

| lane / file | question it asks of `## Capabilities` | verdict |
|---|---|---|
| `kengaku-shokunin/plans/round68_capability_table.py` (189 lines, round 68 A3) | "does every capability the lane **declares** carry exactly one row with the declaring round in the first-working-round cell and an existing backticked evidence path?" Classes T1 no row / T2 wrong round / T3 absent or missing evidence path / T4 duplicate name; `MISMATCH n=` + `PREDICATE R68-A3 pass|fail`; exit 0/1/2; selftest s1–s5 (one red fixture per class + a compliant table). | **Duplication with named divergences** — closest sibling in the fleet |
| `mori-shokunin/tools/mori-register-check.py` (304 lines, round 59 C1) | "does the one self-declaring *active* register bind a required set of `MANIFEST.json` `rounds[i].capabilities_added[j]` keys, with a nonempty name equal to the MANIFEST string, a first-working-round cell equal to `lane_round`, and only lane-relative existing evidence pointers?" | **Duplication with named divergences** (population source differs: MANIFEST, not record prose) |
| `tameshi-shokunin/tools/selfstate-freshness.py` (1303 lines, round 75) | "is every **figure** a capability row declares still what the named instrument prints at the row's pinned revision?" Two row modes (`capability` exact-first-cell, `span` literal byte span), setup refusals instead of silent passes. | **Duplication with named divergences** (freshness of a figure vs membership of a claimed row) |
| `chousa-shokunin/tools/lane-preflight.py` — `G05 scorecard-paths` (function `g05`, lines 222-236) | "does every `corpus/ tools/ .ufo/` path in the **evidence cell** (third cell, `cells[2]`) of a capabilities row exist under the lane root?" Prints `GATE G05 … PASS|FAIL`, exit 0/1/2 via the preflight summary. | **Duplication with named divergences** (path existence only; no claim population, no description, no round cell, no fixture set) |
| `kama-shokunin/tools/round74-selfdesc-canon.py` (597 lines, round 74 C1) | "does the self-description canon resolve the newest capability repertoire whatever heading form it wears (bold / `##` / `###` demonstrated)?" Reuses a byte-frozen reconciler by import. | **Duplication with named divergences** (heading-form resolution; no claim→row binding) |
| `kama-shokunin/tools/round78-selfrecord-round77.py` (830 lines, F2) | Uses the newest `Capabilities — canonical list as of round <N>` table as one of six self-record facts. | **Duplication with named divergences** (the table is a graded fact, not a claim surface) |
| `tsukuroi-shokunin/tools/check-self-assessment.py` (1134 lines, K01–K27) | Requires a row to exist for each frozen `CAPABILITIES` name under the last `## Capabilities` heading; a miss is `CannotEvaluate` (exit 2), not a defect. | **Duplication with named divergences** — the miss class is *evaluation failure*, so it can never be a red verdict |
| `kengaku-shokunin/plans/state_check.py` (rounds 25-27) | Re-derives frozen P2a assertions: the fixed `## Capabilities` section exists with the frozen heading/table shape at a pinned base. | No overlap (frozen-assertion replay, not a row/claim check) |
| `kama-shokunin/tools/round48-append-audit-v3-check.py`, `kama tools/round75-interpretation-pins.py`, `kake scripts/doc_quote_truth.py` | `## Capabilities` appears only in a `HEAD_TITLES` carve-out set, a fixture string replacement, or a fixture table. | No overlap (incidental mention) |

### 2.2 Record-audit lineage (multi-atom audits with a validate block)

| lane / file | shape | verdict |
|---|---|---|
| `chousa-shokunin/tools/claims-audit{,-v2}.py` | rule-TSV driven: one row per checkable claims-file statement + a check class; `--selftest` 10 cases + `--selftest-fault N` forced-fault arm. **No `## Capabilities` rule class** (grep: 0 hits). | No overlap on the atom; **duplication of the audit frame** (rule population + per-row verdict + selftest-that-can-fail) with a divergence: population is hand-written TSV, not a fixed atom list derived from the record. |
| `kotodama-shokunin/reports/round-{27,28}/audit/x62-frozen-record-audit.py` | six duties over frozen generation dirs (MANIFEST, digests, receipt agreement). No `Capabilities` atom. | No overlap |
| `kaidoku-shokunin/tools/round-74/record-audit.py` → `round-76/record-audit.py` | D16–D23 → D16–**D24**, each atom one re-derivation, `--validate` on the receipt, `validate` block in the receipt. | lane-local predecessor, not a sibling |

**Named divergences — D24 `capability-row binding` vs `kengaku round68_capability_table.py`:**

1. **Population derivation.** kengaku's `DECLARED` is a **literal dict of four capabilities**
   (rounds 64-67) inside the tool. D24's population is **derived from the record**: every round
   section whose text says `Capabilities rows appended`, with the row names parsed out of that
   sentence. kengaku can answer "is my frozen list present"; it cannot answer "does the record's
   own claim hold", which is the round-75 defect class (the report says appended, the table stops
   at round 74).
2. **Checked cells.** kengaku checks name, first-round cell (`row[3]`), and a backticked path.
   D24 also requires a **non-empty description** and names the claiming round from the sentence.
3. **Evidence path grammar.** kengaku's `PATH_RE = (?:plans|corpus)/…` cannot express the
   `tools/` or `.ufo/` pointers the round-75 rows actually carry; chousa G05's `cap_pointers`
   accepts all three prefixes. D24 accepting the broader set is *narrower than chousa G05 and
   broader than kengaku* — a real, named divergence on both sides.
4. **Fixture count and shape.** kengaku s1–s5: one fixture per class plus a compliant table, all
   built by string `replace()` on a synthetic table. D24 declares six red fixtures (one per failure
   shape).
5. **Composition.** kengaku is a standalone predicate with its own exit and `MISMATCH n=`; D24 is
   **atom 24 of nine** inside a record audit whose receipt carries a `validate` block, so a single
   red fixture cannot be observed without the other 23 atoms staying green. No sibling record audit
   composes a capability atom at all.

---

## Q3 — `considerthese/` and `merge/kaidoku/`

### 3.1 `considerthese/`

```
for d in *-shokunin; do [ -d "$d/considerthese" ] || echo "absent: $d"; done
```

Absent in exactly four lanes: **`kaidoku-shokunin`, `kotodama-shokunin`, `souji-shokunin`,
`tabi-shokunin`**. Present in the other 17 (`audio, chousa, game-dev-2d, game-dev-3d, kagi, kake,
kama, kasegi, kengaku, kotoba, kumitate, lore, mado, mori, revenger, tameshi, tsukuroi`).

The lane's own record asserts the same absence repeatedly and by measurement — the last three
carrying statements are `LOG.md:3896`, `:3936`, `:3978` ("`considerthese/` absent (measured)"), and
`LOG.md:3864` records it as measured at a round start. **Confirmed: absent, and nothing in this
round's claims depends on it.**

### 3.2 `merge/kaidoku/`

There is **no `merge/` directory in the fleet root and none in the lane** (`kaidoku-shokunin/merge`
does not exist). The merge packages live in the staging campaign repo, outside the fleet:
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/` — members `MERGE-REPORT.md`, `MERGE-REPORT.json`,
`SOURCES.append.md`, `knowledge/`.

`MERGE-REPORT.md` headings, read only (as the assignment scopes), 6 of them:

```
# Merge package — kaidoku
## What gets appended to `corpus/SOURCES.md`
## Knowledge files to add
## Rows no entry rests on (status forced to `queued`)
## `used-by` pointers corrected at packaging time
## Adopt checklist
```

It is a **sources/knowledge adoption package**: staged registry rows, knowledge files, forced-status
rows, `used-by` corrections, and an adopt checklist. It contains **no capability-table surface and
no printed-command surface**, so it does not serve either of this round's claims. The lane's record
agrees it is out of play (`LOG.md:3896/3936/3978`: "Assimilation: none — shokuknow unreachable");
its last recorded adoptions from this package are the sasquatch/unblob slices at round 36
(`LOG.md:3122`, `:3132`) and round 43 (`LOG.md:3190`).

---

## Q4 — fleet census (`scripts/sources-census.sh`)

`scripts/sources-census.sh`, modes `census|validate|overdue|shared|selftest`, reads
`corpus/SOURCES.md` and parses `shokunin.conf` LANES rows textually. `Capabilities` mentions: **0**.
`counting-command`/`plan-command` mentions: **0**. Its validate codes are registry-shape only
(E01–E12 malformed/enum/date/used-by, W01–W04 warnings). **No relevant check** — the census cannot
see either of this round's surfaces, and it is not a place to add one (it is a separate instrument
with its own contract and selftest).

---

## Contradictions stated, not smoothed

1. **Token-level and semantic answers disagree.** The seat's assigned grep yields **one** instrument
   in the fleet (this round's). The semantic scan (fence + subprocess + shlex, then reading) yields
   **one same-class sibling** (`kengaku plans/correction_command_check.py`) that the assigned grep
   cannot see, because it writes the class as "counting command" in prose while its name is
   `correction_command_check`. Both facts are reported; neither is reduced to the other.
2. **`kengaku`'s gate would score this round's red fixture as a skip, not a refusal.**
   `plans/round-76/pre/fixtures/r75-printed.md` carries an abbreviated hash with a `…`; kengaku's
   `run_command` marks a non-`grep`/unparsable/out-of-scope command `out-of-scope` and prices it
   `SKIP`. That is not a defect in kengaku (its predicate is a count-of-`grep` gate); it means the
   two instruments cannot be substituted for one another, so R76-C2's `PLACEHOLDER_UNBOUND` arm is
   **not** already covered by any sibling's green.
3. **Broader and narrower than siblings at once.** D24's evidence-pointer acceptance is broader
   than kengaku's `(?:plans|corpus)` and narrower than chousa G05's `corpus|tools|.ufo` set. There
   is no single fleet convention for "what a capability evidence pointer may be"; this round must
   not claim one.
4. **mori and kengaku ask the same membership question from opposite sources.** mori binds
   `MANIFEST.json` → row; kengaku binds a frozen dict → row; neither binds a *record sentence* →
   row. The round-75 routed defect (a report sentence with no row) is invisible to both, which is
   consistent with the fact that it was found by a human spot-check, not by a sibling gate.

## Risks (for the L1, not acted on here)

- **A future fleet-wide dedup pass will mis-dedup on the token.** `counting-command` is a prose
  phrase in six lanes' `corpus/SOURCES.md` rows before it is an instrument name. Any dedup search
  must be semantic (fence + exec + counter reader), or it will either miss `kengaku` or claim a
  collision with prose.
- **`PLACEHOLDER_UNBOUND` is lane-local vocabulary** (every hit is inside `kaidoku-shokunin`; 9
  files at receipt generation, this seat's own findings file among them). If another lane later
  wants the same refusal it must route and choose its own name; the token carries no fleet-wide
  meaning yet, so nothing external validates the code word's semantics.
- **Do not absorb `kengaku`'s surface.** Its gate is a population gate over *all* claims docs with
  a `grep`-only grammar and an inherited child env; copying it into this lane would import an
  ambient-environment dependence this round's own instrument deliberately refuses. The divergence
  is the value; a merge would delete the property the claim is about.
- **`chousa G05` is a live consumer of the same table** and is red-capable on a `tools/` or `.ufo/`
  pointer. If D24's pointer rules ever tighten below G05's, the two instruments would disagree on
  the same bytes with no one owning the arbitration — that arbitration must be named before either
  gate is cited as fleet policy.
- **Scope:** `merge/kaidoku/` was read at its headings only, and only to answer "does it serve these
  claims" (it does not). Nothing was adopted, and no sibling row, instrument, or record was edited.

## Verification

- `ConnectorCross/receipt.json` — machine-generated: every search's exact `argv`, `cwd`, `rc`, raw
  hit list, the path-shape classification with per-lane membership, the fence+subprocess runner
  inventory, the census counts, the `considerthese` present/absent partition, the
  `shokuknow/merge/kaidoku` member list and its six headings, the four verdicts, and the lane HEAD.
- `ConnectorCross/scan.py` — the generator, shipped beside the receipt. One command reproduces it
  byte-identically modulo peer drift in wave paths:
  `cd kaidoku-shokunin && python3 -I -B .ufo/waves/round-76/w1/ConnectorCross/scan.py > .ufo/waves/round-76/w1/ConnectorCross/receipt.json`.
  It re-runs every search as a fixed argv list (never a shell for the greps), and writes only
  stdout.
- Counts that move between runs (`lesson`, `wave-evidence`, `PLACEHOLDER_UNBOUND` hits) move
  because peer seats are writing wave files while this seat reads; the receipt is the snapshot and
  the invariant classes are stated as invariants in the body.
- Read-only: no `git`/`jj` write, no commit, nothing written outside
  `.ufo/waves/round-76/w1/ConnectorCross*`; seat scratch removed before yield.
