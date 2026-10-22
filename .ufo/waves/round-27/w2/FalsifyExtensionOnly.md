# Round 27, wave 2: falsifying the extension rule (FalsifyExtensionOnly)

Window: 2026-10-22, 15:37:06Z to 15:41:03Z (UTC).

## 1. Verdict

Claim attacked (`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`, "Why" and "Limits"): at REA 6.5.0 the `analyze` evidence id of a copy of jq follows the file extension, not the file name or the directory.

**Holds** for both copies run. The name-only copy has the base id, and the `.dat` copy has the predicted id. No mismatch and no counterexample. Parts not tested are in section 5, marked could-not-evaluate.

## 2. Setup

- Target `/usr/bin/jq`: 30800 bytes, sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. Prefix `e8156675` and suffix `7806` match. (`sha256sum`, exit 0, 15:37:06Z.)
- Copy A, other directory, other name, no extension: `.../FalsifyExtensionOnly/dir-a/renamed-tool`.
- Copy B, other directory, name `jq`, extension `.dat`: `.../FalsifyExtensionOnly/dir-b/jq.dat`.
- Both copies made with `cp`. Each matched `/usr/bin/jq` under `cmp` and sha256 (15:37:23Z).
- REA, one call per target: `TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/w2/FalsifyExtensionOnly/tmp npx -y rea-agents@6.5.0 analyze <PATH> --format json --full-output`.
- Package pins read after the runs (15:39:21Z): rea-agents 6.5.0 `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` (the value the lane entry records); `dist/ghidra/GhidraTargetSnapshot.js` `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b` (recorded value, unchanged); `dist/domain/evidence.js` `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`.
- Installs and updates: none. Existing tools only: npx 11.19.0, node v24.21.0, python3 3.14.8.

## 3. Results

All three REA runs exited 0 with empty stderr. Excerpt from `compare.py` output: `id matches prediction: True`.

| Run | Target | evidence_id | normalized_result.document | Versus prediction | Envelope sha256 |
|---|---|---|---|---|---|
| Copy A | dir-a/renamed-tool | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | target-e815667571d0.bin | Matches the base id | 5ca7d470e6998fd8136534168cbffb8bbb87a05991d8477fca9c841069406b82 |
| Copy B | dir-b/jq.dat | ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2 | target-e815667571d0.dat | Matches the .dat id | fc47066a1f54a75079d963ecd3491aff492bbf22a5599d1fe3703acf8a6d3b9a |
| Control | /usr/bin/jq | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | target-e815667571d0.bin | Base id confirmed at this pin | 1e34604df09e5676ad0c4e58b148feabb7614a526282a52a09b3560269c5ce54 |

Times (UTC): copy A 15:37:29Z to 15:37:35Z; copy B 15:37:38Z to 15:37:44Z; control 15:37:47Z to 15:37:53Z. The subject sha256 is `e815667571d0...` in all three.

## 4. Checks on the envelopes

- `compare.py` (exit 0, 15:38:46Z) compares all 251 leaves of each envelope against the control.
  - Copy A: 3 leaves differ, none inside the id: `data.subject.name` (jq to renamed-tool), `data.subject.local_path`, `meta.duration` (5225ms to 5048ms).
  - Copy B: 5 leaves differ: `data.evidence_id` (the output itself), `data.normalized_result.document` (`.bin` to `.dat`, the only differing leaf the id hashes), `data.subject.name`, `data.subject.local_path`, `meta.duration`.
- `recompute_ids.py` (exit 0, 15:41:03Z) rebuilds each id from its envelope. It takes SHA-256 over sorted-key canonical JSON of the part of the envelope the id hashes (`dist/domain/canonicalDigest.js:8-26`, `dist/domain/evidence.js:156-182`). It reproduces all three stored ids exactly.
  - What-if 1: the control envelope with only `document` changed to `target-e815667571d0.dat` gives `ev_a60580a9...3cd2`, the predicted id. The document value alone explains the change.
  - What-if 2: the control envelope with only `subject.name` and `subject.local_path` changed keeps `ev_14f9...d328`.
