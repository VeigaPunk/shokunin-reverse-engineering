# ReviewerC1 — R86-C1 (calibration) findings

Seat: ReviewerC1 (reviewer, read-only). Full record: `.ufo/waves/round-86/w1/ReviewerC1/attack.md`
with 27 fixtures × {default, substring-only control} receipts under `receipts/`.

## Findings, by severity

1. **High — A3 is a lint and its target is reachable only by a shortcut.** `record-agreement.py` A3
   requires exactly one `| coverage |` line in SCORECARD.md. BASE has 23. Passing A3 therefore needs
   the 22 history rows deleted or relabelled (`04-reach-delete-…`, `04-reach-relabel-…` accepted), a
   round-85 receipt that does not exist at BASE, and no edit that is the claimed record work alone.
   A3 also never reads `ok`, never compares `rev` to `--rev`, and picks the newest named receipt by
   round number. Accepted wrongly: `03c-receipt-rev-zeros`, `03c-decoy-newest-round99-unrelated`.
2. **High — A1 can pass with a stale or non-registry row.** Only `sup[-1]` is read, so a stale
   `count 3` row above a correct one passes (`01a-stale-earlier-wrong-row-plus-correct`). A row inside a
   ``` fence passes (`01d-row-in-code-fence`); the parser has no fence or comment awareness.
3. **Medium — A2 can pass when the absent case has two statuses or a substring match.** The sentence
   splitter on `[.;:]` hides a second verdict (`02b-split-sentence-verdict`); the stem check is a
   substring (`survi` matches "survivability", `02b-stem-substring-lint`). The first `if not case_present:`
   in file order is the one read (`02b-decoy-earlier-branch`, synthetic decoy).
4. **Medium — the frozen plan misdescribes BASE A3.** The plan says row 23 "names only a round-67
   receipt". The bytes: row 23 names rounds 84, 76, 75, 68 and 67 (newest 84 < claimed 85). The counter
   fails A3 earlier, on "found 23 rows" (`03e-base-card-23-rows`). I cannot edit the frozen plan; L1 should record
   the correction.
5. **Confirmed — BASE reproduces.** `--rev 2cf0b7ff…` gives exit 1, `agreed=0/3`, `mismatches` = the three
   atoms (receipt `receipts/base-rev-2cf0b7ff.json`, instrument sha `99cb8f27…`, same as the frozen pre
   receipt). Selftest 11/11 green. The control (`--control substring-only`) accepts every fixture, BASE
   included, as the plan requires.

## Do-nothing control

A1 and A2 are reachable by one record edit each (the claimed work). A3 is not reachable by editing the
three records alone; it needs a new receipt file plus history edits, or a junk receipt that the rule accepts.

## Verification gaps

- Fixtures ran in `--worktree` mode; the `--rev` blob path was checked at BASE only.
- The decoy for A2 is synthetic (the real code has one `if not case_present` branch).
- No production file edited; no VCS mutation; no tool installed.
