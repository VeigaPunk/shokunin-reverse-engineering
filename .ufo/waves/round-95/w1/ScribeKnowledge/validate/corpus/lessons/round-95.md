# Round 95 — lesson (stand-in draft from seat ScribeKnowledge)

## Motive

Round 94 closed with its calibration claim verified on a predicate that was narrower
than its natural reading. The round-94 agreement counter
`tools/round-94/c1-receipt-agreement.py` checks only receipt↔stdout↔rc agreement and
the predicted met/exit per run name, so a receipt pair whose `label` is rewritten
consistently in both files, and a wholly fabricated triple, both pass it (M94-e, found
by the round-94 critic, recorded at `.ufo/waves/round-94/w1/CriticC1.md`). The base
receipts carried a short `--rev` that nothing validated against `git rev-parse`
(M94-f). And the round-94 writer's temp file was the predictable name
`<json-out>.tmp`, so a symlink pre-planted at that name was followed and the write
landed on the link's target (SentinelWrite F1).

Round 95 therefore claims calibration as *the receipt is bound to the world it claims*:
the frozen label, the receipt's own counts, the measured tree and the pinned bytes.
The candidate instruments are `tools/round-95/stop-boundary-repair-battery-v5.py`
(mkstemp temp name, fsync, receipt self-verification, fail-closed exit),
`tools/round-95/c1-agreement-v2.py` (four typed bindings),
`tools/round-95/c1-forgery-refusal.py` (the frozen counting command over the four
committed forgeries) and `tools/round-95/symlink-probe.py` (the public-path
write-escape probe). The parallel depth claim R95-C2 lands craft block 34, a decision
table for the receipt-world-binding failure class, with criteria QUALITY 191 and 192
carrying the frozen keyword atoms of `.ufo/waves/round-95/manifests/block34-after.json`,
and a junk manifest (`.ufo/waves/round-95/manifests/block34-junk.json`) as the
rubber-stamp control that must exit 1.

The round's sourced step is the `open(2)` man page: the `O_NOFOLLOW` rule is what
separates a refused trailing symlink from a followed one, and it is the reason a
predictable temp name is an escape path while a unique name created fresh in the same
directory is not.

---

## Gate

Sources opened this round (CORPUS.md rule 1). Access date 2026-11-05 for each.

| row | URL | access date | HTTP / bytes / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S320 (new) | https://man7.org/linux/man-pages/man2/open.2.html | 2026-11-05 (opened this round) | 200 / 76506 / `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | `If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP` (the `O_NOFOLLOW` description, Linux man-pages 6.19) | the documented refusal of a trailing symlink under `O_NOFOLLOW`, which grounds why a predictable `<json-out>.tmp` is a write-escape path and why `mkstemp` (unique name, `O_EXCL`, same directory) removes it |

Anchor notes on S320. The quote is **not** a raw contiguous byte substring of the
fetched HTML: in the raw file the sentence is broken across lines and carries `<i>` and
`<b>` markup —

```
       <b>O_NOFOLLOW</b>
              If the trailing component (i.e., basename) of <i>path</i> is a
              symbolic link, then the open fails, with the error <b>ELOOP</b>.
```

— so it is exact only after tag-stripping, HTML entity decoding and whitespace
normalisation. The `O_NOFOLLOW` flag appears five times on the page (the
file-creation-flag list; the flag description; twice inside the `O_PATH` discussion;
once in the `ERRORS` list); only the second carries the quoted rule. The page footer
reads `Linux man-pages 6.19            2026-02-08` and the provenance block reads
"This page was obtained from the tarball man-pages-6.19.tar.gz", which is the
"man-pages 6.19" the anchor names.

