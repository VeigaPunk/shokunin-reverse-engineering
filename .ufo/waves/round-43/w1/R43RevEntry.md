# R43RevEntry — round-43 landing-document format review (wave 1, pre-freeze)

**Verdict: CONFIRMED** — all four landing-document formats verified against the
round-42 landed bytes at base `6b9e64fe7e0de202d9383baad5792fbfe039a743`; the
R42-V5 front-matter correction is exact; copyable templates with their cited
evidence delivered in `artifacts/R43RevEntry/`.

Seat: R43RevEntry (reviewer, leaf). Lane root:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `6b9e64fe` (lane main at
round start; current HEAD `d22686e1` + `1ed29de2` are the L1's own round-43
draft/dispatch commits — no landing content yet). No tools installed or
updated (read-only review; nothing gained by an install). Scratch
`/fast/scratch/hyaku/kaidoku-r43/w1-R43RevEntry` created and removed; all
citations are lane paths.

## 1. Knowledge entry `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`

**The R42-V5 correction, verified.** Routed defect R42-V5
(`corpus/lessons/round-42-verifier-spotcheck.md:92`): the round-42 v3-core
entry opened with `status:` at line 3 BEFORE `source:` at line 5. Verified at
base:

- `git show 6b9e64fe:corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md | grep -n '^status:\|^source:\|^verified-at:\|^recheck:'`
  → `3:status:` … `5:source:` … `13:verified-at:` — the violation.
- `git show 6b9e64fe:corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md` →
  sources lines 3–10 (S112, S118, S119, S120, S121, S122, S124, S130),
  `verified-at:` line 11, `recheck:` line 12, **no `status:` field** — the v4
  entry itself is compliant; the new entry inherits its shape.

The governing rule is `/home/vgpnk/Projects/shokunin/CORPUS.md:18`
("Each `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`")
and `:163-166` (provenance trio first; provenance in prose or HTML comments is
unreadable to a freshness sweep). So the new entry's front-matter MUST be:

1. `source:` lines — per the wave-1 spec (`w1-gen.py:98`), the set is S112,
   S118–S121, S130, **S135** (the v4 table's own citations plus the new license
   basis opened this round; S135 capture: HTTP 200, 1068 B, sha256
   `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`,
   re-verified by the R43SrcLicense seat at 2026-10-27T08:17:52Z —
   `artifacts/R43SrcLicense/row-S135-docs.md`);
2. `verified-at: 2026-10-27`;
3. `recheck:` — frozen-interpreter table-only check (15 rules, exit 0) plus the
   round-43 counter as the scored-state re-derivation;
4. ONLY THEN `status:` (the r42 v4 entry needed none; if used, last).

