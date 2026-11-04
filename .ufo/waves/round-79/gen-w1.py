#!/usr/bin/env python3
"""Generate the round-79 wave-1 spec (r79-w1): 12 seats, one v1 wave."""
import json
import pathlib

WAVE = "r79-w1"
REPORT_DIR = ".ufo/waves/round-79/w1"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in parallel. "
    "Do not output philosophical reasoning or verbose plans. Act directly via "
    "tool calls.\n\n")

BOUNDS = """## Bounds (read first)
Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Every path you write is absolute under
that lane; a write anywhere else is a defect (never write the fleet root, a sibling lane, or /tmp).
Work from /home/vgpnk/Projects/shokunin/kaidoku-shokunin; seat tools start at the fleet root, so
relative paths are wrong.
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r79/<your-seat-name>/` (mkdir -p), pass it
explicitly (TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-79/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only git
(`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`, `merge-base`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all. Never edit production files:
the L1 lands every lane edit; you write only under your own evidence dir. Editing a lane file,
even to "fix" a defect you found, is a blocking defect of your seat.
Any git fixture repo you create is `D=$(mktemp -d)` under your scratch root and every later call
names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
commit, and never commit anywhere else.
Security: never write a raw environment dump or a config file's secret values into the lane. A
probe that must show an environment writes the KEY NAMES and the canary presence only. For the
client configs, record only the package pin, the key names and the file digest - never an `env`
block or a token. A pointer binder must retain a pointed line's digest, never its bytes.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task;
read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction of
any kind; use uv tool / npx / an official binary in ~/.local/bin. No system-wide upgrades.
Every `Report:` trailer path a validator renders is relative to
/home/vgpnk/Projects/shokunin/kaidoku-shokunin - write it at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/<that path>. Your final answer is a short JSON:
files_written, findings, evidence, risks.
"""

FROZEN = """## Frozen state (round 79)
base `29d2ca30b83a6a0d85b0aa979de0138fde1660e6` (the round-78 tip after the round-78 non-author
spot-check); declaration `a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d` (both new instruments, the three
new selftest cases in tools/round-78/attack-gate.py, the PROVINCE.md pointer rebind,
plans/round-79-claims.md, the base receipts, the three selftests, the two controls, the
census-start and the two source snapshots); freeze `ed68cd0a6cc790cca342380a2d80d1927a668c8c`
(`.ufo/waves/round-79/claims.json` with both frozen predicates, kill rules and instrument pins;
the round-29 gate audits it CLEAN with no findings and three instrument paths,
`.ufo/waves/round-79/l1/scores/freeze-audit-at-freeze.json`).
Claims (frozen sentences in plans/round-79-claims.md and .ufo/waves/round-79/claims.json):
R79-C1 calibration - `tools/round-79/gate-mutation.py --battery --rev <rev>` applies eight exact
  single-occurrence edits to `tools/round-78/attack-gate.py` at that revision and requires each
  mutant's ONE declared selftest case to be present in the mutated copy's `--selftest` output and
  to FAIL there. An absent declared case is a survivor, never a pass. At base 29d2ca30 the battery
  reports mutants_total 8, killed 5, survivors 3 (`m03-near-miss-re-dead`,
  `m05-atom-absent-bound`, `m08-validate-no-refusal-guard`). At the freeze it reports
  mutants_total 8, killed 8, survivors 0, declared_case_hits 8, target_pin.matched true, pristine
  29 cases 0 failures; `m03`, `m05`, `m08` are each the sole failing case.
R79-C2 freshness - `tools/round-79/pointer-bind.py --battery --rev <rev>` binds PROVINCE.md's five
  drift-prone pointer cells (three REA pins, the Ghidra `application.version` line, the `.bashrc`
  export range) at the line/range they name and requires each declared token to occur there. At
  base it reports checks_total 5, matched 3, mismatches 2 (`omp-pin` record `:8` while the pin is
  at `:12`; `kimi-pin` record `:4126` while the pin is at `:4722`), and its `path-only` control
  reports mismatches 0 on the same record. At the freeze it reports checks_total 5, matched 5,
  mismatches 0, unparsed 0.
Round-78 population under disposition: the two wave mutation survivors (`m03`, `m08`) and the
uncovered atom-absent conjunct (`m05`) ride R79-C1; the round-78 non-author spot-check's routed
item 3 (stale line pointers, path-only rule) rides R79-C2 and item 4 (no self-test receipt at the
final instrument revision) is the unclaimed landing receipt `.ufo/waves/round-79/pre/selftest-gate.txt`;
spot-check items 1, 2, 5 and 6 are record/prose repairs carried unclaimed.
"""

