# Round 30 evidence integrity — SentinelEvidence

**Scope:** read-only audit of all C1/C2 envelopes, manifests, `runs.tsv`, the frozen REA package pin, and carrier inode attributes. No REA run, carrier/mutant write, install/update, or unrelated lane edit was performed. No tools installed or updated.

## Findings table

| ID | Severity / verdict | Observation and exploit path | Impact | Smallest remediation |
|---|---|---|---|---|
| F-1 | **Low — fails the subject-digest binding check** | **Observed:** all 16 refusal envelopes (`r-bad-json`, `r-compressed-flag`, `r-empty`, `r-extra-field`, `r-format-negative`, `r-index-outside`, `r-inflate-ratio`, `r-kind-dev`, `r-nesting-33`, `r-nobits`, `r-not-utf8`, `r-not-zlib`, `r-over-1mib`, `r-trailing-bytes`, `r-two-roots`, `r-two-sections`) are raw refusal JSON without `data.subject.digest.sha256` or a subject name. **Inference / exploit path:** a refusal receipt can be replayed or attributed to a different file at the same logged path; the record does not bind its error to the frozen mutant bytes. | The current mutant bytes match `predictions.tsv`, and each refusal/output still matches its predicted signature. However, the committed refusal evidence alone cannot prove which bytes produced the refusal. No actual tampering was observed. | Have the run harness wrap each refusal with the exact input path and SHA-256 measured around the REA invocation (and retain stdout/exit); require that hash to equal the frozen prediction before accepting the receipt. |
| F-2 | **None — holds** | **Observed:** all 16 C1 envelopes have a subject digest matching `carriers.tsv` and the current carrier bytes. The three accepted C2 envelopes (`g-relocated`, `g-recompressed`, `g-no-root`) likewise match `predictions.tsv` and current mutant bytes. | No C1 or accepted-C2 digest mismatch found. | None. |
| F-3 | **None — holds** | **Observed:** 35 manifest IDs, envelope filenames, and `runs.tsv` IDs are one-to-one. All C1 exits are 0 with `ok=true`; C2 accepted exits are 0 with `ok=true`; C2 refusal exits are 1 with `ok=false` and the frozen refusal message. Run verdict/reason columns agree with those outcomes. | No run/envelope outcome inconsistency found. | None. |
| F-4 | **None — holds** | **Observed:** every run records `rea-agents@6.5.0` and package JSON SHA-256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. That hash and version match the frozen `claims.json` pin and the referenced cached `package.json` bytes. | No package pin mismatch found. | None. |
| F-5 | **None — holds** | **Observed:** `lsattr` reports the immutable (`i`) flag on all 16 carrier files. | Carrier inode protection is present at inspection time. | None. |

**Unknown:** the exact bytes consumed by the 16 refusal runs cannot be recovered from their refusal envelopes; the current mutant-byte match does not establish run-time input identity. This is the F-1 provenance limitation, not evidence that a swap occurred.

## Evidence

**Read-only audit command:**

```sh
timeout 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/SentinelEvidence/audit_round30.py
```

Audit UTC `2026-10-23T03:16:19Z`; **exit 1** (audit completed and reported the 16 missing refusal subject digests). Exact output excerpts:

```text
PKG_CACHE path=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json version=6.5.0 sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c expected_version=6.5.0 expected_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
GROUP C1 manifest=16 envelopes=16 runs=16 ids_manifest_envelopes_runs_match=True
GROUP C2 manifest=19 envelopes=19 runs=19 ids_manifest_envelopes_runs_match=True
  id=g-relocated envelope_subject_digest=8620146512a7a1ffe01ed248726fc3326d74f2a8f853eb7dc94deda7854fbf0c manifest_digest=8620146512a7a1ffe01ed248726fc3326d74f2a8f853eb7dc94deda7854fbf0c digest_match=True disk_digest_match=True subject_name_match=True run_exit=0 expected_exit=0 run_exit_match=True pkg_version=6.5.0 pkg_json_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c pkg_pin_match=True argv_pin_match=True run_verdict=P2-match run_verdict_match=True run_reason_match=True envelope_outcome=ok error_message_match=True
  id=r-empty envelope_subject_digest=MISSING manifest_digest=e26e2ff2951c1da625f4d5871e85bf1912e6e825ee35fb0bf5a7390045c40681 digest_match=missing disk_digest_match=True subject_name_match=missing run_exit=1 expected_exit=1 run_exit_match=True pkg_version=6.5.0 pkg_json_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c pkg_pin_match=True argv_pin_match=True run_verdict=P2-match run_verdict_match=True run_reason_match=True envelope_outcome=refused error_message_match=True
AUDIT_RESULT=FINDINGS finding_count=16
FINDING=c2_r-empty_missing_subject_digest
AUDIT_END_UTC=2026-10-23T03:16:19Z
```

The audit emitted a `FINDING=c2_<id>_missing_subject_digest` for each of the 16 refusal IDs listed in F-1; it emitted no digest, disk-hash, run-exit, run-verdict/reason, or package-pin mismatch for any other checked record. The frozen package pin is `.ufo/waves/round-30/claims.json:68-70` (`rea-agents@6.5.0`, the same package JSON path and SHA-256 shown above).

**Carrier attribute command:**

```sh
timeout 35 sh -c 'date -u +%Y-%m-%dT%H:%M:%SZ; lsattr /fast/scratch/hyaku/kaidoku-r30/carriers/*'
```

UTC `2026-10-23T03:16:19Z`; **exit 0**. All 16 output lines carried `i`; excerpt:

```text
----i----------------- /fast/scratch/hyaku/kaidoku-r30/carriers/elf-aarch64-uv
----i----------------- /fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uvx
```

**Audit artifact:** `/fast/scratch/hyaku/kaidoku-r30/seats/w2/SentinelEvidence/audit_round30.py` — SHA-256 `9ca20f2adba9c915bb49debf3dfa6fda4f115f32f92e9ef81e1f405b5e0b6eca` (hash command at `2026-10-23T03:17:05Z`, exit 0). No other scratch artifact files were created.
