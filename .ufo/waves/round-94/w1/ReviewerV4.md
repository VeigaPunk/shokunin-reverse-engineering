# ReviewerV4 — round-94 wave-1 seat report (R94-C1 instrument review)

Seat: ReviewerV4 (reviewer), lane kaidoku, round 94, wave 1.
Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
Frozen declaration commit reviewed: **dd4524916a0332bb65f83525532da1c1b8d709de**
Scratch (deleted before yield): /fast/scratch/hyaku/kaidoku-r94/ReviewerV4

## Verdict

R94-C1's instrument pair passes all five reviewer-contract items (a)-(e) with **zero findings
above NONE**, at the frozen commit, on an end-to-end re-execution from source:

- **(a) v3 import + score namespace — PASS.** v4 imports v3 by path (v4:35 `V3 = HERE/../round-93/…`,
  v4:45 `_load` at import time) and calls `v3.score(args)` (v4:124) with its own argparse
  Namespace. v3.score reads `root, repair_cmd, work, rev, expect` — all set by v4's parser
  (`json_out` is unread by v3.score). v4's wrapper extends v3's verdict dict with
  `tool/verdict_counter/verdict_sha256/counter_sha256/exit` (v4:125-129), never overwriting
  v3's verdict fields.
- **(b) receipt writer — PASS.** `_default` (v4:53-58): bytes/bytearray → `{"bytes","sha256"}`,
  every other unknown type raises TypeError (no str() fallback — the selftest case
  `unknown-type-raises` pins this as v4's own stricter contract; per ScoutS319's probe the
  stdlib would silently accept a str() fallback, so this is v4-specific strictness, correctly
  framed in the docstring as "JSON encodable version … or raise a TypeError", not as a
  stdlib rule). `write_receipt` (v4:60-73) is `open(tmp) → json.dump(default=_default) →
  os.replace(tmp, path)`; `except BaseException` catches KeyboardInterrupt during dump and
  removes the tmp before re-raising; a `.tmp` symlink pre-plant scenario leaves `<json-out>`
  absent while the victim file is clobbered (SentinelWrite's MED, reproduced in my scratch —
  attacker interaction required, out of the frozen instrument's own threat model, recorded)
  and `<json-out>.tmp` is never left behind by an in-process failure.
- **(c) exit codes + stdout line — PASS.** `return code` (v4:134) is v3's verdict exit
  (0/1, or the early `2, {unevaluable}` paths threaded through the same wrapper);
  `print(label|unevaluable, "met", met_target, "exit", code)` (v4:132-133) matches the
  counter's LINE regex `^(.*) met (True|False|None) exit (\d+)$` (c1:29).
- **(d) agreement counter — PASS.** PREDICTED (c1:28) is exactly the frozen predicate
  (pos True 0; F1-F3 False 1). agree (c1:59-60) compares label string, `met is s_met`
  (identity: covers None vs True/False without exception), exit equality, and `int(rc_text) ==
  s_exit` with an `isdigit()` guard (c1:55). A truncated receipt (`json.loads` ValueError →
  `isinstance(rec, dict)` False → valid False) and a missing `.rc` are both invalid; a None
  met_target can never satisfy `predicted`. Confirmed negatively on the committed base
  (valid/agree/predicted 2/2/2, pos/F3 rows false against the truncated F3 receipt and the
  TypeError'd pos stderr). A live counter invocation without `.rc` files scored 4/0/0 and
  rc 1 — no silent acceptance.
- **(e) frozen pins — ALL MATCH** at the frozen commit by `sha256sum` on the cloned bytes
  (see sha256.txt): v4, agreement, v3, r92 battery, r92 v2, manifest. Runtime support also
  verified: /usr/bin/env = fresh-pack pin, /usr/bin/upx cf2f6e7c… = kill-rule prefix, upx 5.2.0
  self-sha = v2.UPX_SHA256 constant guarded at runtime (v2:209). Lane `git status` showed only
  untracked wave bookkeeping; no tracked bytes drifted.

## Live reproduction (this run, scratch clone at dd45249)

- v4 `--selftest`: rc 0, 3 cases ok (selftest.txt).
- Frozen counting command, four runs: pos rc 0 (stdout line `repaired 12 of 12; … met True
  exit 0`), F1/F2/F3 rc 1. No `.tmp` residues.
- `python3 tools/round-94/c1-receipt-agreement.py --dir $S/work --prefix c1-v4`: rc 0,
  `counts_of_4 {valid 4, agree 4, predicted 4}, met true` — exactly the frozen target.
  Receipt copy: `counter.json`.
- First counter invocation without rc files printed valid 4 / agree 0 / predicted 0, rc 1 —
  the counter correctly invalidates runs whose captured artifacts are incomplete.

## Residual risk (recorded, does not change the frozen verdict)

- `os.replace` sits outside the writer's try block: a replace failure after a successful dump
  leaves a stale `.tmp`, but the finalized `<json-out>` is never partial.
- Pre-planted `<json-out>.tmp` symlink is CONFIRMED harmful (SentinelWrite MED, reproduced in
  my scratch: victim file truncated and replaced by receipt bytes via `open(tmp,"w")` following
  the symlink; `<json-out>` ends up a symlink to the victim after os.replace): attacker
  interaction required; out of scope of the frozen instrument's own claims, recorded here and
  in SentinelWrite.md for the L1.
- The counter's stdout regex is start-anchored only; safe for the frozen v4 line shape.
- I did not review R94-C2's counters (craft-citation-semantic / depth-blocks-v2/v3) — scoped
  to the assigned C2 reviewer seat.

## Reviewer scope note (routed per contract)

ScoutS319's source-evidence probes (json.dump/JSONEncoder anchoring for the S319 row, the
S050 duplicate-URL risk, and the runtime non-enforcement of the docs sentence) belong to the
C2 knowledge-entry seat, not this C1 instrument review; I relayed them to
ScribeKnowledge-28 as the drafting seat. Relayed message text above in my transcript.

## Files written (seat dir)

- `.ufo/waves/round-94/w1/ReviewerV4/ReviewerV4.md` — full findings report (parent)
- `.ufo/waves/round-94/w1/ReviewerV4/sha256.txt` — pin verification receipt
- `.ufo/waves/round-94/w1/ReviewerV4/selftest.txt` — v4 selftest receipt
- `.ufo/waves/round-94/w1/ReviewerV4/counter.json` — live agreement counter receipt
- `.ufo/waves/round-94/w1/ReviewerV4.md` — flat seat summary pointer (per milestone trail)

## Tooling note

No tools installed (stock git, python3.14, sha256sum). Scratch to be deleted before final yield.
