# ResidualGit — CriticGit same-seat source follow-up (appendix to CriticGit.md)

Seat: `KaidokuR23.CriticGit` (same W2 identity; source only, no tests, probes, counter or verify runs). Original `CriticGit.md` (review of C=`2838351…`) is unchanged.
Source F=`9d64b95393bb7134e9fe0dfa9f68df91338a3665` (single commit after C: "close source and historical-witness falsifiers").
I read only `git show F:<path>` for the read set, plus `git diff C F` on the same three paths.

| path at F | sha256 |
|---|---|
| `.ufo/waves/round-23/tools/count-c1.py` | `d76da48fe21eca079354f17a49dd29c9626da5e4b4785ffccac9124c62f91c27` |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `687c40742270344fc18a718cdf1a0e14065f0cb5198b3f701c115ec6467d927e` |
| `.ufo/waves/round-23/verify.py` | `eb65e3bdc854e6e07d9c5ddd3f6742659851debb664e63aa23a2baa372fc6b72` |

Nothing has been run at F, so every count and control at F is **unverified** until the final L1 execution. Counter self-hash enforcement is out of scope, as the brief directs.

## Recheck of earlier findings (source)

- **F1, symlink acceptance: closed.**
  - `count-c1.py` now builds `regular_blobs = dict(r20.tree_entries(root, rev))`. That listing uses `-z --full-tree` and keeps only blobs with mode 100644 or 100755.
  - Knowledge `files` are drawn from `regular_blobs`, so a mode-120000 entry is never scanned.
  - Cited Evidence paths are skipped unless `evidence_path in regular_blobs`. Symlink target text is never decoded.
  - `counter-fixtures.py` adds the `symlink_evidence` and `symlink_knowledge` cases, which commit real symlinks whose target is the envelope or entry text.
- **F5, inherited knowledge loss: closed, given top-level `--root` (see G2).**
  - `knowledge_blobs(ref)` maps each path to its `(mode, oid)` from `ls-tree -r -z`.
  - Any baseline path that is missing at rev, or has a different mode or blob, raises `historical_knowledge_changed`. New paths are allowed.
  - The new fixture cases `inherited_entry_lost` and `inherited_entry_changed` stage all of `corpus/knowledge` (the `git add` pathspec is now `corpus/knowledge`).
  - The other fixed guards are unchanged: catalog bytes, old-root tree ID, SOURCES row prefix, and `historical t1 == ['identify-flutter-build']`.
  - `verify.py` adds prior-wave tree-ID identity for round-20, round-21 and round-22, and checks that README non-empty lines survive in order.
