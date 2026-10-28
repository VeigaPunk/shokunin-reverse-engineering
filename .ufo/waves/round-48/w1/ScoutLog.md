# ScoutLog — LOG.md round-entry format (read-only)

Question: exact heading/format a round-48 `LOG.md` entry must follow, and the line number where it belongs.

Source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md` (3434 lines, trailing newline, no blank line after the last line). Last three round entries are rounds 45, 46, 47. `plans/round-48-claims.md` does not name `LOG.md`. No standing rule in `SKILL.md` or `plans/` prescribes a LOG heading. The format below is the shared shape of those three entries, not a frozen clause.

## Where it belongs

Append after line **3434** (the last line of the file: `` `fullmatch`. ``, the close of the round-47 `**Source.**` bullet). The new heading is therefore line **3436**, with a single blank line at **3435** separating it from round 47. Do not insert earlier: rounds 45–47 are one contiguous append-only tail (round 45 opens at 3234; round 47 has no ledger or amendment subsection after it).

## Heading a round-48 entry must follow

The last three entries do **not** share one heading string. Two generations are present:

| round | line | heading |
|---|---|---|
| 45 | 3234 | `## 2026-10-28 — round 45 (KaidokuR45): the freeze rule becomes an instrument with four red arms; the registry names the six claim-carrying instruments` |
| 46 | 3319 | `### Round 46 — the measure becomes a discriminator: block 23 scores its own forgeries red and the registry names the 38-instrument census` |
| 47 | 3405 | `### Round 47 — an instrument's binding is an equality, and the record is re-derived` |

Rounds 46 and 47 (the two newest) agree, and round 45 does not. The round-48 heading must match 46/47:

```
### Round 48 — <one-line statement of what the round's instruments did>
```

Exact tokens: three hashes, one space, `Round 48`, space, em dash `—` (U+2014), space, then a prose clause. Not `##`, not a date prefix, not `(KaidokuR48)`, not a colon. Round 45's older form (`## <date> — round N (KaidokuRNn): …`) is the previous generation; copying it would break the 46/47 run.

## Body format those three entries share

1. Heading, then one blank line, then a prose opening (not a bullet). Round 47's opening is two sentences naming both claims, both axes, both counters and what each scores. Round 46 opens with `Lane `kaidoku`, round 46, attempt 1. Base `<full sha>.` then the freeze sentence.
2. Then `- **<Label>.**` bullets, each label bold and ending with a period inside the bold. Wrapped continuation lines are indented two spaces.
3. Labels present in the recent entries, in this order where they appear: a claims/freeze bullet, a per-claim before→after bullet carrying the counting command and the receipt path, a record-repair bullet, a source bullet, a frontier bullet, a waves bullet. Round 47 (shortest, and the immediate predecessor) uses exactly four: `Freeze series, disclosed.` / `Before → after, measured.` / `The record repaired, append-only.` / `Source.`
4. Subsections under the entry, when present, are `###` too, so they sit at the same level as the 46/47 entry heading: `### Round N claim ledger` (the 7-column table `claim | axis / surface | before | after | counting command | measured at | verdict (author)`) and `### Round N amendment (append-only) — …` or `### Amendment A<k> — …`. Round 47 has neither subsection yet; round 45 has the ledger plus A2 and A3. A round-48 ledger or amendment, if written, follows that `###` shape and stays inside the entry (before the next round heading).
5. Append-only. Nothing in rounds 45–47 rewrites an earlier heading. A correction to a prior round is a new subsection or a later round's bullet, not an edit of the old entry.

## What is not specified

The claims file's landing requirement binds `SKILL.md` and `SCORECARD.md` only. It does not require a `LOG.md` entry, so the heading shape above is the observed convention of rounds 46–47, not a counter clause. The prose after the em dash is chosen per round (no template token). No date is fixed for the 46/47 form; round 45's date (`2026-10-28`) lives only in the older `##` form.

## Axes

- coverage: all three round entries read in full, plus a search of `plans/` and `SKILL.md` for a LOG-format rule (none found).
- depth: heading byte-pattern compared across 45/46/47; insertion point checked against EOF (3434 lines, trailing newline, no extra blank).
- calibration: the 45 form is reported as the older generation, not averaged into the required heading. Confidence high on the 46/47 pattern and on line 3436; the prose after the dash is not prescribed by any file.
