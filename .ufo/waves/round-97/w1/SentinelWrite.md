# SentinelWrite — write-path security review, round-97 instruments at L

Seat: SentinelWrite (sentinel). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, revision
`867ed98d85f45a18265441c1760386ef353b3d43` (L). No REA call. No host/sysctl/pacman change; no tool
installed. Scratch `$HYAKU_SCRATCH/kaidoku-r97/SentinelWrite` (default `/fast/scratch/hyaku`), removed
on exit. Clone: `git clone --shared <lane> $S/clone` → `checkout --detach 867ed98`;
`rev-parse --show-toplevel` == `$S/clone`. Lane untouched: `git status --porcelain` in the clone
empty before/after, `diff -rq clone clone-snap-A` empty.

**Verdict:** the C1 counter (`stop-boundary-repair-battery-v7.py`) and C1 rule (`kill-rule-v3.py`)
have a **sound** receipt writer — every write I could steer stayed inside `--work` / `--json-out` /
the clone. One HIGH defect sits in the rule's **manifest handling**; the two C2 instruments carry a
**MED** write-escape the C1 writer already closed.

## Findings

**F1 — HIGH: hostile `mutants.json` steers a write outside `--work` (manifest field `file`).**
`kill-rule-v3.py:463-481` `build_copy()`: `rel = m["file"]` → `dst = os.path.join(d, rel)` with `d = work/mut-<name>`,
then `shutil.copyfile(os.path.join(root, rel), dst)`. `rel` is never normalised or confined, so `../` escapes the work
dir. Measured (`wp-manifest.py`, frozen L bytes): `rel="../../src.txt"` → copyfile src `<W>/R/src.txt` (exists), write
dst `<W>/src.txt`, `dst inside --work? False`, `build_copy ok=True`, `dst content='MARKER-X\nMARKER-B\n'` — a write
outside `--work` with manifest-chosen content (`find`/`replace` from the same file). `--mutants` is a caller argument,
so the blast radius is "whatever manifest the caller names". Remediation: reject `rel` that is absolute or contains
`..`; confine `dst` to `d` by `realpath`.

**F2 — MED: `c_bytes` append follows a tracked symlink out of the clone.** `kill-rule-v3.py:415` appends to
`os.path.join(clone, counter)` with `open(..., "a")`; a tracked path that is a symlink is materialised as a symlink in
the clone and the append follows it. Measured (`wp-tests.py` case 9, isolated repo with a symlinked tracked file):
`checkout_is_symlink=True outside_file_now=b'OUTSIDE\n\n# DIRTY-BYTES-FOR-BYTE-BINDING-...'` — the write landed
outside the clone. Latent in the real lane (that path is a regular file). Remediation: `os.open(..., os.O_NOFOLLOW)`
or assert `not os.path.islink()` before appending.

**F3 — MED: the round-97 C2 instruments follow a symlink at their `--json-out`.** `depth-blocks-v4.py:275,297` and
`craft-citation-v2.py:382` write the receipt with a plain `open(args.json_out, "w")` — no `mkstemp`/`os.replace`.
Measured (`wp-c2.py`, frozen L bytes, both exit 0): `depth-blocks-v4 rc=0 victim_intact=False victim_now=b'{\n
"blocks": 36, ...'`; `craft-citation-v2 rc=0 victim_intact=False victim_now=b'{\n "atoms": {"block_present": true,
...'`; `receipt_path_is_symlink=True` for both; contrast `battery-v7 write_receipt victim_intact=True
receipt_is_link=False`. This is the escape class the round-97 C1 writer closed (M95-i/M96-h); the C2 tools were never
migrated. Remediation: use the `mkstemp`+`os.replace`+dir-fsync writer.

**F4 — LOW: the rule's own green receipt omits the `ownrec` binding its label advertises.** `kill-rule-v3.py:795-812`
writes the receipt, re-reads it, and only re-writes **if** the re-read fails — so on the green path the published
receipt has **no `ownrec` key**, yet the label claims `ownrec 1 of 1`. Measured (`wp-jsonout.py` A): `on-disk receipt
has 'ownrec' key: False`. The L1's landing receipt agrees: `.ufo/waves/round-97/l1/scores/c1-at-867ed98….json` →
`ownrec present: False`, `met: True`. `M-r2` is killed precisely on `has_ownrec` being false, and the mutant removes
that same assignment — so the honest artifact and the killed mutant's artifact are indistinguishable on that field.
Remediation: write the `ownrec` block into the receipt before the final publish.

**F5 — LOW: `verify_own_receipt` does not bind counts to the frozen constants or recompute the label.**
`verify_own_receipt` (line 573) checks types, `world_revision` and `mutants_killed == mutants` self-consistency only.
Measured (`wp-jsonout.py` E, F): `E: red receipt (met_target False) -> verify_own_receipt ok=True` (a red receipt
"verifies"); `F: forged green receipt, counts 1 of 1, label 'mutants killed 99 of 99' -> ok=True, reasons=[]`. It
never compares counts to `TOTAL_MUTANTS=21` / `TOTAL_FORGERIES=17`. LOW because the rule builds the receipt itself.

