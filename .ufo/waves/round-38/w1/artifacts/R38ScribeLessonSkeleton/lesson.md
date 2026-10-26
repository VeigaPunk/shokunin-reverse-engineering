# Round 38 — standard big-endian SquashFS v4 toward Core, self-assessment calibration, and the dependency premise the freeze got wrong

Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`. Freeze v1 `e059ca9391642d5b71b6662cabcbdce0d9308719`
(`plans/round-38-claims.md`, `tools/round-38/{c1-counter.py,c2-counter.py}` with their selftests,
harness `tools/round-38/c1-run.sh`, carriers, instruments, census start, R36-CL1 stamp). Control
receipts `efd5c47a72a50b3a434783f82268fb4a96e636a1` — seven frozen controls (`CTL-C1-0/1/2`,
`CTL-C2-0/1/2/3`), **all exit 1**, i.e. no control meets the target, so neither kill rule stopped a
claim. Wave-1 dispatch `9c9d496b` (40 seats). While this seat ran, the L1 left a **freeze v2
amendment** in the working tree (`plans/round-38-claims.md` and `tools/round-38/c1-counter.py`,
`git status` ` M`, mtime 2026-10-26T03:25:45-03:00): it withdraws the v1 extractor-free framing
and pairs before/after receipts, i.e. it applies M38-3's fix by hand. That
amendment is **uncommitted at this seat's read** and is not judged here; v1 is the only frozen bytes
`[L1-FILL]` for the v2 commit. This file is the **wave-1 draft skeleton**, written before
WAVE-DONE; every citation pointer whose final target is set by the L1 at integration is marked
`[L1-FILL]`. Nothing here is claim data: the predicate, counters and carriers are frozen and were
not edited by this seat.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M38-1 | attribution — a report cited receipts it had not committed (R37-CL1, one round later) | fleet `.ufo/reports/round-37/kaidoku.md:14` names a receipts directory under `.ufo/waves/round-37/probes/` (its `rea/` subdirectory); that subdirectory holds one entry (`K1/firmware.bin_extract/…`) and **zero** `*.json` envelopes — the only committed envelope is `.ufo/waves/round-37/probes/rea-k3.json`, with no K2/K4 and no before-arm receipt | none: no rule read a report's citations against the tree; the round-37 verifier spotcheck found it, and the same sentence is repeated verbatim at `corpus/lessons/round-37-verifier-spotcheck.md:80` | pre-report cited-path checker `cited-path-check.py`: every backticked repo-relative path must resolve under a declared root, and a directory cited for receipts must hold ≥1 `*.json`. **Red-before**: `python3 -I -B .ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/cited-path-check.py /home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kaidoku.md <lane> /home/vgpnk/Projects/shokunin` → `:14: '.ufo/waves/round-37/probes/rea/' cited for receipts holds no *.json receipt (1 entries)`, **FAIL (1 of 10 citations), exit 1** (`red-cited-path.txt`). Green: the same command on `corpus/lessons/round-36.md` → `ok (20 citations resolved)`, exit 0 |
| M38-2 | landing — the round closed with no lesson file (R37-CL3, second round) | `git -C <lane> cat-file -e 77091b49…:corpus/lessons/round-37.md` → `fatal: path … does not exist`, **exit 128**; the same call for `round-36.md` → **exit 0**. Re-confirmed at the round-38 base, not merely read from the verifier | PROTOCOL — the lesson file is a report-contract requirement, but nothing checked it *before* the wave closed | lesson-skeleton gate run before WAVE-DONE: for each round, `git cat-file -e $REV:corpus/lessons/round-$N.md`. **Red-before**: `bash .ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/lesson-skeleton-gate.sh <lane> 77091b49… 36 37` → `ok round-36` / `MISSING round-37`, **exit 1** (`red-lesson-gate.txt`). Green: round 36 alone, exit 0. The skeleton itself now exists at `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/lesson.md` while `.ufo/waves/round-38/w1.ready` exists and no `w1.done` marker does |
| M38-3 | stale-premise — the *corrected* BE-dependency premise at the freeze was itself false | the frozen v1 bytes (`git show e059ca93:plans/round-38-claims.md`, copy kept at `.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/claims-at-freeze-v1.md`, sha256 `13ea8eba…9815`), line 27: "26.6.4; no external extractor dependency", and `tools/round-38/c1-run.sh:6`: "no external extractor needed for standard BE v4". Against it: the pinned handler source (S108/S112, `python/unblob/handlers/filesystem/squashfs.py:24-26,68-69`) declares `EXECUTABLE="sasquatch"`, `V4BE_EXECUTABLE="sasquatch-v4be"` and `get_dependencies()` returns both; and the four-arm run on K1 (carrier sha256 `1cfb6c33…117e`, unchanged) gives off-PATH `after.json` → gap `missing-extractor-dependency`, `dependencies ["sasquatch-v4be"]`, **0 files**, versus on-PATH `after.sasquatch-on-path.json` → **5/5 oracle files, 0 gaps**, both exit 0. The round-37 statement (`plans/round-37-claims.md:42-45`) was a *PATH-doctored probe shape*, which is exactly what reproduces; the carrier was never extraction-blocked while the declared tool is resolvable (binaries installed 2026-10-26 01:22, on PATH for the round-37 receipt `.ufo/waves/round-37/probes/rea-k3.json`: coverage `complete`, gaps `[]`, handler `squashfs_v4_be`) | QUALITY #4-style live probe — re-measure on this host with the artifact named by absolute path + sha256 (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK1/summary.json` records both PATHs and every envelope digest; `after.json` is the assigned arm) — the freeze's parenthetical came from a single ambient-PATH run whose PATH filter (`grep -v sasquatch`) removes component names, not the binaries inside a component | before-arm recheck **before** the premise is frozen: `premise-check.py` compares the written premise with an off-path/on-path receipt pair. **Red-before**: `python3 -I -B .ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/premise-check.py --off .ufo/waves/round-38/w1/artifacts/R38ExecAfterK1/after.json --on .ufo/waves/round-38/w1/artifacts/R38ExecAfterK1/after.sasquatch-on-path.json <v1 copy> tools/round-38/c1-run.sh` → names `claims-at-freeze-v1.md:27` and `c1-run.sh:6`, **FAIL, exit 1** (`.ufo/waves/round-38/w1/artifacts/R38ScribeLessonSkeleton/red-premise.txt`). Green: the same command over this lesson (quotes the false sentence, asserts the dependency) → exit 0. The L1's uncommitted v2 amendment applies this fix `[L1-FILL]` |
| M38-4 | harness/environment — the frozen after-mode harness could not produce a receipt at all | `R38ExecAfterK3/harness-after-mode-failure.txt`: at HEAD `9c9d496b`, `bash tools/round-38/c1-run.sh after <carrier> <out> <scratch>` → **exit 1**, `{"details":{"provider_id":"unblob","operation":"extract_firmware","diagnostics":{"reason":"Extraction output root already exists"}}}` with an empty stderr — the harness did `mkdir -p "$OUT"` before REA, and REA refuses a pre-existing extraction root (`rea-agents 6.5.0 dist/artifacts/SafeOutputTree.js:56-58`, non-recursive mkdir → EEXIST). K1's first assigned arm hit the same (`R38ExecAfterK1/summary.json`, `outdir_precreated: true`) | seat `R38ExecAfterK3` — the first falsifier; the freeze shipped the harness with no selftest, so the counters' 15/14-case selftests could not catch it | replace the `mkdir -p` with `rm -rf "$OUT"` (L1 `cb4326b2`, oracle mode unchanged). **Red-before** is the measured exit 1 above; green is `R38ExecAfterK3/harness-after-mode-post-fix-ok.json` at `cb4326b2`: exit 0, handler `squashfs_v4_be`, 4 files, 0 gaps, coverage `complete`, evidence id `ev_fbc3be2e963…` |

