# DraftRegistryCells — round 18, wave 1 (R17-REGISTRY draft)

Author-side advisory draft for L1 (KaidokuR18). No lane file was edited. Paths are relative to LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Pin and state

- Branch tip: `refs/heads/main^{commit}` = `9011581d84527ba34c675f9cf912e54d2e72d470`; `HEAD^{commit}` equal (observed by `git rev-parse --verify`, this round).
- `git status --porcelain --untracked-files=no` empty; `git diff --stat 9011581 -- SKILL.md .ufo/waves/round-17/tools .ufo/gates/citation-drift` empty (observed this round). SKILL.md:445-546 is therefore the committed registry text.
- Worktree bytes equal the `9011581` blobs (sha256 prefixes compared): `compare.py` 555cc34b…, `receipt-validate.py` 61844882…, `pins.py` 9e9c7250…, `buildinfo-probe.py` 94ce3c20…, `citation-drift-probe.py` e2665074….

## Draft

### go-route-compare — 5th cell (replaces SKILL.md:540 cell 5)

```
Pinned values: `FIELDS` (compare.py:39), `ROUTE_FIELDS` (43; compared only when the prediction carries them, 40-43), `RULES` (45-51; `snapshot_label` is non-discriminating, request echo, line 47), required prediction and observation keys (53-62), and a hand prediction's `extra_expectations`, evaluated when present (174-176). No digest is pinned. Write scope: none in the compare path; inputs are read at compare.py:79 and the result JSON is printed at 205 and 224. `--selftest` writes only a `tempfile.mkdtemp()` directory that it removes at 439, and runs this script as a subprocess (392-406).
```

### receipt-validate — 5th cell (replaces SKILL.md:541 cell 5)

```
Pinned values: required-field lists `RETAIN_REQUIRED`, `CARRIER_REQUIRED` and `CARRIER_STEP_REQUIRED` (receipt-validate.py:55-68); digest-key preference `SHA_KEYS` = sha256_post, sha256, sha256_pre (70); `PIN_KEYS` (72). Sibling `pins.py` is loaded by path (53, 87-95) with no digest check; neither this tool nor `pins.py` pins its own digest. Write scope: none in normal mode. Receipts are read (475), committed files and the carrier are hashed (81-84, 146-150, 215), retained logs are read (158), and JSON goes to stdout (516-517). `sys.dont_write_bytecode` is set (49), and the module imports no subprocess module (docstring 32: "No network, no subprocesses"). `--selftest` writes only a `tempfile.mkdtemp()` tree, removed in `finally` (606, 708).
```

### pins — 5th cell (replaces SKILL.md:542 cell 5)

```
Pinned values: no expected digests; the only constant is `_CHUNK = 1 << 20` (pins.py:34). Each entry records sha256, size and mtime_ns of `os.path.realpath(path)` (37-72). A missing path becomes an `error` entry and `snapshot` still exits 0 (39-42, 131). `compare` treats any error entry, or size/mtime movement during the read, as unprovable (51-54, 87-95). Write scope: `snapshot --out FILE` writes `FILE.tmp` and then `os.replace`s it onto FILE (114-122). An existing FILE is replaced with no no-clobber check, and `FILE.tmp` is unlinked on failure (125). Pinned paths are opened read-only (45). `compare` writes nothing (144-157). `--selftest` writes only a `tempfile.mkdtemp()` root, removed with `shutil.rmtree` (170, 263).
```

### go-buildinfo-probe — 5th cell (replaces SKILL.md:545 cell 5)

```
Pinned values: `MAGIC = b"\xff Go buildinf:"`, `ALIGN = 16`, `HEADER_SIZE = 32` (buildinfo-probe.py:30-33); header offsets 14/15/16 and flag masks (38-48); `INFO_START` and `INFO_END` sentinels (52-53); `MAX_STRING = 1 << 20` (55). The source basis is a docstring claim: go1.25.0 `src/debug/buildinfo/buildinfo.go`, sha256 332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45, 599 lines (15-18). The local `~/.local/opt/go-1.25.0/src/debug/buildinfo/buildinfo.go` matches that digest and line count (observed this round). No digest of the tool itself is pinned. Write scope: none. The target is read once (309-310), JSON goes to stdout (611-637), and the file is never executed (4-5). `--selftest` writes only a `tempfile.mkdtemp()` fixture tree, removed in `finally` (502, 596-602).
```

### citation-drift — kind cell changed; row otherwise byte-identical to SKILL.md:448

