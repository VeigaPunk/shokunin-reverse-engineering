# ReopenS091 — round 30, wave 2

Seat `KaidokuR30.ReopenS091` (reviewer). I re-opened SOURCES row S091 (the PyPI release record for uv 0.13.0) and attacked its digests, kind, quote and anchor. Lane HEAD read: `3502b94c5b93d86c5d67866035fd150899456295` (read-only). Scratch: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS091/`.

## Verdict

**S091 holds** on digests, kind and served bytes. One low finding against the row's Gate quote, one low durability risk in the anchor, and one medium finding in an adjacent entry that cites S091 (its recheck line describes a carrier rebuild the counter does not perform).

| attacked | verdict |
|---|---|
| Served bytes equal the committed copy `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json` | holds |
| The 7 wheel digests in the anchor equal the live JSON `.urls[].digests.sha256` | holds |
| The 7 `wheel_sha256` values in `carriers.tsv` equal the live JSON | holds |
| Wheel bytes downloaded fresh from the JSON `url`s hash to those digests, and the 16 members hash to `carriers.tsv` and to the carrier files | holds (extra depth) |
| kind `dataset` fits `CORPUS.md` | holds |
| Gate quote is located, ≤25 words and grounds `teaches` | holds partially (finding F2) |
| Anchor revision pin (whole-file "Served JSON SHA256") is durable | holds today; fragile (finding F3) |
| `positive.md` recheck line: carriers "rebuilt from the S091 wheels if absent" | fails (finding F1) |

## Findings by severity

### F1 — medium — the entry's recheck line claims a rebuild that does not exist (adjacent to S091)

`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:3` says the counter "re-runs REA live on the 16 carriers at `/fast/scratch/hyaku/kaidoku-r30/carriers/`, rebuilt from the S091 wheels if absent". The counter has no rebuild path. In `tools/round-30/c1-rust-positive.py` (lines 220–223), an absent carrier returns exit 2:

```
for r in rows:
    if not os.path.exists(r["path"]) or sha256_file(r["path"]) != r["sha256"]:
        print("PIN carrier %s absent or altered at %s" % (r["id"], r["path"]))
        return 2
```

- **Observation (code search):** `git grep -n -I -e pythonhosted -e '\.whl' -e zipfile -e rebuil HEAD -- tools corpus/evidence/round-30 SKILL.md .ufo/waves/round-30` (2026-10-23T03:14:24Z) found nothing under `tools/`. The only "rebuilt" hits are C2 mutant-rebuild receipts (`mutants=19 rebuilt pin_mismatch=0`) and wave-1 seat reports that rebuilt carriers by hand (`RevCarrierProvenance.md:18`, "Extracted the TSV-named member from each wheel with Python `zipfile`").
- **Observation (counterexample run):** I made a sandbox clone at `.../ReopenS091/clone` and committed `1cd2ce0f` there. That commit points `elf-x86_64-uv` at a non-existent path. Then I ran `TMPDIR=.../tmp timeout 300 python3 -I -B tools/round-30/c1-rust-positive.py --root .../clone --rev 1cd2ce0f3cac18d29527da3cd3d295ffda29b7d8` at 2026-10-23T03:14:51Z. It exited 2, and the full stdout was `PIN carrier elf-x86_64-uv absent or altered at /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS091/absent/elf-x86_64-uv`. No REA call ran, because the PIN check comes before the package check.
- **Inference:** a re-checker who finds the scratch carriers gone gets exit 2 and no rebuild. The carriers *can* be rebuilt by hand from the S091 wheels (F-chain below proves the bytes match), so the defect is in the wording. Either drop "rebuilt from the S091 wheels if absent" from the recheck line, or add a rebuild step. The S091 row itself is not affected.

### F2 — low — the Gate quote grounds the filename half of `teaches`, not the digest half

`teaches` (S091): "The release record names the official wheel archives and their digests." The Gate quote in `corpus/lessons/round-30.md:34` is `"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"`, located on line 1.

- **Observation:** the quote occurs exactly once in the served bytes, at byte offset 13222 of the single 29777-byte line. It is 2 word tokens long, so it meets the ≤25-word rule. The bytes just before it (check run at 03:14:08Z) are `"sha256":"93265932cb2efd1486d4d182211281b3f0b31637e2fc160c4c8d7b15294188d1"},"downloads":-1,"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"`. The digest is two keys before the quoted span and falls outside it.
- **Inference:** the quote shows that the record names the wheel. It does not show that the record carries the digest. A contiguous quote of at most 25 words beginning at `"sha256":"93265932…` would ground both halves. "Line 1" is a weak locator for a one-line JSON file; a byte offset (13222) or the JSON path `.urls[1].filename` is more exact. The anchor cell's 7 digest pairs make up for this in substance; the gap is in the Gate record only.

