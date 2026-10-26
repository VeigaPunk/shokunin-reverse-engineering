# Fixture SKILL slice for grammar exercise (ADVISORY — not the lane SKILL.md)

## Queue-drain craft (fixture)

<!-- sqfs-triage-table v1 -->

| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
|---|---|---|---|---|---|---|---|---|
| `dep-missing-be` | `squashfs_v4*` | `missing-extractor-dependency` | `sasquatch-v4be` | `*` | `*` | `0` | the BE extractor binary is not resolvable on the child PATH -> install the onekey-sec `sasquatch-v4be` binary in `~/.local/bin`, confirm `command -v sasquatch-v4be`, rerun into a fresh output dir | [INFERENCE] unblob 26.6.4 `squashfs.py:68-70`, `get_dependencies`; no BE dep envelope yet |
| `dep-missing-le` | `squashfs_v4*` | `missing-extractor-dependency` | `sasquatch` | `*` | `*` | `0` | the LE extractor binary is not resolvable -> same install, then rerun fresh | `corpus/evidence/round-36/c1/K1/before.json` (D=[sasquatch], H=squashfs_v4_le, P=0) |
| `avm-marker-be-dropped` | `squashfs_v4*` | `extractor-failure` | `none` | `no` | `*` | `0` | unblob treats bytes_used == mkfs_time as AVM and omits `-be`; sasquatch-v4be then reports wrong endianness and exit 1 -> rebuild the body as standard BE or use a patched extractor; never re-run unchanged | unblob 26.6.4 `squashfs.py:48-50`; `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json` |
| `body-extractor-failure` | `squashfs_v4*` | `extractor-failure` | `none` | `yes` | `*` | `*` | the BE `-be` invocation ran and failed on the body -> treat the image as corrupt/mangled; no install fixes it. `published files` is `*`: an xz body failure publishes files beside the failed chunk (R39C2ReconDep) | `env-D7-corrupt-body-a.json` (command `sasquatch-v4be -be -no-exit-code ...`, exit 1, P=0); sibling xz cases P>0 |
| `escaping-symlink-removed` | `squashfs_v4*` | `none` | `none` | `*` | `yes` | `>0` | unblob removed a symlink resolving outside the extraction root and recorded only `MaliciousSymlinkRemoved`; the link is not a published or metadata entry -> expected, do not chase | unblob 26.6.4 `extractor.py:81-89`; `env-C2-chase-first-a.json`, `corpus/evidence/round-38/c1/K1/after.json` |
| `escaping-symlink-removed` | `squashfs_v4*` | `unpublished-entry` | `none` | `*` | `yes` | `>0` | same removal plus at least one retained in-tree link -> the image holds both kinds; the gap belongs to the in-tree link, not to the removed one | `env-D1-in-first-a.json`, `env-D6-two-escaping-a.json` |
| `in-tree-symlink-metadata` | `squashfs_v4*` | `unpublished-entry` | `none` | `*` | `no` | `>0` | every gap is a retained in-tree link -> metadata only, never published; filter by kind, do not install anything | `corpus/evidence/round-38/c1/K2/after.json` |
| `clean` | `squashfs_v4*` | `none` | `none` | `*` | `no` | `*` | recursion published every regular file and no gap or warning was recorded -> nothing to do. `published files` is `*`: a clean image whose tree is one empty directory extracts with `P=0` (R39C2ReconDep `full-be-dirempty-gzip`) | `corpus/evidence/round-38/c1/K3/after.json`, `K4/after.json` (P=4); sibling empty-dir case P=0 |
| `no-squashfs-chunk` | `none` | `*` | `*` | `*` | `*` | `*` | no squashfs handler chunk was selected -> the input is not a SquashFS container at the top level | `env-plain.json` (H empty, P=0) |

## Next section (must terminate the craft section above)
