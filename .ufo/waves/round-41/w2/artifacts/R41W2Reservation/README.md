# R41W2Reservation artifacts (all re-runnable, no vendor bytes)

Session dir used by the transcript scans: `~/.omp/agent/sessions/-Projects-shokunin/2026-10-26T15-10-35-484Z_01a178c3-6bdc-745c-b5ed-ce700e7035cd/`
(one `<Seat>[-N].jsonl` per wave-1 seat; 43 seats = 41 registry members + KaidokuR41 + KengakuR41).

Rebuild:

    L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; S=<scratch>; mkdir -p $S/frz
    git -C $L archive d764389e9cbe61b9d1b07538ff3bff02d50bb34f .ufo/waves/round-41/w1 | tar -x -C $S/frz
    python3 scan.py $S/frz scan-freeze-tree.json                       # 1044 files at the freeze commit
    python3 scan.py $L/.ufo/waves/round-41/w1 scan-live.json           # 1064 files, working tree
    python3 subjects.py $S/frz subjects-freeze-tree.json               # envelope subject digests vs the nine reserved digests
    python3 subjects.py $L/.ufo/waves/round-41/w1 subjects-live.json
    python3 tx-scan.py  <session dir> $L/.ufo/waves/round-41/w1/swarm-registry.json tx-scan.json
    python3 tx-scan2.py <session dir> $L/.ufo/waves/round-41/w1/swarm-registry.json tx-exec2.json

Files: `scan*.json` text/hash scan (hex8 of the 4 pins + 5 image/member/nested digests; REA/unblob markers; file-bytes
equality), `subjects*.json` envelope subject-digest census, `tx-scan.json` every tool call that names a reserved id or
can execute REA/unblob (3955 calls, 43 seats), `tx-exec2.json` the exec-capable bash/eval calls with carrier-source
references, `direct-invocations.json` 103 textual `extract-firmware`/`unblob` command matches (many are prose, see report),
`carrier-cache-or-fetch-invocations.json` every counter/fetch-vendor invocation with its cache, `report-statement-counts.json`.
