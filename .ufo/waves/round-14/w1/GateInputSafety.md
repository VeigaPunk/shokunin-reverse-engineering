# GateInputSafety — C2 quote-fidelity manifest contract: read-only guarantee and unsafe operations

Seat: `KaidokuR14.GateInputSafety` (sentinel, leaf). Wave `kaidoku-r14-w1`. Accessed 2026-10-20 (UTC 05:16, HEAD `767adaf`).
Axes: **calibration** (no false exit-1 or false clean caused by input handling) and **coverage** (every input path the contract admits is named). No harm: read-only review. No code was edited, no test/selftest/gate was run, and nothing was installed.

## Scope and calibration statement

- `.ufo/waves/round-14/tools/quote-fidelity.py` **did not exist** when I last listed `.ufo/waves/round-14/**`. So every finding below is about the **contract text** in `spec.json` `context` "Gate interface" and about the existing gate conventions. None of it describes behaviour of the gate code. Each finding is a risk that an implementation can introduce or rule out. None is an observed defect.
- The language-semantics claims (F1, F2, F3, F7) come from one-line `python3 -I -c` probes of stdlib behaviour on Python 3.14.7. I did not run the gate, its selftest, or any fixture.
- Out of scope (left to sibling seats): heading or substring semantics, same-heading ambiguity, and how whitespace-word counting interacts with Unicode. These belong to ReviewQuoteContract and AttackQuoteGate. I propose no new finding IDs and no new validation classes. Each recommendation reuses `invalid_manifest` or `source_tampered`, with one optional exception in F3.

## Existing gate conventions (evidence)

| Convention | Location | Quote (≤25 words) |
|---|---|---|
| Read-only normal entry | `.ufo/gates/custody-pair/custody-pair.py:13-14` | "The instrument is READ-ONLY over every path it inspects: it opens files for reading only (sha256), never for writing, never renames, never touches mtime." |
| Guards are self-harm guards only | `custody-pair.py:56-57` | "this remains a self-harm guard, not a security boundary" |
| Scratch excludes `/tmp` | `custody-pair.py:665` | "/tmp is excluded (EDQUOT hazard)" |
| Read once, then hash | `custody-pair.py:249-254` | `sha256_file` streams `open(path, "rb")`; `capture_path` uses `os.lstat` and `os.path.isfile` (lines 285, 309) |
| Selftest isolation | `.ufo/gates/citation-drift/citation-drift-probe.py:338` | "self-test: isolated fixture trees, no network, no live-tree write" |
| CNE wins over failed | `citation-drift-probe.py:80-85` | `verdict()` returns `CNE` whenever any tamper/unreadable/`internal_error` finding is present |
| Crash is CNE, not exit 1 | `citation-drift-probe.py:491-493` | `except Exception` → `findings.add("internal_error", ...)` (graded CNE at line 83) |
| Snapshot path join (unconfined) | `citation-drift-probe.py:148` | `path = os.path.join(self.snapshot_dir, slug)` |
| Frozen input pinned outside the input | `.ufo/gates/citation-drift/expected.json:13` | "sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered" |
| Registry write-scope column | `SKILL.md:448` | "normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos" |
| Round contract | `.ufo/waves/round-14/spec.json:3` | "No networking in gate." / "No live artifact mutation." |

Only `subprocess` argv lists appear in the existing gates (`citation-drift-probe.py:102,265,350,366`; `custody-pair.py:1233`). I found no `shell=True`, `os.system`, `eval(`, `exec(`, `pickle`, or `yaml.load` in `.ufo/gates/` (grep, 2026-10-20). The quote gate needs no subprocess at all. Citation-drift needs one because it calls `git show`.

## Findings

