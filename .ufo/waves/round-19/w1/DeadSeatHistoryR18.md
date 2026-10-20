# DeadSeatHistoryR18 — round-19 w1 (read-only scout)

Seat `KaidokuR19.DeadSeatHistoryR18`. Leaf, read-only. Writes: this report only. No lane/git/jj write, no REA or Ghidra call, no carrier executed, no install. Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (contract B).

**Outcome: all five terminal records recovered verbatim; none is `unrecoverable`.** Four of the five are error/abort-terminated with no report; `DecisionRuleApply` completed and returned late. The precise record is **3 error deaths + 1 abort = 4 seats without a report**, not "1 dead + 4 not returned" (SCORECARD) and not "3 dead" alone (fleet erratum) — see Findings 1–3.

## Where the text lives (observed)

`agent://<id>` is empty for the four dead seats (`GatePRODUCERREV`, `GateSUMSRUNLOG`, `TruthREGISTRY`, `ShonenLines`) and returns the final message for `DecisionRuleApply` — it carries only published output. The sanctioned `history://<id>` render shows `GateSUMSRUNLOG`'s refusal truncated at `Refusal (cyber): …`; the full sentence is only in the per-seat event log. The canonical record is the session transcript pair:

`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.<seat>.jsonl`

Each file ends in `{"type":"custom","customType":"session_exit","data":{"reason":"dispose","kind":"normal"}}` — dispose is the harness teardown, not a seat outcome; the outcome is the last `message` with `role:"assistant"`. The `.md` sibling is the published report (0 B for the dead seats).

Agent ids are the ones the assignment names: `wave2-assignments.json:7` (GatePRODUCERREV), `:9` (GateSUMSRUNLOG), `:10` (TruthREGISTRY), `:53` (DecisionRuleApply), `:86` (ShonenLines); registration at `wave2-registration.json:64-66`, `:86-88`, `:97-99`, `:570-572`, `:933-935`.

## r18-dead-seats.json

