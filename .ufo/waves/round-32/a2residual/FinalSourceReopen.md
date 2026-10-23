# Round-32 attempt-2 residual — FinalSourceReopen (S098/S099/S100)

Seat: `KaidokuR32A2.FinalSourceReopen-2`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Measured revision: `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26` (HEAD, verified `git rev-parse` + `git cat-file -t` → `commit`; subject "round-32: bounded ARM64X native-view evidence, source gate and faithful repertoire repair"). UTC evidence window 2026-10-23T07:14:39Z–07:19:48Z. Registry `corpus/SOURCES.md` NOT edited; no Git/JJ write anywhere; no lane file other than this Report written.

**Verdict: SUPPORT.** All three source rows reopen cleanly at bb0af56c; every Gate/audit quote is contiguous in the retained bytes at the claimed location and ≤25 words; fabricated, cross-source (off-topic), and overlong quotes fail support; the captured Microsoft markdown for S099 is byte-identical to a fresh `Accept: text/markdown` response (not HTML rendering); S100's reject scope and flip criteria agree on both retained representations and on three fresh re-fetches: CHPE field/offset/tag definitions absent, machine-type definitions present, no flip. No residual falsification found for this item. 73/73 instrument checks PASS, exit 0.

## 1. Live reopens (observed)

All fetches `curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576` into `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceReopen/reopen/`; every response HTTP 200, exit 0. Files ≤335,441 bytes (<1 MiB cap).

