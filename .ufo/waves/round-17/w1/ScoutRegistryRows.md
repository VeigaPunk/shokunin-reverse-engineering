# Scout — SKILL.md registry rows vs exercised argv (round 17, w1)

Scope: the seven table rows in `SKILL.md` whose 2nd cell is `probe / kaidoku`,
`gate / kaidoku` or `tool / kaidoku` (`grep -c 'kaidoku |' SKILL.md` = 7; no
other row matches). Read-only.

Method (observation): parsed all **2,468** JSON files under `.ufo`; **34**
carry an `argv`/`orig_argv` array; **235** argv records total. Matched each
row's first backticked command token-by-token, `<...>` and `[--x <y>]` as
placeholders. Also grepped non-JSON `.ufo` text for quoted invocations. No
round-17 receipt exercises any of these seven rows yet (`.ufo/waves/round-17`
contains only claims, contract, pilot outputs, wave-1 metadata and w1
`selection-*.json` outputs — none carry `argv`).

## 1. Enumeration

| # | Name | SKILL.md | Kind | Retained argv receipt that exercised the advertised command | Class |
|---|---|---|---|---|---|
| 1 | interactive-r1-recovery | :447 | gate | `.ufo/rounds/interactive-r1/gate-before.json:4` (`argv`); `gate-results.json:7,17,28`; `gate-correction-results.json:9,19,30` | **exercised_match** |
| 2 | citation-drift | :448 | probe | none as written; nearest `.ufo/waves/round-14/verification.json:106` (`citation-strict`), `round-15/verification.json:127`, `round-15/final-recheck.json:17`, `round-16/verification.json:317` | **unlabelled_variant** |
| 3 | custody-pair | :449 | tool | **no argv receipt anywhere**; produced receipt `.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/receipts/custody-live.v2.json` (no argv field) | exercised, argv not retained |
| 4 | quote-fidelity | :450 | gate | `.ufo/waves/round-14/verification.json:93` (`quote-corrected`, absolute paths) | **unlabelled_variant** (relative vs absolute only) |
| 5 | go-snapshot-inventory | :487 | probe | `.ufo/waves/round-15/verification.json:29,46` (exit 0); `verification-initial.json:29,46` (exit 1, traceback) | **exercised_match** |
| 6 | go-selection-preview | :506 | probe | `.ufo/waves/round-16/verification.json:96` (1.24.7) and `:76` (1.24.5 contrast) | **exercised_match** |
| 7 | round16-structural-controls | :507 | probe | `.ufo/waves/round-16/verification.json:353`; `.ufo/waves/round-16/controls.json:403,411,418,1009` | **exercised_match** (placeholders bound to real revs) |

Counts: 7 rows; **4 exercised_match**; **2 unlabelled_variant** (448, 450);
**1 with no argv receipt at all** (449). No row contains the word
`unexercised` or a self-declared "variant" label (`grep -n 'unexercised\|variant' SKILL.md`
returns nothing).

## 2. Row detail and flags

### 1. interactive-r1-recovery — SKILL.md:447
Advertised: `python3 .ufo/rounds/interactive-r1/verify-recovery.py` (relative,
no `-I`). Exercised verbatim — the same relative spelling — at
`gate-before.json:4` (exit 2, `missing_result`), `gate-results.json:7`
(exit 0), and `gate-correction-results.json:9`. The advertised variants are
also retained: `--selftest` (`gate-results.json:17`,
`gate-correction-results.json:19`) and `--admission` (`gate-results.json:28`,
`gate-correction-results.json:30`, exit 2). **Match; no drift.** Caveat: none
of the three receipts records `cwd` (`grep -c '"cwd"'` = 0), so resolution to
the repo root is [INFERENCE], not retained.

