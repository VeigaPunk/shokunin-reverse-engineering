# Record agreement: a record cell is a claim about bytes, and the claim is re-derived by command

source: S255 — https://git-scm.com/docs/git-show (git-show documentation). Re-opened 2026-11-04 by this lane in round 86: HTTP 200, 246736 bytes, sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa`. Located quote, DESCRIPTION: "For plain blobs, it shows the plain contents." (8 words).
verified-at: 2026-11-04 (round 86; BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`)
recheck: 180d

## Claim

`git show REV:path` on a blob shows that object's plain contents (S255, DESCRIPTION). A record that states a value about a committed object is therefore checkable only by reading the object at the revision the record names, never by reading the record's own words. The round-85 non-author spot-check found two such cells wrong while their words were present: S303's scope count ("five scopes") against eight rows that carry its URL, and the mutation counter's docstring, which called an absent declared case "inconclusive" while the code assigns `survived`.

## What the frozen counter re-derives

`tools/round-86/record-agreement.py` reads three record cells with `git show REV:path`:

- **A1** — the newest registry row whose `teaches` cell opens `supersedes S303` must state, after `count`, the number of other registry rows whose source cell carries the S303 URL, and must list exactly those ids.
- **A2** — the sentence of the `tools/round-84/mutation-closure.py` module docstring that names an absent declared case must name the status the code assigns in its `not case_present` branch, and no other status word.
- **A3** — the SCORECARD `| coverage |` row must name a revision-stamped receipt whose round is not older than the row's own round.

The counter's control, `--control substring-only`, accepts a record when it merely contains the token it is about. It accepts the BASE records, which is the evidence that the counter's target can fail.

## Measured outcome

The counter is run at a stated revision with the command in `plans/round-86-claims.md`. Its receipts are in `.ufo/waves/round-86/`. At BASE, zero of three atoms agree. A1 and A2 are repaired by one registry row and one docstring sentence. A3 cannot be met by a record edit under its frozen rule, because the SCORECARD carries 23 `| coverage |` rows and the rule requires exactly one. That is reported in the round-86 lesson as a misspecified atom, not relaxed.

## Limits

The atoms are three finite record checks, not an audit of the whole card. The counter does not inspect fenced code blocks, and a split sentence can hide a second status. A receipt's `rev` is shape-checked only. The knowledge entry does not claim that any value outside these three cells is correct.
