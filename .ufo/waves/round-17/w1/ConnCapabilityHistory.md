# ConnCapabilityHistory — prior capability rows vs. proposed retained REA Ghidra-log capture

Axes: **calibration** (row admission / non-duplication) and **depth** (what the retained bytes enable).
Everything below is read-only observation from the lane tree unless marked **[INFERENCE]**.
Repository state: HEAD `b563c79`, round-17 untracked (`git status`: only `?? .ufo/waves/round-17/`).

## 1. The rows as they actually read

| # | Row (anchor) | What it claims | First-working |
|---|---|---|---|
| 1 | pre-registered two-lane live battery — `SCORECARD.md:619` | frozen-prediction battery + hashed receipts | luna-round-6 |
| 2 | version-symmetry battery — `SCORECARD.md:620` | same form on second pin | luna-round-8 |
| 3 | config custody pre/post-pair — `SCORECARD.md:621` | freeze 5 operator paths, re-verify byte-identity | arc2-loop1-round2 |
| 4 | contained user-service analyze of oversized PEs — `SCORECARD.md:622` | run REA/Ghidra analyzes as systemd user services with validated analyzer disables + memory caps | arc2-loop1-round7 |
| 5 | curated source registry — `SCORECARD.md:2135` (append-only table) | source curation, recheck cadences, rejection | arc3-loop1-round13 |
| 6 | local raw-quote/heading regression audit — `SCORECARD.md:2207` | quote instrument + frozen verdicts | round-14 |

Count is 6, not 4: the base table is `:619-622` (4 rows), r13 and r14 append separate tables (`:2131-2136`, `:2203-2208`). r15 and r16 explicitly add **no** row (`:2257`, `:2316-2317`). This matches `claims.json` C2 fba "capability rows 4 (+r13/r14 appended) -> +1". Admission rule: a row enters only through a round that demonstrates it running; otherwise it is pre-claiming (`AXES.md:57-64`, fleet path `/home/vgpnk/Projects/shokunin/AXES.md`). r14's row carries a `Limits:` paragraph (`SCORECARD.md:2209-2211`) — the precedent for how an instrument row states its boundary.

## 2. What the contained user-service row actually owns (and what it used)

The row text (`SCORECARD.md:622`) claims **containment**: caller-independent systemd service, registry-validated disables, memory caps, evidenced by the r7 hold and r8 OOM control. It was deliberately scoped by the r8 wave "to the analyzer-disable recipe … with the r8 kill cited as the necessity proof, not containment evidence" (`SCORECARD.md:1183-1186`). It does **not** claim log retention.

