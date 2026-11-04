#!/usr/bin/env python3
"""Generate the kaidoku round-70 wave-1 spec (one v1 build+attack wave, 15 seats).

Roles: 5 executor, 2 reviewer, 1 critic, 2 mutation-tester, 1 sentinel,
1 scout, 1 connector, 2 scribe — attack share 5/15 = 33% (reviewer, critic,
mutation-tester), one connector seat. The L1 holds the canonical planner seat
(the validator rejects a planner role). Routing is the host's
task.agentModelOverrides; no model is passed anywhere.

Usage: gen-w1.py <freeze-commit-hash> <declaration-commit-hash>
"""
import json
import pathlib
import re
import sys

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-70/w1'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r70'
PLAN = LANE + '/plans/round-70-claims.md'
CLAIMS = LANE + '/.ufo/waves/round-70/claims.json'
BASE = '5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d'
DECL = sys.argv[2] if len(sys.argv) > 2 else '2c77672509517c773e0687c86dba5266ef329e83'
FREEZE = sys.argv[1] if len(sys.argv) > 1 else 'FREEZE_HASH_PLACEHOLDER'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
R69RECEIPT = LANE + '/.ufo/waves/round-69/l1/scores/c3-at-landing.json'
SPOTCHECK = LANE + '/corpus/lessons/round-69-verifier-spotcheck.md'

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
kaidoku-shokunin round 70, attempt 1, wave w1 = the single v1 build+attack wave (15 seats; policy
band 8-16; attack seats reviewer x2, critic, mutation-tester x2 = 5 of 15 = 33%). Base
{BASE} (the carry-in commit recording the round-69 non-author closure); declaration
{DECL} (six instruments under tools/round-70, the claims plan, the census-start receipt); operative
freeze {FREEZE} (the commit that first adds the claims container).
Three declared claims (plan {PLAN}; container {CLAIMS}):
- R70-C1 (calibration, capability acquisition) — the receipt readers are bound to their producers:
  all ten forged shapes accepted by tools/round-69/packed-elf.py --check-receipt at the base and
  rejected by tools/round-70/packed-elf.py --check-receipt at the measured revision each naming its
  declared clause; the identity shapes also rejected by the hardened
  tools/round-70/contract-probe.py (A5/A6 false) and accepted by the base probe; the genuine
  receipts still pass; tools/round-70/mutation-check.py enforces its target pin, pristine floor and
  per-run work_dir, and --validate rejects a constant battery receipt.
- R70-C2 (operability, capability acquisition) — the safe packer seam: tools/round-70/seam-probe.py
  arms A1_hash_before_exec (an impostor printing the pinned version is refused and provably never
  executed), A2_threaded_path (the producer-bound receipt's upx argv all name the pinned-copy path,
  never the module default), A3_child_env_allowlist (committed child-env cases in the registry and a
  green selftest at that case count), A4_broken_node_typed, A5_packer_exec_format, A6_home_no_tmp,
  A7_per_run_work — 7 of 7 at the measured revision, 0 of 7 against tools/round-69/packed-elf.py and
  tools/round-69/mutation-check.py at the base.
- R70-C3 (coverage, capability acquisition) — a statically linked executable joins the carriers:
  /usr/bin/docker-init (sha256 0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115,
  measured 1268/29/1111 original, 3/3/5 packed, ceiling 10/1268 = 0.0079) as kind `static-exe`;
  target 4 of 4; the frozen checker rejects the round-69 receipt on its producer binding.
