# Curated sources to consider — kaidoku — batch 2 — 2026-11-03

**Status: unassimilated future reading after hyaku.** Source-candidate review only, not a training round, admission, readiness claim or change to the current plan. Public primary material checked on 2026-11-03 UTC. No candidate code or artifact was executed, no live target tested, no private artifact uploaded and no candidate implementation deployed.

## pe-parse: PE address-to-byte interpretation

[Primary repository](https://github.com/trailofbits/pe-parse)

### Original summary

This inspectable PE implementation complements batch-one ELF parsing and generic reader documentation. At the pinned revision, `GetEntryPoint` adds ImageBase to AddressOfEntryPoint; `getSecForVA` locates a virtual section and `ReadByteAtVA` then requests a byte from its stored data. That separates address membership from byte availability. Error-code and location accessors expose another useful distinction: an unavailable byte is not an observed zero or a runtime result.

### Exact source and license

- Version: v2.1.1, published 2022-11-14T17:13:27Z; annotated tag object `e01c757d084ccc79f7225ccd64c43cce4c5e7b0f` peeled through the official GitHub API to commit `7888f1f8de2f6bc302c291a5b4519fad926c0133`. [Release](https://github.com/trailofbits/pe-parse/releases/tag/v2.1.1)
- License: MIT, verified in the pinned repository's license text; retain notices for any later reuse.
- Reading links: [README.md](https://github.com/trailofbits/pe-parse/blob/7888f1f8de2f6bc302c291a5b4519fad926c0133/README.md) · [pe-parser-library/include/pe-parse/parse.h](https://github.com/trailofbits/pe-parse/blob/7888f1f8de2f6bc302c291a5b4519fad926c0133/pe-parser-library/include/pe-parse/parse.h) · [pe-parser-library/src/parse.cpp](https://github.com/trailofbits/pe-parse/blob/7888f1f8de2f6bc302c291a5b4519fad926c0133/pe-parser-library/src/parse.cpp) · [LICENSE](https://github.com/trailofbits/pe-parse/blob/7888f1f8de2f6bc302c291a5b4519fad926c0133/LICENSE)

### Proposed future review

After hyaku, map one already authorized PE's recorded entry-point RVA, image base, section virtual span and file-backed byte span on paper. Read `parse.h` error accessors and VA API; `parse.cpp` lines 502–511, 594–606 and 2715–2748. Ask: can an address belong to a virtual section yet lack a readable file byte? Keep byte evidence, parser behavior and Windows-loader behavior separate.

### Caveats

The stable release is old and does not establish current-format coverage or safety. The repository also advertises a newer prerelease, not substituted here. No parser build, artifact execution or exploitability inference.

### Novelty check

No pe-parse source-family match in the supplied lane inventory/context. A Trail of Bits Electron article already exists, but it is not this parser family. Distinct practical delta: PE virtual/file-address semantics rather than another ELF/DWARF reader.

## Boundary

Any later adoption requires normal independent review after hyaku. Recheck pins and applicable notices first. This note changes no corpus registry, skill, scorecard, training input, authorization or deployment state.
