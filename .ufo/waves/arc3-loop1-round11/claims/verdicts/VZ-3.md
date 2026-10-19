# VZ-3 — independent verdict reconciliation

Measured 2026-10-19 against repository `HEAD=e746ca79e2dbb3cb41436d612f448e81d2c6e585`. This is a per-claim reconciliation, not a scalar round verdict. Numeric observations below were re-derived in this seat; peer reports are cited as the items being adjudicated, not used as measurement evidence.

## C1 — coverage: third `ev_` Evidence-ID family

**Evidence verdict: REPRODUCED for `inspect_artifact` and `inspect_go_binary`, each narrowly. Coverage-closure verdict: UNVERIFIABLE / not yet closed.** The draft notes in `claims/c1/CR-2.md`, `EX-2.md`, and `EX-5.md` concern `inspect_artifact`; `CR-1.md`, `EX-1.md`, and `EX-3.md` concern `inspect_go_binary`. Both are possible answers to the one frozen third-family Unknown, but only one named entry/map token should be integrated for C1. My `/usr/bin/jq` run reproduces `inspect_artifact` behavior, but the exact ZIP IDs in `EX-2.md` and rustc IDs in `EX-5.md` are **UNVERIFIABLE by VZ-3** because those inputs were not rerun. The Go family behavior is reproduced by my Docker run; the peers' path-specific IDs were not used as measurements. `EX-6/entry-draft.md` proposes a separate Vyper hardfork candidate; its compiler/bytecode results are **UNVERIFIABLE by VZ-3** because they were not rerun. `EX-4` had evidence files but no seat `.md` summary at this reading, so its result is also **UNVERIFIABLE**.

I independently copied the ELF and ran these commands with all `TMPDIR` state under `/var/tmp`:

```sh
mkdir -p /var/tmp/kaidoku-vz3-r11-c1
cp /usr/bin/docker /var/tmp/kaidoku-vz3-r11-c1/docker-copy
stat -c '%s' /usr/bin/docker /var/tmp/kaidoku-vz3-r11-c1/docker-copy
sha256sum /usr/bin/docker /var/tmp/kaidoku-vz3-r11-c1/docker-copy
TMPDIR=/var/tmp/kaidoku-vz3-r11-c1 npx -y rea-agents@6.7.0 inspect-go-binary /usr/bin/docker --format json --full-output
TMPDIR=/var/tmp/kaidoku-vz3-r11-c1 npx -y rea-agents@6.7.0 inspect-go-binary /usr/bin/docker --format json --full-output
TMPDIR=/var/tmp/kaidoku-vz3-r11-c1 npx -y rea-agents@6.7.0 inspect-go-binary /var/tmp/kaidoku-vz3-r11-c1/docker-copy --format json --full-output
```

`stat` measured 29,327,600 bytes for each and `sha256sum` gave `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9` for both. The two original-path calls returned the same ID, `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`; the copy returned `ev_ded4cd75aa6f46e4a55fc8fda1a03fe862215ce081fcf699d77580c31feb0bc0`. A fresh recomputation using the installed `dist/domain/canonicalDigest.js` implementation matched all three IDs. Rebinding the copy's semantic path fields to `/usr/bin/docker` recomputed the original ID; changing only display `subject.name`/`subject.local_path` preserved it. The inspected installed source is `dist/domain/evidence.js:159-183` (semantic projection) and `dist/domain/canonicalDigest.js:8-25,27-76` (canonical SHA-256); `dist/application/go/GoBinaryService.js:54-76` supplies path-bearing fields. This verifies only the successful `inspect_go_binary` result shape exercised here.

I also copied `/usr/bin/jq` and ran these commands with scratch under `/var/tmp`:

