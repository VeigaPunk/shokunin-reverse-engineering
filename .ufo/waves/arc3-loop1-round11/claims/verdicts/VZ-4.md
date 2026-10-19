# VZ-4 — independent verdict and convergence

## Scope

This review reconciles the frozen C1/C2/C3 criteria (`claims-frozen.md:15-54`) with the round's submitted drafts. Measurements below are my own re-runs; I do not use a peer's numeric result as measurement evidence. I wrote only this verdict artifact. The C1 entry and coverage-map token remain outside my write scope.

## C1 — third `ev_` ID family

**Candidate verdict: REPRODUCED, narrowly for `inspect_go_binary`. Round-level coverage verdict: UNVERIFIABLE until integration.** The frozen C1 criterion allows a third verb-family ID characterization (`claims-frozen.md:18-28`). I recommend the bounded `inspect_go_binary` draft in `claims/c1/EX-1.md` as the single C1 candidate; this is the candidate I re-derived independently.

Target identity was freshly checked:

```text
$ sha256sum /usr/bin/docker /var/tmp/kaidoku-arc3-r11-ex1/docker-copy
70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9  /usr/bin/docker
70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9  /var/tmp/kaidoku-arc3-r11-ex1/docker-copy
$ stat -c '%n bytes=%s type=%F' /usr/bin/docker /var/tmp/kaidoku-arc3-r11-ex1/docker-copy
/usr/bin/docker bytes=29327600 type=regular file
/var/tmp/kaidoku-arc3-r11-ex1/docker-copy bytes=29327600 type=regular file
```

The local cached package was read directly: `rea-agents@6.7.0` at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`. I independently ran `inspect-go-binary <path> --format json --full-output` twice at `/usr/bin/docker` and once at the byte-identical copy, using that package and `TMPDIR=/var/tmp`. I then recomputed each returned ID from the semantic projection (`subject.digest/format/architecture` plus the fields named in `dist/domain/evidence.js:159-183`) using sorted compact JSON and SHA-256.

```text
path=/usr/bin/docker exit=0
reported_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
recomputed_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd id_match=True
path=/usr/bin/docker exit=0
reported_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
recomputed_id=ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd id_match=True
path=/var/tmp/kaidoku-arc3-r11-ex1/docker-copy exit=0
reported_id=ev_fe7068208c1c6430e235b71a4aa52a42796ab4b6f391e533a62228aaa21d7385
recomputed_id=ev_fe7068208c1c6430e235b71a4aa52a42796ab4b6f391e533a62228aaa21d7385 id_match=True
same_path_repeat_equal=True
byte_identity_equal=True
different_path_outer_id_diff=True
```

The observation is limited to one `inspect_go_binary` operation, one ELF byte identity, a same-path repeat and a same-byte alternate-path copy. The source constructs Evidence with the selected path in `parameters` and an `artifact-path` location (`dist/application/go/GoBinaryService.js:54-77`); the semantic projection excludes top-level display fields but includes those semantic fields (`dist/domain/evidence.js:159-183`), and the digest uses canonical SHA-256 (`dist/domain/canonicalDigest.js:8-25,60-76`). This verifies path sensitivity for these calls, not a universal ID rule across operations, releases, or failure records.

Other C1 drafts are competing alternatives, not additional closures: `EX-3.md` and `CR-1.md` also propose Go ID-domain entries; `EX-2.md`, `EX-4.md`, `EX-5.md`, and `CR-2.md` propose `inspect_artifact`; `EX-6.md` proposes a Vyper hardfork characterization. I did not independently re-run those alternatives. Co-land only one selected entry and its matching map token to meet the frozen one-Unknown requirement.

I re-ran Command A from `SCORECARD.md:88-124` at `HEAD=e746ca79e2dbb3cb41436d612f448e81d2c6e585`:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
```

This is the unchanged baseline, not a post-integration result. No corpus or map change was present at the check; therefore the expected `90/90`, `missing:[]`, `dangling:[]` result is **UNVERIFIABLE** until the parent co-lands one draft entry and token and reruns Command A at the landing revision.

## C2 — freshness receipts

**Verdict: REPRODUCED for the measured candidate values; no current drift found.** The wave has several alternate C2 receipts; the frozen C2 needs one measured item and a disposition (`claims-frozen.md:30-41`).

