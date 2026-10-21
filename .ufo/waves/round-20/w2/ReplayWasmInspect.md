HOLDS — the assigned qcms `inspect-wasm-artifact` replay reproduces the retained result.

**Observation — source revision S and replay.** At S=`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`, the C2 claim names `inspect-wasm-artifact` and requires retained evidence ID and subject SHA (`.ufo/waves/round-20/claims.json:24-30`); the lesson lists this as a first-held verb (`corpus/lessons/round-20.md:14-16`). The retained qcms receipt records exit 0, stdout size 1,541,224 bytes, SHA-256 `a625f911e66513bee1921eb26d3f172fcb9067909220055e80cb38839f7f86b9`, carrier SHA-256 `6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26`, and Evidence ID `ev_4b405f45646e4f950cd835ac59af82e32c556f998ef1bd3a2628d998ea5f0225` (`evidence/c2/wasm-inspect/qcms/receipt.json:18-23,29-41` at S). Its normalized result is retained at `evidence/c2/wasm-inspect/qcms/stdout.json:1` at S.

Replay, from cwd `/tmp/tmp.MAkAu1zLIt` (mkdtemp outside the lane), with stdout captured there:
```sh
REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin npx -y rea-agents@6.5.0 inspect-wasm-artifact /opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/qcms_bg.wasm --format json > /tmp/tmp.MAkAu1zLIt/replay.stdout.json; rc=$?; printf 'CLI_EXIT=%s\n' "$rc"; wc -c /tmp/tmp.MAkAu1zLIt/replay.stdout.json; exit "$rc"
```
Observed output: `CLI_EXIT=0`; `1541224 /tmp/tmp.MAkAu1zLIt/replay.stdout.json`. `sha256sum /tmp/tmp.MAkAu1zLIt/replay.stdout.json` returned `a625f911e66513bee1921eb26d3f172fcb9067909220055e80cb38839f7f86b9`, identical to the retained receipt's stdout digest.

The retained and replayed normalized projections `{evidence_id, sections, imports, exports}`, extracted with `jq -S -c` and hashed with `sha256sum`, both yielded `f079f0b20461559fe4995411916d123e8ce8da1fcce7c4e5816f0f586885a4b2` (`PIPE_EXIT=0` for each extraction). Both summaries report Evidence ID `ev_4b405f45646e4f950cd835ac59af82e32c556f998ef1bd3a2628d998ea5f0225`, subject SHA-256 `6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26`, 13 sections (`Type, Import, Function, Table, Memory, Global, Export, Elem, DataCount, Code, Data, Custom, Custom`), 5 imports, and 23 exports. The field projection hash and full stdout digest match, so the requested evidence ID, section list, import list, and export list are identical to the retained S evidence.

Exact comparison commands (each printed exit 0):
```sh
set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/c2/wasm-inspect/qcms/stdout.json | jq -S -c '{evidence_id,sections:.normalized_result.sections,imports:.normalized_result.imports,exports:.normalized_result.exports}' | sha256sum; rc=$?; printf 'PIPE_EXIT=%s\n' "$rc"
set -o pipefail; jq -S -c '{evidence_id,sections:.normalized_result.sections,imports:.normalized_result.imports,exports:.normalized_result.exports}' /tmp/tmp.MAkAu1zLIt/replay.stdout.json | sha256sum; rc=$?; printf 'PIPE_EXIT=%s\n' "$rc"
sha256sum /tmp/tmp.MAkAu1zLIt/replay.stdout.json; rc=$?; printf 'SHA256_EXIT=%s\n' "$rc"
```

**Inference / limit.** This supports reproducibility of this qcms inspection on the observed carrier and WABT 1.0.42; it does not independently establish the breadth of C2's other target verbs. No tool was installed or updated.

Recorded: 2026-10-21T04:11:24-03:00.
