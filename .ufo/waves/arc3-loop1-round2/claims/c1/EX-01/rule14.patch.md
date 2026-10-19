# Queue-drain rule #14 — SKILL.md PATCH TEXT (NOT APPLIED) — seat EX-01 (executor), chain c1

Wave: arc3-loop1-round2 (kaidoku-shokunin). Pre-image: `SKILL.md` at HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420` (371 lines, sha256
`483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`).
Target: append the bullet below to the end of the queue-drain craft section,
immediately after `SKILL.md:239` (the last line of rule #13, the line carrying
`kernel-OOM-killed (` `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37` `).`),
as rule #14. The patch is a pure insertion of 15 payload lines + one blank
line: zero pre-existing lines change, `SKILL.md` 371 → 387 lines (sha256
`a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28`), and
lines 1–239 stay byte-identical. Not applied by this seat; no repo file was
modified outside this seat's claim directory and seat report.

Revision note (rule #14 applied to this artifact): payload v1 (13 lines, 896 B,
sha256 `a47dc38d…`) was superseded within this seat's own writes after c1
peer evidence landed — RV-1's fidelity list (`seats/RV-1.md` §5: subject
binding, re-establishment clause), CR-1's laundering critique of the
incident-citation family (`claims/c1/CR-1/rule14-candidates.md`), EX-04's
SHONEN-end pointer check (`claims/c1/EX-04/receipts/t1-geometry.txt`). All
identities below were re-derived after the final write; v1 numbers are kept
only as history.

## 1. Payload (verbatim — the block to insert)

<!-- payload-begin -->
- **An artifact that records its own byte-identity must re-derive that
  identity after every revision; a stale self-identity voids the verification
  block, not the work.** Size/hash/line-count claims bind the bytes they
  describe, not an earlier revision of the same patch: after the C1 entry
  patch was revised, its step-4 claim still read 8,316 B / `f95c5a05…` while
  the applied bytes hashed 8,598 B / `d8d85949…`
  (`.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89`), and the chain measured
  three applied identities inside ~20 minutes, the fix being the fresh landing
  hash (`.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md:149-153`). The
  voided block is re-established by re-running its checks against the current
  bytes; the integrator records the fresh identity of the landed revision —
  10,225 B / `dd986f56…` for the landed entry
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`, whose recheck line
  records the mid-wave revision (`SCORECARD.md:1366-1368`; `LOG.md:1411-1412`)
  — never a revert, never a carried-over number.
<!-- payload-end -->

Payload identity (trailing newline included): 1,071 bytes, sha256
`6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f`.
Verify by extracting the lines strictly between the two HTML-comment markers
above (no leading/trailing blank) and hashing them.

This artifact deliberately does not assert its own file identity inline — the
self-identity discipline it lands is the reason: a hash written here would
have to be re-derived after every revision of this file. The fresh artifact
identity is recorded post-write in `identity-final.txt` (same directory, rule
#14 in action) and must be re-derived by the integrator at landing.

## 2. Apply recipe (unified diff, generated on a scratch copy)

```
--- a/SKILL.md
+++ b/SKILL.md
@@ -237,6 +237,22 @@
   (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-19`); the matched natural
   control omitted the disables under the same caps/deadline and was
   kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).
+- **An artifact that records its own byte-identity must re-derive that
+  identity after every revision; a stale self-identity voids the verification
+  block, not the work.** Size/hash/line-count claims bind the bytes they
+  describe, not an earlier revision of the same patch: after the C1 entry
+  patch was revised, its step-4 claim still read 8,316 B / `f95c5a05…` while
+  the applied bytes hashed 8,598 B / `d8d85949…`
+  (`.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89`), and the chain measured
+  three applied identities inside ~20 minutes, the fix being the fresh landing
+  hash (`.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md:149-153`). The
+  voided block is re-established by re-running its checks against the current
+  bytes; the integrator records the fresh identity of the landed revision —
+  10,225 B / `dd986f56…` for the landed entry
+  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`, whose recheck line
+  records the mid-wave revision (`SCORECARD.md:1366-1368`; `LOG.md:1411-1412`)
+  — never a revert, never a carried-over number.
+
 
 
 ## Config custody for live-probe rounds (SOP)
```

Anchor form (does not depend on absolute hunk numbers): insert the payload
plus one empty line immediately after the unique line containing
`kernel-OOM-killed (` `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37` `).`
— not "immediately before the `## Config custody` heading", which would leave
no blank separator.

## 3. Measured before → after (seat-side, scratch tree from the `14b1682` archive)

