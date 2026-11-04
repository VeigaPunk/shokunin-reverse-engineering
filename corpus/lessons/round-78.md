# Round 78 — the instruments' attack classes are enumerated and refused, and the record's surface values are re-derived from live bytes

Base: `6205ec8c575fb070243c0c40e34a2b0daacde46a`.
Declaration: `3e6b1efcad3a743913baa09f46427e5f8877a62b`.
Freeze: `ffcb47d13f0340f88397af6c8d2707a9554abab3`.
Contract: `plans/round-78-claims.md` and `.ufo/waves/round-78/claims.json`.
Axes: calibration (R78-C1, the frozen instruments' ten accepted attack classes refused) and
freshness (R78-C2, eight surface values re-derived from the live objects the record names).

## Gate

Every source below was opened this round with one GET each; snapshots, byte counts and sha256s are
in `.ufo/waves/round-78/l1/sources/`. Quotes are literal contiguous excerpts with their snapshot
line.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S292, Python `stdtypes` Numeric Types, admit (mined) | https://docs.python.org/3/library/stdtypes.html | 2026-11-04 (HTTP 200, 814 496 B, sha256 `16f072e1…`) | "In addition, Booleans are a subtype of integers" (8 words; Numeric Types, snapshot line 441) | `isinstance(x, int)` accepts `True`, so every integer field in a receipt contract must exclude bool explicitly. The row grounds that guard in `check_receipt_like`/`check_receipt`, not the receipt schema (S289 holds JSON's taxonomy). |
| S293, Python `tomllib`, admit (mined) | https://docs.python.org/3/library/tomllib.html | 2026-11-04 (HTTP 200, 34 923 B, sha256 `d98e62f7…`) | "This module provides an interface for parsing TOML 1.1.0 … This module does not support writing TOML." (17 words; module introduction, snapshot line 221) | The Kimi pin is parsed from `mcp_servers.rea.args`, not grepped; a parse failure is an `unparsed` id, never a pass, and the file is never written. |
| S294, GnuPG handbook, Digital signatures, reject | https://www.gnupg.org/gph/en/manual.html | 2026-11-04 (HTTP 200, 113 892 B, sha256 `6d8e63bd…`) | "A signature is created using the private key of the signer" (11 words; Digital signatures, snapshot line 1017) | REJECTED as the authority for signed receipts: a signature authenticates possession of a private key, not the receipt's field contents; the lane holds no key and records no signer. Flip: an operator-owned signing key exists and the lane records its fingerprint and a verification command. |

**Refused reuse (not a row).** `https://docs.python.org/3/library/re.html` was opened for the
grammar question and refused registration: S143 already holds that URL
(`.ufo/waves/round-78/l1/pre-append-url-check.txt` → line 149), and a second row would duplicate
it. `hashlib.html` was likewise already S263 (line 180). The pre-append grep is the fix recorded
under `## Mistakes` M78-1; both snapshots were removed rather than registered.

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
start: exit 0, 197 rows, 23 W04 warnings (`l1/census-start.txt`). At round end: exit 0, 200 rows
(`l1/census-end.txt`), same 23 W04 warnings and none added. Three rows enter (S292 mined, S293
mined, S294 rejected); no existing row's `status`/`recheck`/`used-by` changed.

**Word-count correction (same round, in place).** S294's anchor cell first said 12 words; the quote is 11 (`A signature is created using the private key of the signer`). Corrected here and in the row; the row's other values are unchanged.

**Spot-check (non-author).** The round's outside discernment check is the non-author closure's
document (filed by the closure session, not by this lane); this lesson records the sample it should
re-open (S292 and S293 admits, the S294 reject).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **duplicate-url row** — a source already held as S143 (`re` docs) and S263 (`hashlib` docs) was about to enter the registry a second time; the census reports it as W04 only (a warning, exit 0), so the append would have passed the gate with a duplicate URL in the registry. | `.ufo/waves/round-78/l1/pre-append-url-check.txt`: `grep -nE 'library/(re|hashlib|stdtypes|tomllib)\.html' corpus/SOURCES.md` → lines 149 (S143) and 180 (S263) before the append; the first append of S294 carried the `re` URL and the census printed `S294 duplicate url docs.python.org/3/library/re.html` | CORPUS.md rule 2 (append-only, no duplicate URL) plus a pre-append URL grep — the census W04 is not a pass | the row was replaced by a genuinely new source (S294 GnuPG handbook) and the two snapshots deleted; the grep is committed as the fix, and it fails on the pre-fix registry (lines 149/180) and passes after (no re/hashlib row added) |
| **prose-only mistake** (routed from the round-77 closure, §6 item 3) — two mistakes were recorded as prose paragraphs, so no prevention was recorded for either; CORPUS.md wants one row per mistake with class, evidence, captured-by and fix. | `corpus/lessons/round-77.md` `## Mistakes` (one table row, two prose paragraphs: "fixture for the wrong reason", "a control that cannot fail") | CORPUS.md `## Mistakes` contract (class · evidence · captured-by · fix) | both are now rows here: M78-3 (fixture for the wrong reason) and M78-4 (a control that cannot fail), with the round-78 fixtures/controls named as the fix |
| **fixture for the wrong reason** (carried from round 77) — a red fixture that is red because the code cannot see the field proves nothing about the comparison; the round-78 gate's first `a5` fixture was red for the base instrument because its atom table was absent, not because the nested value differed. | `.ufo/waves/round-78/pre/c1-at-base.json` after the fix: `a5-nested-field` base `exit 0, mismatch_count 0` (bound 1) while the nested `forged_detected` is `false`; before the fix the same fixture scored base `exit 1, mismatch_count 0` from the missing `atoms` table | the gate's own `base_acceptance` arm (a fixture whose base arm is not accepted is not a live attack class) | the fixture receipt gained the atom table so the only reason it passes is the nested field; the base arm now records `accepted true` for all ten fixtures |
| **a computed status dropped** — `tools/round-77/verdict-bind.py` computes a clause status `defect` (e.g. `no_atoms`) and never appends it to the cell's defect list, so the clause is invisible to `mismatch_count` and the record scores green. | `tools/round-77/verdict-bind.py` `bind_cell` (the `status == "defect"` reason is returned in the clause, not collected); round-78 fixture `a6-dropped-defect` accepted at exit 0 (`pre/c1-at-base.json`) while the gate refuses it with `{"reason": "no_atoms"}` | round-78 rule `unbound_verdict` in `tools/round-78/attack-gate.py` (a parsable clause that binds nothing is a defect) and QUALITY row 136 | the rule refuses the shape; the fixture is committed and the base arm proves the round-77 instrument accepts it |
| **record value superseded in place** — `PROVINCE.md` held `openjdk version "21.0.12.1"` and "the live OMP file no longer records the disable"; both were true when written on 2026-10-20 and false on 2026-11-04, and nothing re-derived them. | `pre/c2-at-base.json`: `mismatches 2` — `jdk-version` (record 21.0.12.1, live 21.0.13) and `omp-rea-disable` (record false, live `disabledServers: ["rea"]`) | `tools/round-78/surface-recheck.py`'s declared patterns and typed comparison (QUALITY row 137) | both sentences corrected in `PROVINCE.md` with the 2026-11-04 recheck pointer; `c2-at-record.json` re-derives `mismatches 0` |

## Wave evidence (drafts landed by the L1)

- `ScribeLesson` drafted ten `## Mistakes` rows, one per attack class, at
  `.ufo/waves/round-78/w1/ScribeLesson/mistakes.md` (sha256 `bafe6782…`) plus QUALITY rows at
  `quality.md` (`d5bf8d79…`); the rows filed above are the L1's, and the draft is the per-class evidence
  the closure may re-open.
- `ScribeSources` independently reached the same three sources, the same two mined rows and the same
  withholding of `re.html` behind S143 (`.ufo/waves/round-78/w1/ScribeSources/gate-block.md`), and its
  quote re-measurement corrected S294's word count from 12 to 11.
- `ConnectorSibling` found a real gap in `receipt_auth`: `git show <rev>:<path>` returns link text for a
  mode-`120000` symlink and a tree pseudo-header for a mode-`040000` tree, so a receipt could authenticate
  a pin that is not instrument bytes. Closed in-round by `blob_mode` and the mode check (`1a99064b`), with
  four selftest cases.
- `ExecSurfaceProbe`'s independent re-derivation reports three mismatches where the instrument reports two:
  it compares `.bashrc`'s `$HOME/.local/opt/…` as a literal string, while the instrument expands `$HOME`
  and resolves both sides — the exact trap the C2 kill rule names. The two value drifts agree exactly.
- `ScoutRouted` independently found the `re.html` URL collision with S143 that M78-1 records, and
  reproduced the round-77 wave accounting (12 seats, 10 non-empty, 2 zero-byte).
