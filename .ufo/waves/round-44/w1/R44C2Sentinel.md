# R44C2Sentinel — adversarial review of the R44-C2 rubric + counter (post-fix pass)

**Bottom line (final, counter `085192ea` + rubric `e8cc0ded`).** The pair is sound for the honest
case and the repair is exact: shipped base census exit 1 with exactly `[C2-a1, C2-a2, C2-a4]` and
`usable_as_claim_score false`; the bound SCORECARD block plus a C1-style README row (either row form)
gives exit 0, 80/80 evaluated, `claim_score true`, gate usable; a wrong-value note is refused; a
frozen-path edit gives exit 2 with the gate digest populated; the phantom-row escape fails; every
entry has a measured mutation witness that fails as required (80/80). No blocking and no
rubric-side finding remains. Two documented limits stay with the counter: the counter never reads
`pin` or `inventory` (so they document rather than bind), and a hand-written degenerate rubric still
scores green — only a strict script-pin mode closes that (both attributed counter-side).

Seat `R44C2Sentinel` (sentinel). Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; lane HEAD at
review close `9a8de923053978342fdba6ce047e1cca4eda9dd2`.
**Artifacts reviewed (final state):** counter
`.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py`, 1719 lines, sha256
`085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` (earlier passes at
`a6896459`/1636, `0bd4c882`/1452, `fda73a8e`/1378, `c80f2586`/1341, `10acbe47`); rubric
`.ufo/waves/round-44/w1/artifacts/R44C2Rubric/tools/round-44/c2-rubric.json`, 80 entries, sha256
`e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e` (earlier `a6ae1c1b`, `89dad28b`,
`048e9df6`, `2c67bb6a`); plus `dev-rubric.json`,
`dev-rubric-landing-{bound,unbound}.json`, the seat's receipts, its report
`.ufo/waves/round-44/w1/R44C2Counter.md`, `plans/round-44-claims.md` at `fc5eb54a`, and the C2
seat contracts in `.ufo/waves/round-44/w1-spec.json`.
Read-only: this seat wrote only this report and its probe scratch
(`/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel`, `probe-` prefix honored). No REA, no
network, no lane mutation, no C1 data procedure.

The counter was edited six times and the rubric four times during this review; one probe caught a
torn read (exit 2 `no_evaluable_entries` beside 80 evaluated entries) because the artifact was being
rewritten mid-run — re-probe against a committed sha, never a file being installed. Every finding
below was re-probed against the sha named with it; §Status records what each revision closed and what
it only narrowed.

## Measured ground truth (command A, frozen recipe, git objects only)

| rev | knowledge_files / mapped | citation_resolved_rules / rule_blocks | SCORECARD assertion for that rev |
|---|---|---|---|
| `c29360e3` (R44 base) | 137 / 137, `missing []`, `dangling []` | 21 / 21 | — (no pin) |
| `4d62ee5a` | 130 / 130 | 19 / 19 | `SCORECARD.md:23` "130/130 … command A at `4d62ee5a`" ✓ |
| `e1c83313` | 133 / 133 | 20 / 20 | `SCORECARD.md:23` "133/133 … at `e1c83313`" ✓; `:24` "20/20 … at `e1c83313`" ✓ |
| `8de80f1d` | 137 / 137 | 21 / 21 | `SCORECARD.md:3508` "`knowledge_files=137`, `mapped=137` … `citation_resolved_rules=21/21`" ✓ |

Every pinned value is **true at its own pin** and differs at REV. 12 sampled `## Capabilities`
evidence pointers all resolve at base (receipt R-05). Pointer existence is thus currently green
and uninformative (H2).

Peer records that bear on these findings (read, not re-derived here):
- `R44C2Readme.md` finds four genuine `corpus/README.md` mismatches (dangling `.ufo/waves/kaidoku-r5/05-riscv-deep.md`,
  a malformed date stem, a 4-cell lessons row, a phantom `lessons/round-13-distillation` entry) and
  reports the headline map count clean at base — so the honest stop does not fire and C2 continues,
  while the *headline* check (category b/f) is the one O1 must not score at REV.
- `R44CritC2.md` A2/F4 independently records the self-reference channel that O2 demonstrates
  end-to-end ("a check argv may read its command out of the file under test").

## Rubric review — landed, final shipped `a6ae1c1b` (80 entries, 10 dropped)

Read `.ufo/waves/round-44/w1/artifacts/R44C2Rubric/tools/round-44/c2-rubric.json` and ran it with
the frozen counter. Verified rather than taken on report:

| check | result |
|---|---|
| base census (`--pre-freeze --rev c29360e3`) | 80 entries, **80 evaluated, 3 mismatches, 0 unevaluable**, exit 1 (R-28) |
| the 3 mismatches | `C2-a1-owned-coverage-count` (`UNSUPPORTED:133/133` vs 137/137), `C2-a2-owned-depth-count` (`UNSUPPORTED:20/20` vs 21/21), `C2-a4-owned-depth-craft-range` (`UNSUPPORTED:81-449` vs 81-543) — a genuinely stale `## Owned axes` headline (the row was last refreshed at round 41; rounds 42–43 added four knowledge files and four rule blocks without refreshing it) |
| pinned entries derive at their own pins | `C2-b1` → 133/133 at `e1c83313`; `C2-b3` → 81-343 at `52b0eb29`; `C2-b4` → 81-449 — all match, none at REV (17 entries carry a pin) |
| bound repair applied in a scratch clone at base | 0 mismatches, 80 evaluated, exit 0, `met_target true` (R-29) |
| **wrong-value** correction note (137/137 → 999/999) | 1 mismatch, exit 1 (R-30) — "a note is never evidence" holds mechanically |
| claim mode, C2 repair only (counter+rubric committed at FREEZE) | exit 0, 80 evaluated, `claim_score true`, `met_target true`, `frozen_path_changed []` (R-32); identical at `a6896459` (R-35) |
| claim mode with a C1-style README row | exit 2 `frozen_path_changed ['corpus/README.md']` at both counters (R-33, R-36) |
| same landing with README dropped from `frozen_paths` | exit 0, 80 evaluated, 0 mismatches, `claim_score true` (R-39) — the remediation works |
| craft-range derivation | check rule = last **non-blank** line of the section (`SKILL.md:544-546` are blank) → 81-543 is correct by its own rule |
| inventory / categories | `inventory.ids` equals the entry-id set (as a set; other order); 6 `superseded` declared = 6 present; **24 of 80 entries carry no `category` field** (`C2-d3..d12`, `C2-e01..e14`) |

