# R35Audit26 — S150 source-quote re-open

## Finding

S150 is a **source-quote mismatch** against the live article, not an unreachable-source case. The cited URL is reachable and the article is about disassembling binaries without symbols, but the registered quote `シンボルがない場合のヒント` is absent from both the served page and its article body. The article's actual contents provide specific, contiguous replacement anchors; whether to change the row/quote is a maintainer decision and was not performed here.

The exact heading is not in the article TOC. The TOC lists `パターン認識のコツ` (line 152) with the actual heading text; line 154 says `strip されたバイナリを読むときに手がかりになるパターンを整理してみます。` A stronger passage for the register's no-symbols topic is at body line 69: `strip でシンボルテーブルを削除すると、関数名やラベルが見えなくなります。実際のリバースエンジニアリングはこの状態から始まります。` Thus a quote anchored to a real section/passage can be reopened, but the old invented heading must not be retained as verified evidence.

## Evidence and commands

- Read `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`, `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`, and `.ufo/waves/round-34/r34b/assimilation/staged-ids`. Plan/canonical frozen claim scopes remain unchanged; S150 is only an advisory quarantine probe, not C1/C2 data.
- Register cross-check: `grep` on `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` returns row S150, URL `https://zenn.dev/yasu01/articles/7370bd5d414ec4`, quote `シンボルがない場合のヒント`, class `payload-absent`, with register rationale that source, companion URLs and local artifacts were checked.
- Fetches (temporary files only):
  - `curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' -o /tmp/r35audit26-s150.html -w 'HTML http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://zenn.dev/yasu01/articles/7370bd5d414ec4` → `HTML http=200 bytes=174088 url=https://zenn.dev/yasu01/articles/7370bd5d414ec4`.
  - `curl -sL -A 'Mozilla/5.0' -o /tmp/r35audit26-s150.json -w 'API http=%{http_code} bytes=%{size_download}\n' https://zenn.dev/api/articles/7370bd5d414ec4` → `API http=200 bytes=69896`.
- Read-only Python analysis of `/tmp/r35audit26-s150.html`: decoded 164,066 characters; counts `シンボルがない場合のヒント=0`, `ヒント=0`, `実バイナリを逆アセンブルして読む=4`, `シンボル=14`. The HTML has one H1 and eight H2s, including `パターン認識のコツ`; none is the claimed heading.
- Read-only Python analysis of API JSON `article.body_html` (39,937 chars): claimed heading count 0; `ヒント` count 0; `strip` count 7. API TOC confirms H2 `パターン認識のコツ`; its body line 154 is the quoted contiguous sentence above. Body line 69 is confirmed as the separate, no-symbol-specific quote above.
- `git log --all -S'S150' -- corpus` returned no S150 history; no S150 source row in current lane `corpus/SOURCES.md` was found. The lane quarantine verdict documents the disposition: **REFUSE** (fabrication class), flip by re-anchoring to a real quote and reopening. This report's independent fetch corroborates the absent quote; it does not authorize changing the staged register or verdict.

## Scope and limits

Axes: source fidelity, evidence provenance, and boundary compliance. No lane production/corpus/counter/claim/scorecard/log files, VCS/index/jj state, or other repository were modified. Only this unique wave-one report is written; fetch artifacts are in `/tmp`. No counter or test was run, no claim predicate/scope altered, and no source-tree artifacts were fetched beyond the live URL/API. The register's earlier check of companion URLs/local artifacts is cited as recorded provenance, not independently reproduced. No assertion is made that an alternate quote has been admitted, that an S150 row is live in SOURCES, or that C1/C2 changed.
