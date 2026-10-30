<!--
DRAFT (wave 1, seat ScribeLesson, 2026-10-30) — the candidate content of
`corpus/lessons/round-51.md`. Nothing in the lane tree was edited; this file and
`.ufo/waves/round-51/w1/ScribeLesson/receipts/` are the seat's only writes.

Shape follows `corpus/lessons/round-50.md` (title, freeze paragraph, `## Mistakes`,
`## Gate`, `## Census before -> after`, honest stop). `## Mistakes` is SEEDED with the
two defects the round-50 closure routed (`corpus/lessons/round-50-verifier-spotcheck.md`
section 6, items 1 and 2); every value that only exists once the round lands is a
`<<…>>` placeholder. `## Gate` and `## Census` are scaffolds: the Gate table carries
its header row and no data rows (no round-51 source row is registered yet), and the
Census "end" side is a placeholder (the "before" side is already measured and
committed at `f04b51dd`, so it is stated, not left blank).

Legend: `<<…>>` = placeholder to fill at integration; `<<…>>` inside a Mistakes row =
the evidence pointer to add when the row's fix lands.
-->

# Round 51 — <<HEADLINE: one freeze; the device-accounting law re-derived per carrier class; the ddwrt failed-body route made executable>>

Lane `kaidoku`, round 51, attempt 1. Base `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (round base; the claims-draft commit is `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` and the wave-1 dispatch commit is `39f41d4f15a87689a41c16c5c17ed885fbfb7da3` — see the note below). Declared freeze `<<FREEZE HASH>>` — ONE commit (`plans/round-51-claims.md` with its wave-1 amended text, `tools/round-51/**` — `gap-rule.json`, `c1-counter.py`, `c1-controls.py`, `c1-run.sh`, `fetch-vendor.py`, `sqfs-triage-v6.py`, `census3.json`, the census re-derive tool, `misroot-sweep.sh` and the control fixtures), recorded in `.ufo/waves/round-51/l1/FREEZE` and `LOG.md` before any data run. There is no amendment series: wave 1 (36 seats, `.ufo/waves/round-51/w1/`) built and attacked the drafts before the freeze and its findings are folded into the plan's "Wave-1 amendment record" (F1-F11, from `w1/CritRuleDerive/findings.md`); a counter bug found after the freeze is a miss, never a patch.
Instruments: `tools/round-51/c1-counter.py` (R51-C1 coverage, v2 port of `tools/round-50/c1-counter.py`), `tools/round-51/sqfs-triage-v6.py` (R51-C2 depth, port of `tools/round-50-c3/sqfs-triage-v5.py`).

<<BASE NOTE (resolved by the wave-1 amendment F11; confirm at integration): the claims file header (amended during wave 1) now names three revisions — round base `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (the lane tip at round start), claims-draft commit `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`, wave-1 dispatch commit `39f41d4f15a87689a41c16c5c17ed885fbfb7da3` (the current tip; `origin/main` = same) — and fixes "the C2 before-arm base is the claims-draft commit `f04b51dd…`". The lesson's `Base` line must therefore name the ROUND base `1aa27369…`, and the C2 before-arm base `f04b51dd…` must be stated where the C2 measurement is reported; the freeze hash replaces the dispatch commit in the freeze paragraph once the freeze lands.>>

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M51-1 | `reference-drift` — the LOG never names the commit that landed the round-50 C1 after-receipts: `646d29c9` appears in the round-50 report's Landed-changes table and in `SCORECARD.md`, but nowhere in `LOG.md`, so the append-only log's history of the C1 measurement is incomplete | routed at `corpus/lessons/round-50-verifier-spotcheck.md:76`. Measured at tip `39f41d4f` (receipts `.ufo/waves/round-51/w1/ScribeLesson/receipts/`): `grep -c 646d29c9 LOG.md` → `0` (exit 1, no match; `log_grep_646d29c9.txt`), while `grep -n 646d29c9 SCORECARD.md` → `SCORECARD.md:3796` (`scorecard_grep_646d29c9.txt`). The commit itself is real and reachable: `git cat-file -t 646d29c9` → `commit`; `git merge-base --is-ancestor 646d29c9 refs/heads/main` → exit 0 (`git_commit_646d29c9_type.txt`, `git_646d29c9_ancestor_of_main.txt`); `git show --stat 646d29c9` → the four `corpus/evidence/round-50/c1/<id>/after.json` files (`git_log_oneline_646d29c9.txt`). The uncited hash is **load-bearing, not cosmetic**: it is the commit that added the four envelopes, and wave-1 finding F2 (`.ufo/waves/round-51/w1/CritRuleDerive/findings.md`, F2) shows the v2 counter's `receipt_fresh` clause is false for those receipts precisely because the adding commit (`646d29c9`) is a strict ancestor of the round-51 freeze, not a descendant of it — so the commit the LOG omits is the one that decides a clause's verdict | `none` — no QUALITY criterion requires a LOG entry to name a landing hash (`grep -c 646d29c9 corpus/QUALITY.md` → 0; `grep -n "LOG.md" corpus/QUALITY.md` → no match), and no lane instrument reads the LOG against the landed commits | the append-only LOG correction entry this round, naming `646d29c9` (full hash `646d29c9df4ef77499248f95589cb9526c6dea19`): `<<LOG ENTRY POINTER — the round-51 LOG entry that names the hash>>`. Shown able to fail: the fix counts only when `grep -c 646d29c9 LOG.md` ≥ 1 at the landing revision, and only when the new entry is an append (the prior 308 434 bytes of `LOG.md` stay a byte prefix) |
| M51-2 | `landing` — `SHONEN.md` drifted out of the canonical form: the seed block and the four box texts are canonical, but every box carries **two** indented evidence lines (one is allowed) and **two** trailing prose paragraphs follow the last box ("Round-43 correction: …", "Round 49 (non-author verifier: …)") | routed at `corpus/lessons/round-50-verifier-spotcheck.md:77`. Contract: `PROTOCOL.md:432` (file-contract row for `SHONEN.md`: "the seed block … must diff byte-identical modulo `<name>` … marks are confined to the box character plus **one** indented evidence line per box … no other prose, added boxes, or removed boxes"); the seed itself is `PROTOCOL.md:439-448`. Measured at tip `39f41d4f` (receipts `.ufo/waves/round-51/w1/ScribeLesson/receipts/`): lane `SHONEN.md` sha256 `3ae428cf…` (`shonen_lane_sha.txt`), 20 lines, 8 indented lines over 4 boxes → **4 surplus** (`shonen_box_indent_counts.txt`), and **2 trailing prose paragraphs** after the last box's evidence lines (`shonen_drift_summary.txt`). The seed block itself is NOT the fault: with the mark normalised (`[~]`→`[ ]`) the lane's seed is byte-identical to PROTOCOL's seed (both sha256 `0a6d81c7…`; `shonen_drift_summary.txt`) — so the drift is exactly the surplus marks' lines and the trailing prose, as the closure says | the template clause — `PROTOCOL.md:432` states the mechanical check and it was not applied at the round-50 landing; no lane instrument re-checks the file's canonical form (`tools/round-25/a2/c1-calibration.py:50,83`, `tools/round-44/c2-counter.py:134`, `tools/round-46/gate.py:35` read `SHONEN.md` as a graded file, but none compares its seed block to the template) | regeneration of `SHONEN.md` from the canonical template this round, with the current evidence moved into this round's report and the LOG entry: `<<LANDING POINTER — the regeneration commit>>`. The claims file's routed-defect repair 2 (`plans/round-51-claims.md:236-239`) names the target: the template file `kimi-shokunin/templates/mint/SHONEN.md` verbatim, `<name>` = `kaidoku-shokunin`, the only substitution — sha256 of the substituted bytes `57fb2e04…`. Note the shape of that choice: the template file is the PROTOCOL seed block **plus** a 6-line `<!-- CANONICAL TEMPLATE … -->` header that PROTOCOL's seed block (`PROTOCOL.md:439-448`, 8 lines, sha256 of the substituted bytes `0a6d81c7…`) does not contain; the two differ only by that header (`shonen_seed_vs_template_body.txt`). Both satisfy PROTOCOL's mechanical check on the seed block; the landed file must carry at most one indented line per box and no prose outside the seed block (an HTML comment header is not prose, but say which file was used). Shown able to fail: the fix counts only when the landed file diffs byte-identical against the chosen target modulo `<name>`, carries at most one indented line per box, and has no trailing prose |

<!--
MORE MISTAKES (M51-3, …) to be appended by the L1 as the round lands: the wave-1
pre-freeze attacks (`.ufo/waves/round-51/w1/`) and the w2 falsify wave's findings.
Each row needs: class · evidence pointer · captured-by (the QUALITY row or the
instrument that now catches it) · fix shown able to fail. Rows that cite a
counter/instrument defect must name the mutation that kills it.
-->

## Gate

Sources opened this round (2026-10-30 local; the seats' receipts carry UTC to the second); each located quote is from the served body after tag removal and whitespace collapse (HTML) or an exact line of the fetched text. Receipts: `.ufo/waves/round-51/w1/ScribeSources/`, `<<OTHER SOURCE SEAT RECEIPT DIRS>>`; the L1's own re-fetches land in `.ufo/waves/round-51/l1/srcs/` (copies committed under `corpus/evidence/round-51/c1/index/`).

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| <<S-row>> | <<URL, byte size, sha256>> | <<YYYY-MM-DD, HTTP status>> | <<≤25 words>> | <<admit / reject kept / not registered (honest stop) / re-opened>> |

<!--
Expected rows for this round (per `plans/round-51-claims.md` §"Frontier step"), to be
filled with the located quote and the decision by the SOURCES seat and the L1:
- the unsquashfs / squashfs-tools device-node source row(s) — the primary grounding
  of the device-accounting law (C1's entry cites them plus S243/S244/S245/S249);
- the squashfs-tools `-no-pad` / padding source row (C2's rule block 27 cites it);
- S243/S244/S245/S249 (Freetz patch 101, AVM download index, unblob 26.6.4
  `squashfs.py`, AVM licence) — re-opened this round or carried from round 50's
  attempt-2 gate, with the decision recorded here either way.
No row is registered until its quote is located and its decision is written here.
-->

## Census before -> after

- Round start (`.ufo/waves/round-51/l1/sources-census-start.txt`, committed at `f04b51dd`, blob `aa81d2ac…`): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → **exit 0**, 19 `W04` duplicate-URL lines, final line `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`; **156 rows**.
- Round end: `<<END: exit code, W04 count, row count, receipt path>>` — see the report (`## Sources & frontier`) and `.ufo/waves/round-51/l1/sources-census-end.txt`.

## Honest stop

<<To be written by the L1 if the round stops: what was landed, what was measured, what
was not measured and why, the kill-rule state, and the open L0 items carried. The
round-50 lesson's honest stop (`corpus/lessons/round-50.md` §"Honest stop") is the
shape. If the round completes, this section states that no stop occurred and names
the receipts that carry each verdict.>>
