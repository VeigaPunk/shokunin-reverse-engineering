# R38W2W1Integrity — wave-1 evidence integrity audit (round 38 attempt 2, wave 2)

**Verdict: CONFIRMED** — the wave-1 evidence set is internally complete and consistent with the landed bytes. 40/40 registry names have a matching, non-empty, untruncated report; every artifact path cited in a w1 report resolves at `3b960fe5` (or is a documented sibling-lane/fleet/URL-tail/hypothetical reference); the w1 tree is byte-identical from `3b960fe5` to `HEAD`; the L1's edits to wave-1 drafts (entry title, S110–S116 rows, README rows, PROVINCE wording) all move *toward* the honest-stop measurement and contradict no wave-1 finding. No truncation, no placeholder-only reports, no fabricated citations found.

Seat: R38W2W1Integrity (leaf, wave 2). Lane: `kaidoku-shokunin`. Landing commit judged: `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`; later commit checked where relevant: `0fc6113376a156fddc3ec385386d71c3a4a9f690`; `HEAD` = `e265533e`.

## Method (all read-only)

- `jq` over `.ufo/waves/round-38/w1/swarm-registry.json`; set-diff of member keys vs `*.md` basenames.
- Per report: byte/line/word counts, `iconv` UTF-8 validity, tail-coherence, placeholder scan (`TODO|PLACEHOLDER|TBD|FIXME|FILL ME|<your `).
- Regex extraction of 222 distinct repo-relative paths cited across the 40 reports; each checked with `git cat-file -e 3b960fe5:<path>`; misses classified by reading the citing line, then re-checked at `0fc61133`/`HEAD`, on disk in sibling lanes, or dismissed as URL tails / firmware-internal / hypothetical paths.
- Draft-vs-landed diffs: `git diff 77091b49..3b960fe5 -- PROVINCE.md corpus/SOURCES.md`; landed `corpus/README.md`/`SCORECARD.md`/`corpus/lessons/round-38.md`/entry at the landed commits vs w1 artifacts (`R38ScribeEntry/entry.md`, `R38ScribeSOURCES/append-block.md`, `R38ExecProvincePatch/patch.txt`, `R38ExecReadmePatch/{patch.txt,README.patched.md}`, `R38ScribeLessonSkeleton/lesson.md`, `R38ScribeScorecardDraft/scorecard-section.md`).
- `git diff --stat 3b960fe5..HEAD -- .ufo/waves/round-38/w1/` → empty; `git status --porcelain .ufo/waves/round-38/w1/` → clean. Wave-1 evidence was not touched after landing.
- Sibling/fleet citations spot-verified read-only on disk (14+ paths across chousa/kake/kengaku/revenger/shokuknow/fleet root).

## Headline answers

1. **Registry vs reports: 40 = 40, exact set match** (diff empty, `SET-MATCH`). The registry stores spawn declarations (`kind/role/item/axes/milestone`, `agentId: null` — no result-status fields); it is a dispatch record, not a results manifest.
2. **`w1-results.json` does NOT exist** — not at `3b960fe5`, `0fc61133`, `HEAD`, or on disk. Nothing in w1 references it. The wave's machine state lives in `swarm-registry.json` + `w1-dispatch.json` + `w1-spec.json` + `w1.ready*` instead.
3. **Report health: all 40 pass.** Smallest 4,094 B (`R38ScoutSasquatchReadme`), largest 32,738 B (`R38ScribeEntry`), 640,852 B total; all valid UTF-8; all end on a coherent closing line. The 11 files matching placeholder/TODO patterns quote *other* artifacts (e.g. `R38ExecMirrorGate` quoting ScribeEntry's then-unpublished `<!-- placeholder: … -->` gate state; `R38SimplifierMinimality` flagging the draft lesson's `[L1-FILL]` rows) — none is itself a placeholder.
4. **Cited artifacts: all resolve at `3b960fe5`** after classification (below). `corpus/evidence/round-38/c1/K1..K4`, `tools/round-38/{c1-counter.py,c2-counter.py,freeze-drift.py}`, all 27 cited per-seat `w1/artifacts/<seat>/` subtrees, and every truncated-glob fragment (`ctl-c1-0/1/2.json`, `unblob-command-K{3,4}.txt`, `after-K{1..4}.json`, `replayA/`, `replayB/`) are committed.
5. **Contradictions: none factual.** Landed bytes agree with wave-1's central measured fact everywhere it is restated: K2's in-tree symlink leaves an `unpublished-entry` gap, R38-C1 is an honest stop, nothing is promoted. Landed PROVINCE frontier note, SCORECARD §Round 38 heading ("measured but not promoted (honest stop)"), README frontier bullet, and the landed entry's Status line all say exactly this.

## Seat table

