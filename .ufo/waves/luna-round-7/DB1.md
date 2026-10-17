## CLAIM
Entry 1 (E1D's proposed `inspect_go_binary` text, E1D.md:13-26) is claim-by-claim derivable from the leg-3 receipts; three supporting lines fall outside its cited ranges and the house metadata header is absent.

## METHOD
Read-only mapping of every claim in E1D.md:13-26 and Z1.md:10-24 against `.ufo/waves/luna-round-6/receipts/leg-3.md` (222 lines), `receipts-B/leg-3.md`, SC1.md, and `corpus/QUALITY.md:11-25`. Cross-checked M1.md:11, K3.md:8, C3.md:9, GB1.md:13. Both receipts HEAD-tracked (`git cat-file -e HEAD:...` → present). No probes, network, or writes outside this file.

## FINDINGS
- Derivable, with exact support: package/server 6.5.0 `leg-3.md:3,7`; artifact path/ELF x86_64/SHA-256 `:5,74-79`; call frame and args `:17,52`; Evidence ID `:71`; bytes 29,327,600, ELF/amd64, inline build info at 28,873,984, `go1.26.5-X:nodwarf5`, module path and `GOOS/GOARCH/CGO_ENABLED` `:93-108` (module_text `:108`); unknown/limitations `:8,169-181`. Lane-B corroboration derivable inside E1D's B-ranges: same hash `receipts-B/leg-3.md:17-18`, same Evidence ID `:42`, RESULT `:86`.
- Citation gaps (three holes between E1D.md:26's cited ranges): schema "accepts only `path`" needs `leg-3.md:20-49`; provider `go-build-info` v1 needs `:81-85`; "`module.complete=true` and no unparsed lines" needs `:164-166`. Append `:20-49,81-85,164-166`.
- Format gaps: E1D.md:13-26 lacks the required `source:`/`verified-at:`/`recheck:` opening (`CORPUS.md:17`; ruling d; GB1.md:13 flags the same for Z1.md:10-24). Rows M1.md:11 and K3.md:8 still use underscore stem `2026-10-16-l7-01-inspect_go_binary` while the landing name is hyphenated (E1D.md:8; ruling a; C3.md:9 shows the token truncating at the underscore).
- Z1.md:10-24 (recommended text) is likewise derivable; its ranges `:71-108,:118-166` cover provider and complete/unparsed, and it omits the schema sentence; it also lacks the metadata header.

## THREATS
Derivability rests on retained HEAD receipts, not re-execution. Command A counts, prior-72 byte identity, and the other five entries were not verified here.

## VERDICT
FINDING: Entry-1 content is fully receipt-derivable; before landing add the metadata header, extend leg-3 citations to :20-49,81-85,164-166, and hyphenate the l7-01 row stems.
