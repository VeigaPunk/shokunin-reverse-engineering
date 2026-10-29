#!/usr/bin/env python3
"""Generate the round-50 attempt-2 wave-3 spec (v1 policy, build wave), validate, write dispatch + ready."""
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-50")
BASE = "f890bbead20ca2c549487167f56876ae47f1e1a4"
FREEZE = "435d41fd4ad9211d1579fc447936fb33d2b74467"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
WAVE = "r50-w3"
MILE = ("Round 50 attempt-2 wave 3 (build): source re-opens, landing-text drafts, the C3 triage-v5 instrument "
        "build and pre-freeze attacks; the L1 integrates, freezes the C3 instrument, then runs the REA-dependent "
        "controls and the C1 data run in a quiet window")
REPORT = ".ufo/waves/round-50/w3"
W = REPORT + "/"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r50/"
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
ENTRY = "2026-10-29-r50-le-avm-hsqs-core"

CTX = f"""# Target
kaidoku-shokunin round 50, attempt 2 (the run-11 wrap-up released the round without a closure; this is the re-dispatch), wave 3 of 2 planned waves = the BUILD wave: source re-opens, landing-text drafts, the C3 instrument build and pre-freeze attacks. The C1 freeze `{FREEZE}` is COMMITTED and byte-unchanged; the L1 (alone) runs the REA-dependent controls and the C1 data run AFTER this wave, in the quietest window it can find. Lane root (absolute): {ROOT}. L1 = KaidokuR50 (integration owner; it holds the section-3 planner seat \u2014 the validator rejects `planner` as a swarm role). Base revision `{BASE}` (the attempt-2 claims commit).

# The claims (the plans are the rule \u2014 read them, not this prompt)
- **R50-C1 coverage (resumed, predicate frozen)**: genuine AVM-marker little-endian SquashFS v4 members (`hsqs`, v4.0, xz, `mkfs_time == bytes_used`) of four public FRITZ!OS images (FRITZ!Box 7581/7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30 x86 members), through REA 6.5.0 `extract-firmware` (handler `squashfs_v4_le`), Frontier -> Core. Frozen rule: `{ROOT}/plans/round-50-claims.md` section R50-C1; counter `{ROOT}/tools/round-50/c1-counter.py` (frozen bytes; `--selftest` is offline). Attempt-2 declaration: `{ROOT}/plans/round-50-attempt2-claims.md`.
- **R50-C3 depth (new this attempt, freeze lands after this wave)**: `SKILL.md` rule block 21 table v4 mis-routes the three no-independent-reader handler families (`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`): the `legacy-body-failure` row's glob `squashfs_v[123]*` matches them and its cross-read rule condemns a healthy no-reader body (round-49 `W2Skill.md` F1), and the `clean` row gives no-reader runs an oracle-backed action no oracle can serve (F2; the four committed v2ns `_ddefault` recon envelopes label `clean`/`none`). Claim: table v5 as rule block 22 + scoring instrument `{ROOT}/tools/round-50/sqfs-triage-v5.py`; predicate/controls/kill rule in `{ROOT}/plans/round-50-attempt2-claims.md` section R50-C3.

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside `{ROOT}/{W}<YourSeatName>/` (create it) and your report file `{ROOT}/{W}<YourSeatName>.md`. Draft instruments/docs go under `{ROOT}/{W}<YourSeatName>/` \u2014 never into the lane's `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, nor the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command in the lane or fleet repo. Read-only git (`log`, `show`, `diff`, `ls-tree`, `rev-parse`, `cat-file`, `merge-base`) is fine.
- **No REA runs this wave.** The L1 alone runs REA (controls + data run) after the wave, so the host load stays predictable (round-50 attempt 1 lost its window to `provider_timeout` at load 95\u2013176). Do not invoke `npx rea-agents`, `rea`, or the package at `{PKG}`. Offline counter selftests are allowed where your task names them.
- **Downloads**: only where your task names an image (at most the images your task names), into your scratch only; **vendor firmware bytes are never copied into the lane tree** (AVM licence) \u2014 only hashes, listings, receipts.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`; every later git call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; set `user.name`/`user.email` in that clone only. Never run `git commit` with a throwaway identity anywhere else. Prefer `git clone --shared {ROOT} "$S/clone"` + `git -C "$S/clone" checkout --detach {BASE}` for a lane copy.
- **Scratch**: `S={SCRATCH}w3-<YourSeatName>`; `mkdir -p "$S"`, `export TMPDIR="$S"`. Remove `$S` before you yield AFTER copying receipts into `{W}<YourSeatName>/`. Never write under `/tmp`; nothing under `/tmp` is citable. Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256 and UTC time. A check you did not run is not passed \u2014 say "not run". Never fabricate output. Do not paste session cookies, tokens or `Set-Cookie` headers into any receipt: strip headers before saving.
- **Exit codes are semantic**: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.
- **Absolute paths**: your tools start at the fleet root, not the lane. The `Report:` trailer path in your prompt is relative to {ROOT} \u2014 write it at `{ROOT}/<that path>` (`{ROOT}/{W}<YourSeatName>.md`). A file written at a relative path lands in the FLEET repo and is a defect.
- **Tooling authorization (operator, 2026-10-19)**: you may install/upgrade tools that help the task; first read `/home/vgpnk/.omp/agent/RULES.md` (official channels, update-safety gate; record tool/version/channel/reason in your report). **pacman guard**: all pacman transactions are PAUSED host-wide \u2014 install only via `uv tool`/`npx`/an official binary in `~/.local/bin`, or nothing. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host service.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `/home/vgpnk/Projects/shokunin/.scratch/`, or the fleet repo. Never run a `--data-run`, never write into `corpus/evidence/`.
- Return a final message of at most 8 lines: your verdict, the 1-3 most important findings, your report path.

# What the L1 does with your output
It reads every report, integrates the drafts (entry, rows, bindings, the v5 instrument), commits the C3 freeze (instrument + registry row), scores the C3 controls and the C1 controls in a quiet window, runs the C1 data run, lands everything, and dispatches the falsify wave against the landed bytes. Drafts you write are inputs the L1 reviews and may rewrite. Report; do not wait for others.
"""

T = []


