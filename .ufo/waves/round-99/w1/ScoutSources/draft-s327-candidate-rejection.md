# Draft: further primary source for R99-C2 "invalid overlay size" — REJECTION

Candidate class required by seat item: one further primary source on the truncated-PE
refusal behaviour, from the UPX issue tracker or UPX docs, mentioning
`invalid overlay size`. Searched 2026-11-05.

## Searches run (receipts in this directory)

| query (GitHub issues API, repo:upx/upx) | total_count | outcome |
|---|---|---|
| `"invalid overlay size"` | 0 | no issue names the message (gh-issues.json) |
| `"overlay size"` | 2 | "Datatype of overlay_offset in p_mac.cpp" (macOS packer field type), "v3.95" (release title) — neither touches truncation refusal (gh-issues2.json) |
| `overlay truncated in:title,body type:issue` | 0 | no truncation/overlay issue at all (gh-issues3.json) |

Docs: `doc/upx-doc.txt` at tag v5.2.0, sha256
`4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` — byte-identical to the
copy already registered as S269 and re-opened as S271. Its overlay section (lines 143-164)
documents only `--overlay=copy/strip/skip` semantics and "auxiliary data attached after the
logical end"; the word "invalid" does not occur anywhere in the file (grep -n invalid: no
match). So the docs ground overlay handling, not the corrupt-file refusal, and no new row
would be created for them.

Third-party writeups exist (e.g. 0xdf GitLab "Flare-On 2020: garbage" — manual truncation
repair; hardlyprogramming S325 already registered) but they are outside the required
primary class (issue tracker / docs) and add no authority S324/S326 lack.

## Rejection reason (draft for SOURCES if ever needed)

No UPX issue-tracker or docs source beyond the already-registered S326 (`src/packer.cpp`,
the file that throws the message) states the truncated-PE/`invalid overlay size` behaviour;
a new row would duplicate S326's URL and content. Do not consume an S-id.

## Row shape held for reuse if a genuine issue is later located

`| S3xx | UPX issue NNNN, "<title>" — https://github.com/upx/upx/issues/NNNN (fetched YYYY-MM-DD; N bytes; sha256 `...`; copy `.ufo/waves/round-99/w1/ScoutSources/gh-issue-NNNN.json`) | code | A | <one-claim scope> | <located quote + lines> | <what it grounds, and the not-grounded neighbours> | mined | YYYY-MM-DD | on-release | corpus/knowledge/2026-11-05-r99-pe-upx-truncation-refusal.md |`
