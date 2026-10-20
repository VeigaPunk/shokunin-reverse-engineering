# Scout — `@<slug>` snapshot resolution vs `--snapshot-dir` and the `expected.json` digest check

Timestamp (clock at write): 2026-10-20T17:49:46-03:00. Read-only seat; no lane writes beyond this report.
Labels: **[obs]** executed/read here; **[inf]** inference or recommendation.

## 0. Evidence base

- Subject: `.ufo/gates/citation-drift/citation-drift-probe.py` (735 lines), `expected.json`, `pointer-table.json`.
- File identity **[obs]**: working-tree sha256 == blob at baseline `14f0260ad319ecc26994381b2415d5a999003375` == `7e3480241f28730e076b0ef424443885709190c90c18f4a609b4a0bc7d54e71c`.
  ```
  cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  git show 14f0260:.ufo/gates/citation-drift/citation-drift-probe.py | sha256sum
  7e3480…e71c  -                                                   # exit 0
  sha256sum .ufo/gates/citation-drift/citation-drift-probe.py
  7e3480…e71c  .ufo/gates/citation-drift/citation-drift-probe.py   # exit 0
  git rev-parse refs/heads/main
  d1d981d2cc041dda4656c5b01d2c8445d8d17124                        # exit 0 (tip, not the contract baseline)
  ```
- No tool installs were needed.

## 1. Resolution trace (all **[obs]** unless marked)

1. `Tree.lines` (citation-drift-probe.py:145-157): a target beginning with `@` takes the snapshot branch at :148 and calls `self._snapshot(target[1:])` at :149. The slug is everything after the first `@`, verbatim — no percent-decoding, no segment validation.
2. `_snapshot` (:159-185):
   - :161-167 absent `--snapshot-dir` → `pointer_table_unreadable` (CNE, exit 2), by design.
   - :168 `path = os.path.join(self.snapshot_dir, slug)` — **no `normpath`, no `realpath`, no containment test**. `os.path.join` also discards the base for an absolute slug.
   - :169 `os.path.isfile(path)` — follows symlinks.
   - :173 `data = open(path, "rb").read()`.
   - :174 `pinned = (self.expected.get("snapshots") or {}).get(slug)` — the pin is looked up by the **same raw, unchecked slug string**, not by a canonicalized path.
   - :175-179 no pin → `unpinned_legacy` (CNE).
   - :180-184 digest mismatch → `snapshot_tampered` (CNE).
   - :185 bytes are decoded and returned as `citing` lines, then graded by `check_entry` exactly like an in-repo file.
3. `extracted` entries that carry their own `rev` build a second `Tree` with the same `snapshot_dir` (:250-252), so the *cited* target (`entry["target"]`) takes the identical path. Cache key is the raw target string (:145-146,154-156), which is consistent but not a control.
4. The advertised contract in the module docstring (:30-32) is "`@<slug>` read from `--snapshot-dir`, after verifying its sha256 against expected.json `snapshots`". The path step (:168) does not support the "from `--snapshot-dir`" half.

## 2. Exact escape — table + expected pair

Scratch layout **[obs]**: `case/snap/` is `--snapshot-dir`; `case/secret.txt` sits one level above it. Both pins are computed from the bytes actually present, so the pair is self-consistent.

`table.json` (bytes hashed into `pointer_table.sha256` below):
```json
{"entries": [{"id": "esc-exact", "kind": "exact", "file": "@../secret.txt",
              "line": 1, "must_match": "SECRET_TOKEN="}]}
```
`expected.json`:
```json
{"snapshots": {"../secret.txt": "06df2aed9e1b3241536a9aff5b062e2351119b339300849cbb9b10bcdf72f688"},
 "pointer_table": {"sha256": "d2abce5646313e0beff8117d2f2b25ca6dbba03819531cd9623f8183f939d0b8"}}
```
Literal command and observed exit:
```
B=/tmp/kr20-slug-45ui_qdw/case
P=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py
python3 -I -B "$P" --root "$B/repo" --rev c0fcbe5a874fb7ea43e0fd7031ad392de8dda494 \
  --table "$B/table-pass-dotdot-pinned.json" --expected "$B/expected-pass-dotdot-pinned.json" \
  --snapshot-dir "$B/snap" --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0                         # exit=0
```
**[obs]** `@../secret.txt` was resolved to `<case>/secret.txt`, outside `--snapshot-dir`, and reported clean. No finding names the escape.

Variants, same harness (`python3 -I -B $P --root … --rev … --table … --expected … --snapshot-dir … --strict`) **[obs]**:

| variant | slug / pair | exit |
|---|---|---|
| relative `..` + pin | `@../secret.txt`, key `../secret.txt` | 0 clean |
| absolute slug | `@/tmp/…/case/secret.txt`, key `/tmp/…` (`os.path.join` drops the dir) | 0 clean |
| symlink in dir | `snap/link.txt -> case/secret.txt`, slug `link.txt`, pin `{"link.txt": sha256(secret)}` | 0 clean |
| host file | `@/etc/passwd` and `@../../../../etc/passwd`, pin `sha256(/etc/passwd)=60e21634…d83c`, `must_match ^root:` | 0 clean |
| no pin | same `@../secret.txt`, `snapshots: {}` | 2 `unpinned_legacy` |
| wrong pin | pin `0`*64 | 2 `snapshot_tampered` |
| in-snapshot control | `@external.cfg`, correct pin | 0 clean |

