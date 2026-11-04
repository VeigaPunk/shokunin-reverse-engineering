#!/usr/bin/env python3
"""Generate the kaidoku round-71 wave-1 spec (one v1 build+attack wave, 16 seats).

Roles: 5 executor, 2 reviewer, 1 critic, 2 mutation-tester, 1 sentinel,
1 scout, 1 connector, 2 scribe (16 seats) — attack share 6/16 = 37.5%
(reviewer x2, critic, mutation-tester x2, sentinel), one connector seat. The L1
holds the canonical planner seat (the validator rejects a planner role). Routing
is the host's task.agentModelOverrides; no model is passed anywhere.

Usage: gen-w1.py <freeze-commit-hash>
"""
import json
import pathlib
import re
import sys

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-71/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r71'
PLAN = LANE + '/plans/round-71-claims.md'
CLAIMS = LANE + '/.ufo/waves/round-71/claims.json'
BASE = '82c8e620c9222fb218aa0260570a3765da2afb44'
DECL = '329208cf4a234aac391b7f02b50769c5920f1beb'
FREEZE = sys.argv[1] if len(sys.argv) > 1 else 'FREEZE_HASH_PLACEHOLDER'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
R69RECEIPT = LANE + '/.ufo/waves/round-69/l1/scores/c3-at-landing.json'
R70LAND = LANE + '/.ufo/waves/round-70/l1/scores/c3-at-landing.json'
R70BAT = LANE + '/.ufo/waves/round-70/l1/scores/c1-at-landing.json'
SPOTCHECK = LANE + '/corpus/lessons/round-70-verifier-spotcheck.md'
FIRSTCUT = '4737a542ae3b1b910d8fe43efbd572bc578b07c6'
SUPERSEDED = '7c155617bb42dadf1725b88a06fe3f235c364f0a'

COMMON = f"""Bounds (binding, from the lane round contract):
- Your write scope is your own findings directory {W1}/<YourSeat>/ and your scratch root
  {SCRATCH}/<YourSeat>/ (create both with mkdir -p; everything else in the lane tree and the
  fleet root is READ-ONLY for you). Never touch .ufo/state/, .ufo/watchdog.log, MANIFEST.json,
  any sibling lane repo, or any file you did not author. Never run a mutating git/jj command
  anywhere; seats never commit and never push.
- The instruments under test are FROZEN bytes at the freeze commit {FREEZE} (pins in {CLAIMS});
  read them from the tree or via `git -C {LANE} show {FREEZE}:<path>` — never edit them. Findings
  go in your report files, never in repairs you land yourself.
- Scratch discipline: keep every clone, fixture and work tree under your scratch root; remove it
  before you finish (`trap 'rm -rf -- "$S"' EXIT` / `finally: shutil.rmtree`), receipts first
  copied into your findings dir. `/tmp` is for files under 50 MB only and is never citable
  evidence. No hardcoded /tmp in anything you leave behind.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task;
  first read /home/vgpnk/.omp/agent/RULES.md (official channels only; record tool/version/channel/reason
  in your findings). pacman is PAUSED host-wide: never run pacman install/upgrade/-Sy/-Syu/-U/-R,
  never restart a host service; install via uv tool / npx / an official binary in ~/.local/bin.
- Every `Report:` trailer path you may see is relative to {LANE} — write it at
  {LANE}/<that path> in your own findings dir naming, not at the fleet root.
- End your output with a one-line `VERDICT:` naming what you observed (met / not-met / defect
  named), so the L1 can integrate without re-reading your whole transcript."""