```sh
mkdir -p /var/tmp/kaidoku-vz3-r11-artifact
cp /usr/bin/jq /var/tmp/kaidoku-vz3-r11-artifact/jq-copy
stat -c '%s' /usr/bin/jq /var/tmp/kaidoku-vz3-r11-artifact/jq-copy
sha256sum /usr/bin/jq /var/tmp/kaidoku-vz3-r11-artifact/jq-copy
TMPDIR=/var/tmp/kaidoku-vz3-r11-artifact npx -y rea-agents@6.7.0 inspect-artifact /usr/bin/jq --format json --full-output
TMPDIR=/var/tmp/kaidoku-vz3-r11-artifact npx -y rea-agents@6.7.0 inspect-artifact /usr/bin/jq --format json --full-output
TMPDIR=/var/tmp/kaidoku-vz3-r11-artifact npx -y rea-agents@6.7.0 inspect-artifact /var/tmp/kaidoku-vz3-r11-artifact/jq-copy --format json --full-output
```

Both files measured 30,800 bytes and SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. The repeated original-path outer ID was `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca`; the copy's outer ID was `ev_e5dfa210cb3f51e1bfc5bb5de852270efaaa540a833f358f78524c3fac4d21b6`. The nested `inventory_artifact` ID stayed `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435`. I independently recomputed both outer and nested semantic projections from all three full envelopes; every recomputation matched. This is a real local ELF and one invocation shape; it does not establish a universal REA ID rule.

**Recommendation:** use the `inspect_artifact` draft (`CR-2.md`, proposed `2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`) as the one C1 entry: the independent real-artifact re-run confirms stable nested inventory identity and path-sensitive outer identity. Keep `inspect_go_binary` as alternate/corroborating evidence, not a second C1 entry; do not co-land the separate Vyper Unknown under the same one-claim closure without reopening the frozen choice.

The required coverage postcondition is still absent. I re-ran Command A from `SCORECARD.md:88-124` at both source revisions:

```text
9c1d1fef5595b55d65764626249f164e6816473a:
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
e746ca79e2dbb3cb41436d612f448e81d2c6e585:
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
```

No selected corpus entry or map token is in `corpus/` at this revision, so `90/90` is not measured. The drafts themselves correctly leave post-integration Command A **UNVERIFIABLE**; parent integration must co-land exactly one entry/token and re-run the command on that landing revision.

**Gate identity correction:** `python3 .ufo/gates/c1-census-v10.py --json` exited 0 and returned `"verdict":"PASS"`, `"frontier_rows":14`, `"frontier_errors":[]`, `"stale":[]`, `"ambiguous":[]`, `"undeclared":[]`, `"unresolved":[]`, `"scope_errors":[]`, `"g2_ok":true`, and `current_ok_per_file={"PROVINCE.md":20,"SCORECARD.md":18,"SKILL.md":3}`. The unregistered-bullet check is present at `.ufo/gates/c1-census-v10.py:449-470` (the guard is at `:466-469`); the pointer checker starts at `:492`. However, the supplied key prefix `d6b4deaa…` is **DISCREPANT** with the current file's measured SHA-256: `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573`. `sha256sum` of the worktree file and `git show HEAD:.ufo/gates/c1-census-v10.py | sha256sum` were identical. `SCORECARD.md:1830-1838` records the live `:4126` pointer; I made no custody-path changes.

## C2 — freshness receipts

- **Pacman cache — REPRODUCED.** First-hand commands:

```sh
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' | wc -l
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst.sig' | wc -l
python3 - <<'PY'
from pathlib import Path
p=Path('/var/cache/pacman/pkg')
entries=[x for x in p.iterdir() if x.is_file()]
archives={x.name for x in entries if x.name.endswith('.pkg.tar.zst')}
signatures={x.name for x in entries if x.name.endswith('.pkg.tar.zst.sig')}
missing=sorted(name+'.sig' for name in archives if name+'.sig' not in signatures)
orphan=sorted(name for name in signatures if name[:-4] not in archives)
print(f'archive_files={len(archives)} signature_sidecars={len(signatures)} missing_sidecars={len(missing)} orphan_sidecars={len(orphan)}')
PY
```