Round-69 routed defects this round closes: M69-8 (fabricated receipts passed the frozen counters),
M69-9/S-1 (--upx executed before hashing), M69-10 (untyped preflight leaks), M69-11 (/tmp HOME
fallback, fixed-name scratch dirs), M69-1 (container shape the round-29 gate reads as
INSTRUMENT_NONE — this round's container uses the top-level instruments map with predicates in
claims).
{COMMON}
"""


def item(name, role, task):
    return {"name": name, "role": role,
            "prompt": "/skill:godspeed\n\n" + GS + "\n\n" + task + "\n\n" + COMMON}


ITEMS = [
    item("ExecC1", "executor", f"""Independently re-derive R70-C1's landing-side result with YOUR OWN harness — do not run
{LANE}/tools/round-70/forged-receipts.py; write your own shape builder and invocations. Work under
{W1}/ExecC1/ and scratch {SCRATCH}/ExecC1/.
1. Read {PLAN} (R70-C1) and the predicate in {CLAIMS} claims[0].
2. Cut YOUR OWN forged shapes (at least six, including a wrong-revision, a zeroed instrument hash, a
   relabelled source, an underived ratio, a packed-over-ceiling and an unknown-carrier id) from the
   genuine receipt {R69RECEIPT}.
3. Read the frozen reader via `git -C {LANE} show {FREEZE}:tools/round-70/packed-elf.py` into your
   scratch and run `--check-receipt --root {LANE} --rev {FREEZE}` over each shape: every shape must
   exit 1 naming a clause consistent with its mutation (record the exact clause lines).
4. Run the same shapes against the base reader (`git show {BASE}:tools/round-69/packed-elf.py`,
   plain `--check-receipt`): every shape must exit 0 met true (record each).
5. Write rederive.md with your command transcripts and the per-shape table; end with VERDICT."""),

    item("ExecC1Base", "executor", f"""Independently re-derive R70-C1's BASE-side result (the defect the round closes) and the battery
self-test. Work under {W1}/ExecC1Base/ and scratch {SCRATCH}/ExecC1Base/.
1. Read {PLAN} (R70-C1) and {CLAIMS}.
2. Forge YOUR OWN receipt that lies about its verdict fields but keeps the genuine instrument/rev
   fields of {R69RECEIPT} (e.g. flip met_target to true on a receipt whose carriers rows you set to
   ok=false, or invent counts) and run it against the base reader
   (`git -C {LANE} show {BASE}:tools/round-69/packed-elf.py`, plain --check-receipt): record whether
   the base reader accepts it (the routed M69-8 defect, reproduced independently).