Content echo **[obs]**: an `extracted` entry whose citing target is also `@../secret.txt` (`line 2`, pattern `pointer (\d+)`) and whose `must_match` fails prints the escaped file's line into stdout:
```
CITATION_DRIFT: citation_dead entry=esc-leak @../secret.txt:2 cites @../secret.txt:1-1,
  which lacks 'NEVER_PRESENT' (holds 'SECRET_TOKEN=sk-live-DEADBEEFCAFE0123456789')
CITATION_DRIFT_VERDICT: failed findings=1 exit=1                        # exit=1 with --strict
```
Without `--strict` the identical row prints at exit 0 (the row loop at :446-455 prints every row regardless of verdict). The echoed text comes from :274 (`cited[lo - 1][:64]`), i.e. up to 64 chars of one line per extracted entry. `exact`/`quoted`/`anchor` findings print line numbers or the table's own pattern, not target content.

## 3. Does the digest check mitigate it?

**No for containment; yes only as a byte-substitution guard.** Per clause:

- **Pin lookup** (:174): the key is the raw slug, so an escaped spelling is pinnable by construction. The digest authenticates "whatever bytes this slug names on this host", including `/etc/passwd`. It makes an arbitrary host read *reproducible and pinned*, not contained. **[obs]** §2.
- **`unpinned_legacy`** (:175-179): this is the only brake. It stops an escaped slug that has no matching `snapshots` entry, so an *accidental* `..` in a table is loud (exit 2) **[obs]**. It does not stop a deliberate pair: table and expected are authored together and the pin is computed from the target file. Shape check, not authorization.
- **`snapshot_tampered`** (:180-184): binds bytes, not location. It makes a *mutable* host target brittle (`/etc/passwd` changing turns the run into CNE) **[obs]**, but stable out-of-dir files stay clean.
- **Frozen-run guard** (:413-430): `pointer_table.sha256` compares the table file on disk (:424) to a pin read from `expected.json` on disk (:413). Neither file is read as a Git object at `--rev`, and `expected.json` is not itself pinned, so `--rev 14f0260 …` does not attest the gate's own config **[obs from code]**. An author who ships escape + re-pin passes all preflight; the guard detects post-freeze drift, not an escape authored at freeze.
- **Grading**: an escaped file is graded like any snapshot, so a table entry can satisfy `must_match` from a host file and produce a *clean* attestation while no snapshot exists **[obs]** (§2, exit 0 with `/etc/passwd`).

Calibration on the echo channel **[inf]**: pinning requires knowing the target's digest. So the 64-char echo is not a privilege escalation against a file the pinner cannot read; it matters where author and runner differ (e.g. a root/CI runner executes a committed table and publishes the log to a wider audience) and the digest is obtainable independently. The load-bearing defect is the false containment contract and the attestation surface, not the echo alone.

## 4. Against the round-20 interface (D6c)

- Required at baseline: slug matches `^[A-Za-z0-9._-]+$`, contains no `..`, resolves inside `--snapshot-dir`, else exit 2 `slug_unsafe`; selftest case `slug_escape_refused`.
- Present at baseline **[obs]**: none of it. `grep -n "slug_unsafe\|realpath\|slug_escape" …probe.py` returns nothing; selftest snapshot cases are only `snapshot_missing`, `snapshot_tampered`, `no_snapshot_dir` (:570-578, fixture `@external.cfg` :568-578), so the escape has no red case today.
- Note the regex itself matches `..` (`[.]` is in the class); the separate "no `..`" clause is what rejects it. And `link.txt` passes both lexical clauses while escaping via symlink **[obs]** §2. Therefore "resolves inside `--snapshot-dir`" is the load-bearing clause and must use `os.path.realpath` + a `commonpath`/`relpath` boundary test — a `normpath`/`startswith` check leaves the symlink variant and `/snap` vs `/snap2` prefix confusion open **[inf]**. A useful selftest pair: one `..` case and one in-dir symlink case, both expecting `slug_unsafe`.

## 5. Coverage / remaining unknowns

- **Latent in the live table [obs]**: `.ufo/gates/citation-drift/pointer-table.json` has 60 `entries` (25 extracted / 20 exact / 15 anchor) and **zero** targets starting with `@`; `quoted` (5) and `exempt` (8) also have none. `expected.json.snapshots` pins one slug, `config-toml-landmarks`, that no entry references. So the escape is reachable by any table edit but not by the committed table as-is.
- **Wiring [obs]**: `grep -rn -i "citation.drift" --include=*.py --include=*.sh --include=Makefile .` outside `.ufo/waves/` and the gate dir printed no lines, so no Makefile/verify/CI script in the lane invokes the probe; runs are explicit-argv only. I did not inspect operator-side configs.
- **Not exercised [obs]**: Windows separators; NUL/long slugs; hardlinks; `--snapshot-dir` pointing at the repo root (E15.md:143 uses `.`, which makes every `..` target in-tree but still outside the stated dir contract). I did not enumerate which specific host secrets are readable by the invoking user beyond the temp fixture and `/etc/passwd`.
- **Confidence**: high on the mechanism and exits (read at the cited lines, reproduced across 9 runs). Medium on real-world harm ranking, which depends on who runs the gate and where its stdout goes **[inf]**.
