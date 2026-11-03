# Consider these: Mach-O parser knowledge limits

**Status: unassimilated future reading after hyaku.** Primary sources checked 2026-11-03 UTC. Source candidate only, not a training round, admission or readiness claim. No candidate software, binaries, live targets or private artifacts were run, tested or uploaded.

## macholib: slices and unknown load commands

**Original summary.** macholib's reader keeps fat-file architecture slices separate and selects each Mach-O header's byte order. Its default rejects unknown load commands; an explicit option retains their undecoded data instead. That acceptance mode does not give unknown commands an interpretation. The relocatable-command iterator additionally selects a specific command family rather than describing every command present.

**Exact source.** [Source snapshot 9c2da6781c61b51bb209345a05157a79758d13d6](https://github.com/ronaldoussoren/macholib/commit/9c2da6781c61b51bb209345a05157a79758d13d6), committed 2026-01-02T10:05:38Z. This is a verified commit, not a claimed release tag. Its latest commit only updates copyright, so the timestamp is not evidence of new parser functionality.

**Reading path.** In [MachO.py](https://github.com/ronaldoussoren/macholib/blob/9c2da6781c61b51bb209345a05157a79758d13d6/macholib/MachO.py), read `load_fat`, `load_header`, `MachOHeader.load`, `_RELOCATABLE` and `walkRelocatables`. Then read the [1.16 changelog entry](https://github.com/ronaldoussoren/macholib/blob/9c2da6781c61b51bb209345a05157a79758d13d6/doc/changelog.rst) introducing the unknown-command option.

**Future question.** After hyaku, propose a paper-only worksheet for an already authorized Mach-O description: slice offset and length, magic, command identifier, declared size, decoded fields and unresolved bytes. If two reports list different dependency counts, did they inspect different slices, apply a command filter, or encounter an unsupported command? Record each possibility separately before proposing any comparison run. A permissive parse should never silently become a claim of complete format coverage.

**Limits and rights.** This is implementation reading, not Apple's loader specification, runtime resolution evidence or permission to rewrite an artifact. The repository includes editing functions; they are outside this proposal. [MIT license](https://github.com/ronaldoussoren/macholib/blob/9c2da6781c61b51bb209345a05157a79758d13d6/LICENSE), with copyright and permission notices retained for later reuse.

**Novelty.** No macholib/ronaldoussoren match in the reviewed inventories or prior notes. Existing dyld extraction, LLVM output, ELF and PE parsing sources do not cover this particular unknown-command boundary.

Any later adoption requires independent review after hyaku. No training or deployment changes.
