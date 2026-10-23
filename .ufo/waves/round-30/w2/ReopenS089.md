# R30 w2 — Re-open S089 (quote, hash, scope)

Seat `KaidokuR30.ReopenS089`, reviewer. Attacked: SOURCES row S089 (`corpus/SOURCES.md:95`) and its Gate row
(`corpus/lessons/round-30.md:32`). No REA run, no carrier or mutant touched, no tool installed or updated.

## Verdict

**admit — holds.** All three pinned URLs return bytes whose sha256 equals the row; the quote is on `README.md:95`
verbatim (12 words, ≤25); the row's scope and teaches cells name REA only to exclude it. No actionable defect.

| check | row value | observed (2026-10-23T03:12:18Z) | result |
|---|---|---|---|
| README.md sha256 | `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc` | same, HTTP 200, 9580 B | equal |
| PARSING.md sha256 | `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e` | same, HTTP 200, 3816 B | equal |
| schema sha256 | `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15` | same, HTTP 200, 4621 B | equal |
| upstream HEAD | `e2316a672fc03cb84d296b66198b6b270e915dca` | `HEAD` and `refs/heads/master` both `e2316a67…` | equal |
| quote location | `README.md:95` | line 95, exact match, LF-terminated, no CR in file | located |
| quote length | ≤25 words | 12 words (`wc -w`) | within limit |
| REA claim | none | "not REA behavior…"; "does not establish REA recognition" | scope-clean |

## Findings and evidence

- **Observation — fetch and hashes.** Command (cwd `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS089`):
  `for f in README.md PARSING.md cargo-auditable.schema.json; do timeout 120 curl -sS -L -o $f -w "$f http=%{http_code} size=%{size_download}\n" "$B/$f"; done; sha256sum …`
  with `B=https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca`.
  UTC 2026-10-23T03:12:18Z; each curl exit 0, `http=200`; `sha256sum` printed
  `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc  README.md`,
  `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e  PARSING.md`,
  `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15  cargo-auditable.schema.json`.
  `cmp` against the wave-1 scribe copy (`/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/README.md`) printed `same_as_w1`.
  The Gate row's prefixes `ccca48d9…`, `39e35b88…`, `c6ac9399…` match.
- **Observation — pin.** `timeout 120 git ls-remote https://github.com/rust-secure-code/cargo-auditable HEAD refs/heads/master`,
  UTC 2026-10-23T03:12:19Z, exit 0: `e2316a672fc03cb84d296b66198b6b270e915dca	HEAD` /
  `e2316a672fc03cb84d296b66198b6b270e915dca	refs/heads/master`. (This also supplies the invocation time the
  wave-1 scribe recorded as unknown.) The URLs are commit-pinned, so the bytes do not depend on HEAD moving.
- **Observation — quote.** `awk 'NR>=90&&NR<=97' README.md`, UTC 2026-10-23T03:12:26Z, exit 0:
  `95|The JSON is Zlib-compressed and placed in a linker section named \`.dep-v0\`.`
  `grep -n 'dep-v0' README.md` returns only line 95. `awk 'NR==95' README.md | grep -cF '<quote>'` → `1`;
  `wc -w` on line 95 and on the quote → `12` and `12`. `grep -c $'\r'` → 0 for all three files (line numbering is unambiguous).
- **Observation — other anchors.** `README.md:92-96` is the section `### What is the data format, exactly?` (92)
  through the PARSING link (96). `PARSING.md:26-40` spans Steps 1–3; line 28: "Use your language's recommended
  ELF/Mach-O/PE parser to extract the `.dep-v0` section from the executable." Line 32: "The data is Zlib-compressed."
  Schema line 5: "Describes the `VersionInfo` JSON data structure that cargo-auditable embeds into Rust binaries."
  Each cited range carries the content the row's teaches cell attributes to it.
- **Observation — scope.** The row (sha256 of the line `a48cc7da…7af2`) mentions REA twice, both as exclusions:
  scope "…not REA behavior or a thin-Mach-O-specific guarantee"; teaches "…does not establish REA recognition."
  It also does not overclaim on Mach-O: PARSING.md:28 gives only generic Mach-O guidance (`__DATA` segment), no
  thin/fat distinction, so the thin-Mach-O exclusion is correct.
- **Observation — row stability and admission gates (QUALITY row 45).** `git show <rev>:corpus/SOURCES.md | awk '/^\| S089 \|/' | sha256sum`
  at 2026-10-23T03:12:46Z gives `a48cc7da519b82f58016e2d4673f532627dff67064ea8930b5b5dfd1588b7af2` at
  `24da3459`, `92b1dd2d`, `3502b94c` (lane HEAD) and in the working copy. At base `d210fb8f` `grep -c '^| S089 |'` → `0`
  (exit 1), so the row is new since base. Status `mined`, opened `2026-10-23`, 11 cells (matching the header),
  on the positive entry's `source:` line (`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:1`), in the lesson
  Gate (`round-30.md:32`), and `claims.json:17` has `"claim_row": "S089"`.

## Residual risk (no change required for admission)

- **Low — Gate row records one quote for three URLs.** `round-30.md:32` lists README with "(+ PARSING.md, schema …)"
  and only the README quote. Per-URL quotes for PARSING.md:3 and schema:5 exist only in
  `.ufo/waves/round-30/w1/SrcCargoAuditable.md:14-16`. I re-checked both: PARSING.md:3 "Since the format simply uses
  Zlib and JSON, implementing a parser should be trivial." and schema:5 (above) are verbatim. Inference: the Gate is
  traceable but not self-contained per URL.
- **Low — the entry, not the row, leans on S089 for an REA statement.** `positive.md:73` and `claims.json:21`:
  "The oracle shares the format spec (S089) with REA, not code." S089 grounds the format spec; that REA implements it
  is grounded by S090 (REA code) and the measured agreement, not by S089. Inference: wording only; the row itself is clean.

## Verification gaps

- Did not compare the row against the cargo-auditable git tree (`git cat-file` at `e2316a67`); raw.githubusercontent bytes were the sole source, as the row pins. Unknown whether a CDN could serve different bytes; same bytes were served at 02:42Z (wave 1) and 03:12Z (this seat).

## Sources opened (access date 2026-10-23)

| URL | sha256 | located quote (line) |
|---|---|---|
| https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/README.md | `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc` | `:95` "The JSON is Zlib-compressed and placed in a linker section named `.dep-v0`." |
| https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/PARSING.md | `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e` | `:32` "The data is Zlib-compressed. Simply decompress it." (link markup removed: `[Zlib](…)`) |
| https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/cargo-auditable.schema.json | `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15` | `:5` "Describes the `VersionInfo` JSON data structure that cargo-auditable embeds into Rust binaries." |
| https://github.com/rust-secure-code/cargo-auditable (`git ls-remote`) | n/a (ref listing) | `e2316a672fc03cb84d296b66198b6b270e915dca	HEAD` |

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS089/`)

- `README.md` — `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc`
- `PARSING.md` — `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e`
- `cargo-auditable.schema.json` — `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15`
- `s089-row.txt` (the S089 line from the lane working copy) — `a48cc7da519b82f58016e2d4673f532627dff67064ea8930b5b5dfd1588b7af2`

No processes left running.

Report: `.ufo/waves/round-30/w2/ReopenS089.md`
