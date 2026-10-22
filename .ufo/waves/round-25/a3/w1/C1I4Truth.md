# R25-C1 item I4 — SCORECARD coverage row: true-mapping verification

Seat: KaidokuR25a3.C1I4Truth, 2026-10-22. Read-only on the lane; every command below ran
with cwd /home/vgpnk/Projects/shokunin/kaidoku-shokunin using only `git show` / `git ls-tree`
(read-only git) plus local python on seat-saved copies. No lane file was written except this
report. No tools were installed or upgraded. Scratch root:
/fast/scratch/hyaku/kaidoku-r25-a3/seats/C1I4Truth/

## What was attacked

The acceptance question: are "107/107" (at C1 commit 0e333eb2fc25f538a99058761f379845f2534c42)
and "108/108" (at C2 commit 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76) true mapping statements —
every knowledge file named in the coverage map and no phantom map tokens (missing and dangling
empty) — or only coincidentally equal numerators and denominators?

## F1 — Instrument extraction fidelity: holds (observation)

- Command: `awk 'NR==92||NR==124{print NR": "$0}' SCORECARD.md` then extract lines 93–123 to
  command-a.sh. Output excerpt: `92: ```bash` / `124: ``` `; sha256 of the extracted block
  `e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247`. Exit 0. 2026-10-22T10:46:21Z.
- Cross-check: the same block re-extracted from `git show <REV>:SCORECARD.md` at both revisions
  hashes identically (`out-c1/command-a-at-rev.sh`, `out-c2/command-a-at-rev.sh`, same sha256).
  The working-tree instrument is byte-identical to both committed revisions; no instrument drift.
- Command A itself only runs `git show` and `git ls-tree` (verified by reading the block); it
  writes nothing, so running it against the lane needed no sandbox clone.

## F2 — Command A at the C1 commit: holds (observation)

- Command: `bash run-i4.sh 0e333eb2fc25f538a99058761f379845f2534c42 c1` (wraps command A with
  REV set). Exit 0. 2026-10-22T10:46:30Z–10:46:31Z.
- Excerpt (out-c1/command-a.json): `{"citation_resolved_rules": 17, "coverage_score": 10.0,
  "dangling": [], "depth_score": 10.0, "knowledge_files": 107, "mapped": 107, "missing": [],
  "revision": "0e333eb2...", "rule_blocks": 17}`.

## F3 — Command A at the C2 commit: holds (observation)

- Command: `bash run-i4.sh 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76 c2`. Exit 0.
  2026-10-22T10:46:30Z–10:46:31Z.
- Excerpt (out-c2/command-a.json): `..."dangling": [], "knowledge_files": 108, "mapped": 108,
  "missing": [], "revision": "08c7a729..."}`.

## F4 — Independent git ls-tree counts: holds (observation)

- Command: `git ls-tree -r --name-only <REV> -- corpus/knowledge` piped to `grep -c '\.md$'`.
  Exit 0 both revisions. 2026-10-22T10:46:30Z.
- Excerpt: `107` at 0e333eb2, `108` at 08c7a729 (out-c1/knowledge-md-count.txt,
  out-c2/knowledge-md-count.txt). The ls-tree listing diff between the revisions is exactly one
  added path: `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` (diff exit 1,
  output `108a109`), i.e. the C2 entry alone moves the denominator 107 → 108.

## F5 — Coverage row text at both revisions: holds (observation)

- Command: `git show <REV>:SCORECARD.md` then `grep -n '^| coverage |'` on the saved copy. Exit 0.
  2026-10-22T10:46:30Z.
- Excerpts (line 23 in both): at 0e333eb2 — "107/107 knowledge files mapped; index integrity
  only, **not** fraction of the REA domain held … recount 107/107, missing [], dangling [] at
  `7ef837a473ae65d924b9ea34e7748f722a6cd7d5` (round 25 attempt 3; the row said 78/78 from
  luna-round-7 until then)". At 08c7a729 — same plus "; 108/108 after the round-25 EVM
  selector-naming entry". The row's claimed numbers match the measured state at its own commit
  in both cases.

