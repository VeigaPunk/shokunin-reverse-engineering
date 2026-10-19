# Proposed SKILL.md change — queue-drain rule #14 (PATCH TEXT, NOT APPLIED)

Seat PL-1 (planner, chain c1), wave `arc3-loop1-round2`, 2026-10-19. Target:
`SKILL.md`, section `## Queue-drain craft (rounds 5-12, distilled in round 13)`.
**Nothing here was applied by this seat** (seats are barred from `SKILL.md` this
round); the bytes below were rehearsed on a scratch clone and measured.

## Anchor (verify before applying)

Insert **after** the last line of rule #13, `SKILL.md:239`:

```
  kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).
```

i.e. immediately before the craft section's trailing blank run and
`## Config custody for live-probe rounds (SOP)` (`:242`). No blank line between
rule #13 and rule #14 (matches the rule-12→13 boundary); one blank line after
rule #14's last line.

## Patch (unified diff; base blob `dfcfe65`, result blob `6410e05`)

```diff
@@ -237,6 +237,30 @@ bullet is bounded by the lines it cites.
   (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-19`); the matched natural
   control omitted the disables under the same caps/deadline and was
   kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).
+- **An artifact that records its own byte-identity must re-derive that identity
+  after every revision — a stale self-identity voids the verification block,
+  not the work; the integrator records the fresh identity at landing.**
+  Measured, arc3-round-1: one knowledge-entry patch text carried three different
+  self-identities inside ~20 minutes — its "Verification performed" step 4
+  claimed 8,316 B / sha256 `f95c5a05…` while the patch as written applied to
+  8,598 B / `d8d85949…`; an intermediate revision applied to 9,513 B /
+  32 lines / `a5119120…`, and the landed bytes are 10,225 B / 33 lines /
+  `dd986f56…` (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:5-7`;
+  diagnosis and receipts, round-1 wave tree:
+  `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/proposed-fixes.patch.md` §F2 +
+  `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; the
+  same tree's `claims/c1/verdict.md` §E7/D9 re-applied both revisions
+  independently). None of the three was a lie when written — that is the
+  failure mode: a self-identity expires silently on the next edit. Re-derive
+  size, line count, and sha256 from the bytes you are handing over, never from
+  an earlier revision, and re-derive again after the last byte changes; the
+  cost is one `wc -c -l` + `sha256sum`. On a mismatch, void the self-identity
+  claim only — the artifact's evidence and findings stand — and record the
+  fresh identity at landing (`LOG.md`'s arc3-round-1 entry; `SCORECARD.md`'s
+  `arc3-loop1-round1` section, by section key, never a bare line number — rule
+  #11 form). Deleting the claim does not discharge the rule; an artifact's
+  numbers for another file (carrier, patch output) re-derive the same way.
+
```

Full-text copies beside this file: `rule-14.diff` (git diff, byte-exact) and
`rule-14-block.txt` (the 23-line block as inserted).

## Identity of the change (measured on the rehearsal clone)

| Quantity | Value |
|---|---|
| Inserted lines | 24 (23 rule lines + 1 blank) |
| Inserted bytes | 1,738 |
| Rule block (rstrip'ed) | 1,736 bytes / 23 lines / sha256 `51a87ef6c2fe18295db31a0b34285e937ebed4aeba0d6474b9111b32e75caa0e` |
| Base `SKILL.md` | 371 lines / 27,390 B / sha256 `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` |
| Rehearsed result `SKILL.md` | 395 lines / 29,128 B / sha256 `11647e6da48ccbbfd3ac557d1860d4e267997deddb989aaafc1c941209c47b14` |
| Diff shape | `24 0 SKILL.md`; zero removed lines in `-U0`; every base byte survives (prefix/suffix proof) |
| command A | before `13/13` → after `14/14`, 82/82, 10.0/10.0 |
| Non-vacuity | citation `:5-99` → `13/14`; citation removed → `13/14` |
| Probe / census | `findings=0` (default + strict) / `PASS 0/0/0/0`, loci unchanged |

## Constraints this patch respects

- **Rule-#11 form**: no bare line number into an operator-mutable file
  (`grep -cE '(config\.toml|mcp\.json|bashrc|profile|SCORECARD\.md|LOG\.md):[0-9]+'`
  → 0); record citations are by section/entry key.
- **No version pins**: `grep -cE '[0-9]+\.[0-9]+\.[0-9]+'` → 0 (cannot trip the
  census's gated-token classes).
- **Single countable citation**: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:5-7`
  (append-only target; end ≤ line count holds under growth).
- **No scope widening**: no pointer-table entry, no `expected.json` pin, no
  census scope change is required or proposed.
- **Same-commit companion**: `shonen-refresh.patch.md` (SHONEN.md:6 states the
  rule count and the craft-section range; it goes stale otherwise).
