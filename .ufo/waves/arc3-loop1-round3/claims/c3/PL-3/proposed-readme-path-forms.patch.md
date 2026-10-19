# proposed patch — custody-pair README path forms (seat PL-3, arc3-loop1-round3, chain c3)

Target: `.ufo/gates/custody-pair/README.md` (C2's file — **patch text only**; this seat does not
write it). Base revision quoted: HEAD `c07af80` (README sha256
`fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`); C2's in-progress worktree
revision (`f30df42e…` at 13:14Z) still carries both defects below verbatim — re-verify line numbers
before applying, since C2 edits this file in the same round.

## Defect 1 — README:129, non-resolving relative path (measured)

Measured cause: the README sits at `.ufo/gates/custody-pair/README.md`, so `../waves/…` resolves to
`.ufo/gates/waves/…` — `git cat-file -t HEAD:.ufo/gates/waves` → `fatal: path '.ufo/gates/waves'
does not exist in 'HEAD'`; `git show HEAD:../waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt`
→ exit 128. The cited directory does exist at `.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/`.

```diff
-`../waves/arc3-loop1-round2/claims/c3/EX-31/` holds the live pre/post pair
+`../../waves/arc3-loop1-round2/claims/c3/EX-31/` holds the live pre/post pair
```

## Defect 2 — README:103-105, receipt examples without their base

The three v1-shape examples are written relative to an implied `.ufo/waves/` base that the README
never states; as written they do not resolve from the README's own directory. Fix: name the
repo-relative paths (which is also the form the pointer table's anchors grade).

```diff
-| `stanza-v1` | `arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | sha256, size, mode, uid, gid |
-| `sums-v1` | `arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt` | sha256 |
-| `pipe-v1` | `arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt` | sha256, size, inode |
+| `stanza-v1` | `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | sha256, size, mode, uid, gid |
+| `sums-v1` | `.ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt` | sha256 |
+| `pipe-v1` | `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt` | sha256, size, inode |
```

Both edits are text-only and change no receipt, no path's custody status, and no exit class. If C2's
revision rewrites these blocks, apply the same *form* fix (repo-relative or `../../`-rooted) rather
than the literal line numbers.