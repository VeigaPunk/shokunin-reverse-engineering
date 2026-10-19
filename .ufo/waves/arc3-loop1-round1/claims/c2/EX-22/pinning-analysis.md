# EX-22 — pinning-correctness analysis: the citation-drift table pin

Seat EX-22 | chain c2 | executor | 2026-10-19 | HEAD `e845c2b`
Scope: the C2 claim's frozen-run guard — `expected.json` pinning the sha256 of
`pointer-table.json`. This artifact is analysis + patch text; **nothing was
applied** to `.ufo/gates/citation-drift/` (EX-16's target). All probing ran on
scratch copies under `/var/tmp/ex22` (see §10 note on `/tmp`).

Owner note: EX-16 owns the landing; EX-23's `guard-recipe.patch.md` is the
chain's reference recipe. The patch here is **EX-23's recipe + the
pinning-correctness hardening** that closes EX-23's own named residual #7
("the reference block hashes one read and the existing code re-reads the
file"), re-shaped to EX-23's conventions (`frozen_run.table_sha256`, cases
`table_tampered`/`table_absent`). §7 lists the exact divergences.

## 0. Verified context (read-only)

| fact | value | evidence |
|---|---|---|
| `pointer-table.json` on-disk sha256 | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` | `sha256sum`, `evidence/hashes.txt` |
| worktree bytes vs `HEAD` blob | byte-identical (same digest) | `git show HEAD:… \| sha256sum`, `evidence/hashes.txt` |
| table shape | 14 694 B, 331 lines, pure ASCII, LF, trailing `\n`, `entries` 31 / `quoted` 4 | §10 commands |
| table path is a regular file | `stat` → `regular file`, `nlink=1` | §10 |
| baseline probe at HEAD | selftest `11/11 exit=0`; live `findings=0 exit=0` | `evidence/pristine-selftest.txt`, `evidence/pristine-live.txt` |

Because the table is LF/ASCII today, the normalization and TOCTOU defects in
§1–§2 are **latent, not live** — they cost nothing to close now and cannot be
closed for free later (the pin's provenance is fixed at landing time).

## 1. TOCTOU between hashing the table and using it

**The two-read pattern is measurably racy.** A pin implemented as "read bytes →
hash → compare → *re-open* → parse" grades bytes it never hashed. Measured
(`evidence/pinning-experiments-output.txt`, E2):

- deterministic hook demo: `pin_ok=True parsed={'entries': [{'id': 'EVIL'}]}`;
- live race (a swapper thread alternating the file under the reader, 2 s):
  **50 000 iterations, 3 179 reads where the pin passed and the parsed table
  was the attacker's (6.4 %); single-read variant: 0.**

**EX-23's reference recipe has the same window in the worse direction:** it
parses first (`table = json.load(open(table_path))`, graded) and *then* hashes a
second read (`table_bytes = open(table_path,"rb").read()`). A swap between the
two makes the hash match while the graded entries are the other bytes. Their
`falsepositives.md` §5.7 names this as residual #7, "microsecond window, honest
operator threat model — recorded for the implementer". This seat weaponized it
and closes it.

**Fix (in the patch):** one `read_table_bytes()` call; the returned `bytes`
object is both hashed and parsed (`json.loads(data.decode("utf-8"))`). The
window does not exist by construction, and the patch *removes* a read rather
than adding one.

**Honest scope note:** the swapper thread is an adversarial construction. The
honest-operator argument for the fix is not likelihood but (a) the fix is free,
(b) the pin's whole purpose is to make the graded bytes the pinned bytes, and
(c) "hash A, use B" is the defect class the guard exists to prevent.

## 2. Newline/encoding normalization — hash the exact bytes read

Measured (`evidence/pinning-experiments-output.txt`, E1) on the same table in
LF and CRLF form:

| reading | digest |
|---|---|
| `sha256sum` of the CRLF file (on-disk bytes) | `1494ca7405e9d62e…` |
| binary read of the CRLF file | `1494ca7405e9d62e…` (agrees) |
| binary read of the LF file | `eb9689f4e89f0b8b…` |
| **text-mode read of the CRLF file** (`.read()` → re-encode) | **`eb9689f4e89f0b8b…`** |

The trap: Python text mode applies universal-newline translation, so a pin
measured text-mode on a CRLF file equals the binary digest of the LF file —
i.e. a newline rewrite of the table would pass a text-mode-measured pin. Both
`json.load(open(path))` (text) and `json.loads(bytes.decode())` parse the CRLF
file, so nothing else in the pipeline notices.

**Rule the patch fixes in place:** the pin is the digest of the **exact on-disk
bytes**, measured with `sha256sum` (the receipt tool), and the probe reads in
binary (`read_table_bytes`) and decodes explicitly (`utf-8`), never via locale
or text mode. Consequence, measured: a CRLF rewrite of the table with the LF
pin → `pointer_table_tampered` exit 2 (`evidence/matrix.txt`, `P-crlf-table`;
pristine probe: `findings=0 exit=0` — silent).

Encoding parity checks (E1): a UTF-8 BOM fails `json.load` and `json.loads`
alike (`JSONDecodeError`) — no behavior change; non-UTF-8 bytes → the patch's
digest check fires first → `pointer_table_tampered` (EX-23's C9 measured
`pointer_table_unreadable`; see §7).

## 3. Symlink / hardlink risk on the table path

**Symlink (measured, E3):** plain `open()` follows (`lstat` `S_ISLNK=True`,
`realpath` points outside the gates dir, content read through the link);
`os.open(…, O_NOFOLLOW)` refuses with `ELOOP` (errno 40). Under the reference
recipe a symlinked table is followed silently (and a same-bytes symlink passes).
The patch refuses symlinks → `pointer_table_unsafe` (CNE, exit 2).
A mid-run retarget of the symlink is defeated by the single-read fix (E3:
`pin_ok=True parsed={'entries': []}` — the parsed bytes are the hashed bytes).

**Hardlink (measured, E4):** `os.link` → same inode, `nlink=2`; a tamper through
the *other* name changes the digest, so the pin catches it
(`sha256(a)=ffada425…` ≠ pin), and git reports `M tbl.json` (content-level
detection). Hardlinks do **not** evade a content pin; the residual is
auditability (link identity/nlink is not checked), not integrity. No code
change proposed.

## 4. Non-regular files and torn reads

- **FIFO (measured, E5):** a blocking `open()` hangs — the pristine probe was
  killed at 2 s (`exit=124`, `evidence/matrix.txt` `B-fifo-table`); the patched
  probe refuses in <15 ms. `O_NONBLOCK` (a no-op on regular files, measured) +
  `fstat` `S_ISREG` is what makes the check reachable without hanging.
- **Directory (measured):** pristine `json.load` → `pointer_table_unreadable`
  (`[Errno 21]`); patched → `pointer_table_unreadable` with the refusal detail
  (census parity with EX-23's C8 kept, §7).
- **Torn/truncated read (E6):** JSON parse raises and the digest mismatches —
  both paths are CNE, never a silent pass.

## 5. The patch (text only — not applied)

- `patches/citation-drift-pinning.patch.md` — full text, both files.
- Raw diffs: `evidence/probe.repo.patch.diff` (159 lines, sha256
  `ea60e0bbb3680e2b…`), `evidence/expected.repo.patch.diff` (7 lines, sha256
  `50326b8505c3c74f…`).
- Scratch result: probe sha256 `93f2bead2ef20090…`, expected sha256
  `663be45d60c5d956…` (`evidence/hashes.txt`).
- `patch -p1 --dry-run` from a repo-shaped tree: **OK** for both files.
- Pin value to land: `frozen_run.table_sha256 =
  738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
  (re-measure if the table changes before landing; table edit + re-pin must be
  one commit).

## 6. Before → after measurement (relevant to C2's claim)

| check | pristine (HEAD `e845c2b`) | patched (scratch) | evidence |
|---|---|---|---|
| selftest | `cases=11 passed=11 exit=0` | `cases=13 passed=13 exit=0` | `pristine-selftest.txt`, `patched-selftest.txt` |
| clean tree, pinned expected | `findings=0 exit=0` | `findings=0 exit=0` | `matrix.txt` P-clean-tree |
| table tampered (valid empty table) | **`findings=0 exit=0` (silent pass)** | `exit=2 pointer_table_tampered` | `matrix.txt` P/B-tampered |
| table absent | `exit=2 pointer_table_unreadable` | `exit=2 pointer_table_unreadable` | `matrix.txt` |
| CRLF rewrite of the table | `findings=0 exit=0` (silent) | `exit=2 pointer_table_tampered` | `matrix.txt` P/B-crlf |
| symlinked table | `findings=0 exit=0` (follows) | `exit=2 pointer_table_unsafe` | `matrix.txt` P/B-symlink |
| FIFO table | `exit=124` (hung, killed) | `exit=2 pointer_table_unreadable` | `matrix.txt` P/B-fifo |
| expected.json absent | `exit=2` (1 finding) | `exit=2` (2 findings: unreadable + unpinned_legacy) | `matrix.txt` P-absent-expected; EX-23 C6 parity |
| unpinned expected (legacy) | n/a (no guard) | `exit=2 unpinned_legacy` (declared W2 class) | `matrix.txt` P-legacy-unpinned |
| honest edit + same-commit re-pin | n/a | `findings=0 exit=0` | `out-P-repin-coupled.txt` |
| honest edit, stale pin | `findings=0 exit=0` (silent) | `exit=2 pointer_table_tampered` | `out-P-repin-uncoupled.txt` |
| dir table (C8) / non-UTF8 (C9) | `unreadable` / `unreadable` | `unreadable` / `tampered` | `matrix-extra.txt` |

The pristine "tampered" row is the defect: a table with zero entries yields a
clean verdict, because nothing checks the table itself.

## 7. Divergences from EX-23's reference recipe (for EX-16's consolidation)

Adopted from EX-23: pin key `frozen_run.table_sha256`; cases `table_tampered` /
`table_absent`; `unpinned_legacy` for a missing pin; the two new selftest rows;
per-case fixture pinning.

| # | difference | effect |
|---|---|---|
| D1 | table read **once**, binary, hash == parse | closes residual #7; one read instead of two |
| D2 | `O_NOFOLLOW` + `O_NONBLOCK` + `fstat S_ISREG` | symlink → `pointer_table_unsafe`; FIFO no longer hangs |
| D3 | pin check runs **before** the JSON parse | non-UTF8 table with a mismatching pin → `pointer_table_tampered` (EX-23 C9 measured `pointer_table_unreadable`); both exit 2 |
| D4 | expected.json is read first, in binary, explicit utf-8 | ordering required by D1; C6 parity kept (2 findings) |
| D5 | `pointer_table_unsafe` added to the CNE tuple | new id, symlink-only; EX-16 may fold it to `pointer_table_unreadable` if zero new ids are preferred (then the symlink refusal stays, the id changes) |

EX-23's recipe §3 already says: "If EX-16 lands different ids or placement,
re-run `harness/census.py` and diff `census-results.json`" — D3 is the one row
that shifts (C9); everything else in their census keeps its measured id.

## 8. Residual risks (named, not weaponized)

1. **`expected.json` is unpinned (self-reference).** An actor who edits the
   table *and* re-pins can keep the probe green; the guard is drift/tamper
   detection, not authentication. Mitigation in scope: the pin and the table
   land in one commit, and the probe prints the table path it used. Optional
   strengthening (beyond the frozen claim's 13 cases — do not fold without
   amending): a selftest meta-assert that the live `expected.json` carries a
   64-hex pin, so a deleted pin fails the selftest even though a probe run
   treats it as `unpinned_legacy`.
2. **Hardlink identity** (§3): content is pinned, link identity is not.
3. **Worktree vs `--rev`.** The table is read from the worktree while citations
   are graded at `--rev`; a clean worktree at a pinned revision is assumed.
   This is pre-existing declared semantics (the table is the contract).
4. **The symlink refusal is a behavior change** vs the reference recipe
   (which follows). If EX-16 folds `pointer_table_unsafe` away (D5), the
   refusal class disappears from the census.

## 9. Attacks / refutations attempted, with verdicts

| attack | verdict |
|---|---|
| "The pin's hash/parse split is unobservable in practice" | **REFUTED** — 3 179/50 000 racy reads in 2 s; single-read 0 |
| "A text-mode pin is equivalent to a binary pin" | **REFUTED** — text hash of CRLF == binary hash of LF (`eb9689f4…`) |
| "A CRLF rewrite is content-preserving, so it should pass" | **UPHELD as a policy choice, rejected for the pin** — the pin binds bytes; the rewrite is `tampered` exit 2 |
| "A symlinked table with the committed bytes is harmless" | **PARTIALLY REFUTED** — content-equal is benign, but identity is unverifiable; refusal (exit 2) is the honest class |
| "A hardlink to the table evades the digest" | **REFUTED** — tamper through the other name changes the digest; git shows `M` |
| "The guard can be defeated by a FIFO/dir at the table path" | **CONFIRMED for pristine (hang, exit 124)**; REFUTED for the patched reader (typed CNE, no hang) |
| "The patch regresses the 11 existing selftest cases" | **REFUTED** — 13/13 exit 0 (per-case fixture pinning required, as EX-23's D2 predicted) |
| "The patch breaks the honest edit + re-pin workflow" | **REFUTED** — coupled re-pin `findings=0 exit=0` |

## 10. Reproduction

Scratch root `/var/tmp/ex22` (the wave's `/tmp` is quota-blocked — `dd` of one
1 KiB block fails with `EDQUOT`; the pristine probe runs also died at exit 120
from failed stdout flushes there, and `git init` in a `/tmp` tempdir fails, so
run the selftest with `TMPDIR=/var/tmp/ex22/tmp`):

```sh
python3 evidence/pinning_experiments.py                 # E1-E6, ~3 s
bash evidence/matrix.sh        # before/after matrix (writes out-*.txt)
bash evidence/matrix-extra.sh  # dir / non-UTF8 parity rows
python3 <patched-probe> --selftest --expected <patched-expected.json>
sha256sum .ufo/gates/citation-drift/pointer-table.json   # 738b3a56…
```

Probe runs use the real repo as read-only `--root` (`git show`/`rev-parse`
only); every table mutation in the matrix is a scratch fixture under
`/var/tmp/ex22/exp/`.
