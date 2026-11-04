# Round 80 — kaidoku

Purpose: report the round's three claims as filed, then name the sitting errors (r79) and the four
new ones this round found in its own surface, with the corrected bytes as the check.

## Mistakes

| # | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M80-1 | Unrecoverable instrument provenance — a receipt's `instrument.sha256` names no committed blob, so no reader can re-derive the receipt's instrument. | `.ufo/waves/round-79/l1/scores/c2-at-landing.json` carried `instrument.sha256 a0044c4c5006…`; `git log --all -- tools/round-79/pointer-bind.py` holds only `91d23dad…` and `40905d39…`; `python3 -I -B tools/round-79/pointer-bind.py --validate <base blob>` → `defects ["instrument sha256 is not this file's digest"]` (extracted from `git show 16dfa009:…`). | `none` before round 80; the round-79 non-author spot-check found it by reading one file, and only R80-C2 makes the class checkable (`tools/round-80/receipt-provenance.py`). | Re-take the receipt with the committed instrument and a disclosed `instrument_supersessions` entry. Shown able to fail: the sweep at base reports `receipts 34, flagged 2, unexpected 1` naming this receipt; after the re-take `flagged 1, unexpected 0`, the remaining flag being the declared negative control `prov-forged-instrument.json` (`.ufo/waves/round-80/l1/scores/c2-at-base.json`, `c2-at-landing.json`). |
| M80-2 | A repair that moves a pinned field — re-taking a receipt with an abbreviated `--rev` turns `record.rev` into an 8-hex token, which the same instrument refuses as a committed revision. | My first re-take used `--rev ed68cd0a`; `python3 -I -B tools/round-79/pointer-bind.py --validate` on it returned `defects ["record rev is not a 40-hex commit"]`. The filed r79 receipt's `record.rev` was in fact the full 40-hex (`ed68cd0a6cc7…`), so the defect was introduced by the repair, not inherited. | The instrument's own `--validate`, run before filing (round-79's practice: a receipt is validated before it is cited). | Re-take with the full 40-hex rev; the final receipt validates `{"checks": 5, "defects": [], "matched": 5}`. The r80 provenance sweep also refuses a symbolic rev (`@HEAD@`, `main`) as a committed revision, with a red case. |
| M80-3 | A guard exercised is not a guard pinned — a selftest case reaches a refusal clause without failing when the clause disappears. | At base `16dfa009` eight of the nine `validate_receipt()` clauses survive deletion with every case green (only `: refused without a reason` is killed); reproduced by `w1/ReviewerC3/deletion-receipt.json` and by the r79 `w1/MutInstruments` survivor set. | The deletion test, made executable this round by `tools/round-80/guard-battery.py` (`survivors 9` at base, `0` at landing); before it, the class was named by round 79's mutation seat but not measured over all nine. | One isolating case per clause plus the table row that binds it. Shown able to fail: base `guards 9, rows 0, bound 0, survivors 9` versus landing `rows 9, bound 9, survivors 0, pristine 37/0`; each of the nine mutants fails exactly its declared case (`w1/ExecGate/mutants.json`). |
| M80-4 | Prefix acceptance — a declared token matches inside a longer live token, so a stale or superseded pin scores green. | The round-79 binder binds `rea-agents@6.7.0` inside `rea-agents@6.7.05` and `rea-agents@6.7.00` (frozen fixtures `rb01`/`rb02`); the strictness battery scores the r79 implementation `control_false_greens 4` at base. | `none` until R80-C1; round-79 ReviewerC2 named the limit, no counter existed. | The delimited-token rule with two green controls that a refuse-everything implementation fails. Shown able to fail: the same battery scores the r80 binder `candidate_false_greens 0` and the r79 binder `4` in one run (`.ufo/waves/round-80/l1/scores/c1-at-base.json`, `c1-at-landing.json`). |
| M80-5 | Silent collapse — a parser that maps cells through a dict keeps the last cell and loses an earlier one with no signal. | `parse_record()` at round 79 returns five checks and no duplicate flag for a record declaring `OMP` twice (frozen fixtures `rb03`/`rb04`); measured by the round-80 battery's record arm. | `none` until R80-C1; the count-based rule ("five cells") cannot see a sixth cell that was overwritten. | Count every declared cell and list the repeated client in `duplicates`. Shown able to fail: the control reports `checks_total 5`, the candidate `checks_total 6` with `duplicates ["omp-pin"]` on the same fixture. |

| M80-6 | A new row for a URL already held — the append ran before the duplicate check, so S297 re-rowed RFC 8259 §4 although S049 already teaches that exact scope. | `.ufo/waves/round-80/l1/pre-append-url-check.txt` names the holders (S049 and S289 for the RFC, S143 for the `re` page); the census's `W04` fired for S297 (and fires for S298, the deliberate different-anchor row) — a warning, exit 0, which is why the gate did not stop the append. | The corpus rule (`a URL already held is a refused reuse, not a row`) plus the census `W04`; neither is fatal, so the check has to run before the append. | Drop S297, cite S049 and extend its `used-by` (`corpus/lessons/round-21.md` → `corpus/lessons/round-21.md, corpus/knowledge/2026-11-04-r80-strict-tokens-and-provenance.md`, recorded here as the old → new change); the pre-append check is now a committed receipt. Shown able to fail: the check prints S049 for the RFC URL, so the append is refused; it also prints S143 for the `re` URL, which is why S298 declares itself the same document with a different anchor. |

Sweep that found none of a sixth class: `grep -rn 'defects.append\|DUP\|duplicates' tools/round-79 tools/round-78/attack-gate.py`
was read clause by clause by `w1/ScoutGate` and `w1/ReviewerC3`; no further refusal clause exists in
`validate_receipt()` beyond the nine the table now binds (clause count 9 at both revisions,
`c3-at-base.json`/`c3-at-landing.json` `guards 9`).

## Gate

Round-80 sources, each opened this round with a located quote (≤25 words) and a pinned snapshot in
`.ufo/waves/round-80/l1/sources/`:

| source | URL | accessed | quote (location) | digestion |
|---|---|---|---|---|
| S049 RFC 8259 §4 (held from round 21; re-opened, no new row) | https://www.rfc-editor.org/rfc/rfc8259.txt | 2026-11-04, HTTP 200, 28 360 B, sha256 `61a5378f…` | "The names within an object SHOULD be unique." (line 322, 8 words) | duplicate-cell refusal is an interoperability rule (`SHOULD`); ECMA-404's "does not require" is the recorded counterpoint |
| S298 Python `re` §`\b` | https://docs.python.org/3/library/re.html | 2026-11-04, HTTP 200, 257 722 B, sha256 `24ef5ff0…` | "Matches the empty string, but only at the beginning or end of a word." (line 747, 14 words) | delimited-token rule: token binds only between word boundaries or slice edges |

**Rejected (1 admit-side refusal, with flip):** Wikipedia, `JSON` —
https://en.wikipedia.org/wiki/JSON (opened 2026-11-04; snapshot `w1/ScribeSources/wiki-json.html`,
478 308 B). Reason: tertiary source, and the same article quotes ECMA-404 saying the syntax "does
not require that name strings be unique", so as a row it would sit against the rule it appears to
illustrate. Flip: admit only if a claim needs the grammar-versus-interoperability distinction as its
evidence. **Second candidate, unreachable:** a Stack Overflow question on duplicate JSON keys — the
fetch returned a Cloudflare challenge page (`Just a moment...`, 5 753 B); class `unreachable`, not
fabrication, so no row and no quote.

## Sources

Opened this round: the two URLs above (re-fetched and sha256-pinned in
`.ufo/waves/round-80/l1/sources/`), plus the two rejected candidates. Registry rows 202 → 203: one
new row (S298, the same document as S143 with a different anchor — `\b` rather than `fullmatch`,
stated in the row and warned as `W04`), and one refused reuse (RFC 8259 §4, already S049; the row was
withdrawn before landing and S049's `used-by` gained this round's knowledge entry). Census: 203 rows,
24 `W04` warnings (23 pre-existing plus S298's), exit 0.
