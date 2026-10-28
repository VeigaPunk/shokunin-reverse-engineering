# ScoutSources — exit-2 meaning, round 48

Axes: coverage (the four candidates that could ground a registry exit digit, not a web-wide sweep), depth (located quote, anchor, digest, and the installed module line), calibration (what that quote does not license).

No install. Read-only on the lane tree. `corpus/SOURCES.md` was not edited. Proposed ids are against the worktree census at 2026-10-28T18:51:43Z and are not reserved.

## What the registry claims

`plans/round-48-claims.md` clause 8 (R48-C1): each verdict map is three `N=meaning` segments, exit 0 a success class, exit 1 a not-met class, exit 2 an unevaluable class, the three distinct.

`tools/round-48/meanings.py` states `Exit codes: 0 met; 1 not met; 2 could-not-evaluate` (module docstring) and classifies segment 2 as unevaluable only if it matches `could-not-evaluate|unevaluable|could not evaluate|\busage\b|\berror\b|absent|unreadable|refus` (`meanings.py:60-61`, `236-238`).

The instrument-registry section binds that digit to argparse's usage failure in several cells. Two observed wordings:

- `SKILL.md:1712` `tools/round-41/c2-controls.py`: `2=argparse usage error, nothing evaluated`
- `SKILL.md:1715` `tools/round-41/gen-squashfs.py`: `2=argparse usage error (tree or out missing, or an invalid --endian or --comp choice)`

The same phrase appears on `SKILL.md:1716`, `:1724`, `:1729`, `:1736`, and `SKILL.md:1744` says `2=usage error from argparse`. Those cells are the claim this source can ground. Cells that say `2=could-not-evaluate` for a missing revision or `frozen_path_changed` are a lane convention, not an argparse rule.

## Question and census

Question: which primary text assigns exit status 2 to a usage failure, the meaning those registry cells put on digit 2?

Schema used (`CORPUS.md` Rules, eleven cells): id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by. A row is a claim only after the source is opened. `teaches` on a rejection starts `REJECTED:` and carries `flip:`. `mined` requires a `used-by` path that exists; this seat's admit row is `queued` because no round-48 lesson cites it. A census is structural (`SKILL.md` round-25 note; `SOURCES.md` S074): opening one URL does not verify another.

Worktree census of `corpus/SOURCES.md`, lane root, 2026-10-28T18:51:43Z, the frozen manual commands:

| check | exit | stdout |
|---|---|---|
| rows | 0 | 144 |
| malformed (`NF!=13`) | 0 | 0 |
| tier | 0 | `A=135 B=7 C=2` |
| status | 0 | `mined=138 rejected=6` |
| duplicate ids | 0 | empty |
| enum / tier-inflation | 0 | empty (`receipts/census-enum.out`) |

Last id is `S144`. Next unused ids are `S145` and `S146`. `sources-census.sh` `validate` / `census` were not run. Mined `used-by` existence was not re-run.

## Search log

2026-10-28 UTC. Where searched: the Python 3.14 library page, the Python 3.14 argparse HOWTO, POSIX.1-2017 `diff`, FreeBSD 14.3 `sysexits(3)`, plus the installed `argparse.py` as a same-family check of the library page. Identified 4, screened 4, included 1 (`S145`), excluded 3 (HOWTO and POSIX not given rows; `S146` is the kept rejection). Stop: the library page states status 2 for `ArgumentParser.error`, and the other three do not assign that integer to usage.

| candidate | opened | result |
|---|---|---|
| https://docs.python.org/3.14/library/argparse.html | 2026-10-28T18:50:00Z, HTTP 200, 330759 bytes, sha256 `896dc9a8dfd24109060f0453d899830e361040f536878aa9c727be221b4dd55b` | admit |
| https://docs.python.org/3.14/howto/argparse.html | 2026-10-28T18:50:00Z, HTTP 200, 108968 bytes, sha256 `67e89e55752831140bca3805d160f9e2d471bda43eb27f5d94da023c2a3ddac2` | excluded, no row. Rendered text has 0 hits for `status` and none for `status code` or `sys.exit`. Absence cannot ground a digit. |
| https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html | 2026-10-28T18:50:00Z, HTTP 200, 33988 bytes, sha256 `dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a` | excluded, no row. Issue 7, 2018 edition, EXIT STATUS: "0 No differences were found. 1 Differences were found. >1 An error occurred." (13 words). `>1` is not the integer 2. |
| https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3&manpath=FreeBSD+14.3-RELEASE | 2026-10-28T18:50:01Z, HTTP 200, 59131 bytes, sha256 `51978a07e38901d90aecd7639d4d3e3ecb0aefb99e7e6d7b3d62cfd8937da8f8` | reject row |

