# CR-1 proposed change — rule #14 corrected text (T5) + insertion constraint

Status: NOT applied — this seat may not edit `SKILL.md` (C1's rule lands via the
chain/parent at the records commit). Two parts: (a) replacement text for
EX-05's `fallback-rule14-candidate.txt`; (b) the insertion form, measured.

## (a) Replacement block text (measured: 14 rules / 14 resolved; prior-13
segments byte-identical under form B)

```
- **An artifact that records its own byte-identity re-derives that identity
  after every revision.** A verification block that states its subject's size,
  hash, or line count holds only against the subject's current bytes: the
  identity is re-derived after each revision, a stale self-identity voids the
  verification block rather than the work, and the integrator records the fresh
  identity at landing. The round-1 entry patch churned mid-wave: its recorded
  identity (8,316 B, `f95c5a05…`) stopped describing the artifact it produced —
  an independent re-apply read 8,598 B, `d8d85949…`
  (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; three
  applied identities within 20 minutes, `.ufo/waves/arc3-loop1-round1/claims/c1/
  VZ-1/verdict.md` debt D9) — and the landed bytes were re-derived at landing
  (10,225 B, `dd986f56…`; landing record, SCORECARD.md round-1 section, stamped
  2026-10-19). The landing instance is the EVM entry itself:
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`.
```

Changes vs EX-05's candidate, each with its measurement
(`claims/c1/CR-1/rule14-parser-results.txt`, `rv2-audit-on-draft.txt`):

1. Incident receipts added as real resolvable paths (CR-2's
   `entry-file-identity.txt`, VZ-1's debt D9). EX-05's candidate names
   "critic F2 plus the convergence seat" with **zero** receipt paths
   (`grep -c 'ufo/waves'` = 0), and D9 is VZ-1's debt label — no seat named
   "convergence" exists in either round's roster (r1 `claims-frozen.md:92-95`).
2. The one machine-counted citation is kept, reduced to a **path-only**
   `corpus/knowledge/…` reference and re-framed as the landing instance. In
   EX-05's form it was a bare `:1-12` range presented as evidence of the
   defect, while the range contains none of the incident
   (`F2|D9|stale|superseded|revis|defect` → 0 matches in lines 1-12) and the
   range's line 7 already drifted within the round (rev-B → landing diff,
   2 changed lines: measured). Path-only keeps command A resolution
   (`refs` non-empty, span 1-1 in range) and avoids a bare line range into an
   in-place-rewritten header (rule #11 form tension).
3. Landing record cited by content anchor + stamp, not line number
   (`SCORECARD.md:1366` is in-place-rewritten text under rule #11's own class).

If the chain prefers to keep a line range, the honest frame is the entry's
header block as the *landing* instance (its line 7 records the recheck
re-run), never as defect evidence — the defect lives only in the wave tree and
the records section.

## (b) Insertion form — use a byte-preserving insert

EX-05's `insert-rule.py`, run on a scratch copy of HEAD's SKILL.md with its own
candidate, yields a variant whose **rule-13 parsed segment gains one trailing
newline** (`insertion-form-check.txt`; base tail `.md:23-37\`).\n\n` vs variant
`.md:23-37\`).\n\n\n`; captured variant sha256 `079d44ab…`). Under command A's
own rule-split, "prior 13 rules byte-identical" therefore fails through that
tool. The form used by this seat (append after the section's existing trailing
blank line, so the separator newline before `## Config custody` is preserved)
keeps all prior-13 segments byte-identical for every candidate tested
(`rule-blocks-before.json`: the 13 baseline block sha256s to diff against).

Suggested landing verification:
`python3 claims/c1/CR-1/rule14-parser-test.py`-style extraction (or RV-2's
audit `--rev <work>` plus a 13-block sha256 diff against
`rule-blocks-before.json`) → expect `rules 14 / resolved 14 / depth 10.0`,
prior-13 block sha256s equal.

## Replay certificate available

`claims/c1/CR-1/self-identity-check.py` + `identity-replay.txt`: FRESH on the
landed entry (`dd986f56…`, 10,225 B, 33 lines) and on the EX-12 rev-B output
(`a5119120…`, 9,513 B, 32 lines); STALE on a revised-after-recording artifact.
Census v10 and the citation-drift probe read clean with that stale artifact
in-repo (`census-scope-check.txt`, `citation-drift-head.txt`) — the class is
otherwise uncovered.

## Addendum — live candidate status (same round, ~09:25Z)

The chain moved past this file's T5 while the seat was measuring. EX-01
`rule14.patch.md` (`885fa537…`, mtime 09:13:36) carries payload v2 (1,071 B,
`6cc388cb…`; the v1 → v2 supersession is recorded in its own revision note)
and pins the patched SKILL.md at 387 lines / `a8170b96…` — reproduced
independently in `/var/tmp/cr1-r2/live-apply` via EX-05's
`apply-rule14-from-artifact.py` (`3468c170…`). Parser on the reproduction:
14 rules / 14 resolved / depth 10.0. Two deltas vs this file's part (b):

- the live insertion REMOVES one trailing newline from rule-13's parsed
  segment (484 → 483 bytes) — same class as the +1 the earlier tool added;
  byte-preserving insert still required, or grade explicitly;
- the tool's docstring pins v1 (896 B / `a47dc38d…`, 385 lines /
  `19057c13…`) and its documented CLI invocation skips both identity asserts —
  fix it or record it before the work commit.

The T5 text remains the fallback-wording option; the citation fixes in part
(a) apply to the live payload's `corpus/knowledge/2026-10-19-arc3-r1-evm-
real-solc.md:7` reference as well.
