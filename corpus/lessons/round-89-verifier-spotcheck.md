author: hyaku closure (non-author integrator, @m_zfl)

# Round 89 — non-author spot-check (kaidoku)

Non-author closure review of kaidoku round 89. I did not author this round and did not improve it.
Round-time lane HEAD before the round `0ec2bb4016655f605657d6e0e700ec2e6893ac27`; after
`5068ba6417f3cfc6693ca5e4dbe106c08e305174`. The lane advanced to
`fd9f840bdc1ec16dd1a1d36ff52500b8ede03cdc` at 22:06:46 -0300, after the driver's completion line
(21:52:03); both revisions are reported below, and every claim measurement is taken at the cited
after-HEAD unless the cell says otherwise.

Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-04T21:20:19-03:00 launch kaidoku round=89 pgid=780802 driver=hyaku-inline attempt=1`;
`2026-11-04T21:52:03-03:00 complete kaidoku round=89; hyaku-inline attempt=1`.

## 1. Status ruling — the report is a completion marker

The filed report `.ufo/reports/round-89/kaidoku.md` is 46 lines / 1513 bytes and consists of two
declared claims followed by seven empty section placeholders:

```
$ wc -c .ufo/reports/round-89/kaidoku.md
1513 .ufo/reports/round-89/kaidoku.md
$ grep -c '<!--' .ufo/reports/round-89/kaidoku.md
7
$ grep -cE '^[[:space:]]*-[[:space:]]+\[[xX~ ]\]' .ufo/reports/round-89/kaidoku.md
0
$ grep -oE '\b[0-9a-f]{7,40}\b' .ufo/reports/round-89/kaidoku.md
0ec2bb4016655f605657d6e0e700ec2e6893ac27      # the base revision only; no work commit
```

It carries no `Landed changes`, no measurement, no evidence pointer, no `Sources & frontier`, no
trend verdicts, no SHONEN mark line, and no resolvable commit. Under PROTOCOL §Round-robin
rounds (a filed report recording no lane work is a marker) and the dispatched prompt's own marker
rule (§4: "a contentless report (placeholder text, … or no evidence pointers) counts as the round
failed"), the lane-round is **failed**. The driver's `report_of()` accepted it because that check
is heading + `MIN_REPORT_BYTES` only (scripts/shokunin-watchdog.sh:187-207); completion by the
driver is not admission.

## 2. Step-1 conformance

| item | observed | verdict |
|---|---|---|
| report committed in the fleet repo by the lane identity | `kaidoku-shokunin <kaidoku@shokunin.local>` `d0f49dc5277932a8aaf90febd68e48d09abfe8bb` 2026-11-04 21:52:00 -0300, subject "round-89: kaidoku report (hyaku sweep: L1 returned without committing; attribution defect)"; reachable from `origin/main` | attribution defect (the commit is a hyaku sweep under the lane identity, not a lane commit) |
| `SHONEN` heading with one line per box | heading present; 0 mark lines (`grep -cE '^- \[[x~ ]\]'` = 0) | contract violation; also the marker predicate |
| every cited lane commit exists and is an ancestor of the branch | the report cites no lane commit at all; nothing to test | no citation = marker; ancestry unverifiable |
| lane repo clean of round work and pushed | at round time `jj-lane.sh state` → `branch=main local=5068ba64… remote=5068ba64… ahead=0 behind=0 head=detached tracked=0 untracked=15`; at review close `local=fd9f840b… remote=fd9f840b… ahead=0 tracked=1 untracked=15`; `git status --porcelain` lists `corpus/lessons/round-89.md`, `.ufo/waves/round-89/w1/` (14 seat reports and their receipts), `r89-w1-spec.json`, `r89-w1-dispatch.json`, `r89-w1.ready*` as untracked | **uncommitted round work**: the round's lesson and the whole wave evidence are working-tree only |
| prompt carries the template contract | `.ufo/prompts/kaidoku-round-89.md` §1–§5 differ from `templates/round-prompt.md` only by placeholder substitution (51 diff lines, all `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions); §6 carries the hyaku addendum; no route map is quoted beyond the run-15 lines, which match `MISSION.md` | conformant |
| wave shape | `.ufo/waves/round-89/w1/swarm-registry.json`: 14 members — executor 4, scribe 3, reviewer 2, critic 1, mutation-tester 1, sentinel 1, scout 1, connector 1; attack 4/14 = 28.6 % ≥ 25 %; one connector; `r89-w1-dispatch.json` counts spawn 14 (≥ L2 floor 8, one batched wave) | conformant |
| `LOG.md` entry for the round | `git show fd9f840b:LOG.md \| grep -c 'round 89'` → 0 | contract violation (no iteration-log entry; every landed change must tie to one) |
| `SCORECARD.md` record for the round | `git show fd9f840b:SCORECARD.md \| grep -c 'round 89'` → 0; no diff to `SCORECARD.md` between base and after-HEAD | contract violation (AXES §SCORECARD contract: per-claim score delta, evidence pointer, counting command, measured commit) |
| round lesson | `corpus/lessons/round-89.md` exists but is untracked and its `## Wave r89-w1 — seat results` section is the literal placeholder `<!-- WAVE-SECTION -->` | uncommitted round work; incomplete lesson |

