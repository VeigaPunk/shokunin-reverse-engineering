# ReviewCapabilityTable — what the r17 log-capture row must demonstrate

Seat: `KaidokuR17.ReviewCapabilityTable-3` (advisory, author-side). Read-only.
Axes worked: **calibration** (primary — do not let an undemonstrated row enter) and
**depth** (the row's evidence must be re-derivable, not a restatement of intent).
No REA analyze/search/decompile, no Ghidra, no carrier execution. Bounded scope is
listed in §6; nothing outside it was reviewed.

## 1. The admission rule, exactly as written

`AXES.md:57` defines the separate `capabilities:` table; `:61-62` fixes its four
columns — *name → what it can now do (one line) → evidence pointer (command or
path) → first-working round*; `:63-64` fixes admission: "Rows enter only through a
round that demonstrates the capability running; a capability without a passing
demonstration in the round report is pre-claiming and does not enter the table."
`AXES.md:80` repeats the four columns in the per-repo `SCORECARD.md` contract.
`SCORECARD.md:624` restates the same rule under the existing table.

Three consequences follow directly:

1. The **run must happen in this round**; a tool existing, a plan, a source-model
   prediction (r14–r16), or a pilot that disclaims itself is not a demonstration.
2. The demonstration must **pass** and must be **in the round report**
   (`.ufo/reports/round-17/kaidoku.md`), not only in the wave directory.
3. The evidence pointer must be a **command or path** a reader can re-execute or
   re-open at the round's measured revision.

## 2. What this row specifically must demonstrate

Checklist derived from §1 plus the round's own claim text
(`.ufo/waves/round-17/claims.json:21-22`) and tool contract
(`.ufo/waves/round-17/contract.md`):

| # | Requirement | Why | Anchor |
|---|---|---|---|
| D1 | **≥3 carrier runs** this round, each with a receipt under `.ufo/waves/round-17/runs/*/receipt.json` | C2's own before→after is `0 -> >=3` | `claims.json:22` |
| D2 | Every counted receipt **validates**: `receipt-validate.py` exit 0, pre/post `pins.compare.equal` true, non-empty retained logs | C2 gates the row on exactly this | `claims.json:22`; `contract.md:107` |
| D3 | Each receipt carries **carrier path + sha256 pre/post**, **REA analyze `evidence_id`**, **per-log sha256 + bytes**, **poll count + last-copy UTC**, and the literal `log_capture_limit` | Makes the capture re-checkable and states the miss window | `contract.md:43-47` |
| D4 | The Go-version input is retained too: `runs/<label>/inspect-go.json` (`inspect-go-binary` output) | `analyze` JSON does **not** carry build info — observed in the pilot: `pilot/shfmt.json` and `pilot/esb.json` `normalized_result` keys are only `document, image_base, procedure_count, segment_count, segments, string_count` | `contract.md:35` |
| D5 | If the row's what-cell says it **extracts** diagnostics, the extraction output (`log-extract.py` JSON/stdout) must also be retained per run; a receipt alone does not evidence extraction | The pointer column is the only place a reader can check the verb | `contract.md:51-60` |
| D6 | The demonstration and the validation exit are stated **in the report**; a failed validation means **no row** and an explicit negative branch in the r17 SCORECARD section | AXES:63-64; r16 precedent for the negative branch | `AXES.md:63-64`; `SCORECARD.md:2316-2317` |

Shape follows the two in-round precedents: append under
`### Capability addition (demonstrated before this row)`
(`SCORECARD.md:2203-2207`), keep the summary table at `:615-622` untouched
(r13: "This is an append-only capability record; the earlier line-addressed
summary table is unchanged", `SCORECARD.md:2137-2138`), and put qualifications in
a `Limits:` paragraph after the row (`SCORECARD.md:2209-2211`).

## 3. Pre-claiming hazards in this round's design (findings, severity order)

### P1 (high, calibration) — The round's own measurement cannot tell a claimed row from a demonstrated one
`contract.md:118` makes `measure.py` pass on **SCORECARD capability row text
`retained REA Ghidra-session log`** alone. A row committed before any run would
already flip that check 0→1, so `measure.py` is a necessary, not sufficient, gate.
The row must additionally be gated on D2; the round section should print both
(`row present: yes/no`, `receipt-validate exit: 0/N`) so the before→after is not
satisfiable by text insertion. Also fix the literal token: C2's name
(`claims.json:21`) is "retained REA Ghidra-session log capture" — the substring
`retained REA Ghidra-session log` must appear verbatim in the row or the round's
own presence check reports 0→0.

### P2 (high, calibration) — The drafting seat runs before the runs do
`DraftScorecard` is a **wave-1** seat (`.ufo/waves/round-17/wave1-spec.json`,
item target: "incl. capability row draft"), while the measured carrier runs are
not a wave-1 seat (only `CarrierRunTool` exists). If the draft's row is integrated
verbatim, the row precedes its demonstration. Remedy: the draft may contain the
row only marked `PENDING — no claim`, outside the table or with an explicit
`evidence: PENDING` cell; L1 must not copy it into `SCORECARD.md` until D2 holds.
The safest draft is the negative branch pre-written too: "if no receipt validates,
no capability row enters and the stagnation interval is not reset."

### P3 (high, calibration) — The pilot is not the demonstration
`pilot/README.txt:1` states "NOT the final measured runs" and `:6` states
"pre/post carrier pins were NOT recorded in the pilot." Both disqualify it under
AXES:63-64. Additional pilot gaps found:
- `pilot/SHA256SUMS` has 6 entries; the directory has 12 files. `README.txt`,
  `esb.err`, `esb.exit`, `shfmt.err`, `shfmt.exit` are unhashed (observed by
  enumerating the directory and matching the sums file).
- No `inspect-go.json` artifact exists; `go1.27.0-X:nodwarf5` and `go1.23.12`
  live only as prose in `README.txt:7-8`, with no evidence id, so `predict.py`
  cannot be re-run from pilot artifacts (D4).
- No receipt, no pins, no poll count, no last-copy timestamp.

### P4 (high, calibration) — The pilot itself shows the tail can be lost
Observation: `pilot/shfmt-log/ghidra.log:123-125` ends at
`ANALYZING changes made by post scripts`, while
`pilot/esbuild-0.25.12-log/ghidra.log:118-123` ends one lifecycle line earlier at
`SCRIPT: .../ReaGhidraBridge.java`, with no terminal session marker in either
file. Inference (not proven): the esbuild copy was taken before the post-script
ANALYZING line was appended, i.e. final-line loss occurred at 1 s polling. A row
that says "captures the session log" without the polling limit is contradicted by
the round's own pilot evidence. The what-cell and the `Limits:` paragraph must
carry `contract.md:46-47`'s wording: lines written after the final poll before REA
deletes the runtime root can be missing.

### P5 (high, depth) — Bare log copying is not new repertoire; the harness is
`arc2-loop1-round7/E3.md:9` records that the r7 seat already copied a live
`ghidra.log` out of a REA session before deletion (single snapshot at 19:01:38,
last line 19:01:26, "Lines after 19:01:26 (~4.5 min, through the 19:04:11 exit)
are **not captured**"). So "retained Ghidra log" as an act predates this round.
The row must name the delta: fixed-interval polling loop over **every new**
`/tmp/rea-ghidra-*` dir, pre/post pin maps, per-file hashes, a validator-clean
receipt, and the extraction that separates `bootstrap_missing` from
`snapshot_loaded`. Otherwise a reviewer can correctly say r7 already did it and the
row adds no repertoire (`AXES.md:58-60`).

Corroborating observation: the r7 snapshot path named at `E3.md:9`,
`/var/tmp/arc2-l7r7-E3-scratch/ghidra-snapshot-t1858.log`, **no longer exists**
(checked; `ls`/`sha256sum` both ENOENT). Out-of-tree retention did not survive two
days, so the r17 row's evidence must be repo-relative and committed — today the
whole `.ufo/waves/round-17/` tree is untracked (`git status`: `?? .ufo/waves/round-17/`;
`git cat-file -e HEAD:.ufo/waves/round-17` fails at `b563c79`). Until the run
artifacts are committed at the measured revision, the capability is not yet
retained in the durable sense the row would claim.

### P6 (high, calibration) — Do not reintroduce the R16-PROVENANCE wording
Pins prove only "same bytes at two instants", never "unchanged throughout"
(`contract.md:20`). The same round is correcting exactly this wording via
`temporal-sweep.py` (`contract.md:90-96`). The row and the r17 section must avoid
`unchanged during`, `remained unchanged during`, `stable throughout`,
`pins_unchanged_during_run`; write instead "carrier sha256 equal in the pre and
post pin maps; stability during analysis not evidenced." A row asserting
in-run immutability would make the round's own C1 correction self-invalidating.

### P7 (medium, calibration) — The row-count claim is ambiguous
C2 says "capability rows 4 (+r13/r14 appended) -> +1" (`claims.json:22`). The
summary table has 4 rows (`SCORECARD.md:619-622`); appended rows are already 2
(r13 `:2135`, r14 `:2207`); after r17 the total is 7 while the summary-table count
stays 4. r12 already used the same ambiguous form ("capability rows 4 → 5 only if
it runs", `SCORECARD.md:2109`). State the counting domain explicitly, e.g.
"appended capability rows 2 → 3 (summary table unchanged at 4)", and have
`measure.py`/the report print the same number.

### P8 (medium, depth) — Evidence pointer must be re-derivable and repo-relative
AXES:61-62 allows a command or path. The r14 row's pointer is the good pattern
(executable selftest/frozen commands plus a repo-relative path and
`verification.json`, `SCORECARD.md:2207`). The r13 row's pointer embeds an absolute
worktree path (`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin`,
`SCORECARD.md:2135`) that does not resolve from another worktree — do not copy
that. For r17 use the exact receipt shape `measure.py` counts
(`W/runs/*/receipt.json`, `contract.md:118-119`) and the validator command with its
exit, plus the measured revision.

### P9 (medium, calibration) — Bound the row to what ran
- REA pin: 6.5.0 only; the base table's 6.4.0 row (`SCORECARD.md:620`) is not
  evidence for this one.
- Verb: `analyze` only; the contract's `--search` steps are separate REA sessions
  (`contract.md:40-41`) and are not evidenced unless their logs are retained and
  counted, so the what-cell must not imply all-verb capture.
- Carriers: exactly the pinned set (proposed: out-of-range `shfmt` 1.27.0,
  in-range `esbuild` 1.23.12, plus one more in-range 1.20.x per `claims.json:21`);
  linux/amd64, static analysis, no target execution (`claims.json:26-31`).
- Do not claim Go 1.27 symbol recovery or a recovery promise (`claims.json:26-31`).

### P10 (medium, calibration) — Prediction match is not the capability
C2 bundles two deliverables: the retained capture (capability) and the
prediction-vs-observation table (knowledge entry). `compare.py` exit 1 on a
mismatch is a *reported result*, not a failed capture. The row must claim only the
capture/extract, not "predicts Ghidra's Go behavior"; mismatches stay in the
knowledge entry and the report, never hidden (`claims.json:22`).

## 4. Suggested row skeleton (placeholders, not a claim)

Only paste after D2 holds; one-sentence what-cell, limits after.

```
| retained REA Ghidra-session log capture | Copies `ghidra.log`/`script.log` from every new
`/tmp/rea-ghidra-*` session dir at a fixed poll interval during REA 6.5.0 `analyze`, retains them
in-tree with per-file sha256, pre/post carrier pins and validator-clean receipts, and extracts the
Go analyzer lines that separate `bootstrap_missing` from `snapshot_loaded` on 3 pinned carriers
<slots> | `python3 -I .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/*/receipt.json`
→ exit 0; `.ufo/waves/round-17/runs/` (3 receipts, per-file sha256, analyze `evidence_id`);
`.ufo/waves/round-17/verification.json`; report `.ufo/reports/round-17/kaidoku.md`; source revision
<rev> | round-17 |
```

Limits paragraph must state: polling copy ≠ completeness (last-poll window; pilot
P4); pre/post pins ≠ in-run immutability (P6); in-tree retention only (P5 — r7's
`/var/tmp` snapshot is gone); three carriers / REA 6.5.0 / `analyze` only (P9); no
semantic interpretation of the log; no recovery claim. If D2 fails: no row, and
say so (r16 precedent, `SCORECARD.md:2316-2317`).

## 5. Residual risk and verification gaps

- I did not run `receipt-validate.py`, `carrier-run.py`, `log-extract.py`, or
  `predict.py` (no `W/tools/` existed when checked, and no `W/runs/` either;
  contract forbids REA/analyze runs). Their behaviour is asserted from
  `contract.md`, not observed.
- P4's tail-loss reading is an inference from lifecycle asymmetry; the only
  observation is the two files' final lines.
- The "3 carriers" target is from `claims.json:21`; the third carrier is not yet
  selected in any artifact I read.
- Whether the r17 section will be appended after r16 (current SCORECARD end,
  `:2342-2348`) or replace anything was not reviewed; append-only follows r13/r14.

## 6. Bounded no-finding statements

- Searched `SCORECARD.md` for an existing round-17 section or a pre-existing
  "retained … Ghidra-session log" row: none. File ends at the r16 `Planned:` line.
- Searched all capability rows (`:619-622`, `:2135`, `:2207`) for a claim of log
  retention: none. The r7 row (`:622`) claims the contained systemd analyze and
  analyzer-disable recipe and does not mention logs at all; the log reading lives
  in its linked knowledge entry
  (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:17`) and `arc2-loop1-round7/E3.md:9`,
  ad hoc, not as a row.
- Searched `corpus/knowledge/` for retained log citations: `2026-10-13-r4-10-real-version-pair.md:72-73`
  records the bootstrap message as "observed-not-cited" because the dir was
  deleted — the exact epistemic gap the new capability should close, and a reason
  the row's pointer must not be an ephemeral path.

## 7. Tool installs

None. No pacman/uv/npx install was needed or attempted for this review.
