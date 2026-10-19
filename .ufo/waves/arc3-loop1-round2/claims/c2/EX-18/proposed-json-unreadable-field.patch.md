# Proposed patch text (NOT applied) — expose the H1 unreadable class in `--json`

Seat EX-18 (executor, c2), arc3-loop1-round2. **Patch text only** — the real
target `.ufo/gates/c1-census-v10.py` is EX-16's to write.

Motivating measurement (this seat, `logs/P2.json`, H1 candidate sha256
`8b1a2079…`):

```
SKILL.md absent, H1 candidate, --json:
  verdict = "FAIL"
  scope_errors = []
  counts["SKILL.md"] = {"lines": 0, "loci": 0}
  key set == the unpatched instrument's key set   # no field names the file
```

H1's new class lives in the text report and the exit code only. A JSON consumer
(any downstream gate reading `--json`) sees `FAIL` with every declared field
empty — the cause is unstated. For the `PROVINCE.md`-absent control the marker
class still shows up in `scope_errors`, so only the files whose rows are all
CURRENT lose their cause in JSON.

## Proposed diff (on top of H1's `unreadable` list; context is v10 `main()`)

```diff
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                           "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                           "unresolved": unres, "scope_errors": scope_errors,
+                          "unreadable": unreadable,
                           "g11": g11, "g7": g7, "g2_ok": g2_ok,
```

Semantics: the same list the text report prints (each element
`"<file>: <ExceptionType>"`) becomes machine-readable. Coupled to H1 — the
list object is created by H1's `except OSError as ex` branch; without H1 the
name does not exist.

Independent-tool check (if landed): `python3 c1-census-v10.py --root <root>
--json | python3 -c "import json,sys; d=json.load(sys.stdin);
print(d['verdict'], d.get('unreadable'))"` on an absent-`SKILL.md` root must
print `FAIL ['SKILL.md: FileNotFoundError']`.
