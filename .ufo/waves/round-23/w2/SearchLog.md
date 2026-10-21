# SearchLog: round-23 SOURCES search-note review (corrected)

Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Scope: the round-23 search note (`corpus/SOURCES.md:111`), its registry rows S058–S061, and the retained evidence they cite. All reads were `git show` / `git grep` / `git diff` against the candidate revision, plus `sha256sum` and JSON/zip reads of committed bytes. No REA run, no target execution, no `count-c1.py` run.

Labels: **observed** = read from committed bytes; **inferred** = my reasoning from them; **unknown** = not checkable here.

## Verified (observed)

1. **Count arithmetic.** The note (`corpus/SOURCES.md:111`) says identified5 / screened5 / included4 / excluded1. The five families are the sigrok-cli manual, the sigrok-dumps README, the upstream REA signal guide, the L1 signal envelopes, and the L1 legacy Dart envelope. Four are included as S058–S061. The excluded item is the REA guide. The counts reconcile one-to-one.
2. **Registry rows are pure additions.** `git diff --stat aa1450b… 2838351…` reports `corpus/SOURCES.md | 6 ++++++`, with zero removed lines (`git diff … | grep -c '^-[^-]'` = 0). Existing S001–S057 are unchanged.
3. **Census covers the final registry.** `verify/initial/source-census.json` has `source_rev 6615aea…`, `exit 0`, `passed: true`. `git diff --stat 6615aea 2838351 -- corpus/SOURCES.md` is empty, so the census ran against the same SOURCES.md bytes as the candidate. `source-prefixes.json` reports `old_rows 57`, `new_rows 61`, `old_rows_unchanged: true`, `passed: true`.
4. **Retained source digests match their rows and receipts.**
   - `evidence/sources/sigrok-cli.1` sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9`, matching S058 and `fetches.json`.
   - `evidence/sources/uart-README.txt` sha256 `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66`, matching S059 and `fetches.json`.
   - `evidence/c1/hello_world_8n1_9600.sr` sha256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`, matching `official-download.json` (status 200, size 58381).
   - `evidence/c1/uart-hi.bin` sha256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`, matching the knowledge file.
   - Saber APK (not in repo) `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`, size 41263437, matching S061 and `legacy-saber-download.json`. The receipt says `signature_verification: not performed; digest identity only`.
5. **Located quotes, checked in raw bytes (not parsed JSON).**
   - S058: "Load input from a file instead of a hardware device." at `sigrok-cli.1:111`.
   - S059: "This is a collection of example UART communication (only in one direction)." at `uart-README.txt:5`.
   - S060: literal `"returned":110,"has_more":false`, raw count 1 in `inventory.envelope.json`.
   - S061: literal `"snapshot_hash_sources":2`, raw count 1 in `inspect-dart-legacy-saber.envelope.json`.
6. **Other S-row facts checked.**
   - S059 README: 625 kHz for 9600 baud (line 23), Olimex STM32-H103 origin (line 9), TX probe (line 27).
   - S060 decode: `decode-uart-hi` annotations `300-1100 uart-1: 48` and `1300-2100 uart-1: 69`. `decode-official-uart` has `total_lines 12885`, `has_more false`, and first `48` ('H') at 5512.
   - S061: `abi x86_64`; `libapp.coverage complete`; `string_pool.coverage partial`.
   - S058 "decimal samplerate … explicit": `decode-uart-hi.run.json` argv contains `samplerate=960000`, 4 hits.
   - Version pin: every c1 `*.run.json` wrapper contains `rea-agents@6.5.0` (for example `inventory.run.json:5`, `decode-invalid-decoder.run.json:5`).
   - Refusal side: `decode-invalid-decoder.envelope.json` has `error.code "execution_failure"`, `retryable false`, `exit_code 1`.
7. **Knowledge claim re Python 3.5.2 verified.** `inventory.envelope.json` shows `Python 3.5.2 / 0x30502f0` and a `pd.py` line 138 traceback containing `0b0000_0010_1001_0001`. An underscore-separated binary literal is the cause, as the knowledge file says. My first grep missed the literal and is corrected here.
8. **Used-by paths all resolve** at the candidate: `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`, `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md`, `corpus/lessons/round-23.md`.

## Findings

**F1 — medium (grounding). The excluded guide's contrary claim is not retained.** *Observed.*
- The excluded REA guide has no retained copy and no fetch receipt. `evidence/sources/fetches.json` has 2 entries, both sigrok (S058, S059). `git grep signal-recordings <rev>` has one hit, a 2026-10-15 interactive-session transcript, which is not a receipt. I did not read that transcript further.
- The installed REA skill links the guide by unpinned main-branch URL (`~/.agents/skills/reverse-engineer-anything/SKILL.md:148`). That link is outside the repo.
- Its contrary text exists only as prose. `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:87–88` says its `invalid_request` description "is not substituted for this 6.5.0 observation." `corpus/lessons/round-23.md:24–26` says the description "conflicts with" the 6.5.0 `execution_failure`. The two files characterize it differently.
- The retained side confirms only the 6.5.0 refusal (`decode-invalid-decoder.envelope.json`).
- The exclusion conclusion still holds: an unversioned main-branch document cannot pin 6.5.0 behavior. What cannot be replayed is the word "conflicts" and the "opened" basis.

**F2 — low (sourcing). The knowledge body attributes an unsourced requirement to the UART help record.** *Observed.*
- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` says the help envelope "retains the selected installed module's literal help. RX is optional because TX is another supported direction; at least one actual direction is still required."
- The cited `evidence/c1/uart-help.envelope.json` says `Required channels:` followed by `None.` (help text lines 45–46), then lists `rx` and `tx` under `Optional channels:` (lines 47–49).
- No "at least one" or "must/either" wording appears in that envelope. No retained run exercises the zero-channel case.
- The held witnesses use `rx=0` and `rx=TX`, so the held-witness claims do not depend on this sentence.

