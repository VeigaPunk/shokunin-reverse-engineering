# LB1V5Audit — round 52 wave 1

Verdict: **hypothesis confirmed; deterministic exactly-one violation**.

Read the v5 table/evaluator at `tools/round-50-c3/sqfs-triage-v5.py` (especially `NO_READER_FAMILIES`, `V5_ROWS` and `decision/classify`) and the round-49 census statement in `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` (lines 104–105: both readers refuse the DD-WRT no-pad `squashfs_v3_ddwrt` fixture; entry says receipt `v3-readers`). The probe applies v5 parsing/classification to all 126 envelope JSON files from the specified round-42 corpus and counts no-pad DD-WRT extractor-failure/zero-published-file cases routed to `legacy-body-failure` + `cross-read-legacy`.

Both independent invocations produced identical stdout SHA-256 `93b57e388e481128fa8e4479ab37e7c491240ec9f9dca5b39305de725913db96`, exit 0, exactly one violation: `dmg_Z3_v3ddwrt_inode_table`. Exact command each run: `python3 /fast/scratch/hyaku/kaidoku-r52/w1-LB1V5Audit/probe.py`; UTC `2026-10-30T10:48:58Z` for both. Retained exact stdout at `LB1V5Audit/run1.stdout` and `run2.stdout`; executable probe at `LB1V5Audit/probe.py`.

This establishes the specified C2 before-arm count for this minimal prototype/table bytes; it is not a run of the future v6 instrument or a full executability audit. Disk guard status was read before probe: `/tmp` 24%, `/var/tmp` 41%, `/fast/scratch/hyaku` 47%. No REA run, lane implementation, or tool installation was performed. Checks beyond the two synthetic/offline corpus passes: not run.
