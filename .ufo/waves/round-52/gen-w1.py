#!/usr/bin/env python3
"""Generate the kaidoku round-52 wave-1 (build+attack, v2 policy) spec. R52, KaidokuR52.

Interpolation-check obligation (M51-6): this generator substitutes LANE/W1/BASE at build
time; the emitted item strings must contain no `{...}` placeholders. The separate
check-dispatch.py asserts that before the ready file is written.
"""
import json, pathlib

GS = open('/home/vgpnk/.agents/skills/godspeed/directive.md').read().strip()
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W1 = LANE + '/.ufo/waves/round-52/w1'
BASE = 'ab0eafedc41402b43b41a4362084119578dfe7ce'          # claims-draft commit
LANEBASE = 'c525de54a53eb3c4fee28ede2721da4527cf8ece'      # round-start tip

CONTEXT = f"""# Target
kaidoku-shokunin round 52, attempt 1, wave r52-w1 = the single v2 BUILD+ATTACK wave (64 seats,
policy band 64-128). The device-accounting-law re-freeze package (counter v2, controls,
harness, fetcher) and the triage v6 executability audit, plus doc/source/assimilation work and
pre-freeze attacks. The round freeze (ONE commit adding the round-52 instruments + fixtures +
amended claims) lands AFTER this wave; the L1 alone then scores the pre-freeze controls and
runs the four-carrier vendor re-fetch + REA data run in a quiet window; a falsify wave may
follow the landing. Lane root (absolute): {LANE}. L1 = KaidokuR52 (integration owner; it holds
the section-3 planner seat - the validator rejects `planner` as a swarm role).
Round base `{LANEBASE}` (round-start tip, pushed); claims draft `{BASE}` =
{LANE}/plans/round-52-claims.md (the round's rule - read it, not this prompt).

# The claims (one line each; the plans file is authoritative)
- **R52-C1 coverage**: land the law-derived gap-accounting package (tools/round-52/) and
  promote LE AVM members (`hsqs`) Frontier -> Core, target `carriers_matched == 4`
  (g7581, g7582, c6490, c6430) under the corrected device-accounting law with
  `law_shape_ok`/`census_rederived_ok`/`depth_gap_recorded` true and every binding true.
  Before-state: round-50 receipt `carriers_matched 2` exit 1
  ({LANE}/.ufo/waves/round-50/l1/scores/c1-after-attempt2.json).
- **R52-C2 depth**: triage table v6 as SKILL.md rule block 27 + instrument
  {LANE}/tools/round-52/sqfs-triage-v6.py; the ddwrt FAILED no-pad body
  `dmg_Z3_v3ddwrt_inode_table` must stop routing `legacy-body-failure`/`cross-read-legacy`
  (new row `legacy-body-unreadable`, action `preserve-unresolved`, no cross-read); frozen
  executability audit: before 1 violation at `{BASE}` over the v5 table bytes, after 0;
  `census_outside` 0 both sides (census3 landed in round 51 - a no-regression binding).
- Round-50/51 state you build on: miss receipt above; committed receipts
  {LANE}/corpus/evidence/round-50/c1/<id>/{{run.json,after.json}} (c6430, c6490, g7581, g7582);
  oracle tables {LANE}/tools/round-50/oracle/*.tsv; frozen rule
  {LANE}/tools/round-50/gap-rule.json; counter {LANE}/tools/round-50/c1-counter.py;
  harness {LANE}/tools/round-50/c1-run.sh; fetcher {LANE}/tools/round-50/fetch-vendor.py
  (ALLOWED_HOST download.avm.de); triage v5 {LANE}/tools/round-50-c3/sqfs-triage-v5.py;
  census {LANE}/tools/round-51/census3.py + census3.json; r51 wave drafts under
  {LANE}/.ufo/waves/round-51/ (evidence only - the r51 instruments never landed).

# Contract (binding on every seat)
- **Read-only on the lane tree.** Write ONLY inside {W1}/<YourSeatName>/ (create it) and your
  report file {W1}/<YourSeatName>.md. Drafts (instruments, docs, rows) go under
  {W1}/<YourSeatName>/ - never into the lane's tools/, plans/, corpus/, SKILL.md,
  PROVINCE.md, LOG.md, SCORECARD.md, SHONEN.md, nor the fleet repo. Never commit, push,
  stage, stash, or run any mutating git/jj command in the lane or fleet repo. Read-only git
  (log, show, diff, ls-tree, rev-parse, cat-file, merge-base) is fine.
- **status.json (routed defect 2):** before you yield, write
  {W1}/<YourSeatName>/status.json as an object {{"seat":"<YourSeatName>","role":"<role>",
  "status":"settled"|"failed"|"blocked","summary":"<=40 words","artifacts":["<relative paths
  under your seat dir>"]}} - the L1's wave accounting parses these files, not prose.
- **No REA runs this wave.** The L1 alone runs REA (controls + data run) after the wave, so
  host load stays predictable. Do not invoke `npx rea-agents`, `rea`, or the package at
  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents - READING its source files is
  allowed where your task names it. Offline selftests and synthetic-fixture probes
  (mksquashfs/unsquashfs/sasquatch in your scratch) are allowed where your task names them.
- **Downloads**: only where your task names a URL (at most the URLs your task names), into
  your scratch only; **vendor firmware bytes are never copied into the lane tree** (AVM
  licence) - only hashes, listings, receipts. Never paste session cookies, tokens or
  `Set-Cookie` headers into any receipt: strip headers before saving.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`; every later git call
  names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first
  commit; set `user.name`/`user.email` in that clone only. Never run `git commit` with a
  throwaway identity anywhere else. Prefer `git clone --shared {LANE} "$S/clone"` +
  `git -C "$S/clone" checkout --detach {BASE}` for a lane copy.
- **Scratch**: `S=/fast/scratch/hyaku/kaidoku-r52/w1-<YourSeatName>`; `mkdir -p "$S"`,
  `export TMPDIR="$S"`. Remove `$S` before you yield AFTER copying receipts into
  {W1}/<YourSeatName>/. Never write under /tmp; nothing under /tmp is citable. Check
  /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status before a heavy pass.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout
  sha256 and UTC time. A check you did not run is not passed - say "not run". Never fabricate
  output. Exit codes are semantic: 0 met/clean, 1 not met/violation, 2 could-not-evaluate.
- **Absolute paths**: your tools start at the fleet root, not the lane. The `Report:` trailer
  path in your prompt is relative to {LANE} - write it at {LANE}/<that path>
  ({W1}/<YourSeatName>.md). A file written at a relative path lands in the FLEET repo and is
  a defect.
- **Tooling authorization (operator, 2026-10-19)**: you may install/upgrade tools that help
  the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate;
  record tool/version/channel/reason in your report). **pacman guard**: all pacman
  transactions are PAUSED host-wide - install only via `uv tool`/`npx`/an official binary in
  ~/.local/bin, or nothing. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart a host
  service.
- Never message `agent://all`; never touch a sibling lane, .ufo/state/, .ufo/watchdog.log,
  /home/vgpnk/Projects/shokunin/.scratch/, or the fleet repo. Never run a `--data-run`, never
  write into corpus/evidence/. An executor seat may spawn ONE read-only labrat probe for a
  falsifiable hypothesis; no other seat spawns anything.
- Return a final message of at most 8 lines: your verdict, the 1-3 most important findings,
  your report path.

# What the L1 does with your output
It reads every report + status.json, integrates the drafts (rule, counters, controls, entry,
rows, bindings), amends the claims file from attack findings, commits ONE freeze (instruments
+ claims + fixtures), scores the pre-freeze controls, re-fetches the four carriers through the
pinned vendor chain, runs the REA data run, lands everything, and dispatches a falsify wave
against the landed bytes. Drafts you write are inputs the L1 reviews and may rewrite. Report;
do not wait for others."""

def item(name, role, task):
    return {"name": name, "role": role, "prompt": f"/skill:godspeed\n\n{GS}\n\n{task}"}

