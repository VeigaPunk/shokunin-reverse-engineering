# R38ReviewerEntryQuality — QUALITY-bar review of the drafted C1 entry and SOURCES append block

Seat: reviewer (leaf, advisory). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Reviewed: (a) `.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md` (rows S112–S116,
5926 B as read); (b) the drafted entry `.ufo/waves/round-38/w1/artifacts/R38ScribeEntry/entry.md`
(18 899 B). Nothing was repaired; every finding below is reported, not fixed. No frozen predicate,
counter, carrier, oracle or registry row was changed; no VCS mutation.

Revisions read: base `77091b49`, freeze `e059ca93`, controls `efd5c47a`, dispatch `9c9d496b`,
HEAD `cb4326b2` (worktree). Tooling ledger: **no tool installed or upgraded** (no pacman, no uv, no
npx install; used curl, sha256sum, jq, python3 stdlib, git read-only). Scratch
`/fast/scratch/hyaku/kaidoku-r38/R38ReviewerEntryQuality` (incl. two `recheck*.XXXX` probe dirs)
removed at the end; the only files written are this report and
`artifacts/R38ReviewerEntryQuality/` (checker script).

## 1. SOURCES append block — mechanical schema checks (all pass)

Re-parsed from the artifact bytes (cell split on `|`, 5 non-blank lines):

| row | cells | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|
| S112 | 11 | code | A | mined | 2026-10-26 | on-release | exactly the entry path |
| S113 | 11 | dataset | A | mined | 2026-10-26 | on-release | exactly the entry path |
| S114 | 11 | docs | B | mined | 2026-10-26 | 365d | exactly the entry path |
| S115 | 11 | tool | A | rejected | 2026-10-26 | on-release | exactly the entry path |
| S116 | 11 | own-work | A | mined | 2026-10-26 | on-release | exactly the entry path |

- 11 cells and no literal `|` inside any cell on all five rows (measured).
- Ids S112–S116 are the next unused after the registry's S111 (`grep -oE '^\| S[0-9]+'
  corpus/SOURCES.md | sort -V | tail -3` → S109, S110, S111); absent from
  `.ufo/waves/round-38/assimilation/reg-ids`; the staged merge bundle's S112+ labels are other
  documents (renumber-by-document rule, `R38ExecIdCollision.md` §"Rule for the open four"), so no
  collision is created. S115 `rejected` is per the seat brief (7-Zip rejection candidate with
  reason + flip), not a schema violation.
- The report's embedded block and the artifact are row-identical (diffed; no drift between the two
  copies the L1 could integrate).
- Counter fit: every row matches `c1-counter.py`'s row regex, has `opened == 2026-10-26` (cell 9)
  and the entry path in `used-by` (cell 11), so all five satisfy the counter's `sourced` binding
  (worktree `c1-counter.py:234-246` under the v2 amendment; same rule at v1).

Anchor pins re-verified against the pinned bytes (each check run by this seat):

| pin | command | result |
|---|---|---|
| S112 sha256 `2d7b901b…5599287`, 590 lines | `sha256sum` + `wc -l` on the scout's fetched copy `artifacts/R38ScoutUnblobHandler/squashfs.py.26.6.4.txt` | match |
| S112 line anchors 454/455/463/513/514/522/527 | `sed -n` on that copy | all seven lines carry exactly the quoted text |
| S113 LFS oids = K3/K4 carrier pins | `sha256sum corpus/evidence/round-37/c1/K{3,4}/carrier.bin` vs `.ufo/waves/round-38/c1/carriers.json` | match (`9c7c523c…`, `a29ddc15…`) |
| S113 pointer-file quote | `curl -s` of `…/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be/__input__/squashfs_v4.nopad.bin` | line 2 verbatim `oid sha256:a29ddc15…dfe956ed`, line 3 `size 307` |
| S114 upstream sha256 `100948f3…875fc9`, 1514 B | fresh `curl` of the raw master page | match; the teaches quote sits at upstream lines 9–10 |
| S114 local-copy delta | `sed -n '8,9p' .ufo/waves/round-37/probes/avm.txt` | quote verbatim at avm.txt lines 8–9 (upstream body minus its H1) |
| S115 site sha256 `06761967…1ddcafc`, 6789 B; line 111 | fresh `curl -sSL https://www.7-zip.org/` | match; line 111 is exactly `RPM, SquashFS, UDF, UEFI, VDI, VHD, VHDX, VMDK, XAR and Z.` under `Unpacking only:` (label line 109) |
| S115 probe claim (exit 2, "Cannot open the file as archive", K1–K4) | read `artifacts/R38CrossToolK4/7z-refusal.txt` | 4× `### exit_code=2`, error line verbatim |
| S116 sha256 `1c7c5e88…01ba8dd5`, 216 lines, present at base | `sha256sum` + `wc -l` + `git show 77091b49:tools/round-37/gen-squashfs.py \| sha256sum` | match; lines 7/173/213–214 carry the quoted text |

