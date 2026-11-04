# ReviewerC2 — independent review of R79-C2 (freshness)

Round 79, w1. Base `29d2ca30b83a6a0d85b0aa979de0138fde1660e6`, declaration
`a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d`, freeze `ed68cd0a6cc790cca342380a2d80d1927a668c8c`.
Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; no lane file was modified by this seat.

**Verdict.** The counters re-derive exactly, all five attack shapes behave as the frozen rule
requires, the receipt is digest-only, and the `path-only` control is non-vacuous. One
high-severity **record** defect: the frozen counting command omits `--battery`, so the predicate's
literal command exits 2 and writes nothing. The measured semantic content of R79-C2 survives —
with `--battery` appended, both arms reproduce every count and every check field of the frozen
receipts (only `checked_at` differs) — but the
frozen sentence is not re-runnable as written until that flag is added and the instrument re-pinned.

## 1. Re-derivation of the counters

`checks_total`, `matched`, `mismatches`, `unparsed` recomputed from the landing check list by two
independent readers: (i) hand arithmetic over `checks[]` plus `--validate`, (ii) a separately
written parser that re-extracts the five cells from `git show <rev>:PROVINCE.md` with different
regexes (document-order pin/pointer pairs, first Ghidra pointer, first Ghidra value, first
`.bashrc` pointer), reads the live files and tests the tokens itself.

| counter | landing receipt | re-derived (i) | re-derived (ii) | base receipt (`29d2ca30`) | fresh base run |
|---|---|---|---|---|---|
| `checks_total` | 5 | 5 | 5 | 5 | 5 |
| `matched` | 5 | 5 | 5 | 3 | 3 |
| `mismatches` | 0 | 0 | 0 | 2 | 2 |
| `unparsed` | 0 | 0 | 0 | 0 | 0 |
| `ok` | true | true | true | false | false |
| exit | 0 | 0 | — | 1 | 1 |
| `mismatch_ids` | — | — | — | `omp-pin`, `kimi-pin` | `omp-pin`, `kimi-pin` |

- `--validate .ufo/waves/round-79/l1/scores/c2-at-landing.json` → `{"defects": [], "checks": 5,
  "matched": 5}`, exit 0.
- Fresh run at the freeze (`--battery`) is identical to the landing receipt in every counter and
  in all ten fields of all five checks, including every `line_sha256`.
- Fresh run at base reproduces `omp-pin`/`kimi-pin` as the only mismatches; the recorded values
  are `:8` and `:4126` while the live pins are at `:12` and `:4722`, exactly as the claim states.
- `record.sha256` = `99d29a00ecabf492afee5ec1e393455761bf2947bac6ec1e25e14951b8752ca0` equals
  `sha256(git show ed68cd0:PROVINCE.md)`.
- Instrument pin `91d23dad…e80a90` equals the claims.json pin in the worktree, at the declaration
  and at the freeze.
- Independent reader outputs agree with both receipts on ids, line ranges and all five digests.

## 2. Fixture attacks (synthetic, in scratch; instrument imported read-only)

| # | shape | frozen rule requires | observed | ok |
|---|---|---|---|---|
| a | pointer at line 0 (`f:0`); backwards range (`f:3-2`); range `0-2` | not 0-based, range must be forward | matched false, `unparsed` false, no digest, reason `line range 0-0/3-2/0-2 is not a forward 1-based range` | yes |
| b | range `1-2`, token only on line 2 | range not judged by its first line | matched true, digest over both lines, `line_start 1 / line_end 2` | yes |
| c | pointer `:9` on a 4-line file; range `3-9` | past EOF is a mismatch | matched false, reason `… runs past end of file (4 lines)`; boundary `:4` is inside and yields a token mismatch, not an EOF error | yes |
| d | token on line 2, pointer names line 1; token on line 2, pointer names `3-4` | token must occur on the pointed line/range | matched false, `token '…' is not on line 1` / `… line 3-4`, digest of the pointed lines retained | yes |
| e | record cell with no `:line`, and pointer ending in a bare colon | "a pointer without a line is unparsed" | `unparsed` true, matched false, reason `pointer carries no line number` | yes |
| — | end-to-end fixture repo with green Devin, no-line OMP, past-EOF Kimi, line-0 Ghidra, backwards `.bashrc` | fail-closed | exit 1, 5 / 1 matched / 4 mismatches / 1 unparsed, `ok false` | yes |
| f | two OMP cells, first stale, second green | (not named by the kill rule) | last declaration wins; end-to-end receipt is `ok true`, the stale first pointer never read | yes (residual F2) |
| g | live `rea-agents@6.7.05` vs token `6.7.0`; `application.version=12.1.40` vs `12.1.4` | "token occurs" | matched true (substring) | yes (residual F3) |
| h | pointer path contains a colon and digits (`a:1.json:2`) | split at the line suffix only | matched true, `line_start 2` | yes |

