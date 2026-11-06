# ReviewerCounter probes — R100 w1 (counters at F = 8e24c29a37ca81a0bd1ff5ec73c96a949885322e)

All commands run by seat ReviewerCounter on 2026-11-05. Frozen counter bytes extracted with
`git -C <lane> show F:<path>`; `worktree == F` verified byte-identical for both counters
(`registry-selftest-truth.py` sha256 496a4979ecd6…, `pe-upx-corrupt-battery.py` sha256 8f148d336e6f…).
Probes executed in a `git clone --shared` of the lane checked out at A2 = cbd224ef… (toplevel asserted).
Scratch: /fast/scratch/hyaku/kaidoku-r100/ReviewerCounter (deleted after report).

## P1. C2 population vs SKILL.md at B (6371c886)
- registry rows total 186, dups none. Claim-bearing rows at B (parse_claim != None): **93**.
- set(POPULATION) == set(claim-bearing): exact, both directions empty.
- Seven stated counts at B: attest 15, record(r47) 9, packed-elf(r71) 31, seam-probe(r71) 7,
  record-audit(r76) 17, plan-command(r76) 3, upx-field-value-repair(r89) 16 — matches claims plan.

## P2. Pins
- All 93 rows / 95 pinned files: sha256(file at B) == frozen pin (0 mismatches).
- All 95 pinned files: sha256(file at A2) == frozen pin (0 mismatches) → pins hold at the landing rev.
- B→A2 changed outside .ufo/waves/round-100/pre/: SKILL.md, plans/round-100-claims.md,
  tools/round-100/{forgeries h0..h6, gen-forgeries.py, both counters (new), upx-pe-repair.py (new)}.
  No pinned tool byte changed B→A2.

## P3. C2 argv table vs documented commands
- 89/93 rows: frozen argv ≡ documented self-test command (modulo placeholder spelling
  `<F>/<R>/<dir>/$HYAKU_SCRATCH ≡ {work}/{pkg65}/{rev}` and in-clone `HEAD ≡ {rev}`).
- 4/93 drift (frozen argv ≠ documented verbatim; all four counted == claimed at L1 anyway):
  1. tools/round-53/sqfs-triage-v6.py — doc `python -X utf8 -I -B … --selftest`; frozen `python3 -I -B … --selftest` (drops `-X utf8`, python→python3).
  2. tools/round-55/v6-block-digest.py — same pattern.
  3. tools/round-96/kill-rule-v2.py — doc `--selftest --work <dir>`; frozen `--selftest` (drops --work).
  4. tools/round-96/stop-boundary-repair-battery-v6.py — doc `--selftest --work <dir>`; frozen drops --work.
- L1 receipt (c2-at-cbd224ef…json) records these same argvs; counter_sha256 496a4979ecd6 = F bytes.

## P4. C2 parser probes (imported frozen module)
- CLAIM_RE: "selftest 3 cases; suite covers 18 cases" → 3 (first wins); "18 of 18 cases" → 18;
  "--max-cases 5"/"sub_cases=7" → None; "#cases=9" → **9** (lookbehind allows '#'); "cases: 12" → 12.
- OBS_RE/JSON: two counts → LAST wins ("SELFTEST cases=17 failures=3\nplanned cases=18" → 18);
  JSON int beats text; dict without int `cases` falls to regex and matches inside a STRING value
  ('{"detail": "cases=5"}' → 5); stderr-only counts parsed.
- registry_rows: a row indented by one space is skipped (line.startswith("| `")); any POPULATION row
  thus hidden fails the row atom (fail-closed). Doubled/missing markers → ValueError → exit 2.

## P5. C2 receipt + isolation
- write_receipt probe: missing parent dir → FileNotFoundError; --json-out is a dir → IsADirectoryError;
  both uncaught in main → traceback + exit 1 (predicate-fail semantics) instead of exit 2.
- mkstemp+fsync+os.replace+finally-unlink: no `.receipt-*` leftovers after the failure probes.
- `python3 -I -B <clone>/tools/round-100/registry-selftest-truth.py --selftest` → SELFTEST cases=22
  failures=0, rc=0.
- Full frozen C2 run at A2 (see results file): label met, exit 0; work dir was rmtree'd
  (CANARY.txt deleted); `git -C clone status --porcelain` empty afterwards (clone isolation holds;
  rows ran with cwd=clone, env PATH/HOME/HYAKU_SCRATCH/TMPDIR/LANG only, c2.py:147-150).

## P6. C1 ph_fields ground truth (all 10 pinned carriers, packed with /usr/bin/upx 5.2.0 --best)
For every carrier: first `UPX!` = PackHeader; c_len at i+20; **zlib.adler32(data[i+32:i+32+c_len]) ==
c_adler at i+12 on 10/10** (rule of S327 `ph_decompress` + getPackHeaderSize()=32); range end
i+32+c_len ≤ filesize 10/10; decoy window eligible 9/10 (sevenzip64dll false → decoy_cells 9).
c_len values: t32 35016, t64 40485, w32 33376, w64 39007, winhello 35296, fastlist64 128083,
freeglut32dll 71166, gle64dll 33596, llio32dll 28527, sevenzip64dll 1062110.

## P7. C1 exec-leg strace probes (same argv shape as traced(), c1.py:216-227)
- clean `pass` → 1 exec line, extra=0 (leg passes).
- os.execv self-restart → 2 lines, extra=1 (violation). os.posix_spawn(/usr/bin/true) → 2, extra=1.
- subprocess.run → 2, extra=1. fork without exec → 1 line, extra=0 (invisible, but cannot exec an oracle).
- strace counts failed exec attempts too (any `execve(`/`execveat(` line), first line per log skipped.

## P8. C1 filename-keyed forgery (clone/tools/round-100/w1-review-forgery.py)
- Repairs magic/names/both/intact/overlay/decoy from a self-validating PackHeader scan (adler) +
  section-table rename reversal; refuses `.corrupt-`/`.trunc-` inputs from the FILENAME alone
  (before opening the file). No FORBIDDEN token hits (static arm passes).
- Sanity outside battery: repairs a `both`-tampered t32 pack to unpack-equality (rc 0, sha ok);
  refuses a corrupt-named input rc 2 with no --out.
- Full frozen battery run: see results file (label/exit in results file).

## P9. L1 receipts (cross-check)
- c1-at-a610671d…json: met True, exit 0, full label as TARGET, exec arm invocations 154, violations [].
- c2-at-cbd224ef…json: met True, exit 0, full label as TARGET, excluded {}.
- Invocation arithmetic: 30+9+10+20+40+40+2+3 = 154 traced candidate invocations ✓.
