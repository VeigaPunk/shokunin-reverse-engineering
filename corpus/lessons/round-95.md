# Round 95 — lesson: a receipt is bound to the world it claims, and a frozen gate must be shown to fail on the mechanism it names

Declaration `4bda1d1dd3788973f10e61212b70df18b3b14ea0` (`plans/round-95-claims.md`, `.ufo/waves/round-95/claims.json`, pins in `.ufo/waves/round-95/pins.sha256`); base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`. Wave `r95-w1` (eleven seats, one v1 wave, band 8–16; see `## Wave r95-w1 — seat results`). Claims: R95-C1 (calibration, measured: receipt binding and symlink-safe writing) and R95-C2 (depth, measured: craft block 34). Measured revisions: both claims measured at the declaration `4bda1d1d` (the instruments and the honest run); the craft block and the knowledge entry landed after the freeze, and the C2 counters are re-run at the landing worktree (`--worktree`, recorded in the report).

## Motive

Round 94 closed with two verified claims and four routed defects (its spot-check and lesson, `corpus/lessons/round-94.md` `## Mistakes`): the agreement counter admits a consistently rewritten label pair and a fabricated triple (M94-e); the base receipts carry a short `--rev` that nothing validates (M94-f); the v4 receipt writer follows a symlink planted at the predictable `<json-out>.tmp` name (SentinelWrite F1); and the round-94 kill rule ran only the public runs, so a helper-only selftest could still be green while the public path was not. Round 95 takes the first three as its claim and the craft row for the class as its second.

## Gate

Source opened this round (CORPUS.md rule 1). Access date 2026-11-05 for each.

| row | URL | access date | HTTP / bytes / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S320 (new) | https://man7.org/linux/man-pages/man2/open.2.html | 2026-11-05 (opened this round; two byte-identical fetches) | 200 / 76506 / `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`; page footer "Linux man-pages 6.19" | "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP" (the `O_NOFOLLOW` entry; exact after tag-stripping and whitespace normalisation) | the trailing-component rule that makes a predictable `<json-out>.tmp` an escape path and that `mkstemp`'s `O_EXCL | O_NOFOLLOW` open removes; R95-C1's writer and R95-C2's craft row |

Fetch evidence: `.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html` and `s320-open2-fetch2.html` (committed in the declaration); the seat re-fetch is `.ufo/waves/round-95/w1/ScoutS320/s320-recheck.md`.

Admit / reject. Admitted: S320 (the `O_NOFOLLOW` trailing-component rule), used by `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` and the craft block. Not admitted from the same page: the `O_PATH` interaction and the other `O_NOFOLLOW` occurrences (the page states the flag five times; only the description carries the rule). The `mkstemp` `O_NOFOLLOW` flag is measured on this host (`inspect.getsource(tempfile)`), not sourced from a row, and is recorded as a measurement in the knowledge entry.

Row changes (CORPUS.md rule 2): S320 appended (`mined`, opened 2026-11-05, recheck `on-release`). No existing row edited.

Assimilation: `Assimilation: none` (`merge/kaidoku/` absent; the lane has no `considerthese/` directory).

## Measured

**R95-C1 (calibration) — verified on the frozen predicate at `4bda1d1d`; named limits below; no kill-rule clause fired.**