**F6 — LOW: `--json-out` with a missing parent dir / a directory target raises instead of refusing.** `write_receipt`
calls `tempfile.mkstemp(dir=d, ...)`, `d` = the receipt's parent: missing parent → `FileNotFoundError`; directory
target → `IsADirectoryError`; both escape as tracebacks (`wp-jsonout.py` B, C). `main` guards `os.makedirs(--work)`
but not `--json-out`'s parent.

## Answers to the assigned questions

1. **Writes confined to `--work` / `--json-out`?** C1 counter and rule: yes, except F1 (manifest
   `file`) and latent F2. `blob_sha256` uses `git cat-file blob <rev>:<path>` via `subprocess.run`
   on a **list** — no shell; git itself refuses traversal: `fatal: '../../../../etc/hostname' is
   outside repository` (rc=128, `blob_sha256` → `None`).
2. **Planted symlink at the receipt path / `<path>.tmp` / in the receipt's directory?** C1
   `kill-rule-v3.write_receipt` and `battery-v7.write_receipt`: **the victim survives in every
   case.** At the receipt path `os.replace` replaces the link itself (`victim_intact=True`,
   `link_replaced=True`); at `<path>.tmp` the temp name is `mkstemp`-random so the planted link is
   never opened (`victim2_intact=True`); an attacker-named decoy in the directory survives
   untouched and the receipt lands. A symlinked *parent directory* does redirect the write (POSIX
   `openat` on the caller's own path — not a tool defect). The C2 tools fail all of these (F3).
3. **Does `c_bytes`' `git clone --shared` touch anything outside its work dir?** No: the clone is
   at `work/dirty-clone`; the source `.git` listing and `HEAD` mtime are **identical** before/after
   (`src_git_listing_same=True`, `head_mtime_same=True`); the clone writes an `alternates` pointer
   back at the source's objects (read-only). The *append* inside the clone is the F2 escape.
4. **Does `blob_sha256` pass a user-controlled string into a shell?** **No.** `subprocess.run` takes
   a list, no `shell=True`; grep for `shell=True|os.system|os.popen` over `tools/round-97/` and
   `tools/round-96/` returns nothing.
5. **Anything else a hostile receipt or manifest could drive?** F1, F2, F5. Also: the rule never
   verifies `mutants.json` against `.ufo/waves/round-97/pins.sha256` — it records `mutants_sha256`
   in the receipt but compares it to nothing.

## Reproduced commands (all run; exact exit codes)

| command | exit | verdict |
|---|---|---|
| `python3 -I -B tools/round-97/depth-blocks-v4.py --root <clone> --rev 867ed98… --expect-blocks 36 --shape-from 36 --expect 'blocks 36, resolved 36, required-shaped 1/1'` | 0 | `blocks 36, resolved 36, required-shaped 1/1` |
| `python3 -I -B wp-tests.py` (12 cases) | 0 | 11 pass, 1 fail (my own mis-asserted decoy check, not a tool defect) |
| `python3 -I -B wp-manifest.py` | 0 | hostile manifest `file` escapes `--work` |
| `python3 -I -B wp-jsonout.py` | 0 | ownrec omitted; forged/red receipts verify clean |
| `python3 -I -B wp-c2.py` | 0 | both C2 tools follow the receipt-path symlink; C1 writer does not |

Frozen command A (`kill-rule-v3.py --root . --work $S/workA --mutants .ufo/waves/round-97/mutants.json
--fixtures .ufo/waves/round-97/forgery --prefix forge --decl e859a88… --json-out $S/receipts/c1-A.json`)
was started in the clone and **did not complete** in my budget (see note). The L1's landing receipt
`.ufo/waves/round-97/l1/scores/c1-at-867ed98….json` reports the frozen label
`mutants killed 21 of 21; …; ownrec 1 of 1`, `met_target: True`, `exit: 0`.

**Note (host-load risk, not a write defect).** `M-r2` runs the mutated rule with `--mutants <same
manifest>`, and the mutated rule re-runs its own mutant arm — the `ownrun` subtree **recurses**.
Measured: my command-A run reached `ownrun` nesting depth **13** and **26 GB** of scratch before I
stopped it; the L1's own scratch `…/l1/c1-land/mut/M-r2/ownrun-w/mut/M-r2/ownrun-w/…` reaches depth
**26**. Each level clones the full working tree (`git clone --shared` ≈ 950 MB per clone). Nothing
escapes `--work` and the lane is untouched, but `/fast` free space went 300 G → ~133 G during the
wave with several seats running concurrently. I stopped my run and deleted `$S/workA`.

## Severity ranking

F1 **HIGH** (hostile manifest writes outside `--work`) · F2 MED (`c_bytes` symlink append) ·
F3 MED (C2 instruments follow a receipt symlink) · F4 LOW (green receipt omits `ownrec`) ·
F5 LOW (`verify_own_receipt` accepts unbound counts/label) · F6 LOW (`--json-out` bad target raises).

None of F1–F6 lets a hostile receipt produce a **green** verdict: F1/F2 need a hostile manifest or
tree, F3 corrupts a victim rather than the verdict, F4–F6 weaken binding evidence rather than the
exit code. Every rejection path (`byte-pin-not-bound`, `met-not-typed`, `counts-extra-key`,
`imported-pin-not-bound`) leaves the lane byte-identical: `git status --porcelain` empty and
`diff -rq clone clone-snap-A` empty after the full mutant run.
