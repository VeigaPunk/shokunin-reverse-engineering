# R23-C1 frozen-pin source review

## Findings

**Observed at candidate commit `2838351450ff1ee4baa620c962a1153450d53311` (read with `git show`, not from a moving worktree):**

- `.ufo/waves/round-23/tools/count-c1.py:25,136-146` defines `SELFTEST_MANIFEST_SHA256`, reads only `frozen/expected-v2.json`, verifies the raw manifest SHA-256 against that constant, then hashes every path in the manifest's `inputs` map before loading the fixture runner. The constant `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` matches the candidate `expected-v2.json` SHA-256.
- `.ufo/waves/round-23/frozen/expected-v2.json:1-6` is schema `r23-independent-counter-controls-v2` and enumerates two inputs: `tools/counter-fixtures.py` (`f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`) and `frozen/fixture.json` (`a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`). Both values match SHA-256 computed from those exact candidate blobs. The manifest also carries 21 expected cases; `.ufo/waves/round-23/verify.py:62` expects 21 self-test cases.
- `.ufo/waves/round-23/tools/counter-fixtures.py:23,29-36` reads the pinned `fixture.json` and iterates the manifest's cases. This is the fixture program/input pair covered by the manifest's checked hashes.
- `.ufo/waves/round-23/frozen/expected-v1.json` remains present at the candidate commit (schema `r23-independent-counter-controls-v1`; SHA-256 `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24`). In the reviewed active C1 self-test path, `count-c1.py:selftest` selects v2 only; `verify.py:58-67` invokes that self-test. The fixture runner receives the already-loaded manifest and does not select v1.
- `.ufo/waves/round-23/verify.py:108-109` records SHA-256 values for `count-c1.py`, `counter-fixtures.py`, `expected-v2.json`, and `fixture.json` in its source-pins output. That code computes and records the executable hash; it does not compare the executable hash to a fixed expected value.

The candidate blob SHA-256 values observed were: `count-c1.py` `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`, `counter-fixtures.py` `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`, `fixture.json` `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`, `expected-v2.json` `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`, and `expected-v1.json` `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24`.

## Inference and bounded conclusion

The manifest digest constant pins the complete v2 manifest bytes, including its schema, the exact input-key set and input digests, and all case expectations. Thus the fixture runner and fixture data hashes declared in v2 are both checked before the runner is loaded or reads the fixture data. The older v1 manifest is retained but is not active in the reviewed C1 self-test path.

If “executable digest constant” means a separate hard-coded digest for `count-c1.py` itself, that is not present in this path: the hard-coded digest pins `expected-v2.json`; `verify.py` only records the executable hash. The v2 manifest does not list the counter executable as an input. This distinction is not a failure of the manifest's two declared fixture/input hashes, but it is an explicit boundary on what those checks establish.

## Unresolved gaps / verification limits

- LSP was unavailable (`xd://lsp` returned “No such tool” and listed the mounted device set). Text search was used only for location; conclusions above come from candidate-commit `git show` source and blob hashes, not grep as semantic proof.
- No self-test or verifier was executed, per the read-only source-review assignment. The 21-case count is a source assertion, not a run result.
- The “v1 inactive” conclusion is scoped to the reviewed R23 C1 self-test/verification path, not a repository-wide semantic call graph.
- No installs.

## Produced files

- `.ufo/waves/round-23/w2/ScoutFrozenPins.md` — this report; its SHA-256 is provided in the handoff rather than embedded in itself.
