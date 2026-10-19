# CN-4 — arc3-loop1-round11 convergence verdict

**Chain:** verdicts/convergence (`claims-frozen.md:56-61`). I independently re-derived the measurements below; peer artifacts were inspected for overlap and boundaries, not used as measurement evidence. I wrote only this artifact. Git was not mutated; no custody, corpus, gate, province, scorecard, or log path was changed.

## C1 — coverage / one corpus Unknown

**REPRODUCED — `inspect_go_binary` Evidence-ID domain on the tested REA 6.7.0 calls. UNVERIFIABLE — the requested 89→90 post-integration count.**

The current coverage row `corpus/README.md:62` describes Go build metadata, not Evidence-ID derivation. I independently ran the cached REA 6.7.0 CLI on `/usr/bin/docker` twice, copied its bytes under `/var/tmp`, and ran the same operation on that copy. The target and copy each measured 29,327,600 bytes / SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.

Command shape (all `TMPDIR` values were under `/var/tmp`):

```text
node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-go-binary <path> --format json --full-output
```

Exact selected output from my three calls:

```text
base1: exit=0 operation=inspect_go_binary evidence_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd recomputed_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd id_match=True subject_sha256=70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9 parameters_path=/usr/bin/docker
base2: exit=0 operation=inspect_go_binary evidence_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd recomputed_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd id_match=True subject_sha256=70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9 parameters_path=/usr/bin/docker
copy: exit=0 operation=inspect_go_binary evidence_id=ev_d37d1492f5594a8791db5d32b20b477dac18bb9635596ccb6bed55b693128a4b recomputed_id=ev_d37d1492f5594a8791db5d32b20b477dac18bb9635596ccb6bed55b693128a4b id_match=True subject_sha256=70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9 parameters_path=/var/tmp/kaidoku-cn4-r11-go-final/docker-copy
same_path_projection_equal=True
same_path_ids_equal=True
base_copy_digest_equal=True
base_copy_ids_differ=True
base_to_copy_projection_diff=["locations[0].path", "normalized_result.artifact.path", "parameters.path"]
scratch_removed=true
```

My independent recomputation follows the installed source projection at `dist/domain/evidence.js:159-183` and canonical digest at `dist/domain/canonicalDigest.js:8-25,60-76`. The path-bearing parameter/result/location fields are consistent with `dist/application/go/GoBinaryService.js:54-77`. The result is a bounded characterization of this operation, package version, and successful record shape—not a universal formula for every REA verb or release. The artifact was inspected statically, not executed.

I reran Command A from `SCORECARD.md:88-124` against both frozen source revisions. Exact outputs:

```json
{"citation_resolved_rules":16,"dangling":[],"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
{"citation_resolved_rules":16,"dangling":[],"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
```

No C1 entry or coverage token is landed in either revision, so 90/90 is **UNVERIFIABLE** pending co-landing and a fresh Command A run. Recommend integrating only one `inspect_go_binary` draft and its Go-row token; the other visible C1 drafts are alternative `inspect_artifact` or Vyper candidates and should not create parallel closures. I did not independently re-run those alternatives. All eight C1 seat artifacts were present at final census; EX-1/2/3/4/5/6 and CR-1/2.

## C2 — freshness / one measured staleness receipt

**VERIFIED / REPRODUCED — Ghidra inventory; disposition: NO-CHANGE.** I choose this as the single C2 receipt. At `2026-10-19T19:23:06Z`, I enumerated immediate directories under the installed Ghidra 12.1.4 tree and read `application.version`. Exact output:

```text
Features: 34 immediate module directories
Processors: 39 immediate module directories
application.version=12.1.4
```

Against `PROVINCE.md:46`, the deltas are features `34−34=0` and processors `39−39=0`. This verifies the installed directory inventory only; it does not establish that each module loads or is available in an attached REA session. No erratum is indicated.

I also independently checked the other delivered C2 candidates, but they are alternatives rather than additional frozen C2 claims:

- **Pacman — REPRODUCED.** Read-only regular-file enumeration returned `archive_files=1350 signature_sidecars=1350 missing_sidecars=0 orphan_sidecars=0`; deltas are `+0` against `PROVINCE.md:50`'s recorded live 1,350 and `−206` against its dated 1,556 snapshot. Retain the historical snapshot as dated and the current count as observed; this does not validate signatures or package contents.
- **ASAR — REPRODUCED, bounded.** My focused `find` across `/usr/lib`, `/usr/share`, `$HOME/.config`, `$HOME/.local/opt`, and `/opt/1Password` listed 12 regular `*.asar` files, delta 0 against `PROVINCE.md:49`. `ls -ld /opt/containerd` returned `drwx--x--x 1 root root 12 Oct  9 23:03 /opt/containerd`; that unreadable-by-me subtree prevents a host-wide completeness claim. Keep the count scoped to enumerated roots.

The C2 peer set was complete at final census (EX-7..EX-12, SC-1/SC-2); the measurements above are my independent checks.

## C3 — calibration / `available:true` class

**REPRODUCED — provider capability group. DISCREPANCY — targetless per-tool readiness if `available:true` is read as “callable now.” UNVERIFIABLE — the already-attached Kimi session.**

I started a fresh local REA 6.7.0 stdio server and called `tools/list` then `binary_session` with `{}`. `rea mcp doctor --json --full-output` separately reported `healthy:true`, server `rea@6.7.0` / protocol `2025-11-25`, 207/207 tools, and `request_flow:{tool:"binary_session",ok:true}`. My direct session call returned 207 listed tools, `open:false`, and no call error. Exact selected response values:

```json
{"provider":"rea-artifact-graph","operations":["extract_artifact","inspect_artifact"],"available":true,"reason":null,"availability_code":null}
{"names":["extract_artifact"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."}
{"names":["inspect_artifact"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."}
```

Thus `PROVINCE.md:50`'s provider-capability `available:true` class is reproduced in this fresh local session. The exact per-tool inventory in the same targetless session says both calls are gated until `open_binary`; that is not provider failure, but the two scopes must not be conflated. I did not open a target or invoke either artifact operation.

This local stdio session is not the attached Kimi session. My separate `rea doctor --client kimi --json` exited 1 and reported `identity.live_server.state:"unknown"` and a missing registration at `/home/vgpnk/.kimi-code/mcp.json`. The current lane receipt documents a Kimi TOML pin at `PROVINCE.md:18`; therefore the doctor's legacy/missing path does not prove what the active client is serving. No `binary_session` tool was exposed in this seat for that already-attached session. Do not claim active-Kimi availability either true or false from these results.

The C3 peer set was complete at final census (PL-1/PL-2, RV-1..RV-6). I independently reproduced the provider group and targetless tool-level split; the active Kimi connection remains unresolved.

## Integration disposition

1. Use one C1 Go-ID-domain draft plus its map token, then require Command A at the landing revision to report 90 files / 90 mapped / empty missing and dangling sets. Do not infer that after-state from the current 89/89 controls.
2. Use the Ghidra 34/39 measurement as the single C2 freshness receipt; no count correction is warranted.
3. Qualify C3 as provider-group capability `available:true`; record targetless `tool_availability` as `target_required` and leave attached-Kimi status unknown until `binary_session {}` is called through that client.

No repository source or configuration was changed. All scratch was under `/var/tmp` and removed; no `/tmp` scratch was used. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched.
