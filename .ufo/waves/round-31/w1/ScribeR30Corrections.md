# Round-30 routed defects 3 and 4

## Behavior

[OBSERVATION] The installed rea-agents 6.5.0 `RustAuditableReader.js` has the four refusal-message strings at lines 302, 306, 139, and 143. Its SHA-256 is `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505`, matching the requested `1f3748c9…` prefix. The frozen predictions instead cite lines 151-153, 154-157, 128-129, and 131-134, respectively.

[OBSERVATION] The R30-C2 claim surface includes the 1 MiB compressed and 64x inflate-ratio limits. The earlier l7-02 note already records those limits at line 10. The round-30 refusals entry reports observed messages and error codes for the four cases: `invalid_request` for `r-two-roots`, `r-index-outside`, and `r-not-zlib`; `resource_constraint` for `r-inflate-ratio`.

[INFERENCE] The four code-pointer corrections are `r-two-roots` 151-153 → 302, `r-index-outside` 154-157 → 306, `r-inflate-ratio` 128-129 → 139, and `r-not-zlib` 131-134 → 143.

## Draft paragraph (exact)

Correction (round 31): The code pointers for r-two-roots, r-index-outside, r-inflate-ratio and r-not-zlib in corpus/evidence/round-30/c2/predictions.tsv are RustAuditableReader.js:151-153 → RustAuditableReader.js:302, RustAuditableReader.js:154-157 → RustAuditableReader.js:306, RustAuditableReader.js:128-129 → RustAuditableReader.js:139, and RustAuditableReader.js:131-134 → RustAuditableReader.js:143, respectively. The 1 MiB compressed-size and 64x inflate-ratio limits were already recorded in corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10; the new R30-C2 content is the observed refusal messages and error codes.

## Findings and command evidence

Evidence collection date: 2026-10-23. The exact timestamp observed after the local source hash command was `2026-10-23T04:10:38Z`. The `read` and `grep` tools returned the excerpts below without tool errors, but do not expose numeric exit statuses or per-call timestamps; those are [UNKNOWN]. No shell `sed` or `grep -n` command was run: line extraction and regex matching used the required file-reader and search tools. The excerpts show the requested line content and line-number matches.

[OBSERVATION] `read` on `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js:139-143` returned:

```text
139:        return new RustAuditableResourceFailure({ resource: "memory", reported_limits: { maximum_bytes: maximum } }, "Inflated dependency JSON exceeds the size limit");
140:    if (code === "ERR_TRAILING_JUNK_AFTER_STREAM_END" ||
141:        code.startsWith("Z_") ||
142:        code === "ERR_INVALID_ARG_TYPE")
143:        return new RustAuditableFormatFailure("malformed", "Dependency section is not a complete zlib stream");
```

[OBSERVATION] `read` on the same file at `:302-306` returned:

```text
302:        throw new RustAuditableFormatFailure("malformed", "Dependency JSON declares more than one root package");
303:    for (const [index, pkg] of packages.entries()) {
304:        const outside = pkg.dependencies.find((target) => target >= packages.length);
305:        if (outside !== undefined)
306:            throw new RustAuditableFormatFailure("malformed", `Dependency index ${String(outside)} from package ${String(index)} is outside the package list`);
```

[OBSERVATION] The specialized `grep` search of `RustAuditableReader.js` for `more than one root package|outside the package list|exceeds the size limit|not a complete zlib stream` returned matches at lines 139, 143, 302, and 306, with the exact message lines reproduced above. The specialized `grep` search of `corpus/evidence/round-30/c2/predictions.tsv` returned these frozen rows:

```text
9:r-not-zlib  ... RustAuditableReader.js:131-134 inflateFailure Z_*
12:r-inflate-ratio ... RustAuditableReader.js:73,128-129 RUST_INFLATE_RATIO
19:r-two-roots ... RustAuditableReader.js:151-153 rootIndex
20:r-index-outside ... RustAuditableReader.js:154-157 rootIndex
```

The ellipses above abbreviate intervening TSV fields; the pointer values and row IDs are copied from the tool output. Tool exit status and exact per-call UTC times are not exposed; report collection timestamp is `2026-10-23T04:10:38Z`.

[OBSERVATION] The R30-C2 surface at `.ufo/waves/round-30/claims.json:26` describes the table as covering “exact messages and the 1 MiB compressed / 64x inflate ratio / 32-level nesting limits”. The l7-02 note at `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10` says “Guards — 256 MiB file, 1 MiB section, min(8 MiB, 64× section) inflated JSON, 8 MiB report — are tool bounds, not OS limits.” The existing refusals entry table lines 30, 33, 40, and 41 gives the four observed message/code pairs summarized above.

### Source provenance

Access date for each local source: 2026-10-23. URLs below use `file:///` for the local files. Hashes were printed by `timeout 10 sha256sum <the five paths below> && timeout 5 date -u +%Y-%m-%dT%H:%M:%SZ`; the command printed the timestamp `2026-10-23T04:10:38Z`. Its final status is inferred as 0 because the chained date command ran; the tool did not print a numeric exit status. No web source was opened.

- URL: `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js`; SHA-256: `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505`; quote at line 302: “Dependency JSON declares more than one root package”.
- URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv`; SHA-256: `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315`; quote at line 19: “RustAuditableReader.js:151-153 rootIndex”.
- URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`; SHA-256: `46dcfccb6bdf8eee3d7b94d4f77da84a6e48973a9d4fc67d824195af25f60384`; quote at line 10: “256 MiB file, 1 MiB section, min(8 MiB, 64× section) inflated JSON”.
- URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json`; SHA-256: `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a`; quote at line 26: “1 MiB compressed / 64x inflate ratio / 32-level nesting limits”.
- URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`; SHA-256: `81d41f316a989232f19ba99cd9c7461f432b991f6ab975dddb935cebec07788e`; quote at line 51: “the `code_pointer` column is a frozen annotation the counter does not read”.

## Gates

No REA call, C1/C2 counter, or control was run. No live envelope was verified in this seat. This is source and frozen-record inspection only; no execution result is claimed. No tool was installed or updated.

## Touched surfaces

Read-only: the five source files listed under provenance. Written: this report only. The round-30 refusals entry and predictions file were not edited; the correction paragraph above is a draft for the L1 to append.

## Out of scope

No product-code changes, counter runs, live REA runs, control work, Git or jj writes, or edits to any round-30 source file.

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/ScribeR30Corrections.md`
- Additional scratch artifacts: none.
