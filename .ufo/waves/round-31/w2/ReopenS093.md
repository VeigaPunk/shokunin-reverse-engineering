# ReopenS093 — SOURCES S093 (`pyproj` PyPI release records) and its Gate quote

Seat: wave-2 re-open / falsify. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, frozen at
`35ba7c522dba55f9be27eb161d4254eacaa24330`. All UTC times 2026-10-23. Lane read-only; the only lane
file written is this report. No clone, no REA run, no install or update.

## Verdict

| target | verdict | basis |
|---|---|---|
| SOURCES row S093 | **agree** | all 11 contract columns valid; all five served JSON SHA-256 match; all five wheel filename→digest pairs match both the row anchor and `carriers.tsv`; used-by path exists and cites S093 (6 occurrences) |
| Gate quote for S093 | **holds** on sha/verbatim/≤25-words/line-1, **under-grounds** the digest clause | quote is the 3.7.1 wheel filename only (1 word); `teaches` asserts the records bind filename to SHA-256, and no digest appears in the Gate quote or the Gate sha256 column (which is the served-JSON hash, not the wheel hash). The binding is verified here and in the row anchor, so this is a Gate-evidence thinness, not a false row |
| "line 1" as the quote location | **could-not-fully-locate** (weak location, correct line) | the served record is minified to one line (61,822 bytes, 1 newline), and the quoted filename occurs **twice** on it: offset 36,601 as `.urls[].filename`, offset 37,036 inside a `files.pythonhosted.org` download URL. Only the row anchor's `.urls[]` wording disambiguates; the Gate quote alone does not |
| adjacent: Gate section's closing `used-by` claim | **fails as written** (does not implicate S093's own cell) | lesson says "S092–S097 new (status `mined`, used-by the two round-31 entries)"; every row's used-by cell names exactly one entry, and the *other* cells are incomplete — see Adjacent findings |

## Sources opened (contract §Rules rule 1 record)

All fetched by `curl` (plain HTTPS), access date 2026-10-23; no browser, no challenge bypass.

| URL | fetched (UTC) | bytes | sha256 of bytes read | located quote (≤25 words), line |
|---|---|---|---|---|
| https://pypi.org/pypi/pyproj/3.7.1/json | 2026-10-23T04:29:48Z (re-fetch 04:31:14Z, `http=200 bytes=61822`) | 61,822 | `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7` | line 1, byte offset 36,601: `pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (1 word) |
| https://pypi.org/pypi/pyproj/3.4.1/json | 2026-10-23T04:30:06Z | 60,252 | `e2209485625e12441c5d5e8321cfcc0eff13780dc62937764699a1d4273756ca` | line 1: `pyproj-3.4.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (1 word) |
| https://pypi.org/pypi/pyproj/3.5.0/json | 2026-10-23T04:30:06Z | 60,655 | `b652ced79ac8554f09b4f2544c05d0eaea8622e3d367009e89aa18fdab0d0e7c` | line 1: `pyproj-3.5.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (1 word) |
| https://pypi.org/pypi/pyproj/3.6.1/json | 2026-10-23T04:30:06Z | 56,089 | `4eb7b680f90e15a34a0d55af0cddcb9f0730d1516b3831bfadb0e1c2b108d134` | line 1: `pyproj-3.6.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (1 word) |
| https://pypi.org/pypi/pyproj/3.7.0/json | 2026-10-23T04:30:06Z | 54,523 | `b28551bf19cc04ccfe15e51bf404eadc7a296ba7c60dc714a5ed2b43a8a0e0f4` | line 1: `pyproj-3.7.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` (1 word) |

The served 3.7.1 digest field immediately precedes the quoted filename (offset ~36,590):
`…b5d98d0f30ee"},"downloads":-1,"filename":"pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"`.
The five `urls[].digests.sha256` values equal the row's five wheel digests exactly.

## S093 row against the CORPUS.md SOURCES contract

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md:64-...` (*SOURCES.md — where a shokunin learns*, frozen
contract v1), row shape `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

