# CriticC1: is `routed-defects.py` a circular counter?

Seat: author-side advisory critic (KaidokuR18.CriticC1). Read-only except for this file. No installs. No REA, Ghidra, carrier or lane-tool execution. One throwaway `git clone --shared` under `mkdtemp` (`/tmp/criticc1-*`) took the scratch commits, and it was removed afterwards (`removed True`).

Axes: **calibration** (does 6 → 0 measure discharged defects?), **operability** (can the L1 run the checks over Git objects?), **depth** (which routed sites do the checks miss?).

## Verdict

**Observation.** Under the definitions as written (`.ufo/waves/round-18/contract.md:29-45`), the counter is circular. A token-only commit flips all six defects to closed without fixing any of them. Each check tests for a token that the round-18 writers are told to emit, or a fact the same commit can manufacture. None of them tests the defect's own observable.

- Three of the scribe prompts embed the grep tokens.
  - DraftPinmapCorrection: "must contain `R17-PINMAP` and `comparator verdict`".
  - DraftRegistryCells: "each containing `Write scope:`".
  - DraftS033Row: "`fetch-time only`".
  - The prompts are in `.ufo/waves/round-18/wave1-dispatch.json`, task strings at :1166/:1291/:1311/:1321.
- One draft reasons explicitly about meeting checks (a), (b) and (d) (`.ufo/waves/round-18/w1/DraftPinmapCorrection.md:17`).

**Judgment.** As specified, "6 → 0" is **bookkeeping**. It counts conformance to a token convention. It becomes calibration evidence only with the outcome-bound and anchor-bound checks below. Those checks are fixable defects in the contract, not a tradeoff the canonical judge must reject.

**Counter-finding (the attack fails in one place).** For the citation-drift relabel, the token change *is* the fix: the registered entry at B already has `--strict` and the 0/1/2 gate map (`SKILL.md:448`). Also, the sibling work is substantive. The drafts count 29 mid-run checks (`DraftPinmapCorrection.md:33`) and two differing fresh PR digests (`DraftS033Row.md:32`). The problem is that the counter cannot tell that substance from a token.

## Empirical counterexample

**Observation.** `routed-defects.py` is not yet present in `.ufo/waves/round-18/tools/` (glob at review time). I therefore wrote a **contract-literal re-implementation** of `contract.md:29-45` as a scratch Python eval cell (not committed, not the lane tool), ran it at B, then ran it on a token-only commit in the throwaway clone.

| Step | Command / cell | Exit / result |
|---|---|---|
| Baseline tokens absent | `git grep -n -c "$t" $B -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/knowledge/…r17…md SKILL.md corpus/SOURCES.md` for each of the six IDs | exit 1 (no hits, ×6) |
| Re-implementation at B | `check(LANE, 9011581…)` | `open_count 6`, all checks false |
| SKILL cell count | naive `\|` split on the five rows at B | 5 cells each (parse is safe at B) |
| Clone | `git clone -q --shared --no-checkout LANE /tmp/criticc1-*/sb` | exit 0 |
| Token-only commit | `git diff --numstat B b4d1e7bb…` | +21 lines across 10 files, 5 in-place SKILL cell edits |
| Re-implementation on flip | `check(sb, b4d1e7bb…)` | **`open_count 0`**, every check true |

The flip commit contains only the following. It fixes nothing:

- R17-PINMAP: `R17-PINMAP comparator verdict` appended to the r17 knowledge entry and to SCORECARD. A QUALITY row `| 21 | x | round-17-verifier-spotcheck.md R17-PINMAP | — |`. The comment `# map_sha256` appended to `carrier-run.py`.
- R17-VALIDATE16: `summary.json` = `{"rev":"da64646…","receipts":[{"exit":1}]*8}`. Every validation *failed*, yet the defect is closed. Plus a bare `R17-VALIDATE16` line in SCORECARD and in LOG.
- R17-PRODUCER-REV: `R17-PRODUCER-REV 000…0 111…1`, two non-commit hashes, in SCORECARD and in knowledge.
- R17-SUMS-RUNLOG: `carriers.tsv` **tampered** (one row appended), then a SHA256SUMS line matching the tampered blob. Plus `R17-SUMS-RUNLOG 7/8` in LOG.
- R17-REGISTRY: an empty `Write scope:` appended to the four 5th cells, and `probe` → `gate` in the citation-drift row.
- R17-S032-DIGEST: an S033 row whose cells are `x` except `fetch-time` (anchor) and `supersedes S032 — x` (teaches).

