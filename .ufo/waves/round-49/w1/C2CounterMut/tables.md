## Forgeries (56) — ORIG counter, no battery unless noted

| id | forgery (right strings, wrong facts, or control) | designed | ORIG exit | ORIG red atoms / reason | ORIG --battery exit (failing) | ORIG stdout sha256 (first 16) | accepted |
|---|---|---|---|---|---|---|---|
| F01 | A3 pointer for 33f65a91 dropped (incomplete pointer set) | accept | 0 |  | 0 (none) | 55eecd70a4a533ec | YES |
| F02 | A2 dead hash replaced by an invented non-commit (no report check) | accept | 0 |  | 0 (none) | 13d9e42cc3061ead | YES |
| F03 | A4 empty placeholder report.md written for C1Meaning; lesson re-stated | accept | 0 |  | 0 (none) | c3d46bddc15babef | YES |
| F04 | A6 snapshot fabricated (extra paragraph) and sha256 pin re-written to match | accept | 0 |  | 0 (none) | 575eee4839d2dca8 | YES |
| F05 | A7 teaches inverted fact: "EX_USAGE is 2, not 64" (keeps both tokens) | accept | 0 |  | 1 (mutation set incomplete: 10 of 11) | 63d10c7c1398258f | YES |
| F06 | A8 round-49 identified count inflated 2 -> 200 (identified unverified) | accept | 0 |  | 0 (none) | 77a277a82999f51c | YES |
| F07 | A9 SCORECARD line carries a contradicting suffix (substring match) | accept | 0 |  | 0 (none) | e1a6360ecd7563d1 | YES |
| F08 | historical SCORECARD Round-48 declared freeze rewritten; A1 re-stated to match | accept | 0 |  | 0 (none) | fe0104fc69b91742 | YES |
| F09 | round-48 C1 receipt bytes rewritten; A5 digests re-derived and re-stated | accept | 0 |  | 0 (none) | 7d714d7fb8329b63 | YES |
| F10 | A3 unnamed list drops 8847042a (incomplete unnamed set) | accept | 0 |  | 0 (none) | 67095ad87a015cf8 | YES |
| F11 | A6 S147 sha256 pin zeroed | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | d4bd70f4341db727 | no |
| F12 | A6 S147 quotation marks removed (no quoted passage) | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | a7fddf2a516f587e | no |
| F13 | A7 S148 quote altered (improperly) | reject | 1 | A7 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A7'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A7'] noop []; A3 one point | ab3dba5ba4b55f43 | no |
| F14 | A7 snapshot EX_USAGE value edited to 2 with pin re-written (teaches keeps 64) | reject | 1 | A7 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A7'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A7'] noop []; A3 one point | d1e608a4b72d38bb | no |
| F15 | A7 S148 source URL is the non-3head page | reject | 1 | A7 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A7'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A7'] noop []; A3 one point | 5587724ea59942db | no |
| F16 | A8 second round-49 entry with wrong numbers appended after the correct one | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 2ec1275d7e0b06bb | no |
| F17 | A8 round-49 identified 1 < screened 2 | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 19ea35bb17173786 | no |
| F18 | A8 round-49 screened 3 != included+excluded 2 (identified 3) | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 5ced4a9a5f51c8b7 | no |
| F19 | A8 round-49 rows stated 146 -> 147 (derived 148) | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 947ec5db743b5cec | no |
| F20 | A9 closure calibration row edited to improved | reject | 1 | A9 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A9'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A9'] noop []; A3 one point | 7a949a64c3588bd3 | no |
| F21 | A9 closure admission token rewritten to accepted (all occurrences) | reject | 1 | A9 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A9'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A9'] noop []; A3 one point | 299872cb813993b1 | no |
| F22 | A2 real hash is a side-branch commit that is not an ancestor of REV | reject | 1 | A2 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A2'] noop []; A3 one pointer line number moved -> red ['A2', 'A3'] noop []; A4 reports count  | f31c963bb8d77532 | no |
| F23 | frozen tools/round-49/c2-mismatch.py touched then restored byte-identically (later restore) | reject | 2 | frozen_path_changed | 2 (none) | 6db2239559e92bb3 | no |
| F24 | frozen plans/round-49-claims.md touched then restored byte-identically | reject | 2 | frozen_path_changed | 2 (none) | 97fd6a54e5aa7048 | no |
| F25 | frozen tools file modified and not restored (control) | reject | 2 | frozen_path_changed | 2 (none) | 1d74cf0ce7a7ef73 | no |
| F26 | A2 duplicate line placed before the real one (last line wins in the parser) | accept | 0 |  | 1 (A2 real hash replaced by a non-commit -> red [] noop []) | 98bbe11aa7973e39 | YES |
| F27 | A3 line carries no log_ pointer at all | reject | 1 | A3 | 1 (genuine REV is not green; mutation set incomplete: 10 of 11; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red | 1368c225ee123178 | no |
| F28 | A6 S147 used-by names a lesson that is not the round-49 lesson | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | 36e345c9c63b6148 | no |
| F29 | A6 S147 opened date 2026-10-27 | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | a79a11f56c28d3f0 | no |
| F30 | S145 registry line edited in place (append-only broken) | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | a862f7382172e7a2 | no |
| F31 | A6 S147 source URL changed to another path on the same host | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | 9e82310e2b59fbe8 | no |
| F32 | A6 S147 quotation lengthened to 30 words, present in the snapshot | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | f7df6cd35a62b66b | no |
| F33 | A5 lesson report_c1 names the RAW digest prefix | reject | 1 | A5 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A5'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A5'] noop []; A3 one point | dfc5aa5e240c30f7 | no |
| F34 | A5 lesson c1_raw zeroed | reject | 1 | A5 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A5'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A5'] noop []; A3 one point | 28339ece553512db | no |
| F35 | A1 lesson stale names a commit that is not the lesson header freeze | reject | 1 | A1 | 1 (genuine REV is not green; A2 real hash replaced by a non-commit -> red ['A1', 'A2'] noop []; A3 one pointer line number moved -> red ['A1', 'A3'] noop []; A4 | e5b17bcd26a0ca5e | no |
| F36 | round-48 lesson edited in place (not byte-identical to base) | reject | 1 | A1 | 1 (genuine REV is not green; A2 real hash replaced by a non-commit -> red ['A1', 'A2'] noop []; A3 one pointer line number moved -> red ['A1', 'A3'] noop []; A4 | 06d359cf1e3a1c62 | no |
| F37 | SCORECARD declared == lesson header (no disagreement) | reject | 1 | A1 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1'] noop ['corpus/lessons/round-49.md']; A2 real hash replaced by a non-commit -> red ['A1', 'A2'] | 009fce419d7b3406 | no |
| F38 | A1 lesson declared names a freeze that is not SCORECARD declared | reject | 1 | A1 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1'] noop ['corpus/lessons/round-49.md']; A2 real hash replaced by a non-commit -> red ['A1', 'A2'] | c6ebf99f619731f5 | no |
| F39 | A2 dead hash prefix differs from the real hash prefix | reject | 1 | A2 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A2'] noop []; A3 one pointer line number moved -> red ['A2', 'A3'] noop []; A4 reports count  | b1d3391cedf2f938 | no |
| F40 | A4 seats stated 76 | reject | 1 | A4 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A4'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A4'] noop []; A3 one point | 33da9a3ad014530f | no |
| F41 | A4 missing list drops C1Battery (reports count still consistent) | reject | 1 | A4 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A4'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A4'] noop []; A3 one point | 8e7b83f269d7b90b | no |
| F42 | A3 first pointer numbers wrong (3443 for 3445) | reject | 1 | A3 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A3'] noop []; A4 reports c | d79298425b211d4f | no |
| F43 | A3 second pointer numbers wrong (3443 for 3444) | reject | 1 | A3 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A3'] noop []; A4 reports c | 943095391f3875e2 | no |
| F44 | A3 unnamed list names a hash that LOG.md does name | reject | 1 | A3 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A3'] noop []; A4 reports c | 72fdd386ca93207c | no |
| F45 | LOG.md edited on line 1 (not append-only) | reject | 1 | A3 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A3'] noop []; A4 reports c | 283df6dd9b929ee7 | no |
| F46 | A3 line removed entirely | reject | 1 | A3 | 1 (genuine REV is not green; mutation set incomplete: 10 of 11; A1 swap declared/stale -> red ['A1', 'A3'] noop []; A2 real hash replaced by a non-commit -> red | 8584a51276c2f678 | no |
| F47 | A2 line removed entirely | reject | 1 | A2 | 1 (genuine REV is not green; mutation set incomplete: 10 of 11; A1 swap declared/stale -> red ['A1', 'A2'] noop []; A3 one pointer line number moved -> red ['A2 | f4c0a9db0a769634 | no |
| F48 | S147 teaches opens "fixes S145" instead of "supersedes S145" | reject | 1 | A6 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A6'] noop []; A3 one point | 649b423be9bd230b | no |
| F49 | A8 round-49 included/excluded 1/1 (derived 2/0; screened still 2) | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 02b8f3dbecae9d1d | no |
| F50 | A4 reports stated 71 (derived 72) | reject | 1 | A4 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A4'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A4'] noop []; A3 one point | 0bcd82473f777739 | no |
| F51 | non-.md file placed under the C1Meaning seat directory | accept | 0 |  | 0 (none) | 9a8692e27cf7d94b | YES |
| F52 | SCORECARD A9 line deleted (heading kept) | reject | 1 | A9 | 1 (genuine REV is not green; mutation set incomplete: 10 of 11; A1 swap declared/stale -> red ['A1', 'A9'] noop []; A2 real hash replaced by a non-commit -> red | 93701017720c1dd7 | no |
| F53 | S147 anchor heading names a different section | reject | 1 | A6 | 1 (genuine REV is not green; mutation set incomplete: 10 of 11; A1 swap declared/stale -> red ['A1', 'A6'] noop []; A2 real hash replaced by a non-commit -> red | b7fae7739b71fe00 | no |
| F54 | A8 round-48 entry carries the late marker but its numbers are wrong (rows 144 -> 999) | reject | 1 | A8 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A8'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A8'] noop []; A3 one point | 4fefe16f69de69af | no |
| F55 | A7 S148 quotation lengthened to 30 words, present in the snapshot | reject | 1 | A7 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A7'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A7'] noop []; A3 one point | be957c63ad71e044 | no |
| F56 | A7 S148 quotation marks removed (no quoted passage) | reject | 1 | A7 | 1 (genuine REV is not green; A1 swap declared/stale -> red ['A1', 'A7'] noop []; A2 real hash replaced by a non-commit -> red ['A2', 'A7'] noop []; A3 one point | 08630ce33342993a | no |

## Source mutants (56) — kill status

| id | atom | mutation | shipped battery / genuine | FREEZE run | fixture forgeries that flip it | status | mutant file sha256 (16) |
|---|---|---|---|---|---|---|---|
| M01 | A1 | declared!=SCORECARD check removed | - | exit 1, mismatches 9 | F38 | KILLED | 78e38594bdcab910 |
| M02 | A1 | stale!=lesson-header check removed | - | exit 1, mismatches 9 | F35 | KILLED | cd4fb5a694ab885e |
| M03 | A1 | round-48 lesson byte-identity compare removed | - | exit 1, mismatches 9 | F36 | KILLED | c450db3bf9c2f39c |
| M04 | A1 | declared==stale no-disagreement check removed | - | exit 1, mismatches 9 | F37 | KILLED | 7bacf9d8ce5ca914 |
| M05 | A2 | dead-hash-resolves-to-commit check removed | - | exit 1, mismatches 9 | - | SURVIVED | 1d684b78533704f8 |
| M06 | A2 | 8-hex prefix check removed (dead==real kept) | - | exit 1, mismatches 9 | F39 | KILLED | c7e598077c78bb77 |
| M07 | A2 | real-is-ancestor-of-REV check removed | - | exit 1, mismatches 9 | F22 | KILLED | 314c5bc7d186b13e |
| M08 | A3 | LOG.md append-only startswith compare removed | - | exit 1, mismatches 9 | F45 | KILLED | b938755ec9902043 |
| M09 | A3 | stated-vs-derived line-number compare removed | battery/genuine | exit 1, mismatches 9 | F42, F43 | KILLED | 51e339c841051391 |
| M10 | A3 | only the first log_ pointer checked | - | exit 1, mismatches 9 | F43 | KILLED | 568b6d6a4c25472a |
| M11 | A3 | unnamed-hash check removed | - | exit 1, mismatches 9 | F44 | KILLED | b243ad6a4df87257 |
| M12 | A4 | seats count check removed | - | exit 1, mismatches 9 | F40 | KILLED | 021556f9747b6adf |
| M13 | A4 | missing-seat list check removed | - | exit 1, mismatches 9 | F41 | KILLED | e17787e26a2c77de |
| M14 | A4 | every seat counted as having a report | battery/genuine; genuine | exit 1, mismatches 9 | F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F26, F27, F28, F29, F30, F31, F32, F33, F34, F35, F36, F37, F38, F39, F42, F43, F44, F45, F46, F47, F48, F49, F51, F52, F53, F54, F55, F56 | KILLED | 6ed0f2d83999729c |
| M15 | A4 | non-.md file under seat dir counts as report | battery/genuine; genuine | exit 1, mismatches 9 | F01, F02, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F26, F27, F28, F29, F30, F31, F32, F33, F34, F35, F36, F37, F38, F39, F42, F43, F44, F45, F46, F47, F48, F49, F51, F52, F53, F54, F55, F56 | KILLED | 522f78c075ea95af |
| M16 | A5 | stripped-digest compare removed | battery/genuine | exit 1, mismatches 9 | - | KILLED | d66b094873f092bc |
| M17 | A5 | report-prefix compare weakened to length only | - | exit 1, mismatches 9 | F33 | KILLED | d9e90f216eb5c5b4 |
| M18 | A5 | raw-digest compare removed | - | exit 1, mismatches 9 | F34 | KILLED | 3be2f6545cb687ed |
| M19 | A5 | stripped digest computed without stripping | battery/genuine; genuine | exit 1, mismatches 9 | F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F26, F27, F28, F29, F30, F31, F32, F35, F36, F37, F38, F39, F40, F41, F42, F43, F44, F45, F46, F47, F48, F49, F50, F51, F52, F53, F54, F55, F56 | KILLED | efd99c60c7cfe9a2 |
| M20 | A6/A7 | row teaches must open "supersedes <old> —" removed | - | exit 1, mismatches 9 | F48 | KILLED | 6e1f3ed1bfdbb74f |
| M21 | A6/A7 | anchor sha256 pin to snapshot removed | - | exit 1, mismatches 9 | F11 | KILLED | 1a00bdab39b3095f |
| M22 | A6 | word limit 25 -> 250 (A6) | - | exit 1, mismatches 9 | F32 | KILLED | 35df931aa86ad6f1 |
| M22b | A7 | word limit 25 -> 250 (A7) | - | exit 1, mismatches 9 | F55 | KILLED | 278a407c4d190868 |
| M23 | A6 | anchor must name the snapshot heading removed | battery/genuine | exit 1, mismatches 9 | F53 | KILLED | c12b945ed2f9b12b |
| M24 | A6 | S147 quoted-passage presence removed | - | exit 1, mismatches 9 | F12 | KILLED | 88f10e8c9d5356dc |
| M24b | A7 | S148 quoted-passage presence removed | - | exit 1, mismatches 9 | F56 | KILLED | 3093722a66f11d96 |
| M25 | A7 | S148 quote-in-snapshot check removed | - | exit 1, mismatches 9 | F13 | KILLED | e2980b2439a6ed7b |
| M26 | A7 | snapshot must carry "EX_USAGE 64" removed | - | exit 1, mismatches 9 | F14 | KILLED | 343dc4b1876b4006 |
| M27 | A7 | teaches must name 64 removed (keeps EX_USAGE) | battery/genuine | exit 1, mismatches 9 | - | KILLED | 9ff8fc6e7f75b7a0 |
| M28 | A7 | S148 source URL (3head) check removed | - | exit 1, mismatches 9 | F15 | KILLED | b17386e7f1a2b07d |
| M29 | A6 | S147 source-domain check removed | - | exit 1, mismatches 9 | F31 | KILLED | d4eb17b5326a2102 |
| M30 | A8 | exactly-one search-log entry per round weakened to >=1 | - | exit 1, mismatches 9 | F16 | KILLED | 1c8818612a065c88 |
| M31 | A8 | screened == included+excluded check removed | - | exit 1, mismatches 9 | F18 | KILLED | 93acddd0d9e7948a |
| M32 | A8 | identified >= screened check removed | - | exit 1, mismatches 9 | F17 | KILLED | 2fbe0b98fd2a6133 |
| M33 | A8 | rows B -> A check removed | - | exit 1, mismatches 9 | F19, F54 | KILLED | 71a0857f506ef2c8 |
| M34 | A8 | round-48 late-entry filter removed | battery/genuine | exit 1, mismatches 9 | - | KILLED | e39879e001a8815a |
| M35 | A9 | SCORECARD A9 line presence removed | battery/genuine | exit 1, mismatches 9 | F52 | KILLED | 6880f16fa74f76a7 |
| M36 | A9 | source calibration|harmed row check removed | - | exit 1, mismatches 9 | F20 | KILLED | 4c523ad96c87d808 |
| M37 | A9 | source rejected-harmed token check removed | - | exit 1, mismatches 9 | F21 | KILLED | 4f8a375620f1fa59 |
| M38 | freeze | FREEZE ancestor-of-REV check removed | - | exit 1, mismatches 9 | - | SURVIVED | fae5c604e1cffa29 |
| M39 | freeze | FREEZE..REV path walk (touched) removed | - | exit 1, mismatches 9 | F23, F24 | KILLED | 6e9912e0eca58ed0 |
| M40 | freeze | blob-equality backstop removed | - | exit 1, mismatches 9 | - | SURVIVED | 61432d6b30b802b8 |
| M41 | freeze | plans/round-49-claims.md dropped from the walk | - | exit 1, mismatches 9 | F24 | KILLED | 1973c053449a9b84 |
| M42 | exit | exit code forced to 0 | freeze-run | exit 0, mismatches 9 | F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F27, F28, F29, F30, F31, F32, F33, F34, F35, F36, F37, F38, F39, F40, F41, F42, F43, F44, F45, F46, F47, F48, F49, F50, F52, F53, F54, F55, F56 | KILLED | 9b1ea9326e9f64ab |
| M43 | exit | battery failing list ignored in exit code | - | exit 1, mismatches 9 | - | SURVIVED | 563df793b06e8521 |
| M44 | battery | do-nothing all-nine-red check removed | - | exit 1, mismatches 9 | - | SURVIVED | 8e8b9f298a09f0c9 |
| M45 | A2 | absent A2 line accepted | battery/genuine; freeze-run | exit 1, mismatches 8 | F47 | KILLED | 4fce4614b511ec51 |
| M46 | A3 | absent A3 line accepted | battery/genuine; freeze-run | exit 1, mismatches 8 | F46 | KILLED | 3be0088150f98d2a |
| M47 | A3 | no-log_-pointer check removed | - | exit 1, mismatches 9 | F27 | KILLED | f58eb5f30a15349b |
| M49 | lesson | lesson lines: first occurrence wins (not last) | - | exit 1, mismatches 9 | F26 | KILLED | 2e9adedd6adab4f2 |
| M50 | A4 | reports count check removed | battery/genuine | exit 1, mismatches 9 | F50 | KILLED | a8fe88d6b9b6ebeb |
| M51 | A6/A7 | row append-only compare of S145/S146 removed | - | exit 1, mismatches 9 | F30 | KILLED | 1c1028b3d36ee52d |
| M52 | A8 | and/or swapped in the A8 (inc,exc) clause | - | exit 1, mismatches 9 | F18, F49 | KILLED | af5210e9595efe69 |
| M53 | A6/A7 | row used-by lesson check removed | - | exit 1, mismatches 9 | F28 | KILLED | df00d89f17cf4ce9 |
| M54 | A6/A7 | row status/tier/opened check weakened (date dropped) | - | exit 1, mismatches 9 | F29 | KILLED | b413be211b077f79 |
| M55 | exit | battery-broken: orig with a no-op battery mutation (see BB pair) | battery/genuine | exit 1, mismatches 9 | - | KILLED | ad90e315fd6ac65e |