Quote word counts in `teaches` (measured): S112 3+6, S113 2 (+2 unquoted paraphrase), S114 20,
S115 11, S116 8 — all ≤25.

## 2. Entry draft — QUALITY-bar review

### 2a. What verifies (checked, not assumed)

- **Provenance trio first:** lines 1–5 are `source:` (S112, S113, S114, S115, S116), line 6
  `verified-at: 2026-10-26, access window 06:16:41Z–06:24:00Z …`, line 7 `recheck:` with a cadence
  and a runnable-looking command. Order and presence conform to the seat brief.
- **Source rows exist:** every id on a `source:` line (S112–S116) exists in the append block; the
  bottom Sources table additionally cites S107, S108, S110, S111, all present in
  `corpus/SOURCES.md`. **No cited id is absent from both** (checker:
  `artifacts/R38ReviewerEntryQuality/check-entry.py` → "cited ids absent …: NONE"). All five
  `source:`-line rows satisfy the frozen counter's `sourced` binding (opened 2026-10-26 + used-by
  names the entry), so `entry_present`+`sourced` will both turn true when the entry lands.
- **Counts carry commands and reproduce.** I re-ran the entry's own jq on the four receipts its
  Receipts table names and got exactly the table's numbers:
  `jq -c '.normalized_result|{files:(.files|length),bytes:.published_bytes,gaps:(.extraction_gaps|length),cov:.coverage,handlers:[.chunks[].handler]}'`
  → K1 `{"files":5,"bytes":9656,"gaps":0,"cov":"partial","handlers":["squashfs_v4_be"]}`;
  K2 `{"files":3,"bytes":10283,"gaps":1,"cov":"partial",…}`;
  K3 (diagnostic) `{"files":4,"bytes":28,"gaps":0,"cov":"complete",…}`;
  K4 `{"files":4,"bytes":28,"gaps":0,"cov":"complete",…}`. Stored evidence ids match the table
  (`ev_eccca733…`, `ev_4d478254…`, `ev_096b500d…`, `ev_3d1197d1…`).
- **Oracle-match counts are real:** importing the frozen counter's own `load_oracle`/`published`/
  `matched` and applying them to `R38ExecProvincePatch/after-K{1..4}.json` yields hits
  5/3/4/4 of oracle rows 5/3/4/4 — the entry's "5 3 4 4 hits out of 5 3 4 4".
- **Chunk/unpublished/depth claims hold** on all four ProvincePatch receipts: single chunk with
  `root_file_range {offset:0, length:<carrier size>}` and `extraction_failed:false`; K1
  `unpublished_entries: []`; K2 exactly the `var/lib/run-link` symlink; `max_depth 3` and empty
  `depth_limited_paths` on all four.
