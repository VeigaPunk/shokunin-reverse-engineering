# ReviewerC2 — scoped findings (R89-C2 attack)

Full evidence: `.ufo/waves/round-89/w1/ReviewerC2/report.md` (receipts in
`.ufo/waves/round-89/w1/ReviewerC2/receipts/`, 10 JSON files).

1. **Re-derivation.** Base `0ec2bb40`: `blocks 28 resolved 28 expect 29 unresolved 0 met=False
   exit=1` (red, reproduces `pre/c2-depth-at-base.json` field-for-field). Worktree: `blocks 29
   resolved 29 expect 29 unresolved 0 met=True exit=0`. Extra: green also at `--rev HEAD`
   (`8bbb40cc0`); wrong target (`--expect-blocks 28`) red exit 1; selftest 10/10 exit 0. Tool
   sha256 equals the frozen pin `359f15e1…`.
2. **Red worlds.** Refused (exit 1): citation-only stub (`shape:words:4<25`, `shape:spans:1<2`);
   25-word one-span block (`shape:spans:1<2`); range past EOF (`range:…:3-9 of 3`); doc created
   this round under `--rev` (`absent:… does not exist in 'HEAD'`). **Pass (exit 0):** duplicated
   block; valid block inside a fenced code example; this-round doc under `--worktree` (by design —
   the predicate's `--rev` is the guard, and item 4 shows no this-round doc is involved).
3. **Floor sweep.** Blocks 1–28 at base: 39–2,902 words, 2–354 spans, `below_floor: []` — no real
   block under `MIN_WORDS 25`/`MIN_SPANS 2`; nearest is block 7 (39 words / 2 spans), fail-closed
   if trimmed.
4. **Separability.** Block 29 cites exactly the three base-present docs (r88-binfo-chain-geometry
   99 ln, r87-upx-magic-tamper-repair 125 ln, r86-record-agreement 27 ln at `0ec2bb40`); C1's
   new-this-round entry is not cited. **Verdict: separable.** Block 29 text unchanged since its
   landing commit (craft section sha256 `7e848f9e…53de` identical at `8bbb40cc0`, HEAD, worktree).

Verdict: **no kill-rule violation found; C2 predicate green on every arm I ran.** MED findings for
the L1: (1) declared evidence `.ufo/waves/round-89/w1/ExecMatrix/matrix.json` does not exist yet,
so block 29's "two pinned carriers" sentence is unverifiable today (check it against C1's
four-carrier population when it lands); (2) the counter cannot see a duplicated block that
replaces an existing one at frozen count — pin the craft-section hash at integration. LOW: fence
blindness and `--worktree` trust are latent, no live instance.
