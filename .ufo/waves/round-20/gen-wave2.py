#!/usr/bin/env python3
"""Generate the round-20 wave-2 (falsify) spec (L1-authored). Usage: gen-wave2.py <SRC-commit>."""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W17 = LANE + "/.ufo/waves/round-17"
W18 = LANE + "/.ufo/waves/round-18"
W19 = LANE + "/.ufo/waves/round-19"
W20 = LANE + "/.ufo/waves/round-20"
B = "14f0260ad319ecc26994381b2415d5a999003375"
F = "808cbb31a1e24656da5ba4967497e602fbca7415"
S = sys.argv[1]
CON = W20 + "/contract.md"
L20 = LANE + "/corpus/lessons/round-20.md"
SPOT = LANE + "/corpus/lessons/round-19-verifier-spotcheck.md"
REA = "npx -y rea-agents@6.5.0"
WABT = "/home/vgpnk/.local/opt/wabt-1.0.42/bin"
K = LANE + "/corpus/knowledge/"
with open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")) as f:
    DIRECTIVE = f.read()

HDR = (f"Baseline B={B}; C3 freeze F={F}; measured source S={S} (read Git objects at S with `git -C {LANE} show {S}:<path>`, "
       "never trust the working tree for rev-scoped claims). ")
RO = ("# Acceptance\nRead-only: write only your report. Start with a one-line verdict `HOLDS` / `FALSIFIED` / `PARTIAL` for "
      "the thing you attack, then the evidence: exact commands with exit codes, path:line anchors, observation vs "
      "inference. Never fabricate. Scratch only under mkdtemp outside the lane.")
MT = ("# Acceptance\nWork in your own clone `/tmp/kr20w2-<YourSeatName>` of LANE checked out at S (contract `Writers`); "
      "never write the lane. Apply each mutant, run the named command, record exit and the finding that should catch it, "
      "restore. Report a table mutant → expected → observed → killed/survived. One-line verdict first.")

items = []


def add(name, role, target, acc=RO):
    items.append({"name": name, "role": role,
                  "prompt": "/skill:godspeed\n" + DIRECTIVE + "\n# Target\n" + HDR + target.strip() + "\n" + acc})