Observations tied to the kill rule:

- **0-based**: rejected before slicing (`start < 1`, instrument `:94`), so the Python negative-index
  trap cannot turn line 0 into the last line.
- **first-line-only range**: `pointed = lines[start-1:end]` (`:104`) and the token test scans every
  pointed line (`:106`) — the second-line case is matched, the out-of-range case is not.
- **path not read**: the battery reads exactly `pointer.rsplit(":", 1)[0]` (`:174`) and the digest
  is over that file's pointed slice; no other file is touched.
- **unparsed vs mismatched**: an unparsed cell is not matched, so the receipt's
  `mismatches = len(checks) - matched` also counts it (`:203`). At both frozen revisions
  `unparsed 0`, so this has no effect on the claim's counters; it only shapes the fail-closed
  arithmetic of a broken record.

## 3. Digest-only retention

Landing receipt, per check, exactly ten fields: `id`, `line_start`, `line_end`, `line_sha256`,
`matched`, `unparsed`, `reason`, `path`, `pointer`, `tokens`.

- Every `line_sha256` is 64 hex chars; recomputed from the live pointed lines (including the
  `.bashrc` 28-29 range joined) all **5/5 equal**.
- No pointed-line bytes: a 12-byte sliding-window scan of each pointed line (with the declared
  tokens and the path removed) finds **0** windows in the receipt. No `env` key, no `api_key` /
  `secret` / `token=` / `ghp_` / `sk-` / `Bearer` substrings.
- What is retained beyond digests: pointer paths, the declared tokens (`rea-agents@6.7.0`,
  `application.version=12.1.4`, `GHIDRA_INSTALL_DIR=`, `JAVA_HOME=`), 1-based ranges and
  `checked_at` — the package pin and key names, never an environment block or a secret value.

## 4. The `path-only` control at the freeze

Re-run with `--battery --control path-only --rev ed68cd0…`: exit 0, `checks_total 5`,
`matched 5`, `mismatches 0`, `unparsed 0`. Every check carries `line_start: null`,
`line_end: null`, `line_sha256: ""`. Base is the same 0, while the line-bound arm at base is 2.

It must report 0, and that does not make the claim vacuous:

1. The control is defined as the round-78 rule — the path exists, the line is never read — so its
   0 is structural, not evidential. Its value is the base contrast: on the *same stale record*
   where the line-bound arm returns 2, the control returns 0. That is an executed demonstration
   that path-only scoring is blind to exactly the drift R79-C2 targets.
2. The control cannot substitute for the claim's receipt. Its checks have null ranges and empty
   digests, and `--validate` on it exits 1 with 10 defects (`matched without a pointed-line digest`,
   `matched without a 1-based line range`) — the kill rule "the `path-only` control used as the
   claim's counter" is mechanically enforced, not just prose.
3. The claim's counter is the line-bound arm: five matched checks with 1-based ranges whose digests
   recompute from the live bytes (5/5), and a base arm with two named mismatches at the recorded
   stale lines. The control contributes only the negative contrast.

## 5. Findings

