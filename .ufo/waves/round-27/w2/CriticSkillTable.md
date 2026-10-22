# CriticSkillTable — round 27, wave 2

Attacked: SKILL.md section "Evidence-ID identity under a renamed copy and on a second carrier — round 27"
(`SKILL.md:912-936` at lane tip 4084d8975b684a8837b1c858eea0008ce9ab49e0). Read-only on the lane.
REA was not run, because this item does not call for it. Package roots were read as files only. No installs.

Overall verdict: fails on three fixable wording points (checks 2, 3, 4) and one placement point (check 7).
The measured core holds (check 1).

## Checks

1. Rule 1 (map extensions through the suffix rule) against the table and envelopes: holds (observation).
   Command (15:37:08Z): `python3 -I -B counterfactual.py`. It loads `tools/round-26/recompute-ids.py`,
   compares the hashed leaves of the base and renamed envelopes, then rewrites only `normalized_result.document`. Exit 0.
   Excerpt: `DIFF jq analyze: 1 hashed leaves differ: ['.normalized_result.document']`, the same for inspect and tinyxxd;
   address verbs `0 hashed leaves differ`; `CF jq analyze document=target-e815667571d0.bin id=ev_14f9d92f…d328 equals_base=True`;
   `CF tinyxxd analyze document=target-7b1e5d0c970a.bin … equals_base=True`. Lane support: the round-26 replay
   `jq-renamed.bin` kept `ev_14f9d92f…` (`.ufo/waves/round-26/w2/ReplayRenamedCopy.md:26`, `SAME`).
   `.data.subject.digest.sha256` exists in `analyze` envelopes (jq paths query, 15:36:53Z, exit 0).

2. Rule 1 says "map each name's extension", which is wrong for symlinks on Linux and diverges on Windows: fails (inference from code; no live run).
   Commands (15:38:35Z and 15:39:28Z, exit 0): `sed -n 27,36p dist/application/BinaryTargetResolver.js`, `sed -n 8579p dist/cli-runtime/binary-BVOr2mgE.js`.
   Excerpts: `const canonical = await realpath(candidate);`, `const sourcePath = process.platform === "win32" ? candidate : canonical;`,
   `targetPath: installation.platform === "win32" ? target.sourcePath ?? target.path : target.path,`. On Linux, Ghidra snapshots the realpath.
   Node demo on scratch symlinks (15:39:28Z, `node_exit=0`):
   `{"typed":"links/jq-link.dat",…,"realpath":"/usr/bin/jq","suffix_typed":".dat","suffix_linux_rea":".bin"}` and
   `{"typed":"links/jq-link",…,"realpath":"…/jq-r27-renamed.dat","suffix_typed":".bin","suffix_linux_rea":".dat"}`.
   Counterexample: `analyze` on a `.dat` symlink to `/usr/bin/jq` should mint base `ev_14f9d92f…`. Rule 1 predicts a change.
   On Windows the typed name decides. The measured copies are regular files (`stat`: `regular file …jq-r27-renamed.dat`), so the table is unaffected.
   Correction: "the extension of the file's real path after symlinks are resolved (Linux); Windows uses the typed path and is unmeasured".

3. The lead sentence and table use "extension class" without defining it: fails as wording (observation; fixable).
   Text: "content-keyed across directories only while the file extension class stays the same"; the table cell reads "differs when the extension class differs (`.dat` against none)".
   Counterexamples: no extension and `.bin` both map to suffix `.bin`, so the id is unchanged (round-26 replay, check 1). `.dat` and `.DAT` give
   different ids (`CF jq analyze document=…DAT id=ev_a32ada96… equals_base=False`, and `.dat` → `ev_a60580a9…`).
   A case-insensitive reading of "class", or a "has an extension or not" reading, mispredicts both cases.
   Correction: replace "extension class" with "suffix after the `^\.[A-Za-z0-9]{1,12}$`-else-`.bin` mapping (case-sensitive)".

4. The table row says `inspect-binary-layout` ids differ "whenever the path string differs": overreaches (inference from code).
   Command (15:38:00Z, exit 0): `sed -n 8405,8440p dist/cli-runtime/cli.js`. Excerpt: `service.inspectAndClose({ path: resolve(args.path) }`.
   `BinaryLayoutService.js:61,67` hashes `parameters: input.data` and `locations … path: value.artifact.path`.
   Node (15:38:51Z, exit 0): `/usr/bin/../bin/jq` → `"resolve":"/usr/bin/jq"`; from `/usr/bin`, `resolve("jq")` → `/usr/bin/jq`.
   Counterexample: argv `./jq` (cwd `/usr/bin`) and argv `/usr/bin/jq` are different strings with the same hashed path, so the ids should be equal.
   `/bin/jq` stays distinct because `resolve` does not follow symlinks. Correction: "whenever the absolute path after lexical
   normalization (`path.resolve`, symlinks not followed) differs".

