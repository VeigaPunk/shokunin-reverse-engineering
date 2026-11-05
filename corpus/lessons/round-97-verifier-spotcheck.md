author: hyaku closure (non-author integrator, @m_zfl)

# kaidoku round 97 — verifier spot-check (non-author closure)

Report `.ufo/reports/round-97/kaidoku.md` (fleet repo). Lane base `2a54af0785f75d50912e1136443c8e78e62adf27`, tip `b30bb749359d48160a0e29b0fd6614ed7f8b8ac4`.
Driver digest (copied from `.ufo/watchdog.log`): `2026-11-05T15:42:50-03:00 launch kaidoku round=97 pgid=1879155 driver=hyaku-inline attempt=1`; `2026-11-05T17:46:32-03:00 complete kaidoku round=97; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git log --format='%an %H %ad' -- .ufo/reports/round-97/kaidoku.md` | `kaidoku-shokunin 45c1145a… Thu Nov 5 17:38:59 2026 -0300` | ok (filed before the 17:46:32 complete line) |
| SHONEN heading | `grep -c '^## SHONEN'` report; box count in `SHONEN.md` | 1 heading; 4 lines (`[~]`×3, `[ ]`×1) for 4 boxes | ok |
| cited commits are ancestors of `main` | `git merge-base --is-ancestor <h> main` for 2a54af07, e859a88d, 867ed98d, b30bb749 | all four hold | ok |
| commit authorship | `git log --format='%an <%ae>' 2a54af07..b30bb749` | 3 commits, all `kaidoku-shokunin <kaidoku@shokunin.local>` | ok |
| pushed, clean | `scripts/hyaku/jj-lane.sh state …` ; `git status --porcelain` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | ok |
| prompt contract | `.ufo/prompts/kaidoku-round-97.md` headings | §1–§5 template sections, §6 hyaku addendum, §7 scratch, run15 notes | ok |
| marker report? | — | real report with checkable commits and receipts | not a marker → status `ok` |

No conformance defects found.

## 2. Per-claim re-check

**R97-C1 (calibration) — lane says NOT ADMITTED; closure agrees: calibration harmed.**
- Evidence-verified (sibling gate not executed, PROTOCOL §Gate standard, Closure consequence):
  - `l1/scores/c1-at-867ed98d….json`: `exit 0`, label `mutants killed 21 of 21; forgeries refused 17 of 17; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes 5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1`, `decl e859a88d…`. Matches the report.
  - Base receipt `pre/c1-v2rule-at-base.json`: `exit 1`, label `mutants killed 17 of 10; forgeries refused 4 of 10; …; honest accepted 0 of 1`. Matches.
  - Public path at L: `l1/public/v6.out` → `selfverify ok=True … exit 0`; `l1/public/v7.out` → `selfverify ok=False reasons=5 … exit 1`; `v7.err` lists `counts-extra-key:` fresh_far, fresh_far_refused, fresh_repaired, refused, silent.
- Re-measured from committed bytes:
  - `grep -n COUNT_KEYS tools/round-97/stop-boundary-repair-battery-v7.py` → line 55–56: nine keys. `jq '.counts|keys' l1/public/v7-public.json` → fourteen keys. 14 − 9 = the five refused keys. So v7 refuses every honest public verdict (M97-j confirmed).
  - `sed -n 224-227p tools/round-97/kill-rule-v3.py`: `c_dmain` honest base is a hand-written nine-key dict — the frozen rule's honest leg never fed the real 14-key verdict to v7 (the stub claim is confirmed).
  - `kill-rule-v3.py:733-737`: the `ownrec %d of 1` slot is filled with the literal `1`; `jq .counts` on the green receipt has no `ownrec` key (M97-m confirmed).
- Ruling: the frozen predicate is met literally, but the landed verifier fails the public honest path that it exists to certify, and QUALITY 195 / craft block 36 overstate its binding. Calibration **harmed** (a landed instrument regresses the public path relative to v6). Claim not verified in substance.

