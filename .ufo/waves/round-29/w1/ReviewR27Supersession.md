# Review: round-27 `instrument_supersessions` append and its ledger note

- Seat: `KaidokuR29.ReviewR27Supersession` (Kaidoku round 29, wave 1; leaf — no subagents)
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`, tip `18be864a528873b2b70d8c94e31f880290249e90`
- Scope: the append to `.ufo/waves/round-27/claims.json` between base and tip, checked against the round-24 gate's supersession rule (path, commit, reason), immutability statements in the round-27/round-25 claims files, and the `corpus/claim-freezes.tsv` round-27 note.
- Method note: this harness exposes no `lsp` device (inventory: `ast_edit`, `debug` only) and no LSP server answers JSON/TSV; all checks are git-content checks over committed bytes (read-only git: show/diff/log/ls-tree/merge-base/rev-parse, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`). Text grep was used only to locate rule text; every conclusion below cites committed bytes or executed commands. REA: none. Network: none. Tool installs: none. Pacman: not used.
- Times are UTC as produced by `date -u +%FT%TZ` inline with each command.

## VERDICT

**Holds — the append is a legitimate disclosure, not a rewrite of a frozen file.**
Base→tip the file gains exactly 3 inserted lines (0 deletions) forming one new EOF member `instrument_supersessions` with a single conforming entry; every prior byte is preserved, every field of the entry verifies against committed state, and the round-24 gate run at tip confirms the disclosed revision is absorbed (no finding for the disclosed instrument) while the row stays FLAGGED for unrelated, still-disclosed findings.

## Findings by severity

No High or Medium findings. Three informational items:

- **Info-1 (timing stamp anomaly, cause unknown).** The two receipts cited in the reason carry `utc=2026-10-22T20:03:39Z` (red) and `utc=...T20:03:51Z` (green), while the disclosing commit `7431096` (which contains both receipt files) has committer timestamp `2026-10-22T17:03:06-03:00` = `20:03:06Z` — i.e. stamps 33 s / 45 s after the commit time. Cause unknown (jj rewrite/snapshot ordering or clock handling; [unknown]). Immaterial to legitimacy: both receipt files are verifiably in the commit and at tip (`git show tip:<path>`), red precedes green, and their content matches the reason's quoted counts.
- **Info-2 (member-name variance vs precedent).** The appended entry uses `sha256_after` where round-24's own precedent entry used `sha256`. The governing rule requires only `path`, `commit`, `reason` (QUALITY row 33; gate docstring `.ufo/waves/round-24/tools/freeze-gate.py:22-24`; gate code keys disclosure on `(path, commit)` with nonempty `reason`, `:89-91`), and the gate ignores extra members. Not a defect; recorded as schema drift between the two precedent entries.
- **Info-3 (trust limits inherited from the rule).** The round-24 gate's own limits line (`:33-35`): commit timestamps and authorship are not authenticated; the ledger is author-written and checked for agreement, not completeness. Legitimacy here therefore rests on content agreement, which this review established independently (checks 4–8 below); it is not cryptographic proof of who/when.

## Evidence log

Every check: producing command, excerpt, exit code, UTC time, and label.

**1. The change is a pure 3-line insertion at EOF.**
`git diff bacbe9cc 18be864 -- .ufo/waves/round-27/claims.json` → `1 file changed, 3 insertions(+), 0 deletions(-)`; single hunk `@@ -58,5 +58,8 @@` adding `  ],`, `  "instrument_supersessions": [`, and the entry line between the last `not_claimed` element and its former closing `]` (which now closes the new array). `git show <rev>:... | wc -l`: base 62 lines, tip 65 lines. Exit 0. 2026-10-22T20:26:17Z. **Observation.**

**2. Valid JSON, no duplicate keys, single new top-level member.**
`python3 -c` json.load with `object_pairs_hook` dup detection over saved base/tip bytes: base top-keys `[attempt, base, claims, freeze_kind, frozen_by, instruments, not_claimed, pre_freeze_probe, round]` (no `instrument_supersessions`), tip = same 9 + `instrument_supersessions`; `dup-keys: []` in both. Exit 0. 2026-10-22T20:31:05Z. **Observation.**

**3. The appended object, verbatim.**
`{"path": "tools/round-27/c2-xpin-check.py", "commit": "7431096bb16e7dd3c37e08f7307952e231b94cf8", "sha256_after": "1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783", "reason": "INSTRUMENT_REVISED in round 29 (routed defect 2 of corpus/lessons/round-27-verifier-spotcheck.md and defect 2 of round-28-verifier-spotcheck.md): selftest-only revision. ... Receipts: .ufo/waves/round-29/before/r27-c2-xpin-selftest-unpatched.txt (cases=6 failures=1, exit 1) and .ufo/waves/round-29/after/r27-c2-xpin-selftest-patched.txt (cases=6 failures=0, exit 0). The round-27 C2 measurement is not re-run or re-scored."}` (full string in scratch `r27-claims-at-tip.json:63`). Exit 0. 2026-10-22T20:31:05Z. **Observation.**