### F1 — HIGH (calibration and read scope): a manifest path can leave the manifest directory
- **Exploit path.** The contract says "paths relative to manifest directory". The natural implementation is `os.path.join(manifest_dir, path)` or `Path(manifest_dir) / path`, and both discard the base when `path` is absolute. Probe: `os.path.join('/m/fixtures','/etc/passwd')` → `/etc/passwd`, and `pathlib` behaves the same. A path such as `../../corpus/SOURCES.md` normalizes out of the fixture tree. A symlink inside `fixtures/` does the same.
- **Impact.** The manifest's own `sha256` vouches for whatever file it names (see F4), so a manifest can grade quotes against a live corpus file or any readable file and still report `clean`. That breaks the "local captured source excerpts only" limit in `claims.json` C2. It also breaks the "frozen inputs" premise of the L1 frozen run. If findings echo source text, it is a read-disclosure path as well. It cannot write anything.
- **Existing precedent.** Citation-drift has the same unconfined join (`:148`), but its digest pin lives in a separate `expected.json`.
- **Smallest remediation.**
  1. Reject an absolute `path`.
  2. Compute `real = os.path.realpath(os.path.join(manifest_dir_real, path))` and require `os.path.commonpath([real, manifest_dir_real]) == manifest_dir_real`.
  3. Report anything else as `invalid_manifest` (exit 2).
- This is a self-harm guard. TOCTOU stays out of scope, in the same terms as `custody-pair.py:56-57`.

### F2 — MEDIUM (calibration): duplicate JSON keys in `sources` are silently last-wins
- **Exploit path.** Probe: `json.loads('{"sources":{"S017":{"path":"a"},"S017":{"path":"b"}}}')` → `{'S017': {'path': 'b'}}`. A reader of the manifest sees the first S017 entry (the pinned correct excerpt), but the gate grades against the second. The QuoteGateCode brief makes duplicate *quote* IDs invalid. Duplicate *source-map keys* cannot be seen after `json.load`.
- **Remediation.** Use `json.load(fh, object_pairs_hook=...)` with a hook that raises on any repeated key at any level. Report it as `invalid_manifest`. This is the same class as the existing duplicate-ID rule, not new scope.

### F3 — MEDIUM (calibration): an uncaught exception exits 1, which collides with "failed"
- **Exploit path.** Probe: `python3 -c "1/0"` → exit 1. Any traceback in the gate becomes a red "failed" verdict, for example from `UnicodeDecodeError` on a non-UTF-8 source, `IsADirectoryError`, `PermissionError`, `KeyError` on a missing field, or `TypeError` when `quotes` is not a list. A red-before fixture would then "pass" for the wrong reason. Argparse usage errors already exit 2, which is the correct CNE.
- **Remediation.**
  1. Wrap every input read and decode in `except (OSError, UnicodeDecodeError, ValueError)` and report `invalid_manifest`.
  2. Add one top-level `except Exception` → exit 2, following citation-drift `:491-493`.
  3. The finding ID for that catch-all is an L1 decision: reuse `invalid_manifest`, or add `internal_error` (precedent: `citation-drift-probe.py:83`). Either way it must never be 1.

### F4 — MEDIUM (calibration of the tamper claim): the source `sha256` is self-attested by the manifest
- **Exploit path.** `sources.{id}.sha256` sits in the same file as the `path` it vouches for. `source_tampered` therefore proves only that the source and the manifest are mutually consistent. A coordinated rewrite of excerpt plus manifest still reads clean. Citation-drift avoids this by pinning the table digest in a separate `expected.json` (`expected.json:11-14`). The C2 gate interface takes no `--expected`.
- **Remediation, with no gate scope expansion.**
  - L1's frozen run must check digests **outside the gate** first: `sha256sum -c` over the gate script, every manifest, and every source excerpt, against the values in the fixture producer's `expected.json`. Only then should it run the gate.
  - The fixture producer's "every input SHA256" must explicitly include the **manifest files themselves**, not only the excerpts.
  - Wording: the SKILL row should describe `source_tampered` as "excerpt bytes differ from the manifest pin". It should not say "source authenticity verified".

### F5 — LOW (availability and calibration): non-regular files, and hash/read being separate operations
- **Exploit path.**
  - A `path` that resolves to a FIFO, `/dev/zero`, `/dev/stdin`, or a directory either hangs or reads without bound.
  - Hashing in one `open()` and parsing in a second `open()` lets the two reads see different bytes. The same happens with `Path.read_text`, which may also apply universal-newline translation and then disagree with the bytes that were hashed.
- **Remediation.**
  1. Open each input exactly once in `"rb"`.
  2. Check `stat.S_ISREG(os.fstat(fd).st_mode)`; anything else is `invalid_manifest`.
  3. Read the bytes, hash *those bytes*, then `bytes.decode("utf-8")` strictly from the same buffer.
  4. Run all digest checks before any quote is evaluated (QuoteGateCode brief).
  5. Give CNE precedence over failed, as in citation-drift `:80-85`, so a tampered source never yields mixed exit-1 findings.

