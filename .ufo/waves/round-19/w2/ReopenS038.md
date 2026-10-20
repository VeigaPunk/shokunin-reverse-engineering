# Reopen S038 — go.dev release-list JSON, go1.25.0 linux-amd64 archive

Seat: KaidokuR19.ReopenS038-3 (wave 2, read-only scout). No delegation, no production
edits, no REA/MCP device, no carrier execution, no installs.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only).
- Observed main tip: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git -C . rev-parse refs/heads/main`, exit 0).
- Contract baseline B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; C3 prediction freeze:
  `a1140e76fffdc1be032d9d813dbb686157803bbc` (`git -C . rev-parse a1140e7`, exit 0).
- Row under test: `corpus/SOURCES.md:44` (`S038`, tier A, dataset, status `mined`, opened
  2026-10-20, recheck `180d`).
- Lesson quotes under test: `corpus/lessons/round-19.md:42-43`.

## Verdict (short)

- **Identity holds.** The live endpoint still serves one top-level `go1.25.0` object with
  `stable: true` and one linux/amd64 archive file, `go1.25.0.linux-amd64.tar.gz`,
  sha256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`, size `59659213`
  [OBSERVATION]. A fresh archive download today re-hashed to the same digest and size
  [OBSERVATION].
- **Eight frozen carrier hashes match archive members and installed bytes, 8/8**, on three
  retained archive copies; the excluded `link` also matches its frozen digest [OBSERVATION].
- **Row/lesson quote is byte-exact** for JSON lines 14644 and 14648 [OBSERVATION].
- **One calibration gap:** neither the row nor the lesson quote records the fetched JSON
  document's sha256 (`6b83804b…925950`), so the "line 14644" citation is not tied to a
  document revision, although adjacent row S036 does carry a fetched-document digest
  [OBSERVATION + INFERENCE on consequence].
- **One cross-reference inconsistency outside the row:** `claims.json:28` credits C3 to
  `S034/S035/S023`; `claims.json:41`, `corpus/lessons/round-19.md:16` and the knowledge
  doc's source line credit `S035/S023/S003` [OBSERVATION].
- No falsifying fact was found for S038's stated identity/provenance scope.

## 1. Live endpoint, entry fields, and line anchors

```
$ curl -fsSL -m 120 -o /tmp/kr19-ReopenS038-go-dl.json \
    'https://go.dev/dl/?mode=json&include=all'; echo "curl exit=$?"
curl exit=0
2256879 2026-10-20 16:16:05.745780946 -0300
6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950  /tmp/kr19-ReopenS038-go-dl.json
```

Parsed with Python (`json.loads`, exit 0):

| Fact | Value |
|---|---|
| top-level release entries | 369 |
| top-level entries with version `go1.25.0` | 1 |
| that entry's `stable` | `true` |
| linux/amd64 file in that entry | exactly one: `go1.25.0.linux-amd64.tar.gz`, kind `archive` |
| its sha256 | `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613` |
| its size | `59659213` |

Line anchors in the freshly fetched copy (`grep -n`, exit 0):

```
14514:  "version": "go1.25.0",
14644:    "filename": "go1.25.0.linux-amd64.tar.gz",
14648:    "sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",
14649:    "size": 59659213,
```

The multiple `"version": "go1.25.0"` hits below 14514 are per-file objects inside the same
release entry; only 14514 is the release object.

Freshness cross-check against the w1 copies already on disk:

```
$ sha256sum /tmp/kr18-dl/dl.json /tmp/kr19-SourcesRowsDraft-fetch/go-dl.json
6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950  /tmp/kr18-dl/dl.json
6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950  /tmp/kr19-SourcesRowsDraft-fetch/go-dl.json
```

Three fetches at 12:14, 15:37 and 16:16 local produced byte-identical documents, so line
14644/14648 are stable for today's listing [OBSERVATION]. This is a same-day check only;
the listing is regenerated on each Go release [INFERENCE from the endpoint's role, not
observed here].

`stable` semantics: 285 of 369 top-level entries carry `stable: true`, including every
`go1.25.x` point release (`go1.25.0` … `go1.25.14`); the first/current stable entry is
`go1.27.3`. So `stable: true` only marks a released, non-RC object — it is a locator, not a
current-release claim. S038's scope cell already says "not the Go 1.26 or 1.27 release
train", so the row is not making a stale-current claim [OBSERVATION + reading of row text].

```
$ python3 (json parse, stable census); echo $?
0
entries 369 | stable true 285 | go1.25 entries incl. rc: 18 (15 stable point releases + 3 rc)
```

## 2. Local official archive re-hash

```
$ sha256sum /tmp/go1.25.0.linux-amd64.tar.gz \
            /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz \
            /tmp/kr19-SourcesRowsDraft-fetch/go1.25.0.linux-amd64.tar.gz
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  /tmp/go1.25.0.linux-amd64.tar.gz
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  /tmp/kr19-SourcesRowsDraft-fetch/go1.25.0.linux-amd64.tar.gz
```