**4. The disclosed commit is real, uniquely identifying, and correctly placed in history.**
`git log -n1 7431096…` → `7431096bb16e7dd3c37e08f7307952e231b94cf8 2026-10-22T17:03:06-03:00 round-29: hygiene - r27 C2 selftest patch applied (selftest-only, 1c8259a8, red->green receipts)...`, parent `dbd87cfa09eb89306c4e07d3171a4556eb732024` (the round-29 freeze). `git merge-base --is-ancestor`: 7431096→tip exit 0; 7431096→base exit 1 (revision postdates the round-29 base); a4f674b3 (r27 freeze)→base exit 0. `git log a4f674b3..18be864 -- tools/round-27/c2-xpin-check.py` lists exactly one commit, `7431096…` — the `commit` field names the only post-freeze revision, so no undisclosed later revision exists. Exit 0 throughout. 2026-10-22T20:26:17Z. **Observation.**

**5. Hash chain is exact.**
`git show <rev>:tools/round-27/c2-xpin-check.py | sha256sum`: base `d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3` (== the `instruments` pin frozen at a4f674b3), 7431096 `1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783`, tip `1c8259a8…` — equal to the entry's `sha256_after`; the file did not change after the disclosed commit. Exit 0. 2026-10-22T20:26:17Z. **Observation.**

**6. "Selftest-only" is true.**
`difflib.SequenceMatcher` opcodes between the base and 7431096 bytes: all non-equal ranges fall in old lines 301–323, strictly inside `def selftest():` (old line 298) and before the next top-level `def _rows_fixture` (old line 338); the patch touches nothing outside `selftest()`. Cross-check: `git diff bacbe9cc 7431096 -- <path>` shows one hunk `@@ -298,29 +298,39 @@` whose every ± line is inside the function. Exit 0. 2026-10-22T20:31:05Z. **Observation.** (So the frozen measurement logic — `measure()` and counters — is untouched, consistent with the ledger note "the round-27 C2 measurement is not re-scored".)

**7. The reason's citations and receipts are accurate.**
- `corpus/lessons/round-27-verifier-spotcheck.md:152-153`, routed defect 2: "**Red C2 selftest.** `tools/round-27/c2-xpin-check.py --selftest` exits 1 from `97358f75` on (`correct-stub`). Re-anchor the fixture in a new commit and commit the green receipt. Do not count it as a claim." (grep, exit 0, 2026-10-22T20:29:53Z) — the patch is precisely the ordered remedy.
- `corpus/lessons/round-28-verifier-spotcheck.md:87`, defect 2: "Round-27 routed defect 2 is still open: the r27 selftest stays `FAIL correct-stub`, exit 1. ... apply and re-run it, with a receipt." **Observation.**
- Red receipt at tip: `FAIL correct-stub: exit 0, expects ... rev=dbd87cfa…`, `selftest cases=6 failures=1`, `exit=1`. Green receipt at tip: `PASS correct-stub at 97358f75 …`, `PASS correct-stub at cd32264f …`, `selftest cases=6 failures=0`, `exit=0` — matching the reason's quoted counts and the "anchored at fixed revisions (97358f75, cd32264f)" wording. `git show 18be864:<receipt>` exit 0. 2026-10-22T20:28:40Z. **Observation.**

**8. Conformance to the round-24 gate's supersession rule, by text and by execution.**
- QUALITY row 33 (`corpus/QUALITY.md:43`): "A later instrument change is allowed only as an appended `instrument_supersessions` entry (path, commit, reason) with a re-taken before record; an undisclosed post-freeze change ... is a finding, never a clean freeze." The entry carries path+commit+reason (extra `sha256_after`), and the re-taken records exist (red before/green after receipts beside the original state). **Observation.**
- Gate rule text (`.ufo/waves/round-24/tools/freeze-gate.py:17,22-24`): `INSTRUMENT_REVISED` fires when "commits in freeze..MEASURED changed it and the claims file at MEASURED does not list each of them under instrument_supersessions"; "a later revision is disclosed with `"instrument_supersessions": [{"path", "commit", "reason"}]` appended to the same file." Code `:89-91` keys disclosure on `(path, commit)` + nonempty `reason` — all three present. My saved copy of the gate hashes `8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329` — the exact sha256 pinned in round-24's own supersession entry, so the cited rule source is the pinned revision. **Observation.**
- Executed read-only at tip (`python3 r24-freeze-gate.py --root <lane> --rev 18be864…`, exit 0, 2026-10-22T20:32:03Z): round-27 findings are `INSTRUMENT_UNPINNED` (tools/round-26/recompute-ids.py), `INSTRUMENT_ABSENT` + `INSTRUMENT_REVISED disclosed:0` for tools/round-27/xpin-attribute.mjs (the R27-C2 product, a different instrument), and **no finding at all for `tools/round-27/c2-xpin-check.py`** — the appended (path, commit) with reason absorbed its revision. The row remains FLAGGED with the same finding codes the ledger row records; the disclosure whitens nothing. **Observation.**

