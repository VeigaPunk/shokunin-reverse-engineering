# ScoutProducerRevSites — every r17 revision-assertion site at `9011581`

Seat: `KaidokuR18.ScoutProducerRevSites` (scout, leaf, read-only). Baseline `B` =
`9011581d84527ba34c675f9cf912e54d2e72d470` (`refs/heads/main` tip = `HEAD`). Axes: calibration,
operability, depth. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier executed, no `jj`, no
git write. Installs/updates: **none**. The only file written is this report.

Routed defect under scope: `corpus/lessons/round-17-verifier-spotcheck.md:139` (R17-PRODUCER-REV) — "Name
the producing revision per pass wherever \"measured source revision\" is cited."

## Verdict (observation)

- The literal phrase **"measured source revision"** occurs **once** in the r17 material of the five named
  surfaces: `SCORECARD.md:2353`. It names only the round-level `d0ab299…` source revision and the
  `b31975de…` evidence revision; it names **no** producing revision for either carrier pass.
- `LOG.md`, the r17 knowledge entry, and `corpus/lessons/round-17.md` never use the literal phrase; they
  state the same fact as "Source revision" / "evidence revision" / "pre-falsify source revision".
- `SKILL.md` contains **none of the six r17 revision hashes** (whole file, not just the r17 section): zero
  sites there.
- Exactly **one** site in the five surfaces names a producing revision per pass:
  `corpus/lessons/round-17.md:122`. It is a *Tools* bullet under "In-round revisions", not a
  measured-revision statement, and it still says the second pass "started at" `95e34db` rather than that
  the retained receipts were produced by it.
- Net: the defect is open at B on 1 literal-phrase site plus 27 other revision-bearing lines tabulated
  below (SCORECARD 6, LOG 8, knowledge 5, lesson 8, SKILL 0); the knowledge entry (a contract-required
  surface for the closure line) has **no** producer statement.

## Sites, surface by surface

Kind legend: **M** = measured/source revision claim; **V** = verification/evidence revision; **F** =
prediction freeze; **B** = baseline of measurement; **P** = producing revision; **R** = retention
location / file revision.

### `SCORECARD.md` — Round 17 section starts `:2350`

