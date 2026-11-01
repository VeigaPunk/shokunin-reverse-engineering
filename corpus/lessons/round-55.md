# Round 55 — the carry-in repair round: four routed round-54 closure defects close, and the corrections ledger gains its mechanical pin

Lane kaidoku, round 55, fresh-start round, L1-inline on the Windows host (2026-11-01).
Round base `79421b757f36b2ddb776631ecfd57d42dc2f33e2` (the r54 spot-check commit);
declaration `23f746f3…`; operative freeze `622b8e38…` (first commit adding
`.ufo/waves/round-55/claims.json`; an unpinned first freeze attempt was reset before
landing, M55-3). No wave (no dispatch surface on this host; the kaidoku round-53 L0
question stays open and unanswered). Both claims are offline over committed bytes;
the executed instruments are the two new frozen round-55 tools and the R29 gate.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S255 | https://git-scm.com/docs/git-show — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-55/l1/s255/` (git-show.html `0a95cbcd8868054d851eedb192864798092c597592851989f5d1bb392730168a`) | "For plain blobs, it shows the plain contents." (DESCRIPTION, 8 words) | admit, tier A docs (the tool's own manual, consistent with S142's tiering of git-scm.com docs), mined: grounds the revision-pinned blob read both round-55 instruments perform — a digest or pin verdict is computed over the bytes at a named revision, never over a mutable worktree. It grounds a read discipline, not any REA surface; no git internals were modified. Used by `plans/round-55-claims.md`, `tools/round-55/corrections-pin.py`, this lesson. |
| R55 reject 1 | grounding the pin's read discipline in `git cat-file` documentation (fetched first: scratch `git-cat-file.html`) | reject — the instruments call `git show REV:path`, not cat-file; the manual of the command actually executed is the honest anchor, and the cat-file fetch is disclosed here as the rejected candidate | reject row |
| R55 reject 2 | silently dropping the unreproducible r54 digest value `b340ed2b48facca7` and printing only the new digest | reject — a filed receipt is never repaired by deletion; the value stays in the filed receipt and is superseded by a dated correction that transcribes the sweep which failed to reproduce it (`records/v6-digest-repro.txt`) | reject row |
| R55 reject 3 | writing the corrections-pin gate to hard-code `corpus/claim-freezes-corrections.tsv` only, with no `--ledger` argument | reject — the same law governs any append-only TSV the lane keeps; the general form is what let the gate demonstrate red on the historical v2-ledger edit, which is the strongest evidence the pin catches the real event class | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-55/l1/census-start.txt` (exit 0, 19 standing W04) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing controls | `.ufo/waves/round-55/l1/scores/c1-before.txt` (the four routed-r54 repairs absent at the base) and `scores/c2-before.txt` (no pin instrument, 0 registry rows, 0 capability rows) | both arms red at the base, committed at the freeze | measured pre-data; a do-nothing control cannot land receipts, corrections, instruments or rows |

Assimilation: none — `considerthese/` does not exist in this lane (measured at round
start); the shokuknow register is unreachable from this host; the report carries
`Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M55-1 | receipt-authoring (a digest without its extraction command) | `.ufo/waves/round-54/l1/scores/c2-after.txt:9` printed the 16-hex prefix `b340ed2b48facca7` with no command; the r54 closure could not reproduce it (spot-check §5 item 3) and this round's ~100-boundary battery (`records/v6-digest-repro.txt` transcribes the families: section boundaries, joiners, suffixes, normalizations, CRLF, combinations, worktree bytes, instrument-native parse/render) also failed to reproduce it; the generating scratch died with the r54 session | the round-54 non-author closure; re-captured by this round's sweep | a receipt that states a digest MUST transcribe the command that produced it, in the receipt itself, before landing (the lesson this rule generalizes is QUALITY row 76's discipline for commands). The value is superseded, not deleted: the extraction of record is `tools/round-55/v6-block-digest.py` (full digest `946e5359…d204bcc` at four revisions), and corrections 2 of the r54 lesson and the round-55 report carry the supersession |
| M55-2 | helper-mechanics (absolute Windows paths are not repo-relative) | the first declaration commit `29a7477b…` passed `C:/Users/…` absolute paths to `treecommit.py`; `os.path.join(repo, "C:/…")` yields the absolute path, so four files were hashed from disk but planted under a `C:` directory in the repo tree (tools blobs read empty through their intended paths); caught immediately at verification (`git ls-tree 29a7477b`, blob sha `e3b0c442…` = empty) | this round's L1, by the post-commit pin re-derivation | `treecommit.py` takes repo-relative forward-slash paths (its docstring says so; M54-4's "pass explicit file paths" was satisfied but with the wrong form); the commit was discarded with a compare-and-swap `git update-ref` back to the base and re-landed correctly as `23f746f3…` — the discarded sha is disclosed here and nowhere cited as evidence |
| M55-3 | freeze-mechanics (an instrument named in a frozen atom must be pinned) | the first freeze attempt named `tools/round-29/freeze-gate.py` in atom T2 without an instruments-map entry; the R29 gate pre-flight returned FLAGGED `INSTRUMENT_UNPINNED` for it (disclosures 29 of 30, missing [round-55]); the commit was local and unpushed and was reset before landing | the R29 gate itself (the pre-flight), before any repair data landed | the re-frozen container `622b8e38…` pins the gate (sha256 `25b54339…93eb2` — the same value SKILL's round29-freeze registry row records, making this the first claims file to pin it) and the pre-flight then reads round-55 CLEAN with all three instruments audited; rule: every path a frozen atom names is pinned or removed, checked by running the gate at the freeze rev BEFORE the ledger row lands |
| M55-4 | helper-pathspec (a wave receipt silently dropped from the freeze commit) | the freeze commit `622b8e38…` landed 12 of the 13 named paths: the tip-gate receipt `.ufo/waves/round-54/l1/scores/freeze-gate-tip-90f3a9b9.json` was passed as `.ufo/waves/round-55/l1/scores/…` (wrong round directory), and `treecommit.py` treats a path missing on disk as a removal no-op; caught by the after-arm `git cat-file -e` at the landing (fatal: exists on disk, but not in 765118a4) | this round's L1, by the after-arm content check | the receipt landed in the follow-up commit `e21be31a…` with this row; rule: after every helper commit, re-derive the landed path count (`git diff-tree -r --name-only`) against the intended list, and `git cat-file -e` every receipt the container text claims was committed |
| M55-5 | push-mechanics (an aborted local commit reached the remote) | the M55-2 declaration commit `29a7477b…` was created by a `treecommit.py` call that also carried `--push`; the push succeeded before the `C:` tree defect was caught by the post-commit verification, so origin/main carried the garbage commit and the local chain (rebased correctly to the true base) was no longer a fast-forward of it | this round's L1, when the close-commit push was rejected non-fast-forward against `29a7477b…` | never combine an unverified commit shape with a push in one helper call: commit, verify the tree (`git ls-tree` count and blob sizes), then push as a separate act; the recovery is a faithful replay of the round's commits onto the pushed base with every internal sha re-cited and the stray subtree removed by a content correction, never a force-push |

## Claim disposition (filled at the record commits)

C1 (calibration, the four routed-r54 closure repairs (a)-(d)): before 0/4 at the
base (`scores/c1-before.txt`), after 4/4 content-checked at the landing
(`scores/c1-after.txt`, committed with the record). C2 (depth, capability
acquisition — the corrections-ledger mechanical pin): before absent (0 instrument /
0 registry rows / 0 capability rows, `scores/c2-before.txt`), after selftest 11/11,
green demo clean, red demo exit 1 on line 29 `round-53`, registry row in SKILL,
capability row in SCORECARD (`scores/c2-after.txt`). Verdicts in SCORECARD's
round-55 section and LOG.

## Freeze

First commit adding the container `.ufo/waves/round-55/claims.json`:
`622b8e38ce675a911dd16b6f3fe8cb13247bb755`. No amendments; the unpinned first
attempt never landed (M55-3, reset before the ledger row existed). The frozen
instruments and pins: `tools/round-29/freeze-gate.py` `25b54339…93eb2`,
`tools/round-55/corrections-pin.py` `f71e6b21…d40a`,
`tools/round-55/v6-block-digest.py` `22785c1e…741c` — bytes unchanged from the
claims commit `23f746f3…`.

## Corrections (round 55, sha re-citation)

Appended after the push (nothing above is edited). The rebase builder (M55-6)
skipped its sha-substitution pass for this lesson, the claims container, the FREEZE
receipt, the ledger row and the SCORECARD record section, so the pushed bytes of
those files cite the orphaned first-chain shas (`23f746f3…`, `622b8e38…`,
`765118a4…`, `e21be31a…`, `25b5b256…` — objects that exist only in this host's
object store). Corrections of record for THIS file, by role:

- declaration: `c191d8df…` (was `23f746f3…`) — in the header, M55-3 and the Freeze
  section below;
- freeze: `1f9be6eb…` (was `622b8e38…`) — in the header, M55-4 and the Freeze section;
- landing: `fa4cd11…` (was `765118a4…`) — in M55-4;
- landing follow-up: `627a9c20…` (was `e21be31a…`) — in M55-4.

M55-6 (mined here, class receipt-authoring/tooling): the rebase helper's per-file
renderers applied the orphan-sha substitution to LOG, SOURCES, QUALITY, SKILL and
the r54 lesson but skipped it for five files; caught by the post-push citation
sweep (`git show <tip>:<file> | grep -c '<orphan sha>'` per touched file). Fix:
a substitution pass is verified by the SAME sweep that would catch its absence —
run the grep before committing, not after pushing.
