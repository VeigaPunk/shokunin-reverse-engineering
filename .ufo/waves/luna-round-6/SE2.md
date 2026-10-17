## CLAIM
No SHA-256 drift was observed in the three operator configs or `~/.bashrc` between the two captures. Full-battery immutability is unverified because the first capture followed L1.

## METHOD
Ran `date -Is && sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc` at `2026-10-16T18:17:17-03:00` and again at `2026-10-16T18:28:09-03:00`, after all ten leg receipts were present. The first receipt listing showed `leg-1.md` already existed (mtime Oct 16 18:16); L1's command is recorded at `EX1.md:5-8`.

## FINDINGS
Both captures returned the same hashes:
- `/home/vgpnk/.config/devin/mcp_config.json`: `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4`
- `/home/vgpnk/.omp/agent/mcp.json`: `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b`
- `/home/vgpnk/.kimi-code/config.toml`: `4af27747eb93244fcd343fc15552dc7b3ae689fcd7d00f2dea46faca1ca42707`
- `/home/vgpnk/.bashrc`: `7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598`

The three config hashes also match the older round-2 sentinel (`luna-round-2/S2.md:9-11`), but that is not a round-6 pre-L1 baseline.

## THREATS
No pre-L1 hash was captured in this seat, and S2 did not hash `.bashrc`; any mutation and reversion before 18:17:17 cannot be excluded.

## VERDICT
FINDING: full-battery config immutability is unverified because the baseline was taken after L1; no drift was observed afterward.
