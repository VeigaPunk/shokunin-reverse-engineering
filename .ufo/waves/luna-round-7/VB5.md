## CLAIM
Each Z-recommended entry text's quoted outputs (entries 1–6) are consistent with the round-6 receipt bytes; ≥3 exact strings spot-quoted per entry.

## METHOD
`grep -F` byte-exact spot-checks against `.ufo/waves/luna-round-6/receipts/leg-{3..8}.md` and `receipts-B/leg-{3..8}.md`; rendered values compared against receipt JSON fields. Read Z1–Z6, E1D–E6D, G1/G4/G6, SC1. Read-only; no probes, network, or tracked-file writes.

## FINDINGS
Byte-verbatim (`grep -F` hit):
- E1 (Z1 text): `70f68a77…45c9`, `go1.26.5-X:nodwarf5`, `github.com/docker/cli/cmd/docker`, `ev_6718…6a4b`, `CGO_ENABLED=1`; provider `"id":"go-build-info"…"version":"1"` and guards 256/1/16/8 MiB present (leg-3:172,208).
- E2 (E2D): `1b44ed…d1f7`+`ev_0618…99d3`, `d006ac…ecae42`+`ev_9ea9…bff2`, `da80ed…0a1e` beside `"evidence_kind":"inferred"`,`"file_offset":2287779`; B `"rustc_commit":null` (leg-4:28; B:47).
- E3 (E3D): hash, Evidence ID, and the `timeout 240 npx -y rea-agents@6.5.0 inspect-electron-fuses …` command verbatim (leg-5:3,8); all nine fuse name/state pairs match.
- E4 (G4): hash, Evidence ID, `package_index` verbatim; `"indexes":[],"views":[],"triggers":[]` (B:35).
- E5 (E5D): hash, Evidence ID, `0x100000`, `7f 45 4c 46`, `33668` verbatim; B compare confirms same hit/offset (B:68).
- E6 (E6D): hash, Evidence ID, `HAS_SYMS, DYNAMIC, D_PAGED` verbatim.

Non-verbatim renderings (values match, surface differs): E3 `RunAsNode=disabled` vs `"name":"RunAsNode","state":"disabled"`, offset `35,260,752` vs `35260752`; E4 `wal:null`/`rows:null`/`column_count:2` vs `"wal":null`/`"rows":null`/`"column_count":2`; E5 `33,668` vs `33668`, Z5's `searched.bytes:33668` dossier-path form; E6 `0x3cf0` vs `0x0000000000003cf0`, `objdump -f /usr/bin/jq` vs `"provider_executable":"objdump","command_arguments":["-f","/usr/bin/jq"]` (literal string absent from leg-8 A; appears once as prose in leg-8 B:29). No fabricated string or wrong value found.

## THREATS
Renderings could drift in later edits; E3's `=`-form and E6's `0x3cf0`/argv are furthest from byte-verbatim. Z2/Z5 absence claims for E2D/E5D are stale vs the current tree (both exist). Pointer accuracy checked only where sampled.

## VERDICT
CLEAN — every sampled quote resolves to receipt bytes or a value-identical rendering; no mismatch or fabrication found.
