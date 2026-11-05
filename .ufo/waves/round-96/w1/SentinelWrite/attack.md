# SentinelWrite — adversarial review of the receipt write paths (round 96, lane HEAD 3baac2ef4)

Scope: `write_receipt` in `tools/round-96/stop-boundary-repair-battery-v6.py` (L83-101),
`tools/round-96/symlink-probe-v2.py` (L55-72, probe main L75-138) and
`tools/round-96/kill-rule-v2.py` (L86-104, plus `build_copy` L297-317, `c_probe` L266-292,
`c_fsync` L249-263). Bytes read with `git show HEAD:<path>` (blob copies in
`evidence/`); the lane tree was never written. All probes ran in
`/fast/scratch/hyaku/kaidoku-r96/SentinelWrite` (removed at the end) against a
`git archive HEAD` fixture repo.

Verdict: **no HIGH.** The receipt writer itself (the `<path>.tmp` symlink, the
`<json-out>` symlink, the mkstemp flags, the fsync-before-replace order) is sound in all
three copies. The defects are in what surrounds it: the kill rule's scratch-copy step, the
probe's stale-receipt reuse, and a fsync check that counts calls without ordering.

## Findings

| ID | Sev | Where (HEAD) | Finding | Evidence |
|---|---|---|---|---|
| F1 | MED | kill-rule-v2.py:299, 303, 311 | `build_copy` clears `mut-<name>` with `shutil.rmtree(d, ignore_errors=True)`. A pre-existing **symlink** at `mut-<name>` is not removed (rmtree refuses a symlink and the error is swallowed), so `makedirs`/`copyfile`/`open(dst,"w")` write through it. The mutant bytes land in the link's target (`victim_overwritten: true`; a precious file at the mutant's relative path was replaced). The counted verdict then runs on bytes outside the scratch. No privilege boundary is crossed (the work dir is owned by the same uid, and every seat runs as `vgpnk`), but the lane-never-mutated guarantee and the provenance of the counted copy both depend on the work dir being symlink-free. A TOCTOU window also exists between `rmtree` (299) and `copyfile` (303) for the same-uid actor. | `evidence/attack_probes.out.json` key `kill2_build_copy_symlink` |
| F2 | MED | symlink-probe-v2.py:93-94, 106-113 | The probe clears only `<target>.tmp` before the run, not `<target>` (receipt.json). `receipt_valid` is `isinstance(json.load(target), dict)` with no `writer_rc == 0` and no freshness check. A writer that **exits 1 and writes nothing**, run with the `--work` of an earlier honest run, gives `verdict: hardened`, `met: true`, exit 0. Not attacker-dependent: re-running the public probe leg with a reused scratch triggers it. The kill rule's `c_probe` is immune (it `rmtree`s `probe-run`, kill-rule-v2.py:269), so the frozen counting command is not falsified, but the public command 3 can be. The probe's `met` then claims "the writer produced a valid receipt without escape", which is false. | `evidence/attack_probes.out.json` key `probe_stale_receipt`: run1 writer_rc 0 verdict hardened; run2 writer_rc 1, receipt_valid true, victim_intact true, verdict hardened, met true, rc 0 |
| F3 | MED | kill-rule-v2.py:249-263 (`c_fsync`), K-fsync | K-fsync asserts `os.fsync` count ≥ 1 during `write_receipt`. It does not assert ordering relative to `os.replace`. A writer that calls `os.replace` **before** `fsync` (fsync on the replaced path) passes K-fsync (`{'ok': True, 'fsync_calls': 1}`). So the M2 kill (fsync removal) is presence-only; a fsync-ordering regression survives. This is a calibration gap in C1's kill rule, not a write-path exploit. | `evidence/fsync_order_demo.py`, `evidence/fsync_order_demo.out` |
| F4 | LOW | stop-boundary-repair-battery-v6.py:378, 383, 386-388; v3.py:329 | `--rev HEAD` produces a receipt whose `revision` is the literal `"HEAD"` (v3 writes `args.rev` raw, v6 `main` never normalises it). `verify_receipt` then refuses `revision-not-bound` and `head-not-bound`, exit 1. Fail-closed (no false green), but the round-96 supersession's "resolve_rev accepting HEAD" fix does not make a green HEAD run possible on the public path. The frozen commands use hex (`--rev <decl>`, `--rev <landing>`), so they are unaffected. Fix would be to write `receipt["revision"] = resolve_rev(root, args.rev)` before `write_receipt`. Reproduced: `evidence/runA-v6-symlink-stdout.txt` (`selfverify reason: revision-not-bound`, `head-not-bound`, `... met False exit 1`) and `evidence/runA-v6-symlink-receipt.json` (`"revision": "HEAD"`). | runA |
| F5 | LOW | v6.py:95, 151; probe2.py:66, 111; kill2.py:98 | No directory fsync after `os.replace` in any of the three writers. A crash after the rename can lose the rename (receipt absent). It cannot leave a torn file: the temp is fsynced first, so "complete JSON or absent" holds. | code |
| F6 | LOW | all three `write_receipt` | `os.fdopen` is outside the `try`; if it raised, `fd` would leak. Only reachable with an invalid fd, so negligible. Recorded for completeness. | code |
| F7 | LOW | v6.py:358-360; kill2.py:511-514 | Selftest default root is `$HYAKU_SCRATCH` or the hard-coded `/fast/scratch/hyaku`. kill2's `_selftest` then `rmtree`s `<that>/kaidoku-r96/selftest-killrule` with `ignore_errors=True`. The env var is the operator's own, so this is hygiene only. The hard-coded `/fast` path fails with a traceback when absent and the user is non-root; no security effect. | code |
| F8 | info | all three | mkstemp creates receipts `0600` (verified `0o600` in `attack_probes.out.json`), ignoring the umask. Previous `open("w")` gave `0644`. No lane impact (git tracks only the exec bit). | probes |