- Before (do-nothing controls, committed in the declaration, `.ufo/waves/round-95/pre/`): the pinned round-94 agreement counter over the four committed forgeries prints `counts_of_4` valid 4, agree 4, predicted 4, `met true`, exit 0 (`c1-old-counter-admits-at-base.json`). The pinned v4 writer with the planted `<json-out>.tmp` symlink: `victim_intact false`, verdict `followed-symlink`, receipt valid (`c1-symlink-v4-at-base.json`).
- After (the strengthened instruments at `4bda1d1d`): `python3 -I -B tools/round-95/c1-forgery-refusal.py --root . --fixtures .ufo/waves/round-95/forgery --old-prefix forge --old-counter tools/round-94/c1-receipt-agreement.py --honest-dir .ufo/waves/round-95/l1/scores --honest-prefix honest --world-rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --instrument-rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect '<frozen label>' --json-out .ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json` → exit 0: `forgeries refused 4 of 4; before admits True; honest accepted True`. Each forgery carries exactly its intended reason: `forge-pos` → `label-not-frozen`, `forge-F1` → `label-not-recomputed`, `forge-F2` → `revision-not-bound`, `forge-F3` → `pins-not-bound`.
- Honest public run: `stop-boundary-repair-battery-v5.py --json-out` → exit 0, stdout `selfverify ok=True reasons=0` then `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0` (`honest-pos.json/.stdout/.rc`).
- Symlink probe on v5: `symlink-probe.py` → exit 0, `victim_intact true`, `receipt_valid true`, verdict `hardened` (`c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`).
- Independent reproduction (ExecRepro, own clone): label, counts, class, `counter_sha256`, rc, stdout and the forgery battery's full JSON match the committed receipts. The honest receipt's full JSON differs only in the fresh-provenance `nonce` and the `fresh_packed_sha256` values, which are per-run random (nonce `8996258291ee0a2a` vs `3b1961c96a2fe80d`); the labels and the fresh-cell classes match. ReviewerV5 re-ran all four selftests (rc 0) and the frozen commands (rc 0 each).
- Named limits found by the wave's attacks are **outside the frozen predicate**, so they do not void the frozen verdict; they are not closed here, because closing them would change counter bytes after the freeze: see `## Named limits`.

**R95-C2 (depth) — verified on the frozen predicate at the landing worktree; named limits below.**

