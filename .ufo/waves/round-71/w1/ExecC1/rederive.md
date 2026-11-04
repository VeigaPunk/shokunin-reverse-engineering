# ExecC1 — independent landing-side rederivation

Axes: coverage/runtime environment; run-bound provenance; read-only isolation.

## Scope and method

Read the round-70 verifier spot-check, R71-C1 plan and frozen container claim. This seat rederived the assigned route/environment/binding subset independently; it did not execute seam-probe.py, reproduce A1–A7, or run A9 concurrency. No assertion of the full 10/10 predicate follows from this seat alone.

Extracted both tools with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show b827a8b5d54f2885ec9be7786389f356c59226ce:tools/round-71/<name>` into this seat's scratch root. SHA256 values equal the container pins (`pins.json`):

- packed-elf.py: `5cf95aaa0892c4e4f1b82edb60590b57e6667467ed607b15989bb867e7d8efe0`
- seam-probe.py: `7c7734af66f571618bb948f90a5d2d7048f245de122f294574939970db1bf157`

The independently authored `rederive.py` launches the frozen route, parses retained raw JSONL without importing either instrument, computes binding independently, builds altered receipt copies, and invokes the frozen packed-elf receipt checker. seam-probe.py is extracted/pinned only, never executed. Python standard library only; no installs or upgrades. LSP is not exposed among available tools; no symbol refactor was needed.

## Commands and nonce

Executed:

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ExecC1/rederive.py
```

Harness launch argv and exit codes are retained verbatim in `route.command.json` and `check-*.command.json`. Route shape:

```text
/usr/bin/python3 -I -B <seat scratch>/packed-elf.py
 --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
 --rev b827a8b5d54f2885ec9be7786389f356c59226ce
 --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
 --work <seat scratch> --challenge <own nonce>
 --nonce-commitment <own hash> --child-env-log <seat scratch>/env.jsonl
 --json-out <seat findings>/c1-route.json
```

Generated 32 random bytes with `secrets.token_bytes(32)`, encoded as 64 lowercase hex characters; the contract hashes this ASCII encoding, not the underlying random bytes. Wrote `nonce-commitment.txt` before route launch. Commitment: `20256a954f2613bef25019a6b8c260883cb5f852a624e3af7a5335005326822e`. This is this seat's independent commitment, not the lane's earlier landing commitment. Exported `KAIDOKU_ENV_CANARY=probe` in route parent environment.

Checker shape (same frozen route tool, not seam-probe):

```text
/usr/bin/python3 -I -B <seat scratch>/packed-elf.py
 --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
 --rev b827a8b5d54f2885ec9be7786389f356c59226ce
 --check-receipt <retained receipt> --nonce-commitment <own hash>
```

## Per-arm evidence

| Arm | Observed result | Evidence |
|---|---|---|
| Frozen bytes | Both SHA256 values equal container pins | pins.json |
| Full four-carrier route | exit 0; met_target true; carriers_matched 4 / target 4 | c1-route.json; route.command.json |
| Raw environment cardinality | 31 JSONL records; upx 21, node 2, readelf 8 | env.jsonl; independent-results.json |
| Exact allowlist | Every record has exactly HOME/LANG/PATH/TMPDIR | independent-results.json exact_keys true |
| Child containment | Every HOME/TMPDIR is a strict path descendant of receipt.run_root, itself under seat scratch | home_tmp_descendants and run_root_is_scratch_descendant true |
| Canary | Exported in parent, absent from every logged environment | canary_exported probe; canary_absent true |
| Required observed children | Packer, node and readelf all appear | required_children_present true |
| Nonce commitment | SHA256(run_nonce ASCII) equals commitment | nonce_hash_matches true |
| Independent binding | SHA256(nonce + ':' + instrument.sha256 + ':' + comma-joined sorted packed_sha256 values) equals run_binding | independent_binding_matches true |
| Genuine checker | exit 0; met true; failing [] | check-genuine.stdout; check-genuine.command.json |
| Round-70 transplant | exit 1; names `run_nonce absent` (also producer/revision/run_root/environment mismatches) | transplanted.json; check-transplanted.stdout |
| One nonce digit flipped | exit 1; sole failure `run_nonce hash != commitment 20256a...` | wrong-nonce.json; check-wrong-nonce.stdout |
| Binding zeroed | exit 1; sole failure `run_binding != derived` | broken-binding.json; check-broken-binding.stdout |

The transplant is an unchanged copy of `.ufo/waves/round-70/l1/scores/c3-at-landing.json`. Wrong nonce and broken binding are deep copies of this seat's genuine receipt, each changed in exactly the specified field.

## Evidence limitation: git child observation

The raw log contains no git record. Frozen packed-elf.py:758–764 invokes git through a separate direct `subprocess.run(..., env=cenv)` rather than the recording `run(..., capture=...)` wrapper. Source therefore supports the git allowlist routing, but these raw runtime records do **not** independently observe git's environment. The literal broad description “records every child” overstates the observed class; A8's narrower enumerated packer/node/readelf predicate passed. This seat does not report a canary leak or an A8 predicate failure.

The launcher logs its own `dict(os.environ)` immediately before exec; this is pre-exec environment evidence, not a post-exec process inspection. No additional runtime instrument was installed.

## Retained evidence and cleanup

All evidence is under this report's directory: harness, pins, commitment, genuine/three altered receipts, raw env.jsonl, route/check command records, stdout/stderr, and independent-results.json. Receipt-internal scratch paths are historical run pointers, not current evidence links. The harness copied the raw log before its `finally: shutil.rmtree(SCRATCH)` cleanup; scratch was removed on successful completion. No builds, project tests, linters, formatters, mutating git/jj operations, global configuration writes, or external-state remediation were performed. Only specifically assigned route/check experiments ran.

Round-70 routed bookkeeping/source/census defects remain inputs for other seats; this seat does not claim to repair or re-evaluate them. No blockers.

Self-evaluation (1–5): accuracy 4 (git runtime evidence explicitly limited); completeness 5 (all six assigned steps and three attacks retained); clarity 4 (full argv uses command JSON plus readable abbreviations); actionability 5 (exact receipts and clause outputs retained); conciseness 4 (scope qualifications add length). Overall 4.4. Integration improvement: distinguish git source-level environment routing from recorded child observations. The user should agree because both the passing subset and its boundary are explicit.

VERDICT: met — assigned four-carrier/environment/binding rederivation and all three rejection arms; defect named: git children are not present in the observed-environment log."} آباد Dar? success?}??