### R1 (blocking) — freezing `corpus/README.md` makes C2 unscorable at a REV that carries C1's landing

The rubric's `frozen_paths` is `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `SKILL.md`, with a
bound `expected_edit` only on `SCORECARD.md`. C1's landing must add a `corpus/README.md` map/index
row. Claim-mode simulation in a scratch clone (counter + rubric committed at FREEZE; REV = one C1
knowledge file + one README row + the C2 repair block): exit 2
`frozen_path_changed: ['corpus/README.md']`, while the C2 repair itself is accepted
(`SCORECARD.md … bound_edit_applied`, 8 appended lines) (R-33). Same run without the C1 row: exit
0, `claim_score true` (R-32). So the predicate is reachable in isolation and the cross-claim
dependency is the only thing that stops it.

**Smallest fix.** Drop `corpus/README.md` from C2's byte-frozen set and bind the README lines the
rubric actually cites with `preserve` digests (the entries already carry `line_sha256`); the three
README-derived entries derive at `HYAKU_FREEZE`, so C1's row cannot move their values. Alternatively
take C2's score at a REV that precedes C1's README landing and declare that order — weaker, and it
splits the round's measured revision.

### R2 (major, **closed at `e8cc0ded`**) — the predicate cannot distinguish a derivation from a hardcoded printer

**Closed rubric-side:** all 80 entries carry a measured witness and **80/80 fail as required**
(`fitness.not_demonstrated = []`). The last one was genuinely vacuous: `C2-c16`'s round-17 capability
row holds a command with an argument and a glob, so the pointer check saw no pointer; the check now
takes every word inside a backticked token, resolves a glob against the committed tree, and rejects
a pointer created after the base (`fabricated_pointer`). The counter-side caveat below stands.

A one-entry rubric whose command prints `{"observed": "137/137"}` without reading anything scores
`entries_evaluated 1, mismatches [], met_target true, exit 0` (R-31). The counter now verifies an
entry's declared `check_script_sha256` against the hashed inline payload (`script_pin_mismatch`), so
a *pinned* rubric is tamper-evident — but a pin proves the script text, not that the script derives.
The landed rubric answers this with a measured witness table: `fitness` reports 80 witnessed,
**79 fail as required**, and `C2-c16-cap-pointer` recorded as `STILL-GREEN` (its witness broke two
`SCORECARD.md:626` path tokens and the entry still resolved) — honest, but one entry is unproven.
`pin` is now consistent (commits for pinned clauses, the `HYAKU_FREEZE` sentinel for freeze-tree
entries) yet the counter still never reads it. **Remaining fix:** replace C2-c16's witness with one
that fails, and either add `{pin}` substitution to the counter or drop the field.

### R3 (minor) — `pin` is decorative at the counter level

Each pinned entry's script hardcodes its rev (`REV2='e1c83313'`), and the entry also carries
`pin: e1c83313`. The counter substitutes `{rev}`, `{freeze}`, `{repo}` but not `{pin}`, so an entry
whose `pin` and script disagree scores on the script and the field silently lies. **Fix:** add a
`{pin}` substitution and require pinned scripts to use it (or drop the field); then the pin is one
authority rather than two.

### R4 (minor, **closed at `e8cc0ded`**) — generated check scripts carried dead branches

Zero of the 80 scripts carry `2==1` any more (measured on the shipped file); the K_VALUE dispatch
leftovers are gone too. Closing nit only: the statement-pattern form is now generated per entry.

### R5 (minor) — `inventory` and `category` are reviewer aids, not bindings

### R6 (major) — the README entry check is silenced by a literal phrase

`C2-h2-readme-knowledge-entries-resolve` and `C2-h3-readme-lessons-entries-resolve` skip any table
row containing the text `not a corpus note` (`if 'not a corpus note' and 'not a corpus note' in l:
continue`). A row naming a file that does not exist, annotated with that phrase, is not reported:
probe with `` | `2099-01-01-bogus-phantom` (not a corpus note) | … | `` on the repaired tree → h2
stays green (the two mismatches in that run are the unrepaired `C2-a1` and a coverage-map row, R-38).
A free-text exemption is a laundering channel for exactly the class the claim measures. **Fix:** make
the exemption structural — the row must be a `lessons/` row (or name a path under `corpus/lessons/`),
not a sentence any row can carry.

### R7 (major) — `claim_gate.usable_as_claim_score` ignores the outcome

The gate is `claim_score AND rubric_source == 'freeze' AND both *_at_freeze digests non-null`
(`:1243-1248`). It does not include `exit_code`, `met_target` or `frozen_path_changed`. Measured: the
claim-mode run that exits **1** with one mismatch still reports `usable_as_claim_score: true`
(R-37). A reviewer trusting the gate can cite a failing run as a claim score. **Fix:** add
`exit_code == 0 and not frozen_path_changed and met_target` to the gate.