def add(name, agent, task):
    t = GODSPEED + task + (
        "\n\nWrite your findings to `<ROOT>/<W><SEAT>.md` (verdict first, then a findings table "
        "with exact commands, exit codes, sha256s); extra artifacts under `<ROOT>/<W><SEAT>/`.")
    T.append({"name": name, "agent": agent,
              "task": t.replace("{ROOT}", ROOT).replace("{W}", W).replace("{FREEZE}", FREEZE)
              .replace("{ENTRY}", ENTRY).replace("{BASE}", BASE).replace("{PKG}", PKG).replace("{SCR}", SCRATCH)
              .replace("<ROOT>", ROOT).replace("<W>", W).replace("<SEAT>", name)
              .replace("<FREEZE>", FREEZE).replace("<ENTRY>", ENTRY)
              .replace("<BASE>", BASE).replace("<PKG>", PKG)
              .replace("<SCR>", SCRATCH)})


# ------------------------------------------------------------------ source re-opens (S243/S244/S245/S249)
add("SrcReopenFreetz", "scout",
    "Re-open the Freetz AVM_LE/AVM_BE patch source (planned row S243). Open "
    "`https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` "
    "today: record UTC date, HTTP status, bytes, sha256 (attempt-1 recorded 1,153 B, sha256 e28b3341... prefix, "
    "2026-10-28). Verify the attempt-1 Gate quotes still locate: line 7 `+#define AVM_LE 2`; lines 17-18 the byte-order "
    "condition naming `SQUASHFS4_LE` or `AVM_LE` selecting `__LITTLE_ENDIAN`. Save the fetched body in your seat dir and a "
    "copy receipt (command, exit, sha256, UTC). State whether the row can be registered this round as planned (tier B, "
    "kind code, scope 'AVM LE/BE symbol definitions', teaches 'supersedes nothing; new row').")
add("SrcReopenAvmIndex", "scout",
    "Re-open the AVM download index (planned row S244). Open `https://download.avm.de/fritzbox/` and the four model "
    "`fritz.os/` indexes (`fritzbox-7581/other/fritz.os/`, `fritzbox-7582/other/fritz.os/`, "
    "`fritzbox-6490-cable/deutschland/fritz.os/`, `fritzbox-6430-cable/deutschland/fritz.os/`): UTC date, HTTP status, "
    "bytes, sha256 per body; the listing rows for the four pinned image files (name, size, date). Then HTTP HEAD each of the "
    "four image URLs named in `{ROOT}/tools/round-50/carriers.json` and record status, Content-Length, Last-Modified, ETag "
    "against the frozen `http_last_modified`/`http_etag` pins \u2014 any drift means the chain is unfetchable and the L1 must "
    "know BEFORE the data run. No image body downloads. Also confirm attempt-1's located quote (7581 listing row "
    "`FRITZ.Box_7581-07.18.image` `19-Aug-2024 12:33` `32010240`) still appears.")
add("SrcReopenUnblob", "scout",
    "Re-open the unblob 26.6.4 LE handler source (planned row S245). Open "
    "`https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`: UTC date, "
    "HTTP status, bytes, sha256 (attempt-1: 19,842 B, sha256 2d7b901b... prefix). Verify the located quotes: line 455 "
    "`NAME = \"squashfs_v4_le\"`; lines 53-54 `case Endian.LITTLE, _:` then `commands_args.append(\"-le\")`; line 48 the only "
    "`is_avm` inside `case Endian.BIG, 4:`. IMPORTANT: the registry already holds S108/S112 for this same URL opened "
    "2026-10-26 scoped to the BE branch \u2014 a new row S245 is a same-URL-different-scope row and the census will emit a W04 "
    "duplicate-URL WARNING. Verify on a scratch copy of `{ROOT}/corpus/SOURCES.md` plus a draft S245 row that "
    "`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch copy>` still exits 0 (warnings "
    "allowed) and record the exact W04 line. Save the body + receipt in your seat dir.")
add("SrcReopenLicence", "scout",
    "Re-open the AVM licence text (planned row S249). Open "
    "`https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt`: UTC date, HTTP status, bytes, "
    "sha256 (attempt-1: 67,591 B, sha256 6c601b34... prefix). Verify the attempt-1 quote still locates: line 850 \"The "
    "licensee may create only one copy of the software, which may be used exclusively for backup use.\" Save the body + "
    "receipt. State the tier/kind/scope cells you would give the row (tier A scoped to 'AVM firmware licence restricts "
    "redistribution'; kind docs).")

# ------------------------------------------------------------------ C1 landing-text drafts
add("ScribeEntryC1", "scribe",
    "Draft the C1 knowledge entry `{ROOT}/{W}<SEAT>/entry-draft.md`, paste-ready for "
    "`corpus/knowledge/{ENTRY}.md`. Open `{ROOT}/plans/round-50-claims.md` (R50-C1 section incl. Disclosed limits 1-7 and "
    "the carrier table) and `{ROOT}/plans/round-50-attempt2-claims.md`. Required shape: provenance trio first (`source:` "
    "citing S243/S244/S245/S249 with URLs and anchors; `verified-at:` the attempt-2 data commit placeholder `<REV>`; "
    "`recheck:` `on-refetch` naming the fetch-vendor chain command), then: the surface (LE AVM `hsqs` v4.0 xz members, "
    "marker `mkfs_time == bytes_used`); the four carriers with pins (from carriers.json); what REA does (`extract-firmware "
    "--max-depth 1`, handler `squashfs_v4_le`, sasquatch 4.5.1 on the child PATH, unblob 26.6.4, `-le` argv, the AVM trailer "
    "removed by the carve; the cable tars' BE `sqsh` ARM sibling is NOT a carrier and appears as a second chunk with "
    "`unknown-chunk-handler` on the uncarved member only); results placeholders `<FILLED AT LANDING>` for "
    "carriers_matched/gaps/evidence ids; the census (70 model directories, 28 LE `hsqs` marker rows in 16 models); the "
    "marker-is-a-constant-of-the-bytes honesty clause (attempt-1 amendment); the carrier-swap history (7530/7590 out on "
    "REA's 120 s provider_timeout at load, kept Frontier as '~13k-file LE AVM rootfs'); Still-Frontier list (LE AVM rootfs "
    "of ~13k files under the 120 s limit, AVM kernels, nested sub-images below depth 1, v2ns, v3 broadcom/nonstandard, gzip "
    "v3, v4 Broadcom); limits 1-7 restated. Label every claim observation/inference/unknown per QUALITY 5. Name what was "
    "NOT examined (QUALITY 7). Keep total under 220 lines.")