```json
{
  "schema": "r18-dead-seats-v1",
  "round": 18,
  "baseline": "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0",
  "transcript_dir": "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18",
  "seats": [
    {
      "seat": "GateSUMSRUNLOG",
      "agent_id": "KaidokuR18.GateSUMSRUNLOG",
      "wave": "w2",
      "report_path": null,
      "terminal_state": "error",
      "stop_reason": "error",
      "provider": "devin",
      "model": "gpt-6-1-sol",
      "terminal_at": "2026-10-20T17:01:28.430Z",
      "error_line": "Devin stream error failed_precondition: Your weekly usage quota has been exhausted. Visit https://app.devin.ai/settings/usage to purchase on-demand usage or turn on auto-reload. (trace ID: 6875f7fb519a5a259ace0b8cc505f6f3)",
      "preceding_errors": [
        {
          "at": "2026-10-20T17:01:17.565Z",
          "provider": "anthropic",
          "model": "claude-opus-5-5",
          "kind": "tool_refusal",
          "line": "Tool call was not executed because the provider stream ended with an error before the tool could run: Refusal (cyber): This request triggered restrictions on violative cyber content and was blocked under Anthropic's Usage Policy. To learn more, see https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback."
        },
        {
          "at": "2026-10-20T17:01:27.365Z",
          "provider": "openai-codex",
          "model": "gpt-6.1-sol",
          "kind": "error",
          "line": "Codex error event: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your request. Otherwise, confirm that the access_programs.cyber parameter is set to the appropriate tier, and note that some cybersecurity requests are still limited, even when Daybreak is on. (code=cyber_policy)"
        }
      ],
      "evidence": [
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.GateSUMSRUNLOG.jsonl:159",
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.GateSUMSRUNLOG.jsonl:164",
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.GateSUMSRUNLOG.jsonl:167"
      ],
      "exit_code": null,
      "exit_code_note": "fleet report says exit 1; transcripts record no exit code"
    },
    {
      "seat": "GatePRODUCERREV",
      "agent_id": "KaidokuR18.GatePRODUCERREV",
      "wave": "w2",
      "report_path": null,
      "terminal_state": "error",
      "stop_reason": "error",
      "provider": "zai",
      "model": "glm-5.3-flash",
      "error_status": 429,
      "terminal_at": "2026-10-20T17:21:57.287Z",
      "error_message": "Retry budget exhausted after 10 retries: 429 Rate limit reached for requests\nRate limit reached for requests (type=1302)",
      "error_line": "Rate limit reached for requests (type=1302)",
      "observed_429_stops": 20,
      "evidence": [
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.GatePRODUCERREV.jsonl:120"
      ],
      "exit_code": null,
      "exit_code_note": "fleet report says exit 1; transcripts record no exit code"
    },
    {
      "seat": "TruthREGISTRY",
      "agent_id": "KaidokuR18.TruthREGISTRY",
      "wave": "w2",
      "report_path": null,
      "terminal_state": "error",
      "stop_reason": "error",
      "provider": "zai",
      "model": "glm-5.3-flash",
      "error_status": 429,
      "terminal_at": "2026-10-20T17:24:05.997Z",
      "error_message": "Retry budget exhausted after 10 retries: 429 Rate limit reached for requests\nRate limit reached for requests (type=1302)",
      "error_line": "Rate limit reached for requests (type=1302)",
      "observed_429_stops": 24,
      "evidence": [
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.TruthREGISTRY.jsonl:134"
      ],
      "exit_code": null,
      "exit_code_note": "fleet report says exit 1; transcripts record no exit code"
    },
    {
      "seat": "ShonenLines",
      "agent_id": "KaidokuR18.ShonenLines",
      "wave": "w2",
      "report_path": null,
      "terminal_state": "aborted",
      "stop_reason": "aborted",
      "provider": "zai",
      "model": "glm-5.3-flash",
      "terminal_at": "2026-10-20T17:31:34.206Z",
      "error_line": "Request was aborted",
      "preceding_error": {
        "at": "2026-10-20T17:30:55.068Z",
        "line": "429 Rate limit reached for requests / Rate limit reached for requests (type=1302)"
      },
      "observed_429_stops": 28,
      "aborted_by": "not recorded; parent KaidokuR18 task completed at 17:31:34.215Z (9 ms later), so parent teardown is the inference",
      "evidence": [
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ShonenLines.jsonl:155",
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl:1267"
      ],
      "exit_code": null,
      "exit_code_note": "no exit code recorded"
    },
    {
      "seat": "DecisionRuleApply",
      "agent_id": "KaidokuR18.DecisionRuleApply",
      "wave": "w2-late",
      "report_path": ".ufo/waves/round-18/w2/DecisionRuleApply.md",
      "terminal_state": "completed",
      "stop_reason": "stop",
      "provider": "anthropic",
      "model": "claude-opus-5-5",
      "terminal_at": "2026-10-20T17:20:19.673Z",
      "error_line": null,
      "report_written_at": "2026-10-20T17:19:26.842Z",
      "report_lines": 371,
      "final_message_first_line": "I applied the frozen rule to the 15 observations and the verdict is **confirmed**; my report's first line is **PARTIAL** only because two written provenance statements are false.",
      "evidence": [
        "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.DecisionRuleApply.jsonl:355",
        "/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:84"
      ],
      "exit_code": null,
      "exit_code_note": "not a dead seat; returned late and was integrated"
    }
  ]
}
```

## Findings