### R8 (minor) — the gate is built before the digests are known

`claim_gate` is constructed at result initialisation with `counter_sha256_at_freeze: None`
(`:1098-1104`) and patched only at `:1243`. Every early-return path (`freeze_not_ancestor`,
`frozen_path_changed`, `rubric_changed`) returns before the patch, so the receipt can show a
top-level `counter_sha256_at_freeze: a6896459…` beside `claim_gate.counter_sha256_at_freeze: None`
(observed on the exit-2 run, R-36). Conservative (never green) but self-contradictory. **Fix:** patch
the gate immediately after the digest assignment, before any early return, or compute it lazily at
exit.

### R9 (minor) — the README Knowledge row must use a bare stem

Inserting the C1-style row with the Coverage-map form `` `knowledge/2026-10-28-…` `` into the
`## Knowledge` table makes `C2-h2` report `UNSUPPORTED:dangling:knowledge/…` (R-40) because it
compares the backticked first cell with the bare file stem. The real landing must use the bare stem;
worth stating in the C1 landing recipe or normalising the leading `knowledge/` in the check.

Now closed on the rubric side: all 80 entries carry `category` (a 18, b 15, c 9, d 8, e 27, f 3) and
`inventory` carries `inventory_sha256` (recomputed over the sorted ids: match) plus `superseded_count
6`. The counter still never reads them, so they bind nothing at scoring time. **Remaining fix:**
have the counter refuse a rubric whose entry-id set differs from `inventory.ids`.

## Status against the v1 review

| finding | status (final sha `0bd4c882`) | evidence |
|---|---|---|
| B3 "a correction note repairs a mismatch" | **closed** | `supersession` path deleted; `score` repairs only via `repair_command` re-derivation (`:994-1015`); selftest arms `note_alone` 1, `note+re-derivation` 0 (R-10) |
| B5 "relaxation admits arbitrary in-place edits" | **closed** | `appended_text` requires the FREEZE blob as a prefix (`:461-468`); `append_text` byte-equality, `append` line identity, `preserve` digests; in-place edit → `not_append_only` (R-12); weak bindings rejected at parse (R-20) |
| B7 "no pre-freeze mode, CTL-C2-0 unevaluable" | **closed** | `--pre-freeze` with `claim_score: false`; declared-freeze equality skipped in census mode and recorded (R-21) |
| H1 "empty rubric is met" | **closed** | `entries_evaluated == 0` → exit 2 `no_evaluable_entries`; e2e probe exit 2 (R-19) |
| H4 "pinned-rev checks have no git objects" | **closed by design** | checks get `HYAKU_REPO` (a `git clone --shared`) and `HYAKU_REV`, so a pinned-rev derivation is possible (`:690-700`) |
| O4 added file under `frozen_dirs` | **closed at `fda73a8e`** | directory branch appends the path to `changed`; probe → `["tools/round-44/evil.py"]` (R-22) |
| O5 marker-only / empty `expected_edit` | **closed at `fda73a8e`** | parse-time `expected_edit_binds_no_content` → exit 2 (R-20) |
| O6 `--pre-freeze` + declared freeze | **closed at `fda73a8e`** | census runs, `declared_freeze` recorded, exit 1 with the mismatch (R-21) |
| O7 `--rubric` mints a claim score | **closed at `fda73a8e`; `claim_gate` in the json-out at `a6896459`** | `claim_score = (not pre_freeze) and rubric_source == 'freeze'`; `--rubric` run → exit 0 but `claim_score false` (R-23); the receipt now carries `claim_gate` with `usable_as_claim_score` — but the gate ignores the outcome (R7) and is stale on early returns (R8) |
| O2 self-reference, counter side | **visibility + inline script pin at `085192ea`** | argv naming the rubric is refused (`self_referential_check` → exit 2, R-25); a check reading the *asserting file* still scores met (R-24); receipts record `reads_subject`, subject sha256 at FREEZE/REV, `argv_digests`, `inline_payload`, and an entry may pin its inline script (`check_script_sha256`) which the counter verifies (`script_pin_mismatch` → exit 2) — drift control, not a derivation control |
| O3 check-script provenance | **visibility only at `0bd4c882`** | `check_scripts` records path-token scripts with scope and FREEZE/REV shas; an inline `-c` payload yields `check_scripts: []` (R-26); unfrozen scripts are labelled, not refused |
| O1 pin binding | **addressed by the rubric, verified** | 17 pinned entries derive at their own revs (133/133 at `e1c83313`, 81-343 at `52b0eb29`); residual R3 (the `pin` field is not counter-enforced) |
| O2 `asserted` provenance | **addressed for an honest author** | `line_sha256` on every entry; `asserted` = the derived value; a copied statement value yields `UNSUPPORTED:<value>`; wrong-value note → exit 1 (R-30); residual R2 (hardcoded check scores met, R-31) |
| O3 free-form check argv | **surfaced, not enforced** | `check_scripts` records path tokens; the counter reads neither `pin` nor `check_script_sha256`; residual R2 |
| **R1 README frozen vs C1's landing** | **closed** | rubric `89dad28b` drops README from `frozen_paths`; claim mode with a C1-style README row + the bound SCORECARD block → exit 0, 80 evaluated, `claim_score true` (R-39, re-verified at the landed rubric) |
| **R6 literal-phrase escape in the README checks** | **closed at rubric `a6ae1c1b`** | the exemption is structural (a `lessons/` name); a phantom row with the old phrase now reports `UNSUPPORTED:dangling:2099-01-01-bogus-phantom`, exit 1 (R-46) |
| **R9 `knowledge/`-prefixed Knowledge row** | **closed at rubric `a6ae1c1b`** | the check normalises a leading `knowledge/`; a prefixed C1 row is accepted, exit 0 (R-45) |
| **R7 gate ignores the outcome** | **closed at `085192ea`** | `usable_as_claim_score` now conjuncts `exit_code == EXIT_MET`, `met_target`, no `frozen_path_changed`, no `unevaluable` (`:1060-1069`); a failure run reports false |
| **R8 gate built before the digests** | **closed at `085192ea`** | every return path goes through one `finalize()`; the early-return receipt now carries the counter digest inside the gate too |
| B6 sibling attribution, H1–H3, H5, H6 | **open** | R2, R5 and the hardening list |

