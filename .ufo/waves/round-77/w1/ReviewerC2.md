# ReviewerC2 — R77-C2 independent re-derivation, base 188562d4

Seat: ReviewerC2-9 · 2026-11-04 · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Instrument: `tools/round-77/prefile-receipt.py`, sha256 `174eedb56369414f5e4310afa9fe5ee6400e5145e4801452c9d21a7abac2d3fd`
— byte-identical in working tree, declaration `819cf30e`, and the freeze pin in `.ufo/waves/round-77/claims.json` (`instruments` map). I measured the pinned bytes.

## Verdict (one line)

The frozen base predicate for R77-C2 **reproduces exactly** (exit 1, `arms_ok 4 of 6`, `validate.defects []`, selftest 13/13); every arm's observation was independently confirmed, with **one claim-text imprecision** (the base reason clause says "three" round-76 gate receipts lack `exit`; five do) and **one structural trust gap** (receipt stdout provenance and `rev` are taken on trust — a self-consistent forged filing receipt would satisfy arm A2).

## 1. Fresh battery run (my own work dir)

```
python3 -I -B tools/round-77/prefile-receipt.py --root . --rev 188562d4 \
  --work /fast/scratch/hyaku/kaidoku-r77/ReviewerC2-9/w --battery \
  --json-out /fast/scratch/hyaku/kaidoku-r77/ReviewerC2-9/c2.json
→ exit 1, arms_ok 4, arms_total 6, ok false, validate {arms 6, defects []}
```

Receipt filed at `.ufo/waves/round-77/w1/ReviewerC2-9/c2.json`.

| arm | met | observed (verbatim) |
|---|---|---|
| clone-run | true | `rc 0, prefile: PASS, receipt_defects []` |
| record-receipt | false | `.ufo/waves/round-77/l1/scores/prefile-at-filing.json absent at 188562d4` |
| gate-exits | false | `round-76: 5 gate receipts, missing ['.ufo/waves/round-76/l1/scores/gate-at-freeze.txt: no exit', '…gate-at-record.txt: no exit', '…gate-at-tip.txt: no exit', '…gate-disclosures.txt: no exit', '…gate-selftest-at-tip.json: no exit']` |
| red-no-exit | true | `defects ['missing key exit']` |
| red-verdict | true | `defects ["passed True disagrees with exit 1 and verdict 'FAIL'"]` |
| red-rev | true | `defects ["rev '0000000000000000000000000000000000000000' is not the expected '509c105140e90f7299b024796914e2639c206cb9'"]` |

Selftest: `cases 13, failures []`, exit 0 — matches the frozen "13 cases" and carries both red fixtures (red-no-exit/verdict/digest/rev/env/argv/line/empty-stdout, red-battery-ok/arms) and legitimate look-alikes (green-genuine, green-fail-receipt — a FAIL receipt is a valid receipt, verdict-anchored — prose "prefile: PASS is what we want" is not a verdict).

## 2. Arm-by-arm verification

(a) **clone-run really ran on a clean clone.** The arm's receipt binds `rev 188562d43e3cc58b217ad7aa763fb296c5b8a0b7` (full base sha), argv `bash <scratch>/w/clone-run/lane/tools/round-29/prefile-check.sh <scratch>/w/clone-run/lane`, `env_keys [HOME, LANG, PATH, TMPDIR]`, stdout digest `aab2e357…46f990` which I re-derived independently from the stdout bytes (matches). I additionally made my own independent clone (`git clone --no-checkout` + `checkout --detach 188562d4`): `rev-parse --show-toplevel` = the clone dir, `HEAD` = `188562d43e3c…`, `git status --porcelain` **empty**. The battery's clone receipt re-checked via the CLI (`--check-receipt --expect-rev 188562d43e3c…`) → `defects []`, exit 0.

(b) **filing receipt really absent at base.** `git show 188562d4:.ufo/waves/round-77/l1/scores/prefile-at-filing.json` → `fatal: … exists on disk, but not in '188562d4'` (exit 128); `git ls-tree -r 188562d4 -- .ufo/waves/round-77` is empty. A2's red is genuine committed-tree absence, not a working-tree artifact.

