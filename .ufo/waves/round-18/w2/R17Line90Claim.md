HOLDS

# R17Line90Claim — w2 falsify, round 18

- **Seat:** `KaidokuR18.R17Line90Claim`, an author-side advisory reviewer and leaf. This is a recommendation, not an admission.
- **Revisions:** REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
- **Claim tested:** `corpus/lessons/round-18.md:51-52` (REV) says two things:
  - `corpus/lessons/round-17.md:90` inherits the R17-PINMAP overstatement.
  - `round-17.md:88,122` carry the R17-VALIDATE16 overstatement.
  The question was whether those anchors hold at REV and whether every overstated site has a named correction somewhere at REV.
- **Scope:** read-only on the lane; the only lane write is this file. Git writes happened only in a mkdtemp `--shared` clone with `origin` removed, deleted after use. No REA, no Ghidra, no carrier execution, no jj. No installs or updates.

## Verdict

**HOLDS.**

1. **All three anchors carry the quoted overstatements at REV.** The bytes are identical to the baseline: `round-17.md` has a 0-line diff from 9011581 to REV.
2. **Every overstated site found has a named correction at REV.** That is the 7 factual sites in the census below, plus QUALITY #19 handled by the new row #21.
3. **Every correction is a pure append** (0 deleted lines).

One LOW finding (F1) is about how durable this is. The C1 counter `routed-defects.py --strict` stays exit 0 when the corrections for 5 of the 7 sites are removed. Four of those five are the subject of this claim (`round-17.md:88/90/122`, `SCORECARD.md:2364`); the fifth is knowledge `:3`. At REV the coverage exists only in prose.

## 1. Anchors at REV (observation)

| Anchor | Text at REV (cell / sentence) | Defect | Baseline |
|---|---|---|---|
| `corpus/lessons/round-17.md:88` | fix cell: "…its fixture now uses the producer's object shape; **all 16 receipts were validated**." | VALIDATE16 | identical (C3) |
| `corpus/lessons/round-17.md:90` | fix cell: "Every mid-run check is retained with its instant (second pass: 2–8 per run, all equal); **the entry states identical bytes at those instants only**; …" | PINMAP (second clause) | identical (C3) |
| `corpus/lessons/round-17.md:122` | "…**All 16 receipts pass the final validator (verification pass).**" | VALIDATE16 | identical (C3) |

Why `:90` "inherits" the overstatement [INFERENCE from observed bytes]:

- The second clause vouches for knowledge `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:32` ("They show identical bytes **at those instants** only"), and "those instants" includes the mid-run ones.
- At REV, all 29 mid-run records in the 8 second-pass receipts are verdict-only. Their key set is exactly `{changed, entries, equal, missing, taken_at_utc}` and no map is kept (C9).
- "Identical bytes" at mid-run instants is therefore a comparator verdict described as the compared object. Two rules exclude that:
  - QUALITY #19 (`corpus/QUALITY.md:29`): a map is retained at every named instant.
  - QUALITY #21 (`corpus/QUALITY.md:31`): a verdict is never described as the compared object.
- The first clause ("check … retained") is accurate. `round-18.md:51` quotes only the second clause, so the attribution is scoped correctly.
- The captured-by cell of `:90`, "#19 now does", is not an overstatement: the outside spot-check caught R17-PINMAP through #19 (`corpus/lessons/round-17-verifier-spotcheck.md:108`) [INFERENCE].

Why `:88/:122` are overstated (observation):

- `.ufo/waves/round-17/verification.json` at REV retains exactly 8 distinct `receipt-validate-*` labels (C9).
- `:122`'s "final validator" is the blob at `d0ab299`. It is identical to the `9011581` blob (`2762496c…`), and its sha256 `618448829b…` equals `validator_sha256` in `.ufo/waves/round-18/evidence/validate16/summary.json` (C10). So the round-18 remapped replay ran the very validator `:122` names.

## 2. Coverage census: overstated site → named correction at REV