- Mechanism, read from code and not run (`dist/ghidra/GhidraTargetSnapshot.js:13-14` and `:76-79`): the snapshot is named `target-<first 12 hex of sha256><suffix>`. The suffix is the caller's extension when it matches `^\.[A-Za-z0-9]{1,12}$`, otherwise `.bin`. The `document` value is that snapshot name. All three observed values follow this rule.

## 5. Verdict per point attacked

| Point | Verdict | Basis |
|---|---|---|
| Other directory, other name, no extension keeps the base id | holds | Copy A id equals control id and predicted id |
| Name `jq`, extension `.dat`, other directory gets the predicted id | holds | Copy B id equals predicted id |
| Extensions that differ after mapping (`.bin` against `.dat`) give different ids | holds | Copy B against control; subject digest equal |
| Extensions equal after mapping (none against none) give equal ids | holds | Copy A against control |
| Name and path stay out of the id | holds for these copies | Section 4 leaf diffs and what-if 2 |
| Base id at this pin is ev_14f9...d328 | holds | Control run at 15:37:47Z |
| Extension outside the regex maps to `.bin` | could-not-evaluate live | Code only (`GhidraTargetSnapshot.js:76-79`) |
| Directory alone does not enter the id | could-not-evaluate in this check | Never varied alone here (section 6, item 1) |

## 6. Residual risk and gaps

1. Directory was never varied alone. Copy A changed directory and name; copy B changed directory and extension. Round 26 recorded a same-name, no-extension copy in another directory keeping the id (`.ufo/waves/round-26/w1/RunAnalyzeInspect.md`, line 41). That is cited, not re-run here.
2. Only two extension cases ran (none, and `.dat`). Not run: an extension outside the regex, an explicit `.bin` (the code predicts the base id), upper-case extensions, and names with several dots.
3. Envelope sha256 values identify these three files only. The envelopes carry `meta.duration`, so a rerun would probably change the hash [INFERENCE]. The evidence ids are the stable values.
4. No `target-*` snapshot file remained under TMPDIR (glob run after 15:39:21Z found none). Where REA wrote or removed the snapshot was not checked.
5. One control run on `/usr/bin/jq` was added beyond the two copy runs. The item allows that target, and the leaf diffs need a same-session reference.
6. Not run: rea-agents 6.7.0, the inspect verb, tinyxxd, MCP sessions.
7. For the lead: the lane entry's "Limits" paragraph says no separate extension-only or name-only run existed. Copies A and B now provide one each, though each also varies the directory. Apart from this report, no lane file was changed.

## 7. Commands (all exit 0)

- `sha256sum /usr/bin/jq` at 15:37:06Z. `cp` of both copies and `cmp` of each at 15:37:23Z.
- Three `TMPDIR=<tmp> npx -y rea-agents@6.5.0 analyze <PATH> --format json --full-output > out/<name>.json 2> out/<name>.stderr` calls, times in section 3.
- `python3 -I -B compare.py > out/compare.txt` at 15:38:46Z. `python3 -I -B recompute_ids.py > out/recompute.txt` at 15:41:03Z.

## 8. Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/w2/FalsifyExtensionOnly/)

- `compare.py` sha256 `127b28f67e74af37587c29cd83596a699b6955770d89f078f087ff5cfe76679e`
- `recompute_ids.py` sha256 `57be3442b2c4c1ab2c380cbeab25be7b4b84809eafe1bf4de69b8f316b3b1437`
- `out/copy1-noext.json` sha256 `5ca7d470e6998fd8136534168cbffb8bbb87a05991d8477fca9c841069406b82`
- `out/copy2-dat.json` sha256 `fc47066a1f54a75079d963ecd3491aff492bbf22a5599d1fe3703acf8a6d3b9a`
- `out/control-usrbin-jq.json` sha256 `1e34604df09e5676ad0c4e58b148feabb7614a526282a52a09b3560269c5ce54`
- `out/*.stderr` (three files, all empty) sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `out/compare.txt` sha256 `423320de2e6de2380f62b5bde7cb5fc63a775b0215ed0db9dfa97a289439b599`
- `out/recompute.txt` sha256 `c4864c14b1ceea670a207d5575db6bd7e979270c303650c38a5e1d55c92a9198`
- `dir-a/renamed-tool` and `dir-b/jq.dat` (copies) sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` each
- `tmp/` holds only Node's compile cache (listed at 15:39:21Z), not hashed.