**F3 — low (linkage, corrected from my draft). S060's path list omits the help record.** *Observed.*
- S060 enumerates three paths: `inventory.envelope.json`, `decode-uart-hi.envelope.json`, `decode-official-uart.envelope.json`.
- The knowledge body also relies on `uart-help.envelope.json`, which S060 does not list.
- Correction: my draft said the knowledge header cites S060's source for uart-help. It does not. The header points at the directory `evidence/c1/`, which covers the help file only by containment.

**F4 — low (text integrity). Missing word-spaces in round 21–23 prose, including version pins.** *Observed.*
- Round-23 additions: `corpus/SOURCES.md:64` `sigrok-cli0.7.2`; `:64–67` `opened2026-10-21` (four times); `:65` `and625kHz at9600baud`; `:66` `sigrok0.7.2` and `REA6.5.0`; `:67` `REA6.5.0`; `:111` `identified5`, `screened5`, `included4`, `excluded1`, `for6.5.0`.
- In the new knowledge file: `reports110 examined`, `Python3.5.2`, `at960000Hz`, `baud9600`.
- The pattern predates round 23 (baseline `SOURCES.md:101`, `:102`, `:105`: `Identified2`, `Identified3`, `screened3`, `included1`).
- Machine-read registry cells (ID, tier, status, date, recheck, used-by) and digests are intact.
- Impact: version pins read as malformed (`sigrok-cli0.7.2`), which invites misreading.

**F5 — info (third-party source internal inconsistency; row survives).** *Observed.*
- The S059 README wiring table says `0 (green) TX` (line 27). Its capture command says `-p '1=TX'` (line 35). The recording's own metadata says `probe1 = TX`.
- S059 says "TX channel", which holds by name. The REA decode selects `rx=TX` by name, so the row's claim survives.
- The row does not claim a probe index. A reader who maps TX to probe 0 from the README table would be wrong.

**F6 — none (stop rationale).** *Observed.* No S-row turns a debugger mention into a witness. S056 is alias-only and is described as "not successful debugger execution." Both debugger verbs remain Adjacent, as the note says.

**Retracted from my draft.** My earlier "identified/excluded ambiguity" finding is withdrawn: the five families map one-to-one to four included rows plus one excluded guide. My earlier claim that the excluded guide was "corroborated by the retained envelope" was too strong: the retained envelope corroborates only the 6.5.0 side.

## Produced files and hashes

- `.ufo/waves/round-23/w2/SearchLog.md` (this file). Its own hash is reported in the final message, since a file cannot embed its own hash.
- No other files were written. No peer report was edited.

## Installs or none

None. Pacman was not touched. No package, tool, or config was installed or changed.

## Process notes (disclosed deviations)

- One `git status --short` ran in the lane worktree. It may refresh the index stat cache. It did not stage, commit, or run `jj`. The lane index was not intentionally written.
- I ran `ls` and a grep for "signal" across `~/.agents/skills/reverse-engineer-anything/`. That search is broader than the item; it found the SKILL.md link (F1). Nothing outside it was read.
- Python was used only as a JSON/zip reader over committed bytes (`python3 -I -B`). It was not the counting command and no tests, builds, or linters ran.

## Open risks

- F1 cannot be replayed from the repo. The guide's live content was not re-fetched (no live tool run).
- The census validates row format and the `kaidoku` scope. It does not validate quote truth or claim scope. Quote truth was checked here, for the located quotes only.
- Not checked: whether the inherited identify-flutter-build witness appears in these rows (outside this seat's item); the S061 "another carrier" clause, which is truncated in the row.