## Gate

### Sources opened this round (2026-10-26) — ids from the ScribeSOURCES block `[L1-FILL]` for final numbering

| row | source | decision | reason | flip |
|---|---|---|---|---|
| S112 | unblob 26.6.4 `squashfs_v4_be` magic-pattern dispatch (same file as S108, pattern-level scope) | **admit** | the dispatch that routes a standard BE v4 image to `SquashFSv4BEHandler` is the producer statement the claim moves; scope keeps it distinct from S108 (extractor names, argv, AVM test) and it explicitly does *not* claim in-process extraction | the pattern block or the `EXTRACTOR` binding changes at tag 26.6.4, or the row is read as evidence that the handler extracts without `sasquatch-v4be` |
| S113 | unblob 26.6.4 `squashfs_v4_be` integration fixtures (K3/K4 byte provenance, LFS rule, `__output__` apples) | **admit** | closes R37-CL2's fixture half: tag 26.6.4 = commit `1fcc7a0a584…`, `__input__/squashfs_v4.bin` = LFS oid `9c7c523c…97c0` (4096 B) = committed `K3/carrier.bin`, `__input__/squashfs_v4.nopad.bin` = `a29ddc15…56ed` (307 B) = `K4/carrier.bin`, MIT; the LFS pointer trap is named so a clone cannot be mistaken for bytes | an LFS oid or media byte differs from the lane carrier sha256 at that tag, or the tag is re-pointed |
| S114 | Freetz-NG wiki "SquashFS 4 (BE)" (registers the round-37 copy `.ufo/waves/round-37/probes/avm.txt`) | **admit**, scope-limited | closes R37-CL2's text half: the Freetz-NG raw page is live per the wave-1 scout (HTTP 200, 1514 B, sha256 `100948f3…5fc9`; not re-fetched by this seat), and this seat independently fetched the older raw path `Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` (HTTP 200, 1496 B, sha256 `c1c43f6f…a5d5`, `diff` against `.ufo/waves/round-37/probes/avm.txt` empty, 2026-10-26); per the scout, its only delta against the wiki page is the stripped H1. It states AVM-BE properties only, no carrier and no extractor behaviour | upstream rewording (pinned sha mismatch), or a real AVM-BE image that contradicts the block-length/mkfs_time properties |
| S115 | 7-Zip 26.04 supported-format list **and** the BE-v4 refusal probe | **reject** (as a BE-v4 oracle) | empirical only: the vendor's page lists SquashFS among "Unpacking only:" formats (line 111), so "7-Zip cannot read SquashFS" would be a fabrication; what was observed is narrower — the installed 7-Zip 26.04 (x64, 2026-10-05) refuses all four frozen BE v4 carriers, `exit 2`, "Cannot open the file as archive" (`R38CrossToolK4/7z-refusal.txt`, K1–K4) | a 7-Zip release that opens one of these carriers and publishes members matching the oracle; then the FLIP is a positive row, not a repaired rejection |
| S116 | `tools/round-37/gen-squashfs.py` (own-work; K1/K2 provenance) | **admit** | K1/K2 are lane-generated standard BE gzip images; the writer is committed at the base (`sha256 1c7c5e88…` as recorded in the block) and its `MAGIC` map / `mkfs = bytes_used if e == 'avm' else MKFS_TIME` lines are the reason an AVM image cannot be produced by accident | the writer changes after the freeze, or K1/K2 stop being reproducible from the committed source trees |

