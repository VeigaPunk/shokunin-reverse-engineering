# CC7 — compare leg 7 (search_bytes ELF magic)

## CLAIM
Lane-B re-run of leg 7 (MCP `open_binary` on `/bin/true`, then `search_bytes` pattern `7f 45 4c 46`) reproduces the pre-registered RESULT class; the cross-lane comparison of hit + offset agrees exactly, and full stdout is byte-identical to Lane A's.

## METHOD
- Protocol: `.ufo/waves/luna-round-6/P0.md:9` (L7 = `search_bytes` ELF magic on small ELF, hit + offset) and lane-A leg-7 receipt (`receipts/leg-7.md:3-15`), read as the compare assignment requires.
- Ran `cd /tmp && npx -y rea-agents@6.5.0 --mcp` via own stdio client (`/tmp/rea-cc7/runner.mjs`): initialize (id 1), initialized, `open_binary /bin/true` (id 2), `search_bytes` (id 3). Raw-byte fd capture, 240s per-response deadline, stdin-close shutdown.
- Carrier `/bin/true` -> `/usr/bin/true`, 43320 B, sha256 `8bc9a73a…02d` verified pre-run.
- Compare method: sha256 + `cmp` of my raw stdout vs lane-A embedded stdout (its extract first confirmed to hash to lane A's declared value); jq extraction of hit/offset.

## FINDINGS
- My stdout: 19151 B, sha256 `3492d27d66e0…29a8` = lane-A declared stdout sha; `cmp` byte-identical.
- Hit: exactly 1 match. Offset: `file_offset 0` (`address 0x100000`, `segment_2.1`); searched 33668 B, complete true — both lanes equal.
- Exit 0; server exited normally on stdin close (no kill). Client times: init 655ms / open_binary 24ms / search_bytes 5076ms. stderr differs only in timestamp/duration fields (both lanes 2 `status:ok` lines).
- Receipt `receipts-B/leg-7.md` (22879 B): embedded stdout re-hashed `3492d27d…29a8` and offset-`cmp`'d byte-clean against the live capture.
- No config edits; post-run `git status` shows only pre-existing untracked `.ufo/` entries; HEAD `f0e8cde` unchanged.

## THREATS
- Byte-identity is specific to this carrier/host (sha pinned above); only stderr timing varies run-to-run.
- Concurrent lane-B seats probed while mine ran (other npx processes seen); no interference observed in results.
- npx cache served rea-agents 6.5.0; registry availability was not exercised.
- stdout evidence_id/profile digests matched across lanes, but were not independently re-derived from the carrier bytes.

## VERDICT
CLEAN — leg 7 RESULT class observed; hit + offset and full stdout bytes agree cross-lane; hashed receipt, server terminated.