## F6 — True mapping, not matching numbers: holds (observation + inference)

Instrument-internal gap attacked: command A's `mapped` set is any `2026-10-DD-name` token
anywhere in the `## Coverage map` section, so a file named in prose (not a table row) would
still count, and a stray token in prose would create dangling. Auxiliary check
`check-map-rows.py` (exit 0, 2026-10-22T10:46:43Z) splits section tokens from actual `|`-table
rows:

- C1 (out-c1/check.json): `"knowledge_files": 107, "stems_named_in_table_rows": 107,
  "stems_not_named_in_any_row": [], "distinct_row_tokens": 107, "row_tokens_without_file": [],
  "distinct_section_tokens": 107, "section_tokens_without_file": [], "section_table_rows": 61`.
- C2 (out-c2/check.json): same shape with 108, 62 rows.
- Inference: at both revisions the mapping is a genuine bijection — every knowledge file stem is
  named inside a real coverage-map table row, and no row or section token references a
  nonexistent file. 107/107 and 108/108 are true mapping statements, not numeric coincidence.
- Caveat (inference): "mapped" means "named at least once in a table row"; 108 files across 62
  rows means rows are multi-file and the instrument does not require a dedicated row per file.
  Also, the token regex `2026-10-\d{2}-[a-z0-9-]+` cannot match a non-dated or uppercase stem;
  today `non_dated_knowledge_files` is `[]` at both revisions, so numerator and denominator
  coincide. A differently named future file would silently fall out of `mapped` while still
  counting in `knowledge_files` — that would surface as a nonempty `missing`, so the instrument
  would not silently overclaim.

## Acceptance answer

Both statements are true mapping statements (observation): at 0e333eb2 command A reports
mapped=107, knowledge_files=107, missing=[], dangling=[] with all 107 stems named in map table
rows; at 08c7a729 mapped=108, knowledge_files=108, missing=[], dangling=[] with all 108 stems
named in rows. Independent ls-tree counts agree (107, 108), the delta is exactly the C2 entry,
and the coverage row text at each commit matches the measured state. Verdict: holds.

## Residual risk and verification gaps

- The instrument proves index integrity of the map, not that each map row's annotation is
  accurate about the file's content; that is out of I4 scope and untested here (unknown).
- I did not re-verify the row's third-party anchors (`3395b6d` measurement, the 7ef837a
  recount) — only the two revisions the item names (untested here, not failed).
- All commands above were executed by this seat; no check in this report is inherited.

## Artifacts (scratch root as above; sha256)

- command-a.sh (extracted SCORECARD command A, lines 93–123) e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247
- run-i4.sh (runner) 7c3afa128c141107be7625aaa2d04a844725b66ca7d6ac861966b2dc363d477a
- check-map-rows.py (row-level mapping checker) 3e4dd539749cbbeb0534fccdc9c76599f11be29d07cdd8f67e7e601d35759415
- out-c1/command-a.json 9b354f61a1a35770d52d5845231c8e1e8b759b61ce981008082ed495e65e9083
- out-c1/ls-tree-knowledge.txt 3556180e6efd65927836dd1fae3fa647826a0b18f06ec41605dee2a87579d843
- out-c1/coverage-row.txt 33a85be00d7f84f626e26a5826f64e97dcc1a0577681f940686bfa0e5a4b2746
- out-c1/check.json ae8e5e7e17a9f0460278d371db926d71ebebbd1fee45319355904f11ea41998d
- out-c1/command-a-at-rev.sh e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247
- out-c2/command-a.json a856cf6f8fa67cf6cf40ae89c87c3c4e57855b35dc1d3ed74ac82b0446438a5a
- out-c2/ls-tree-knowledge.txt 6da520a897700b7890a8c2ce83ce9e7851e391436504d28d9ab1c56f26d2007a
- out-c2/coverage-row.txt 33ddc3e67b98b90ca6b81323d13133fb8553d350206d30508f48b15f2650cad8
- out-c2/check.json cea323c9fa1c05bb01c3dc8a0e60c0151133c2ae05a3a35aec13256e822378d3
- out-c2/command-a-at-rev.sh e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247