**Body must record** (per the claims file and the round-42 entry's shape): the
round-42 stop (C02 declared `{extractor-failure, unpublished-entry}` vs observed
`{depth-limited, extractor-failure, unpublished-entry}`; stop receipt
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`; M42-2 in
`corpus/lessons/round-42.md:26`; QUALITY 85 `corpus/QUALITY.md:93`); the
generator change (refusal, exit 3 `declared_tuple_unobserved`, red/green
CTL-C1-2); the frozen-table byte-identity (region sha256 at `d1681696` vs
measured rev); the new score (`matched/n`, exit, `combo_unseen_majority`,
`counter_sha256` + `counter_sha256_at_freeze` per the freeze-integrity rule);
the manifest's `generator.tuple_check`; the carried limits.

Template: `artifacts/R43RevEntry/template-1-knowledge-entry.md` (with the
L1-fill checklist).

**Hygiene note (transient, resolved):** at 08:2xZ an empty untracked file sat
at this exact corpus path (observed via `git status --porcelain` + zero-byte
read); by my next check it was gone. If a seat created it, that was a bounds
touch (seats never write `corpus/`); if the L1 pre-created it as a placeholder,
note the R42-V2 lesson (no green/assert without committed output). Nothing
remains to fix; the L1 writes the entry only when the measured numbers exist.

## 2. SCORECARD `## Round 43` section

Verified format at `SCORECARD.md:3469-3487` (base). Structure to mirror:

1. `## Round 43 — <one-line summary>`;
2. one-line header paragraph: `Base \`6b9e64fe…\`; freeze \`<<F>>\`
   (\`plans/round-43-claims.md\` + frozen paths); controls \`<<c>>\`; data
   \`<<d>>\`; measured revision \`<<REV>>\`; scores \`<<s>>\`. Wave 1: N seats
   (\`.ufo/waves/round-43/w1/\`). Lesson \`corpus/lessons/round-43.md\`.`
3. claim table — columns EXACTLY:
   `| claim | axis / surface | before | after | counting command | measured at | verdict (author) |`;
4. `Owned scores:` paragraph (coverage/depth/calibration deltas with command A
   and the saturation line; capability-row sentence);
5. optional `### Capability addition` 4-column table
   (`| Capability | What it can now do | Evidence pointer | First-working round |`);
6. `- **planned (round 44, after a steer):** …`;
7. `- **retired:** none.`

Claim-row content is dictated by `plans/round-43-claims.md`: R43-C1 before =
freeze exit 2 `no_manifest_at_rev` + CTL-C1-1/2/3 receipts; after = `matched 78`
target, `observed_features_match_declared true`, every binding true, exit 0;
counting command `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
R43-C2 before = gate exit 1, `rows_failed` 18 (CTL-C2-0); after = exit 0,
`rows_failed []`, `rows_total ≥ 129`; counting command
`python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV>`.
The round-42 `planned` bullet already names this round's moves (QUALITY-85
refreeze; second choice R41-CL3 copies) — the round-44 planned bullet must
carry forward whatever wave 2/closure routes (R42-CL2 wave-2 attack, R40-CL2).

Template: `artifacts/R43RevEntry/template-2-scorecard-round-43.md`.

## 3. LOG round-43 entry

Verified format at `LOG.md:3174-3185` (base); entries append at end of file.
Heading `## Round 43 — 2026-10-27 (KaidokuR43)` then bullets in the round-42
order: **Claims** / **Wave 1** / **Data** / **Scores at `<rev>`** /
**Re-verification (freshness)** / **Frontier step** / **Tool install**.
Round-43 specifics: freeze hash; wave size from `w1-results.json`; C1 data =
78 envelopes seeded by the freeze via `heldout-gen-v4r43.py --run` (L1-run,
post-freeze) with `generator.tuple_check` all-equal; C2 data = 17 copies +
map under `corpus/evidence/round-43/local-sources/` + `local-sources.json`;
Frontier step = SOURCES 134 → 135 (S135), census exit 0 both ends,
assimilation admit `sasquatch-prebuilt-package-inventory` (re-grounded per
`w1/R42Assim.md` ADMIT, ≥1 reject on record), quarantine slice 5 rows
hand-checked, `considerthese/`: absent as a report line.

Template: `artifacts/R43RevEntry/template-3-log-round-43.md`.

## 4. Round report required sections (prompt §4)

Read `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-43.md` §4 in
full. Required sections, in order, for the L1 report at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kaidoku.md`:

1. **Work performed**
2. **Landed changes**
3. **Before → after measurements**
4. **Sources & frontier**
5. **Trend verdicts** (`expansion`, `quality`, `discernment`; one of
   `improved` / `harmed` / `unchanged` / `unprovable-but-better`, with
   evidence; no scalar)
6. **SHONEN** (`[x]` only with a named non-author verifier; `[~]` with a
   resolvable evidence pointer; `[ ]` untouched)

Marker rule: a contentless report (placeholder text, missing required sections
other than **Sources & frontier** and **Trend verdicts**, or no evidence
pointers) = round **failed**; skipping those two named sections alone is `ok`
plus one logged minimum-content conformance defect. Sources & frontier must
carry the census before→after (`scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku`, exit 0 at round end required; start
output already committed at `.ufo/waves/round-43/census-start.txt`), rows added
by tier, rows touched old→new, frontier rows advanced.

Template: `artifacts/R43RevEntry/template-4-round-report-sections.md`.

## Residual risk / verification gaps

- Templates quote the round-42 formats exactly, but the round-43 numbers
  (`matched`, exits, commit hashes) are L1-fill by construction — this seat
  runs nothing post-freeze.
- The `## Round 43` SCORECARD heading summary and the planned-round-44 bullet
  depend on wave-2/closure outcomes not yet written; the template marks them.
- S135's source line in Template 1 uses the L1's recorded 08:08Z capture plus
  the R43SrcLicense seat's independent 08:17:52Z re-open; the L1 should paste
  the access time of its own authoritative capture in the `source:` cell.
