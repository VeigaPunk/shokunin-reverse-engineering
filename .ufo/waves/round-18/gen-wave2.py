#!/usr/bin/env python3
"""Generate the round-18 wave-2 (falsify) spec. Every item attacks one wave-1 output at REV."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W18 = LANE + "/.ufo/waves/round-18"
B = "9011581d84527ba34c675f9cf912e54d2e72d470"
F = "eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0"
R = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
T = W18 + "/tools"
GOD = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
SRCZIP = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip"
SPOT = LANE + "/corpus/lessons/round-17-verifier-spotcheck.md"
KE = LANE + "/corpus/knowledge/2026-10-20-r18-swiss-map-replay.md"
K17 = LANE + "/corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
LES = LANE + "/corpus/lessons/round-18.md"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    DIRECTIVE = f.read()
ACC = ("# Acceptance\nRead-only: write only your report. Verdict first line: HOLDS / BROKEN / PARTIAL. "
       "Paste each command with its exit code, cite exact path:line anchors at REV " + R + " (git show REV:path), "
       "label observation vs inference, never fabricate. A finding needs a reproducing command.")
items = []


def add(name, role, body):
    items.append({"name": name, "role": role,
                  "prompt": "/skill:godspeed\n" + DIRECTIVE + "\n# Target\n" + body.strip() + "\n" + ACC})


# ---- C1: routed-defects, one attack per defect x2 (substance truth, gate weakness) ----
DEF = {
    "PINMAP": f"{SPOT}:137; corrections at {K17} (Round-18 correction) and SCORECARD.md round-18; receipts {W18}/runs/*/receipt.json pin_checks map_path/map_sha256",
    "VALIDATE16": f"{SPOT}:138; {W18}/evidence/validate16/summary.json and its stdout files; LOG.md/SCORECARD.md R17-VALIDATE16 lines",
    "PRODUCERREV": f"{SPOT}:139; LOG.md/SCORECARD.md/{K17} R17-PRODUCER-REV lines naming 2711674 and 95e34db",
    "SUMSRUNLOG": f"{SPOT}:140-143; {W17}/predictions/SHA256SUMS at REV vs 2711674; {W18}/evidence/sums-runlog.json; LOG R17-SUMS-RUNLOG line",
    "REGISTRY": f"{SPOT}:144-146; {LANE}/SKILL.md rows citation-drift, go-route-compare, receipt-validate, pins, go-buildinfo-probe at REV",
    "S032": f"{SPOT}:147; {LANE}/corpus/SOURCES.md S032/S033 rows; {W18}/evidence/s032-digests.json",
}
for k, v in DEF.items():
    add(f"Truth{k}", "reviewer", f"""Attack whether R17-{k} is really discharged at REV, by substance not tokens: re-derive every
number/hash/claim in the correction from artifacts ({v}). Is any correction itself false or a new overstatement? Run
`python3 -I -B {T}/routed-defects.py --root {LANE} --rev {R}` and say whether its closure of this defect is deserved.""")
    add(f"Gate{k}", "reviewer", f"""Attack the routed-defects.py check set for R17-{k} ({T}/routed-defects.py): in a mkdtemp `git clone --no-local {LANE}`
