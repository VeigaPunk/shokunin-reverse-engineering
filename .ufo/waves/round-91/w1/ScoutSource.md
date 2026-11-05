# ScoutSource — S313 re-open, round 91 (wave `r91-w1`, seat `ScoutSource`)

**Item.** Re-open the frozen source row **S313** (UPX v5.2.0 `src/p_unix.cpp`) and record the access
evidence for the round's sourced claim (R91-C1's knowledge entry
`corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md`). Read-only; nothing written to the corpus.

- **Access date (UTC):** `2026-11-05` (`date -u +%Y-%m-%d` → `2026-11-05`).
- **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; no lane file touched).
- **Scratch:** `S=/fast/scratch/hyaku/kaidoku-r91/ScoutSource` (removed before yield).
- **Tools:** `curl 8.23.0` (OpenSSL 3.6.5), `coreutils sha256sum`/`stat`, `git` (read-only `ls-remote`).
  No installs or upgrades were performed this seat, so no pacman transaction and no tooling-channel
  record is required (the operator tooling directive was read at `/home/vgpnk/.omp/agent/RULES.md`).

---

## 1. Access record — v5.2.0 (the row's canonical URL)

| field | value |
|---|---|
| URL | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` |
| HTTP status | `200` |
| sha256 | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` |
| size | `24181` bytes |

Commands (exit codes as returned):

```
curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp -o "$S/p_unix_v520.cpp"
  → curl_v520_rc=0
curl -o /dev/null -s -w '%{http_code}' https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp
  → status_v520=200
sha256sum "$S/p_unix_v520.cpp"
  → bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e
stat -c '%s bytes' "$S/p_unix_v520.cpp"
  → 24181 bytes
curl -sIL -o /dev/null -w 'final_code=%{http_code} url=%{url_effective}\n' <same URL>
  → final_code=200 url=https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp
```

**Row match.** The row's recorded sha256 (`bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`)
and size (`24181`) reproduce exactly. The row is **confirmed** on its own recorded values.

**Tag resolved to a commit, and the commit serves the same bytes** (independent of the tag-name URL):

```
git ls-remote https://github.com/upx/upx.git 'refs/tags/v5.2.0*'
  → bc521d8d825298cffd342d6de8ec0bc397ad6849  refs/tags/v5.2.0        (annotated tag object)
  → 034b6d0d81c53998c07ad6f34bfead6f5c5445ce  refs/tags/v5.2.0^{}     (the commit)
curl -fsSL https://raw.githubusercontent.com/upx/upx/034b6d0d81c53998c07ad6f34bfead6f5c5445ce/src/p_unix.cpp
  → rc=0, sha256 bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e, 24181 bytes
cmp -s <commit-fetch> <tag-URL-fetch>  → BYTE-IDENTICAL to tag-URL fetch
```

The tag-name URL and the tag's commit URL serve identical bytes, so the row's URL is stable and
content-addressed by the tag commit `034b6d0d…`.

## 2. The four pinned line numbers on v5.2.0

`grep -n -F <pattern> "$S/p_unix_v520.cpp"` (each pattern searched literally):

| # | pattern | expected | **measured** | verdict |
|---|---|---|---|---|
| 1 | `unpackExtent(unsigned wanted` | 476 | **476** | match |
| 2 | `fi->readx(&hdr, szb_info);` | 485 | **485** | match |
| 3 | `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)` | 496 | **496** | match |
| 4 | `fi->readx(ibuf+j, sz_cpr);` | 504 | **504** | match |

All four expectations reproduce; 4 of 4.

Context at the decode-side bound (v5.2.0), which is the check the round's claim rests on:

```
493:        }
494:        if (sz_unc <= 0 || sz_cpr <= 0)
495:            throwCantUnpack("corrupt b_info");
496:        if (sz_cpr > sz_unc || sz_unc > (int)blocksize)
497:            throwCantUnpack("corrupt b_info");
```

So the row's own quoted anchors — line 472 comment, 485 `fi->readx(&hdr, szb_info);`, 497
`throwCantUnpack("corrupt b_info");`, 504 `fi->readx(ibuf+j, sz_cpr);` — and the round's citation of
line 496 all hold on the bytes the row names. The v5.2.0 `unpackExtent` loop reads a 12-byte `b_info`
header, then exactly `sz_cpr` payload bytes, so the next header's offset is a function of the stored
`sz_cpr` value — the chain law S313 is admitted for.

## 3. Access record — upstream `master`

| field | value |
|---|---|
| URL | `https://raw.githubusercontent.com/upx/upx/master/src/p_unix.cpp` |
| HTTP status | `200` |
| sha256 | `6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3` |
| size | `24365` bytes |
| master HEAD at access | `7c7bea44146c7ad6e17cb2d0bb9566805b44a91a` (`git ls-remote … refs/heads/master`) |

```
curl -fsSL https://raw.githubusercontent.com/upx/upx/master/src/p_unix.cpp -o "$S/p_unix_master.cpp"
  → curl_master_rc=0
curl -o /dev/null -s -w '%{http_code}' <master URL>  → status_master=200
sha256sum → 6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3
stat -c '%s bytes' → 24365 bytes
curl -fsSL https://raw.githubusercontent.com/upx/upx/7c7bea44146c7ad6e17cb2d0bb9566805b44a91a/src/p_unix.cpp
  → rc=0, sha256 6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3, 24365 bytes
```

