# RV-7 proposed changes — coverage-gate semantics (arc3-loop1-round3, chain c2)

Status: proposal only; this seat wrote no tool code. Base revision tested:
`7cd19c3c…` (round-3 landed, /var/tmp copy). Both items below were measured on
that revision; item 1 reproduces CR-4's open proposal item 1 (cross-referenced,
not duplicated), item 2 is this seat's own finding.

## 1. Sidecar write escapes the guard (cross-ref: CR-4 `proposed-write-guard.patch.md` §1)

Reproduced independently at `A5_sidecar_escape` (see `V-clean.json`):

```
capture --paths <d>/target.sha256 --out <d>/target      # exit 0
SIDECAR: <d>/target.sha256                              # scoped file overwritten
```

The guard inspects `--out` only; the derived sidecar `out.with_name(out.name +
".sha256")` is written unguarded. Exit 0, scoped file's bytes moved. No new
patch text here — CR-4's §1 patch (guard `(out, sidecar)`) covers it; this entry
exists so the round report counts two independent reproductions.

## 2. `--require-paths` gates on stanza count while printing an `unaccounted` list it does not enforce

Measured at `B6_dup_stanzas` (see `V-clean.json`): a reference built from the
same scratch path five times

```
capture --out dup5.txt --paths a.conf a.conf a.conf a.conf a.conf   # 5 stanzas, 1 distinct path
verify dup5.txt --live --require-paths 5                            # exit 0, VERDICT: MATCH paths=1
```

passes the gate. The printed line is then internally contradictory:

```
REFERENCE-COVERAGE: 5/5 paths present in reference; unaccounted: ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile
```

i.e. it reports all five canonical paths unaccounted and exits 0. The README's
wording ("fewer than N **stanzas**") declares the stanza semantics, so this is
**not a claim violation** — it is a coherence defect between the gate decision
and the line it prints, and it means `--require-paths 5` does not by itself
prove canonical-path coverage (it proves stanza count).

Patch shape (one line, `reference_coverage` — choose either, not both):

```python
# (a) enforce what the line reports: distinct resolved paths, not stanzas
    ok = len(have) >= required
# (b) or declare the field advisory in the line itself
    line = ("REFERENCE-COVERAGE: %d/%d stanzas present in reference; advisory-unaccounted: %s"
            % (len(ref_sections), required, ...))
```

Option (a) changes behaviour for duplicate-stanza references (they would now
exit 2); option (b) changes only text. (a) is the fail-closed reading of the D3
debt's intent; (b) is text-only. Either way a selftest case pinning the choice
would make the semantics executable, e.g. `duplicate-stanza-reference-gate`.

## 3. Not proposed

The remaining RV-7 measurements (write-guard arms A1–A4, D3 arms B1–B5) are
confirmations of the landed declarations, not change requests. The default
no-flag 1-of-5 exit 0 is the declared opt-in behaviour and is unchanged by
design; the load-bearing D3 proof is the flag path (PRE: flag absent → argparse
exit 2 without class; POST: flag present → exit 2 with `REFERENCE-COVERAGE`;
M2 revert: flag parsed and ignored → exit 0 MATCH).
