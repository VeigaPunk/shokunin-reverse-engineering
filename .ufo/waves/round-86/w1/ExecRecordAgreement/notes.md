# ExecRecordAgreement — notes on the R86-C1 counter candidate

Candidate: `candidate/tools/round-86/record-agreement.py` (sha256 `a8c5a3db6f05fab2980b24a4751288cdd281ada1777fb2e70d76e52bc572f317`).
Production `tools/round-86/record-agreement.py` (sha256 `99cb8f27…`, the pinned instrument) is untouched; no commit, no edit outside this seat dir.
Full unified diff: `candidate-vs-production.diff` (same directory).

## Frozen parts kept

- The three atom ids, their atom sentences (module docstring bullets), the target (3 atoms, `mismatches` empty), the kill rules and the `--control substring-only` function body. The control function is byte-identical to production (AST segment compared: `control_substring_only IDENTICAL 648`).
- Counting command shape `--root . --rev <40-hex> --json-out <receipt>` is unchanged; `--rev` is now validated.

## Changed hunks (candidate line numbers) and why

| Lines | Change | Why |
|---|---|---|
| 1–58 | Module docstring: added the object-locating paragraph, the reading rule (`--rev` = committed blob; `--worktree` = fixture only, refused with `--rev`), exit 2 for unusable revision/mode, and a residual-limit sentence. Atom bullets verbatim. | Make the reading mode explicit; production docstring promised exit 2 for an unreadable revision but returned exit 1. |
| 60–65 | `CONTROL_NAME`, `SCHEMA` named constants (values unchanged). | Single source for the control name that `choices=` and the driver share. |
| 68 | `SUPERSEDE_RE = supersedes S303(?!\d)` (was `startswith`). | `supersedes S3031 —` used to satisfy the prefix; now it does not open the S303 supersession. |
| 69 | `COUNT_CLAUSE_RE` uses `\b` after the digits, `re.S`. | `count 3x` no longer reads as 3. |
| 70 | `ROW_RE = ^ {0,3}\|\s*S\d{3,}\s*\|` — the original row shape, now used file-wide. | Frozen "rows of corpus/SOURCES.md"; see 150–200. |
| 71–76 | `ID_IN_TEXT_RE`, `RECEIPT_RE` (round is a regex group, not re-split from the path), `REV_RE`, `PIPE_OPEN_RE`, `FENCE_OPEN_RE`, `FENCE_CLOSE_RE`. | The first draft split the receipt path on `/` and read the round from the wrong field; fixed before any receipt was saved. |
| 86–100 | `git_blob`: `git cat-file -t REV:path` must be `blob`, then `git cat-file blob`; strict UTF-8. Replaces `git show`. | `git show` prints a tree listing (exit 0) for a directory and applies textconv; S255 requires the committed object's bytes. |
| 102–105 | `rev_reader`. | Wraps `git_blob`. |
| 108–117 | `worktree_reader`: explicit UTF-8; `OSError` (incl. IsADirectory) and decode errors → `Unreadable`. | Directory-named receipt must be unreadable, not a crash. |
| 129–143 | `fenced_flags`. | Rows inside fenced code must not count. |
| 145–147 | `is_delimiter`. | Header/delimiter recognition for the registry header. |
| 150–200 | `registry_rows` replaces `registry_table`. Rows are file-wide `ROW_RE` lines outside fences that directly follow a blank line, the header, or another row; a row-shaped line glued to prose goes to `ignored`; exactly one `| id |` header with `source`+`teaches`; each counted row must have the header's cell count. | First draft took only the first contiguous block: at BASE it stopped at the blank line in SOURCES line 166 and silently dropped S170–S303 (url_rows became 7). The file-wide rule restores the 209 rows and `url_rows` equal to the pre-receipt's 8. |
| 203–217 | `owned_axes_coverage_rows`: the `| coverage |` row must be under `## Owned axes`. | Production required exactly one `| coverage |` line in the whole file and found 23 (history sections). See flag F2. |
| 219–249 | `atom_supersede_count`: column indices from the header (`source`, `teaches`); exactly one `count` word; `len(listed)==declared`; no duplicate ids; `ignored_row_shaped_lines` in the detail. Atom rule unchanged. | Duplicate ids and an over-long list with a correct set could pass production; a second `count` could be read as the first. |
| 251–293 | `atom_docstring_status`: branch found by `ast` (`not case_present` If, exactly one; exactly one assigned status string); docstring by `ast.get_docstring`; sentence match case-insensitive; stem and other-status match on word boundaries. | Production took the first triple-quoted string in the file and the first `if not case_present` regex match; both can be the wrong object. Atom rule unchanged (name the assigned status; no other status word in the one absent-case sentence). |
| 295–335 | `atom_receipt_pointer`: receipts named by the Owned-axes row; covering = all receipts at the newest named round, each must be a blob at rev with a JSON-object `rev` of 40 hex; `receipt_round < claim_round` still refuses. | Ties at the newest round were resolved by `max` order (first one only). A non-object JSON receipt now gives a clear reason. |
| 337–345 | `ATOMS` unchanged. | — |
| 347–365 | `control_substring_only` unchanged (identical). | Frozen control. |
| 367–421 | `digest`, `run_atoms` (extracted, same semantics), `instrument_record`, `evaluate`/`run_control` take `mode` and emit `"mode"` in the receipt. | Receipts must say whether they are a measurement (`rev`) or a fixture (`worktree-fixture`). Schema string unchanged. |
| 423–484 | Selftest fixtures (`SOURCES_HEAD`, `srow`, `sources_doc`, `CODE_OK`, `CODE_ELIF`, `CARD_OK`, `GENUINE`, receipt constants). | New case fixtures; `GENUINE` is the agreeing world. |
| 486–506 | `_write_tree`, `_git`, `_commit_tree` (fixture git repos only, created under the selftest tempdir). | Rev-mode cases need committed fixtures. |
| 508–612 | `_atom_cases` (worktree-mode atom cases), `_rev_cases` (committed vs worktree bytes). | Each named case binds an atom (see table). |
| 614–623 | `_cli` runs the candidate in a subprocess with `-I -B`. | Exit-code refusals are part of the contract. |
| 625–646 | `_eval_atoms`, `_check`: defective-record cases must also be accepted by the control on the same reading. | Keeps the control a false green (a control refusing a defective record fails the case). |
| 648–717 | `selftest` prints one `CASE` line per case, the `SELFTEST cases=N failures=M` summary, and `--selftest-json`. The count is the real number of cases; production printed `len(cases)+1`. | Honest count; per-case atom binding recorded in `selftest.json`. |
| 719–end | `main`: `--selftest-json`; `--worktree` with `--rev` → exit 2 (`REFUSED`); `--rev` must be 40-hex and resolve to a commit → else exit 2; `--worktree` must be a directory; no mode → exit 2; unknown `--control` → exit 2 (argparse `choices`). Receipt `mode` recorded. | Explicit reading mode, no silent preference. |