The seat's selftest is green on independent runs (R-10: 12 arms at `c80f2586`; R-27: 16 arms at
`0bd4c882`; R-47: 24 arms at `085192ea`), so the paths exercised below are the delivered ones.

---

# Findings — three open (O1–O3), four closed by fix (O4–O7)

Line references in O4–O7 are to `c80f2586`, the revision where each hole was demonstrated; the
closing change and its verification are named at the head of each section.

## O1 (blocking) — No pin binding: a **true** historical statement is scored as a mismatch, and the sanctioned repair rewrites it

The rubric schema has no `pin` field. A check is arbitrary argv evaluated against the REV export;
nothing requires it to read a pin out of the line it measures, and nothing forbids scoring a
pinned statement at REV.

**Exploit (measured, and already in the round's own reasoning).** `SCORECARD.md:23` says
"133/133 knowledge files mapped after the round-41 landing … command A at `e1c83313`". Measured:
133/133 **at `e1c83313`** (R-03) and 137/137 at REV (R-01). A rubric entry that runs command A at
REV reports a mismatch; the repair is an appended line carrying 137/137, which now contradicts the
`at e1c83313` qualifier inside the same cell — and the counter passes it. The seat's own dev-arm
report takes exactly this reading: "*`dev-scorecard-map-count` — `SCORECARD.md`'s coverage headline
claims 133 … `corpus/knowledge/*.md` holds 137 at the base. A real candidate for the frozen rubric
(category b), and a candidate C2 repair*" (`R44C2Counter.md`, "Lane dev-arm findings"). That
statement is true at its pin; treating it as a defect is the failure mode, not a probe artefact.
Same for depth: `:24` "20/20 … at `e1c83313`" → 20/20 at the pin, 21/21 at REV.

**Does the counter catch it?** No. It compares one observation to one transcribed `asserted` at
one revision.

**Smallest fix.** Entry field `pin` (`null` or a commit). The counter (i) extracts the qualifier
from the entry's cited line (`at\s+\`([0-9a-f]{7,40})\``) and refuses a disagreement (exit 2
`pin_disagrees_with_line`); (ii) for a pinned entry, materialises that rev (the counter already has
`HYAKU_REPO`) and requires the check to derive against it — a check that reads the REV export for a
pinned entry is exit 2; (iii) a REV-state entry is admissible only when the line carries no
qualifier; (iv) the appended block may not carry a value for a pinned entry (pinned history is
immutable; a supersession is a *new* dated statement with its own derivation).

## O2 (blocking) — `asserted` has no provenance, and a self-referential check scores the round met

`asserted` is a free transcription (schema `R44C2Rubric`: `{id, file, line_at_base, asserted, …}`);
the counter never relates it to the base blob. Combined with O3, the predicate is satisfiable
without doing the calibration work.

**Exploit A (measured end-to-end).** One entry, `command` = a Python one-liner that does
`'133/133' in Path('SCORECARD.md').read_text()`, `asserted = true`. Result: `entries_evaluated 1`,
`mismatches []`, `met_target true`, **exit 0** (receipt R-18). The check reads the file it asserts
about, so a corrupt-but-self-consistent file passes; the current count is 137.
**Exploit B (green without work).** Transcribe `asserted = "137/137"` for `SCORECARD.md:23`: the
REV observation matches, no mismatch, the frozen line still says 133/133.
**Exploit C (manufactured work).** Transcribe `asserted = "136/136"`: the base mismatch is
guaranteed, CTL-C2-0 is red by construction, and one bound append repairs it.

**Does the counter catch it?** No — there is no `line_at_base`, `line_sha256` or substring check
anywhere in `parse_rubric`/`score`.

**Partial mitigation at `0bd4c882`.** A check whose argv literally names the rubric
(`c2-rubric.json`, the rubric path, the `{rubric}` placeholder) is refused as
`self_referential_check` → exit 2 (R-25). The exploit above does not name the rubric — it reads
`SCORECARD.md`, the file whose statement it verifies — and at `0bd4c882` still scores
`met_target: true`, exit 0 (R-24), with `check_scripts: []`. The refusal therefore closes the narrow
circular case only; the provenance half (asserted bound to the cited base line, plus a per-entry
mutation control) remains the rubric-side fix.

