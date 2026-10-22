# ReviewQuality37 — routed defect 1: r26 entry and QUALITY row 37 say analyze/inspect ids are content-keyed without the suffix condition

Reviewed 2026-10-22 (run window 18:26:28Z). Read-only; no lane files written except this report; no installs; no network sources opened. All line numbers are working-copy positions at review time. Lane HEAD moved during the run: dispatch tip a2673116 → 9db24c9e ("round-28: R28-C2 and R28-C1 knowledge entries, SOURCES S084-S086 ..., QUALITY rows 41-43, pre-freeze hex screen", `git log --oneline a2673116..9db24c9e`, exit 0).

## Verdict

- The r27 entry already states the condition correctly: **holds**, taken as a whole (main statement plus its own wave-2 corrections).
- Routed defect 1, half 1 ("Add a QUALITY row superseding row 37"): **done and committed** — row 41 at QUALITY.md:51 is in commit 9db24c9e (`git show 9db24c9e:corpus/QUALITY.md | grep -c "Supersedes row 37"` → 1, exit 0; at a2673116 the same grep gave 0, exit 1).
- Routed defect 1, half 2 ("Append a round-27 pointer to the r26 entry, table rows analyze/inspect and Use"): **drafted correctly in the working copy** (r26 entry :137-146, section "## Pointer appended in round 28 (routed defect 1 of corpus/lessons/round-27-verifier-spotcheck.md:152)") but **not yet committed**: `git show 9db24c9e:corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md | grep -c "Pointer appended"` → 0, exit 1. The L1 still needs to commit it.
- Attack verdict on the drafted pointer text and on row 41: **holds**. The condition they state matches the r27 entry and the installed 6.5.0 code; two nuances are omitted but live in their citations (see Residual risk).

## Sentences that need the pointer (path:line)

All in `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`:

1. `:32` — table row: "| `analyze` | base = repeat = copy, `ev_14f9d92f…b3d328` | content-keyed |". Needs the pointer: "content-keyed" there is suffix-conditional.
2. `:33` — table row: "| `inspect` | base = repeat = copy, `ev_14f9d92f…b3d328` (the same id as `analyze`) | content-keyed |". Same need.
3. `:110` — Use bullet: "To show two envelopes from these seven verbs came from the same bytes and request, compare ids". Needs the pointer: for `analyze`/`inspect`, equal bytes and request are not sufficient; both paths must also map to the same snapshot suffix.

Does not need the pointer:

- `:113` ("An equal id between `analyze` and `inspect` is expected...") — a same-run same-path statement; suffix equality is trivial there. The routed defect names "table rows `analyze`/`inspect`, `## Use`"; `:110` is the Use sentence.
- QUALITY row 37 (`corpus/QUALITY.md:47`) is deliberately left as written: the QUALITY header rule is "replaced by a new row naming the row it supersedes, never rewritten", and row 41 (`:51`) carries the supersession. Row 41 itself records "Row 37 stays true within its scope (same file name, other directory)".
- The r26 Limits (`:120-121`, "directory-insensitivity at an identical file name") already scope the claim honestly; the spot-check ruled the sentences not false, only incomplete (`corpus/lessons/round-27-verifier-spotcheck.md:112`).

## The exact condition

The `analyze`/`inspect` id is equal across two paths of the same bytes only when both paths map to the same Ghidra snapshot suffix. The snapshot name is `target-<sha256[0:12]><suffix>`; the suffix is the path's extension when it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin`.

Evidence pointers:

- Canonical lane statement: `corpus/QUALITY.md:51` (row 41, committed at 9db24c9e).
- r27 entry `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`: `:44-50` (mechanism; snapshot name and suffix rule at `:45-47`), `:71-72` (decision-rule rows) and `:75-76` ("content-keyed across directories only while the extension class stays the same").
- Primary source, verified this round from the installed bytes (package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`):
  - `dist/ghidra/GhidraTargetSnapshot.js:13-14`: "const suffix = safeExtension(sourcePath);" / "const snapshotPath = join(runtimeRoot, `target-${expectedSha256.slice(0, 12)}${suffix}`);" and `:76-78`: "return /^\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : \".bin\";". sha256 `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b` (sha256sum, exit 0, 18:26:28Z) — byte-identical to the S083 record (`corpus/SOURCES.md:89`).
  - Bundled runtime the CLI actually runs, `dist/cli-runtime/binary-BVOr2mgE.js`: snapshot name at `:5261`, `safeExtension` regex at `:5316-5318` (the entry cites `:5318`). sha256 `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df` — byte-identical to the sha the r27 entry correction bullet records (`:100-102`).

## Confirmation detail (observation)

The r26 entry `:122-124` records a falsify-wave replay: a copy named `jq-renamed.bin` kept the `analyze` table id, which the entry left unexplained ("name and extension changed together"). The suffix rule predicts exactly that: base `/usr/bin/jq` has no extension → `.bin`; `jq-renamed.bin` → `.bin`; same suffix, same id. The r27 condition explains a result the r26 entry could not.

## Verdict on whether the r27 entry already states it correctly

Holds. The statement `:45-47`, the decision rule `:71-76`, the live falsifications `:113-116` and the entry's own corrections are mutually consistent and match the installed code. One wording caveat a citation should respect: the main-text sentence `:46` ("the suffix is the caller's extension") is intentionally over-wide and is narrowed by the entry's own appended corrections `:104-107` — on Linux the path is resolved with `realpath` (`binary-BVOr2mgE.js:293`) so a symlink's own extension is ignored, and the rule is case-sensitive (`.dat` vs `.DAT` differ). The entry is correct as a whole; a pointer that quotes only `:46` without the corrections would overstate.

## Residual risk and verification gaps

- The r26-entry pointer is working-copy only at review time (grep at HEAD 9db24c9e gave 0, exit 1). Uncommitted drafts can still change; `:137-146` are working-copy positions that will shift once committed.
- The drafted pointer (`:143-144`) and row 41 use the shorthand "a copy with another extension gets another id". Strictly the mapping comes first: two different extensions that both fail the regex both map to `.bin` and keep the id. Both texts state the mapping in the immediately preceding sentence, so they are internally correct; read alone, the shorthand could mislead. The drafted pointer also omits the realpath/case nuance and the route-changing-extension caveat (`:108-112` of the r27 entry, e.g. `.asar`/`.zip` change `subject.format` by route, not by suffix); both are covered because the pointer cites the r27 entry and S083.
- The realpath symlink behavior is read from code, not run (the r27 entry says so at `:104-107`); I did not run it either.
- No lsp server applies: every artifact here is markdown prose plus installed JS read directly with line-cited windows, so text-level line checks are exact; grep was used only for line numbering and commit-state counts, never as semantic proof.
- Producing commands with exit codes are quoted above (log: exit 0; grep counts at a2673116: 0/0 exit 1; at 9db24c9e: 0 then 1; sha256sum: exit 0); all reads ran in the 2026-10-22T18:26:28Z window.
