# Validate16Run — R17-VALIDATE16 executed (8/8 pass-1 receipts, all exit 0)

Scope: `corpus/lessons/round-17-verifier-spotcheck.md:138` (R17-VALIDATE16): run the
round-17 `receipt-validate.py` as committed at `9011581d84527ba34c675f9cf912e54d2e72d470`
over the 8 first-pass receipts frozen at `da64646adcb19c1ede7537b799b8c7d283fe43da`.

## Result (observation)

- All 8 pass-1 carrier receipts validate **clean: exit 0, zero findings, `kind: carrier`,
  `status: valid`, `checks_performed: 341` each**. Per-label exits:
  calib-esbuild-0.25.12:0, calib-shfmt:0, pro-aether:0, pro-containerd-shim:0,
  pro-esbuild-0.21.5:0, pro-esbuild-0.27.7:0, pro-notesmd-cli:0, pro-op:0.
- Written evidence: `.ufo/waves/round-18/evidence/validate16/summary.json` +
  `<label>.stdout`/`<label>.stderr` (stderr empty for all 8). Contract shape holds:
  `rev` = da64646…, 8 receipts each with int `exit` (routed-defects.py R17-VALIDATE16 check).

## Validator reads absolute paths — remap was required (observation)

- `receipt-validate.py:53` resolves sibling `pins.py` by absolute path
  (`PINS_PATH`); `verify_file` (`:204-247`) recomputes sha256 of every recorded `path`;
  `check_binding` (`:151-180`) reads `retained_logs[].files.ghidra.log.path` bytes and
  matches the bound `session_dir` string plus the carrier's live full MD5.
- Receipts record absolute paths under the live lane. The working tree now holds pass-2
  `runs/` bytes (wrote-over). To avoid validating pass-2 files against pass-1 receipts I
  extracted the frozen tree and rewrote **only** the path prefix in temp receipt copies:
  - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` → `/tmp/r17-validate16.MWZBce`
    (16 occurrences per receipt, byte-for-byte `str.replace`; verified).
  - Tree: `git archive da64646 .ufo/waves/round-17` + `git show da64646:.ufo/waves/round-16/selection.py`
    (a pinned path outside round-17; sha256 `6917da09…` matches the pinned value —
    without it every receipt exits 1 `missing_file`, observed on the first run batch).
- Left unremapped by design (live-bytes targets of the recorded digests): carrier binaries
  (`/usr/bin/aether`, `/usr/bin/containerd-shim-runc-v2`, `/usr/bin/op`, `/usr/bin/shfmt`,
  `/home/vgpnk/.local/bin/notesmd-cli`, 3 esbuild under `kimi-code/node_modules`), and all
  Ghidra typeinfo data under `~/.local/opt/ghidra_12.1.4_PUBLIC/`. `/tmp/kr17-rea-*`
  session dirs no longer exist but are only log-content needles (`:164-175`), not file
  reads — the retained log copies under `runs/` carry the bytes and still bind.

## Why pass-1 receipts pass where prose said they were unvalidated (inference)

R17-VALIDATE16 says the 8 `da64646` receipts "have only w2 seat prose". This run supplies
the missing validator evidence: the receipts' recorded digests, pins snapshots, pins_compare,
and bound-session needles all re-verify against the frozen pass-1 tree plus live carrier
bytes. Validation is against bytes-present-now (the validator's own stated limitation,
docstring lines ~34-37); a file changed and restored would not be caught.

## Commands run (every one, with exit)

- `git show 9011581:...receipt-validate.py > /tmp/receipt-validate-9011581.py; sha256sum; wc -l` — exit 0; sha256 `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`, 744 lines.
- `git ls-tree --name-only da64646 .ufo/waves/round-17/runs/` — exit 0; 8 label dirs + run-log.txt.
- `git show 9011581:{receipt-validate.py,pins.py} > $TMP/val/…; git archive da64646 .ufo/waves/round-17/runs | tar -x` — exit 0; pins.py sha256 `9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0`.
- Path/pins surveys via python3 -c — exit 0.
- `stat` of recorded carrier/temp paths — exit 1 (session dirs absent; carriers present) — expected.
- `git archive da64646 .ufo/waves/round-17 | tar -x -C $TMP` — exit 0.
- Receipt prefix-rewrite python — exit 0 (16 replacements × 8).
- **`python3 -I -B $TMP/val/receipt-validate.py --selftest` — exit 0; exact last line: `SELFTEST: CLEAN cases=9`**.
- First validation batch (before selection.py restore) — exits 1 per receipt; sole finding class `missing_file` on `.ufo/waves/round-16/selection.py`.
- `git show da64646:.ufo/waves/round-16/selection.py > $TMP/...` — exit 0; sha256 matches pinned `6917da09…`.
- Final per-receipt runs `python3 -I -B $TMP/val/receipt-validate.py $TMP/receipts/<label>.json` — **all exit 0** (stdout/stderr retained, sha256 in summary.json).
- Two bash loops produced truncated "no output" runs (shell busy artifact); replaced by a python subprocess loop — no data lost.

## Files changed

- `.ufo/waves/round-18/evidence/validate16/summary.json` (new)
- `.ufo/waves/round-18/evidence/validate16/<label>.stdout` / `<label>.stderr` ×8 (new)
- `.ufo/waves/round-18/w1/Validate16Run.md` (this report)

No installs. No lane VCS commands beyond read-only `git show/ls-tree/archive`. No carrier executed.