| seat | report ok | cited artifacts ok | contradictions |
|---|---|---|---|
| R38ConnSeparability | yes | yes | — |
| R38ConnSiblingOverlap | yes | yes | — ; all citations are lane-prefixed sibling/fleet paths, 14 spot-checked on disk (chousa `round51/claims-erratum.md:12-19` exists and matches the quoted c3 dot-strip fix; chousa `round34/claims-a2.md` C3 line matches) |
| R38CriticClaimsC1 | yes | yes | — ; `corpus/knowledge/archive/<STEM>.md` is a counter-variant fixture cell, not a lane file |
| R38CriticClaimsC2 | yes | yes | — ; `corpus/evidence/doctor/doctor-6.5.0.txt` is a proposed fixture ("create …"), `2026-10-26-zzz-stub.md`/`docs/x.md` are negative examples |
| R38CriticSourcedClaim | yes | yes | — ; `scripts/sources-census.sh` is a fleet-root path (exists at `/home/vgpnk/Projects/shokunin/scripts/`) |
| R38CrossToolK1 | yes | yes | — ; `docs/deep/nested/file.dat`, `docs/readme.md` are carrier-internal paths (committed under `R38ExecProvincePatch/extract-K1/`) |
| R38CrossToolK2 | yes | yes | — |
| R38CrossToolK3 | yes | yes | — |
| R38CrossToolK4 | yes | yes | — ; cites only `unblob-command-K{3,4}.txt`, matching exactly what is committed |
| R38ExecAfterK1 | yes | yes | — |
| R38ExecAfterK2 | yes | yes | — |
| R38ExecAfterK3 | yes | yes | — |
| R38ExecAfterK4 | yes | yes | — |
| R38ExecBeforeArmRecheck | yes | yes | — |
| R38ExecEnvelopeRules | yes | yes | — |
| R38ExecIdCollision | yes | yes | — |
| R38ExecMirrorGate | yes | yes | — ; its census E04 duplicate-URL flag on draft S114 is what the L1 resolved by swapping the S114 URL |
| R38ExecProvincePatch | yes | yes | — ; draft Edit 3 (`## Round-38 additions to Core`) intentionally **not** landed; Edit 2 wording replaced by an inline frontier note (see findings F2) |
| R38ExecQuarantine | yes | yes | — ; shokuknow read-only inputs verified on disk |
| R38ExecReadmePatch | yes | yes | — ; draft rows re-worded by the L1 at landing (finding F3) |
| R38ExecRecountBase | yes | yes | — |
| R38ExecSelftests | yes | yes | — |
| R38MutC1 | yes | yes | — |
| R38MutC2 | yes | yes | — |
| R38RevengerPremise | yes | yes | — |
| R38ReviewerCodeAudit | yes | yes | — ; `tools/round-38/__pycache__/` correctly described as gitignored byproduct |
| R38ReviewerControlReplay | yes | yes | — ; `replayA/`, `replayB/` committed |
| R38ReviewerEntryQuality | yes | yes | — |
| R38ReviewerPredicateIdentity | yes | yes | — ; `docs/x.md` class = negative test examples |
| R38ReviewerReportDraftHealth | yes | yes | — ; itself documents that `tools/adb`, `tools/master/README-AVM-BE` etc. are URL tails, and flags the round-38/probes path defect |
| R38ScoutFreetzAvm | yes | yes (n/a) | — ; flags the assignment path defect `.ufo/waves/round-38/probes/avm.txt` (real copy is `round-37/probes/avm.txt`, committed); honest handling |
| R38ScoutSasquatchReadme | yes | yes (n/a) | — |
| R38ScoutUnblobFixtures | yes | yes | — |
| R38ScoutUnblobHandler | yes | yes | — |
| R38ScribeEntry | yes | yes | — ; draft entry title + source set superseded by L1 (findings F1, F4) |
| R38ScribeLessonSkeleton | yes | yes | — ; draft's 9 `[L1-FILL]` all filled in the landed lesson (0 remain) |
| R38ScribeSOURCES | yes | yes | — ; flags the same assignment path defect (F3) pre-landing |
| R38ScribeScorecardDraft | yes | yes | — ; draft's `[L1-FILL]` "125/125 after a landed entry" estimate superseded by landed 126/126 — correct, because **two** entries landed (BE entry + format-matrix); the draft marked the number L1-FILL |
| R38SentinelBounds | yes | yes | — ; fleet-root citations (`.ufo/l0-questions.md`, `.ufo/state/disk-guard.log`, kengaku files) verified on disk; explicitly labeled untracked/fleet |
| R38SimplifierMinimality | yes | yes | — ; its L1-FILL findings (S5/S8/L4) verified addressed in landed bytes |

## Findings by severity

**Critical / High: none.**

**Medium: none.**

**Minor / informational:**