- Before (base `b5331db1`): craft has 33 blocks; `craft-citation-semantic.py --manifest block34-after.json --block 34` exit 1 (`block 34 missing`); `depth-blocks-v2.py --expect-blocks 34` exit 1 (`blocks 33 resolved 33 expect 34`); `depth-blocks-v3.py --expect-blocks 34 --shape-from 34` exit 1 (`.ufo/waves/round-95/pre/c2-base-*`).
- After (landed in the lane, measured with `--worktree` because the commit follows this lesson): `craft-citation-semantic.py --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --worktree` exit 0 `ok` (`.ufo/waves/round-95/l1/scores/c2-after-block34-worktree.json`); `depth-blocks-v2.py --worktree --expect-blocks 34` exit 0 `blocks 34 resolved 34 expect 34 unresolved 0 met=True`; `depth-blocks-v3.py --worktree --expect-blocks 34 --shape-from 34` exit 0 `blocks 34, resolved 34, required-shaped 1/1 ... met=True`. Before the knowledge entry landed, both depth counters exited 1 with `unresolved 1`, because block 34 cites it; this is the citation check working.
- Junk control (rubber-stamp): `block34-junk.json` exit 1 with three keyword reasons (`QUALITY 191 lacks ['str() fallback']`, `QUALITY 192 lacks ['complete JSON or absent']`, `QUALITY 192 lacks ['helper-only selftest']`) — the control fails on the keyword atoms, not on a missing block (MutationC1's requirement, checked at landing).
- Block 34 text is byte-identical to the seat draft (`diff` against `.ufo/waves/round-95/w1/ScribeC2Block/block34.md`, `BLOCK-IDENTICAL`).

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M95-a · a selftest world evaluated with the wrong denominator (own, this round).** The battery's mini-world legs did not thread `--intact-total`, so the strengthened instrument used its default 6 against a mini world with intact arm 1, and every mini forgery and the honest mini leg failed for the wrong reason. Evidence: `.ufo/waves/round-95/l1/scores/m95a-intact-denominator-red-green.txt` (RED: 2 failures, exit 1; GREEN: 0 failures, exit 0). Captured-by: the mini selftest's exact-reason assertions caught it (the forgery reason was wrong), not any frozen gate. Fix: `_run_leg` takes `intact_total`; the mini legs pass 1.
- **M95-b · a planted-symlink selftest that is not idempotent (own, this round).** The v5 selftest planted `receipt.json.tmp` in a case directory that survived the previous run, so a second run died with `FileExistsError`. Evidence: `.ufo/waves/round-95/l1/scores/m95b-selftest-idempotence-red-green.txt` (RED run 2 exit 1; GREEN runs 1 and 2 exit 0). Captured-by: none — the selftest was only ever run once before the rerun. Fix: the case directory is removed before planting.
- **M95-c · single-binding fixtures that violated two bindings (own, this round).** The first `badlabel` and `rewritten` fixtures were `met_target true` with a label that also failed recomputation, so `verify_receipt` reported two reasons where the case expected one. Captured-by: the exact-reason assertions (`reasons == [...]`). Fix: the fixture was made to violate exactly one binding (`met_target false` for the bad-label case; counts rewritten with the label for the rewrite case).
- **M95-d · a whole-file landing edit that broke the file (own, this round).** A two-operation edit to the v5 counter inserted a stray body line and left a syntax error at line 169; the file was rewritten whole and the selftests re-run (6/6). Captured-by: none; the next selftest run caught it. Class: landing. Fix: whole-file rewrite; the selftests are the check.
- **M95-e · a stale pin in the plan after the instruments were rewritten (own, this round).** The plan's v5 and v2 pins were computed before the v5 rewrite and the v2 `--root` threading, so the declaration briefly named bytes that no longer existed. Captured-by: none before the freeze; the pins were recomputed from the final bytes into `pins.sha256` and the plan was corrected before the declaration commit. Class: stale-premise. Fix: pins recomputed from `sha256sum` and the plan quotes the committed `pins.sha256`.
- **M95-f · a caller passed the wrong honest-leg prefix to the battery (own, this round).** `--honest-prefix honest-pos` made the battery look for `honest-pos-pos.json`; the battery reported `honest accepted False` and exit 1. Captured-by: the battery's honest leg (the instrument reported the caller error correctly). Fix: re-run with `--honest-prefix honest`; the battery command in the claims file names the right prefix.
- **M95-g · the declared named limits were not exhaustive (the round's main mistake; caught by the wave, not by the lane).** R95-C1's limits named provenance, the hostile parent-directory swap and the `--expect` binding. CriticC1 showed the instrument also does not bind: the unlabelled-counts case, the revision to the measured tree (a verifier `--rev` of another commit carrying the same tool bytes exits 0), the repair pin, the imported battery pins, and `public_met`; and that a run without `--json-out` skips self-verification and exits 0, though the v5 docstring says a green exit only comes through a verified receipt. Evidence: `.ufo/waves/round-95/w1/CriticC1.md` (attack table A1b, E1', E2, F1x, G1x, H1x, nojson), `ReviewerV5` finding 2 and `w1/ReviewerV5/ReviewerV5.md`. Captured-by: none — the frozen kill rule runs only the four committed forgeries and the honest run, which all carry `--json-out`. Fix: named in the knowledge entry (section (f)) and the SCORECARD; the closure is a round-96 declaration (see `## Planned`).
- **M95-h · the frozen kill rule cannot see the writer's own gates (the mutation finding).** Five of ten single-line mutants survive the frozen commands: fsync removed (M2), self-verify forced ok (M3), fail-closed `code = 1` removed (M4), the public revision binding removed (M6), and the probe's hard-coded verdict (M10). MutationC1 shows each is killed by a check the frozen commands do not run (a `main()`-level negative control; a v5 revision selftest; an fsync count; a probe receipt-content check). Evidence: `.ufo/waves/round-95/w1/MutationC1.md`, `w1/MutationC1/mutants.md`. Captured-by: none under the frozen rule. Fix: routed to round 96 as four named kills; not applied here (counter bytes are frozen).
- **M95-i · a probe-writer that follows a planted symlink (SentinelWrite).** The probe's own `--json-out` is written with `open(..., "w")`, so a planted symlink at that path is followed (LOW; outside the probe's frozen command, which passes `--json-out` under `--work`). Evidence: `.ufo/waves/round-95/w1/SentinelWrite.md` finding (f). Captured-by: none. Fix: route the probe's receipt through the same mkstemp and `os.replace` writer; routed to round 96.

No further sweep was run; the mistakes above are the ones this round's evidence records.

## Named limits (round 95; none closed here unless `## Measured` says so)

1. R95-C1: the bindings bind a receipt to the world it claims and do not authenticate its provenance (named before data).
2. R95-C1 (M95-g): unbound fields — unlabelled counts, the measured tree (HEAD never compared), `repair_sha256`, the imported battery pins, `public_met`; and self-verification is skipped without `--json-out`.
3. R95-C1 (M95-h): five writer and probe gates are outside the frozen kill rule (M2, M3, M4, M6, M10).
4. R95-C1 (M95-i): the probe's own `--json-out` follows a planted symlink; `verify_receipt` re-opens the path, not the written descriptor (LOW). A parent-directory swap stays out of scope.
5. R95-C1 (ReviewerV5): a counts object missing a key raises `KeyError` rather than a typed refusal (LOW, refuse-side); a caller-supplied empty `--expect` waives `label-not-frozen` (LOW).
6. R95-C2: the keyword atom is a vocabulary check (QUALITY 188 residual, named before data); the junk control tests its own vocabulary (CriticC2 A2).
7. R95-C2 (CriticC2): a criterion citing QUALITY 192 for a 191 row is not caught (A5); the depth counters accept junk table rows (A6) and rows with keyword-free criteria (A7); both are shape-only floors.
8. Unchanged from round 94: the fresh-pack arm has one source (`/usr/bin/env`); PE and Mach-O remain unmeasured.

## Planned (next steered round only)

(a) A round-96 declaration closing named limits 2 and 3: bind `revision` to HEAD and the measured tree, bind the repair and imported pins, reject unlabelled counts, make self-verification mandatory on every exit (no `--json-out` green), and add the four named `main()`-level kills (M2, M3, M4, M6) and the probe receipt check (M10) to the frozen kill rule. (b) The probe's receipt through the hardened writer (limit 4). (c) A non-author check of block 34's criteria against the rule each one states (limit 7). (d) A second fresh source for the held-out arm, carried from round 93.

## Wave r95-w1 — seat results (eleven seats, none dead)

- ExecRepro (executor): independent reproduction at `4bda1d1d`; all runs and selftests re-run in its own clone; differences limited to the per-run nonce (see `## Measured`).
- ScribeC2Block (scribe): drafted block 34 and QUALITY 191–192; verified in its clone (craft-citation exit 0 `ok`; junk exit 1 with three keyword reasons; depth v2/v3 34/34 after the knowledge entry lands); its `--rev` run needs the committed commit, its `--worktree` run needs the working tree — both are recorded.
- ScribeKnowledge (scribe): drafted the knowledge entry, the S320 row and lesson drafts; census verified in its own fixture (`E11` for the two missing consumers before they land, exit 1; exit 0 with them present).
- ScoutS320 (scout): two fetches, byte-identical, sha256 `d665489c…`, quote located with the `O_NOFOLLOW` context and the man-pages version (`w1/ScoutS320/s320-recheck.md`).
- ConnectorOverlap (connector): sibling-overlap scan; kake's `scripts/instrument_receipts.py` and tabi's receipt writers use the predictable `.tmp` shape (no r95 claim overlaps); souji's `souji-receipt-write.py` and kama's witness writer are already hardened; kumitate's `receipt-bind.mjs` checks receipt↔instrument bytes at a judged revision (`w1/ConnectorOverlap/overlap.md`). Overlap: the class is held by no sibling's r95 claim.
- ReviewerV5 (reviewer): all four tools read in full at `4bda1d1d`; pins match; selftests rc 0; no HIGH or MED; three LOW findings (named limit 5).
- ReviewerScope (reviewer): contract conformance of the declaration (`w1/ReviewerScope/scope.md`).
- CriticC1 (critic): eleven attacks on the instrument; the gaps in M95-g and named limit 2; the `--json-out`-less skip.
- CriticC2 (critic): the keyword atom and depth-counter residuals (named limits 6–7).
- MutationC1 (mutation-tester): 10 mutants in fresh clones; 5 killed, 5 survived (M95-h, named limit 3).
- SentinelWrite (sentinel): no HIGH or MED; the `mkstemp` `O_EXCL | O_NOFOLLOW` open and the `os.replace` onto a planted link are measured with strace (named limit 4).

## Verdict (per claim)

- R95-C1 — **verified on the frozen predicate** (forgery battery 4 of 4 refused with exact reasons; honest run accepted with self-verification; probe hardened; the before-side admits 4 of 4 and the v4 writer follows the planted symlink). The broader "bound to the world" is **not** established: named limits 2–5.
- R95-C2 — **verified on the frozen predicate** (craft block 34 landed; after-manifest exit 0; junk control exit 1 on keyword reasons; depth 34/34 at the landing worktree). The predicate is a vocabulary check: named limits 6–7.
- Harm check: the owned scores coverage, depth, calibration and freshness are unchanged (10.0 proxies); no owned axis is harmed by the measurements.
- Exploratory claims: none.
