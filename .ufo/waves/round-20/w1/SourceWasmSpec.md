# SourceWasmSpec — WebAssembly Core binary format: import and export entries

Seat: KaidokuR20.SourceWasmSpec-2 (leaf, read-only; no subagent dispatch; no patch; no lane writes beyond this report).
Last observation clock: 2026-10-20T17:48:04-03:00 (`date -Iseconds`). Scope: interpreting `inspect-wasm-artifact` and `compare-wasm-interfaces` results.

## Source (observed, fetched by this seat)

| item | value |
|---|---|
| URL (primary) | https://webassembly.github.io/spec/core/binary/modules.html |
| page title | `Modules — WebAssembly 3.0 (2026-10-20)` (line 8 of the fetched HTML) |
| access (fetch) | `2026-10-20T17:46:56-03:00` (curl HTTP 200, 56891 bytes) |
| sha256 (fetched HTML, `/tmp/wasm-binary-modules.html`) | `5d1afa388503fd2fdf743e6e339c5fe8e969f3c910b8c62ca59b9e130f89df8f` |
| source pin (raw reST) | https://raw.githubusercontent.com/WebAssembly/spec/main/document/core/binary/modules.rst (HTTP 200, `2026-10-20T17:47:31-03:00`), sha256 `d0f17c145d460cc69ebba265204c8e1d0103fe9fb1108b6a18c66882ebe8c047` |
| last commit touching that reST (GitHub API `commits?path=`) | `a6ed9b2b5f266953872660b1b9ad95d7ca1c4515`, committer 2026-04-30T15:44:19Z, "[spec] Use `fieldidx` instead of `u32` (#2149)" |
| companion page for externtype | https://webassembly.github.io/spec/core/binary/types.html (HTTP 200, 29524 bytes, `2026-10-20T17:47:16-03:00`), sha256 `751151ff9ed7299fe5c9f79692cb8575e410dd05be1d324018c206784e47f2c2`; reST sha256 `663b471c9a44e7c90b4f15385a514ca13ef00f0467d52e25789f3cb2b5cdb022` |

Revision caveat (inference): the HTML title date is a build date, not a commit. The HTML and the `main` reST were fetched minutes apart but are not proven to be the same revision. The commit pin above is the last change to `modules.rst` as of the fetch; it is not a guarantee that the HTML was built from that commit.

## Located quote (verbatim, one contiguous sentence, 16 words)

> External indices are encoded by a distiguishing byte followed by an encoding of their respective value.

- Section: `Indices`, the paragraph after the `typeidx`…`labelidx` table.
- Location: modules.rst:48 (`:ref:`External indices <syntax-externidx>` are encoded by a distiguishing byte…`); fetched HTML line 112. The spelling "distiguishing" is in the source and is quoted as-is.
- Why it supports scope: it states that an export's `externidx` is a kind byte plus an index, not a type.

## Observations (grammar, from the fetched modules page)

1. **Import section, id 2.** Heading `Import Section` (HTML line 228; reST line 145). Grammar, HTML lines 233–234:
   `importsec ::= im*:section_2(list(import))`;
   `import ::= nm_1:name nm_2:name xt:externtype ⇒ import nm_1 nm_2 xt`.
   An import entry is therefore a two-part name (module name, field name) followed by an `externtype`. The entry carries a type, not an index.
2. **Export section, id 7.** Heading `Export Section` (reST lines 226–231). Grammar, HTML lines 290–291:
   `exportsec ::= ex*:section_7(list(export))`;
   `export ::= nm:name xx:externidx ⇒ export nm xx`.
   An export entry is a single name followed by an `externidx`. No type is present in the entry.
3. **externidx encoding**, HTML lines 115–119: `0x00 x:funcidx ⇒ func x`; `0x01 x:tableidx ⇒ table x`; `0x02 x:memidx ⇒ memory x`; `0x03 x:globalidx ⇒ global x`; `0x04 x:tagidx ⇒ tag x`. Kind byte, then an index in that kind's index space.
4. **externtype encoding** (types page, reST line 208 and HTML line 137 onward): `0x00 x:typeidx ⇒ func x`; `0x01 tt:tabletype ⇒ table tt`; `0x02 mt:memtype ⇒ mem mt`; `0x03 gt:globaltype ⇒ global gt`; `0x04 jt:tagtype ⇒ tag jt`. The import's `xt` is defined on this page, not on modules.html. For a function import, the externtype carries a `typeidx` directly.
5. **Section presence.** Every section is optional; an omitted section is equivalent to an empty one (modules.rst:66; HTML line 130).
6. **Function section.** "It decodes into a list of type indices that classify the functions defined by a module." (Function Section, HTML line 238 heading; rendered text).

