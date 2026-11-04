# ExecRedControls — round-67 w1 report

**Seat:** ExecRedControls · **claim touched:** R67-C1 (read-only; no score run)
**Base:** `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92` · **Freeze:** `3663e6b21dccf4c4957f459301156664d8b151d6`
**Engine (unchanged, imported by path under pin):** `tools/round-50/c1-counter.py`
`9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`
**Instrument at run:** counter `5d6cc82a…`, rule v2 `b55d5e87…` (both = HEAD blobs = claims pins)

**Verdict: battery green.** 20/20 fixtures fire as declared, both supplementary checks pass,
the wrapper's control reproduces at 2 of 4 under round 50 and 4 of 4 under round 67, and the
2/4 was recomputed independently from the raw envelopes. The two must-fail families (foreign
gap kinds, removals naming a non-symlink) all fire with the exact clause message; the two
class boundaries (block-device, FIFO) do not fire, which is the rule's intent. No red fixture
failed to fire.

## Files written (all inside this lane)

| path | what |
|---|---|
| `.ufo/waves/round-67/w1/ExecRedControls/red_controls.py` | the battery: loads the engine under its pin, rebuilds each fixture on its own root/trusted-run-root, asserts the pre-mutation baseline resolves, then checks polarity **and** the clause message |
| `.ufo/waves/round-67/w1/ExecRedControls/red.json` | machine-readable result: pins, instrument chain, rule delta/decomposition, carrier census, 20 fixtures, 2 supplementary checks, verdict |
| `.ufo/waves/round-67/w1/ExecRedControls/red.md` | fixture rationale, admit/reject statement, hiding-risk analysis, findings |
| `.ufo/waves/round-67/w1/ExecRedControls/wrapper-control.json` | fresh `--control` receipt from the current instrument (`814f960c…`, 2/4, exit 0) |
| `.ufo/waves/round-67/w1/ExecRedControls/wrapper-control-at-freeze-blob.json` | the same control from the dispatch-pin blob `f78ed365…` (same numbers) |

No writes outside the lane. No git/jj mutation. Scratch `/fast/scratch/hyaku/kaidoku-r67/ExecRedControls`
created and deleted; nothing under `/tmp`. No subagent dispatched (the single labrat was not needed;
the instrument is deterministic and the battery is a pure function).

## Behaviour (what the battery establishes)

1. **Control reproduced.** `python3 -I -B tools/round-67/avm-le-counter.py --control --rev <base>`
   exits 0 with `gaps_ok_round50 2`, `gaps_ok_round67 4`. Per carrier: `c6430`/`c6490` pass both
   rules; `g7581`/`g7582` fail only under round 50 on `dev/pts/0 … dev/pts/7`. The same 2/4 falls
   out of `disposition_check` called directly with both rule models, and matches the wrapper.
2. **Rule delta is one boolean.** Models differ only in `required["char-device"] true→false`;
   `allowed`, `structural`, `removed.diagnostic`, `removed.kinds` and `removed.silent` are
   identical. Flipping the boolean back reproduces round 50 exactly (2/4, same carriers). Restoring
   the round-50 `silent` row on the round-67 rule changes no carrier (4/4 either way) — the
   restoration in `7cfe83e4` is evidence-neutral.
3. **(a)/(b) are boundaries, (c)/(d) are rejections.** Block-device and FIFO rows with no
   disposition pass (not required in either rule). A gap whose kind is not allowed for its entry
   kind fails four ways (structural kind with a path, `dir` row with a gap, REA kind on a
   symlink/FIFO, path-less foreign kind), both structural allowances are exact, and
   `MaliciousSymlinkRemoved` naming a char-device/FIFO entry fails on `removed.kinds`; so do the
   exclusivity, outside-trusted-root and no-row variants.
4. **Publication is kind-independent.** `nonregular_published` names a published regular file at
   the path of a symlink, char device, dir, FIFO and block device, and does not name a regular
   path that is not a non-regular entry, so no class waiver can materialise a row.
5. **Fail-closed root.** `disposition_check(..., root=None)` fails with
   `no extract root: paths cannot be resolved`.
6. **Clause set unchanged (23) and freshness holds.** `carrier_fresh_ok` is live again; the
   engine's prior-pin harvest at the freeze returns 18 pins from three sources, none of them one
   of the four carrier pins, so the clause can pass on its own.