**F1 — high — the frozen counting command omits `--battery`.** `plans/round-79-claims.md:86`,
`claims.json` (`counting_command` and `predicate`) and the instrument's `PREDICATE` constant all
read `python3 -I -B tools/round-79/pointer-bind.py --root . --rev <measured> --json-out <receipt>`.
The instrument requires the mode flag (`:319`): that exact command exits **2**, prints
`usage: --battery --rev <rev> [--json-out <path>] [--control path-only]`, and writes **no**
receipt — so the predicate's literal command cannot exit 0 at the freeze or 1 at base. Adding
`--battery` reproduces both frozen receipts exactly (counts and all check fields; only
`checked_at` differs). The freeze audit (`freeze-audit-at-freeze.json`: `clean 29`,
`required_clean ["round-79"]`, `required_failed []`) recorded round-79 clean, so it did not catch
this — executing the frozen command would have exited 2.
Repair: add the flag in the plan, claims.json and the instrument's `PREDICATE` (which is copied
into every receipt), then re-pin the instrument hash and re-freeze. This does not falsify the
measured counter; it blocks verbatim re-derivation as frozen.

**F2 — low — duplicate declaration collapse.** Pin cells are collected into a dict, so the last
declaration wins (`:127`); the Ghidra pointer/value and `.bashrc` pointer take the first match
(`:138`, `:147`). A stale duplicate is dropped before it is compared: the end-to-end fixture with a
stale first OMP cell and a green second cell yields `ok true`, `checks_total 5`, `unparsed 0`.
The frozen record is single-celled for each scoped family (3 pin pairs, 1 Ghidra pointer), so its
counts stand; the probe also shows 2 `application.version=` values and 6 `.bashrc` pointers in the
record, only the first of each being used. A per-family uniqueness assertion would close this.

**F3 — info — substring token semantics.** `token in line` (`:106`) accepts a longer value that
contains the token: `rea-agents@6.7.05` satisfies `rea-agents@6.7.0`, and
`application.version=12.1.40` satisfies `application.version=12.1.4`. The claim's wording ("each
declared token to occur there") is met; exact token-boundary matching would strengthen a future
claim.

**F4 — info — dead parameter and decoded digest.** `bind()` takes `line_count` but never uses it
(every call passes 0; EOF is `len(lines)`, `:100`); lines arrive from text-mode `readlines()` with
`errors="replace"` (`:117`), so the digest is over decoded, newline-normalised text rather than
raw bytes. No effect on these five LF/UTF-8 files (5/5 digests recompute equal); a CRLF or
non-UTF-8 config would hash a normalised line.

## 6. Residual risk and verification gaps

- The instrument's input is the live filesystem. `checked_at` is present, but the receipt cannot be
  cryptographically tied to those bytes; my later re-run reproduces every digest, so no drift
  occurred in the interval, but a future reader can only re-check against the then-live files.
- `--validate` proves internal re-derivation only. Its own selftest accepts a forged receipt with
  arbitrary digests (`green-forged-consistent` expects no defects), so a clean validate is not
  evidence of truth; the live recomputation performed here (5/5) is.
- Cannot prove the landing run used `--battery`; only that adding it reproduces the receipt exactly.
- The freeze-gate audit was not re-run by this seat (out of scope for the C2 arm).

## 7. Evidence

- `.ufo/waves/round-79/w1/ReviewerC2/receipt.json` — acceptance receipt: `counts`, `fixtures`
  (17 cases, all ok), `digest_only`, `path_only_control`, findings, residual risks, gaps.
- `.ufo/waves/round-79/w1/ReviewerC2/{base,freeze,base-pathonly,freeze-pathonly}.json` — fresh
  receipts from this seat's re-run.
- Tooling: nothing installed or upgraded; all runs `python3 -I -B` against the lane instrument,
  read-only git (`show`, `rev-parse`, `status`, `log`). Scratch under
  `/fast/scratch/hyaku/kaidoku-r79/ReviewerC2/`, removed before yield.