## Item-by-item (the seat's (a)-(h))

- **(a) planted `<json-out>.tmp` symlink — NOT exploitable.** `mkstemp` picks a random 8-char
  name with `O_EXCL`, so the predictable name is never used. Probe: the planted link to the
  victim survives untouched (`a_victim_intact: true`), the receipt is a complete regular file
  (`a_target_json_ok: true`) in all three writers. The planted tmp link is left in place
  (`a_tmp_left: ["receipt.json.tmp"]`); the writer neither follows nor removes it. The
  round-95 M95-i escape is closed in this code.
- **(b) planted symlink AT `<json-out>` — NOT exploitable.** `os.replace(tmp, path)` renames
  over the directory entry and never follows it. Probe: victim intact, target a regular file
  (`b_victim_intact: true`, `b_target_regular: true`), dangling link replaced too
  (`c_dangling_replaced: true`). The live v6 public run (`runA`) did the same against both
  planted links: both victims unchanged (`VICTIM-A-JSON`, `VICTIM-A-TMP`), `receipt.json`
  became a regular 0600 file.
- **(c) hostile parent directory — out of scope, still named.** `plans/round-95-claims.md:114`
  ("parent-dir swap is out of scope this round") and `corpus/lessons/round-95.md:64` ("A
  parent-directory swap stays out of scope"). Consequence noted, not graded: an actor who
  controls the parent can swap the file between `os.replace` (v6.py:95) and `verify_receipt`'s
  `open(path)` (v6.py:151). The r95 M95-i LOW already names that re-open-by-path issue.
- **(d) mkstemp flags — sound.** CPython 3.14.8 `tempfile._bin_openflags` = `0o400302`, which
  includes `O_EXCL` and `O_NOFOLLOW` (and `O_CREAT|O_RDWR`). Mode `0600`. Unknown-type raise
  leaves neither target nor residue (`d_raised`, `d_residue: []`).
- **(e) fsync before replace — ordering present in code** (v6.py:93-95, probe2.py:64-66,
  kill2.py:96-98: flush → fsync → replace). Checked by the code, not by strace. The
  inverted-order writer passes K-fsync (F3). No directory fsync (F5).
- **(f) probe victim placement — the victim cannot be pre-planted into a passing state.** The
  probe writes `victim.txt` itself with an 8-byte `secrets` nonce each run (probe2.py:89-91),
  so pre-planted victim content cannot match `victim_intact`. A pre-planted `symlink-run`
  pointing at an attacker dir is the hostile-parent case (out of scope). A stale
  `receipt.json` in the run dir can change the verdict: **F2**.
- **(g) kill-rule scratch copies — F1.** The `mut-<name>` path is rmtree'd with errors ignored
  (kill2.py:299), and the copy writes through a planted symlink; `c_probe` is immune because its
  `probe-run` is rmtree'd (kill2.py:269). The attack needs a same-uid actor (no boundary) or a
  stale link left by an earlier run in the same work dir.
- **(h) `/fast/scratch` assumptions — F7.** Only the selftest default and the env var; no
  security effect.

## Reproduction

All commands run from `/fast/scratch/hyaku/kaidoku-r96/SentinelWrite` (scratch). Exit codes
are from this session.

- `python3 -I -B $S/tree/tools/round-96/stop-boundary-repair-battery-v6.py --selftest --work $S/st-v6` → exit 0, `SELFTEST cases=13 failures=0` (`evidence/st-v6.out`).
- `python3 -I -B $S/tree/tools/round-96/kill-rule-v2.py --selftest --work $S/st-kill2` → exit 0, `SELFTEST cases=4 failures=0` (`evidence/st-kill2.out`).
- `python3 -I -B attack_probes.py > attack_probes.out.json` → exit 0 (`evidence/attack_probes.py`, `evidence/attack_probes.out.json`).
- `python3 -I -B fsync_order_demo.py` → exit 0, `K-fsync verdict on fsync-after-replace writer: {'ok': True, 'fsync_calls': 1}`.
- Live v6 public run with planted `receipt.json.tmp` and `receipt.json` symlinks:
  `python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --root $S/tree --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work $S/runA/work --rev HEAD --expect '<FROZEN_LABEL>' --json-out $S/runA/receipt.json` → exit 1 (the process ended with status 1; its stdout ends `... met False exit 1`). Both victims intact. The HEAD-revision failure is F4. Receipt copy: `evidence/runA-v6-symlink-receipt.json`.

## Named limits (not re-graded)

- Same-directory swap between the write and the verify (r95 limit, M95-i LOW; parent swap
  out of scope per round-95 plan).
- Provenance: a consistent re-authored receipt is indistinguishable (r95 limit, carried).
- The planted-symlink probe checks one victim file; it does not model a race inside the
  writer.

## Recommended smallest fixes (not applied; lane is read-only for this seat)

1. F1: in `build_copy`, refuse if `os.path.islink(d)`, and use `shutil.rmtree(d, onerror=raise)`
   (or a fresh `mkdtemp` per mutant); open `dst` with `O_NOFOLLOW`.
2. F2: in the probe, `os.remove(target)` if lexists before the writer runs, and require
   `writer_rc == 0` and a receipt created in this run for `receipt_valid`.
3. F3: K-fsync should check ordering, e.g. record `os.replace` and `os.fsync` calls in one
   instrumented list and require the first fsync to precede the first replace.
4. F4: write `receipt["revision"] = resolve_rev(root, args.rev)` in v6 `main` before
   `write_receipt`.
5. F5: optional `os.open(dirname)` + `fsync` after `os.replace`.
