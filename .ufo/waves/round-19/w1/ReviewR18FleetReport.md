# Round-18 fleet report review

## Axes and result

- **Calibration:** distinguish a direct contradiction from a later status update or missing evidence.
- **Freshness:** compare against the specified lane tip, `a245bb00c581ae3423a10a055c77d4bc873918df`.
- **Depth:** check role totals, committed report counts, install identities, and claim/run chronology.

**Result: no confirmed statement in the fleet report contradicts the lane files at that tip.** Seat totals and roles, install details, and the amended C1–C3 measurements agree. One later W2 disposition is not independently retained in the lane records; see residual risk below.

## Checks

### Seat counts — agree

**Observation.** Fleet report lines 83–85 give W1 89 seats/89 reports, W2 98 seats/94 reports, and 187 seats overall. At the requested tip, `wave1-spec.json` and `wave2-spec.json` have 89 and 98 items; role distributions match the report exactly. The committed `w1/` and `w2/` directories contain 89 and 94 Markdown reports. The four missing W2 reports are GatePRODUCERREV, GateSUMSRUNLOG, TruthREGISTRY, and ShonenLines. No count contradiction found.

**Command (exit 0):**
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && A=a245bb00c581ae3423a10a055c77d4bc873918df && for w in 1 2; do printf 'wave%s total=' "$w"; git --no-optional-locks show "$A:.ufo/waves/round-18/wave$w-spec.json" | /home/vgpnk/.local/bin/jq '.items|length'; printf 'wave%s role counts: ' "$w"; git --no-optional-locks show "$A:.ufo/waves/round-18/wave$w-spec.json" | /home/vgpnk/.local/bin/jq -r '.items[].role' | LC_ALL=C sort | uniq -c | tr '\n' ';'; printf '\nwave%s reports=' "$w"; git --no-optional-locks ls-tree --name-only "$A" ".ufo/waves/round-18/w$w/" | grep -c '\.md$'; done
```

### Installs — agree; lesson omission is separate

**Observation.** Fleet report line 90's Go archive hashes match the committed environment record at `.ufo/waves/round-18/w1/SentinelReaEnv.md:74-75` (also `carriers/build.sh:4`). The one `markdown-it-py==4.0.0` use is recorded as an ephemeral `uv run --no-project --with` in `.ufo/waves/round-18/w2/GateREGISTRY.md:91,154`; it explicitly says no global or tool install. No contradictory install disclosure found. The fleet report itself notes the Go install record was not copied into the round lesson; that is an omission, not a false statement about what was installed.

**Command (exit 0):**
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && A=a245bb00c581ae3423a10a055c77d4bc873918df && git --no-optional-locks grep -n -I -E 'markdown-it-py|uv run --with|bbca37cc395c974|2852af0cb20a131' "$A" -- .ufo/waves/round-18/w2/GateREGISTRY.md .ufo/waves/round-18/w1/SentinelReaEnv.md .ufo/waves/round-18/carriers/build.sh .ufo/waves/round-18/w2/ReopenS035.md
```

### Claims and chronology — agree, with a source metadata caveat

**Observation.** Fleet report lines 9–11 identify the original claims, and lines 16–22 describe the amendments and measured work. At the requested tip, `.ufo/waves/round-18/claims.json:10-28,33-40` contains C1–C3 and the amended 15-label C3 scope; the scorecard records 0→15 and 15/15 at `SCORECARD.md:2453`. The run log records 15 runs, starting at `13:24:07-03:00` and ending at `13:32:10-03:00`, consistent with report line 19's UTC interval. The amended claims file is present in the predictions commit, whose committer timestamp is `13:23:55-03:00`, before the first run. Thus the report's narrower statement that the amendments were committed before any `analyze` is supported.

**Observation / source caveat.** The claims file itself labels the amendment `13:25:00-03:00` and says “before any round-18 REA run”; the run log starts at `13:24:07-03:00`. The timestamp and parenthetical in that source metadata do not agree with the run log. This does **not** contradict the fleet report's commit-time wording, but the timestamp should not be treated as a reliable edit-time record.

**Command (exit 0):**
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && A=a245bb00c581ae3423a10a055c77d4bc873918df && printf 'amendment=' && git --no-optional-locks show "$A:.ufo/waves/round-18/claims.json" | /home/vgpnk/.local/bin/jq -r '.amendments[0].at' && printf 'first_run=' && git --no-optional-locks show "$A:.ufo/waves/round-18/runs/run-log.txt" | grep -m1 ' start ' && printf 'prediction_commit=' && git --no-optional-locks show -s --format='%cI' eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0
```

## Residual risk / verification gap — W2 dispositions

**Observation.** Fleet report line 84 gives two dead seats and says TruthREGISTRY and ShonenLines were not returned at integration; its line 101 erratum later gives three dead seats and says ShonenLines had not returned. The committed `SCORECARD.md:2462` is explicitly an integration-time snapshot: one dead (GateSUMSRUNLOG) and four not returned (including GatePRODUCERREV and TruthREGISTRY). The W2 registration records all four absent-report seats only as `kind:"spawn"`; their four report files are absent at this tip, so the lane snapshot retains no failure text for the reported causes.

**Inference.** Because the scorecard scopes its dispositions to integration and the fleet report/erratum are later, the status difference may be a later update rather than a factual contradiction. The lane commit cannot independently verify the added death classifications or causes; I therefore do not count this as a confirmed contradiction. This is the only material reconciliation gap found.

**Command (exit 0):**
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && A=a245bb00c581ae3423a10a055c77d4bc873918df && git --no-optional-locks show "$A:SCORECARD.md" | nl -ba | grep -F -C 2 '1 dead'
```

