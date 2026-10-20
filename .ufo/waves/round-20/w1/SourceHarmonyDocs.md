# SourceHarmonyDocs — HAP package layout: Stage `module.json5` vs FA `config.json`

Seat: KaidokuR20.SourceHarmonyDocs-2 (leaf, read-only; report is the only write). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Fetched 2026-10-20 (`date -Iseconds` at fetch: `2026-10-20T17:48:25-03:00`; later check `2026-10-20T17:49:23-03:00`).

Axes: calibration (quote verbatim, label gaps), coverage (Stage, FA, HAP, build/release phases), depth (pinned-revision drift checked).

## Commands and exits (observed)

| command | exit / result |
|---|---|
| `curl -sSL https://developer.huawei.com/consumer/en/doc/harmonyos-guides/application-package-structure-stage` | HTTP 200, but body is a 1,768-byte JS shell (`Document`); direct curl yields no text. Rendered text was obtained via the `read` tool (jina renderer) and matches the gitee source below. |
| `curl -sSL https://gitee.com/openharmony/docs/raw/master/en/application-dev/quick-start/{application-package-structure-stage,application-package-structure-fa,hap-package,module-configuration-file,application-configuration-file-overview-fa,application-configuration-file-overview-stage,app-structure}.md` | all HTTP 200 |
| `curl … raw/master/zh-cn/application-dev/quick-start/package-structure.md` | 404 (path guess, not a doc) |
| `curl … raw/17cfc13445818ddc98b65dfb1c55246f39851625/en/…/application-package-structure-{stage,fa}.md` (commit pinned by search index) | HTTP 200; content differs from master (see Revision drift) |
| `sha256sum` on the fetched files | recorded below |
| `grep -o` of each quote against the fetched file | all 6 quoted strings matched verbatim (exit 0) |

No tool was installed or updated by this seat. Only `curl`, `grep`, `sha256sum`, `diff` (already present).

## Sources and hashes (master, unpinned, fetched 2026-10-20)

| file (gitee openharmony/docs, master, en/application-dev/quick-start/) | SHA-256 |
|---|---|
| application-package-structure-stage.md | `1ba4a5907cdfcf84d936b93ef72da48f1b9cf9f3272ac68b2f034feb70be3c3c` |
| application-package-structure-fa.md | `6f2f38173b709f3ddb5cd5252af6b111f5c0e83ae70900ed3c1cb9dc312c1428` |
| application-configuration-file-overview-stage.md | `943d9a864a1b09d061429342280ff50dd5fa780a912a3ec6445d74df9c402ec7` |
| application-configuration-file-overview-fa.md | `09edff56315241b6cb51f508c320436c06c6fc0720b856ebe09126fc23bfade2` |
| module-configuration-file.md | `8ff1190b078b15255b3a53ac1b3c688a1407769583cea5f61fbb12ed16898e0d` |
| hap-package.md | `2d0a67e7b5a70cd25869d560032107a32cdbb86ea4a3d3c42679be81b0a90156` |

Developer-site mirror (same content, rendered): https://developer.huawei.com/consumer/en/doc/harmonyos-guides/application-package-structure-stage (read via `read`, 2026-10-20).

## Primary quote (required)

- Quote: "there are two types of configuration files: one app.json5 file and one or more module.json5 files" (16 words; `**` bold markers stripped).
- Located: `application-configuration-file-overview-stage.md:12` (section: intro, "Application Configuration Files (Stage Model)").
- Source: https://gitee.com/openharmony/docs/blob/master/en/application-dev/quick-start/application-configuration-file-overview-stage.md

## Findings (scope: which files a HAP must contain; Stage vs FA)