| Check | Before (tree-before) | After (tree-v2, payload applied) |
|---|---|---|
| command A (recipe `SCORECARD.md:88-124`) | 13 rules, 13/13, 82/82, 10.0/10.0 | **14 rules, 14/14, 82/82, 10.0/10.0** |
| prior rules | — | prefix 1–239 byte-identical (`cmp`); diff = 15 added, **0 removed/changed** |
| SKILL.md identity | 371 lines `483b0eba…` | 387 lines `a8170b96…` |
| E21/census token classes (`.ufo/gates/c1-census-v10.py:163-167`) | — | `PIN=0 VER=0 PTR=0 CACHE=0 REA_GATE=0` over the 1,071 payload bytes |
| census v10, committed bytes (sha256 `6f1d19ff…`) | `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; `SKILL.md lines=371 loci=2` | identical except `SKILL.md lines=387 loci=2`; full-output diff = that one line |
| citation-drift probe | `reported findings=0 exit=0` at HEAD | cannot stale: table's only SKILL.md entry is `anchor` (content-anywhere); `shonen-skill-range` needle stays at `SKILL.md:233` |
| SHONEN.md:6 pointer check (EX-04's convention: stated end == last rule line) | stated 243 vs last rule 239 → FAIL (EX-04 measured) | post-append last rule line = **254**, next heading 258 → refreshed SHONEN must state `SKILL.md:81-254` |
| end-to-end from this artifact | — | payload extracted from the patch text (hash `6cc388cb…`) applies cleanly → 14/14; identical patched SKILL.md `a8170b96…` (`evidence/e2e-from-artifact.txt`) |

Fidelity of the adapted runner (`evidence/commandA-worktree.py`): on the
unpatched scratch copy it reproduces the canonical real-repo command A numbers
exactly (13/13, 82/82, 10.0/10.0).

## 4. Same-commit obligations for the integrator

1. Land the payload per §2; re-run command A at the work commit and expect
   rules 14/14 (any other number means the append landed elsewhere).
2. Re-derive and record the fresh `SKILL.md` identity at landing (size +
   sha256) in the LOG/SCORECARD round record — the practice this rule
   distills (round 1: the entry patch's stale `8,316 B`/`f95c5a05…` claim was
   superseded; the landed identity `10,225 B`/`dd986f56…` was recorded
   instead, `SCORECARD.md:1366-1368`). Note the on-disk round-1 patch
   `claims/c1/EX-12/knowledge-entry.patch.md` (sha256 `d662c195…`) still
   declares `9,513 B`/`a5119120…` for superseded bytes (RV-1's F4 residual) —
   do not copy that number as the landed identity.
3. Refresh `SHONEN.md:6` in the same commit (its text is stale on two counts:
   range `81-243` and `13/13`). Proposed same-line replacement, after the
   append: `` asserted: `SKILL.md:81-254` (craft section; rules #11-14 added
   arc2 rounds 4/7/9 + arc3 round 2); 14/14 rule blocks have resolvable
   citations, not a full semantic audit — `SCORECARD.md`, command A; no
   identified outside verifier.``
4. Expect `SKILL.md lines=` to move in census output (371 → 387) while loci
   stay 2 and the verdict stays PASS; do not read the line-counter move as
   drift. Do not widen the census scope rows or the probe's pointer table
   (r4 laundering precedent) — this text needs neither.

## 5. Origin evidence, peer cross-check, and self-attack

- Origin, first-hand: the stale window is CR-2's F2 — applying the then-current
  patch yielded 8,598 B / `d8d85949…` while its step-4 claim still read
  8,316 B / `f95c5a05…`
  (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/proposed-fixes.patch.md:36-49`,
  `entry-file-identity.txt`, `seats/CR-2.md:86-89`). The chain verdict D9
  records the three applied identities inside ~20 minutes (8,598 / 8,316 /
  9,513 B) and makes the fresh landing hash the fix
  (`claims/c1/verdict.md:149-160`); VZ-1's row sustains it independently
  (`seats/VZ-1.md:115`). The landed revision measured 10,225 B /
  `dd986f56…`, recorded at landing (`SCORECARD.md:1366-1368`;
  `LOG.md:1411-1412`). The current patch artifact declares 9,513 B /
  `a5119120…` (its step 4, `claims/c1/EX-12/knowledge-entry.patch.md:99-101`)
  — self-consistent at rev B, superseded by landing.
- Peer cross-check (c1 peers' independent measurements, re-derived by me
  where numbers are reused): CR-1's and EX-02's candidate-form runs put a
  citation-free "honest" rule at 13/14, depth 9.29
  (`claims/c1/CR-1/rule14-parser-results.txt`,
  `claims/c1/EX-02/prediction-prereg.md`); RV-1's T4 shows that naming the
  incident's recheck command verbatim turns the census red
  (undeclared=1) — a needle-free paraphrase is required, and this payload
  scans 0 on every needle class. RV-1's §5 fidelity list is satisfied item by
  item: subject binding (the claim binds the bytes it describes, the patch
  records the output), actor split (author re-derives; integrator records at
  landing), disposition fidelity (the block is re-established by re-running
  its checks), boundedness ("after every revision"), falsifiability (14/14 +
  re-checkable numbers at cited paths), citation form (the counted citation is
  the incident's own landed entry — the only honest one per RV-1 §5.6), and
  instrument safety (needle-free).
- Attacks on my own text, with verdicts: (a) *over-generalization* — a rule
  that read "any stale identity voids the work" would contradict the measured
  handling (work kept, hash re-recorded); wording keeps the bound and the
  consequence (verification block only). (b) *citation laundering* — the
  counted `corpus/knowledge` citation is the churned artifact's landed entry,
  not an unrelated file; the incident ledger is the wave/round records cited
  beside it; a decoration-only citation (CR-1's T3) would pass the metric and
  is explicitly not this text. (c) *misattribution* — v1 attributed the
  8,316 B claim to the entry; v2 binds it to the patch's step-4 claim, which
  is where CR-2 measured it. (d) *instrument interaction* — the append adds no
  census locus and no needle (measured), moves only the `lines=` counter, and
  cannot stale the probe's SKILL.md anchor or the SHONEN needle (measured).
