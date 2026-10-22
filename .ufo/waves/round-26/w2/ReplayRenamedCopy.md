# ReplayRenamedCopy — renamed-copy probe of the entry limit "sensitivity to a different file name was not tested"

Seat: KaidokuR26.ReplayRenamedCopy, wave 2 (falsify), 2026-10-22. Target: the Limits sentence in
`corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`: "The copy kept the file
name `jq`, so the table shows directory-insensitivity at an identical file name; sensitivity to a
different file name or extension was not tested." Method: byte-identical copy of `/usr/bin/jq`
under a new name and extension, the four assigned verbs with the frozen argv from
`.ufo/waves/round-26/claims.json` `verbs_argv`, ids compared with `corpus/evidence/round-26/c1/table.tsv` base ids.

## Inputs and custody

- Copy: `/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReplayRenamedCopy/jq-renamed.bin`, sha256
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, 30,800 bytes — equals the
  carrier pin in claims.json (`/usr/bin/jq` measured same digest and size, command `sha256sum` +
  `stat`, 2026-10-22T13:00:08Z, exit 0). Observation.
- Table bytes judged: commit `ebe2cb4a` (`git show ebe2cb4a:corpus/evidence/round-26/c1/table.tsv |
  sha256sum` → `89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df`), identical to the
  working-tree file; `git diff --stat ebe2cb4a HEAD -- corpus/evidence/round-26/c1/` empty. Observation.
- Invocation per contract: `TMPDIR=<seat>/tmp npx -y rea-agents@6.5.0 <argv>` from the login shell
  (`GHIDRA_INSTALL_DIR` set, 7 `REA_*` variables present). No tools installed. Read-only lane access only.

## Per-verb results (all `--format json --full-output`, path = the renamed copy)

| verb | frozen argv (path elided) | exit, UTC start–end | id at renamed path | vs table base_id |
|---|---|---|---|---|
| analyze | `analyze <P>` | 0, 13:00:36Z–13:00:42Z | `ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328` | SAME |
| decompile | `decompile <P> 0x103fa0` | 0, 13:00:53Z–13:00:59Z | `ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df` | SAME |
| function | `function <P> 0x103fa0` | 0, 13:01:38Z–13:01:43Z | `ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5` | SAME |
| inspect-binary-layout | `inspect-binary-layout <P>` | 0, 13:01:56Z–13:01:57Z | `ev_6a4412e2830767f19089b65ee740cc74d23dae12e0fcee825eaf5588d6a71f81` | DIFFERENT |

Base ids taken from table.tsv: analyze `ev_14f9d92f…b3d328`, decompile `ev_03d78618…6014df`,
function `ev_b2b7e9e4…0488b5`, inspect-binary-layout `ev_294a449c…0a71bd`. Every envelope had
`ok: true` and `.data.subject.digest.sha256` = `e8156675…7806`; stderr files are 0 bytes. The
layout envelope carries the renamed path in all three projection-reachable fields
(`.data.subject.local_path`, `.data.parameters.path`, `.data.normalized_result.artifact.path`). Observation.

## Verdict on the entry's limit sentence

1. As a description of the round's coverage the sentence is ACCURATE. Observation: all three runs per
   table row used basename `jq` (copy rows ran `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`,
   runs.tsv); a grep of `.ufo/waves/round-26/w1/` for rename/name/extension finds no renamed run —
   ReplayA.md: "Not tested: a renamed copy (the entry says so too)", and PredictionCritic.md had
   flagged "The copy run cannot detect basename or extension sensitivity". No wave-1 seat closed the gap.
2. The gap the sentence discloses is now partially closed, and no counterexample to the entry
   appeared: for the three tested content-keyed verbs the id is unchanged under a different file
   name AND extension, so the entry's content-keyed verdicts (and its Use advice to compare ids for
   the seven verbs) extend to renamed copies for at least analyze, decompile and function.
   Inference from observation.
3. `inspect-binary-layout` returned a fourth distinct id at a fourth distinct path (`ev_6a4412e2…`,
   vs base `ev_294a449c…` at `/usr/bin/jq` and copy `ev_52da4b3d…` at `…/alt/jq`), i.e. the
   path-sensitive verdict holds under a rename too; its id keys the run path, not the name or bytes.
   Observation.
4. Mechanism check agrees with the entry's Why section: the three unchanged verbs never see the
   caller path (Ghidra imports a content-named copy), while BinaryLayoutService writes the run path
   into kept fields; the observed SAME/DIFFERENT split matches that model exactly. Inference, from
   the observed ids plus the entry's source citations.

## Limits of this probe

One carrier, one pin (6.5.0), one probe per verb, single run (no repeat; determinism at the same
path is already established by the round's base/repeat rows). Name and extension changed together
(`jq` → `jq-renamed.bin`), so sensitivity to a name change alone versus an extension change alone is
not separated. The four other content-keyed verbs (inspect, xrefs, read-bytes, instructions) were
not in scope. Conclusions are per tested verb only.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReplayRenamedCopy/`)

- `jq-renamed.bin` — `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`
- `out/analyze.json` — `c67cfeab1c4eeb94294f77527ea8aa10c7fc4139d9a138a4961ab83980488480`
- `out/decompile.json` — `adffc0bcc0409144a883eb4396c93bbfdb21df0e36d2f40e1053a748b8cf80dc`
- `out/function.json` — `e6afa2aeb3df97147c544c0b9c0399b403dec7db7e273fd76c9253fc5ac5102e`
- `out/inspect-binary-layout.json` — `5463aeaf0d93b5cf83178048e7c15094c98b45fdc53aead8ef0c9bc995b917d0`
- `out/<verb>.err` — four files, 0 bytes each (stderr empty)

Recommendation to the L1: the limit sentence is accurate and honest; if the entry is ever revised,
this probe (ids above, artifacts hashed here) supplies the missing name+extension data point for
three of the seven content-keyed verbs and for the path-sensitive verb, with no change to any
table verdict.
