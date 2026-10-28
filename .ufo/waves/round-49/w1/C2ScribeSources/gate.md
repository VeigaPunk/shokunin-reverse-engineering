## Gate

Sources re-opened this round (2026-10-28, UTC; HTTP status, byte count and sha256 are the
re-open instant's; each snapshot is byte-identical to its re-open, see the receipts).

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S147 | https://plato.stanford.edu/entries/popper/ (SEP, *Karl Popper*, substantive revision Fri Jul 31, 2026; heading above the quotes `2. Backdrop to Popper’s Thought`; sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`, snapshot `corpus/evidence/round-49/c2/popper.html`) | 2026-10-28T21:09Z, HTTP 200, 118,135 bytes | "if a theory is incompatible with possible empirical observations it is scientific; conversely, a theory which is compatible with all such observations" (22 words); "it is consistent with all possible observations, is unscientific" (9 words) | **admit** (tier A, `mined`). Supersedes S145: the same page and clauses, with the locator corrected from §3 to §2 `Backdrop to Popper’s Thought`; the second quote carries the consequential clause ("is unscientific") that the first, at the 25-word limit, cannot. Province check: it grounds the lane's instrument discipline (a clause that cannot fail is not a check), not any RE surface; cited by this lesson only. |
| S148 | https://man7.org/linux/man-pages/man3/sysexits.h.3head.html (sysexits(3head), Linux man-pages 6.19, 2025-09-21; `SYNOPSIS`; snapshot `corpus/evidence/round-49/c2/sysexits.html`, sha256 `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340`) | 2026-10-28T21:09Z, HTTP 200, 12,725 bytes | "#define EX_USAGE 64 /* command line usage error */" (9 words) | **admit** (tier A, `mined`). Supersedes S146: the reachable sibling of the URL S146 recorded as 404. `EX_USAGE` is 64 in this header; the lane's 0/1/2 exit meanings are its own convention and no sysexits value grounds exit 2. The tier is A because the page reproduces the header's own `#define` lines; the lane's convention claim is not taken from it. |
| S149 (candidate, not a registry row unless L1 adds it) | https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 (FreeBSD sysexits(3)) | 2026-10-28T21:09Z, HTTP 200, 59,251 bytes, sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` | "EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, a bad syntax in a parameter" (23 words) | **reject** (`rejected`). REJECTED: a second mirror of the value S148 already carries (EX_USAGE 64), with no meaning for the lane's exit 2, so it adds no claim S148 cannot carry. Flip: a claim whose verdict depends on an independent archive of the header rather than one mirror; then this row is admitted as `mined`. |

S145 and S146 are left untouched. Both lines are byte-identical to the round-49 base, which the
freeze counter requires (A6 and A7 read them as the superseded rows); the corrections are the
new rows above, not edits in place.

### Round-48 closure disagreements, recorded

The closure (`corpus/lessons/round-48-verifier-spotcheck.md`, "Discernment spot-check") disagreed
with two annotations of the round-48 curation. Both are recorded here with their disposition:

1. **S145 locator: disagree; corrected by S147.** The row named `2. The Problem of Demarcation`.
   Re-derived from the snapshot with the counter's own normalization: the quote sits after the
   heading `2. Backdrop to Popper’s Thought` and before the heading `3. The Problem of
   Demarcation`, so the clause is under §2. The decision (admit) stands.
2. **S146 rationale and flip: disagree; corrected by S148, and the S146 shape is not repaired in
   place.** The round-48 row said "no locator exists to quote" and its flip named `man 3 sysexits`
   locally or the FreeBSD handbook page. The reachable sibling `sysexits.h.3head.html` (HTTP 200)
   carries `EX_USAGE` 64, and the FreeBSD mirror agrees (S149 candidate). S146's `teaches` still does not open with the
   `REJECTED: <reason>; flip: <what would change the verdict>` form the closure asked for; that
   line is frozen byte-identical by the counter, so the defect is recorded open rather than
   edited. The reject decision (S146, `rejected`) is reconfirmed at decision level: the URL as
   written still returns 404 on 2026-10-28 (196-byte body, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`).

### Candidate rejected this round

S149 (FreeBSD sysexits(3), above) is rejected: it duplicates the value S148 already cites from a
second mirror, and it names no meaning for the lane's exit 2. Flip: a claim whose verdict needs an
independent archive of the header. Whether S149 is a registry row is an L1 decision: if it is
added as `rejected`, the search log's excluded count for round 49 includes it (A8 derives
excluded from new rejected rows); if it is not, the search log must not count it as excluded.