| Site | Kind | What it says (verbatim fragment) | Gap |
|---|---|---|---|
| `SCORECARD.md:2352-2353` | B, F | "Baseline: `b563c799d97774aae4351276fe43cb897311e349`. Predictions frozen: `271167473d87ef710f07ecdd98caf0ce12091686`." | none (baseline/freeze correctly named) |
| `SCORECARD.md:2353-2356` | **M, V** | "Measured source revision (committed and pushed before the single verification pass): `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905`; verification evidence revision `b31975de62de5413a6f2d244f2690eaeb3d18c25`." | **the literal-phrase site.** No per-pass producer. The sentence equates "measured" with the *verification* pass, so a reader infers the 16 run receipts were produced at `d0ab299`, which is false for both passes |
| `SCORECARD.md:2356-2358` | V | "Producer argv/cwd/exit/stdout/stderr and pre/post pins: `.ufo/waves/round-17/verification.json` (79 commands, all expected exits)…" | "Producer" here is the *verification* pass's 79 commands, not `carrier-run.py`'s receipts |
| `SCORECARD.md:2361` | M | Column header "…command and measured revision" | The per-row measured revision is a single round-level value; no pass column exists |
| `SCORECARD.md:2363` | M, V | "(baseline exit 0 at `b563c79`; 4/4 corrected at `d0ab299` and `b31975d`) … at `b563c79` and `b31975d` (17/17 `exercised_match`)" | Correct for the *controls*; they were measured at the verification revision, not by the carrier runs |
| `SCORECARD.md:2364` | F, M | "8/8 compare exit 0 per pass against predictions frozen at `2711674`; all 16 receipts `receipt-validate.py` exit 0 (MD5-anchored binding)" | "per pass" appears with no revision per pass; the 16 receipts' validator runs are the verification pass (see R17-VALIDATE16) |
| `SCORECARD.md:2374` | R, P-adjacent | "carries pre/mid/post pin maps with instants … receipts … (16 across two passes, **8 retained at HEAD**, 8 at `da64646`)" | `da64646` is named as a *retention* location, not a producer; "**8 retained at HEAD**" is a live-HEAD prose pin that moves with every commit (text-level HEAD keying, out of C2's py/sh lint scope) |

### `LOG.md` — round-17 entries `:2033` and `:2069`

| Site | Kind | What it says (verbatim fragment) | Gap |
|---|---|---|---|
| `LOG.md:2035-2036` | B | "baseline `b563c799d97774aae4351276fe43cb897311e349`" | — |
| `LOG.md:2041-2042` | B | "Baseline `temporal-sweep.py --sites-rev b563c79`… `invocation-audit.py` at b563c79" | — |
| `LOG.md:2046-2047` | F | "routes predicted … committed at `271167473d87ef710f07ecdd98caf0ce12091686` before the first run." | — |
| `LOG.md:2066-2067` | M | "Measured values follow in the next entry after the single post-integration execution pass." | names the pass, not the runs' producers |
| `LOG.md:2071-2072` | **M, V** | "Source revision `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` (committed and pushed before the pass); verification evidence `b31975de62de5413a6f2d244f2690eaeb3d18c25`." | round-level only; no per-pass producer |
| `LOG.md:2096-2097` | **P-adjacent** | "Second carrier pass, 14:27–14:40 UTC, all 8 exit 0 / compare 0. Replicate expectations were frozen at `95e34db` before it." | `95e34db` is introduced as the *expectation freeze* revision, not as the tool revision that wrote the receipts; no first-pass producer anywhere in LOG |
| `LOG.md:2102` | V | "Verification pass at `d0ab299`, `verify.py`: 79 commands, all expected" | — |
| `LOG.md:2115` | V | "Final rechecks at `b31975d`, retained via `retain.py`" | — |

### `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`

| Site | Kind | What it says (verbatim fragment) | Gap |
|---|---|---|---|
| `:1` (frontmatter `source:`) | **R, F** | "retained runs under `.ufo/waves/round-17/runs/` (second pass) and at lane commit `da64646adcb19c1ede7537b799b8c7d283fe43da` (first pass); predictions frozen at lane commit `271167473d87ef710f07ecdd98caf0ce12091686` before any measured run." | first pass gets a *retention commit*, second pass gets **no revision**; neither is called a producing revision. This is the frontmatter a contract-check line must touch |
| `:2` (`verified-at:`) | P-adjacent | "first pass 13:47–14:00 UTC, second pass 14:27–14:40 UTC **with the hardened capture tool**" | relative adjective ("hardened") instead of a revision |
| `:29-33` | P-adjacent | "In the second pass each pin map is retained with its UTC instant … The first-pass receipts kept only pre/post maps." | distinguishes passes by receipt shape, still no revision |
| `:47` | F | "All eight predictions were committed at `2711674` before the first measured run." | — |
| `:115` | R | "…as frozen in `predictions/replicate-expectations.json`." | machine file does carry `first_pass_revision` (see adjacent sites) |

No `R17-PRODUCER-REV`, no `95e34db`, no `d0ab299`, no "produced by" in this file (grep, no matches).

### `corpus/lessons/round-17.md`

| Site | Kind | What it says (verbatim fragment) | Gap |
|---|---|---|---|
| `:6` | R | "This file was first committed mid-round at `da64646adcb19c1ede7537b799b8c7d283fe43da`." | file revision, not producer |
| `:30` | F | "Predictions were committed at `271167473d87ef710f07ecdd98caf0ce12091686` before the first measured run." | — |
| `:81-82` | B, R | "At baseline `b563c79`…" ; "the round-17 verification pass exercised (`.ufo/waves/round-17/verification.json`, labels `citation-strict` and `custody-capture`)" | round-16 routed sites |
| `:88`, `:90` | R | "At `da64646`, `receipt-validate.py` rejected all 8 producer receipts…"; "The `da64646` knowledge entry and lesson said…" | `da64646` used as the *defective* revision |
| `:122` | **P** | "The first-pass receipts at `da64646` were produced by the pre-hardening `carrier-run.py`. The second pass started at `95e34db`." Also: "The binding check was then made MD5-anchored and line-anchored. All 16 receipts pass the final validator (verification pass)." | the only per-pass producer sentence in the five surfaces; "started at" ≠ "produced by"; does not state that the MD5-anchored binding post-dates the second-pass receipts (so no receipt carries it) |
| `:126` | B | "The initial lane state was clean at `b563c799d97774aae4351276fe43cb897311e349`." | — |
| `:145-149` | **M, V** | "- Source revision `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905`. The single verification pass `python3 -I -B .ufo/waves/round-17/verify.py b563c79…` retained 79 commands…" | round-level; no producer |
| `:150-151` | V | "Final rechecks at the evidence revision `b31975de62de5413a6f2d244f2690eaeb3d18c25`…" | — |

### `SKILL.md` — r17 section `:509-546`

- `:511-512` references the knowledge entry; `:514-515` says routes were "frozen in Git before the
  measured runs"; `:516-517` says "8/8 routes matched in both passes".
- Registry rows `:537-546` cite commands, exits, selftests and pinned values; `:537`'s pinned-value cell
  names the 146-path pin set, `RUNS_DIR`, `runs/run-log.txt` and `verification.json`, **no revision**.
- Whole-file grep for `da64646|d0ab299|b31975d|95e34db|2711674|b563c79`: **no matches**. SKILL has no
  R17-PRODUCER-REV target.

## Adjacent lane sites (outside the five, same claim)

| Site | What it says | Note |
|---|---|---|
| `.ufo/waves/round-17/w2/draft-scorecard.md:10-11` | "Committed pre-falsify source revision: `da64646…`. Final measured source revision: `{FINAL:REV}`." | the other literal-phrase use; a draft with an unresolved placeholder, frozen in w2 |
| `.ufo/waves/round-17/predictions/replicate-expectations.json:83` | `"first_pass_revision": "da64646adcb19c1ede7537b799b8c7d283fe43da"`; `"frozen_before": "second (replicate) measured pass with the w2-hardened carrier-run.py"` | machine-readable pass attribution; no second-pass revision field |
| `corpus/lessons/round-17-verifier-spotcheck.md:10-12` | predictions `2711674…`; S `d0ab299…`; evidence `b31975de…`; delivered A `de6c721…` | the routed defect's own revision header |
| `LOG.md:2115` | final rechecks at `b31975d` | listed above |

## Cross-check of the routed premise (observation; supports calibration)

Commit chain at B (`git log --format='%H %cI %s'`):

| Revision | Committer time | `carrier-run.py` blob | Role |
|---|---|---|---|
| `2711674` | 2026-10-20T10:46:45-03 | `bc964acdfb0751310ee014799627774c45469f38` | predictions frozen (pre-run) |
| `da64646` | 11:06:06-03 | `bc964acdfb…` (same) | first-pass receipts committed |
| `95e34db` | 11:27:35-03 | `c536e3e4bd0b3091efd43d01448326cec5a63cc8` | hardened tools + frozen replicate expectations, **before** the rerun |
| `d0ab299` | 11:47:24-03 | `f91bbc76c73991ba5d74137ca69b115dcee7c12f` | "source revision"; post-rerun integration |
| `b31975de` | 11:48:35-03 | `f91bbc76…` | verification pass committed |
| `de6c721` | 11:50:03-03 | `f91bbc76…` | final rechecks; delivered A |
| `9011581` (B) | 12:06:56-03 | `f91bbc76…` | round-18 baseline |

Observations from Git objects (not from prose):

- `runs/pro-aether/receipt.json` blob is identical at `da64646` and `95e34db` (`413d2b975b44…`, first-pass
  shape: **no** `steps.analyze.pin_checks`); it changes at `d0ab299` and is identical at B
  (`d552512e4149…`, second-pass shape: 2–8 `pin_checks`; pro-aether = 3).
- The `steps.analyze` window across all 8 second-pass receipts at B is
  `2026-10-20T14:27:42.859987Z` → `14:40:02.270081Z`, i.e. after the `95e34db` commit (14:27:35Z) and
  before `d0ab299` (14:47:24Z).
- **No retained receipt in either pass records a producing revision or a tool digest** (recursive key
  scan: no `revision`, no `md5`; `binding` exists only as `retained_logs[].binding.logfile_ok/target_ok`).
  The second-pass receipts lack `carrier.md5_pre` and `binding.md5_ok`; the string `md5` occurs 0 times in
  the `da64646` and `95e34db` `carrier-run.py` blobs and 11 times in the `d0ab299` blob
  (`carrier-run.py:132,344`), i.e. those keys were introduced after both passes. So the spotcheck's
  discriminator is right in effect, but the name `binding.md5_ok` is a *tool-emitted key that never
  reached a receipt*.
- Inference (labelled): per-pass producer attribution rests on commit boundaries + tool blob identity,
  not on receipt self-record. Best statement supported by evidence: **first pass** = pre-hardening
  `carrier-run.py`, blob `bc964acd…`, present at the freeze commit `2711674` and at `da64646` (which
  first commits the receipts); **second pass** = `95e34db` tool blob `c536e3e4…`; **verification** =
  `d0ab299` tool blob `f91bbc76…`.

## Closure implications (advisory to L1; no edits made)

1. The contract's R17-PRODUCER-REV check (`.ufo/waves/round-18/contract.md:36-37`) needs, in **both** `SCORECARD.md` and the
   r17 knowledge entry, a line containing `R17-PRODUCER-REV` and **≥2 distinct 40-hex hashes**. Neither
   file has such a line at B. A correction line that satisfies it and the spotcheck's instruction:
   `R17-PRODUCER-REV: first pass produced by da64646adcb19c1ede7537b799b8c7d283fe43da (carrier-run.py
   blob bc964acd…, identical at 271167473d87ef710f07ecdd98caf0ce12091686); second pass produced by
   95e34db62f2693c455d7ee4dfef24b8f3ebc007d (blob c536e3e4…); verification at
   d0ab2992149a38794e5ef2474ba5d4ef5ee1e905.` (append-only; `2711674`/`95e34db` full hashes are
   `271167473d87ef710f07ecdd98caf0ce12091686` / `95e34db62f2693c455d7ee4dfef24b8f3ebc007d`.)
2. Put the same sentence, or a pointer to it, beside `SCORECARD.md:2353-2356` and in the knowledge
   frontmatter `source:` block, because those are the two surfaces a reader treats as the measured-
   revision statement. `LOG.md:2071-2072` and `corpus/lessons/round-17.md:145-151` are the matching
   non-required sites if the L1 wants one consistent wording across all four.
3. `corpus/lessons/round-17.md:122` should keep its content but may be rephrased to "produced by the
   `95e34db` `carrier-run.py` (blob c536e3e4…); the MD5-anchored binding landed at `d0ab299` after the
   pass", which removes the "started at" ambiguity without editing history.
4. Operability side-note: `SCORECARD.md:2374` "8 retained at HEAD" is a text-level HEAD pin. It is not in
   C2's lint scope (py/sh only) but it silently re-points at every new commit; naming `da64646` or the
   branch tip would make it stable. Not part of the R17-PRODUCER-REV check.
5. Do not touch the round-17 receipts or retained logs (non-goal); the correction is prose-only.

## Remaining unknowns (bounded)

- Whether the tool bytes present in the worktree at first-pass runtime (13:47–14:00Z) were exactly blob
  `bc964acd…` committed at 14:06Z. No receipt self-records a tool digest; `git log` over
  `carrier-run.py` shows no change between `2711674` and `da64646`, so this is the best available
  attribution, but it is inference.
- Whether the whole second pass used one tool blob: commit order supports it (only `95e34db` precedes the
  first receipt; `d0ab299` is 7 minutes after the last), but the receipts themselves cannot prove it.
- Whether an r18 receipt-schema change should add a producer revision/digest field; out of scope here and
  blocked by the non-goal on editing r17 retained receipts.

## Command log (as executed; all read-only)

```
$ git rev-parse --verify 'refs/heads/main^{commit}'   -> 9011581d84527ba34c675f9cf912e54d2e72d470   exit=0
$ git rev-parse --verify 'HEAD^{commit}'              -> 9011581d84527ba34c675f9cf912e54d2e72d470   exit=0
$ git status --porcelain --untracked-files=no         -> (empty)                                    exit=0
$ git rev-parse --verify --quiet <rev>^{commit} for 95e34db d0ab299 b31975de da64646 2711674
  b563c79 9011581                                     -> all resolved (full hashes above)            exit=0 each
$ git log --format='%H %cI %s' -n 12 --date-order 9011581 | sed -n '1,12p'                          exit=0
$ git diff --stat 9011581 -- SCORECARD.md LOG.md SKILL.md corpus/lessons/round-17.md \
    corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md -> (empty)                            exit=0
$ python3 -I -B <blob-eq-worktree + anchor scan over the 5 files>  -> blob-eq-worktree True (all 5)  exit=0
$ for rev in 2711674 da64646 95e34db d0ab299 b31975de de6c721 9011581; do \
    git rev-parse --verify --quiet "$rev:.ufo/waves/round-17/tools/carrier-run.py"; done           exit=0
$ git log --format='%H %cI %s' -- .ufo/waves/round-17/tools/carrier-run.py \
    .ufo/waves/round-17/run-carriers.sh | sed -n '1,12p'                                           exit=0
$ python3 -I -B <receipt key/shape scan at B, da64646, 95e34db, d0ab299>                           exit=0
$ python3 -I -B <receipt blob identity across 95e34db, d0ab299, 9011581>                           exit=0
$ python3 -I -B <8-receipt analyze window min/max>                     -> 14:27:42.859987Z..14:40:02.270081Z exit=0
$ grep (tool) 'measured source revision' over the lane; 'source[_ ]revision'; 'R17-PRODUCER-REV';
  '95e34db|da64646'; per-file anchor scans for SCORECARD/LOG/knowledge/lesson/SKILL        -> matched; no tool error
$ grep (tool) 'da64646|d0ab299|b31975d|95e34db|2711674|b563c79' in SKILL.md              -> no matches
```

Every quote above is copied from the blob at B; the five files are byte-identical to the working tree
(`git diff` empty, plus the explicit `blob == worktree` check), so line numbers are rev-exact.

Lane state during this scan (observation, not my write): `git status` showed sibling-seat edits to
`.ufo/waves/round-17/tools/compare.py` and `.ufo/waves/round-17/verify.py`. Those two files are outside
this report's scope, and the five scanned surfaces re-checked clean against B after the edits appeared
(scoped `git status`/`git diff` empty, exit 0), so no finding here depends on them.
