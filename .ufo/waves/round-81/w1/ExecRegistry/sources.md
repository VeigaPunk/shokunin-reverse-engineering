# Scoped source decisions — round 81 ExecRegistry

Opened 2026-11-04. Two URLs opened, screened 2; admitted 1, rejected 1 for the stated claim. No SOURCE row created; existing URL identities reused.

## Admit: GFM table-cell escaping

URL: https://github.github.com/gfm/ (opened with #tables-extension-).
Existing URL rows S258 and S273 already duplicate this URL historically; reuse S258 for escaped-pipe semantics and S273 for positional-row context, never add a third row. Suggested used-by addition for the existing row: round-81 registry calibration; this advisory does not edit SOURCES.md.

Opened text: GitHub Flavored Markdown Spec 0.29-gfm, §4.10 Tables, example 200: “Include a pipe in a cell’s content by escaping it, including inside other inline spans”. Example `| b `\|` az |` renders a code span containing one literal pipe. Thus attack-gate's control alternatives remain a single purpose cell when authored `base-only\|all-refuse\|no-fixtures`; frozen split_cells unescapes them back to the original alternatives. Do not escape a structural delimiter just to bury write scope inside pinned.

## Reject: random names imply collision-free distinct work paths

URL: https://docs.python.org/3/library/tempfile.html (opened with #tempfile.mkdtemp).
Reuse existing S274/S276 URL identity and rejection; no new row. Not a source for this round's registry grammar.

Opened text says names “include a string of random characters”; mkdtemp says “There are no race conditions in the directory’s creation”, caller-only access, and returns the absolute pathname. Reason: randomness alone does not establish the stronger claim that independently selected path names never collide. Flip: explicit primary-source collision handling/retry or non-reuse semantics, scoped to successful creations, plus an appropriate bounded observation if making an operational distinctness claim. This rejection does not deny the documented race-free creation guarantee.

Assimilation: none. Source reuse is advisory for L1 integration; external state and source registry untouched.
