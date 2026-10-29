# C2ScorecardDraft — SOURCES correction-row drafts (B6, B7, B8)

Outside `SCORECARD.md`; routed to the L1's SOURCES landing. Append-only: S145–S149 stay byte-identical; each new row supersedes one. Registry columns: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by` (11 cells, as in `corpus/SOURCES.md` line 5). Snapshot offsets are character offsets in the tag-stripped, whitespace-collapsed text of the committed snapshot (receipt: `tools/round-50/c2-grammar-check.py` run and the inline checks in `C2ScorecardDraft.md`).

Verified at base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (snapshot bytes from `git show <base>:corpus/evidence/round-49/c2/<file>`, no network):

| check | result |
|---|---|
| `freebsd-sysexits.html` 59,251 B | quote `EX_USAGE (64) The command was used incorrectly` (7 words) at offset 11050; `ERRORS` heading at 10784 (before, and before the second `ERRORS` at 13621); `DESCRIPTION` at 10564 ends before `ERRORS` → locator is **`ERRORS`** |
| `popper.html` 118,135 B | 21-word quote `falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific` at 12284; `2. Backdrop to Popper’s Thought` heading at 8872; `3. The Problem of Demarcation` at 12986 → quote under **§2** |
| `popper.html` 9-word quote | `it is consistent with all possible observations, is unscientific` present at 12719 |
| CORPUS.md `tier` (line 93–96) | **A** = primary/authoritative (spec, official docs, source, original paper, maintainer statement, own gate output); **B** = strong secondary (expert write-up with reproducible detail, survey, textbook); **C** = lead only; `community` never A |
| S149 `teaches` / `status` (base) | `REJECTED: a second mirror of the value S148 already carries …` / `rejected` — kept |

## S150 — B6 (supersedes S149, reason and locator)

```
| S150 | sysexits(3) FreeBSD manual, origin of the header — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 (snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html`, sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`) | docs | C | supersedes S149 — the reason and the locator of S149: the quote sits under `ERRORS`, not `DESCRIPTION`, and FreeBSD is the origin of the sysexits header (man7, S148, is the Linux rendering), so S149 is not "a second mirror" of S148 | `ERRORS` heading (snapshot: quote after the `ERRORS` heading, before its second occurrence); "EX_USAGE (64) The command was used incorrectly" (7 words) verbatim | S149 stays `rejected`; this row carries no admitted claim; its only use is to correct the S149 reason and locator | rejected | 2026-10-28 | on-request | —
```

## S151 — B7 (supersedes S147, tier only)

```
| S151 | Stanford Encyclopedia of Philosophy, Karl Popper — https://plato.stanford.edu/entries/popper/ (snapshot `corpus/evidence/round-49/c2/popper.html`, sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`) | docs | B | supersedes S147 — the tier only: an expert survey is tier B under CORPUS.md `tier` (`strong secondary … survey`), not A (`primary or authoritative`); S147's locator, its two quotes and the admit stand | `2. Backdrop to Popper’s Thought` heading above both quotes (snapshot: quotes precede `3. The Problem of Demarcation`); "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words); "it is consistent with all possible observations, is unscientific" (9 words) | tier B: support for the scope `falsifiability as a demarcation criterion` only, never sole support for an admitted entry | mined | 2026-10-28 | 365d | corpus/lessons/round-49.md
```

## S152 — B8 (supersedes S138, `teaches` narrowed)

Attack on the plan's B8 wording: "a located quote that grounds the 22-member census" cannot exist. The census is a count over content-addressed member bytes, not a sentence on the tree page: `w1/C1S138Reopen.md` (round 49) records that the row URL's page does not contain a sentence that grounds the `teaches` clause (`regression dataset, not an independent producer`). The draft therefore narrows `teaches` to what a page quote can carry and grounds the census in the receipts. Check before use: `w1/C1S138Reopen.md` says the draft manifest sha256 `4bc53dbb…` is not the file (`06a72dd5…`); this draft cites no manifest digest.

```
| S152 | unblob 26.6.4 SquashFS expected member trees — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (member base https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/; commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`) | dataset | A | supersedes S138 — the `teaches` cell only: the 22-member census (4 endian trees) is a count over the LFS-pinned member bytes of the receipts `.ufo/waves/round-49/w1/C1S138Reopen/receipts/`, not a sentence of the tree page; "regression dataset, not an independent producer" is the lane's reading, not a quote | LFS pointer oids and the live media bytes (receipts), tag `26.6.4` commit `1fcc7a0a…`; no page quote grounds the census | the 22 committed oracle members match their LFS oids and the live media bytes (`C1S138Reopen`); sorted tree digest `21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca` (2026-10-28) | mined | 2026-10-28 | 180d | corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md
```

Open for the L1: the `status` vocabulary for a correction row (`rejected` is used here because S149 is kept rejected); the `A`/`B` choice for S152 is the S138 tier kept as is (`A`), which the round-49 closure called defensible; a reviewer may prefer `B` for a dataset that is the publisher's own regression oracle.