| # | Overstated site (REV) | Routed by | Named correction(s) at REV | Guarded by `routed-defects.py`? |
|---|---|---|---|---|
| 1 | knowledge `:30-32` ("each pin map is retained … All maps are equal") | spotcheck `:137` | knowledge `:204`; `round-18.md:51` | **yes** (`routed-defects.py:240-245`) |
| 2 | knowledge `:3` (recheck "exit 0 = … mid-run checks consistent") | r18 itself (w1 `CriticDiscernment.md`) | knowledge `:205` | **no**: M3 → exit 0 (C14) |
| 3 | `SCORECARD.md:2374` ("pre/mid/post pin maps with instants") | spotcheck `:137` | `SCORECARD.md:2438`; `round-18.md:51` | **yes**: M2 control → exit 1 (C13) |
| 4 | `corpus/lessons/round-17.md:90` | r18 itself (w1 `ScoutPinmapSites.md` §2 row 3) | `round-18.md:51` ("Also … inherits the same overstatement") | **no**: M1 → exit 0 (C13) |
| 5 | `SCORECARD.md:2364` ("all 16 receipts … exit 0") | spotcheck `:138` | `SCORECARD.md:2439`; `LOG.md:2159`; `round-18.md:52` | **no**: M1 → exit 0 |
| 6 | `corpus/lessons/round-17.md:122` | spotcheck `:138` | `round-18.md:52`; `LOG.md:2159` | **no**: M1 → exit 0 |
| 7 | `corpus/lessons/round-17.md:88` | r18 itself (w1 `CriticC1.md:65`, `ScoutValidate16Sites.md:38`) | `round-18.md:52`; `LOG.md:2159` | **no**: M1 → exit 0 |
| — | QUALITY #19 `corpus/QUALITY.md:29` (the unmet rule, not a false claim) | spotcheck `:137` | new row #21 `corpus/QUALITY.md:31` (why-cell `R17-PINMAP`); rows 1–20 unchanged | yes (`quality-admission-row`) |

**Append-only (observation, C4/C5).** From 9011581 to REV, `git diff --numstat` shows:

| File | Added | Deleted |
|---|---|---|
| `LOG.md` | 44 | 0 |
| `SCORECARD.md` | 14 | 0 |
| `corpus/QUALITY.md` | 1 | 0 |
| knowledge entry | 8 | 0 |

- `round-17.md` and the spotcheck do not appear in the numstat (unchanged).
- The hunks for the knowledge entry, SCORECARD and LOG are at file end.
- The QUALITY change is the single row-21 insertion after row 20 (1 added, 0 deleted).

**Checked and not overstated** (C6/C7/C8; judgments are [INFERENCE] unless noted):

- `corpus/lessons/round-17.md:30`: "Second-pass pins are equal at every retained instant". This is a verdict-level statement, and every verdict is `equal: true` (C9). No map or bytes are claimed.
- `round-17.md:81` and `:106`: "pin check" / "checks".
- `LOG.md:2087` and `:2100`: "Mid-run pin checks retained: 2–8 per run, all equal".
- `SKILL.md:537`: "pins equal at every recorded instant".
- `SCORECARD.md:2374`, column 3: "`receipt-validate.py` exit 0 ×8". This matches the 8 labels (observation, C9).
- `SCORECARD.md:2378`, knowledge `:194`, `round-17.md:41`: "All 16 logs reach `REPORT: Analysis succeeded`". This is about log content, not validation. I did not re-measure it; w1 `ScoutValidate16Sites.md:68` did.
- `ScoutMistakeSweep`'s "report:35" is the out-of-lane fleet file `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md`; the lane has no such path (C6, rc 128). Its `:35` ("mid-run pin checks retained") and `:62` ("8/8 receipts valid") are accurate.

**Numbers inside the corrections (observation):**

- "29/29 second-pass checks" (`round-18.md:51`, knowledge `:204`): 29 records, one key set, all `equal: true` (C9).
- "8 validations were retained" (`round-18.md:52`, `SCORECARD.md:2439`): 8 distinct labels (C9).
- None of the 8 `da64646` receipts carries `pin_checks` (C11). The remapped 8/8 therefore involves no verdict-only mid-run entries, so QUALITY #21's "accepted, not verified" clause is not engaged.
- I read the summary (`rev` `da64646…`, 8 entries, every `exit` 0) but did not re-execute it.

## 3. Findings

### F1 — LOW (calibration / operability): the C1 counter does not guard 5 of the 7 site corrections

**Observation.**

- `routed-defects.py` at REV anchors R17-PINMAP only to knowledge `:30-32` and `SCORECARD.md:2374` (`PINMAP_ANCHORS`, `.ufo/waves/round-18/tools/routed-defects.py:64-65`).
- For R17-VALIDATE16 it requires only a SCORECARD line and a LOG line containing `R17-VALIDATE16` plus `k/8` (`:430-433`, `:477-483`). No `file:line` anchor is required.

**Mutations (C12-C14).** All were built in a mkdtemp `--shared` clone with origin removed, using `commit-tree` with a fixed identity and date. Rebuilding gave identical SHAs.