### F6 — LOW (unsafe operations): no shell, no subprocess, no regex built from manifest text
- **Risk.**
  - `re.search(quote, text)` or `re.compile(section)` turns `.`, `*`, `(` and similar characters in a quote into metacharacters. That can produce a **false clean** (`.` matches a spliced character), and it opens ReDoS on crafted input.
  - Any subprocess adds a shell or argv surface that the gate does not need.
- **Remediation.**
  - Section match: compare the heading line exactly with `==`.
  - Quote containment: plain `quote in section_text`.
  - Heading detection may use a fixed literal pattern such as `^#{1,6} `.
  - The gate needs only `argparse, hashlib, json, os, stat, sys, tempfile`. It should not import `subprocess`, `socket`, `urllib`, `http`, `shutil.rmtree` over computed paths, `pickle`, `eval`, or `exec`.
  - After integration, L1 can confirm "no networking" and "no shell" statically with a grep over these imports. That is a source read, not a test run.

### F7 — LOW (accidental writes): write scope of normal entry and selftest
- **Normal entry.**
  - It must open nothing for writing and print only to stdout/stderr, with no log, receipt, or cache file.
  - The single-file layout matters. A hyphenated script is never imported, so no `.pyc` is written for it. If the code producer splits logic into an importable helper module in `tools/`, every run writes `tools/__pycache__/`. That is covered by `.gitignore:1 __pycache__/` (checked with `git check-ignore`), but it is still a working-tree write during a "no live artifact mutation" run.
  - Keep the gate in one file, or invoke it with `-B`.
- **Selftest.**
  - Write fixtures only inside `with tempfile.TemporaryDirectory(...)`, which cleans up on exception. Never write into `fixtures/`, `tools/`, the manifest directory, or the repo.
  - `TemporaryDirectory` cleanup does not run on SIGKILL. An in-repo fixture directory would then surface in `git status`. `fixtures/` is *not* git-ignored (`git check-ignore` matched nothing for `.ufo/waves/round-14/fixtures/x.md`), so it could get committed. Out-of-repo scratch avoids this.
  - `TMPDIR` is unset on this host, so default `tempfile` uses `/tmp`. `/tmp` is tmpfs mounted with `usrquota` (`findmnt`), and custody-pair documents an EDQUOT hazard there.
    - The live quota could not be measured: `quota` is not installed, and I did not install it because it is not needed for this review.
    - Either follow custody-pair's order (`/dev/shm` then `/var/tmp`, `custody-pair.py:659-665`), or accept `/tmp` and record that choice. Both are cheap. The point is that the choice is explicit.
  - If the selftest re-invokes the gate for each case, as the interactive-r1 convention does in `SKILL.md:447`, use `subprocess.run([sys.executable, "-I", __file__, "--manifest", p])` as an argv list with no shell. That is the only acceptable subprocess.
- **Atime.** Reads can move atime on relatime mounts. That is not a content mutation, and custody-pair deliberately ignores atime for this reason (`custody-pair.py:101-103`).

### F8 — LOW (interpreter hygiene): script-directory shadowing
- **Exploit path.** `python3 /abs/tools/quote-fidelity.py` puts `tools/` first on `sys.path`. A `json.py` or `hashlib.py` placed in `tools/` would then run on L1's frozen run.
- **Remediation.**
  - Probe: `python3 -I` on 3.14.7 gives `isolated=1 safe_path=True ignore_environment=1 no_user_site=1`, which also neutralizes `PYTHONPATH` and the user site.
  - L1 may register the command as `python3 -I .../quote-fidelity.py --manifest PATH`.
  - The existing gates are registered without `-I`, so this is optional hardening and not a defect against convention.

### F9 — LOW (output safety)
- Findings should print the stable ID, the quote `id`, and the source `id`. Print manifest-supplied strings through `ascii()` or `repr()` so terminal control sequences in a crafted quote or section cannot reach the terminal.
- Do not echo source bytes beyond the quote already in the manifest. This keeps the F1 read-disclosure surface closed even if confinement regresses.

## Minimal path-handling recipe (recommended; not implemented by this seat)

