## CLAIM
Citation check for entries 5–6: `E6D.md` is fully citation-supported and carries `source:`/`verified-at:`/`recheck:`; `E5D.md` traces to its receipts but omits the house header and under-cites three facts.

## METHOD
Read-only `grep`/`sed` over `.ufo/waves/luna-round-6/receipts{,-B}/leg-{7,8}.md` and `SC5/SC6.md`, plus `corpus/QUALITY.md:11-25`, `corpus/README.md:59-67`, `SCORECARD.md`, `…/skills/shokunin/protocol/CORPUS.md:17`; cross-read round-7 `E5D/E6D/E5V/E6V/G5/G6/M2/N1/F3/C3/Q6`. No probes, network, or tracked writes; only this seat file written.

## FINDINGS
Entry 5 (`E5D.md`): cited facts resolve — Evidence `ev_4b0badc6…`/SHA `8bc9a73a…` at `receipts/leg-7.md:11-13,21` (cited `:8-14,21`); hit `0x100000`, offset 0, 33,668 B, `complete:true` at `receipts-B/leg-7.md:58-60` (cited `:56-61`); byte-identical stdout `receipts-B/leg-7.md:64-72`; block-scope limits `leg-7.md:21` / `receipts-B/leg-7.md:32`.

Gap A: METHOD cites `leg-7.md:3-12` + `receipts-B/leg-7.md:21-25` for "Ghidra 12.1.4, default auto-analysis" and effective `limit=100`; those facts sit at `leg-7.md:13,21` and `receipts-B/leg-7.md:32,60` — outside both ranges (recorded request `leg-7.md:9` carries no limit).

Gap B: `E5D.md` has no `source:`/`verified-at:`/`recheck:` (`CORPUS.md:17`; parent ruling (d)); `E6D.md:12-14` shows the pattern.

Entry 6 (`E6D.md`): all citations resolve — `receipts/leg-8.md:8-14,19` (args `:8`, SHA `:11`, Evidence `:12/:19`, flags `0x150`, start `0x3cf0`, exit 0, format/version unknown/null); `receipts-B/leg-8.md:41-55` (same Evidence `:54`), `:6-8,16-35` (B carrier `b1c22172…`, `ev_d1ea68…` `:29`), `:67-76`. Header present; hyphenated token matches `[a-z0-9-]+`; RESULT-only framing, no Core-promotion claim (`:19,:25-26`).

Rows: `M2.md:11-12,16-17` cite A/B receipts correctly (`limit=100` at `leg-7.md:21` sits inside cited `:8-27`).

## THREATS
Post-landing values (78/78, 10.0, QUALITY pass, prior-72 byte identity) are unverifiable before integration; both entry files absent at HEAD (`F3.md:6-7`). `K4.md:10-12` still proposes underscore tokens (`l7-05-search_bytes`, `l7-06-inspect_with_objdump`); used verbatim they map 72/78 (`C3.md:9,13`) and conflict with ruling (a). This checks retained records, not re-execution.

## VERDICT
FINDING: entry 6 is citation-clean; entry 5's facts trace but E5D needs the three header fields and wider ranges (`leg-7.md:3-13,21`; `receipts-B/leg-7.md:21-25,32,60`); keep K4's underscore tokens out.
