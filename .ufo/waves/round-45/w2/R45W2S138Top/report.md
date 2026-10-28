# R45 W2 — the S138 correction, attacked

Seat `R45W2S138Top` (leaf, no dispatch). Lane `kaidoku`, round 45, wave 2 — adversarial
falsification of a landed, measured artefact.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base
`149133d47aa7e90796f96047afe6d251a3e65b2c`; freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`;
landing `e715263cb51b713c342ab992d527fe9d61d6f8ff` (2026-10-28T15:33:03Z); A1
`1f4b27f82353d6544dc0c8048b3cfdadd8525d12` (15:34:20Z, the first met measurement); A2
`fedd11bf5ff9fe42d061169f78d77df59af4eca1` (15:49:17Z); A3
`f59565b782c18b0eb691bec12f52d2f80d9f5032` (15:52:06Z, the measured revision per
`SCORECARD.md`); tip when this seat started `a63d109f` (15:58:04Z); tip when it finished
`0ee50aaf` (15:59:26Z, the wave-1 record commit — the tip moved under the seat; all named
revisions are ancestors of both tips, and every hash below was re-checked at `0ee50aaf`).

Read-only on the lane tree and the fleet repo: the only paths written are
`.ufo/waves/round-45/w2/R45W2S138Top{,.md}`. Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W2S138Top` (removed after the receipts were copied).
No git/jj mutation; git commands used were `rev-parse`, `log`, `show`, `ls-tree`,
`merge-base --is-ancestor`, `status --porcelain`. Nothing installed (`curl`, `python3`,
`sha256sum`, `awk` sufficed; pacman untouched).

## 0. What I attacked, and the verdict

| # | attack | target | verdict |
|---|---|---|---|
| A1 | Re-fetch `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` live; record status, bytes, sha256, UTC and the entries it lists | correction's central claim "this round fetches the top URL itself" | **holds** (§1) |
| A2 | Second live fetch; compare bytes and parsed listing; compare both against the wave-1 pair | same claim + R45-CL12's per-request-digest statement | **holds as a class**; the "667 bytes" figure is not an invariant and is no longer checkable (§1.3, F6) |
| A3 | Read the S138 row field-by-field and check each clause of the correction against it | `corpus/SOURCES.md:144` (11 columns) | **falsified in two clauses** (F2, F3) |
| A4 | Check "round 44 opened its descendants instead" against the round-44 oracle manifest and every round-44 saved HTML page | correction clause 2 | **holds** (bounded negative, §2 C2) |
| A5 | Check "22 members, 4 endian trees" against the committed evidence tree and the manifest counters | correction's evidence clause | **holds** (§2 C7) |
| A6 | Run the registry's own append-only gate `tools/round-38/registry-immutable.sh` base→A1/A3/tip, plus a line-hash and diff check | correction label "append-only (no column edited)" | **holds** (§3) |
| A7 | Grep every round-45 claim surface for S138 | correction clause "no round-45 claim cites S138" | **holds** (§4) |
| A8 | Check whether the receipt the correction cites resolves at the revisions the round measured | `This round fetches ... (receipt .ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md)` | **falsified at landing, A1, A2, A3 and the A3 record commit** (F1) |
| A9 | Check M45-2's fix-cell enumeration ("HTTP status, bytes and sha256, the located quote is recorded") | `corpus/lessons/round-45.md:17` | **partly falsified** (F4); the "sha256" half is self-cancelling (F4b) |
| A10 | S138's `used-by` against the round's own precedent for S140/S141 | correction's last sentence | **holds as stated, calibration call for L1** (F5) |

Severity-ordered findings are in §5; residual risk and verification gaps in §7.

## 1. Receipts

All times UTC. `S=/fast/scratch/hyaku/kaidoku-r45/R45W2S138Top`, `TMPDIR=$S`; no `/tmp` writes.
Receipt artefacts copied to `receipts/` beside this file.

