## CLAIM
Compare the six frozen L9 names with A6’s reported 6.5-only MCP set and determine whether this round’s L9 exact-absence result corroborates A6 per name.

## METHOD
Read `.ufo/waves/luna-round-2/A6.md:5,8`, its cited 6.4.0 and 6.5.0 MCP tool-list receipts, and round-8 `PR1.md:11,18`, `PS3.md:18`, and receipt inventory. Searched A6’s 6.4 MCP receipt for the six names (no matches); its 6.5 MCP receipt contains them. No probe run.

## FINDINGS
All six frozen L9 names are in A6’s reported 6.5-only MCP set (`luna-round-2/A6.md:8`) and absent from its 6.4.0 MCP list (receipt search returned no matches):

| Name | A6 6.5-only | Round-8 L9 absence evidenced |
|---|---|---|
| `inspect_go_binary` | Yes | No |
| `inspect_rust_binary` | Yes | No |
| `inspect_electron_fuses` | Yes | No |
| `inspect_sqlite_database` | Yes | No |
| `search_bytes` | Yes | No |
| `inspect_with_objdump` | Yes | No |

Round-8 `PR1.md:11,18` marks L2 and L9 pending; `PS3.md:18` says L9 has no receipt. The available receipt inventory contains L1 and L6 only; neither `leg-9.md` nor `leg-2-tools.txt` is present. A6’s report is at `luna-round-2/A6.md`; no A6 report was found in `luna-round-4`.

## THREATS
A6’s older package/list comparison is not the missing round-8 tools/list output. Do not treat L9’s prediction or the A6 baseline as an observed L9 result.

## VERDICT
FINDING: A6 predicts all six names absent from 6.4.0, but round-8 L9 per-name corroboration is unverified until its receipt and L2 list exist.