The `master` branch URL and the pinned master commit serve identical bytes.

## 4. Master: the same four lines at the same numbers?

| # | pattern | v5.2.0 | **master** | same number? |
|---|---|---|---|---|
| 1 | `unpackExtent(unsigned wanted` | 476 | **479** | no — shifted +3 |
| 2 | `fi->readx(&hdr, szb_info);` | 485 | **488** | no — shifted +3 |
| 3 | `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | 496 | **499** | no — shifted +3 |
| 4 | `fi->readx(ibuf+j, sz_cpr);` | 504 | **ABSENT** | **the line no longer exists** |

Line 4 is gone on master: `grep -n -F 'ibuf+j' "$S/p_unix_master.cpp"` → no match; the payload read
is now `506: fi->readx(cbuf, sz_cpr);` preceded by `505: MemBuffer cbuf(sz_cpr);`. The in-place
overlapping-decompression placement was replaced by a separate buffer.

**Is the decode-side check at line 496 unchanged on master?** — **Yes, semantically and textually; only
its line number moved.** The check's source text is byte-identical:

```
499:        if (sz_cpr > sz_unc || sz_unc > (int)blocksize)
500:            throwCantUnpack("corrupt b_info");
```

and it sits in the same place in the same loop (immediately after
`if (sz_unc <= 0 || sz_cpr <= 0) throwCantUnpack("corrupt b_info");` at 497-498, immediately before
the payload read). The bound is still the decoder's only per-block arithmetic check: the next header
is still not cross-checked. The +3 shift comes from three added lines upstream of the function (not
from any change to the bound itself).

**The chain law still holds on master.** The master payload read is still `fi->readx(cbuf, sz_cpr)` —
exactly `sz_cpr` bytes consumed from `fi` between two `b_info` header reads — so the "next header
begins exactly `sz_cpr` bytes later" property the S313 row is admitted for is preserved. Only the
*destination buffer* of the read changed (`ibuf+j` → a fresh `MemBuffer cbuf`).

## 5. Where the drift landed (extra: recheck-relevant)

Same measurement across the upstream tags, to bound the drift window for the row's `recheck` field
(row currently `on-release`):

| upstream ref | sha256 | bytes | `unpackExtent` | `readx(&hdr,…)` | bound | payload read |
|---|---|---|---|---|---|---|
| `v5.2.0` | `bf83c413…642e` | 24181 | 476 | 485 | **496** | `fi->readx(ibuf+j, sz_cpr);` @504 |
| `v5.2.1` | `99710306591d0ff7b69e337e37db533763d82cde41ae12f14d4198d9903c38dd` | 24482 | 479 | 488 | **499** | `fi->readx(ibuf+j, sz_cpr);` @507 |
| `v5.3.0` | `6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3` | 24365 | 479 | 488 | **499** | `fi->readx(cbuf, sz_cpr);` @506 (`ibuf+j` absent) |
| `master` (= `v5.3.0` bytes) | `6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3` | 24365 | 479 | 488 | **499** | `fi->readx(cbuf, sz_cpr);` @506 (`ibuf+j` absent) |

`cmp -s master v5.3.0` → identical bytes for `src/p_unix.cpp`.

Reading of the drift, for the row's `recheck` field (the row is tag-pinned at `v5.2.0`, so this is a
**drift record, not a failure**):

- The row's own content is **unaffected**: `v5.2.0` still serves the recorded bytes and the recorded
  line numbers (4 of 4 anchors reproduced). The row's `recheck: on-release` is satisfied for the
  pinned ref — a re-open at `v5.2.0` reproduces the sha256, the size and all four cited line numbers.
- What drifted is **upstream master relative to the pinned tag**: a +3 line shift and the
  `ibuf+j` → `cbuf` payload-read rewrite. The rewrite landed between `v5.2.1` and `v5.3.0`.
- The **decode-side bound at 496 is preserved** through every upstream ref measured
  (`v5.2.0` → `v5.3.0` → `master`), so the round's claim — that the bound is the decoder's only
  per-block arithmetic check and the refusal therefore has to follow `upx -t` — is not contradicted by
  upstream's later work.

## 6. Scope, and what was *not* done

- Read-only against the lane and against `upx/upx`; **no corpus file, no lane file and no registry row
  was created, edited or deleted** by this seat. The only files written are this report and its three
  attached artifacts inside this seat directory (below).
- No measurement of R91-C1's or R91-C2's counters was attempted here; this seat's item is the source
  access record only.

## 7. Files written by this seat

| path (absolute) | sha256 / size |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ScoutSource.md` | this report (the `Report:` trailer path) |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ScoutSource/p_unix_v520.fetched.cpp` | `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` / 24181 B |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ScoutSource/p_unix_master.fetched.cpp` | `6b17409f51fe087ded4d843f497df1458e982dcc0ff77b208ba427fa76a0aed3` / 24365 B |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ScoutSource/p_unix_v520_vs_master.diff` | `9869845448aa23a59d02889dd26b0da3b7891e1ec7b08830019f80d6ff088dcf` / 4259 B (`diff -u`, exit 1 = differences present) |

Scratch dir `/fast/scratch/hyaku/kaidoku-r91/ScoutSource` deleted before yield.