- **Ghidra inventory — VERIFIED, delta 0/0.** I enumerated immediate real directories (excluding symlinks) in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features` and `/Processors`, and read `application.version`. Output: `Features_real_directories=34`, `Processors_real_directories=39`, `application.version=12.1.4`. This matches `PROVINCE.md:46`; it verifies directory counts, not that every module loads or is REA-ready. It independently corroborates the Ghidra receipts in `claims/c2/EX-11.md`, `EX-12.md`, `SC-1.md`, and `SC-2.md`.
- **Pacman cache — VERIFIED, current delta 0.** A fresh `os.scandir` count restricted to non-symlink regular files under `/var/cache/pacman/pkg` returned `archives=1350 signatures=1350 missing=0 orphan=0`. This matches the current count in `PROVINCE.md:50` and corroborates `EX-7.md`, `EX-8.md`, and `EX-9.md`. The row's 1,556 value is explicitly historical; I did not re-observe that old directory state. Relative to that recorded comparator, the arithmetic delta is `1350 - 1556 = -206`, not a fresh measurement of the historical snapshot. Sidecar matching is by filename only, not signature verification.
- **ASAR inventory — VERIFIED, bounded, delta 0.** A read-only walk of `/usr/lib`, `/usr/share`, `~/.config`, `~/.local/opt`, and `/opt/1Password`, counting regular non-symlink `*.asar` files, returned `regular_file_count=12`, `asar_symlinks=0`, `traversal_errors=0`; the twelve paths match the inventory enumerated by `claims/c2/EX-10.md`. This matches `PROVINCE.md:49`. The result is bounded to those roots and is not a proof of host-wide completeness.

Disposition for the matching counts: retain the current values; no corrective edit is motivated by these measurements. The C2 receipts do not make a claim of module operation, archive signature validity, or exhaustive host-wide search.

## C3 — `available:true` capability class

**Verdict: REPRODUCED at provider-capability scope; CORRECTED/qualified at tool-readiness scope; active Kimi session UNVERIFIABLE.** The frozen request calls for `binary_session {}` or a capability result and requires the result to be scoped (`claims-frozen.md:43-54`).

I independently started the installed REA 6.7.0 stdio server with `TMPDIR=/var/tmp`, initialized MCP protocol `2025-03-26`, called `tools/list`, then `tools/call` with `name: "binary_session"` and `arguments: {}`. This was my new verifier session, not the already-running Kimi agent. Exact selected output:

```text
tools/list={"binary_session":true,"count":207,"extract_artifact":true,"inspect_artifact":true}
open=false
cleanup_pending=false
server package=rea-agents@6.7.0 client=vz-4-verifier
capability group={"operations":["extract_artifact","inspect_artifact"],"available":true,"reason":null,"availability_code":null,"effects":["launches_process","may_write_filesystem"]}
tool availability={"names":["extract_artifact"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."}
tool availability={"names":["inspect_artifact"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."}
```

Thus the `available:true` provider group recorded at `PROVINCE.md:50` is **REPRODUCED**. In the same targetless session, neither individual tool is ready to run until `open_binary` selects a target. This is a scope qualification, not evidence that the provider is missing. The current attached Kimi session remains **UNVERIFIABLE** from this seat: the measured server identity is my separately started `vz-4-verifier` session, not the active client connection.

Peer reconciliation: `PL-1.md:3,18-24` and `RV-6.md:17-21` make the same capability-vs-tool-readiness distinction, which my call reproduces. Doctor-only reports (`RV-1.md`–`RV-3.md`) do not establish operation-level availability and do not contradict the new-session measurement. `RV-4.md:7-14` has an internally uncertain launcher path; a direct path check returned `exists=False` for its cited `.../9b9809298fe917ac8/...` path and `exists=True` for the actual cached `.../9b9809298fe40d2c/...` package used in my call. I do not rely on RV-4's command provenance; its underlying provider-level result is independently reproduced here.

## Convergence

- C1's `inspect_go_binary` candidate is directly reproduced, but C1 coverage is not closed until one corpus draft and its map token are co-landed and Command A passes at the landing revision.
- C2 has multiple no-drift measurements; one is sufficient for the frozen claim. Keep the measured scope and limitations with the chosen receipt.
- C3 reproduces provider capability, not targetless tool readiness and not the active Kimi connection. Preserve all three scopes in any integrated wording.
- No tracked file, corpus entry, coverage map, province, skill, scorecard, log, gate, or peer artifact was edited by this seat.
