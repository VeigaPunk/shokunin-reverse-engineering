# ScribeKnowledge — round 94, seat ScribeKnowledge (scribe)

Seat directory: `.ufo/waves/round-94/w1/ScribeKnowledge/`
Scratch: `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r94/ScribeKnowledge` (deleted before yield)
Lane repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` — READ-ONLY. No lane file was created,
edited or deleted; every draft was written into the seat directory only.

## Deliverables

| file | what it is |
|---|---|
| `.ufo/waves/round-94/w1/ScribeKnowledge/knowledge.md` | draft of `corpus/knowledge/2026-11-05-r94-receipt-path-json.md` |
| `.ufo/waves/round-94/w1/ScribeKnowledge/s319-row.md` | the single S319 registry row for `corpus/SOURCES.md` |
| `.ufo/waves/round-94/w1/ScribeKnowledge/lesson-sections.md` | draft sections `## Gate`, `## Mistakes`, `## Census` for `corpus/lessons/round-94.md` |
| `.ufo/waves/round-94/w1/ScribeKnowledge/verify.txt` | census command, exit codes, S319 row verdict |
| `.ufo/waves/round-94/w1/ScribeKnowledge.md` | this report |

## Drafts

### 1. `knowledge.md` → `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`

Opens with the provenance trio as its first three lines: `source:` (S319, the URL
`https://docs.python.org/3/library/json.html`, anchor `#json.dump`, docs page sha256
`8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0`), `verified-at:` (2026-11-05
and base `8a40ceb6516bb38c19c37bcbff2bb3332f31c832`), `recheck:` (on-release, or 90d).

53 lines total. **Lines 1–12 carry every claim the craft Refs span cites**, so a
`corpus/knowledge/2026-11-05-r94-receipt-path-json.md:1-12` citation resolves and is
self-contained:

- L4 the documented sentence, verbatim: *"It should return a JSON encodable version of the object or raise a TypeError."*
- L6 `json.dump` raises `TypeError: Object of type bytes is not JSON serializable` for a bytes value
- L7 the round-93 counter stored the raw output bytes in `fresh_cells[*].output` and wrote its receipt with `json.dump`
- L8–L10 the three evidence pointers (`.ufo/waves/round-93/l1/scores/c1-pos-json-stderr-at-ca5aa6a2.txt`; `.ufo/waves/round-94/pre/c1-base-v3-pos.stderr` / `.stdout` / `.rc`; `.ufo/waves/round-94/pre/c1-base-v3-agreement.json` valid 2 of 4)
- L11–L12 the v4 fix (bytes become a length and a sha256; `<json-out>.tmp` renamed only on success) with its evidence paths `.ufo/waves/round-94/l1/scores/c1-v4-{pos,F1,F2,F3}.json` and `c1-v4-agreement.json`

Body sections after L12: the full documented statement; the behaviour measured on this host; the
successor writer; **Calibration: what the sentence does not say**; **What this entry does not
claim**. One claim per sentence. **No pipe character anywhere** (`grep -c '|' knowledge.md` → 0).
No credential material.

### 2. `s319-row.md` → one row appended to `corpus/SOURCES.md`'s Registry table

```
| S319 | Python json module documentation — https://docs.python.org/3/library/json.html | docs | A | json.dump default-hook behaviour on Python 3.14 | json.dump section #json.dump, docs page sha256 8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0, accessed 2026-11-05 | the default hook must return a JSON-encodable value or raise TypeError, so a receipt writer must encode bytes itself | mined | 2026-11-05 | on-release | corpus/knowledge/2026-11-05-r94-receipt-path-json.md, corpus/lessons/round-94.md |
```

11 cells exactly (13 pipe-delimited fields, 12 pipe characters, no pipe inside any cell). All
11 values are as specified; the `teaches` cell paraphrases rather than quotes so that no pipe
character can appear in a cell — the verbatim quote is carried in the knowledge entry and in the
lesson's Gate table instead.

### 3. `lesson-sections.md` → sections of `corpus/lessons/round-94.md`

- **`## Gate`** — the table (row · URL · access date 2026-11-05 · HTTP/bytes/sha256 · located
  quote · used for) with S319 as the only row; Row-changes old→new (S319 appended, no other
  registry row edited); and the Admit/Reject line: **admitted this round: S319 only**; the
  rejected item is the docs sentence about `TypeError` in the *example* `default()` function —
  the `# Let the base class default method raise the TypeError` comment and the subclass
  sentence "Implement this method in a subclass such that it returns a serializable object for
  o, or calls the base implementation (to raise a TypeError)" — **not admitted, because it is
  an example and an encoder-subclass method, not the `json.dump` parameter contract**.