| Commit | Change from REV | `routed-defects.py --strict` |
|---|---|---|
| REV | — | exit 0, `open_count` 0 |
| M1 `86ba338c9858e18c0abae43fcc9b5e40b1865d8d` | Strips every correction mention of `round-17.md:88`, `:90`, `:122` and `SCORECARD.md:2364` (2 lines in `round-18.md`, 1 in `LOG.md`, 1 in `SCORECARD.md`; at M1, `git grep` for those anchors in the lesson/LOG/SCORECARD/knowledge returns rc 1) | **exit 0, `open_count` 0**; PINMAP and VALIDATE16 both `open=False` |
| M3 `66b27c5be8063e07564a20c0a90fe6f74b45eef8` | Deletes knowledge `:205` (the `:3` recheck correction) | **exit 0, `open_count` 0** |
| M2 control `c82101674cc556bdb297e2e6051d41db53e71383` | Removes only `SCORECARD.md:2374` from the `SCORECARD.md:2438` PINMAP line | **exit 1**, `R17-PINMAP` open: `substance scorecard-correction-anchored`, detail "no line containing 'R17-PINMAP' + 'SCORECARD.md:2374' + 'not the map'". This shows the harness does detect an anchor it checks. |

**Why this matters.**

- The lane's own correction standard (`corpus/lessons/round-17.md:83`) is that a correction carries the marker, the exact `file:line` and the required phrase. The counter enforces this for 2 PINMAP sites only.
- w1 `CriticC1.md:69` (V2) proposed exactly the missing clauses: "the anchor `SCORECARD.md:2364`. A round-18 lesson line anchors `round-17.md:122` and `:88`."
- Neither the tool, `contract.md:33-35`, `RoutedDefectsTool.md`, `SimplifyRoutedDefects.md` nor `round-18.md` records a decision to drop them (C15: within those files, the anchors appear only on `round-18.md:51-52`).
- `round-18.md:8` reads as if each defect is "closed by a named correction **and** a substance check". For VALIDATE16 the "named" half is token-level, and per-site naming of the routed `SCORECARD.md:2364` and `round-17.md:122` is not measured.
- Nothing is missing at REV. The risk is that the "6 → 0" count would stay green if these sites lost their corrections.

**Suggested fix (author-side, advisory).** Add the following needles to `_d_validate16`/`_d_pinmap`, each with a selftest fixture in which stripping the anchor keeps the defect open:

- `SCORECARD.md:2364` on the SCORECARD/LOG R17-VALIDATE16 lines;
- `round-17.md:88` and `:122` on a `round-18.md` R17-VALIDATE16 line;
- `round-17.md:90` on a `round-18.md` R17-PINMAP line;
- `go-carrier-diagnostics.md:3` on a knowledge R17-PINMAP line.

Alternatively, state in `round-18.md` that these inherited-site corrections are prose-only.

### F2 — INFO: the `:90` correction names the site but gives no replacement statement

- `round-18.md:51` co-locates the marker, the site anchor and the required phrase, so it meets `round-17.md:83` by line.
- Unlike knowledge `:204` ("The statement that holds is: …") and `SCORECARD.md:2438`, it says "inherits the same overstatement" without a replacement for `:90` [INFERENCE: acceptable under the lane rule].

### F3 — INFO: the knowledge self-attestation tag sits outside the cited range

- The "(QUALITY #19)" tag is at knowledge `:33`, just outside the corrected range `:30-32` (the sentence spans `:32-33`).
- Correction `:204` replaces the sentence's substance but does not name the tag. QUALITY #21 (`:31`) now covers inline `(QUALITY #N)` tags as a class.

## 4. Residual risk and verification gaps

- **Not re-executed:** the remapped da64646 validation 8/8. `summary.json` was read only; re-execution belongs to `TruthVALIDATE16`/`Validate16Run`.
- **Search method:** the census used `git grep` phrase families (C7, C8, plus the pin/validat sweeps in C6) over `corpus`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `README.md` and `.ufo/reports`, plus a full-tree "all 16|16 receipts" grep. An overstatement phrased with none of those tokens would be missed. No LSP applies to Markdown prose, so this is a text census, not semantic proof.
- **Out of scope:** the other 4 routed defects (PRODUCER-REV, SUMS-RUNLOG, REGISTRY, S032-DIGEST).

## 5. Commands (argv → exit). Lane = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; R = REV, B = baseline