3. Run the frozen battery's self-test: `python3 -I -B {LANE}/tools/round-70/forged-receipts.py
   --selftest --root {LANE} --base-rev {BASE} --base-tool tools/round-69/packed-elf.py --work
   <your scratch>` — record cases/failed/ok.
4. Run the frozen battery's --validate over a constant receipt you write (no mutant rows, survivors
   []) and over the r69-era battery receipt {LANE}/.ufo/waves/round-69/l1/scores/c1-at-landing.json
   — record both verdicts and whether the structural check distinguishes them honestly (the r69
   receipt predates the work_dir/target_pin fields; report what --validate says and whether that is
   the honest reading for a frozen r70 validator).
5. Write rederive.md with transcripts; end with VERDICT."""),

    item("ExecC2", "executor", f"""Independently re-derive R70-C2's seam arms with YOUR OWN harness — do not run
{LANE}/tools/round-70/seam-probe.py. Work under {W1}/ExecC2/ and scratch {SCRATCH}/ExecC2/.
1. Read {PLAN} (R70-C2) and the predicate in {CLAIMS} claims[1].
2. From `git -C {LANE} show {FREEZE}:tools/round-70/packed-elf.py` and
   `git show {BASE}:tools/round-69/packed-elf.py` write both blobs into your scratch.
3. Build your own impostor script (prints `upx 5.2.0`, touches an execution log) and run each blob
   with --upx impostor --root {LANE} --rev <its rev> --pkg {PKG} --work <scratch>: record rc, the
   unevaluable clause, and whether the impostor's log exists, for BOTH blobs.
4. Build your own broken node shim (exit 7) and an exec-format-less --upx file (+x text); run both
   blobs through those scenarios; record rc/clause/traceback for each.
5. Run each blob's --selftest and record cases/failed; run the frozen
   tools/round-70/mutation-check.py twice (blob from git at {FREEZE}, --patch-set r70, same --work,
   --min-pristine-cases 0) and record the two work_dir values.
6. Write rederive.md with the base-vs-freeze comparison table; end with VERDICT."""),

    item("ExecC3", "executor", f"""Independently verify R70-C3's carrier evidence from the host bytes. Work under
{W1}/ExecC3/ and scratch {SCRATCH}/ExecC3/.
1. Read {PLAN} (R70-C3) and the predicate in {CLAIMS} claims[2].
2. Re-derive the declared constants yourself: sha256 of /usr/bin/docker-init; `file -L` (statically
   linked?); pack a copy with `upx --best -q` into your scratch; `upx -d` roundtrip and `cmp` byte
   identity; REA analyze ({PKG}, `node scripts/rea.mjs analyze --format json <path>`) of original
   and packed copies; record procedure/segment/string counts for both and the readelf -h format.
3. Compare each number against the frozen registry (`git -C {LANE} show
   {FREEZE}:tools/round-70/packed-elf.py` CARRIERS/DECLARED_ORIG) and the plan's declared values
   (1268/29/1111, 3/3/5, ceiling 10, ratio 0.0079).
4. Also verify the OTHER three carriers' pins still match the frozen table (jq, xxd, libz sha256s).
5. Write verify.md with every command and value; end with VERDICT."""),

    item("ExecControls", "executor", f"""Run the frozen controls and independent receipts at the freeze state. Work under
{W1}/ExecControls/ and scratch {SCRATCH}/ExecControls/.
1. Read {PLAN} (kill rules and do-nothing controls) and {CLAIMS}.
2. Run `python3 -I -B {LANE}/tools/round-70/controls.py --root {LANE} --rev {FREEZE} --base-rev
   {BASE} --tool tools/round-70/packed-elf.py --base-tool tools/round-69/packed-elf.py --battery
   tools/round-70/mutation-check.py --r69-receipt {R69RECEIPT} --pkg {PKG} --work <scratch>
   --json-out <your findings>/controls-at-freeze.json` — all seven arms must show what they must
   (record the receipt bytes under your findings dir).
3. Run `python3 -I -B {LANE}/tools/round-70/forged-receipts.py --root {LANE} --rev {FREEZE}
   --base-rev {BASE} --tool tools/round-70/packed-elf.py --base-tool tools/round-69/packed-elf.py
   --probe tools/round-70/contract-probe.py --base-probe tools/round-69/contract-probe.py
   --base-probe-rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a --battery
   tools/round-70/mutation-check.py --base-material {R69RECEIPT} --landing-material
   {LANE}/.ufo/waves/round-70/l1/pre/c3-at-declaration.json --pkg {PKG} --work <scratch>
   --json-out <your findings>/battery-at-freeze.json` — the landing-material at the freeze is the
   declaration-rev genuine receipt (the landing re-measures later); record the receipt and whether
   every arm holds at the freeze state.
4. Record any arm that fails with its observation; write receipts.md; end with VERDICT."""),

    item("ExecSweep", "executor", f"""Run the standing receipts duties at the freeze state. Work under {W1}/ExecSweep/ and scratch
{SCRATCH}/ExecSweep/.
1. Read the SKILL.md gate registry rows for tools/round-56/receipt-audit.py and
   tools/round-57/record-receipt-audit.py and tools/round-51/census3.py (registry home
   {LANE}/SKILL.md, round29-freeze and later rows), then run each per its registered entry command
   against {LANE} at the freeze commit {FREEZE}: the freeze-receipt completeness audit over
   {CLAIMS}, the named-path completeness audit, and the registry census over corpus/SOURCES.md.
   Record each tool's exit code and verdict verbatim.
2. Note any finding that names this round's container or files (expected: the round-70 row is not
   yet in corpus/claim-freezes-v2.tsv — that row lands with the record commit; the
   receipt-audit may therefore report the container's own receipts as pending — record it as
   expected-pending, never as a clean bill).
3. Write sweep.md with each command, exit code and verdict; end with VERDICT."""),

    item("ReviewerGates", "reviewer", f"""Review the six frozen instruments against the three predicate sentences, clause by clause. Work
under {W1}/ReviewerGates/ and scratch {SCRATCH}/ReviewerGates/.
1. Read {PLAN} and {CLAIMS} (predicates, kill rules, do-nothing controls, instrument pins).
2. For each predicate, trace EVERY clause to the instrument code that reads it
   (`git -C {LANE} show {FREEZE}:<tool>` for tools/round-70/packed-elf.py,
   contract-probe.py, mutation-check.py, seam-probe.py, forged-receipts.py, controls.py): name any
   clause no code reads (QUALITY #87), any comparison whose computed value is printed but never
   folded into the verdict (QUALITY #105), and any arm whose observation is asserted rather than
   derived.
3. Check the exit-code contract (0 met / 1 named / 2 could-not-evaluate) of each instrument against
   its registry semantics; check every selftest/validate mode actually fails on a named negative.
4. Review the container shape against the round-29 gate's expectations (top-level instruments map,
   predicates naming tools/round-70 paths, no bare script names) and report whether
   `python3 -I -B tools/round-29/freeze-gate.py --root {LANE} --rev {FREEZE}` (run it) audits
   round-70 CLEAN.
5. Write review.md with one section per instrument (findings with file/line, severity, and whether
   the predicate survives); end with VERDICT."""),

    item("ReviewerRepairs", "reviewer", f"""Review this round's landed repairs and drafts for append-only discipline and write scope. Work
under {W1}/ReviewerRepairs/ and scratch {SCRATCH}/ReviewerRepairs/.
1. Read {SPOTCHECK} (the routed defects M69-1/8/9/10/11), then verify each routed defect has a
   landing target in the round-70 declaration: `git -C {LANE} show {BASE}:LOG.md | tail -40`
   (the carry-in entry), the appended erratum in corpus/lessons/round-69.md (`git show
   {BASE}:corpus/lessons/round-69.md | tail -20`), and {PLAN} repairs section.
2. Verify append-only: `git -C {LANE} diff {BASE} {FREEZE} -- LOG.md corpus/lessons/round-69.md`
   must show additions only (no deletions); record any filed byte rewritten anywhere in that range
   (`git diff {BASE} {FREEZE} --stat` — expect only the carry-in + declaration files).
3. Review the SCORECARD.md round-69 section tail (git show {BASE}:SCORECARD.md | tail -30) for the
   final honest-stop correction — this round must not have silently promoted the C2/C3 capabilities
   the closure refused; check the declaration's claims do not re-score any axis number.
4. Write review.md (findings with severity; anything that is a defect of the lane's own files is
   named as such); end with VERDICT."""),

    item("CriticClaims", "critic", f"""Falsify the three claims' predicates as written — find a way to meet each target without the
claimed work being true. Work under {W1}/CriticClaims/ and scratch {SCRATCH}/CriticClaims/.
1. Read {PLAN} and {CLAIMS} (predicates verbatim; attack them as written, never a widened or
   re-frozen variant).
2. R70-C1: forge receipts that bind the producer correctly (copy instrument.sha256/rev from a
   genuine receipt — {R69RECEIPT} for the base pair, the declaration-rev receipt
   {LANE}/.ufo/waves/round-70/l1/pre/c3-at-declaration.json for the freeze pair) while lying about
   verdict-relevant fields the clauses may not read (unpacked_counts, refusal block, packed sha256,
   runs records, before_ceilings entries, format). Run the frozen checker
   (tools/round-70/packed-elf.py at {FREEZE} via git show blob) and the hardened probe on each: any
   lying receipt that passes either reader is a counter defect (record the exact field).
3. R70-C2: attack each seam arm — an impostor that removes its own execution log after running;
   an argv that never reaches the loop because the instrument refuses earlier; a child-env audit
   recorded but never passed to subprocess; an A7 that passes with sequential runs but collides
   concurrently (run two batteries with the same --work in parallel and compare).
4. R70-C3: a receipt with four rows where one static row is fabricated from a DYNAMIC binary
   (relabelled kind); does the frozen checker notice? A genuine receipt whose dinit counts were
   copied from libz?
5. Write falsify.md: for each attack, whether it meets the target (shortcut found → named
   defect with the exact command) or is rejected (the named clause); end with VERDICT."""),

    item("MutReaders", "mutation-tester", f"""Generate NEW mutants of the frozen round-70 readers beyond the frozen five and score them. Work
under {W1}/MutReaders/ and scratch {SCRATCH}/MutReaders/.
1. Targets (copies in your scratch only, never the frozen files): `git -C {LANE} show
   {FREEZE}:tools/round-70/packed-elf.py` — mutate the NEW binding clauses (registry pin compare,
   ratio recompute, packed<=ceiling, rev compare, ids-set compare) one at a time (>= 6 mutants,
   e.g. `!=` -> `==` on a pin check, `>` -> `>=` on a ceiling, drop the DECLARED_ORIG lookup).
2. For each mutant: run `--check-receipt <shape> --root {LANE} --rev {FREEZE}` over at least three
   forged shapes you build from {R69RECEIPT} (or reuse the shapes the frozen battery writes under
   its scratch — build your own). A mutant is DEAD iff at least one shape that the pristine reader
   rejects is ACCEPTED by the mutant (or the clause set visibly shrinks on a shape the pristine
   reader names) — a syntax error is not a kill (QUALITY #108: the closing case feeds the mutated
   function a false input).
3. Record for each mutant: patch site, diff, the shapes' verdicts pristine vs mutant, killed /
   survived / unevaluable. Survivors are findings: name the exact case that should have killed it
   and route it to the next freeze (never repair the frozen bytes yourself).
4. Write battery.md with the table; end with VERDICT."""),

    item("MutProbe", "mutation-tester", f"""Attack the COUNTERS themselves — can each frozen round-70 counter fail loudly? Work under
{W1}/MutProbe/ and scratch {SCRATCH}/MutProbe/.
1. Targets (copies in your scratch only): tools/round-70/forged-receipts.py, seam-probe.py,
   controls.py, mutation-check.py at {FREEZE} via git show.
2. For each counter, mutate its ARM EXPRESSIONS (an `ok` comparison flipped, an expected rc
   changed, a clause-membership test inverted) and check whether the counter's own --selftest /
   --validate / a staged failing run notices: a counter whose flipped arm still exits 0 is a
   false-green counter (QUALITY #105/109). At minimum: flip one forged-receipts shape expectation,
   one seam-probe arm comparison, one controls arm expectation, and the mutation-check target-pin
   comparison; run each mutated copy against the real inputs (the r69 receipt, the declaration-rev
   receipt {LANE}/.ufo/waves/round-70/l1/pre/c3-at-declaration.json, your own forged shapes) and
   record whether the verdict changes.
3. Also probe the honest-green path: does each counter's receipt carry its observations (a reader
   that prints ok=true with no per-arm data is not evidence)?
4. Write battery.md with the mutation table and any false-green findings; end with VERDICT."""),

    item("SentinelScope", "sentinel", f"""Scope and safety audit of the round so far. Work under {W1}/SentinelScope/ and scratch
{SCRATCH}/SentinelScope/.
1. `git -C {LANE} status --porcelain` and `git -C {LANE} diff {BASE} {FREEZE} --stat` — every
   changed path must belong to this round (tools/round-70, plans/round-70-claims.md,
   .ufo/waves/round-70/**, corpus/lessons/round-69.md, LOG.md, SCORECARD untouched so far); name
   any path outside the lane's write scope.
2. Scan the six frozen tools (`git show {FREEZE}:tools/round-70/<tool>`) for: writes outside
   --work or the caller's scratch; subprocess calls whose env inherits more than the recorded
   allowlist (the packer seam must use build_child_env; note the REA node calls' env honestly);
   any network access; any secret, token, cookie or vault reference (op://) in code or receipts;
   any fixed-name scratch dir; any /tmp literal.
3. Verify the wave bounds so far: no seat has written outside its findings dir; the fleet root and
   sibling repos untouched (`git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -v
   '.scratch'` should be empty or name only other lanes' pre-existing files).
4. Verify the pacman guard was not violated: no pacman transaction ran (check your own observations
   only; report the guard as binding for the rest of the round).
5. Write audit.md with findings by severity (blocking / advisory / note) and file:line; end with
   VERDICT."""),

    item("ScoutSource", "scout", f"""Open the environment-contract source for this round's sourced claim, and screen a second
candidate. Work under {W1}/ScoutSource/ and scratch {SCRATCH}/ScoutSource/.
1. Fetch https://docs.python.org/3/library/subprocess.html (record HTTP status, byte count, sha256,
   access date 2026-11-04). Locate the env parameter contract — the sentence saying the child
   inherits the current process environment by default and env, when not None, defines the new
   process's environment. Copy a located quote of <= 25 words with its section/anchor (e.g. the
   Popen env bullet) verbatim.
2. Screen a second candidate: https://docs.python.org/3/library/tempfile.html (mkdtemp semantics,
   for the per-run scratch arm) — same evidence capture; then decide ADMIT or REJECT as a SOURCES
   row with a reason (does a second row add a claim the subprocess row does not already ground?
   Rejections are evidence of taste; give the flip condition).
3. Ground each candidate against the claims: the subprocess env contract grounds R70-C2's
   A3/A6 (build_child_env allowlist, no inherited environment); note precisely which arms rest on
   it.
4. Write sources.md with: fetch evidence (status/bytes/sha/date), the located quotes with anchors,
   the admit/reject decisions with reasons, and the proposed SOURCES.md rows (id S272 next unused;
   tier, scope, anchor, teaches, status mined, used-by the round-70 knowledge entry path); end with
   VERDICT."""),

    item("ConnectorCross", "connector", f"""Sibling-overlap scan: does any other lane own this round's ground? Work under
{W1}/ConnectorCross/ and scratch {SCRATCH}/ConnectorCross/.
1. Read {LANE}/PROVINCE.md (Core and Frontier) and the sibling repos' PROVINCE.md files
   (/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md — read-only).
2. The round's ground: (a) provenance-bound receipt readers (a gate binding a saved receipt to its
   producer instrument and revision); (b) the safe packer seam (hash-before-exec, minimal child
   env, per-run scratch); (c) packed static executables as a REA triage carrier class. For each,
   record which sibling (if any) claims the surface and whether this round absorbs their ground or
   stays inside kaidoku's REA-triage province.
3. Read /home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md if present (read-only) and
   record whether any staged theme matches this round's claims (the frozen claims may not be
   widened by it — record fit or no-fit for the report's Assimilation line).
4. Write scan.md with one row per ground item (owner, overlap verdict, evidence path); end with
   VERDICT."""),

    item("ScribeKnowledge", "scribe", f"""Draft the round-70 knowledge entry and its index rows. Write under {W1}/ScribeKnowledge/ (drafts;
the L1 lands them).
1. Read {PLAN}, {CLAIMS}, and the round-69 entry {LANE}/corpus/knowledge/2026-11-03-r69-packed-route-contract.md
   (format precedent), plus {W1}/ScoutSource/sources.md when it exists (the S272 row material).
2. Draft corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md: opens with the provenance
   trio as line-start lines (source: the S272 row id + URL + anchor for the subprocess env
   contract, plus the lane's own frozen instruments as own-work evidence; verified-at: the freeze
   commit; recheck: the re-runnable command), then the three capabilities' contracts: the
   provenance-bound reader clauses (rev + instrument hash + registry tables + declared counts +
   ratio relation + rows/target/arm truth), the safe seam (hash-before-exec, threaded validated
   path, child-env allowlist, typed refusals, per-run scratch), and the static-exe carrier
   (constants, ceiling per class). Limits section: what is NOT claimed (other packers, anti-UPX
   stubs, PE/Mach-O, other static binaries than the pinned carrier, REA node env unchanged).
3. Draft the corpus/README.md additions: the coverage-map row for the new entry, the
   knowledge-index row (four cells, below the table delimiter), and the round-70 frontier note
   superseding the round-68/69 lines for packed static binaries (Core for the pinned carrier under
   UPX 5.2.0; still Frontier: other packers, other static binaries, anti-UPX stubs, PE/Mach-O).
4. Write the drafts under your findings dir with exact target paths in a MANIFEST line; end with
   VERDICT."""),

    item("ScribeLesson", "scribe", f"""Draft corpus/lessons/round-70.md. Write under {W1}/ScribeLesson/ (drafts; the L1 lands it).
1. Read {LANE}/corpus/lessons/round-69.md (format precedent: title, Gate table, Mistakes table,
   Outcome, Census), {SPOTCHECK}, and {PLAN}.
2. Draft the lesson: header (round 70, attempt 1, base/declaration/freeze commits, the three
   claims with axes); a `## Gate` skeleton with a candidate table (the S272 subprocess-env row and
   the tempfile screen from the scout's sources.md, with fetch evidence and located quotes; rows
   for admit/reject decisions), a spot-check placeholder line `[L1 — filled by the non-author
   closure.]`, and a `## Mistakes` table seeded with the design-time mistake: M70-1 class
   before-arm-world (forged shapes cut from the round-70 four-carrier receipt would fail the base
   reader for the wrong reason — target 4 != 3 — producing a false before-arm; captured-by: the
   wrong-world control the battery's selftest carries; fix: shapes are cut from the base-world
   receipt the base reader accepts, and the selftest's wrong-world control proves the guard can
   fail). Leave rows for the wave's findings to be filled by the L1.
