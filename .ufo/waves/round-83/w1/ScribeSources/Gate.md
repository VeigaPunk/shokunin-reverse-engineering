# Round83 source Gate — ScribeSources

Axes: attribution accuracy, provenance auditability, scope fidelity, actionability, concision. Author-side findings only; no outside admission or new authority claimed.

## Access and decisions

Access date: 2026-11-04. Both live URLs opened successfully through functions.read (native HTML reader); no source-access failures. No HTTP status, raw-body digest or publisher authenticity measurement is inferred from reader success.

| decision | URL and located anchor | quote (each ≤25 words) | scoped reason and flip |
|---|---|---|---|
| Admit/reuse existing S255 | https://git-scm.com/docs/git-show#_description ; DESCRIPTION, plain-blobs paragraph | “For plain blobs, it shows the plain contents.” (8 whitespace words) | Grounds reading the named repository blob rather than the mutable working file. Does not define the lane's positive-attribution grammar or prove parser correctness. Flip: reject this usage if the purported evidence instead reads an unpinned working file or if no blob is named. |
| Reject usage, not the documentation | https://git-scm.com/docs/git-diff#_description ; `git diff --no-index` form | “This form is to compare the given two paths on the filesystem.” (13 whitespace words) | A filesystem comparison does not establish that positive attribution was read from a committed object. Flip: admit for an explicitly filesystem-difference claim; explicit two-revision diff semantics are a different scoped use. S261 already holds this document for numstat: do not add a new id. |

Search accounting: two known primary URLs identified, opened and screened; one existing source reused, one use rejected; zero new registry rows. Stop: these two paragraphs locate the requested distinction. Registry row-count census was not executed by this seat; L1 owns integrated census and final measurement.

## Exact read provenance

- functions.read https://git-scm.com/docs/git-show returned the plain-blobs sentence in DESCRIPTION (reader output artifact://107802).
- functions.read https://git-scm.com/docs/git-diff returned the filesystem sentence in DESCRIPTION, `--no-index` form (reader output artifact://107803).
- Command actually executed, exit 0: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 650344bc37ca303fb9487c1174192057af499b9b:corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md`. Its first line positively names S286 before the em dash and says `duplicate S299 withdrawn in-round` afterward. No probe or parser was executed by this seat.
- Existing `.ufo/waves/round-83/pre/legacy.json` was read, not rerun: eight cases, two real, mismatch_count 3, including real-withdrawn expected false / observed true. Its recorded entry revision is the same base; recorded entry SHA256 c14b43393b85cc64275f06c00a9195fd03d0e54c4e78c01f897649096b5089ee is receipt evidence, not a fresh hash measurement here.
