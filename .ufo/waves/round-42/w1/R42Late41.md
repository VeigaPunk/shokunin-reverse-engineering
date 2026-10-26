# R42Late41 — inherited round-41 state: disposition of uncommitted wave-2 files and closure-D2 pointer

**Verdict: DONE** — every closure-D1 leftover is resolved at HEAD `fdabdfa4` (committed in `ae5dc3f3` or removed as stray; zero round-41 paths uncommitted, zero round-41 paths touched by the round-42 launch), closure-D2 is resolved (`.ufo/waves/round-41/w2/R41W2C2Table.md` exists, is committed, and supports the citing sentence), and all 33 `w2-dispatch.json` seats have a committed report. Two residual routing gaps for the L1 before the freeze (F-1, F-2 below), both LOW/documentation.

Attacked: the closure `corpus/lessons/round-41-verifier-spotcheck.md` D1/D2 claims against the live tree and the commit history since tip `740644747865`; per-path authorship by mtime vs report commit `4c87e06d` (2026-10-26 18:29:41 -03) and closure commit `c4a38ea2` (18:31:27); per-late-report content vs the committed round-41 record; dispatch-seat ↔ report-file coverage. Read-only: `git status/log/show/diff/ls-files`, `ls -la --time-style=full-iso`, `jq`, `find -newermt`. No VCS mutation; no lane write outside my report and artifacts dir.

## 1. Commit scaffold since the round-41 tip

| commit | author date | committer date | what |
|---|---|---|---|
| `c4a38ea2` (protocol-shokunin) | 18:31:27 -03 | — | the verifier spot-check itself (closure) |
| `ae5dc3f3` (kaidoku-shokunin) | 18:36:04 -03 | **18:44:28 -03** | "round-41: wave-2 settled — remaining reports, results ledger, lesson wave-2 section" |
| `fdabdfa4` (kaidoku-shokunin) | 18:50:50 -03 | — | round-42 launch; `git show --name-only \| grep round-41` → **empty** |

## 2. Per-path disposition (closure-D1 inventory)

At closure the status carried 2 tracked edits + 16 untracked lines. Today `git status --porcelain --untracked-files=all` shows **only round-42 w1 paths** (16 lines under `.ufo/waves/round-42/`); `.gitignore` covers only `__pycache__/`+`*.pyc`, so nothing is hidden.

