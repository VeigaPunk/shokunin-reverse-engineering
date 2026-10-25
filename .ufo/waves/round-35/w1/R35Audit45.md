# R35Audit45 — wave one, item: verify source capture dates

Seat: R35Audit45 (mutation tester, leaf member — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Writes: this report only; all probe work in private `/tmp/r35audit45-dates/` (plain files, no git init, no VCS/index/jj state touched). Lane read-only throughout.

## Verified capture-date evidence (all read-only)

**Capture commit** `d2729cba895b8664f3ccb27196091494f3cda83b` ("round-35: instruments-first prep — … jsc2js source captures"):
- author date `2026-10-25T05:08:51-03:00`, committer date `2026-10-25T16:05:46-03:00`.
- `git ls-tree -r --name-only d2729cba — .ufo/waves/round-35/prep/jsc-sources` → exactly `jsc2js-readme.md`, `releases-page1.json`, `releases-page7.json`.

**Freeze ordering** — `git merge-base --is-ancestor d2729cba 131eacfa` → `ANCESTOR_OK`;
`131eacfaf474d398fde974a86d5a30acfb1ab1f6` = "round-35: freeze claims C1/C2", committer `2026-10-25T16:05:56-03:00` (10 s after capture commit). Capture commit is also an ancestor of HEAD `3ecf42981a0b63414de90ade643040d609dbb8a5` (16:13:53, "commit failing do-nothing controls before claim data"). Timeline: base `aa04633a` → captures `d2729cba` (16:05:46) → freeze `131eacfa` (16:05:56) → data line (first `13d7a815` 16:07:04) → canonicalize `2323d197` → controls `3ecf4298`. Holds in both author and committer clocks → **"captured in prep before the freeze" verified**.

**Blob identity (committed vs worktree, sha256)** — byte-identical:
- `jsc2js-readme.md` `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`
- `releases-page1.json` `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c`
- `releases-page7.json` `499e2b227a6eb2c3053a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc`

**Capture content dates** — `releases-page1.json` (xqy2006/jsc2js GitHub API): `published_at` range `2026-08-14T13:12:04Z` … `2026-10-21T08:33:45Z`; `releases-page7.json`: `2025-08-24T03:19:17Z` … `2025-08-25T13:30:20Z`. All ≤ declared capture date 2026-10-25. README capture makes no date claims.

**SOURCES rows** — S125/S129 absent at HEAD and in all local history (`git log --all -S S125 -- corpus/SOURCES.md` → empty): C1 data not yet landed at verification time. Frozen instrument binds dates only via `c1-coverage-counter.py` check body: `cells[7].startswith("2026-10-25")` on the SOURCES `opened` cell — consistent with the verified capture date.

## Mutation probe (one plausible defect)

- **Invariant challenged:** sources were captured on 2026-10-25 in prep before the freeze; plausible defect: capture content postdating the declared capture date (date-drift/fabrication).
- **Detector** `/tmp/r35audit45-dates/dates_check.py` (bounded): I0 blob provenance vs committed sha256 (warn-only), I1 capture-commit ancestry of freeze, I2 capture clocks on 2026-10-25 and ≤ freeze clock, I3 every `published_at` ≤ 2026-10-25.
- **Mutant (scratch copy only):** `releases-page1.json` line 38 `published_at` `2026-10-21T08:33:45Z` → `2026-10-26T08:33:45Z` (one byte; release id 419322632).
- **Pristine:** `DATES_CLEAN capture=2026-10-25 before freeze=2026-10-25T16:05:56-03:00`, exit 0, no warnings.
- **Mutated:** `WARN: blob_differs_from_committed_capture:releases-page1.json` + `DATES_FAIL: capture_postdates_declared_date:releases-page1.json:id=419322632:published_at=2026-10-26T08:33:45Z`, exit 1 → **KILLED** on the date invariant (I3), not merely the blob check.
- **Restored:** `cp pristine/releases-page1.json releases-page1.json`; sha256 back to `4a5199dd…`; `cmp` → `BYTE_IDENTICAL_RESTORED`; detector exit 0 clean.

## Advisory notes (coverage findings, not contract changes)

1. The frozen C1 instrument never inspects `.ufo/waves/round-35/prep/jsc-sources/` — the "captured before freeze" assertion is plan-level and was verified here by commit history, not by the counter. A capture-postdating mutant would not be caught by the frozen instrument alone; my probe covers that gap manually.
2. Scoring caveat: the counter reads `.ufo/waves/round-35/claims-canonical.json` at `--freeze`, but the canonical file is first present at `2323d197` (16:13:40); the first commit adding `claims.json` is `131eacfa` (16:05:56), whose tree has only `claims.json`. `--freeze 131eacfa` yields counter exit 2 (unevaluable); scoring must pass a freeze rev ≥ `2323d197`.

## Limits

Did not run the frozen counters (not my item; read-only git + file reads only). Did not fetch anything; content dates come from committed capture bytes. Worktree capture mtimes (Oct 25 15:59) are checkout artifacts, not evidence — commit/blob identity is the binding evidence.
