# ExecC2 — R93-C2 draft validation (dress rehearsal for the L1 landing)

Seat: ExecC2 (executor), lane kaidoku, round 93, wave r93-w1. Freeze commit
`92a240521bd1bf2213b75d18d9b176a8dafdc67c`. Scratch: `/fast/scratch/hyaku/kaidoku-r93/ExecC2`
(deleted before yield; all receipts copied into `.ufo/waves/round-93/w1/ExecC2/`).

## Verdict

**HIGH — do not land the drafts unchanged.** Draft block 32 as written fails
both frozen depth counters on atom `no-citation`: it cites no
`corpus/knowledge/<stem>.md` path, and `resolve()` in
`tools/round-89/depth-blocks-v2.py` (imported by v3) returns
`["no-citation"]` for any block with zero knowledge citations
(`depth-blocks-v2.py:75-77`). v2/v3 report `blocks 32, resolved 31,
unresolved [{block: 32, problems: ["no-citation"]}], met_target false,
exit 1`. The claim's own frozen target ("32 blocks, resolved 32" / v3
`--expect-blocks 32` met) is unreachable with the current draft bytes; the
kill rule "any depth regression counter unmet" would fire at scoring.

**Everything else is green.** The citation-semantic atoms all pass
(after-manifest `ok`, exit 0), block 31 is byte-untouched (before-manifest
exit 1 with exactly the frozen atom), the insertion is pure addition, and the
inserted bytes equal the draft files (verified mechanically).

**Minimal repair, proven green:** add one knowledge citation to block 32's
text — in my proof-of-fix clone I appended
`` `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md` `` (present at
the freeze, so QUALITY-159-clean) to the block's Refs line. Result: v2 32/32
met=True exit 0; v3 `--expect-blocks 32 --shape-from 32` met=True exit 0;
after-manifest still ok; before-manifest still exit 1 with the same single
atom. The L1 may prefer the round-93 knowledge entry it lands in the same
commit (then the citation is outside-base by one commit — its call under
QUALITY 159).

## Steps, commands, exit codes

All runs: `cd $S/cand` (or `cand2`), `TMPDIR="$S/tmp"`,
`python3 -I -B <tool> --root <tree> --worktree ...`. Scratch
`S=/fast/scratch/hyaku/kaidoku-r93/ExecC2`.