But its evidence production read the log: the r7 entry cites `ghidra.log:276`/`:278` honor lines (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:17`), and `.ufo/waves/arc2-loop1-round7/E3.md:9` records a **snapshot copy**:

- `/var/tmp/arc2-l7r7-E3-scratch/ghidra-snapshot-t1858.log`, 461 lines / 35,650 B, sha256 `0f37896f…6df8`, copied 19:01:38, last line 19:01:26 — **~4.5 min of the run (through the 19:04:11 exit) not captured**.

That artifact no longer exists: `/var/tmp/arc2-l7r7-E3-scratch/` is absent (checked this session); no repo copy exists (grep for the hash matches only `E3.md:9`); r7's receipt manifest lists three files and no log (`.../round7/receipts/MANIFEST.txt`). So r7 demonstrates **capture once, custody never** — a hash plus prose survive, not the bytes.

## 3. Before-state: every prior log use is unretained

- `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:72-73`: `Missing Go bootstrap type info` seen in `ghidra.log`; "dir since deleted, so this is observed-not-cited".
- `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:64-65`: timeline read from live `/tmp/rea-ghidra-hKzt9I/ghidra.log`; dir removed at `-deleteProject`.
- `corpus/knowledge/2026-10-13-r4-14-libsignal.md:50`: "the log dies with it" (wholesale deletion).
- `.ufo/waves/arc2-loop1-round6/E5.md:48`: "ghidra.log/script.log not recoverable"; `E3.md:45` same class. r6 was where the missing log blocked the analyzer-honor check.
- Baseline inventory: `git ls-tree -r --name-only b563c79 | grep -c 'ghidra\.log'` → **0**; `grep -c 'rea-ghidra'` → **0**.

So the capability state before r17 is: **committed, re-checkable REA session-log bytes = 0**, with at least five read-but-lost instances. That is the concrete "before" the new row can stand on.

## 4. Pilot: mechanics shown, capability not yet demonstrated

`.ufo/waves/round-17/pilot/README.txt:1` says "NOT the final measured runs". `:4-5` records 1 s polling `cp` and "no keep knob found"; `:6` records the two limits: the last copy can miss tail lines, and **pre/post carrier pins were not recorded**. `SHA256SUMS:1-4` pins the four retained log files (11,207 B and 10,973 B; 123/125 lines; `sha256sum -c` → all 6 OK this session).

What the retained bytes carry (observation):
- `pilot/shfmt-log/ghidra.log:83-85`: `Untested Go version [1.27.0]`, `Missing Go bootstrap type info…`, `GolangSymbolAnalyzer … unable to get GoRttiMapper`.
- `pilot/esbuild-0.25.12-log/ghidra.log:63-67`: `Using Go API snapshot for 1.23.12`, `Using Go API snapshot for version 1.23.12`, … `Go version 1.23.12`.

That is the first time these lines exist as bytes in the repo rather than as a deleted path. But the pilot alone fails the admission test: no pins, no receipt, tail known-incomplete — exactly what `carrier-run.py`/`receipt-validate.py` add (`contract.md` sections carrier-run.py, receipt-validate.py).

## 5. Overlap verdict — same artifact, three lifecycle stages

**[INFERENCE, grounded in anchors above]** The shared object is `ghidra.log`; the rows differ by lifecycle stage:

| Stage | Prior state | New row? |
|---|---|---|
| 1. **Capture** — read/copy the live log | Demonstrated repeatedly: r3 E11/E12 samples, r4-12, r4-14, r6 attempts, r7 E3 snapshot | **No** — prior technique |
| 2. **Custody** — bytes committed, carrier pinned pre/post, receipt validates, attribution to own run | Never: r7 snapshot left the tree; baseline holds 0 log bytes | **Yes** |
| 3. **Extraction/compare** — mechanical classification of Go analyzer lines + prediction-vs-observation | Never as an instrument; prior use was seat-side grep (r7 `E3.md:41-51`) | **Yes** |

Independence check: the pilot's capture ran in a plain `Popen` with **no systemd** (`README.txt:2-4`), while r7's systemd run never retained its log. Remove either mechanism and the other still stands — the rows are orthogonal, not nested.

Also adjacent but not overlapping: row 3 (`SCORECARD.md:621`) is a pre/post pin pair too, but it pins **inputs/environment** (5 operator config paths); the new row pins **outputs/evidence** (carrier + its session log). Same custody pattern, different artifact class — worth naming in the row so a reviewer does not read it as another config-custody instance.

## 6. Proposed move (one, bounded)

Enter the row with the **measured phrase unchanged** — `retained REA Ghidra-session log capture` is the exact string `measure.py` keys on (`contract.md` measure.py) — and put the scope distinction inside the row's "What it can now do" cell:

> durable custody of a pinned carrier's own REA/Ghidra session log across teardown (bytes + sha256 + pre/post pin compare in a validating receipt), with mechanical Go-analyzer-line extraction and prediction-vs-observation comparison; the act of reading the live log is prior technique (`.ufo/waves/arc2-loop1-round7/E3.md:9` snapshot), not the claim.

Gate: row enters only after **≥3 final runs** exist under `.ufo/waves/round-17/runs/*/receipt.json`, each `receipt-validate.py` exit 0, `pins_compare.equal` true; pilot cited only as preliminary. First-working round: `round-17`. Append-only: do **not** widen or edit row 4; the cross-reference in the new row is the only link.

**Affected axes**
- **calibration — improves**: blocks both failure modes — pre-claim (pilot has no pins/receipt, `README.txt:1,6`) and double-count (r7's log check stays inside the containment row's evidence, not a second capability). Supplies a falsifiable before/after: committed log bytes 0 at `b563c79` → >0 at the measured revision.
- **depth — improves (indirectly)**: the row points at the retained lines that carry the prediction-vs-observation table (shfmt `:83-85`, esbuild `:63-67`), and makes future citations possible where r4-10 had to write "observed-not-cited" (`:72-73`).
- **No axis harmed**: no existing row edited, no score relabeled, no new REA operation, no carrier executed.

## 7. Risks / contradictions to state

1. **Pilot-as-evidence is the trap.** Citing `pilot/` in the evidence pointer would satisfy a text grep while violating `AXES.md:62-64` (no passing demonstration) and the pilot's own `README.txt:6`. The pointer must be the final receipts.
2. **"Capture" wording invites the duplicate charge.** r7 E3 already copied the log by hand; if the row says "capture" without the custody qualifier, a non-author reviewer can reasonably call it r7's technique re-entered. Keep "retained … custody" as the noun.
3. **Completeness overclaim.** Polling cannot guarantee the final lines (`README.txt:6`; `carrier-run.py`'s `log_capture_limit` field). The row must carry that limit, in the shape of r14's `Limits:` (`SCORECARD.md:2209-2211`); `receipt-validate.py` must not treat a short tail as tamper.
4. **Cross-lane attribution.** New-dir detection can grab a sibling lane's session log (the SentinelPollRace lane owns this). The row's limits should say captures are attributable only to the run the tool itself started.
5. **Measurement coupling.** Paraphrasing the row name breaks `measure.py`'s `retained REA Ghidra-session log capture` check; scope text must live in the description cell, not the name.
6. **Mismatch handling.** `claims.json` C2 requires mismatches reported, never hidden; the row must not imply the prediction table matched — it records comparisons, including failures.

## 8. Verification the L1 can run

```sh
git ls-tree -r --name-only b563c79 | grep -c 'ghidra\.log'          # expect 0 (before)
python3 -I .ufo/waves/round-17/measure.py <REV>                     # capability row present 0->1
python3 -I .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/*/receipt.json  # exit 0 each
(cd .ufo/waves/round-17/pilot && sha256sum -c SHA256SUMS)           # 6x OK today
grep -c 'arc2-loop1-round7/E3.md' <capability row>                  # cross-reference present
```

No tools installed; no REA analyze/search/decompile and no Ghidra run was performed.
