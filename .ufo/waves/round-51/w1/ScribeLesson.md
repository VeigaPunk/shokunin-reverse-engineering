# ScribeLesson — round-51 lesson skeleton draft (wave 1, build)

Seat: `ScribeLesson` (leaf; no subagent dispatch; read-only on the lane tree).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Lane tip at read time: `39f41d4f15a87689a41c16c5c17ed885fbfb7da3` (`origin/main` = same).
**Draft:** `.ufo/waves/round-51/w1/ScribeLesson/lesson.md` — the candidate content of `corpus/lessons/round-51.md`, shape-following `corpus/lessons/round-50.md`.
**Receipts:** `.ufo/waves/round-51/w1/ScribeLesson/receipts/` (30 files; each carries the exact command, exit code, stdout sha256 and UTC second).
Writes made by this seat: the two paths above only. No lane file, `plans/`, `corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` or fleet file was touched; no git/jj mutation; no REA run; no download.

## Verdict

Draft delivered. `## Mistakes` is seeded with the two defects the round-50 closure routed (`corpus/lessons/round-50-verifier-spotcheck.md:76-77`), each row already carrying its class, its measured evidence pointer and its captured-by verdict, with the landing-time pointer left as a `<<…>>` placeholder. `## Gate` and `## Census` are scaffolds with the round-50 column headers; the Census "before" side is filled because it is already measured and committed, the "end" side is a placeholder.

## Findings

- **F1 — M51-1 (`reference-drift`) confirmed and quantified.** `grep -c 646d29c9 LOG.md` → `0` (exit 1, no match) at tip `39f41d4f`; the same hash is at `SCORECARD.md:3796`. The commit is real and reachable: `git cat-file -t 646d29c9` → `commit`, `git merge-base --is-ancestor 646d29c9 refs/heads/main` → exit 0, and it is the commit that added the four `corpus/evidence/round-50/c1/<id>/after.json` files (full hash `646d29c9df4ef77499248f95589cb9526c6dea19`). Captured-by: **none** — `grep -c 646d29c9 corpus/QUALITY.md` → 0 and `grep -n "LOG.md" corpus/QUALITY.md` → no match; no lane instrument reads the LOG against landed commits. Fix row: the append-only LOG correction entry this round, with the fail condition stated (the hash must appear at the landing revision **and** the prior 308 434 bytes of `LOG.md` must remain a byte prefix — measured at `log_md_bytes_at_tip.txt`).

- **F2 — M51-2 (`landing`) confirmed, and the drift is narrower than the closure's wording.** The lane `SHONEN.md` (sha256 `3ae428cf…`, 20 lines) has 8 indented lines over 4 boxes → **4 surplus** (one per box; the contract allows one), plus **2 trailing prose paragraphs** after the last box's evidence lines ("Round-43 correction: …" at line 18, "Round 49 (non-author verifier: …)" at line 20). The seed block is **not** at fault: with the mark normalised (`[~]`→`[ ]`) the lane's seed is byte-identical to PROTOCOL's seed (`PROTOCOL.md:439-448`), both sha256 `0a6d81c7…`. The closure's "the seed block and box texts are canonical" is therefore exactly right, and the drift is precisely (a) one surplus indented line per box and (b) the trailing prose. Captured-by: **the template clause** (`PROTOCOL.md:432`) — the rule existed and was not applied at the round-50 landing; no lane instrument re-checks the file's canonical form (the three lane tools that read `SHONEN.md` read it as a graded file, none compares its seed block to the template).

- **F3 — the uncited hash `646d29c9` is load-bearing, not cosmetic.** Wave-1 finding F2 (`w1/CritRuleDerive/findings.md`) shows the v2 counter's `receipt_fresh` clause is **false** for the four committed round-50 envelopes precisely because the commit that added them (`646d29c9`) is a strict *ancestor* of the round-51 freeze, not a descendant of it. The very hash the LOG omits is the one that decides a clause's verdict. The lesson's M51-1 row now says so, so the fix is not filed as cosmetic hygiene.

- **F4 — the claims file was amended during wave 1; the draft was re-read against the amended bytes.** `plans/round-51-claims.md` now carries the "Wave-1 amendment record" (F1-F11 from `w1/CritRuleDerive/findings.md`) and an amended header naming three revisions (round base `1aa27369…`, claims-draft `f04b51dd…`, dispatch `39f41d4f…`) plus "the C2 before-arm base is the claims-draft commit `f04b51dd…` (F11)". The draft's freeze paragraph and `<<BASE NOTE>>` were updated to that state rather than to the pre-amendment text.

- **F5 — the SHONEN regeneration target is decided by the claims file, and the two candidates differ by one header.** Routed-defect repair 2 (`plans/round-51-claims.md:236-239`) names the template file `/home/vgpnk/Projects/kimi-shokunin/templates/mint/SHONEN.md` verbatim with `<name>` = `kaidoku-shokunin` (substituted bytes sha256 `57fb2e04…`). That file is PROTOCOL's seed block (`PROTOCOL.md:439-448`, sha256 `0a6d81c7…`) **plus** a 6-line `<!-- CANONICAL TEMPLATE … -->` header the seed block does not contain; the two differ only by that header (`shonen_seed_vs_template_body.txt`). Both satisfy PROTOCOL's mechanical check on the seed block, so the lesson states the digests of both and asks the landing to say which file was used — the file that is landed must be diffable against a named target.

- **F6 — Census "before" is already committed and can be stated, not guessed.** `.ufo/waves/round-51/l1/sources-census-start.txt` (committed at `f04b51dd`, blob `aa81d2ac…`, file sha256 `b4a6d2d6…`) records **exit 0**, **19** `W04` duplicate-URL lines, final line `kaidoku ok …/corpus/SOURCES.md`, **156 rows** — matching the claims file's declared census-before exactly. The draft states it; only the "end" side is a placeholder.

## Out of scope (not this seat)

The draft does not carry a `## Sources & frontier` table or a `## Wave-2 dispositions` section: no round-51 source row is registered and no wave-2 seat has run. Both are named as placeholders in the Gate and Honest-stop scaffolds instead of being invented. The `## Mistakes` table is left with exactly the two seeded rows; M51-3+ are the L1's to append as the wave-1 attacks and the w2 falsify findings land (the draft says so in place).

## Artifacts

- Draft: `.ufo/waves/round-51/w1/ScribeLesson/lesson.md`
- Receipts: `.ufo/waves/round-51/w1/ScribeLesson/receipts/` (30 files: `log_grep_646d29c9.txt`, `scorecard_grep_646d29c9.txt`, `quality_grep_646d29c9.txt`, `git_commit_646d29c9_type.txt`, `git_646d29c9_ancestor_of_main.txt`, `git_show_stat_646d29c9.txt`, `log_md_bytes_at_tip.txt`, `shonen_lane_sha.txt`, `shonen_box_indent_counts.txt`, `shonen_drift_summary.txt`, `shonen_target_A_protocol_seed_sha.txt`, `shonen_target_B_template_verbatim_sha.txt`, `shonen_seed_vs_template_body.txt`, `shonen_lane_vs_targetA_diff.txt`, `protocol_shonen_contract_row.txt`, `census_start_tail.txt`, `census_start_W04_count.txt`, `sources_row_count.txt`, `spotcheck_routed_defects_6.txt`, and the git/base-revision receipts).
- Tool installs/updates: none. No network access was used by this seat.