1. **Count closure (observation).** `SCORECARD.md:2462` names five seats for a gap of four: 98 members (`.ufo/waves/round-18/wave2-registry.json`, 98) minus 94 `w2/*.md` reports. The four without a report are `GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY`; `DecisionRuleApply` has `.ufo/waves/round-18/w2/DecisionRuleApply.md` (371 lines, 31742 B, committed at main in `06df023`) and `agent://KaidokuR18.DecisionRuleApply` returns its final message. The 94/98 counts reproduce the round-19 draft `.ufo/waves/round-19/w1/ScorecardDeadSeatDraft.md:19`; this report adds the verbatim records it lacked.
2. **Both published counts are half-right (observation).** Fleet erratum `.ufo/reports/round-18/kaidoku.md:101`: "Dead seats in W2: 3 (GateSUMSRUNLOG, GatePRODUCERREV, TruthREGISTRY)". That is exact for error-terminated seats, but `ShonenLines` also ended without a report, at `stopReason:"aborted"` ("Request was aborted", 17:31:34.206Z). `SCORECARD.md:2462`'s "4 not returned" has the right cardinality with the wrong membership (it lists `DecisionRuleApply`, which returned; it omits the abort as a terminal state). The durable record is: **4 no-report seats = 3 error + 1 abort; 1 late report**.
3. **`GateSUMSRUNLOG` terminal cause (observation, with calibration correction).** The last assistant message is Devin quota exhaustion (17:01:28.430Z, `…jsonl:167`), not a policy refusal. Preceding it: an Anthropic `Refusal (cyber)` on a `write` (17:01:17.565Z, `:159`, "blocked under Anthropic's Usage Policy") and an `openai-codex` `cyber_policy` flag (17:01:27.365Z, `:164`). So `SCORECARD.md:2462`'s "provider usage-policy refusal" describes the 17:01:17 step, and `LOG.md:2178-2179`'s `"cyber" usage policy, exit 1` describes the refusal step plus a claim the transcript does not carry.
4. **The "exit 1" is not in the record (observation).** No transcript stores a process exit code; both the fleet report (`:84`, `:101`) and the committed `LOG.md:2178-2182` say "exit 1". `exit_code` is therefore `null` in the JSON (`not_recorded`), not confirmed. This closes open item 1 of `ScorecardDeadSeatDraft.md:47`.
5. **Who aborted `ShonenLines` (inference).** The parent transcript shows `KaidokuR18.ShonenLines [task] running up 43m10s` at 17:25:21Z (`…d07.jsonl:1264`), then the parent's `wait` result "KaidokuR18 [task] — completed … duration 1h9m" at 17:31:34.215Z (`:1267`). The seat's aborted message is 17:31:34.206Z — 9 ms earlier. No message names an abort actor. Inference: the L1 session's completion tore down its in-flight child; the direction (parent completion → child abort) is a 9 ms coincidence, not a recorded causal field. This closes open item 2 of `ScorecardDeadSeatDraft.md:48` as far as the record allows.
6. **Retry accounting (calibration).** The terminal text "Retry budget exhausted after 10 retries" is the harness budget. The transcripts hold 20 (`GatePRODUCERREV`) and 24 (`TruthREGISTRY`) assistant `stopReason:"error"` records each at `errorStatus:429`; `ShonenLines` holds 28 before its abort. Count of provider stops ≠ retry budget.
7. **`DecisionRuleApply` is not a death (observation).** It wrote the report at 17:19:26.842Z (`…jsonl` write tool result), stopped with `stopReason:"stop"` at 17:20:19.673Z (`:355`), and exited at 17:27:19.697Z. The fleet report `:84` records it as returned late and integrated. It belongs in `r18-dead-seats.json` only as `terminal_state:"completed"` (or omitted from a dead-only view).
8. **Freshness of the anchor (observation).** `SCORECARD.md:2462` exists at B (2471 lines) and is absent at the round-18 wave-2 REV `b2aad08` (2440 lines; no `W2: 98 seats` line). The R18 measured block post-dates `b2aad08`; the correction must anchor to B. The defect is stated at `corpus/lessons/round-18-verifier-spotcheck.md:197` and summarized at `:146`.

## Commands run (exit codes)

- `git -C <lane> ls-tree -r --name-only refs/heads/main .ufo/waves/round-18/w2 | grep -E 'GatePRODUCERREV|GateSUMSRUNLOG|TruthREGISTRY|ShonenLines|DecisionRuleApply'` → exit 0; one path, `DecisionRuleApply.md`.
- `stat -c '%s %n' .ufo/waves/round-18/w2/{GatePRODUCERREV,GateSUMSRUNLOG,TruthREGISTRY,ShonenLines,DecisionRuleApply}.md` → exit 1; the four are `No such file or directory`, `DecisionRuleApply.md` = 31742 B.
- `ls .ufo/waves/round-18/w2/*.md | wc -l` → 94; `ls .ufo/waves/round-18/w2 | wc -l` → 95; `wc -l < …/DecisionRuleApply.md` → 371; `python3 -I -B -c 'json.load(open("…/wave2-registry.json")); print(len(d["members"]))'` → 98 (combined exit 0).
- `grep -n "Dead seats in W2\|returned late" .ufo/reports/round-18/kaidoku.md` → exit 0; matches at `:84` and `:101`.
- `grep -n "Dead: GateSUMSRUNLOG\|Still running at" LOG.md` → exit 0; `:2178` and `:2179`.
- `grep -n "R18-DEADSEAT-RECORD\|3 dead\|4 not returned" corpus/lessons/round-18-verifier-spotcheck.md` → exit 0; `:146` and `:197`.
- Transcript parse (stdlib `json` over the five `.jsonl`, streaming, read-only) → all records parsed, no nonzero exit.

## Limits and hygiene

- The transcript directory is host-local under `~/.omp/agent/sessions/`; `history.db` holds prompt history only (`CREATE TABLE history (id, prompt, created_at, cwd, session_id, use_count)`), so the durable artifact is the JSON block above, not the path. `~/.omp/agent/agent.db*` and credential files were not opened.
- I did not verify the fleet "exit 1", the carrier/build claims, or any wave-2 report content; those are outside this target. I did not rerun any seat.
- No tool install or upgrade. No pacman. No `jj`, no git write, no REA/Ghidra, no carrier execution.
