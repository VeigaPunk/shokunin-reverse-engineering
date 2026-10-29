# ExecErrataSweep — carry-over audit of attempt 1's not-landed list (round 50, attempt 2, wave 3)

**VERDICT: the carry-over list is mostly addressed, but C1 cannot be met with the frozen
bytes — and the blocker is a defect in the frozen `gap-rule.json`, not the host load.**

The attempt-2 plan addresses 6 of the 11 attempt-1 not-landed items outright, re-scopes 2,
and leaves 3 unowned (SHONEN, QUALITY row 94, and — the serious one — the frozen gap rule
that makes the C1 target of 4 carriers unreachable). The attempt-1 controls' four
`could_not_evaluate` controls were re-scored by the L1 in this wave and **all four now
behave as planned** — but the positive control (CTL-C1-POS) is red for a different reason:
`carriers_matched 2` of `target 4`, because `gaps_ok` fails on g7581 and g7582 under the
frozen gap rule.

Detail: `…/w3/ExecErrataSweep/carry-over.md` (the checklist, §A items, §B the controls
table, §C extra findings). Reproduction: `…/w3/ExecErrataSweep/repro_gaps_ok.py` +
`repro-gaps-ok.json` + `counterfactual-gaprule.txt`.

---

## Findings

| # | Finding | Exact command | Exit | sha256 / key output | UTC |
|---|---|---|---|---|---|
| F1 | **Frozen `gap-rule.json` cannot admit the 7581/7582 carriers → C1 target of 4 is unreachable.** The rule sets `required["char-device"]=true`, `allowed["char-device"]=["unpublished-entry"]`, `removed.silent["char-device"]=["247:0"]`. The kept carriers' frozen non-regular tables hold **13** char-devices each for g7581/g7582 (`dev/led 247:0`, `dev/pts/0..7 136:0..136:7`, `dev/tiatm 230:0`, `dev/ttyp0..2 3:0..3:2`) vs **1** for c6430/c6490 (`dev/led 247:0`). The 12 non-`247:0` devices carry **no** `unpublished-entry` gap (unblob cannot create a device node unprivileged and reports none) and are not removals → `disposition_check` → "required entry with no disposition" → `gaps_ok` False → `carriers_matched` caps at 2/4. | `python3 -I -B .ufo/waves/round-50/w3/ExecErrataSweep/repro_gaps_ok.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json-out …/repro-gaps-ok.json` | **0** (defect reproduced) | stdout `{"defect_reproduced": true, "live": {"live:c6430": true, "live:c6490": true, "live:g7581": false, "live:g7582": false}, "pos": {"pos:c6430": true, "pos:c6490": true, "pos:g7581": false, "pos:g7582": false}}`; json sha256 `6db7c0fc59b5f368db14e4ac213332290425bb09730cd89f029309b94efd2882`; stdout sha256 `ca444ce5412d6414dc7dcf5d1340bc773fa3861488881a581ebc95c71fcfca09`; script sha256 `f09b40da13a95ab74e709b78d6575f68e0dff46ec634cc314de247c9b7792fe9` | 2026-10-29T20:58:43Z |
| F2 | **Root cause is a wave-1 gap in the rule's own evidence, and the seat that wrote the rule said so.** The rule (sha256 `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`, byte-identical to `w1/C1GapRule/gap-rule.json`) was derived from **two** carriers only. `w1/C1GapRule.md:66`: "Only c6430 and a7530 censused (task cap). a7590/c6490 unknown: … **any `b`/`p`/`s` row or a second device major:minor needs a rule edit before the freeze**." The carriers were swapped **after** that seat ran (a7530/a7590 → g7581/g7582), and no seat re-censused the new carriers' device set before the freeze. The rule's char-device tightening vs round-41 (`required` false→true, `allowed` []→["unpublished-entry"]) was validated only against carriers with a single device node. | `grep -n "second device major" -B2 -A2 .ufo/waves/round-50/w1/C1GapRule.md` ; `sha256sum tools/round-50/gap-rule.json .ufo/waves/round-50/w1/C1GapRule/gap-rule.json` ; `git log --oneline -- tools/round-50/gap-rule.json` (one commit: `435d41fd` FREEZE) | 0 | both sha256 `43f7c8d7…0fa0ef`; round-41 rule (`.ufo/waves/round-41/c1/gap-rule.json`) has `char-device: allowed [] / required false / silent {}` | 2026-10-29T20:58Z |
| F3 | **Counterfactual: either minimal rule edit makes all four carriers pass** — proving the defect is in the *rule*, not the counter and not the carriers. `CF-1` (`required[char-device]=false`, the round-41 shape) → g7581/g7582 `gaps_ok=True` ("637 gaps (1 structural), 3 removals, 0 silent, on 1001 non-regular entries"). `CF-2` (`silent[char-device]` extended with the 12 other `major:minor` details) → `gaps_ok=True` ("13 silent"). Both leave c6490/c6430 green. | `python3 - <<EOF` replay of the frozen `disposition_check` over three rule variants (script + full output: `…/ExecErrataSweep/counterfactual-gaprule.txt`) | 0 | see `counterfactual-gaprule.txt` | 2026-10-29T20:58Z |
| F4 | **The L1's own attempt-2 controls reproduce it.** CTL-C1-POS (`controls-attempt2/pos/receipt.json`) is `misbehaved`, why **"expected exit 0, got 1"**, `carriers_matched 2` / `target 4`, `failing: ["g7581:gaps_ok","g7582:gaps_ok"]`, and **every documentation binding is true** (`bindings_false: []`; `entry_present`, `sourced`, `coverage_map_row`, `province_core_row`, `frontier_note` all true). So the landing texts work; the carrier clauses do not. | `python3 -c "import json;print(json.load(open('.ufo/waves/round-50/controls-attempt2/pos/receipt.json'))['measured']['carriers_matched'])"` | 0 | receipt stdout sha256 `11956a04daf81bde2ddffe61ba8214fc917f084250ace63b265a3c2ae16516dc`; control utc `2026-10-29T20:43:19Z` | 2026-10-29T20:43:19Z |
| F5 | **The four attempt-1 "could_not_evaluate" controls are now `as_expected`** — the attempt-1 blockers were environmental, exactly as the attempt-2 plan predicted. Attempt-2 `controls-attempt2.json`: CTL-C1-0 `as_expected` (exit 1, matched 0), CTL-C1-1 `as_expected` (exit 1, matched 0), CTL-C1-2 `as_expected` (exit 1, matched 0, `projection_ok` fires on all four slots), CTL-C1-3 `as_expected` (exit 1, matched 0, slot `g7581` fails `chunks`+`hits`), CTL-C1-4 `as_expected` (exit 1, matched 2, slot `g7581` fails `layout_ok` **only** — the `slot_fails_exactly: ["marker"]` arm), CTL-C1-POS **`misbehaved`** (exit 1, matched 2). `kill_rule_fires` false — no control reached the target, so the kill rule does not fire. | `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/controls-attempt2.json'));print(json.dumps(d['controls'],indent=1))"` | 0 | per-control stdout sha256s: c0 `6d7f3834…82fc2`, c1 `5cc7b4f9…6c30b`, c2 `25f7b243…a92eb`, c3 `6372175a…6c96`, c4 `b04fe1c0…833c61`, pos `11956a04…16516dc`; wall_s 6.836 / 290.398 / 72.452 / 39.038 / 58.094 / 78.432 | 2026-10-29T20:43:19Z |
| F6 | **The attempt-1 report's control wording does not match its own receipts.** The fleet report line 14 and `corpus/lessons/round-50.md:47` and `LOG.md:3471` all say CTL-C1-2/-3/-4/POS were "`could_not_evaluate`". The receipts say `verdict: "misbehaved"` with `why: "counter reported could-not-evaluate (exit 2)"`; `summary.json` has `unevaluated: []` and `failures: [CTL-C1-2, CTL-C1-3, CTL-C1-4, CTL-C1-POS]`; `score.out.txt` **exit 1**. The driver only sets `status: could_not_evaluate` when the counter's receipt still carries `carriers` (so `rerun_errors` is derivable) — an exit-2 `rerun_env_error` receipt has no `carriers` key, so `summarize()` returns `present: False` and `c1-controls.py:1554-1567`'s dependent branch is unreachable. | `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/controls-attempt1/summary.json'));print(d['failures'],d['unevaluated'])"` ; `sed -n '1538,1570p' tools/round-50/c1-controls.py` | 0 | summary.json sha256 `45bfa9f29fa8fbb117156ee078a5fdf008b1446af93dd8106dc17b8207946348`; score.out.txt sha256 `b7e4249d86a37ff828d6d76102b7f9f743467775bffa019bbe1895d07e425b30` | 2026-10-29T02:27:03Z (attempt-1) |
| F7 | **The attempt-1 "six files over 1 MiB were skipped" note is misattributed.** All six are `a7530`/`a7590` — the two carriers **dropped** before the freeze. The frozen oracle dir holds only the four kept carriers (`c6430`, `c6490`, `g7581`, `g7582`; `git ls-tree -r --long HEAD -- tools/round-50/oracle/`), so "their content is the frozen oracle tables" is false. They are absent from disk **and** from git history (`git log --all --oneline -- <path>` → 0 commits each). For the four kept carriers the wave-1 census copies **are** committed and byte-identical to the frozen tables (`c6430.oracle.tsv` sha256 `f657ef513614824a9bfcf9f297bbe14482ac27a97dc6bb898481f2f1e49b5165` = frozen = wave-1). No wave-1 file over 1 MiB was committed (largest = 904 638 B). | `git ls-tree -r --long HEAD -- tools/round-50/oracle/` ; `git log --all --oneline -- .ufo/waves/round-50/w1/C1GapRule/census/a7530.lls` ; `sha256sum tools/round-50/oracle/c6430.oracle.tsv .ufo/waves/round-50/w1/C1GapRule/census/c6430.oracle.tsv` ; `git ls-tree -r --long HEAD -- .ufo/waves/round-50/w1/ \| awk '$4>1048576' \| wc -l` | 0 | 0 commits per skipped file; `f657ef51…b5165` (all three copies equal) | 2026-10-29T20:58Z |
| F8 | **The wave-3 dispatch spec predates the L1's two plan commits and is stale in two ways.** `w3-spec.json`/`w3-dispatch.json` were written 17:30:16; `6f4aba63` (entry-stem fix) landed 17:32:55 and `03f852b9` (C3 path move) 17:38:32. Six seat prompts still name the old stem `2026-10-29-r50-le-avm-hsqs-core` (ScribeEntryC1, ScribeRowsSources, ScribeProvinceBinding, ScribeReadmeMap, RevEntryBar, ConnCrossClaim) and three name the old C3 path `tools/round-50/sqfs-triage-v5.py` (ExecTriageV5, ExecRegistryRow, ConnCrossClaim). The built instrument still carries `INSTRUMENT_RELPATH = 'tools/round-50/sqfs-triage-v5.py'` (`w3/ExecTriageV5/tools/round-50/sqfs-triage-v5.py:256`, 88 704 B) and the registry-row draft's cell-0 is the old path. | `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/w3-spec.json'));[print(i['name'],i['prompt'].count('2026-10-29-r50-le-avm-hsqs-core'),i['prompt'].count('tools/round-50/sqfs-triage-v5.py')) for i in d['items'] if '2026-10-29-r50-le-avm-hsqs-core' in i['prompt'] or 'sqfs-triage-v5' in i['prompt']]"` ; `stat -c '%y %n' .ufo/waves/round-50/w3-spec.json` ; `git log -1 --format='%ci %s' 6f4aba63 03f852b9` | 0 | spec mtime `2026-10-29 17:30:16.748872284 -0300`; commits 17:32:55 / 17:38:32 | 2026-10-29T20:58Z |
| F9 | **`SKILL.md:1607`'s live-limits line still contradicts a C1 Core promotion** ("Big-endian and AVM SquashFS … are not claimed"), flagged by `w1/C1LandingMap.md` finding 14 as "annotate/supersede in the round-50 landing or the entry". It is **not** in the attempt-2 plan (`grep -ci "1601\|limits block" plans/round-50-attempt2-claims.md` → 0) and has no wave-3 owner. | `grep -n "Big-endian and AVM SquashFS" SKILL.md` ; `grep -n "1601-1602" .ufo/waves/round-50/w1/C1LandingMap.md` | 0 | `SKILL.md:1607` | 2026-10-29T20:58Z |
| F10 | **The attempt-1 report's "host load 95–176" has no receipt in the lane.** `grep -rn "load\|uptime\|nproc" .ufo/waves/round-50/controls-attempt1/` → 0 hits; the only load evidence is `l1/dev-arm-timeouts.txt` ("load average 42.5-54"). The figure appears only in prose (lesson `:47`, `LOG.md:3471`, the attempt-2 plan, the w3 spec). | `grep -rn "load\|uptime\|nproc" .ufo/waves/round-50/controls-attempt1/` | 1 (no match) | only evidence: `l1/dev-arm-timeouts.txt:3` | 2026-10-29T20:58Z |
| F11 | **SHONEN is not "unchecked" — the fleet report misstates the file.** `SHONEN.md:5,8,11,14` carry `- [~]` (all four); the report prints them as `- [ ]`. Attempt-1 did not regress them and attempt-2 cannot promote them (the lane's own rule needs a non-author verifier). | `grep -n "^- \[" SHONEN.md` ; `grep -n "^- \[" /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kaidoku.md` | 0 | 4×`- [~]` vs 4×`- [ ]` | 2026-10-29T20:58Z |
| F12 | **Frozen bytes are intact and the L1's C3 path rule is measured, not assumed.** `git diff --stat 435d41fd…HEAD -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` → empty (exit 0). I independently reproduced the L1's path measurement on a scratch clone of `f890bbea`: adding `tools/round-50/sqfs-triage-v5.py` after the freeze → `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` (C1 would exit 2); adding `tools/round-50-c3/sqfs-triage-v5.py` → `frozen_drift = []` (green). | `git diff --stat 435d41fd…HEAD -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` ; scratch clone `git clone --shared <lane> "$S/clone" && git -C "$S/clone" checkout --detach f890bbea…` then the two probe commits + the frozen counter's own `frozen_drift()` | 0 (diff empty); 0 (drift empty at the c3 path) | drift probe rev `4cc6ccac75dfb6b1b5a3bf8b5a17dfa8d6c0a9b5` | 2026-10-29T20:58Z |

---

## Carry-over verdict table (summary; full detail in `carry-over.md` §A)

| attempt-1 not-landed item | addressed by attempt-2? | owner |
|---|---|---|
| C1 knowledge entry | **YES** (stem corrected at `6f4aba63`) | `ScribeEntryC1` → L1 step 3 |
| PROVINCE `## Round-50 additions to Core` + frontier note | **YES** | `ScribeProvinceBinding` → L1 step 3 |
| corpus/README.md coverage-map row | **YES** | `ScribeReadmeMap` → L1 step 3 |
| SCORECARD capability row + Owned-axes `140/140` | **YES** | `ScribeCapabilityRow` + `ExecB1Impact`/`CritB1Text` → L1 step 3 |
| SKILL.md bindings | **RE-SCOPED** — C1 binds no SKILL path; the 12 registry rows already landed at `11ccdb72`; the stale `SKILL.md:1607` limits line is **unowned** (F9) | L1 |
| SOURCES rows S243/S244/S245/S249 | **YES** — ids are free in the live registry; the plan's "staged S206 re-grounded as S243" is the **same source** (Freetz patch 101, identical URL) re-numbered, so no id collision — but the staged row's **tier A** vs the planned **tier B** must be settled explicitly | `ScribeRowsSources` + 4 `SrcReopen*` + `CritSourcingRules` → L1 step 3 |
| SHONEN promotion | **NO** — and the attempt-1 report misstated the file (F11) | nobody (correctly: promotion needs a non-author verifier) |
| wave-2 seats (37, never dispatched, specs unrecoverable) | **YES, replaced** — w3 = 35 seats (attack roles 11/35 = 31.4% ≥ 25%) + w4 planned | wave shape |
| QUALITY row 94 dropped | **NO** — draft + probe committed and green; one append away; `corpus/QUALITY.md` still ends at 93 | nobody |
| six wave-1 >1 MiB receipt files | **NO** — and the attempt-1 rationale is wrong (F7); the loss is dropped-carrier detail, which the claim does not need | nobody |
| *(new)* frozen `gap-rule.json` blocks the C1 target | **NO** — not in the plan (F1–F4) | **L1 decision** |

## Controls table (attempt 1 → attempt 2)

| control | attempt-1 verdict (receipt) | attempt-1 error text | attempt-2 verdict | attempt-2 note |
|---|---|---|---|---|
| CTL-C1-0 | `as_expected` (exit 1, matched 0) | — | `as_expected` | — |
| CTL-C1-1 | `as_expected` (exit 1, matched 0) | — | `as_expected` | — |
| CTL-C1-2 | `misbehaved` (exit 2) | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | `as_expected` (exit 1, matched 0) | `projection_ok` fires on all four slots |
| CTL-C1-3 | `misbehaved` (exit 2) | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | `as_expected` (exit 1, matched 0) | slot `g7581` fails `chunks`+`hits` |
| CTL-C1-4 | `misbehaved` (exit 2) | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | `as_expected` (exit 1, matched 2) | slot `g7581` fails `layout_ok` only |
| CTL-C1-POS | `misbehaved` (exit 2) | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | **`misbehaved`** (exit 1, matched 2) | `g7581:gaps_ok`, `g7582:gaps_ok` — F1 |

Attempt-1 `kill_rule_fires` false and attempt-2 `kill_rule_fires` false: no control reached
`carriers_matched == 4` with every binding true, and the do-nothing tree's
`receipt_clauses_green` was `{}` — the kill rule did not fire in either attempt.

## What the L1 must decide (F1–F4)

The C1 target of 4 carriers is **unreachable** with the frozen bytes: `tools/round-50/` is
byte-frozen, and `tools/round-50/gap-rule.json` cannot admit g7581/g7582's 12 extra
char-device nodes. The plan's own discipline (`plans/round-50-claims.md` header: "a counter
bug found after the freeze is reported as a miss, never patched") makes this a **reported
miss**, not a silent patch — but this is a *rule* defect, and the plan's "Frontier step"
allows a new freeze. Two minimal, evidence-backed rule edits both make all four carriers
pass (F3). The L1's options, in order of fidelity to the frozen discipline:

1. **Report C1 as a miss** and land the documentation bindings + entry as *Frontier*-level
   (not Core) — the claim's own disclosure (5) says the carriers are four of 28 census rows,
   and the honest reading of the four carriers is "two of four verified".
2. **New freeze** (never an amendment) with the corrected `gap-rule.json` — either
   `required["char-device"]=false` (the round-41 shape, CF-1) or `silent["char-device"]`
   extended with the 12 other `major:minor` details (CF-2) — and re-run the controls +
   data run under it. This restores the target of 4 and is what the wave-1 seat's own note
   required ("a second device major:minor needs a rule edit before the freeze").
3. Do **not** patch the frozen rule in place: that would make `frozen_path_changed`
   non-empty and turn every C1 measurement into exit 2.

Either way the L1 must land the entry/PROVINCE/README/SOURCES rows (their bindings are all
**true** in the attempt-2 POS run) and must **not** claim `carriers_matched 4` without a
measurement that shows it.

## Risk notes for the integration

- **Do not integrate the C3 instrument at `tools/round-50/sqfs-triage-v5.py`.** That path is
  inside the frozen prefix; I measured `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']`
  on a scratch clone — C1 would exit 2 at every later REV. The L1's `03f852b9` moved the plan
  to `tools/round-50-c3/`; the built instrument and the registry-row draft still carry the old
  path (F8). Also note `tools/round-50-c3/` is outside B9's census prefix
  (`CENSUS_REV_PREFIX = 'tools/round-50'`), so B9 needs no row for it — but the lane's
  registry discipline (row 92) still wants one, and the L1's plan says so.
- **Do not integrate any draft that names the old entry stem.** The counter reads the stem
  from `tools/round-50/c1-counter.py:377-378`; the six stale prompts (F8) put the old stem
  in front of five seats.
- **Re-read `ScribeLogDraft/log.md`** — line 17 still names the old stem
  `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md`; the other drafts (entry, rows,
  province, readme) already use the frozen stem.
- The **S243 tier** (F-table row "SOURCES rows") needs an explicit L1 decision before the
  rows land: the staged row for the same source (Freetz patch 101) carries tier **A**, the
  planned row carries tier **B**.

## Verification and honesty notes

- **The lane tip moved twice under this seat** (`6f4aba63` 17:32:55, `03f852b9` 17:38:32,
  `d71829bf` 17:54:57 — the last one adds the C3 pre-freeze amendments from the wave-3
  attacks). I re-verified at the newest tip: the frozen bytes are still unchanged
  (`git diff --stat 435d41fd…d71829bf -- tools/round-50/ plans/round-50-claims.md
  tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` → empty, exit 0) and the
  gap-rule defect **still reproduces** (`repro_gaps_ok.py` re-run at `d71829bf` → exit 0,
  `defect_reproduced: true`, same four-carrier verdict). None of the three commits touches
  `tools/round-50/gap-rule.json`, so F1–F4 stand as written.
- **`tools/round-50-c3/sqfs-triage-v5.py` currently holds a 49-byte stub** ("# simulated C3
  instrument") — the real 88 704 B build is still in the seat dir at
  `.ufo/waves/round-50/w3/ExecTriageV5/tools/round-50/sqfs-triage-v5.py` with the old
  `INSTRUMENT_RELPATH`. The L1 must land the real file at the `tools/round-50-c3/` path the
  plan now names (F8).

- Everything marked "measured" above was run by this seat and carries its command, exit code
  and sha256. The gap-rule reproduction and the two counterfactuals were run by this seat.
- The attempt-2 control receipts and the live `corpus/evidence/round-50/c1/**` receipts were
  read, **not** re-run: they are the L1's own artifacts, written 17:34–17:52 local.
- The wave-3 spec/dispatch files, `controls-attempt2*`, `l1/scores/c1-before-attempt2.json`
  and `corpus/evidence/round-50/c1/**` are **untracked** in the lane at the time of this
  report (`git status --porcelain`); the L1 owns them.
- **No REA run was performed by this seat** (contract). No git mutation was performed in the
  lane or the fleet repo; the only git writes were to a throwaway clone under
  `/fast/scratch/hyaku/kaidoku-r50/w3-ExecErrataSweep/` (created with
  `git clone --shared`, `git -C "$D" rev-parse --show-toplevel` asserted before its two
  probe commits).
- **Tool installs: none.** Host changes: none. Nothing outside this seat's directory
  (`.ufo/waves/round-50/w3/ExecErrataSweep{,.md}`) was written.
- Claims I could not verify and therefore did not assert: whether the L1 intends a new
  freeze (option 2 above) — that is an operator/L1 decision; whether the 13k-file carriers
  would have passed the same rule (they were dropped pre-freeze and are not in the frozen
  oracle set, so it cannot be checked from the lane); whether the tier-B choice for S243 is
  the one the closure wants (a curation judgment the lane reserves for the author/closure).
- **Correction made during this seat:** my first draft of the carry-over table reported an
  "S243 id collision" between the plan's "staged S206 re-grounded as S243" and the planned
  S243 row. That was wrong and is corrected above: the staged `S206`
  (`/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md:107`) is the **same
  source** as the planned S243 (identical URL, Freetz patch 101), so the re-grounding is
  consistent. The real open item is the **tier** (staged `A` vs planned `B`), which is what
  the row now flags.
