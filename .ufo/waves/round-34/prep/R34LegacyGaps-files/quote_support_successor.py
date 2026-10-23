#!/usr/bin/env python3
"""R34LegacyGaps successor core for the archived round-32 quote gate.

`.ufo/waves/round-32/source-reopen/verify_quotes.py` is a secondary gate with no
selftest: it executes at import with hardcoded snapshot/scratch paths, so it
cannot be replayed from an isolated fixture and is NOT declared conformant here.
It also mixed informational rows into its check list (every `drift:html:*` row
was recorded with a literal True predicate), so its row count overstates checks.

This successor carries only the mechanical support predicate that the archived
gate used - contiguous location on one raw line, exact expected line, and a
25-word cap - plus a row kind split that keeps diagnostics out of the check
count. It reads plain text; no binary content, no network, no scratch paths.

Selftest mutants are applied by the outer harness to copies of this file:
  Q-1  word cap  `if w > MAX_WORDS:`            -> `if w > MAX_WORDS + 1:`
  Q-2  location   `if want_line is not None and ln != want_line:` -> `if want_line is not None and ln is None:`
The newline guard is not mutated: it only sharpens the reason string, because a
quote containing a newline can never be found on one raw line anyway. Neither
outcome-bearing clause may be left unexercised.

Exit: 0 all support rows match expectation (or selftest green), 1 mismatch,
2 unusable cases file.
"""

import argparse
import json
import os
import sys

MAX_WORDS = 25


def word_count(quote):
    return len(quote.split())


def supports(text, quote, want_line=None):
    """Return (ok, why) for a mechanical quote-support row.

    A quote is supported when it is one non-empty raw-line-contiguous string,
    has at most MAX_WORDS words, and is located at exactly `want_line` when a
    line is required. `text` is the whole document.
    """
    if not isinstance(quote, str) or not quote.strip():
        return False, "empty quote"
    if "\n" in quote:
        return False, "quote is not one contiguous raw line"
    if want_line is not None and (not isinstance(want_line, int) or isinstance(want_line, bool) or want_line < 1):
        return False, "line is not a positive integer"
    w = word_count(quote)
    if w > MAX_WORDS:
        return False, "quote has %d words (>%d)" % (w, MAX_WORDS)
    lines = text.splitlines()
    start = want_line or 1
    ln = None
    for i in range(start - 1, len(lines)):
        if quote in lines[i]:
            ln = i + 1
            break
    if ln is None:
        return False, "quote not found from line %d" % start
    if want_line is not None and ln != want_line:
        return False, "quote found at line %d, not %d" % (ln, want_line)
    return True, "line=%d words=%d" % (ln, w)


def run_cases(root, cases):
    """Run declarative rows. `kind: diagnostic` rows are reported but never counted."""
    fails = 0
    support_rows = 0
    info_rows = 0
    for case in cases:
        if not isinstance(case, dict) or not case.get("name"):
            print("FAIL\tunnamed case\tcase is not an object with a name")
            fails += 1
            continue
        name = case["name"]
        if case.get("kind") == "diagnostic":
            info_rows += 1
            print("INFO\t%s\tnot a check" % name)
            continue
        path = os.path.join(root, case.get("file", ""))
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            print("FAIL\t%s\tinput unusable: %s" % (name, exc))
            fails += 1
            support_rows += 1
            continue
        ok, why = supports(text, case.get("quote"), case.get("line"))
        want = case.get("expect") == "pass"
        good = ok == want
        fails += not good
        support_rows += 1
        print("%s\t%s\t%s" % ("ok" if good else "FAIL", name, why))
    print("cases=%d support=%d informational=%d failures=%d" % (
        len(cases), support_rows, info_rows, fails))
    return 0 if fails == 0 else 1


def fixture_text():
    run26 = " ".join("w%02d" % i for i in range(1, 27))
    return "\n".join([
        "# fixture source",                                                       # 1
        "The two low bits of StartOffset contain a range type.",                  # 2
        "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file.",  # 3
        run26,                                                                    # 4
        "A quote that starts here and",                                           # 5
        "continues on the next raw line.",                                        # 6
    ]) + "\n"


def selftest():
    text = fixture_text()
    run26 = " ".join("w%02d" % i for i in range(1, 27))
    cases = [
        ("located on the expected line, within the cap",
         supports(text, "The two low bits of StartOffset contain a range type.", 2), True, "line=2"),
        ("located without a line requirement",
         supports(text, "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file."),
         True, "words=16"),
        ("expected line after the real one", supports(text, "The two low bits of StartOffset contain a range type.", 3), False,
         "not found from line 3"),
        ("fabricated quote", supports(text, "The three low bits of StartOffset contain a range type.", 2), False,
         "not found"),
        ("contiguous 26-word run present in the bytes", supports(text, run26, 4), False, ">25"),
        ("quote spanning two raw lines",
         supports(text, "A quote that starts here and\ncontinues on the next raw line.", 5), False,
         "one contiguous raw line"),
        ("empty quote", supports(text, ""), False, "empty quote"),
        ("quote located later than the expected line",
         supports(text, "continues on the next raw line.", 5), False, "line 6, not 5"),
        ("line hint is not an integer", supports(text, run26, "4"), False, "positive integer"),
    ]
    fails = 0
    for name, (ok, why), want, why_sub in cases:
        good = ok == want and why_sub in why
        fails += not good
        print("%s\t%s\t%s" % ("ok" if good else "FAIL", name, why))
    print("selftest cases=%d failures=%d" % (len(cases), fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="round-34 successor core for archived quote-support rows")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", help="directory inputs are resolved against")
    ap.add_argument("--cases", help="JSON list of {name, file, quote, line, expect, kind}")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.cases or not a.root:
        ap.error("one of --selftest or --root with --cases is required")
    try:
        with open(a.cases, encoding="utf-8") as fh:
            cases = json.load(fh)
    except (OSError, ValueError) as exc:
        print("CASES unusable: %s" % exc)
        sys.exit(2)
    if not isinstance(cases, list):
        print("CASES unusable: not a JSON list")
        sys.exit(2)
    sys.exit(run_cases(a.root, cases))


if __name__ == "__main__":
    main()
