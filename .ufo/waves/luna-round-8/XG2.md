## CLAIM
Current `/usr/bin/docker`, `/usr/bin/rg`, and `/usr/bin/jq` match all three round-6 SC SHA-256 pins. However, the 6.5.0 primary L4 did not use `/usr/bin/rg`, so these pins do not establish same-carrier identity for all three across the primary batteries.

## METHOD
Read round-6 SC1/SC2/SC6 and L3/L4/L8 receipts; ran `sha256sum /usr/bin/docker /usr/bin/rg /usr/bin/jq` and `stat -Lc '%n -> %N | size=%s | inode=%i | device=%D'` on those paths. No REA/MCP calls or writes beyond this report.

## FINDINGS
- Current hashes: docker `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`; rg `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`; jq `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. Each exactly matches its SC pin (SC1:10-11, SC2:10, SC6:8); current sizes are respectively 29,327,600, 4,377,936, and 30,800 bytes.
- Docker and jq were also the 6.5.0 primary L3/L8 carriers: `receipts/leg-3.md:5,17`; `receipts/leg-8.md:8-12` records jq's matching digest.
- SC2 pins `/usr/bin/rg`, and lane-B L4 used it with that digest (`receipts-B/leg-4.md:14-18`). Primary lane-A L4 instead used Signal's `libsignal-client.node` (`receipts/leg-4.md:9-21`). Thus the rg match is against the SC2 candidate and lane-B run, not the primary lane-A L4.

## THREATS
A matching current SHA-256 identifies the same bytes as the recorded pin, but does not prove which bytes a later 6.4.0 process consumed. Carrier pins alone also do not pin the full execution environment or reproduce outputs.

## VERDICT
FINDING: Docker and jq match the 6.5.0 primary carriers; rg matches the SC2/lane-B carrier, not primary lane-A L4, so full same-carrier reproduction across both primary batteries is not established.