add("ScribeRowsSources", "scribe",
    "Draft the four SOURCES append rows + search-log entry at `{ROOT}/{W}<SEAT>/rows.md`. Read "
    "`/home/vgpnk/Projects/shokunin/CORPUS.md` section SOURCES.md (contract v1) and the registry tail of "
    "`{ROOT}/corpus/SOURCES.md` (last row S248; S150-S242 are intentionally skipped \u2014 cited in earlier lessons as refused "
    "staged rows; the registry is append-only, ids never reused). Rows (11 columns, no `|` inside any cell, `opened` "
    "2026-10-28 with the attempt-2 re-open 2026-10-29 recorded in the round lesson's Gate, status `mined`, `used-by` exactly "
    "`corpus/knowledge/{ENTRY}.md`): S243 Freetz patch (kind code, tier B scoped 'AVM LE/BE symbol definitions', anchor "
    "patch :7,:17-18); S244 AVM download index (kind dataset, tier A scoped 'which firmware images AVM publishes and their "
    "sizes', anchor the index paths + listing dates, recheck 90d); S245 unblob squashfs.py at tag 26.6.4 (kind code, tier A "
    "scoped 'the little-endian v4 handler and its sasquatch -le argv', anchor :53-54,:455 \u2014 the W04 duplicate-URL warning "
    "against S112 is expected and allowed); S249 AVM licence info_en.txt (kind docs, tier A scoped 'AVM firmware licence "
    "restricts redistribution', anchor :850). Each row's `teaches` = one grounded learner benefit, no cell over ~200 chars. "
    "Plus the search-log prose entry (question/query, where, date, identified/screened/included/excluded counts, stop "
    "rationale \u2014 reuse attempt-1's counts from `{ROOT}/.ufo/waves/round-50/w1/C1SrcFreetz.md` and siblings, updated for "
    "this attempt's re-opens). Verify your block on a scratch registry copy with "
    "`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>` exit 0 (warnings allowed) and paste "
    "the output.")
add("ScribeProvinceBinding", "scribe",
    "Draft the PROVINCE.md bindings at `{ROOT}/{W}<SEAT>/province.md`: (1) a `## Round-50 additions to Core` section in "
    "the style of `## Round-49 additions to Core` (read it, `{ROOT}/PROVINCE.md:432`): one table, row surface 'genuine "
    "AVM-marker little-endian SquashFS v4 (`hsqs`) members of four public FRITZ!OS images (7581/7582 07.18, 6490 Cable "
    "07.57, 6430 Cable 07.30 x86 members) \u2014 handler `squashfs_v4_le`, marker `mkfs_time == bytes_used`' naming the entry "
    "path `corpus/knowledge/{ENTRY}.md`; Ports/keys cell (no new REA key; unblob 26.6.4 runs plain `sasquatch -le`, "
    "`REA_UNBLOB_COMMAND`; sasquatch 4.5.1; `extract-firmware --max-depth 1`); Probe cell with the exact Use/expect "
    "sentences (command shape, expected handler, `extraction_gaps` rule per the frozen gap rule); Verified-evidence cell "
    "pointing at `corpus/evidence/round-50/c1/` and the counter. (2) the `Round-50 frontier note` line: dated 2026-10-29, "
    "names the entry stem `{ENTRY}`, the token `LE AVM`, states what moved (LE AVM members `hsqs` -> Core on the four "
    "carriers) and what stays Frontier (LE AVM rootfs of ~13k files under REA's 120 s limit, AVM kernels, nested "
    "sub-images below depth 1), and which earlier notes it supersedes (the LE-AVM clause of the round-40/41/42/44/49 "
    "notes' Still-Frontier lists). Paste-ready, no placeholders except `<REV>`/counts marked FILLED-AT-LANDING.")
add("ScribeReadmeMap", "scribe",
    "Draft the corpus/README.md bindings at `{ROOT}/{W}<SEAT>/readme.md`: (1) the `## Coverage map` row for the entry "
    "stem `{ENTRY}` (section name 'SquashFS LE AVM members (round 50)' with entry stem + state 'Core on four pinned vendor "
    "carriers, bounded' + the supersession note for the round-49 note's LE-AVM clause); (2) the `## Frontier` edit: remove "
    "the LE-AVM `hsqs` clause, keep the ~13k-file clause, name the superseding entry; (3) the `## Knowledge` index row "
    "(entry stem, topic, source `S243, S244, S245, S249; receipts corpus/evidence/round-50/c1/; counter "
    "tools/round-50/c1-counter.py`, verified-at 2026-10-29). Study how the round-49 rows are written "
    "(`{ROOT}/corpus/README.md`, coverage-map row for `2026-10-28-r49-squashfs-v1v2-core`). Paste-ready.")
add("ScribeCapabilityRow", "scribe",
    "Draft the SCORECARD bindings at `{ROOT}/{W}<SEAT>/scorecard.md`: (1) the capabilities-table row (name: 'AVM LE "
    "SquashFS v4 carrier custody + REA extraction' \u2014 what it can now do in one line, evidence pointer "
    "`corpus/evidence/round-50/c1/` + the counting command, first-working round 50); (2) a `## Round 50, attempt 2 "
    "(2026-10-29)` section skeleton mirroring `## Round 34, run-6 re-dispatch (2026-10-25)` (read it): claims table "
    "(R50-C1 coverage, R50-C3 depth) with before/after/command columns, placeholders FILLED-AT-LANDING; (3) the exact "
    "replacement text for the `## Owned axes` coverage row's leading fraction and evidence pointer so it reads "
    "`140/140 knowledge files mapped at the round-50 attempt-2 landing` with the new entry named \u2014 read the current row "
    "first (`{ROOT}/SCORECARD.md`, `## Owned axes`) and keep every later historical clause intact (the frozen C2 atom B1 "
    "re-derives the FIRST `N/N knowledge files mapped` occurrence, so 140 must lead). Paste-ready blocks.")