## Inferences (not stated on the cited page; label before use)

- [INFERENCE] An export's signature cannot be read from the export entry. For a `func` export, the signature is reached by: export → `funcidx` → function index space → (imported function's externtype `typeidx`, or the function section's type index for a local function) → type section. The grammar supports every hop; the full resolution rule is in the Validation/Structure pages, which this seat did not fetch.
- [INFERENCE] For `compare-wasm-interfaces`, a stable import key is the pair `(nm_1, nm_2)`, and the import's comparable payload is its `externtype`. For exports the key is the name; the payload is the kind plus index. An index-only difference in an export may reflect a change in import count or ordering, not a changed definition. This is a reading consequence, not a spec statement.
- [INFERENCE] The `name` production (UTF-8 byte vector) is in `values.html`, which this seat did not fetch. Name-equality claims over non-ASCII names depend on that page.

## Gaps and limits

- Validation rules (for example, export names must be unique, and index bounds) live in the Validation/Structure pages; not fetched. Do not cite this row for them.
- The `name` production and the `typeidx` range rules are in `values.html` and were not checked.
- No executable verification: this seat did not run `inspect-wasm-artifact`, `compare-wasm-interfaces`, WABT, or any Go binary. The spec is cited only for grammar.

## Draft

Row for `corpus/SOURCES.md` (11 columns; id placeholder to be assigned at integration):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | WebAssembly Core Specification 3.0, Binary Format — Modules (Import and Export sections) — https://webassembly.github.io/spec/core/binary/modules.html | spec | A | Grammar-level meaning of an import or export section entry in the WebAssembly binary format, for reading `inspect-wasm-artifact` and `compare-wasm-interfaces` results; not validation or instantiation semantics | Page title `WebAssembly 3.0 (2026-10-20)`, fetched 2026-10-20T17:46:56-03:00, HTML sha256 `5d1afa388503fd2fdf743e6e339c5fe8e969f3c910b8c62ca59b9e130f89df8f`; reST `document/core/binary/modules.rst` at commit `a6ed9b2b5f266953872660b1b9ad95d7ca1c4515` (2026-04-30), sha256 `d0f17c145d460cc69ebba265204c8e1d0103fe9fb1108b6a18c66882ebe8c047`; `Indices` rst:48 (HTML:112); `Import Section` rst:145 (HTML:228, grammar 233–234); `Export Section` rst:226 (HTML:285, grammar 290–291); externidx HTML:115–119 | An import entry is `name name externtype` (module name, field name, type); an export entry is `name externidx` (name, kind byte plus index, no type). Interpret an export as an index reference resolved through the index spaces, not as a signature. The companion externtype definition is on binary/types.html (a separate row is needed to cite it). | queued | 2026-10-20 | 90d | — |

Recheck rationale: the page is a live spec revision with a build date in its title, so a 90-day recheck is chosen over `on-release`. The companion `types.html` row (externtype, sha256 `751151ff9ed7299fe5c9f79692cb8575e410dd05be1d324018c206784e47f2c2`) is not drafted here because the contract asks for one row; the integration owner may add it.

## Commands run (exit codes)

- `date -Iseconds` (exit 0), several times.
- `curl -sSL -o /tmp/wasm-binary-modules.html -w ...` https://webassembly.github.io/spec/core/binary/modules.html → HTTP 200, exit 0.
- `curl -sSL -o /tmp/wasm-binary-types.html ...` binary/types.html → HTTP 200, exit 0.
- `curl -sS 'https://api.github.com/repos/WebAssembly/spec/commits?path=document/core/binary/modules.rst&per_page=1'` → commit `a6ed9b2b…`, exit 0.
- `curl -sS -o /tmp/modules.rst ...` and `/tmp/types.rst` from raw.githubusercontent.com `main` → HTTP 200, exit 0.
- `python3` stdlib tag stripping into `/tmp/wasm-modules.txt` (exit 0); `sha256sum`, `grep -n`, `sed -n` (exit 0). The types-page extraction was printed to stdout and not saved.

No packages installed or updated. No Go toolchain binary, REA, or Ghidra was executed. Writes: this report only.

## Hand-off to main agent

- Checks to run: none required for this seat; the row is drafted, not integrated. The integration owner assigns the id and decides whether to add the `types.html` companion row.
- Findings: spec grammar only; no findings about lane tools.
- Process note: one erroneous edit during this seat's work replaced the report body; the report was rewritten in full from the same observations. The current file is the complete rewrite.
