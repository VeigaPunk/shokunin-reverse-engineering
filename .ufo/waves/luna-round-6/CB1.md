# CB1 — forge attack on receipts-B

## CLAIM
receipts-B can be trivially faked by copying lane A's stdout: the copy passes the pre-registered cross-lane comparison, and BB seats' self-authored reports defeat nothing. Attack demonstrated by construction; no actual fraud found.

## METHOD
Attack assembled offline, zero execution: `grep -m1 -F '{"result":{"_meta"' receipts/leg-9.md | sha256sum` → `2b596b31…39be41` = hash recorded at `receipts/leg-9.md:11`: lane-A text alone yields its exact hashed bytes. Cross-lane census: lane-A stdout hashes occur in `receipts-B/leg-{1,2,7,10}.md` (e.g. `38d44bf8…` at `receipts-B/leg-2.md:8` = `receipts/leg-2.md`), though lane-B client identities differ (`receipts-B/leg-2.md:4` BB2 vs `receipts/leg-2.md:3` EX2). Trusted control: my /tmp run of the leg-9 route (npx rea-agents@6.5.0 mcp, unique clientInfo `luna-round-6-CB1-forge`, wait-for-id:2 then EOF) exited 0, no leftovers; raw stdout `1ff84c06…` and frame `2b596b31…` both equal lane A's; client id occurs 0× in stdout.

## FINDINGS
Attack: copy command/stdout/stderr/exit/hash from `receipts/leg-N.md` into `receipts-B/leg-N.md`, relabel request frames, write a matching BB report — reads/writes only, no execution. Machine-checkable fields stay consistent because honest lane-B reproduction is byte-identical: my control with a different client identity proves hash equality, BB1/2/7/10 receipts show it too. Copying inherits class agreement and grants hash agreement; demanding lane-B≠lane-A hashes would fail those four honest receipts, so no class/hash comparison separates copy from run. Only stderr varies across honest runs (times 18:19:26 vs 19:03:47) — unhashed, non-comparable, trivially regenerated. Scratch files (`/tmp/rea-bb7/stdout.raw` matches declared hash) are equally re-creatable.

## THREATS
Feasibility, not observed fraud: run-vs-copy is undecidable from artifacts. A /proc watcher (PID 16242) logged new npx/node starts during the wave; it contradicts non-execution only if cross-referenced per seat — not part of the comparison, and defeated by a decoy process. Per-seat nonces inside hashed output, or wire capture, would defeat the attack; neither exists. My control used lane-A method reading (assignment-required), so it shows determinism, not independence.

## VERDICT
FINDING: receipts-B are trivially forgeable by copying lane-A stdout; the pre-registered cross-lane comparison cannot detect it and BB reports add no anchor.
