# ExecTriageControls — R50-C3 control fixtures, round 50 attempt 2, wave 3

**Verdict: the four C3 control fixtures, the envelope manifest and the receipts are built and
ready for the L1's post-freeze scoring — but no control was scored, because the C3 instrument
does not exist yet (it is not written by this seat and this wave must not write it). Every
`expected-red` number here is a *prediction* computed offline from committed lane bytes; the
table side is measured, the evaluator side is a reconstruction of the attempt-2 claim text.**

Seat artefacts: `.ufo/waves/round-50/w3/ExecTriageControls/` (README, manifest, four control
documents in two surface variants each, four `expected-red.json`, `receipts.tsv`/`receipts.json`,
`commands.sh`, the generator `build_controls.py` and the decision dumper `analyze.py`).
Lane base `f890bbead20ca2c549487167f56876ae47f1e1a4`. No REA run, no network, no write outside the
seat directory, no tool installed.

## Findings

| # | finding | evidence (exact command → exit, sha256) |
|---|---|---|
| F1 | The held-out dir holds **126** envelopes, **committed at base**; the four v2ns `_ddefault` files are named exactly and are committed blobs | `git -C <lane> ls-tree -r --name-only f890bbea… -- .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes` → exit 0, stdout sha256 `6a6cb63ccbaa9fc7…` (13802 B); `git ls-tree -r f890bbea… -- <envdir>` → exit 0, stdout sha256 `608c23b85e0acf00…` (20480 B); `find <envdir> -mindepth 1 -maxdepth 1 -type d` → exit 0 (R02/R04/R08) |
| F2 | `ctl-do-nothing` is the v4 table at base **extracted, not hand-copied**: the assembled document is **byte-identical to base `SKILL.md`** | `git show f890bbea…:SKILL.md` → exit 0, stdout sha256 `19046cf204ce999e…` (316807 B) = sha256 of `ctl-do-nothing.skill.md` (R01/R06); extracted block sha256 `99cd54d7fe884748…` (`v4-table-at-base.md`) |
| F3 | The base table's `clean` row decides **51** envelopes; **19** of them are no-reader-family `_ddefault` runs (v2ns 4, v3_broadcom 7, v3_nonstandard 8) with no gap and >0 files → the v5 evaluator's `clean-unverified`/`record-unverified`. **The base mismatch count is 19, not 4** — the claim's predicate names only the four v2ns rows ("among the mismatches"), so the predicate holds, but the instrument's base number is 19 under the claim's own three-family text | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill <base SKILL.md> --json <126 envelopes>` → exit 0, stdout sha256 `dbc134658d5a9054…` (225292 B) (R03); per-envelope tuples in `envelopes-manifest.json` |
| F4 | **The corpus cannot witness F1** (the `squashfs_v[123]*` over-match): all **7** envelopes the `legacy-body-failure` row decides are reader-backed (`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`), so no no-reader envelope ever reaches that row. **It cannot witness the second new label either**: no no-reader envelope among the 126 carries an `extractor-failure` gap, so `no-reader-failure`/`preserve-unresolved` has zero members here. Both must be justified by the rule text + the reader census, and only the instrument's own mutation battery can witness them | same R03 run: 7 envelopes with `v4_label_at_base = legacy-body-failure`, families as listed; no-reader `_ddefault` tuples all have `G = []`, `P > 0` (manifest) |
| F5 | **The junk control is a parse refusal, not a comparison.** All 15 rows labelled `clean` trip the v4 parser's duplicate-label check: `sqfs-triage-v4: line 531: duplicate label 'clean' (first on line 530)`, exit **2**, stdout empty (`e3b0c44298fc1c14…`) | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill ctl-junk.skill.md --table-only` → exit 2 (R11-ctl-junk); `--json` run also exit 2 (R10-ctl-junk). Its table side was therefore computed by substituting the label of the row the base table matched (first-match order and every other cell unchanged) → 94 pair mismatches |
| F6 | **The v5 instrument needs a `--skill`-style argument.** The claim's predicate command line (`--root --rev --freeze --envelopes --json-out`) names no document to score, yet the controls must be scored *before* the v5 table lands; without such an argument the mutants could only be scored by committing them into `SKILL.md`, which breaks the freeze ordering | `commands.sh` §4 (the post-freeze invocation), README §"Instrument requirements" 1 |
| F7 | **The live-table marker check must accept a v4 table.** The landed `SKILL.md` will carry the v4 table as history (rule block 21) *and* the v5 table (block 22); the instrument must prefer v5 when both are present and must still score a v4-only document — that document is `ctl-do-nothing`. Likewise the vocabulary check must be membership, not equality (the v5 vocabulary is a superset of the v4 one) | README "Instrument requirements" 2–3; `.skill.v5surface.md` variants differ from `.skill.md` on exactly 2 lines (marker + vocabulary), receipt R07 |
| F8 | **`ctl-action-swapped` is red only if the instrument compares (label, action) pairs**: 32 of its 51 mismatches are action-only (label `clean` matches, action `inspect-input` ≠ `none`). A label-only comparison would report the same 19 as the do-nothing control | R10-ctl-action-swapped: exit 0, stdout sha256 `63cba22de8baad49…` (226259 B); `ctl-action-swapped.expected-red.json`: 51 pairs / 19 labels / 51 actions |
| F9 | The **no-reader family set is a fork the L1 must pin**: the claim names three families, but the round-49 census gives `v3_broadcom` a *partial* reader (7-Zip lists the committed LE broadcom fixture, unsquashfs refuses it). Expected base mismatch counts: **19** (claim's three) / **12** (census two) / **4** (v2ns only); all three keep the four v2ns `_ddefault` rows among the mismatches | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` "What stays Frontier"; `.ufo/waves/round-49/w2/W2Skill.md` F1/F9; `family_set_readings` in every `expected-red.json` |
| F10 | The three control documents are exact, single-intent mutations of the base table: `ctl-guard-deleted` has 14 rows (the `legacy-body-failure` row removed), `ctl-junk` has 15 rows all labelled `clean`, `ctl-action-swapped` has 15 rows with the `clean` row's action `inspect-input` | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill ctl-<X>.skill.md --table-only` → exit 0 for the three (stdout sha256 `e3b0c44298fc1c14…` = empty stdout, rules printed on stderr) and exit 2 for the junk table (R11-*) |
| F11 | **"Rule block 22" is already taken — the landing order must not renumber.** The craft section holds **25** rule blocks at the tip (the split `tools/round-46/attest.py:craft_blocks` uses): block 21 is the v4 triage table (the claim's "rule block 21"), block 22 is the freeze-integrity table, and blocks 23/24/25 carry the explicit titles `23. `, `24. `, `25. ` that three frozen counters assert. Landing the v5 table as a *numbered* block 22 therefore either collides with the freeze block or forces blocks 22–25 → 23–26, which breaks `tools/round-46/attest.py` (asserts the title `23. `), `tools/round-47/exact.py` (`24. `) and `tools/round-48/meanings.py` (`25. `) at the new tip. **Safe landing:** insert the v5 table as an unnumbered bullet right after the v4 bullet (blocks 1–21 are unnumbered) and leave 22–25 untouched; the instrument then finds the v5 table by marker, not by block number | craft-block census receipt `receipts-craft-blocks.txt` (stdout sha256 `41ff99bd5ae8f18d…`, 1958 B, 25 blocks); title assertions at `tools/round-46/attest.py:196`, `tools/round-47/exact.py:196`, `tools/round-48/meanings.py:339`; `tools/round-45/c1-counter.py:163` asserts `rule_blocks == 22` — already false at the tip (25), and unchanged by one more bullet (26) |
| F12 | The lane tip moved once during this wave (`6f4aba63`, "attempt-2 claims corrected — entry stem pinned to the frozen counter constants"); **`SKILL.md` and the 126 envelopes are byte-unchanged** and the correction touches only the C1 entry stem, so every expectation here still holds | `git diff --stat f890bbea… HEAD -- SKILL.md` → empty; `git diff --name-only f890bbea… HEAD` → `plans/round-50-attempt2-claims.md` only |

## Expected reds (predictions — the L1 scores them post-freeze)

| control | clause guarded | expected exit | expected pair mismatches (claim's three-family reading) |
|---|---|---|---|
| `ctl-do-nothing` | "do-nothing (v4 table at base → red)" | 1 | 19 (19 label / 19 action) |
| `ctl-junk` | "junk table (every row `clean` → red)" | 1 (exit 2 if the duplicate-label check stays) | 94 (94 label / 19 action) |
| `ctl-guard-deleted` | "guard-row-deleted mutant → red" | 1 | 26 (19 inherited + 7 the guard row decided) |
| `ctl-action-swapped` | "swapped-action mutant → red" | 1 | 51 (19 label / 51 action) |

Envelope lists, the family-set readings and the caveats are in
`.ufo/waves/round-50/w3/ExecTriageControls/ctl-<X>.expected-red.json`.

## Risks and blockers

- **Risk (instrument):** if the v5 instrument refuses a v4-marked document or compares labels
  only, `ctl-do-nothing` and `ctl-action-swapped` lose their intended reds (F6–F8). This is a
  pre-freeze design requirement, not a post-freeze surprise.
- **Risk (grammar):** the junk control needs the duplicate-label check dropped to be a mismatch
  red; otherwise its red is a refusal, which proves less (F5).
- **Limit (evidence):** the evaluator side of every expected red is a reconstruction of the
  attempt-2 claim text, not a run of the frozen instrument; the L1's base number must equal the
  reading its instrument implements (F3, F9).
- **Limit (corpus):** the held-out dir is the round-42 recon corpus (126 envelopes, committed
  since round 42; v4 scored 78 of them at R43-C1). It witnesses F2 only — F1 and the
  `no-reader-failure` half have no member in it (F4).
- **Blocker:** none for this seat. Nothing here requires the instrument to exist; the L1 freezes
  it and runs `commands.sh` §4.
