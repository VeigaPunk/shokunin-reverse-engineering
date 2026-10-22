# Wave 2 seat report — RecomputeIndependent (Kaidoku round 26, attempt 1)

Target: the 24 committed evidence ids in corpus/evidence/round-26/c1/ (8 frozen verbs x base/repeat/copy).
Revision judged: fe3eb4edf410244eff46151a148c8f754be1ce80 (lane HEAD at start). All hashed bytes are
committed blobs, extracted with `git archive fe3eb4ed... corpus/evidence/round-26/c1` into my scratch.
Worktree drift at run time (7 paths: QUALITY.md, README.md, the r26 knowledge entry, three w1 reports,
untracked w2 dir) does not touch corpus/evidence/ (observation, `git status --porcelain`, 2026-10-22T13:02Z).

## Method

I wrote my own recompute from a direct read of the installed rea-agents 6.5.0 sources. I did not open
tools/round-26/recompute-ids.py (only its --help, to learn the CLI). Sources read 2026-10-22, package
root /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/:

- dist/domain/canonicalDigest.js, sha256 f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9.
  Quote: "JSON object keys follow RFC 8785's UTF-16 code-unit order in both".
- dist/domain/evidence.js, sha256 f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff6.
  Quote: "Hash semantic content, including raw results and excluding display-subject fields."

Semantics I implemented (observation, from those sources): id = "ev_" + sha256(canonical JSON of
semanticProjection(data without evidence_id)); projection keys are subject (reduced to digest, format,
architecture — path/name/local_path dropped), provider, analysis_profile, predicate_type, operation,
parameters, raw_result, normalized_result, confidence, authority, environment, limitations,
relationship_coverage (only when non-null), locations, evidence_links; canonical JSON sorts object keys
by UTF-16 code units and uses JSON.stringify string/number semantics, undefined members omitted.

Frozen rules read: .ufo/waves/round-26/claims.json, sha256 1137c312d9d1a4aa83ec4f7b167bcd03423de955d89ede1e53f3c6bf6bfbcb5f.

## Commands, exits, times (UTC 2026-10-22)

1. My recompute (Python, own canonicalizer + projection, reads Git blobs at REV):
   `python3 -I -B .../my_recompute.py fe3eb4edf410244eff46151a148c8f754be1ce80`
   13:04:56Z-13:05:16Z, exit 0. Excerpt: "SUMMARY match=24 total=24 flags=0".
2. Package-truth cross-check (Node imports the real digestCanonicalValue and parseEvidence):
   `node .../node_crosscheck.mjs` — 13:04:56Z-13:05:16Z, exit 0.
   Excerpt: "SUMMARY match=24 total=24 parseAccept=24". parseEvidence accepted all 24 records
   (its authentication recomputes the id from content and rejects mismatches).
3. Lane tool on the extracted committed envelopes:
   `python3 -I -B tools/round-26/recompute-ids.py --verbose <24 envelope paths>` — 13:04:56Z-13:04:57Z,
   exit 0. Excerpt: "recomputed ids: 24 match of 24 total". (An earlier invocation at 13:04:56Z exited 2
   because I passed a wrong relative tool path from my scratch cwd; not a lane defect, rerun above.)
4. Committed receipt cross-check: corpus/evidence/round-26/c1/recompute-ids.txt at REV says
   "recomputed ids: 24 match of 24 total", rc=0 — consistent with my runs.

## Verdict (falsify attempt: no counterexample found)

- Match counts: my recompute 24 of 24; lane tool 24 of 24; package parseEvidence 24 of 24 accept;
  committed receipt 24 of 24. Envelopes where the two recomputes disagree: none. Envelopes where any
  recomputed id differs from the committed id: none.
- Independent integrity checks, all 24/24 (my script output columns): committed envelope bytes sha256
  equals runs.tsv envelope_sha256; each envelope's .data.evidence_id equals its table.tsv cell
  (base_id/repeat_id/copy_id) and its runs.tsv evidence_id; ok==true in all 24.
- inspect-binary-layout path sensitivity re-derives: my implementation reproduces the alternate-path id
  ev_52da4b3df64645306a8046c6571ce7849fd2ae4383e8d05f16601fefcdccd161 from the copy envelope, because
  /parameters/path, /normalized_result/artifact/path and /locations/0/path carry the path into the hash
  while subject.path is dropped from the projection (observation; agrees with the lane tool --verbose
  diagnostics and with the derived verdict "path-sensitive").

## Findings by severity

- High/Medium: none.
- Informational (observation): analyze and inspect share one id, ev_14f9d92f41c6a4218108768927a622dbd
  7057ade4bcd305d083e0d6826b3d328, across all six envelopes, while the envelope files differ (different
  runs.tsv envelope_sha256). I compared the two .data objects field by field: key sets equal and every
  field's JSON equal, so the records are semantically identical (operation binary_overview for both) and
  only file-level key order/whitespace differs. Both records pass package parseEvidence. This is the
  semantic-id design working, not a collision defect; R26-C1's rules do not require distinct ids per verb.

## Residual risk and verification gaps

- I judged committed bytes at one revision (fe3eb4ed) and did not re-run the 24 REA CLI observations;
  whether the live 6.5.0 CLI still produces these envelopes is outside this seat's scope.
- My canonicalizer is proven equal to the JS one only on the value domain present: integers within
  2^53, no floats, ASCII keys/strings. My script flags floats, big ints and lone surrogates and saw
  flags=0, but exotic number formats were not exercised (unknown, untested domain).
- parseEvidence acceptance is package truth for 6.5.0 only; the 6.7.0 package root was not tested
  (the claim pins 6.5.0).

## Artifacts (scratch root /fast/scratch/hyaku/kaidoku-r26/seats/w2/RecomputeIndependent/)

- my_recompute.py — e0f43b907df3ccf61d9d43fe8d1b45a676fab6190e1774f6a2e589073cdabc66 (my implementation)
- node_crosscheck.mjs — eed45ab98ebbd95175fdd2df1715cf571659b86b55a97af9383d87cea8d165f8
- out/my_recompute.stamped.out — 5572943cadc47b3d5bbf179439aa7790a74b0cfd1f5ac687e0ff6be2dff97b57
- out/node_crosscheck.stamped.out — c35b8d76813d7fa9593099ea87b3248a2fe2c0ffaef68ea4274609abe1dbb080
- out/lane_tool.stamped.out — a8feba3c8ed39c3533c73b39f2fe11240003473b7381a0ec9a649e4d466e9edf
- out/rev-extracted.tar — 478cd384eb922d3bb631a50c9e579a12484b645c51df4c9e79b42c53f2b67bfd
  (git-archive extraction at fe3eb4ed: 24 envelopes plus table.tsv 89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df,
  runs.tsv 250a00a8ddda82eb712def66300fdfeef185d5296afde6dfe040c8784040d6c5,
  recompute-ids.txt 28fd4e8760099d7abe3322950445d58bb6edf8b44ca6ebba52d13fd2e427e4fb; each envelope's
  sha256 is verified against the runs.tsv receipt column in my script output, 24/24 yes)

Tooling installs: none (host node v24.21.0 and python 3.14.8 were sufficient; pacman untouched).
