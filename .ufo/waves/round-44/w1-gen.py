#!/usr/bin/env python3
"""Generate round-44 wave-1 spec, dispatch and ready files (L1 artifact)."""
import json, os, hashlib

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-44")
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
MILE = "Round 44 wave 1: pre-freeze build, oracle freeze, counter port, calibration rubric, attack of the draft"
REPORT = ".ufo/waves/round-44/w1"

CTX = """# Target
kaidoku-shokunin round 44, wave 1 = PRE-FREEZE build, oracle freeze, counter port, calibration rubric, source opening and attack of the draft. Lane root (absolute): /home/vgpnk/Projects/shokunin/kaidoku-shokunin. L1 = KaidokuR44 (integration owner; holds the canonical section-3 planner seat — the wave validator rejects `planner` as a swarm role, so bounded planning data-walks ride scouts/connectors/revengers; recorded in plans/round-44-claims.md). Base c29360e3ba5381a5ab69e372d0d9577970f85018 (lane main). Read the DRAFT claims FIRST: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-44-claims.md.

# Contract
- Fresh-start posture: claims are declared narrow and falsifiable; every claim carries a do-nothing control scored before data (prompt §9). Do NOT widen scope.
- R44-C1 (coverage): `squashfs_v1`+`squashfs_v2` (both byte orders) through REA 6.5.0 `extract-firmware` → Core on 4 committed unblob 26.6.4 fixtures; independent oracle = `/usr/bin/unsquashfs` (squashfs-tools 4.7.5) + the unblob `__output__` expected trees. Handler binding is per-carrier EXACT equality, never prefix.
- R44-C2 (calibration): a frozen `tools/round-44/c2-rubric.json` of enumerated self-assessment statements across SCORECARD.md/SHONEN.md/corpus/README.md; `tools/round-44/c2-counter.py` re-derives each asserted value at REV and reports mismatches. If the wave-1 census finds ZERO mismatches at base, the C2 claim STOPS (honest stop) — report that rather than loosening.
- Every score/check receipt you write carries your seat name, the command, exit code, stdout sha256 and wall time; honest capture beats a pass (QUALITY §failure-honesty).
- Artifacts go to .ufo/waves/round-44/w1/<Seat>/ ; tools you author go to .ufo/waves/round-44/w1/artifacts/<Seat>/ (the L1 installs them under tools/round-44/). Never write outside the lane tree except your own scratch under /fast/scratch/hyaku/kaidoku-r44/ or $HYAKU_SCRATCH with a probe-<seat> prefix; TMPDIR is honored.
- Never run the after-side C1 data procedure (`tools/round-44/c1-run.sh`): the L1 runs it after the freeze. Controls may run the counter's --selftest and dev-arm inputs only.
- Fleet identity is `kaidoku`; never claim ownership of sibling lanes' surfaces (tooling/builds).
- Exit codes are semantic: 0 met/clean, 1 failed, 2 could-not-evaluate. A 2 never counts toward the target.
- Read /home/vgpnk/.omp/agent/RULES.md before installing anything; pacman is paused per the addendum guard.
"""

def T(name, agent, task):
    return {"name": name, "agent": agent, "task": GODSPEED + task}