3. Do not invent results: every cell that depends on measurements not yet in the wave outputs gets
   a `<L1 fills: ...>` placeholder instead of prose.
4. Write the draft under your findings dir; end with VERDICT."""),
]

SPEC = {
    "wave": "r70-w1",
    "milestone": "r70-w1 build+attack: three frozen claims verified and attacked, six instruments "
                 "reviewed clause-by-clause, new reader mutants, counter false-green probes, scope "
                 "audit, sourced rows, sibling scan, knowledge and lesson drafts.",
    "reportDir": ".ufo/waves/round-70/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

rendered = json.dumps(SPEC)
assert "{W1}" not in rendered and "{LANE}" not in rendered and "{SCRATCH}" not in rendered
assert FREEZE != 'FREEZE_HASH_PLACEHOLDER', 'pass the freeze commit hash'
for it in ITEMS:
    assert it["prompt"].startswith("/skill:godspeed\n\nYou are a Godspeed-enabled subagent."), it["name"]
    assert re.search(r"\{[A-Z_]{2,}\}", it["prompt"]) is None, it["name"]
out = LANE + '/.ufo/waves/round-70/r70-w1-spec.json'
pathlib.Path(out).write_text(json.dumps(SPEC, indent=1))
print(json.dumps({"items": len(ITEMS),
                  "roles": sorted({i["role"] for i in ITEMS}),
                  "attack": sum(1 for i in ITEMS if i["role"] in
                                ("reviewer", "critic", "mutation-tester", "labrat")),
                  "spec": out}))