| row | URL | fetched | http | bytes | sha256 (observed) | equals retained/claimed? |
|---|---|---|---|---|---|---|
| S098 | raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s | 07:14:39Z | 200 | 2686 | `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` | YES — registry/lesson hash; also equals `corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s` (sha256sum re-run) and claims.json line 50 |
| S098 | …/loadconfig-arm64.s | 07:14:40Z | 200 | 423 | `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d` | YES — registry/lesson hash; equals `c1/inputs/loadconfig-arm64.s` and claims.json line 49 |
| S099 | learn.microsoft.com/en-us/windows/arm/arm64x-pe with header `Accept: text/markdown` | 07:14:40Z | 200 | 7386 | `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66` | YES — byte-identical to committed `corpus/evidence/round-32/sources/arm64x-pe.md` (blob `a2ff977c`). Capture method confirmed: content-negotiated Markdown, not HTML |
| S100 | learn.microsoft.com/en-us/windows/win32/debug/pe-format with header `Accept: text/markdown` | 07:14:40Z | 200 | 183798 | `563f2dd952e16ca836036189ee82e46f1dbde29d716ee4ea5d2277e9562609d8` | NO — a distinct Microsoft Markdown representation, see §4 |
| S100 | learn.microsoft.com/en-us/windows/win32/debug/pe-format (HTML) | 07:14:40Z | 200 | 281747 | `2f0600144d3611f653668e297ce5eb4acfe2a64f6c5d2a90252b87995e7058fb` | NO vs captured `d0c584f1…` (282123 B); diff is 4 Akamai bot-protection lines only, see §4 |
| S100 | raw.githubusercontent.com/MicrosoftDocs/win32/docs/desktop-src/Debug/pe-format.md | 07:17:16Z | 200 | 335441 | `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0` | YES — unchanged since capture; equals committed `corpus/evidence/round-32/sources/pe-format.md` (blob `9d81b6b3ee7a65f171981a698984be200b9fa37a`, matching A2SourceReject's stated blob) |

Retained-snapshot hashes re-verified at HEAD: arm64x-pe.md `a9be76a8…`, pe-format.html `d0c584f1…`, pe-format.md `b17271a3…` — all equal the SOURCES.md rows (lines 104–106) and the round-32 lesson. Working tree at HEAD: 7 untracked entries only (a2residual/a2audit/independent-pe scratch), `git status --porcelain corpus/evidence/round-32/` clean — no tracked evidence modified.

## 2. Quote receipt (Gate + audit quotes, observed contiguous, ≤25 words)

Quoted bytes, exact line hits from the verifier (§6):

| quote | source bytes | line | words | contiguous |
|---|---|---|---|---|
| "Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together." (lesson S099 row; A2SourcesPrimary) | arm64x-pe.md `a9be76a8…` | 50 | 19 (link markup counted; 19 flattened) | yes |
| "The built Arm64X binary has two sets of code, entry points, and other elements" (A2SourcesPrimary) | arm64x-pe.md | 56 | 14 | yes |
| line 64 default-view text "By default, Arm64X binaries appear to be Arm64 binaries. …" (lesson: "line 64 separately explains default Arm64 appearance") | arm64x-pe.md | 64 | paraphrase-cited, text confirmed on that line | yes |
| "`.xword __chpe_metadata`" (lesson S098 row; A2SourcesPrimary) | loadconfig-arm64ec.s `c043b748…` | 20 | 2 | yes |
| "`.rva __hybrid_code_map`" / "`.rva __x64_code_ranges_to_entry_points`" / "`.rva __arm64x_redirection_metadata`" (A2SourcesPrimary, lines 59–67 claim) | loadconfig-arm64ec.s | 64 / 66 / 67 | 2 each | yes |
| "`.section .rdata,"dr"`" / "`.word 0x140`" (A2SourcesPrimary, paired ARM64 lines 1–15 claim) | loadconfig-arm64.s `7c29f128…` | 1 / 5 | 2 each | yes |
| "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file." (lesson S100 row; A2SourceReject line 131) | pe-format.md `b17271a3…` | 131 | 16 | yes |
| "ABI that enables interoperability between native ARM64 and emulated x64 code." (A2SourceReject line 130) | pe-format.md | 130 | 11 | yes |
| "The load configuration structure has the following layout for 32-bit and 64-bit PE files:" (A2SourceReject line 1926) | pe-format.md | 1926 | 14 | yes |
| "The low 2 bits of the displacement are zero and are not stored." (A2SourceReject line 560) | pe-format.md | 560 | 13 | yes |
| "The Windows SDK winnt.h header defines the following macros:" (A2SourceReject line 2174) | pe-format.md | 2174 | 9 | yes |
| A2SourceReject HTML citations: ARM64EC definition cell, value cells `0xA641`/`0xA64E`, ARM64X definition cell | pe-format.html `d0c584f1…` | 963 (`0xA641`), 964 (def), 968 (`0xA64E`), 969 (def) | — | yes (one `td` each) |
| A2SourceReject line-1961 cells: offset `116/184`, size `4/8`, field `GuardLongJumpTargetCount`, separate cells not one sentence | pe-format.md | 1961 | — | yes; HTML `</tbody>`/`</table>` at 5412/5413 after cells at 5407–5411 |

ms.date cross-checks observed: arm64x-pe.md `ms.date: 2025-11-06` (matches SOURCES S099 row); A2SourceReject's load-config64.md line 9 `ms.date: 12/05/2018` confirmed in the retained scratch bytes of that auxiliary page.

## 3. Able-to-fail negative controls (observed FAIL, as required)

- Fabricated (one-word perturbation of the S099 line-50 quote): FAILS — absent.
- Fabricated CHPE attribution ("CHPEMetadataPointer is stored at offset 0xC8…") against pe-format.md: FAILS — absent.
- Off-topic cross-source: S099's true line-50 quote checked against pe-format.md: FAILS; S100's true line-131 quote checked against arm64x-pe.md: FAILS.
- Overlength: a contiguous 26-word run present in pe-format.md line 2 is REJECTED on the ≤25-word rule ("26 words >25") — the support rule is not vacuously passing.

## 4. S100 reject scope/flip agreement (observed)

Token census (script §6, counts re-computed independently of A2SourceReject): `CHPEMetadataPointer`, `CHPE`/`chpe`, `MetadataPointer`, `CodeMap`, `0xC8`/`0xc8` = **0** in all five byte streams: retained pe-format.md, retained pe-format.html, live raw-GitHub docs markdown (unchanged `b17271a3…`), live learn `Accept: text/markdown` (`563f2dd9…`), live learn HTML (`2f060014…`). Scope: the same streams DO document the machine types — ARM64EC definition sentence, ARM64X definition sentence, values `0xA641` and `0xA64E` present in retained md/html and in the live learn markdown (ARM64X definition at line 167 of 2037). The rejection is the bounded CHPE offset/tag scope, not a page rejection — registry row S100 ("Candidate authority … only", "REJECTED: both searched representations omit…"), lesson ("The page is not rejected for other scopes"), and A2SourceReject ("Not a page rejection") all agree with the bytes.

Flip re-check against a later fetch (today) of both pinned flip URLs: neither conjunct is met — no `CHPEMetadataPointer` Load Configuration Layout row with offset cell `200`/`0xC8`, and no code-map range-tag bit definition — in either representation. **No flip.**

Drift characterization (observed): unified diff captured-vs-live HTML = 4 changed lines, all Akamai bot-protection (`bazadebezolkohpepadr` script + noscript pixel) vs `</head>`/`</body>`; zero timestamp/meta/content-class lines. Searched-token content is unchanged.

## 5. Captured-Markdown vs Accept:text/markdown (assignment clause)

- S099: captured hash `a9be76a8…` **equals** today's `Accept: text/markdown` response byte-for-byte (7386 B). The landed capture is genuinely content-negotiated Markdown, not an HTML rendering. SUPPORT.
- S100: the captured/committed Markdown (`b17271a3…`, 335,441 B) is labeled in SOURCES and A2SourceReject as the MicrosoftDocs/win32 `docs`-branch Markdown (raw.githubusercontent.com), which is exactly where it came from and still matches today. Learn's `Accept: text/markdown` response is a **different, shorter representation** (`563f2dd9…`, 183,798 B). This is an honest identity difference, not a defect: the registry does not claim learn-markdown bytes, and the new representation independently satisfies the reject census (§4). [INFERENCE on why they differ: learn serves the `win32-pr` `live` rendering pipeline versus the `win32` docs branch; not separately proven — the `win32-pr` commit blobs were 404 in A2SourceReject and I did not retry them.]

## 6. Instrument, commands, observed outcomes

Fetcher (per row; all exit 0, HTTP 200):
```
curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576 \
  [--header 'Accept: text/markdown'] --output <name> \
  --write-out '<label> http=%{http_code} size=%{size_download}\n' '<URL>'
```
Observed write-out lines: `S098ec http=200 size=2686` / `S098a64 http=200 size=423` / `S099 http=200 size=7386` / `S100md http=200 size=183798` / `S100html http=200 size=281747` / `S100gh http=200 size=335441`.

Verifier: stdlib-only Python 3.14 script at `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceReopen/verify_quotes.py` (11,411 bytes; named for L1 to commit if this receipt is admitted). Runs: 07:17:31Z (run1: 66 checks, 1 FAIL = checker expectation bug, not source defect: I expected `0xA641` on HTML line 964; A2SourceReject attributes the definition sentence there and the value cell is line 963 — re-located, both confirmed), 07:18:58Z (run2: 73 checks, 1 FAIL = my overlength control crossed line boundaries so it failed by absence, not by count — control rewritten), **07:19:48Z run3: TOTAL=73 FAIL=0, exit 0**. Full run3 output (73 PASS lines) retained at `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceReopen/verify-out.txt`; census at `…/census.json`; reopen bytes under `…/reopen/`. Scratch df at start: `/dev/nvme1n1p2 804G 582G 222G 73% /fast`. Tools installed: none. No pacman/uv/npm activity. No held-item inspection. No process left running.

## 7. Residual risk and verification gaps

Addendum 07:23:21Z: during this seat's run, lane HEAD advanced `bb0af56c…` → `bbdd793d55807cfea9193ef5aaf0ae86a5c25a10` (L1/sibling activity: LOG.md, corpus/lessons/round-32.md modified in worktree; not this seat's writes). `git diff --stat bb0af56c… bbdd793d… -- corpus/SOURCES.md corpus/evidence/round-32/ .ufo/waves/round-32/claims*.json` is EMPTY and all five evidence-file sha256 values re-read unchanged at the new HEAD — every observation above holds at `bbdd793d…` unchanged.

- Learn's S100 text/markdown representation (`563f2dd9…`) is new evidence not covered by the frozen reject's two pinned URLs; it is censused here and consistent with the reject, but the pinned flip rule would not automatically admit/deny via it. [INFERENCE] that this is a rendering-pipeline difference, unproven.
- The auxiliary winnt.h page (`load-config64.md`, `27c3fdea…`) was not re-fetched this session; its retained claims (CHPEMetadataPointer named once, no offset value, struct ends at SEHandlerCount) are cited from A2SourceReject bytes, not re-opened. Not needed for the three assigned rows.
- GitHub code-search 401s in A2SourceReject remain a disclosed non-evidence item; unchanged by this session.
- This seat performed no capability, counter, or carrier work; S098's "references are not populated-map or reader-result proof" limit stands as written.

Report: `.ufo/waves/round-32/a2residual/FinalSourceReopen.md`
