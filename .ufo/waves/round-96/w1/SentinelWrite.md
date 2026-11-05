# SentinelWrite — receipt write-path attack review (round 96, sentinel)

Lane HEAD read: `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (via `git show HEAD:<path>`; no lane writes).
Full write-up: `.ufo/waves/round-96/w1/SentinelWrite/attack.md`. Evidence copies and probe sources:
`.ufo/waves/round-96/w1/SentinelWrite/evidence/`.

## Verdict

No HIGH. The receipt writer itself is sound: planted `<json-out>.tmp` and planted `<json-out>`
symlinks both leave the victim intact, `mkstemp` gives `O_EXCL|O_NOFOLLOW` with mode 0600, and
the fsync precedes the replace. Three MED findings sit in the surrounding code.

| ID | Sev | Location (HEAD) | Summary |
|---|---|---|---|
| F1 | MED | kill-rule-v2.py:299,303,311 | `build_copy` `rmtree(ignore_errors)` leaves a planted `mut-<name>` symlink in place; mutant bytes overwrite files at the link target (demonstrated). Same-uid only; breaks the "lane never mutated" guarantee for the counted copy. |
| F2 | MED | symlink-probe-v2.py:93-94,106-113 | Probe does not clear a stale `receipt.json`; `receipt_valid` is only `isinstance(dict)`. A writer that exits 1 with a reused `--work` reads `hardened`, `met true`, exit 0 (demonstrated). Frozen kill-rule path immune; public command 3 is not. |
| F3 | MED | kill-rule-v2.py:249-263 (K-fsync) | Counts `os.fsync ≥ 1`, does not check ordering vs `os.replace`; an fsync-after-replace writer passes (demonstrated). M2 kill is presence-only. |
| F4 | LOW | v6.py:378-388; v3.py:329 | `--rev HEAD` writes `revision: "HEAD"`; verify refuses `revision-not-bound` and `head-not-bound`, exit 1 (fail-closed, demonstrated). The supersession's HEAD fix does not make a HEAD public run green; frozen hex commands unaffected. |
| F5 | LOW | v6.py:95; probe2.py:66; kill2.py:98 | No directory fsync after replace (lost rename, never torn). |
| F6 | LOW | all three writers | `os.fdopen` outside `try` (fd leak only on invalid fd). |
| F7 | LOW | v6.py:358-360; kill2.py:511-514 | Selftest defaults read `$HYAKU_SCRATCH`/`/fast/scratch/hyaku`; kill2 selftest rmtrees that subpath. Hygiene only. |
| F8 | info | all | Receipts are 0600 (umask ignored). |

Named and out of scope, confirmed still named: hostile parent-directory swap
(`plans/round-95-claims.md:114`; `corpus/lessons/round-95.md:64`).

Seat items (a)-(h): (a) and (b) not exploitable (probed in all three writers and in a live v6
run); (c) out of scope, named; (d) sound (`tempfile._bin_openflags` = `0o400302`, mode 0600);
(e) ordering present in code, no directory fsync (F5); (f) the victim cannot be pre-planted to
pass, a stale receipt can (F2); (g) F1; (h) F7.

## Commands and exit codes (scratch-only, lane untouched)

- `python3 -I -B $S/tree/tools/round-96/stop-boundary-repair-battery-v6.py --selftest --work $S/st-v6` → exit 0, 13 of 13 cases.
- `python3 -I -B $S/tree/tools/round-96/kill-rule-v2.py --selftest --work $S/st-kill2` → exit 0, 4 of 4 cases.
- `python3 -I -B attack_probes.py` → exit 0 (writer probes for all three writers, F1 build_copy, F2 stale receipt).
- `python3 -I -B fsync_order_demo.py` → exit 0 (F3: `{'ok': True, 'fsync_calls': 1}` on the inverted writer).
- Live v6 public run, planted `receipt.json.tmp` and `receipt.json` symlinks, `--rev HEAD`, identity_noop repair → exit 1; victims intact; F4 reasons `revision-not-bound`, `head-not-bound`.

Receipts copied to `.ufo/waves/round-96/w1/SentinelWrite/evidence/`: `attack_probes.out.json`,
`fsync_order_demo.out`, `st-v6.out`, `st-kill2.out`, `runA-v6-symlink-{stdout.txt,stderr.txt,receipt.json}`,
and the probe sources. Files I wrote in the lane: `.ufo/waves/round-96/w1/SentinelWrite.md`,
`.ufo/waves/round-96/w1/SentinelWrite/attack.md`, and the `evidence/` directory above.

## Tooling

No tools installed or upgraded. Interpreter used: `python3` 3.14.8 (host), `upx` 5.2.0 (host, used by the v6 live run only).

## Recommended smallest fixes (not applied)

F1: refuse `islink(mut-<name>)`, `rmtree` with `onerror=raise`, fresh dir per mutant. F2: remove
`<target>` before the writer runs; require `writer_rc == 0` and a receipt created this run. F3:
instrument call order, require fsync before replace. F4: normalise `revision` to the full hex
before `write_receipt`. F5: optional directory fsync after replace.