Exact output: `1350`, `1350`, then `archive_files=1350 signature_sidecars=1350 missing_sidecars=0 orphan_sidecars=0`. The same-name comparison was computed from directory entries, not inferred from equal counts. This matches the live comparator at `PROVINCE.md:50` (delta `0`). The `1,556` value there is a dated 2026-10-13 snapshot, not a current value; `1,350 - 1,556 = -206` is only the arithmetic delta against that recorded snapshot, which cannot be revalidated from today's cache. This independently reproduces `claims/c2/EX-7.md`, `EX-8.md`, and `EX-9.md`; it does not verify signature cryptography or archive contents.

- **ASAR inventory — REPRODUCED, BOUNDED.** The focused command `find /usr/lib /usr/share "$HOME/.config" "$HOME/.local/opt" /opt/1Password -type f -name '*.asar' -printf '%p\t%s bytes\n' | sort` listed 12 regular files; its paired `wc -l` returned `12`, matching `PROVINCE.md:49` (delta `0`). A wider scan including `/opt` printed `find: ‘/opt/containerd’: Permission denied` and exited `1`; therefore the count is reproduced in the readable roots, not proven host-wide. This confirms the boundary stated in `claims/c2/EX-10.md`.

- **Ghidra inventory — REPRODUCED.** I ran this read-only enumeration against the installed tree:

```python
from pathlib import Path
root=Path('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra')
props=(root/'application.properties').read_text()
version=next(x.partition('=')[2] for x in props.splitlines() if x.startswith('application.version='))
print('application.version='+version)
for name in ('Features','Processors'):
    entries=sorted(p.name for p in (root/name).iterdir() if p.is_dir())
    print(f'{name}: count={len(entries)}')
```

Exact output: `application.version=12.1.4`, `Features: count=34`, `Processors: count=39`. Against `PROVINCE.md:46`, deltas are `0/0`. This independently confirms `claims/c2/EX-11.md`, `EX-12.md`, `SC-1.md`, and `SC-2.md`; it measures installed directory counts, not module loadability.

## C3 — `inspect_artifact` / `extract_artifact` availability

**Provider-capability verdict: REPRODUCED. Targetless per-tool readiness: CORRECTED/QUALIFIED. Attached Kimi session: UNVERIFIABLE.** `rea` was not on `PATH`; I used `npx -y rea-agents@6.7.0 capabilities --format json`. Its `rea-artifact-graph` group returned `operations:["extract_artifact","inspect_artifact"]`, `available:true`, `reason:null`, `availability_code:null`, with server/package version `6.7.0`.

I independently launched a new REA 6.7.0 stdio server, initialized MCP protocol `2025-03-26`, and called `binary_session` with `{}`. `tools/list` returned 207 tools, including `binary_session`, `inspect_artifact`, and `extract_artifact`. The fresh session reported `open:false`, `cleanup_pending:false`; the same capability group was `available:true`. Its per-tool `tool_availability`, however, returned both operations as `available:false`, `reason:"target_required"`, remediation `Call open_binary with a supported local target.` This is target gating, not provider absence: the unqualified `available:true` is accurate for provider capability but not for calling either tool with no target open. No target was opened or extracted.

The separate `npx -y rea-agents@6.7.0 doctor --client kimi --json` exited `1`; exact relevant fields were `registration:kimi ok=false classification=config_drift detail=/home/vgpnk/.kimi-code/mcp.json` and `live_server.state="unknown"` (doctor remediation: call `binary_session` in the active client). Thus the provider capability is freshly reproduced in a standalone CLI/MCP session, but the already-running Kimi client is not proven connected and remains **UNVERIFIABLE**. No configuration was changed. This agrees with the distinction in `claims/c3/PL-1.md` and `RV-6.md`; doctor-only notes (`RV-1.md`–`RV-3.md`) correctly stop at unverifiable. `RV-4.md:7-14` has a self-correcting/uncertain executable path, so its invocation provenance is not independently reliable; the provider result itself was reproduced by my own command.

## Scope

Only this artifact was written by VZ-3. REA/client configuration, custody paths, corpus, province, gates, and tracked source files were not changed. Existing unrelated worktree changes were left untouched. Scratch/output files from the independent REA calls were confined to `/var/tmp/kaidoku-vz3-r11-*`; no `/tmp` path was used.