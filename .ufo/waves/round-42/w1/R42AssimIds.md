# R42AssimIds — assimilation id-collision and quarantine checks (kaidoku round 42, wave 1)

**VERDICT: DEFECTS FOUND** — the 0–3-space collision guard is sound and proven (indented `  | S002 |` is
caught, census exit 0 on the fixture), the kaidoku quarantine slice is 5 rows and byte-identical to round 41
(`7383a90e…28e6a`), and the collision count is 24 (`S106`–`S129`); but the register's kaidoku ids are the
**staging** namespace, not the lane registry (3/5 ids do not exist in the lane registry, 2/5 name a different
document than the register's cited URL), and **4 staged rows already duplicate a held document by exact URL**
plus 4 more behind a pinned ref — so an id-joined adoption would append duplicates. Nothing was appended.

Seat: `R42AssimIds` · L1 `KaidokuR42` · base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` · lane HEAD at run time
`fdabdfa46fd1652ce370fa72fca1d00751d01528` (`fdabdfa4 round-42: draft claims (not frozen), start census,
wave-1 spec/generator/dispatch` over `ae5dc3f3 round-41: wave-2 settled …`, 2 commits, **neither touches
`corpus/SOURCES.md`**).

Inputs read (read-only): lane `corpus/SOURCES.md` at the base commit;
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md`;
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`;
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`; lane round-41 lesson + committed round-41
assimilation artifacts (for the comparison). No campaign tool was run and nothing under `/home/vgpnk/Projects/shokuknow`
was written.

---

## 1. Id collision check, and the guard proof

`A` = `.ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation` (lane-relative). The base blob was written to
scratch **first** (`S=/fast/scratch/hyaku/kaidoku-r42/R42AssimIds`), then every list was derived from that file.

```console
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:corpus/SOURCES.md > "$S/work/SOURCES.base.md"
show exit=0
$ sha256sum "$S/work/SOURCES.base.md"
3cf6cf99de275e68dcd06d5c297c5f22e36749657f1a8d8128df2755ead18727  …/work/SOURCES.base.md
```

```console
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' SOURCES.base.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md \
    | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
reg count: 129
staged count: 132
collision count: 24
--- reg first/last:  S001 … S129
--- staged first/last: S106 … S237
--- collisions: S106 S107 … S129          (contiguous, no gaps, no duplicate ids)
```

| list | rows | range | gaps | dups | sha256 |
|---|---|---|---|---|---|
| `reg-ids` | 129 | S001–S129 | none | 0 | `d1cd69af6a7dec716869274da7866426cc8af9ea76015e6b9ee18f197307577b` |
| `staged-ids` | 132 | S106–S237 | none | 0 | `93841167c73394fa7f15835b802caa9964757971a654c0d0837ec166c5da089b` |
| `collisions` | **24** | S106–S129 | none | 0 | `9c9463858aa387fdc4717ffd557bbdb4ce41d30976859b9a4b2bd038d0281049` |

**Both id lists, compactly** (full lists are the two artifacts above): `reg-ids` = `S001-S129`;
`staged-ids` = `S106-S237`. Collisions = `S106-S129` (24).

Revision independence: `corpus/SOURCES.md` is byte-identical at the base commit, at lane HEAD and in the
working tree (`sha256 3cf6cf99…8727` for all three; `git status --porcelain -- corpus/SOURCES.md` empty), so the
count is not an artefact of the base pin. Round-41's committed list compared: `reg-ids` 126 → **129**,
`staged-ids` 132 → 132, `collisions` 21 (S106–S126) → **24** (S106–S129). The drift grew by exactly the three
rows round 41 adopted (S127, S128, S129, round-41 Gate "Registry 126 → 129 rows").

### Guard proof — indented colliding row, on a census-valid scratch registry

Fixture `guard/registry-indented.md` (7 lines) carries `S001`, an **indented** `  | S002 |` row and `S003`;
`guard/staged.md` carries `  | S002 |` + `| S099 |`.

```console
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file validate/corpus/SOURCES.md
file	ok	/fast/scratch/hyaku/kaidoku-r42/R42AssimIds/work/validate/corpus/SOURCES.md
exit=0                                   # the fixture with the indented row is census-valid

$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' guard/registry-indented.md | grep -oE 'S[0-9]+' | sort
S001
S003                                     # column-zero-only pattern: misses the indented row
$ comm -12 reg-ids-zero-broken staged-ids-zero-broken | wc -l
0                                        # BROKEN pattern: false green, as the census clause predicts

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/registry-indented.md | grep -oE 'S[0-9]+' | sort
S001
S002
S003                                     # 0-3-space pattern catches it
$ comm -12 reg-ids-guard staged-ids-guard
S002                                     # count 1 -> nonempty collisions, guard proven
```

Full transcript: `guard/guard-proof.txt`; fixtures + derived lists: `guard/registry-indented.md`,
`guard/staged.md`, `guard/reg-ids-guard`, `guard/staged-ids-guard`, `guard/collisions-guard`,
`guard/reg-ids-zero-broken`, `guard/collisions-zero-broken`, `guard/census-validate.txt`.
The census clause the guard mirrors is `/home/vgpnk/Projects/shokunin/CORPUS.md:152-153` ("accepts 0–3 leading
ASCII spaces before Markdown table rows and headings; 4 or more spaces are indented code and are ignored").
The real data carries **no** indented row this round (`corpus/SOURCES.md` 129/129 column-zero;
`SOURCES.append.md` 132/132 column-zero), so the widened pattern changes today's count and only removes the
false-green class.

### Depth: are the 24 collisions duplicates or drift?

`collisions` alone cannot tell a real duplicate from positional drift, so I joined by document
(`doc-join.py`, artifact, exit 0). Every one of the 24 colliding ids names a **different document** in the two
lists (`collision-documents.tsv`: `distinct_documents=distinct` for 24/24, `same` for 0) — e.g. staged `S109` is
the binwalk v3 README while lane `S109` is a neovim v0.12.6 release; staged `S107` is the sasquatch README while
lane `S107` is the onekey-sec sasquatch release page. **Verdict: positional drift, not duplicate staging**, so
the repair is `CORPUS.md` rule 2's renumber-by-document, never arithmetic.

Two stronger keys then found the duplicates the id check would have missed:

```console
$ python3 "$A/doc-join.py" SOURCES.base.md /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md "$A/doc-join.tsv"
staged=132 registry=129 same-document=0 drift-different-document=1 new-document=131 url_duplicates=4 weak_only_candidates=4
exit=0
```

| staged id | held by lane | basis | document |
|---|---|---|---|
| S107 | S111 | URL exact | `…/devttys0/sasquatch/master/README.md` |
| S122 | S116 | URL exact | `https://unblob.org/formats/` |
| S192 | S114 | URL exact | `…/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` |
| S216 | S125 | URL exact | `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` |
| S106 | S110, S117 | ref-pinned (`HEAD` vs `26.6.4`) | `…/onekey-sec/unblob/HEAD/README.md` |
| S109 | S129 | ref-pinned (`HEAD` vs commit `2671397…`) | `…/ReFirmLabs/binwalk/HEAD/README.md` |
| S183, S189 | S108, S112 | ref-pinned (`main` vs `26.6.4`) | `…/unblob/main/python/unblob/handlers/filesystem/squashfs.py` |

`renumber-map.tsv` is that table as data. The ref-pinned four are the class that bit round 41 differently: there
the repair *was* the pinning (`…/binwalk/HEAD/README.md` → `…/binwalk/2671397…/README.md`, round-41 Gate), so an
exact-string join now reports "new" for a document the lane already holds. The join is deliberately two-key for
that reason; the weak key is a hand-check candidate, never a verdict.

### Would the append gate refuse those four? (executed, not asserted)

`census-precheck.py` builds a scratch lane mirror (corpus/ + SKILL.md + PROVINCE.md + the two `used-by` targets
the baseline census reports missing), inserts the four URL-exact rows as `S238`–`S241` normalised to census
schema (recheck prose → `180d`, cells de-piped, `used-by corpus/lessons/round-42.md`), and validates:

```console
$ python3 "$A/census-precheck.py" <lane> <staged> "$S/work/precheck" "$G"
exit=0
$ sources-census.sh validate --file <mirror>/corpus/SOURCES.md     # baseline, no append
file … 13× W04, no E-code
file	ok	…/baseline/corpus/SOURCES.md                              exit=0
$ … validate --file <mirror>/corpus/SOURCES.md                     # with S238–S241 appended
file	W04	S238 duplicate url raw.githubusercontent.com/devttys0/sasquatch/master/README.md across scopes
file	W04	S239 duplicate url unblob.org/formats across scopes
file	W04	S240 duplicate url raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt across scopes
file	W04	S241 duplicate url download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os across scopes
file	ok	…/precheck/mirror/corpus/SOURCES.md                       exit=0
```

So the gate *warns*, it does not refuse — `scope_key = u SUBSEP scope` (`sources-census.sh:646-649`): same URL
with a different scope cell is W04, same URL with the same scope cell is E04. The four staged scope cells all
differ textually from the lane's, hence W04. **Fail-ability probe** (a gate that cannot fail proves nothing):
appending `S242` with lane `S111`'s scope cell verbatim gives

```console
file	E04	S242 duplicate url raw.githubusercontent.com/devttys0/sasquatch/master/README.md within scope sasquatch's self-description (patch set over unsquashfs for vendor-modified SquashFS) and source-build prerequisites only; not the onekey-sec packaged binary, not proof any image extracts
census exit=1
```

Two incidental facts the pre-check established, both worth carrying into any append this round:
(a) an EOF append lands **outside** the registry table — `corpus/SOURCES.md` has `## Registry` at :3 and
`## Paths` :138, `## Search log` :163, `## Leads (unopened)` :221, so a naive append yields
`E12 row outside Registry section` ×4 (observed); insert at the end of the table.
(b) the lane registry's own baseline is clean apart from 13 pre-existing W04 warnings and, in a partial mirror
missing `SKILL.md`/`corpus/QUALITY.md`/`tools/round-27/xpin-attribute.mjs`, three bogus `E11 missing used-by`.

---

## 2. Quarantine slice

```console
$ awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
    {print $4, $5}' "$R" > "$A/quarantine-slice"
awk exit=0
row count: 5
$ sha256sum "$A/quarantine-slice"
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  …/assimilation/quarantine-slice
$ cat "$A/quarantine-slice"
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

306 bytes, 5 lines, every line carries an S-id (`ok=5 bad=0`).

### Compare with round 41

Round-41 lesson (`git show c4a38ea…:corpus/lessons/round-41.md`, Gate § 59-62) records *"Quarantine slice: 5
rows, sha256 `7383a90e…28e6a`, byte-identical to rounds 38–40; nothing appended from it."* Verified against the
**committed artifact**, not the prose:

```console
$ git -C … cat-file -p c4a38ea…:.ufo/waves/round-41/w1/artifacts/R41Assim/assimilation/quarantine-slice > r41-quarantine-slice
$ sha256sum r41-quarantine-slice "$A/quarantine-slice"
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  r41-quarantine-slice
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  …/assimilation/quarantine-slice
$ cmp r41-quarantine-slice "$A/quarantine-slice" && echo "cmp: BYTE-IDENTICAL"
cmp: BYTE-IDENTICAL
```

**Same five rows, same order, same bytes, same sha256 as round 41** — the register has not been regenerated, so
round 42 inherits exactly round-41's quarantine state and appends nothing new from it (round-41's own verdict).
The register's header and `## By lane` totals remain stale as the prompt warns: line 254 says kaidoku has **1**
row while the derived slice has **5** (1 `payload-absent` + 4 prose-class), and the header claims 194
payload-absent rows overall — deriving the slice yourself is mandatory, confirmed.

### Row structure and a namespace defect (this round's new finding)

The five rows are not one schema. Field counts from the same `awk`:

```console
$ awk -F'|' -v l='kaidoku' '… {print NR": NF="NF"  id="$4}' "$R"
82: NF=9  id= S150
315: NF=7  id= S113`
316: NF=7  id= S117`
317: NF=7  id= S136`
318: NF=7  id= S147`
```

Rows 315–318 are degraded: the id cell carries a **trailing backtick** (`S113\``) and the register's class
vocabulary (`payload-absent` / `unreachable`) is replaced by the reason prose (`the cited source could not be
fetched…` / `the gate block named no locator…`) with the cited-source cell holding either a URL or a **local
Gate heading** (`## Gate — S136`, `## Gate — S147`). That is the register's unchecked family the prompt names —
unverifiable, never fabrication.

The new finding is the namespace. Resolving the slice against the lane registry by id and by URL:

| slice row | id in lane registry (`S001–S129`)? | lane row at that id | register's cited URL resolves in the lane registry? | in `SOURCES.append.md`? |
|---|---|---|---|---|
| `S150` | **no** (id > max) | — | no (zenn yasu01) | yes → staged `S150` |
| `S113` | yes, **different document** | unblob 26.6.4 test fixtures (BE v4) | no (`developer.android.com/tools/adb?hl=en`) | yes → staged `S113` |
| `S117` | yes, **different document** | unblob README at tag 26.6.4, format-count sentences | no (`doi.org/10.1109/SP46214.2022.9833799`) | yes → staged `S117` |
| `S136` | **no** | — | n/a (`## Gate — S136`) | no (staged `S136` cites the lane corpus file) |
| `S147` | **no** | — | n/a (`## Gate — S147`) | no (staged `S147` cites the HOST-CONTRACT path) |

**3 of 5 ids (`S136`, `S147`, `S150`) do not exist in the lane registry at all** (its max id is `S129`), and
**2 of 5 (`S113`, `S117`) point at a different document in the lane than the register's cited URL**. The three
external URLs that the register cites resolve *exactly* into `SOURCES.append.md` (`S113`, `S117`, `S150`), i.e.
the register's kaidoku ids are the **staging** id space (plus two own-work rows located by a Gate heading), not
the lane's. Consequence for the L1: **the quarantine slice must be applied by document, never by id** — an
id-joined hand-check would inspect the wrong lane rows (unblob fixtures for an adb page) and silently pass.

### Supplementary hand-check of the one `payload-absent` row (reproduces)

The single non-prose row is `S150` (staged row, lane does not hold it): register class `payload-absent`, cited
`https://zenn.dev/yasu01/articles/7370bd5d414ec4`, quote `` `シンボルがない場合のヒント` ``. Opened live
2026-10-26 in scratch:

```console
$ curl -sS -A 'Mozilla/5.0' -o zenn-yasu01.html -w 'http=%{http_code} bytes=%{size_download}\n' <url>
http=200 bytes=174088
$ sha256sum zenn-yasu01.html        -> 0ab0da3b2bb8913ed5f7e86f70aace2a00adbb973e51cada4994a70692f253b5
$ grep -c 'シンボルがない場合のヒント' zenn-yasu01.html      -> 0
$ grep -c '場合のヒント'            zenn-yasu01.html      -> 0
$ grep -o '<meta property="og:title" content="[^"]*"'  -> 実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む
```

The page served is the right article (`og:title` matches the staged row's title) and its 20 section headings
contain no `シンボルがない場合のヒント` and no `逆アセンブル` heading (`逆アセンブル` survives only inside
`Step 2：逆アセンブルしてエントリポイントを見る` and body prose). **The register's `payload-absent` verdict
reproduces on the live payload**; the staged row's second claimed anchor is also absent, so the row is
refuse-or-repair material for a future adoption. Per the prompt this is a hand-check note, not an adoption —
my seat appends nothing and the register stays untouched.

---

## Findings

| # | class | finding | evidence |
|---|---|---|---|
| F1 | checked, passes | 0–3-space guard catches an indented colliding id on a **census-valid** registry; the column-zero-only pattern false-greens | `guard/guard-proof.txt`, `guard/census-validate.txt` (exit 0) |
| F2 | expected state | 24 collisions, `S106`–`S129`, contiguous; **all 24 are positional drift**, not duplicate staging | `collisions`, `collision-documents.tsv` (24/24 `distinct`) |
| F3 | **defect (package)** | 4 staged rows duplicate a held document by **exact URL** (`S107`→`S111`, `S122`→`S116`, `S192`→`S114`, `S216`→`S125`) and 4 more behind a pinned ref (`S106`, `S109`, `S183`, `S189`); the id check alone cannot see them | `doc-join.tsv`, `renumber-map.tsv` |
| F4 | calibration | those 4 URL duplicates produce census **W04, not E04** (different scope cells), so the append gate passes them: `scope_key = url SUBSEP scope`; the same URL with the lane's scope cell does trip E04 | `guard/census-precheck.txt` (exit 0, 4×W04), `guard/census-precheck-e04-probe.txt` (E04, exit 1) |
| F5 | calibration | an append to EOF produces `E12 row outside Registry section`: this registry has three sections after the table | `guard/census-precheck.txt` first run; `corpus/SOURCES.md:138,163,221` |
| F6 | checked, unchanged | quarantine slice 5 rows, `7383a90e…28e6a`, **byte-identical** to round 41's committed artifact | `cmp` transcript above; `quarantine-slice-r41-committed` |
| F7 | **defect (register)** | the register's kaidoku ids are the **staging** namespace: 3/5 ids absent from the lane registry (max `S129`), 2/5 name a different document in the lane; 3/5 external URLs resolve exactly into `SOURCES.append.md` | join table above, `quarantine-slice-detail.tsv` |
| F8 | supplementary | the one `payload-absent` row reproduces on the live page (HTTP 200, quote absent, 20 headings) | fetch transcript above |

## Retained evidence

`.ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/` — 25 files, 61 765 bytes, `sha256sums.txt`:

- `reg-ids` 129 · `staged-ids` 132 · `collisions` 24 · `collision-documents.tsv` (24 rows) · `doc-join.tsv`
  (132 rows, 8 columns) · `renumber-map.tsv` · `quarantine-slice` · `quarantine-slice-r41-committed` ·
  `quarantine-slice-detail.tsv`
- `doc-join.py`, `census-precheck.py` (the two tools I authored; both read only their arguments and write only
  their outputs, no `/tmp`, no network)
- `guard/`: `registry-indented.md`, `staged.md`, `reg-ids-guard`, `staged-ids-guard`, `collisions-guard`,
  `reg-ids-zero-broken`, `staged-ids-zero-broken`, `collisions-zero-broken`, `census-validate.txt`,
  `guard-proof.txt`, `census-lane-baseline.txt`, `census-precheck.txt`, `census-precheck-appended-rows.txt`,
  `census-precheck-e04-probe.txt`

Not copied (cite only): the base registry (`sha256 3cf6cf99…8727`, rebuild with
`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:corpus/SOURCES.md`);
the live zenn page (`sha256 0ab0da3b2bb8913ed5f7e86f70aace2a00adbb973e51cada4994a70692f253b5`, rebuild with the
`curl` line above); `SOURCES.append.md` and the register (external, read-only).

## Risks and blockers for the L1

1. **Adoption must be document-keyed.** Any row taken from `merge/kaidoku/` this round must be matched by
   `doc-join.tsv`/`renumber-map.tsv` first: 8 staged ids name documents the lane already holds, and the 4
   exact-URL ones would pass the census as W04 if appended with a paraphrased scope (F3/F4). If the round adopts,
   the renumber map is staged id → lane id, and no staged row is appended as-is (recheck prose, escaped pipes —
   see the normalisation the pre-check had to perform on these four rows' cells).
2. **Do not apply the quarantine slice by id** (F7). Three of its ids do not exist in the lane; two name another
   document. Applying it needs the register's cited URL/heading, i.e. the staging id space, as the join key.
3. **The slice is unverifiable this round beyond reproduction** (F6/F8): it is unchanged since round 38 and only
   the single `payload-absent` row can be hand-checked against a live payload; the four prose-class rows are
   `unreachable`-family and must not be called fabrication. If the round wants adoption open, that is an L0
   decision on the two `## Gate — S136/147` locators, not something this seat can resolve.
4. **Census append mechanics** (F5): insert at the end of the `## Registry` table, not at EOF.
5. **No frozen-path contact**: I wrote only `.ufo/waves/round-42/w1/R42AssimIds.md` and this seat's artifacts
   directory; `corpus/SOURCES.md` is byte-identical to the base blob and no registry row was appended, so the
   C1/C2 freeze-integrity rule is untouched by this seat.

## Tooling, scratch and bounds

No tool was installed or upgraded (uv/npx/pacman unused); no REA, unblob, sasquatch, unsquashfs or 7z run was
needed for these checks. One network read: the single `curl` of the cited zenn article (HTTP 200), as the
register hand-check requires. `python3` 3.14 and GNU coreutils from the base system. Scratch was
`/fast/scratch/hyaku/kaidoku-r42/R42AssimIds` with `TMPDIR` inside it, and it has been removed (`test -e` false)
after every cited byte was copied into the artifacts directory; no third-party image or fixture was fetched, so
nothing third-party sits in the lane. No VCS mutation of any kind was performed; the only git calls were
`show`, `cat-file`, `log`, `rev-list`, `status` and `rev-parse`, each with `-C` naming the lane.
