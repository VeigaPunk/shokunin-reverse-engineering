source: S319 — Python json module documentation — https://docs.python.org/3/library/json.html, anchor #json.dump, docs page sha256 8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0, accessed 2026-11-05. The registry row is S319 in corpus/SOURCES.md.
verified-at: 2026-11-05, base 8a40ceb6516bb38c19c37bcbff2bb3332f31c832. The frozen round-93 counter is tools/round-93/stop-boundary-repair-battery-v3.py, sha256 60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3.
recheck: on-release, or 90d. Re-fetch the page with curl -fsSL https://docs.python.org/3/library/json.html and re-hash it. The located sentence must still read as quoted.
The `json.dump` documentation states, at the `#json.dump` anchor, that the `default` hook "should return a JSON encodable version of the object or raise a TypeError".
The same section states that a `TypeError` is raised when no `default` hook is supplied.
The module never encodes bytes on the writer's behalf: `json.dump` raises `TypeError: Object of type bytes is not JSON serializable` for a bytes value.
The round-93 counter stored the repair's raw output bytes in `fresh_cells[*].output` and wrote its receipt with `json.dump`, so the honest repair crashed the receipt writer.
Evidence: `.ufo/waves/round-93/l1/scores/c1-pos-json-stderr-at-ca5aa6a2.txt` carries the traceback.
Evidence: `.ufo/waves/round-94/pre/c1-base-v3-pos.stderr` carries the same traceback at the base revision, `.ufo/waves/round-94/pre/c1-base-v3-pos.stdout` is empty and `.ufo/waves/round-94/pre/c1-base-v3-pos.rc` reads 1.
Evidence: `.ufo/waves/round-94/pre/c1-base-v3-agreement.json` counts valid 2 of 4, agree 2 of 4, predicted 2 of 4.
The successor `tools/round-94/stop-boundary-repair-battery-v4.py` imports the frozen v3 verdict code by path and changes only the receipt writer: bytes become a length and a sha256.
The successor writes the receipt to `<json-out>.tmp` and renames it onto the target path only on success, so a failed write leaves the target absent rather than truncated; its evidence is `.ufo/waves/round-94/l1/scores/c1-v4-pos.json`, `.ufo/waves/round-94/l1/scores/c1-v4-F1.json`, `.ufo/waves/round-94/l1/scores/c1-v4-F2.json`, `.ufo/waves/round-94/l1/scores/c1-v4-F3.json` and `.ufo/waves/round-94/l1/scores/c1-v4-agreement.json`, which counts valid 4 of 4, agree 4 of 4, predicted 4 of 4.

## What the documentation states, in full

`json.dump` serializes through the standard encoder unless a `default` callable is supplied.
The documented sentence, quoted from the `#json.dump` section of the page, is: "It should return a JSON encodable version of the object or raise a TypeError."
The sentence is a requirement on the author of the hook, not a prohibition the standard library enforces.
The hook is therefore the writer's own responsibility, and the module never encodes bytes on the writer's behalf.

## The behaviour measured on this host

`json.dump` raises `TypeError: Object of type bytes is not JSON serializable` for a bytes value when no `default` hook is supplied. Measured on Python 3.14.8 with a one-line probe, and reproduced by the frozen round-93 counter.
The round-93 counter stored the repair's raw output bytes in `fresh_cells[*].output` and wrote its receipt with `json.dump` at `tools/round-93/stop-boundary-repair-battery-v3.py:353`.
The crash therefore happened on the honest repair, after the verdict was computed and before the receipt was complete.

## The successor writer

`tools/round-94/stop-boundary-repair-battery-v4.py` imports the frozen v3 verdict code by path and changes only the receipt writer.
Bytes become a length and a sha256 through the `default` hook, and any other unknown type still raises TypeError.
The receipt is serialized to `<json-out>.tmp` and renamed onto the target path only after `json.dump` returns.
A failed write therefore leaves the target path absent rather than truncated.

## The anchor, located

The quoted sentence occurs twice on the page: in the `#json.dump` section (heading **Basic Usage**, in the `default` parameter bullet) and in the `#json.JSONEncoder` section (heading **Encoders and Decoders**). It is not under `#json.dumps`, whose section text is only "Serialize obj to a JSON formatted str using this conversion table."
The sentence is not a raw contiguous byte substring of the HTML: it is exact after tag-stripping and whitespace normalisation, twice.
The page reached by the `/3/` alias is labelled **Python 3.15.2 documentation** while the host interpreter is Python 3.14.8. The quoted sentence is byte-identical in the pinned 3.13, 3.14 and 3.15 pages (two occurrences each), so the version gap does not affect this proposition.

## Calibration: what the sentence does not say

The documented sentence states the contract the hook author is expected to honour; it is not a claim about what the standard library does to a badly behaved hook.
Measured on this host: a hook that returns `str(o)` for every unknown object makes `json.dump` exit 0, so a `str()` fallback would succeed where the successor refuses it.
Measured on this host: a hook that returns `bytes` yields `ValueError: Circular reference detected` rather than a `TypeError`, because the returned bytes are themselves not encodable and are handed back to the hook.
The successor counter therefore treats "a JSON-encodable value or TypeError" as a rule it enforces on itself, and it refuses the `str()` fallback rather than inheriting one.

## What this entry does not claim

The entry does not claim that the successor writer preserves the bytes it replaces.
The entry does not claim that a helper-only selftest exercises the public command path.
The helper-only selftest is recorded at `.ufo/waves/round-94/pre/c1-v4-selftest.txt` and covers three writer cases.
The entry does not claim that any Python version other than the one measured here behaves the same way.
The entry does not claim that the docs page is stable; the recheck line carries the fetch command and the page digest.