ROLE_TEXT = {
    "scout": "Read-only reconnaissance. Name what the surface holds and what it misses; run the "
             "commands you cite.",
    "connector": "Cross-lane pattern finding, read-only across sibling lanes; absorb nothing.",
    "executor": "Write and run code fixtures under your own evidence dir; never edit a lane file.",
    "reviewer": "Independent re-derivation. Re-run the counter yourself and check the bytes.",
    "critic": "Adversarial falsification. Your job is to find the claim false or the counter blind.",
    "mutation-tester": "Mutate copies in scratch and show each mutant killed by a named case.",
    "sentinel": "Adversarial security and scope review of the instruments and the wave bounds.",
    "scribe": "Draft prose/registry rows under your own evidence dir; the L1 lands them.",
    "revenger": "Reverse-engineer the record's own behaviour and history from committed bytes.",
}

L1 = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

ITEMS = [
    {
        "name": "ScoutRouted",
        "role": "scout",
        "task": f"""## Target
Read-only recon of the round-79 instrument surface and the round-78 wave accounting.
Write only under {L1}/.ufo/waves/round-79/w1/ScoutRouted/.

## Change
1. Inventory the two round-79 instruments' CLI contracts from committed bytes at the freeze
   `ed68cd0a`: for each of `--battery`, `--selftest`, `--validate`, `--control`, name the argv,
   the exit contract and the receipt fields it writes (`grep -n` the `add_argument` block and the
   `main` exit paths). Do not run anything that writes outside your evidence dir.
2. Re-derive the round-78 wave accounting from `{L1}/.ufo/waves/round-78/r78-w1-results.json`:
   count seats, seats with non-empty output, seats whose evidence dir exists, and compare with
   the round-78 SCORECARD sentence "10 seats returned substantive evidence ... 1 returned a
   progress note only ... 1 returned a truncated final answer". Paste the numbers.
3. List, from `{L1}/.ufo/waves/round-79/claims.json`, every numeric clause each claim asserts and
   the receipt field that carries it; flag any clause with no receipt field.
4. Read `{L1}/.ufo/waves/round-79/l1/scores/freeze-audit-at-freeze.json` and quote the round-79
   entry (findings, instruments, verdict) verbatim.

## Acceptance
Receipt JSON with `cli` (per mode: argv, exit, fields), `wave_accounting` (seats, nonempty,
evidence_dirs, report_claim), `claim_fields`, `freeze_gate`. Report at
{L1}/.ufo/waves/round-79/w1/ScoutRouted.md.""",
    },
    {
        "name": "ConnectorSibling",
        "role": "connector",
        "task": f"""## Target
Cross-lane, read-only: does any sibling lane already implement a (a) selftest-mutation battery or
(b) line-bound pointer/source-position checker, and what does this lane's version add or miss?
Write only under {L1}/.ufo/waves/round-79/w1/ConnectorSibling/.

## Change
1. Search read-only across `/home/vgpnk/Projects/shokunin/*/tools/` and
   `/home/vgpnk/Projects/shokunin/*/scripts/` for mutation-testing and pointer/line-binding code
   (`grep -rlE 'mutant|survivor|mutation' ...`, `grep -rlE 'line_sha256|:line|line number' ...`).
   Never write a sibling lane; never run a sibling lane's gate.
2. Name at most four concrete precedents with file:line and quote the binding/clause text. For
   each, state whether it (i) counts an absent detector as a pass, (ii) treats a pointer's line or
   range, (iii) pins the mutated target by digest.
3. State one attack a sibling pattern would catch that round-79's instruments do not, or state
   that none was found and give the exact search command and its count.
4. Check `{L1}/corpus/SOURCES.md` for a row that already holds the POSIX grep page or the
   cargo-mutants book; name the id and line if present (this is the pre-append duplicate check, a
   referee for the source seat).

## Acceptance
Receipt JSON with `precedents` (lane, path, line, quote, properties), `gap` (one item or `none`
plus the command), `registry_hits` (ids or `none`). Report at
{L1}/.ufo/waves/round-79/w1/ConnectorSibling.md.""",
    },
    {
        "name": "ExecRebind",
        "role": "executor",
        "task": f"""## Target
Independent re-derivation of R79-C2 with your OWN script (never import
`tools/round-79/pointer-bind.py`; re-implement from the claim text).
Write only under {L1}/.ufo/waves/round-79/w1/ExecRebind/.

## Change
1. Write `rebind.py` under your evidence dir. It must read `PROVINCE.md` at a `--rev` (git show),
   extract the five pointer cells (three REA pins, the Ghidra `application.version` pointer, the
   `.bashrc` export range), then for each: resolve `~`, read the file, and report whether every
   declared token occurs on a line inside the declared 1-based line/range. Record the pointed
   lines' sha256 only.
2. Run it at base `29d2ca30` and at the freeze `ed68cd0a`. Report per check: pointer, line/range,
   token, matched, reason. The round-79 claim says base has exactly two mismatches (omp-pin,
   kimi-pin) and the freeze has zero.
3. Independently locate the live pin lines (`grep -n 'rea-agents@6.7.0'` in the three client
   configs) and state whether the record's line numbers agree. This is the fact the claim rests on.
4. Run your script's negative control: rewrite one pointer to `:1` in a scratch copy of the
   record and show your script reports a mismatch (a control that can fail).

## Acceptance
Receipt JSON with `per_rev` (rev, checks, matched, mismatches, mismatch_ids, reasons),
`live_pin_lines`, `negative_control`. Report at
{L1}/.ufo/waves/round-79/w1/ExecRebind.md.""",
    },
    {
        "name": "ExecBaseArm",
        "role": "executor",
        "task": f"""## Target
Independent re-derivation of R79-C1's base arm with your OWN mutant application (never import
`tools/round-79/gate-mutation.py`).
Write only under {L1}/.ufo/waves/round-79/w1/ExecBaseArm/.

## Change
1. Read the eight mutant definitions from `tools/round-79/gate-mutation.py`'s `MUTANTS` table at
   the freeze (`grep`/`python3 -c` the JSON-able fields; you may parse the file, not call it).
2. Write `mutate.py` under your evidence dir: for each mutant, write the base gate blob
   (`git show 29d2ca30:tools/round-78/attack-gate.py`) with that ONE exact edit applied into your
   scratch dir, run `python3 -I -B <copy> --selftest`, parse the case JSON lines, and report
   whether the mutant's declared case is present and failing.
3. Confirm at base: exactly three mutants survive (`m03`, `m05`, `m08`), the other five are killed,
   and each of the three survivors' declared cases is ABSENT from the base selftest's case list
   (not merely passing). Quote the base `SELFTEST cases=N failures=M` line.
4. Show one refusal control: apply a mutant anchor twice and show your applier refuses instead of
   applying it.

## Acceptance
Receipt JSON with `base` (mutants, killed ids, survivor ids, declared_case_absent ids, selftest
summary), `refusal_control`, `run_notes`. Report at
{L1}/.ufo/waves/round-79/w1/ExecBaseArm.md.""",
    },
    {
        "name": "ExecCaseInventory",
        "role": "executor",
        "task": f"""## Target
Case inventory across the two revisions: the three round-79 selftest cases in
`tools/round-78/attack-gate.py` must be ABSENT at base and PRESENT and passing at the freeze, and
the gate's selftest count must move 26 -> 29 with nothing else lost.
Write only under {L1}/.ufo/waves/round-79/w1/ExecCaseInventory/.

## Change
1. Extract the case-name list from `--selftest` output at base `29d2ca30` and at the freeze
   `ed68cd0a` (run the instrument at each `--rev` by `git show <rev>:tools/round-78/attack-gate.py`
   into your scratch dir, then run the copy; do not modify the lane).
2. Diff the two name lists: report `added`, `removed`, and the case/failure counts at each rev.
   The claim expects exactly three added (`red-near-miss-unparsed`, `red-atom-absent`,
   `red-validate-refused-no-reason`), none removed, 26 -> 29 cases, 0 failures at both.
3. For each of the three added cases, name the ONE code path it exercises (`judge_group`'s
   unparsable near-miss branch; `bind_clause`'s atom-absent return; `validate_receipt`'s
   refused-without-a-reason guard) with file:line at the freeze.
4. Check that no case name is duplicated in either list (`sort | uniq -d`).

## Acceptance
Receipt JSON with `base` and `freeze` (cases, failures, names_digest), `added`, `removed`,
`duplicates`, `case_to_path` (case, path, line). Report at
{L1}/.ufo/waves/round-79/w1/ExecCaseInventory.md.""",
    },
    {
        "name": "ReviewerC1",
        "role": "reviewer",
        "task": f"""## Target
Independent review of R79-C1: re-derive its counters from committed receipts and try to falsify
its clauses. Do not run a sibling lane's gate; do run the round-79 battery yourself in scratch.
Write only under {L1}/.ufo/waves/round-79/w1/ReviewerC1/.

## Change
1. Read `{L1}/.ufo/waves/round-79/claims.json` R79-C1 and
   `{L1}/.ufo/waves/round-79/l1/scores/c1-at-landing.json`; re-derive every numeric clause
   (`mutants_total`, `killed`, `survivors`, `declared_case_hits`, `target_pin`, pristine counts)
   from the receipt's own mutant list. Report any clause the receipt does not carry.
2. Digest bind: `git show ed68cd0a:tools/round-78/attack-gate.py | sha256sum` and
   `git show ed68cd0a:tools/round-79/gate-mutation.py | sha256sum`; compare with the receipt's
   `target.sha256`/`target_pin.expected` and the claims.json pins.
3. Attack the counter with at least three forgeries of your own (a receipt file you write in
   scratch): (a) `killed true` with the declared case absent; (b) `mutants_total 8` with 7
   entries; (c) `survivors 0` while `survivor_ids` names one. Run
   `python3 -I -B tools/round-79/gate-mutation.py --validate <forged>` and paste the defects.
4. Check `m03`/`m05`/`m08` are each the sole failing case in the landing receipt (`detector_count
   1`, `sole_detector true`) and say whether that is what the claim asserts.

## Acceptance
Receipt JSON with `clauses` (name, value, rederived, ok), `digest_bind`, `forgeries` (shape,
defects), `sole_detectors`. Report at {L1}/.ufo/waves/round-79/w1/ReviewerC1.md.""",
    },
    {
        "name": "ReviewerC2",
        "role": "reviewer",
        "task": f"""## Target
Independent review of R79-C2: re-derive its counters and attack the binder's line/range semantics.
Write only under {L1}/.ufo/waves/round-79/w1/ReviewerC2/.

## Change
1. Read R79-C2 in `{L1}/.ufo/waves/round-79/claims.json` and
   `{L1}/.ufo/waves/round-79/l1/scores/c2-at-landing.json`; re-derive `checks_total`, `matched`,
   `mismatches`, `unparsed` from the check list.
2. Attack with synthetic fixtures (write them in scratch, do not edit the lane): (a) a pointer at
   line 0 or a backwards range; (b) a range whose second line carries the token but whose first
   does not; (c) a pointer past EOF; (d) a token that appears elsewhere in the file but not on the
   pointed line; (e) a record cell with no `:line`. For each, state what the frozen claim's rule
   requires and what the committed instrument does — import it as a module or run `--selftest` to
   compare (do not edit it).
3. Verify the receipt retains line digests only: `python3 -c` over the landing receipt, listing
   every field per check; confirm no client-config line bytes or env values are present.
4. Re-run the `path-only` control at the freeze and state whether it now also reports 0 (it must:
   a control that cannot fail). Explain why that does not make the line-bound claim vacuous.

## Acceptance
Receipt JSON with `counts`, `fixtures` (shape, expected, observed, ok), `digest_only`,
`path_only_control`. Report at {L1}/.ufo/waves/round-79/w1/ReviewerC2.md.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "task": f"""## Target
Falsify the CLAIMS' SHAPE, not their arithmetic: §9 sizing, axis naming, causal separability, and
whether a do-nothing control reaches either target.
Write only under {L1}/.ufo/waves/round-79/w1/CriticClaims/.

## Change
1. Read `{L1}/plans/round-79-claims.md`, `{L1}/.ufo/waves/round-79/claims.json` and the round-78
   section of `{L1}/SCORECARD.md`. Decide each question and give evidence:
   - Is R79-C2 a re-score of a rule the lane already holds (round-78's freshness recheck) rather
     than a new surface? Name the surface it moves and the command that would show it unmoved.
   - Does R79-C1's `sole_detector` clause actually bind what the claim says (case independence)?
   - Are the two claims causally separable (neither counter reads the other's receipt)?
   - Does the base arm separately measure a do-nothing control for each claim, and can either
     control meet the target (`pre/c1-at-base.json`, `pre/controls/c1-empty-set.json`,
     `pre/controls/c2-path-only.json`)?
   - Is the lowest-axis obligation met (C1 on a tied-lowest axis) and is the nudge waiver
     correctly not claimed?
2. Try to construct ONE receipt that passes both counters while doing no real work; if you cannot,
   name the clause that blocks it.
3. Name the weakest clause in each claim and a concrete next-round hardening.

## Acceptance
Receipt JSON with `questions` (question, verdict, evidence), `both_pass_forgery` (or the blocking
clause), `weakest_clauses`. Report at {L1}/.ufo/waves/round-79/w1/CriticClaims.md.""",
    },
    {
        "name": "MutInstruments",
        "role": "mutation-tester",
        "task": f"""## Target
Mutation-test the two round-79 instruments' own selftests: find conjuncts no selftest case kills.
Write only under {L1}/.ufo/waves/round-79/w1/MutInstruments/.

## Change
1. Copy `tools/round-79/pointer-bind.py` and `tools/round-79/gate-mutation.py` at the freeze into
   your scratch dir (do not edit the lane). Write at least six mutants total, each ONE edit:
   pointer-bind - (a) `matched` true whenever the path exists (the path-only rule); (b) line
   treated as 0-based; (c) range compared as its first line only; (d) the `unparsed` flag never
   set; gate-mutation - (e) an absent declared case counted as killed; (f) `--validate` skips the
   "killed without its declared case failing" guard.
2. For each mutant, run the instrument's `--selftest` on the mutated copy and report: exit,
   failing cases, whether it is killed, and which case kills it. Name any survivor.
3. For every survivor, name the missing case that would kill it (one sentence) — do not write it
   into the lane; the L1 routes it.
4. State the pristine selftest summary for both instruments at the freeze.

## Acceptance
Receipt JSON with `mutants` (id, instrument, edit, killed, killed_by, failing_cases),
`survivors`, `missing_cases`, `pristine`. Report at
{L1}/.ufo/waves/round-79/w1/MutInstruments.md.""",
    },
    {
        "name": "SentinelScope",
        "role": "sentinel",
        "task": f"""## Target
Adversarial security and scope review of the round-79 instruments, receipts and wave bounds.
Write only under {L1}/.ufo/waves/round-79/w1/SentinelScope/.

## Change
1. Secret-exposure review: enumerate every field the two instruments write into receipts
   (`grep -n 'json.dump\\|receipt\\['` in both). For each field, state whether it can carry a
   client-config line's content, an env value or a credential; the pointer binder must retain only
   a pointed line's sha256 and the record's own pointer cell.
2. Path/scope review: where do the instruments write (`--json-out`, `--work`, temp dirs)? Can a
   caller make them write outside the lane root, into the fleet root, `/tmp` or a sibling lane
   (e.g. `--work /home/vgpnk/Projects/shokunin`)? Show the code path with file:line and whether a
   guard exists.
3. Scratch hygiene: `gate-mutation.py --battery` creates a `tempfile.mkdtemp` under `--work`; does
   it ever remove it? Name the consequence and whether the round is affected (the driver's reaper
   and the lane's landing cleanup).
4. Child environment: what environment do the mutated copies run under
   (`run_selftest`'s `env`)? Name the keys and whether the canary/secret keys are excluded.
5. Check the wave bounds in `{L1}/.ufo/waves/round-79/r79-w1-spec.json`: every seat writes only
   under the lane, every prompt names the scratch root, no seat is told to commit.

## Acceptance
Receipt JSON with `receipt_fields` (field, can_carry_secret, guard), `paths` (writer, escapable,
guard), `scratch`, `child_env`, `wave_bounds`. Report at
{L1}/.ufo/waves/round-79/w1/SentinelScope.md.""",
    },
    {
        "name": "ScribeSources",
        "role": "scribe",
        "task": f"""## Target
Draft the round-79 `## Gate` block rows for `corpus/SOURCES.md` from sources you open yourself.
Write only under {L1}/.ufo/waves/round-79/w1/ScribeSources/.

## Change
1. Open BOTH pages with one GET each and save the snapshots under your evidence dir:
   `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html` and
   `https://mutants.rs/`. Record HTTP status, byte count and sha256 for each.
2. Locate a literal contiguous quote of at most 25 words that grounds the decision it is cited
   for, with its section heading and snapshot line:
   - POSIX grep `-n`: the line-number semantics the pointer binder relies on (1-based numbering of
     each file's lines).
   - cargo-mutants welcome page: the mutation-testing vocabulary the battery relies on (a bug
     inserted in the source that no test failure catches = a surviving mutant).
   Count the words yourself and paste the count.
3. Pre-append duplicate check: `grep -n` `corpus/SOURCES.md` for both URLs and for the hosts
   `pubs.opengroup.org` and `mutants.rs`. A URL already held is a refused reuse, not a row.
4. Draft two 11-column registry rows in the fleet schema
   (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`),
   ids as `S295`, `S296` only if the registry's highest id is below them — check
   `grep -oE 'S[0-9]{3,}' corpus/SOURCES.md | sort -u | tail -3` and report the actual next ids.
   No cell may contain a literal or escaped `|`. Draft only; the L1 appends.
5. Draft the Gate-block table lines (source, URL, accessed, quote with location, digestion).

## Acceptance
Receipt JSON with `snapshots` (url, status, bytes, sha256), `quotes` (text, words, location),
`duplicate_check`, `next_ids`, `rows_draft` (markdown), `gate_block_draft`. Report at
{L1}/.ufo/waves/round-79/w1/ScribeSources.md.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "task": f"""## Target
Draft `corpus/lessons/round-79.md`'s `## Mistakes` rows and the QUALITY.md rows from committed
evidence; draft only, the L1 lands them.
Write only under {L1}/.ufo/waves/round-79/w1/ScribeLesson/.

## Change
1. Read `{L1}/corpus/lessons/round-78-verifier-spotcheck.md` §3, §4 and §6 and the round-78
   lesson `{L1}/corpus/lessons/round-78.md`. For each of the six routed items, name whether
   round 79 closes it, where (claim, receipt, or record edit), and what a mistake row would say.
2. Read `{L1}/tools/round-79/gate-mutation.py` and `{L1}/tools/round-79/pointer-bind.py`. Name at
   least two mistake-class candidates the instruments' own design exposes, each with class,
   evidence pointer (`path:line`), captured-by (a QUALITY row or protocol rule) and a fix that a
   test would show able to fail. Candidates to weigh: the round-78 survivor itself ("a detector
   that does not exist counted as a pass"); a control that cannot fail (path-only); a pointer
   compared by path; a receipt field that carries line bytes rather than a digest.
3. Draft 3-5 `## Mistakes` table rows in the fleet shape (class · evidence · captured-by · fix)
   and 2-3 `QUALITY.md` rows (`#N` numbering: read the current highest id first; do not reuse).
4. State the coverage-map consequence: if the L1 lands one knowledge entry, the
   `tools/round-66/coverage-selfcheck.py --selfcheck` denominator moves 157 -> 158 and the map
   needs one row; name the row text you would add.

## Acceptance
Receipt JSON with `routed_items` (item, closed_by, pointer), `mistakes` (rows), `quality_rows`,
`coverage_map_note`. Report at {L1}/.ufo/waves/round-79/w1/ScribeLesson.md.""",
    },
]


def main() -> None:
    items = []
    for item in ITEMS:
        items.append({
            "name": item["name"],
            "role": item["role"],
            "prompt": (GODSPEED + BOUNDS + FROZEN
                       + f"## Role\n{ROLE_TEXT[item['role']]}\n\n"
                       + item["task"]),
        })
    spec = {
        "wave": WAVE,
        "milestone": ("r79-w1: the selftest mutation battery and the line-bound pointer binder "
                      "are frozen with measured base arms and attacked from six directions; "
                      "independent re-derivation, falsification, instrument mutation, security "
                      "review, source rows and lesson draft."),
        "reportDir": REPORT_DIR,
        "context": FROZEN + "\n" + BOUNDS,
        "items": items,
    }
    out = pathlib.Path(__file__).with_name(f"{WAVE}-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(json.dumps({"spec": str(out), "items": len(items),
                      "roles": sorted({i["role"] for i in items})}))


if __name__ == "__main__":
    main()