All three are 59,659,213 bytes (`stat`, and the w1 listing). A fourth, independent fresh
download today:

```
$ curl -fsSL -m 300 -o /tmp/kr19-ReopenS038-archive.tar.gz \
    https://go.dev/dl/go1.25.0.linux-amd64.tar.gz; echo "curl exit=$?"
curl exit=0
$ stat -c '%s' /tmp/kr19-ReopenS038-archive.tar.gz
59659213
$ sha256sum /tmp/kr19-ReopenS038-archive.tar.gz
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613
```

Final-header check (`curl -fsSIL`, exit 0): `location:
https://dl.google.com/go/go1.25.0.linux-amd64.tar.gz`, `content-length: 59659213`,
`last-modified: Tue, 12 Aug 2025 20:51:05 GMT`, `etag: "4a2478b"`. The go.dev URL is a 302
to Google's download host, consistent with the row's `curl -fsSL` claim.

Archive shape: `tar -tzf` → 16,088 entries = 14,496 regular files + 1,592 directories
(exit 0), matching the "14,496-file tree" statement in `.ufo/waves/round-19/w1/
ToolchainIdentity.md:13` [OBSERVATION]. Each of the eight carrier member paths occurs
exactly once in the archive (per-path `tar -tzf … | wc -l` = 1, exit 0).

## 3. Eight frozen carrier hashes vs archive members

Frozen source: `.ufo/waves/round-19/predictions/carriers.tsv` (4 columns: label, installed
path, tier, sha256). Method: stream each member with `tar -xzOf` and pipe to `sha256sum`
(no extraction destination, no execution), and hash the installed file. Run for three
retained archives; loop exit 0 each time.

| Label | Member (`go/…`) | archive = frozen | installed = frozen |
|---|---|---|---|
| t1250-go | `bin/go` | MATCH | MATCH |
| t1250-gofmt | `bin/gofmt` | MATCH | MATCH |
| t1250-asm | `pkg/tool/linux_amd64/asm` | MATCH | MATCH |
| t1250-cgo | `pkg/tool/linux_amd64/cgo` | MATCH | MATCH |
| t1250-compile | `pkg/tool/linux_amd64/compile` | MATCH | MATCH |
| t1250-cover | `pkg/tool/linux_amd64/cover` | MATCH | MATCH |
| t1250-preprofile | `pkg/tool/linux_amd64/preprofile` | MATCH | MATCH |
| t1250-vet | `pkg/tool/linux_amd64/vet` | MATCH | MATCH |

Result: 8/8 archive members equal those exact values, and the installed files equal them,
for `/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz`, `/tmp/go1.25.0.linux-amd64.tar.gz`, and
`/tmp/kr19-SourcesRowsDraft-fetch/go1.25.0.linux-amd64.tar.gz`.

The excluded ninth binary (`link`, no Go build info, `decision-rule.json` `excluded`):

```
$ tar -xzOf /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz go/pkg/tool/linux_amd64/link | sha256sum
a4286eaff6094de7f88d55299a61a14d5aae2bfbd19687ba6d5330a730aee983  -
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/link
a4286eaff6094de7f88d55299a61a14d5aae2bfbd19687ba6d5330a730aee983
```

This equals the frozen `excluded[0].sha256` in `.ufo/waves/round-19/predictions/
decision-rule.json`. So S038's teaches-cell "nine carrier binaries … hash identically to
the same members extracted from that archive" is literally true (8 frozen labels + link)
[OBSERVATION]; note the run cohort is eight labels and `link` is excluded from runs, so
"nine" counts installed binary members, not counted C3 labels.

Per-prediction carrier bindings also equal the table (`predictions/t1250-*.prediction.json`
→ `carrier.sha256` for all eight; Python, exit 0), i.e. the archive-to-freeze link is
scoped to the same bytes the binding gate names.

## 4. Freeze integrity (predictions unchanged)

```
$ cd .ufo/waves/round-19 && sha256sum -c predictions/SHA256SUMS
… 19/19 lines "OK" …
check exit=0
```

```
$ git -C LANE diff --stat a1140e76fffdc1be032d9d813dbb686157803bbc..refs/heads/main \
      -- .ufo/waves/round-19/predictions
(no output) exit=0
$ git -C LANE show a1140e7:.ufo/waves/round-19/predictions/carriers.tsv | sha256sum
c0498b8e91acf06c82b7e22762f6fc91d446d50a817bdfc3e24c387d0df0d953  -
$ git -C LANE show refs/heads/main:.ufo/waves/round-19/predictions/carriers.tsv | sha256sum
c0498b8e91acf06c82b7e22762f6fc91d446d50a817bdfc3e24c387d0df0d953  -
```

