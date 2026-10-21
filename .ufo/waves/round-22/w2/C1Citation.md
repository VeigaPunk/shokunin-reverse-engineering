# R22-C1 citation-path review

## Finding — Medium: directory-prefix citations count matching files never named by the entry

`count-c1.py` says a witness must cite a retained file “by full lane path” (`.ufo/waves/round-22/tools/count-c1.py:2-9`). The working-tree diff still installs `CITED` as `EVIDENCE_PREFIX + [A-Za-z0-9._/-]*` (`count-c1.py:74-75`) and then accepts any path for which `r20.is_cited(path, cited)` is true (`count-c1.py:111-120`). The inherited helper explicitly expands a cited trailing-slash directory to every descendant: `cited_prefixes` returns those directory strings and `is_cited` accepts `path.startswith(c)` (`round-20/tools/verb-coverage.py:127-133`). Consequently, a directory mention (or an exact decoy-file citation plus a directory mention) causes an unmentioned sibling evidence file to be treated as the cited file.

This is an implementation/contract mismatch, not a cryptographic-authentication limitation. I used an accepted original CLI envelope (`ok: true`, `meta.command: debug-with-gdb`, `data.operation: gdb_console`) with one evidence ID in the eligible entry, so the matching record itself passed `bind_cli`; the counter returned the sibling's path as `bound_evidence`. The acknowledged “no cryptographic authentication” limit does not say that an entry may omit the retained file path. The generic R20 helper documents directory support, but C1's file-level wording is stricter.

### Narrow fix

Keep R20's generic directory-citation behavior for its callers; in C1, require exact file-path membership (e.g. replace the `is_cited(path, cited)` predicate with `path in cited`). Add a fixture where the entry cites `decoy.json` and mentions the `c1/` directory, while the only matching record is in uncited sibling `gdb.json`; expect `debug-with-gdb` not exercised. Preserve the current exact-file positive control. The existing `uncited_path` fixture only replaces the cited path with `not-cited` (`counter-fixtures.py:118-120`) and does not cover directory-prefix expansion.

## Bounded scratch observations

All fixture and Git mutations were confined to `/tmp/c1-attack-3d5xxf04`; source and evidence trees in the lane were not modified. The four runs invoked the live working-tree counter with the scratch revision named below. Full raw stdout strings, exact argument vectors, exit codes, and stderr are in the same-name JSON attachment `C1Citation.json` (`runs[].stdout`, `runs[].argv`, `runs[].exit`, `runs[].stderr`). `stderr` was empty in all four runs.

Every run exits **1** because none exercises all six T1 verbs; this is the counter's expected incomplete-claim exit, not a process failure. The positive and two attack fixtures exercise one verb; the exact-decoy-only negative control exercises none. Exact stdout JSON for the positive and both attacks reports `t1_exercised_count: 1`, `t1_exercised: ["debug-with-gdb"]`, and `targets["debug-with-gdb"].exercised: true`; the negative control reports count 0 and `exercised: false`.

| Case | Exact counter argv suffix (`--root /tmp/c1-attack-3d5xxf04 --rev …`) | Exit | Observed C1 stdout fields |
|---|---|---:|---|
| `control_exact_citation` | `f6b9aae11ce5a56d40bf45f119f899d4812da8e4` | 1 | `t1_exercised_count=1`; `bound_evidence=[["ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",".ufo/waves/round-22/evidence/c1/gdb.json"]]` |
| `attack_bare_prefix` (entry names only `.ufo/waves/round-22/evidence/c1/`) | `cb7f4a5e2390fc85b29633d360ff4431fc64a6f1` | 1 | Same count and bound path: the entry did not name `gdb.json` at all. |
| `attack_uncited_sibling` (entry names `decoy.json` and separately the directory; matching record is only in `gdb.json`) | `f0a4bb01d13abcce71e21b7c7c9c6937b35b6c4d` | 1 | Same count and bound path: `gdb.json` was not named by its full path in the entry. |
| `control_decoy_exact_only` (entry names `decoy.json`, no directory mention; matching record remains in `gdb.json`) | `acdfbfccf0f20f7bb28df943c83e2d422786c1bb` | 1 | `t1_exercised_count=0`; `bound_evidence=[]`; `exercised=false`. |

For example, the exact execution vector for the sibling attack was `/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1-attack-3d5xxf04 --rev f0a4bb01d13abcce71e21b7c7c9c6937b35b6c4d`; it exited 1, emitted the JSON summarized above, and wrote no stderr. The attachment contains complete stdout, not just these fields.

## Diff, verification, and residual risk

- Reviewed the working-tree diff against lane `HEAD` `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; `count-c1.py` and `counter-fixtures.py` were modified in that worktree. The diff adds original-envelope / command / operation binding and stronger source-row eligibility; those checks were present in the scratch proof and did not prevent the citation-path false positive. The prefix predicate remains in the diff.
- The C1 fixture's `uncited_path` mutant tests omission of the exact citation, but there is no directory-citation or uncited-sibling case (`counter-fixtures.py:78-120`). The built-in selftest was observed exiting 0 with `counter_controls_clean`; that does not cover this finding.
- LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool: xd://lsp”, and no LSP device is mounted. Literal grep was used only for locating the knowledge entry and S051+ source rows; behavior conclusions are from source, diff, and scratch executions, not grep as semantic proof.
- No REA tool, target executable, debugger, remote connection, device, or live runtime was used. Canonical-runtime selection, same-identity rerouting, and saturation claims are not applicable to this static counter review. No tools were installed.
- Residual risk is bounded: this finding lets a matching record already retained beneath the C1 prefix count without its file path being cited; it does not create a matching record or bypass the current envelope/operation/refusal checks. Source relevance and scope admission remain explicitly manual per the counter's reported limit.