- **F1 — w1-results.json absent.** `.ufo/waves/round-38/w1-results.json` does not exist anywhere (three commits + disk). If any downstream consumer expects a wave results aggregate, it will not find one; the registry + per-seat reports are the only machine-readable wave-1 state.
- **F2 — L1 rewrote the PROVINCE draft instead of landing it.** Draft patch (`w1/artifacts/R38ExecProvincePatch/patch.txt`) proposed 3 edits incl. a 13-line `## Round-38 additions to Core` section (Core row "Standard big-endian SquashFS v4 via the `squashfs_v4_be` handler") and a bullet continuation reading "big-endian standard SquashFS v4 superseded for Core — see `## Round-38 additions to Core`". Landed `PROVINCE.md` delta vs base is exactly two lines: the C2 `REA MCP server` pointer repair, and an inline frontier continuation ("Round 38: standard BE v4 measured through `sasquatch-v4be` …, not promoted — R38-C1 honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap."). No Round-38 Core section exists at `3b960fe5`. This is the correct outcome under the honest stop and the draft's own gating ("do not land it as a promotion row until the L1 rules on the gap"); no wave-1 statement is falsified — but any reader expecting the draft's Core section from the w1 evidence will not find it.
- **F3 — SOURCES rows materially rewritten at landing (draft ≠ landed).** Draft `append-block.md` vs landed `corpus/SOURCES.md` @`3b960fe5` (total diff: 6 insertions, 1 deletion):
  - **S112**: URL `github.com/onekey-sec/unblob/blob/…` (draft) → raw `raw.githubusercontent.com/…` (landed); scope rewritten from "magic PATTERNS … dispatch" to "v4 BE extractor dependency and argv … not the binaries themselves".
  - **S114**: Freetz-NG wiki blob URL (draft; the exact URL the mirror-gate census flagged as duplicate E04) → `Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` (landed).
  - **S115**: draft = 7-zip.org vendor page, type `tool`, grade A → landed = "7-Zip 26.04 BE v4 refusal — own-work (committed tool output)", rejected row; the landed entry (line 22) consistently says the refusal "is recorded as a rejected row (S115), not as a source".
  - **S116**: draft = `tools/round-37/gen-squashfs.py` own-work row → landed = unblob formats-matrix row (`https://unblob.org/formats/`), which supports the *assimilated* entry; the K1/K2 provenance survives in the landed entry body (line 11 names `tools/round-37/gen-squashfs.py`), so no evidence is orphaned.
  - **S110**: scope extended with unblob's own "78+" format-count sentence (the count-conflict the format-matrix entry relies on).
  - **S111**: unchanged. No landed row cites the defective `.ufo/waves/round-38/probes/avm.txt` (0 hits in landed SOURCES and entry).
- **F4 — Landed entry title differs from the w1 draft title.** Draft (`R38ScribeEntry.md:174` / `entry.md`): "Big-endian SquashFS v4: the `squashfs_v4_be` handler extracts through `sasquatch-v4be`, and gap-free depends on the link, not the endianness". Landed: "Standard big-endian SquashFS v4 through REA: needs `sasquatch-v4be`; in-tree symlinks stay gaps (measured, not promoted)". The draft also cited sources S112–S116; the landed entry's source lines are S112–S114 (S115 demoted to rejected row, S116 repurposed — both consistently reflected in SOURCES). Same measured facts, reframed from "gap-free depends on the link" to "in-tree symlinks stay gaps (measured, not promoted)".
- **F5 — README rows re-worded at landing.** Draft coverage-map row: "Big-endian SquashFS v4 recursion (round 38) … held (bounded, standard big-endian SquashFS v4) …" → landed: "Big-endian SquashFS v4 through REA (round 38) … measured, **not promoted** (Frontier) — … K1 5/5, K2 3/3, K3 4/4, K4 4/4 … K2's in-tree [symlink]"; knowledge-index row landed with "Frontier, not Core". The per-carrier file counts in the landed row match the w1 receipts' shape (K1 5 regular files, K2 3, K3/K4 4 — oracle rows committed at `corpus/evidence/round-38/c1/K*/`).
- **F6 — Assignment path defect (pre-flagged, correctly contained).** The wave assignment named `.ufo/waves/round-38/probes/avm.txt`, which does not exist; four seats (ScoutFreetzAvm, ScribeSOURCES, ReviewerReportDraftHealth ×2) flagged this before landing and used the committed `round-37/probes/avm.txt` (sha256 `c1c43f6f…`). Landed bytes contain no reference to the defective path.

## Residual risk & verification gaps

- Citation extraction was regex-based; a path wrapped across lines in an unusual way could in principle be missed. Mitigated: every extraction fragment ending in `-` or `/` was manually resolved, and all 27 per-seat `w1/artifacts/` subtrees cited were confirmed committed.
- Sibling-lane and fleet-root citations were verified against today's disk state (read-only); those lanes can move independently, so their resolution is a point-in-time fact, not a freeze-grade guarantee.
- I did not re-derive the numeric contents of w1 receipts (counts, sha256s inside artifact JSONs) — that is the other wave-2 seats' ground (control replay, counter reruns). My scope was existence/integrity/consistency, and at that level nothing failed.
- `w1-results.json` absence is reported as fact; whether the round's protocol *requires* that file is not decidable from the lane alone.

## Tooling record

Nothing installed or upgraded; no `pacman`, no `uv`, no `npx`; only `git` (read-only subcommands: show/log/diff/ls-tree/cat-file/rev-parse/status), `jq`, `grep`, `find`, `ls`, `iconv`, `wc`, `sed -n` (print-only), `tail`/`head`. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2W1Integrity` (path list only) removed at close.