| column | cell summary | contract check | verdict |
|---|---|---|---|
| id | `S093` | `S`+3 digits, unique; 97 rows, malformed 0 (`awk -F'|' … NF!=13` → `malformed=0`) | pass |
| source | "PyPI release records for pyproj 3.4.1, 3.5.0, 3.6.1, 3.7.0, and 3.7.1 — " + five canonical `https://pypi.org/pypi/pyproj/<v>/json` URLs | title + canonical URL; each URL opened and 200/JSON | pass |
| kind | `dataset` | in enum (`spec·docs·paper·code·tool·dataset·talk·book·community·own-work`) | pass |
| tier | `A` | A = primary/authoritative for the cell's scope; scope is the maintainer-declared filename+digest metadata, which the index publishes authoritatively; not `community` | pass |
| scope | "Official filename and SHA-256 metadata for the five … wheel containers referenced by `corpus/evidence/round-31/c1/carriers.tsv`; not the extracted database bytes or REA behavior" | scoped to a claim/topic; explicit non-scope | pass |
| anchor | "PyPI JSON records fetched 2026-10-23; served JSON SHA-256: <five>; `.urls[]` `filename` / `digests.sha256` (line 1): <five filename — digest pairs>" | line + revision (version-pinned URLs + served-byte hash), not a bare homepage; every claimed value reproduced here | pass, with the caveat that “line 1” is non-discriminating (single-line minified JSON; see Verdict) |
| teaches | "The official release records bind each named wheel archive to its declared SHA-256, supporting wheel-level carrier provenance; they do not verify the embedded `proj.db` bytes or REA behavior." | one grounded learner benefit, with limits | pass |
| status | `mined` | cited by ≥1 used-by path (yes) | pass |
| opened | `2026-10-23` | matches observed fetch date | pass |
| recheck | `on-release` | allowed cadence (`ISO date`/`90d`/`180d`/`on-release`) | pass |
| used-by | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | path exists; entry cites S093 (6 occurrences, `source:` line + carrier rows) | pass |

Append-only: the row was introduced by `0007731e` and is byte-identical at lane tip — `git show 0007731e:corpus/SOURCES.md | awk 'NR==99' | sha256sum` = `awk 'NR==99' corpus/SOURCES.md | sha256sum` = `8987bf7ac9d8cc15983b8a5b9312e8bba0b8eb208efc91ad94cbd721a230e6d9` (both, read-only git).

## Gate table (corpus/lessons/round-31.md:32)

Gate row as written:

