# Round 43 non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

## Conformance

- Report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kaidoku.md` landed by lane identity `kaidoku-shokunin` in fleet commit `d07f60c9419bbc6eeaf1330faf9c8f3ddae8e248`; SHONEN has four `[~]` assessment lines. Report cites final lane HEAD `dadb1ef1e3262d687d08496759b50e97b2a5b2fe`; `git merge-base --is-ancestor dadb1ef1e3262d687d08496759b50e97b2a5b2fe refs/heads/main` exited 0. Helper state: `ahead=0 behind=0 head=detached tracked=0 untracked=0`; lane `git status --porcelain` empty. Report says remote branch equalled HEAD.
- Prompt contains mission/axes binding, claims, frontier duties, report contract, commit/push scope and L0 side channel. It does not visibly include the verbatim L2 minimum or all required round-level and child-lane clauses; record this as a status-neutral prompt-fidelity defect. Report omits old-row touch/frontier advancement details and substantive trend evidence; status-neutral.
- Dispatch digest copied from watchdog log: `2026-10-27T04:55:20-03:00 launch kaidoku round=43 pgid=3053828 driver=hyaku-inline attempt=1`; `2026-10-27T06:04:03-03:00 lane-dead-no-report kaidoku round=43; retry same round (hyaku-inline attempt=1: L1 died: provider fallback exhausted (gpt-6-luna invalid_prompt))`; `2026-10-27T06:04:06-03:00 launch kaidoku round=43 pgid=58948 driver=hyaku-inline attempt=2`; `2026-10-27T09:15:28-03:00 complete kaidoku round=43; hyaku-inline attempt=2`.
- Required census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → `kaidoku ok`; 13 W04 duplicate-URL warnings. Not a marker: report contains actual committed work, measurements, evidence and SHONEN.

## Claim re-checks and axes

| claim | independent check and observed result | axis verdict |
|---|---|---|
| R43-C1 calibration | `git show dadb1ef1:.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json \| jq '{matched,n,bindings_ok}'` → `78,78,true`; receipt has `bindings_false=[]`, `observed_features_match_declared=true`, and tuple-check evidence. Receipt is evidence-verified, not newly executed; measured revision is ancestor of final HEAD. Confirms frozen finite predicate, not independent source authenticity (W2 reported provenance/path-ID weaknesses). | improved (bounded frozen calibration predicate) |
| R43-C2 coverage | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show --numstat 6b9e64fe..dadb1ef1 -- corpus/SOURCES.md` → `4 0 corpus/SOURCES.md`; committed score receipt jq → `rows_checked=19`, `rows_total=137`, `rows_failed=[]`. Frozen scorer stops because expected 3 additions but observed 4; gate/copy audit does not override frozen predicate. | unchanged (claim not met; no measured axis harm) |

Axis verdicts: coverage **unchanged** (claim not met; map proxy does not satisfy it); calibration **improved** within bounded receipt; depth **unchanged** (no depth claim). No axis evidenced harmed. Since C2 does not verify, reject-honest-stop.

## Learning trends

- Expansion: improved — new admitted sasquatch release-matrix entry on uncovered packaging-inventory frontier, citing mined S136/S137.
- Quality: improved — entry scopes the evidence and records mutable-response limits; re-opened projection confirms release/asset counts. C1 remains bounded by provenance limitations.
- Discernment: improved — sampled admit and reject agree with reopened evidence; new-source quote is located and within 25 words. Lesson's assertion that the non-author closure is in the report was premature; this artifact supplies that check.

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| sasquatch release-matrix entry | admit | `curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases \| jq -r '.[].tag_name'` returned 8 tags, v4.5.1-6 through v1.0; projection `jq -c '[length,(map(.assets\|length)),(map([.assets[]\|select(.digest)]\|length))]'` | agree | Confirms 8 releases and the inventory premise; rendered releases page does not provide the asset list. |
| sasquatch-unblob-compatibility candidate | reject | `corpus/lessons/round-42.md` Gate rejection cited in r43 lesson; r43 admitted entry lines 82–86 expressly excludes compatibility claim | agree | Packaging inventory does not establish package/unblob behavior; prior rejection remains warranted. |
| New row S136 quote | source used by admitted entry | API above; `corpus/SOURCES.md:142`, `corpus/lessons/round-43.md:18` | agree | Quote `sasquatch-v4.5.1-6` is 1 word at JSON `$.tag_name`, within 25-word limit; current endpoint returns it. |

## Routed defects

- Kaidoku next round: C2 scorer/plan mismatch (3 planned rows vs raw 4/0 diff; M43-2); preserve honest stop and derive future predicate from exact append block.
- Kaidoku next round: W2 found C1 source/provenance and manifest-ID/path weaknesses, plus C2 parent-symlink and escaping-copy-path weaknesses; carry instrument limitations explicitly.
- Operator/integrator: dispatched prompt omits canonical full contract clauses; fix generated prompt template outside lane ownership.
- Status-neutral report conformance debt: include SOURCES old-row changes/frontier advancement details when applicable.
