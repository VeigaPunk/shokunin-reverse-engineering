# Round 87 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. This is closure evidence, not a lane-authored correction and not a promotion.
Nothing below rewrites a lane-authored byte.

- Lane HEAD before the round: `99f8b6a8979978fe02dc3c8f674ce4fdee3ab44b`.
- Declaration `f0ebf61161d08279dca98841461330ad442d3023`; repair candidate `b5c7a49e20647bb73117ed1ffb4f68dd69916cd8`;
  wave dispatch `1c8a76f41f340d575b707d597678efdfed0550c4`; measured revision `73c3a29740884b0c134bbe50e3c9b13f141daccf`;
  record commit `4136ac0cc6640829655c637ad016db530450b822` (reviewed lane tip, = remote `refs/heads/main`).
- Report: fleet `.ufo/reports/round-87/kaidoku.md`, committed as `0b45dae1d89f648a67e1dcf541c98ae1e4f2599d`.

## 1. Disposition and method

**Status: ok. Admitted: true. Verdict: admitted.** R87-C1 (coverage, capability) is re-measured by
the integrator on this host: `recovered 0 of 8` (do-nothing) and `4 of 8` (cheap rule) at the
declaration, `recovered 8 of 8` with all three controls true and exit 0 at the measured revision. No
owned axis is harmed; the record files are append-only (0 deletions).

Method. The claim's measuring instrument — the frozen battery, a registered *counter*, not a gate —
was **re-run by the integrator** over a sandbox extraction of the measured revision
(`git archive 73c3a297 | tar -x` into `/fast/scratch/hyaku/closure-kaidoku-r87/tree`), with the
host's pinned `/usr/bin/upx` (sha256 `cf2f6e7c…c969`), the four pinned carriers, and the
`rea-agents@6.5.0` package whose `package.json` hashes `a5003023…0a6c`. Lane-owned **gates**
(`freeze-precheck.py`, `registry-opened-check.py`) and the tools' `--selftest` modes were **not**
executed: every gate/selftest statement below is committed-evidence verification (PROTOCOL §Gate
standard, *Closure consequence*). Committed bytes were recounted with `git show`, `grep -c`,
`sha256sum`, `git diff --numstat`, `git merge-base --is-ancestor` and `scripts/sources-census.sh`.

## 2. Step-1 conformance

