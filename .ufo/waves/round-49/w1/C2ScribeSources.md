# C2ScribeSources — round 49, wave 1 (pre-freeze) — registry rows S147/S148 and the lesson Gate draft

## Verdict

**Drafts ready to fold; not freezable as-is for one counter item.** Rows S147 (fixes S145's locator) and S148 (fixes S146's rationale) are drafted, sha256-pinned to snapshots re-opened live at 2026-10-28T21:09Z, and pass the draft counter's atoms A6 and A7 on an overlay of the lane base. Census validation adds no finding. Three things L1 must decide before the freeze:

1. **A7 is vacuous for the teaches value.** The counter accepts a row that says `EX_USAGE is 2` as long as the digit `64` appears elsewhere in the teaches cell, and it does not require the lane-convention statement. Probe green (§F2). Fix before freeze (literal-token test; sketch in §F2).
2. **A8 is coupled to the S149 decision.** The gate rejects FreeBSD sysexits(3) as a candidate. If the search log counts it as excluded, the registry must carry it as a `rejected` row, or A8 reads `excluded 0` vs `1`. Both variants measured (§F3).
3. **Hygiene before the freeze.** `tools/round-49/__pycache__/` (three `.pyc`, 18:09–18:10 local) exists in the draft tree from ungated `python3` runs by a sibling seat. The freeze would commit them. Remove before FREEZE (§F5). This seat did not create them and did not delete them.

Also: rows S147/S148 cite `corpus/lessons/round-49.md`; the census validator exits 1 (E11) until that lesson exists, so lesson and rows must land in the same commit (§F4).

## Drafted artifacts (all under this seat's w1 dir; nothing under `corpus/` written)

| artifact | path (under `.ufo/waves/round-49/w1/C2ScribeSources/`) | sha256 |
|---|---|---|
| S147 + S148 rows (insert after the S146 line, registry line 152) | `rows.md` | `7e85b95e8bf1430f2812b69bececa2289e91653f2ba86552b69aa56c46941e75` |
| S149 candidate row (rejected; optional) | `rows-optional-S149.md` | `1eb9036795cc1f32455fd7f716a21a1ee2309108febeee701b76a8c10364f74a` |
| lesson `## Gate` block (S147 admit, S148 admit, S145/S146 untouched, closure disagreements, S149 reject) | `gate.md` | `e69ce8e6d72a9f7e7f5667238c945a7a193f749b3b43e7a17dd0641fad718b38` |
| snapshot S147 (land at `corpus/evidence/round-49/c2/popper.html`) | `staged/corpus/evidence/round-49/c2/popper.html` | `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` (118,135 bytes) |
| snapshot S148 (land at `corpus/evidence/round-49/c2/sysexits.html`) | `staged/corpus/evidence/round-49/c2/sysexits.html` | `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` (12,725 bytes) |
| S149 candidate copy (not a corpus snapshot) | `candidates/freebsd-sysexits-3.html` | `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` (59,251 bytes) |
| full candidate registry (scratch build, for L1 diffing) | `candidate-SOURCES-scratch.md` | `807f0d42dc01c02817630d8937f65adecd997402c0077ed4105f0e32ecca7db7` |
| overlay verifier (read-only; loads the draft counter without writing bytecode) | `verify/verify_rows.py` | `fff0a3995159bc3119cd8b03f32c489ff3961e596abda944ec2b4053af847596` |

Snapshot bytes are the draft snapshots in `.ufo/waves/round-49/draft/snapshots/` (identical sha256 to the live re-open; §R). The landing move is `cp staged/corpus/evidence/round-49/c2/* corpus/evidence/round-49/c2/` (create the directory); the sha256 pins in the rows match those bytes.

## Row content (what was drafted and why)