add("ScribeLessonGate", "scribe",
    "Draft the attempt-2 additions to `{ROOT}/corpus/lessons/round-50.md` at `{ROOT}/{W}<SEAT>/lesson.md` (append-only; "
    "the L1 appends, you draft): a `## Attempt 2 (2026-10-29, re-dispatch)` header; Gate rows for the four re-opened "
    "sources S243/S244/S245/S249 (URL, access dates 2026-10-28 and 2026-10-29, the <=25-word located quotes with line "
    "numbers from attempt-1 receipts `{ROOT}/.ufo/waves/round-50/w1/C1SrcFreetz.md`, `C1SrcUnblob.md`, `C1SrcAvmIndex.md` "
    "\u2014 re-verify each quote against your own re-fetch or say so); the registry-diff block (rows 152 -> 156, ids "
    "S243/S244/S245/S249, S150-S242 skipped on purpose, statement carried from attempt 1); the assimilation block "
    "(theme AVM LE reaffirmed: staged S206 re-grounded as S243 \u2014 admit; `avm-le-image-genuine-marker` and "
    "`avm-le-variant-reachability` stay refused with attempt-1's reasons and flip conditions, read them from "
    "`{ROOT}/.ufo/waves/round-50/w1/C1SrcFreetz.md` F6 / the attempt-1 lesson Gate and restate); the census before/after "
    "block (start receipt `.ufo/waves/round-50/l1/sources-census-start-attempt2.txt`, exit 0, 15 W04, 152 rows).")
add("ScribeLogDraft", "scribe",
    "Draft the LOG.md attempt-2 entry at `{ROOT}/{W}<SEAT>/log.md`: `## 2026-10-29 \u2014 round 50 attempt 2 (KaidokuR50), "
    "re-dispatch after the run-11 wrap-up release` with bullets: the resume decision (claims released without advance; C1 "
    "resumed under the frozen bytes, verified unchanged receipt `.ufo/waves/round-50/l1/frozen-unchanged-attempt2.txt`); "
    "C3 declared (depth, W2Skill F1/F2); the wave-3 shape (37 seats, role mix placeholder); the C3 freeze placeholder "
    "(hash FILLED-AT-LANDING); controls/data-run placeholders; landing placeholders. Study the LOG.md round-50 attempt-1 "
    "entry style (`{ROOT}/LOG.md` tail). Keep the lane's evidence-per-bullet style: every bullet names a path or command.")

# ------------------------------------------------------------------ C3 instrument build
add("ExecTriageV5", "executor",
    "Build the C3 scoring instrument draft `{ROOT}/{W}<SEAT>/tools/round-50/sqfs-triage-v5.py` (stdlib only, honours "
    "TMPDIR and `--work`, never writes under `/tmp`). Port `{ROOT}/tools/round-42/sqfs-triage-v4.py` (read it fully; keep "
    "its parse rules: marker line, column order, glob semantics, action-column scoring). CLI: `--root LANE --rev REV "
    "--freeze FREEZE --envelopes DIR --json-out PATH --selftest [--skill PATH]`. It reads SKILL.md from git at `--rev` "
    "(`git -C root show REV:SKILL.md`; read-only), parses the `<!-- sqfs-triage-table v5 -->` table, and for each envelope "
    "in DIR computes (a) the table label via the v5 rows and (b) the evaluator label from the envelope's declared tuple + "
    "the C3 precedence text in `{ROOT}/plans/round-50-attempt2-claims.md` R50-C3: no-independent-reader families "
    "(squashfs_v2_nonstandard, squashfs_v3_broadcom, squashfs_v3_nonstandard) take `clean-unverified` (gaps none, >0 "
    "files, action `record-unverified`) or `no-reader-failure` (extractor-failure, 0 files, action `preserve-unresolved`); "
    "reader-backed families (squashfs_v1, squashfs_v2, squashfs_v3, squashfs_v3_ddwrt, squashfs_v4*, both v4s) keep the "
    "v4 rows with `legacy-body-failure` narrowed to the reader-backed v1-v3 families. Output JSON: `pair_mismatches` "
    "(envelope, table label, evaluator label), `evaluator_missing`, `table_labels`, `n_envelopes`, plus per-envelope "
    "detail. `--selftest` (offline, fixtures built under `--work`): (1) the v4 table at base parsed by the v5 parser "
    "mismatches the evaluator on the four v2ns `_ddefault` envelopes (red-before witness); (2) a v5 table draft (embedded "
    "string) matches on all of: 2 v2ns clean, 1 v2ns failed, 2 v3-family legacy rows, 3 clean v4 rows, 1 symlink row; (3) "
    ">=6 single-point table mutations each flip >=1 pair (guard row deleted; glob widened to `squashfs_v[123]*`; action "
    "swapped on the new rows; a no-reader family moved to `clean`; precedence order swapped; a cell blanked) \u2014 none a "
    "no-op, none cross-flipping. Test against the real envelope dir "
    "`{ROOT}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` in read-only mode and report the label "
    "distribution table v4 produces today (this is the before-state evidence). Do NOT edit SKILL.md.")
add("ExecTriageControls", "executor",
    "Build the C3 control fixtures + receipts at `{ROOT}/{W}<SEAT>/`: (1) `envelopes-manifest.json`: sha256 + size + "
    "declared-tuple summary for every envelope in "
    "`{ROOT}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` (expect 126; name exactly the four v2ns "
    "`_ddefault` files); verify the count and that the dir is committed at base (`git ls-tree`). (2) The four control "
    "tables as files: `ctl-do-nothing` = the v4 table extracted at base (extract, do not hand-copy); `ctl-junk` = a table "
    "where every row's label is `clean`; `ctl-guard-deleted` = the v4 table with the `legacy-body-failure` row removed; "
    "`ctl-action-swapped` = the v4 table with the `clean` row's action replaced by `inspect-input`. For each, write "
    "`expected-red.json` naming the clause that must fire (mismatch count > 0, which envelopes). (3) A README mapping each "
    "control to the kill-rule clause it guards. Nothing here runs the real instrument (it does not exist yet); the L1 runs "
    "them post-freeze.")