### Assimilation — theme sasquatch / unblob / AVM (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`)

**Id-collision check (scratch, before any append).** `^ {0,3}\|[[:space:]]*S[0-9]{3,}` over the lane
registry and the staged append block: **111 registry ids** (S001–S111), **132 staged ids**
(S106–S237), `comm -12` → **6 collisions, S106–S111** (`reg-ids` sha256 `015e600e…`, `staged-ids`
`93841167…`, `collisions` `b184a461…`; lane HEAD at read `cb4326b2`). Guard proof on a fixture with a
two-space-indented `  | S002 |` row → detected (`S001 S002`, count 2); indentation matrix cases b–f
agree; **0** registry and **0** staged S-rows escape the 0–3-space pattern, 0 tab-indented, 0
unmatched (`R38ExecIdCollision/guard-proof.txt` §A–§C).

Resolved **by document**, not by number: staged S106 (unblob README at `HEAD`) is the same document
as lane **S110** (unblob README at tag 26.6.4 — the pinned row wins); staged S107 (devttys0 README
`master`) is the same URL as lane **S111** — both are dropped rather than renumbered. The other four
colliding ids are new documents (core(5), binwalk, dncil, jadx READMEs) and take the next unused ids
on append. This round's opened rows therefore start at **S112**, above the highest lane id.