Installed check, not a fifth candidate: `/usr/lib/python3.14/argparse.py`, Python 3.14.8, 106825 bytes, sha256 `b9f0fa53be3d7c9c10a71a8eecc538a27c32fbe7abe337818d0d36e138bfc5c5`, `error()` at line 2785 calls `self.exit(2, ...)`. The docs page titles itself Python 3.14.10. The 3.14.8 rendered docs were not fetched separately. Unknown: whether that patchlevel's HTML differed. The installed `error()` agrees with the sentence below.

## Located quote (admit)

URL: https://docs.python.org/3.14/library/argparse.html#argparse.ArgumentParser.error
Access: 2026-10-28T18:50:00Z. Fragment: `receipts/quote-argparse-error.htmlfrag` (sha256 `e5f7232570756022015c1dfba2c194fd37a9e85ce88e33d11ea8e4c304347071`).

21-word quote, visible text of that definition:

> This method prints a usage message, including the message, to sys.stderr and terminates the program with a status code of 2.

## Located quote (reject)

URL: the FreeBSD 14.3-RELEASE `sysexits(3)` page above. Access: 2026-10-28T18:50:01Z. ERRORS.

13 words: "The successful exit is always indicated by a status of 0, or EX_OK."

14 words: "EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments"

The page also says this interface is deprecated. That is scope, not the flip. The flip is the integer.

## Rows

Both lines are `NF=13` (`awk` on `receipts/proposed-rows.md`, 2026-10-28, printed `1 13` and `2 13`). Enum on those two lines printed nothing.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S145 | Python 3.14 library reference, argparse — https://docs.python.org/3.14/library/argparse.html | docs | A | Status used when ArgumentParser.error rejects an argument list; not exit 1, not --help, and not the lane's could-not-evaluate vocabulary | Page title Python 3.14.10 documentation; fetched 2026-10-28T18:50:00Z, HTTP 200, 330759 bytes, sha256 896dc9a8dfd24109060f0453d899830e361040f536878aa9c727be221b4dd55b; anchor #argparse.ArgumentParser.error | An invalid argument list ends in ArgumentParser.error, which prints a usage message and exits 2, the unevaluable class those registry cells name on digit 2. Quote: "terminates the program with a status code of 2." | queued | 2026-10-28 | on-release | — |
| S146 | FreeBSD sysexits(3) manual, 14.3-RELEASE — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3&manpath=FreeBSD+14.3-RELEASE | docs | A | Candidate BSD convention for the registry digit 2 meaning incorrect usage; not a Python status and not a lane verdict | FreeBSD 14.3-RELEASE sysexits(3), fetched 2026-10-28T18:50:01Z, HTTP 200, 59131 bytes, sha256 51978a07e38901d90aecd7639d4d3e3ecb0aefb99e7e6d7b3d62cfd8937da8f8; section ERRORS, EX_USAGE | REJECTED: incorrect usage is defined as EX_USAGE 64, and the only success status on the page is 0, so the page never assigns 2 to usage or to could-not-evaluate; flip: a published sysexits, this page or the header it documents, that defines the integer 2 as incorrect usage or as could-not-evaluate. | rejected | 2026-10-28 | on-release | — |

Admit `S145`. Reject `S146`.

`S145` stays `queued` until a lesson's Gate cites it. Pointing `used-by` at a missing `corpus/lessons/round-48.md` would be the round-47 `E11`, not a mined row. Do not append `S145` into `## Paths` or the search log; the registry table ends at `S144`.

## What the admit does not say

- It does not assign exit 1 to not-met. Argparse's documented status for this failure is 2, and `exit()` defaults to 0. Status 1 is not given a predicate-false meaning on this page.
- It does not make the word `usage` mean status 2. On Python 3.14.8, 2026-10-28T18:52:00Z: `python3 -c 'import argparse; p=argparse.ArgumentParser(prog="p"); p.add_argument("x"); p.parse_args([])'` exited 2, stdout sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty), stderr sha256 `fbf43992be81d6faee26acbf7a11d6442c87b7c4a754eba3c55ac77c1619181f` (`usage: p [-h] x` / `p: error: the following arguments are required: x`). The same parser with `parse_args(["-h"])` exited 0, stdout sha256 `4207017980439cf1deb58add5bc6f8b9fdd99ed7705766963481011a05f44cf8`, and that stdout begins `usage: p [-h]`. Help is usage text at status 0. The status-2 path is `error()`, not `--help`.
- It does not ground the rest of the unevaluable regex (`absent`, `unreadable`, `could-not-evaluate`, `frozen_path_changed`). A cell may say `2=argparse usage error` and still be a local policy about which conditions call `error()`. The page grounds the status those cells name, not every condition the cell lists.
- POSIX `diff`'s `>1 An error occurred` is not a license to write `2=error` as if POSIX had assigned 2. `meanings.py` would accept the word `error` in a digit-2 cell; the POSIX sentence does not.