## 3. Per-claim re-check

R89-C1 (coverage, capability acquisition — the wrong-value first-block `b_info.sz_cpr` class enters
Core). Evidence-verified, not re-executed (the claim rests on a lane-owned counter; PROTOCOL §Gate
standard forbids me executing it):

```
$ sha256sum tools/round-89/upx-field-value-repair.py tools/round-89/upx-field-battery.py
332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070  tools/round-89/upx-field-value-repair.py
f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720  tools/round-89/upx-field-battery.py
# both equal the `instruments` pins in .ufo/waves/round-89/claims.json

$ jq -c '{label,met_target,exit,controls_ok,repair_sha256}' .ufo/waves/round-89/pre/c1-candidate-at-declaration.json
{"label":"recovered 4 of 4","met_target":true,"exit":0,
 "controls_ok":{"N1-refuse-plain":true,"N2-corrupt-payload":true,"N3-intact-idempotent":true,"isolation":true},
 "repair_sha256":"332917f2b6…"}
$ jq -c '{label,met_target,exit,recovered}' .ufo/waves/round-89/pre/c1-base-r88-repair.json
{"label":"recovered 0 of 4","met_target":false,"exit":1,"recovered":0}
$ jq -c '{label,met_target,exit,recovered}' .ufo/waves/round-89/l1/scores/c1-r88class-regression.json
{"label":"recovered 4 of 4","met_target":true,"exit":0,"recovered":4}
$ jq -c '{label,met_target,exit,recovered}' .ufo/waves/round-89/l1/scores/c1-r87class-regression.json
{"label":"recovered 8 of 8","met_target":true,"exit":0,"recovered":8}
$ ls .ufo/waves/round-89/l1/scores/
block29-cells.json  c1-r87class-regression.json  c1-r88class-regression.json
```

Observed: the after-receipt is the *declaration-time* run (committed at `9da6c980`, the declaration
commit) whose `repair_sha256`/`tool_sha256` are byte-identical to the landed instruments, with all
four controls true; the before-receipt (unchanged round-88 repair) is 0 of 4 with the same controls
true; the round-87 and round-88 regression arms are green and committed at `5a46542a` (after-HEAD).
No receipt measures the main arm at the landing revision, and the receipts carry no `revision`
field — a defect routed below, not a reason to doubt the class (fixture population pinned by digest,
instrument bytes identical). R89-C1 stands **met** on committed evidence.