- **`## Mistakes`** — three rows in the required `class · evidence pointer · captured-by · fix`
  form: **M94-a** (a frozen counter's receipt writer crashes on the honest case; evidence
  `.ufo/waves/round-94/pre/c1-base-v3-pos.stderr`; captured-by `none`; fix: v4 receipt writer +
  `c1-receipt-agreement` counter on the public command), **M94-b** (a truncated receipt read as
  evidence; D-93-D; evidence `.ufo/waves/round-93/l1/scores/c1-pos-json-at-ca5aa6a2.json`;
  captured-by `none`; fix: atomic write via `<path>.tmp` rename), **M94-c** (the counter's own
  selftest never exercised the public `--json-out` path; evidence `.ufo/waves/round-93/l1/scores/c1-v4`
  absent and `.ufo/waves/round-94/pre/c1-v4-selftest.txt`; captured-by `none`; fix: the C1
  counting command runs the public CLI).
- **`## Census`** — `Before: exit 0 (.ufo/waves/round-94/census-before.txt)` and
  `After: (filled at landing)`.
- `## Measured` is left as a placeholder for the L1.

Every file cited by the lesson sections exists at `dd4524916a0332bb65f83525532da1c1b8d709de`
or is created by this round; the check is in the verification log below.

## Census command, exit code, S319 row verdict

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$S/fleet" kaidoku
```

The literal `--root "$S/clone" kaidoku` form cannot work: the clone is a lane repository, not a
fleet root, so the script exits **2** with `ERROR: config not found: $S/clone/shokunin.conf` and
`ERROR: unknown lane (not a dir, not in conf or root): kaidoku`. The scratch fleet root
`$S/fleet` supplies exactly what the script needs and points at the clone
(`$S/fleet/kaidoku-shokunin` → symlink → `$S/clone`), so the registry read is still
`$S/clone/corpus/SOURCES.md`.

- **Run A** (S319 row appended, landing files absent): **exit 1** — `W04 S319 duplicate url
  docs.python.org/3/library/json.html across scopes`, `E11 S319 missing used-by
  corpus/knowledge/2026-11-05-r94-receipt-path-json.md`, `E11 S319 missing used-by
  corpus/lessons/round-94.md`. The two E11s are expected at this stage (both used-by targets are
  this round's landing candidates).
- **Run B** (S319 row appended, landing files present): **exit 0** — `W04 S319 …` plus
  `kaidoku ok $S/fleet/kaidoku-shokunin/corpus/SOURCES.md`; 33 output lines.

**S319 row verdict: PASS on every error code.** No E01–E12 is raised for S319 in run B. The only
finding is **W04**, a warning the census header defines as not affecting a clean lane's status.
W04 is expected here: the URL is already used by **S050** under a different scope; S319's scope
(the `json.dump` default-hook contract) is a materially distinct proposition from S050's
duplicate-name and non-finite-number decoder behaviour, and it carries its own locator. The
census raises **E04** only when two rows share both URL *and* scope; the scopes differ, so E04
correctly does not fire. Recorded either way, as instructed.

## Supporting verification (all run by this seat)

| check | command | result |
|---|---|---|
| clone pinned | `git -C "$S/clone" rev-parse HEAD` | `dd4524916a0332bb65f83525532da1c1b8d709de` |
| clone toplevel asserted | `git -C "$S/clone" rev-parse --show-toplevel` | `$S/clone` |
| source fetch | `curl -sSL -w 'HTTP %{http_code} size %{size_download}\n' -o json.html https://docs.python.org/3/library/json.html` | `HTTP 200 size 116296` |
| source digest | `sha256sum json.html` | `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0` (matches the frozen pin) |
| second fetch | same curl again + `cmp` | byte-identical |
| quote occurrences | tag-strip + whitespace-normalise, `/3/`, `3.13`, `3.14`, `3.15` pages | 2 on each page; not a raw contiguous HTML substring |
| page version label | `<title>` of `/3/` | "Python 3.15.2 documentation"; host interpreter is Python 3.14.8 |
| stdlib behaviour | `json.dump({"x": object()}, io.StringIO())` | `TypeError: Object of type bytes is not JSON serializable` |
| calibration: `str()` fallback | `json.dump(..., default=lambda o: str(o))` | exits 0 — the fallback the successor refuses would succeed |
| calibration: bytes hook | `json.dump(..., default=lambda o: b"x")` | `ValueError: Circular reference detected`, not `TypeError` |
| v3 has no selftest | `grep -c selftest tools/round-93/stop-boundary-repair-battery-v3.py` | `0` |
| base receipts truncated | `json.load` on `pre/c1-base-v3-pos.json` and `pre/c1-base-v3-F3.json` | both fail to parse (char 706 and char 703) |
| v4 receipt shape | `jq`-equivalent read of `.ufo/waves/round-94/l1/scores/c1-v4-pos.json` | `fresh_cells[*].output` = `{"bytes": 34432, "sha256": "3b3bf4e6…"}` — the "length and a sha256" claim |
| cited files exist | `git cat-file -e dd4524916…:<path>` for every path cited in the lesson | all present, except the two landing candidates (`corpus/knowledge/2026-11-05-r94-receipt-path-json.md`, `corpus/lessons/round-94.md`) and `.ufo/waves/round-94/census-before.txt`, which are created by this round, and `.ufo/waves/round-93/l1/scores/c1-v4`, which is cited **as an absence** |