CONTEXT = f"""# Target
kaidoku-shokunin round 71, attempt 1, wave w1 = the single v1 build+attack wave (16 seats; policy
band 8-16; attack seats reviewer x2, critic, mutation-tester x2, sentinel = 6 of 16 = 37.5%; one
connector). Base {BASE} (the round-70 lane tip: report, close, non-author spot-check); declaration
{DECL} (five instruments under tools/round-71, the claims plan, the census-start receipt); operative
freeze {FREEZE} (the commit that first adds the claims container; round-29 gate preflight CLEAN).
Three declared claims on three distinct axes (plan {PLAN}; container {CLAIMS}):
- R71-C1 (coverage, capability acquisition; Frontier -> Core) — the seam's runtime evidence class:
  tools/round-71/packed-elf.py routes every child (packer, REA node, readelf, git) through the
  four-key allowlist and records the OBSERVED child environment via --child-env-log; the receipt
  carries run_root, child_env_observed, run_nonce and run_binding (--challenge/--nonce-commitment);
  tools/round-71/seam-probe.py adds A8_child_env_observed, A9_concurrent_collision and
  A10_run_binding — 10 of 10 at the measured revision, 7 of 10 at the round-70 landing 7c155617.
- R71-C2 (calibration, capability acquisition) — the six lying-field shapes (unpacked_counts,
  packed_sha256, section_count/upx_list_rc, runs argv, refusal, format) enter the frozen battery:
  tools/round-71/forged-receipts.py cuts them from the round-70 landing receipt, relabels them to
  the round-70 FIRST-CUT world {FIRSTCUT}, and requires first_cut_rc 0 and superseded_rc 1 (clause at
  {SUPERSEDED}); 18 forged rows total (10 base-world + 6 lying + 2 landing-world).
- R71-C3 (operability, capability acquisition) — the registry drift census runs again:
  tools/round-71/registry-census.py reads the SKILL.md registry block under grammar v2 (unescaped
  pipe split, GFM \\| unescape, owner = last cell, write = second-last, pinned = the joined middle
  cells), reports zero nonconformant rows over the whole registry, and its 14-case selftest shows
  it can fail; the base state is six nonconformant round-70 rows (defects ['pinned-empty']) and
  round-51 census3 exit 2.
Round-70 non-author routed defects in play: the capability rows (repaired at record), the census
W04 erratum, the ca9817cf->ca9817cd erratum, the SOURCES search log + tempfile rejection row, the
wave-settlement receipt, the dead scratch pointers (named as run pointers, not evidence), and the
six lying-field classes (this round's R71-C2). Read the round-70 spot-check first:
{SPOTCHECK} — every disagreement or routed defect it names is this round's input.
{COMMON}
"""


def item(name, role, task):
    return {"name": name, "role": role,
            "prompt": "/skill:godspeed\n\n" + GS + "\n\n" + task + "\n\n" + COMMON}