Observation (quoted, master):
1. Stage: "Each module must contain a module.json5 configuration file" (9 words), stored at `<module>/src/main/module.json5`. Source: `module-configuration-file.md:9`.
2. Stage build: module.json5 plus app.json5 fields "generating the final module.json file for the created HAP or HSP" (`application-package-structure-stage.md:43`). The `.ets` sources become `.abc` files and AppScope resources merge into `resources` (`:41-42`).
3. FA: "you must declare the package structure of the application in the config.json file" (`application-configuration-file-overview-fa.md:23`); config.json has three mandatory tags app, deviceConfig, module (`:28`).
4. FA layout: `config.json`, an `assets/` folder holding resources, libraries and code (`entry/resources`, `resources.index`, `js/`), and `pack.info` (`application-package-structure-fa.md:18-31`).
5. Discriminator: "The storage locations of internal files differ between the FA model and the Stage model" (`application-package-structure-fa.md:18`); FA legacy status: "The FA application development model is supported in API version 8 and earlier." (`application-package-structure-fa.md:14`).
6. A HAP content statement: "A HAP is a module package consisting of code, resource files, third-party libraries, and an application configuration file" (`hap-package.md:9`). Entry vs feature types are declared in module.json5 (per the pinned revision's text; see drift).
7. Release: each app is at least one HAP; App Pack contains only .hap/.hsp; `pack.info` is generated at packing (`application-package-structure-stage.md:48-50`).

Gap (observed): neither the Stage nor the FA page gives a normative enumerated required-file list for a HAP. The must-contain statements are: module.json5 per module (Stage), config.json (FA), and the general "code, resource files, third-party libraries, and an application configuration file" (hap-package.md:9). A Stage HAP's file list (module.json, .abc, resources, pack.info at packing) is derived from the build-phase description, not a checklist. [INFERENCE]

## Revision drift (depth check)

Pinned commit `17cfc13445818ddc98b65dfb1c55246f39851625` (the search index's gitee blob) differs from master. The pinned FA page says "The difference between the application package structures in the FA model and stage model lies in where the internal files of a HAP file are stored." and the pinned Stage page uses `doc-guides-V3` links and "a HAP of the entry type ... whose type field is set to entry in module.json5". The master wording is different. Consequence: quotes here are master-anchored; the report does not use pinned-only wording. The drift itself is an observation worth a `recheck` on each release.

## Rejected / not used

- `zh-cn/…/package-structure.md` (404): path guess, not a source.
- `config-file-fa.md`, `fa-config-file.md`, `config-file.md` (404): path guesses, not sources.
- Developer-site direct curl: JS shell, not text. Used only via the `read` renderer; not a primary anchor.

## Draft

SOURCES.md row (11 columns; `id` placeholder):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | OpenHarmony docs, Application Package Structure in Stage Model / FA Model, module.json5 and config.json pages — https://gitee.com/openharmony/docs/blob/master/en/application-dev/quick-start/application-package-structure-stage.md | docs | A | Package layout only: which file identifies a Stage-model HAP (module.json5, merged to module.json in build) versus an FA-model HAP (config.json), as the docs state; not a normative required-file list | master, unpinned, fetched 2026-10-20; SHA-256 stage `1ba4a5907cdfcf84d936b93ef72da48f1b9cf9f3272ac68b2f034feb70be3c3c`, fa `6f2f38173b709f3ddb5cd5252af6b111f5c0e83ae70900ed3c1cb9dc312c1428`; `application-configuration-file-overview-stage.md:12`; `application-package-structure-fa.md:14,18`; `module-configuration-file.md:9`; `application-configuration-file-overview-fa.md:23`; `hap-package.md:9` | Stage HAPs carry a module.json5 per module that becomes module.json in the build product; FA HAPs declare structure in config.json and keep files under assets/; FA is API 8-and-earlier. The docs give no enumerated required-file checklist. | queued | 2026-10-20 | on-release | — |

Second row considered and not added: the pinned `17cfc134…` revision. It is drift evidence, not a separate authority; it belongs as a recheck note on S0NN.

## Out of scope / not done

- No `SOURCES.md` write (only the report, per the lane contract). The corpus SOURCES.md `S0NN` id is for the integration owner to assign.
- No REA, Ghidra or Go binary was run.