0. Clone: `git clone --shared -q <lane> $S/cand && git -C $S/cand checkout -q 92a24052…` —
   toplevel `$S/cand`, HEAD `92a240521bd1bf2213b75d18d9b176a8dafdc67c`, clean.
   Tool pins: `craft-citation-semantic.py` sha256
   `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340` (matches
   the row-188 draft's pin); `depth-blocks-v2.py`
   `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`;
   `depth-blocks-v3.py`
   `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f`.

0a. Baselines on the pristine clone (calibration before editing):
   - `craft-citation-semantic.py --root $S/cand --worktree --manifest …/block31-before.json --block 31 --json-out $S/pre-before-baseline.json`
     → exit 1, single atom, byte-identical to the committed base receipt
     `…/pre/r93-c2-block31-before.json`:
     `row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]`
   - `depth-blocks-v2.py --root $S/cand --worktree --expect-blocks 31` → `blocks 31 resolved 31 expect 31 unresolved 0 met=True exit=0`
   - `depth-blocks-v3.py --root $S/cand --worktree --expect-blocks 31 --shape-from 31` → `blocks 31, resolved 31, required-shaped 1/1 … met=True exit=0`
   - `craft-citation-semantic.py --selftest --work $S/work/selftest` → `cases=10 failures=0`, exit 0.

1. Candidate tree built in the clone only:
   - SKILL.md: draft block 32 inserted between block 31's Refs line and the
     blank line before `## Config custody for live-probe rounds (SOP)`
     (heading measured at line 767 in the freeze clone, matching the item;
     block 32 lands at lines 767-776, one blank line kept before the heading).
   - corpus/QUALITY.md: draft Row 188 appended as the last bullet (line 319),
     blank-line separated, `- **Row 188 (…` format matching the file.
   - Byte fidelity: `git diff -U0` added-lines diffed against the draft files
     → the only deltas are the structural blank separators
     (`skill-bytediff.txt`: `11d10 <` one trailing blank;
     `quality-bytediff.txt`: `1d0 <` one leading blank). No drift in any draft
     byte.

2. After-manifest (step-2 deliverable): `craft-citation-semantic.py --root $S/cand --worktree --manifest …/manifests/block32-after.json --block 32 --json-out $S/after-dryrun.json`
   → **exit 0, `ok`**. Atoms `{block_present, marker, shape}` all true;
   checked rows: 176/178/184/188, `missing_keywords: []` on all four.

3. Depth regression: **FAILS on the drafts as written.**
   - `depth-blocks-v2.py --root $S/cand --worktree --expect-blocks 32 --json-out $S/post-v2.json`
     → `blocks 32 resolved 31 expect 32 unresolved 1 met=False exit=1`;
     unresolved: `[{"block": 32, "problems": ["no-citation"]}]`.
   - `depth-blocks-v3.py --root $S/cand --worktree --expect-blocks 32 --shape-from 32 --json-out $S/post-v3.json`
     → `blocks 32, resolved 31, required-shaped 1/1 expect 32 shaped_required 1/1 unresolved 1 met=False exit=1`;
     same `no-citation` on block 32. The shape clause itself HOLDS
     (`shaped_required 1/1`) — block 32's decision table passes the boundary
     requirement; only the knowledge-citation floor fails.
   - Flag notes: v2/v3 `--help` confirm the flag spellings used;
     `--shape-from 32` passed explicitly per the item. v3's `--expect`
     (frozen label) was not passed — no frozen v3 label exists for this round
     in claims.json; `--expect-blocks` drives `met_target`.

4. Before-manifest against the edited clone: `… --manifest …/block31-before.json --block 31 --worktree --root $S/cand --json-out $S/post-before.json`
   → **exit 1 with the same single atom** as the base receipt (verbatim above).

5. Insertion disturbance check: `git -C $S/cand diff --stat` →
   `SKILL.md | 11 ++++++++++`, `corpus/QUALITY.md | 2 ++`,
   `2 files changed, 13 insertions(+)`; `--numstat` → `11 0 SKILL.md`,
   `2 0 corpus/QUALITY.md`. Zero deletions ⇒ block 31's bytes and every other
   line are untouched. `git status --porcelain` shows only the two intended
   modified files.

6. Proof-of-fix variant (`$S/cand2`, copy of cand + the one Refs-line
   knowledge citation):
   - after-manifest → `ok exit 0`;
   - v2 → `blocks 32 resolved 32 expect 32 unresolved 0 met=True exit=0`;
   - v3 `--expect-blocks 32 --shape-from 32` → `blocks 32, resolved 32, required-shaped 1/1 … met=True exit=0`;
   - before-manifest → exit 1, same single atom.

## Draft defects (verbatim)

1. **HIGH — block 32 has no `corpus/knowledge/` citation.** v2/v3 `resolve()`:
   `refs = re.findall(PATTERN, rule); if not refs: return False, ["no-citation"]`
   (`tools/round-89/depth-blocks-v2.py:75-77`). Draft block 32 cites QUALITY
   rows 176/178/184/188, `corpus/lessons/round-92-verifier-spotcheck.md:96-100`
   and `tools/round-93/craft-citation-semantic.py` — no knowledge path — so
   `met_target` cannot be true at 32 blocks. Fix: one knowledge citation in
   the block (Refs line suffices; verified).
2. NOTE — row 188's Evidence line cites `corpus/lessons/round-93.md` (M93-a),
   absent at the freeze (`git cat-file -e 92a24052…:corpus/lessons/round-93.md`
   → exit 128). No frozen counter reads it (the citation-semantic checker
   reads only SKILL.md and corpus/QUALITY.md; depth counters resolve only
   `corpus/knowledge/` paths), so it breaks no atom — but the landing commit
   must carry that lesson or the citation dangles (QUALITY 159 class).
3. NIT — the item prose says "craft ends at line 766, heading at 767";
   measured in the freeze clone: block 31's Refs line 765, blank 766, heading
   767. Anchor-based insertion, no impact.

## Files written (lane)

- `.ufo/waves/round-93/w1/ExecC2.md` (this report)
- `.ufo/waves/round-93/w1/ExecC2/` receipts: `pre-before-baseline.json`,
  `pre-v2-baseline.json`, `pre-v3-baseline.json`, `after-dryrun.json`,
  `post-v2.json`, `post-v3.json`, `post-before.json`, `fix-after.json`,
  `fix-v2.json`, `fix-v3.json`, `fix-before.json`, `skill-bytediff.txt`,
  `quality-bytediff.txt`, `diff-stat.txt`.

## Bounds, tooling, cleanup

- Only seat-directory writes in the lane; clones and fixtures under scratch;
  every counter run carried `TMPDIR="$S/tmp"` and the selftest `--work`.
- Read-only git only in the lane (`clone` source, `rev-parse`, `cat-file -e`,
  `ls-tree`, `log`); fixture/clone mutations asserted via
  `git rev-parse --show-toplevel` = the clone dir.
- No tool installs or upgrades (stock `python3`); no pacman, no host changes.
- Scratch `/fast/scratch/hyaku/kaidoku-r93/ExecC2` deleted before yield.
