source: S265 https://man.freebsd.org/cgi/man.cgi?query=ar&sektion=5 (Archive Headers, Representing File Names, Archive String Tables); S266 https://raw.githubusercontent.com/freebsd/freebsd-src/main/include/ar.h (ARFMAG); S267 https://sourceware.org/binutils/docs/binutils/ar.html (thin archives); S268 https://raw.githubusercontent.com/llvm/llvm-project/main/llvm/include/llvm/Object/Archive.h (magic/header)
verified-at: 2026-11-03; prospective development, scored result recorded separately
recheck: tools/round-65/compare.py against independently generated pinned fixtures; exact invocation in comparison receipt

# Bounded ar name resolution without extraction

[OBSERVATION] GNU long filenames are addressed by offset into a preceding // table. Offset is not an ordinal: it must identify the start of a slash-newline-terminated name. BSD #1/N stores filename bytes before payload inside the declared body size. Thus stored size and actual payload size differ by N. Physical next-header offset advances by the entire stored body plus one newline for odd length, not by payload length alone. Original reader supports this bounded profile; no REA or external archive tool execution is claimed.

| Input evidence | Action | Why |
|---|---|---|
| Normal magic, simple name | Preserve ordinal, header offset and body digest | Duplicate names do not erase occurrences |
| GNU // then /decimal | Resolve entry-start offset; hash member payload separately from table | Header text is an indirection, not member name |
| BSD #1/N | Take N name bytes; digest only remaining body | Hashing filename plus data conflates metadata with content |
| GNU / | Preserve as opaque symbol_table record | Presence is not verification of index semantics |
| Thin magic | Refuse unsupported before following paths | Payload lives outside container custody |
| Offset into middle of name, absent table, bad pad or truncated body | Emit specific malformed finding and no partial inventory | Avoid plausible but fabricated records |

Checklist: identify regular nonsymlink input and its digest; apply1MiB/128record/64KiB stored-body caps; parse60byte headers and strict decimal size; preserve alignment; resolve name representation; never turn a name into an output path; report only complete bounded inventory or refusal.

[OBSERVATION] Source disagreement: FreeBSD ar(5) prints0x96 for the first ar_fmag byte, but FreeBSD ar.h ARFMAG and LLVM constructor use ASCII backtick0x60. The executable header definition is the discriminating evidence. We reject the numeric typo, not the manual's entire layout account. Short source notes in prep/source-notes.md retain this reasoning.

[UNKNOWN] Symbol-index validity, linker selection, object semantics, runtime behavior, authenticity and safety. AIX, thin, /SYM64/, NUL-padded BSD names, non-ASCII names and broader dialect validity are unsupported. Other numeric header fields are opaque: complete means this profile's inventory, not universal archive validation. No extraction or member execution occurs. Fresh recipe instances are controlled demonstrations, not unbiased accuracy estimates.

## Measured after freeze — 2026-11-03

Original post-freeze run at data revision59b7b131d1ffee7b5b22753ee14704cb4f3b3828 matched33/33 exact construction-oracle cases, comparison.json records full argv/UTC/stdout/exit. Freeze9aa1601cb3a1bfdf95871e1748462f50919fc421 follows instruments70b5a5d6. Controlled recipe varies names, lengths, offsets and ordering; boundary/refusal fixtures may repeat. This supersedes the earlier prospective execution status only. Outside judgment recorded separately.

Round65 outside-review scope clarification: only GNU / and // are classified as special; BSD __.SYMDEF symbol semantics are not recognized. Special-table positional legality is not validated. Inventory profile acceptance is not dialect certification.
