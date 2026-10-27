# R43SrcLicense — S135 row (unblob 26.6.4 LICENSE)

**Verdict: DONE — with one spec conflict.** The row greens the fleet census validator at exit 0 as
delivered (`kind` = `docs`); the seat spec's literal `kind` = `license` is **FALSIFIED** against
`scripts/sources-census.sh` (E05, exit 1). Both variants are delivered; the L1 decides which ships.
The L1's 2026-10-27T08:08Z capture is **CONFIRMED** byte-for-byte: HTTP 200, 1068 B,
sha256 `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`.

## 1. Fetch receipt (re-opened independently)

| field | value |
|---|---|
| command | `curl -sS -o LICENSE -w 'HTTP %{http_code} ...' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE` |
| HTTP status | **200** |
| access time (UTC) | **2026-10-27T08:17:52Z** |
| bytes | **1068** |
| sha256 | **`67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`** |
| local git blob sha1 | `81c6779148944d35164d0ea1dc396e9b332bc89f` |
| GitHub contents API (`?ref=26.6.4`) | HTTP 200; `name` LICENSE, `size` 1068, `sha` `81c6779148944d35164d0ea1dc396e9b332bc89f` |
| tag ref | `git ls-remote --tags … refs/tags/26.6.4` → `1fcc7a0a584a70a96c31f5a276c20944d199a089` (same commit S130 pins; lightweight tag) |

So the L1's `1068 B` / `67303bbd…` capture is confirmed, **not corrected**. Independent identity
beyond the raw endpoint's own digest: `git hash-object` of the fetched bytes equals the tag's tree
blob sha reported by the contents API — the bytes are the blob the tag actually points at, not merely
whatever that one GET returned.

Text (21 lines, LF, trailing newline): `MIT License` / `Copyright (c) 2022 ONEKEY GmbH` / the standard
MIT permission paragraph on lines 5–10 and the notice condition on lines 12–13.

Scope check behind the row's "covering" wording: the contents API for
`tests/integration/filesystem/squashfs?ref=26.6.4` lists 11 version subdirs
(`squashfs_v1 … squashfs_v4_le`) and **no** LICENSE-bearing name, so the repo-root LICENSE is the
covering text for the fixture bytes; no per-fixture licence carved out.

## 2. The row (recommended — `kind` = `docs`, validator exit **0**)

```
| S135 | unblob 26.6.4 LICENSE — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE | docs | A | the MIT license text covering the unblob 26.6.4 fixture bytes the round-42/43 C1 generators embed (fixtures.json pins; not the handler code, not extractor behaviour) | `LICENSE:5-8` "Permission is hereby granted, free of charge, to any person obtaining a copy ... to deal in the Software without restriction"; HTTP 200 at 2026-10-27T08:17:52Z, 1068 B, sha256 67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e | the fixture bytes may be committed and regenerated in the lane evidence tree | mined | 2026-10-27 | 180d | corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md |
```

Anchor discipline: 13 pipe-fields (NF=13, 11 columns); the quoted permission span is **20 words**
(≤ 25) and names its lines as `LICENSE:5-8`; the `...` marks the elided tail of line 6, so the quote
is an explicitly-marked splice of line 5 → line 8, not a contiguous quotation. No cell contains a
pipe, so no column drift.

## 3. Validator evidence (scratch, row inserted at line 141 after S134, inside `## Registry`)

Harness: base `SOURCES.md` from `git show 6b9e64fe…:corpus/SOURCES.md` + the row + a scratch root
whose `corpus/` mirrors the lane by symlink (so E11 resolves every pre-existing `used-by`), plus one
stub for the round-43 knowledge entry the lane has not written yet. `$S` below is that scratch root,
deleted at yield; each run's stdout is copied verbatim into this artifacts dir
(`val-docs.out`, `val-license.out`, `val-docs-nostub.out`, `overdue.out`) and those files, not the
scratch paths, are the evidence.

**`kind` = `docs`**

```
$ sources-census.sh validate --file "$S/w-docs/corpus/SOURCES.md"
file	ok	/fast/scratch/hyaku/kaidoku-r43/w1-R43SrcLicense/w-docs/corpus/SOURCES.md
EXIT=0
```

No `S135` line of any class appears (the 13 `W04` lines are the base registry's pre-existing duplicate
URLs, unchanged from the base run). Census mode: `rows 135` (base 134 + 1), `status.mined 130`,
`status.rejected 5`, `status.invalid 0`. Overdue mode: exit 0, S135 appears only as the informational
`cadence S135 recheck=180d opened=2026-10-27` line — not overdue.

**`kind` = `license` (as the seat spec worded it)**

```
$ sources-census.sh validate --file "$S/w-license/corpus/SOURCES.md"
file	E05	S135 kind=license
EXIT=1
```

## 4. Conflict for the L1, stated verbatim

Seat spec: `kind `license`` **and** "Run the row through the census validator … exit must be 0".
Validator (`scripts/sources-census.sh`, fleet repo, unmodifiable from this lane):

```
if (kind !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/)
  printf "%s\tE05\t%s kind=%s\n",lane,id,kind
```

