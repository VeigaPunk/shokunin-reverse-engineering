# R29-C1 lookup manifest audit

## Verdict

**`rows_complete=152/152`: holds at `18be864a528873b2b70d8c94e31f880290249e90`.** The recorded C1 counter receipt reports 16/16 valid carrier runs and 152/152 complete rows, with exit 0. The independent manifest audit below found no lookup-manifest exceptions.

## Findings

The Git-archived target revision contains 304 manifest entries and 304 response files, plus `manifest.json`. All 304 response hashes match their manifest SHA-256; all statuses are 200; and all entries record a positive integer `tries` value (304/304 are `1`). URL shapes match: 152 exact 4byte page-0 URLs and 152 exact OpenChain `filter=false` URLs. There are 152 distinct held-out selectors; each has exactly one OpenChain response and at least one 4byte response (all have page 0). The manifest/file sets match in both directions; no duplicate manifest filenames were found.

There are no page-1+ files and no non-null `next` pointers in the saved 4byte responses. Thus there are no pagination links to validate; the p1+ linkage condition is vacuously satisfied, with all page-0 chains terminating. **Exceptions: none** across the audited conditions.

## Evidence

1. **Manifest audit — observation.** Producing command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecManifestC1/audit.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin 18be864a528873b2b70d8c94e31f880290249e90`; UTC `2026-10-22T20:22:27Z`; exit 0 (`audit_exit=0`). The script reads the selected commit with `git archive` (reported `archive_exit: 0`), not the mutable working tree. Exact output excerpt:

   ```text
   "4byte_page0_files": 152,
   "4byte_pagination_files": 0,
   "db_files_excluding_manifest": 304,
   "exceptions": [],
   "exceptions_count": 0,
   "file_manifest_set_equal": true,
   "heldout_rows": 152,
   "heldout_unique_selectors": 152,
   "manifest_entries": 304,
   "non_null_next_pointers": 0,
   "openchain_files": 152,
   "saved_p1plus_link_checks_passed": 0,
   "selectors_with_exactly_one_openchain": 152,
   "selectors_with_one_or_more_4byte_pages": 152,
   "selectors_with_page0": 152,
   "sha256_checked": 304,
   "sha256_matches": 304,
   "status_counts": {"200": 304},
   "tries_counts": {"1": 304},
   audit_exit=0
   ```

2. **Row-completeness verdict — observation from the recorded counter receipt.** Receipt: `.ufo/waves/round-29/after/c1-at-18be864a.txt`, lines 1–5. Producing command recorded there: `python3 -I -B tools/round-29/c1-fresh-naming.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 18be864a528873b2b70d8c94e31f880290249e90`; UTC `2026-10-22T20:16:35Z`; exit 0. Exact output excerpt:

   ```text
   runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1
   exit=0
   ```

   The counter defines row completeness as a valid carrier run plus complete saved lookups (C1 counter source, `tools/round-29/c1-fresh-naming.py:20-26`). The manifest audit independently confirms the listed lookup inventory, response hashes, status, tries, and URL/pagination conditions.

## Risks and blockers

No blockers. Pagination-link validation had zero p1+ pages to exercise; the audit observed zero non-null `next` pointers. This report relies on the recorded counter receipt for `rows_complete` and does not re-run REA or the counter.

Scratch artifact (not in the lane): `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecManifestC1/audit.py` — SHA-256 `0ece4c81865e0273cc19a9799929db2f6005be845054816cd9389cbf6735acc9`. No tools were installed or updated.