### F3 — low (residual risk) — the whole-file sha256 pin is unstable across future uv uploads

- **Observation:** the per-version body carries project-wide, mutable fields. Its `last_serial` is 42570783, equal to the project-wide `x-pypi-last-serial: 42570783` header and to `last_serial` in `https://pypi.org/pypi/uv/json` (fetched 03:15:02Z; latest release `0.13.5`). It also carries `ownership` and a non-empty `vulnerabilities` list (GHSA-hq85-5cpj-mr62, `fixed_in` 0.13.4).
- **Inference:** the next upload or advisory for uv will change the served bytes. "byte-identical to the committed copy" (LOG.md:3018; lesson Gate) will then stop holding, even though the 7 file digests cannot change: PyPI files are immutable per filename. The `on-release` recheck should compare `.urls[].filename`/`digests.sha256` rather than the whole-file sha256. The row is correct as of 2026-10-23.

## Evidence

### E1 — the live fetch equals the committed copy (observation)

`timeout 120 curl -sS -D headers.txt -o pypi-uv-0.13.0.live.json -w '%{http_code} %{size_download} %{url_effective}\n' https://pypi.org/pypi/uv/0.13.0/json`, run at 2026-10-23T03:12:30Z, exited 0 with `200 29777 https://pypi.org/pypi/uv/0.13.0/json`.

`sha256sum` gave `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c` for both the live file and the committed `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json`, and `cmp` exited 0. That value equals the anchor's "Served JSON SHA256".

### E2 — three-way digest match (observation)

`timeout 60 python3 -I -B check_s091.py` ran at 2026-10-23T03:12:53Z and exited 0. Excerpts:

```
info.name uv info.version 0.13.0 info.yanked False yanked_reason None
urls_count 19 packagetypes ['bdist_wheel', 'sdist']
carriers 16 distinct_wheels 7 distinct_pairs 7
tsv_mismatches 0
anchor_pairs 7
anchor_mismatches 0 anchor_set_eq_tsv_set True
anchor_served_sha_eq_live True
lesson_quote_count_in_live 1
```

None of the 7 wheels is yanked. Each anchor digest string `"sha256":"<hex>"` occurs exactly once in the served bytes. The anchor's 7 (filename, digest) pairs are the same set as the 7 distinct pairs in `carriers.tsv`.

### E3 — fresh wheel bytes and member chain (observation)

`timeout 900 python3 -I -B chain_s091.py` ran from 2026-10-23T03:13:31Z to 03:13:34Z and exited 0. It downloaded each wheel from its JSON `url` on `files.pythonhosted.org` into my own scratch. Each wheel's `fresh_sha256` and size equal the JSON values (`fresh_eq_json True` ×7). The shared `/fast/scratch/hyaku/kaidoku-r30/wheels/` copies are also equal (`shared_eq_json True` ×7). For all 16 rows, the `carriers.tsv` member read in memory gives `tsv_sha_eq True tsv_size_eq True carrier_file_eq True`. The script ended with `chain_failures 0`.

Carriers were only read; nothing was written to them or to mutants.

### E4 — kind `dataset` (observation)

`/home/vgpnk/Projects/shokunin/CORPUS.md:91-92`: "`kind` — `spec` · `docs` · `paper` · `code` · `tool` · `dataset` · `talk` · `book` · `community` · `own-work`." CORPUS.md lists the kinds but does not define them.