items = [
# ---------------- executors (17) ----------------
item("ExecCounterV2", "executor",
f"""Port the C1 counter to the round-52 freeze. Read {LANE}/tools/round-50/c1-counter.py (port
it, do not rewrite its semantics) and {LANE}/plans/round-52-claims.md (R52-C1). Produce the
full draft {W1}/ExecCounterV2/c1-counter.py changing exactly: GAPRULE default ->
tools/round-52/gap-rule.json; frozen walk -> tools/round-52/**, plans/round-52-claims.md,
tools/round-50/carriers.json, tools/round-50/gap-rule.json, tools/round-50/oracle/**,
tools/round-50-c3/sqfs-triage-v5.py; constants per the claims (entry stem
2026-10-30-r52-avm-le-squashfs-core, core_heading `## Round-52 additions to Core`,
frontier_mark `Round-52 frontier note`, opened 2026-10-30, prov_base
/fast/scratch/hyaku/kaidoku-r52, receipts dir corpus/evidence/round-52/c1, scratch prefix
/fast/scratch/hyaku/kaidoku-r52/); claim grammar accepts {{R50-C1, R52-C1}}; NEW clauses:
law_shape_ok (allowed[device-kind]==[] and no device detail under removed.silent),
census_rederived_ok (score-time non-regular census re-derivation via the frozen reader +
unsquashfs -lln, both directions, exit 2 oracle_env_error when the reader cannot run),
depth_gap_recorded (receipt records the depth-limited gap's input_path + continuation_id),
prior-pins allow-list re_scored_pins for exactly the four round-50 pins (carrier_fresh_ok =
fresh OR allow-listed; receipt names prior_pin_sources), projection retry policy: up to 3
attempts on provider_timeout AND up to 2 on execution_failure whose failing diagnostic names
an ENOENT inside the extraction tree, fresh extraction root per attempt, attempt count +
failing diagnostic recorded, any other error red; freeze-drift gating exit 2
frozen_path_changed with a selftest case proving exit 2 on a mutated frozen byte. Keep the
whole binding set and exit-code map of v1. The counter MUST be runnable with --selftest
offline (fixture trees in scratch, never the live lane). Python 3 -I -B compatible. If the
port exceeds your budget, deliver the complete diff-spec (hunk-level) instead of a partial
file - never a broken file."""),
item("ExecControls", "executor",
f"""Port the C1 controls driver. Read {LANE}/tools/round-50/c1-controls.py and
{LANE}/plans/round-52-claims.md (R52-C1 controls bullets). Produce the full draft
{W1}/ExecControls/c1-controls.py implementing the round-52 pre-freeze control set over
committed round-50 receipts (offline; no REA): CTL-OLD (round-50 gap-rule.json via the v2
counter's controls mode -> expect carriers_matched 2, exit 1), CTL-NEW (round-52 law rule ->
expect 4, exit 0), CTL-DN (empty/absent receipt dir -> exit 1 or 2, never 0), CTL-JUNK (a
syntactically valid junk rule requiring every kind with an impossible allowance -> 0 of 4,
exit 1), and the rule-mutation fixtures from the claims (M1 all-thirteen whitelist -> red by
law_shape_ok; M2 fourteenth-device census fixture -> green under the law, red under any
whitelist; M3 required.char-device=true + only 247:0 -> reproduces the 2/4 miss; M4
strict-subset whitelist -> red). The driver pins the round-50 constants explicitly
(--provenance-base /fast/scratch/hyaku/kaidoku-r50, --receipt-fresh-base 646d29c9 or the
committed receipts' first-add commit read from git; expose both as flags). Every control
prints a one-line verdict + exit code and writes a JSON receipt per control. Deliver also
{W1}/ExecControls/EXPECTED.md: the expected verdict table the L1 freezes."""),
item("ExecTriV6", "executor",
f"""Port the triage instrument to v6. Read {LANE}/tools/round-50-c3/sqfs-triage-v5.py (port it)
and {LANE}/plans/round-52-claims.md (R52-C2). Produce the full draft
{W1}/ExecTriV6/sqfs-triage-v6.py changing exactly: the ddwrt route - for a FAILED-body
envelope of a family with no validated independent reader (frozen reader-census table cited
from the round-49 entry), the new table row label `legacy-body-unreadable` with action
`preserve-unresolved` (no cross-read); the evaluator implements the same precedence; the two
clean ddwrt no-pad _ddefault envelopes keep `clean`; every other v5 label unchanged (the
frozen 126-envelope corpus {LANE}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/
must score pair_mismatches 0 in BOTH the v5-baseline mode and v6 mode); a NEW frozen
executability audit counting FAILED-body envelopes whose prescribed action cross-reads a
family with no validated second reader (v5 table -> 1 violation naming dmg_Z3_v3ddwrt_inode_table;
v6 table -> 0); the census clause re-deriving registry-vs-active-census (port
{LANE}/tools/round-51/census3.py semantics; census_outside 0 both sides, census-guard-deleted
mutant -> red); freeze-drift gating exit 2 frozen_path_changed + selftest case; --selftest
offline, TMPDIR/--work honoring (scratch discipline), keeping v5's 18-case battery green and
adding: new-row-deleted mutant red, action-swapped mutant red, audit-guard-deleted mutant
red, do-nothing (v5 table at base -> audit red). If the port exceeds your budget, deliver the
complete hunk-level diff-spec instead of a broken file."""),
item("ExecRunsh", "executor",
f"""Port the C1 harness. Read {LANE}/tools/round-50/c1-run.sh (port it - it is bash; keep every
guard) and {LANE}/plans/round-52-claims.md (R52-C1). Produce the full draft
{W1}/ExecRunsh/c1-run.sh changing exactly: ROUND_SEGMENT kaidoku-r52; SCRATCH_PREFIX
/fast/scratch/hyaku/kaidoku-r52/; EVIDENCE_SEGMENT /corpus/evidence/round-52/; default OUTDIR
corpus/evidence/round-52/c1/<id>; claim label R52-C1 in run.json/oracle-run.json schemas
(schema names kaidoku-r52-c1-run-v1); everything else byte-faithful (pins: rea-agents@6.5.0,
unblob 26.6.4, sasquatch 4.5.1, unsquashfs 4.7.5; the FIXED_PATH; the data-run guard; the
provider_timeout retry loop; the superblock precondition; the three-producer oracle arm).
Validate your draft with `bash -n` and a --dry-run executed from a scratch copy (the dry-run
writes nothing; capture its output). Deliver also {W1}/ExecRunsh/deltas.md: the exact diff
lines vs the round-50 file."""),
item("ExecFetchVendor", "executor",
f"""Repair the fetcher's selftest (routed defect 4). Read {LANE}/tools/round-50/fetch-vendor.py -
the network guards are the https-scheme check, the ALLOWED_HOST = download.avm.de pin and the
redirect refusal; the round-50 disclosure says --selftest never exercises them. Produce the
full draft {W1}/ExecFetchVendor/fetch-vendor.py: byte-port to round-52 (paths/segments
kaidoku-r52; carrier table argument defaulting to tools/round-52/carriers.json; keep
tools/round-50/carriers.json loadable as --prior) with a --selftest that ALSO proves each
guard fails closed, offline (no network): for each guard, a fixture call where that guard
alone is deleted must produce the red (redirect-off-host refused, non-https refused,
wrong-host refused) - run the real deleted-guard fixture copies in your scratch and record
the observed refusals; guards present -> selftest green. The selftest must never fetch vendor
bytes. Also add a --plan mode that prints, per carrier, the URL, expected image sha256,
member path and member sha256 from the carrier table WITHOUT any network call. Deliver
{W1}/ExecFetchVendor/deltas.md with the exact guard lines."""),
item("ExecRuleFixtures", "executor",
f"""Build the round-52 gap rule + fixture set. Read {LANE}/plans/round-52-claims.md (R52-C1:
the law, the rule-shape clause, mutations M1-M4), {LANE}/tools/round-50/gap-rule.json (the
grammar), and the four {LANE}/tools/round-50/oracle/<id>.nonregular.tsv tables. Deliver under
{W1}/ExecRuleFixtures/: (1) gap-rule.json - the law-derived rule: claim R52-C1,
required.char-device=false, allowed[char-device]=allowed[block-device]=allowed[fifo]=
allowed[socket]=[] (empty lists), symlink/other families carried over unchanged from the
round-50 rule where the law says nothing about them, every cell legal in the v1 parser
grammar; (2) junk-rule.json - syntactically valid, every kind required with an impossible
allowance; (3) mutant rules M1/M3/M4 as JSON files (all-thirteen whitelist;
required-true+247:0-only; strict-subset whitelist); (4) fixture census files for M2
(a nonregular.tsv + minimal receipt-shaped fixture whose census carries a fourteenth unlisted
device, e.g. dev/ttyS0 4:64) with a README stating the expected verdict of each file under
the law rule and under each mutant; (5) a scratch script that validates every rule file
against the v1 grammar (parse with the v1 counter's gap_rule_model by importing it read-only
from a scratch clone) - receipts for all. No REA runs."""),
item("ExecMisrootSweep", "executor",
f"""Draft the lane-side misroot sweep helper (routed defect 5's lane half). The protocol clause:
for every untracked file one of your seats wrote into the FLEET repo, copy byte-exact into
the lane, cmp, delete the fleet copy (the one permitted fleet deletion), record under
## Mistakes. Produce {W1}/ExecMisrootSweep/misroot-sweep.sh: read-only by default -
git -C <fleet> status --porcelain (no pathspec), classifies untracked files by content (does
the file name kaidoku/round-52?), prints a classification report, --apply performs the
protocol's copy+cmp+delete for lane-classified strays ONLY after showing what it would do;
--selftest on fixture repos (a throwaway fleet-like fixture repo with a planted stray)
proves classify/copy/cmp and that a non-lane stray is never touched; never touches
.scratch/, .ufo/state/, or another lane's files. bash -n clean; run the selftest in your
scratch and receipt it."""),
item("ExecGrammar", "executor",
f"""Freeze the offline receipt-ingestion grammar for the v2 counter. Read the input-grammar docs
in {LANE}/tools/round-50/c1-counter.py (header + disposition_check) and one receipt per
carrier {LANE}/corpus/evidence/round-50/c1/<id>/run.json. Deliver
{W1}/ExecGrammar/grammar.md: the exact JSON paths the v2 controls mode reads per carrier
(published-file list, gap list, removal diagnostics, subject digest, handler list), verified
against all four committed receipts; then a standalone scratch script that computes the
three-family disposition clause per carrier under (a) the round-50 rule (expect c6430/c6490
pass, g7581/g7582 fail on the twelve char-devices) and (b) the claims' law (all four pass),
printing the per-carrier verdict table with counts. Receipt for the script run into your seat
dir. This is the CTL-OLD/CTL-NEW expectation witness - exactness matters more than speed."""),
item("ExecStatusHelper", "executor",
f"""Build the wave-accounting helper (routed defect 2). The r51 results handoff carried no
per-seat fields; this wave's seats write {W1}/<SeatName>/status.json. Produce
{W1}/ExecStatusHelper/wave-accounting.py: reads every seat dir under a wave root argument,
parses status.json (tolerating missing/malformed files - report them as unknown, never
crash), and prints JSON {{seats_total, settled, failed, blocked, unknown, by_role,
missing:[...], parse_errors:[...]}}; --check exits 0 only when every expected seat name
(passed as a second argument file or --expected) has a parseable settled|failed status.json.
--selftest on a fixture tree with: a settled seat, a failed seat, a malformed status.json, a
missing seat. Run the selftest in scratch and receipt it. The tool must honour TMPDIR and
accept a scratch --work argument."""),
item("ExecCensusCheck", "executor",
f"""Receipt the census no-regression state at the round-52 base. Run, from a scratch clone of
{LANE} at {BASE} (git clone --shared + checkout --detach; read-only otherwise):
python3 -I -B tools/round-51/census3.py --root . --rev <BASE> --check  (expect exit 0,
outside [], unregistered [], duplicates []) and --historical (expect exit 1, outside 13
against the frozen round-48 census2). Write both receipts (command, exit, stdout sha256,
UTC) into {W1}/ExecCensusCheck/. Then state in report.md: what the v6 instrument's census
clause must reproduce (census_outside 0 at base and at landing) and which census3.py
functions it ports. Do NOT modify anything in the clone beyond the checkout; delete the
clone after copying receipts."""),
item("ExecCarrierProbe", "executor",
f"""Receipt the vendor chain feasibility (no downloads beyond HEAD). For each of the four
carriers in {LANE}/tools/round-50/carriers.json (g7581, g7582, c6490, c6430): curl -sSI the
exact external.url (max-time 30), record HTTP status, content-length, etag, last-modified
(strip all other headers - never save Set-Cookie). Then read {LANE}/tools/round-50/fetch-vendor.py
and answer in report.md: (1) the exact procedure it uses to go from image URL to pinned
member bytes (extraction steps, tools, where the member sha256 is verified); (2) whether that
procedure needs any tool absent from this host (check command -v for each); (3) the disk
budget (4 x content-length + extraction overhead) vs disk-guard status. Receipts into
{W1}/ExecCarrierProbe/. No image bytes are downloaded this wave."""),
item("ExecV5Baseline", "executor",
f"""Receipt the v5 baseline the v6 port must preserve. In your scratch
(S=/fast/scratch/hyaku/kaidoku-r52/w1-ExecV5Baseline; export TMPDIR=$S), run
python3 -I -B {LANE}/tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/v5st (expect
18/18) and the v5 scoring mode over the frozen corpus
{LANE}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ with whatever table/CLI
mode v5 exposes for scoring (read its argparse first; the r50 receipts
{LANE}/.ufo/waves/round-50/c3/c3-after.json show the exact scoring invocation - reproduce
that shape). Record: pair_mismatches, evaluator_missing, and the routed label+action of
envelope dmg_Z3_v3ddwrt_inode_table (expect legacy-body-failure / cross-read-legacy).
Receipts + the envelope's row into {W1}/ExecV5Baseline/. Report anything that does not
reproduce."""),
item("ExecSelftestInv", "executor",
f"""Inventory the v1 counter selftest cases. Read {LANE}/tools/round-50/c1-counter.py's
selftest section (the probe/add fixture cases near the end of the file). Deliver
{W1}/ExecSelftestInv/cases.md: every selftest case as a table row (case id/name, what it
asserts, keep/port-as-is or adapt-for-r52 or drop, and why); then the NEW selftest cases the
round-52 claims demand that v1 lacks: frozen-path-drift exit 2 case, ENOENT-retry-exhausted
red case (deterministic fixture), law_shape_ok red case (all-thirteen whitelist), census
re-derivation fail case, prior-pin allow-list visible-in-receipt case, depth_gap_recorded
case, wrong-carrier-set case (receipts for only two carriers must not pass). For each new
case: the fixture it needs and the expected exit/finding. This manifest is what the L1
verifies the port's selftest against."""),
item("ExecPriors", "executor",
f"""Build the PRIOR_CARRIER_TABLES wiring data. Read {LANE}/tools/round-50/carriers.json (all
four carrier entries: id, sha256, external url/image_sha256/member/member_sha256, oracle +
nonregular table paths). Deliver {W1}/ExecPriors/priors.json: the exact constant block the
v2 counter embeds - the four prior_pins with their sha256 values, the re_scored_pins
allow-list (the same four), prior_pin_sources (paths into tools/round-50/carriers.json), and
the per-carrier prior oracle/nonregular table paths - with a README.md stating where each
value was read from (file + jq path). Validate every listed path exists at {BASE} (git
cat-file) and receipt the check."""),
item("ExecSbProbe", "executor",
f"""Build the superblock/layout probe the data run uses on fetched members. Read the
superblock summary code in {LANE}/tools/round-50/c1-run.sh (the embedded python) and
{LANE}/tools/round-41/sqfs-list.py --inspect semantics. Produce
{W1}/ExecSbProbe/sb-probe.py: reads a member file, prints JSON {{magic, byte_order, version,
compression_id, block_size, mkfs_time, bytes_used, avm_marker, bytes_used_le_file_size}} and
exits 0 only for hsqs/v4.0/compression 4/avm_marker true; --allow-nonavm waives with a
recorded waiver (control carriers only). Build a synthetic fixture in scratch: mksquashfs a
tiny directory tree (with one fifo via a privileged-free method if possible, else a plain
tree), run the probe on it, receipt the observed output; also receipt the probe REFUSING a
non-squashfs file. bash/python -I -B compatible; no network."""),
item("ExecOracleDry", "executor",
f"""Dry-run the oracle arm on a synthetic image. Build in your scratch a tiny squashfs image
with mksquashfs (a directory with 2 regular files + 1 symlink + 1 fifo if creatable
unprivileged - mknod fifo p works unprivileged; record if not), then exercise the THREE
oracle producers of {LANE}/tools/round-50/c1-run.sh's oracle arm against it: the pure-Python
reader (python3 -I -- {LANE}/tools/round-41/sqfs-list.py --layout auto --files ... --nonregular
... --inspect ...), /usr/bin/unsquashfs (-no-xattrs -f -no-exit-code + -lln listing), and
sasquatch (check its availability; sasquatch -le on a standard LE image). Verify the three
producers agree on the synthetic image (the reader's grammar: relpath TAB sha256 TAB size;
nonregular grammar dir|symlink|char-device|block-device|fifo|socket). Deliver receipts +
oracle-dry.md stating: which producers ran, any agreement mismatch, and what this predicts
for the real oracle arms. C1_ALLOW_NONAVM=1 semantics apply (synthetic image is not AVM) -
use the env var the harness supports or note its absence."""),
item("ExecWaveCheck", "executor",
f"""Build and run the dispatch interpolation check (M51-6 fix). Produce
{W1}/ExecWaveCheck/check-dispatch.py: reads a spec JSON (and optionally the rendered
dispatch JSON), asserts every item prompt and the context contain NO unresolved placeholder
markers - regex for \\{{[A-Z_0-9]+\\}} (2+ char uppercase-ish names) and for literal
'{LANE}'-style unused braces - and prints the offending item name + snippet; exit 0 clean,
exit 1 violations found; --selftest on fixture strings proving both directions. Then RUN it
against the actual wave spec at {LANE}/.ufo/waves/round-52/w1-spec.json and receipt the
output (expect exit 0; if it finds violations, report them - do not fix the spec yourself).
Receipt + the tool into your seat dir."""),
# ---------------- scribes (8) ----------------
item("ScribeEntryC1", "scribe",
f"""Draft the R52-C1 knowledge entry. Read {LANE}/plans/round-52-claims.md (R52-C1), the
round-50 miss entry {LANE}/corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md, the
round-51 NOT-promoted entry {LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md,
and the SCORECARD round-50/51 sections. Draft the FULL text of
corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md under {W1}/ScribeEntryC1/entry.md:
provenance trio first (source: citing S243/S244/S245/S249, S250, S251, and S252 - the
mknod(2) row opened this round - plus RECEIPT-PLACEHOLDER markers for the fresh round-52
receipts; verified-at: 2026-10-30; recheck: the counter command from the claims), then: the
two-round miss history (2/4 under the round-50 rule; r51 stopped pre-freeze), the law and
per-class census (Cable 1, FRITZ!Box 13), the branch ground (S250 lines, S252 CAP_MKNOD),
the pre-freeze controls, the fresh data-run placeholders (per-carrier receipt pointers), the
promotion statement CONDITIONAL on carriers_matched 4, and the honest width statement (fifo/
socket/block unexercised; reached-scope limit). Every number carries its command. NOTHING in
the draft asserts the data run already succeeded - conditional wording only."""),
item("ScribeProvince", "scribe",
f"""Draft the R52-C1 PROVINCE.md bindings. Read {LANE}/plans/round-52-claims.md,
{LANE}/PROVINCE.md (the Frontier LE-AVM bullets, the round-50 measured-not-promoted section,
the `## Round-39 additions to Core` section shape, and any round-51 notes), and the SCORECARD
round-50/51 rows. Draft under {W1}/ScribeProvince/: (1) the `## Round-52 additions to Core`
section text - LE SquashFS v4 members (`hsqs`) promoted with the law, the per-class census,
fresh-run receipt pointers (placeholders), and the honest scope (what stays Frontier: AVM
kernels, nested sub-images, >120s rootfs, fifo/socket/block kinds unexercised); (2) the exact
frontier-note line edits (which Frontier bullets lose the LE-members clause, dated
supersession, quote old lines and give replacements); (3) the fate of the round-50
`measured, not promoted` section and the round-51 NOT-promoted entry pointer (keep as
history, dated cross-references). Placeholders marked so the L1 cannot land a false
measurement."""),
item("ScribeReadme", "scribe",
f"""Draft the R52-C1 corpus/README.md bindings. Read {LANE}/corpus/README.md (coverage map rows
for the r50/r41/r51 squashfs entries, the frontier notes) and
{LANE}/plans/round-52-claims.md. Draft under {W1}/ScribeReadme/: the coverage-map row for
2026-10-30-r52-avm-le-squashfs-core.md (same shape as the r50 row, receipt placeholders), and
the dated frontier-note edit moving LE AVM members (`hsqs`) out of the frontier list (quote
old lines, give replacements). Keep the map's three-cell row shape (r50 falsify finding:
every map row is 3 cells). Also state the map-count arithmetic the SCORECARD head must
carry: 141 -> 142 with this entry, with the counting command (git ls-tree at REV |
corpus/knowledge stems vs mapped tokens - the claims' command A semantics)."""),
item("ScribeScorecard", "scribe",
f"""Draft the SCORECARD round-52 section skeleton. Read {LANE}/SCORECARD.md (the round-50
attempt-2 and round-51 sections at the file end, the Owned-axes heads, the planned rows) and
{LANE}/plans/round-52-claims.md. Draft under {W1}/ScribeScorecard/section.md: the
`## Round 52 (2026-10-30)` section skeleton - base {LANEBASE}, claims draft {BASE}, wave
shape placeholders, the claims table (R52-C1 coverage / R52-C2 depth) with the BEFORE column
filled from committed bytes (C1: carriers_matched 2 exit 1,
.ufo/waves/round-50/l1/scores/c1-after-attempt2.json; C2: executability violation 1 on
dmg_Z3_v3ddwrt_inode_table at the claims-draft base, receipt placeholder), AFTER/verdict/
command/measured-commit columns as placeholders, plus the coverage-head update line
(141 -> 142 once the entry lands) and the planned(next round) row placeholder. No verdict
may be pre-filled."""),
item("ScribeLesson", "scribe",
f"""Draft the round-52 lesson skeleton. Read {LANE}/corpus/lessons/round-51.md (structure:
title, freeze paragraph, ## Mistakes table, ## Gate, census before/after, honest-stop
sections) and the round-51 closure's routed defects in
{LANE}/corpus/lessons/round-51-verifier-spotcheck.md section 6. Draft under
{W1}/ScribeLesson/lesson.md: corpus/lessons/round-52.md with the freeze paragraph
placeholders, a ## Mistakes section SEEDED with rows for the inherited defects this round
commits to fix (M51-6 dispatch interpolation - class dispatch, captured-by none at r51, fix
= the check-dispatch.py assertion run before the ready file, receipt to be attached; per-seat
results fields - class observability, captured-by none, fix = status.json convention +
wave-accounting.py; round-band shortfall - class round-shape, captured-by the band rule,
fix = 64-seat v2 wave + falsify wave plan), each row's evidence pointer and fix marked
PLACEHOLDER until the round proves the fix ran; plus empty ## Gate and census sections. No
invented mistakes beyond the inherited ones."""),
item("ScribeSources", "scribe",
f"""Draft the round-52 SOURCES row S252. The L1 opens this URL independently; you open it too
(receipts with UTC, HTTP status, bytes, sha256): fetch
https://man7.org/linux/man-pages/man2/mknod.2.html into your scratch; locate the EPERM
privilege text - the sentence about lacking privileges such as CAP_MKNOD (mknod(2) documents
EPERM for device files without CAP_MKNOD; FIFO/socket creation is not that case). Deliver
{W1}/ScribeSources/rows.md: ONE row in the exact 11-column registry grammar (id S252, kind
docs, tier A for the scope `unprivileged device-node creation is CAP_MKNOD-gated on Linux`,
anchor = section title + access date, teaches = the CAP_MKNOD gate sentence paraphrase
(max 1 sentence), status mined at first registration, used-by = the round-52 entry stem) +
your Gate block fields (URL, access date, <=25-word located quote with its location) + the
fetch receipt. If the page moved or the quote cannot be located, say so - never invent."""),
item("ScribeBlock27", "scribe",
f"""Draft SKILL.md rule block 27 text. Read {LANE}/plans/round-52-claims.md (R52-C2), SKILL.md
rule block 26 (the `- **26. SquashFS ...` item inside `## Queue-drain craft`, around line
548), and the round-49 reader-census entry it cites. Draft under {W1}/ScribeBlock27/block27.md:
the full markdown text of the new `- **27. SquashFS extract_firmware outcome triage v6 - the
failed-body executability rule (round 52).` item: dated supersession of block 26's ddwrt rows
(block 26 stays as history); the new `legacy-body-unreadable` row whose action is
`preserve-unresolved` (no cross-read) for FAILED bodies of families with no validated
independent reader; the reader-census table citation; the F5 scoping correction of block 26's
*"`symlink` and `special` both count"* phrasing (device-node kinds carry no disposition under
the extraction law - state it as the law's scope, cite the entry); file:line pointers
resolvable at the landing (use placeholders LANE-RELATIVE like corpus/knowledge/<stem>.md:N-M
and mark N-M PLACEHOLDER where the line numbers depend on the landing). Keep block 26's
numbering convention and table style."""),
item("ScribeMergeAdopt", "scribe",
f"""Prepare the assimilation adoption (ONE theme, 1-3 entries) - draft only, nothing appends.
Read /home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md (77 staged entries; the
table maps target paths), /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md, and
the staged knowledge bytes under /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/.
Pick the ONE entry whose subject best serves THIS round's ground (SquashFS extraction/variants,
AVM firmware, device nodes, padding, unsquashfs/sasquatch/unblob behavior) and that is NOT
already-held ground (check {LANE}/corpus/README.md coverage map; a restating entry is a
reject). For your candidate: (1) full staged text + its SOURCES.append.md row id; (2) the
re-grounding plan - which cited source YOU (and the L1) must re-open, the Gate fields
needed; (3) the id-collision analysis: the staged row id vs the lane registry
({LANE}/corpus/SOURCES.md holds 158 rows S001-S251; run the collision grep from the
campaign addendum: grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' on both files) - the staged
id WILL likely collide (package starts S106); propose the renumbered id continuing the lane's
S-space BY DOCUMENT (cite the target URL/anchor, never arithmetic), with old->new; (4) the
scratch transformation: the normalized 11-column row (ISO recheck, no pipe chars in any cell,
used-by = the adopted entry path, status mined). Deliver {W1}/ScribeMergeAdopt/plan.md + the
normalized row + the transformed entry text (with its source: re-pointed to the renumbered
row). Also list the NEXT-best candidate as the reject with reason (the Gate needs >=1
reject)."""),
# ---------------- scouts (7) ----------------
item("ScoutMknod", "scout",
f"""Open the mknod(2) man page (R52-C1's kernel-side law ground; the L1 opens it independently -
your fetch is the second reader). Fetch https://man7.org/linux/man-pages/man2/mknod.2.html
into your scratch (record UTC, HTTP status, bytes, sha256); locate: (1) the EPERM sentence
about device files and CAP_MKNOD (quote <=25 words with section location); (2) whether FIFO
(mkfifo/mknod S_IFIFO) and UNIX-domain socket creation need privileges per this page (quote
the relevant ERRORS text); (3) also fetch
https://man7.org/linux/man-pages/man7/capabilities.7.html and locate the CAP_MKNOD
definition line (quote <=25 words). Deliver under {W1}/ScoutMknod/: receipts, located quotes,
and SOURCES-row fields for a capabilities(7) row (candidate S253) IF it adds ground beyond
mknod(2) alone - say whether it does. No edits outside your seat dir."""),
item("ScoutMergeThemes", "scout",
f"""Independently scan the assimilation package for THIS round's theme (second reader; do NOT
read ScribeMergeAdopt's outputs). Read /home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md
(77 staged entries) and list the entries whose subject touches this round's ground: SquashFS
extraction/variants, AVM firmware, device nodes, padding, unsquashfs/sasquatch/unblob
behavior, firmware formats. For each candidate (at most 3): its target path, its round, its
source: citation and the corresponding row id in
/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md, a one-line what-it-claims, and
your adopt/reject lean with reason (lane bar: {LANE}/corpus/QUALITY.md; already-held ground
{LANE}/corpus/README.md - an entry restating held ground is a reject). Do NOT fetch the cited
URLs (adoption re-opens them in-round; fetching is the adoption step's job, not the scan's).
Deliver {W1}/ScoutMergeThemes/scan.md. Report at {W1}/ScoutMergeThemes.md."""),
item("ScoutCarrierChain", "scout",
f"""Verify the re-fetch chain semantics for the data run (read-only + HEAD only). Read
{LANE}/tools/round-50/fetch-vendor.py end-to-end and {LANE}/tools/round-50/carriers.json.
Answer with receipts: (1) the exact chain per carrier: image URL -> download -> image sha256
verify -> member extraction (which tool? unsquashfs? 7z? the script's own code) -> member
sha256 verify -> cache file naming (sha256.bin?); (2) does the member extraction need
privileged mknod (the FRITZ!Box images contain /dev entries - does extracting the OUTER
container hit device nodes? which flags avoid it); (3) what happens on sha mismatch at each
stage (exit code, message); (4) the disk and time budget for all four carriers (HEAD
content-lengths: g7581 32010240 - fetch the other three HEADs yourself); (5) does the script
write anything outside its --cache-dir. Deliver {W1}/ScoutCarrierChain/chain.md + receipts.
No image bytes downloaded."""),
item("ScoutCensusRecheck", "scout",
f"""Independently re-check the census no-regression state (second reader; do NOT read
ExecCensusCheck's outputs). From a scratch clone of {LANE} at {BASE}: (1) run
python3 -I -B tools/round-51/census3.py --root . --rev {BASE} --check (expect exit 0) and
--historical (expect exit 1, outside 13); (2) verify census2.json (tools/round-48/census2.json)
is byte-identical to its state at the round-48 landing (git log -1 --format=%H --
tools/round-48/census2.json; the file must not have changed since - a changed frozen census
is a defect, report it); (3) name the frozen calibration surfaces that consume census2.json
(grep tools/round-50/c2-record.py and tools/round-50/selftest-r49-c2.py) and confirm landing
census3.json broke none of them (they read census2, which is untouched). Receipts into
{W1}/ScoutCensusRecheck/. Delete the clone after."""),
item("ScoutDraftsInventory", "scout",
f"""Inventory the round-51 drafts the round-52 ports build on. Walk
{LANE}/.ufo/waves/round-51/w1/ and {LANE}/.ufo/waves/round-51/l1/ (read-only): list every
draft file (path, bytes, sha256, first line), and for the big ones (ExecCounterV2/c1-counter.py
draft if present, ExecTriV6/sqfs-triage-v6.py draft, ExecControls, ExecRunsh, ExecFetchSelftest,
ExecRuleFixtures, ExecOfflineGrammar) state: is it complete enough to port from (syntactically
valid? python3 -m py_compile or bash -n in your scratch), what it already implements vs the
r52 claims (r52 paths/constants differ - list the sed-able deltas), or is it evidence-only
(the r51 disposition says the counter/harness/v6 drafts never landed). Deliver
{W1}/ScoutDraftsInventory/inventory.md with a draft->r52-target map and a port-from verdict
per draft (use-draft vs port-from-r50-source). The L1 ports from the best source, never from
memory."""),
item("ScoutV6Corpus", "scout",
f"""Manifest the frozen triage corpus and the moving pair. For
{LANE}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ (126 files): build a
sha256 manifest (sorted, sha256sum output) into {W1}/ScoutV6Corpus/manifest.txt; then from
the v5 scoring receipts {LANE}/.ufo/waves/round-50/c3/c3-after.json and the envelope bytes
themselves, identify the ddwrt family envelopes: which are FAILED-body, which are the two
clean no-pad _ddefault ones, and confirm the v6 change moves EXACTLY the pair
(dmg_Z3_v3ddwrt_inode_table = the only FAILED no-pad ddwrt body) - list every ddwrt envelope
with its handler/failed/pad fields as evidence. If the count is not exactly 1 moving FAILED
pair + 2 clean, the claims' C2 before/after arithmetic is wrong - say so loudly with
evidence."""),
item("ScoutQualRows", "scout",
f"""Map which routed defects already have QUALITY criteria. Read {LANE}/corpus/QUALITY.md in
full (the numbered criteria), {LANE}/corpus/lessons/round-51.md ## Mistakes, and
{LANE}/corpus/lessons/round-51-verifier-spotcheck.md sections 6-7. Deliver
{W1}/ScoutQualRows/map.md: for each round-51 routed defect (round shape, per-seat results
fields, interpolation, misroot prevention, census W04 duplicates, carried L0) - does a
QUALITY criterion already cover the class (row number) or is this round's fix
uncriterion'd (then the lesson row must cite the fix's observed failure before any new
criterion); plus the current QUALITY row count (last row number) so the round knows where
new rows would start. Read-only."""),
# ---------------- reviewers (8) ----------------
item("RevCounterPort", "reviewer",
f"""Build the port-fidelity checklist for the C1 counter. Diff-read
{LANE}/tools/round-50/c1-counter.py against the R52-C1 section of
{LANE}/plans/round-52-claims.md and deliver a checklist of every v1 behavior the v2 port MUST
preserve (receipt digest binding, subject-digest equality, projection rerun, first-add-after-
freeze clause, exit-code map, binding list with their exact doc markers, selftest case
inventory) and the exact list of what MUST change (paths, constants, gating, the offline
controls mode, the four new clauses law_shape_ok/census_rederived_ok/depth_gap_recorded/
re_scored_pins, the retry policy, rule grammar {{R50-C1,R52-C1}}). For each: the file:line in
v1 and the demanded v2 behavior. This checklist is what the L1 verifies the port against -
completeness is the deliverable, not opinions. Deliver {W1}/RevCounterPort/checklist.md."""),
item("RevTriPort", "reviewer",
f"""Build the port-fidelity checklist for the triage v6. Diff-read
{LANE}/tools/round-50-c3/sqfs-triage-v5.py against the R52-C2 section of
{LANE}/plans/round-52-claims.md and deliver the MUST-preserve checklist (H1 duplicate-glob
refusal, the receipt gate re-reading what it wrote, instrument_sha256 binding, the
counting-bullet guard, selftest inventory, the 126-envelope scoring semantics, exit-code map)
+ the exact MUST-change list (the ddwrt row, the evaluator precedence, the executability
audit, the census clause ported from tools/round-51/census3.py, drift gating, new registry
row). file:line for each. Deliver {W1}/RevTriPort/checklist.md."""),
item("RevRunshPort", "reviewer",
f"""Build the port-fidelity checklist for the c1-run.sh harness. Diff-read
{LANE}/tools/round-50/c1-run.sh against the R52-C1 section of
{LANE}/plans/round-52-claims.md: the MUST-preserve list (pins rea-agents@6.5.0/unblob
26.6.4/sasquatch 4.5.1/unsquashfs 4.7.5; FIXED_PATH and C1_CHILD_PATH override; data-run
guard; occupied-slot guard; scratch-segment + prefix guards; provider_timeout retry loop;
superblock precondition; the three-producer oracle arm with its grammar validation; receipt
fields) + the MUST-change list (segments kaidoku-r52, prefix, evidence round-52, schema
kaidoku-r52-c1-run-v1, claim R52-C1). file:line each. Also name anything in the harness the
claims forgot to mention (e.g. C1_KEEP_ENVELOPE, C1_ALLOW_NONAVM, C1_REA_ATTEMPTS). Deliver
{W1}/RevRunshPort/checklist.md."""),
item("RevFetchGuards", "reviewer",
f"""Review the fetcher guard-repair design. Read {LANE}/tools/round-50/fetch-vendor.py in full:
enumerate EVERY network surface (urllib usage, redirect handling, URL construction) and
verify the claims' guard list (https-scheme, ALLOWED_HOST pin, redirect refusal) is complete
- name any surface the selftest plan misses (e.g. file:// scheme, header injection,
--cache-dir traversal). Then review the ExecFetchVendor draft when it lands under
{W1}/ExecFetchVendor/ (if absent, review the plan in the wave context): does --selftest stay
offline, is each deleted-guard fixture a REAL deletion (byte-level, not a mock), does the
red-before show the honest refusal? Deliver numbered findings under
{W1}/RevFetchGuards/findings.md."""),
item("RevDocsDrafts", "reviewer",
f"""Attack the docs-binding drafts for overstatement (the r50 falsify class). Read the scribe
drafts under {W1}/ScribeEntryC1/, {W1}/ScribeProvince/, {W1}/ScribeReadme/,
{W1}/ScribeScorecard/, {W1}/ScribeBlock27/ (they land in parallel - if a draft is absent,
review the claims file's landing-bindings bullet instead and say which you did) and
{LANE}/plans/round-52-claims.md. Attack: any sentence asserting a measurement before the
receipts exist (must be placeholder-marked); stem/heading constant mismatches against the
claims (2026-10-30-r52-avm-le-squashfs-core, `## Round-52 additions to Core`, `Round-52
frontier note`); source-row citations that do not exist yet presented as existing (S252 is
being opened THIS round - drafts may cite it only as opened-this-round); coverage-head
arithmetic (141 -> 142; show the count command). Deliver numbered findings under
{W1}/RevDocsDrafts/findings.md."""),
item("RevV6Draft", "reviewer",
f"""Review the round-51 v6 draft for salvage. Read
{LANE}/.ufo/waves/round-51/w1/ExecTriV6/ (the invalid draft + its receipts - the r51
disposition says it was syntactically invalid and never integrated). In your scratch:
py_compile it; if it compiles, diff its structure against
{LANE}/tools/round-50-c3/sqfs-triage-v5.py (what does it already change? does its ddwrt row
match the r52 claims' design?); if it does not compile, identify the exact broken region(s)
and whether the surrounding logic is worth porting. Deliver {W1}/RevV6Draft/verdict.md:
salvage yes/no with the exact lines worth taking, the lines to drop, and why - the L1 uses
this to decide port-from-draft vs port-from-v5. Evidence over opinion."""),
item("RevClaimsFrozen", "reviewer",
f"""Verify the claims file's constants against committed bytes (freeze-readiness). Read
{LANE}/plans/round-52-claims.md and check at {BASE} (git show): (1) the entry stem
2026-10-30-r52-avm-le-squashfs-core does NOT exist yet (no collision with the r51 entry
2026-10-30-r51-avm-le-squashfs-core.md); (2) PROVINCE.md has no `## Round-52 additions to
Core` heading yet; (3) the coverage map head is 141 (count mapped tokens vs
corpus/knowledge files with the SCORECARD command A semantics at {BASE}); (4) rule block
count is 26 at {BASE} (the craft section); (5) the four round-50 carrier receipt dirs exist
(corpus/evidence/round-50/c1/<id>/after.json) and the oracle tables
tools/round-50/oracle/*.tsv exist; (6) census3.py + census3.json exist; (7) SOURCES.md holds
S250/S251 and no S252 yet. Deliver {W1}/RevClaimsFrozen/checklist.md with each check's
command + observed value + pass/fail."""),
item("RevGrammarOffline", "reviewer",
f"""Second-reader the offline disposition grammar (do NOT read ExecGrammar's or LB2OfflineClause's
outputs first - derive independently, then compare). From
{LANE}/tools/round-50/c1-counter.py's disposition_check + the four committed
{LANE}/corpus/evidence/round-50/c1/<id>/run.json receipts, independently compute the
three-family disposition verdict per carrier under (a) the round-50 rule and (b) the r52 law
(required.char-device=false, allowed device kinds empty). Deliver
{W1}/RevGrammarOffline/verdict.md: your per-carrier table (expected: r50 rule -> c6430 pass,
c6490 pass, g7581 fail, g7582 fail; law -> all pass), the JSON paths you read, and ANY
disagreement with the claims' stated expectations with evidence. This is the CTL-OLD/CTL-NEW
expectation cross-check."""),
# ---------------- critics (7) ----------------
item("CritRuleDerive", "critic",
f"""Attack the R52-C1 law encoding AS AMENDED (the r51 wave-1 amendments F1-F11 are baked into
{LANE}/plans/round-52-claims.md - read them first; your job is to verify the ANSWERS hold
and hunt NEW holes, not re-litigate answered ones). Read the plans file, the round-50 rule
{LANE}/tools/round-50/gap-rule.json, the disposition-check docs in the v1 counter, the four
nonregular tables. Attack: (1) does allowed[device-kind]=[] + required=false + law_shape_ok
actually fail closed on a future extractor emitting device gaps, or is there an escape
(e.g. a gap kind rename, a gap on a path that maps to no oracle row)? (2) M2's fourteenth-
device fixture - does the law rule actually score it GREEN while a whitelist scores RED, or
does required=false make M2 vacuous (both score green)? If vacuous, M2 tests nothing - say
so and propose the fix; (3) is CTL-NEW (4/4 over round-50 envelopes) a real derivation
consistency check or does it pass for any rule that ignores device rows entirely (then it
cannot distinguish the law from a no-device-check rule - name what does)? Numbered findings
+ severity under {W1}/CritRuleDerive/findings.md."""),
item("CritCounterV2", "critic",
f"""Attack the R52-C1 v2 counter design. Read {LANE}/plans/round-52-claims.md (R52-C1),
{LANE}/tools/round-50/c1-counter.py (what v1 enforces), and the SCORECARD round-50 rows.
Attack: the frozen-walk choice (should tools/round-41/sqfs-list.py and the oracle producers
be in the walk?); the offline controls mode (can rule-override or a stale rule-bytes pin go
unnoticed? demand the receipt name the rule file's sha256); the drift gate (could a drift
exit 2 be misread as a pass by the accounting?); the bindings list (compare v1's binding set
against the r52 landing bindings - name anything dropped); the retry policy (below). Numbered
findings + severity under {W1}/CritCounterV2/findings.md."""),
item("CritRetry", "critic",
f"""Attack the projection retry policy (r52 claims R52-C1; r51 F6 as amended by the r51
disposition: no retry policy is admitted without proof able to fail). Read the claims'
retry bullet, {LANE}/.ufo/waves/round-50/l1/scores/c1-after-attempt2.json (the g7581 ENOENT
failure fields - quote them), and the v1 counter's projection rerun code. Attack: (1) the
deterministic-ENOENT control - can a FIXTURE even be deterministic when the real failure is a
race (the fixture proves the policy can exhaust, not that it exhausts on the real cause)?
Is that distinction stated in the claims honestly enough? (2) can the retry mask a REAL
defect (an extractor that deterministically fails path X on run 1 and run 2 but passes run 3
by scheduling luck)? (3) is the 2-attempt ENOENT budget justified by any evidence, or
arbitrary? (4) does the receipt make attempts auditable (per-attempt diagnostics recorded)?
(5) the honest-stop wording: if g7581 fails after all attempts, the claim misses - confirm
the claims file says that and nothing amends it post-hoc. Numbered findings + severity +
the exact control design you would demand, under {W1}/CritRetry/findings.md."""),
item("CritTriV6", "critic",
f"""Attack the R52-C2 v6 design. Read {LANE}/plans/round-52-claims.md (R52-C2),
{LANE}/tools/round-50-c3/sqfs-triage-v5.py (the docstring's ddwrt boundary discussion, the
H1/H2 guards), and the round-50 C3 receipts {LANE}/.ufo/waves/round-50/c3/c3-after.json.
Attack: (1) the new row - is `legacy-body-unreadable`/`preserve-unresolved` the right
label/action, and does the evaluator change stay within "every v5 label unchanged except the
one ddwrt FAILED-body pair" (name the exact envelope set that moves and verify from the
receipts it is exactly 1)? (2) the executability audit - can it red-before for a reason
OTHER than the ddwrt body (audit false positives on the 126 corpus)? (3) census_outside
inside the triage instrument - scope creep or coherent (the claims say no-regression
binding; is embedding it in v6 better than leaving it to census3.py runs)? (4) the r51
disposition's warning - clean DD-WRT extraction is not independent-reader success; does v6
keep `clean` on the two nopad _ddefault envelopes on VALID grounds (which receipt proves
their readers succeeded - quote it), or should they also be `legacy-body-unreadable`?
Numbered findings + severity under {W1}/CritTriV6/findings.md."""),
item("CritClaims", "critic",
f"""Attack the round-52 claims file itself. Read {LANE}/plans/round-52-claims.md in full and
apply the fleet claim-sizing rules (declare concrete re-derivable values; no universal
clauses without enumerating; a do-nothing control cannot reach the target; one predicate
sentence across plan/counter/receipt; never narrow after landing; a coverage claim names its
surface and the command that would show it unmoved; calibration claims count mismatches).
Attack: (1) sizing - is `carriers_matched 4` + bindings one command re-derivable over
committed bytes at closure (the closure does not run REA - name exactly which receipt fields
it reads)? (2) the C1 do-nothing control (CTL-OLD) - is it truly the cheapest control that
skips the claimed work, committed BEFORE data? (3) the C2 before-arm - it runs at the
claims-draft commit over the v5 table bytes: is that receipt generatable TODAY (pre-wave) or
does it depend on the v6 instrument existing (circularity - the audit that measures the
before-state is shipped by the claim itself; is that honest and is the witness independent)?
(4) causal separability + distinct axes; (5) anything that violates the sizing rules.
Numbered findings + severity under {W1}/CritClaims/findings.md."""),
item("CritFetchChain", "critic",
f"""Attack the carrier re-fetch chain design. Read {LANE}/tools/round-50/fetch-vendor.py,
{LANE}/tools/round-50/carriers.json (the four entries with image sha256 + member path +
member sha256), and {LANE}/plans/round-52-claims.md (the data-run bullet). Attack: (1) pin
verification stages - the image sha is verified against carriers.json's image_sha256: is
that recorded for all four, and what happens if AVM re-publishes a changed image (last-modified
drift - does the chain fail closed on image-sha mismatch BEFORE member extraction)?
(2) TOCTOU/interrupted downloads (partial file hashed?); (3) the member extraction - which
tool, and does extracting the outer container hit device nodes/fifo rows (privilege)? What
flags avoid it? (4) cache naming and reuse - could a stale wrong-bytes cache file satisfy
the pin? (5) the kill rule if a fetched member's sha mismatches (stop, not skip). Numbered
findings + severity under {W1}/CritFetchChain/findings.md."""),
item("CritBand", "critic",
f"""Attack the round-52 round shape. Read {LANE}/plans/round-52-claims.md (## Round shape +
routed-defect repairs 1-3), this wave's spec at {LANE}/.ufo/waves/round-52/w1-spec.json, and
the r51 spotcheck section 6 items 1-3. Attack: (1) wave accounting - 64 seats now + a falsify
wave (32-64) after the landing: does the round stay <=128 in every outcome, and is the
>=25% attack share met round-wide (compute it from the spec roles; state the definition you
use)? (2) per-seat status.json - what if a seat dies mid-write or never starts (partial
JSON, missing file): does wave-accounting.py's unknown-classification keep dead seats
VISIBLE (the r51 lesson: dead seats stay dead in the evidence)? (3) the interpolation check
- blind spots (lowercase placeholders, nested braces, context-only markers)? (4) what
happens if the falsify wave finds <32 items - the residual <=8 call: is that consistent
with the band rules? Numbered findings + severity under {W1}/CritBand/findings.md."""),
# ---------------- mutation-testers (4) ----------------
item("MutGapRule", "mutation-tester",
f"""Freeze the gap-rule mutation battery (table math, no counter needed). Read
{LANE}/tools/round-50/gap-rule.json, the disposition-check docs in
{LANE}/tools/round-50/c1-counter.py, the four {LANE}/tools/round-50/oracle/<id>.nonregular.tsv
tables, and the disposition data in {LANE}/corpus/evidence/round-50/c1/<id>/run.json. For
each mutation: M1 require-char-device (=true, silent 247:0 only), M2 whitelist all thirteen
details, M3 whitelist a strict subset (e.g. add only 136:0-136:7), M4 drop symlink removal
diagnostic, M5 require symlinks with only the gap allowed, M6 the r52 law encoding
(required char-device=false, allowed device kinds empty) - compute the three-family clause
verdict per carrier per mutation FROM THE DATA (a scratch script doing the clause math) and
record the full expected-verdict matrix (which mutants must be red at which carriers,
which green). Cross-check M2/M6 against the claims' law_shape_ok semantics: M2 must be red
BY law_shape_ok (not by disposition). Receipt the script + matrix into
{W1}/MutGapRule/."""),
item("MutTriV6", "mutation-tester",
f"""Design the v6 mutation battery. Read {LANE}/tools/round-50-c3/sqfs-triage-v5.py (its
committed mutation battery + selftest), {LANE}/plans/round-52-claims.md (R52-C2), and the
round-50 controls receipts {LANE}/.ufo/waves/round-50/c3/ctl-*.json. Design the v6
mutations: the audit-guard deleted, the new `legacy-body-unreadable` row deleted, its action
swapped back to `cross-read-legacy`, the ddwrt glob broadened back into
`legacy-body-failure`, the census guard deleted, plus the v5 carryovers (do-nothing, junk
table, guard-row-deleted, action-swapped). For each: what it must flip (a pair, an audit
finding, the census count), how the selftest witnesses it, and the no-op risk (a mutation
nothing observes = the guard around it is dead). Verify from the round-50 receipts which v5
mutations were actually observed red (the battery's committed evidence) and carry those
forward. Deliver the battery spec under {W1}/MutTriV6/battery.md."""),
item("MutControlsV2", "mutation-tester",
f"""Attack the round-52 control designs for dead controls. Read
{LANE}/plans/round-52-claims.md (the controls bullets in both claims) and
{LANE}/.ufo/waves/round-50/controls-attempt2.json (what the r50 controls caught). For each
r52 control (CTL-OLD, CTL-NEW, CTL-DN, CTL-JUNK, the rule mutations M1-M4; C2's do-nothing,
junk table, audit-guard-deleted, row-swapped, census-guard-deleted): state what claimed work
it skips, what exactly it observes, and how it could pass while the claim is false (the
dead-control test). Name any control redundant with another and any MISSING control (e.g.
wrong-carrier-set control: the counter scoring receipts of only two carriers must not pass;
a receipts-from-the-wrong-round control). Deliver the table under
{W1}/MutControlsV2/findings.md."""),
item("MutC1Bindings", "mutation-tester",
f"""Design the binding-mutation battery for the v2 counter's documentation bindings. Read
{LANE}/tools/round-50/c1-counter.py's binding checks (the docs bindings: entry existence +
stem, PROVINCE heading + row, README map row, SOURCES used-by, scorecard head constants) and
{LANE}/plans/round-52-claims.md (the landing-bindings bullet). For each binding: the fixture
mutation that must flip it (entry renamed, heading typo'd, map row removed, used-by dropped,
wrong stem) and the expected finding id; plus the no-op risk check (a binding whose fixture
mutation changes nothing = dead check). Also design the receipts-side mutations (a receipt
whose subject digest != carrier pin; a receipt naming the wrong handler; a stale
receipt-fresh-base). Deliver the battery spec under {W1}/MutC1Bindings/battery.md."""),
# ---------------- labrats (4) ----------------
item("LB1V5Audit", "executor",
f"""Falsifiable probe: is the C2 before-arm deterministic at exactly 1 violation? Hypothesis:
running the v5 table bytes through a minimal executability-audit prototype (scratch script,
NOT the v6 instrument) over the 126-envelope corpus
{LANE}/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ reports exactly ONE
violation, envelope dmg_Z3_v3ddwrt_inode_table (v5 routes it cross-read-legacy while its
family has no validated second reader). Read the v5 table + evaluator for the label/action
extraction, the round-49 reader-census entry for the no-reader family list, then implement
the minimal audit in scratch and run it TWICE (same inputs) - receipts must show identical
output. Falsified if: 0, 2+, or nondeterministic violations (name them). Report at
{W1}/LB1V5Audit.md + receipts under {W1}/LB1V5Audit/."""),
item("LB2OfflineClause", "executor",
f"""Falsifiable probe: does the committed-data disposition math match the claims'
expectations? Hypothesis: a standalone scratch implementation of the three-family
disposition clause (ported read-only semantics from
{LANE}/tools/round-50/c1-counter.py) scored over the four committed
{LANE}/corpus/evidence/round-50/c1/<id>/after.json envelopes + oracle tables yields 2/4
under the round-50 rule (c6430, c6490 pass; g7581, g7582 fail on twelve char-devices each)
and 4/4 under the r52 law. Independent implementation - do NOT read ExecGrammar's or
RevGrammarOffline's outputs. Run it, receipt the per-carrier verdict table. Falsified if
any cell differs from the expectation (then CTL-OLD/CTL-NEW expectations are wrong - a
stop-the-round finding). Report at {W1}/LB2OfflineClause.md + receipts."""),
item("LB3CensusIdem", "executor",
f"""Falsifiable probe: is the census no-regression clause able to fail? Hypothesis:
tools/round-51/census3.py --check exits 0 at {BASE} AND exits nonzero on a tampered census
fixture. In your scratch: (1) run --check at {BASE} from a --shared clone (receipt);
(2) build a tampered fixture: copy census3.json, delete one listed path (or add one foreign
path), point a --file-style invocation (read the tool's argparse for the offline mode) at
the tampered copy, expect exit != 0 with the diff named; (3) run twice for determinism.
Falsified if the tampered census still exits 0 (the clause cannot fail = dead guard - a
stop-the-round finding for the v6 census clause design). Report at {W1}/LB3CensusIdem.md +
receipts."""),
item("LB4Mknod", "executor",
f"""Falsifiable probe: does this host's kernel ground the branch asymmetry live? Hypothesis:
as an unprivileged user in your scratch, mkfifo succeeds (fifo creation needs no privilege),
mknod of a char device fails EPERM (device creation is CAP_MKNOD-gated), and a bind() socket
in the filesystem succeeds - the exact asymmetry the device-accounting law rests on
(S250's branch structure + S252's EPERM text). Run the three probes in your scratch
(mkfifo p; python3 -c os.mknod char 0:0 expecting PermissionError; python3 socket bind a
sun_path under $S), receipt command+exit+stderr for each, twice (determinism). Clean up the
nodes. Falsified if any probe contradicts the asymmetry (then S252's scope needs a caveat -
report it). No host writes outside $S. Report at {W1}/LB4Mknod.md + receipts."""),
# ---------------- sentinels (3) ----------------
item("SentCreds", "sentinel",
f"""Credential and vendor-bytes scan. Scan: (1) {LANE}/plans/round-52-claims.md and
{LANE}/.ufo/waves/round-52/ (everything written so far) for session cookies, tokens,
Set-Cookie, op:// refs, private keys - report findings with file:line; (2) verify no vendor
firmware bytes live in the lane tree at {BASE}: the largest new files under
{LANE}/corpus/evidence/round-50/c1/ are receipts (JSON), not images - list any file over
1 MiB and identify it; (3) check the round-52 claims and this wave spec for accidental
secrets (URLs with credentials, tokens). Deliver the scan receipt under
{W1}/SentCreds/scan.md."""),
item("SentSecrets", "sentinel",
f"""Scan the inheritance surface before the ports land. (1) Walk
{LANE}/.ufo/waves/round-51/w1/ and l1/drafts/ : any file carrying credential material
(cookies, tokens, op://, private keys) that a port could copy into tools/round-52/? List
file:line; (2) the merge package entries slated for adoption candidates
(/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/ - read-only): do the squashfs/AVM-
adjacent staged entries contain credential material or op:// refs (CORPUS rule: none may
enter the corpus)? (3) the four vendor URLs in carriers.json - confirm none embed
credentials. Deliver {W1}/SentSecrets/scan.md. Read-only."""),
item("SentWaves", "sentinel",
f"""Audit this wave's own spec for write-scope violations. Read
{LANE}/.ufo/waves/round-52/w1-spec.json: for EVERY item, does its prompt instruct writes
ONLY into {W1}/<SeatName>/ and the seat's scratch? Flag any item whose text could be read
to permit lane-tree edits, fleet-repo writes, .scratch/ or .ufo/state/ touches, sibling-lane
writes, REA execution, --data-run, corpus/evidence writes, or git mutations (commit/push/
stash). Also flag any prompt that names a URL not justified by its task, and any
credential-shaped string in the spec. Deliver {W1}/SentWaves/audit.md with item-by-item
verdicts (clean / finding). Read-only."""),
# ---------------- revengers (2) ----------------
item("RevExtractor", "revenger",
f"""Reverse the extractor's disposition path (read-only source analysis). In
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents (READ-ONLY - do not execute
anything there): find the extract-firmware verb implementation, follow it to where it runs
unblob/sasquatch and where it builds the result envelope's published-file list,
unpublished_entries (gaps) and removal diagnostics. Answer with file:line evidence:
(1) where is unpublished_entries computed and from what comparison (staged inventory vs disk
walk)? (2) why does a char-device oracle entry produce NEITHER a gap NOR a removal - is the
comparison inventory scoped to entries the handler STAGED (and the squashfs handler stages
no device nodes), or does the disk walk simply not stat them? (3) where does the
depth-limited gap come from and does the envelope carry input_path/continuation_id for it
(the r52 depth_gap_recorded clause needs them)? (4) where does the readlink ENOENT class
come from (symlink projection walking a deleted entry?) - which code path, and is the race
plausible (name the window)? Deliver {W1}/RevExtractor/analysis.md with file:line for every
claim."""),
item("RevCounterEscape", "revenger",
f"""Attempt to defeat the v2 counter design BEFORE it is built (read-only attack on the
design + the v1 code). Read {LANE}/tools/round-50/c1-counter.py and
{LANE}/plans/round-52-claims.md. Construct concrete escapes: (1) caller-supplied inputs -
can a forged receipts dir + rule file score PASS on the planned controls mode (rule
override, receipt digest not bound to git, freeze pin stale)? (2) the projection rerun -
can a receipt-shaped file planted in the receipts dir satisfy projection_ok without any REA
run (what does v1 actually re-run vs read)? (3) the prior-pins allow-list - can a
non-allow-listed stale pin slip through (name the exact check)? (4) the bindings - can a
binding pass with a placeholder file (empty entry with the right stem)? For each escape:
whether v1 blocks it (file:line) and what the v2 MUST add. Deliver
{W1}/RevCounterEscape/escapes.md."""),
# ---------------- connectors (3) ----------------
item("ConnSiblings", "connector",
f"""Sibling-overlap scan for round 52. Read {LANE}/PROVINCE.md (Adjacent + Frontier) and scan
the sibling provinces' boundary declarations: /home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md,
/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md,
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md (read-only). Question: does the
round's ground - a squashfs extraction device-accounting law, a ddwrt pad/failed-body route
fix, a carrier re-fetch chain - bleed into any sibling's owned surface? Also: does the
assimilation package (/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/) hold entries
whose subject a sibling owns (report, never absorb)? Also scan the sibling lanes' recent
lessons dirs for squashfs/AVM work this week (corpus/lessons/round-5*.md titles only) that
would make the r52 entry's claims overlap a sibling's fresh ground. Deliver
{W1}/ConnSiblings/findings.md."""),
item("ConnSources", "connector",
f"""Cross-source consistency scan for the extraction claims. Read {LANE}/corpus/SOURCES.md
rows S108, S112, S138, S245, S250, S251 (the unblob/sasquatch/squashfs-tools family) and
{LANE}/corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md +
{LANE}/corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, then answer: (1) which
existing rows already carry "what the extractor publishes" claims whose scope the new law
must respect (append-only: a correction is a NEW row, never an edit)? (2) do any two rows
disagree about unblob/sasquatch device-node or symlink behavior? (3) which rows should the
round-52 entry's used-by NOT cite (scope mismatch)? (4) does the planned S252 (mknod(2))
duplicate any existing row's URL/anchor (the registry has 19 W04 duplicate-URL warnings -
name whether mknod adds another or is fresh)? Deliver {W1}/ConnSources/findings.md."""),
item("ConnDocs", "connector",
f"""Cross-check the scribe drafts against each other for constant drift (they land in
parallel; absent drafts - note and move on). Read every draft under {W1}/ScribeEntryC1/,
{W1}/ScribeProvince/, {W1}/ScribeReadme/, {W1}/ScribeScorecard/, {W1}/ScribeBlock27/,
{W1}/ScribeLesson/, {W1}/ScribeSources/, {W1}/ScribeMergeAdopt/ and build the constant
matrix: entry stem (2026-10-30-r52-avm-le-squashfs-core), core heading
(`## Round-52 additions to Core`), frontier mark (`Round-52 frontier note`), map count
141 -> 142, claims file path, receipts dir (corpus/evidence/round-52/c1), S-ids cited
(S243/S244/S245/S249/S250/S251/S252 + any merge row) - one row per draft per constant,
flagging ANY divergence. Also flag placeholder-style inconsistencies (some drafts marking
receipts RECEIPT-PLACEHOLDER, others [PLACEHOLDER] - propose one convention). Deliver
{W1}/ConnDocs/matrix.md."""),
# ---------------- simplifier (1) ----------------
item("SimpV1Audit", "simplifier",
f"""Audit the v1 instruments for dead weight the ports must drop. Read
{LANE}/tools/round-50/c1-counter.py, {LANE}/tools/round-50/c1-controls.py and
{LANE}/tools/round-50-c3/sqfs-triage-v5.py: list code paths, flags, constants and selftest
cases that are unreachable or round-50-specific (e.g. attempt-1 workarounds, dead env vars,
unused error branches, controls modes v2 replaces), each with file:line and a keep/drop
recommendation for the v2 port. Dropping a behavior the L1 has not confirmed dead is a
defect - mark uncertain ones KEEP-with-question. Deliver the list under
{W1}/SimpV1Audit/audit.md."""),
]

spec = {
    "wave": "r52-w1",
    "milestone": "r52-w1 build+attack: C1 law package ports, triage v6 audit, docs/sources/assimilation drafts, pre-freeze attacks and probes; L1 freezes, controls, carrier re-fetch, REA data run",
    "reportDir": ".ufo/waves/round-52/w1",
    "context": CONTEXT,
    "items": items,
}

out = pathlib.Path(LANE + '/.ufo/waves/round-52/w1-spec.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(spec, indent=1))
print(f"wrote {out} items={len(items)}")
roles = {}
for it in items:
    roles[it['role']] = roles.get(it['role'], 0) + 1
print("roles:", roles)
attack = roles.get('critic',0)+roles.get('reviewer',0)+roles.get('mutation-tester',0)+roles.get('labrat',0)
print(f"attack share (reviewer/critic/mutation-tester/labrat): {attack}/{len(items)} = {100*attack/len(items):.1f}%")
