# ReviewS018 — S018 re-open of the Check Point article (round 14, w1)

Seat: KaidokuR14.ReviewS018 (leaf, source-only). No REA, no target execution, no builds/tests/linters.
Access date: 2026-10-20 (UTC, from `date -u`).
Tools: none installed or upgraded. `curl` and Python 3 were already present; used as-is.

## Scope

Reopen S018 (Check Point Research, "Breaking the Seal: Static Deobfuscation of JSCeal's Compiled V8 Bytecode") and verify:
(a) the round-13 corrected location of the quote "The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.";
(b) the original Gate anchor `Decompiled output`.

## Source access (fresh, this session)

| Route | Location | Result |
|---|---|---|
| Direct HTTP GET | `https://research.checkpoint.com/2026/breaking-the-seal-static-deobfuscation-of-jsceals-compiled-v8-bytecode/` | HTTP 200, `text/html; charset=UTF-8`, 355,603 bytes, 4,569 lines |
| Reader fetch (omp `read`, native method) | same URL | Article body returned; `# Introduction` section contains the quote |

- Raw snapshot: captured this session, hashed, then deleted from the lane directory for custody (see Recommendation to L1); not committed.
- SHA-256 of snapshot: `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e`
- WAF status: **not encountered** in either fetch. The grep hits for "challenge" (raw lines 2952–2984) are sign-in URL strings inside an article `<pre>` code sample, not a WAF interstitial. Both captures are fresh opens; nothing here relies on prior round-13 text.
- Article metadata (raw `<meta>`): published 2026-08-31; modified 2026-09-24.

## Findings (severity order)

### F1 — Corrected quote location holds (verified, no defect)
- The quote occurs exactly once in the whole document (raw HTML line 489, `<p class="wp-block-paragraph">`).
- It sits inside the `Introduction` section: `<h1>` at raw line 469, next `<h1>` `Distributed payloads` at raw line 497. Python section check: quote substring True.
- Quote is contiguous, verbatim, 19 whitespace-separated words (within the 25-word cap). Em dash U+2014 matches.
- Reader-mode fetch places the same sentence under `# Introduction`, so the two routes agree on section.

### F2 — Original Gate anchor `Decompiled output` is a mislocation (verified)
- `Decompiled output` is the `<h1>` at raw line 625; the next `<h1>` is `Obfuscation layers` at raw line 707.
- Python section check: quote substring **False** in lines 625–707. The quote does not appear in that section, and nowhere else in the article.
- The section is topically adjacent (it says View8 "lifts V8 bytecode into pseudocode"), so the original pointer was plausible but does not contain the quoted sentence. The round-13 correction is correct to supersede it.

### F3 — The "line 87 (heading at line 77)" figure is not reproducible from the raw bytes (low severity, calibration)
- In the raw HTML the Introduction heading is at line 469 and the quote paragraph at line 489 (offset 20). The round-13 note's offset is 10 (77 → 87), so the cited numbers come from a different rendering and cannot be checked against the captured bytes.
- The section-plus-heading anchor is the reproducible locator. The line number should not be used as a gate key unless the rendering is pinned.

### F4 — Registry anchor omits the Introduction (low severity, registry note; no edit made)
- `corpus/SOURCES.md` S018 row names anchors `Analysis methodology` and `Decompiled output`. The quote used in the Gate lives under `Introduction`.
- The round-13 lesson states the row "needs no superseder" because its topic anchors remain valid. That is consistent with the registry wording, but the row does not name the section that carries the quoted claim. L1 may decide whether to add `Introduction` to the row; this seat did not edit shared files.

### F5 — Version identity (limitation)
- The modified timestamp (2026-09-24) precedes the round-13 open. Today's snapshot is the only version I can attest. I cannot prove that round 13 read byte-identical text, and I make no such claim.

## Verification gaps and limits

- Source-only. I did not run `quote-fidelity.py`, did not run `--selftest`, and did not run the gate against any manifest. Those belong to L1 after integration.
- I did not run the reader-mode line count; the rendered line numbers were not re-derived.
- The sentence is an author statement about their pipeline. Opening the page establishes provenance and location only. It does not establish that the JSCeal pipeline behaves as described.
- Access date and snapshot hash above are for this session only.

## Recommendation to L1

- Treat the corrected S018 location as **verified** on section and heading: `Introduction`, contiguous, 19 words.
- If the gate uses line numbers, do not pin them to round-13's rendering (F3). Pin the heading and the captured-bytes SHA-256 instead.
- Decide on F4 at integration; no action taken here.
- **Custody (raised by KaidokuR14.CustodySafety).** The raw article copy is a full copy of a Check Point "All rights reserved" page including malware IOCs. The lane remote (VeigaPunk/shokunin-reverse-engineering) is public. L1 MUST keep the raw copy out of the commit. Retain only the SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e`, the byte count (355,603), and the bounded excerpts already quoted above.
- Custody action taken: the raw snapshot `s018-raw.html` was deleted from this lane directory after its hash was recorded. Deletion was not a request to keep it out of the commit only; the copy is gone. The source page is mutable (modified 2026-09-24), so a fresh fetch may return different bytes and a different hash from `31b82315…dd5e`. The F1/F2 raw-line references (469, 489, 625, 707) therefore cannot be re-checked locally from the deleted capture. They are valid only for the captured bytes. CustodySafety reports no secrets or session tokens in the page (GTM id only).