**Smallest fix.** (i) Parse-time: `asserted` must be a byte substring of `blob(BASE, file)` at
`line_at_base`, and `line_sha256` must equal sha256 of that line; otherwise exit 2
(`asserted_not_in_base_line`). (ii) The census's `observed_at_base` is re-derived by the counter at
BASE and must equal the committed census value (drift is exit 2, not a mismatch). (iii) Rubric
contract: every entry declares `derivation` = the independent source of truth (e.g. "count of
`git ls-tree corpus/knowledge`" for a claim about counts) and the counter requires a per-entry
mutation control: in a scratch tree, mutate the *reality* side and require the check to flip
(`derivation_fails_mutation`). A check that cannot be made to fail is exit 2, not a pass. This is
the only defence against the always-true class.

## O3 (blocking) — Free-form `command`/`repair_command`: trivially green, and committed data is executed

`check.command` is arbitrary argv (`parse_rubric :370-401`; `run_entry :683-760`), executed with
`env = dict(os.environ)` (`:966-970`) and `cwd` = exported tree. No script pin, no allow-list, no
env scrub.

**Exploit 1 (always-true).** `{"command": ["sh","-c","echo 137/137"], "asserted": "137/137"}` —
schema-legal, green on every revision, no repo read (the O2 demo is the same class with a file
read).
**Exploit 2 (execution from frozen data).** A pre-freeze-corrupted rubric can run `git checkout`,
write inside the clone, or read absolute paths; `-I -B` on the counter does not constrain the
child. `repair_command` is a second such argv, so the "independent re-derivation" of B3 can itself
be a command that prints the asserted value.
**Exploit 3 (environment leakage).** HOME, proxy/credential variables and `HYAKU_*` are visible;
a check can be satisfied by bytes outside the scored tree. `HYAKU_REPO` also lets any check read
any revision (`git -C $HYAKU_REPO show <rev>:<path>`), so the *export* surface is not a
containment boundary — a trade-off the design should state, since that handle is what makes O1's
pinned checks possible.

**Does the counter catch it?** No.

**Smallest fix.** `command` becomes `{script: "tools/round-44/checks/<name>.py", script_sha256,
args:[…]}` with `script_sha256` frozen; execute `[sys.executable,"-I","-B",script,*args]`,
`shell=False`, a fixed minimal env (`PATH`, `HYAKU_*`, `TMPDIR` under `--work`; no HOME, no
proxy vars), args confined to the tree; require `repair_command` to satisfy the same constraint.
Document `HYAKU_REPO` as read-any-rev (not containment).

**Partial mitigation at `0bd4c882`.** Each entry record now carries `check_scripts`: the argv path
tokens ending in a known extension, with `scope` (`frozen`/`unfrozen` against the rubric's frozen
paths and dirs) and the sha256 at FREEZE and REV (R-24, R-26). Two limits: an inline `-c`/`sh -c`
payload yields `check_scripts: []`, so the record is blind to exactly the class that trivially
greens a check; and an unfrozen script is *labelled*, not refused. Treat `check_scripts` as audit
evidence, not as a control.

## O4 (closed at `fda73a8e`) — A file **added** under `frozen_dirs` was not `frozen_path_changed`

**Verified closed (R-22).** The directory branch now appends the added path to `changed`: probe
→ `{"frozen_path_changed": ["tools/round-44/evil.py"], "notes": [{"state": "added_under_frozen_dir"}]}`.
`tools/round-44/c2-rubric.json` and `tools/round-44/c2-counter.py` added after the freeze are
`added_after_freeze` → exit 2 for the same reason. Kept below as the record of the hole.

`freeze_integrity` `:520-523`: when the path has no blob at FREEZE it records
`{'state': 'added_under_frozen_dir'}` and `continue`s — it is not appended to `changed`.

**Exploit (measured, unit probe R-14).** Freeze a repo containing `tools/round-44/a.txt`; add
`tools/round-44/evil.py` and commit. `freeze_integrity(..., frozen_dirs=('tools/round-44',))`
returns `frozen_path_changed: []` with only the note above. The claim freezes `tools/round-44/*`
("all round-44 tools"), so a post-freeze tool/check/data file is an admitted freeze violation that
the receipt reports as clean. The seat's selftest arm tests a *changed* file, not an added one.

**Smallest fix.** In that branch, `changed.append(path)` as well (state `added_under_frozen_dir`);
add a selftest arm for the added case. (Deliberate over-strictness elsewhere — touched-and-restored
is `changed` — is correct and should stay.)

## O5 (closed at `fda73a8e`) — `expected_edit` marker-only and empty-`append` bound arbitrary appended content

**Verified closed (R-20).** A contentless binding is now rejected at parse time:
`{"marker": "M"}` → exit 2 `rubric_malformed: expected_edit_binds_no_content:SCORECARD.md`.
`marker`/`preserve` are additional conditions; the binding must carry `append_text` or a non-empty
`append`. Kept below as the record of the hole.

`verify_expected_edit` `:471-507`: `append_text` is byte-exact and `append` is line-exact, but if
only `marker` is given the function returns `bound_edit` after checking that the marker occurs
somewhere in the appended block; `{"append": []}` also returns `bound_edit`.

**Exploit (measured, unit probes R-11, R-13).**
- `{"marker": "Round-44 C2 correction"}` on `SCORECARD.md` + append
  `"Round-44 C2 correction: fabricated"` and `"### R43-C2 met"` → `bound_edit`, arbitrary content
  admitted. Variant B of my v1 demo, now at the appended-block level rather than in place.
- `{"append": []}` → `bound_edit` while binding nothing.
In-place edits and deletions remain blocked (prefix), so this is content-level fraud (a fabricated
verdict appended to a frozen file), not history rewriting.

**Smallest fix.** At parse time, any declared `expected_edit` must carry `append_text` (non-empty
string) or a non-empty `append` list; `marker`/`preserve` are *additional* conditions only. An edit
that binds nothing (`append: []`, marker-only) is exit 2 `expected_edit_binds_nothing`. Also report
the sha256 of the whole appended block in the receipt so the reviewer sees exactly what landed.

## O6 (closed at `fda73a8e`) — `--pre-freeze` could not score the frozen rubric: `rubric_freeze_mismatch`

**Verified closed (R-21).** With a rubric declaring the canonical freeze, `--pre-freeze` at BASE
now runs: `pre_freeze true, claim_score false, declared_freeze 3b0fcaa9…, entries_evaluated 1,
mismatches ['sanity'], exit 1`. The equality check still applies in claim mode. Kept below as the
record of the hole.

`score :876-883` enforces `rubric['freeze'] == freeze` unconditionally, and in pre-freeze mode
`freeze` is set to the measured rev (`:838-841`).

**Exploit / failure (measured, e2e R-15).** A rubric that names the round-44 freeze (the field the
claim needs) scored at BASE with `--pre-freeze` exits 2:
`rubric_freeze_mismatch: 3b0fcaa9… != c29360e3…`. So CTL-C2-0 ("the frozen rubric scored at the
BASE") is still unevaluable as specified; the only workaround is a rubric copy whose `freeze`
field is rewritten — i.e. the control scores a different rubric than the frozen one, which is
exactly the "loosening" the kill rule is meant to prevent. The seat's `pre-freeze-census` receipt
uses such a copy.

**Smallest fix.** In `--pre-freeze`, do not enforce declared-freeze equality. Record
`declared_freeze` and `declared_freeze_matches: false` in the receipt and continue; `claim_score`
already distinguishes a census from a score. Then CTL-C2-0 can score the frozen bytes.

## O7 (closed at `fda73a8e`) — `--rubric` minted a `claim_score: true` receipt without the rubric-freeze check

**Verified closed (R-23).** `claim_score = (not pre_freeze) and rubric_source == 'freeze'`; a
claim-mode run with `--rubric` now exits 0 with `claim_score false` and `rubric_source file`, so
the receipt cannot be cited as a claim. Kept below as the record of the hole.

`score :846-856, 890-900`: with `--rubric FILE`, `rubric_source = 'file'` and the
`if rubric_source == 'freeze'` byte comparison is skipped; `claim_score` is `not pre_freeze`, so a
claim score can be issued from an arbitrary (e.g. edited) rubric file.

**Exploit.** Edit the installed rubric's asserted values, score with `--rubric /tmp/edited.json
--rev <REV> --freeze <FREEZE>` → exit 0, `claim_score: true`, `rubric_sha256` of the edited file,
and no `frozen_path_changed`. The receipt records `rubric_source: "file"`, so it is auditable —
but nothing refuses it, and the L1 must know to reject it (my O2 demo receipt shows
`claim_score: true` with `rubric_source: "file"`, R-18).

**Smallest fix.** A claim score (`not pre_freeze`) requires `rubric_source == 'freeze'`, else exit
2 `claim_score_requires_frozen_rubric`; or split the switch: `--dev-arm` implies
`claim_score: false`. `--pre-freeze` may keep `--rubric`.

---

## Freeze-order and `claim_score` consequences (introduced at `fda73a8e`)

- **Hard dependency.** Because an addition under `frozen_dirs` is a change and the rubric and
  counter are auto-frozen, the L1 must commit `tools/round-44/c2-counter.py` **and**
  `tools/round-44/c2-rubric.json` **in the freeze commit**. Installing either afterwards makes
  every score exit 2 `added_after_freeze` — correct discipline, but unrecoverable without a new
  freeze, so the order must be asserted before the freeze commit is made.
- **`claim_score`, not `met_target`, is the gate.** A dev-arm or census run can exit 0 with
  `met_target: true` and `claim_score: false` (R-23). Any C2 score receipt the claim cites must
  show `claim_score: true`, `rubric_source: "freeze"`, and non-null `counter_sha256_at_freeze`
  and `rubric_sha256_at_freeze`. At `a6896459` the receipt carries `claim_gate` itself — but do not
  trust it: it is true on an exit-1 run (R7) and its counter digest is stale `None` on early-return
  receipts (R8). Until both are fixed, use `exit_code == 0 and met_target and not
  frozen_path_changed` alongside the gate.
- **Cross-claim.** `frozen_dirs: ["tools/round-44"]` makes C2 exit 2 if C1's landing adds any file
  there. The claims already require all round-44 tools in the freeze; the `## Separability`
  section should say so explicitly (the `R44RevKill` K1/S1 class, now with a mechanical trigger).

---

# Hardening

**H1 — inventory binding (rubric seat).** The counter now refuses an empty rubric, but not a
degenerate one. Freeze `inventory_sha256` over the census's sorted entry ids; the rubric must
contain exactly those ids; report `entries_count`, `superseded_count` and a per-category count. A
`superseded` entry needs a resolvable at-BASE reference or it is exit 2.

**H2 — pointer existence is not evidence.** 12/12 sampled capability pointers resolve at base, so
`test -e` is green now and green for a stub. Freeze the pointer's blob hash at BASE and report it;
a pointer created at REV is `fabricated_pointer` (exit 1), not a repair.

**H3 — self-reference discriminator.** The rule is "a second source of truth", not "reads a
file". `SCORECARD` "137/137" must be checked by counting `git ls-tree corpus/knowledge` and command
A's mapped-stem set — never by grepping SCORECARD/README. For SHONEN's "`PROVINCE.md:97-125`
byte-identical at `52b0eb29`" there is no second copy: freeze a reference blob hash and name the
other side, or drop the entry with a reason.

**H4 — category (e) receipt trust.** A cited receipt is committed JSON; editing `exit_code` 1→0
flips "not met" to agreement. Freeze every cited receipt blob and its counter blob; require the
receipt's `counter_sha256` to equal the frozen counter blob's hash.

**H5 — category (d) must be token-bound.** Keyword overlap is a green generator. The planned
(round 43) row promises a R42-C2 refreeze and a wave-2 attack; round 44 worked SquashFS v1/v2
(`SCORECARD.md:3498, :3507`). Score only `R{N+1}-C{k}` or an existing path/stem as a membership
test; prose plans are dropped with a reason.

**H6 — sibling attribution.** `mismatches` is a flat list: a partial C1 landing (file without its
index row → 138 files / 137 mapped) makes C2 unreachable, and the tempting repair is an append on
a surface C2 does not own. Record `mismatch_origin` (first commit introducing the state, or
`sibling:<claim>`) and report `mismatches_self` vs `mismatches_sibling`; the claim target is
`mismatches_self == 0`.

**H7 — receipt completeness.** Add `rubric_sha256_at_freeze`, `appended_block_sha256` per bound
file, `mismatches_self/sibling`, and `pin` per entry to the receipt. `counter_sha256_at_freeze` is
already present but is `null` when the counter is installed after the freeze (the seat discloses
this; installing counter+rubric in the freeze commit is the only admissible order).

---

# Freeze checklist (apply to the landed rubric + installed counter)

**Still open — the rubric seat + L1 must satisfy these:**

1. Every `asserted` is a byte substring of the cited base line; `line_sha256` matches, and the
   census's `observed_at_base` is reproduced by the counter at BASE (O2).
2. Every pinned statement carries `pin` extracted from its own line; pinned checks derive at the
   pin, not at REV; a REV-state entry carries no qualifier (O1).
3. `command`/`repair_command` are frozen scripts with `script_sha256`, a fixed minimal env,
   tree-contained args, and a per-entry mutation control that makes each check fail (O3, H1).
4. Category (e) entries freeze their cited receipt and its counter blob (H4); category (d) entries
   are token-bound (H5); the receipt carries `mismatch_origin`/`mismatches_self` (H6).

**Closed in the counter — verify the installed sha, do not re-litigate:**

5. `frozen_dirs` includes `tools/round-44`; counter + rubric are committed **in** the freeze
   commit (an addition afterwards is `added_after_freeze` → exit 2) (O4, R-22).
6. Every `expected_edit` carries `append_text` or a non-empty `append`; a contentless binding is
   rejected at parse (O5, R-20).
7. CTL-C2-0 runs with `--pre-freeze` and the **frozen** rubric: receipt shows `pre_freeze true`,
   `claim_score false`, `declared_freeze` (O6, R-21).
8. Every cited score receipt shows `claim_score true`, `rubric_source "freeze"`, non-null
   `counter_sha256_at_freeze` / `rubric_sha256_at_freeze`, **and `exit_code 0` with
   `frozen_path_changed []`** — the receipt's own `claim_gate` is true on a failing run (O7, R7, R8).
12. The README checks' `not a corpus note` exemption is replaced by a structural rule (R6), and the
    C1 landing row uses a bare stem, not `knowledge/…` (R9).
9. **`corpus/README.md` is not in C2's byte-frozen set** (or C2's score is taken before C1's README
   landing). Otherwise the round's measured REV gives exit 2 (R1, R-33).
10. Pinned entries use a `{pin}` substitution the counter can verify, or the field is dropped —
    one authority for the pin, not two (R3).
11. Every entry has a mutation witness: in a scratch tree its statement (and its derivation source)
    is mutated and the entry must report a mismatch (R2).

---

# Receipts

Commands run by seat `R44C2Sentinel`; `sha256_stdout` is the first 16 hex of the stdout sha256;
`exit` is semantic (0 clean, 1 not met, 2 could-not-evaluate). Counter sha
`c80f25866efb044a…` where a probe ran the artifact.

| id | command | exit | sha256_stdout | wall |
|---|---|---|---|---|
| R-01 | command A `--rev c29360e3` | 0 | `ae2fa5a4f6dd103b` | 0.10s |
| R-02 | command A `--rev 4d62ee5a` | 0 | `963a187dbd28e2a4` | 0.10s |
| R-03 | command A `--rev e1c83313` | 0 | `d70a5800cf6407f4` | 0.10s |
| R-04 | command A `--rev 8de80f1d` | 0 | `ae2fa5a4f6dd103b` | 0.10s |
| R-05 | 12 capability pointers, `git cat-file -e c29360e3:<p>` | 0 | `f4d3f1452008dd4f` | 0.02s |
| R-06 | v1 relaxation demo (suffix containment vs exact blob) | 0 | `6e6f326f0b3b97d6` | 0.02s |
| R-07 | `merge-base --is-ancestor 6b9e64fe f3f8db38` (round-43 base→freeze) | 0 | `01ba4719c80b6fe9` | 0.00s |
| R-08 | `merge-base --is-ancestor f3f8db38 6b9e64fe` (freeze→base) | 1 | `01ba4719c80b6fe9` | 0.00s |
| R-09 | lane HEAD at first review | 0 | `d72cc836adbe6e43` | 0.00s |
| R-10 | `c2-counter.py --selftest` (independent) | 0 | `94156c8ac1d77d30` | 0.39s |
| R-11 | unit: marker-only `expected_edit` + fabricated append | 0 | `0d65abce16e32b0f` | 0.03s |
| R-12 | unit: in-place edit under `append` binding | 0 | `e84ef0528cb2e850` (`not_append_only`) | 0.03s |
| R-13 | unit: `{"append": []}` binding | 0 | `38e4d1159a4457fd` | 0.03s |
| R-14 | unit: **added** file under `frozen_dirs` (v1 sha `c80f2586`) | 0 | `2cc33efe7fdebf09` | 0.04s |
| R-15 | e2e: `--pre-freeze` with rubric declaring the canonical freeze (v1 sha `c80f2586`) | 2 | `74773bada9747eb6` | 0.04s |
| R-18 | e2e: self-referential entry (grep SCORECARD for `133/133`) at `c80f2586` | 0 | `3be7eb0377a7564a` | 0.35s |
| R-19 | e2e: empty rubric at `c80f2586` | 2 | `46a29fd3dabd5ddd` | 0.33s |
| R-20 | e2e: marker-only `expected_edit` at `fda73a8e` | 2 | `a2cc1aebe947ff42` | 0.04s |
| R-21 | e2e: `--pre-freeze` + declared freeze + mismatching entry at `fda73a8e` | 1 | `1f3096e2a27a8b33` | 0.32s |
| R-22 | unit: **added** file under `frozen_dirs` at `fda73a8e` | 0 | `a86f320b99bbb61d` | 0.03s |
| R-23 | e2e: claim-mode run with `--rubric` at `fda73a8e` (exit 0, `claim_score false`) | 0 | `d202faf2fa7a9def` | 0.34s |
| R-24 | e2e: self-referential-to-SCORECARD entry at `0bd4c882` (my O2 exploit, still met) | 0 | `060e37f609c403d1` | 0.34s |
| R-25 | e2e: check reading the rubric itself at `0bd4c882` | 2 | `3296efc2a5433520` | 0.32s |
| R-26 | e2e: inline `-c` payload → `check_scripts: []` at `0bd4c882` | 0 | `060e37f609c403d1` | 0.34s |
| R-27 | `c2-counter.py --selftest` at `0bd4c882` (16 arms, independent) | 0 | `11bfa8531c94587d` | 0.47s |
| R-28 | rubric base census (80 entries, `--pre-freeze`) | 1 | `ef6f997a2aa34420` | 5.17s |
| R-29 | rubric after the bound repair block (scratch clone, pre-freeze) | 0 | `8d78a61e7caa0453` | 5.25s |
| R-30 | rubric with a **wrong-value** correction note (137/137 → 999/999) | 1 | `abd36745b6c7d389` | 5.41s |
| R-31 | one-entry rubric whose check prints the asserted value (no derivation) | 0 | `060e37f609c403d1` | 0.58s |
| R-32 | claim mode, C2 repair only (counter+rubric at FREEZE) | 0 | `7ee41dce6e14d126` | 5.45s |
| R-33 | claim mode, C2 repair **plus** C1's README landing | 2 | `41538aa5384e5da6` | 0.11s |
| R-34 | `c2-counter.py --selftest` at `a6896459` (20 arms, independent) | 0 | `efa6f811ea0bdc4e` | 1.46s |
| R-35 | claim mode at `a6896459` with the landed rubric, C2 repair only | 0 | `bfd563da1cee74d7` | 7.92s |
| R-36 | claim mode at `a6896459`, C2 repair + C1 README row (README still frozen) | 2 | `2b175d911d01e41b` | 0.12s |
| R-37 | gate on a failing run: exit 1, `usable_as_claim_score` still true | — | — (field read) | — |
| R-38 | bogus Knowledge row carrying `not a corpus note` (h2 stays green) | 1 | `a7c59cc44535b5e9` | 6.59s |
| R-39 | README dropped + realistic C1 landing row + C2 repair | 0 | `ffa2e9c016df8346` | 6.87s |
| R-40 | non-canonical `knowledge/…`-prefixed Knowledge row → h2 dangling | 1 | — (field read) | — |
| R-41 | final base census (counter `a6896459`) | 1 | `ef6f997a2aa34420` | 6.25s |
| R-42 | final claim mode: C1 landing + C2 repair (both artifacts at FREEZE) | 0 | `8c212d5d08df2e6f` | 6.82s |
| R-43 | final early-return receipt: post-freeze edit to `SHONEN.md` | 2 | `de55f68ee0a6913e` | 0.11s |
| R-44 | shipped rubric `a6ae1c1b` base census (counter `085192ea`) | 1 | `ef6f997a2aa34420` | 6.53s |
| R-45 | shipped rubric: C1 landing with `knowledge/`-prefixed row | 0 | `4e6d23b59423a613` | ~7s |
| R-46 | shipped rubric: phantom row with the old escape phrase | 1 | `d7897bf55f30d8e2` | ~7s |
| R-47 | `c2-counter.py --selftest` at `085192ea` (24 arms, independent) | 0 | `a5e942a1efa3172b` | 1.21s |
| R-48 | final base census (rubric `e8cc0ded`, counter `085192ea`) | 1 | `ef6f997a2aa34420` | 8.53s |

Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel/` (`cmdA.py`, `relax.py`,
`dirprobe2/`, `pre-rubric.json`, `selfref-rubric.json`, `empty-rubric.json`, `r-*.json`,
`receipts.tsv`).

# Residual risk

- Final state re-probed at counter `085192ea` + rubric `a6ae1c1b`: shipped base census exit 1 with
  exactly `[C2-a1, C2-a2, C2-a4]` and `usable_as_claim_score false` (R-44); a prefixed C1 row is
  accepted (R-45); the phantom row now fails (R-46); full landing exit 0 with gate usable (R-42); a
  frozen-path edit gives exit 2 with the gate digest populated (R-43). If another revision lands
  before the freeze, re-run R-42..R-46 and R-31 (hardcoded check) against the installed sha.
- Findings are about the **predicate as implemented**, not about the census's real mismatch count.
  Whether the honest stop fires is decided by the frozen rubric, which is another seat's artifact.
- Probes used a fabricated rubric and the lane's committed bytes only. No REA, no network, no
  fixture driver, no write to `tools/round-44/` or any fleet-root tracked file.