| # | command (exact, abridged only where marked) | exit | HTTP | bytes | sha256 (body / stdout) | UTC |
|---|---|---|---|---|---|---|
| R1 | `curl -sS -L --max-time 60 -D f1.hdr -o f1.html -w '%{http_code}\|%{size_download}\|%{num_redirects}\|%{url_effective}' 'https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs'` | 0 | 200 | 238,204 | `647c6a981042a2c0e9068adf96b414e795432de6c2192c2b07209320b12cea75` | 16:00:29Z→16:00:30Z |
| R2 | same URL, `-o f2.html`, no `-D` | 0 | 200 | 238,204 | `ca8587a039abd11c1931c5d7c488a5c537f3dacf11622ab77405d59254a4706c` | 16:00:49Z |
| R3 | `curl -sS -L -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs?ref=26.6.4' -o api1.json` | 0 | 200 | 11,007 | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` | 16:00:49Z→16:00:50Z |
| R4 | same contents-API URL again, `-o api2.json` | 0 | 200 | 11,007 | `be3180fc…` **byte-identical to R3** | 16:00:50Z |
| R5 | `curl -sS -L 'https://api.github.com/repos/onekey-sec/unblob/git/ref/tags/26.6.4' -o tag.json` | 0 | 200 | 382 | `refs/tags/26.6.4` → `commit 1fcc7a0a584a70a96c31f5a276c20944d199a089` | 16:00:50Z |
| R6 | `bash registry-immutable.sh <LANE> 149133d4 <rev>` for rev ∈ {A1, A3, tip `a63d109f`} (lane bytes, script sha256 `b3ea8fc7e36fa8be…`) | 0,0,0 | — | 0 B stdout each | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty ⇒ no row changed outside status/recheck/used-by) | 16:03:41Z |
| R7 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | — | 1,518 B | `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19`; 14 × `W04` (S138 among them), `kaidoku ok` | 16:03:47Z |
| R8 | `python3` parse of R1's embedded payload (`payload.codeViewTreeRoute.tree.items`) | 0 | — | 11 items | items-JSON sha256 `236177929362501b8c1eb9586cb26465f640e525bd672ae78f50f913765e5463` | 16:04Z |

R1's response headers (`receipts/f1.hdr`): `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
`x-github-request-id: 58F9:22277:CC6B62:144753C:6AE21C1D`. No `content-length` header; size is
`%{size_download}`. `num_redirects=0` and `url_effective` is the URL unchanged.

### 1.1 What the top URL lists (R1/R8), verbatim

`<title>` — `unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub`
(byte 27,143 of 238,204). Then exactly **11 entries, every one a directory, zero files**:

```
squashfs_v1            squashfs_v2              squashfs_v2_nonstandard
squashfs_v3            squashfs_v3_adaptive     squashfs_v3_broadcom
squashfs_v3_ddwrt      squashfs_v3_nonstandard  squashfs_v4_be
squashfs_v4_broadcom   squashfs_v4_le
```

The contents-API body for the same path (R3) lists the same 11 `type: "dir"`, `size: 0` entries,
in the same order. Occurrences in the 238,204-byte page, all **0**: `__output__`,
`squashfs_v2.0_be.bin_extract`, `little_endian`, `NOT handler code`, `oid sha256`. So the page
confirms the path at tag `26.6.4` and two of its children; it carries none of the row's scope
(byte orders, `__output__`, 22 members, LFS hashes).

### 1.2 The tag

`refs/tags/26.6.4` → `commit 1fcc7a0a584a70a96c31f5a276c20944d199a089` — the commit the S138
`source` cell pins. Holds.

### 1.3 R1 vs R2 — the pair is not byte-stable, and neither is the wave-1 figure

Same length (238,204), different digests; **179 differing bytes**, first at offset 27,734, last
at 28,307 (the `fetch-nonce`/request-id region). The parsed 11 entries are **equal** across the
pair. The wave-1 receipt reports a *different* pair: 238,102 B, 667 differing bytes, differences
from 27,429 to 175,633.

Consequence: the invariant is "two fetches of this URL are never byte-identical, but the parsed
directory list is" — not any byte count. R45-CL12's "differ in 667 bytes"
(`corpus/lessons/round-45.md:133`) is a property of that one pair, and its inputs were not
committed (the wave-1 scratch was deleted), so 667 cannot be re-derived by anyone. See F6.

## 2. The correction paragraph, clause by clause

Text as landed (`corpus/lessons/round-45.md:36-46`, unchanged from `e715263` through
`0ee50aaf`; the A2/A3 diffs touch other hunks only):