(c) **round-76 gate receipts really lack `exit`.** `git ls-tree -r --name-only 188562d4 -- .ufo/waves/round-76/l1/scores` yields 17 files; five match the arm's `gate-[^/]*\.(json|txt)$` glob. Per-file `grep -cE '"exit"\s*:|^exit='` over `git show 188562d4:<path>`:

| path | carries_exit |
|---|---|
| `.ufo/waves/round-76/l1/scores/gate-at-freeze.txt` | false (grep count 0) |
| `.ufo/waves/round-76/l1/scores/gate-at-record.txt` | false (grep count 0) |
| `.ufo/waves/round-76/l1/scores/gate-at-tip.txt` | false (grep count 0; body is the R29-freeze-gate disclosures JSON, no exit field — routed defect 3 confirmed) |
| `.ufo/waves/round-76/l1/scores/gate-disclosures.txt` | false (grep count 0) |
| `.ufo/waves/round-76/l1/scores/gate-selftest-at-tip.json` | false (grep count 0; it is a round-76 plan-command selftest receipt, 7 cases, no exit key — it matches the glob only by filename) |

(d) **each red fixture refused for its declared reason.** red-no-exit → `missing key exit`; red-verdict → defect containing `passed` ("passed True disagrees with exit 1 and verdict 'FAIL'" — the genuine run on the working tree is FAIL/exit 1 because SKILL.md is modified); red-rev → defect containing `expected`. All three refusal shapes are the declared ones; no collateral defects.

## 3. `check_receipt`: re-derived vs trusted

**Re-derived from receipt bytes alone:** (1) presence of all 8 required keys (`rev, argv, exit, passed, prefile_line, stdout, stdout_sha256, env_keys`), early-return on absence; (2) `exit` is an int and not a bool; (3) `stdout` is a non-blank string; (4) `stdout_sha256` == sha256 of the stdout bytes; (5) `prefile_line` == the last `^prefile: (PASS|FAIL)$` line of stdout (anchored, per-line stripped); (6) at least one such verdict line exists; (7) `passed` == (`exit == 0` and token == `PASS`); (8) `argv` is a string list with an element ending in `tools/round-29/prefile-check.sh`; (9) `env_keys` == exactly the sorted four-key allowlist; (10) when `--expect-rev` is supplied, `rev` equals it.

