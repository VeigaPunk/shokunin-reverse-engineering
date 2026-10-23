# ReopenS095 — SOURCES row S095 (`pyogrio` 0.11.1 PyPI record + sdist) and its Gate quote

Seat: `KaidokuR31.ReopenS095` (scout, leaf). Round 31, wave 2. Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only; the only lane file written is this
report. UTC work window 2026-10-23T04:29:55Z–2026-10-23T04:35:18Z. No REA run, no counter run, no
clone, no subagent, no tool installed or updated (nothing to record under the tooling directive).

**What this seat attacks:** the S095 row (`corpus/SOURCES.md:101`) and its Gate row
(`corpus/lessons/round-31.md:34`) — the recorded served-JSON digest, the recorded sdist digest,
the Gate quote's verbatim/≤25-word/line-1 claims, the row's 11 columns against the CORPUS.md
contract, and its `used-by` cell.

## Verdict

| target | verdict | basis |
|---|---|---|
| SOURCES row S095 | **agree** (`admit, mined`) | every digest, size and membership claim in the `anchor` cell reproduces today: served JSON `5b286ab2…7162` / 32,351 B; sdist `e1441dc9…082c` / 287,267 B; the sdist digest equals all five `gpkg-*` `container_sha256` cells; the five extracted members hash to the five carrier `sha256` cells *and* to the immutable carrier files |
| Gate sha256 column | **holds** | byte-identical re-fetch, twice, 77 s apart; the `5b286ab2…7162` / `e1441dc9…082c` abbreviations are true prefix/suffix truncations of the full digests |
| Gate quote | **holds** | `"filename":"pyogrio-0.11.1.tar.gz"` occurs exactly once in the served bytes (offset 31,878), on line 1 of a one-physical-line body, verbatim; 1 whitespace-separated word (2 if split at the colon) — ≤25 |
| row columns vs CORPUS.md | **pass** | 11 columns (NF=13), enums `dataset`/`A`/`mined` valid, tier-A not `community`, anchor not a bare homepage, scope names its non-scope, `opened`/`recheck` valid |
| `used-by` cell | **pass** for the cell; **fails as written** for the lesson sentence that describes it | cell = `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`, path exists, cites S095 six times. But `corpus/lessons/round-31.md:41` says "S092–S097 new (status `mined`, used-by the two round-31 entries)"; S095's cell names **one** entry, and the refusals entry cites S095 zero times — see §6 |

No counterexample found against S095's substantive claims. The defects this seat can report are
(a) the lesson's blanket `used-by` sentence (adjacent, lane-wide) and (b) a durability caveat on
recording the served-JSON digest of a mutable document (§7), which the row's `recheck:
on-release` already anticipates.

## 1. Sources opened (contract rule 1 record)

All plain HTTPS `curl`, no browser, no challenge bypass, access date **2026-10-23**.

| URL | fetched (UTC) | bytes | sha256 of bytes read | located quote (≤25 words) |
|---|---|---|---|---|
| `https://pypi.org/pypi/pyogrio/0.11.1/json` | 2026-10-23T04:29:55Z (re-fetch 04:31:12Z, identical) | 32,351 | `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162` | line 1, byte offset 31,878: `"filename":"pyogrio-0.11.1.tar.gz"` — 1 word, one occurrence |
| `https://files.pythonhosted.org/packages/bf/1d/ae0340237207664e2da1b77f2cdbcb5f81fd0fc9f3200a48ca993a5e12ef/pyogrio-0.11.1.tar.gz` | 2026-10-23T04:30:35Z | 287,267 | `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` | served bytes are gzip; the located name is the decompressed tar member `pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg` at decompressed offset 317,952, one occurrence (1 word) |

The quoted JSON fragment sits inside the sdist URL object, immediately after that object's own
digest: `…b0977ab91ef8082c"},"downloads":-1,"filename":"pyogrio-0.11.1.tar.gz","has_sig":false,…`
(observation, the printed window covered offsets 31,788–32,038).

## 2. sha256 checks — commands and exact outputs