(remove its origin remote first; never touch {LANE}) make the cheapest commit that flips R17-{k} closed without fixing the
defect, or that re-opens the defect while the tool still says closed. Report the diff and the tool output.""")
add("RoutedSelftestMut", "mutation-tester", f"""Mutation-test {T}/routed-defects.py: copy it to /tmp, apply ≥6 single-point mutations (one per defect's substance check, e.g. invert, drop a required token), run `--selftest` on each; list survivors (mutations the selftest does not catch).""")
add("RoutedBaselineRerun", "executor", f"""Re-run the C1 counting command at baseline and REV: `python3 -I -B {T}/routed-defects.py --root {LANE} --rev {B}` and `--rev {R}` and `--strict` variants; paste open counts, exits; confirm 6→0 and that each baseline-open check names a real gap.""")
add("Quality21Ground", "critic", f"""Attack QUALITY #21 ({LANE}/corpus/QUALITY.md row 21): is it grounded in a lesson with red-before ({LES} Mistakes row 1), or a restatement of #19? Would #21 have caught the r17 sentence? Run the red-before: `receipt-validate.py --require-mid-maps` on {W17}/runs/*/receipt.json (expect 1) and on {W18}/runs/*/receipt.json (expect 0).""")
add("QualityRowsIntact", "reviewer", f"""Check QUALITY rows 1-20 are byte-identical B→REV and row 21 has 4 cells and a resolvable why-cell: `git diff {B} {R} -- corpus/QUALITY.md`.""")
add("LessonMistakesAudit", "reviewer", f"""Audit {LES} `## Mistakes`: for every row check class vocabulary (/home/vgpnk/Projects/shokunin/CORPUS.md:171-178), evidence pointer resolves at REV, captured-by is right, and the fix is shown able to fail with a reproducing red command. Run each red command you can.""")
add("LessonGateAudit", "reviewer", f"""Audit {LES} `## Gate`: each admit/reject has resolvable evidence; each new SOURCES row has URL, date and a ≤25-word contiguous located quote; re-check each quote verbatim against the source.""")
add("R17Line90Claim", "reviewer", f"""The r18 lesson says `corpus/lessons/round-17.md:90` inherits the PINMAP overstatement and `round-17.md:88,122` the VALIDATE16 one. Verify those anchors at REV and whether every overstated site now has a named correction somewhere at REV.""")
add("ValidateRemapAttack", "critic", f"""Attack the R17-VALIDATE16 evidence: the remapped validation of the 8 da64646 receipts ({W18}/evidence/validate16/). Could the remap have validated pass-2 bytes or skipped checks (341 checks per receipt)? Reproduce one receipt's validation yourself from `git archive da64646` in mkdtemp.""")
# ---- C2 ----
add("LintRerun", "executor", f"""Re-run C2 counting: `python3 -I -B {T}/head-rev-lint.py --root {LANE} --rev {B}` and `--rev {R}` (+ `--strict`); paste live/fixture/annotated/excluded; check every annotated site really reads HEAD only to compare with the branch tip.""")
add("LintMutation", "mutation-tester", f"""In a mkdtemp clone of {LANE} (origin removed), for each of the three fixed files (.ufo/gates/citation-drift/citation-drift-probe.py, .ufo/gates/custody-pair/custody-pair.py, .ufo/waves/round-17/verify.py) restore its {B} bytes alone, commit, run head-rev-lint at that commit: each must report exactly 1 live site. Report per file.""")
add("LintBlindSpots", "reviewer", f"""Attack head-rev-lint's "0 live" at REV: search REV's scanned scope for HEAD-pinning forms it misses (git log -1, show HEAD, @, HEAD~0, runtime-built defaults, shell). List every miss with path:line and whether it is a live pin.""")
add("LintSelftestMut", "mutation-tester", f"""Mutation-test {T}/head-rev-lint.py --selftest with ≥5 single-point mutations (context classifier, annotation rule, wrapper detection); report survivors.""")
add("JjRedBeforeRerun", "executor", f"""Re-run `python3 -I -B {T}/jj-red-before.py --out /tmp/kr18w2-jjrb.json` and its --selftest; compare with {W18}/evidence/jj-red-before.json (14/14 held); confirm the lane's refs/heads/main is unchanged before/after and no file under {LANE} changed (`git -C {LANE} status --porcelain`).""")
add("JjSandboxSafety", "sentinel", f"""Security review of {T}/jj-red-before.py at REV: origin removal, env scrub, HOME/XDG isolation, rmtree target guard, -R on jj calls. Any path that could write {LANE} or the fleet repo? Cite lines.""")
add("RevpinReview", "reviewer", f"""Review {T}/revpin.py at REV: run --selftest and `--root {LANE}`; attack the `pushed` semantics (ancestor vs equality) and failure attribution.""")
add("CitationDriftReview", "reviewer", f"""Review the in-place change to .ufo/gates/citation-drift/citation-drift-probe.py (`git diff {B} {R} -- .ufo/gates/citation-drift/`): run --selftest; run the SKILL.md:448 strict argv at `--rev {R}` and at `--rev {B}`; confirm explicit-rev behaviour unchanged and new findings exit 2.""")
add("CustodyReview", "reviewer", f"""Review custody-pair.py change (`git diff {B} {R} -- .ufo/gates/custody-pair/`): run `selftest`; run `capture --out /tmp/kr18w2-c.txt` from cwd=/ and check repo-* headers; compare against the r17 receipt {W17}/custody/custody-r17.v2.txt with `verify` (expect MATCH semantics on stanzas, metadata headers ignored). Delete your /tmp files.""")
add("Verify17Review", "reviewer", f"""Review {W17}/verify.py change (`git diff {B} {R} -- .ufo/waves/round-17/verify.py`): the preflight must run before any write; prove in a mkdtemp clone with LANE constant swapped that an off-branch HEAD exits 2 before writing verification.json. Never run it in {LANE}.""")
add("Verify18Review", "reviewer", f"""Review {W18}/verify.py (round-18 pass harness) statically: does it pin source via revpin, refuse before running, cover every round-18 counting command and selftest, and avoid overwriting r17 evidence? List missing commands.""")
add("ControlsRerun", "executor", f"""Run no-harm controls: `python3 -I -B {W18}/controls.py {B} {R}` and `--selftest`; paste the summary; flag any changed blob outside the contracted set and any LOG/SCORECARD prefix break.""")
add("ControlsAttack", "reviewer", f"""Attack {W18}/controls.py: could a harmful change pass (e.g. editing a prior knowledge file besides the r17 appendable entry, deleting a SKILL table row, editing an S0xx immutable cell)? Demonstrate in a mkdtemp clone.""")
add("SkillDeletedLines", "reviewer", f"""Review every deleted/replaced SKILL.md line B→REV (`git diff {B} {R} -- SKILL.md`): was any cited table, decision or registry fact lost or weakened? Is each new registry row field-complete per PROTOCOL.md row fields (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:411-419)?""")
add("SkillJjSection", "reviewer", f"""Review SKILL.md section "Revision pins under jj — round 18" at REV: every claim grounded (S036, jj audit F1/F2, jj-red-before receipt); decision table actionable; no overclaim about origin/main.""")
# ---- C3 per-run re-derivation (15) ----
labels = [l.split("\t")[0] for l in open(W18 + "/predictions/carriers.tsv") if l.strip()]
for lab in labels:
    add(f"Run{lab.replace('-', '').replace('.', '')}", "reviewer", f"""Re-derive carrier run `{lab}` independently: from {W18}/runs/{lab}/logs/*/ghidra.log raw lines extract route (GoApiSnapshot INFO/WARN), `Go analysis failure`, `Invalid index:` / `Unable to read past EOF:` values; compare with the frozen prediction `git show {F}:.ufo/waves/round-18/predictions/{lab}.prediction.json`; check log binding (session path, target-<sha12>, MD5) and carrier sha256; run `python3 -I -B {W17}/tools/receipt-validate.py --require-mid-maps {W18}/runs/{lab}/receipt.json`. Verdict per field.""")
add("FreezeBeforeRun", "reviewer", f"""Attack "predictions frozen before the run": compare commit/push time of {F} (git log, `.git/logs/refs/remotes/origin/main`) with the earliest step timestamp in every {W18}/runs/*/receipt.json; confirm prediction blobs at {F} equal those at REV; any run artifact present at {F}?""")
add("DecisionRuleApply", "critic", f"""Apply the frozen rule `git show {F}:.ufo/waves/round-18/predictions/decision-rule.json` yourself to the observations in {W18}/runs/*/observation.json and logs: confirmed / refuted / unresolved? Attack whether the rule was weak enough to be unfalsifiable and whether D's held-out members were truly held out (emulator calibrated only on aether?).""")
add("EmulatorIndependence", "critic", f"""Attack {T}/swiss-misread.py: is there any hard-coded carrier-specific value (addresses, the indices 22386945/15606016/17645861) or tuning to the outcomes? Read the code at {F}; re-run it at {F} bytes on s1246-swiss-nethttp and kimi-webbridge and check outputs equal the frozen ones.""")
add("EmulatorMutation", "mutation-tester", f"""Mutation-test swiss-misread.py: copy {F}'s version to /tmp; mutate the bound struct size (88→112), the pkgPath follow, the name-flag test; for each, re-run on s1246-swiss-nethttp, s1250-swiss-nethttp, aether and report whether predictions change (they should) and whether --selftest catches it.""")
add("EmulatorSourceCheck", "revenger", f"""Independently from {SRCZIP} (GoMapType, GoType.getUncommonType, GoUncommonType, GoName, GoRttiMapper.resolveNameOff, MemoryByteProvider) confirm the H1 read chain produces `Invalid index: N` (not past-EOF) for s1246-swiss-nethttp; compute N from carrier bytes yourself.""")
add("KimiWebbridgeDerive", "revenger", f"""For /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge derive by your own byte parsing which named map type(s) produce `Invalid index: 15606016` under H1 (types base, SlotSize, the GoName at types+SlotSize, its pkgPath offset). Never execute it.""")
add("S1250NethttpSilent", "revenger", f"""Explain from bytes why s1250-swiss-nethttp is silent under H1 although it has the same 40-slot named maps (name at types+40: flags, pkgPath bit). Is the misread present but silent? Cite offsets.""")
add("AetherDualPath", "revenger", f"""Reconcile aether's retained stack (`{W18}/runs/calib-aether/logs/*/ghidra.log` lines 97-200, struct/interface frames) with the map-path claim in {KE}: is the entry's INFERENCE wording accurate? Which path does Ghidra's markup order reach first?""")
add("LogExtractNewFields", "executor", f"""Re-run `{W17}/tools/log-extract.py --selftest` and on all 15 r18 logs and 16 r17 logs; verify invalid_index_reads/eof_reads against `grep -nE` raw lines; confirm old fields of the 16 r17 logs are byte-equal to `git show {B}`'s extractor output.""")
add("CompareNewFields", "executor", f"""Re-run `{W17}/tools/compare.py --selftest` and compare on all 15 r18 pairs and 8 r17 pairs; r17 outputs must be byte-identical to the retained compare.json; report any difference.""")
add("ReceiptValidateRerun", "executor", f"""Re-run `{W17}/tools/receipt-validate.py --selftest` and `--require-mid-maps` over all 15 r18 receipts; tamper one copied mid map in /tmp copy of a run dir (rewrite paths) and show exit 1 with mid_map_sha256_mismatch.""")
add("CarrierRunSelftest", "executor", f"""Re-run `{W17}/tools/carrier-run.py --selftest` and `bash {W18}/run-carriers.sh --selftest`; check the runner selftest can fail (forced red on a /tmp copy).""")
add("CarrierRebuild", "executor", f"""Rebuild the 12 synthetic carriers with `OUT=$(mktemp -d) bash {W18}/carriers/build.sh` and `sha256sum -c` against {W18}/carriers/SHA256SUMS; confirm the receipts' carrier sha256_pre equal the sums. Never execute a carrier.""")
add("ProducerJson", "reviewer", f"""Check every {W18}/runs/*/producer.json: branch_tip equals {F}, tool sha256s equal the blobs at {F}; does any run lack it?""")
add("MidMapsRetained", "reviewer", f"""For every r18 receipt, recompute sha256 of each pins/mid-<n>.json and compare with map_sha256, and compare each map to pins_pre with {W17}/tools/pins.py compare; report totals.""")
add("RunHygiene", "sentinel", f"""Review the r18 runs for leaks: any session.json/bridge token copied under {W18}/runs? leftover /tmp/kr17-rea-* dirs? env keys recorded in receipts (child_env_keys)? Report.""")
add("KnowledgeEntryReview", "critic", f"""Attack {KE} at REV: every number (15/15, 22 mid maps, 11 non-D, line numbers 97/177/408/451/73/206, Evidence IDs) re-derived; overclaims vs QUALITY #5/#7/#9/#21; provenance trio first; sources cited exist.""")
add("KnowledgeDecisionTable", "reviewer", f"""Review the decision table in {KE} and SKILL.md "Swiss-map misread replay — round 18": is each row supported by observations (counts) and labelled where INFERENCE?""")
add("R17EntryCorrection", "reviewer", f"""Review the appended "Round-18 correction" in {K17}: filed bytes 1-198 unchanged vs {B}; each correction line true (29 mid checks, blob ids bc964ac/c536e3e).""")
add("ReplicateAetherId", "reviewer", f"""The entry says aether's r18 Evidence ID equals the r17 second-pass ID. Verify from {W18}/runs/calib-aether/receipt.json and {W17}/runs/pro-aether/receipt.json; also check r17's replicate expectation file to explain the r17 first/second-pass difference.""")
add("IntermediateFallback", "reviewer", f"""kimi-webbridge go1.24.13 → `Falling back from 1.24.13 to 1.24.6`: verify in its log and that r17 knowledge "Not examined" listed this route as unexercised ({K17}:185-187). Is the README/LOG "first observed" claim correct across the corpus (`git grep -n 'Falling back from 1.24' {R}`)?""")
# ---- frontier ----
for sid, what in [("S033", "PR #9348 head via git ls-remote, .patch digest stability"),
                  ("S034", "https://go.dev/doc/go1.24 runtime section lines 571-573 and sha256"),
                  ("S035", "/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi map files sha256 and anchors"),
                  ("S036", "jj v0.45.1 docs/git-compatibility.md sha256 and lines 114-116")]:
    add(f"Reopen{sid}", "scout", f"""Re-open SOURCES row {sid} ({LANE}/corpus/SOURCES.md at REV): {what}. Verify anchor, tier, scope, teaches, quote in {LES} Gate verbatim (≤25 words). Verdict agree/disagree with reasons.""")
add("CensusRerun", "scout", f"""Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` and the frozen manual census commands in /home/vgpnk/Projects/shokunin/CORPUS.md:133-148 from {LANE}; paste outputs/exits; explain W04.""")
add("SearchLogAudit", "reviewer", f"""Audit the round-18 search-log entry in {LANE}/corpus/SOURCES.md: are identified/screened/included/excluded counts (11/11/4/7) consistent with the named sources and w1 reports under {W18}/w1/?""")
add("PathsAudit", "reviewer", f"""Audit SOURCES `## Paths` changes B→REV: S032 removed from the route path, two new paths; every id resolves; no row cell other than allowed fields changed (`git diff {B} {R} -- corpus/SOURCES.md`).""")
add("UsedByResolve", "scout", f"""For every mined row in {LANE}/corpus/SOURCES.md at REV, check each used-by path exists at REV (git cat-file -e); list missing.""")
# ---- calibration / trends / adjacency ----
add("ClaimsSeparable2", "critic", f"""Re-judge separability at REV: is C1 still coupled to C3 (routed-defects PINMAP requires a round-18 receipt with mid maps)? Is C2 separable? Recommend the honest wording of each claim's independence.""")
add("ScorecardAudit", "reviewer", f"""Audit SCORECARD.md round-18 section at REV (append-only vs {B}: `git diff {B} {R} -- SCORECARD.md` must have 0 deletions); every number has its command.""")
add("LogAudit", "reviewer", f"""Audit LOG.md round-18 entry at REV: append-only (0 deletions vs {B}); every claim cites evidence; seat counts and role mix match {W18}/wave1-dispatch.json and {W18}/w1/ (count reports).""")
add("TrendVerdicts", "critic", f"""Judge the three LEARNING trends (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:31-38) for round 18 from REV evidence: expansion (is the Swiss-map entry on uncovered ground per {LANE}/corpus/README.md and PROVINCE.md?), quality, discernment. Give verdicts with reasons.""")
add("AxisHarmCheck", "reviewer", f"""Look for harm on any axis (coverage, depth, calibration, operability, freshness, adjacency) B→REV: any admitted entry now false, any proxy decreased, any tool behaviour regressed for explicit-rev callers?""")
add("ShonenLines", "reviewer", f"""Read {LANE}/SHONEN.md and propose the round-18 `[~]` line per box with a resolvable evidence pointer at REV; never `[x]`.""")
add("SiblingOverlap2", "connector", f"""Sibling overlap at REV: does any other lane (/home/vgpnk/Projects/shokunin/*-shokunin) hold Go map/Swiss/Ghidra-Go knowledge or claim jj branch-tip tooling the lane now registers? Report contested scope.""")
add("ProvinceAccuracy", "connector", f"""Check {LANE}/PROVINCE.md is still accurate after round 18 (Swiss-map replay ground, jj tooling): should a frontier/core line change? Propose exact text, cite lines.""")
add("CoverageMapRow", "connector", f"""Check the README coverage map row 35 edit (`git diff {B} {R} -- corpus/README.md`) is accurate and that every knowledge file at REV is indexed (count files vs indexed names).""")
add("OpenRoutedQueue", "connector", f"""List every routed defect from verifier spot-checks round-12..17 still open at REV (the r18 lesson names two r12 items as open); confirm or add.""")
add("WaveEvidenceComplete", "scout", f"""Check wave-1 evidence at REV: {W18}/wave1-dispatch.json task count 89 equals reports under {W18}/w1/ (names), registration recorded; list seats without reports.""")
add("MisrootSweep", "scout", """Run `git -C /home/vgpnk/Projects/shokunin status --porcelain`; list untracked files whose content names kaidoku or round-18 (grep -l). Read-only.""")
add("ReaPinStill", "scout", """Confirm the r18 receipts' REA argv used rea-agents@6.5.0 (grep receipts) and the cached package integrity is unchanged (`npx -y rea-agents@6.5.0 --version`).""")
add("SimplifyR18Tools", "simplifier", f"""YAGNI review of the round-18 tools at REV ({T}/*.py, {W18}/measure.py, controls.py, verify.py, gen-predictions.py): duplicated helpers, dead options; list deletions that preserve every counting command.""")
add("SimplifyR17Edits", "simplifier", f"""YAGNI review of the in-place round-17 tool edits B→REV (`git diff {B} {R} -- .ufo/waves/round-17/tools/`): any added branch never exercised by a selftest or a run?""")
add("ReportDraft", "scribe", f"""Draft the round-18 report sections "Work performed" and "Before → after measurements" from REV evidence only ({LANE}/LOG.md round-18 entry, SCORECARD round-18, {W18}/claims.json amendments). Put the draft under `## Draft` in your report; every sentence cites path:line or a command.""")
add("ReportSources", "scribe", f"""Draft the round-18 report "Sources & frontier" section: rows before→after (32→36), tiers added, rows touched old→new, census outputs, frontier advanced. Under `## Draft`, each fact cited.""")
add("ScorecardMeasuredDraft", "scribe", f"""Draft the SCORECARD round-18 claim table rows (C1 calibration, C2 operability, C3 depth) with before→after, counting command and measured revision {R}, from: routed-defects open_count 6→0, head-rev-lint live 3→0 (fixture 8→15, annotated 0→6), measure.py C3 compare_jsons_with_extra 0→15. Under `## Draft`.""")
add("CapabilityCandidate", "critic", f"""Is "byte-level Ghidra Go map-misread prediction (swiss-misread.py) confirmed on held-out carriers" a capability-table entry per AXES.md §Capabilities (/home/vgpnk/Projects/shokunin/AXES.md:57-64), or double-counting C3? Decide with reasons.""")

spec = {
    "wave": "kaidoku-r18-w2",
    "axes": ["calibration", "operability", "depth"],
    "reportDir": ".ufo/waves/round-18/w2",
    "maxLanes": 100,
    "context": (
        "# Goal\nKaidoku round 18 wave 2 (falsify). Attack what wave 1 produced at lane revision " + R +
        f" (baseline {B}; C3 predictions frozen at {F}). Claims: {W18}/claims.json (see `amendments`). "
        "You are an author-side advisory seat, never an outside reviewer. REA CLI only (`npx -y rea-agents@6.5.0`); never xd://mcp__rea_* devices.\n"
        "# Contract\nLeaf: never delegate (executors may spawn at most one read-only labrat). Never run REA analyze/search/decompile or Ghidra. "
        "Never execute carrier binaries. Write ONLY your report. Never edit any lane file. The lane is jj-colocated: never run `jj` or any git write "
        "(add/commit/stash/checkout/reset/rebase/push) in the lane; read-only git only; writes and jj only inside a mkdtemp clone whose origin remote you remove first. "
        "Never write the fleet repo /home/vgpnk/Projects/shokunin outside the lane dir. Every `Report:` trailer path is relative to "
        f"{LANE} — write it at {LANE}/<that path>. Run python as `python3 -I -B`. Keep reports concise; cite path:line; label observation vs inference; "
        "never fabricate output. Message only KaidokuR18 if blocked; never the orchestrator, never agent://all.\n"
        "# Host safety\nYou and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md "
        "first (official channels; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are "
        "PAUSED host-wide (read-only `pacman -Q*` queries are fine); install via `uv tool`/`npx`/an official binary in ~/.local/bin "
        "instead, or report the need. When the pause lifts: before any `pacman -S` run `pacman -Sp --print-format '%n %v' <pkgs>` "
        "and proceed only if every listed package is not installed; never -Sy/-Syu/-U/-R, downgrade, or restart a host service. "
        "Never open/copy/query ~/.omp/agent/agent.db* or credential/auth files; never launch omp CLI processes; never modify "
        "client routing or host services. Prefer no installs."),
    "items": items,
}
with open(os.path.join(HERE, "wave2-spec.json"), "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
from collections import Counter
print(len(items), dict(Counter(i["role"] for i in items)))