## Behaviour changes versus production (for the L1)

1. **A3 locates the Owned-axes row, not the only `| coverage |` line.** Production stopped at BASE with `expected exactly one | coverage | row, found 23`; the reason was the history sections, not the claim. Candidate reads the row under `## Owned axes`. The atom's meaning is unchanged. **Decision for the L1** (flag F2).
2. **A1 no longer accepts `supersedes S3031`** as the S303 supersession (anchored `(?!\d)`).
3. **A1 rejects a count clause with a repeated `count` word, duplicate ids, or a list longer than the count.**
4. **A1 rejects a row-shaped line glued to prose** (recorded in `ignored`); a row after a blank line still counts.
5. **`--rev` that does not resolve, or is not 40-hex, is exit 2** (production: exit 1 with mismatches).
6. **`--worktree` with `--rev` is exit 2** (production silently used `--worktree`).
7. Receipts carry `mode`. Selftest count is the real count.

## Selftest cases and the atom each binds (48 cases, failures 0)

Also in `selftest.json` (`cases[]` with `name`, `atom`, `expect`, `got`, `ok`).

- `all`: genuine-agreement; rev-reads-committed-bytes-not-worktree-edits
- A1-s303-supersede-count (17): a1-wrong-count; a1-id-missing-and-foreign (one id missing, one foreign); a1-id-list-longer-than-count; a1-superseding-row-states-no-count; a1-row-in-prose-paragraph; a1-row-indent-3-spaces-accepted; a1-row-indent-4-spaces-refused; a1-blank-lines-between-rows-accepted; a1-url-row-after-blank-line-is-counted; a1-row-glued-after-prose-line-refused; a1-row-inside-fenced-code; a1-teaches-supersedes-other-id; a1-count-clause-repeated; a1-malformed-extra-pipe; a1-newest-superseding-row-wrong; a1-older-superseding-row-wrong-newest-right; rev-refuses-committed-defect-despite-clean-worktree
- A2-docstring-status (7): a2-absent-case-says-inconclusive; a2-two-absent-case-sentences; a2-status-only-in-other-sentence; a2-other-sentence-status-does-not-refuse (status word in another sentence, must NOT refuse); a2-conflicting-word-in-absent-sentence; a2-second-not-case-present-branch; a2-elif-branch-form-accepted
- A3-receipt-pointer (13): a3-stale-receipt-round; a3-no-receipt-named; a3-receipt-absent-at-rev; a3-receipt-rev-39-hex; a3-receipt-rev-6-hex; a3-receipt-json-list-not-object; a3-receipt-not-json; a3-two-receipts-only-older-exists; a3-two-receipts-both-exist; a3-history-row-does-not-count; a3-no-owned-axes-section; a3-two-owned-axes-coverage-rows; a3-receipt-path-is-directory
- cli (9): cli-worktree-with-rev-refused (2); cli-unknown-control-refused (2); cli-rev-not-full-sha-refused (2); cli-rev-unknown-refused (2); cli-no-mode-refused (2); cli-rev-genuine-exits-0; cli-worktree-fixture-genuine-exits-0; cli-rev-defect-exits-1; cli-control-accepts-defect-exits-0

