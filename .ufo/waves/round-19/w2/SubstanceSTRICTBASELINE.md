# C1 STRICT-BASELINE — wave-2 review

## Finding — High: the substance check can falsely close on an arbitrary replayable tool

**Observation.** The current worktree implementation at `.ufo/waves/round-19/tools/routed-r18.py:195-229` checks that the receipt names B18, includes `--strict`, and records exit 1; it re-hashes stdout/stderr, then loads the tool from the receipt-selected `tool_rev` and compares that tool's SHA-256 with the receipt-selected digest (`:204-218`). It only requires `open_count` to be truthy (`:217-218`). It then replays that selected tool and compares exit/stdout/stderr (`:219-228`). It never requires `tool_rev == a245bb00c581ae3423a10a055c77d4bc873918df` (A18), nor the claimed `open_count == 6`. The current worktree diff adds `env=scrubbed_env()` to that replay (`:224-226`), but does not bind the tool identity. The main-commit implementation at 279e has the same gap at `:182-200`.

This disagrees with the named correction: `corpus/lessons/round-19.md:58` at main (line 59 in the current worktree) explicitly says the retained run used the tool blob from A18 and had open 6; `SCORECARD.md:2485` likewise records open 6 and the paired green run. The original finding was that no strict red run had been retained (`corpus/lessons/round-18-verifier-spotcheck.md:195`).

**Mutation observation.** In the isolated `mktemp` clone `/tmp/kr19-w2-substance-strictbaseline.lkeIJB`, based at observed main 279e, I changed only the test-copy of `routed-defects.py`'s `main()` to print `{"open_count":1}` and exit 1, preserving its validator functions. A fabricated receipt points `tool_rev` at that commit and hashes the tool and 17-byte output correctly. Running the current worktree counter against mutant revision `ff25c678fd5ed39babf78b8f13911bd6da4c18d5` returned `R18-STRICT-BASELINE: named=true, substance=true` (`open 1`), total `open_count: 0`, exit 0. Thus the check has a reproducible **false close** even though the retained result is not the A18 strict-baseline result. This test changed only the temporary clone, not the lane.

**Inference.** Pin the accepted tool to the named A18 object/content and validate the expected baseline result (at minimum open 6, rather than any positive count); otherwise a same-repository counterfeit tool plus self-consistent receipt closes this routed defect.

## Actual B/main observations — no false open or false close on the retained artifacts

Main was first observed at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, then advanced during review to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; final measurements below pin 279e. The worktree counter subsequently differed from that main blob (`d7d7ec0be3233d4746dc78476c72ccbcd7a15b1a` vs main `ae1651db86bf3c1262025f624b392c4851f4cb42`), so I ran the committed counter from a clone whose counter blob was verified equal to 279e, and separately ran the current worktree candidate.

The committed counter reports the expected baseline red state (7 open; strict receipt absent) and main closed state (0 open; strict-baseline named and substance true, open 6). The current worktree candidate gives the same 7 → 0 result. These are not false classifications for the actual target data.

I independently re-derived the strict-baseline result from immutable objects. At 279e, the retained receipt names `rev=9011581d84527ba34c675f9cf912e54d2e72d470`, exit 1, `tool_rev=a245bb00c581ae3423a10a055c77d4bc873918df`, and tool SHA-256 `b004c3ed76fd72aca7667e85d335c8296257e8b7e4891ef53113043950e72b03` (`.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json:14-20`). The immutable retained red stdout has `open_count: 6` (`.../9011581d8452.stdout.txt:292-295`). The paired `454dee6923750698cc36041236db13b52c6fcade` receipt is exit 0 and its output has `open_count: 0` (`454dee692375.receipt.json:14-20`; `454dee692375.stdout.txt:298-301`). Replaying the A18 tool blob directly reproduces both retained stdout hashes and empty-stderr hashes exactly.

## Commands and exit codes

`git rev-parse refs/heads/main` → `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (exit 0).

Committed counter, run with the 279e counter blob in the clone:

```text
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-substance-strictbaseline.lkeIJB --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
```

Result: `open_count=7`, `R18-STRICT-BASELINE` substance false because its receipt is absent; exit 1.

```text
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-substance-strictbaseline.lkeIJB --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
```

Result: `open_count=0`, strict-baseline substance true with open 6; exit 0. The clone's counter blob was `ae1651db86bf3c1262025f624b392c4851f4cb42`, identical to the 279e object.

The current worktree candidate (`routed-r18.py` hash `d7d7ec0be3233d4746dc78476c72ccbcd7a15b1a`) also returned baseline 7/exit 1 and main 0/exit 0 on the same pinned targets:

```text
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
```

Exit 1.

```text
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
```

Exit 0.

Independent replay from the A18 tool blob, extracted in the temporary clone (`git hash-object` `309eb25aee7ec564bfbe4a47086eeaa71f3156e5`; content SHA-256 matches the receipt):

```text
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-substance-strictbaseline.lkeIJB --rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict
```

Exit 1; stdout SHA-256 `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316`; stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

```text
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-substance-strictbaseline.lkeIJB --rev 454dee6923750698cc36041236db13b52c6fcade --strict
```

Exit 0; stdout SHA-256 `7873566c4c95374be4306b5d6461dd717eb7508c251b46c20d2d8070f5ab92d4`; stderr SHA-256 is the same empty-file hash above. These equal the immutable receipts' recorded hashes.

Counterfeit mutation command (current worktree counter; all mutation artifacts were in the mkdtemp clone):

```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-substance-strictbaseline.lkeIJB --rev ff25c678fd5ed39babf78b8f13911bd6da4c18d5 --strict
```

Result: total `open_count=0` and exit 0, despite the strict defect's counterfeit `open 1` output.

## Residual risk and verification gaps

- **Observation:** `routed-r18.py` itself notes at main `:191-192` (current worktree `:219-220`) that replay verifies the result, not the historical process's time/authenticity. Reproducible output does not prove the recorded timestamps or that the original process actually ran.
- **Observation:** the `lsp` device is not mounted (`No such tool: xd://lsp`), so no server status, references, definition, or diagnostics were available. Literal search was used only to locate correction anchors; semantic assessment above is from direct source and immutable-blob replay.
- No builds, broad suites, or installs were run; verification was limited to the requested counter, direct immutable-tool replays, and the isolated mutant.