## Findings the L1 must action

- **F7 (evidence-chain, highest).** The committed control receipt bound by `--score`
  (`.ufo/waves/round-67/l1/pre/control-dryrun.json`, `69cb4a99…`) was generated with counter
  `e44cacf5…` and rule `e66ba02…`; the instrument is `5d6cc82a…` and the rule `b55d5e87…`. Its
  numbers are unchanged (2/4, `control_ok true`), so the new second-conjunct binding passes, but
  the receipt the score will cite was not produced under the rule being scored. Commit `7cfe83e4`
  says "before records re-taken" yet does not include this file in its diffstat.
  Remedy: re-take it with the current pair (this lane's `wrapper-control.json` is that run,
  `814f960c…`; it differs from the committed file only in `counter` and `rule_v2_sha256`), and/or
  make `--score` also compare the bound receipt's `rule_v2_sha256`.
- **F2 (rule text).** `class_disposition.char-device` says the class is "accounted for by the
  re-derived oracle table (every char-device row re-derived … by unsquashfs)". The pinned engine
  re-derives **regular files only** (`c1-counter.py:2127`, docstring at :2094). The real
  compensating controls are the drift-protected frozen non-regular table and
  `nonregular_unpublished`. Correct the prose next round; the score is unaffected because the
  block is inert (F4).
- **F3 (latent).** `class_disposition.block-device` claims the "same reason", but
  `allowed.block-device == []`: a recorded `unpublished-entry` gap on a block device is rejected
  while a silent row passes. No impact on these four carriers (zero block-device rows); a fifth
  carrier with block devices would fail on its own evidence.
- **F5 (documentation).** `patch_engine` also replaces `mod.rea_package_problems`, while the
  numbered list says "five things" and does not name it. It *is* disclosed in `REA_PKG_R67` and in
  the receipt's `patches.rea_pkg`; add it to the enumeration.
- **F1 (dispatch).** The seat card pins counter `f78ed365…` / rule `e66ba02…`, three disclosed
  corrections behind. Following the card literally aborts on a hash mismatch. Point the card at
  `claims.json → instruments` or update the numbers.
- **F6 (note).** An unknown non-regular kind is unrequired at function level
  (`c1-counter.py:1552`); score level catches it via `gap_rule_ok` (`kinds_seen − allowed`), so
  there is no scoring hole.

## Can the admitted classes hide a real extraction failure?

No content failure. They can hide the silent loss of a device/fifo node, and the measured state
is exactly that: on all four carriers `normalized_result.unpublished_entries` holds **only
symlinks** (636/636/612/567) and **zero** char devices — the 13 devices per FRITZ carrier appear in
no gap and in no unpublished-entry list, only in the frozen table. `gaps_ok` never reads
`unpublished_entries`, and the non-regular table is frozen but not byte-re-derived. What still
binds: publication equality for every kind, exact regular-file oracle hits, `chunks_ok`,
`depth-limited` 1, `unknown-chunk-handler` 0, per-row symlink requirement, path shape, the removal
family. So the waiver accepts the by-design skip and cannot hide a regular-file loss, which is the
claim's substance.

## Limits

- No `--score`, no REA, no carrier bytes: the L1 owns the data run. Only the control path was
  exercised dynamically; the score-side GAPRULE patch was verified statically (lane-relative name
  resolves through `git show` at the freeze; the absolute form exits 128).
- Block-device/FIFO/socket rows do not exist on the four carriers; those fixtures append labelled
  synthetic rows (`dev/sda1`, `dev/fifo-test`) to a real envelope.
- Instrument and rule moved four/two times during the wave. The battery pins by HEAD-blob equality
  at run time and records the chain (`3663e6b2 f78ed365 → 1e7fe7b7 55decb51 → ecc4de0e e44cacf5 →
  7cfe83e4 5d6cc82a`; rule `e66ba02 → b55d5e87`), all disclosed, none undisclosed. `red.json`
  describes this run (HEAD `2dd5f2cd`), not any later commit.
- The seat card's "three NEW red fixtures" lists four, with contradictory expectations for (a)/(b);
  executed all four with the per-item polarity and recorded the defect in `red.md`.