### Reachability probes (in the scratch clone only — the L1 lands the real bytes)

These are not the claim's measurement; they show the drafts are compatible with the frozen
counters so the L1 does not land a candidate that cannot pass.

- With the drafted knowledge entry copied to `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`
  in the clone, a plausible block 33 citing it as `:1-12` resolves:
  `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --worktree --expect-blocks 33` →
  `blocks 33 resolved 33 expect 33 unresolved 0 met=True exit=0` (exit 0);
  `python3 -I -B tools/round-91/depth-blocks-v3.py --root . --worktree --expect-blocks 33 --shape-from 33`
  → `blocks 33, resolved 33, required-shaped 1/1 … met=True exit=0` (exit 0).
- With QUALITY rows 189/190 carrying the frozen keyword atoms and a block 33 whose three rows
  cite them: `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest
  .ufo/waves/round-94/manifests/block33-after.json --block 33 --worktree --json-out …` →
  `ok exit 0`, `failing: []`, all three rows `missing_keywords: []`, `atoms: block_present/marker/shape
  all true`.

## Findings and named limits for the L1

1. **The documented sentence is a requirement on the hook author, not an stdlib prohibition.**
   Measured: a `str()` fallback makes `json.dump` exit 0, and a hook returning `bytes` yields
   `ValueError: Circular reference detected`, not `TypeError`. The knowledge entry states the
   sentence as the contract the successor *adopts and enforces on itself*. The S319 `teaches`
   cell is worded accordingly ("so a receipt writer must encode bytes itself"), not as a claim
   about the stdlib's behaviour.
2. **The quote occurs twice on the page** — `#json.dump` (heading "Basic Usage", the `default`
   parameter bullet) and `#json.JSONEncoder` (heading "Encoders and Decoders"). It is **not**
   under `#json.dumps`. It is not a raw contiguous HTML substring. The row is anchored to
   `#json.dump`; the lesson Gate section records both occurrences.
3. **Version label.** The `/3/` alias serves "Python 3.15.2 documentation" while the host
   interpreter is Python 3.14.8; the sentence is byte-identical in the pinned 3.13/3.14/3.15
   pages (2 occurrences each), so the gap does not affect the proposition. The row's scope says
   "on Python 3.14" as specified; the version-label nuance is recorded in the knowledge entry
   and the Gate section rather than changing the frozen cell.
4. **S050 overlap.** The URL is already in the registry under S050 with a different scope, so
   W04 is expected. S319 is scoped as the `json.dump` default-hook contract — a materially
   distinct proposition with its own locator — following the lane's S300/S303 precedent. No
   other registry row is edited this round, so S050's `used-by` is not extended.
5. **`c1-v4` at round 93 is an absence, cited as such** in M94-c. `ls .ufo/waves/round-93/l1/scores/ | grep c1-v4`
   returns nothing, confirming the successor did not exist at round 93.
6. **The v3 counter has no `--selftest` at all** (`grep -c selftest` → 0); the helper-only
   selftest is the v4's, with three cases (`.ufo/waves/round-94/pre/c1-v4-selftest.txt`,
   `SELFTEST cases=3 failures=0`). M94-c is worded to state that the *public* path was never
   exercised, which is true for both counters.
7. **Tooling:** no package was installed, upgraded or removed. Every command ran on the host's
   existing `git`, `curl`, `python3` (3.14.8), `grep`, `cmp`, `sha256sum` and the fleet's
   `scripts/sources-census.sh`. No pacman transaction was attempted (host-wide pause honoured).
   No host state was mutated.

## Out of scope for this seat

The L1 lands the candidate bytes: `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`, the
S319 row in `corpus/SOURCES.md`, the QUALITY rows 189/190, craft block 33 and the
`corpus/lessons/round-94.md` sections, and re-measures both claims at the landing commit. This
seat wrote drafts only and touched no lane file.