### 2. citation-drift — SKILL.md:448  ← flagged
Advertised (relative script, `--root .`, relative table/expected, **no** `-I`,
**no** `--strict`):
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`

All four argv receipts differ from the advertised spelling:
- `.ufo/waves/round-14/verification.json:106` — script/table/expected absolute, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, **`--strict`** appended; no `-I`; exit 0.
- `.ufo/waves/round-15/verification.json:127` — same absolute form, `--strict`; **exit 1** (`--rev 7ad23fe…`).
- `.ufo/waves/round-15/final-recheck.json:17` — same absolute form, `--strict`; exit 0 (`--rev ba3b219…`).
- `.ufo/waves/round-16/verification.json:317` — same, **plus `-I`**; exit 0.

So the exercised universe carries: relative→absolute (all four), `--strict`
(all four; the row's primary command omits it), and `-I` only from round 16
(row omits it). Even normalizing paths, the advertised non-strict command
still does not equal any exercised argv. Non-strict quoted invocations exist
only in prose, e.g. `.ufo/waves/arc2-loop1-round4/E9.md:237,493` — not argv
receipts. **Round-17 implication:** C1(b)'s "re-exercised with its isolated
absolute argv" will retain an argv that still differs from this row (relative
flags + no `--strict`), so the row needs an explicit label/correction or the
invocation audit will count it again. At this snapshot no round-17
citation-drift receipt exists.

### 3. custody-pair — SKILL.md:449
Advertised: `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]`
(relative, no `-I`). **No argv array anywhere under `.ufo` mentions
`custody-pair` (0 of 235).** What is retained:
- A produced v2 receipt: `.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/receipts/custody-live.v2.json`
  — `:3` pins the instrument sha `112d01dc…`, `:6` `capture-label: ex33-live-5path`,
  `:8` `cwd: /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `:10`
  `paths: 5  present: 5`; sidecar `.sha256:1`; digest also in `manifest.sha256:13`.
  There is no `argv` field in the receipt.
- Quoted invocations only: `.ufo/waves/arc3-loop1-round2/seats/EX-31.md:74,77,79`
  (relative `python3 .ufo/gates/custody-pair/custody-pair.py capture --out $EX/… --label …`),
  `.ufo/waves/arc3-loop1-round2/seats/CR-4.md:96`,
  `.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/attack-rewrite.md:170`;
  harness variants add `--paths` (`.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/tools/attack_real.sh:14`)
  or use `--out -` (`.ufo/waves/arc3-loop1-round2/claims/c3/RV-14/independent-battery.sh:20`).

[INFERENCE] The `custody-live.v2.json` header (repo-root cwd, five canonical
paths, label supplied) is consistent with the advertised command executed
from the repo root; the receipt proves the capture happened but not the argv
tokens. Flag: this row cannot be matched by an argv-only auditor at all, so
it needs either a labelled receipt that records `argv` or an explicit
"unexercised argv" label.

