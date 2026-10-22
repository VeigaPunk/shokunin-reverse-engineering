# S086 source open: Solidity documentation, Library Linking

Seat: KaidokuR28a2.SourceSolidityLinking (scout, leaf). Opened 2026-10-22. Lane read-only; this report is the only lane file written.

## Answer

The Solidity project's own compiler documentation at release tag `v0.8.30` states the unlinked-library placeholder form `__$53aea86b7d70b31448b230b20ae141a537$__` and calls it "a 34 character prefix of the hex encoding of the keccak256 hash of the fully qualified library name". The bytes are stable across two fetches and the tag resolves to commit `73712a01b2de56d9ad91e3b6936f85c90cb7de36`. The S086 row already committed at lane commit `9db24c9e` matches this source on URL, sha256 and lines 74 and 91; I recommend adding line 75 to its anchor cell, because that is the line carrying the "34 character" claim the row's teaches cell repeats, and appending the resolved commit.

## Opened source record (observation)

- URL (pinned by release tag): https://raw.githubusercontent.com/ethereum/solidity/v0.8.30/docs/using-the-compiler.rst
- Repository: github.com/ethereum/solidity. Tag `v0.8.30` is lightweight and names commit `73712a01b2de56d9ad91e3b6936f85c90cb7de36`.
- Bytes read: 39001, sha256 `76e5db1df6cb67b189c0e8e0b27ed9546a03e5655ffdb400653d62196baac4ae`, identical on fetches at 2026-10-22T18:23:27Z and 2026-10-22T18:24:14Z.
- Section: `.. _library-linking:` at line 69, heading `Library Linking` at line 71, under `docs/using-the-compiler.rst`.
- Quote is taken from the raw reStructuredText bytes, not from rendered HTML, so it is a direct quote.
- Cross-check: `develop` at the same path (fetched 2026-10-22T18:23:18Z, 46974 bytes, sha256 `442d104bb52794bfab1a5feff1074df9ffbc142c86b0a2c51bfe939cf990357f`) has the same three lines at the same numbers 74, 75 and 91. The anchor does not depend on the tag choice for those lines, but the tag keeps the served bytes immutable.

## Quote with line

Primary (line 74), 8 words: `the bytecode contains substrings of the form ``__$53aea86b7d70b31448b230b20ae141a537$__```

Secondary (line 75), 21 words: `The placeholder is a 34 character prefix of the hex encoding of the keccak256 hash of the fully qualified library name.`

Supporting (line 91) defines refilling: `--link` makes solc read input files as "unlinked binaries (hex-encoded) in the ``__$53aea86b7d70b31448b230b20ae141a537$__``-format given above" and link them in place.

Structure check on the documented example (observation, computed): the whole token is 40 characters, `__$` + 34 hex + `$__`; the 34 inner characters are all hex. Line 103-106 adds that before 0.5.0 the placeholder was the fully qualified library name itself, a format `solc --link` still accepts but no longer emits.

## What this source does and does not say

- Says (observation): bytecode of a library-using contract contains such substrings; they are placeholders for library addresses; solc inserts addresses when invoked as linker (`--libraries` or `--link`).
- Does not say (observation): anything about REA, about any carrier file, or that a placeholder makes a file non-hexadecimal. The "not hex" step is an inference from the bytes themselves, confirmed below, not a documentation statement.

## Recommendation for the SOURCES row

The row exists in the lane at `corpus/SOURCES.md:92` with status `mined`, opened `2026-10-22`, recheck `on-release`, used-by `corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md` (which cites S086 three times). Verdict: accept the row as committed; it is accurate against the opened bytes.

- kind: `docs` — correct; this is the compiler project's documentation of its own output, not the compiler source and not a third-party description.
- tier: `A` — correct by the registry's convention (compare S021, Solidity ABI specification, tier A). It is the primary authority for the placeholder format.
- scope: keep as committed: "The unlinked-library placeholder that solc writes into the bytecode of a contract that calls an external library, and how `solc --link` fills it; not REA's parser." It correctly refuses to claim REA behaviour, which the page never mentions.
- anchor: keep `sha256 76e5db1d...`, `:74` (placeholder form), `:91` (`--link`); add `:75` (34-character rule) and, for immutability, the resolved commit `73712a01b2de56d9ad91e3b6936f85c90cb7de36`. Without `:75` the teaches cell's "34 hex" has no anchor line.
- teaches cell: retain; its first clause is supported by `:74`/`:75`. Its second clause (REA refusal as `invalid_format`) is not from this source and should stand on the envelope evidence named next, which the scope cell's "not REA's parser" already permits.

