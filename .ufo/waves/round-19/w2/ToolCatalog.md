# Round 19 W2 — REA catalog cache rerun

## Finding

**No actionable discrepancy observed.** The live installed-cache rerun under `--strict` reproduces `.ufo/waves/round-19/evidence/rea-catalog.json` byte-for-byte (stdout SHA-256 `e18b82a2b9aca737fbcbb5ddeb96c4807ebca08c5c41c10df7b1d85e8d8e160a`; exit 0). Both versions report 153 CLI commands and 207 MCP tools, with distinct tool-catalog digests as recorded below. No `FINDING`, `NOTE`, or `REFUSED` was emitted.

## Observations

At inspection, `refs/heads/main` resolved to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; the requested baseline is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. The scoped diff against that baseline adds the catalog tool and evidence JSON (414 and 30 lines respectively); neither existed in the baseline at these paths.

The probe enumerates cache entries and refuses missing or duplicate installs (`tools/rea-catalog.py:73-103`), imports the package's catalog modules (`:51-66,106-130`), and checks recomputed-vs-recorded digest, independent counts and CLI version (`:180-210`). The output's `method_argv` is the per-cache Node command; its exact argv and package directory are also recorded in `evidence/rea-catalog.json:8-14,22-28`.

| Version | Observed cache path | CLI commands | MCP tools | `tools_sha256` | Version corroboration |
|---|---|---:|---:|---|---|
| 6.7.0 | `/home/vgpnk/.npm/_npx/a1722018f28f9df2` | 153 | 207 | `af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639` | manifest and `rea --version` both 6.7.0 |
| 6.5.0 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` | 153 | 207 | `805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded` | manifest and `rea --version` both 6.5.0 |

The installed manifests state 6.7.0 and 6.5.0 at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json:4` and `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json:4`. The evidence records the same paths, counts and digests at `evidence/rea-catalog.json:3-7,17-21`. The live JSON output was byte-identical to that file, including both `method_argv` values.

**Inference / scope:** this confirms that the two locally installed cache packages returned the recorded catalog identities at the time of the probe. It is not independent authentication of the package archives or a registry provenance check; the digest is specifically the package's recomputed default full-schema tool-catalog digest, not a package-file digest (`tools/rea-catalog.py:45-49,58-60`).

## Commands and exit codes

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
exit 0 — 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=3 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 -- .ufo/waves/round-19/tools/rea-catalog.py .ufo/waves/round-19/evidence/rea-catalog.json
exit 0 — both scoped paths are additions relative to the baseline (414 + 30 lines)

python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/rea-catalog.py --strict
exit 0 — two cache records; stdout matched evidence/rea-catalog.json byte-for-byte; per-version probe and version corroboration succeeded
```

The wrapper's per-cache probe command is `node --input-type=module -e <PROBE> <package-dir>` (`tools/rea-catalog.py:51-66,106-110`); its package directories and exact probe text are retained in `evidence/rea-catalog.json:8-14,22-28`.

## Verification gaps

No self-test or mutation test was run; this assignment required the live cache identity comparison, and no production file was modified. The observation is point-in-time and scoped to the two default versions in `tools/rea-catalog.py:40`.