**9. Precedent.**
Round-24 itself disclosed its freeze-gate revision the same way: `.ufo/waves/round-24/claims.json` `instrument_supersessions` entry for commit `9fb4eacd23eb69ee9d659dd041e006e9ccd61480` with path/commit/sha256/reason (extracted exit 0, 2026-10-22T20:26:17Z); `corpus/lessons/round-24.md:45-50` calls this "exactly the deviation path QUALITY33 allows; it is not silent." The round-27 append follows the established channel, in the file that pinned the instrument, with strictly more verification detail. **Observation.**

**10. No immutability statement is violated.**
- Round-27 claims file: contains **no** immutability clause at all — top-keys at base are the 9 listed in check 2; `frozen_by`/`freeze_kind` describe instruments-first pinning, no bar on later disclosed appends. **Observation.**
- Round-25 claims file has `postfreeze_claim_immutability`: "After actual F these claims remain immutable. Do not append instrument_supersessions to launder **the subject's** post-freeze absence/unpinned/revision debt; the only permitted future disclosure is the separately authorized truthful R25 FLAGGED ledger append..." — scoped to R25's own claims and R25's subject (`tools/round-25/instrument-custody.py`). Its `original_results_immutable.old_files` ("All original claims ... remain byte/mode identical") scopes to the pre-R25 records backing the 11 ledger rows. The round-27 claims file was created in round 27 (first commit a4f674b3), i.e. after and outside both scopes; the R25 clause itself presupposes `instrument_supersessions` as the legitimate disclosure channel and prohibits only its use to launder. **Inference** (textual scoping), backed by the observation that the append touches neither R25's claims file nor its subject nor any pre-R25 record.
- Positive corroboration: `git log` for the claims file has exactly two commits ever — a4f674b3 (create) and 18be864 (this append); nothing else was ever modified in it. **Observation.**

**11. The ledger note is committed, accurate in every assertion.**
- `corpus/claim-freezes.tsv:15` (v1) and `corpus/claim-freezes-v2.tsv:17` (v2), round-27 rows, identical note text; both files are 17/20 lines at tip and `git diff --stat 18be864 -- corpus/claim-freezes.tsv corpus/claim-freezes-v2.tsv .ufo/waves/round-27/claims.json tools/round-27/c2-xpin-check.py` is empty (working tree = tip; exit 0, 2026-10-22T20:32:03Z). **Observation.**
- Note asserts: "revised d8de667f -> 1c8259a8 in 7431096b" (checks 4–5 ✓), "selftest() only (every other line byte-identical)" (check 6 ✓), "disclosed under instrument_supersessions in .ufo/waves/round-27/claims.json" (checks 1–3 ✓), "selftest red -> green receipts ..." (check 7 ✓), "the round-27 C2 measurement is not re-scored" (claims targets/content unchanged apart from the append; check 1 + gate run ✓). **Observation.**

## Residual risk and verification gaps

- Receipt `utc` stamps postdate the commit timestamp by 33–45 s (Info-1); cause unknown, not resolvable from git metadata alone. No effect on any conclusion here.
- Commit timestamps/authorship unauthenticated (the gate's own stated limit) — this review verified content agreement, not operator identity.
- I did not re-run the patched selftest myself; I verified the committed receipts' contents against the reason's claims and the byte-level patch. A live re-run would only re-derive the same committed state.
- The gate run audits rounds 14–29 at tip; I inspected only the round-27 element in detail (other rounds' FLAGGED statuses match the committed ledger and are outside this item).
- `.ufo/waves/round-29/w1/` does not exist at tip (this report is new in the working tree, to be integrated by the L1).

## Artifacts (scratch: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewR27Supersession/`)

| file | sha256 |
|---|---|
| `r27-claims-at-base.json` | `ff45e9ce64b417f11bea12884feb26499d30ce30766bec674f9f0d03a37662b2` |
| `r27-claims-at-tip.json` | `f65f86244001a791ef82a22e3606bddf37d6df8ba59663330ce860a24113b2fd` |
| `r27-claims-base-to-tip.diff` | `05fe4d9cf4b8a84f66bf06bf8eefb683ea084d855cfb8f8e836c0ae80d43cd3d` |
| `c2-selftest-patch.diff` | `bd080c44c28a8e5a45b31b94341ebe51e0d4faa1fdae45f369a1406d2931b3a0` |
| `c2-at-base.py` | `d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3` |
| `c2-at-7431096.py` | `1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783` |
| `r24-freeze-gate.py` | `8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329` |
| `claim-freezes-at-tip.tsv` | (unhashed extract; bytes = tip `corpus/claim-freezes.tsv`) |
| `claim-freezes-v2-at-tip.tsv` | (unhashed extract; bytes = tip `corpus/claim-freezes-v2.tsv`) |

Scratch hashes computed 2026-10-22T20:31:05Z via `sha256sum` (exit 0). The two instrument copies hash identically to their `git show` sources, binding the scratch evidence to the committed blobs.