## Carrier cross-check that the row's teaching clause leans on (observation)

- Carrier h09 runtime `.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/out/Cr1LibUser.noopt.runtime.hex`: 1149 bytes, sha256 `f9dc4ccf369a7595bcc1344371737a771ced7922f129d5ae2db0b8b5287c6c68`, equal to the `runtime_sha256` in `corpus/evidence/round-28/c1/carriers.tsv:10`. Exactly one placeholder, `__$a2bad93077572174e8e5044433a5a7d5f3$__`; its 34 inner characters are hex.
- Removing hex digits and newlines leaves only 4 `_` and 2 `$`, i.e. the placeholder container is the only non-hex material in the file.
- `corpus/evidence/round-28/c1/envelopes/h09.json` records code `invalid_request`, category `invalid_input`, `details.issues[0].reason = "invalid_format"`, message "Hex carrier requires complete hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior separators are invalid." So the refusal is REA's hex rule rejecting the placeholder, and the docs row correctly supplies why the bytecode is unlinked in the first place.

## Provenance of the row itself

`git show HEAD:corpus/SOURCES.md | grep -c '^| S086'` returns 1, and `git log -S'| S086 |'` names commit `9db24c9e` ("round-28: ... SOURCES S084-S086 with search log ..."). The working tree holds an uncommitted search-log line at `corpus/SOURCES.md:163` referencing S084-S086; I did not touch it. So the row is already integrated, not a draft awaiting integration, and no duplicate row is needed.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceSolidityLinking/)

- `using-the-compiler-v0.8.30.rst` — tag `v0.8.30` bytes, sha256 `76e5db1df6cb67b189c0e8e0b27ed9546a03e5655ffdb400653d62196baac4ae`
- `refetch-v0.8.30.rst` — second fetch, same sha256 `76e5db1df6cb67b189c0e8e0b27ed9546a03e5655ffdb400653d62196baac4ae`
- `using-the-compiler-develop.rst` — `develop` bytes, sha256 `442d104bb52794bfab1a5feff1074df9ffbc142c86b0a2c51bfe939cf990357f`

No tools were installed or updated for this seat; `curl`, `git`, `python3` and `sha256sum` were already present.

## Commands, exits, times

- `curl -sS --max-time 90 -o using-the-compiler-v0.8.30.rst -w 'HTTP %{http_code} bytes %{size_download}\n' <pinned URL>` — exit 0, "HTTP 200 bytes 39001", 2026-10-22T18:23:27Z.
- `sha256sum using-the-compiler-v0.8.30.rst` — exit 0, `76e5db1d...` (full value above), 2026-10-22T18:23:27Z.
- `curl ... -o refetch-v0.8.30.rst ...` — exit 0, "HTTP 200 bytes 39001", 2026-10-22T18:24:14Z; `sha256sum` of both files identical, exit 0.
- `git ls-remote https://github.com/ethereum/solidity 'refs/tags/v0.8.30^{}' 'refs/tags/v0.8.30'` — exit 0, one line `73712a01b2de56d9ad91e3b6936f85c90cb7de36 refs/tags/v0.8.30` (no peeled line, so the tag points straight at a commit), 2026-10-22T18:23:34Z.
- `grep -o '__\$[0-9a-fA-F]*\$__' <carrier> | sort | uniq -c` — exit 0, one match `1 __$a2bad93077572174e8e5044433a5a7d5f3$__`; `tr -d '0-9a-fA-F\n' | fold -w1 | sort | uniq -c` — exit 0, `4 _`, `2 $`, 2026-10-22T18:24:0xZ.
- Python read of `envelopes/h09.json` — exit 0, printed the `invalid_format` reason and message quoted above, 2026-10-22T18:24:0xZ.

## Confidence and remaining unknowns

- Confidence: high that the URL, sha256, tag-to-commit mapping and line-74/75/91 wording are exactly as recorded; two independent fetches agree and the tag resolves.
- Inference, not observation: that the 34-character rule means the container adds `__$` and `$__` (total 40); the page shows the example but does not spell out the container widths. The lane carrier matches this reading.
- Unknown: whether the deployment of docs.soliditylang.org for `v0.8.30` renders identically; not needed, since the raw source bytes are the opened source.
- Unknown: whether an older release tag states the same wording; only `develop` was compared, and it matches.