add("ExecRegistryRow", "executor",
    "Draft the instrument-registry v2 row for `tools/round-50/sqfs-triage-v5.py` at `{ROOT}/{W}<SEAT>/registry-row.md`. "
    "Read the region between the `instrument-registry v2` markers in `{ROOT}/SKILL.md` and the 12 rows the round-50 "
    "attempt-1 landing added (six tools/round-49, six tools/round-50); mirror their exact cell grammar (cell-0 path; "
    "gate|probe kind; entry command `python3 -I -B tools/round-50/sqfs-triage-v5.py`; verdict map binding 0/1/2 to "
    "meanings per the round-48 meaning rule; self-test spelling `--selftest`; pinned-value path = the envelopes manifest). "
    "Then verify the B9 coupling: simulate the landing set (every `tools/round-50/**` .py/.sh at the future REV = the "
    "current 6 + `sqfs-triage-v5.py`) against the region rows and confirm each is cell-0 of exactly one row; name any "
    "other path that would dangle. Read `{ROOT}/tools/round-50/c2-record.py` atom B9 first so your simulation uses its "
    "exact derivation.")
add("ExecB1Impact", "executor",
    "Verify the C2 B-atom couplings at the planned attempt-2 landing. Read `{ROOT}/tools/round-50/c2-record.py` "
    "(atoms B1-B11) and `{ROOT}/plans/round-50-claims.md` (B-atom definitions). Produce `impact.md`: (1) B1: the "
    "knowledge-file count at base (`git ls-tree -r --name-only {BASE} -- corpus/knowledge | grep -c '\\.md$'`) and at the "
    "planned landing (+ the C1 entry) = 140; the exact text the coverage row must lead with; (2) B9: the registry region "
    "derivation at the planned landing (see the sibling seat's method) \u2014 confirm `sqfs-triage-v5.py` is the ONLY new "
    ".py/.sh under tools/round-50; (3) every other atom: which files it reads at which rev and whether the planned "
    "landing (entry, PROVINCE round-50 section, README rows, SOURCES S243-S245/S249, SKILL rule block 22 + one registry "
    "row, SCORECARD attempt-2 section + coverage-head update) can flip it \u2014 name any risk and the mitigation; (4) the "
    "re-run command the L1 runs at the final REV to prove `mismatches 0` (the exact argv).")
add("ExecCounterSelftest", "executor",
    "Run the frozen instruments' OFFLINE selftests at base and record receipts under `{ROOT}/{W}<SEAT>/`: "
    "`python3 -I -B {ROOT}/tools/round-50/c1-counter.py --selftest` (expect 169 cases, failures [] \u2014 attempt-1 "
    "recorded that at the freeze; confirm it still holds at base), `python3 -I -B {ROOT}/tools/round-50/c1-controls.py "
    "selftest` (expect 20/20), `python3 -I -B {ROOT}/tools/round-50/c2-record.py --selftest` (29 cases), "
    "`python3 -I -B {ROOT}/tools/round-50/selftest-r49-c2.py --root {ROOT}` (exit 0, failures []). Scratch under `$S`; "
    "c2-record needs `--work` under `$S`. Record exit codes, case counts, wall times, and the tool versions (python3 "
    "--version). NO REA, no carrier fetches.")
add("ExecCensusMid", "executor",
    "Record the attempt-2 SOURCES census receipts at `{ROOT}/{W}<SEAT>/`: run the frozen manual census commands from "
    "/home/vgpnk/Projects/shokunin/CORPUS.md section 'Census' against `{ROOT}/corpus/SOURCES.md` (rows count, malformed-"
    "rows count, tier histogram, status histogram, duplicate ids, enum violations, mined-used-by existence) and save each "
    "command + output. Then run "
    "`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` and "
    "save its full output (expect exit 0, 15 W04 lines, final line `kaidoku ok ...`; compare with "
    "`{ROOT}/.ufo/waves/round-50/l1/sources-census-start-attempt2.txt` and flag any drift). Also compute the row count "
    "(`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' {ROOT}/corpus/SOURCES.md`) \u2014 this is the before number (152) the "
    "report needs.")
add("ExecAssimGuard", "executor",
    "Re-run the assimilation id-collision guard at the current registry (attempt-1 receipts exist at "
    "`{ROOT}/.ufo/waves/round-50/assimilation/`; re-derive at the tip). In `$S`: the exact guard from "
    "`{ROOT}/plans/round-50-claims.md` section 'Assimilation' (grep 0-3-space pattern on "
    "`{ROOT}/corpus/SOURCES.md` -> reg-ids; same on `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` -> "
    "staged-ids; `comm -12` -> collisions). The registry now holds S246-S248 beyond attempt-1's S001-S149 \u2014 recompute the "
    "overlap count (attempt 1: 44 ids, 0 same-source) and state whether any of S246-S248 collides with a staged id. "
    "Re-derive the quarantine slice (the awk from the plan) and count rows (attempt 1: 5). Copy the receipts (reg-ids, "
    "staged-ids, collisions, quarantine-slice) into `{ROOT}/{W}<SEAT>/assimilation/`. The source repo is READ-ONLY: run no "
    "campaign tool there, never write there.")
add("ExecErrataSweep", "executor",
    "Carry-over audit of attempt 1's not-landed list. Read `{ROOT}/.ufo/reports/round-50/kaidoku.md` is NOT readable "
    "(fleet repo, read-only is fine actually: `{ROOT}` is the lane; the report lives at "
    "`/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kaidoku.md` \u2014 read it) section 'Not landed': the C1 entry, "
    "PROVINCE/README/SKILL/SCORECARD bindings, SOURCES rows S243-S245/S249, SHONEN promotion, wave-2 seats, QUALITY row "
    "94 dropped. For each item: is it addressed by this attempt's plan "
    "(`{ROOT}/plans/round-50-attempt2-claims.md`) \u2014 yes/no/partial, and by which seat or L1 step. Also read "
    "`{ROOT}/.ufo/waves/round-50/controls-attempt1/` receipts and tabulate exactly which controls scored `as_expected` vs "
    "`could_not_evaluate` and the error text (the attempt-2 controls run must re-score the latter). Output: "
    "`carry-over.md` checklist.")
add("ExecFetchDry", "executor",
    "Dry-run the C1 fetch chain (no image downloads). Read `{ROOT}/tools/round-50/fetch-vendor.py` (its `--spec --root "
    "--rev --cache --image-cache --json-out --selftest` CLI) and `{ROOT}/tools/round-50/carriers.json`. Determine and "
    "record: the exact argv the L1 runs to materialise all four carriers into "
    "`/fast/scratch/hyaku/kaidoku-r50/carrier-cache/` (what `--rev` must be and why \u2014 read how the script resolves the "
    "spec at the rev); what `fetch-vendor.py --selftest` covers (run it, scratch only); the containment rules it enforces "
    "(origin allowlist, cache-not-in-lane, pin checks); estimated download size per carrier (HTTP HEAD Content-Length; "
    "record the four). Then verify the counter's expectations: how `c1-counter.py --carrier-cache` resolves `<pin>.bin` "
    "names (read the code) \u2014 confirm `<pin>` is the carrier `sha256` field. Output `fetch-plan.md` with the exact "
    "commands.")
