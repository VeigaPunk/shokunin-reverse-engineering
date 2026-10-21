# Source058 — S058 row + lesson Gate review (R23-C1, wave 2)

Seat: KaidokuR23.Source058. Candidate `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Every corpus and evidence fact below was read from candidate bytes via `git show <candidate>:PATH` (observed), or is marked otherwise. Source-review only; no live tool run; no target, device, or process contact.

Process note: an early draft cited `corpus/SOURCES.md` from the moving worktree. That draft was superseded. The row text, line numbers, and hashes below come from candidate bytes.

## Verdict

The quote, its location, and the version pin hold at the candidate. Two cell-level overstatements and one linkage gap were found. One stale W1 proposal was re-evaluated and is superseded.

## Gate axes

| Axis | Result | Evidence (candidate bytes) |
|---|---|---|
| Versioned | PASS | Tag `sigrok-cli-0.7.2` in URL; `corpus/SOURCES.md:64`; `corpus/lessons/round-23.md:16` |
| Located | PASS | `Load input from a file instead of a hardware device.` appears exactly once (`grep -c` = 1) in `.ufo/waves/round-23/evidence/sources/sigrok-cli.1:111`, under `-i, --input-file` (`:110`). |
| Pin integrity | PASS | `git show … sigrok-cli.1 \| sha256sum` = `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9`, matching the row anchor and `evidence/sources/fetches.json` (status 200, size 19180). |
| ≤25 words | PASS | 10 words (`wc -w`). |
| File-input meaning only | PASS for the quote; FAIL for row scope (F1) | Quote is file-input meaning. Row scope is wider; see F1. |
| No REA-result attribution to manual | PASS | Lesson `round-23.md:16` and row `SOURCES.md:64` both disclaim REA output semantics. Body grep of the knowledge entry: "manual" appears only at its line 1; S058 is never named in the body (F3). |
| Used-by paths exist | PASS | `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` and `corpus/lessons/round-23.md` both exist at candidate. |

Lesson preamble quote rule: `round-23.md:10-11`.

## Findings

**F1 — MEDIUM — row scope exceeds the gate.**
`corpus/SOURCES.md:64` scope: "File-input and protocol-decoder option meanings for sigrok-cli0.7.2". The lesson gate row (`round-23.md:16`) admits "option meaning only" for one located quote, the input-file sentence. No located quote in the gate supports any protocol-decoder meaning. The manual does contain decoder-option text (`sigrok-cli.1:297-298`, "The list of supported options depends entirely on the protocol decoder."). So this is an unlocated scope claim, not a contradicted one.
Suggested fix: narrow the scope cell to file-input option meaning, or add a located quote for each admitted meaning.

**F2 — LOW — samplerate clause overgeneralizes.**
`SOURCES.md:64` teaches: "decimal samplerate and decoder selections are explicit in the exercised calls."
- `.ufo/waves/round-23/evidence/c1/decode-uart-hi.run.json` argv contains `binary:numchannels=1:samplerate=960000` (observed).
- `.ufo/waves/round-23/evidence/c1/decode-official-uart.run.json` argv is `['npx','-y','rea-agents@6.5.0','decode-signal-recording', '…/hello_world_8n1_9600.sr', '--decoders','uart:rx=TX:baudrate=9600', '--annotations','uart=rx-data', '--all_lines','--format','json','--full-output']`. A programmatic check found no `samplerate` token (observed).
The samplerate clause holds for one of the two decode calls. The decoder-selection clause holds for both.
Suggested fix: "in the synthetic binary-input call". The manual's own input-format example is `samplerate=1mhz` (`sigrok-cli.1:145`), so "decimal" is a fact about the REA calls, not about the manual.

**F3 — LOW–MEDIUM — S058 linkage is header-only.**
Line 1 of the knowledge entry `source:` names S058. A body grep for `S058` returns zero matches. The body names S059 once. The entry never invokes the admitted input-file meaning. The used-by cell is therefore satisfied only by the header.
This matches the falsifier "new source relevance … unsupported" in `claims.json` (R23-C1). It is also the concrete instance of `w1/CriticSource.md:17`: the counter does not check relevance mechanically.
Sibling entries name their consumed sources in the body. For example, `2026-10-20-r20-wasm-interfaces.md` names S040, S041, S042, and S048 in its body.
Suggested fix: either add a body sentence that ties the file-load (`--input_format` in the uart-hi call, knowledge line 46) to the quoted input-file sentence, or remove S058 from the entry's `source:` and the row's used-by.

**F4 — informational, no defect.** The quote, the row `teaches` cell, and the lesson decision agree with one another. No REA result field (ev IDs, `returned`, `has_more`, exit codes, annotations) is attributed to the manual anywhere in candidate text.

## Stale W1 proposals, re-evaluated at candidate

- `w1/ReviewSourceQuality.md` LOW, "used-by lesson path absent": **resolved.** `corpus/lessons/round-23.md` exists at candidate and holds the S058 gate row at line 16.
- `w1/CoverageMap.md` S0xx proposal: **superseded; do not reuse.** The proposal rows are at `CoverageMap.md:246` (S058 = "Round-23 C1 offline sigrok evidence family"), `:252` (S060 = Dart AOT family), and `:259` (S059 = sigrok-cli 0.7.2 AppImage, kind tool, tier A). The candidate registry instead has S058 = manual, S059 = dumps README, S060 = REA envelopes, and S061 = Dart legacy envelope (`round-23.md:19`). Citation drift: `ReviewSourceQuality` cites `CoverageMap.md:213-220` for these proposals, but 213–222 is prose; the rows are at 246–259. Sibling report not edited.
- `w1/CriticSource.md:17` (any qualifying S058+ row unlocks every verb cited in the entry; relevance unchecked): **still applies.** F3 is the concrete instance.
- `w1/UartSemantics.md:158` and `:267` (tag peels to commit `b584f959…`; tarball `doc/sigrok-cli.1` `cmp` IDENTICAL, sha `e3f06dfe…`): **W1-reported, not re-observed by this seat.** Used only as residual-risk context (R1).

## Produced files and hashes

- `.ufo/waves/round-23/w2/Source058.md`: this report. It overwrote this seat's earlier draft at the same path. No other files were written. Hash is reported in the final message.

## Installs

None. No pacman, uv, npm, cargo, or host change. The seat ran only `git show`, `grep`, `sed`, `sha256sum`, `wc`, `ls`, and a read-only `python3 -c` JSON parse of two `.run.json` argv fields.

## Open risks

- **R1 (low):** the row pins a git tag, which is mutable in principle. The retained-bytes sha256 and `fetches.json` make the cited bytes self-verifying. The W1-reported tag peel and tarball `cmp` further reduce exposure. A commit-pinned URL would remove the remaining exposure.
- **R2:** the `teaches` cell mixes manual-derived and call-derived clauses in one sentence. F2 is the concrete instance.
- **R3:** the registry locator names the option and a unique phrase, not a line number. That is adequate for a 599-line manpage with a unique phrase, and weaker than the JSON-pointer locators used for S060 and S061.
- **R4 (not reviewed here):** the gate's count logic (`count-c1.py`, `opened == "2026-10-21"`) and the S059 and S061 rows are outside this seat's assigned scope.