- **Decision 1 — ADMIT `unblob-format-matrix`.** Re-opened live 2026-10-26: `https://unblob.org/formats/`
  HTTP 200, 216890 B, sha256 `8f8c29af…bbc5`; `grep -o '<h2 id=' | wc -l` → **97**, and
  `grep -c 'more than 30 different'` → **3** — both counted claims of the entry reproduce; the vendor SquashFS list (including v4-BE) is the
  entry's own reading and was not re-counted here, so the admit rests on the two counts plus the
  page's identity. Reason: producer's own coverage statement, small, re-countable. Flip to refuse: the next
  fetch changes the handler count or the vendor list, or the quoted "more than 30" sentence
  disappears. Its staged id S122 must be renumbered into the S112+ space on append `[L1-FILL]`.
- **Decision 2 — REFUSE `sasquatch-unblob-avm-branch` as staged.** Its closing premise ("a real AVM
  image still needs Freetz's patched `mksquashfs4-avm-be` … or a genuine AVM firmware image") is
  contradicted by the staged sibling `avm-image-extraction.md` of the same date, which records the
  image built and extracted 4/4; its source S189 is `unblob/main` **unpinned** although lane S108
  already pins tag 26.6.4 with the same method; S190/S191 are campaign-local
  `lanes/kaidoku/round9/work/lead2-avm-branch.tsv`. Its valid half (the AVM branch is signalled by a
  missing `-be`) is carried by the admitted S114 scope. Flip: premise corrected to the round-11
  result and S189 repinned to 26.6.4.
- **Decision 3 — REFUSE `avm-image-extraction`, `avm-image-build-blocker`, `avm-le-image-genuine-marker`,
  `avm-le-variant-reachability`, `avm-firmware-image-unblob` as staged.** Each carries measurement rows
  from campaign-local `lanes/kaidoku/round{10,11,12,13,14}/work/*.tsv` (QUALITY #1: not lane-retained
  bytes); the live sources inside them (S198, S206, S214, S216, S217, S220) are unproblematic but do
  not carry the measurements. Same disposition as round 36's decisions 2–4, restated for the
  entries still staged. Flip: import the tsvs (and the built image / build log the rows cite) into the
  lane and re-measure.
- No existing registry row's `status`, `recheck` or used-by cell changed this round.

### Quarantine slice (absent-defect register, READ-ONLY; kaidoku rows: 5)

Derived with the assignment's `awk`; **5 rows**, every line carrying an S-id (register lines 82,
315–318); the seat's re-derivation is byte-identical to `.ufo/waves/round-38/assimilation/quarantine-slice`
(`diff` exit 0, sha256 `7383a90e…`). Hand-checked live this round
(`R38ExecQuarantine/quarantine-verdicts.txt`):