add("ExecOracleVerify", "executor",
    "Independently spot-check ONE frozen oracle table before the data run: c6430 (smallest). Fetch "
    "`https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image` into "
    "`$S` (record sha256 against the frozen `image_sha256` 52e3687d... in `{ROOT}/tools/round-50/carriers.json`), extract "
    "tar member `./var/remote/var/tmp/x86/filesystem.image` (record member sha256 against the frozen "
    "`member_sha256`), carve to `bytes_used` (read the superblock at offset 0: magic hsqs, bytes_used; the frozen carrier "
    "length is 23,861,507 \u2014 your carve must hash to the frozen carrier sha256 da1c8049...). Then run `/usr/bin/unsquashfs "
    "-lls` on the carve + `{ROOT}/tools/round-41/sqfs-list.py --layout auto` (read `--help` first) and compare BOTH "
    "against the frozen `{ROOT}/tools/round-50/oracle/c6430.oracle.tsv` + `c6430.nonregular.tsv`: row counts equal, and "
    "sha256 equal for a deterministic sample of 25 rows (first 10, last 10, 5 hash-random) plus ALL nonregular rows. Any "
    "disagreement is a STOP-THE-CLAIM finding \u2014 report it loudly. Record every command + exit + table counts. Vendor "
    "bytes stay in scratch; never into the lane tree.")
add("ScoutQuietWindow", "scout",
    "Characterise the host-load window for the REA-dependent steps (the L1 schedules controls + the C1 data run after "
    "this wave). Over ~10 minutes sample `uptime` and `vmstat 5 5` every ~2 min into `{ROOT}/{W}<SEAT>/load-samples.tsv` "
    "(UTC, load1/5/15, us/sy/id/wa). Read `{ROOT}/.ufo/waves/round-50/l1/dev-arm-timeouts.txt` and the "
    "`{ROOT}/.ufo/waves/round-50/controls-attempt1/` receipts: tabulate at which load the 120 s `provider_timeout` fired "
    "vs succeeded (attempt-1 data: 40-48 s at load 40-54; timeouts at 42-54 once and 95-176 in the controls window). "
    "Also read `/home/vgpnk/.omp/agent/config.yml` keys `async.maxJobs` and `task.maxConcurrency` (read-only) and report "
    "them. Conclude with a threshold recommendation (e.g. 'start when load1 < N') and a monitoring one-liner the L1 can "
    "re-run. Do not run REA; do not start heavy processes.")

# ------------------------------------------------------------------ attacks
add("CritC3Design", "critic",
    "Attack the C3 claim design BEFORE its freeze. Read `{ROOT}/plans/round-50-attempt2-claims.md` R50-C3, "
    "`{ROOT}/SKILL.md` rule block 21 (the v4 table) and rule block 20/21 headers for the supersession style, and "
    "`{ROOT}/.ufo/waves/round-49/w2/W2Skill.md` F1/F2. Questions: (1) predicate identity \u2014 is the predicate sentence "
    "in the claims file the same sentence the instrument's docstring will carry (the sibling seat builds it; check the "
    "claims text is freeze-ready)? (2) do the new no-reader labels contradict any S112/S119/S120-cited semantics in the "
    "v4 rows (quote the cells)? (3) is `squashfs_v3_ddwrt` correctly reader-backed (check "
    "`{ROOT}/corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`: oracle backhand-cli + 7-Zip) and does the narrowed "
    "`legacy-body-failure` glob keep it? (4) the before-state: at base, does the v4 table really label the four v2ns "
    "`_ddefault` envelopes `clean`/`none` \u2014 verify by running `{ROOT}/tools/round-42/sqfs-triage-v4.py --skill "
    "{ROOT}/SKILL.md --json` over "
    "`{ROOT}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` (read its `--help`; scratch outputs only) and "
    "pasting the four rows; (5) junk controls \u2014 is any control green-by-accident (e.g. does the junk table produce zero "
    "pairs because the evaluator also says clean)? Name each hole with the fix. Do not edit anything.")
add("CritC1Resume", "critic",
    "Attack the C1 resumption. Read `{ROOT}/plans/round-50-claims.md` (R50-C1 predicate + controls + kill rule), "
    "`{ROOT}/plans/round-50-attempt2-claims.md`, and attempt-1's controls receipts "
    "`{ROOT}/.ufo/waves/round-50/controls-attempt1/`. Verify with commands: (1) frozen bytes unchanged "
    "(`git -C {ROOT} diff --stat {FREEZE} {BASE} -- tools/round-50/ plans/round-50-claims.md` \u2014 must be empty); (2) the "
    "predicate's date window 'SOURCES rows opened 2026-10-28..2026-10-29' is still satisfiable today (2026-10-29) and "
    "the four planned rows carry `opened` 2026-10-28; (3) `mkplan.py --check`-style predicate/docstring equality: does "
    "`{ROOT}/tools/round-50/` contain the mkplan checker or is the equality asserted another way \u2014 find how attempt 1 "
    "proved it (read `.ufo/waves/round-50/l1/` for mkplan outputs) and say whether it re-runs at scoring; (4) kill-rule "
    "coverage: name any CTL that could reach the target green WITHOUT the claim being true (the forgery CTL-C1-2 route) "
    "and any clause that could go red for environment reasons at scoring time (host load, unsquashfs version drift "
    "\u2014 record `/usr/bin/unsquashfs --version` today vs the frozen 4.7.5); (5) the controls-before-data order: is it "
    "actually enforceable (what in the frozen harness stops a data run before controls are scored)? Report every hole "
    "with its minimal fix-as-process (the L1 cannot amend the freeze).")
