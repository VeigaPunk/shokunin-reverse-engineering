# Round 51 — pre-freeze sources disprove a shared special-inode law; provider-recovery honest stop

Lane kaidoku, attempt 1, L1 KaidokuR51. Round-start branch tip
`1aa273694f4409d3432fbcd73e83a33bee0dd8e9`; declared claims at
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`, wave evidence at
`39f41d4f15a87689a41c16c5c17ed885fbfb7da3`.

## Claims and stop

R51-C1 (coverage): re-freeze the device-accounting law and re-run four pinned LE
AVM members, then promote Frontier to Core. R51-C2 (depth): triage v6 with a
DD-WRT failed-body discriminator/executability audit plus a registry census.
**Neither target was verified. No R51 claim freeze was made and no R51 REA data
run occurred.** The final sources entry is labelled NOT promoted, and PROVINCE's
Frontier remains unchanged. Census-only success is not substituted for C2.

The parent first delivered `WAVE-DONE kaidoku r51 r51-w1: all 36 seats settled`,
results `.ufo/waves/round-51/r51-w1-results.json`. Its subsequent recovery boundary:
“finish current round using already-submitted wave identities only; no additional
waves or provider-replacement seats”; unmet work must be explicitly unverified.
It also restricted continuation to defensive/source/documentary work and barred
routing around denials. No denial was bypassed and no exploit/target testing was
initiated. This boundary supersedes the earlier two-wave plan. The required
64–128-seat round and independent falsify wave are **unmet**, not waived into a
passing admission. There were 36 submitted identities, one build wave, no w2.

Same-identity implementation continuations returned after WAVE-DONE: the census
seat delivered a diagnostic; the fetcher remained incomplete; the triage draft
remained syntactically invalid. The latter two are preserved only as evidence,
not production code. The L1 counter/harness drafts are also wave artifacts, not
frozen or accepted gates. No provider-replacement identities were spawned.

## Gate

Both new registry rows were opened this round by ScribeSources, and the L1
independently opened the canonical tagged URLs. Seat fetch ledgers, source
bodies and located-quote checker are in
`.ufo/waves/round-51/w1/ScribeSources/`; the narrower L1 adoption is the final
registry text, not every proposed inference in the draft.

| row | URL and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S250 | https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c — 2026-10-30 | :1287 `if(root_process)`; :1328 `res = mknod(pathname, S_IFIFO, 0);`; :1349 `res = mknod(pathname, S_IFSOCK, 0);` | admit, tier A code, mined: char/block-device creation has a root gate; FIFO/socket calls do not share it. Does not prove REA gap behavior or operative binary identity. Tag commit 708c59ae80853b0845017c33b42e56061cc546cd; body sha256 6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341 |
| S251 | https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c and companion mksquashfs_help.c — 2026-10-30 | help :467 `-nopad` / `do not pad filesystem to a multiple of 4K`; parser :7113 `strcmp(argv[i], "-nopad")` | admit, tier A code, mined: a writer-side option, not a reader witness or shipped-body provenance. Main source sha256 509241bb1aaa1a4fd144d3c7ddc96e628a9d34033573b04836672352fb4f17e2; help sha256 9136f6e6ac57859cb45df633128f68e615b412dc8b6abfa4da8374373f981ac2 |
| proposed shared special-inode law | same S250 body and the four historical round-50 envelopes | FIFO/socket branches outside `if(root_process)` | **reject** the inference that all special kinds disappear because unprivileged mknod is impossible. Flip: independently demonstrated behavior for each kind on the operative extractor, with branches distinguished. The source stays admitted; the unsupported inference does not. |
| proposed v6 reader premise | `.ufo/waves/round-51/w1/CritTriV6/findings.md` and its receipts | clean extraction is not independent-reader success | **reject** the premise that the clean DD-WRT no-pad envelopes prove their readers succeeded. Flip: an explicit body-to-reader-support mapping with measured unknown handling and before/after controls. |

Rows added: S250/S251, both tier A, both mined directly at first registration;
no existing status/recheck/used-by cell changed (old→new changes: none). They
support `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`, which occupies
the planned filename but explicitly denies promotion. No new rejected-source
row is invented: the rejections above concern candidate inferences, not a
failed source opening. External non-author admit/reject spot-check is **pending**;
this wave remains the lane, not an independent verifier.

Assimilation: **none**. The read-only package scan is
`.ufo/waves/round-51/w1/ScoutMergeThemes/scan.md`: its recommended AVM-LE provenance
theme was not fetched/re-grounded for adoption before the recovery boundary.
No staged row or entry was appended, no campaign tool was run, and no id
renumbering or collision-guard claim is made for this non-adoption.
`considerthese/` was absent at round start; no operator-authored proposal edited.

## Mistakes

| id | class | evidence pointer | captured-by | fix and observed failure |
|---|---|---|---|---|
| M51-1 | landing/misroot | MutGapRule wrote `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` at fleet root; ScribeScorecard's message identified it | absolute-path wave contract, violated | containment, not prevention: copied byte-exact, cmp succeeded, removed fleet copy; sha256 0bde7b78a25ded8beb0bec7c3ec3566bcf64c70332c8811e60de0b3f6afec602. Preserved at lane-relative `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` and wave `w1/misroot/`. First containment used only the wave path; second copy established the protocol's same-relative lane path. No preventive helper is claimed fixed. |
| M51-2 | rule contradiction | ScribeScorecard `probe-device.out`, `probe-full.out`, `probe-mutations.out` | QUALITY 94 class control | required.char-device=true plus empty device allowances scores 0/4; required=false scores 4/4 dispositions. Proposed amendment corrected. Full control instrument/data target unverified, so not a completed claim fix. |
| M51-3 | source scope | ScribeSources F1/F3/F4; S250/S251 tagged sources | QUALITY source-versus-inference rules | rejected shared char/FIFO/socket mknod premise; source and SKILL correction now distinguish branches. Negative evidence is the actual FIFO/socket branch outside the device root gate. Upstream flag corrected to -nopad; no v6 behavior claimed. |
| M51-4 | census scope | ScoutCensusRecheck F1–F3: historical claims census42, registry55, outside13 | none for the scope distinction | new registry-only census diagnostic compares both set directions, parser/refusal and negative cases call actual production functions. Its selftest demonstrates missing/extra/duplicate/malformed inputs fail; census2 remains correct for its narrower rule and frozen meanings.py is not silently migrated. C2 remains unverified. |
| M51-5 | editing/tool schema | L1 duplicate docstring incident; ExecTriV6 resumed malformed CUT writes | exact edit/read discipline | L1 restored pristine counter bytes and used small exact edits; draft selftest 184 cases eventually returned 21 green +163 red, zero failures (artifact 22111). No claim target measured and draft is evidence-only. Invalid triage draft never integrated. Tool issue filed; this is containment, not proof schema mismatch is repaired. |
| M51-6 | dispatch interpolation | gen-w1.py item strings contain unresolved `{LANE}`/`{W1}` markers | none before dispatch | common context supplied absolute roots, but item-local placeholders violate the stronger per-item contract. Taken dispatch remains immutable; the final report records the defect rather than regenerating dispatch evidence. No checker fix is claimed. |
| M51-7 | historical record | round-50 closure routed absent literal 646d29c9 in LOG and noncanonical SHONEN prose | closure | LOG append now names the omitted commit; SHONEN regenerated verbatim modulo name from template. Exact template comparison recorded in L1 receipts. Historical evidence stays in LOG/report, no author [x] promotion. |
| M51-8 | citation-range drift | first bounded landing SKILL note cited :15-69 but the new knowledge file has 68 lines (`wc -l`); structural counter at 96aee1a5 resolved 25/26 blocks | QUALITY 77 and command A | corrected range to :15-68; preserved negative `l1/integrity-at-96aee1a5.json`; the same counter re-measures at the correction landing. Structural citation resolution is not v6/executability verification and gives no C2 target credit. |

## Disposition of the other routed round-50 defects

- C3 freeze drift: no v6 freeze or working v6 gate landed; **unverified**.
- fetch-vendor network-guard selftests: same-identity continuation remained
  incomplete, no deleted-guard proof; **unverified**, original frozen tool unchanged.
- preventive fleet-root control: defective helper draft rejected (RevSweep),
  not production; containment only, operator-side preventive duty remains open.
- credential values in historical pushed round-45 blob: unchanged carried L0
  `kaidoku | round-50`; no credential use or history rewriting attempted.

## Census and bounded verification

Start receipt `.ufo/waves/round-51/l1/sources-census-start.txt`: exit 0,
156 rows, 19 W04 warnings. End receipt is
`.ufo/waves/round-51/l1/sources-census-end.json`; exact outputs and exit codes
are retained. Diagnostic receipts are `l1/census3-{before,selftest,after}.json`.
The registry-only diagnostic is not admission of either claim. Its committed
before/after are read-only comparisons, not external-target tests.

Expansion unchanged: source corrections concern already-named SquashFS ground;
no Frontier→Core or capability. Quality improved only for bounded corrections
and the registry diagnostic. Discernment unchanged: outside spot-check pending.

Generated-mirror cleanup: retained `w1/ScribeSources/mirror-SOURCES.md` after cmp,
removed the seat's generated whole-corpus mirror from the wave (not admissible
evidence under scratch discipline). Original counts and retained counts are in
`l1/artifact-census.json` and `l1/artifact-census-retained.json`. Seat report paths
into the discarded mirror describe that earlier measurement, not retained files.
Full source bodies and fetch/quote/census receipts remain.
