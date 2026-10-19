# Proposed patch TEXT — deterministic same-second case for the custody-pair selftest

Target: `.ufo/gates/custody-pair/custody-pair.py` (owner: EX-31 / chain c3 integrator).
Status: **not applied** (patch text only; reviewer seat RV-13, wave arc3-loop1-round2).
Pinned revision this text was authored against: sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (39157 B).

## Why

RV-13 ablation (evidence: `receipts/ns-ablation.txt`): a scratch copy of this
instrument with `mtime_ns`/`ctime_ns` removed from `compare_section` (epoch-only
compare) returns `MATCH exit 0` for an in-place same-content rewrite whose mtime
was restored nanosecond-exact, where the landed instrument returns
`REWRITE-DRIFT moved=ctime_ns exit 11` on the identical fixture. So `ctime_ns` is
the load-bearing field for the fresh-fixture / same-whole-second class.

The existing selftest case `same-content-rewrite-inplace-ctime-pin` does catch the
epoch-only variant — measured 5/5 DIRTY (13/15, exit 3) — but only because the
whole selftest fits inside one wall second. If a selftest run straddles a second
boundary, an epoch-only regression passes that case. The case below removes the
timing dependence: it *asserts* the same-whole-second condition, and asserts that
`ctime_epoch` is equal while `ctime_ns` differs, i.e. it pins sub-second precision
as the discriminator.

## Proposed hunk (to sit next to the existing ctime-pin case, same idioms)

```python
    # 2b. same-whole-second in-place rewrite: the epoch fields are EQUAL and only
    #     the ns field moves.  Asserts the same-second precondition so the case
    #     cannot degrade into a second-boundary race, and pins ctime_ns (not
    #     ctime_epoch) as the discriminator.
    def case_ctime_ns_only():
        fixture.write_bytes(payload)
        os.utime(fixture, (1_700_000_000, 1_700_000_000))
        # wait for a fresh whole second so capture + rewrite fit inside one second
        now = time.time()
        time.sleep(max(0.0, int(now) + 1 - now) + 0.01)
        out_rec, rc = capture_to("same-second-pre.txt", [fixture])
        assert rc == EXIT_MATCH, "reference capture exit %d" % rc
        before = capture_path(fixture)
        os.utime(fixture, (1_700_000_000, 1_700_000_000))   # keep mtime pinned
        fixture.write_bytes(payload)                         # identical bytes, in place
        os.utime(fixture, ns=(1_700_000_000 * 10 ** 9, 1_700_000_000 * 10 ** 9))
        after = capture_path(fixture)
        assert before["inode"] == after["inode"], "fixture setup: inode moved"
        assert before["sha256"] == after["sha256"], "fixture setup: content moved"
        assert before["mtime_ns"] == after["mtime_ns"], "fixture setup: mtime not restored"
        assert before["ctime_epoch"] == after["ctime_epoch"], \
            "precondition failed: capture and rewrite landed in different seconds"
        assert before["ctime_ns"] != after["ctime_ns"], "ctime_ns did not move"
        out = root / "same-second.out"
        rc = _run_verify([str(out_rec), "--live"], out)
        assert rc == EXIT_REWRITE_DRIFT, "expected REWRITE-DRIFT, got %d" % rc
        assert "moved=ctime_ns" in out.read_text(), "ctime_ns not reported as the moved field"
    run_case(cases, "same-content-rewrite-same-second-ns-pin", case_ctime_ns_only)
```

Note: if `capture_to` returns the receipt path under a name the harness does not
already use, adjust the two names to the local convention; the assertions are the
substance. `time` is already imported in the module; no new imports.

## Two wording items (no behaviour change)

1. `README.md` exit-code table and the module docstring call exit 11
   "same-content rewrite". Measured (RV-13 `receipts/replay2-summary.txt`, case
   c4-noop-chmod): a `chmod` to the *same* mode on an already-correct file also
   lands in exit 11 with `moved=ctime_ns` — no content and no metadata changed.
   A genuine mode change lands in exit 12 (`METADATA-DRIFT`). Suggested wording:
   "an inode metadata change consistent with a same-content rewrite (ctime moved
   with sha256 equal)".
2. Cross-ref EX-33 §4.1 (`claims/c3/EX-33/attack-rewrite.md:104-115`): `verify`
   does not read the receipt's `<receipt>.sha256` sidecar, so a tampered receipt
   verifies MATCH exit 0 (RV-13 reproduced: `receipts/tamper-evidence/`). EX-33
   already proposes the fail-closed sidecar check in `verify`; this patch does not
   duplicate it.