add("CritSourcingRules", "critic",
    "Attack the planned SOURCES rows against the contract. Read `/home/vgpnk/Projects/shokunin/CORPUS.md` section "
    "SOURCES.md (contract v1 rules 1-6) and `{ROOT}/corpus/QUALITY.md` rows 42, 35, 36, 93. For each planned row "
    "S243/S244/S245/S249 (drafts land from the scribe seat; if absent, judge the plan text in "
    "`{ROOT}/plans/round-50-attempt2-claims.md`): (1) 11 columns, no `|` in any cell; (2) quote <=25 words, located, "
    "contiguous in the served bytes (the receipts carry sha256s); (3) tier per the CORPUS tier TEXT (quote it) \u2014 is "
    "tier B right for a distro patch file (S243)? is tier A right for a directory index (S244) and a licence text "
    "(S249)? (4) the W04 duplicate-URL warning S245 shares with S112/S108: confirm the validator still exits 0 with "
    "warnings (run it on a scratch copy with a draft S245 row) and quote the W04 line; (5) `used-by` points at a file "
    "that will exist only at the landing \u2014 is writing the row before the entry exists a violation of 'an index row is "
    "a claim' (CORPUS rule) or correct here (the row and the entry land in the same commit)? (6) is any of the four a "
    "correction needing `supersedes` instead (S112/S108/S114 stay byte-identical)? Verdict per row: register as "
    "planned / fix-then-register / refuse.")
add("CritB1Text", "critic",
    "Attack the planned SCORECARD coverage-head update. Read `{ROOT}/tools/round-50/c2-record.py` atom B1 and the "
    "current `## Owned axes` coverage row in `{ROOT}/SCORECARD.md`. The planned update (from the claims file): lead the "
    "row with `140/140 knowledge files mapped at the round-50 attempt-2 landing`. Check: (1) B1's exact derivation "
    "\u2014 does it read the FIRST `N/N knowledge files mapped` occurrence in the row, and does any earlier `N/N` appear "
    "in the row prefix that would shadow it? (2) does the update break B2 or any other atom that reads the same row or "
    "neighbouring rows? (3) the round-48/49 historical clauses in the row cite older counts (138, 133...) \u2014 confirm "
    "B1 only binds the first occurrence; (4) is `140` the right count (run `git ls-tree -r --name-only {BASE} -- "
    "corpus/knowledge | grep -c '\\.md$'` = 139 at base; +1 entry at landing)? Quote the derivation lines.")
add("RevEntryBar", "reviewer",
    "Pre-write the entry acceptance bar. Read `{ROOT}/corpus/QUALITY.md` rows 1-93 and "
    "`{ROOT}/plans/round-50-claims.md` R50-C1 predicate documentation bindings. Produce `bar.md`: the checklist a "
    "reviewer will apply to `corpus/knowledge/{ENTRY}.md` at the landing \u2014 numbered, each item citing the QUALITY row "
    "or predicate clause it enforces (provenance trio first citing S243/S244/S245/S249; observation/inference/unknown "
    "labels; what-was-NOT-examined; version pins rea-agents@6.5.0/unblob 26.6.4/sasquatch 4.5.1/unsquashfs 4.7.5; counts "
    "carry commands; the carrier-swap and marker-constant disclosures present; no credential material; no universal "
    "clauses beyond the enumerated four carriers; the entry's `source:` lines name rows whose `used-by` names the entry). "
    "For each item also give the one command that checks it. This becomes the falsify wave's entry-review rubric.")
add("RevB9Registry", "reviewer",
    "Review the existing instrument-registry rows as B9 sees them. Read `{ROOT}/tools/round-50/c2-record.py` atom B9 "
    "and the region between the `instrument-registry v2` markers in `{ROOT}/SKILL.md`. Verify at base: every "
    "`tools/round-49/**` and `tools/round-50/**` .py/.sh path (control fixtures excluded) is cell-0 of exactly one row "
    "with a gate|probe kind, an entry command naming the path, a verdict map binding 0/1/2, a selftest spelling and a "
    "pinned-value path (run the atom's own derivation logic by hand; the counter's `--selftest` covers shape, not this "
    "tree). Then check the 12 rows added at the attempt-1 landing for cell-shape drift that the counter's parser might "
    "miss (extra columns, nested pipes, trailing spaces). Report `b9-at-base: green/red` with the exact finding list.")
add("RevPrevArt", "reviewer",
    "Audit the round-41 -> round-50 counter port for scoring-time drift. Read "
    "`{ROOT}/tools/round-41/c1-counter.py` and `{ROOT}/tools/round-50/c1-counter.py` (both frozen; read-only), "
    "`{ROOT}/.ufo/waves/round-50/w1/C1CounterPort/PORT-DELTA.md`, and the docstrings of both. Produce `port-audit.md`: "
    "(1) every behavioural delta confirmed present (handler name, superblock layout, sasquatch binary, target ids, "
    "round tokens, provider_timeout retry, fetch containment, oracle re-derivation); (2) every round-41 clause that "
    "should have been ported but was not (name it, cite both line numbers); (3) every LE-specific clause with its "
    "selftest case; (4) the four documentation-binding clauses (PROVINCE section name, frontier-note tokens, entry stem "
    "token, README map, SOURCES window) \u2014 quote the exact literals the counter greps for, so the landing text uses "
    "THEM verbatim (this is load-bearing: a wording miss is a red binding at scoring time). No edits.")
add("RevV21Guard", "reviewer",
    "Four-file consistency matrix for the SquashFS family wording. Read `{ROOT}/SKILL.md` (decision-table SquashFS row + "
    "rule blocks 19-21), `{ROOT}/PROVINCE.md` (round-49 additions + frontier note), `{ROOT}/corpus/README.md` (coverage "
    "map + frontier + knowledge index), and `{ROOT}/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`. Build "
    "`consistency.md`: for each family (v1.0, v2.0, v2.1, v2ns, v3, v3_ddwrt, v3_broadcom, v3_nonstandard, v4 std LE/BE, "
    "AVM-BE, AVM-LE) \u2014 what status each of the five surfaces states today, and any contradiction (W2Skill F3 claimed "
    "PROVINCE was fixed at the attempt-1 landing: verify the landed row really scopes v1.0/v2.0, names the v2.1 "
    "exclusion, carries a Use/expect command and a refusal signature; quote the cells). Flag every place the "
    "attempt-2 landings (C1 entry + C3 block 22) must NOT contradict. No edits.")