The frozen carrier table is bit-identical at the freeze commit and at the observed main
tip, so the member comparison above is against the same freeze the C3 rule names
[OBSERVATION]. (Run-log/compare evidence is other seats' scope; not re-measured here.)

## 5. Row and lesson quote check

`corpus/lessons/round-19.md:42-43` quotes:

- `"filename": "go1.25.0.linux-amd64.tar.gz",`
- `"sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",`

Byte-level check against the fresh document (Python, exit 0):

```
14644 repr: b'    "filename": "go1.25.0.linux-amd64.tar.gz",'
14648 repr: b'    "sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",'
filename quote substring: True
sha256 quote substring: True
line14649: b'    "size": 59659213,'
```

Both quotes are contiguous substrings (modulo the table's stripped leading indentation) and
the cited line 14644 is the filename line in the 6b8380… document. The row's anchor cell
(`SOURCES.md:44`, column `anchor`) states the same version/stable/file/sha256/size and
"fetched 2026-10-20", and its downloads-cross-check sentence matches today's independent
re-download. No quote mismatch found.

## Findings

### F1 — identity and freshness hold (no action)

[OBSERVATION] Endpoint entry and archive agree on `2852af0c…b613` / `59659213` across a
fresh JSON fetch (digest `6b83804b…925950`), a fresh archive download, and three retained
copies; the eight frozen carriers and the excluded `link` equal the archive's members and
the installed files. [INFERENCE] Within its stated scope ("archive digest and size … not
the Go 1.26/1.27 train") S038 is accurate and fresh as of 2026-10-20 16:16 -03.

### F2 — calibration gap: fetched-document digest is not anchored (append-only candidate)

[OBSERVATION] `corpus/SOURCES.md:44` records only the entry's sha256/size plus the fetch
date; the lesson quote cites "fetched copy line 14644" (`corpus/lessons/round-19.md:42`)
without a document digest. The w1 report does record it
(`.ufo/waves/round-19/w1/SourcesRowsDraft.md:33`: 2,256,879 bytes, sha256
`6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`). Adjacent row S036
(`SOURCES.md:42`) carries a fetched-document sha256 in its anchor, so the omission is
inconsistent with local practice.
[INFERENCE] Because the listing is regenerated, a future rechecker cannot tell which
document revision "line 14644" indexed; the line anchor can drift while the row still
reads correct. This affects anchor reproducibility, not the archive-identity claim.
Suggested append-only fix (owner: lesson/SOURCES integrator, not this seat): add the
document digest to the S038 quote row or anchor, e.g. "line 14644 of the 2026-10-20 fetch,
document sha256 6b8380…925950".

### F3 — wording note: `stable: true` is a locator, not freshness

[OBSERVATION] 285/369 top-level entries carry `stable: true`, including all 15 `go1.25.x`
point releases; current stable per the endpoint is `go1.27.3`. The row's locator phrasing
"version `go1.25.0` with `stable` true" is accurate as a selector and the scope cell
already excludes later trains. [INFERENCE] No edit required; a reader could misread
`stable` as "current stable", which the scope cell counteracts.

### F4 — related cross-reference inconsistency in `claims.json` C3 (outside row scope)

[OBSERVATION] `claims.json:28` (C3 `sourced`) says "with S034/S035/S023";
`claims.json:41` (amendment C3 `sourced`) says "with S035/S023/S003";
`corpus/lessons/round-19.md:16` says "sourced: S038, with S035/S023/S003"; the knowledge
doc source line (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:1`) lists S038,
S035, S023, S003. S034 is the Go 1.24 release-notes runtime source; S003 is the Ghidra
12.1.4 Base source.
[INFERENCE] The line-28 list predates the amendment and names S034 where the mechanism
chain uses S003; this is a calibration defect in the claim text, not in S038, and belongs
to a C3/claims seat. Reported here only because it surfaced while checking C3's sourcing.

## Remaining unknowns

- Whether the JSON line numbers survive the next listing regeneration. Not determinable
  from today's data; the document digest is stable only across today's three fetches.
- No independent signature check of the archive was done. Go publishes sha256, not a
  signed tarball; trust rests on HTTPS to go.dev/dl plus agreement of the published digest
  with three retained copies and one fresh download [OBSERVATION of method].
- Full installed-tree byte identity beyond the nine tool binaries was not re-checked; only
  the archive's regular-file count (14,496) was observed, consistent with w1's
  `ToolchainIdentity.md:13` claim, which remains w1's evidence, not mine.
- Run-bound logs and `compare.json` counts (C3's measured outcome) are outside this
  ticket; untouched.

## Tooling / installs

None. No pacman, uv, npm, cargo or binary installs; no REA CLI or MCP device use; no
carrier execution and no `--help`/`version` invocation of any carrier. No clone was
created because this ticket required no mutation test. Only /tmp scratch downloads were
written: `/tmp/kr19-ReopenS038-go-dl.json` and `/tmp/kr19-ReopenS038-archive.tar.gz`.