| # | Command | Exit / result |
|---|---|---|
| C1 | `git cat-file -t R; git cat-file -t B; git rev-parse HEAD` | 0, 0; HEAD = R |
| C2 | `git show R:corpus/lessons/round-18.md \| nl -ba` | 0 (lines 49-56, 62-63 read) |
| C3 | `git show {R,B}:corpus/lessons/round-17.md \| nl -ba \| sed -n '88p;90p;122p'` | 0/0, byte-identical text |
| C4 | `git diff R..B` `--stat` / line count on `corpus/lessons/round-17.md` | 0, 0 lines |
| C5 | `git diff --numstat B R -- <round-17.md, knowledge, SCORECARD.md, LOG.md, QUALITY.md, spotcheck>` | 0 (44/0, 14/0, 1/0, 8/0) |
| C6 | `git show R:.ufo/reports/round-17/kaidoku.md`; `nl -ba /home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md` | 128 (absent in lane); 0 |
| C7 | `git grep -n -i -E 'all 16\|16 receipts' R -- '*.md'` | 0 |
| C8 | `git grep -n -i -E 'each pin map\|All maps are equal\|pin maps with instants\|…\|identical bytes' R -- '*.md' '*.py'` | 0 |
| C9 | `python3 -I -B -c` (parse `R:verification.json` labels; sum `steps.analyze.pin_checks` over `R:.ufo/waves/round-17/runs/*/receipt.json`) | 0: 8 labels; 8 receipts; 29 checks; one key set; all equal |
| C10 | `git rev-parse {d0ab299,B}:.ufo/waves/round-17/tools/receipt-validate.py`; `git show B:… \| sha256sum` | 0: `2762496c…` ×2; `618448829b…` |
| C11 | `python3 -I -B -c` (`pin_checks` in `da64646:…/runs/*/receipt.json`) | 0: None ×8 |
| C12 | `mktemp -d /tmp/r17line90-XXXXXX && git clone --quiet --shared --no-checkout <Lane> $T/c && git -C $T/c remote remove origin` | 0; remotes empty |
| C13 | `python3 -I -B -c` builder (`read-tree R`; replace exact substrings; `hash-object -w`; `update-index --cacheinfo`; `write-tree`; `commit-tree -p R`; env `GIT_INDEX_FILE=$T/c/.git/probe-idx`, author/committer `probe <probe@invalid>` 2026-10-20T00:00:00Z) → M1, M2; then `python3 -I -B $T/c/routed-defects.py --root $T/c --rev {R,M1,M2} --strict` (tool = `R:` blob, sha256 `034f5ead…84b2`, equal to the lane blob) | builder 0; R: 0; M1: 0; M2: 1 |
| C14 | same builder, M3 (delete knowledge line 205); `routed-defects.py --rev M3 --strict` | builder 0; tool 0 |
| C15 | `git grep -n -E '2364\|round-17\.md:(88\|90\|122)\|anchor-bound\|\bV2\b' R -- .ufo/waves/round-18/tools contract.md w1/RoutedDefectsTool.md w1/SimplifyRoutedDefects.md corpus/lessons/round-18.md` | 0; only `round-18.md:51,52` match |
| — | `rm -rf /tmp/r17line90-qVOvZN` | 0 |

The M1 replacement strings, applied to `R:` blobs and asserted to occur once each:

- `round-18.md`: ``" Also `corpus/lessons/round-17.md:90` (\"the entry states identical bytes at those instants only\") inherits the same overstatement (w1 `ScoutPinmapSites.md`)."`` → `""`
- `round-18.md`: ``"`SCORECARD.md:2364` and `corpus/lessons/round-17.md:88,122` (\"all 16\") "`` → `""`
- `LOG.md`: ``"; r17's \"all 16\" (`SCORECARD.md:2364`, `corpus/lessons/round-17.md:88,122`) had 8 retained runs."`` → `"."`
- `SCORECARD.md`: ``"`SCORECARD.md:2364` (\"all 16 receipts `receipt-validate.py` exit 0\") had 8 retained validations; "`` → `""`

M2 (`SCORECARD.md`): ``"`SCORECARD.md:2374` (\"pre/mid/post pin maps with instants\") is wrong"`` → `"the capability row (\"pre/mid/post pin maps with instants\") is wrong"`.

One aborted M3 attempt exited 2: `--rev` was passed with no argument because unreferenced commits are not visible to `git log --all`. It was re-run with the explicit SHA (C14). Its accidental `git diff` against the empty clone worktree was read-only and confined to the clone.