TASKS = [
 # ---- C1 core build ----
 T("R44C1Revenger","revenger",
   "Reverse-engineer the binding between unblob 26.6.4 squashfs_v1/squashfs_v2 handlers and REA 6.5.0 extract-firmware's published derivation tree, in support of plans/round-44-claims.md R44-C1. Read tools/round-42/c1-counter.py and carriers.json; write .ufo/waves/round-44/w1/R44C1Revenger.md mapping: for each of the 4 carriers (v1-le/v1-be/v2-le/v2-be) what derivations[].handler string REA actually emits, what the extract-root child_path looks like, and whether v1/v2 derivations can collide with a v3/v4 handler under the per-carrier EXACT-equality rule (never a prefix). Ground it in rea-agents@6.5.0 `dist/application/**/FirmwareReports.js` and unblob 26.6.4 handler source (corpus SOURCES S119, S123). Also confirm sasquatch 4.5.1 is the extractor unblob invokes for v1/v2 (not unsquashfs) and record the exact `-be`/`-le`/`-da` flags from S119 source lines. Output: markdown table per carrier {carrier, handler, root_example, flag_set, collision_risk}."),
 T("R44C1Oracle","executor",
   "Author tools/round-44/c1-oracle.py (author in your artifacts dir; L1 installs it) — the frozen oracle builder for R44-C1. For each carrier id in tools/round-44/carriers.json (v1-le, v1-be, v2-le, v2-be — fixtures already committed at corpus/evidence/round-42/c2/fixtures/v{1,2}-{le,be}--squashfs_v{1,2}.0_{le,be}.bin): (a) run `/usr/bin/unsquashfs -lls <bin>` and parse the member census (type, mode, owner, size, mtime, path); (b) extract to a fresh scratch dir and compute sha256 of every REGULAR file; (c) record symlinks/device entries as non-regular rows; (d) ALSO walk the committed `corpus/evidence/round-44/oracle/<id>__output__/` tree (the unblob expected output, fetched pre-freeze by R44SrcOracle) and record its member digests as a SECOND independent oracle; (e) write carriers.json oracle block per carrier: {members:[{path,size,sha256,type}], oracle_tool:'unsquashfs', oracle_ver:'4.7.5', output_tree_digest:<sha256 of sorted path+sha256 lines>}. The oracle is INDEPENDENT (squashfs-tools upstream) — never derive it from a REA/sasquatch receipt. Write .ufo/waves/round-44/w1/R44C1Oracle.md + the carriers.json oracle block in your artifacts dir."),
 T("R44C1Counter","executor",
   "Author tools/round-44/c1-counter.py (author in artifacts; L1 installs it) — a PORT of `git show c29360e3:tools/round-42/c1-counter.py` per plans/round-44-claims.md R44-C1. Functional deltas only; keep the freeze-integrity walk, segment-bounded extract-root rule, evidence-id recompute, counter_sha256 self-hash, and the counter-time REA rerun binding verbatim. Changes: (1) superblock probe becomes v1/v2 — read magic(4B), s_major(u16@28), s_minor(u16@30), endianness(from magic order), compression(u16@20), bytes_used; v1/v2 superblock layout differs from v3 so implement a v1v2 parser (see unblob `unblob/handlers/filesystem/squashfs.py` v1/v2 classes, S119); (2) oracle binding becomes the unsquashfs member census + __output__ tree digests from carriers.json (NOT the v3 LZMA oracle path); (3) handler family binding frozen per-carrier to exactly `squashfs_v1` or `squashfs_v2` (a v3/v4 handler on a v1/v2 carrier fails handler_ok); (4) `--selftest` covers: correct map on a dev-arm receipt, red on a v3 receipt fed to a v1 carrier, red on a fabricated oracle-only envelope (rerun projection mismatch). Write tools/round-44/c1-counter.py + .ufo/waves/round-44/w1/R44C1Counter.md (diff vs round-42 counter)."),
 T("R44C1Run","executor",
   "Author tools/round-44/c1-run.sh + c1-run.py (artifacts dir; L1 installs) — the AFTER-freeze data procedure for R44-C1. It must: for each carrier id in tools/round-44/carriers.json, create a fresh outdir under corpus/evidence/round-44/c1/<id>/, run `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <fixture> <outdir>` capturing stdout+stderr, write <outdir>/run.json {command, exit_code, stdout_sha256, wall_s, carrier, rev_at_run}; copy the produced receipt tree verbatim; and a top-level manifest.json mapping carrier->outdir+run.json path. IMPORTANT: the L1 runs this AFTER the freeze — seats NEVER run it; you only author it and write a --dry-run that prints the commands without executing. Write .ufo/waves/round-44/w1/R44C1Run.md."),
 T("R44C1Controls","executor",
   "Author tools/round-44/c1-controls.py + the four control receipts (artifacts; L1 installs the tool) per plans/round-44-claims.md R44-C1 controls: CTL-C1-0 do-nothing (run the frozen c1-counter.py at the freeze with receipts absent → expect exit 1, carriers_matched 0, every doc binding false); CTL-C1-1 (copy corpus/evidence/round-42/c1 after-receipts into .ufo/waves/round-44/controls/c1-1/ and score → expect non-zero: subject.digest/handler/superblock fail since v3 receipts cannot pass a v1/v2 predicate); CTL-C1-2 (fabricate an 'oracle-only' envelope whose published-file claims are computed from carriers.json oracle with no real REA run → counter must exit non-zero on the counter-time rerun projection binding); CTL-C1-3 (a receipt captured with sasquatch stripped from child PATH → expect non-zero with missing-extractor-dependency, not a clean match). Each control: write the input tree + a receipt.json {control, command, exit_code, stdout_sha256, wall_s, expected:'non-zero'|'exit1'}. Author the tool + write .ufo/waves/round-44/w1/R44C1Controls.md; the L1 runs the controls at the freeze."),
 # ---- oracle fixtures / sources ----
 T("R44SrcOracle","scribe",
   "Open SOURCES row S138 = unblob 26.6.4 SquashFS `__output__` expected trees (dataset) AND fetch the bytes pre-freeze into corpus/evidence/round-44/oracle/ (artifacts: you fetch+report; L1 commits). For each of v1-little_endian, v1-big_endian, v2-little_endian, v2-big_endian under https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/: list `__output__/` via the GitHub contents API, download every member file (media.githubusercontent.com base), record {path, bytes, sha256, fetched_at}. Write SOURCES row S138 text (URL, dataset, tier A, what it grounds = the second oracle member tree; NOT handler code, NOT extractor behaviour, NOT a C1 carrier) + located quote `LICENSE:5-8` already in S135. Also write the S139 draft: squashfs-tools upstream releases page https://github.com/plougher/squashfs-tools/releases (docs/tool) grounding `/usr/bin/unsquashfs` 4.7.5 identity. Output: .ufo/waves/round-44/w1/R44SrcOracle.md + oracle/ tree + SOURCES row text for S138 and S139."),
 T("R44EntryDraft","scribe",
   "Draft the R44-C1 knowledge entry corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md (author in artifacts; L1 lands it after data) per corpus/QUALITY.md criteria. Open with `source:`, `verified-at:` (fill at landing), `recheck:` (180d). Body: what moved Frontier→Core (squashfs_v1, squashfs_v2 both byte orders through REA extract-firmware), the 4 carriers with their oracle census, the superblock fields observed, the per-carrier handler binding rule, the disclosure that v2ns/broadcom/nonstandard/gzip-v3 stay Frontier and why (no independent reader for v2ns — measured: unsquashfs 4.7.5 and 7z 26.04 both refuse). Keep it a FACT entry (what the bytes showed), not opinion. Write .ufo/waves/round-44/w1/R44EntryDraft.md + the entry draft."),
 T("R44Quarantine","scribe",
   "Re-derive the kaidoku-package 5-row quarantine slice hand-check (round-43 did it at .ufo/waves/round-43/w1/R43Quarantine.md). Read .ufo/waves/round-44/assimilation/ and .ufo/quarantine/ if present; verify no staged row has been silently adopted into corpus/knowledge/ since round 43 (git log + ls). Write .ufo/waves/round-44/w1/R44Quarantine.md: verdict table {row, status, adopted?} + the line `Assimilation: none` for the report. Also one line on `considerthese/` (absent → say so)."),
 # ---- C2 calibration rubric ----
 T("R44ScoutCalib","scout",
   "Enumerate the candidate self-assessment statements for the R44-C2 rubric (plans/round-44-claims.md). Read SCORECARD.md (`## Capabilities` rows + their Evidence pointer cells; `## Owned axes` headline values + revision pins; every `## Round <N>` claim table's `met`/`not met` verdict vs its cited receipt exit code; `planned (round <N+1>)` rows vs what round N+1 actually worked), SHONEN.md (`path:line` and `N of M` assertions and their pinned-revision qualifiers), corpus/README.md (coverage-map row count vs corpus/knowledge/*.md count under command A). For EACH statement produce: {file, line, asserted_value, check_command, observed_value, mismatch?} — a check_command is one reproducible shell/python one-liner that re-derives the asserted value at a given rev (read-only git show/ls-tree, NO network, NO REA). Write the census to .ufo/waves/round-44/w1/R44ScoutCalib.md (markdown table) AND .ufo/waves/round-44/w1/R44ScoutCalib.json (list of {file,asserted,check,observed,mismatch}). This is recon only — do NOT fix anything."),
 T("R44C2Rubric","executor",
   "Assemble the R44-C2 rubric from R44ScoutCalib's census (read .ufo/waves/round-44/w1/R44ScoutCalib.json; if absent run the census yourself read-only). Produce tools/round-44/c2-rubric.json in artifacts: a list of entries {id, file, line_at_base, asserted, check:{argv, cwd:'scratch-clone'}, expected:'match'|'superseded', note}. Rules: every entry's check re-derives the value independently (recount map rows, re-resolve the pointer, re-run the pinned command at its declared rev); drop any statement whose value cannot be re-derived mechanically (record dropped ids + reason). Include the seeded-mismatch spec: which single entry a control will corrupt (e.g. a capabilities evidence path). The rubric is FROZEN at freeze time — make it complete now. Output tools/round-44/c2-rubric.json + .ufo/waves/round-44/w1/R44C2Rubric.md (entry count, dropped list, base mismatch count)."),
 T("R44C2Counter","executor",
   "Author tools/round-44/c2-counter.py (artifacts; L1 installs) implementing plans/round-44-claims.md R44-C2. Reads tools/round-44/c2-rubric.json + --rev/--freeze/--work/--json-out. Behaviour: (1) freeze-integrity walk identical in spirit to c1-counter (frozen paths incl. the rubric itself byte-compared FREEZE→REV; appended C2 repair notes are allowed ONLY on rubric-named files and only as an appended dated block whose diff the rubric's `expected_edit` clause binds — never a raw numstat); (2) for each rubric entry, clone the rev's tree into --work scratch (git archive or git worktree, read-only), run the entry's check argv, compare observed to asserted; (3) a mismatch = check output != asserted AND no appended supersession/correction note at REV makes the check pass; (4) exit 0 iff mismatches==0 and every entry evaluable; exit 2 on malformed rubric (missing check/command), absent frozen file, or a check that cannot run; (5) --selftest: green on a clean dev rubric, red on a seeded mismatch, exit2 on a rubric entry with no command. Write tools/round-44/c2-counter.py + .ufo/waves/round-44/w1/R44C2Counter.md."),
 T("R44C2Shonen","scout",
   "SHONEN.md assertion census for the C2 rubric (works alongside R44ScoutCalib which covers SCORECARD+README): enumerate every SHONEN.md assertion of form `path:line`, `N of M`, a range `a-b`, or a bare path pointer, plus its pinned-revision qualifier if any. For each: resolve the pointer at its pinned rev AND at the base rev; flag any that resolve at the pinned rev but are stale/unresolvable at base without an explicit superseded marker. Read-only. Write .ufo/waves/round-44/w1/R44C2Shonen.md + .json {assertion, pinned_rev, resolves_at_pinned, resolves_at_base, stale_without_marker?}."),
 T("R44C2Controls","executor",
   "Author tools/round-44/c2-controls.py + control receipts (artifacts) per plans/round-44-claims.md C2 controls: CTL-C2-0 do-nothing (frozen c2-counter.py at freeze scored at BASE → exit non-zero iff frozen rubric shows mismatches>0 at base; if 0 at base the claim stops); CTL-C2-1 seeded mismatch (scratch clone, corrupt the rubric-named seeded entry — e.g. delete an evidence path or decrement a count → counter must report the mismatch and exit non-zero); CTL-C2-2 malformed rubric (drop a check command → expect exit 2); CTL-C2-3 rubric-immutability (attempt a mid-round rubric edit → counter flags frozen_path_changed on c2-rubric.json). Write the tool + .ufo/waves/round-44/w1/R44C2Controls.md with a receipt.json per control {control,command,exit_code,expected}."),
 T("R44C2Sentinel","sentinel",
   "Adversarial review of the R44-C2 rubric+counter design (read plans/round-44-claims.md, R44C2Rubric.md, c2-counter.py draft in artifacts). Hunt bypasses: a repair that makes a check pass without fixing reality (e.g. rewriting the asserted count to match the wrong observed value); a rubric entry whose check is self-referential (reads the file it asserts about, so a corrupt file passes); a check that is trivially green (always-true); rubric loosening mid-round; a `frozen_path_changed` relaxation that lets an arbitrary edit through. Report each bypass with a concrete exploit and whether the frozen counter catches it. Write .ufo/waves/round-44/w1/R44C2Sentinel.md."),
 # ---- attack / falsify of the draft ----
 T("R44CritC1","critic",
   "Adversarial review of R44-C1 draft (plans/round-44-claims.md + c1-counter.py draft). Attack: is the unsquashfs oracle truly independent (different producer than sasquatch)? Can a v3/v4 receipt pass the v1/v2 handler binding? Is the superblock probe correct for v1 vs v2 layout (check against unblob v1v2 parser + `file`/`unsquashfs -s` output on the 4 fixtures)? Is the carve/bytes_used rule right for v1/v2? Does the do-nothing control really fail (a stale round-42 receipt path must NOT accidentally satisfy the root rule)? Is 4 thin fixtures enough — and is that disclosed as a limit rather than hidden? Report concrete counterexamples with file+line; a 'looks fine' verdict requires you tried at least 3 distinct attacks. Write .ufo/waves/round-44/w1/R44CritC1.md."),
 T("R44CritC2","critic",
   "Adversarial review of R44-C2 draft + rubric. Attack: is a 0-mismatch census at base an automatic honest stop (and is that check actually run before the freeze)? Can the seeded-mismatch control be gamed (corrupt something NOT in the rubric → is it still caught)? Does re-deriving each asserted value actually catch a wrong count, or can the check and the file drift together (self-referential check)? Is `planned (round N+1)` vs 'what N+1 worked' decidable, or is the comparison fuzzy enough to hide a mismatch? Name the weakest rubric entry and propose the exact check that hardens it. Write .ufo/waves/round-44/w1/R44CritC2.md."),
 T("R44C1Mutants","mutation-tester",
   "Mutate-and-run probe of the C1 dev-arm (the counter's --selftest arms): for each of the 4 carriers produce a receipt mutation (wrong handler string e.g. squashfs_v3 on a v1 carrier; truncated superblock; a symlink gap replaced by a fabricated file claim; a doctored extract-root path with a `..` component; an oracle member with a flipped sha256). Run the frozen c1-counter.py --selftest + each mutation and record whether it flags it red (expected: every mutation caught). Report any mutation that scores GREEN — that is a counter hole to fix before freeze. Write .ufo/waves/round-44/w1/R44C1Mutants.md."),
 T("R44RevFreeze","reviewer",
   "Verify the frozen-paths list in plans/round-44-claims.md `## Frozen paths` is COMPLETE for R44-C1 and R44-C2: walk each predicate's named inputs (tools, carriers, oracle trees, rubric, control inputs, the round-42 counter it ports from, the round-42/43 score receipts the controls replay, SKILL.md/SCORECARD.md/SHONEN.md/corpus/README.md/SOURCES.md as C2 targets). For each: is it listed as frozen, and is freezing it correct (a C1 carrier must NOT change; a C2 target's frozen text pins the checked statement while repairs land appended)? Flag anything the predicate reads that is NOT frozen (a moving input = an unverifiable claim) and anything frozen that need not be. Write .ufo/waves/round-44/w1/R44RevFreeze.md {path, frozen?, needed?, issue}."),
 T("R44RevKill","reviewer",
   "Review the kill rules and separability of plans/round-44-claims.md. (a) Kill rules: each claim's control set — is there a control whose GREEN result unambiguously stops the claim, and is every control shown able to FAIL at the freeze before data? (b) Causal separability: C1 and C2 share corpus/README.md + corpus/SOURCES.md — does C2's rubric tolerate the C1 landing (map-row count read at REV not frozen) and does C2's rubric avoid pinning SOURCES row count? Flag any hidden coupling (e.g. a shared frozen file whose C1 landing would trip C2's frozen_path_changed). Write .ufo/waves/round-44/w1/R44RevKill.md."),
 T("R44ConnPattern","connector",
   "Cross-axis pattern finder for round 44 (mandatory each wave). Look at the two claims' shared machinery: the freeze-integrity walk is identical in c1-counter and c2-counter — is the right move a shared module tools/round-44/freeze_check.py both import (single source of truth for frozen_path_changed), or is that premature abstraction for a 2-file case? Also compare the oracle-binding in C1 (receipt-vs-independent-reader) against the C2 rubric binding (asserted-vs-re-derived) — same 'compare two independent derivations' pattern; name the one contract both satisfy. Recommend ONE small deduplication or 'keep separate'; justify by diff size. Write .ufo/waves/round-44/w1/R44ConnPattern.md."),
 # ---- cross-cutting / protocol ----
 T("R44ConnSibling","connector",
   "Cross-sibling overlap scan: the prompt names siblings `tooling` (shell/Git/TS productivity) and `builds` (compiled codebases). Confirm R44-C1/C2 stay inside the kaidoku surface (REA + reverse engineering; corpus self-assessment) and do not claim tooling's or builds' surfaces — e.g. c1-run.sh is a lane-internal runner, not a tooling-lane tool; the C2 rubric checks kaidoku's OWN files, never a sibling's. Also check `sibling-owned` Frontier adjacency: PROVINCE.md's contested-scope rule — confirm no C1/C2 surface is already sibling-owned. Write .ufo/waves/round-44/w1/R44ConnSibling.md."),
 T("R44ConnRouted","connector",
   "Routed-defect ledger for round 44 (the prompt's routed-defect list is binding). For each routed defect that touches kaidoku (e.g. TMPDIR/mkdtemp /tmp routing — counters must honor TMPDIR and accept a scratch argument; LFS fixture custody; sasquatch nonstandard magic; the M43-2 frozen-numstat repair — diff expectations are row-identity checks; reaper notice / /tmp not citable), write the row: {defect_id, status for this round, where addressed in plans/round-44-claims.md or tools/round-44/}. Read .ufo/routed/ or the prompt §routed list; produce .ufo/waves/round-44/w1/R44ConnRouted.md — a ledger the report can paste."),
 T("R44Debt","scribe",
   "Debt-ledger entry for round 44: enumerate every disclosed limit in plans/round-44-claims.md (thin 4-fixture carrier set for C1; v2ns/broadcom/nonstandard/gzip-v3 stay Frontier; published v1/v2 rootfs unfetchable; C2 rubric enumerates only frozen statements; counter verifies a check passes, not that reality is fixed). Write .ufo/waves/round-44/w1/R44Debt.md as a table {debt, claim, why-disclosed, future-round-exit-condition} — these are the honest-stop backstops, never silently dropped."),
 T("R44ScoutSkill","scout",
   "SKILL.md / PROVINCE.md drift check for C1+C2: (a) the v4 triage table and instrument registry — do they still reflect repo state at base (e.g. handler cells mention squashfs_v1/v2/v3 legacy rows, selftest counts)? (b) PROVINCE.md `## Frontier` — list every SquashFS surface it still names Frontier (confirm the C1 claim's scope: squashfs_v1+v2 move; v2ns/v3_broadcom/v3_nonstandard/v4_broadcom/gzip-v3 stay). (c) Confirm SKILL.md's instrument-registry selftest counts parse and each referenced tool file exists. Read-only. Write .ufo/waves/round-44/w1/R44ScoutSkill.md + .json."),
 T("R44Prefile","executor",
   "Re-run the lane's pre-file gate machinery (per the prompt's file-only-after-WAVE-DONE rule and round-43's finalize-green prefile gate): author tools/round-44/prefile-check.sh (artifacts; L1 installs) that asserts — (a) every launched wave has its WAVE-DONE signal before a report is filed; (b) the report path .ufo/reports/round-44/kaidoku.md exists only after all waves done; (c) the claims file's frozen-paths list is non-empty. You only author it + write .ufo/waves/round-44/w1/R44Prefile.md; the L1 runs it at pre-file time."),
 T("R44Simplify","simplifier",
   "YAGNI review of the round-44 surface: read plans/round-44-claims.md + the drafted tools/round-44/* in artifacts. Flag anything built 'just in case' that no predicate needs — e.g. a c1 counter arm for a handler family not in carriers.json, an oracle path for a carrier not frozen, a rubric entry with no landing consequence. Recommend the smallest deletable set. Also: is a 5th carrier (a broadcom/v3 fixture) scope creep — confirm dropping it is correct because the claim's target is the frozen 4. Write .ufo/waves/round-44/w1/R44Simplify.md."),
 T("R44MistakeHunt","critic",
   "Mine the lane's own mistake classes for a round-44 example (the lesson needs one mined mistake). Candidates to verify: (a) the L1's pre-freeze probe guessed `squashfs_v2.0_be.expected` (HTTP 404) before reading the directory listing — class stale-premise; confirm it is real by reproducing the 404 vs the correct `__output__/` listing 200; (b) check `.ufo/waves/round-43/` lesson Gate rows and mistakes.md for a fresher example. Pick ONE verifiable mistake, write the mistakes.md row {class, evidence, captured-by, fix-with-red-green}. Write .ufo/waves/round-44/w1/R44MistakeHunt.md."),
 T("R44Shonen","scribe",
   "Draft the report's `## SHONEN` content skeleton (author in artifacts; L1 finalizes after waves): a shonen-grade summary of round 44 — what moved, what the frozen counters measured, what stopped, and the mined mistake. Pull phrasing discipline from corpus/lessons/round-43.md and the lane's SKILL.md shonen guidance: concrete axis deltas, named evidence pointers, zero unfalsifiable claims. Write .ufo/waves/round-44/w1/R44Shonen.md."),
 T("R44ScoutSEAT","scout",
   "Seat-planning data-walk (bounded planner-task riding a scout, per the planner ruling): given plans/round-44-claims.md's two claims and the wave-1 roster, produce the recommended WAVE-2 seat plan — which seats attack the landed claim (revenger/critic/sentinel on the after-receipts + counter rerun binding; mutation-tester on the frozen counter vs mutated after-receipts; reviewer on frozen_path integrity; scribe on report assembly). Recommend a wave-2 size in [32,64] and a per-seat task list. Write .ufo/waves/round-44/w1/R44ScoutSEAT.md."),
 T("R44LabV2ns","scout",
   "Empirical check (read-only, one hypothesis): `squashfs_v2_nonstandard` cannot be promoted to Core this round because no oracle independent of sasquatch/unblob exists. Test every plausible independent reader on corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin: /usr/bin/unsquashfs -lls, 7z l, backhand unsquashfs-backhand -l, binwalk -e scratch, and the committed unblob __output__ tree if present. Record per reader {tool, version, command, exit, produced_tree?}. If any truly independent reader produces a full member tree, report it (it changes the C1 scope); otherwise confirm v2ns stays Frontier. Write .ufo/waves/round-44/w1/R44LabV2ns.md."),
 T("R44C1Doc","scribe",
   "Draft the PROVINCE.md + corpus/README.md documentation deltas for R44-C1 (artifacts; L1 lands after data): (a) `## Round-44 additions to Core` row naming squashfs_v1 + squashfs_v2 (both byte orders) through REA extract-firmware, citing the knowledge entry + the four carriers; (b) the Frontier-note line superseding the `SquashFS v1/v2` Frontier bullet ONLY (do not touch v2ns/v3_broadcom/v4_broadcom/gzip-v3 frontier text); (c) corpus/README.md coverage-map row mapping the new knowledge stem `2026-10-28-r44-squashfs-v1v2-core`; (d) check the README map-block `awk` command in corpus/README.md so the new row keeps the map row count == knowledge file count invariant true. Write .ufo/waves/round-44/w1/R44C1Doc.md + the three text blocks."),
 T("R44C1FixtureAudit","reviewer",
   "Verify the four C1 carrier fixtures are byte-stable and the correct files: for each of corpus/evidence/round-42/c2/fixtures/{v1-le,v1-be,v2-le,v2-be}--squashfs_v*.bin, recompute sha256 and compare to the pin in tools/round-42/fixtures.json and tools/round-44/carriers.json; confirm `file` reports the expected SquashFS version/endianness/compression; confirm the fixture MIT licence is honoured (S135) and the bytes are the committed unblob fixtures, not re-downloaded drift. Also verify the v2ns fixture is NOT among the C1 carriers (it stays Frontier). Write .ufo/waves/round-44/w1/R44C1FixtureAudit.md {carrier, sha256_match, file_verdict, licence}."),
 T("R44C2Readme","scout",
   "corpus/README.md census for the C2 rubric (parallel to R44ScoutCalib which covers SCORECARD): enumerate every checkable statement — the coverage-map row count vs corpus/knowledge/*.md count under command A, the `## Frontier` bullet list vs PROVINCE.md Frontier lines, any `N of M` or path:line assertions, and the table header consistency. For each produce {line, asserted, check_command, observed, mismatch?} (re-derivable, read-only). Write .ufo/waves/round-44/w1/R44C2Readme.md + .json."),
 T("R44C2Plan","scout",
   "Planned-vs-actual census for the C2 rubric: for each `## Round <N>` section in SCORECARD.md, extract its `planned (round <N+1>)` row text and compare against what round <N+1> actually worked (its ## Round N+1 heading + claim table). Flag any plan row whose promised work was NOT done in N+1 and carries no `(after a steer)`/`superseded`/`historical` marker (a dangling plan is a self-assessment mismatch). Produce {round, planned_text, actual_N1, mismatch?}. Read-only. Write .ufo/waves/round-44/w1/R44C2Plan.md + .json."),
 T("R44C2SentReview","reviewer",
   "Second-pass review of the C2 rubric completeness (read R44ScoutCalib.json + R44C2Readme.json + R44C2Shonen.json + R44C2Plan.json when present; if a seat's output is absent, enumerate that surface yourself). Is the union of the four censuses COMPLETE for the rubric's scope, or did a whole class of self-assessment statement fall through (e.g. capability-table `Evidence pointer` cells, `## Owned axes` revision pins, LOG.md verdict claims)? Report coverage gaps and the exact rubric entries to add. Write .ufo/waves/round-44/w1/R44C2SentReview.md."),
 T("R44Assim","scribe",
   "Assimilation ledger line for the report (§10): confirm `.ufo/waves/round-44/assimilation/` is empty/absent and produce the single line `Assimilation: none` plus one sentence on why (the package's full 5-row quarantine slice was hand-checked in round 43; no staged row adopted since). Also confirm `considerthese/` does not exist (one report line). Write .ufo/waves/round-44/w1/R44Assim.md."),
 T("R44Watchdog","scribe",
   "Watchdog/unblob ledger for the report: read /home/vgpnk/Projects/shokunin/.ufo/watchdog.log for this lane's round-44 launch lines (any lane-dead-no-report kaidoku round=44 = inherited uncommitted outputs to name in the report per the prompt's attempts clause) and unblob.log for unblob/sasquatch run lines this session. Produce the attempt history {launch, complete, dead} for round 44 so the report names whether this is attempt 1 and what was inherited. Write .ufo/waves/round-44/w1/R44Watchdog.md."),
]

