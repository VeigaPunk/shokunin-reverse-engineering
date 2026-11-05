## Gate

Sources opened this round (CORPUS.md rule 1). Access date 2026-11-05 for each.

| row | URL | access date | HTTP / bytes / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S319 (new) | https://docs.python.org/3/library/json.html | 2026-11-05 (opened this round) | 200 / 116296 / `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0` | `It should return a JSON encodable version of the object or raise a TypeError.` (the `#json.dump` section, **Basic Usage**, `default` parameter bullet) | the `default` hook contract of `json.dump` that the round-94 receipt writer must honour (bytes become a length and a sha256) |

Anchor notes on S319. The quoted sentence occurs **twice** on the page: in the `#json.dump` section (heading **Basic Usage**) and in the `#json.JSONEncoder` section (heading **Encoders and Decoders**); it is **not** under `#json.dumps`, whose section text is only "Serialize obj to a JSON formatted str using this conversion table." It is not a raw contiguous byte substring of the HTML: it is exact after tag-stripping and whitespace normalisation. The page reached by the `/3/` alias is labelled **Python 3.15.2 documentation** while the host interpreter is Python 3.14.8; the sentence is byte-identical in the pinned 3.13, 3.14 and 3.15 pages (two occurrences each), so the version gap does not affect this proposition.

Row changes (CORPUS.md rule 2, old → new, logged here):

- S319 appended (`mined`, opened 2026-11-05, recheck `on-release`, used-by `corpus/knowledge/2026-11-05-r94-receipt-path-json.md` and `corpus/lessons/round-94.md`). No other registry row is edited this round.

Admit / reject. Admitted this round: **S319 only** (the `json.dump` `default`-parameter contract, one located quote). Rejected: the docs' sentence about `TypeError` inside the *example* `default()` function — the `# Let the base class default method raise the TypeError` comment in the `JSONEncoder.default` example and the subclass sentence "Implement this method in a subclass such that it returns a serializable object for o, or calls the base implementation (to raise a TypeError)" — **not admitted, because it is an example and an encoder-subclass method, not the `json.dump` parameter contract**. The admitted sentence is the `default` parameter's own text inside the `#json.dump` section.

Duplicate URL note: S319's URL is already used by S050 (`Python JSON library documentation — https://docs.python.org/3/library/json.html`) under a different scope, so the census raises the expected `W04` duplicate-url-across-scopes warning for S319 (a warning, not an error). S319 is a distinct row because its scope is the `json.dump` default hook, not S050's duplicate-name and non-finite-number decoder behaviour.

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M94-a · a frozen counter's receipt writer crashes on the honest case (round-93 M93-e, carried).** `tools/round-93/stop-boundary-repair-battery-v3.py` stores the fresh cell's raw output bytes in `fresh_cells[*].output` and writes its receipt with `json.dump`, which raises `TypeError: Object of type bytes is not JSON serializable` on the honest repair; the positive control therefore exits 1 with no valid receipt. Evidence: `.ufo/waves/round-94/pre/c1-base-v3-pos.stderr` (exit 1, `TypeError` at `json.dump`), `.ufo/waves/round-94/pre/c1-base-v3-pos.stdout` (empty), `.ufo/waves/round-94/pre/c1-base-v3-pos.rc` (`1`), and the round-93 reproduction `.ufo/waves/round-93/l1/scores/c1-pos-json-stderr-at-ca5aa6a2.txt`. Captured-by: `none` — the v3 counter's own verdict was green on stdout, and no counter read the receipt file back. Fix: the successor `tools/round-94/stop-boundary-repair-battery-v4.py` changes only the receipt writer (bytes become a length and a sha256 through the `default` hook), and the frozen counting command runs the **public** CLI with `--json-out` and then `tools/round-94/c1-receipt-agreement.py`, which re-reads each receipt and requires the receipt, the stdout line and the predicted verdict to agree (`counts_of_4` valid 4, agree 4, predicted 4).

- **M94-b · a truncated receipt file read as evidence (D-93-D, carried).** A crash inside `json.dump` leaves a partial file that begins like a receipt and fails to parse, so a reader who skips validation can misread it as a pass. Evidence: `.ufo/waves/round-93/l1/scores/c1-pos-json-at-ca5aa6a2.json` (706 bytes; `json.load` fails at line 33 column 14, character 706); the routed defect D-93-D is named at `corpus/lessons/round-93-verifier-spotcheck.md:75`; the same shape is the base receipt `.ufo/waves/round-94/pre/c1-base-v3-pos.json` and `.ufo/waves/round-94/pre/c1-base-v3-F3.json` (both fail to parse, at character 706 and character 703). Captured-by: `none` — no counter parsed the receipt it had just written, so a truncated file was carried as if it were a receipt. Fix: an atomic write — the receipt is serialized to `<json-out>.tmp` and renamed onto the target path only after `json.dump` returns, so a failed write leaves the target path **absent** rather than truncated; the agreement counter treats an absent or unparseable receipt as not valid.

- **M94-c · the counter's own selftest never exercised the public `--json-out` path.** The frozen round-93 counter has no `--selftest` at all (`grep -c selftest tools/round-93/stop-boundary-repair-battery-v3.py` = 0), and the successor's `--selftest` exercises the writer's helpers only (`_default`, `write_receipt`); neither reaches the public command that produces the receipt under `--json-out`. Evidence: `.ufo/waves/round-93/l1/scores/c1-v4` is absent (no v4 receipt existed at round 93), and the helper-only selftest output `.ufo/waves/round-94/pre/c1-v4-selftest.txt` (`selftest bytes-encoded: ok`, `selftest bytes-receipt-reparses: ok`, `selftest unknown-type-raises: ok`, `SELFTEST cases=3 failures=0`). Captured-by: `none` — a helper-only green is not a green public run. Fix: the C1 counting command runs the public CLI with `--json-out` for all four frozen runs and the agreement counter re-reads the written receipts, so a helper-only green cannot stand in for the claim's evidence.

## Census

- Before: exit 0 (`.ufo/waves/round-94/census-before.txt`).
- After: (filled at landing).

## Measured

(filled at the landing commit by the L1)
