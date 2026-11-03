# Curated sources to consider — kaidoku — 2026-11-03

**Status: unassimilated future reading after hyaku.** This is a separate source-candidate note, not a training round, source admission, readiness claim or instruction to change the current plan. Existing dated reflections remain unchanged.

Public primary sources were read on **2026-11-03 (UTC)**. No candidate code was installed or executed, no live target was tested, and no analyzed artifact was uploaded. All commentary below is original; source material is linked rather than copied.

## 1. LLVM llvm-readobj command reference
- **Type and source:** Primary tool-semantics reference — [primary source](https://llvm.org/docs/CommandGuide/llvm-readobj.html)
- **Version / maintenance:** Rolling LLVM documentation; match to installed tool version before use. Official reference opened 2026-11-03; no host tool execution or version change. [Evidence](https://llvm.org/docs/CommandGuide/llvm-readobj.html#differences-to-llvm-readelf)
- **Why it fits:** Documents low-level object-reader output and the differences between llvm-readobj and its llvm-readelf alias. Useful for precise claims about what a static reader actually reports across ELF, Mach-O and PE/COFF.
- **Reading and proposed later use:** Read description, alias differences, relevant format switches and exit status. After hyaku, propose an evidence-field map for one already authorized artifact, keeping absent fields, parser errors and unsupported formats separate.
- **Limits:** A successfully parsed header does not establish runtime behavior, exploitability or full format validity. Documentation may be newer than the recorded host tools. Treat parser disagreement as a finding requiring byte-level explanation.
- **License:** Apache-2.0 WITH LLVM-exception (LLVM project documentation source). [License evidence](https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT)
- **Duplicate check:** Explicit overlap: llvm-readobj is already named among host fallback readers; LLVM COFF source/test deep links also exist. This is a new semantics reference, not a new tool/readiness claim. Distinct gap: output and alias interpretation.

## 2. pyelftools
- **Type and source:** Maintained repository — [primary source](https://github.com/eliben/pyelftools)
- **Version / maintenance:** v0.33, commit 52ce435186022bd6b32012a998931fe86c985ec8, tag dated 2026-05-29. Official tags and commit page verified v0.33; PyPI independently displays the same May 2026 release. [Evidence](https://github.com/eliben/pyelftools/commit/52ce435186022bd6b32012a998931fe86c985ec8)
- **Why it fits:** A readable Python implementation of ELF and DWARF parsing, useful as a second implementation to inspect alongside Ghidra and binutils. Its examples and tests make individual section, symbol and debug-information interpretations easier to trace.
- **Reading and proposed later use:** Read the user guide and relevant parser/tests at the pinned release. After hyaku, consider comparing a small set of byte-backed fields from an authorized artifact with an existing reader, explicitly recording disagreements.
- **Limits:** Parser agreement is not independent ground truth. Handle malformed artifacts in isolation and never execute the artifact. The main-branch license points out bundled construct licensing; inspect the release’s notices before copying code.
- **License:** Public-domain dedication / Unlicense-style terms; bundled construct has its own MIT notice. [License evidence](https://raw.githubusercontent.com/eliben/pyelftools/main/LICENSE)
- **Duplicate check:** No pyelftools repository/source family found in the supplied inventory/context. ELF and DWARF standards are already present; added value is an inspectable alternate implementation rather than another generic format introduction.
- [Bundled construct license](https://raw.githubusercontent.com/eliben/pyelftools/main/elftools/construct/LICENSE)
- [Official release metadata](https://pypi.org/project/pyelftools/)

## Admission boundary

Re-check the exact version, relevant sections and licensing before later use. Any adoption needs the lane’s normal independent review and evidence gates after hyaku. This file changes no corpus registry, skill, scorecard, training input, authorization or deployment state.