| check | command / evidence | observed result |
|---|---|---|
| Report landed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-87/kaidoku.md` (fleet) | `kaidoku-shokunin kaidoku@shokunin.local 0b45dae1d89f648a67e1dcf541c98ae1e4f2599d` |
| Report is substantive, not a marker | report body | One declared claim with a frozen predicate, five cited lane commits, before/after with a counting command, Sources & frontier with both census outputs, three trend verdicts, `## SHONEN`; `grep -c '^## SHONEN'` → 1, four `[~]` lines matching the four `SHONEN.md` boxes |
| Required sections and order | report headings | Work performed → Landed changes → Before → after measurements → Sources & frontier → Trend verdicts → SHONEN → Wave shape → Stale-lane → Tool installs → Misroot sweep → Open L0 → Routed |
| Cited commit existence and ancestry | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> refs/heads/main` for `99f8b6a8`, `f0ebf611`, `b5c7a49e`, `1c8a76f4`, `73c3a297`, `4136ac0c` | All six are commits and all six are ancestors of `refs/heads/main` (tested against the branch ref, never `@{u}`) |
| Lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state kaidoku-shokunin`; `git -C kaidoku-shokunin status --porcelain` | `branch=main local=4136ac0cc6640829655c637ad016db530450b822 remote=4136ac0cc6640829655c637ad016db530450b822 ahead=0 behind=0 head=detached tracked=0 untracked=6`; the six untracked entries are the orchestrator handoff markers `.ufo/waves/round-85|86|87/r8*-w1.ready(.dispatched)` — no lane round work left uncommitted |
| Report lands last | `git log -1 --format='%ai %ci'` on the lane tip and the report commit | Lane tip author/committer `2026-11-04 19:29:23 / 19:29:26 -0300`; report commit `19:27:23 / 19:30:19 -0300`. The report's *author* timestamp is a jj working-copy artifact and precedes the lane tip; its *committer* timestamp follows the lane push, and the cited hash is the pushed tip, so the landed bytes were committed after the lane work — no filed-before-commit defect |
| Template contract in the dispatched prompt | rendered `templates/round-prompt.md` (`{{FLEET_ROOT}}`→fleet root, `{{LANE}}`→`kaidoku`, `{{ROUND}}`→`87`, `{{AXES}}`→the lane's axes line) compared line by line with `.ufo/prompts/kaidoku-round-87.md` | 0 absent lines across all six template sections. Round-level items present: mission/axes binding, 1–3 distinct-axis claims with a lowest-axis claim and a do-nothing control, the batched ≥8 L2 floor, commit-then-push, push scope, L0 side channel. Five child-lane items present: report path, commit-before-report, `SHONEN` heading, hash-citation rule, write scope. Hyaku addendum is section 6 |
| L2 route map vs `MISSION.md` | `MISSION.md` §L2 concurrency; prompt §3 | `MISSION.md` states role classes → route buckets with no alias pins, and prompt §3 says route through `task.agentModelOverrides`; no bucket conflict. The addendum's alias history is operator directive text, not a MISSION bucket |
| Wave shape | `r87-w1-spec.json`, `r87-w1-results.json`, `ufo-wave-policy.json` | `seats 11`, all eleven with a non-empty output, 0 dead: scout 1, executor 3, scribe 2, reviewer 1, critic 1, mutation-tester 1, sentinel 1, connector 1. Policy `minLanes 8` / `maxLanes 256`, directive band 8–16 → 11 in band. Attack 3/11 = 27.3 % (≥ 25 %); connector 1 (≤ 2); L2 floor ≥ 8 met inside one wave; planner held by the L1 (the validator rejects `planner`), disclosed |
| Dispatch/completion digest | `.ufo/watchdog.log` (mutable; digest copied) | No `lane-dead-no-report kaidoku round=87` line. Digest verbatim below |

```text
2026-11-04T18:48:30-03:00 launch kaidoku round=87 pgid=1340784 driver=hyaku-inline attempt=1
2026-11-04T19:30:45-03:00 complete kaidoku round=87; hyaku-inline attempt=1
```

Conformance defects found are routed in §6; none turns this real report into a marker, so `failed`
does not apply. No SHONEN box is written here and no `[x]` is claimed.

## 3. Per-claim re-check

### R87-C1 — coverage (capability) — target `recovered 8 of 8`, controls true, exit 0

**Re-measured by the integrator**, in a sandbox extraction of `73c3a297` (tools byte-identical there
and at the tip: repair `96da7d8e…bec24`, counter `0f2d2bd8…4b0`):

```sh
cd /fast/scratch/hyaku/closure-kaidoku-r87/tree   # git archive 73c3a297 | tar -x
python3 -I -B tools/round-87/upx-tamper-battery.py --root . \
  --repair-cmd tools/round-87/upx-magic-repair.py --upx /usr/bin/upx \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/closure-kaidoku-r87/work --json-out /fast/scratch/hyaku/closure-kaidoku-r87/recheck-real.json
```

| run | observed (integrator) | reported | agree |
|---|---|---|---|
| real repair | `recovered 8 of 8 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True, 'N3-intact-idempotent': True} met=True exit=0` | 8 of 8, controls 4/4, 0/4 recovered, 4/4, exit 0 | agree |
| do-nothing `identity` | `recovered 0 of 8`, `N1-refuse-plain False`, `met=False exit=1` | 0 of 8, exit 1 | agree |
| cheap rule `naive-global` | `recovered 4 of 8`, `N1-refuse-plain False`, `met=False exit=1` | 4 of 8, N1 false, exit 1 | agree |

Per-case arms in the integrator's receipt: all eight cases `recovered True` with
`{repair_rc0, windows_only, test_ok, identity, rea_recover}` all true; `N1` rc 2 on all four plain
originals; `N2` never recovered on any carrier; `N3` byte-identical on all four. Unpacked sha256 per
carrier equals the pin (`e8156675…`, `7b1e5d0c…`, `6c78c5e5…`, `0bd49c8d…`). REA 6.5.0 counts after
repair: jq `167/30/190`, xxd `99/29/103`, libz `184/29/199`, dinit `1268/29/1111` — the four
declared original inventories, matching the report line.

Pin preconditions verified on this host: `sha256sum /usr/bin/jq /usr/bin/xxd /usr/lib/libz.so.1.3.2
/usr/bin/docker-init /usr/bin/upx` prints exactly the five pins in the counter; the REA package
`package.json` hashes `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb3050a6c` (version 6.5.0).

Before-state (end-to-end domain task, evidence-verified, not re-executed): `.ufo/waves/round-87/w1/ExecReaBefore/before.json`
shows, per carrier, the tampered file running (`runtime.rc 0`, jq `jq-1.8.2`, dinit `tini 0.19.0`),
`upx -t/-l/-d` exiting 2 with `NotPackedException`, REA blind to the tamper (jq/xxd/dinit 3
procedures = stub only; libz 98 of 184), then after repair `upx -t` rc 0, `upx -d` sha256 = the pin,
REA at the declared count. The report's "REA counts after repair" line and its before/after numbers
match this file.

Kill-rule clauses: the counter is pinned by sha256 in `claims.json`; `--repair-cmd` is the only
population input; the repair reads only `--in`/`--out` (ReviewerRepair PASS, and its imports are
`argparse/json/struct/sys`). The declared weakening (M87-3, a chain-walk-free heuristic also scores
8/8) is disclosed in the report, the lesson, QUALITY row 152 and the knowledge entry; the frozen
predicate is unchanged and still met.

**Claim verdict: met, re-measured.** Axis `coverage`: **improved** — the measured before→after is the
counter, not the saturated 0–10 proxy (10.0 before and after; `SCORECARD.md` diff edits no score row).

### No-harm re-checks

| surface | command | observed |
|---|---|---|
| Owned axis rows | `git diff 99f8b6a8 4136ac0c -- SCORECARD.md` | 17 insertions, **0 deletions**; `grep -c '^-[^-]'` → 0; coverage/depth/calibration/freshness rows untouched; one capability row and one round section appended |
| Append-only files | `git diff --numstat 99f8b6a8 4136ac0c -- LOG.md SCORECARD.md SKILL.md PROVINCE.md corpus/QUALITY.md corpus/SOURCES.md corpus/README.md corpus/lessons/round-87.md plans/round-87-claims.md` | `LOG 10/0`, `SCORECARD 17/0`, `SKILL 13/0`, `PROVINCE 31/0`, `QUALITY 4/0`, `SOURCES 3/0`, `README 4/0`, lesson `59/0`, plan `83/0` — every record file append-only |
| Prior instruments untouched | `git diff --stat 99f8b6a8 4136ac0c -- tools/round-70 tools/round-84 tools/round-85 tools/round-86` | empty — the round-84 freeze precheck is kept byte-identical (the fix is a new superseding file) |
| Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | `kaidoku ok …/corpus/SOURCES.md`, **exit 0**, 27 `W04` duplicate-URL warnings, all pre-existing (none names S306–S308) |
| Registry delta | `grep -c '^\| S[0-9]' corpus/SOURCES.md` at both revisions; tier histogram; malformed-row awk | 210 → **213**; A 191 → 194, B 11 → 11, C 8 → 8; malformed rows 0; the three new rows are `mined`, `opened 2026-11-04`, `recheck 180d`, `used-by corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` (path exists) |
| Capability row + Core move | `SCORECARD.md` capability table; `PROVINCE.md` `## Round-87 additions to Core`; `corpus/README.md` round-87 note | capability `UPX magic-tamper repair` with the 8/8 receipt pointer; Frontier class "anti-UPX stub whose magic … is altered" moved to Core for the four carriers × magic-only tampers; entry-altered stubs, other packers, BE/PE stay Frontier |
| Mistakes mined | `corpus/lessons/round-87.md` `## Mistakes` | M87-1..M87-4, each with class · evidence pointer · captured-by · fix. M87-1 receipt shows the three pre-freeze findings (`…-at-base.js` twice, plus the genuine M87-4 `upx-magic-repair.py`); M87-2 receipt is red on round 86 (`S305`, flags `no-document`, `no-locator`) and clean at the base; M87-3 has the cheap-v4 receipt; M87-4 is disclosed as unrouted-but-named |
| Round criteria landed | `corpus/QUALITY.md` rows 152, 153 | both appended with their evidence and the lesson they cite (M87-3, M87-2) |

## 4. Discernment spot-check (LEARNING.md — checked from outside)

Sources were re-opened by the integrator over the network (`curl`), never read from the lesson.
All four fetches returned HTTP 200 with the byte counts and sha256 the rows and lesson claim.

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S306 UPX `src/stub/src/include/linux.h` | **admit** (code, tier A, mined) | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h` fetched 2026-11-04: 200, 19689 bytes, sha256 `5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9` | **agree** | The lesson's quote (11 words) is at line 579, and every anchor the row states resolves exactly: `#define UPX_MAGIC_LE32` 540, `struct b_info` 570 / `sz_cpr` 572, `struct l_info` 579 / `l_magic` 582, `struct p_info` 588. The quote normalizes the file's column spacing; the words and location are right |
| S307 UPX `src/p_lx_elf.cpp` | **admit** (code, tier A, mined) | same URL pattern: 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | **agree** | Quote (8 tokens) is exactly line 8065 `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic`; the stated overrides exist at 7755 (`PackLinuxElf64::unpack`) and 9023 (`PackLinuxElf32::unpack`) and the check repeats at 9310. The `teaches` cell (the Linux ELF unpacker's own end-of-file check) is grounded by the quote |
| S308 UPX `src/packhead.cpp` | **admit** (code, tier A, mined) | same URL pattern: 200, 13236 bytes, sha256 `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a` | **agree** | Quote (9 tokens) is lines 64–66 verbatim; `get_packheader_checksum` starts at 62, `buf += 4;` is 65, `blen -= 4;` is 66. The `teaches` cell (the checksum starts after the four magic bytes) is exactly what the code does |
| UPX `src/p_unix.cpp` | **reject** (no row) | same URL pattern: 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | **agree** | Line 671 does carry the same `sz_cpr` check inside `PackUnix::unpack`, but both Linux ELF classes define their own `unpack` (7755, 9023), so the ELF claim rests on S307 and a row for `p_unix.cpp` would duplicate the scope. The stated flip condition (a carrier unpacked through `PackUnix::unpack`) is the right one |

Row-level check: S306–S308 are the only new rows; each carries a locator, an ISO `opened` date, no
"no document opened" text, `status mined`, and a `used-by` path that exists — the substance of the
round's M87-2 fix, verified by eye (its gate was not executed). The lane's own gate decisions agree
with this spot-check on 3 admits and 1 reject, each with a reason.

## 5. Axis verdicts and trends

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | R87-C1 re-measured 0/8 → 8/8 with controls true (integrator run); the PROVINCE Frontier class "anti-UPX stub whose magic … is altered" moves to Core for four pinned carriers, one capability row enters, one knowledge entry lands on ground the coverage map listed as Frontier. The 0–10 proxy is saturated at 10.0; the move is measured on the surface, not the number |
| depth | **unchanged** | No score row edited; the round's SKILL addition is a four-row symptom→action table inside the coverage claim's landing, not a new depth measurement. No depth instrument changed (`tools/round-70`…`round-86` diff empty) |
| calibration | **unchanged** | The report's numbers match the receipts and the integrator's re-run; the overstated plan sentence ("only a structural repair reaches") is disclosed as M87-3 rather than left standing. Nothing measured regressed, nothing new claimed |
| freshness | **unchanged** | Three sources opened and mined with 180d recheck; no stale entry re-verified this round and none is flagged stale |
| adjacency | **unchanged** | ConnectorR87 found no sibling holding UPX/ELF repair ground (`w1/ConnectorR87/links.md` §2); no contested scope reported, none absorbed |

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | One admitted knowledge entry on uncovered ground (`corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`), its `source:` citing three rows that went absent → mined this round (S306–S308), plus one capability row entering through a demonstrated run; the coverage map's Frontier line became a Core row |
| quality | **improved** | A weaker instrument entry is superseded by a stronger one: `tools/round-87/freeze-precheck.py` replaces the round-84 `.js`/`.json` pattern (round-84 file kept byte-identical, 13-case selftest, and the pre-freeze receipt shows the old pattern's false findings), and the M87-2 registry check is red-before at `4cc03025` (S305) and clean at the base. The repair was hardened against the wave's decoy and DoS findings before the scored run, and the new entry's limits are stated in it. No admitted entry failed its re-check |
| discernment | **improved** (lane self-assessed "unchanged, pending non-author closure"; that closure is this file) | The outside spot-check agrees with the gate on its admits (S306, S307, S308 — quotes and digests re-opened) and its reject (`p_unix.cpp`), each with a reason above; the two mined mistakes became grounded `QUALITY.md` criteria 152 and 153 citing `corpus/lessons/round-87.md`. The critic's falsified rationale was reported, not hidden |

Round: **admitted** — the single claim verifies by re-measurement and no axis is harmed.

## 6. Routed defects for the next steered round

1. **V87-1 (evidence durability, M87-3).** `w1/CriticClaim/receipts/cheap-v4-checksum-lite-rea.json`
   names its repair as `../../../../../fast/scratch/hyaku/kaidoku-r87/CriticClaim/var/v4-checksum-ph-lite.py`,
   and that scratch tree is deleted (correct scratch discipline). The heuristic script is not
   committed, so M87-3 and QUALITY row 152's pointer cannot be re-derived by a reader — a receipt
   without its instrument is a claim, not evidence. Commit the heuristic (or the counter revision that
   freezes it as the second cheap-rule control, already planned) next round.
2. **V87-2 (missing receipt).** The report's Sources bullet states "The new rows pass
   `registry-opened-check` (base `99f8b6a8` → `73c3a297`: clean)"; no receipt at that revision is
   committed — `w1/ExecFixCheck/base-clean.json` is `base == rev == 99f8b6a8` and `l1/fixcheck-r86-red.json`
   is the round-86 red. The rows do carry locators, opened dates and resolvable `used-by`, so the
   substance holds; commit the 99f8b6a8 → measured-revision receipt.
3. **V87-3 (routing provenance).** The report records "the amendment-9 map with every role on
   `@m_mim`", while `~/.omp/agent/config.yml` now shows `@m_flash` for every role except reviewer
   (`@m_zfl`) and `r87-w1-results.json` records no per-seat model. Routing is operator-owned and is
   not a claim, but the statement is unverifiable from committed bytes: record the captured route per
   seat when a claim could depend on it.
4. **V87-4 (stale-lane actuator).** The `## Stale-lane` line says only "respawn-per-round driver; no
   other mission of this lane is open" and does not grade this mission (launch 18:48:30 → complete
   19:30:45, 42 min) as `progressing` or `silent`, which the report contract asks for any mission open
   longer than two driver ticks.
5. **Carried (not re-judged here).** V86-6 (A3 coverage pointer), V86-7 (round-86 counter false
   greens), R85-4, the planner-seat deviation, M87-3's second cheap-rule control, M87-4 (claimed
   artifact inside counter-scanned claim strings), the counter exit-contract fixes F5/F6 (uncaught
   exception exits 1; N1 counts rc `None` as a refusal) and the twelve surviving repair mutants /
   six surviving counter mutants. All stay on the queue; none is a pass.

Observation for the operator, not a lane defect: the fleet working tree carries ` M
.ufo/reports/round-84/kama.md` (another lane's report), `?? after`, and orchestrator `.scratch/*`
closure files; none is kaidoku round-87 work and none was touched. SHONEN box 2's end-to-end domain
task is now evidenced (tamper → REA before → repair → `upx -d` to the pin → REA after), and boxes 1,
3 and 4 carry resolvable pointers; the four boxes look checkable by a non-author, but promotion and
`[x]` are operator-owned and none is written here.