T = W20 + "/tools"
# ---- re-run every counting command (reviewers) ----
add("RerunRoutedB", "reviewer", f"Re-run `python3 -I -B {T}/routed-r19.py --root {LANE} --rev {B} --strict`; expect 11 open, exit 1. Paste JSON summary.")
add("RerunRoutedS", "reviewer", f"Re-run `python3 -I -B {T}/routed-r19.py --root {LANE} --rev {S} --strict --live`; claim is 10/11 closed at S with only D5 open (its final-census record lands in the last lane commit), exit 1. For every item paste named/substance/why; any other open item falsifies.")
add("RerunVerbB", "reviewer", f"Re-run `python3 -I -B {T}/verb-coverage.py --root {LANE} --rev {B}`; claim 128/153 mentioned, 0/5 targets exercised.")
add("RerunVerbS", "reviewer", f"Re-run verb-coverage at {S}; claim 133/153, 5/5 exercised with bound_evidence paths. Open each bound file and confirm the ev id, operation token and success status are really in its bytes.")
add("RerunMeasureS", "reviewer", f"Re-run `python3 -I -B {W20}/measure.py {S} --freeze {F}` (read `--help` first); report c1/c2/c3 fields, especially c3.first_failure_bound and matched.")
add("RerunControls", "reviewer", f"Re-run `python3 -I -B {W20}/controls-r20.py {B} {S}`; paste the verdict and every changed-cell / protected-change line.")
add("RerunCensusTip", "reviewer", f"Run `python3 -I -B {LANE}/.ufo/gates/c1-census-v10.py --root <git archive {S} export in mkdtemp>`; claim VERDICT PASS exit 0. Also run it at B (expect FAIL undeclared=2).")
add("RerunSourcesCensus", "reviewer", f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` and the CORPUS.md manual census commands (/home/vgpnk/Projects/shokunin/CORPUS.md:133-148) on `git show {S}:corpus/SOURCES.md`; expect 47 rows, exit 0, W04 only for S033/S047.")
add("RerunTimestampsW20", "reviewer", f"Run `python3 -I -B {T}/evidence-timestamps.py --root {LANE} --rev {S} --path .ufo/waves/round-20 --strict` and over corpus/lessons, SCORECARD.md, LOG.md; any finding falsifies QUALITY #23 compliance of this round.")
add("RerunSelftests", "reviewer", f"Run every round-20 tool selftest at S from a `git archive {S}` export (tools/*.py, measure.py, controls-r20.py, verify.py, run-carriers.sh --selftest) plus the in-place edited gates (custody-pair `selftest --scratch <mkdtemp under /var/tmp>`, citation-drift-probe --selftest, receipt-validate, head-rev-lint, wave-outcomes, jj-red-before, c1-census-v10 --selftest). Table tool → last line → exit.")
# ---- re-open every new SOURCES row ----
for pair in (("S040", "S046"), ("S041", "S042"), ("S043", "S044"), ("S045", "S047")):
    a, b = pair
    add(f"Reopen{a}{b}", "scout", f"Re-open SOURCES rows {a} and {b} yourself (`git show {S}:corpus/SOURCES.md | grep -E '^\\| ({a}|{b}) '`), fetch/open each source now, and check each quote in `{L20}` Gate table byte-for-byte at the stated location; check tier/kind/scope/anchor honesty and that used-by paths exist at S. One verdict per row.")
# ---- review each new/changed entry ----
for slug in ("2026-10-20-r20-wasm-interfaces", "2026-10-20-r20-rizin-command-observation",
             "2026-10-20-r20-objdump-architecture-list", "2026-10-20-r20-harmony-application-graph"):
    add("Entry" + slug.split("r20-")[1].split("-")[0].capitalize() + "Claims", "reviewer",
        f"Check every factual sentence of `{K}{slug}.md` at S against the retained files it cites (ev ids, sha256, counts, statuses); list each unsupported or overstated sentence with the contradicting byte.")
for slugs in (("2026-10-20-r20-wasm-interfaces",), ("2026-10-20-r20-rizin-command-observation",),
              ("2026-10-20-r20-objdump-architecture-list", "2026-10-20-r20-harmony-application-graph")):
    add("Entry" + "".join(s.split("r20-")[1].split("-")[0].capitalize() for s in slugs) + "Quality", "critic",
        "Judge " + " and ".join(f"`{K}{s}.md`" for s in slugs) + f" against `{LANE}/corpus/QUALITY.md` rows 1-25 (criteria 4-12, 25 especially): observation/inference labels, what was not examined, carrier identity. Admit or reject each with reasons.")
add("EntryPeErratum", "reviewer", f"Check the round-20 erratum appended to `{K}2026-10-13-pe-surface.md`: does it preserve the original bytes as a prefix (`git show {B}:` vs `{S}:`), and is the re-run sweep reproducible now?")
# ---- C2 independent replays ----
add("ReplayWasmInspect", "executor", f"Re-run `REA_WABT_BIN_DIRECTORY={WABT} {REA} inspect-wasm-artifact /opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/qcms_bg.wasm --format json` in mkdtemp; compare evidence_id, sections/imports/exports with `{W20}/evidence/c2/wasm-inspect/qcms/`.", RO)
add("ReplayWasmCompare", "executor", f"Re-run the synthetic compare from `{W20}/evidence/c2/wasm-compare/compare-synth-both.receipt.json` argv (rebuild inputs from the retained files) in mkdtemp; compare evidence_id and summary.", RO)
add("ReplayRizin", "executor", f"Re-run `{REA} execute-rizin-command /usr/bin/jq iI --format json`; compare with `{W20}/evidence/c2/rizin/jq-iI-1.stdout` (ev id, bytes). Also replay `iI; iS` on the PE path in `{W20}/evidence/c2/rizin-pe/06-semicolon-chain/receipt.json` and settle whether `;` chains.", RO)
add("ReplayObjdumpArch", "executor", f"Re-run `{REA} list-objdump-architectures --format json`; compare ev id and stdout with `{W20}/evidence/c2/objdump/architectures-json/` and `objdump -i`.", RO)
add("ReplayHarmony", "executor", f"Rebuild the Stage HAP from `{W20}/evidence/c2/harmony/carrier-recipe.json`, confirm its sha256 equals the retained carrier, re-run inspect-artifact + project-harmony-application-graph per the retained receipts; compare ev ids.", RO)
# ---- C1 per-item attacks ----
add("AttackD1", "scout", f"Attack R19-D1: run S's custody-pair selftest with scratch (a) inside a Git worktree whose `.git` is a FILE (worktree/submodule style), (b) a symlink into the lane, (c) /var/tmp; does the refusal and cleanup hold? Check the lane has no nested `.git` under `.ufo` (`find {LANE}/.ufo -name .git`).")
add("AttackD2", "scout", f"Attack R19-D2: build a mkdtemp fixture repo with timestamps in formats the lint might miss (`T±HHMM`, space+Z, fractional, JSON-escaped) introduced in commits with known committer times; run S's evidence-timestamps.py and list misses. Also check the lint uses committer not author time.")
add("AttackD3", "scout", f"Attack R19-D3: verify `{W20}/evidence/carrier-guard*/` records at S: arm/check/disarm present (the L1 disarmed all three guards after the runs), check records cover every run label's instant (compare times with runs/run-log.txt), carrier set equals predictions/carriers.tsv, live modes of the real files now equal disarm.json `mode_restored`. Never execute a Go binary.")
add("AttackD3Disarm", "scout", f"Attack the recovery change to routed-r19 `_s_d3` at S (a valid disarm.json later than every retained check replaces the fresh check). In your own clone of LANE at S, commit (a) a disarm.json whose taken_at_utc precedes the last check, (b) one with a different carrier set, (c) one with action!=disarm, (d) delete disarm.json while modes are restored; run routed-r19 --root <clone> --rev <commit> --strict for each; D3 must go open in all four. Table.")
add("AttackD4", "critic", f"Attack R19-D4: in a mkdtemp export of S, plant a new undeclared rea pin block in SCORECARD.md and a live pin inside the new DATED rows; does the census fail the first and what does it do with the second? Judge whether the re-key is declaration or suppression.")
add("AttackD5", "critic", f"Attack R19-D5. In your own clone of LANE at S (branch main at S): run `python3 -I -B {T}/final-census.py --root <clone> --out-dir <clone>/.ufo/waves/round-20/verify`, commit only its two outputs, run routed-r19 --rev <that commit> --strict (D5 should close). Then forge: record rev != parent, an extra changed path in the record commit, a wrong stdout_sha256, exit 1, argv as flat strings; D5 must stay open for each. Describe what the closure must check at the final tip.")
add("AttackD6a", "scout", f"Attack R19-D6a: at S run head-rev-lint.py and confirm the nested class names round-17 verify.py:83 and round-18 revpin.py:113; build a fixture with a 3-deep helper chain and a decoy name collision; report misses.")
add("AttackD6b", "sentinel", f"Attack R19-D6b and its recovery change (work base /fast/scratch, PrivateTmp=yes, optional --host-home read-only HOME): probe S's revexec.py sandbox with harmless payloads: write to $HOME (with and without --host-home), write to host /tmp (must not reach the host), write elsewhere under /fast/scratch outside the work dir, connect TCP 127.0.0.1, connect AF_UNIX `/run/user/1000/bus`, read ~/.ssh listing (names only, no content). Report which are refused and whether --host-home widens anything beyond read access.")
add("AttackD6c", "scout", f"Attack R19-D6c: craft pointer-table/expected pairs with slugs `..%2fx`, unicode dot variants, a symlinked snapshot-dir, and a hardlink outside; run S's citation-drift-probe.py; report any escape.")
add("AttackD6d", "scout", f"Attack R19-D6d: craft receipts (object and list shaped) where `analyze` follows a decoy `rea-agents@` token in another position, uses `npx --yes`, or `rea-agents@latest`; run S's receipt-validate.py --require-mid-maps; also re-validate all round-19 pass2 receipts and the round-20 run receipts.")
add("AttackD6e", "scout", f"Attack R19-D6e: feed S's wave-outcomes.py flat maps with seats named `causes`, `wave`, `seats`, and a wrapped map containing a seat named `causes`; report miscounts.")
add("AttackD6f", "scout", f"Attack R19-D6f: are the two new jj_ cases red when their guarded behaviour is removed (mutate in a /tmp clone)? Report per case.")
# ---- C3 attacks ----
add("AttackFreezeOrder", "reviewer", f"Prove or refute: no analyze ran before F was pushed. Compare F's committer time (`git log -1 --format=%cI {F}`), the helper's remote state, `{W20}/runs-start.txt` and the first `start` line of `{W20}/runs/run-log.txt`; check `git diff {F} {S} -- .ufo/waves/round-20/predictions` is empty.")
add("AttackPredictionBlobs", "reviewer", f"For each of the 19 labels, check `{W20}/predictions/<label>.prediction.json` first_failure equals `predictions/swiss-misread-v2/<label>.json` first_failure.h1 at both F and S, and SHA256SUMS verifies.")
add("AttackReceipts", "reviewer", f"Run `python3 -I -B {W17}/tools/receipt-validate.py --require-mid-maps {W20}/runs/<label>/receipt.json` for all 19 labels at S (from a git archive export if paths allow); report exits and findings.")
add("AttackLogBinding", "reviewer", f"For each label confirm the compared ghidra.log is bound to its run (session path + carrier digest prefix in the log bytes, sha256 in the receipt) — QUALITY #20.")
add("AttackFirstFailureOracle", "scout", f"Independent oracle: for every `{W20}/runs/*/logs/*/ghidra.log`, grep -n the first `Go analysis failure` / `Failed to read Go info` line and its `Invalid index`/EOF cause; compare with `{W20}/runs/<label>/compare-ff.json` observed objects. Table.")
add("AttackCompareRerun", "reviewer", f"The in-run compare used the wrong prediction file (lesson Mistakes 6). Re-run `python3 -I -B {T}/compare-first-failure.py --prediction {W20}/predictions/swiss-misread-v2/<label>.json --log <bound log> --extractor {T}/first-failure-extract.py` for all labels from F's tool bytes (`git show {F}:...`); confirm the retained re-run records match.")
add("CriticC3Verdict", "critic", f"Given the retained C3 outcomes at S (match count k/19, which D labels failed, which silent labels failed), is the depth claim `improved`? Is the forecast non-trivial (an all-silent baseline's score)? Could any go1.24.6 outcome have been known before F (round-18 inspect-go-binary records, round-18 synthetic s1246 logs with index 22386945), weakening held-out status per label? What may and may not be claimed in the knowledge entry?")
add("MutateEmulatorV2", "mutation-tester", f"Mutate S's swiss-misread-v2.py: remove the variadic mask (both sites), invert first_failure null/non-null, shift the uncommon offset; for each, run `--selftest` and the retro (`{T}/retro-v2.py --v2-dir <mutant outputs> --pass2-dir {W19}/runs/pass2 --extractor {T}/first-failure-extract.py`). Killed/survived table.", MT)
add("MutateCompareFF", "mutation-tester", f"Mutate S's compare-first-failure.py (ignore index, ignore kind, treat null as match-anything, drop envelope unwrap) and first-failure-extract.py (take first ERROR line, include AnalysisTaskWrapper); run selftests and the 19-label compare. Killed/survived.", MT)
add("MutateRouted", "mutation-tester", f"Mutate the S tools routed-r19.py checks: for each of D1..D6f revert the corresponding fix in a clone (e.g. restore custody-pair's no-refusal, remove slug check) and commit to the clone; run routed-r19 --rev <clone commit> --strict; does the item go open? Table.", MT)
add("MutateGuardsAndLint", "mutation-tester", f"Mutate carrier-guard.py (check ignores mode, ignores ctime), evidence-timestamps.py (author time, skip JSON), verb-coverage.py bound_evidence (drop operation token, drop refusal filter); run each selftest and the real measurement at S. Killed/survived.", MT)
# ---- admission critics ----
add("CriticAdmitC1", "critic", f"Judge C1 admission: 11→0 with substance; QUALITY 22→25 with rows 1-22 byte-identical (`git diff {B} {S} -- corpus/QUALITY.md`); census PASS. Any item closed only by tokens? Any harm?")
add("CriticAdmitC2", "critic", f"Judge C2 admission: 128→133/153 mentioned, 5/5 bound exercised. Is each target genuinely uncovered ground (no earlier entry held it)? Is the coverage map at 100% (controls)? Which target is weakest (pathless objdump, synthetic HAP)?")
add("CriticNoHarmS", "critic", f"No-harm at S: LOG/SCORECARD prefix, prior lessons unchanged, r17-19 runs/predictions unchanged, in-place tool edits keep old selftests, README Frontier coordinates (:175, :180) and pointer-table entries still resolve (`citation-drift-probe.py` strict at S). Report any harm.")
add("CriticSeparabilityS", "critic", f"At S, is each claim verifiable with the others reverted? Especially: C3 measurement depends on the D6d receipt-validate edit; C1 D3 depends on carriers.tsv. Rule each.")
add("CriticTrendsS", "critic", f"Propose evidence-backed trend verdicts (expansion, quality, discernment) for round 20 at S per LEARNING.md; name the strongest reason each could be `harmed`.")
add("CriticLesson", "critic", f"Attack `{L20}` Mistakes rows: is each fix shown able to fail with the failure text retained? Which row's red-before is only asserted? Is any mistake of this round missing (sweep w1 reports for errors the lesson omits)?")
add("CriticQuality2325", "critic", f"Attack QUALITY #23-#25 at S: grounded in the cited lessons? duplicates? would they have caught the incidents? any vacuous clause?")
add("CriticFrontierStepS", "critic", f"Frontier-step conformance at S: SOURCES rows opened this round with Gate quotes, census before/after, mined mistake with fix, sourced claim citing S###. Any defect?")
# ---- other reviewers ----
add("ReviewScorecardR20", "reviewer", f"Review the round-20 SCORECARD section at S (append-only; claims, before→after, commands, measured commits). Every number re-derivable? Any X.Y.Z token outside census scope?")
add("ReviewLogR20", "reviewer", f"Review LOG.md round-20 entries at S: append-only vs B, every entry cites evidence, no superseded claim left standing.")
add("ReviewSkillRowsR20", "reviewer", f"Review the new SKILL.md registry rows (routed-r19 … round20-measure) at S against the actual CLIs (`--help`) and PROTOCOL Gate standard fields.")
add("ReviewProvinceR20", "reviewer", f"Review PROVINCE.md `Round-20 additions to Core` at S: every surface resolves; no cross-domain bleed; claims match knowledge entries.")
add("ReviewReadmeR20", "reviewer", f"Review corpus/README.md at S: new coverage row on former blank line 69, Archives row extension; command A (every knowledge file mapped) and that :175/:180 pointers still hold.")
add("ReviewWaveRecords", "reviewer", f"Recount attempt-1 W1 from committed records at S: `{W20}/wave1-registry.json` (100 spawn members with agent ids), `{W20}/w1/swarm-registry.json` (0 assigned: pre-record copy), `w1/*.md`; seats with/without reports (L1 count: 98 reports; ConnSiblingHarmony and ConnJjSelftests reportless, transcripts end `aborted`); per QUALITY #22 each reportless seat needs a cause. Check `wave1-dispatch-attempts.json`. Also list every seat name cited in `{L20}`, SCORECARD round-20 and the knowledge entries; each must have a report in `{W20}/w1/`.")
add("ReviewRecoveryReuse", "reviewer", f"Attack the recovery reuse: attempt 1 landed d1d981d..aad0869 and checkpoints aa78b0d/7a1e0df (pushed, 'admission pending'); attempt 2 landed 81c2021 and later commits up to S. For each checkpoint-only artifact (`w1/patches/RoutedR19Fix.patch`, the C3 knowledge entry, SOURCES used-by appends, README row, measure.py hunk, the >1 MiB Wasm patches) state whether S uses it and whether it was re-verified (re-run, not trusted). Verify `git diff aa78b0d {S} -- .ufo/waves/round-20/tools/routed-r19.py` equals RoutedR19Fix.patch plus the named recovery hunks only; flag any check weakened.")
add("ReviewGuardRestore", "sentinel", f"The guarded Go toolchains were disarmed by the L1 before S. Check every `{W20}/evidence/carrier-guard*/disarm.json` at S vs live `stat -c %a` of each manifest path and each arm.json `mode_before`; flag any still-cleared or wrongly restored mode. Never execute.")
# ---- scouts on residual / adjacency ----
add("ScoutRizinShell", "scout", f"Settle the contradiction in `{K}2026-10-20-r20-rizin-command-observation.md`: does `{REA} execute-rizin-command /usr/bin/jq '!true'` run a shell (use only `!true`, never other commands)? Report exit and raw_result; it decides the entry's shell-escape wording.")
add("ReviewInstallRecordWabt", "scout", f"Find whether the WABT 1.0.42 install at {WABT} matches the lesson record: binary versions, the archive sha256 `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131` against the GitHub release `.sha256` asset (fetch it now), and that it is not on PATH.")
add("ConnSiblingOverlapS", "connector", f"Re-scan sibling lanes at the time of S for WASM/rizin/objdump/HarmonyOS ownership; confirm kaidoku's new Core rows do not absorb sibling ground.")
add("ConnFleetRefs", "connector", f"Do any sibling lanes cite kaidoku files changed in place this round (custody-pair, citation-drift, receipt-validate, head-rev-lint, wave-outcomes, jj-red-before, c1-census-v10)? A behaviour change there could affect them; list references.")
add("ScribeShonen", "scribe", f"Draft the SHONEN lines for round 20 (four boxes per `{LANE}/SHONEN.md`) as `[~]` with resolvable pointers at S; do not mark `[x]`.", RO)

spec = {
    "wave": "kaidoku-r20-w2",
    "axes": ["calibration", "coverage", "depth"],
    "reportDir": ".ufo/waves/round-20/w2",
    "maxLanes": 100,
    "context": (
        "# Goal\nKaidoku round 20 wave 2 (FALSIFY): attack what wave 1 and the L1 produced. Claims: "
        f"{W20}/claims.json; contract {CON}; lesson {L20}. You are an author-side falsifier seat, never an outside "
        "reviewer. Every item names what it attacks; report HOLDS/FALSIFIED/PARTIAL first. REA CLI only via "
        "`npx -y rea-agents@6.5.0` (never xd://mcp__rea_* devices; never edit ~/.omp/agent/mcp.json).\n"
        "# Contract\nLeaf: never delegate (executors may spawn one read-only labrat). Never execute any Go toolchain "
        "binary; never run REA analyze/search/decompile or Ghidra on go-1.24.6 files. Read-only seats write only their "
        "report; mutation-testers work in their own /tmp clone. Scratch only under mkdtemp outside the lane. Never run "
        "`jj` or git writes in the lane; never write the lane beyond your report; never write the fleet repo "
        "/home/vgpnk/Projects/shokunin outside the lane dir, sibling lanes, .ufo/state, MANIFEST.json or client "
        f"configs. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Concise; "
        "path:line anchors; observation vs inference; never fabricate; timestamps from the clock. Final message at "
        "most 6 lines. Message only KaidokuR20Recovery (the round-20 recovery L1) if blocked; never agent://all.\n"
        "# Host safety\nYou and every seat may install or upgrade tools that help the task — read "
        "/home/vgpnk/.omp/agent/RULES.md first (official channels; record tool/version/channel/reason). pacman guard: "
        "ALL pacman transactions are PAUSED host-wide (read-only `pacman -Q*` fine); install via `uv tool`/`npx`/an "
        "official binary in ~/.local/bin, or report the need. When the pause lifts: before any `pacman -S` run `pacman "
        "-Sp --print-format '%n %v' <pkgs>` and proceed only if every listed package is not installed; never "
        "-Sy/-Syu/-U/-R, downgrade, or restart a host service. Never open ~/.omp/agent/agent.db* or credential files; "
        "never launch omp CLI processes. Prefer no installs."),
    "items": items,
}
with open(os.path.join(HERE, "wave2-spec.json"), "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
print(len(items), dict(Counter(i["role"] for i in items)))