ITEMS = [
    item("ExecC1", "executor", f"""Independently re-derive R71-C1's landing-side result with YOUR OWN harness — do not run
{LANE}/tools/round-71/seam-probe.py; write your own launcher, env-log parser and checker invocations.
Work under {W1}/ExecC1/ and scratch {SCRATCH}/ExecC1/.
1. Read {PLAN} (R71-C1), {CLAIMS} claims[0], and the round-70 spot-check {SPOTCHECK}.
2. Extract the frozen route and probe blobs: `git -C {LANE} show {FREEZE}:tools/round-71/packed-elf.py`
   and `...:tools/round-71/seam-probe.py` into your scratch; record their sha256 and confirm they
   equal the container pins.
3. Generate your OWN 32-byte nonce, compute its sha256, and run the route at the freeze:
   `<python> -I -B <scratch>/packed-elf.py --root {LANE} --rev {FREEZE} --pkg {PKG} --work <scratch>
   --challenge <nonce> --nonce-commitment <hash> --child-env-log <scratch>/env.jsonl --json-out
   <findings>/c1-route.json` (four carriers; expect exit 0 met 4 of 4).
4. With YOUR OWN parser of the raw JSONL: assert every record's key set is exactly
   HOME/LANG/PATH/TMPDIR, the packer/node/readelf children appear, every HOME/TMPDIR is under the
   receipt's run_root, and a canary you export (`KAIDOKU_ENV_CANARY=probe`) is absent. Then run the
   frozen checker `--check-receipt <findings>/c1-route.json --nonce-commitment <hash>` (expect 0).
5. Build three altered copies yourself (transplant the round-70 landing receipt {R70LAND}; flip one
   nonce hex digit; set run_binding to zeros) and run the frozen checker with the commitment over
   each: each must exit 1 and name run_nonce (transplanted) / run_nonce hash / run_binding.
6. Write rederive.md with commands, receipts and the per-arm table; end with VERDICT."""),

    item("ExecC1Base", "executor", f"""Independently re-derive R71-C1's BASE world and the three missing-arm failures. Work under
{W1}/ExecC1Base/ and scratch {SCRATCH}/ExecC1Base/.
1. Read {PLAN} (R71-C1) and {CLAIMS}.
2. Recreate a pinned upx copy at the path the round-70 landing receipt records
   (`{R70LAND}` carriers[0].runs.pack.argv[0]); verify sha256 against the UPX pin.
3. Run the frozen round-71 probe at the round-70 landing:
   `<python> -I -B {LANE}/tools/round-71/seam-probe.py --root {LANE} --rev {SUPERSEDED} --tool
   tools/round-70/packed-elf.py --battery tools/round-70/mutation-check.py --pkg {PKG} --work
   <scratch> --receipt {R70LAND} --expect-upx <pinned copy> --json-out <findings>/base-probe.json`
   — record arms_passed/target/failed (expect 7 of 10, A8/A9/A10 false) and the exact observation
   text each of the three carries.
4. Independently show WHY each of the three cannot be satisfied by the round-70 route: run the
   round-70 blob with `--child-env-log`, `--challenge` and `--carriers` (record rc and stderr), show
   its receipt has no run_root/child_env_observed/run_nonce, and run its `--check-receipt` with
   `--nonce-commitment` (record rc). Also show the round-70 probe's target is 7 (seven arms).
5. Write base.md with transcripts; end with VERDICT."""),

    item("ExecC2", "executor", f"""Independently re-derive R71-C2 with YOUR OWN shape builder — do not run
{LANE}/tools/round-71/forged-receipts.py for steps 2-3; write the six forgeries yourself. Work under
{W1}/ExecC2/ and scratch {SCRATCH}/ExecC2/.
1. Read {PLAN} (R71-C2) and {CLAIMS} claims[1].
2. From {R70LAND}, cut your own six copies, relabel each to the first-cut world (rev {FIRSTCUT},
   instrument.sha256 = the blob hash of `git show {FIRSTCUT}:tools/round-70/packed-elf.py`), and lie
   exactly one verdict-relevant field each: unpacked_counts, packed_sha256, section_count+upx_list_rc,
   runs.pack.argv (drop --best), refusal.packed_rc, format.type.
3. Extract the first-cut reader (`git show {FIRSTCUT}:tools/round-70/packed-elf.py`) and the
   superseded reader (`git show {SUPERSEDED}:tools/round-70/packed-elf.py`) to scratch; run
   `--check-receipt <copy> --root {LANE} --rev {FIRSTCUT}` with both: record first_cut rc/met and
   superseded rc/failing clauses. Every first cut must accept; every superseded run must name the
   declarative clause you lied about.
4. Run the frozen battery at the freeze (this exercises the shipped implementation):
   `<python> -I -B {LANE}/tools/round-71/forged-receipts.py --root {LANE} --rev {FREEZE} --base-rev
   5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d --tool tools/round-70/packed-elf.py --base-tool
   tools/round-69/packed-elf.py --probe tools/round-70/contract-probe.py --base-probe
   tools/round-69/contract-probe.py --base-probe-rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a
   --battery tools/round-70/mutation-check.py --base-material {R69RECEIPT} --landing-material
   {R70LAND} --first-cut-rev {FIRSTCUT} --first-cut-tool tools/round-70/packed-elf.py
   --superseded-rev {SUPERSEDED} --pkg {PKG} --work <scratch> --json-out <findings>/battery.json`
   — record exit, shapes/lying/landing counts, failures.
5. Write rederive.md with your six-row table plus the battery receipt; end with VERDICT."""),

    item("ExecC3", "executor", f"""Independently re-derive R71-C3 with YOUR OWN parser. Work under {W1}/ExecC3/ and scratch
{SCRATCH}/ExecC3/.
1. Read {PLAN} (R71-C3) and {CLAIMS} claims[2].
2. Write your own cell splitter (split on unescaped pipes, unescape `\\|`, drop the header and
   delimiter rows) and, for every registry data row at {BASE}, record the cell count, the tool path
   and whether the path exists at that rev. Confirm: four round-69 rows have 8 cells and six
   round-70 rows have 6; every other row has 7.
3. Apply YOUR OWN reading rule (owner = last cell, write = second-last, pinned = joined middle) to
   the 8-cell rows and record the reconstructed pinned/write/owner cells; show the six 6-cell rows
   reconstruct no pinned cell (the defect).
4. Simulate the repair in scratch: copy SKILL.md, append the owner cell `kaidoku` to the six
   round-70 rows only, and re-run your parser — record 0 nonconformant rows, the path count, and
   prove the four round-69 rows are byte-identical to the base bytes (`diff` on those lines).
5. Run the frozen census at the base and at the freeze:
   `<python> -I -B {LANE}/tools/round-71/registry-census.py --root {LANE} --rev {BASE} --generate
   --out <findings>/census-base.json` (expect exit 1, six rows) and the same with `--rev {FREEZE}`
   (expect exit 1 too at the freeze: the repair lands at the record commit, after this wave — record
   and explain that, never call it met); run the census `--selftest` (expect 14 cases, 0 failures)
   and round-51 census3 at the base (expect exit 2).
6. Write rederive.md; end with VERDICT."""),

    item("ExecControls", "executor", f"""Run the frozen controls at the freeze and independently re-check each. Work under
{W1}/ExecControls/ and scratch {SCRATCH}/ExecControls/.
1. Read {PLAN} (kill rules and do-nothing controls), {CLAIMS}, and {SPOTCHECK}.
2. Run `<python> -I -B {LANE}/tools/round-71/controls.py --root {LANE} --work <scratch> --probe
   tools/round-71/seam-probe.py --battery tools/round-71/forged-receipts.py --census
   tools/round-71/registry-census.py --json-out <findings>/controls-at-freeze.json` — all six arms
   must show what they must; record the receipt and each arm's observation.
3. Independently re-check the three do-nothing numbers from committed bytes: the round-70 battery
   receipt {R70BAT} carries shapes 10 / landing_probe_shapes 2 / no lying_shapes; the round-70
   landing receipt {R70LAND} has no run_root/child_env_observed/run_nonce; the round-70 probe has
   seven arms (read its source at {SUPERSEDED} and count the arm() calls).
4. For each control, state what a shortcut would have to do to reach the claim target and whether
   the control would catch it; write controls.md; end with VERDICT."""),

    item("ExecSweep", "executor", f"""Run the standing receipts duties at the freeze state. Work under {W1}/ExecSweep/ and scratch
{SCRATCH}/ExecSweep/.
1. Read the SKILL.md registry rows for tools/round-56/receipt-audit.py,
   tools/round-57/record-receipt-audit.py, tools/round-51/census3.py and
   tools/round-68/registry-conformance.py, then run each per its registered entry command against
   {LANE} at {FREEZE}: the freeze-receipt completeness audit over {CLAIMS}, the named-path audit,
   the registry census (census3 — record its exit and the exact seven-cells error: it is the routed
   M70-7 defect, not a surprise), and the round-68 registry conformance census. Record each exit
   code and verdict verbatim; expected-pending is never a clean bill.
2. Re-run the sources census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
   --root /home/vgpnk/Projects/shokunin kaidoku` — record exit, row count, malformed count and the
   W04 warning count (the round-70 report said "the same 20"; the start receipt says 21 — record the
   true number).
3. Run the round-71 census and the no-/tmp fixture audit: `grep -rn "mkdtemp(dir=\"/tmp\")\\|/tmp/"
   {LANE}/tools/round-71/` (record hits and whether they are literals/comments), and record the
   disposition evidence for the persistent receipt-audit bare-name `package.json` finding (run the
   audit, quote the exact finding line, and say whether a fix or a declared exception is the honest
   next step).
4. Write sweep.md with each command, exit code and verdict; end with VERDICT."""),

    item("ReviewerGates", "reviewer", f"""Review the five frozen round-71 instruments against the three predicate sentences, clause by
clause. Work under {W1}/ReviewerGates/ and scratch {SCRATCH}/ReviewerGates/.
1. Read {PLAN}, {CLAIMS} (predicates, kill rules, controls, pins), and {SPOTCHECK}.
2. For each predicate, trace EVERY clause to code that reads it (`git -C {LANE} show
   {FREEZE}:tools/round-71/<tool>`): name any clause no code reads (QUALITY #87), any computed value
   printed but never folded into the verdict (QUALITY #105), and any arm whose observation is
   asserted rather than derived. Pay special attention to A8's launcher-artifact exclusion
   (PYTHONCOERCECLOCALE popped before the observation and the exec), A9's distinctness assertions,
   A10's binding formula and the nonce-commitment direction (compute A = sha256(nonce), compare to
   the caller's commitment — not the reverse), C2's first-cut/superseded relabelling (does the shape
   prove the field is read, or only that the rev is bound?), and C3's join rule (can a 7-cell row be
   misread as 8 or vice versa? can a junk row pass?).
3. Check the exit-code contract (0 met / 1 named / 2 could-not-evaluate) of each instrument and
   whether each `--selftest`/`--validate` fails on a named negative (run them; record cases).
4. Confirm the container shape audits CLEAN at the freeze:
   `python3 -I -B tools/round-29/freeze-gate.py --root {LANE} --rev {FREEZE}` (record the round-71
   entry).
5. Write review.md with one section per instrument (findings with file/line, severity, whether the
   predicate survives); end with VERDICT."""),

    item("ReviewerRepairs", "reviewer", f"""Review the round's committed artifacts and the routed-defect dispositions for append-only
discipline, scope and predicate identity. Work under {W1}/ReviewerRepairs/ and scratch
{SCRATCH}/ReviewerRepairs/.
1. Read {SPOTCHECK} in full and list its seven routed defects with this round's intended disposition
   (from {PLAN} §Repairs carried); name any routed defect the plan leaves unanswered.
2. Verify the frozen state: `git -C {LANE} diff --stat {BASE} {FREEZE}` (record every path); confirm
   no LOG.md, SCORECARD.md, corpus/, PROVINCE.md or SKILL.md file changed between base and freeze
   (the round's records land later), and that the four round-69 SKILL registry rows are
   byte-identical at {FREEZE} to {BASE} (`git show` both, diff the block lines).
3. Verify predicate identity: normalize whitespace in {PLAN}'s three predicate sentences and in
   {CLAIMS}'s `claims` strings; they must be equal (record the comparison command and result).
   Verify the container's `instruments` pins equal the blobs at {FREEZE} and that `loaded_by_counter`
   pins equal their blobs; verify the plan's claim that the pre receipts precede the container
   (commit order via `git log --follow` / `git log -- .ufo/waves/round-71/`).
4. Review the intended SKILL.md repair (six round-70 rows gain the owner cell; nothing else
   changes): draft the exact replacement lines and the old->new disclosure the L1 must paste into
   LOG.md; name any row where appending `| kaidoku |` would change a cell boundary (there must be
   none).
5. Write review.md; end with VERDICT."""),

    item("CriticClaims", "critic", f"""Falsify the three predicates as written — find a way to meet each target without the claimed work
being true. Work under {W1}/CriticClaims/ and scratch {SCRATCH}/CriticClaims/.
1. Read {PLAN} and {CLAIMS}. For each claim, write the shortest shortcut that satisfies its
   predicate and score it: for R71-C1, can a fabricated env log pass A8 (the probe parses the raw
   log, but the log path is caller-supplied — what does the arm actually prove)? can pre-created
   run_roots satisfy A9? can the nonce/binding be recomputed from the genuine receipt (the
   commitment is sha256 of a nonce that the receipt publishes — state exactly what transplantation
   the binding does and does not prevent)? For R71-C2, can the six lying rows be produced without a
   first-cut reader (e.g. by relabelling and asserting rc)? does the superseded rejection depend on
   the field being read or on an unrelated clause? For R71-C3, can a junk registry exit 0 (e.g. a
   row with 7 cells but empty pinned, a duplicate path, an absent path, a fabricated block)?
2. Build each shortcut and run the frozen instrument against it; record exact commands and exits.
   Distinguish (a) a predicate bug worth a supersession this round, (b) a named limit that the
   predicate already discloses, (c) a non-issue.
3. Write falsify.md with one section per claim and a classification per shortcut; end with VERDICT
   naming which targets are reachable without the work."""),

    item("MutProbe", "mutation-tester", f"""Attack the counters themselves — can each frozen round-71 counter fail loudly, and can it be made to
pass falsely? Work under {W1}/MutProbe/ and scratch {SCRATCH}/MutProbe/.
1. Read {PLAN} (predicates and kill rules) and {CLAIMS}.
2. For the registry census: build registries that should fail and check it does (a row with 7 cells
   but an empty pinned cell; two rows for one path; a path that does not exist; a marker typo; a
   block with no data rows). Then build a registry that should pass and check it does. Record each
   exit code and finding code.
3. For the seam probe's validate: a receipt with ten arms all `ok: true` and empty observations; a
   receipt whose `arms_passed` contradicts rows; a receipt whose `failed` list contradicts rows.
   Record each.
4. For the forged battery's validate: six lying rows with rc pair (0, 0); a lying list of five; a
   genuine block missing. Record each. Then ask whether the battery's `check()` can be made to pass
   with a reader that ignores a field — mutate a copy of the superseded reader to drop the
   `unpacked_counts` clause and confirm the battery's L1 row fails (the counter catches a weakened
   reader).
5. Write mutations.md with a table (mutant, expected, observed, verdict); end with VERDICT."""),

    item("MutReaders", "mutation-tester", f"""Generate NEW mutants of the frozen round-71 route and checker beyond the frozen five, and score
them. Work under {W1}/MutReaders/ and scratch {SCRATCH}/MutReaders/.
1. Targets (copies in your scratch only, never the lane tree): the route blob at {FREEZE}
   (`git show {FREEZE}:tools/round-71/packed-elf.py`) and the probe blob (`seam-probe.py`).
2. Route mutants, one seam each: (a) `build_child_env` returns `dict(os.environ)` merged with the
   allowlist; (b) the launcher drops the PYTHONCOERCECLOCALE pop or the exec uses a different env;
   (c) `run_root` becomes a fixed directory under --work; (d) `nonce_clauses` accepts a missing
   run_nonce; (e) the run_binding hashes only the nonce; (f) `observed_env` reports all_allowlisted
   True unconditionally. Score each with the route's `--selftest` and, where relevant, with a probe
   run or the checker over an altered receipt: record killed/not-killed and the exact failing case.
3. Probe mutants: (g) A8 accepts a raw log with an extra key; (h) A9 does not check distinctness;
   (i) A10 accepts a wrong binding. Score each by running the mutated probe against the freeze world
   with your own fixtures and record whether the arm flips.
4. Restore every target byte-exactly from git and prove it (sha256 equal). Write mutants.md; end
   with VERDICT listing survivors with exact lines."""),

    item("SentinelScope", "sentinel", f"""Safety audit of the round's frozen instruments and wave scope. Work under {W1}/SentinelScope/ and
scratch {SCRATCH}/SentinelScope/.
1. Read the five frozen instruments at {FREEZE} plus the changed-path list
   (`git -C {LANE} diff --stat {BASE} {FREEZE}`).
2. Audit: (a) credential material — scan the tools and every committed receipt for secret-like
   patterns, cookies, `op://`, tokens, and state that assignment text embedded in dispatch/spec JSON
   is not evidence of a leak; (b) scratch boundaries — every mkdtemp/work-dir path honoured from
   --work, no hardcoded /tmp output, selftest scratch owned and removed; (c) child environment —
   the launcher's declared artifact exclusion (PYTHONCOERCECLOCALE) and whether any child inherits
   the caller env; (d) network — any network primitive or command; (e) the nonce: is the plaintext
   or any secret committed? (the commitment hash is public by design; the nonce must live only in
   scratch); (f) write scope — the wave writes only its findings dirs.
3. Report blocking / advisory / note findings with file:line and the smallest remediation; record
   whether any pacman command ran (`/var/log/pacman.log` entries for today) and that the guard
   stayed binding. Write scope.md; end with VERDICT."""),

    item("ScoutSource", "scout", f"""Open the sources for this round's sourced claim and the routed rejection row. Work under
{W1}/ScoutSource/ and scratch {SCRATCH}/ScoutSource/.
1. Open https://github.github.com/gfm/ (the GFM spec, section 4.10 Tables) live AND save a snapshot
   under your findings dir with status/bytes/sha256/date; locate the sentence about the number of
   cells in table rows versus the header row (the tolerance rule). Record the exact contiguous quote
   (<=25 words) and its anchor. Compare with the existing S258 row ({LANE}/corpus/SOURCES.md):
   S258's scope is the escaped-pipe rule; this round needs the cell-count tolerance rule for the
   registry grammar addendum — decide whether a NEW row (S273, next unused id) is warranted and
   state the distinct scope, or whether S258's scope already covers it (then say so and propose no
   row). Also check whether GFM says anything about a row with FEWER cells than the header (quote
   it) and whether that grounds reading a 6-cell row as a defect.
2. Open https://docs.python.org/3/library/tempfile.html (live + snapshot) and screen it for the
   REJECTED row S274 the round-70 routed defect 4 asks for: quote `mkdtemp`'s promise, then show
   with a grep sweep that the page does not ground distinctness/uniqueness/collision-freedom; give
   the rejection reason and the flip condition.
3. Write sources.md with fetch evidence (status, bytes, sha256, access date 2026-11-04), the located
   quotes with anchors, the ADMIT row draft (id S273: kind spec, tier A, scope, teaches, status
   mined, used-by corpus/knowledge/2026-11-04-r71-registry-grammar.md) and the S274 REJECTED row
   draft (reason + flip), plus the round-71 search-log paragraph (question, where searched, date,
   identified/screened/included/excluded counts, exclusion reasons, stop rationale). End with
   VERDICT."""),

    item("ConnectorCross", "connector", f"""Sibling-overlap scan: does any other lane own this round's ground? Work under
{W1}/ConnectorCross/ and scratch {SCRATCH}/ConnectorCross/.
1. Read {LANE}/PROVINCE.md (Core/Frontier) and the sibling PROVINCE.md files under
   /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md (read-only).
2. The round's ground: (a) registry row grammar / Markdown table parsing as a lane drift census;
   (b) pre-committed run binding / receipt authenticity beyond field equality; (c) observed child
   environment capture and concurrent scratch isolation for a subprocess route. For each, record
   which sibling (if any) claims the surface, with the PROVINCE line, and whether this round stays
   inside kaidoku's REA-triage province.
3. Read /home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md and its package rows if present
   (read-only); record whether any staged theme matches this round's claims (fit or no-fit for the
   report's Assimilation line — the frozen claims may not be widened).
4. Check {LANE}/considerthese/ (report absent if it is); write scan.md with one row per ground item;
   end with VERDICT."""),

    item("ScribeKnowledge", "scribe", f"""Draft the round-71 knowledge entry and its index rows. Write under {W1}/ScribeKnowledge/ (drafts;
the L1 lands them).
1. Read {PLAN} (R71-C1/C2/C3), {CLAIMS}, {W1}/ScoutSource/sources.md when it exists, and the format
   precedent {LANE}/corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md.
2. Draft corpus/knowledge/2026-11-04-r71-registry-grammar.md: opens with the provenance trio as
   line-start lines (`source:` S273's id + URL + anchor, with S258 cited as the escaped-pipe
   authority; `verified-at:` the freeze commit; `recheck:` the re-runnable census command), then:
   the grammar-v2 rule (split on unescaped pipes, unescape `\\|`, owner = last, write =
   second-last, pinned = joined middle cells); the two filed shapes and why the round-69 rows are
   read, never rewritten; the six round-70 rows' omitted owner cell and the disclosed repair; the
   census's capability and its selftest; and a Limits section: the parser is not a complete GFM
   implementation (it reads only the marked registry block, strips leading spaces, does not parse
   inline HTML), a nonconformant row is named rather than skipped, and the round-50 census3 stays
   byte-identical.
3. Draft the corpus/README.md additions: a coverage-map row for the new entry, a knowledge-index row,
   and a round-71 frontier note: the registry drift census is Core again; the seam's runtime
   env-capture/concurrent-scratch class moves Frontier -> Core for the measured route, with the
   limits (only the four-key allowlist and the pinned carriers; the launcher's one declared artifact
   exclusion; the binding is replay/transplant rejection, not cryptographic authenticity).
4. Draft the SCORECARD `## Capabilities` rows for R71-C1/C2/C3 (capability, what it can now do,
   evidence pointer, first-working round 71) and a `## Round-71` section skeleton naming the three
   claims and their receipts.
5. Write the drafts with exact target paths in a MANIFEST line; end with VERDICT."""),

    item("ScribeLesson", "scribe", f"""Draft corpus/lessons/round-71.md. Write under {W1}/ScribeLesson/ (drafts; the L1 lands it).
1. Read {LANE}/corpus/lessons/round-70.md and round-70-verifier-spotcheck.md (format precedent),
   {PLAN}, and {CLAIMS}.
2. Draft the lesson: header (round 71, attempt 1, base/declaration/freeze, the three claims), a
   `## Gate` table seeded with S273 (admit candidate) and S274 (reject candidate) from
   {W1}/ScoutSource/sources.md when it exists, a spot-check placeholder line
   `[L1 — filled by the non-author closure.]`, a `## Mistakes` table seeded with: M71-1
   registry-row-shape (the six round-70 SKILL rows omit the owner cell; no gate caught it because
   the frozen parser died before reaching them; captured-by: the new grammar census — a 6-cell row
   must produce `pinned-empty`); M71-2 launcher-artifact (the Python launcher coerces LC_CTYPE into
   its own environment; captured-by: the raw-log allowlist assertion itself — the first smoke run
   showed LC_CTYPE and the fix was PYTHONCOERCECLOCALE=0 plus the declared pop); and M71-3 for the
   wave's strongest finding (placeholder `<L1 fills>`).
3. Record the census start (21 W04 warnings, 179 rows, exit 0 — from
   {LANE}/.ufo/waves/round-71/l1/census-start.txt) and leave the end census `<L1 fills>`.
4. Do not invent results: every cell that depends on measurements not yet in the wave outputs gets
   a `<L1 fills: ...>` placeholder. Write the draft with the exact target path; end with VERDICT."""),
]