```
manifest_real = realpath(args.manifest); must be a regular file (fstat after open "rb") else invalid_manifest
base = dirname(manifest_real)
for each source: reject isabs(path) or non-str; real = realpath(join(base, path))
  commonpath([real, base]) != base -> invalid_manifest
  fd = open(real, "rb"); S_ISREG(fstat) else invalid_manifest; data = read(); close
  sha256 is 64-hex string else invalid_manifest; hexdigest(data) != pin.lower() -> source_tampered
  text = data.decode("utf-8") (strict) else invalid_manifest
all digests checked before any quote; any CNE finding -> exit 2 over 1
no subprocess / shell / network / regex-from-input; stdout only
```

## Severity summary

| ID | Severity | Axis | One-line remediation |
|---|---|---|---|
| F1 | High | calibration | Reject absolute paths; confine via `realpath` and `commonpath` → `invalid_manifest` |
| F2 | Medium | calibration | `object_pairs_hook` rejecting duplicate keys → `invalid_manifest` |
| F3 | Medium | calibration | Catch input errors and crashes → exit 2, never 1 |
| F4 | Medium | calibration | L1 runs `sha256sum -c` (manifests included) before the gate; reword the tamper claim |
| F5 | Low | coverage | One read, `S_ISREG`, hash and decode from the same bytes |
| F6 | Low | calibration | `==` heading match, `in` substring match, no subprocess |
| F7 | Low | no-harm | No writes in normal entry; selftest only in an out-of-repo `TemporaryDirectory`; single file or `-B` |
| F8 | Low | no-harm | Optional `python3 -I` in the registered command |
| F9 | Low | no-harm | `ascii()` on echoed strings; never echo source bytes |

## Checks for L1 after integration (none run by this seat)
1. Grep `tools/quote-fidelity.py` for `subprocess|socket|urllib|http|eval\(|exec\(|shell=True|open\([^)]*['"]w`. The only hit allowed is the selftest's own fixture writes inside `TemporaryDirectory`.
2. Selftest cases worth pinning, if L1 judges them in scope:
   - an absolute path → 2 `invalid_manifest`
   - a `../` escape → 2 `invalid_manifest`
   - a duplicate `sources` key → 2 `invalid_manifest`
   - a non-UTF-8 source → 2 (not 1)
3. Run `git status --short` before and after both `--manifest` and `--selftest` runs. The output should be identical.
4. Run `sha256sum -c` on the pinned inputs, manifests included, before the frozen run.

## Sources opened (all local, accessed 2026-10-20)
- `kaidoku-shokunin/.ufo/waves/round-14/spec.json:3` (context, gate interface), and items QuoteGateCode, QuoteSourceFixtures, ReviewQuoteContract, AttackQuoteGate, GateInputSafety (targets only).
- `kaidoku-shokunin/.ufo/waves/round-14/claims.json:20-26` (C2 limits: "local captured source excerpts only; no whole-registry or semantic truth assertion").
- `kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py:1-173,270-499`; `.../citation-drift/expected.json:1-85`.
- `kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py:2-188,248-323,654-743`.
- `kaidoku-shokunin/.ufo/gates/c1-census-v10.py` (grep only: `os.path.join` read paths at `:476-482,643`).
- `kaidoku-shokunin/SKILL.md:445-449` (gate registry rows).
- `kaidoku-shokunin/.ufo/waves/round-14/measure.py:1-33`: L1 counts C2 by the presence of `tools/quote-fidelity.py` in Git objects. That is read-only and writes nothing.
- `kaidoku-shokunin/corpus/lessons/round-13-verifier-spotcheck.md:13`: "Review found S017's spliced quotation and S018's mislocated exact quote."
- Host facts: `python3 --version` → 3.14.7; `df -h`/`findmnt` show `/tmp` as tmpfs with `usrquota`; `TMPDIR` unset; `quota` not installed; `git check-ignore` results as quoted in F7.

## Limitations
- The gate code was absent at review time, so these are contract and convention risks, not observed defects. A finding is retired only by reading the landed code.
- I did not measure the `/tmp` EDQUOT hazard live. The only evidence is custody-pair's documentation plus the `usrquota` mount option.
- I made no installs, and no RULES.md-governed action was taken.
- This seat is author-side and cannot provide non-author admission.