## Per-definition attack and stronger check

Each item lists the contract lines, then the cheapest flip, the gap, a stronger objective check, and how the prototype of that check behaved. The prototypes are scratch code, run at B and on the flip commit. "Rejects flip" means the stronger check stays red on `b4d1e7bb…`.

### 1. R17-PINMAP (`contract.md:29-32`)
- **Cheapest flip.** Two token lines, a stub QUALITY row and a comment containing `map_sha256`.
- **Gap (observation).**
  - Check (d) is a substring test, so a comment satisfies it.
  - Checks (a) and (b) accept the token on any line. The routed sites stay unqualified in place: knowledge `:30-32` "each pin map is retained … All maps are equal", `SCORECARD.md:2374` "pre/mid/post pin maps with instants", and `QUALITY.md:29` (#19 requires the map).
  - The forward fix cannot repair round-17 evidence (`ScoutPinmapSites.md:88`).
- **Stronger check.**
  - **P1 anchor-bound.** Each routed site named at `round-17-verifier-spotcheck.md:137` has a correction line carrying `R17-PINMAP` plus that exact anchor (`…r17-go-carrier-diagnostics.md:30`, `SCORECARD.md:2374`, `QUALITY #19`). The anchored line's bytes at REV must equal those at B, so the anchor still points at the corrected sentence.
  - **P2 AST.** The dict passed to `….setdefault("pin_checks", …).append(...)` in `carrier-run.py` has the constant keys `map_path` and `map_sha256` (B: `carrier-run.py:481`).
  - **P3 exercised.** At least one `.ufo/waves/round-18/runs/*/receipt.json` exists in which every `pin_checks[*].map_sha256` equals the sha256 of the blob at `map_path`. This is satisfiable only after the L1's C3 runs, which use W17 `carrier-run.py`. Plus a retained `receipt-validate` selftest result for the tampered-mid-map red case.
- **Prototype result.** P1 and P2: false at B, false on the flip (rejects the flip).

### 2. R17-VALIDATE16 (`contract.md:33-35`)
- **Cheapest flip.** A hand-written JSON file with eight int exits, plus two bare token lines.
- **Gap (observation).**
  - The check is **outcome-blind**: eight `exit: 1` close the defect.
  - Nothing binds the entries to the eight `da64646` receipt blobs or to the validator bytes.
  - The routed lesson site `round-17.md:122` has no required correction. A third unrouted site makes the same claim: `round-17.md:88` "all 16 receipts were validated".
- **Hazard (observation → inference).** Each receipt records absolute log paths, e.g. `…/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log`. The validator opens `ghidra.log` from those paths (`receipt-validate.py:150-158` at B). At B the worktree holds only `rea-ghidra-J5bcRT` for aether. A naive run would read pass-2 files at the same paths (`analyze.json` etc.) or miss the logs. The Validate16Run prompt does require a recorded remap. *Inference:* first-pass receipts predate `md5_pre` (counts below), so exits may be nonzero. Only the Validate16Run output can settle this.
- **Stronger check.**
  - **V1.** The summary's label set equals the 8 labels from `git ls-tree da64646 …/runs/*/receipt.json`. Each entry carries `receipt_blob` equal to that ls-tree id. `validator_sha256` equals the sha256 of `B:…/receipt-validate.py`. Each `stdout_sha256` matches a retained stdout blob at REV. `remap` is non-empty.
  - **V2 outcome-bound.** Let k = the number of entries with `exit == 0`. The SCORECARD and LOG correction lines carry `R17-VALIDATE16`, the literal `k/8` and the anchor `SCORECARD.md:2364`. A round-18 lesson line anchors `round-17.md:122` and `:88`.
  - **Strongest.** `W18/verify.py` re-executes the validator over the archived `da64646` receipts under the recorded remap and compares the exits (PROTOCOL "Claimed ≠ re-executed").
- **Prototype result.** V1 and V2: false at B, false on the flip (k=0 and no `0/8` stated).

### 3. R17-PRODUCER-REV (`contract.md:36-37`)
- **Cheapest flip.** Any two 40-hex strings next to the token.
- **Gap (observation).**
  - The hashes are not required to exist, to be ancestors, or to be the producers.
  - The check requires a correction in the r17 knowledge entry, which cites no measured source revision. Its only hashes are `da64646`/`2711674`, in the header.
  - Meanwhile the real "measured source revision" sites are `SCORECARD.md:2353-2355`, `LOG.md:2071` and `round-17.md:145`. LOG is not checked.
- **Stronger check.**
  - **R1.** Every hash on an `R17-PRODUCER-REV` line satisfies `git cat-file -t` = commit and is `merge-base --is-ancestor` of REV.
  - **R2.** The named set includes `95e34db62f2693c455d7ee4dfef24b8f3ebc007d` (pass-2 producer) and `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` (S).
  - **R3 truth.** `md5_pre` occurs 0× in `carrier-run.py` at `da64646` and at `95e34db`, and 2× at `d0ab299`. It occurs 0× in `B:runs/pro-aether/receipt.json` (observed below).
  - **R4.** Anchored corrections exist for `SCORECARD.md:2353` and `LOG.md:2071`.
- **Prototype result.** R1 and R2: false at B, false on the flip.

### 4. R17-SUMS-RUNLOG (`contract.md:38-40`)
- **Cheapest flip.** Tamper `carriers.tsv` and add a matching line, or simply add the honest line.
- **Gap (observation).** The check is **tautological**. It compares SHA256SUMS against `REV:carriers.tsv`, the very blob the same commit can change. Only `controls.py` (`contract.md:144`) would catch the tamper. The frozen manifest was regenerated at `95e34db`, which dropped the `carriers.tsv` line and added `replicate-expectations.json` (diff below). Restoring one line is not the same as restoring the freeze. `7/8` is a fixed token, not a derived count.
- **Stronger check.**
  - **S1.** Every line of `2711674:SHA256SUMS` is present byte-exact at REV. Every REV line verifies against its REV blob. `rev-parse REV:carriers.tsv` equals `rev-parse 2711674:carriers.tsv`.
  - **S2.** The LOG line carries `k/n`, where k is computed from `da64646:runs/run-log.txt` " end " lines (7) and n from the `da64646` receipts (8), plus the missing label `calib-shfmt`.
- **Prototype result.** S1: false at B, false on the flip. On a genuine-restore commit (`ec20268f…`, frozen line restored, tsv untouched) S1 is true and the contract check is true. S2 computes to `7/8`.

### 5. R17-REGISTRY (`contract.md:41-43`)
- **Cheapest flip.** Append an empty `Write scope:` to the four rows and relabel citation-drift as `gate`.
- **Gap (observation).** The routed defect (`round-17-verifier-spotcheck.md:145`) names **two** missing fields: "no pinned-value path or write scope". The check tests only the write-scope token, and an empty value passes. PROTOCOL row fields list `pinned-value path, write scope` separately (`PROTOCOL.md:401-403`). The column header is `Pinned values / write scope` (`SKILL.md:535`).
- **Stronger check.**
  - **G1.** The 5th cell has non-empty text after `Write scope:` *and* a pinned-values clause. Every repo path named in the cell resolves at REV (`git cat-file -e REV:path`).
  - **G2.** Kind `gate`, `--strict` present in the registered argv, and `0 clean / 1 failed` present in cell 3.
- **Prototype result.**
  - G1: false at B, false on the flip.
  - G2: false at B, **true on the flip**. This is correct: the relabel is the real fix (counter-finding above).
  - Calibration note: my first G2 draft also required removing the "probe semantics" sentence. That would have rejected the drafted cell, which keeps the sentence by design. I dropped that clause.

### 6. R17-S032-DIGEST (`contract.md:44-45`)
- **Cheapest flip.** An S033 row with `x` cells, `fetch-time` in the anchor and `supersedes S032 —` in teaches.
- **Gap (observation).**
  - S032's row keeps the unreproducible digest `436c0f63…` unqualified (`SOURCES.md:38`).
  - Its status may stay `mined`.
  - No retained fetch pair proves the instability.
  - The 11-cell regex is weaker than the lane's own validator.
- **Stronger check.**
  - **D1.** S032's status cell contains `superseded` (allowed by `contract.md:144`).
  - **D2.** `scripts/sources-census.sh validate --root … kaidoku` exits 0 at REV.
  - **D3.** A committed fetch-pair evidence file holds ≥2 differing sha256 values for the S033 URL with UTC times (`DraftS033Row.md:32` has `8a94af63…` and `dab89ce7…`).
- **Prototype result.** D1: false at B, false on the flip.

## Smallest safe correction (for the L1)

1. Keep `routed-defects.py`'s token checks as the **routing-ledger** layer. Report them as `named_correction_present`, not as "defect closed".
2. Add a second, independent count, `substance_closed`, built from P1/P2(+P3), V1/V2, R1/R2, S1/S2, G1/G2 and D1/D2/D3. Each obligation must derive from the routing document's anchors or from a Git-object computation, never from a token the writer chooses. Its red state at B is already observed above (all false).
3. Claim C1 as `open 6 → 0` **only if `substance_closed` is also 6**. Otherwise report both numbers, e.g. "6 → 0 ledger; k/6 substance". V2 makes the VALIDATE16 outcome explicit even when k < 8.
4. Selftest red cases to add: the flip commit above (all six token-only edits) must stay open under `substance_closed`. Add the SUMS tamper variant and the `exit: 1`×8 summary.

Impacted axes: calibration (the counter would overstate discharge), depth (three routed sites are uncovered: `round-17.md:88`, `LOG.md:2071`, S032's own row), operability (the remap hazard in any receipt re-validation).

## Supporting commands (read-only, run in LANE)

```text
git rev-parse refs/heads/main HEAD            → 9011581… 9011581… (exit 0)
git show B:…/carrier-run.py | grep -n 'map_sha256\|pin_checks'  → 413, 481 (no map_sha256) (exit 0)
git show B:…/predictions/carriers.tsv | sha256sum → 8ac38afe…3eb5
git diff 2711674 B -- …/predictions/SHA256SUMS → -carriers.tsv line, +replicate-expectations.json line (exit 0)
git diff --stat 2711674 da64646 -- …/tools/carrier-run.py → empty (exit 0)
md5_pre count in carrier-run.py: da64646 0, 95e34db 0, d0ab299 2; in B:runs/pro-aether/receipt.json 0 (grep exit 1)
git show da64646:…/runs/run-log.txt → 7 start/end pairs, calib-shfmt absent, no final exit line (exit 0)
git ls-tree -d B …/runs/pro-aether/logs/ → rea-ghidra-J5bcRT; da64646 → rea-ghidra-JpGezV
git grep -n 'all 16 receipts|All 16 receipts|16 receipts' B → SCORECARD.md:2364, corpus/lessons/round-17.md:88, :122 (+ unrelated waves hits)
git grep -n '436c0f63' B → corpus/SOURCES.md:38 (row) and spotcheck:147 only
git show B:SKILL.md | grep -n 'Pinned values / write scope' → 445, 485, 504, 535 (exit 0)
```

Scratch eval cells (Python, not committed): the contract-literal checker (B → 6, flip → 0), the stronger-check prototype (B and flip all false except G2-lite on the flip, S1 true on the genuine restore), and `shutil.rmtree` of the clone.