```
| citation-drift | gate / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --table /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json --expected /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json --strict` (exercised argv: `.ufo/waves/round-16/verification.json` and `.ufo/waves/round-17/verification.json`; the same argv without `--strict` is the probe mode, an unexercised variant); **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
```

Probe-vs-strict sentence: the bold "probe semantics" sentence is kept verbatim. It is what makes `gate` honest with a probe default. Its code basis is at citation-drift-probe.py:482-484 (`--strict` flag, "default probe semantics (0 reported / 2 could-not-evaluate)") and 329-333 (verdict label `reported` vs `clean`, exit map). Observed this round at the baseline: probe mode → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

## Findings (each sentence cites its anchor)

1. **Write scope, normal mode, all five tools.** No normal path writes. Verified by reading the full bodies and grepping write, subprocess and mkdir sites.
   - `compare.py`: reads at 79; no subprocess outside `_selftest` (406). Its docstring says "Writes nothing outside tempfiles created by --selftest" (28).
   - `receipt-validate.py`: reads only (475, 81, 147, 158). No subprocess import. `dont_write_bytecode` at 49.
   - `pins.py`: reads at 45 and 135. The only normal-mode write is `snapshot --out` at 117-122, via a `.tmp` sibling.
   - `buildinfo-probe.py`: one read at 309. Writes appear only in `selftest` (522-568).
   - `citation-drift-probe.py`: reads at 153, 290, 301; `git show` and `rev-parse` at 102, 265, 273 (read-only git). Writes only in `build_fixture` (349-366) and `selftest`.
2. **`pins snapshot` is not write-only-to-`--out`.** It transiently creates `<out>.tmp` (117) and overwrites any existing `<out>` (122). The row's "writes one map" (SKILL.md:542) omits both facts; the draft cell above states them.
3. **Exit codes beyond the row's wording.** These are not in the 5th cells; they are for L1 to decide.
   - `buildinfo-probe.py` exit 2 also covers `Malformed` ELF (630-634; `elf_parse` 73-93). Observed: a 8-byte `\x7fELF` stub → `error: "malformed: not ELF"`, exit 2. The row's "2 unreadable" (SKILL.md:545) undercounts; suggested wording: "2 unreadable or malformed ELF".
   - `pins.py` exit 2 also covers unparsable or shape-invalid snapshots (147-150) and a failed `snapshot` write (128-129). SKILL.md:542 says "2 unreadable".
   - `receipt-validate.py` exit 2 also covers no arguments (730-732) and missing `pins.py` (733-737). SKILL.md:541 says "2 unreadable".
   - `compare.py` exit 2 matches the row: invalid input at 210-220.
4. **Citation-drift argv is complete for today's table.** `--snapshot-dir` is needed only for `@`-prefixed targets (citation-drift-probe.py:128-147). `pointer-table.json` has zero `@` targets (grep `"@`: 0). Kinds are anchor 15, exact 20, extracted 25 (grep -o this round). The row argv (SKILL.md:448) therefore runs the full table without `--snapshot-dir`.
5. **Frozen guard holds.** `sha256sum pointer-table.json` = `7994eec7e764e8c3195dd79efb850b63d437aa610e6a9d96ed24484bb53789d1`, equal to `expected.json:12`. The frozen revision `679af5d749f2fd48b9d543e3c99d348d5458f90f` exists (`git cat-file -t`). Its strict run gives `CITATION_DRIFT_VERDICT: failed findings=36 exit=1`, consistent with `expected.json:4-10` (verdict failed, `citation_dead`).
6. **Unused pinned snapshot.** `expected.json:15-17` pins a digest for `config-toml-landmarks`, and no pointer-table entry references it (grep `config-toml`: 0). It is inert.
7. **Literal sentence conflict, flagged, not drafted.** The row's last sentence, "no line number into an operator-mutable file is pinned (rule #11)" (SKILL.md:448), conflicts with the table. `pointer-table.json` has 50 `"line"`-keyed entries (grep -c), 11 of them into `SCORECARD.md`, 4 into `SKILL.md`, 2 into `LOG.md`, plus others (python tally this round). The sentence needs narrowing, e.g. to "no line number is the frozen digest target", or rule #11 must define the term. I did not edit it; the L1 decides.
8. **`--rev` default `HEAD`.** `citation-drift-probe.py:477` defaults `--rev` to `HEAD`. The row always passes `--rev <REV>`, so it is not affected today. C2 changes this default.
9. **Probe-vs-strict semantics confirmed in code and run.** See the paragraph above the findings.

## Commands run (all read-only; none modifies LANE)

- `git rev-parse --verify refs/heads/main^{commit}`, `git rev-parse --verify HEAD^{commit}`, `git log --oneline -3 refs/heads/main`: `9011581…` on both.
- `git status --porcelain --untracked-files=no` (empty); `git diff --stat 9011581 -- SKILL.md .ufo/waves/round-17/tools .ufo/gates/citation-drift` (empty).
- `git show 9011581:<path> | sha256sum` vs `sha256sum <worktree path>` for the five tools (match).
- `python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root <LANE> --rev 9011581… --table … --expected …` → `reported findings=0 exit=0`; same with `--strict` → `clean findings=0 exit=0`.
- Same probe with `--rev 679af5d…` `--strict` → `failed findings=36 exit=1`.
- `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py /nonexistent/x` → exit 2 (`unreadable`).
- `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py /etc/hostname` → exit 0, `format: unrecognized`, `found: false`.
- `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py <(printf '\x7fELF…')` → exit 2, `malformed: not ELF`.
- `sha256sum ~/.local/opt/go-1.25.0/src/debug/buildinfo/buildinfo.go` and `wc -l` → `332fff28…f45`, 599.
- Grep and read passes over the five tool sources and the gate (no selftest run).

Not run: any `--selftest`, any REA or Ghidra command, any carrier execution, `jj`, any git write, any lane write.

## Installs and updates

None. I used `python3` (stdlib, already present), `git`, `sha256sum` and `wc`. No package was installed or upgraded.

## Limits

- Write scope and pins are read from code and checked with the read-only commands above. I did not exercise `pins snapshot` on a live path, so the `.tmp`/overwrite behaviour rests on reading lines 114-131.
- The `pinned values` claims are for the working-tree bytes at `9011581`, which equal the branch tip.
- Round-17 wording for `2 unreadable` in the registry rows is my reading of the code paths cited; the L1 owns the final text.