| closure path | who wrote it / when | final or partial | consistent with the committed record? | disposition (what actually happened) |
|---|---|---|---|---|
| `M w2/R41W2ReproV4.md` | seat R41W2ReproV4; mtime 18:28:44, after report commit `4c87e06d` 18:29:41 era | final report (terminal CONFIRMED + artifacts + ledger entry) | yes — the edit corrects its own harness-failure wording EPIPE→E2BIG (146,561-byte `--argjson` over `MAX_ARG_STRLEN` 131,072), matching round-41.md M41-5 | **committed as round-41 evidence** in `ae5dc3f3` (+3/-1; diff in artifacts) |
| `D w2/artifacts/R41W2Reservation/tx-exec-calls.json` | seat R41W2Reservation artifact, tracked at `74064474` | evidence file (final; superseded on disk by the seat's `tx-exec2.json`, also committed) | yes — `git diff 74064474..HEAD` on the file is **empty** | **restored to committed bytes, never committed as a deletion**; `git log` last touch `74064474`. Committed evidence stands |
| untracked `w2/R41W2C1Rescore.md`, `R41W2C2CounterMut.md`, `R41W2Reservation.md` | three late wave-2 seats; mtimes 18:30:46 / 18:31:00 / 18:30:57 (after report commit, at/before closure commit 18:31:27) | final reports — each opens with a terminal verdict and full method/evidence; each has a structured ledger entry in `r41-w2-results.json` | yes — see §3 | **committed as round-41 evidence** in `ae5dc3f3` |
| untracked late artifacts (InterpMut, Table, Reservation, C1Docs, C1Mutants trees) | the corresponding seats | final artifacts | yes — spot-checked Table probes (`divergence-results.json`, 9 `env-*.json`) match the report's executed table verbatim | **committed** in `ae5dc3f3` (the 247-file diff) |
| untracked `.ufo/waves/round-41/w2.ready.dispatched` | wave launcher marker | bookkeeping | n/a | **committed** in `ae5dc3f3` |
| untracked `r41-w2-results.json` (206 lines) | L1 settlement ledger | final | 33 entries = 33 seats; verdicts consistent with each report's own (see `ledger-verdicts.txt`) | **committed** in `ae5dc3f3` |
| stray `green.err`/`red.err`, lane root | not a seat report; untracked; mtime not preserved (files gone) | stray (redirect fragments, cited by closure D1) | n/a | **deleted (stray)** — correct per closure D1 |
| stray `green.err`/`red.err`, `corpus/evidence/round-41/c1/V4/` | same | stray | n/a | **deleted (stray)** — correct per closure D1 |

Stray-deletion attribution: the files are gone and were never tracked (they appear in no commit, and `git diff --name-status 74064474..HEAD` has no D/T entries). The lane-root and V4 directory mtimes are **identical to the nanosecond** — `18:44:18.003442569 -03:00` — one cleanup instant 10 s before `ae5dc3f3`'s committer timestamp `18:44:28`, and both paths were off-limits to seats (bounds forbid lane-root and `corpus/` writes). **[INFERENCE]** the L1 (kaidoku-shokunin) removed them during the settle commit; the filesystem alone cannot name the actor.

Non-item checked: `unblob.log` in the lane root is **not** a round-41 stray — tracked since round-38 `7a1ac7fe` ("misroot unblob.log"), worktree clean. Leave as committed round-38 evidence.

## 3. Late reports vs the committed round-41 record

- `R41W2C1Rescore.md` — CONFIRMED; R41-C1 met at `e9a24d07` **and** `e1c83313`; matches the lesson's wave-2 section verbatim ("re-scored met at e9a24d07 and e1c83313").
- `R41W2C2CounterMut.md` — DEFECTS FOUND; the one-line `declared` mutant flips NOT MET→MET (52/52, exit 0) with the 70-case selftest passing; 19/29 mutants killed. Matches the lesson sentence and closure §R41-C2.
- `R41W2Reservation.md` — CONFIRMED, zero reservation hits by four routes; matches the lesson sentence.
- `R41W2C2Table.md` — DEFECTS FOUND (1 MEDIUM F1 dep-missing-le cause cell, 3 LOW, 2 INFO); the lesson's tail already cites it for exactly the F1 MEDIUM. Supports D2 — see §4.

## 4. Closure D2 — the dead pointer is alive and supports the sentence

`corpus/lessons/round-41.md` R40-CL5 row: "fixed in prose | block 20 cause cells, no embedded table copy, layout pre-check, block-18/19 sentences; reviewed `w2/R41W2C2Table.md`". At closure the file was neither committed nor on disk; it is now on disk (mtime 18:38:22) and **committed in `ae5dc3f3`** (113 lines). Its §6 walks the R40-CL5 ledger item by item (M1–M3, L1–L7) against the frozen bytes at `e9a24d07` and confirms every item repaired — precisely the four sentence groups the citing row names — while filing new residues (F1–F4). The pointer is supported; no erratum needed.

## 5. Seats with no report file: none

`w2-dispatch.json` `.taskCall.tasks[].name` = 33 seats; `git ls-files .ufo/waves/round-41/w2/` contains the same 33 `R41W2*.md` files, 1:1 by name, all committed (`ae5dc3f3` for 7 late ones + the rest at `74064474`). The results ledger has 33 entries; 29 carry structured JSON verdicts, 4 (Freeze, Reservation, Sibling, Simplify) are plain strings whose verdicts I read from their `.md` headers (CONFIRMED / CONFIRMED zero-hits / DONE / DEFECTS FOUND).

## 6. Residual findings for the L1 (pre-freeze; LOW, documentation routing)

- **F-1 — the late C1Rescore calibration defects are committed evidence but routed nowhere.** `R41W2C1Rescore.md` D1 (counter compares (rel, sha256), not size — closed in fact), D2 (predicate's `--max-depth 1` never asserted directly; depth-3 rejected only incidentally via REA's 8 MiB report cap), D3 (PROVINCE Core row "four frozen carriers **no extractor** touched before the freeze" overstates — wave 1 ran `sasquatch-v4be` directly on V3/V4 for the oracle; the claims' "no REA or unblob" wording is the precise one), D4 (observation: `run_provenance_ok` is a path-shape token test). The lesson's "Open C1 limits" lists four *other* items and closure D5 lists three *other* omissions — D1–D4 appear in neither (the lesson predates the report by ~2 min). The round-42 draft absorbs D1 (P42-C1 binds "same sha256 **and size**"); D2 and D3 have no draft provision. Route them in the freeze (routed-defect row or erratum) or they die with the round-41 entry.
- **F-2 — ReproV3's exact-path wording recommendation is ledger-only.** The ledger's `depth_notes` recommend "strip one `$output/` from each path, **including the derivation root**" (literal reading of the rule would score V3 0/8); it is not in closure D5, and the round-42 draft's C1 predicate says "segment-bounded per round-41 closure D5". The v4 counter should state the strip explicitly.
- M41-4 (post-commit artifact edits) did **not** recur: `find .ufo/waves/round-41/w2 -newermt '2026-10-26 18:44:28'` → empty; the three late-mtime reports (18:38:22/18:40:44/18:43:24) all predate the commit instant 18:44:28, and worktree bytes equal HEAD everywhere (clean status).

## 7. Out-of-scope observation

The 16 untracked paths under `.ufo/waves/round-42/` at audit time (`w1-validate.out`, `w1.ready.dispatched`, `artifacts/R42AssimIds/*`, `artifacts/R42ScoutCalib/*`, `w1/swarm-registry.json`) are in-flight round-42 wave-1 work owned by the L1 and the launching seats — listed here only so the next status reader does not mistake them for round-41 residue.

## 8. Tooling record

No tool installed, upgraded, or removed; no pacman transaction. Used only: `git` (read-only subcommands), `ls -la --time-style=full-iso`, `find -newermt` (lane only, not under /fast/scratch), `jq`, `head`. Scratch `/fast/scratch/hyaku/kaidoku-r42/R42Late41*` removed before yielding.

## Artifacts

- `artifacts/R42Late41/evidence.md` — verbatim commands and outputs (status, commits, mtimes, per-file attribution, post-commit-write check, dispatch coverage, ReproV4 delta, unblob.log check).
- `artifacts/R42Late41/ledger-verdicts.txt` — 33 seat verdicts (29 ledger JSON + 4 from report headers).

Seat R42Late41 (leaf). Report path relative to lane root: `.ufo/waves/round-42/w1/R42Late41.md`.
