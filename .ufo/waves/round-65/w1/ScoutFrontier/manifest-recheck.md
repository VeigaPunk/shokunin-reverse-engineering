# R65-C1 closure manifest — independent re-derivation (ScoutFrontier, r65 w1)

Derivation, not the instrument: the `CLOSURE` literal and the three singleton pins
(`PROBE_PIN`, `NODE_PIN`, `INTERPRETER_PIN`, with `NODE_PATH`, `INTERPRETER_PATH`) were
extracted from `tools/round-65/jsc-closure-matrix.py` by `ast.parse` + `ast.literal_eval`
of the module source (no import, so no bytecode is written), then every path was hashed
with `hashlib.sha256` in 1 MiB chunks. `closure_findings()` was not called.

Instrument bytes at the time of this check:
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6  tools/round-65/jsc-closure-matrix.py`

Command (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`), exit 0:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B - <<'EOF'   # ast.literal_eval(CLOSURE) + sha256 per entry
EOF
```

Result line: `ENTRIES 30 CLOSURE_DICT 27` / `MISMATCHES 0 []`
(27 toolchain-root-relative entries + probe + node + interpreter = the 30 the plan calls
"Closure (30 pinned entries)", matching `closure_findings()`'s own `len(CLOSURE) + 3`.)

## Mismatch count: 0 of 30

| # | entry (root = `/home/vgpnk/.local/share/kaidoku-jsc`) | frozen sha256 | recomputed sha256 | verdict |
|---|---|---|---|---|
| 1 | `d8-14.8.178.14/d8` | `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` | `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` | ok |
| 2 | `d8-14.8.178.14/snapshot_blob.bin` | `b5c418dc0c6006d8dc6f4ac9981182eecf783cd892ae4c4b4ba16977c17bf2bb` | `b5c418dc0c6006d8dc6f4ac9981182eecf783cd892ae4c4b4ba16977c17bf2bb` | ok |
| 3 | `d8-14.8.178.14/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | ok |
| 4 | `d8-14.8.178.1/d8` | `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` | `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` | ok |
| 5 | `d8-14.8.178.1/snapshot_blob.bin` | `601efdc639d9f439cca3d1274e0917ab28ee09d6870787d6052d8949fa73e24d` | `601efdc639d9f439cca3d1274e0917ab28ee09d6870787d6052d8949fa73e24d` | ok |
| 6 | `d8-14.8.178.1/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | ok |
| 7 | `d8-14.7.173/d8` | `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` | `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` | ok |
| 8 | `d8-14.7.173/snapshot_blob.bin` | `80590f459ddbac237de5f282196b2c551e24982f31150cb8998a3b4898ea2720` | `80590f459ddbac237de5f282196b2c551e24982f31150cb8998a3b4898ea2720` | ok |
| 9 | `d8-14.7.173/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | ok |
| 10 | `jsc2js-src/View8/view8.py` | `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c` | `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c` | ok |
| 11 | `jsc2js-src/View8/README.md` | `557d14a20a622d42f620547b19c41d2f7224bc264f6fc22f64bedb4164efcf50` | `557d14a20a622d42f620547b19c41d2f7224bc264f6fc22f64bedb4164efcf50` | ok |
| 12 | `jsc2js-src/View8/Bin/VersionDetector.exe` | `61347ee8eddcbe2c77229bc3f8ee8ccc9437e31710afbfc33b5ace886747c95e` | `61347ee8eddcbe2c77229bc3f8ee8ccc9437e31710afbfc33b5ace886747c95e` | ok |
| 13 | `jsc2js-src/View8/Parser/parse_v8cache.py` | `98ffc4b5b638f955f45fb219b1934a03a03a921fc4c18fcea6f08d495dcc3bc5` | `98ffc4b5b638f955f45fb219b1934a03a03a921fc4c18fcea6f08d495dcc3bc5` | ok |
| 14 | `jsc2js-src/View8/Parser/sfi_file_parser.py` | `7ce34163cace6e818f405d0177400c0d24fab36e35644c893e8437dccae444a1` | `7ce34163cace6e818f405d0177400c0d24fab36e35644c893e8437dccae444a1` | ok |
| 15 | `jsc2js-src/View8/Parser/shared_function_info.py` | `b5c79cdd27fdc2a2480a7b34a5142bd83b92ddda9f563f99d34a5f987d1aae2e` | `b5c79cdd27fdc2a2480a7b34a5142bd83b92ddda9f563f99d34a5f987d1aae2e` | ok |
| 16 | `jsc2js-src/View8/Simplify/function_context_stack.py` | `51b6f4f50c45741626ad3a9ad4ddc199ff0288d51c662d18001fd2d2f4f9a810` | `51b6f4f50c45741626ad3a9ad4ddc199ff0288d51c662d18001fd2d2f4f9a810` | ok |
| 17 | `jsc2js-src/View8/Simplify/global_scope_replace.py` | `0f217057142f07503780265d1d13488bfa26ac24ee97a4a1438565017d2fe16e` | `0f217057142f07503780265d1d13488bfa26ac24ee97a4a1438565017d2fe16e` | ok |
| 18 | `jsc2js-src/View8/Simplify/simplify.py` | `9603ff0fc837720cbb39cc3b27ba1a7e707dba76d3f05203bfb623f746402cf7` | `9603ff0fc837720cbb39cc3b27ba1a7e707dba76d3f05203bfb623f746402cf7` | ok |
| 19 | `jsc2js-src/View8/Translate/jump_blocks.py` | `ab0acbff954a1424f3c0804b0942ad84372c5d510b8ae299ae0621cdbf33f044` | `ab0acbff954a1424f3c0804b0942ad84372c5d510b8ae299ae0621cdbf33f044` | ok |
| 20 | `jsc2js-src/View8/Translate/translate.py` | `0e07589374ad38541c2edaf9867e7dc8ad4636eb6dff3532ea62503a01ff9f78` | `0e07589374ad38541c2edaf9867e7dc8ad4636eb6dff3532ea62503a01ff9f78` | ok |
| 21 | `jsc2js-src/View8/Translate/translate_table.py` | `717e2a67c3792b09160082efa50f0553f35ef197293e625bf653dedb382cf4a3` | `717e2a67c3792b09160082efa50f0553f35ef197293e625bf653dedb382cf4a3` | ok |
| 22 | `venv/lib/python3.15/site-packages/parse/__init__.py` | `27ddec2fdfc9a5a97d8086eb4c073f3f9a3c7a8e5086c13adc198114ac6ba8c0` | `27ddec2fdfc9a5a97d8086eb4c073f3f9a3c7a8e5086c13adc198114ac6ba8c0` | ok |
| 23 | `venv/lib/python3.15/site-packages/parse/__init__.pyi` | `0ada9b911ad08edcbb9d8e06fc57033fdc2eb93bd4e978ffae53af928c0d4f00` | `0ada9b911ad08edcbb9d8e06fc57033fdc2eb93bd4e978ffae53af928c0d4f00` | ok |
| 24 | `venv/lib/python3.15/site-packages/parse-1.22.4.dist-info/METADATA` | `e4179e24374e7084ebe589092e44bf2c8aa03cfec9756a56fcaa98a056bb232c` | `e4179e24374e7084ebe589092e44bf2c8aa03cfec9756a56fcaa98a056bb232c` | ok |
| 25 | `venv/lib/python3.15/site-packages/parse-1.22.4.dist-info/RECORD` | `58aa77c758d4c307da016a6e4db5011d7069bfa1053c836235cce94e7b2bd8c6` | `58aa77c758d4c307da016a6e4db5011d7069bfa1053c836235cce94e7b2bd8c6` | ok |
| 26 | `venv/pyvenv.cfg` | `87a6b46ee1f9261cabbe8efb4b60639c50dfc14d77157fd670390e411152f335` | `87a6b46ee1f9261cabbe8efb4b60639c50dfc14d77157fd670390e411152f335` | ok |
| 27 | `inputs/atom.compiled.dist.jsc` | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` | ok |
| 28 | **probe** `.ufo/waves/round-64/inputs/probe-electron.jsc` (repo-relative) | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` | ok |
| 29 | **node** `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node` | `7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c` | `7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c` | ok |
| 30 | **interpreter** `/home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15` | `aac3ade3f7d90fbf63e3ea0c46120a0cfbd159e1e503dde04721979507a1548b` | `aac3ade3f7d90fbf63e3ea0c46120a0cfbd159e1e503dde04721979507a1548b` | ok |

Missing: 0. Pin mismatch: 0.

## Cache state of the toolchain root (`cache_entries(root)` scope)

```
$ find /home/vgpnk/.local/share/kaidoku-jsc \( -name '__pycache__' -o -name '*.pyc' \) -print | wc -l
0
```

Exit 0, empty output: no `__pycache__` directory and no `*.pyc` anywhere under the root.
The four directories named in `.ufo/waves/round-65/prep/precache-dirs.txt`
(`jsc2js-src/View8/{Parser,Simplify,Translate}/__pycache__`,
`venv/lib/python3.15/site-packages/parse/__pycache__`) are all gone.

Scope note (observed, not a predicate failure): a bytecode cache **does** exist outside the
root, at `tools/round-65/__pycache__/` in the lane repo — see `w1/ScoutFrontier.md` §2.

## Interpretation

Clause (i) of the frozen predicate — "the frozen closure manifest matches every one of its
entries (count and sha256) with no Python bytecode cache present before the first run" — is
satisfied by the tree as measured, on the root scope the instrument itself checks
(`cache_entries(root)` at `tools/round-65/jsc-closure-matrix.py:244`). Clauses (ii) and (iii)
are the matrix run's to establish; this file measures nothing about labels or the census.
