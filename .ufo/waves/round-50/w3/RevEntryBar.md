# RevEntryBar — round 50 attempt 2, wave 3: entry acceptance bar

**Verdict: DONE — the entry acceptance bar is pre-written, exercised against the w3 entry draft, and
shipped with receipts; no REA run, no lane mutation, no installs.** The bar (`RevEntryBar/bar.md`,
sha256 `89d483fd6c2c…4f239`, 19 numbered items across A–F) is the falsify wave's rubric for
`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` at the landing REV. Applied to the current
w3 draft it already catches one real gap (F1 below) and its own commands were calibration-tested
(F2–F4). Seat-id report; inputs read: QUALITY.md rows 1–93, `plans/round-50-claims.md` R50-C1,
`plans/round-50-attempt2-claims.md`, frozen `tools/round-50/c1-counter.py`, `corpus/SOURCES.md`,
sibling drafts `ScribeEntryC1/entry-draft.md`, `ScribeProvinceBinding/check-bindings.py`,
`SrcReopenAvmIndex/MANIFEST.sha256`.

## Findings

| # | finding | evidence (command → exit; sha256; UTC) |
|---|---|---|
| F1 | **The w3 entry draft's `source: S244` line carries no sha256** — bar item 2 fails it as written. The hashes exist: root index `75e886e2…40764`, `fritzbox-7581.body c1dd76d6…48589`, `fritzbox-7582.body 18ccf345…3d70d`, `fritzbox-6490-cable.body 4de20237…2beb7`, `fritzbox-6430-cable.body ab4da28c…eaabf` (w3 `SrcReopenAvmIndex/MANIFEST.sha256`; attempt-1 `w1/C1SrcAvmIndex/receipts/` for the cable dirs). L1/ScribeEntryC1: add the listing sha256s to the S244 line at landing. | `awk '/^source:/{n++; if ($0 !~ /sha256/) print "NO-SHA " NR}' ScribeEntryC1/entry-draft.md` → `NO-SHA 13`, exit 0 — `receipts-validate-final.txt` sha256 `c3100940…c128`, 2026-10-29T20:40Z |
| F2 | **Bar-command calibration, three fixes from the first validation pass** (kept honest, not hidden): (i) pin grep must strip backticks — the draft writes `` `sasquatch` 4.5.1 `` so a literal `grep -c 'sasquatch 4.5.1'` false-negatives (0 hits; fixed command reports 1); (ii) oracle tsvs have no header and no trailing newline — `wc -l`-minus-1 undercounts (4555 vs true 4556; `awk END NR` now reproduces 4556/4564/4709/3955 exactly, matching the plan and the draft's results table); (iii) the unlabelled-prose awk now tracks HTML-comment state and exempts `N. [label]` list items (first pass reported 11 unlabelled, all comment-block/numbered-label artifacts; fixed command reports 0). | `receipts-validate-first-pass.txt` sha256 `310d4d40…7cc88` vs `receipts-validate-final.txt` sha256 `c3100940…c128`, both 2026-10-29T20:38–20:40Z |
| F3 | **The prompt-named entry stem is the corrected-away name; the bar pins the counter's.** The frozen counter pins `ENTRY/STEM = 2026-10-28-r50-avm-le-squashfs-core` (`c1-counter.py:377-378`); the attempt-2 claims file's first draft `2026-10-29-r50-le-avm-hsqs-core` was corrected at `6f4aba63` ("the counter, not this file, is the rule"). Bar item 1 requires the pinned path present AND the wrong stem absent at REV. | `git show HEAD:tools/round-50/c1-counter.py \| sed -n '377,393p'` → constants as cited, exit 0; `git log --oneline f890bbe..HEAD` → one commit, `6f4aba63` — `receipts-bundle.txt` sha256 `f3b25a7c…f595`, 2026-10-29T20:37Z |
| F4 | **Registry linkage cannot go green before the landing commit — expected, scored 2 until then.** At HEAD only S246–S248 exist; S243/S244/S245/S249 land with the entry. The bar's item-5 snippet was run against the draft + HEAD SOURCES: cited {S243,S244,S245,S249}, linked [], exit 1 (red path verified). The frozen counter's own reds (`S-id substring S1120`, opened-window, used-by) are cited in the bar. | python3 snippet in `receipts-validate-final.txt` → `cited ['S243','S244','S245','S249'] linked []`, exit 1 — same receipt, 20:40Z |
| F5 | **Frozen bytes verified unchanged.** `git diff --stat 435d41fd… HEAD` over `tools/round-50/`, `plans/round-50-claims.md`, `tools/round-41/sqfs-list.py`, `tools/round-27/xpin-attribute.mjs` is empty, exit 0; frozen counter sha256 at HEAD `9820811bf29f…9bd813`. Lane HEAD `6f4aba63`; named base `f890bbe` is its parent. | `receipts-bundle.txt` R1/R3/R6, sha256 `f3b25a7c…f595`, 20:37Z |

## Bar shape (what the falsify wave gets)

19 items, each with the one command that checks it and the QUALITY row / predicate clause it
enforces: A. identity/placement (item 1; counter `:377-378`, QUALITY 4). B. provenance-first
(items 2–4; S243/S244/S245/S249 named by the claim's frontier step, QUALITY 1/29/42/18/73).
C. bidirectional registry linkage (item 5; QUALITY 29, counter `:2462-2477` + its selftest reds).
D. content discipline (items 6–10; QUALITY 5/7/8/39/1/6/13, evidence-id call citations).
E. required disclosures (items 11–14; carrier-swap + Still-Frontier, marker-constant, seven
disclosed limits, no universals beyond the four carriers). F. hygiene (items 15–19; no credential
material per M50-4, no placeholders, QUALITY 19/23 timestamps, companion PROVINCE/README bindings
via the counter's own predicates, cited-receipt existence per QUALITY 52). Verdict rule: all met →
0; any violated → 1; L1-produced evidence absent → item scores 2, never clean.

## Notes for the L1

- Apply F1 at landing: give the S244 `source:` line the five listing sha256s (F1 names them).
- Bar items 4, 16 (second half) and 18 depend on L1-produced artifacts (srcs-attempt2 re-opens,
  data run, counter run); until they exist those items are 2 per the verdict rule — that is the
  intended behavior, not a defect.
- The bar deliberately does NOT re-derive carrier pins, oracle, or REA projections — those are the
  frozen counter's clauses and the falsify wave's re-run duties.
- No tools installed (nothing needed); scratch `/fast/scratch/hyaku/kaidoku-r50/w3-RevEntryBar`
  removed after copying receipts. No lane file touched outside `.ufo/waves/round-50/w3/RevEntryBar*`.