5. Overreach to other pins, other verbs or MCP: holds, with one fixable omission (observation).
   The table header pins `rea-agents@6.5.0`, and round-26 rule 1 already bars comparing ids across pins.
   6.7.0 has the same `safeExtension` (`tail -5 …a1722018…/GhidraTargetSnapshot.js`, 15:36:32Z, exit 0), and so does the MCP bundle
   (`dist/mcp/main-kBXHZ8S5.js:7142-7145`, 15:39:28Z). Neither is claimed. Only the eight named verbs appear.
   Omission: the entry's Limits (two carriers, one address, CLI only, no 6.7.0, MCP or error envelopes; directory, name and extension
   changed together, so the extension-only effect is inferred) are absent from the SKILL section, yet rule 1 is phrased without that scope.
   Correction: one sentence carrying those limits.

6. Rule 2 (do not rename a copy's extension unless it is under test): holds (observation).
   `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:120`: "The copy kept the file name `jq`".
   The rule is stricter than needed (no extension → `.bin` is harmless), but it is safe.

7. Rule 3 (a duplicate-bytes counter must allow two genuine runs): fails on placement and duplicate authority (observation).
   Command (15:39:15Z, exit 0): `rg -n "byte-identical|duplicate|shared" corpus/QUALITY.md`. Excerpt from row 40: "ships … a green selftest
   case for the legitimate look-alike … It tells duplicates apart by the call record (distinct `utc_start`, seat and output file)".
   That is the same rule, landed in the same round (97358f75), in the quality ledger that owns instrument rules. The SKILL copy
   is a second authority, and a weaker one: it names no discriminator, so a counter that simply drops the duplicate check satisfies it.
   This is a counter-design rule, not an evidence-id identity rule.
   Tradeoff that both texts leave unsaid: the round-27 lesson (`corpus/lessons/round-27.md:80`) records `utc_start` and seat as
   seat-written labels. A copied base envelope filed as a fake "repeat" row therefore passes a row-40 counter, and that forgery
   fakes exactly the base-equals-repeat stability the table reports.
   The REA fact itself holds: `sha256sum` of the tinyxxd layout base and repeat both give `f601872b…3130`, and `meta.duration` is `"132ms"` in both (15:37:42Z, exit 0).
   Correction: keep only the identity fact ("two genuine runs can return byte-identical envelopes; a fast verb repeats `meta.duration`")
   and point to QUALITY row 40 for the counter rule.

8. Contradiction with the round-26 section above: holds (observation). Line 914 says "This section narrows the round-26
   table above for `analyze` and `inspect`". The round-26 claim "content-keyed across directories" is literally still true.
   Unflagged leftovers elsewhere in SKILL.md: Known limits (r4) at `SKILL.md:411-412` still reads "`analyze`/`inspect` and
   `analyze_function` ids stayed equal across paths", with no qualifier and no pointer. The round-26 cell
   "compare ids" (`SKILL.md:894`) has no forward note either. Correction: append "(same suffix only; see round 27)" to both.

9. Mechanism provenance: holds, with a note (observation). The CLI's `bin` is `scripts/rea.mjs`, and the call site is the bundled copy
   `dist/cli-runtime/binary-BVOr2mgE.js:5944`. Its `safeExtension` (`:5316-5319`) matches the cited `dist/ghidra/GhidraTargetSnapshot.js:76-78`,
   which has sha256 `a27e4107…f52b` and agrees with the entry (15:35:26Z, exit 0). Citing the bundle line too would point at the code that actually runs.

## Impacted axes
Correctness of decision rules (checks 2, 3, 4), scope honesty (check 5), single authority (check 7), stale contradiction (check 8).

## Smallest safe correction (all in `SKILL.md:912-936`, plus two qualifiers)
Define the suffix on the realpath with case-sensitive mapping (Windows uses the typed path, unmeasured). Restate the layout row as "absolute
path after `path.resolve`". Add the entry's Limits sentence. Replace rule 3 with the REA fact plus a pointer to QUALITY row 40. Qualify `SKILL.md:411-412` and `:894`.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r27/seats/w2/CriticSkillTable/`)
- `counterfactual.py` 4489f54199446b09c10b0a4e177f4977e0b7dc8b4e088c9a5d7217c151891b89
- `cf.out` 16f66ae3d61fbe13313e0d30f4507a02b11dfbec31668e975cb4b473e4b9e033
- `code-trace.out` fd83ab03cf3f1ab578d5894abed27a89f6b623e909b15ff62d30d7212f259edc
- `links/jq-link.dat` → `/usr/bin/jq` and `links/jq-link` → `…/carrier/renamed/jq-r27-renamed.dat` (symlinks, no content of their own)

Unknown: no live REA run confirms checks 2 and 4. They rest on reading the 6.5.0 code and on Node's own `realpath` and `resolve`.
A live check would run `analyze` on `links/jq-link.dat` and expect `ev_14f9d92f…d328`.
