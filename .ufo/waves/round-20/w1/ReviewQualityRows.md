# ReviewQualityRows — QUALITY #23/#24 proposal + rows 1-22 digest

Seat: KaidokuR20.ReviewQualityRows-2 (read-only; this report is my only lane write).
Clock at write: 2026-10-20T17:50:23-03:00 (observed, `date -Iseconds`, exit 0).
No installs or upgrades performed (tooling directive: none needed).

## 1. Baseline state and anchors

- [observation] `git diff --stat 14f0260ad319ecc26994381b2415d5a999003375 -- corpus/QUALITY.md` → no output, exit 0: the worktree QUALITY.md is identical to the baseline rev, so line anchors below are valid at both.
- [observation] Rows 18-22 anchors: `grep -E '^\| (18|19|20|21|22) \|' corpus/QUALITY.md` → hits at corpus/QUALITY.md:28,29,30,31,32 (exit 0). Signals table `## Signals of weak material` at corpus/QUALITY.md:34, its rows 1-6 at :36-43.

## 2. Rows 1-22 digest at 14f0260ad319ecc26994381b2415d5a999003375

Command (verbatim, as assigned; run with cwd=LANE):

```
git show 14f0260ad319ecc26994381b2415d5a999003375:corpus/QUALITY.md | grep -E '^\| *([1-9]|1[0-9]|2[0-2]) *\|' | sha256sum
```

exit=0 → `245f9a92f71a2c7c5f471f7682da6e4271df4efdd347ac9667cc515faf71ef54  -`

Calibration caveat [observation]:
- `… | grep -E '^\| *([1-9]|1[0-9]|2[0-2]) *\|' | wc -l` → `28`, exit 0 — the pattern matches **28 table rows, not 22**.
- `… | grep -oE '^\| *[0-9]+ +' | tr -d '| '` → `1 2 3 … 22` then `1 2 3 4 5 6`, exit 0: the signals table reuses numbers 1-6, so the "rows 1-22 digest" folds in signals rows 1-6 (corpus/QUALITY.md:36-43).
- [inference] A future digest mismatch may originate in either table; re-verifiers should first count matched lines (expect 28 at this rev) before hunting drift. The value above is reproducible exactly as the assigned one-liner.

## 3. Grounding

- #23 (evidence timestamps ≤ shipping commit, mechanised):
  - [observation] `corpus/lessons/round-19-verifier-spotcheck.md:182-183` — D2: future-dated evidence timestamp (`claims.json:36`, 16:20 inside a 16:09:17 commit), withdrawn, "timestamps must be at or before their shipping commit".
  - [observation] `.ufo/waves/round-20/contract.md:41-45` — the round fixes the mechanisation: `W20/tools/evidence-timestamps.py` compares every explicit-zone timestamp per tracked line at REV against the introducing commit's committer time (`git blame --porcelain REV`), finding `future_dated <path>:<line>`, `--strict` exit 1.
- #24 (no-execution contract needs a technical guard record):
  - [observation] `corpus/lessons/round-19-verifier-spotcheck.md:184-185` — D3: carrier execution by InstallRecordDraft despite the prohibition; "there is still no enforcement that prevents or detects carrier execution".
  - [observation] `corpus/lessons/round-19.md:90` — Mistake 5: "wave contract, not technically enforced"; "**No demonstrated enforcement fix.** … SHA-256 checks do not detect prior execution."
  - [observation] `.ufo/waves/round-20/contract.md:46-49` — guard interface fixed this round: `carrier-guard.py {arm,check,disarm}` records sha256/size/mode/ctime_ns, clears exec bits, detects `mode_restored`/`ctime_changed`/`content_changed`, declares loader-mapped execution and root out of scope; armed state `W20/evidence/carrier-guard/manual-arm.json` (contract.md:89).

## 4. Duplicate check (rows 1-22 at corpus/QUALITY.md:11-32; signals 1-6 at :36-43)

- #23 [observation over the row texts]: no existing row constrains evidence-timestamp ordering vs the shipping commit. Nearest: #18 (:28) retains argv/rev/stdout/exit — no timestamp rule; #19 (:29) admits instants only with retained pin maps — compares instants to each other, never to commit time; #21 (:31) retained-keys; #22 (:32) seat cutoffs. **Not a duplicate.**
- #24 [observation]: no existing row governs prohibition-enforcement claims. #9 (:19) and #10 (:20) gate *positive* runtime/capability claims; the inverse — a declared prohibition presented as enforced/prevented/detected — is unaddressed. **Not a duplicate.**

## 5. Proposed rows (author-side advisory; L1 owns admission and final wording)

To be appended after corpus/QUALITY.md:32:

```
| 23 | An evidence timestamp in a retained record is admitted only when it is at or before the committer time of the commit that introduced the line carrying it, and the comparison is mechanised: every timestamp with an explicit zone in every tracked file at the measured revision is checked against the introducing commit's committer time (`git blame --porcelain REV`; finding `future_dated <path>:<line>`, `--strict` exit 1). A future-dated timestamp is fixed by a withdrawal or an append naming `file:line`, never by rewriting filed bytes; a green result covers only explicit-zone timestamps the check parses — zone-less or date-only instants are outside its scope and are checked manually or marked so. | `corpus/lessons/round-19-verifier-spotcheck.md:182-183` (D2: `claims.json:36` carried 16:20 inside a 16:09:17 commit — withdrawn; "timestamps must be at or before their shipping commit"); mechanised interface `.ufo/waves/round-20/contract.md:41-45` | — |
| 24 | A statement that a prohibition is in force ("carriers are never executed", "writes are refused", "no network access") is admitted as declared-process only; calling it enforced, prevented, or detected requires a technical guard record: the named guard tool, its retained arm/check (or red-case) records at named instants, and its declared limits. The guard's green is described only by what it verifies (e.g. exec bits cleared at arm, modes still exec-free, ctime and content unchanged; loader-mapped execution and root declared out of scope). A content hash does not detect prior execution, and a contract clause alone is not a guard. | `corpus/lessons/round-19-verifier-spotcheck.md:184-185` (D3: InstallRecordDraft executed a carrier despite the prohibition — "no enforcement that prevents or detects carrier execution"); `corpus/lessons/round-19.md:90` (Mistake 5: "wave contract, not technically enforced"; "SHA-256 checks do not detect prior execution"); guard interface `.ufo/waves/round-20/contract.md:46-49`, armed record `:89` | — |
```

[inference] Supersedes is "—" for both: #23 complements #18/#19 without narrowing them (timestamp-vs-commit is a distinct field from retention/instants), #24 complements #9/#10 (opposite polarity of claim). Neither rewrites an existing row.

## 6. Residual risk and verification gaps

- Digest ambiguity: the assigned pattern spans admission rows 1-22 **and** signals rows 1-6 (§2); L1 may want a disambiguated canonical digest command before pinning it in claims.
- The mechanisation claims rest on the contract's fixed interfaces (contract.md:41-45, :46-49); the tools' actual red/green runs are executor-seat deliverables — not exercised by this read-only seat, not verified here.
- Proposed wording is advisory; final row text and admission are L1's.
- Lane safety: no Go carrier executed, no REA analyze/search/decompile run, no git writes in LANE, no writes outside this report.
