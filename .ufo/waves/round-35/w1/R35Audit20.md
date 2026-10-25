# R35Audit20 — Verify approximate reconstruction warning

Seat: R35Audit20 (executor, leaf). Wave r35-build, milestone "Build evidence and first falsifications".
Item: verify the approximate-reconstruction warning behind claim C1 (`.jsc -> source mapping` assimilation via S125/S129).
Read-only audit; no lane writes except this report. Commands run under lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Findings

**F1 — VERIFIED: the warning exists, verbatim, in the frozen prep capture.**
The only round-35 artifact carrying the approximate-reconstruction warning is the jsc2js README capture
`.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` (219 lines, blob `62876f3e135466093d3bd001669dd5408cb9f3f8`). Exact locations:

- Chinese: line 13 `还原/重建为 JavaScript 近似源码`; line 48 `` `xxx.js` 为基于字节码分析还原的近似 JavaScript ``; line 49 `（变量名 / 控制流结构可能与原始源码不同，属于"语义近似重建"）`; lines 90–93 `还原 JS 不能 100% 重建原始源码：变量/函数名可能匿名或被重写；控制流可能被结构化重排；常量折叠或运行时优化不会完整还原。`
- English: line 117 `readable (approximate) JavaScript`; line 122 `approximate JavaScript reconstruction`; lines 156–157 ``contains an approximate JavaScript reconstruction … (Identifiers / control flow may differ from the original source; this is a semantic approximation.)``; lines 205–208 `JavaScript reconstruction cannot be 100% identical to the original: Variable / function names may be missing or replaced. Control flow may be structurally reorganized. Constant folding / runtime optimizations are not perfectly reversible.`

The English block at 205–208 is the canonical warning statement; the Chinese block at 90–93 is its byte-equal counterpart.

**F2 — VERIFIED: the evidence predates the freeze and is immutable.**
All three captures (readme, releases-page1.json, releases-page7.json) were committed in `d2729cba` ("instruments-first prep"), which precedes the freeze commits (`f1ea3a6d`/`e4ca43dd` → canonical freeze `2323d197`). At `2323d197` the readme blob hash equals the current worktree hash (`git hash-object` == `git rev-parse 2323d197:...` = `62876f3e…`). The warning is frozen background, not authored after the freeze.

**F3 — VERIFIED: the warning is unique to the README; release inventory pages carry none.**
`grep -o -i 'approximate|近似|reconstruct|100%|cannot be|warning'` over `releases-page1.json` and `releases-page7.json` → zero hits. Both pages are GitHub API captures of repo `xqy2006/jsc2js` (URLs in JSON `url`/`html_url` fields, e.g. `https://api.github.com/repos/xqy2006/jsc2js/releases/419322632`). So the release-inventory source (S129 candidate) has no approximate-reconstruction caveat; only the mapper-contract source (S125 candidate) does.

**F4 — STATE: S125/S129 not yet present; counters pinned.**
`corpus/SOURCES.md` holds exactly 106 rows (S001–S106), matching the census-start base count `rows=106`; S125/S129 are post-base mined rows per C1. Instrument hashes match canonical pins: C1 `e28792c7…`, C2 `576c14dd…`, plan `45b644a4…` (sha256sum).

**F5 — ADVISORY (falsification-relevant): the frozen counter does not test the warning.**
C1's predicate P35-c1 and `tools/round-35/c1-coverage-counter.py` `check()` validate: entry existence, provenance-trio lines, `source:` row citation (S125/S129), SOURCES row (mined/opened 2026-10-25/used-by names entry), PROVINCE stem, README map entry. None of them require the approximate-reconstruction warning. The mapper-contract entry could pass the counter while omitting the limitation text. Recommendation (non-scoring): the mapper-contract entry should carry the F1 warning (cite capture lines 90–93/205–208) so the admitted frontier record stays honest about approximation; the release-inventory entry needs no such caveat (F3).

## Commands / output / limits

- `grep -n -E "近似|approximate|100%|reconstruct" .ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` → lines 13, 48–49, 90, 117, 122, 156, 205.
- `sed -n '88,94p;203,210p;46,50p;154,158p' …/jsc2js-readme.md` → verbatim warning text.
- `git log --oneline -- …/prep/jsc-sources/` → only `d2729cba` (instruments-first prep).
- `git ls-tree 2323d197 -- …prep/jsc-sources/` → three blobs; `git hash-object` == `git rev-parse 2323d197:…` = `62876f3e…`.
- `grep -o -i "approximate…|近似|reconstruct…" releases-page1.json releases-page7.json` → no output.
- `grep -c -E '^\| S[0-9]+' corpus/SOURCES.md` → 106.
- `sha256sum tools/round-35/c1-coverage-counter.py tools/round-35/c2-calibration-counter.py plans/round-35-claims.md` → e28792c7… / 576c14dd… / 45b644a4… (match canonical pins).

Limits: no network fetch performed; repo identity `xqy2006/jsc2js` sourced only from captured JSON URL fields. No lane file written besides this report; no VCS mutation; no installs.