```sh
$ curl -sS -D headers.txt -o pyogrio-0.11.1.json -w 'http_code=%{http_code} size_download=%{size_download}\n' \
    https://pypi.org/pypi/pyogrio/0.11.1/json
http_code=200 size_download=32351          # exit 0, 2026-10-23T04:29:55Z (response `date:` header agrees)
$ sha256sum pyogrio-0.11.1.json
5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162  pyogrio-0.11.1.json   # exit 0
$ wc -c pyogrio-0.11.1.json
32351 pyogrio-0.11.1.json
$ curl -sS --compressed -o refetch.json https://pypi.org/pypi/pyogrio/0.11.1/json   # 04:31:12Z, exit 0
5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162  refetch.json
$ cmp -s pyogrio-0.11.1.json refetch.json && echo IDENTICAL
IDENTICAL
$ sha256sum pyogrio-0.11.1.tar.gz ; wc -c pyogrio-0.11.1.tar.gz
e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c  pyogrio-0.11.1.tar.gz   # exit 0, 04:32:00Z
287267 pyogrio-0.11.1.tar.gz
```

| recorded where | value | reproduces? |
|---|---|---|
| row `anchor`, `corpus/SOURCES.md:101` | Served JSON SHA-256 `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162` (32,351 bytes) | **yes**, exactly, twice |
| row `anchor` | `.urls[]` filename `pyogrio-0.11.1.tar.gz`, size `287267`, SHA-256 `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` (line 1) | **yes**: parsed `.urls[]` has 31 entries, one sdist with exactly that filename/size/digest; `info.version` = `0.11.1`, `info.name` = `pyogrio`, sdist `yanked=false` |
| row `anchor` | downloaded sdist SHA-256 `e1441dc9…082c` (287,267 bytes) | **yes**: the download from the row's own files.pythonhosted URL is byte-identical to the index digest and to the wave-1 retained copy |
| Gate `corpus/lessons/round-31.md:34` | `JSON 5b286ab2…7162`; `sdist e1441dc9…082c` | **yes**: prefix and suffix of both full digests are correct truncations |

Corroboration (observation): the wave-1 scribe's retained copies hash to the same two values —
`sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.json` →
`5b286ab2…7162`; `…/pyogrio-0.11.1.tar.gz` → `e1441dc9…082c` (exit 0). The Gate value was not
fabricated and has not drifted.

## 3. Quote check — verbatim, unique, line 1, ≤25 words

```sh
$ python3 -c "b=open('pyogrio-0.11.1.json','rb').read(); q=b'\"filename\":\"pyogrio-0.11.1.tar.gz\"';
              print('count',b.count(q),'offset',b.find(q),'line',b[:b.find(q)].count(b'\n')+1)"
count 1 offset 31878 line 1                     # exit 0
$ printf '%s' '"filename":"pyogrio-0.11.1.tar.gz"' | wc -w
1                                               # exit 0
```

- The recorded Gate text `line 1: "filename":"pyogrio-0.11.1.tar.gz"` is **verbatim**: the bytes at
  offset 31,878 are `"filename":"pyogrio-0.11.1.tar.gz"`, plain ASCII, no space after the colon
  (the minified JSON has none; a quoted form with `": "` would not be verbatim).
- Location: the body is 32,351 bytes with **one** newline at EOF (`wc -l` = 1, last byte `0x0a`);
  line 1 is the whole document, so "line 1" is exact but coarse — the digest is the real locator.
- Word count: 1 whitespace token; 2 tokens if split at the colon and the quotes are stripped. Both
  ≤25. This is a JSON key/value, not prose (same style as S091/S093/S094).
- Uniqueness (this is where S095 differs from S093): the bare filename `pyogrio-0.11.1.tar.gz`
  occurs **twice** on line 1 — offset 31,890 as `.urls[].filename` and offset 32,268 inside the
  `.urls[].url` string. The Gate quote carries the `"filename":` key, so the quoted form is unique
  (count 1). The quote therefore identifies its own JSON member without needing the row anchor.