- **The K1 symlink-removal diagnostic is verbatim** in `R38ExecAfterK1/after.sasquatch-on-path.json`:
  `{"input_path":"$input","report":{"__typename__":"MaliciousSymlinkRemoved","severity":"WARNING","link":"…/firmware.bin_extract/link-to-hello","target":"…/extracted/hello.txt"}}`
  (the entry's `…` elides only scratch paths; field names and values match).
- **The counter-state sentence in `verified-at` is accurate:** `R38ExecRecountBase/c1-at-freeze.json`
  and `c1-at-tip.json` both read `carriers_matched 0`, `entry_present false`, `sourced false`
  (re-read from the artifacts).
- **The false frozen premises are refused, not repeated.** The draft's opening bullets name the
  `sasquatch-v4be` dependency, refuse "no external extractor" ("unblob 26.6.4 contains no in-process
  SquashFS reader; the handler always shells out"), state that the round-37
  `missing-extractor-dependency` gap **reproduces** when the binary is absent, and the closing
  section states K2's unavoidable gap and that `carriers_matched` cannot exceed 3 under the frozen
  counter. This is the honest reading of the wave-1 measurements
  (`R38ExecAfterK1.md` §2a/§3, `R38ExecAfterK3.md` §2–4, `R38ExecAfterK4.md` F1 dependency matrix,
  `R38CrossToolK1.md` §6) and corrects `plans/round-38-claims.md:27,64` — a claims-doc defect for
  the L1 to disclose, since the freeze forbids editing it.
- **Cross-tool framing is honest:** "Read this as driver parity, not as two-implementation
  agreement" — exactly the caveat `R38CrossToolK4.md` §5a.3 requires (same binary, same `-be` flag
  on both legs).
- **Negative claims carry sweeps:** the reader-refusal table sweeps all four carriers for both
  `unsquashfs` 4.7.5 (exit 1, 4/4) and 7-Zip 26.04 (exit 2, 4/4) with artifact paths; the AVM
  negative is scoped to what was parsed ("Observed on the two fixture carriers … the parse itself
  was not re-run here", scout-labelled).
- **Quotes:** every true quoted span (backtick/double-quote delimited) is ≤25 words (measured over
  the whole entry; the two >25 hits my first pass reported were the reviewer script's own
  blockquote-line captures, not quotes). Locations: S112 quotes carry line ranges (L24-26, L40-41,
  L48-50 — all verified against the pinned copy); the REA continuation quote is located by
  continuation id + envelope; tool-output quotes are located by artifact.
- **No credential material** (pattern scan: none).
- **Byte arithmetic:** K1 9656 = 18+9000+609+0+29; K2 10283 = 22+21+10240; K3 = K4 = 28 = 4×7 —
  all correct against the oracle sizes.

### 2b. Entry defects (reported, not repaired)

- **B1 (medium — the recorded recheck command cannot reproduce).** The `recheck:` line ends with
  `… bash tools/round-38/c1-run.sh after … "$S/K4" >/dev/null && jq -c '…' "$S/K4/after.json"`.
  The harness prints the envelope to **stdout** and never writes `after.json` into OUTDIR
  (`tools/round-38/c1-run.sh:26-28`; the extraction tree contains only extracted members).
  Measured, run verbatim: harness exit 0, then `jq: …/K4/after.json: No such file or directory`,
  **jq exit 2** — the expected output can never be observed by that command. With stdout captured
  instead (`> "$S/after.json"`), the same run prints exactly the stated expectation
  `{"files":4,"gaps":0,"handlers":["squashfs_v4_be"]}` (measured). The verify command must itself
  reproduce (QUALITY #13's rule; #18's recheck clause).
- **B2 (low — one count without its command).** The oracle-match sentence ("re-implemented exactly
  as the frozen counter does it … → `5 3 4 4` hits out of `5 3 4 4`") gives the rule but no
  runnable command; every other count in the entry carries one. The numbers are real (I reproduced
  them with the counter's own functions), but the entry's own standard is "every number carries its
  command".
- **B3 (low — edited kind text attributed to carriers.json).** The carrier table's column is
  "kind (carriers.json)" but the K2 cell reads "symlink + space in a name" where carriers.json says
  "symlink + unicode name" (the correction is right — the name is ASCII with a space,
  `R38CrossToolK2.md` §7.1 — but it is presented as carriers.json's text). Quote verbatim or mark
  the correction inline.
- **B4 (low — unlabelled universal).** "It appears whenever `sasquatch-v4be` is not resolvable by
  the unblob subprocess" is measured on K1 (assigned arm), K3 (arm A) and K4 (dep-probe matrix);
  K2's off-PATH run was never measured (its seat ran ambient PATH only). The mechanism (S112
  `get_dependencies` + `command.py` FileNotFoundError) makes it a safe inference, but the sentence
  is stated as observed fact with no inference label or K2 caveat.
- **B5 (low — wrong gloss in the Sources table).** The grouped row "S107, S108, S110, S111" glosses
  S108 as "unblob handler at the old path". S108's registered path is the same
  `python/unblob/handlers/filesystem/squashfs.py` at tag 26.6.4 as S112's (registry row verified);
  there is no old path. The grouped row's "what it grounds here" cell also omits S108's ground.
- **B6 (low — S114 quotes without locators, propagated from A1).** The Gate section's two S114
  quotes are located only as "S114 (AVM-BE block length)" / "S114 (AVM-BE marker)". Measured
  locations: upstream raw lines 9–10 (block length) and avm.txt lines 13–14 (mkfs_time; upstream
  14–15). QUALITY #42 wants the line or section with the quote.
- **B7 (low — spliced pointer quote).** The S113 Gate quote
  `oid sha256:a29ddc15…dfe956ed / size 307` joins pointer-file lines 2 and 3 with " / " replacing
  the newline — not one contiguous run of the served bytes (QUALITY #42's contiguity rule; line 2
  alone is contiguous and sufficient).
- **B8 (info).** The REA continuation quote is a 19-word contiguous **prefix** of a longer
  sentence, truncated without ellipsis. Contiguous, located, ≤25 — acceptable, noted for
  completeness.
- **B9 (info — receipt-set mixing).** The Receipts table draws K1 from `R38ExecProvincePatch`,
  K2/K4 from the `R38ExecAfterK2`/`R38ExecAfterK4` seats and both K3 envelopes. All eight named
  envelopes/id pairs verify, but the L1 should land one canonical receipt set and re-point this
  table (the entry itself flags "Not committed evidence yet").
- **B10 (info — one negative without its sweep inline).** The Sources-table ground "that the
  devttys0 README says nothing about big-endian" rests on the scout's sweep
  (`grep -c -i -E 'big|endian|-be'` → 0, `R38ScoutSasquatchReadme.md` Finding 1), which the entry
  does not name at that point (the AVM section names the scout for its own parse).

## 3. Append-block findings (defects reported, not repaired)

- **A1 (low, quote locator).** S114's `teaches` quote carries no line/section locator in the row —
  neither `anchor` nor `teaches` names where in the pinned bytes the 20-word passage sits
  (measured: upstream lines 9–10; local copy lines 8–9). S113's quote location is derivable from
  its anchor (the LFS pointer file is named) but likewise not stated in the `teaches` cell.
- **A2 (medium, uncommitted anchor path).** S115's `anchor` cites
  `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt`, untracked at every revision I
  read (`git status --porcelain` lists `.ufo/waves/round-38/w1/` untracked; no commit contains it).
  R37-CL1's rule is "commit every receipt the report cites; cite only what is committed" — until
  the L1 commits that artifact or re-points the anchor, a reader resolving the row dead-ends.
  S112–S114/S116 anchors cite only upstream URLs and committed lane paths.
- **A3 (low, scope wording contradicted by the lane's own control).** S115's `scope` says "not a
  SquashFS reader", but the lane's positive control shows 7-Zip 26.04 *does* read little-endian
  SquashFS v4 (`artifacts/R38CrossToolK1/7z-le-positive-control.txt`: exit 0, `Type = SquashFS`,
  `Method = ZLIB`, `Big-endian = -`; `R38CrossToolK3.md` §3). Accurate scope: "not a **big-endian**
  v4 reader / not a BE-v4 oracle" — which is what the `teaches` cell already says.
- **A4 (low, mislabel propagation).** S116's `scope`/`teaches` say the writer "emits the standard
  big-endian **gzip** images". `file(1)` reports "zlib compressed" and the superblock compression
  id is 1 (zlib/gzip method), no gzip container (`R38ExecAfterK1.md` D4, `R38CrossToolK2.md` §5).
  The claims file's wording is the origin; the entry itself uses the accurate "compressor gzip
  (id 1)" phrasing in its AVM section.
- **A5 (info, no defect).** S112's scope correctly refuses the "in-process extraction" reading
  ("the selected handler still shells out to `sasquatch-v4be`"), and S113's scope bounds K3/K4
  provenance to the `__input__`/`__output__` fixture pair. Both match the pinned source and the
  measured dependency matrix (`R38ExecAfterK4.md` F1: only-`sasquatch-v4be` PATH → ok;
  only-`sasquatch` → gap; neither → gap).

## 4. Calibration hazards the entry had to satisfy (ground truth used above)

1. **"No external extractor" is false.** unblob 26.6.4's `squashfs_v4_be` handler shells out to
   `sasquatch-v4be -be …` (`squashfs.py:25-26,40-41,65-69`); with that binary off `PATH` the
   assigned arm reproduces `missing-extractor-dependency` and publishes 0 files. Gap-free receipts
   exist only because `~/.local/bin/sasquatch-v4be` is installed. The draft refuses this premise
   correctly.
2. **K2 can never be gap-free.** Its in-tree symlink `var/lib/run-link -> ../../a/run.sh` is
   retained as metadata and costs one `unpublished-entry` gap on every run; under the frozen
   counter (`after_gaps_empty` per carrier) K2 cannot match, so `carriers_matched` tops out at 3
   and P38-C1 is an honest stop as frozen. The draft states this in "What this is not claimed to
   show".
3. **Cross-tool "independence" is driver parity** (same executable, same flag on both legs); the
   independent anchors are the K1/K2 source-tree oracles and the K3/K4 `__output__` expectations
   (which are unblob's own lineage). The draft carries the caveat.
4. **Evidence ids are run-path-sensitive** (three K4 runs → three ids; stored == recomputed is what
   holds) — the draft's Receipts-table limit states this with the actual id triple.
5. **Claims-text mislabels** ("gzip images", "unicode name") are corrected or avoided in the draft
   (B3 records the one place the correction is mis-attributed).

## 5. Concurrent freeze-v2 amendment observed mid-review (recorded, not judged)

While this review was running, the worktree gained **uncommitted modifications to two frozen
instruments** (observed 03:28 -03:00 via `git status --porcelain`; I wrote neither file):

```
 M plans/round-38-claims.md      (mtime 03:25:45.200983368 -0300; diff: 83 lines changed)
 M tools/round-38/c1-counter.py  (mtime 03:27:58.062389102 -0300; diff: 71 lines changed)
```

The claims diff self-declares "**freeze v2** (pre-scoring amendment)": it drops the falsified v1
premise ("no external extractor dependency", `plans/round-38-claims.md:27,64` at v1), restates
P38-C1 with `sasquatch-v4be` available, and **adds a paired before-receipt clause**
(`corpus/evidence/round-38/c1/K*/before.json`, run with `sasquatch-v4be` unavailable, publishing
none of the oracle files and naming `sasquatch-v4be` as the missing dependency). The counter diff
adds `before_*` bindings (`before_present`, `before_subject_ok`, `before_operation_ok`,
`before_missing_extractor_gap`, `before_oracle_hits == 0`) and selftest cases for them (18 cases,
was 15). Facts I verified around it:

- **No claim was scored under v1** — the only counter runs on record are the do-nothing recounts
  (`R38ExecRecountBase`, `carriers_matched 0` at base/freeze/tip), so the v2 note's "no claim was
  scored under v1" matches the retained record.
- **The committed controls are still the v1 bytes** (`git ls-files .ufo/waves/round-38/controls/`
  → 7 files, unmodified in the worktree); the v2 note says "Kill rules apply to the v2 controls",
  so v2 controls still have to be generated, scored and committed.
- **The `sourced` binding is unchanged** (`c1-counter.py:234-246` in the worktree: same
  `c[8] == OPENED and ENTRY in used` rule) — every §1 conclusion about S112–S116 survives v2.
- **K2 is still blocked under v2:** `matched()` still requires `after_gaps_empty`
  (worktree `c1-counter.py:204`), and K2's in-tree symlink produces an `unpublished-entry` gap on
  every run — so `carriers_matched` still tops out at 3 and C1 remains an honest stop unless the
  gap clause is re-scoped again.
- **Before-receipt coverage is incomplete:** no `before*.json` exists anywhere yet
  (`find .ufo/waves/round-38/w1/artifacts -name 'before*.json'` → empty;
  `corpus/evidence/round-38/c1/` absent). Before-shape envelopes exist for K1
  (`R38ExecAfterK1/after.json`, off-PATH), K3 (`R38ExecAfterK3/after.json`, arm A) and K4
  (`R38ExecAfterK4/dep-probe/env-nosasq-gap.json`, `env-leonly-gap.json`); **K2 was never measured
  with `sasquatch-v4be` off PATH** (`R38ExecAfterK2.md` ran ambient PATH only), so a K2
  before-receipt must still be produced before any v2 scoring.

Consequences for my two review targets:

- **B11 (entry, scope gap under v2).** The drafted entry predates the v2 amendment: it contains no
  before-receipt section, does not name `corpus/evidence/round-38/c1/K*/before.json`, and its
  Receipts table lists after envelopes only (K3's arm-A envelope is the only before-shape envelope
  it names, without calling it that). Under v2 the entry must carry the paired before/after
  evidence per carrier; the measured before-arm material exists for K1/K3/K4 and is missing for K2.
- The **append block needs no change** for v2 (schema and `sourced` binding unchanged; no new
  source candidate appears in the v2 claims' sourced sentence, `plans/round-38-claims.md:113-115`).
- Process note for the L1's filing checklist: `.ufo/waves/round-38/w1.ready.dispatched` is present
  but untracked — the same leftover class as routed defect R36-CL1; it must be committed before the
  round is filed.

## 6. Verdict

- **Append block: schema-conforming** (11 columns, no in-cell pipes, ids S112–S116 next-unused,
  statuses per brief, opened 2026-10-26, used-by exactly the entry, all five rows satisfy the
  frozen counter's `sourced` binding) with **all anchor pins verified against the pinned bytes**.
  Defects: A1 (missing quote locator, S114/S113), A2 (anchor cites an uncommitted artifact, S115),
  A3 ("not a SquashFS reader" overstates — the lane's own LE positive control contradicts it),
  A4 ("gzip" mislabel propagated into S116).
- **Entry draft: substantively honest and measured** — it refuses the false frozen premises, names
  the real dependency, states K2's unavoidable gap and the resulting honest stop, and every number
  I checked reproduces from the named receipts. Defects: B1 (the `recheck:` command cannot
  reproduce — measured jq exit 2; the fix is to capture stdout), B2 (oracle-match count without a
  command), B3–B7 (attribution/locator/splice wording), B8–B10 (informational).
- **No violation of the hard rules:** no unverifiable claim found (all checked claims reproduce),
  no credential material, quotes ≤25 words, source rows all exist, status/used-by/opened conform.
- For the L1: the entry as drafted will turn `entry_present`/`sourced` true; the remaining C1
  bindings (`province_core_row`, `coverage_map_row`) and the receipts' landing are the
  integration's work; `carriers_matched` will be 3 (K2's symlink gap), so P38-C1 stays an honest
  stop under v1 **and under the v2 worktree amendment** (the v2 counter still requires
  `after_gaps_empty`, worktree `c1-counter.py:204`). Under v2 the entry additionally needs the
  before-receipt section (B11) and a K2 before-receipt must still be produced; the v2 controls
  still have to be generated and scored before any claim data is scored.