`registry` (the wave-1 draft's kind) is not in the list, so the L1's change to `dataset` is required. `dataset` is also the lane's existing convention for registry and release-list metadata records: S037 and S080 (npm registry records) and S038 and S047 (Go release list JSON) are all `dataset` (awk over `corpus/SOURCES.md` at 03:13Z). The alternatives fit worse. A served JSON record is not `code`, `docs` or `tool`, and `own-work` applies only to repo paths and commands.

The census lines from CORPUS.md:145 and :147, run in the lane at 03:14:14Z, printed nothing for enum or tier violations. Both S091 `used-by` paths exist (`exists:` ×2), and the malformed-row count is `0`.

Tier A fits the scope, wheel filenames and digests, because PyPI is the primary record of what was uploaded. **Inference:** this is consistent with tier rule A, "primary or authoritative for that scope".

### E5 — base carrier for C2 (observation)

`refusals.md:1` cites "S091 (wheel digest of the base carrier)". The C2 base carrier `elf-x86_64-uvx` comes from `uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` = `52c7da0f…16ed`, which matched in E2 and E3.

## Sources opened (access date 2026-10-23)

| URL | sha256 of bytes read | located quote (line) |
|---|---|---|
| https://pypi.org/pypi/uv/0.13.0/json | `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c` | line 1: `"downloads":-1,"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"` |
| https://pypi.org/pypi/uv/json | `27e7b529380679a714d280fc6e7a7be06e0b7ad88fef31fd05bd2904247ac893` | line 1: `"last_serial":42570783` |
| …/ff/27/2a2dde8a…/uv-0.13.0-py3-none-macosx_10_12_x86_64.whl | `93265932cb2efd1486d4d182211281b3f0b31637e2fc160c4c8d7b15294188d1` | `uv-0.13.0.dist-info/WHEEL:4`: `Tag: py3-none-macosx_10_12_x86_64` |
| …/9e/d4/d42eabbd…/uv-0.13.0-py3-none-macosx_11_0_arm64.whl | `a5f93ae362b751737cecef0bbc0294624be68a843ff9b32d86e6862a26101630` | `WHEEL:4`: `Tag: py3-none-macosx_11_0_arm64` |
| …/c3/75/19013838…/uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | `52c7da0fd9056d9551124777ec77de53f0df7017daf8f98a19e947b7837416ed` | `WHEEL:4`: `Tag: py3-none-manylinux_2_17_x86_64` |
| …/fd/f2/0b7d95cf…/uv-0.13.0-py3-none-manylinux_2_28_aarch64.whl | `f840e640fe16591f6d71a94e8863707b7ba43c5786d1fe662868a9fb44c53e50` | `WHEEL:4`: `Tag: py3-none-manylinux_2_28_aarch64` |
| …/52/5a/8c135e80…/uv-0.13.0-py3-none-manylinux_2_31_riscv64.whl | `78187f23c0b51d1be824096ec8a656c417acca312f5451ba1e2ee057ec5a6e87` | `WHEEL:4`: `Tag: py3-none-manylinux_2_31_riscv64` |
| …/b2/00/73abae6c…/uv-0.13.0-py3-none-win_amd64.whl | `0367b4e0ae4dcef32da4aa2ad2f3853b6ad81d50c187abe50d343d892b8fea21` | `WHEEL:4`: `Tag: py3-none-win_amd64` |
| …/e7/92/cf7f8765…/uv-0.13.0-py3-none-win_arm64.whl | `286d5976bffe3ed0c62601c0393adb3748f0d88aa24f38cd80ebab773f5b5f74` | `WHEEL:4`: `Tag: py3-none-win_arm64` |

Wheel URLs are under `https://files.pythonhosted.org/packages/`. The full URLs are in `chain_s091.out`.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReopenS091/`)

| file | sha256 |
|---|---|
| `check_s091.py` | `3e431b129e2b8a6dbb05dbce95c1ba38871018fea3873e0166db73fda034c71b` |
| `check_s091.out` | `c76741935f7f09a30ea445ec25053b38252940e8a2cc27340d38e3b09eab1dda` |
| `chain_s091.py` | `31c9543108b766d83ebcab256cde7dbb97a6ff0211d022f4e8eb67c4c16e24bb` |
| `chain_s091.out` | `3026837b5773adf283d3059deb1beef7cb1fdc3698fd35d5a372d8fed2d8bb00` |
| `pypi-uv-0.13.0.live.json` | `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c` |
| `headers.txt` | `2b67958906f013deb2d4b74e1bc9f993859701e16f4002a2413761b0ce9f5dae` |
| `fetch-utc.txt` | `2d7b7e8d7c25cf1a54859169766bbe743764e164b563380c98e5aafb5fc452ce` |
| `chain-utc.txt` | `62eabcfd4bb82b78d9952c7dc7e89df466377714067beb2e5126c5d7860a4a85` |
| `absent-carrier.out` | `25a85e5861f3df0d062c070ccefa32a36f926fe11acd3aee3a4042ec811972ba` |
| `uv-project.json` | `27e7b529380679a714d280fc6e7a7be06e0b7ad88fef31fd05bd2904247ac893` |
| `uv-project.headers` | `879b4f13a6da0653098b7ca74efc8cbd838a84b46b5c440f7ac29c3f6b32fc34` |
| `wheels/*.whl` (7) | equal to the 7 PyPI digests above |
| `clone/` | sandbox clone of lane `3502b94c`, plus control commit `1cd2ce0f` (`ctl: carrier path absent`) |

## Residual risk and verification gaps

- REA was not run, as this item does not require it. No carrier or mutant was executed or written; carriers were opened read-only for sha256 only. The C2 counter was not run.
- CORPUS.md does not define kinds, so the `dataset` verdict rests on the enum plus lane precedent (inference), not on a definition.
- F3 is a forward-looking inference. I did not observe a byte change, and the body `last_serial` currently equals the project-wide serial.
- No `lsp` server applies: the targets are Markdown/TSV/JSON rows and one Python counter read by line. Code-path claims rest on reading lines 195–234 of the counter, a `git grep` text search, and the observed exit-2 run.

## Tooling

No tools were installed or updated (curl, python3 with zipfile and hashlib, and git were already present). I started no long-lived processes and none remain.