### 4. quote-fidelity — SKILL.md:450  ← flagged
Advertised (relative, `-I`): `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json`.
Exercised at `.ufo/waves/round-14/verification.json:93` (`quote-corrected`)
with **absolute** script and manifest paths (`:96` onwards), `-I` present,
exit 0. Difference is relative→absolute only (`-I` is consistent, so **no
missing-`-I` drift**). Under a normalizer that absolutizes against the repo
root this is a match; under a literal comparator it is not — the tool being
built this round must state which (`W/tools/invocation-audit.py` contract
says only "placeholders `<...>` as wildcards ... modulo leading
`python3`/interpreter path"). The row's `--frozen` variant is retained
absolute at `round-14/verification.json` commands/2, `round-15/verification.json`
commands/5, `round-16/verification.json` commands/15; `--selftest` at
round-14/15/16 commands/1,4,14.

### 5. go-snapshot-inventory — SKILL.md:487
Advertised and exercised identically (absolute, `-I`):
`python3 -I …/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`.
Four argv records: `round-15/verification.json:29,46` (both exit 0) and
`round-15/verification-initial.json:29,46` (both **exit 1**, stderr
`TypeError: '<' not supported between instances of 'dict' and 'dict'` at
`:43`/`:60`, revision `856d193b…` = `initial_failed_revision`; the passing
file's `inventory_equal` is `true`). The row's pinned cell already records
the "Round-16 correction" that fixed the advertised spelling
(`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:76-88`).
Calibration: argv equality includes a failed run; match ≠ success.

### 6. go-selection-preview — SKILL.md:506
Advertised and exercised identically (absolute, `-I`): `.ufo/waves/round-16/verification.json:96`
(`selection-1.24.7-linux-amd64`, exit 0) and the documented contrast at `:76`
(`selection-1.24.5-linux-amd64`, exit 0). Secondary: the row's 4th-cell
fixture self-check advertises **two** `--fixtures`; the retained argv
(commands/3, label `all-developer-fixtures`, exit 0) passes **eight**
`--fixtures` (both advertised files plus six w2 case files) — a superset, so
the exact two-file argv is not retained. Round-17 w1 `selection-1.27.2.json`
etc. are outputs, not argv receipts.

### 7. round16-structural-controls — SKILL.md:507
Advertised: `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/controls.py <BEFORE> <AFTER>`.
Exercised at `.ufo/waves/round-16/verification.json:353` (exit 0, cwd
recorded) with `<BEFORE>`=`6235498b4112350eebce0812a74af1781fc0ee88`,
`<AFTER>`=`27b8fc13156230981312c44380cddab1f2bd318d`; `.ufo/waves/round-16/controls.json:403`
(`argv`, script-only), `:411` (`orig_argv`, includes `python3 -I`), `:418`
(`producing_command`), `:419` (`repo_root`), `:1009` (`revisions`). The row's
claim "argv and resolved immutable revisions retained" is observed true.
Match.

## 3. Flag summary (rows whose advertised command differs from every exercised argv)

- **:448 citation-drift** — relative vs absolute (script, `--root .`,
  table, expected) **and** missing `--strict` in the advertised command
  **and** `-I` present only in the round-16 receipt. Clearest drift; the four
  retained receipts are all a different invocation shape.
- **:450 quote-fidelity** — relative vs absolute (script + manifest); no
  missing `-I`.
- **:449 custody-pair** — no exercised argv exists; the produced v2 receipt
  and seat-report quotes attest execution but carry no argv. Cannot be
  matched or falsified by an argv-only audit.
- No drift: :447 (relative == relative, but `cwd` unretained), :487, :506,
  :507 (absolute + `-I` both sides).

## 4. Calibration notes for the invocation-audit producer

1. **Path-form normalization is undefined in the contract.** Row :447
   matches literally; row :450 matches only if relative paths are resolved
   against the repo root. Without that rule the audit reports a false
   `unlabelled_variant` for :450 (and, if the row is rewritten to absolute,
   for :447). The normalizer's path rule must be written down.
2. **`cwd` is not uniformly retained.** Round-16 receipts carry `cwd` (22
   entries); round-14/15, final-recheck and the interactive-r1 receipts carry
   none. A relative advertised command matched against a cwd-less receipt is
   not reproducibility-proven.
3. **`-I` is not stable across rounds.** The same tool family is retained
   without `-I` in rounds 14/15 and with `-I` in round 16, so an audit that
   treats interpreter flags as insignificant is the only stable reading.
4. **`--strict` changes the verb.** The citation-drift row advertises the
   probe (non-strict) form, but every retained argv is the strict gate form;
   these are different exit maps (0/2 vs 0/1/2), not a flag cosmetic.
5. **Match ≠ success.** :487's exact argv has four retained runs: two exit 1
   (traceback at `856d193b…`) and two exit 0. A matching receipt can be a
   failed run.
6. **Receipt-without-argv.** :449's `custody-live.v2.json` is a real
   product receipt that pins the instrument sha, cwd, path count and label
   but not argv; an argv-only receipt set cannot see it.

## 5. Bounded unknowns

- No round-17 receipt for :448 yet (the C1(b) re-exercise is not retained at
  this snapshot); whether its "isolated absolute argv" will match the row's
  relative spelling is currently **unknown**.
- Whether `.ufo` Git history contains a deleted argv receipt that matched
  :448/:450 exactly was not checked (working tree only; no Git object reads).
- The `custody-pair` argv used for `custody-live.v2.json` is not recoverable
  from any retained artifact; only the receipt header constraints are.