> **C1** "The row's top URL `…/squashfs` is the endpoint the `opened` cell names" ·
> **C2** "round 44 opened its descendants instead (contents-API listings under
> `squashfs_v1|v2/.../__output__`)" ·
> **C3** "This round fetches the top URL itself (receipt `.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md`)" ·
> **C4** "so the cell's claim is true as of 2026-10-28 and false as of 2026-10-28T11:12Z" ·
> **C5** "The column cannot be edited (CORPUS rule 2: a row present at BASE may differ only in
> status, recheck, used-by)" ·
> **C6** "the row is `mined`" ·
> **C7** "the evidence is the descendant member set (22 members, 4 endian trees) plus this
> round's live top-page fetch" ·
> **C8** "no `used-by` row is added because no round-45 claim cites S138"

| clause | verdict | evidence |
|---|---|---|
| C1 | **falsified** | the `opened` cell is `2026-10-28` — a date, not an endpoint. The census enforces exactly that (`scripts/sources-census.sh:27`, `E08 opened not a past/present ISO date`; parse of column 10 at `:627,:660`). The URL lives in the `source` cell (column 2). Under the other available reading — the round-44 Gate cell, whose `opened` column *does* carry prose — that cell names the **descendant** contents-API endpoints, i.e. the opposite of what C1 says. F2. |
| C2 | **holds** | manifest `corpus/evidence/round-44/oracle/manifest.json` (sha256 `06a72dd5…f5fe`): 10 listings, every `repo_path` under `tests/integration/filesystem/squashfs/squashfs_v{1,2}/{little,big}_endian/__output__[/…]`, all `replayed_from_saved_receipt: true`, `started_at == finished_at == 2026-10-28T11:12:37Z`. Of the 5 HTML pages saved anywhere in the round-44 wave tree, only one is unblob's: `R44MistakeHunt/tree-200.html`, `og:url = …/squashfs_v2/big_endian/__output__` (2 items, both `.bin_extract`). No round-44 artefact saves the top URL. Bounded negative: a live fetch that left no artefact cannot be excluded, but nothing in the lane records one. |
| C3 | **falsified at every measured revision** | the cited path has **0 entries** in `git ls-tree -r <rev> -- .ufo/waves/round-45/w1/R45W1SrcS138Fix` at `e715263`, `1f4b27f8`, `fedd11bf`, `f59565b7`, `1d04c6af`, `a63d109f`; it first appears at `0ee50aaf` (2026-10-28T15:59:26Z, `--diff-filter=A`). Its own first fetch is stamped `2026-10-28T15:39:00Z` — **5 m 57 s after the landing commit**. The act is real (R1/R2/R3 reproduce it); the pointer is not. F1. |
| C4 | **falsified** | (i) the row did not exist at 11:12Z: S138 entered `corpus/SOURCES.md` at `b2a1bd91` (author 2026-10-28T11:21:40Z, commit 11:59:37Z); "the cell's claim is false as of 11:12Z" asserts a falsehood about a cell that was not yet written. (ii) the truth instant is date-granular while the falsity instant is minute-granular, so a literal reading makes the same calendar day both true and false; the receipt supplies the instant (15:39:00Z) and R1 supplies a re-verification (16:00:29Z). F3. |
| C5 | **holds** | `tools/round-38/registry-immutable.sh:2-4` states the same rule ("only status, recheck and used-by may differ at REV"), matching `SKILL.md:1607`. The gate's own run over base→A1/A3/tip exits 0 with empty stdout (§3). |
| C6 | **holds** | column 8 = `mined`. |
| C7 | **holds on committed bytes** | `find corpus/evidence/round-44/oracle -type f ! -name manifest.json` → 22 files, 152 B total, 7 distinct sha256, 4 `__output__` directories (`squashfs_v{1,2}/{big,little}_endian`); manifest `counts` agrees (`files 22, total_bytes 152, distinct_content_sha256 7, failures 0`). |
| C8 | **holds as written; calibration call** | `grep -rn S138 plans/round-45-claims.md SKILL.md tools/round-45/` → no match (the `tools/round-44/*` matches are round-44 instruments and `plans/round-44-claims.md` is round 44). But see F5: the same round set `used-by corpus/lessons/round-45.md` on S140/S141, and this lesson cites S138. |

## 3. Is it append-only (no column edited)?

Yes, three ways, all read-only:

