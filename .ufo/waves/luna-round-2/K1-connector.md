## CLAIM
REA-version calibration’s sibling-overlap status, based on committed province boundaries only.

## METHOD
Compared `git -C <lane> show HEAD:PROVINCE.md | nl -ba` for kaidoku lines 39-42 and 88-109, and each sibling’s committed `PROVINCE.md`; no live probe or config-file inspection.

## FINDINGS
- **tsukuroi:** No substantive overlap: it owns host package, systemd, driver/firmware and boot state, and refuses binary RE; the calibrated REA client-version inventory is not among those surfaces (`tsukuroi-shokunin/PROVINCE.md@HEAD:3-17`; `kaidoku-shokunin/PROVINCE.md@HEAD:39-42`).
- **kama:** No substantive overlap: its claimed config-related surface is model endpoint/baseURL and served-model health; its config-root rule prohibits writes, not REA MCP pin inventory (`kama-shokunin/PROVINCE.md@HEAD:3-15,45-49`; `kaidoku-shokunin/PROVINCE.md@HEAD:39-42`).
- **mori:** The required report is in `.ufo/waves/luna-round-2/`, a namespace adjacency to mori’s `.ufo/waves/*` settlement state; this report does not alter the registry/results pair or fleet telemetry, so the adjacency is recorded, not absorbed (`mori-shokunin/PROVINCE.md@HEAD:3-10`; report path).
- Kaidoku’s Core explicitly owns the REA MCP surface and lists the Devin, OMP, and Kimi client-config paths; its adjacent boundary reserves editing client configs and setup/install actions to the operator (`kaidoku-shokunin/PROVINCE.md@HEAD:39-42,101-106`). Thus those read-for-calibration paths are inside kaidoku’s declared surface; this seat made no config edits.

## THREATS
This is a document-scope comparison only. I did not inspect live config contents or verify sibling runtime state; province documents may not reflect unrecorded changes.

## VERDICT
CLEAN