# S140 row candidate — git-status documentation

Seat `R45W1SrcGitStatus`, round 45 wave 1. Read-only on the lane tree; every write below is
inside `.ufo/waves/round-45/w1/R45W1SrcGitStatus/`.

## Provenance envelope

| field | value |
|---|---|
| source URL | `https://git-scm.com/docs/git-status` |
| HTTP status | `200` (`HTTP/2 200`, server `cloudflare`, via `1.1 varnish`) |
| bytes | `99934` (header `etag: W/"6adf6913-1865e"` = 0x1865e = 99934, consistent) |
| sha256 | `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9` |
| UTC access | `2026-10-28T15:41:04Z` (second independent fetch, `2026-10-28T15:38:50Z` first; `cmp` identical) |
| `last-modified` | `Mon, 26 Oct 2026 14:52:03 GMT` |
| saved page | `.ufo/waves/round-45/w1/R45W1SrcGitStatus/git-status.html` (99934 B, sha256 above) |
| extracted text | `.ufo/waves/round-45/w1/R45W1SrcGitStatus/git-status.txt` (sha256 `fd785b552795b940133da0b7a3807e6da3a40218b45ff39803311a03568ec1ac`) |
| receipts | `receipt-fetch.txt`, `receipt-headers.txt`, `receipt-quote-presence.txt`, `receipt-v1-semantics.txt`, `receipt-instrument-binding.txt`, `receipt-schema.txt` (same directory; each carries command, exit, stdout sha256, UTC) |

## The row (lane schema, 11 columns)

Landed verbatim shape, one line:

| S140 | git-status documentation — https://git-scm.com/docs/git-status | docs | A | Git's Version 1 porcelain status format and its `-z` variant — the form a gate parses to read worktree state; not porcelain v2, not diff/diff-tree output (S141), not the 44 prose mentions in `corpus/**.md` nor the 10 older tool call sites that run `--porcelain` without `-z` | anchors `#_porcelain_format_version_1` (HTML byte offset 76125) and `#_pathname_format_notes_and_z` (90511); page fetched 2026-10-28T15:41:04Z, HTTP 200, 99,934 B, sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`; quoted paragraphs are `<p>` index 62 (v1 stability) and 65 (`-z` machine parsing) | The v1 porcelain format is guaranteed not to change backwards-incompatibly between Git versions or based on user configuration and is ideal for parsing by scripts; `-z` is recommended for machine parsing, ends each filename with NUL (ASCII 0), reverses rename pairs to `to` then `from`, and quotes nothing — which is exactly what the dirty arm reads (`tools/round-45/frozen-path-preflight.py:137`). | mined | 2026-10-28 | on-release | corpus/lessons/round-45.md |

## Gate block

URL: https://git-scm.com/docs/git-status
Accessed: 2026-10-28T15:41:04Z — HTTP 200, 99934 bytes, sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`
Quote: "guaranteed not to change in a backwards-incompatible way between Git versions or based on user configuration. This makes it ideal for parsing by scripts." — anchor `#_porcelain_format_version_1`, 24 words, byte-contiguous in the saved page (including the raw HTML once newlines are collapsed)

## Located passages (verbatim, with word counts)

| # | anchor (`id=`) | words | quote | raw-HTML contiguous | quote sha256 |
|---|---|---|---|---|---|
| Q1 | `_porcelain_format_version_1` (76125) | 24 | guaranteed not to change in a backwards-incompatible way between Git versions or based on user configuration. This makes it ideal for parsing by scripts. | **yes** (1 hit after whitespace collapse) | `d1d0a42a48373f4f8ee9a9a237c33b3b5b4840c422cf4d51054274b4fa1daaa9` |
| Q2 | `_porcelain_format_version_1`, `<p>` 65 | 11 | There is also an alternate -z format recommended for machine parsing. | no — inline `<code>-z</code>` splits the bytes | `b7b16ce1c525232f19934237051a93f81e3e2225cb7cbf9303797077add946d8` |
| Q3 | `_porcelain_format_version_1`, `<p>` 65 | 18 | Second, a NUL (ASCII 0) follows each filename, replacing space as a field separator and the terminating newline | no — inline `<em>NUL</em>` | `cf2d909d78270443ad4cdeaf5664a1714f84d0ec8f4735332ed56ca87a9f8b6c` |
| Q4 | `_pathname_format_notes_and_z` (90511) | 25 | When the -z option is given, pathnames are printed as is and without any quoting and lines are terminated with a NUL (ASCII 0x00) byte. | no — inline `<code>-z</code>` | `5d4a71db8a6686dda4892937717fd7f694344438767cca690e1bad48e4c3895c` |

Full Q1 paragraph (for context; the subject of the 24-word span):

> Version 1 porcelain format is similar to the short format, but is guaranteed not to change in
> a backwards-incompatible way between Git versions or based on user configuration. This makes
> it ideal for parsing by scripts. The description of the short format above also describes the
> porcelain format, with a few exceptions:

Presence receipt: `receipt-quote-presence.txt`, exit 0, `RESULT: PASS`, all four quotes hit
exactly one `<p>` each; stdout sha256 `86d9dc50727e8afd5c0863448efbab1e2d473725ab3d06663d6687e88acd6df0`.

