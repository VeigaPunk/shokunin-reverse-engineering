# ConnectorOverlap — scoped report (R95-W1, read-only sibling-overlap scan)

Full findings: `.ufo/waves/round-95/w1/ConnectorOverlap/overlap.md`. Summary:

## Verdict

- **Receipt world-binding class (R95-C1): no overlap.** No sibling round-95 declaration
  claims it (only kake, lore, mori have round-95 wave dirs; kake's freeze.md covers its
  self-assessment counter and conditional contract; lore/mori cover snapshot preservation
  and census). Landed sibling instruments of the same family, cite-as-independent-discovery:
  kama r72 RECEIPT_TIP_BINDING (revision binding, plans/round-72-claims.md:67-90), kumitate
  receipt-bind.mjs (receipt↔instrument bytes, fail-closed symlink rows, O_NOFOLLOW read),
  chousa receipt-pin.py + digest-in-tree.py (header consistency; pins must re-derive from
  committed bytes).
- **Symlink write-escape in a receipt writer (R95-C1 probe / F1): no sibling claim; class is
  fleet-recurring.** Hardened precedents: souji-receipt-write.py:530-542 (r60: mkstemp +
  stale-temp sweep + "a temp is never a receipt"), kama-llamacpp-live.py:337-347 (r49
  Sen1Witness F1: O_EXCL+O_NOFOLLOW pid temp — same mechanism as kaidoku v4's defect,
  remedied there in r49), kaidoku tools/round-42/fetch-carrier.py:276,307 (lane's only
  O_NOFOLLOW site). Unremediated v4-shape writers remain in sibling live trees, cleanest
  instance: kake scripts/instrument_receipts.py:643-646 (`temporary = destination + ".tmp"`,
  plain open → follows a planted symlink; writes corpus/knowledge/instrument-receipts.json;
  digest 162dd685…, kake commit 4f443b3f, file last touched 2026-11-03); also tabi
  aria-loopback-round13.mjs:103-105,805-807, tameshi bash-witness-study.py:795-797, mori
  round13-16 regression writers, kotodama gate fixture pinners, kumitate
  make-dispatch-actual.mjs:384-386.

## Lane facts at 4bda1d1dd3788973f10e61212b70df18b3b14ea0 (git grep, rc 0)

- Receipt-writer-role call sites: tools/round-94/stop-boundary-repair-battery-v4.py:62,65-68,131
  (the F1 carrier, `path + ".tmp"` plain open); tools/round-95/stop-boundary-repair-battery-v5.py:76-79,252
  (hardened mkstemp writer); tools/round-95/symlink-probe.py:63-65,98-99,103-106 (probe,
  own receipt direct open); tools/round-95/c1-agreement-v2.py:181,243,280;
  tools/round-95/c1-forgery-refusal.py:131,269; tools/round-93/stop-boundary-repair-battery-v3.py:352-353;
  tools/round-93/craft-citation-semantic.py:276-277 — all direct-open except v4 (temp) and v5 (mkstemp).
- Scale: 265 files with json.dump, 155 with --json-out, 7 with mkstemp, 1 with O_NOFOLLOW.

## Proposed move

Ground R95-C2 block 34's `temp-file symlink escape` row in fleet-wide recurrence: cite the
pinned sibling instances (digests above) beside the S320 O_NOFOLLOW entry and record the
unclaimed sibling instances in the round-95 lesson. Improves depth + freshness; touches no
frozen byte, so C1's kill-rule diff clause stays empty.

## Method notes

- Two early wildcarded grep calls (`*-shokunin/tools` + `!` exclusion) returned false
  "No matches found"; discarded. All numbers from explicit-path scans (11 sibling trees,
  3 sibling round-95 wave dirs, 12 sibling plans dirs).
- Read-only throughout: grep/sha256sum/git rev-parse/git log only; no sibling or lane file
  edited; no host change; no tool installed.

## Files written

- .ufo/waves/round-95/w1/ConnectorOverlap/overlap.md (full tables, verdict, move, risks,
  second-order traces, verification commands)
- .ufo/waves/round-95/w1/ConnectorOverlap.md (this report)