- **S147** (`supersedes S145`): same SEP page, tier A, `mined`, opened 2026-10-28, recheck 365d, used-by `corpus/lessons/round-49.md`. Anchor: heading `2. Backdrop to Popper’s Thought` (the heading above both quotes; they precede `3. The Problem of Demarcation`); quote 1 (22 words) `if a theory is incompatible with possible empirical observations it is scientific; conversely, a theory which is compatible with all such observations`; quote 2 (9 words) `it is consistent with all possible observations, is unscientific` (the consequential clause the closure asked for, which quote 1 cannot carry inside 25 words); SEP version `substantive revision Fri Jul 31, 2026` (the closure's "exact version anchor", present in the snapshot at the page head); sha256 pin.
- **S148** (`supersedes S146`): sysexits(3head) on the reachable man7 URL, tier A, `mined`. Anchor: `SYNOPSIS`; `#define EX_USAGE 64 /* command line usage error */` (9 words); version `Linux man-pages 6.19, 2025-09-21`; sha256 pin. Teaches: `EX_USAGE is 64`, and the lane's 0/1/2 exit meanings are its own convention, so no sysexits value grounds exit 2.

## Findings

Exit-code semantics as in the contract (0 met, 1 not met, 2 could-not-evaluate). Every command below was run at the times in §R.

| # | finding | severity | command (abbreviated; full paths under the seat dir) | exit | evidence (sha256 / value) |
|---|---|---|---|---|---|
| F1 | Rows S147/S148 pass counter atoms A6 and A7 on an overlay of lane base + rows + snapshots; genuine = green, all listed counterfactuals red as their atom | pass | `python3 -I -B verify/verify_rows.py > receipts/verify-rows.json` (counter loaded from `round-49/draft/tools/round-49/c2-mismatch.py`, counter sha `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`) | 0 | `receipts/verify-rows.json` `bd01ab17c20b93de6fd28ba6615a551c2ebe0881191c799fc8d7d466ed4bf9ea`; genuine `A6 green A7 green`; A6 snapshot edit → red (sha pin + quote); A6 wrong-heading anchor → red; A7 snapshot edit → red; A7 `EX_USAGE is 64`→`is 2` → red |
| F2 | **A7 is vacuous on the value.** A teaches cell `EX_USAGE is 2; EX__BASE is 64` is green: A7 checks `EX_USAGE` present and `\b64\b` present, not the claim. The convention-statement is not checked either (teaches with the 0/1/2 clause deleted is green). The battery's only A7 mutation (`is 64`→`is 2`) turns red only by removing the token `64`, so it cannot see this. | **medium** (calibration of the S148 claim) | same verify run; probes `PROBE A7 teaches says EX_USAGE is 2 and EX__BASE is 64` and `PROBE A7 teaches drops the lane-convention statement` | 0 (probes report green) | `receipts/verify-rows.json`: both probes `A7 green` with empty reasons. Suggested fold (not applied): A7 requires the literal `EX_USAGE is 64` in `c[6]` and the token `convention` in `c[6]`; add a battery mutation that changes `64` to `2` inside the literal and asserts red. |
| F3 | **A8 couples to the S149 decision.** A8's derived `excluded` counts new registry rows whose status is `rejected`. Gate's S149 reject is only in prose unless it is a row. | medium (search-log seat) | `python3 -I -B -` (importlib load of the draft counter; `m._derived(ov, m.LANE_BASE, 'REVX')` over overlays of the two candidate registries; full text in `receipts/a8-derived.txt`) | 0 | `S147+S148 only → (146, 148, 2, 0)`; `S147+S148+S149 → (146, 149, 2, 1)`. L1 must choose: add `rows-optional-S149.md` (search log: excluded 1), or leave it out (search log: excluded 0, no excluded claim). Do not count it in the log without the row. |
| F4 | **Landing order.** S147/S148 `used-by` `corpus/lessons/round-49.md`, which does not exist in the base. Census validate exits 1 with E11 until it lands. | medium (ordering) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/root/corpus/SOURCES.md --today 2026-10-28` | 1 (scratch root) | `receipts/val-root-full.tsv` (sha `806284cd3c02246e529e95557f45af5f6a3eddd57da55493a182dea3c5d20ff3`) is identical to the base run `receipts/val-base-full.tsv` (`diff` exit 0): candidate adds no finding. Remaining E11 are three scratch-root files absent from the scratch tree (`SKILL.md`, `corpus/QUALITY.md`, `tools/round-27/xpin-attribute.mjs`). Lane HEAD validate `… --file /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` returns `file ok` exit 0. Land the lesson and rows in one commit. |
| F5 | **Pycache in the draft tree.** Three `.pyc` under `round-49/draft/tools/round-49/__pycache__/` (`c1-counter`, `c1-run`, `c2-mismatch`, mtimes 18:09:53–18:10:36 local). Not created by this seat (my imports used `-B` and `sys.dont_write_bytecode`). A FREEZE commit that includes `tools/round-49` would freeze them. | medium (hygiene) | `find …/draft -name __pycache__` | — | L1: `find .ufo/waves/round-49/draft/tools/round-49 -name __pycache__ -exec rm -r {} +` before FREEZE; run tools with `-B` thereafter. |
| F6 | **S146 cannot be repaired in place.** Closure routed defect 3 asked for `REJECTED: <reason>; flip: …` teaches shape on S146; A7 requires S146's line byte-identical to the base, so the shape stays non-conformant. Recorded open in `gate.md`. | low-medium (quality; frozen-rule conflict) | `grep -n '^| S146 ' corpus/SOURCES.md` vs base | — | S146 unchanged; decision for L1: accept as open, or let A7 allow a supersession-only line. |
| F7 | **A6 accepts any anchor that also names a wrong heading** as long as the right heading is present (containment, not nearest-heading). | low | `verify/verify_rows.py` probe `PROBE A6 anchor names the WRONG S145 heading AND the right one` | 0 (probe green) | `receipts/verify-rows.json`. Not exploitable against the drafted rows; cosmetic misleading anchor only. |
| F8 | **Tier A forced by the counter.** A6/A7 require `c[3] == 'A'`. The man7 mirror of sysexits is a derivative (Linux man-pages of a BSD header); tier A is defensible because the page reproduces the header's `#define` lines and the lane's convention claim is not taken from it. A tier B judgment would make A7 red. | low (judgment, disclosed) | counter source, `a7` / `_snapshot_row` | — | Disclosed in `gate.md` row S148. |
| F9 | **Snapshot provenance is pinned, not receipted.** The counter binds bytes by sha256 only; the URL, status and instant live in this seat's `receipts/reopen.tsv`, not in the corpus. | low | `receipts/reopen.tsv` `67b8f0e445023a827778c75e04a48997d1c5434a57b92a2bdeed11cff63b3bd8` | — | L1 may commit `reopen.tsv` next to the snapshots (not read by the counter). |
| F10 | Census numbers after the rows: rows 146→148, tier.A 136→138, status.mined 139→141, rejected unchanged 7. S149 variant: rows 149, tier.A 139, mined 141, rejected 8. | info | `bash …/sources-census.sh census --file <scratch>/root/corpus/SOURCES.md --today 2026-10-28` | 0 | `receipts/cen-cand.tsv` `1daa0062ac6fe78b1c0e74a48d83546b0ca2306fe4737a1728312ac348d9b32d`; base `receipts/cen-base.tsv` `45fbe81148408d6f9fcf62e57794d9f4999f1dfe889ad4524f70d0390d6f47d0` |
| F11 | Quotes re-checked independently against the snapshot bytes (tag-stripped, whitespace-normalized): all four present, word counts correct. | pass | inline `python3 -I -B -` check | 0 | Q1 22 words present; Q2 9 words present; S148 `#define` line 9 words present; S149 candidate 23 words present |

## Closure disagreements: disposition

- S145 locator (closure: wrong section): **corrected by S147**; the clause sits under §2 `Backdrop to Popper’s Thought`, not §3. Verified by the A6 wrong-heading probe going red (F1).
- S145 "consider the consequential clause, cite an exact version": **done in S147** (second quote; SEP `substantive revision Fri Jul 31, 2026`).
- S146 rationale and flip (closure: "no locator exists", wrong flip): **corrected by S148** (reachable `sysexits.h.3head.html`, `EX_USAGE 64`).
- S146 teaches shape (closure: missing REJECTED form): **not repaired; frozen by A7** (F6).
- Decision-level: both admit and reject decisions reconfirmed in substance; the annotations are what changed.

## Re-open (§R)

All four URLs fetched with `curl -sS -L -m 60 -A 'Mozilla/5.0 (kaidoku-r49 reopen)' -o <bin> -w '%{http_code} %{size_download} %{url_effective}' <url>`, exit 0 each, UTC instant per line in `receipts/reopen.tsv`:

- `https://plato.stanford.edu/entries/popper/` → 200, 118,135 bytes, sha `2c2d48c6…` (byte-identical to the draft snapshot).
- `https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` → 200, 12,725 bytes, sha `d9db4b96…` (identical).
- `https://man7.org/linux/man-pages/man3/sysexits.h.3.html` → **404**, 196 bytes, sha `80c3fe2a…` (closure value confirmed).
- `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3` → 200, 59,251 bytes, sha `1fc793a2…` (S149 candidate).

## Checks not run

- The full draft counter on a REV (`c2-mismatch.py --rev … --battery`) was **not run**: it needs the whole round-49 lesson, SCORECARD record and search-log entries, which are other seats' outputs. Only A6 and A7 were exercised.
- Census `validate` against the real lane root with the candidate was **not run**: that would require writing into the lane; the scratch-root comparison in F4 is the substitute (identical findings to base).
- No data run, no `c1-run.sh --data-run`, no commit, push, stage, or mutating git in the lane or fleet repo.

## Tooling

None installed or updated. `curl`, `python3`, `gawk` (used by the census script), `git` read-only subcommands (`show`, `cat-file`, `rev-parse`). No pacman.

## Scratch

`/fast/scratch/hyaku/kaidoku-r49/C2ScribeSources` removed after the receipts were copied into this seat's w1 dir.