R89-C2 (depth — craft rule block 29 and the target-aware depth atom). Re-measured by me, with my own
counter over committed bytes (the lane's gate was not executed):

```
# mine: split SKILL.md's '## Queue-drain craft ' section on '^- \*\*', resolve each block's
# corpus/knowledge/<stem>.md[:start[-end]] at the revision, then apply the declared shape floor
# (>=25 words, >=2 backticked spans)
$ python3 <inline counter>  # at 5068ba6417f3cfc6693ca5e4dbe106c08e305174
blocks 29 resolved 29 unresolved []
$ python3 <inline counter>  # at 0ec2bb4016655f605657d6e0e700ec2e6893ac27
blocks= 28
$ jq -c '{blocks,resolved,unresolved,revision,met_target,exit}' .ufo/waves/round-89/pre/c2-depth-at-base.json
{"blocks":28,"resolved":28,"unresolved":[],"revision":"0ec2bb40…","met_target":false,"exit":1}
```

Block 29's citations at after-HEAD are `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`
(99 lines at base), `…-r87-upx-magic-tamper-repair.md` (125 lines at base) and
`…-r86-record-agreement.md` — all present at the base revision, so the claim is causally separable
(the round-88 M88-9 defect is fixed); the block is 245 words with 34 backticked spans, above the
shape floor. R89-C2 stands **met**, re-measured by me. No committed after-receipt exists for it
either (`.ufo/waves/round-89/l1/scores/` holds only the cell matrix and the two regression arms).

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | the wrong-value `sz_cpr` class enters Core: `PROVINCE.md` "Round-89 additions to Core", `corpus/README.md` round-89 coverage row and frontier note, knowledge entry `2026-11-04-r89-binfo-field-value-class.md` (113 lines at after-HEAD), three registry rows; class measured 4 of 4 vs 0 of 4 for the unchanged round-88 repair (committed receipts), regression arms 8 of 8 and 4 of 4 at after-HEAD |
| depth | **improved** | craft block 29 (field value classes and their refusal signatures) lands: 28 → 29 blocks, 29/29 resolved by my own count at after-HEAD; base arm red at 28 with `--expect-blocks 29` (committed receipt naming the base revision); the round-88 target-blind counter superseded by `depth-blocks-v2.py` with a declared supersession in `claims.json` |
| calibration | **harmed** | the committed entry states `verified-at: 2026-11-04 (round 89; measured revision and receipt in SCORECARD '## 2026-11-04 — round 89')` and no such section exists (grep count 0 at both after-HEAD and the tip `fd9f840b`); it also names `tools/round-89/field-class-matrix.py`, absent from the tree (`ls tools/round-89/` → `depth-blocks-v2.py`, `upx-field-battery.py`, `upx-field-value-repair.py`), and cites `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, which is untracked; neither claimed axis move has a `SCORECARD.md` record or a `LOG.md` entry, and the round's own report asserts two met claims with zero evidence. Self-assessment surfaces do not match the repo state they claim |
| freshness | unchanged | no drift claim; the round-88 docstring defect (D1) is routed, not repaired (the frozen bytes stand) |

## 5. Discernment spot-check (LEARNING.md §"Discernment is checked from outside")

Sampled from `corpus/lessons/round-89.md` `## Gate` (untracked at review close — read from the
working tree, defect D-89-6): two admits and two rejects, every source re-opened by me on
2026-11-04.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S311 UPX v5.2.0 `src/p_lx_elf.cpp` (admit, code, tier A) | admit | `curl https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp` → HTTP 200, 373743 bytes, sha256 `551fc8675a594937…`; line 7101 `// Peek: unpack into ibuf, but do not write`, line 7104 `if (sz_block1 < sz_elf_hdrs) {`, line 7105 and line 7308 `throwCantUnpack("corrupt b_info");` | **agree** | the byte count, digest and line numbers reproduce exactly; the throw is the block walk's short first-block peek, so the message names the walk, not one field — exactly what the row's `teaches` and craft block 29 use it for |
| S312 UPX v5.2.0 `src/p_unix.h` (admit, code, tier A) | admit | same URL → HTTP 200, 6651 bytes, sha256 `73bd992ec0fb4602…`; line 192 `packed_struct(l_info)`, line 200 `packed_struct(p_info) { // 12-byte packed program header`, line 202 `LE32 p_filesize;`, line 203 `LE32 p_blocksize;` | **agree** | line numbers and the quoted text reproduce; it grounds the `l_info + 12` / `b0 = l_info + 20` offsets the entry uses |
| UPX v5.2.0 `src/headers.h` (reject — round-88 rejection stands) | reject | same URL → HTTP 404, 14-byte body `404: Not Found` | **agree** | the path does not exist at tag `v5.2.0`; the flip condition (the file appears at a later tag) is stated and unmet |
| UPX v5.2.0 `src/p_unix.cpp` (re-opened, reject retained) | reject | same URL → HTTP 200, 24181 bytes, sha256 `bf83c4133c27d394…`; `grep -n 'corrupt b_info'` → lines 491, 495, 497, 502, 553, 682, 690, all inside `PackUnix::unpack`; `grep -c 'un_shlib_1'` → 0 | **agree** | the shared-object carriers unpack through `PackLinuxElf64::un_shlib_1`/`PackLinuxElf32::un_shlib_1` (S311); round-87's flip condition ("a carrier class unpacked through the base class") is still unmet, so the rejection is the right call and is traceable both ways |
| new `corpus/SOURCES.md` rows S311/S312: Gate quote ≤ 25 words with a location | check | lesson Gate cells: S311 "Peek: unpack into ibuf, but do not write" (9 words) + "if (sz_block1 < sz_elf_hdrs)" (3 words) at lines 7096-7104, throw at 7105; S312 "packed_struct(p_info) { // 12-byte packed program header" (6 words) at line 200 | **agree** | both quotes are inside the 25-word limit, located, and reproduce verbatim; `opened` is 2026-11-04 with HTTP status and byte counts, and the status change (absent → mined, `used-by` set) is logged old→new |