1. **Row bytes.** `git show <rev>:corpus/SOURCES.md | grep '^| S138 |' | sha256sum` =
   `fbfb0186e09836b45d3baf9ea1a2358dfe78a4eb2536fa645c397a2056f8f2ba` at base, freeze, landing,
   A1, A3 and tip. The row is still line 144 at the tip.
2. **File shape.** `corpus/SOURCES.md` 160,905 B / 243 lines (139 registry rows) at base →
   162,110 B / 245 lines (141 rows) at the tip; `git diff <base>..<tip> -- corpus/SOURCES.md` is
   **2 insertions, 0 deletions** — S140 and
   S141 only. `corpus/SOURCES.md` sha256 at the tip is `70be416d0294871d969b587bd4eb2f4980bc46f1d8faa9636ecf0176edbc401a`,
   the same digest the wave-1 receipt read.
3. **The registry's own gate.** `registry-immutable.sh <LANE> 149133d4 {A1,A3,tip}` → exit 0,
   empty stdout, three times (R6). No row changed outside columns 9/11/12, no row deleted, no
   reorder.

Also unchanged across base→tip: `corpus/lessons/round-44.md`,
`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, `corpus/evidence/round-44/oracle/manifest.json`
(`git diff --stat` all empty), so the correction did not rewrite the round-44 record either.
Census at the tip: exit 0, 14 × W04, S138 still one of them (R7) — the correction adds and removes
no duplicate-URL warning.

## 4. Does any round-45 claim cite S138 (it should not)?

No. `grep -rn S138 plans/round-45-claims.md SKILL.md tools/round-45/` → 0 matches;
`tools/round-45/registry-scope.json` names instruments, not sources. The round-45 documents that do
mention S138 are the wave spec/dispatch files (`w1-spec.json`, `w1-dispatch.json`, `w2-spec.json`,
`w2-dispatch.json`, `r45-w1-results.json` — seat prompt text), `SCORECARD.md` §Round 45 ("the S138
`opened` over-claim is corrected append-only with a live fetch"), `LOG.md:3204,3205,3265`, and the
lesson itself (M45-2 + the correction): record prose and prompt text, none of them a claim. So C8's
premise is true.

## 5. Findings

### F1 — the correction's evidence pointer is dangling at every revision the round measured (medium-high; the one to route)

*Attacks:* C3 and, transitively, `SCORECARD.md` §Round 45's "corrected … with a live fetch".

Input → differing value:

```
git -C <LANE> ls-tree -r --name-only <rev> .ufo/waves/round-45/w1/R45W1SrcS138Fix | wc -l
e715263cb51b  1f4b27f82353  fedd11bf  f59565b7  1d04c6af  a63d109f  →  0 0 0 0 0 0
0ee50aaf                                                                 →  1
```

and the receipt's own first fetch (`R1`, report §1) is `2026-10-28T15:39:00Z`, while the landing
commit is `2026-10-28T15:33:03Z` and A1 is `15:34:20Z`. So: at landing and A1 the cited act had not
yet happened; at A2 (15:49Z), A3 (15:52Z) and at `1d04c6af` — the commit that *declares* A3 the
measured revision — the act had happened but its receipt was not in the tree. It is citable only
from `0ee50aaf`, 6+ minutes after the era's last measurement, and only because that commit later
became the tip.

Why it matters here specifically: the round's own M45-2 class is "a receipt discipline"; a
correction that fixes an unbacked credit with a credit to a file that does not exist at the
measured revision repeats the class in a new place. No instrument catches it — `c1-counter.py`
checks `SKILL.md` citations, `c2-counter.py` checks registry rows, the census checks `used-by`
paths, and none of them reads a prose path in a lesson.

Fix (either): (a) land the receipt at or before the revision that is called measured — e.g. put
`report.md` (or a 2 KB copy under `corpus/evidence/round-45/`) in the A-stage commit, and re-run
the two counters; or (b) keep A3 as measured and add one append-only sentence naming the commit
that first contains the receipt (`0ee50aaf`) plus the stable identity below, so a reviewer at A3
knows the pointer is forward. Do not silently re-point the sentence at HEAD.

Disclosure for the L1: the whole `w1/<seat>/` tree lands at `0ee50aaf`, so the lesson's other
seat-report citations (M45-3's `R45W1CritC1`/`R45W1CritC2`) are forward references too. This is a
round-wide convention question, not an S138-only slip — but C3 is the only citation that carries a
*fetch* claim, where "the act postdates the landing commit" is independently checkable.

### F2 — "the endpoint the `opened` cell names" is not what the cell holds (medium)

*Attacks:* C1.

Input → differing value: `corpus/SOURCES.md:144`, column 10, is `2026-10-28` — 10 characters, no
URL. `scripts/sources-census.sh` treats the column as an ISO date and rejects anything else (`E08`,
parse at `:627`, epoch check at `:660-662`). The URL C1 quotes is column 2 (`source`). If the
sentence is instead read against the round-44 Gate cell, that cell names
`api.github.com/…/squashfs_v{1,2}/{little,big}_endian/__output__?ref=26.6.4` — descendants.

Fix: "The endpoint the row credits — the one in its `source` cell — is
`…/squashfs`; the `opened` date is what inherits the credit."

### F3 — the truth/falsity instants are anachronistic and mismatched in granularity (medium)

*Attacks:* C4.

Input → differing value: `git show b2a1bd91:corpus/SOURCES.md | grep -c '^| S138 |'` → 0 before
that commit; the row first exists at `b2a1bd91`, authored `2026-10-28T11:21:40Z` (committed
`11:59:37Z`). The correction's falsity instant `2026-10-28T11:12Z` precedes the row by ~9 minutes
(author) / ~47 minutes (commit), so no "cell's claim" was false then — the fact was. And the truth
side is date-granular, so "true as of 2026-10-28 … false as of 2026-10-28T11:12Z" is only coherent
if the reader supplies the ordering from context.

Fix (values from the receipts): "the document had not been opened as of round 44's last listing
(2026-10-28T11:12:37Z); the row has asserted `opened 2026-10-28` since it was created
(`b2a1bd91`, 11:21:40Z) without a top-URL fetch; the top URL was first fetched at
2026-10-28T15:39:00Z and re-fetched at 2026-10-28T16:00:29Z, so the date is true from
15:39:00Z."

### F4 — M45-2's fix cell over-states what exists (low)

*Attacks:* `corpus/lessons/round-45.md:17`, "the top URL is fetched live this round with its HTTP
status, bytes and sha256, the located quote is recorded, and the Gate states which endpoints were
actually opened."

(a) *Located quote.* There is no S138 row in the round-45 Gate table (only S140, S141) and the
correction paragraph quotes nothing. The only located text anywhere is the page `<title>`
(9 words; wave-1 receipt §3, byte 27,041 of its page), which the same receipt rules insufficient for the row's scope: "The top
page carries **no prose at all**, so no sentence can be mined for the scope predicate." A reader
told "the located quote is recorded" will look for a scope-supporting quotation and find none.

(b) *sha256.* The same lesson's R45-CL12 says an HTML digest here "is not a page identity". The
fix cell nonetheless lists "sha256" as part of what was captured; the receipt records it with the
caveat, the fix cell does not.

Fix: "…its HTTP status and byte count; the only located text is the page `<title>`, which confirms
the path at tag `26.6.4` and not the row's scope; the citable identity is the contents-API body
(`11,007 B`, sha256 `be3180fc…`), stable across four fetches from two seats."

### F5 — `used-by` left short of the round's own precedent (low; L1's call)

*Attacks:* C8's conclusion, not its premise.

S140 and S141 carry `used-by corpus/lessons/round-45.md` because block 22 cites them. The round-45
lesson cites S138 in M45-2 and in this correction, and rule 2 *permits* `used-by` edits, so leaving
S138's `used-by` at the round-44 knowledge entry only is a choice, not a constraint. C8's stated
reason ("no round-45 claim cites S138") is true, so the sentence is not false — but the
justification answers a narrower question than the cell's semantics. Recommend either extending
`used-by` with `corpus/lessons/round-45.md` (E11 passes: the path exists) or stating the narrower
sense: "no round-45 *claim* cites S138, so the cell is left at the round-44 entry; the lesson cites
it only as the object of this correction."

### F6 — R45-CL12's "667 bytes" is unreproducible and not an invariant (low; residual risk)

*Attacks:* `corpus/lessons/round-45.md:132-135`.

R1/R2 give 179 differing bytes in the offsets 27,734–28,307 with equal length; the wave-1 pair was
667 differing bytes spanning 27,429–175,633 at length 238,102. So the count and even the mutated
span differ per pair: the digest varies, the listing does not (items-JSON sha
`2361779293…` here; 11 entries in both seats). The *class* claim holds; the *number* should not be
quoted as a measurement a future row can check, and the pages it was derived from are gone.

Fix: replace the figure with the invariant — "two fetches of this URL are never byte-identical
(the per-request nonce region differs; the parsed 11-entry listing is identical), so cite the
listing and the contents-API body, never the HTML digest."

## 6. What holds, stated so the L1 can cite it

- The top URL is live: HTTP 200, no redirect, 238,204 B, sha256 `647c6a98…`, 2026-10-28T16:00:29Z;
  it is a pure directory index of **11 directories, 0 files**, and contains none of the row's
  scope tokens.
- Its stable identity is the contents-API body `11,007 B`, sha256 `be3180fc…`, byte-identical on
  two fetches now **and** to both wave-1 fetches (15:39:20Z, 15:40:42Z) — four fetches, two seats,
  ~21 minutes apart.
- Tag `26.6.4` still resolves to `1fcc7a0a584a70a96c31f5a276c20944d199a089`.
- Round 44 opened only descendants (10 contents-API listings, 4 `__output__` trees, one descendant
  HTML page); no artefact of round 44 saves the top URL.
- The row is intact: line-hash identical at base/freeze/landing/A1/A3/tip; the append-only gate
  exits 0 three ways; `SOURCES.md` grew by exactly two rows.
- The declared descendant evidence is real on committed bytes: 22 files / 152 B / 7 distinct
  sha256 / 4 `__output__` directories, matching the manifest's `counts` and the row's anchor cell.

## 7. Residual risk and verification gaps

- **The wave-1 pair is unverifiable.** Its two 238,102-byte pages were in scratch and are gone;
  667 is a self-reported number. Reproducing the class (done) is not reproducing the figure.
- **"Round 44 never fetched the top URL" is bounded to saved artefacts.** A live fetch that wrote
  no receipt leaves no trace; I checked the 5 saved HTML pages, the oracle manifest, and the 34
  round-44 files that mention the top URL (citations, wave specs, prompts — none a fetch receipt
  for it).
- **The 15:39:00Z fetch is self-reported** by the seat that made it. I corroborate the *state*
  (page live, same 11 entries, same contents-API digest) but not that instant.
- **A1's "first met measurement" and A3's "measured revision" both precede their evidence pointer**
  (F1). I did not re-run the C1/C2 counters (other seats own them); I only checked the citation
  they do not read.
- **The tip moved under this seat**: HEAD was `a63d109f` (15:58:04Z) when the seat started and
  `0ee50aaf` (15:59:26Z, the wave-1 record commit) when it finished. Every named revision is an
  ancestor of the current tip, and every hash above was re-checked at `0ee50aaf`; if the tip moves again, the F1 command is the one to re-run.
- **One process slip, disclosed:** the first write of this report resolved against the fleet root
  and created `/home/vgpnk/Projects/shokunin/.ufo/waves/round-45/w2/R45W2S138Top/report.md`. It was
  copied into the lane at the path above, and the fleet-root tree it had created
  (`round-45/{,w2/{,R45W2S138Top}}`, containing only that file) was removed; the fleet repo's only
  `round-45` status entry afterwards is the L1's own `.ufo/reports/round-45/kaidoku.md`, and no
  tracked file was touched.
- **Not run:** no mutation of any lane file; no fixture repository was needed (the two git-level
  attacks are pure reads against the lane's own history); no counter re-measurement; no install.

## 8. Receipts

`receipts/f1.hdr` (R1 headers), `receipts/api1.json` (R3 — the citable identity),
`receipts/tag.json` (R5), `receipts/top-listing.json` (R8, 11 entries + page hash/bytes/UTC),
`receipts/census-validate.txt` (R7), `receipts/gate/out-<rev>.txt` (R6, three empty stdout files
whose emptiness *is* the pass, with the exit codes and stdout hash recorded in §1). Page bodies
from R1/R2 were deliberately not retained: by the round's own finding they are not identities;
their digests, sizes and the parsed listing are in `receipts/top-listing.json`. Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W2S138Top` was removed after this copy.