**Which two things were asked for.** (1) the *Porcelain Format Version 1* paragraph carrying both
the backwards-incompatible-change guarantee and "ideal for parsing by scripts" — Q1 above, in
section `#_porcelain_format_version_1`; (2) the `-z` alternative recommended for machine parsing
with NUL-terminated fields — Q2+Q3 in the same section's `<p>` 65, corroborated by the dedicated
`#_pathname_format_notes_and_z` section (Q4, "NUL (ASCII 0x00) byte"). Both located; both anchors named.

## Behaviour check against the page's own claims (host git 2.56.0)

Fixture: `mktemp -d -p $S`, `git -C "$D" init -q -b main`, identity set only inside `$D`,
`rev-parse --show-toplevel` equal to `$D`. Receipt `receipt-v1-semantics.txt`.

| doc claim | observed | verdict |
|---|---|---|
| `-z` fields NUL-terminated, no trailing LF (Q3) | 72 B output, 5 NUL, 0 LF | met |
| rename pair reversed to `to` then `from`, `->` omitted (Q2) | `R  renamed.txt\0plain.txt\0`; non-`-z` prints `R  plain.txt -> renamed.txt` | met |
| no quoting under `-z` (Q2/Q4) | `-z` emits raw `with space.txt`; non-`-z` emits `"with space.txt"` | met |
| `color.status` not respected (same section) | `-c color.status=always` ⇒ 0 ESC bytes | met |
| `status.relativePaths` not respected; paths root-relative (same section) | from `$D/sub` with `status.relativePaths=true` ⇒ ` M sub/nested.txt` | met |

**Precision note for the dirty arm.** A rename costs **two** NUL-terminated fields, so
`st.stdout.split("\x00")` (`frozen-path-preflight.py:140`) yields the entry `R  <to>` **and** a
bare `<from>` with no status prefix; the fixture's 4 dirty paths produced 5 list elements.
Harmless for the arm's only use (`not dirty`, a boolean), but `receipt["dirty"]` is not
one-element-per-path when a rename is present. Worth a line in the lesson; not a defect.

## Reconciliation with the landed row

`corpus/SOURCES.md:146` already carries S140 (commit `e715263cb51b713c342ab992d527fe9d61d6f8ff`,
"round-45: land SKILL rule block 22 … S140/S141; the lesson"). That commit is **not** an ancestor
of the freeze `f762b727…` (`merge-base --is-ancestor` exit 1); `git show f762b727:corpus/SOURCES.md
| grep -c S140` = 0. So the row is post-freeze record, which is permitted (`SOURCES.md` is not frozen).

Cell-by-cell against my independent derivation — 4 columns identical in substance, 3 differ in precision:

| cell | landed | this row | disposition |
|---|---|---|---|
| id, kind, tier, status, opened, recheck, used-by | `S140`,`docs`,`A`,`mined`,`2026-10-28`,`on-release`,`corpus/lessons/round-45.md` | same | **identical**; all seven values are in-vocabulary (`on-release` 92×, `Nd` 49×; `docs` 47×; `mined` 136×) |
| source | `git-status documentation — https://git-scm.com/docs/git-status` | same | identical |
| scope | "Git's Version 1 porcelain status format, the form a gate should parse to read worktree state" | adds the `-z` variant and the explicit non-scope | **sharper**: the `-z` variant is what the instrument actually runs |
| anchor | "Page fetched 2026-10-28 (HTTP 200, 99,934 bytes, sha256 `903e31c5…`); anchors `Porcelain Format Version 1` and the `-z` machine-parsing paragraph" | adds anchor slugs `#_porcelain_format_version_1` / `#_pathname_format_notes_and_z`, byte offsets, and UTC | **sharper**: prose names do not resolve; slugs do |
| teaches | "…guaranteed not to change backwards-incompatibly and is the form a script should parse; `-z` makes the fields NUL-terminated, which is what the dirty arm reads." | adds the "between Git versions or based on user configuration" qualifier and the rename-field-order fact | **sharper**, no contradiction |
| tier / bytes / status | — | all re-measured and equal | confirmed |

No cell of the landed row is false. Two cells are under-specified rather than wrong: `scope`
omits `-z` (the only variant the instrument invokes), and `anchor` names the anchor by prose
instead of by `id=`, so a reader cannot resolve it by fragment.

## Calibration note on the lesson Gate block

`corpus/lessons/round-45.md:25` quotes 21 words with `…`:
"guaranteed not to change … between Git versions or based on user configuration … ideal for parsing by scripts"
(tokens 22, words excluding the ellipsis 21 — the stated count is right). The elision drops
"This makes it", so the string is **not byte-contiguous on the page** (`byte_contiguous_on_page:
False`, checked against the saved text). The claim it makes is faithful; the only cost is that a
mechanical byte-grep of the Gate quote will miss. The 24-word span in Q1 is contiguous in both
the rendered text and the raw HTML, so it is the safer string if the Gate block is re-cut.

## Limits

- Quotes Q2–Q4 are verbatim in the rendered text but not raw-contiguous, because the page wraps
  `-z` in `<code>` and `NUL` in `<em>`. Byte-presence for those is claimed at the text-content
  level only; the receipt prints both metrics so the distinction is auditable.
- One access window (2026-10-28T15:38:50Z and 15:41:04Z). The page is `on-release`/`last-modified
  2026-10-26`, so it is expected to be stable; no second-day recheck was run.
- Behaviour evidence is from git 2.56.0 on this host, not from the doc's claimed range of versions.
  The doc's guarantee is about forward compatibility, which a single-version test cannot falsify.
