# SC-3 — seat report (chain c3, role scribe)

Wave `arc3-loop1-round4` · lane: declared fallback on the devin lane (recorded in
the freeze; not a lane signal) · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · no git mutations · custody
paths read-only (hash/stat and the tool's own read-only captures only; every
demo ran on scratch copies) · scratch `/var/tmp/sc3-r4`, never `/tmp`.

Task (seat line): "injection ledger + records drafts for the parent (PIN-FREE).
`claims/c3/records-drafts/` and `claims/c3/SC-3/ledger.md`."

**Verdict: delivered.** The ledger carries the four residuals × before × after ×
declared class, with every cell measured first-hand on both revisions (base
`7cd19c3c…`; landing `29bb45ae…`, caught in flight by a 15 s watcher), plus a
compound finding that two of the four debts are one decision. Both records
drafts are written and pin-free-measured. Nothing in this seat's tree contradicts
any peer's measurement; the two peer contradictions found were resolved as
revision-order, not substance (see §4).

## 1. Work performed (evidence pointers)

All paths under `claims/c3/SC-3/` unless noted.

| # | work | evidence |
|---|---|---|
| 1 | **Identity + method record** (rule #14): base tool `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 L), base README `f30df42e…` (185 L); landing tool `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 L), landing README `125e7e02…` (267 L, moved again to `9d9400da…`/272 L after my citation — re-derived below); scratch copy of each, sha re-derived at copy and at close | `evidence/identity.txt` (+`IDENTITY.sha256`), `evidence/after/tool-29bb45ae.py`, watcher `/var/tmp/sc3-r4/watch/watch.log` (15 s samples from 14:05:44Z; caught the landing transition at 14:09:30Z) |
| 2 | **Before-state harness** (8 legs + controls): `harness/injections.sh` on the base copy — a1 (both sidecar spellings), b1/b2 (mkdir / `--out ''`), c0–c7 (padded v2, sums, pipe, distinct controls, 1-of-5), d1–d3 (ghost), k1/k2 (selftest, paths); second driver for the guard controls and the compound case | `evidence/before/summary.txt` + 30 per-leg `.out`/`.rc`, `evidence/before/controls-summary.txt` (g1/g2, i1–i9), `evidence/before/SHA256SUMS` (55 entries, `sha256sum -c` all OK) |
| 3 | **After-state, same harness, on the landing** (no leg changed between runs — the base and after transcripts are directly comparable) | `evidence/after/summary.txt` + 30 per-leg `.out`/`.rc`, `evidence/after/controls-summary.txt`, `evidence/after/SHA256SUMS` (54 entries, all OK) |
| 4 | **Landing-arrival discipline**: watcher caught `29bb45ae…` at 14:09:30Z; copy re-derived 3× identical; README churn inside the window (`f30df42e…` → `91fd386b…` → `125e7e02…` → `9d9400da…`) recorded rather than smoothed | `watch.log`, §3 below |
| 5 | **Cross-seat corroboration folded into the ledger** (not trusted from prose): EX-23's sidecar probe (before + scratch-variant), EX-24's 13-leg matrix (before/after/sabotage/fixture-rev), RV-7's diagonal mutation matrix, RV-8's independent before-state, CU-1's attack battery and custody recompute | ledger §"cross-corroboration" column; each pointer named by file |
| 6 | **Records drafts** (the seat's second deliverable): a LOG entry and a SCORECARD section, both PIN-FREE, with the C3 bullet/row/learning/carried-debt complete and the C1/C2 slots left to the parent | `claims/c3/records-drafts/LOG-entry-draft.md`, `claims/c3/records-drafts/scorecard-section-draft.md` |
| 7 | **Pin-free simulation** (the drafts' own gate): census projection over base/records/control scratch trees, plus CN-2's token checker; re-run after the section was revised with after-values (rev 2) | `evidence/sim/{census-base,census-records,census-control}.out`, `rev2-census-*.out`, `SHA256SUMS` (6 OK), `rev2-SHA256SUMS` |
| 8 | **End-to-end sanity on the landing** (the user's scenario, not an import check): capture the five custody paths with the landed tool, verify against live with the coverage gate | `evidence/after/live-pre.txt` + `.sha256` (receipt `f7a89abd…`), `CUSTODY_PAIR_CAPTURE: OK paths=5/5 exit=0`, `CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0` |
| 9 | **Baselines for the records** (independent of the tool): command A at HEAD `015e1ba` and census PASS | §3 below; raw in `/var/tmp/sc3-r4/` (re-run at close, unchanged) |

## 2. Proposed changes

**none by this seat.** Scribe role: no tool code, no patch text, no target write.
The two drafts under `claims/c3/records-drafts/` are the parent's to apply (append
at EOF); the ledger is the chain's measurement artifact. This seat did not write
`.ufo/gates/custody-pair/` (EX-21's target), `corpus/`, `SKILL.md`,
`PROVINCE.md`, any README, `LOG.md`, `SCORECARD.md` or `SHONEN.md`.

## 3. Before → after measurement for the chain's claim

**Before (base `7cd19c3c…`, this seat, 14:04–14:07Z)** — all four residuals
reproduced; the full matrix is `ledger.md` §The ledger. The three headline
numbers:

| residual | before | after (landing `29bb45ae…`, 14:10Z) |
|---|---|---|
| (a) sidecar scope | spelling A: exit **0**, measured file replaced by the 2-line sidecar (`b6a98d9c…` → `03b5430f…`); spelling B: exit **0**, neighbour + `X.sha256.sha256` written | both spellings exit **2** with the guard's message; victims re-derive their pre-image shas; no second derived sidecar |
| (b) mkdir outside try | raw `NotADirectoryError` traceback at `custody-pair.py:653`, exit **1** | `USAGE: cannot create the receipt directory (…)`, exit **2**, no traceback; fresh parent still created (`OK paths=1/1 exit=0`) |
| (c) coverage counts stanzas | padded v2 / sums / pipe all exit **0** with **0** coverage lines; 5-distinct also exit 0 | all three padded shapes exit **2** with `reference covers 1 of the required 5 distinct paths` + the coverage line; 5-distinct still exit 0; 1-of-5 unchanged exit 2 |
| (d) both-absent MATCH | exit **0** `MATCH`, `compared=0/11`, `0/0` contract; compound: 5 all-absent stanzas pass the gate **and** read `MATCH 5/5` | ruling landed in README §"The both-absent `MATCH`"; every both-absent row now prints `the MATCH is an agreement on absence, not a verified presence`; compound still `MATCH 5/5` **by declared ruling**, but non-silent |

Supporting numbers: selftest **22 → 28** CLEAN (`after-k1.out`; the six new
claim-relevant case names all PASS); every receipt self-pins
`29bb45ae…` (`# tool:` header re-derived from `work-after/fixtures/r1.txt`);
end-to-end pair `MATCH 5/5 exit 0`; the controls table in `ledger.md` shows all
eleven control legs green on both revisions. Baselines at HEAD `015e1ba`:
command A `{"knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [],
"citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0,
"depth_score": 10.0}`; census `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)` exit 0. Pin-free: records projection **17 loci → 17 loci**, PASS
0/0/0/0; control FAIL undeclared=1 exit 1; CN-2 checker `PIN_FREE_VERDICT: CLEAN`
on both drafts.

**Landing-window churn, recorded (rule #14 class).** The tool moved exactly once
(`7cd19c3c…` → `29bb45ae…`, 14:09:30Z) and stayed; the README moved four times
in the window (`f30df42e…` → `91fd386b…` → `125e7e02…` → `9d9400da…`, the last
after my first citation). My after-transcripts are against the tool revision and
were unaffected; the README citations in the ledger name `125e7e02…` (the bytes I
read the ruling from) and the parent must re-derive the settled README at the
commit point. The README's own selftest line and case list match my transcript
(28 cases), so the revisions differ in prose, not in the claim.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| 1 | "the before-state is a paraphrase of r3's ledger, not a measurement" | **refuted** — every before leg was re-run on a scratch copy with fresh fixtures and fresh shas; the r3 ledger's numbers appear only in the cross-corroboration column |
| 2 | "the after-column is taken from peers' variants" (the failure mode R4 named at first draft) | **refuted by re-measurement** — the landing arrived mid-task and every after cell was re-run on the landed copy; peers' variant values survive only as corroboration |
| 3 | "the coverage fix would refuse legitimate references" | **refuted** — 5-distinct and mixed sets still exit 0 with `MATCH 5/5`; the 1-of-5 refusal is byte-identical to the base's |
| 4 | "the sidecar fix closes only the spelling EX-23 tested" | **refuted on the landing** — spelling B (EX-23's open half) now refuses too, with `vic`/`vic.sha256` intact and no `vic.sha256.sha256` |
| 5 | "the mkdir fix regresses `--out ''` or fresh parents" (CR-4 item 6 / RV-7 attack 1) | **refuted on the landing** — `--out ''` keeps its declared USAGE class with a named message; fresh-parent capture still succeeds |
| 6 | "the (d) ruling is a costume that leaves the compound case silent" | **refuted** — the compound case still reads `MATCH 5/5` (the declared ruling), but each both-absent row now carries the `agreement on absence, not a verified presence` note; the claim's "adjudicate and document" is satisfied by text that a reader cannot miss in the tool's own output |
| 7 | "the records drafts are pin-free by assertion" | **refuted by measurement** — census projection rev 2: records tree PASS 0/0/0/0 at **17 loci unchanged**, control FAIL undeclared=1; CN-2's token checker CLEAN on both literal bodies |
| 8 | "the gate now means the canonical five" (the tempting overclaim) | **refuted and kept open** — a 5-distinct-non-canonical reference still passes (measured both revisions); ledger R3 records this as a scope statement, not a defect, so the records cannot silently inherit a stronger claim |
| 9 | "my evidence copies are byte-equal to the raw scratch tree" | **verified** — `sha256sum -c` clean on all three manifests (before 55/55, after 54/54, sim 6/6) |

## 5. Blockers

**None outstanding.** Two timing facts worth the parent's attention:

- The **README is still moving** (`9d9400da…`, 272 L at 14:11Z; cited in the
  drafts/ledger as `125e7e02…`/267 L, the bytes I read the ruling from). The
  tool digest is stable at `29bb45ae…` across every poll from 14:09:30Z. The
  README-dependent facts in my drafts were re-checked against `9d9400da…`: the
  ruling section name is unchanged, and the selftest count still reads 28
  (`CLEAN cases=28 passed=28 failed=0`), so the later revisions differ in prose,
  not in the claim. The parent should still re-derive the settled README at the
  commit point.
- **The registry row is patch text, not landed.** `SKILL.md` still carries the
  round-3 row; `claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md`
  holds the line-neutral replacement (base `5eec51c0…`/390 L → patched
  `8e56f3d9…`/390 L). Applying it in the same commit as the tool + README is the
  parent's step, and it is the last open clause of the C3 claim that this seat
  can see.

EX-21's landing package arrived at 14:12Z (after my first draft close) and was
folded in: their run of my harness reproduces my after-matrix leg-for-leg, their
live pair (`MATCH 5/5` plain and gated, both sidecars `sha256sum -c` OK) was
re-verified independently by me against the landed tool, and their selftest
transcript reads the same 28 cases. All three are cited in `ledger.md`
§"Cross-seat landing corroboration".

## 6. Deliverable identities (re-derived at close, rule #14)

| artifact | sha256 |
|---|---|
| `seats/SC-3.md` (this report) | `64d24a76b0162b1a3ad0284ca1cff03646fa717ef3e669552a501fc668ea353c` (pre-identity-row revision; this row's own insertion moves it — the parent's read is the authority) |
| `claims/c3/SC-3/ledger.md` | `b661d15e72e123d2890a70a37009fcb22a6e4124d603a0f2544f5376972a809d` |
| `claims/c3/records-drafts/LOG-entry-draft.md` | `2d64ded83347b581ddd61d7e2d7d340f6a5c812cadab3a87deccf2e93e3324a2` |
| `claims/c3/records-drafts/scorecard-section-draft.md` | `e4ebc08b661b30315ccb14276b767dd85229a1bdd3dde6495bbde527dd538043` |
| `claims/c3/SC-3/harness/injections.sh` | `4f06845665498cea2ba9768d2a1645c4f75d7e2b1162ecded89a46b1f242e7bf` |
| landed tool / README (observed) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 L) / `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` (272 L) |

Evidence manifests: `evidence/before/SHA256SUMS` (55/55 OK),
`evidence/after/SHA256SUMS` (54/54 OK), `evidence/sim/SHA256SUMS` (6/6 OK) and
`rev2-`/`rev3-SHA256SUMS` (3/3 OK each), all verified from their own dirs.