`license` is not in the enum and **no** lane in the fleet has ever used it as a `kind` (fleet-wide scan
of `*/corpus/SOURCES.md`: zero rows with `| license |`). Control that the check is live and the row is
parsed: `kind` = `Z` on the same row → `E05 S135 kind=Z`, exit 1.

The two requirements are mutually unsatisfiable **in this round without a fleet-repo change**
(extending the enum), which is outside every lane seat's write bounds. Delivered resolution: `docs`
(the licence text is a document), which satisfies the hard gate (exit 0) and loses only the
"this is a licence" signal in the kind cell; the scope cell and anchor keep the licence meaning
explicit. If the L1 prefers `license`, the row is `row-S135-license.md` — but the census validate at
the freeze will exit 1, so do not ship it as-is.

## 5. Ordering constraint the L1 must plan around

`used-by` is checked on disk for every `mined` row (E11). The round-43 knowledge entry
`corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md` **is absent from the lane at
2026-10-27T08:15Z** (no `2026-10-27` file under `corpus/knowledge/`). With the row installed but that
file absent:

```
$ sources-census.sh validate --file "$S/w-docs/corpus/SOURCES.md"   # knowledge stub removed
file	E11	S135 missing used-by corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md
EXIT=1
```

So S135 must land **together with, or after,** the v4-scored knowledge entry — otherwise the round's
own census validate reds on the row the round just added. (Base `SOURCES.md` alone validates `ok` /
exit 0: the row is the only delta in these runs.)

**Disclosure — a bounds leak I caused and reversed.** My harness mirrored the lane's `corpus/` by
symlink, so the `touch` that stubbed that exact `used-by` path wrote an **empty placeholder into the
real lane** at `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md` (mtime 05:20 local /
08:20Z), i.e. inside `corpus/`, which my bounds forbid. I caught it on the final `git status` check,
confirmed the file was 0 bytes (so demonstrably mine, not a peer's draft), removed it, and re-checked:
`git status --porcelain` now shows only `.ufo/waves/round-43/…` entries, and `git diff --stat
6b9e64fe -- corpus tools plans SKILL.md LOG.md PROVINCE.md SCORECARD.md SHONEN.md` reports only
`plans/round-43-claims.md` (the L1's draft, not mine). No other lane path was written: the modified
`SOURCES.md` lives only in scratch, and every other mirror entry was a read-only symlink.

## 6. Fixtures clause grounding (why this row backs P43-C1)

`tools/round-42/fixtures.json` at the base (sha256 `9f957663c1f21940ec17e32f98485425145b6c4e7eb265a7b12327b629c3da9b`)
pins `"26.6.4"` and `https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/...`
for the carrier inputs — the same tag this LICENSE belongs to. The row therefore cites the licence of
exactly the tree whose fixture bytes the C1 generators embed. It does **not** license the unblob
handler code or any extractor behaviour, which is why the scope cell excludes both; the row also says
nothing about the round-42 carrier cache or the OpenWrt/DD-WRT/AVM published images (those keep their
own S131–S134 publisher rows and carry no licence basis from here).

## 7. Bounds compliance

- Wrote only: this report and `artifacts/R43SrcLicense/` (`row-S135-docs.md`, `row-S135-license.md`,
  `LICENSE.unblob-26.6.4.txt`, `fetch-receipt.txt`, `api-license.json`, `api-fixdir.json`,
  `val-docs.out`, `val-license.out`, `val-docs-nostub.out`, `overdue.out`). Largest file 11 007 B.
- Lane state at yield: no edit to `tools/`, `plans/`, `SKILL.md`, `LOG.md`, `PROVINCE.md`,
  `SCORECARD.md`, `SHONEN.md`; no VCS mutation; no fleet-repo or sibling-lane write. One transient
  violation of my own — an empty `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md` created by
  a harness `touch` through a `corpus/knowledge` symlink — was detected and removed (§5); `git diff
  --stat 6b9e64fe -- corpus` is empty at yield.
- Network: three read-only GETs (raw LICENSE, contents API ×2) and one `git ls-remote`. No extractor,
  no REA, no unblob, no firmware image. No `xd://` device calls.
- Tooling: **no installs, no upgrades** (curl 8.23.0, git 2.56.0, GNU Awk 5.4.1 already present).
- Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43SrcLicense` removed before yielding; every path
  cited above lives in the artifacts dir.

## 8. Limits

- The validate runs are scratch harnesses (symlinked corpus mirror + one stub for a not-yet-written
  knowledge entry), not a run on the live lane: they prove the row's field shape, id/url uniqueness
  and enum compliance, not the final tree state. The live tree will differ only if the knowledge
  entry lands under a different filename than the plan names. [INFERENCE]
- `180d` recheck puts S135 due 2027-04-25; MIT text is effectively static, so the cadence is a
  formality, not a real drift risk. [INFERENCE]
- The "no per-fixture LICENSE" check covers the eleven version subdirs' top level only (one contents
  listing); I did not walk every nested `__input__`/`__output__` directory for a stray licence file.
- Whether `docs` or a new `license` kind is the right long-term fleet encoding is the L1's call; I
  record the two validator outcomes and take no position beyond the round gate.
