#!/usr/bin/env python3
"""Generate the round-78 wave-1 spec (r78-w1): 12 seats, one v1 wave."""
import json
import pathlib

WAVE = "r78-w1"
REPORT_DIR = ".ufo/waves/round-78/w1"
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
Scratch: create ONE dir `/fast/scratch/hyaku/kaidoku-r78/<your-seat-name>/` (mkdir -p), pass it
explicitly (TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only git
(`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`, `merge-base`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all. Never edit production files:
the L1 lands every lane edit; you write only under your own evidence dir. Editing a lane file,
even to "fix" a defect you found, is a blocking defect of your seat.
Any git fixture repo you create is `D=$(mktemp -d)` under your scratch root and every later call
names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
commit, and never commit anywhere else.
Security (round-72 incident, QUALITY row 128): never write a raw environment dump or a config
file's secret values into the lane. A probe that must show an environment writes the KEY NAMES and
the canary presence only. For the client configs, record the `rea` entry's package pin, the
`disabledServers` presence and the file digest only - never an `env` block or a token.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task;
read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction of
any kind; use uv tool / npx / an official binary in ~/.local/bin. No system-wide upgrades.
Every `Report:` trailer path a validator renders is relative to
/home/vgpnk/Projects/shokunin/kaidoku-shokunin - write it at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/<that path>. Your final answer is a short JSON:
files_written, findings, evidence, risks.
"""

FROZEN = """## Frozen state (round 78)
base `6205ec8c575fb070243c0c40e34a2b0daacde46a` (the round-77 tip after the round-77
non-author spot-check, plus this round's commit of that wave's late `CriticClaims` evidence);
declaration `3e6b1efcad3a743913baa09f46427e5f8877a62b` (both instruments, `plans/round-78-claims.md`,
ten attack fixture trees and their generator, the census-start and three source snapshots);
freeze `ffcb47d13f0340f88397af6c8d2707a9554abab3` (`.ufo/waves/round-78/claims.json` with both
frozen predicates and instrument pins, the two selftest receipts, the base receipts and the three
controls; the round-29 gate audits it CLEAN with no findings).
Claims (frozen sentences in `plans/round-78-claims.md` and `.ufo/waves/round-78/claims.json`):
R78-C1 calibration - `tools/round-78/attack-gate.py --battery` materialises ten committed attack
  fixtures, measures that the frozen round-77 instruments ACCEPT each one (`base_accepted`,
  measured: 10 of 10), then applies the one declared rule per fixture that must refuse it
  (`refused`); the genuine control is the real record judged by every rule. Rules: receipt_auth,
  qualified_atom, near_miss_field, negated_verdict, value_mismatch, unbound_verdict, clean_run,
  filing_rev, gate_receipt_schema, gate_receipt_rev.
R78-C2 freshness - `tools/round-78/surface-recheck.py --battery` re-derives eight surface values
  from the live objects PROVINCE.md names. At base it reports `mismatches 2`: `jdk-version`
  (record `21.0.12.1`, live `21.0.13`) and `omp-rea-disable` (the record says the live OMP file
  no longer records the disable; the live file carries `disabledServers: ["rea"]`).
Round-77 routed defects under disposition (`.ufo/waves/round-77/w1/CriticClaims.md`,
`corpus/lessons/round-77-verifier-spotcheck.md` §6 and §8): §8 items 8-10 and §6 item 7 ride
R78-C1; §6 items 1-6 and §8 item 11 are record/prose repairs carried unclaimed; §8 item 12 is the
process duty (the inherited evidence is committed at the base commit).
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

ITEMS = [
    {
        "name": "ScoutRouted",
        "role": "scout",
        "task": """## Target
Map every round-77 routed defect to the artifact that closes it in round 78.
Read-only; write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScoutRouted/.

## Change
1. Read `.ufo/waves/round-77/w1/CriticClaims.md` (committed at the base) and
   `corpus/lessons/round-77-verifier-spotcheck.md` sections 6 and 8 in full. Enumerate every
   numbered item with its one-line claim.
2. For each item, name the round-78 artifact that closes it: a rule id in
   `tools/round-78/attack-gate.py`, a fixture under `.ufo/waves/round-78/attacks/`, a
   `tools/round-78/surface-recheck.py` check, or `record-only` (the record/report repair). Cite
   the file and line (`grep -n`).
3. Name every item that is NOT closed by either instrument and say why (record-only, or open).
4. Check the wave accounting claim yourself: `python3 -c` over
   `.ufo/waves/round-77/r77-w1-results.json` - count seats, seats with non-empty output, and
   compare with the round-77 report's sentence "10 seats returned evidence". Paste the numbers.

## Acceptance
Receipt JSON with `items` (id, claim, closed_by, pointer), `unclosed` and `wave_accounting`
(seats, nonempty, substantive_dirs, report_claim). Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScoutRouted.md.""",
    },
    {
        "name": "ConnectorSibling",
        "role": "connector",
        "task": """## Target
Cross-lane pattern finding, read-only: how do sibling lanes bind a receipt to the instrument that
produced it, and what does this lane's rule add or miss?
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ConnectorSibling/.

## Change
1. Read-only search sibling lanes for receipt-authentication patterns: grep for `instrument`,
   `sha256`, `rev` in `mado-shokunin/tools/`, `kagi-shokunin/tools/`, `kumitate-shokunin/tools/`,
   `tameshi-shokunin/tools/` (read-only; never write a sibling lane). Name at most four concrete
   precedents with file:line and quote the binding clause.
2. State the difference: what round 78's `receipt_auth` requires (40-hex rev, instrument path +
   sha256 re-derived from the blob at that rev, named receipt must resolve) and what a sibling
   does differently.
3. Name one attack the sibling pattern would catch that this lane's rule does not, or state that
   none was found and the search you ran.

## Acceptance
Receipt JSON with `precedents` (lane, path, line, quote), `difference`, `gap` (one item or
`none` + the search). Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ConnectorSibling.md.""",
    },
    {
        "name": "ExecAttackFixtures",
        "role": "executor",
        "task": """## Target
Independently reproduce the base arm: run the frozen round-77 instruments on all ten committed
fixtures and report each verdict with your own wrapper (do not import the gate).
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ExecAttackFixtures/.

## Change
1. Read `tools/round-78/attack-gate.py` `materialise()` and write your own materialiser in your
   scratch dir: copy `.ufo/waves/round-78/attacks/<fixture>/`, `git init`, commit with fixed
   dates, substitute `@HEAD@` in receipts, commit again, copy `tools/round-29/prefile-check.sh`
   in. Assert `git -C <dir> rev-parse --show-toplevel` equals your dir before each commit.
2. For the five record fixtures (a1-a6) run
   `python3 -I -B tools/round-77/verdict-bind.py --root <fixture> --rev HEAD --json-out <r>` and
   record exit, mismatch_count, defects. For the four receipt fixtures (b1-b4) run
   `python3 -I -B tools/round-77/prefile-receipt.py --root <fixture> --rev HEAD --work <w>
   --battery --json-out <r>` and record the `clone-run`, `record-receipt` and `gate-exits` arms.
3. Compare with the frozen `pre/c1-at-base.json` `base` fields. Name any fixture whose base
   observation does not reproduce (this falsifies the claim's base arm).
4. Delete your scratch tree last.

## Acceptance
Receipt JSON with `fixtures` (id, instrument, exit, mismatch_count or arms, reproduced bool) and
`disagreements`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ExecAttackFixtures.md.""",
    },
    {
        "name": "ExecSurfaceProbe",
        "role": "executor",
        "task": """## Target
Independently re-derive the eight surface values with your own commands and compare them to
`PROVINCE.md` at the base revision.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ExecSurfaceProbe/.

## Change
1. Read `PROVINCE.md` at `6205ec8c` with `git show 6205ec8c:PROVINCE.md` and extract the recorded
   values with your own patterns (three `rea` pins, the Ghidra `application.version`, the
   `GHIDRA_INSTALL_DIR` path, the JDK version, `JAVA_HOME`).
2. Derive the live values yourself, a different way than the instrument: `python3` to load the
   three client configs (json/tomllib) and print only the `rea` entry's package pin and, for OMP,
   `disabledServers`; `grep` the Ghidra `application.properties`; `java -version`; `grep` the
   `.bashrc` exports. Never print an `env` block or a token.
3. Report the exact drift: which values differ, the recorded value and the live value, with the
   command and its output line.
4. Say whether `tools/round-78/surface-recheck.py`'s `pre/c2-at-base.json` `mismatches 2` names the
   same two checks; name any check it misses.

## Acceptance
Receipt JSON with `recorded`, `live`, `mismatches` (check, recorded, live, command), `agreement`
with the instrument. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ExecSurfaceProbe.md.""",
    },
    {
        "name": "ReviewerC1",
        "role": "reviewer",
        "task": """## Target
Independent re-derivation of R78-C1 at the freeze.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ReviewerC1/.

## Change
1. Run the counting command yourself at the freeze rev:
   `python3 -I -B tools/round-78/attack-gate.py --root . --rev ffcb47d13f0340f88397af6c8d2707a9554abab3
   --work <scratch> --battery --json-out <receipt>` and paste the receipt's `fixtures_total`,
   `base_accepted`, `refused`, `validate`.
2. Re-derive each fixture's refusal from the fixture bytes: for each of the ten, name the rule
   that fires and the exact substring/path that triggers it (`grep -n` in the fixture). Any
   fixture refused by a rule other than its declared one is a finding.
3. Check the base arm yourself for at least four fixtures: run the frozen instrument named by the
   class and show the field that counts as accepted.
4. Attack over-tightening: construct (in scratch) a minimal record whose cell is correct and whose
   receipt is authenticated, and show the gate's `scan_record` reports no finding for it. Say what
   you had to include.

## Acceptance
Receipt JSON with `receipt` (counts), `per_fixture` (id, rule, trigger), `base_checks`,
`overtightening_probe`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ReviewerC1.md.""",
    },
    {
        "name": "ReviewerC2",
        "role": "reviewer",
        "task": """## Target
Independent re-derivation of R78-C2.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ReviewerC2/.

## Change
1. Run `python3 -I -B tools/round-78/surface-recheck.py --battery --root . --rev 6205ec8c575fb070243c0c40e34a2b0daacde46a
   --json-out <receipt>` and paste `checks_total`, `matched`, `mismatches`, `unparsed`, `validate`.
2. Re-derive the two mismatches from the live bytes yourself (a different command than the
   instrument) and state the exact recorded and live values.
3. Check the record's parse: for each of the eight checks, quote the recorded text the regex
   matched and the live line. Name any check whose recorded text does not actually state the value
   the parse claims.
4. Check the pointer rule: does the instrument compare the record's named path with the declared
   live source? Try a record copy whose Devin pointer names another file and show it refused.
5. State the receipt's `checked_at` and whether a live change after it would invalidate the claim.

## Acceptance
Receipt JSON with `receipt` (counts), `mismatches` (check, recorded, live, commands), `parse_quotes`,
`pointer_probe`, `checked_at`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ReviewerC2.md.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "task": """## Target
Falsify R78-C1 and R78-C2. Find a fixture the gate accepts, a genuine cell it refuses, or a rule
that is blind to a shape it names.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/CriticClaims/
(one directory per fixture-attempt, absolute paths).

## Change
1. C1: for each rule in `tools/round-78/attack-gate.py` (`receipt_auth`, `qualified_atom`,
   `near_miss_field`, `negated_verdict`, `value_mismatch`, `unbound_verdict`, `clean_run`,
   `filing_rev`, `gate_receipt_schema`, `gate_receipt_rev`), construct in scratch at least one
   shape the rule names but does not catch, or say why it cannot exist. Pay special attention to:
   a receipt whose `rev`+`instrument` are copied from a real receipt but whose counters are
   edited; a clause with a trailing comma or a backtick; a verdict group spanning a line break;
   `mismatches 0` (plural with a different count noun); a group with two receipts where the
   nearest is green.
2. C2: find a record wording that the parse accepts but that does not state the live value (e.g. a
   value in a historical sentence later superseded in the same file), or a live change the
   instrument cannot see.
3. Score every attempt: `accepted` (the gate passes a record it should refuse) or `refused`.
   Paste the command and the receipt field that decides it.

## Acceptance
Receipt JSON with `attempts` (claim, shape, command, verdict, evidence) and `falsified` (bool).
Report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/CriticClaims.md.""",
    },
    {
        "name": "MutGate",
        "role": "mutation-tester",
        "task": """## Target
Mutation-score `tools/round-78/attack-gate.py`: each mutant must be killed by a named case or
fixture; survivors are reported, never hidden.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/MutGate/.

## Change
1. Copy the instrument to scratch and apply at least eight single-point mutations, one per run:
   (a) `auth_findings` returns `[]`; (b) `QUALIFIED_ATOM_RE` matches nothing; (c) `NEAR_MISS_RE`
   matches nothing; (d) `NEGATION_RE` matches nothing; (e) `bind_clause` treats a defect status as
   a bound pass; (f) `judge_receipt_fixture` clean_run accepts `exit != 0`; (g) `filing_rev`
   drops the ancestor check; (h) `validate_receipt` skips the `refused-without-reason` guard.
2. For each mutant run the selftest and the battery over the ten fixtures and record which named
   case/fixture kills it (exit != 0 or the specific defect). A mutant killed by nothing is a
   survivor - report it with the run's output tail.
3. Record `sole` per mutant: whether exactly its declared detector failed.

## Acceptance
Receipt JSON with `mutants` (id, edit, killed_by, sole, survivor bool) and `survivors`.
Report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/MutGate.md.""",
    },
    {
        "name": "SentinelScope",
        "role": "sentinel",
        "task": """## Target
Security and scope review of the two instruments and the wave bounds.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/SentinelScope/.

## Change
1. Read `tools/round-78/surface-recheck.py` for credential exposure: does any code path write a
   config file's `env` block, a token, or a raw environment into a receipt? Trace `probe_live()`
   and the `recorded`/`live`/`texts` fields that reach the receipt. Name every field and its
   content class.
2. Check the receipt path containment: `--json-out` can be any path; does the instrument write
   outside the lane or the scratch? Does `attack-gate.py --work` accept a path outside the scratch
   and write there? Name the primitive and whether it is a defect.
3. Check `materialise()` for repo-escape: a fixture path with `..`, a symlink inside a fixture, a
   `git` invocation without `-C <fixture>`. Report what you find with a command.
4. Verify that neither instrument writes to `/tmp` when `TMPDIR`/`--work` point at the scratch:
   run each with `TMPDIR=<scratch>` and list any file written outside it (`find` evidence).

## Acceptance
Receipt JSON with `receipt_fields` (name, class safe|sensitive), `path_primitives` (name, defect
bool), `repo_escape`, `scratch_check`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/SentinelScope.md.""",
    },
    {
        "name": "ScribeSources",
        "role": "scribe",
        "task": """## Target
Draft the three round-78 SOURCES rows and the lesson `## Gate` block text; the L1 lands them.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScribeSources/.

## Change
1. The three snapshots are committed at `.ufo/waves/round-78/l1/sources/`
   (`stdtypes.html`, `tomllib.html`, `re.html`). For each, record the byte count, sha256, and a
   located quote with its `grep -n` line (a contiguous excerpt of at most 25 words).
2. Draft the three registry rows in the lane's 11-column schema
   (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`),
   ids S292/S293 (mined) and S294 (rejected). The rejected row carries its reason and flip
   condition. `used-by` lists exactly the admitted knowledge entry that cites the row.
3. Check the registry for id and URL collisions first: run
   `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u`
   and grep for the three URLs. Paste both outputs.
4. Draft the lesson Gate block: admit reasons for S292/S293 with the digest and the quote, the
   reject for S294, and the access date 2026-11-04.

## Acceptance
Files: `rows.md` (three rows verbatim, ready to append), `gate-block.md`, `shots.txt` (the
commands and outputs), `report.json`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScribeSources.md.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "task": """## Target
Draft the round-78 `## Mistakes` rows and the QUALITY criteria they ground; the L1 lands them.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScribeLesson/.

## Change
1. Read `.ufo/waves/round-77/w1/CriticClaims.md` section 1 and 2 and
   `tools/round-78/attack-gate.py` (`bind_clause`, `judge_group`, `auth_findings`). Identify the
   defect classes the round-77 instruments left open, and for each write a `## Mistakes` row in
   the lane's shape: class - evidence pointer - captured-by - fix. The row must name a rule that
   should have caught it and now does.
2. Write one QUALITY criterion (a numbered row in the lane's style) that states the general rule:
   an instrument that reports a clause status `defect` must collect it into the defect list it
   scores; a status that is computed and dropped is an over-set. Cite the round-77 code path
   (`tools/round-77/verdict-bind.py` `bind_cell`) and the round-78 fixture `a6-dropped-defect`.
3. Name one more criterion for the surface recheck: a record value that a *declared* regex parses
   from prose must state the live object's value, not a historical one (a superseded value in the
   same file is a trap). Cite `PROVINCE.md`'s history.
4. Format both ready to append; never rewrite filed bytes.

## Acceptance
Files: `mistakes.md` (rows), `quality.md` (two rows), `report.json`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/ScribeLesson.md.""",
    },
    {
        "name": "RevengerInstruments",
        "role": "revenger",
        "task": """## Target
Reverse-engineer, from committed bytes, what the two round-77 instruments actually do, and record
the acceptance table the round-78 gate's base arm depends on.
Write only under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/RevengerInstruments/.

## Change
1. Read `tools/round-77/verdict-bind.py` `bind_cell`/`audit`/`receipt_defects` and
   `tools/round-77/prefile-receipt.py` `battery`/`check_receipt` at the freeze. For each of the
   ten attack classes, name the exact code path that lets the fixture through (line numbers), and
   the condition under which it would refuse.
2. Verify your reading by executing the instruments on the fixtures (your own materialiser; the
   gate's `materialise()` is a readable reference). Report per-class `accepted` and the receipt
   field that proves it.
3. Reconstruct the two mutation survivors the round-77 closure routed (`c1-rev-show-to-worktree`,
   `c2-nonint-exit-accepted`): does the round-78 gate close either? Show the code path.
4. State what neither round-77 instrument nor the round-78 gate can see (the honest limit set).

## Acceptance
Receipt JSON with `classes` (id, code_path, would_refuse_if, accepted, evidence), `survivors`,
`limits`. Report at
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-78/w1/RevengerInstruments.md.""",
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
        "milestone": ("r78-w1: the attack gate and the surface recheck become runnable "
                      "instruments with measured base arms; independent re-derivation, "
                      "falsification, mutation scoring, security review, source rows and lesson "
                      "draft, and the round-77 routed-defect closure map."),
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