SPEC = {
    "wave": "r71-w1",
    "milestone": "r71-w1 build+attack: three frozen claims verified and attacked, five instruments "
                 "reviewed clause-by-clause, new route/probe mutants, counter false-green probes, "
                 "safety audit, sourced rows, sibling scan, knowledge and lesson drafts.",
    "reportDir": ".ufo/waves/round-71/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

rendered = json.dumps(SPEC)
assert "{W1}" not in rendered and "{LANE}" not in rendered and "{SCRATCH}" not in rendered
assert FREEZE != 'FREEZE_HASH_PLACEHOLDER', 'pass the freeze commit hash'
for it in ITEMS:
    assert it["prompt"].startswith("/skill:godspeed\n\nYou are a Godspeed-enabled subagent."), it["name"]
    assert re.search(r"\{[A-Z_]{2,}\}", it["prompt"]) is None, it["name"]
out = LANE + '/.ufo/waves/round-71/r71-w1-spec.json'
pathlib.Path(out).write_text(json.dumps(SPEC, indent=1))
print(json.dumps({"items": len(ITEMS),
                  "roles": sorted({i["role"] for i in ITEMS}),
                  "attack": sum(1 for i in ITEMS if i["role"] in
                                ("reviewer", "critic", "mutation-tester", "labrat")),
                  "spec": out}))
