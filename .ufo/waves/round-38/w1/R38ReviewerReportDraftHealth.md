# R38ReviewerReportDraftHealth — pre-integration health check of wave-1 report drafts

Seat: `R38ReviewerReportDraftHealth` (reviewer, leaf). Scope: (1) for every artifact/report
referenced by another seat under `.ufo/waves/round-38/w1/`, verify the referenced path resolves
and its evidence (exit codes, counts, hashes) is coherent with the frozen counters'
expectations; (2) assemble the integration frame — every production file this round will land
must have a supplying artifact; (3) list dangling or inconsistent references.

All observations are read-only. No counter, predicate, carrier, oracle, control or lane
surface was touched. Verification commands: `sha256sum`, `jq`, `git show/log/status/diff/ls-tree`
(read-only), two scratch fixture repos (created with `mktemp -d "$S/fx.*"` + `git init -q`,
toplevel verified before first commit, both removed), one frozen-counter selftest run from a
scratch mirror, and one binding simulation of the drafted patches + append block + stub entry
+ draft receipts against the **frozen** counter bytes. No tool was installed or upgraded
(nothing beyond the already-present curl/git/jq/python3/node was needed; pacman untouched).
Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ReviewerReportDraftHealth` is removed at the end of
this seat; every number cited below is reproduced in this report.

Snapshot taken 2026-10-26 ~06:30Z (03:30 -03:00) at lane HEAD `cb4326b2aa4c2024af0651fe6115b82d0c4de3df`
with a **live worktree** (see W1). 26 seat reports present at `.ufo/waves/round-38/w1/*.md`;
30 seat artifact directories.

## 1. Integration frame — COMPLETE as of this snapshot

| production file | supplying artifact | state |
|---|---|---|
| claim receipts `corpus/evidence/round-38/c1/K*/after.json` ×4 | `artifacts/R38ExecAfterK{1,2,3,4}/after.json` | present (but see F3: environment split) |
| knowledge entry | `artifacts/R38ScribeEntry/entry.md` (18 899 B) + `counts.txt` (5 790 B) | present (landed ~03:25, during this check) |
| SOURCES rows block | `artifacts/R38ScribeSOURCES/append-block.md` (5 926 B, S112–S116) | present; byte-identical to `R38ExecMirrorGate/append-block{.as-received,.normalized}.md` (diffed) |
| PROVINCE patch | `artifacts/R38ExecProvincePatch/patch.txt` | present (3 edits + static checks) |
| README patch | `artifacts/R38ExecReadmePatch/patch.txt` + `README.patched.md` + `checks.txt` | present; applies cleanly (`git apply` rc 0 on the current lane README) |
| SCORECARD section + LOG entry | `artifacts/R38ScribeScorecardDraft/scorecard-section.md` (14.5 KB) | present |
| lesson file | `artifacts/R38ScribeLessonSkeleton/lesson.md` | present (landed during this check), with red-before artifacts (`red-cited-path.txt`, `red-lesson-gate.txt`, `red-premise.txt`) |

**Decisive check — the drafted surfaces satisfy every C1 surface binding under the frozen
(v1) counter.** I built a scratch fixture repo from committed lane bytes: PROVINCE with the
patch's 3 edits applied (both BEFORE lines matched verbatim; append extracted), README with
the patch applied via `git apply` (rc 0), a stub entry whose `source:` line names S112,
`corpus/SOURCES.md` + the real append block, and the best available draft receipts (K1 =
`R38ExecProvincePatch/after-K1.json`, K2 = `R38ExecAfterK2/after.json`, K3 =
`R38ExecAfterK3/diagnostic-after-with-declared-extractor.json`, K4 = `R38ExecAfterK4/after.json`).
Frozen counter (`git show e059ca93:tools/round-38/c1-counter.py`, sha256 `a7a62b09…16db8`)
on that fixture:

```
bindings: province_core_section=true, province_core_row=true, frontier_note=true,
          entry_present=true, entry_source_ids=[S112], opened_source_rows=[S112],
          sourced=true, coverage_map_row=true