Census (run by me, not by the lane): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `kaidoku ok
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, with the declared cross-scope
warning `W04 S311 duplicate url raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp`. Row
count re-derived from committed bytes: `git show <rev>:corpus/SOURCES.md | grep -cE
'^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 215 at `0ec2bb40`, 217 at `5068ba64` — matches the
reported 215 → 217.

## 6. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | net new admitted entry `corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md` on ground the coverage map did not hold (`corpus/README.md` gains the "Packed-ELF `b_info` value classes (round 89)" row and the round-89 frontier note; `PROVINCE.md` gains the Core row); its `source:` lines cite the newly mined S311/S312; registry 215 → 217 rows |
| quality | **harmed** | the new entry is admitted while carrying two non-resolving pointers (`verified-at` → a `SCORECARD.md` section that does not exist; `tools/round-89/field-class-matrix.py` → absent) and citing an untracked receipt, and nothing marks or corrects them at the tip; the two claimed measurements have no persisted score row. The additions themselves are real (QUALITY rows 161-165, later 166-167; block 29 supersedes the flat round-88 routing), which is why this reads as the trade the round actually made, not as a null round |
| discernment | **improved** | the outside spot-check agrees with the gate on all four sampled decisions (2 admits, 2 rejects) and on the quote-length rule, each re-opened at its URL; no disagreement to mine |

## 7. Routed defects (the lane fixes these in its next steered round)

- **D-89-1 (marker report).** `.ufo/reports/round-89/kaidoku.md` is a placeholder skeleton; file a
  real report for this round as an erratum-bearing next-round record, or accept the failed row. The
  driver's `report_of()` accepted it (heading + byte floor only) — the known marker hole.
- **D-89-2 (attribution).** The report commit `d0f49dc5` is a hyaku sweep under the lane identity
  ("L1 returned without committing"). The lane must land its own report commit; the sweep is
  recorded as an attribution defect.
- **D-89-3 (no landing measurement).** `l1/scores/` holds no `c1-at-<rev>.json` and no
  `c2-at-<rev>.json`; the C1 after-receipt is the declaration-time run and names no revision, and
  the C2 after-state exists only as prose. Re-run both frozen counters at the round's measured
  revision and commit the receipts.
- **D-89-4 (uncommitted round work).** `corpus/lessons/round-89.md` (with its `## Wave r89-w1 —
  seat results` section still `<!-- WAVE-SECTION -->`) and the whole `.ufo/waves/round-89/w1/` seat
  evidence (14 seats, receipts), plus `r89-w1-spec.json`/`r89-w1-dispatch.json`, are untracked in
  the lane repo. Commit them or record why not.
- **D-89-5 (no LOG / SCORECARD record).** `LOG.md` has no round-89 entry and `SCORECARD.md` no
  round-89 section: neither claimed axis move carries its score delta, evidence pointer, counting
  command and measured commit, and the round's capability does not enter the capabilities table.
- **D-89-6 (dead pointers in an admitted entry).** `corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md`
  `verified-at:` points at a `SCORECARD.md` section that does not exist; the entry names
  `tools/round-89/field-class-matrix.py`, which is not in the tree, and cites
  `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, which is uncommitted. Repair the pointers or the
  entry is not evidence (PROTOCOL §Evidence standard).
- **D-89-7 (post-completion advance).** The lane pushed `fd9f840b` at 22:06:46 -0300, after the
  driver's completion line, editing the round-89 entry and adding QUALITY 166-167. It is
  round-89-labelled work landing after the round closed; the lane records it in its next `LOG.md`
  entry and commits the receipts it cites.

## 8. Ruling

`lanes.kaidoku = failed` (marker), `admitted = false`, `verdict = failed-marker`. The two declared
axis moves are real on committed evidence (coverage and depth improved; C2 independently
re-measured by me), but a marker report closes nothing, calibration is harmed by the
non-resolving self-assessment pointers, and the round's own records (report, LOG, SCORECARD,
lesson) are absent or uncommitted. No promotion: `SHONEN.md`'s four boxes remain `[ ]`, and box 2
(an end-to-end domain task logged in `LOG.md`) has no round-89 `LOG.md` entry to cite — none of the
four boxes is checkable by a non-author from this round's record.