```
| S093 | https://pypi.org/pypi/pyproj/3.7.1/json (and the 3.4.1, 3.5.0, 3.6.1, 3.7.0 records) | 2026-10-23 | 3.7.1 `2ad9561a…b1b7` (others in `SrcPypiPyproj.md`) | line 1: `pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | admit, mined |
```

- access date `2026-10-23`: **observation**, matches this seat's fetches.
- sha256 abbreviation `2ad9561a…b1b7`: **observation**, prefix/suffix match the full served hash.
- "others in `SrcPypiPyproj.md`": **observation**, `.ufo/waves/round-31/w1/SrcPypiPyproj.md` exists and records all five JSON SHA-256 values (`:19-23`, `:61-65`) and all five wheel digests (`:46`); both sets match this seat's fetch.
- quote: **observation**, byte-exact substring of the served bytes (`grep -F` count 1 line / 2 occurrences; Python `in` check true), 1 word (≤25), on line 1 (the record has exactly one line).
- decision "admit, mined": consistent with the row (status `mined`, used-by present).

Two bounded Gate weaknesses, neither falsifying the row:

1. **Quote does not carry a digest.** Rule 1 demands a quote "grounding `teaches`"; `teaches` is about filename→SHA-256 binding, but the quoted text is a filename and the Gate sha256 column holds the served-JSON hash (`2ad9561a…b1b7`), not a wheel digest. The wheel digests appear only in the row's anchor and `SrcPypiPyproj.md:46`; anyone re-opening from the Gate quote alone can confirm the name, not the binding. Severity: minor/evidence thinness (the binding is true; re-verified here).
2. **"line 1" cannot locate the quote within the bytes.** The record is one line, so `line 1` is the whole 61,822-byte document; the filename also occurs in a download-URL path at offset 37,036. The row anchor's ``.urls[] `filename` `` resolves it; the Gate quote's location string does not.

## Adjacent findings (produced while checking used-by; not a defect in S093's own row)

- **S093 is cited by one entry, not two.** `grep -n 'S093\|pyproj' corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` → no output (exit 1); the refusals entry never mentions S093 or pyproj. So the Gate section's sentence "S092–S097 new (status `mined`, used-by the two round-31 entries)" (lesson:41) overstates S093's used-by.
- **Three used-by cells omit a citing entry.** Per contract, used-by = "repo-relative paths of the knowledge entries or lessons citing the row". Observed cells (`awk -F'|' … $12`): S092→refusals only, S093–S097→positive only. But the positive entry's `source:` line ends `…; S092 (REA 6.5.0 SQLite reader code, for the inferences below)` (`2026-10-23-r31-sqlite-positive.md:3`), so **S092 used-by omits the positive entry**; and the refusals entry's `source:` line reads `source: S092 (…); S096 and S097 for the file-format and PRAGMA terms` (`2026-10-23-r31-sqlite-refusals.md:3`), so **S096 and S097 used-by omit the refusals entry**. Rule 2 permits an in-place `used-by` change logged old→new, so this is fixable without touching frozen content.
- S093's own used-by cell is accurate and complete (positive is its only citing entry).

## Commands, outputs, exit codes

All paths absolute; scratch root `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/`.

1. `timeout 60 curl -sS -D headers-3.7.1.txt -o pyproj-3.7.1.json https://pypi.org/pypi/pyproj/3.7.1/json` → **exit 0**, 2026-10-23T04:29:48Z; `sha256sum` → `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7`; headers start `HTTP/2 200`.
2. `for v in 3.4.1 3.5.0 3.6.1 3.7.0; do timeout 60 curl -sS -o pyproj-$v.json https://pypi.org/pypi/pyproj/$v/json; echo "$v exit=$?"; done` → `3.4.1 exit=0` … `3.7.0 exit=0`, 04:30:06Z; hashes as in the Sources table.
3. `timeout 60 curl -sS -o /dev/null -w 'http=%{http_code} bytes=%{size_download}\n' https://pypi.org/pypi/pyproj/3.7.1/json` → `http=200 bytes=61822`, 04:31:14Z.
4. `timeout 120 python3 -I -B verify-s093.py > verify-s093.out 2>&1` → **real_exit=0**, 04:32:32Z, last line `VERDICT ALL-PASS`; 60 PASS lines, 0 FAIL. Full output: artifact `verify-s093.out`.
5. `python3 -c` byte comparison: pinned copy `corpus/evidence/round-31/c1/pypi-pyproj-3.7.1.json` vs fresh fetch → `pinned==fetched: True len= 61822`.
6. `grep -F -o '<filename>' pyproj-3.7.1.json | wc -l` → `2`; Python occurrence offsets `36601`, `37036`.
7. `awk -F'|' 'NR==99 {print "NF="NF}' corpus/SOURCES.md` → `NF=13`; census `rows=97`, `malformed=0`.
8. Read-only git: `git log -S 'S093' --oneline -- corpus/SOURCES.md` → `0007731e round-31: entries (…)`; line-99 sha equal at `0007731e` and tip (both `8987bf7a…e6d9`).

Conclusion labels: every sha/digest/citation equality above is an **observation** from a run command. The
severity calls on the Gate quote and the used-by incompleteness are **inference** from contract text. No
**unknown** remains for S093 itself; the only thing this seat did not check is whether the wheel archives
themselves (not their declared digests) are byte-identical to `carriers.tsv` container shas — out of scope
here and covered by wave-1 `ReviewCarrierProvenance.md`.

## Scratch artifacts (sha256)

| file | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/verify-s093.py` | `0420d59c280369db546523536a63c015e7490ce221149f5ac69cf963b86baff2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/verify-s093.out` | `aa3b31967e833e77649b5f61d34ed369253f81477e466e971577e4f19fd29132` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/pyproj-3.4.1.json` | `e2209485625e12441c5d5e8321cfcc0eff13780dc62937764699a1d4273756ca` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/pyproj-3.5.0.json` | `b652ced79ac8554f09b4f2544c05d0eaea8622e3d367009e89aa18fdab0d0e7c` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/pyproj-3.6.1.json` | `4eb7b680f90e15a34a0d55af0cddcb9f0730d1516b3831bfadb0e1c2b108d134` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/pyproj-3.7.0.json` | `b28551bf19cc04ccfe15e51bf404eadc7a296ba7c60dc714a5ed2b43a8a0e0f4` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/pyproj-3.7.1.json` | `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS093/headers-3.7.1.txt` | `fbe28778a3ccfa8cc1c39905d00ce0300502d080123a4ad278a4425dda0f163f` |

`tmp/` was created for `TMPDIR` and is empty (no REA run). No tool installs or updates.

Report: `.ufo/waves/round-31/w2/ReopenS093.md`
