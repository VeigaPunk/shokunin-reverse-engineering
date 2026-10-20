HOLDS — the 12 synthetic carriers rebuild byte-identical under the prescribed command, `sha256sum -c` passes 12/12, and every synthetic receipt's `carrier.sha256_pre` equals its SHA256SUMS line (and `sha256_post`) at REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94.

Lane: kaidoku-shokunin @ b2aad08ceeee8dd125ce0d316056d8bd766c7f94 (HEAD == REV, verified `git rev-parse HEAD`).
Scope: C3 carrier set, `.ufo/waves/round-18/carriers/` + `runs/*/receipt.json`. No carrier was executed.

## Commands run (all under lane dir unless noted; observation)

1. `OUT=$(mktemp -d) bash .ufo/waves/round-18/carriers/build.sh` — exit 0, ~14 s. Stdout printed 12 `<sha256>  s1…` lines; every hash is byte-identical to `carriers/SHA256SUMS` lines 1–12 (`git show b2aad08:.../SHA256SUMS` == working file, sha256 `6b998a77…92137`).
2. Rebuild to a retained dir `OUT=/tmp/kr18-carriers-<n>` then `cd $OUT && sha256sum -c .../carriers/SHA256SUMS` — exit 0, output `OK` for all 12 files:
   `s1246-noswiss-methods/nethttp/nomethods`, `s1246-swiss-methods/nethttp/nomethods`, `s1250-noswiss-methods/nethttp/nomethods`, `s1250-swiss-methods/nethttp/nomethods`.
3. `~/.local/opt/go-1.24.6/bin/go version` → `go version go1.24.6 linux/amd64`; `~/.local/opt/go-1.25.0/bin/go version` → `go version go1.25.0 linux/amd64` — the two toolchains `build.sh:16` requires exist (installed by wave 1 per `build.sh:3-5`; pre-existing, no install this wave).
4. `git diff b2aad08… -- .ufo/waves/round-18/runs .ufo/waves/round-18/carriers/{SHA256SUMS,build.sh,src}` — empty (exit 0): receipts, sums, recipe, and sources are unchanged since REV. `git status --porcelain` shows only wave-2 scaffolding as `??` (gen-wave2.py, w2/, wave2-*.json/txt) — nothing under carriers/runs.
5. Per-receipt check at REV (read-only `git show b2aad08:.../runs/<label>/receipt.json`, python3 -I -B): for all 12 synthetic labels, `carrier.sha256_pre` == `carrier.sha256_post` == the SHA256SUMS entry, `label` field matches the directory name, and `carrier.path` ends with `/<label>` → mismatches: none.
6. Deployed copies: `sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1*` — the 12 hash values form exactly the SHA256SUMS set (sort/diff equal modulo path column); `~/.local/share/kaidoku-r18/carriers/SHA256SUMS` is byte-identical to the lane file (`diff` exit 0). So the bytes the receipts' `carrier.path` pointed at still match `sha256_pre` (observation; the path field itself is `~/.local/share/kaidoku-r18/carriers/<label>`, e.g. `runs/s1246-swiss-methods/receipt.json` carrier.path).
7. The three non-synthetic receipts (`calib-aether`, `calib-notesmd-cli`, `real-kimi-webbridge`, all `receipt.json:9`) have `sha256_pre` values not in SHA256SUMS — expected: they are real/calibration carriers, not part of the 12-member synthetic set (claims.json amendment: 12 synthetic + 3 others). Each still satisfies `sha256_pre == sha256_post` (no in-run drift).

## Anchors (REV b2aad08)

- Recipe: `carriers/build.sh:11` `out=${OUT:-$here/bin}`; `:13-14` hermetic `mktemp` cache + trap; `:15-26` loop {1.24.6,1.25.0}×{swiss,noswiss}×{methods,nomethods,nethttp} with `env -i`, `GOEXPERIMENT=noswissmap`, `-trimpath -buildvcs=false`, `CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GOAMD64=v1`; `:28` `sha256sum s1*`.
- Sums: `carriers/SHA256SUMS:1-12` — 12 lines, exactly the 12 names the loop generates (`s${ver//./}-$layout-$prog`).
- Receipts: `runs/<label>/receipt.json:9` `"sha256_pre"`, `:8` `"sha256_post"`, `:7` `carrier.path` (carrier block opens at `:5`, `label` at `:23` in s1246-swiss-methods; identical layout for the other synthetics).
- Cross-evidence: `evidence/carrier-buildinfo.json` records the same sha256 per carrier with matching `go_version`/`GOEXPERIMENT` build settings (spot-checked s1246-noswiss-methods, s1246-swiss-methods, s1250-noswiss-methods — all consistent).

## Findings / caveats

- F1 (operability note, not a defect): `OUT=$(mktemp -d) && … bash build.sh` — my first invocation — silently writes to `carriers/bin/` because `OUT` is not exported (`build.sh:11` default). The prescribed env-prefix form `OUT=$(mktemp -d) bash build.sh` works correctly. The accidental `carriers/bin/` produced identical hashes anyway (extra determinism datapoint) and was removed; `git status` clean afterward. Reproducer for the footgun: `OUT=$(mktemp -d); bash build.sh` → output lands in `carriers/bin`, `$OUT` stays empty.
- F2 (observation): no drift mechanism could break the claim here — rebuild is deterministic across two output dirs and the Go build cache was a fresh `mktemp` each run; `-trimpath` removes path dependence.
- F3 (boundary of check): reproducibility is verified on this host/toolchain pair only; portability to another host is not claimed and not tested. Inference: pinned official-tarball toolchains + `env -i` make cross-host drift unlikely but unproven.

## Verdict

HOLDS. No reproducing counterexample found. The C3 carrier substrate (sums, recipe, receipts' `sha256_pre`) is self-consistent and regenerates exactly.

Report: .ufo/waves/round-18/w2/CarrierRebuild.md
Tools installed this wave: none (used pre-existing go1.24.6/go1.25.0 under ~/.local/opt, coreutils sha256sum, git, python3 -I -B).
