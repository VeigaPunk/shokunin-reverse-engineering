# SentinelScope — round-67 w1 audit receipt (scope, secrets, provenance)

Read-only audit of the committed bytes `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92` → `3663e6b21dccf4c4957f459301156664d8b151d6`
(operative freeze). No lane file was written outside this directory; no git/jj mutation was run; scratch was
`/fast/scratch/hyaku/kaidoku-r67/SentinelScope` (created, used as `TMPDIR`, deleted before yield).

Audit time: 2026-11-03 21:53–21:58 local. Lane HEAD at audit start and end: `3663e6b2…` (the worktree already carried the
L1's untracked data-run output — see F8).

## 1. Write scope — CLEAN

`git diff --name-status a7a4ce6 3663e6b` = 13 entries: 11 `A`, 2 `M`, 0 `D`, 0 `R`. Every path is lane-relative, has no
leading `/` and no `..` component, and matches the declared write scope (`tools/round-67`, `.ufo/waves/round-67`, `plans`,
`LOG.md`, `corpus/claim-freezes-v2.tsv`):

| st | path |
|---|---|
| A | `tools/round-67/avm-le-counter.py` |
| A | `tools/round-67/gap-rule-v2.json` |
| A | `tools/round-67/mutation-battery.py` |
| A | `tools/round-67/c1-run.sh` |
| A | `plans/round-67-claims.md` |
| A | `.ufo/waves/round-67/claims.json` |
| A | `.ufo/waves/round-67/l1/pre/control-dryrun.json` |
| A | `.ufo/waves/round-67/l1/pre/control-dryrun-c2.json` |
| A | `.ufo/waves/round-67/l1/pre/score-dryrun-at-base.json` |
| A | `.ufo/waves/round-67/l1/pre/selftest-r50.txt` |
| A | `.ufo/waves/round-67/l1/pre/selftest-c2.json` |
| M | `LOG.md` (+10, append-only at EOF) |
| M | `corpus/claim-freezes-v2.tsv` (+2 rows: `round-64`, `round-66`) |

Totals: **+2129 / −0 lines**; `numstat` reports no binary (`-`) entry. Largest added blob 46 026 B (`c1-run.sh`); no
blob is large enough to be a firmware carrier (the four carriers are 20–30 MB class).

`git ls-tree` file count: base 49 295 → freeze 49 306 (+11 = exactly the 11 `A` paths). Worktree `git ls-files` = 49 306.

## 2. Vendor bytes — CLEAN at the freeze

- `git ls-tree -r 3663e6b | grep '^corpus/evidence/round-67/'` → **none**.
- Committed `corpus/evidence/` blob count: base 3645 → freeze 3645 (unchanged; no evidence blob added).
- `tools/round-50/carriers.json` is **not** in the range (unmodified). It carries per-carrier `url` (public
  `download.avm.de` firmware URLs) plus `sha256`/`image_sha256`/`member_sha256` pins — hashes and public vendor URLs only,
  no bytes.
- `git check-ignore corpus/evidence/round-67/x.bin` → not ignored (so accidental bytes would show as untracked, not hide).

Caveat: the worktree — not the commit — now holds uncommitted data-run receipts (F8).

## 3. Secrets and private material — CLEAN

Scan of all 2129 added lines for `BEGIN .*PRIVATE KEY|token|cookie|password|secret|op://|api[_-]?key|bearer |ssh-rsa|AKIA`
(case-insensitive): **0 matches**.

Absolute-path scan of added lines: 9 lines name `/fast/scratch/hyaku/kaidoku-r67/` (the documented scratch base: `PROV_BASE`
in the counter, `SCRATCH_PREFIX`/usage text in the harness) and 1 line names `/home/vgpnk/Projects/shokunin` in plan prose
(a repo path, not a secret). Zero added lines contain a host `/tmp/…` path (`grep -E '(/tmp/[A-Za-z0-9]|=/tmp|"/tmp)'` →
empty). The apparent `/tmp/` hit in the r50 selftest receipt is the carrier-internal path `./var/remote/var/tmp/x86/kernel.image`
(firmware content, not a host path).

## 4. Instrument integrity — CLEAN except the noted rule-delta

### 4.1 Pins (claims.json `instruments` map vs actual bytes) — 7/7 match

| instrument | claims.json | actual |
|---|---|---|
| `tools/round-67/avm-le-counter.py` | `f78ed365…5e0320` | `f78ed365…5e0320` |
| `tools/round-67/mutation-battery.py` | `cabc0a0b…4851ab` | `cabc0a0b…4851ab` |
| `tools/round-67/gap-rule-v2.json` | `e66ba022…a4169e` | `e66ba022…a4169e` |
| `tools/round-67/c1-run.sh` | `00be5a87…a70ca` | `00be5a87…a70ca` |
| `tools/round-50/c1-counter.py` | `9820811b…bd813` | `9820811b…bd813` |
| `tools/round-66/closure-boundary.py` | `3c5cfb03…1045b` | `3c5cfb03…1045b` |
| `tools/round-66/coverage-selfcheck.py` | `1be9d046…555aa` | `1be9d046…555aa` |

`ENGINE_PIN` / `CLOSURE_PIN` / `COVERAGE_PIN` constants inside the instruments equal the same digests.

### 4.2 Parse / structure — CLEAN

- `python3 -m py_compile tools/round-67/avm-le-counter.py tools/round-67/mutation-battery.py` → OK.
- `bash -n tools/round-67/c1-run.sh` → OK.
- `json.load(tools/round-67/gap-rule-v2.json)` → OK (7 top-level keys: `allowed, class_disposition, removed, required,
  round, structural, supersedes`).
- Escaped pipe: the file contains **0 backslashes** and no `\|` — nothing to mis-parse. The engine's own parser is clean on
  all three models: `rule_problems.round67 = []`, `.round50 = []`, `.junk = []` in the reproduction (and in the committed
  receipt).

### 4.3 Predicate identity

- `claims.json` R67-C1 predicate **==** `avm-le-counter.py` `PREDICATE` (byte-identical). R67-C2 **==** `mutation-battery.py`.
- `plans/round-67-claims.md` holds the same **words** but as a `>` blockquote with hard wrapping (lines 42–45, 93–96); after
  stripping `^> ?` and reflowing whitespace both predicates match exactly. Literal byte-identity is therefore false — F5.

### 4.4 Gap-rule delta (the frozen rule vs the round-50 rule)

`diff -u tools/round-50/gap-rule.json tools/round-67/gap-rule-v2.json` shows exactly four changes:

1. `"claim": "R50-C1"` → `"round": "round-67"` + `"supersedes"`;
2. added `class_disposition` (char-device / block-device, with the not-publishable reason);
3. `required.char-device`: `true` → `false`;
4. **`removed.silent` (the `{"char-device": ["247:0"]}` allowance) deleted.**

`allowed` and `structural` are byte-unchanged. `removed.diagnostic/kinds/disposition` are unchanged; `removed.silent` is not.
The engine consumes `removed.silent` (`c1-counter.py:1550–1568`, `silent_detail_matches`), and the delta is *observable*:
`control-dryrun.json` reports `1 silent` under the round-50 rule and `0 silent` under the round-67 rule for `c6490` and
`c6430`. This contradicts A5 and the counter docstring — F1.

Counter's own patches are disclosed in the receipt (`patches.clauses` / `dropped_clauses`): the clause set drops
`carrier_fresh_ok`. That is a deliberate, disclosed narrowing (same pinned carriers; freshness cannot hold) and is not
counted as a defect — recorded here so the L1 sees it was examined.

## 5. Claim substance — re-derived where local evidence allows

### 5.1 Controls reproduce exactly (independent re-run, scratch output)

- `avm-le-counter.py --control --root <lane> --rev a7a4ce6` → exit 0; identical on 9/9 compared fields (`gaps_ok_round50 2`,
  `gaps_ok_round67 4`, `control_ok true`, `exit_code 0`, both rule digests, `rule_problems`, `per_carrier`, `red_controls`)
  against the committed `l1/pre/control-dryrun.json`.
  Red fixtures: dropped symlink gap `bin/adsl` still fails under rule v2; a junk rule waiving symlinks passes it
  (`junk_rule_would_pass true`); a char-device path published as a regular file is named (`firmware.bin_extract/dev/led`).
- `mutation-battery.py --selftest` → `SELFTEST CLEAN cases=9 failures=0` (9/9 cases, exit 0), matching `selftest-c2.json`.
- `mutation-battery.py --control` → exit 0, `killed_before 0`, `survived_before 2`, and **identical mutant sha256s**
  (`5e84208a…`, `2b98a7f7…`) and r66 selftest summaries (30 / 26 cases) as `control-dryrun-c2.json`.

No committed receipt in the range was found to be fabricated against a cheap, deterministic re-run.

### 5.2 Char-device census (docstring claim) — CLEAN

From the committed oracle tables:

- `tools/round-50/oracle/g7581.nonregular.tsv`: **13** char-device rows = `dev/led dev/pts/0..7 dev/tiatm dev/ttyp0..2` —
  exactly the counter docstring's list.
- `g7582`: 13; `c6490`: 1 (`dev/led`); `c6430`: 1 (`dev/led`).
  The `dev/led` device detail `247:0` matches the deleted `removed.silent` entry, which explains the r50 `1 silent`.

The round-50 failure note ("required entry with no disposition … `dev/pts/0..7`") lists 8 of the 13 — consistent: 5 of the
13 rows carry `unpublished-entry` gaps and 8 carry none. No contradiction with the 13-device census.

### 5.3 Ordering atoms — CLEAN (receipt cited by A0 is absent — F4)

`git merge-base --is-ancestor cf705c53 3663e6b` → 0; `… 39a91a99 3663e6b` → 0. Commit order is carry-in → instruments →
freeze, as declared.
But `claims.json` A0 cites `.ufo/waves/round-67/l1/records/r67-order.txt`; no `l1/records/` directory exists at the freeze
(`ls .ufo/waves/round-67/l1/` → `census-start.txt  pre  scores`; `git ls-tree` has no `round-67/l1/records`).

## 6. Findings (summary; detail in `../SentinelScope.md`)

| id | sev | one line |
|---|---|---|
| F1 | MEDIUM | A5 + counter docstring say `removed` unchanged; `removed.silent` was deleted (engine-consumed, 1→0 silent observable) |
| F2 | MEDIUM-LOW | `--score` accepts any `--gap-rule` and never checks its digest, though the docstring and kill_rule promise a drift refusal |
| F3 | MEDIUM-LOW | R67-C1's second conjunct (round-50 control = 2 of 4) is neither checked nor bound by `--score` |
| F4 | LOW | A0 cites `l1/records/r67-order.txt`, which does not exist at the freeze |
| F5 | LOW | "byte-identical" predicate claim is false as bytes (plan blockquotes + hard-wraps); words match |
| F6 | LOW | Three exit-2 contracts (counter crash, battery control drift, battery fixture git failure) return exit 1 |
| F7 | INFO | Freeze ledger has no `round-67` row (expected pre-freeze; must land before close) |
| F8 | INFO | L1 data-run output appeared under `corpus/evidence/round-67/c1/` mid-audit (untracked, out of range) |

## 7. Reproduction commands (all read-only over the lane)

```
git -C <lane> diff --name-status A B ; git -C <lane> diff --numstat A B ; git -C <lane> ls-tree -r A|B
git -C <lane> diff A B | grep -E '^\+' | grep -i -E 'BEGIN .*PRIVATE KEY|token|…'
python3 -m py_compile tools/round-67/{avm-le-counter,mutation-battery}.py ; bash -n tools/round-67/c1-run.sh
python3 -I -B tools/round-67/avm-le-counter.py --control --root <lane> --rev A --work $S/w --out $S/ctl.json
python3 -I -B tools/round-67/mutation-battery.py --selftest --root <lane> --work $S/b --out $S/s.json
python3 -I -B tools/round-67/mutation-battery.py --control --root <lane> --rev A --work $S/c --out $S/c.json
awk -F'\t' '$2=="char-device"' tools/round-50/oracle/<id>.nonregular.tsv
```

## 8. Limits

- `--score` was **not** run (needs the carrier cache, `--pkg65` rea-agents 6.5.0 and a full REA extraction; also the
  documentation bindings do not exist until the prose lands). The score path is audited statically and through its
  deterministic control.
- The four carrier pins were verified as hashes/paths only, not by re-fetching or re-hashing vendor bytes (no bytes in the
  lane; licence).
- The char-device census was verified against the committed round-50 oracle tables, not re-derived from the carriers.
- Nothing was installed or upgraded (no `pacman`, no `uv`, no network).