## Receipts

`.ufo/waves/round-48/w1/ScoutSources/receipts/`. Captures: `captures/argparse-314.body`, `argparse-howto.body`, `posix-diff.body`, `sysexits.body`, checked against `captures.sha256`. Probe stderr/stdout: `probe-bad.err`, `probe-help.out`. Module digest: `argparse-module.sha256`.

## IRC

After this report was filed, `C2Floor` sent the single token `DISALLOWED`. It named no clause, path, or row. The admit/reject above is unchanged. A reply to `agent://C2Floor` was not delivered: `C2Floor is not running`.

`ScribeLesson-2` (same day) proposed ADMIT argparse docs as grounding the whole `2=unevaluable` class, and REJECT OpenBSD `sysexits.3`, with digests `521adff647…` (argparse), `867b5a26…` (`sys.exit`, screened), `4cf3eb9d…` (sysexits). Those digests are not the captures in this report. Reconciliation sent back: keep the admit on `#argparse.ArgumentParser.error` and the 21-word status-2 sentence; do not extend it to the unevaluable class; the rejection I opened is FreeBSD 14.3 `sysexits(3)`, not OpenBSD, and I did not open their `sys.exit` page.

Later the same seat pinned that capture and numbered it S149, folding the FreeBSD page into the staged S146 note (`ScribeLesson/lesson.md` Gate). Checked against the worktree, not against that message alone. `corpus/SOURCES.md` already has S145 (SEP Popper) and S146 (man7 `sysexits.h.3.html`, HTTP 404). S147/S148 are only in `w1/ScribeSources.md`, not in the registry, so S149 is the argparse id only if those two land first; ids are not skipped. The staged S146 teaches cell has no flip. The flip is in `corpus/lessons/round-48.md`: open FreeBSD and quote `EX_USAGE`, "then the row can ground exit 2 as a usage refusal." The FreeBSD capture quotes `EX_USAGE (64)`. That is the observation the flip asked for, and it falsifies the predicted admit. It is not an in-place upgrade of S146 (source, anchor, and teaches stay put) and it is not evidence that the flip is satisfiable. The FreeBSD page is its own rejected row. `ScribeLesson/lesson.md` S149 still says the quote "grounds the registry's `2=unevaluable` class"; that sentence is the overclaim already refused. S150 in that draft is a pointer, not a row.

Re-read of `ScribeLesson/lesson.md` Gate after their correction pass: S149/S150 are marked provisional on S147/S148 landing; the registry S146 line is still the 404 row (teaches cell unchanged); S150 is a real FreeBSD reject with sha256 `51978a07…` and the 14-word `EX_USAGE (64)` quote; S149 is `queued` on the 3.14 URL and sha256 `896dc9a8…`. Two residuals remain in that draft: S149 still calls the quote a precedent for the unevaluable class's `usage` token, and S150's source cell also carries their OpenBSD capture.

Second re-read: those two residuals are gone. S149 names `--help` exiting 0 and does not ground the unevaluable class. S150's source cell is the FreeBSD URL only; OpenBSD sha256 `4cf3eb9d…` is in the search-log line under the table. One attribution remains: S150's decision says the FreeBSD page "self-describes as non-portable." The captured FreeBSD body says the interface "has been deprecated" and "Its use is discouraged." The words "non-portable" are only in the OpenBSD search-log quote.

Third re-read: that attribution is fixed. S150 now says usage is 64, not 2, and quotes the FreeBSD page that the interface "has been deprecated" and its use "is discouraged." "non-portable" stays only in the OpenBSD search-log line. No further correction on those two rows.

Their first closeout called the six-row Gate fully peer-verified by this seat. That covers S149 and S150 only, plus the observation that the registry S146 line was still the man7 404 when last read. S145, S147, and S148 were not opened here.

Their corrected closeout matches that limit: S145/S146 are the L1's staged rows, S147/S148 are ScribeSources-2's, and this seat's check is S149/S150 (pin, scope, attribution, flip falsification). Nothing further open on those two rows.