- **F6, unquoted/relative `ls-tree`: closed for the new-entry scan, reintroduced in the new guard (G2).**
- **F4, git config and hooks: mostly closed.** Both `count-c1.py` and `verify.py` now set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_COUNT=1` with `core.hooksPath=/dev/null`, after the `GIT_*` scrub and before any git call.
  - Env-supplied config takes precedence over local config, so lane-local hooks are suppressed as well.
  - The clones' local config is fresh, which removes global filters, autocrlf and hooks from the clone and checkout steps.
  - Child counters (the R22 legacy counter and `pre-v3-counter.py`) re-scrub `GIT_*` and so drop these overrides. They only run read-only `rev-parse`/`show`/`ls-tree`, which run no hooks and apply no filters to `rev:path`, so no count impact follows.
  - Remaining gap: G1.
- **F3, census binding: partially closed.** The census now runs on the private clone with `--today 2026-10-21`, and the script's digest is recorded. Residual: G4.
- **Setup-error mapping:**
  - `count-c1.py` now catches `RuntimeError`, which is how `counter-fixtures.command()` reports git failures. A setup failure therefore exits 2, and `verify.py` adds a PATH git-shim control that expects exit 2 with `controlled_git_failure`.
  - `verify.py` gained a top-level handler for `OSError`, `ValueError` and `CalledProcessError`, mapping them to exit 2.
  - Residual: G3.

## Remaining concrete findings (4)

### G1 — The git attributes file is not neutralised for the `verify.py` clone checkout (provenance of executed bytes; [INFERENCE] about the host file, which I did not read)
- `GIT_CONFIG_GLOBAL=/dev/null` replaces only the global config files. When `core.attributesFile` is unset, git still reads the default `$XDG_CONFIG_HOME/git/attributes` (or `~/.config/git/attributes`).
- Several attributes need no config driver: `text`/`eol=crlf`, `ident` and `working-tree-encoding`. Any of them would rewrite the bytes that `git checkout rev` writes into the clone (`verify.py`, clone/checkout block). `verify.py` executes the counter, describe scripts and controls from that checkout, and records `source-pins.json` from the checkout bytes.
- Effect: digest-checked selftest inputs fail closed with exit 2 (`snapshot_tampered`). The after-c1 count still reads Git blobs, so it would not be falsely raised. However, the recorded pins and the "materialised from the named commit" code hashes would differ from the blob digests without anything flagging it.
- Smallest correction: add `GIT_CONFIG_KEY_1=core.attributesFile`, `GIT_CONFIG_VALUE_1=/dev/null` and `GIT_CONFIG_COUNT=2` in both files. Alternatively, set `XDG_CONFIG_HOME` to an empty private directory, or assert in `verify.py` that each executed file's sha256 equals that of `git show rev:<file>`.

### G2 — The inherited-knowledge guard is silently vacuous when `--root` is not the top level of the repo (possible false hold; observed in source)
- `knowledge_blobs` runs `git -C root ls-tree -r -z <ref> -- corpus/knowledge/` without `--full-tree`. Git interprets that pathspec, and limits the listing, relative to the working directory.
- With `--root <LANE>/corpus` (or any subdirectory), both the baseline and rev listings come back empty, so `historical_knowledge_changed` can never fire.
- Every other read keeps working, because `rev:path`, `r20.tree_entries --full-tree` and `r22.measure` all use paths from the top of the tree. The historical identify-flutter-build credit would then be counted even if a rev deletes or edits the R22 knowledge entries.
- This needs a misdirected `--root`. `verify.py` and the claims command both pass a top-level root.
- Smallest correction: add `--full-tree`. Alternatively, fail with exit 2 unless `git rev-parse --show-prefix` is empty.

### G3 — Some setup and predicate failures in `verify.py` still escape as exit 1 with no summary (error mapping; observed in source)
- The top-level handler catches only `OSError`, `ValueError` and `CalledProcessError`.
- **`pre-v3-red`:** `fixture_runner.run(clone, …)` calls `counter-fixtures.command()`, which raises `RuntimeError` on any git failure. That error is uncaught, so the run ends in a traceback with exit 1, which the docstring defines as "discrepancy". Its intended meaning is input failure, exit 2.
- **`signal_ok`:** `by_name = {row['name']: …}` and `by_name['decode-uart-hi']`, `['inventory']`, `['decode-official-uart']`, `['decode-invalid-decoder']` raise `KeyError` when a record is unnamed or missing. Because the predicate runs inside `record()` before the JSON is written, neither `signal-records.json` nor `summary.json` is produced.
- Smallest correction: add `RuntimeError` and `KeyError` to the handler. Better, have `signal_ok` use `.get` and return False, so the check is recorded as failed.

### G4 — The census "private committed clone" scope is asserted, not established by committed code (provenance; unverified)
- `census-tool.json` hard-codes `'input_scope': 'private committed clone; explicit date2026-10-21'`. The census itself is invoked as `sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-10-21 <clone>`.
- Whether the script reads `<clone>/corpus/SOURCES.md` rather than a lane under the live `--root`, and which tree it uses to resolve E11 dangling used-by, depends on an uncommitted script outside Git and outside this read set. Nothing recorded checks that scope.
- The script's digest is computed with a separate read before execution, so the hash and the executed bytes are not tied together.
- The record's `source_rev` stamp is only as true as that unverified scope.
- Smallest correction: pass `--file <clone>/corpus/SOURCES.md` (per the script's own usage line in the C review). Alternatively, record the path the script reports (the census stdout names the file it read) and assert that it is under the clone. Separately, execute a hashed private copy of the script.

## Not findings
- Pre-v3 red control semantics and the 25-case expectations belong to the Numerator seat.
- Unchanged R22 and R21 logic was not re-audited.
- Counter self-hash enforcement is excluded by the brief.

## Produced files
- `.ufo/waves/round-23/w2/ResidualGit.md`: this appendix (hash in the handoff).
- Scratch copies (ignored): `.ufo/waves/round-23/runtime/CriticGit/F-{count-c1.py,counter-fixtures.py,verify.py}`, byte-identical to `git show F:…` (digests in the table above).

## Installs
None.
