# R35Audit01 — Reopen S125 live: exact quote/anchor verification

- Seat: R35Audit01 (executor, leaf). Item: "Reopen S125 live and verify exact quote/anchor. Read-only or private /tmp only; no lane writes."
- Measured revision: HEAD `3ecf4298` ("round-35: commit failing do-nothing controls before claim data (C1/C2 exit 1)"). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Constraints honored: read-only lane access; only writes are this report; /tmp used for fetched bytes; no find/du under /fast/scratch; no delegation/background; no VCS mutation; no lane production file touched.

## Verdict

HOLDS — the S125 source (jsc2js README) is live, the prep capture `jsc2js-readme.md` is **byte-identical** to the live raw bytes at audit time, the anchor headings are present in both, and every candidate quote checked exists verbatim in both. No falsification found.

## Evidence (commands, output, limits)

### 1. Live fetch vs capture — byte identity

```
curl -sS -o /tmp/s125-readme-live.md -w "http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" \
  https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md
→ http=200 bytes=8996 url=https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md
sha256sum /tmp/s125-readme-live.md .ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md
→ df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3  (both)
diff -q /tmp/s125-readme-live.md .ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md; echo $?
→ 0
```

Capture bytes: `jsc2js-readme.md` 8,996 B, sha256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`.
Sibling captures (recorded, S129 scope — outer audits R35Audit02/03): `releases-page1.json` 631,043 B sha256 `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c`; `releases-page7.json` 487,166 B sha256 `499e2b227a6eb2c3053a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc`.

### 2. Repository identity / anchor URL validity

```
curl -sS https://api.github.com/repos/xqy2006/jsc2js   (HTTP 200)
→ full_name=xqy2006/jsc2js  default_branch=main  archived=False
  pushed_at=2026-10-21T08:53:24Z  open_issues_count=15  stargazers_count=119
```

- Raw anchor `https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md` resolves (200) and `main` is the default branch. Repo not archived.
- The selftest/claims source cell (counter fixture) reads `jsc2js README — https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md` — URL matches the live/anchor used above.

### 3. Anchor headings (present in capture == live bytes; capture line numbers)

`# jsc2js` (1) · `## 项目简介` (7) · `## 快速开始` (18) · `### 1-4` (20/28/38/51) · `## 说明` (62) · `## 参考与致谢` (97) · `# English` (109) · `## Overview` (115) · `## Quick Start` (126) · `### 1-4` (128/136/146/159) · `## Notes` (170) · `## References & Acknowledgments` (212).

### 4. Candidate quotes verified verbatim (byte substring, `grep -cF`, capture == live)

- `jsc2js` 用于将v8生成的 **JSC 字节码**逆向为可读的 JavaScript — count 1
- reverses **V8‑generated JSC bytecode** into readable (approximate) JavaScript — count 1 (note U+2011 non-breaking hyphen in `V8‑generated`)
- The patch set covers V8 5.1 and later — count 1
- V8 5.1 是当前 `.jsc` 路径的兼容下界 — count 1
- 由node编译出来的jsc可能无法正常反编译，electron则正常 — count 1
- `loadjsc()` — count 4; `python view8.py --disassembled` — count 2

### 5. Row-id hygiene (no collision with staged or existing rows)

- `corpus/SOURCES.md` row table currently ends at **S106** (max id); full-file grep for `S125|S129` → no match; no `S12x` rows exist.
- `.ufo/waves/round-34/r34b/assimilation/staged-ids` lists S106–S236 — a staged ID-range planning artifact only, not committed rows; it does not reserve S125/S129 in the registry.

### 6. Claim C1 red-state at measured revision (expected, honest before data)

- HEAD `3ecf4298` is the "failing do-nothing controls" commit; `git ls-tree HEAD -- corpus/knowledge` → 0 `r35-jsc2js*` entries; `corpus/README.md` coverage map holds neither filename (0 hits); `PROVINCE.md` (lane root) carries only the Frontier bullet `**.jsc` → source mapping** — … View8/jsc2js-style` (lines 147–148) and **no** Round-35 Core-addition table yet.
- C1 instrument expectations (frozen, `d2729cba`/`a85ca674` pins) read immutable git objects only; they check entry existence, provenance trio `source:`/`verified-at:`/`recheck:`, `source:` citing the row, row presence with `status=mined`, `opened=2026-10-25*`, `used-by` naming the entry, PROVINCE stem and README filename. The counter imposes no anchor-content rule; exactness of the quote/anchor is a drafting obligation — verified here byte-exact against the live source.

## Limits

- Byte identity holds at the fetch instant (2026-10-25); upstream can change later. The capture is the pinned record (sha256 above) and the frozen counter scores git objects only (no re-fetch at score time).
- S129 release-page/pagination verification is outside this seat (R35Audit02/03).
- Counters were not executed by this seat (parent owns post-integration gates); do-nothing red and final green remain gate items.