add("MutPlan", "mutation-tester",
    "Mutation-test both claims' instruments BEFORE data (scratch only; frozen files copied to `$S`, never edited in "
    "place). (1) C1 counter `{ROOT}/tools/round-50/c1-counter.py`: run `--selftest`, then >=12 single-point mutations in "
    "the scratch copy (handler-name compare, marker equality, bytes_used bound, evidence-id recompute, projection "
    "compare, oracle path map, parameters prefix test, TARGET constant, receipt first-add check, full-history flag, "
    "unblob pin, sasquatch pin); for each: does `--selftest` catch it (exit != 0)? List SURVIVORS with a one-line "
    "suggested case. (2) The v4 evaluator `{ROOT}/tools/round-42/sqfs-triage-v4.py` vs the planned v5 precedence: which "
    "single mutation of the v4 TABLE (not the evaluator) flips the four v2ns `_ddefault` labels \u2014 confirm at least the "
    "glob-widening is the load-bearing defect (W2Skill F1) by constructing the minimal v4-table mutant that re-labels "
    "v2ns correctly and showing the evaluator agrees (scratch). Both receipts with commands + exits.")
add("RevTriageV4", "revenger",
    "Reverse-engineer the v4 table/evaluator contract precisely, so the v5 port cannot silently diverge. Read "
    "`{ROOT}/tools/round-42/sqfs-triage-v4.py` in full and `{ROOT}/SKILL.md` rule block 21. Document: the marker-line "
    "grammar; column order and which columns are scored; glob semantics per column (`*`, `+` suffix, `squashfs_v[123]*` "
    "\u2014 is it fnmatch or a custom matcher?); row precedence (first match wins?); how the evaluator derives the expected "
    "label from an envelope's declared tuple (fields, precedence rules, tie-breaks); what `action` mismatches count vs "
    "`label` mismatches. Then: name the four v2ns `_ddefault` envelope files exactly and state what label v4 gives each "
    "today and what the evaluator (v5 precedence) would give (`clean-unverified` or `no-reader-failure`) \u2014 with the "
    "declared-tuple fields that decide. Output `v4-contract.md` with line citations.")
add("SentReceipts", "sentinel",
    "Security review of this attempt's receipt path. (1) Scan the attempt-1 wave evidence that this attempt re-uses "
    "(`{ROOT}/.ufo/waves/round-50/w1/C1Src*` receipt dirs, `{ROOT}/.ufo/waves/round-50/l1/`) for credential-class "
    "material (Set-Cookie values, `_gh_sess`, tokens, `op://` refs) \u2014 command + hit count; the round-45 `f1.hdr` "
    "incident is the precedent (values redacted at the tip in commit 11ccdb72; history unpurged, L0 open). (2) Re-verify "
    "`{ROOT}/tools/round-50/fetch-vendor.py` containment at base: origin allowlist exactly `https://download.avm.de`, no "
    "`file://`, cache refuses a lane-resident path, TLS verification on, redirect handling, no header persistence. (3) "
    "Check `.gitignore`/`.gitattributes` for anything that would accidentally commit a `.image`/`.bin` dropped in the "
    "tree. Findings with file:line + one-command repro each.")
add("ConnCrossClaim", "connector",
    "Cross-claim coupling matrix for attempt 2. Files both claims may write or read: `SCORECARD.md` (C3 attempt-2 "
    "section + capability row; C1 coverage-head update), `LOG.md` (one entry or two), `SKILL.md` (C3 block 22 + registry "
    "row; C1 needs NO SKILL edit \u2014 confirm), `PROVINCE.md` (C1 round-50 section + note; C3 possibly the round-49 row "
    "refusal-signature residue), `corpus/README.md` (C1 rows), `corpus/SOURCES.md` (C1 rows S243-S245/S249), "
    "`corpus/knowledge/{ENTRY}.md` (C1), `tools/round-50/sqfs-triage-v5.py` (C3). Read the frozen counters' walks "
    "(`{ROOT}/tools/round-50/c1-counter.py`, `c2-record.py`) and produce `coupling.md`: per file, which claim writes "
    "which region, which counter/atom reads which region, the safe landing order, and any landing text that could flip "
    "B1/B9 or a C1 documentation binding. Name the single riskiest coupling and its mitigation.")
add("ConnSiblings", "connector",
    "Sibling-overlap scan (required connector seat). Read-only: grep `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md`, "
    "`*/SKILL.md`, `*/corpus/knowledge` (skip kaidoku) for `squashfs_v2_nonstandard`, `v3_broadcom`, LE AVM, `hsqs`, "
    "`sqfs-triage`; and `/home/vgpnk/Projects/shokuknow/merge/*/knowledge` for the same tokens (which sibling could "
    "adopt the no-reader triage ground first). Also confirm no sibling owns FRITZ!Box firmware extraction (revenger "
    "arbitration ADJ-06 was about runtime debugging, not extraction \u2014 verify from "
    "`/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md`). Report the adjacency sentence the C3 landing and the "
    "C1 entry should carry (expected: none needed \u2014 say so with the grep evidence).")


def main():
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES} for t in T]
    spec = {"wave": WAVE, "milestone": MILE, "reportDir": REPORT, "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w3-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path], capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s" % (proc.returncode, proc.stdout[:1500], proc.stderr[:1500]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {t["name"]: {"kind": "spawn", "agentId": None, "role": t["agent"], "item": None,
                           "axes": AXES, "milestone": MILE} for t in wave_tasks}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": WAVE, "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1", "path": ".ufo/waves/round-50/w3/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None, "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0, "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": "Issue exactly one batched task call with taskCall ({context, tasks}); never split a wave.",
    }
    with open(os.path.join(WAVE_DIR, "w3-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w3"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w3/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": WAVE, "reportDir": REPORT, "members": members}, f, indent=1)
    if "--no-ready" in sys.argv:
        print("ready file NOT written (--no-ready)")
    else:
        with open(os.path.join(WAVE_DIR, "w3.ready"), "w") as f:
            json.dump({"lane": "kaidoku", "round": 50, "wave": WAVE,
                       "dispatch": os.path.join(WAVE_DIR, "w3-dispatch.json"), "l1": "KaidokuR50"}, f)
        print("ready written:", os.path.join(WAVE_DIR, "w3.ready"))
    print(json.dumps({"items": len(items), "counts": plan["counts"],
                      "roles": {r: sum(1 for t in T if t["agent"] == r) for r in sorted({t["agent"] for t in T})}}, indent=1))


if __name__ == "__main__":
    main()