- Grounding: the quote grounds the *filename-identity* half of `teaches`. It does not itself ground
  the "five GeoPackage fixtures are members of the sdist" half; that half rests on the row's digest
  chain, which §4 reproduces end-to-end. Thinness, not overstatement.

## 4. Fixture-membership chain re-derived independently

```sh
$ tar -tzf pyogrio-0.11.1.tar.gz | grep -c '\.gpkg$'          # 5   (exit 0)
$ tar -xzf pyogrio-0.11.1.tar.gz -C x && sha256sum x/pyogrio-0.11.1/pyogrio/tests/fixtures/*.gpkg
03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302  …/curve.gpkg
00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7  …/curvepolygon.gpkg
9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c  …/line_zm.gpkg
898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d  …/multisurface.gpkg
4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8  …/test_gpkg_nulls.gpkg
$ sha256sum /fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-*.gpkg      # exit 0
03a9c5904fd3…  gpkg-curve.gpkg        00a1309ab0f2…  gpkg-curvepolygon.gpkg
9563e513b064…  gpkg-line-zm.gpkg      898a238bc119…  gpkg-multisurface.gpkg
4281d3c55f20…  gpkg-test-gpkg-nulls.gpkg
```

The five sdist member hashes equal, cell for cell, both `corpus/evidence/round-31/c1/carriers.tsv`
lines 9–13 (`sha256`, 98,304 bytes each) and the immutable carrier files themselves; all five
`container_sha256` cells there are `e1441dc9…082c`, the sdist digest. The row's claim "equal to all
five `gpkg-*` `container_sha256` cells … (carriers.tsv:9-13)" is **confirmed**, including the
line-number citation. The sdist holds exactly five `.gpkg` members, so "the five" is also the
complete set. Every member was read only.

