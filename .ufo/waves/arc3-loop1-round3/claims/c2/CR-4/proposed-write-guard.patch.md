# CR-4 proposed changes — write-guard (arc3-loop1-round3, chain c2, critic seat)

Status: proposal only; this seat writes no tool code. Base revision tested:
`112d01dc…` (round-2 landed) plus reference variants built in scratch. The
round-3 landing by EX-21 was in churn while this seat measured; the landed
guard was re-tested at `dc841464…` (guard body diff-identical at `89bfebec…`,
selftest 21/21 CLEAN) — items 1, 5, 6 and 8 below are still open there; items 2
and 4 are closed by that landing (see the seat report's verdict table).

## 1. Guard the derived sidecar path too (new bypass, class VZ-4)

Evidence: `.ufo/waves/arc3-loop1-round3/claims/c2/CR-4/run-current.out` case T7.

```
--paths <scope>/vic.sha256 --out <scope>/vic     # exit 0
SIDECAR: <scope>/vic.sha256
victim-CLOBBERED
```

The guard examines `--out` only; `sidecar = out.with_name(out.name + ".sha256")`
is written unguarded, so a scoped file whose name is `<X>.sha256` is overwritten
by the receipt sidecar while `--out X` passes the guard. The literal extension
`out ∈ set(paths) ∪ CUSTODY_PATHS` does not close this (measured: ALLOWED on both
the current and L1 variants; REFUSED only on the fail-closed reference variant
which guards `(out, sidecar)`).

Patch shape (drop-in for the guarded block in `cmd_capture`):

```python
        candidate_paths = (out, out.with_name(out.name + ".sha256"))
        for cand in candidate_paths:
            if <guard-predicate>(cand, [*paths, *CUSTODY_PATHS]):
                print("USAGE: refusing to write a receipt over a guarded path: %s" % cand,
                      file=sys.stderr)
                return EXIT_USAGE
```

## 2. Keep inode identity in the guard (D7) — verify it landed

Evidence: case T1 (custom scope) and T9 (canonical `.bashrc`) — hardlink alias,
ALLOWED+CLOBBERED on the current and literal-extension variants.

The landed round-3 docstring declares the inode arm; the grounding check is that
the selftest gains a hardlink case, and that `_same_file` is fail-closed or at
least never *crashes* on a not-yet-existing `--out` (the ordinary case). The
landed `_same_file` returns False on OSError, so T13–T15 below must be exercised.

## 3. Proposed selftest cases (target: 15 → ≥18)

Fixture-level, no custody path touched (mirrors the existing case 12):

1. `refuses-hardlink-alias-of-scoped-path` — scratch `hl.conf` + hardlink
   `hl-alias.out`; `capture --out hl-alias.out --paths hl.conf` → exit 2, both
   files byte-identical before/after. (Cases T1/T9.)
2. `refuses-sidecar-path-of-scoped-file` — scratch `vic.sha256`; `capture
   --out vic --paths vic.sha256` → exit 2, `vic.sha256` unchanged. (Case T7.)
3. `allows-fresh-out-and-missing-scoped` — `capture --out new-receipt.txt
   --paths does-not-exist.conf` → exit 13 (ABSENT), receipt written, no
   traceback (regression guard for an inode arm calling `os.stat` on a
   nonexistent `--out`). (Cases T13–T15.)
4. (optional) `refuses-relative-spelling` — `cd` into the fixture dir,
   `capture --out ./x --paths x` with `x` scoped → exit 2. This is the half-fix
   trap: compare *resolved* forms on both sides, never
   `out.resolve() vs {Path(p).expanduser()}`.

## 4. TOCTOU — declare with the measured number (scope, not defect)

Evidence: `toctou-race.sh` against revision `68e30768…`: 300 attempts, 141 refusals
(exit 2), 159 guard-passed runs, and **76 clobbers of the guarded file through the
raced symlink** (25% of attempts). The landed docstring already declares TOCTOU
"inherent and out of scope" — the honest declaration should carry the measured
rate, and a one-line hardening exists for the symlink vector: open the output
with `O_NOFOLLOW` (or `fstat` the opened descriptor and re-check `(st_dev,
st_ino)` against the scope before writing), which converts the race into a
declared refusal. The hardlink vector is not racy (identity is stable across the
check), so O_NOFOLLOW does not regress it.

## 5. Declared-exit-map hole in the same block (case T16)

Evidence: `run-current.out` case T16 — `--out <existing-regular-file>/sub/r.txt`
→ `out.parent.mkdir(parents=True, exist_ok=True)` raises `NotADirectoryError`
outside the `try`, so the tool dies with a raw traceback at exit 1 (D6 class, in
the write path). Reproduced on the current revision and on all three reference
variants. Patch shape: move the `mkdir` inside the existing `try:` (which
already catches `OSError`) or guard it explicitly and return USAGE.

## 6. Self-refutation of this seat's own reference variant (case T17)

`--out ''` under the L3 reference variant dies with a traceback (exit 1):
`Path("").with_name("" + ".sha256")` raises `ValueError` — the eager sidecar-name
computation lands outside the `try` that catches `OSError`. The base revision
gets this right (exit 2 USAGE, `Is a directory: '.'`). Landing note: compute the
sidecar name inside the guarded region, or catch `(OSError, ValueError)` and map
both to USAGE; a guard arm that makes the *declared* map worse than the revision
it hardens is a regression, not a hardening.

## 7. Non-atomic write — receipt landed, sidecar failed

Evidence: case T4 (`--out /proc/self/fd/9`): receipt bytes were written through
the alias while the sidecar write failed, so the tool exited 2 (a refusal-flavored
class) *after* a completed destructive write. If the guard adopts an alias arm,
the same ordering matters: write the receipt to a temp name in the target
directory, then `os.replace` it and the sidecar, so a failed sidecar cannot leave
a receipt that no sidecar authenticates, and no write happens on a refused run.

## 8. Inode arm fails open when the scoped side is unstattable (landed revision)

Evidence: `attack-failopen.sh` / `failopen-landed.out` at `dc841464…`.

```
scoped : <sandbox>/blocked/watch.conf   (parent mode 000 — untraversable)
alias  : <sandbox>/outside/alias.conf   (hardlink of the scoped file)
$ capture --out outside/alias.conf --paths blocked/watch.conf
exit=14                              # UNEVALUABLE — D2's declared class
RECEIPT: outside/alias.conf  sha256=e02216…
victim-CLOBBERED                     # the receipt landed on the measured inode
```

`_same_file` wraps `os.stat` in `try/except OSError: return False`, so when the
scoped path cannot even be stat'ed the inode arm silently reports "not the same"
— and the tool clobbers a file it simultaneously records as unevaluable. The
landed docstring says the guard refuses `--out` when it "would resolve to — or
share an inode with — any path being captured"; that sentence is untrue for an
unstattable scoped path.

Patch shape (either is small): make the arm fail closed for a scoped path whose
`capture_path` section carries `stat_error`/`read_error`

```python
        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        unstattable = [p for p, s in zip(paths, sections) if s.get("stat_error")]
        if unstattable and args.out != "-":
            print("USAGE: refusing to write a receipt over an unstattable scoped path"
                  " (alias-check cannot be proven): %s" % unstattable[0], file=sys.stderr)
            return EXIT_USAGE
```

(the receipt can still be produced with `--out -`), or state the exception in the
docstring scope sentence next to the existing TOCTOU sentence. Severity: low
under the declared threat model — an actor able to create the alias can already
write the file — but the contract sentence should not be absolute when it is not.