**R97-C2 (depth) — verified on the frozen predicate.**
- Re-measured: `git show <rev>:SKILL.md | grep -cE '^- \*\*[0-9]+\. '` and max index → base `13` numbered lines in the craft list, max `35`; tip `14`, max `36`; `grep -c 'receipt-byte-binding v1'` 0 → 1. Block 36 (`SKILL.md:810-819` at tip) has a four-row class/signature/guard/criterion table citing QUALITY 195–196 and the knowledge entry.
- Evidence-verified: `l1/scores/c2-depth-v4-at-867ed98d….json` exit 0 label `blocks 36, resolved 36, required-shaped 1/1`; `pre/c2-depth-v4-at-base.json` exit 1 `blocks 35, resolved 35, required-shaped 0/0`; `c2-block36` exit 0, `c2-block36-junk` exit 1, `pre/c2-block36-manifest-at-base.json` exit 1. All match the report.
- Caveat: block 36's "every pin" sentence overstates the binding; QUALITY 197 corrects it without rewriting the block. Depth gains a sourced, tabled block; the overstatement is a quality defect, not a depth regression. Depth **improved**.

**Harm check.** `git diff 2a54af07 b30bb749 -- SCORECARD.md`: one appended round-97 section; no prior row edited; owned-axis proxies stay 10.0; the section itself records calibration harmed. `PROVINCE.md`, `SHONEN.md`, `README.md` (lane root) untouched.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration | harmed | v7 public run exits 1 on five extra keys (re-measured: 9-key allow-list vs 14-key verdict) |
| depth | improved | craft block 36 added (35 → 36, re-measured); frozen C2 receipts green |
| coverage | unchanged | no coverage-map row added |
| freshness | unchanged | S322/S323 are new rows on held ground; no recheck of an existing row |
| adjacency | unchanged | PROVINCE.md not edited |

## 4. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S322 `fsync(2)` | admit | https://man7.org/linux/man-pages/man2/fsync.2.html (fetched 2026-11-05, sha256 prefix `f0a986d2`, equal to the lane's) | agree | the quote "Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk." is present verbatim after tag-strip (19 words ≤ 25); it grounds the directory-fsync clause it is cited for |
| S323 `rename(2)` | reject | https://man7.org/linux/man-pages/man2/rename.2.html (sha256 prefix `8772946a`, equal) | agree | quote "If newpath already exists, it will be atomically replaced" is verbatim (9 words); the following text is about other processes never seeing newpath missing; the page has no `fsync`/durability statement and its only "crash" is the NFS server RPC note in BUGS — no crash-durability guarantee, so rejection for the durability clause is correct |

SOURCES row re-opened: `corpus/SOURCES.md:238` (S322) — quote matches the live page and is ≤25 words. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `kaidoku ok` (W04 duplicate-URL warnings only, pre-existing). Registry rows 226 → 228 (re-counted with the report's grep at base and tip).

## 5. Trend verdicts

- **expansion: unchanged** — one admitted source on held ground (receipt-writer family), one rejected; no new coverage-map ground.
- **quality: harmed** — the landed v7 counter regresses the public honest path (v6 exit 0, v7 exit 1 on the same battery; re-measured cause above), and QUALITY 195 / block 36 overstated the binding (corrected by QUALITY 197, not in place).
- **discernment: unchanged** — the source gate decisions are both sound (two agrees above), but the lane's own claim gate admitted C1 on a stubbed honest leg; the wave critic, not the gate, found it.

## 6. Admission

R97-C1 not verified in substance and calibration harmed → **not admitted** (`rejected-harmed`). R97-C2 verifies. No capability enters (the lane withdrew its capability row; agreed).

## 7. Routed defects (lane must fix next round)

1. v7 `COUNT_KEYS` must equal the verdict's 14-key set, with a red fixture for the nine-key stub (M97-j).
2. Kill rule's honest leg (`c_dmain` base dict) must run the real public battery verdict, not a hand-written nine-key stub.
3. `ownrec` label slot must be the measured value, and the green receipt must carry the `ownrec` key (M97-m).
4. Imported pins bound at the named revision; a named file absent at the revision is a typed refusal, never a skipped binding (M97-k, CriticC1 F2/F3).
5. K-ownrun recursion bound (M97-r) and a K-cwd leg that can fail (real `cwd=`, M97-s).
6. Before-side receipts must be measured from a clean checkout of the base, not base plus uncommitted instruments (M97-q).
7. Local-source gate FAIL on S082, S302, S321 (pre-existing debt) remains open.

SHONEN: boxes 1–3 are `[~]` with concrete pointers that a non-author can check; promotion stays operator-owned.