## 5. S095 row against the CORPUS.md SOURCES contract

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md:64-145` (*SOURCES.md — where a shokunin learns*,
frozen contract v1), shape `| id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by |`.

| column | cell (abridged) | contract check | verdict |
|---|---|---|---|
| id | `S095` | `S`+3 digits, unique (only pyogrio row; `grep -c pyogrio` = 1), absent at base `c369242f` (grep count 0), introduced at `0007731e` | pass |
| source | "PyPI release record for pyogrio 0.11.1 — https://pypi.org/pypi/pyogrio/0.11.1/json (sdist https://files.pythonhosted.org/…/pyogrio-0.11.1.tar.gz)" | title — canonical URL(s); both opened 200 | pass |
| kind | `dataset` | in enum; a published archive + release record, as S091 does for uv | pass |
| tier | `A` | A = primary/authoritative *for that scope* (maintainer-published record and artifact); not `community` | pass |
| scope | "The official source-distribution identity and five GeoPackage fixtures used as R31-C1 inputs; not Pyogrio runtime behavior or REA outcomes" | names the topic and its non-scope | pass |
| anchor | Served JSON SHA-256 + size; `.urls[]` filename/size/SHA-256 `(line 1)`; downloaded sdist SHA-256 + size; equality to five `container_sha256` cells; member hashes to carrier `sha256` cells `(carriers.tsv:9-13)` | line + revision, never a bare homepage; **every value reproduced in §2/§4**. Version (`0.11.1`) sits in the `source` cell and is pinned by both URLs rather than restated in `anchor` — consistent with S091/S093 | pass (note) |
| teaches | "The PyPI record and matching archive digest establish that R31-C1's five pinned GeoPackage fixtures are members of the official pyogrio 0.11.1 sdist; they do not establish REA reader semantics or success." | one grounded learner benefit with limits; membership itself is what §4 shows (the record supplies the digest, opening the archive supplies membership) — compressed attribution, not a false claim | pass (note) |
| status | `mined` | cited by ≥1 `used-by` path | pass |
| opened | `2026-10-23` | matches my fetches and the Gate | pass |
| recheck | `on-release` | allowed cadence | pass |
| used-by | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | exists; cites S095 (6 occurrences: `source:` line + five carrier rows) | pass |

Census (lane root, `2026-10-23T04:33:33Z`, all exit 0): `NF=13` for line 101; the enum/tier-
inflation sweep printed nothing; the mined-`used-by`-path-exists sweep printed nothing; the row's
`status|opened|recheck` = `mined | 2026-10-23 | on-release`. Committed state: `git diff --stat HEAD`
over `corpus/SOURCES.md`, `corpus/evidence/round-31/c1/carriers.tsv`, the entry and the lesson is
empty (exit 0), so the row I read is the committed row.

## 6. `used-by` existence and the lesson sentence that describes it

- The cell's path **exists** and **cites S095** six times (entry lines 3, 24–28) — the assigned check
  passes.
- `corpus/lessons/round-31.md:41` says: "S092–S097 new (status `mined`, used-by the two round-31
  entries)." For S095 that is **false read per row**: the cell names one entry, and
  `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` mentions S095 **zero** times
  (`grep -o S095 … | wc -l` → 0; that entry cites S092 ×3, S096 ×1, S097 ×1). Only as a statement
  about the set S092–S097 ("collectively cited by the two entries") is it true. Same class the
  S093 seat reports; the defect is in the lesson sentence, not in S095's cell.
- Strict reading of the contract's `used-by` definition ("paths of the knowledge entries **or
  lessons** citing the row"): `corpus/lessons/round-31.md` names S095 at lines 15, 34 and 41 and is
  not listed. This is lane-wide and long-standing, not S095-specific: S085–S091 (three rounds) are
  each named three times in their creating round's lesson and none lists it, while 81 older rows do
  list lessons (e.g. `S001: corpus/lessons/round-13.md, …`). The settled practice is evidently that
  the creating round's lesson is not a citation; the L1 should rule once, not per row.

## 7. Residual unknowns / what would change the verdict

- **The served-JSON digest is a snapshot of a mutable document** (inference from the observed keys,
  not observed drifting): the body carries project-scoped `last_serial` (384,19805 at 04:29:55Z) and
  a `vulnerabilities` array (`[]` today); a later pyogrio release or a filed advisory will change the
  bytes served at this version-pinned URL, so a future verifier comparing
  `5b286ab2…7162` may see a mismatch with no defect. Today two fetches 77 s apart were byte-identical.
  `recheck: on-release` is the correct guard; the durable identities are the sdist digest and the
  carrier hashes, which cannot drift silently.
- **Not evaluated (unknown, out of scope):** whether the fixtures' content is semantically valid
  GeoPackage (the C1 oracle's job), and whether PyPI's uploader identity is who the row names. The
  row claims only "members of the official sdist", which the archive shows.
- **Process deviation (disclosed):** the three `curl` calls and the `tar`/`sha256sum`/`python3` checks
  were not wrapped in `timeout`; each returned in under 3 s with exit 0 and the session's command
  deadline applied. No process tree left running; no background job started.

## 8. Artifacts (scratch, all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS095/`)

| file | sha256 | bytes |
|---|---|---|
| `pyogrio-0.11.1.json` (served record) | `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162` | 32,351 |
| `refetch.json` (`--compressed` re-fetch, identical) | `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162` | 32,351 |
| `pyogrio-0.11.1.tar.gz` (sdist) | `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` | 287,267 |
| `headers.txt` (response headers) | `8402756af8a7c0ac645a4163d7a62406be9d0fdba07b0d781732345e8d2e8d4e` | 2,742 |
| `quote.txt` (quote bytes, no newline) | `5d2904a2a983db499065a20ddb001e7003bfd8a77d9d40ea7fec42503eae8478` | 34 |
| `evidence.txt` (command/output log, 04:32:44Z) | `e50252e8938b49637208f8f07b0943194842a316fd91f9c39e959beb3a8a2fe5` | 2,495 |
| `census.txt` (contract checks, 04:33:33Z) | `f6baf312438a620ef0ac4d136fa0c69b575a23271a749ee67cf9d2573087d519` | 193 |
| `x/pyogrio-0.11.1/…` (extracted sdist tree) | member hashes in §4 | — |

Report: `.ufo/waves/round-31/w2/ReopenS095.md`