def main():
    os.makedirs(WAVE_DIR, exist_ok=True)
    spec = {"wave": "r44-w1", "milestone": MILE, "reportDir": REPORT,
            "context": CTX,
            "items": [{"name": t["name"], "role": t["agent"],
                       "prompt": t["task"], "axes": AXES} for t in TASKS]}
    with open(os.path.join(WAVE_DIR, "w1-spec.json"), "w") as f:
        json.dump(spec, f, indent=1)
    members = {}
    for t in TASKS:
        members[t["name"]] = {"kind": "spawn", "agentId": None, "role": t["agent"],
                              "item": None, "axes": AXES, "milestone": MILE}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1",
        "wave": "r44-w1",
        "policy": {"source": "config", "maxLanes": 256, "minLanes": 16,
                   "waveMinLanes": 32, "waveMaxLanes": 64,
                   "declaredMaxLanes": None, "hardCeiling": 256,
                   "rampBatchSize": 5, "rampIntervalMs": 700,
                   "globalRunnerCeiling": 1056},
        "counts": {"spawn": len(TASKS), "resume": 0, "total": len(TASKS)},
        "registry": {"schema": "ufo-swarm-registry-v1",
                     "path": ".ufo/waves/round-44/w1/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": {"applied": False, "mechanism": None, "reason": None,
                       "savedBytes": 0, "payloadBytesBefore": 0,
                       "payloadBytesAfter": 0},
        "taskCall": {"context": CTX, "tasks": TASKS},
        "resumeSends": [],
        "note": ("Issue exactly one batched task call with taskCall "
                 "({context, tasks}); never split a wave into multiple task "
                 "calls (one-swarm-per-wave). Then one hub send per "
                 "resumeSends entry.")
    }
    with open(os.path.join(WAVE_DIR, "w1-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    registry = {"schema": "ufo-swarm-registry-v1", "wave": "r44-w1",
                "reportDir": REPORT, "members": members}
    os.makedirs(os.path.join(WAVE_DIR, "w1"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w1/swarm-registry.json"), "w") as f:
        json.dump(registry, f, indent=1)
    ready = {"lane": "kaidoku", "round": 44, "wave": "r44-w1",
             "dispatch": os.path.join(WAVE_DIR, "w1-dispatch.json"),
             "l1": "KaidokuR44"}
    with open(os.path.join(WAVE_DIR, "w1.ready"), "w") as f:
        json.dump(ready, f)
    print("wrote", len(TASKS), "seats")
    import collections
    print(collections.Counter(t['agent'] for t in TASKS))

if __name__ == "__main__":
    main()