Two byte-identical fetches are committed at
`.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html` and
`.ufo/waves/round-95/l1/scores/s320-open2-fetch2.html` (each 76506 bytes, each
sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`). The live
re-fetch by this seat returned HTTP 200 and 76506 bytes with the same sha256.

Row changes (CORPUS.md rule 2, old → new, logged here):

- S320 appended (`mined`, opened 2026-11-05, recheck `on-release`, used-by
  `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`,
  `corpus/lessons/round-95.md`). No other registry row is edited this round.

Admit / reject. Admitted this round: **S320 only** — the `O_NOFOLLOW` description of
`open(2)`, one located quote, tier A because the scope (the documented refusal of a
trailing symlink) is exactly what the man page is the authority for. Rejected from the
same page, each with its reason:

- the `O_PATH` paragraphs ("When `O_PATH` is specified in `flags`, flag bits other than
  `O_CLOEXEC`, `O_DIRECTORY`, and `O_NOFOLLOW` are ignored" and "If `path` is a
  symbolic link and the `O_NOFOLLOW` flag is also specified, then the call returns a
  file descriptor referring to the symbolic link") — **not admitted, because they describe
  the `O_PATH` override of `O_NOFOLLOW`, a flag the round's writer never opens with**;
  the round's proposition is the plain `O_NOFOLLOW` refusal.
- the parenthetical caveat inside the `O_NOFOLLOW` entry ("the `ELOOP` error that can
  occur in this case is indistinguishable from the case where an open fails because
  there are too many symbolic links found while resolving components in the path
  prefix") — **not admitted, because the round does not claim to distinguish the two
  `ELOOP` causes**; the named limit is that the strengthened bindings bind the receipt
  to the world it claims and do not authenticate provenance.
- the `ERRORS` list's general `ELOOP` entry ("Too many symbolic links were encountered
  in resolving `path`") — **not admitted as a separate row, because the quoted rule is
  already carried by the `O_NOFOLLOW` description**; a second row for the same page and
  the same sentence would duplicate the scope rather than widen it.
- the `O_TMPFILE` notes and the `creat(2)`/`openat(2)` cross-references — **not
  admitted, because they concern other flags and other calls**; nothing in round 95
  claims `O_TMPFILE` behaviour or a `creat`/`openat` path.

Assimilation: `merge/kaidoku/` is absent and the lane has no `considerthese/`
directory, so `Assimilation: none`.

---

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

> **Drafting note.** The round-95 mistake rows below are the ones this seat can trace
> to committed bytes: the three round-94 defects that round 95 carries and closes
> (M94-e, M94-f, SentinelWrite F1), plus the one erratum this seat found while
> drafting the Gate. The L1 supplies any further round-95 mistakes its own wave seats
> found (the wave's critic, mutation-tester, sentinel and reviewer seats report under
> `.ufo/waves/round-95/w1/`); those rows are appended here by the L1 with the same
> class · evidence pointer · captured-by · fix shape. Nothing in this draft asserts a
> mistake that no committed receipt or file supports.

- **M94-e · the frozen agreement counter is narrower than its natural reading
  (round-94, carried and closed by R95-C1).** The round-94 counter
  `tools/round-94/c1-receipt-agreement.py` validates receipt↔stdout↔rc agreement and
  the predicted met/exit per run name; a receipt pair whose `label` is rewritten
  consistently in both files, or a wholly fabricated triple, passes it. Evidence:
  `.ufo/waves/round-94/w1/CriticC1.md` and `w1/CriticC1/fixtures/` (cases H, J, K exit
  0); the committed before-receipt
  `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json` prints `valid 4`,
  `agree 4`, `predicted 4`, `met true`, exit 0 over the four committed forgeries.
  Captured-by: `none` — no counter scores the counter. Fix: the round-95 instrument
  `tools/round-95/c1-agreement-v2.py` adds the four typed bindings (`label-not-frozen`,
  `label-not-recomputed`, `revision-not-bound`, `pins-not-bound`), and
  `.ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
  shows each committed forgery refused with exactly its intended single reason
  (`forgeries refused 4 of 4; before admits True; honest accepted True`).

- **M94-f · the base receipts carried a short `--rev` that nothing validated (round-94,
  carried and closed by R95-C1).** The round-94 base runs were invoked with a short
  revision while the claims' `before.revision` names the full hash, and no instrument
  resolved `--rev` against `git rev-parse`. Evidence: the `revision` fields of
  `.ufo/waves/round-94/pre/c1-base-v3-*.json`; the committed forgery fixture
  `.ufo/waves/round-95/forgery/forge-F2.*` carries the 9-char short revision of the
  same shape and is refused with `revision-not-bound`. Captured-by: `none` — nothing
  validated `--rev` against `git rev-parse`. Fix: the round-95 binding
  `revision-not-bound` requires the receipt's `revision` to equal the full 40-hex
  resolution of `--rev` (`tools/round-95/c1-agreement-v2.py`, `_resolve_rev`), and the
  writer's own self-verification fails closed on the same mismatch
  (`tools/round-95/stop-boundary-repair-battery-v5.py`, `verify_receipt`).

- **SentinelWrite F1 · the v4 writer's predictable `<json-out>.tmp` name is a
  write-escape path (round-94 sentinel finding, carried and closed by R95-C1).** A
  symlink pre-planted at the predictable temp name is followed by the writer, so the
  write lands on the link's target. The `open(2)` `O_NOFOLLOW` description
  (`https://man7.org/linux/man-pages/man2/open.2.html`, S320) states the documented
  shape: a trailing symlink makes the open fail with `ELOOP`, while earlier path
  components are still followed — so the protection must be applied to the exact file
  being created. Evidence: `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`
  (`victim_intact false`, `verdict "followed-symlink"`, `receipt_valid true`) beside
  `.ufo/waves/round-95/l1/scores/c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
  (`victim_intact true`, `receipt_valid true`, `verdict "hardened"`, `tmp_is_symlink
  true`, `tmp_left true`). Captured-by: `none` — the round-94 frozen bytes are
  immutable, so the finding was routed, not fixed in place. Fix: the round-95 writer
  `tools/round-95/stop-boundary-repair-battery-v5.py` creates its temp file through
  `tempfile.mkstemp` (a unique name, `O_EXCL` semantics, in the receipt's own
  directory) and `os.replace`s it onto the target path only after `flush()` and
  `fsync()`.

- **M95-a (landing requirement, not yet a defect) · the `S320` row's `used-by` names
  two files that do not exist at the declaration commit.** The row's `used-by` cell
  names `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` and
  `corpus/lessons/round-95.md`, neither of which exists at
  `4bda1d1dd3788973f10e61212b70df18b3b14ea0`. Evidence: the census's `E11`
  (dangling used-by) code against a registry that carries the row before its two
  consumers land; this seat reproduced both arms in its own scratch clone
  (`.ufo/waves/round-95/w1/ScribeKnowledge/verify.md`): run A (the row with neither
  consumer present) raises the two expected `E11` findings, run B (the row with both
  consumers present) exits 0 with no finding against S320. Captured-by: the census
  (`scripts/sources-census.sh validate`, code `E11`) — the only instrument in the lane
  that notices, and it fires only if the row is landed before its consumers. Fix: the
  L1 lands the knowledge file and the lesson file in the same commit as the row.

> **Placeholder for the L1-supplied round-95 mistakes.** The wave's other seats
> (critic, mutation-tester, sentinel, reviewer, executor) report their findings under
> `.ufo/waves/round-95/w1/`; the L1 appends those rows here in the same
> class · evidence pointer · captured-by · fix shape. This draft asserts no round-95
> mistake that no committed receipt or file supports.