Every atom-bound case was also checked for the failure reason (each refused case printed its `why`/detail; spot-checked: prose, fence, 4-space, count, id list, duplicate, rev 39-hex, JSON list, older-only receipt, directory receipt, S303 in other sentence).

## Lane runs (candidate, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`)

- `base.json`: `--rev 2cf0b7ff93c698809bed321f7338276a22d6beb9` → exit 1, `mismatches` = A1, A2, A3; `agreed 0/3`.
  - A1: `no row whose teaches opens supersedes S303`; `url_rows` = S079, S080, S083, S090, S092, S119, S123, S303 (8, matches the pre-receipt).
  - A2: sentence `an absent declared case is inconclusive, never a pass).`, code status `survived`.
  - A3: claim round 85; named receipts r67, r68, r75, r76, r84; newest r84 < 85 → `predates`.
- `control.json`: `--control substring-only` → `mismatches` `[]`, `ok true` (accepts the defective records, as required).
- Refusals: `--worktree` with `--rev` → exit 2; `--control file-exists` → exit 2.

## Flags for the L1 (decisions and facts I did not change)

- **F1 — pinned instrument.** `.ufo/waves/round-86/claims.json` pins `tools/round-86/record-agreement.py` at sha `99cb8f…`. Integrating this candidate changes that sha to `a8c5a3…`; that needs a recorded instrument supersession by the L1. I did not touch `claims.json`. The `pre/` receipts were produced by `99cb8f…`.
- **F2 — A3 row selection (decision).** The frozen text says "the `| coverage |` row"; the production counter required exactly one such line in the whole file and found 23. The candidate picks the Owned-axes row. This changes how A3 locates its object (not what it checks). If the L1 does not accept this, A3 cannot be reached without rewriting history sections.
- **F3 — the plan's BASE description of A3 is inaccurate.** The row names five receipts (r67, r68, r75, r76, r84), not only r67; the newest is r84, which predates the row's round 85. Still a mismatch, now for the "predates" reason.
- **F4 — no round-85 receipt exists** under `.ufo/waves/round-85/l1/scores/` at BASE (checked with `git ls-tree`). A3 can only pass once a receipt with a blob `rev` is committed at the measured revision; that is record work, not counter work.
- **F5 — A1 count for the repair is 7, not 3.** At BASE the other URL rows are S079, S080, S083, S090, S092, S119, S123 (7; S303 excluded). A supersession row must say `count 7` and list exactly those seven ids.
- **F6 — grammar trap for the repair writer.** Every S-id after the count clause is treated as part of the declared list. A row like `supersedes S303 … count 7 (…) the older S303 row is preserved` fails because `S303` is a foreign id. Put any mention of S303 before the count.
- **F7 — residuals (declared, not closed).** A non-covering receipt named by the A3 row need not exist; A2 is a sentence check, not a semantics proof; A1 checks one sentence shape.

## Reachability check (fixture, not a measurement)

On a fixture copy built from the BASE bytes, with a corrected supersession row (`count 7`, the seven ids), the docstring sentence set to `survived`, and a round-85 receipt, the candidate reaches `agreed 3/3`, exit 0. Receipt: `receipts/repair-fixture-simulation.json` (mode `worktree-fixture`). It proves the target is reachable with the frozen rules; it does not repair the lane.

## Tools

No tool installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r86/ExecRecordAgreement` removed on exit of each command (trap).