- **S150 REFUSE (fabrication class).** Live article HTTP 200, 174088 B, sha256 `42d59c48…6e34`; the
  registered section heading 「シンボルがない場合のヒント」 occurs **0** times, as do 「ヒント」 and
  「シンボルがない」. The article is real and on-topic and its own recheck (`llvm-objdump` → 6) holds;
  the named section does not. (Round-36's verdict stands.)
- **S113 ADOPT-WITH-ANCHOR, count must be corrected.** Live page HTTP 200, 368063 B; **22**
  `hreflang` links = **21 locales + x-default**, so the row's "served in 17 locales" is not
  reproducible — the mechanism (multi-locale surface, bare URL unstable) is.
- **S117 UNVERIFIABLE (not fabrication).** DOI resolves 302 → IEEE Xplore **202** with a 0-byte body;
  Semantic Scholar 429 twice; dblp bot-challenged. Crossref (DOI-keyed, 200) confirms title and venue
  "SoK: Demystifying Binary Lifters…", SP 2022, pp. 1100–1119 — the paper exists, the abstract-level
  quotes cannot be checked against a readable body.
- **S136 ADOPT-WITH-ANCHOR.** `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` (12897 B), heading
  line 3; the quoted phrase `2 of 24 verbs are` occurs once, at line 8. Own work, locatable now, still
  unadopted.
- **S147 ADOPT-WITH-ANCHOR (heading names need correction).** `HOST-CONTRACT.md` (3386 B);
  `grep -c '207 tools'` → 1 at line 41; there is no "REA release" heading — the headings are
  `## State as of this writing` and `## Expected \`doctor\` output on this host`. **Drift caveat:** the
  frozen counting command pins `rea-agents 6.5.0`, while the contract text says 6.7.0.
- None of the five is cited by an admitted entry, so none is appended.

### Kill-rule and control status

Seven frozen controls, all **exit 1** (`CTL-C1-0/1/2`, `CTL-C2-0/1/2/3` in
`.ufo/waves/round-38/controls/`): no control meets its target, so neither claim was stopped before
data. The controls do not, however, exercise the harness: M38-4 is the defect they could not see.

### Wave-1 falsifiers this draft must carry forward

- **K1 assigned arm fails the predicate, on the mechanism, not the bytes.** `R38ExecAfterK1/after.json`
  is a valid envelope (`evidence_id` recomputes) that identifies the chunk as `squashfs_v4_be` and
  publishes **0 files** with the dependency gap; it cannot satisfy "carries no extraction gap". The
  wave's complete K1 envelope is the on-PATH arm.
- **K2 cannot satisfy "no extraction gap" as frozen.** Its oracle is 3 regular files; REA correctly
  publishes all 3 and additionally reports one `unpublished-entry` gap for the symlink
  `firmware.bin_extract/var/lib/run-link`. A predicate that forbids every gap makes K2 structurally
  unmatchable on these bytes — reported, not repaired (predicate frozen at `e059ca93`).
- **K4 is clean:** coverage `complete`, handler `squashfs_v4_be`, 4/4 apples, 0 gaps, `ev_3d1197d1…`.
  K3's post-harness-fix envelope is also clear: 4/4, 0 gaps, `ev_fbc3be2e…`.
- **The freeze v2 amendment is in the working tree, not in a commit.** At this seat's read
  (2026-10-26T06:26Z) `git status --porcelain` shows ` M plans/round-38-claims.md` and
  ` M tools/round-38/c1-counter.py`; both were still changing while this file was written, so no
  insertion count, selftest case count or predicate sentence from v2 is asserted here. Until it is
  committed, `e059ca93` is the only frozen byte set, and its predicate is the one M38-3 falsifies.
- At the tip `9c9d496b` the recount is `carriers_matched 0` (C1) and `mismatches 1` (C2,
  `prov_core:REA MCP server` → `evidence/doctor/`), i.e. both measures still sit at the base
  (`R38ExecRecountBase/{c1-at-tip,c2-at-tip}.json`). Claim data is not yet committed; the after
  receipts are still wave artifacts `[L1-FILL]`.

### Routed defects carried into this round — status at the draft

- **R37-CL1** (commit every receipt the report cites) — fix shown as M38-1; not yet enforced by a lane
  script `[L1-FILL]`.
- **R37-CL2** (register `avm.txt` and the unblob BE fixtures) — closed by S113 (fixtures) + S114
  (Freetz note, naming the committed copy) on append `[L1-FILL]`.
- **R37-CL3** (file `## Gate` decisions, including the 7-Zip rejection) — this section is the filing;
  the underlying "no lesson file" class is M38-2, whose gate this draft passes.
- **R36-CL1** (commit the `w2.ready.dispatched` stamp) — landed: the freeze commit carries
  `.ufo/waves/round-36/w2.ready.dispatched` (`git ls-tree -r --name-only e059ca93 .ufo/waves/round-36`).
- **R36-CL2/CL4/CL6** — landed as fixes per the frozen plan; not re-measured by this seat.
- `considerthese/` is absent in this lane (`ls considerthese` → no such file or directory), as the
  plan states.

## [L1-FILL] citation pointers

- Core row `## Round-38 additions to Core` citing `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`
  and naming `squashfs_v4_be`: `PROVINCE.md:<line>`.
- Frontier note superseding the big-endian bullet; sibling-aside repair at the round-36 Core row;
  `corpus/README.md` Frontier bullet: `<line>`.
- SOURCES rows S112–S116 with `used-by` = the entry path; register order and renumber map of the four
  new staged documents: `corpus/SOURCES.md:<line>`.
- After receipts committed at `corpus/evidence/round-38/c1/K*/after.json`; landing commit: `<hash>`.
- Correction pointers into `corpus/lessons/round-37-verifier-spotcheck.md` for R37-CL1..CL3 closure.
