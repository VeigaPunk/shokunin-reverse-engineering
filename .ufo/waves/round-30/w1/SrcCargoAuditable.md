# R30-C1 source draft — S089

## Behavior
Opened the cargo-auditable repository at pinned HEAD and fetched its README, parsing guide, and JSON schema. Drafted one S089 row and its Gate note below. This is a source-curation result only; no REA call or carrier/mutant execution was performed.

## Drafted row

```text
| S089 | cargo-auditable format, parsing and schema documentation — https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/README.md; https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/PARSING.md; https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/cargo-auditable.schema.json (repository github.com/rust-secure-code/cargo-auditable, `git ls-remote` HEAD `e2316a672fc03cb84d296b66198b6b270e915dca`) | docs | A | The official `.dep-v0` record encoding and general ELF, PE, and Mach-O extraction guidance relevant to R30-C1's positive input class; not REA behavior or a thin-Mach-O-specific guarantee | commit `e2316a672fc03cb84d296b66198b6b270e915dca`; README.md sha256 `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc`, `:92-96` (especially `:95`); PARSING.md sha256 `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e`, `:26-40`; schema sha256 `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15`, `:5` | The positive format is JSON compressed with Zlib in a linker section named `.dep-v0`; the parser guide names ELF, PE, and Mach-O extraction but does not establish REA recognition. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md |
```

## Gate

- URL: https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/README.md; access date: 2026-10-23; sha256: `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc`; quote (`README.md:95`): “The JSON is Zlib-compressed and placed in a linker section named `.dep-v0`.”
- URL: https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/PARSING.md; access date: 2026-10-23; sha256: `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e`; quote (`PARSING.md:3`): “Since the format simply uses Zlib and JSON, implementing a parser should be trivial.”
- URL: https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/cargo-auditable.schema.json; access date: 2026-10-23; sha256: `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15`; quote (`cargo-auditable.schema.json:5`): “Describes the `VersionInfo` JSON data structure that cargo-auditable embeds into Rust binaries.”

## Findings and evidence

- **Observation — upstream revision.** Command: `timeout 60 git ls-remote https://github.com/rust-secure-code/cargo-auditable HEAD`. Exact stdout: `e2316a672fc03cb84d296b66198b6b270e915dca\tHEAD`. Exit 0. The tool transcript did not expose this invocation's exact UTC time; it ran before the README fetch completed at `2026-10-23T02:42:07.168101114Z` (the downloaded file mtime), so the invocation time remains unknown. The requested access date is 2026-10-23 UTC.
- **Observation — README fetch.** Command: `timeout 120 curl -fLsS https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/README.md -o /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/README.md`. Stdout empty; exit 0. File mtime observed as `2026-10-22 23:42:07.168101114 -0300` (`2026-10-23T02:42:07.168101114Z`). `functions.read` showed the quote at README line 95.
- **Observation — parsing-guide fetch.** Command: `timeout 120 curl -fLsS https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/PARSING.md -o /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/PARSING.md`. Stdout empty; exit 0. File mtime observed as `2026-10-22 23:42:33.096766876 -0300` (`2026-10-23T02:42:33.096766876Z`). `functions.read` showed the format description at line 3 and ELF/Mach-O/PE extraction guidance at lines 26-38.
- **Observation — schema fetch.** Command: `timeout 120 curl -fLsS https://raw.githubusercontent.com/rust-secure-code/cargo-auditable/e2316a672fc03cb84d296b66198b6b270e915dca/cargo-auditable.schema.json -o /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/cargo-auditable.schema.json`. Stdout empty; exit 0. File mtime observed as `2026-10-22 23:42:33.104910354 -0300` (`2026-10-23T02:42:33.104910354Z`). `functions.read` showed the quoted schema description at line 5.
- **Observation — content hashes.** `timeout 60 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/README.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/PARSING.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/cargo-auditable.schema.json` exited 0 and returned, respectively, `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc`, `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e`, and `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15`. Its invocation UTC time was not emitted.
- **Observation — target knowledge path.** At `2026-10-23T02:44:11Z`, `timeout 30 sh -c 'date -u +%Y-%m-%dT%H:%M:%SZ; sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/draft-S089.md; if test -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md; then printf "knowledge-entry=present\\n"; else printf "knowledge-entry=absent\\n"; fi'` exited 0 and printed `knowledge-entry=absent`. The row is drafted with the requested `mined`/`used-by` values, but the mined-status prerequisite (an existing used-by path) was not met at this observation; do not treat the proposed row as ready to land until that path exists.
- **Inference — claim boundary.** The docs ground `.dep-v0` as Zlib-compressed JSON and give general ELF, PE and Mach-O parsing guidance. They do not establish REA detection, a successful inspection, or a thin-Mach-O-specific guarantee.

## Gates, touched surfaces, and limits

- Scope gate passed: used the pinned upstream docs, recorded hashes and a located quote under the requested 25-word limit; did not use REA or execute any carrier/mutant.
- Touched lane surface: this report only. `corpus/SOURCES.md` and `CORPUS.md` were read; neither was changed. The requested knowledge path was checked and absent.
- Out of scope: editing `SOURCES.md`, creating the knowledge entry, REA measurement, counter execution, builds, tests, installs, and any carrier/mutant execution. No tool was installed or updated.
- Known limit: `git ls-remote` invocation UTC time and some read/hash tool-call timestamps were not emitted, so those exact times are unknown. Source access date is recorded as 2026-10-23 and fetched-file mtimes are retained above.

## Scratch artifacts

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/README.md` — sha256 `ccca48d944ac5d0fe12e663bc26a650bcfd58fbe89e4470b2931e9d3546b5ebc`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/PARSING.md` — sha256 `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/cargo-auditable.schema.json` — sha256 `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15`.
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/draft-S089.md` — sha256 `25e868f10862ff3009eca6e52f490174032e3fd6abf53e97a57cf89653f48648`.

Report: `.ufo/waves/round-30/w1/SrcCargoAuditable.md`