carriers_matched = 3   (K1 matched, K2 NOT, K3 matched, K4 matched)   met_target=false, exit 1
```

So the frame's surface drafts (PROVINCE row + supersession note + entry + SOURCES row +
coverage-map row) are counter-coherent; the only carrier binding that fails is K2
(`after_gaps_empty=false`, 3/3 hits) — F2 below.

## 2. Reference resolution — no dangling references beyond expected-missing classes

I extracted 111 unique lane-relative paths from all 26 reports and re-ran after the late
landings. Result classes:

- **Resolving:** every `.ufo/waves/round-38/w1/artifacts/...` path cited by any report, all
  committed corpus/tools/plans paths, shokuknow read-only inputs
  (`Projects/shokuknow/.ufo/waves/corpus-expansion-1/{absent-defect-register.md,quote-lint-full-v5.json}`,
  `merge/kaidoku/SOURCES.append.md`), and `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`.
- **Expected-missing until L1 integration (not defects):**
  `corpus/evidence/round-38/c1/K*/{before,after}.json` (claim data lands only at integration;
  `corpus/evidence/round-38/` is empty today) and
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (the entry exists as
  the draft artifact; the corpus path is L1's to create).
- **Real dangling reference (spec-side, already reported by two seats; confirmed):**
  `.ufo/waves/round-38/probes/avm.txt` — named by the wave assignment text — does not exist.
  The committed copy is `.ufo/waves/round-37/probes/avm.txt` (1 496 B,
  sha256 `c1c43f6f…a9a5d5`). R38ScoutFreetzAvm (path-correction section) and
  R38ScribeSOURCES (F3) both routed this; the **assignment text itself is still wrong**, so
  any future re-dispatch re-introduces the dead path.
- Regex artefacts of my own extraction (`tools/adb`, `tools/sasquatch`, `tools/unblob/...`,
  `tools/master/README-AVM-BE` = URL tails; `corpus/evidence/round-37/c1/K` = glob) — not
  report defects.

## 3. Findings, by severity

### F1 — CRITICAL (freeze integrity, in progress): freeze v2 exists only as an uncommitted worktree edit, and the worktree counter currently crashes

- `git status` shows **two tracked files modified**: `tools/round-38/c1-counter.py` and — new
  since my earlier checks — `plans/round-38-claims.md`. HEAD (`cb4326b2`) still carries the v1
  bytes: counter `a7a62b09…16db8`, claims `13ea8eba…9815`. Worktree counter hashes I observed
  at six successive reads: `f27f982b` → `edda9bb3` → `a2e22884`/`d24b48ce` → `21105978` →
  `12f09870` → `1b6a8d10` → `1b4dc730` (a sibling is actively editing; R38ExecSelftests §4 and
  R38MutC1 independently recorded the same churn, MutC1 archiving two diff snapshots).
- The claims-doc worktree diff announces **"freeze v2 (pre-scoring amendment)"**: it restates
  P38-C1 with "sasquatch-v4be available" for the after-arm plus a **paired committed
  before-receipt** requirement, and says "No claim was scored under v1; v2 is the frozen bytes
  every receipt and score now complies with." **But no v2 commit exists** — the "frozen bytes"
  are currently uncommitted worktree state with no revision a counter `--freeze` could name.
- The worktree counter is also **broken right now**: its selftest and any measure() run crash
  with `AttributeError: 'NoneType' object has no attribute 'get'` at `gaps(envs.get(...))`
  (line 135/186 region) whenever a carrier lacks a `before.json` — I reproduced the crash via
  `--selftest` (exit 1, traceback) and via a fixture measure() run. The frozen v1 selftest
  passes (15 cases, green 1 / red 14, failures [], exit 0 — re-run by me from a scratch
  mirror), and `c2-counter.py --selftest` passes at frozen bytes (14 cases, green 1 / red 13,
  exit 0 — re-run by me).
- Consequences the wave must resolve before WAVE-DONE: (a) commit v2 (claims + counter +
  selftest + **v2 controls**) or revert to v1 — until then no `--freeze` argument names the
  bytes that would score the round; (b) the v2 note says "Kill rules apply to the v2 controls"
  but `controls/` still holds only the seven v1 receipts (`efd5c47a`) scored under the v1
  counters — v2 controls do not exist yet; (c) v2 requires `corpus/evidence/round-38/c1/K*/
  before.json` — no such drafts exist yet (R38ExecBeforeArmRecheck holds envelopes in its
  artifact dir, not staged receipts); (d) every seat that ran "the counter" from the worktree
  path mid-wave (R38ExecAfterK1 §2e, R38ReviewerEntryQuality, R38ExecEnvelopeRules, my
  binding sim) got different counter generations at different times; K1's seat is the only one
  that re-ran its fixture against both generations and showed the verdict is
  generation-independent. The v1-frozen result in §1 is the stable reference point.

### F2 — CRITICAL (claim fatal, v1 as frozen): P38-C1 cannot reach `carriers_matched == 4` on these carriers — K2 is structurally unmatchable

Measured, independent of the premise question:

- K2's image contains symlink `var/lib/run-link -> ../../a/run.sh` (verified in the committed
  `K2/src` tree). REA/unblob publishes only regular files and records exactly one
  `unpublished-entry` gap for it — reproduced in three separate K2 runs (seat `out`, seat
  `out2`, fixed harness) plus the ProvincePatch quad. Under the frozen (and v2) clause
  `after_gaps_empty == []` per carrier, **K2 can never match**. With the best available
  receipts the maximum is `carriers_matched = 3` (my §1 sim; same number reported by
  R38ExecProvincePatch F1, R38ExecEnvelopeRules §4, R38ExecReadmePatch §5,
  R38ReviewerEntryQuality §4.2, R38ScribeEntry "Not claimed" section).
- The asymmetry is carrier content, not extractor state: K1's symlink
  (`link-to-hello -> ../hello.txt`) escapes the image root, is dropped with a
  `MaliciousSymlinkRemoved` WARNING, and produces **no** gap; K2's internal symlink produces
  the gap. (R38ScribeEntry "Gap-free depends on the link target" section documents the
  mechanism from the receipts.)
- Therefore, on the v1 freeze the claim ends in an **honest stop** unless the L1's v2 re-freeze
  changes the gap clause — and the v2 worktree diff I read does **not** relax
  `after_gaps_empty`; it only adds the before-arm. The v2 freeze as drafted still cannot pass
  K2. This is the wave's central unresolved decision.

### F3 — HIGH (evidence incoherence across the four receipt drafts): they were produced under two different extractor environments, and the seat reports' environment claims conflict

| draft | environment actually required by its outcome | gap | hits |
|---|---|---|---|
| `R38ExecAfterK1/after.json` | `sasquatch-v4be` **absent** (PATH-stripped, verified by the seat) | 1 `missing-extractor-dependency` | 0/5 |
| `R38ExecAfterK2/after.json` | `sasquatch-v4be` **present** (required: extraction succeeded) | 1 `unpublished-entry` | 3/3 |
| `R38ExecAfterK3/after.json` | absent (PATH-stripped, verified) | 1 `missing-extractor-dependency` | 0/4 |
| `R38ExecAfterK4/after.json` | present (ambient PATH; seat's own dep-probe matrix) | [] | 4/4 |

- Scoring these four as-is gives `carriers_matched = 1` (K4 only) — I measured this on a
  fixture repo containing exactly the four seat `after.json` files (all four evidence ids
  recompute; per-carrier `matched`: K1 false, K2 false, K3 false, K4 true). Scoring the mixed
  on-PATH set gives 3 (§1). Neither reaches 4. Three candidate quads exist in the artifacts
  (seats' `after.json`, seats' on-PATH diagnostics, ProvincePatch quad) and the L1 must pick
  one — under v1/v2-as-drafted all three fail on K2.
- **R38ExecAfterK2.md §1 states "No sasquatch on PATH; stock unblob handled the image."** That
  statement is inconsistent with the receipt it lands: unblob's `squashfs_v4_be` handler
  publishes regular files only through the external `sasquatch-v4be` (`shutil.which` on PATH;
  `ExtractorDependencyNotFoundReport` otherwise), and K1/K3's PATH-stripped runs plus K4's
  dep-probe matrix prove a gap+0-file outcome whenever the binary is unreachable. A successful
  3/3 K2 extraction therefore implies the binary WAS resolvable in that run; the report shows
  no `command -v` verification and no env capture for its run. The receipt itself is valid and
  self-consistent — the prose environment claim is what is unsupported. (Fix class: correct
  the report line before it is quoted anywhere; the K2 report's own §4 evaluation, which is
  correct, does not depend on it.)

### F4 — HIGH (claim-premise falsified; already routed to L1 by five seats, confirmed here): "no external extractor dependency" is false; the before-arm reproduces

The v1 claims text ("run with stock unblob 26.6.4; no external extractor dependency" +
"the round-37 'missing-extractor-dependency' before-arm does not reproduce") is contradicted by
wave-1 measurement on all four carriers (R38CrossToolK1 §6, R38ExecAfterK1 §2a/2c,
R38ExecAfterK3 arms A/B/C, R38ExecAfterK4 dep-probe matrix, R38ExecBeforeArmRecheck 16/16
matrix, R38ScoutUnblobHandler §4-6): unblob 26.6.4 has no in-process SquashFS reader; BE v4
always shells to `sasquatch-v4be -be`; the gap reproduces whenever the binary is off PATH. The
root cause of the round-37 "non-reproduction" is that `~/.local/bin` was on PATH (the v2
claims diff now says the v1 probes never actually stripped it — consistent with the round-37
verifier's observation). This finding is already the driver of the v2 re-freeze (F1); no new
action beyond landing v2 coherently.

### F5 — HIGH (instrument falsification, relevant to scoring honesty): the frozen counter's selftest does not protect its core checks, and a fabricated-but-consistent receipt scores met

R38MutC1 (27 single-logic mutants, my read of its table): 19 mutants survive the selftest —
including removal of the oracle-hit comparison (M02), handler check (M03), gap check (M05),
subject-digest check (M22), operation/provider check (M23), and evidence-id recomputation
(M07). Probe A: a receipt whose `normalized_result.files` were copied from the frozen oracle
TSV and re-minted with `xpin-attribute.mjs` — no REA run anywhere — makes the **frozen**
counter exit 0 with `carriers_matched == 4, met_target = true`. This is the carried R36-CL3
blind spot now formally reproduced against this round's instrument (it also means the §1/§3
counter verdicts certify envelope internal consistency, not that REA ran; the honest evidence
that REA ran is the cross-tool + provenance + environment matrix around the receipts, not the
counter alone). R38ExecSelftests independently documents the same class plus the live-drift
crash (its §4 table records `12f09870` → "no verdict: AttributeError").

### F6 — MEDIUM (frozen harness): `c1-run.sh after` could not produce any receipt at the freeze; fixed post-freeze in `cb4326b2`

At `e059ca93`/`9c9d496b` the harness `mkdir -p "$OUT"`; REA refuses an existing output root
("Extraction output root already exists", exit 1) — reproduced by three seats and kept as
failure envelopes (`R38ExecAfterK3/harness-after-mode-failure.txt`,
`R38ExecAfterK1/harness-after.envelope.json`,
`R38ExecAfterK4/harness-after-head9c9d496b-failure.json`). The L1 fixed it at `cb4326b2`
(03:19:01) and post-fix runs exit 0 (`harness-after-mode-post-fix-ok.json`, my read of
`R38ExecProvincePatch/harness-after-K1.json`: 5 files, gaps [], coverage partial). Coherence
consequence: every after receipt in the wave was produced outside the freeze-time harness
bytes; the SCORECARD/LOG drafts say so. Disclosed, not a new gap — but the v2 freeze must name
the harness bytes receipts are expected to match, or the disclosure stays permanent.

### F7 — MEDIUM (coherent but worth landing in the verdict): pre-claim state, controls, and counter blind spots all verified

- RecountBase receipts: I re-read all five JSONs; they match the report's quotes exactly
  (c1-at-base/freeze/tip: `carriers_matched 0`, `frontier_note true` (v1 vacuous binding),
  exit 1; c2-at-base/tip: `mismatches 1`, `unresolved [["prov_core:REA MCP server",
  "evidence/doctor/"]]`, guards `base_pointers 48`, observed `124/124, 17/17, [9,9],
  [81,314], [97,125]`). The dispatch text's "expect exit 2" for run 1 was wrong (observed 1);
  the seat's explanation of the counter's actual exit-2 paths is correct — spec defect, not
  counter defect.
- Controls: all seven receipts in `.ufo/waves/round-38/controls/` carry `exit 1` and
  `output.met_target false` (ctl-c1-1 shows `carriers_matched 3`; c2 controls mismatches
  1/1/0/0). Kill rules not triggered — coherent with the claims doc.
- Carrier/oracle/binary pins re-hashed by me: K1 `1cfb6c33…`, K2 `403cb0a8…`, K3 `9c7c523c…`,
  K4 `a29ddc15…` (match wave carriers.json); K1/K2 oracle.tsv `0c993e74…`/`6567cc50…`, K3/K4
  `638a6f75…`; `sasquatch-v4be` `fac88740…`, `sasquatch` `ad02d27a…`, unblob `0ce7b624…`,
  `gen-squashfs.py` `1c7c5e88…` — all agree with every report that cites them.
- Doctor-pointer mismatch is real: `PROVINCE.md:44` still carries the unresolved
  `evidence/doctor/`; the target document `.ufo/waves/round-19/evidence/doctor/` exists
  (doctor-6.5.0.txt, doctor-6.7.0.txt); the ProvincePatch Edit-1 repair points exactly there
  (same document, as QUALITY 77 requires).
- Blind spots confirmed (report class, not repair): `frontier_note` is a whole-file scan and
  true pre-claim (v1); `measure()` never reads `c['path']`, so carrier bytes at `--rev` are
  never hashed (material is honest — pins verified by me and three seats); `carriers_unchanged`
  false at base means "absent".

### F8 — LOW (draft defects to fix before landing; none blocking the frame)

1. **Digest transcription typo in the lesson draft**: `R38ScribeLessonSkeleton/lesson.md` Gate
   S116 row says `sha256 1c7e5e88…`; the actual bytes hash `1c7c5e88324d64ad…01ba8dd5` (as the
   scribe's own S116 row and my re-hash agree). One-character class error in a cited digest.
2. **S115 scope cell overstatement** (R38ReviewerEntryQuality A3): "not a SquashFS reader" is
   contradicted by the lane's own LE positive control (`R38CrossToolK1/7z-le-positive-control.txt`,
   exit 0, `Type = SquashFS`); accurate wording is "not a **big-endian** v4 reader".
3. **S114 quote locator missing** (EntryQuality A1): the ≤25-word quote has no line/section
   anchor in the row (measured location: upstream raw lines 9–10 / `avm.txt` lines 8–9).
4. **Uncommitted anchor path** (EntryQuality A2): S115's anchor cites the wave-1 artifact
   `artifacts/R38CrossToolK4/7z-refusal.txt` — untracked until the L1 commits `w1/` (R37-CL1
   class). Same for every seat report that cites wave artifacts; resolves at integration commit.
5. **Claims-text mislabels inherited into drafts**: K2 kind "symlink + unicode name" (the name
   is ASCII `space name.txt` — a space); K1/K2 "gzip images" (zlib-compressed blocks, no gzip
   container). Frozen `carriers.json` carries the "unicode" kind — not repairable this round;
   the entry draft already uses the corrected wording ("symlink + space in a name"), the
   PROVINCE/README patches still say "gzip". Cosmetic only; pins unaffected.
6. **Evidence ids are path-sensitive** (K1 report D3, K2 report §6, K4 report §8): identical
   outcomes under different staging paths produce different `ev_…` ids; stored==recomputed is
   what the counter checks and it holds for all ten draft envelopes (R38ScribeScorecardDraft
   xpin table + K1 §2d + my sim's `after_evidence_id_ok true` ×4). Landed receipts will embed
   dead `/fast/scratch/...` paths — acceptable to the counter, disclosed by three seats; the
   SCORECARD draft carries the question.

### F9 — INFO (assignment-text defects this wave worked around; re-dispatch hazard)

- `.ufo/waves/round-38/probes/avm.txt` (see §2) — real path is round-37.
- unblob handler URL in the assignment lacks the `python/` segment → 404 at tag 26.6.4
  (R38ScoutUnblobHandler §1; S112 uses the resolving path).
- "expect exit 2" for the base c1 recount — frozen behaviour is exit 1 (F7).
- K1/K2 "gzip" and K2 "unicode name" mislabels (F8.5).

## 4. Wave progress vs frame at snapshot

- Reports present (26): 4 CrossTool, 4 ExecAfter, RecountBase, Selftests, BeforeArmRecheck,
  EnvelopeRules, IdCollision, MirrorGate, ProvincePatch, ReadmePatch, Quarantine,
  ConnSeparability, MutC1, ReviewerEntryQuality, 4 Scouts, ScribeSOURCES, ScribeScorecardDraft.
- No report yet (7 seats still running at snapshot): R38CriticSourcedClaim, R38CriticClaimsC1,
  R38CriticClaimsC2, R38ReviewerPredicateIdentity, R38ReviewerCodeAudit, R38SentinelBounds,
  R38RevengerPremise (artifact dirs exist for all but RevengerPremise). These are
  falsifiers/audits, not production suppliers — the integration frame (§1) does not depend on
  them, but WAVE-DONE should not be declared before their verdicts land (especially
  CriticClaimsC1/C2 kills and PredicateIdentity, which must rule on the v1→v2 predicate-identity
  question raised in F1).
- Frame suppliers all present (§1). The two pre-integration gaps that remain are L1 actions,
  not missing seats: (a) commit freeze v2 (claims + counter + selftest + v2 controls) or revert
  to v1, and state in the round report which bytes scored; (b) pick the receipt quad and stage
  `corpus/evidence/round-38/c1/K*/after.json` (+ `before.json` under v2) — knowing that under
  both v1 and v2-as-drafted K2 fails `after_gaps_empty` and the claim is an honest stop
  (F2), unless v2 is amended again before commit.

## 5. Residual risks / verification gaps

- I did not re-run REA, the harness after-mode, or any extractor; the receipt-level facts I
  score are read from the draft envelopes whose evidence ids I recomputed only through the
  frozen counter's own path (which per F5 cannot prove REA ran — the extractor-provenance
  matrix from the executor/cross-tool seats is the corroboration I relied on).
- The v2 worktree state was moving while I read it; hashes quoted here are point-in-time
  (`1b4dc730…` last observed for the counter, claims doc diff read once). The crash
  reproduction (F1) was on `12f09870`/`1b4dc730`-era bytes; if the L1 has since added a
  `None` guard, re-verify before quoting.
- The binding simulation used a stub entry (`source: S112 — …`); the real entry draft's first
  five `source:` lines name S112–S116 and its receipt table matches the quad I scored, so the
  binding outcome carries over, but I did not re-run the sim with the full entry text.
- `R38ScribeLessonSkeleton/lesson.md` and `R38ScribeEntry/entry.md` landed during this check;
  I read them but did not line-audit every citation inside them (EntryQuality's findings A1-A5
  are the seat tasked with that and its §2 was still "(pending the scribe's artifact)" at my
  read — its final entry verdict may supersede my F8 items).