**Taken on trust** (forgery probes, module imported and exercised directly):
- **F1 — stdout provenance: TRUSTED.** A fully self-consistent receipt whose stdout no run ever produced (fabricated `prefile: PASS` text, matching digest, PASS verdict, exit 0, four-key env_keys) → `check_receipt` returns `[]`, accepted. The digest binds stdout to itself, not to a real execution. (My first, sloppier forgery that kept `prefile_line: prefile: FAIL` under a PASS stdout *was* refused — but by clause 5's internal consistency, not provenance.)
- **F2 — rev: TRUSTED unless a caller passes `--expect-rev`.** Same self-consistent body with `rev = "f"×40`, no expect_rev → accepted. Shape of rev is not even checked. **The battery never passes expect_rev** for A1's clone receipt or A2's filing receipt — only the red-rev arm exercises it.
- **F3 — exit-0-with-FAIL-verdict look-alike:** exit 0, `prefile: FAIL`, `passed false` is internally consistent → accepted by `check_receipt` (correct: a failing run's receipt is valid evidence); `--filing` separately refuses it, but nothing re-derives that a committed filing receipt came from `--filing`.
- **F4 — wrong rev with expect_rev:** refused, as declared.
- env_keys records key **names only** (values never enter the receipt — round-72/QUALITY-128 clean); that the four keys reflect the actual child environment is trusted.

## 4. Landing target analysis

The landing target is exit 0 = every arm met + `validate.defects []`, i.e. `arms_ok 6 of 6`:

- **A1 clone-run:** gate must run in a clean shared clone at the landing rev with rc ∈ {0,1} and a well-formed receipt (base already does: rc 0, PASS). No new requirement.
- **A2 record-receipt:** `.ufo/waves/round-77/l1/scores/prefile-at-filing.json` must be **committed** at the measured landing rev, parse as JSON, pass `check_receipt` (self-consistency only), and carry `exit == 0`. Note: not bound to the landing rev (no expect_rev) and not bound to a real run (F1) — see risks.
- **A3 gate-exits under the newest-round-dir rule:** at any landing rev containing `.ufo/waves/round-77/` files, `latest_round_dir` resolves to `round-77` (numeric max of `round-\d+` dirs). A3 then inspects **only** `.ufo/waves/round-77/l1/scores/gate-*.(json|txt)` and requires ≥1 match, every match carrying `exit` (JSON int key or `^exit=N$` line).

**Answer: yes** — a committed filing receipt with exit 0 (self-consistent) plus round-77's own gate receipts all carrying `exit` would satisfy the landing target, because the newest-round-dir rule drops round-76's five exit-less receipts from inspection entirely. The repair is prospective; nothing in the claim amends round-76. Two conditions are easy to miss: round-77's scores dir must contain **at least one** `gate-*.json|txt` (empty glob ⇒ `bool(gate_files)` false ⇒ arm red), and `gate-record-raw.log`-style `.log` files are outside the glob (uninspected by design).

## 5. Findings by severity

- **[Medium] Claim-text undercount in the frozen base clause** — the frozen sentence (claims.json `claims[1].predicate`, the instrument's `PREDICATE` constant, and the assignment text all byte-agree) says base is red because of "the filing receipt absent and **three** round-76 gate receipts without exit". The gate-exits arm and my independent grep show **five** round-76 gate receipts without exit (the three `gate-at-*.txt` plus `gate-disclosures.txt` and `gate-selftest-at-tip.json`). The arithmetic conclusion (`arms_ok 4`, exit 1) is unaffected — two arms are red either way — but the enumerative count is wrong as stated. Recommend an erratum note at landing; do not rewrite the frozen sentence.
- **[Medium] A2/filing-receipt provenance is trusted, not re-derived** — a committed, self-consistent, hand-written filing receipt (never-run stdout + matching digest + exit 0 + any rev) satisfies A2 and the landing target. This is the same "cited as green" class as round-76 routed defect 1, one step stronger (self-consistent but unbound). A one-line strengthening would be `check_receipt(receipt, expect_rev=rev)` in arm A2 — but that changes a frozen arm definition, so it is the L1's call, not mine. Until then, the real provenance anchors are the `--filing` refusal semantics and the A1 live clone run.
- **[Low] A3 glob escape hatch** — `gate-*.(json|txt)` only; a `gate-*.log` (round-77's scores dir already has `gate-record-raw.log` on disk) escapes the exit requirement. Frozen arm definition; noted as residual risk, not a defect.
- **[Low] LANG portability** — `env_keys` must equal the four-key allowlist of *non-empty* keys; on a host with `LANG` unset, every A1 receipt would be refused (`env_keys … not the four-key allowlist`) for environmental, not instrument, reasons. My host sets LANG; arm green here.
- **[Info] A1 "runs clean" means well-formed, not PASS** — rc ∈ {0,1} with a verdict line passes the arm; a FAILing clone at a future landing would still count as met. The observed text carries the rc and verdict line, so the receipt stays honest.

## Residual risk / verification gaps

- I did not (and could not) measure any landing rev — none is committed yet; the landing analysis is rule-derived from the instrument source, not a measurement.
- I audited only R77-C2 (`prefile-receipt.py`); `verdict-bind.py` / R77-C1 is out of my seat.
- The freeze summary references "the two base receipts"; I searched the frozen claims.json recursively for battery-schema receipts and found none embedded — they presumably live in the claims rows' evidence cells under other schemas. Unverified by me; my base reproduction stands independently.
- The L1's working tree churned during my run (SKILL.md modified; `prefile-at-filing.json` appeared untracked, then was absent from the scores dir listing minutes later). My verdicts read committed tree objects only and are unaffected.

## Evidence index (all under the lane)

- `.ufo/waves/round-77/w1/ReviewerC2-9/c2.json` — my full battery receipt (base).
- `.ufo/waves/round-77/w1/ReviewerC2-9/clone-receipt.json` — A1's clone-run receipt, re-checked via CLI with `--expect-rev`, defects [].
- Commands of record: battery/selftest as in §1; `git show 188562d4:…` probes as in §2(b)(c); forgery probes exercised `check_receipt` directly on the pinned instrument.
- Tooling: no installs, no upgrades; stock `python3`, `git`, `coreutils`. Scratch `/fast/scratch/hyaku/kaidoku-r77/ReviewerC2-9/` deleted after receipt copy; no pacman; no writes outside the lane evidence dir and scratch.
