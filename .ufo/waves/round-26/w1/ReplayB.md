# ReplayB — independent replay attack on R26-C1 verdicts (inspect, read-bytes, function, instructions, inspect-binary-layout)

Seat: KaidokuR26.ReplayB, 2026-10-22. Lane read-only; scratch under /fast/scratch/hyaku/kaidoku-r26/seats/ReplayB/. No tool installs (npx rea-agents@6.5.0 per contract only).

## Method

- Carrier copy: `cp /usr/bin/jq alt3/jq`; `sha256sum` both, 2026-10-22T12:13:07Z, exit 0. Both `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, `stat` 30,800 B each. Observation: byte-identical, matches claims.json carrier.
- Ten replay calls, strictly sequential, one per verb per path, frozen argv from claims.json `verbs_argv` (e.g. `npx -y rea-agents@6.5.0 inspect /usr/bin/jq --format json --full-output`; address verbs take `0x103fa0`, read-bytes adds `--length 64`). TMPDIR=ReplayB/tmp. Exits 0, `.ok == true`, subject digest e8156675…f7806 on all ten. Envelope write times 12:15:04Z–12:15:48Z (UTC corrected, see caveat below).
- Comparison inputs: run-seat envelopes under seats/RunAnalyzeInspect, RunReadBytesLayout, RunDecompileFunction, RunXrefsInstructions, read 2026-10-22T12:16:56Z; carrier/alt/jq sha256 re-checked equal to carrier at that time.
- UTC caveat: filesystem mtimes read exactly 3 h behind `date -u` (touchtest mtime 09:17:40 vs `date -u` 12:17:40Z). runs.tsv columns are mtime+3 h, calibrated on that pair; hard `date -u` anchors: 12:13:07Z setup, 12:16:56Z extraction, 12:17:40Z touch test, 12:19:37Z manifest.

## Findings

### F1 — cross-session base stability: holds

My fresh-session base run (different cwd, different TMPDIR, ~15+ min after the run seats) reproduces every run-seat base and repeat id exactly. Observation, from `jq -r '.data.evidence_id'` on 21 envelope files, exit 0:

| verb | my base id | run-seat base == repeat id | match |
|---|---|---|---|
| inspect | ev_14f9d92f41c6a421…826b3d328 | same (RunAnalyzeInspect) | yes |
| read-bytes | ev_99b0c6e1f03c73c8…8947500c | same (RunReadBytesLayout) | yes |
| function | ev_b2b7e9e4313ef4f2…4e0488b5 | same (RunDecompileFunction) | yes |
| instructions | ev_b20a0f25f149070f…a1125f8b | same (RunXrefsInstructions) | yes |
| inspect-binary-layout | ev_294a449cecf2d7b6…760a71bd | same (RunReadBytesLayout) | yes |

My inspect-binary-layout base id also equals the claims.json `pre_freeze_probe.evidence_id` from 11:59:16Z — third independent session, same id.

### F2 — alt3 copy versus their copy

Their copy ran at /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq; mine at seats/ReplayB/alt3/jq; both byte-identical to /usr/bin/jq (sha256 re-checked 12:16:56Z).

- inspect, read-bytes, function, instructions: my alt3 id == my base id == their copy id == their base id. Four ids, one value each. Observation. Derived verdict per frozen rules: content-keyed. Confirmed.
- inspect-binary-layout: base ev_294a449c… (mine == theirs == probe), their copy ev_52da4b3df64645306a8046c6571ce7849fd2ae4383e8d05f16601fefcdccd161, my alt3 ev_8de0a0dc5f9e175d765d1fe71a1a2f1b35e916399e5f885b9f2a0a1d65ef42ab. Three distinct ids for one byte-identical content at three paths. Observation. Derived verdict: path-sensitive. Their verdict re-derives.

### F3 — inspect-binary-layout id is path-keyed, not mtime-keyed

`touch alt3/jq` (mtime ns 1792671187899174802 → 1792671459834841032, changed), rerun same argv, 2026-10-22T12:17:40Z, exit 0, `.ok == true`: id unchanged, ev_8de0a0dc… both runs; envelope sha256 changed (fc9714f0… → cfe8fa6b…). Observation: mtime does not enter the id; envelope bytes carry non-identity material. With F2, the id is a function of content plus path. That mtime-exclusion is measured; separating exact path from other path-derived metadata is inference [INFERENCE: path-keyed].

### F4 — envelope bytes are session-unique; identity lives in evidence_id

No two envelopes in my seat or across seats share a sha256 (MANIFEST.sha256, 43 lines), yet ids match per F1/F2. Each sampled envelope text contains exactly the path it ran on (one `/usr/bin/jq` occurrence in base files, zero alt3 references; inverse for alt3 files; `grep -c`, exit 0) — consistent with claims `diagnostics_not_gating`. Observation.

### F5 — provider environment dependency (attempt1 episode)

My first ten calls, run from an environment lacking `GHIDRA_INSTALL_DIR`, all failed: npx exit 1, `.ok == false`, stdout `{"ok":false,"error":{"code":"provider_unavailable",…,"retryable":true,…,"rejections":[{"provider_id":"ghidra","code":"not_configured","reason":"Set GHIDRA_INSTALL_DIR to an extracted Ghidra 12.1.x release directory."…` (envelopes/inspect-base.attempt1.json, written 12:13:35Z). The ten error envelopes carry no `.data.evidence_id`; base and alt3 error bytes are identical for inspect-binary-layout (sha 1272e215…, path-independent). With host env `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` set, all ten succeeded. Observation. The frozen invocation string `TMPDIR=<seat>/tmp npx -y rea-agents@6.5.0 <argv>` silently relies on ambient host env; this is a portability observation, not a counterexample — under frozen rules such triples derive no-id, which still re-derives.

## Verdict per verb (attack on R26-C1 verdict re-derivation for my five verbs)

- inspect: holds — content-keyed re-derives; independent session reproduces id across base/repeat/copy.
- read-bytes: holds — content-keyed re-derives.
- function: holds — content-keyed re-derives.
- instructions: holds — content-keyed re-derives.
- inspect-binary-layout: holds — path-sensitive re-derives; replay strengthens it (third path gives a third id; mtime excluded as id input).

No counterexample found for any of the five attacked verdicts.

## Residual risk and verification gaps

- Env pinning gap: claims `invocation` does not name GHIDRA_INSTALL_DIR; a rerun without it yields all-no-id rows (F5). Rows remain re-derivable, but the measured content-keyed/path-sensitive pattern is env-conditional. Unknown: whether other REA_* vars are load-bearing for these five verbs (I passed the host's full REA_* set on reruns).
- I ran base + one alternate-path run per verb, not a same-seat repeat; repeat stability rests on the run seats' committed repeat envelopes plus my cross-session base match, which is the stronger direction but not a fresh same-seat triple.
- analyze, decompile, xrefs are outside this seat's five verbs; untouched here.
- The inspect-binary-layout id mechanism beyond "path enters the id" (exact key material) is unknown; only mtime is excluded by measurement.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/ReplayB/, sha256 in MANIFEST.sha256)

alt3/jq (e815667571d0…f7806); runs.tsv (21 rows: 10 final, 10 attempt1, 1 touchtest); envelopes/: 10 final `<verb>-{base,alt3}.json` + `.stderr`, 10 `<verb>-{base,alt3}.attempt1.json` + `.stderr`, `inspect-binary-layout-alt3.touchtest.json`; MANIFEST.sha256. Key ids: base ev_14f9d92f… / ev_99b0c6e1… / ev_b2b7e9e4… / ev_b20a0f25… / ev_294a449c…; alt3 same except inspect-binary-layout ev_8de0a0dc….
