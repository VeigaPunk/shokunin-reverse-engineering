# FinalC1Measure — residual re-measure of frozen R32-C1 (round 32, attempt 2 residual wave)

Seat: `KaidokuR32A2.FinalC1Measure-2`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only).
Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalC1Measure` (301 226 bytes, 42 files).
Measured product: `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26` (the C1 data commit), per assignment.
Freeze instrument hashes verified before the run: working-tree == `bb0af56c` == `claims.json`
instruments block for `c1-arm64x-positive.py` (`7a534be6…0f1a`), `arm64x_oracle.py`
(`17eea1f9…6686`), `build-arm64x-carriers.sh` (`7da284da…37ba`), `carriers.tsv`
(`8cf97b37…316e`), `predictions.tsv` (`fd804949…c56b`).

## 1. The single read-only measure run (exercised)

Exact argv (cwd = lane root):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC \
  JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  timeout 900 python3 -I -B tools/round-32/c1-arm64x-positive.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
```

- Started `2026-10-23T07:16:35Z`, ended `2026-10-23T07:18:16Z`; wall 100.14 s; **EXIT=0**; no
  timeout (inner `timeout 900` unused). No `--write-evidence`; read-only measure mode.
- Session `env | grep ^GIT_` showed only `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT`
  (no routing vars set anyway); the three routing vars were explicitly removed in argv.
- Full stdout retained at `counter.stdout.txt` (sha256 `e2f194bc2e258fee04830997591148ad9b39d6cb013d58609ed464f529e7cff1`); stderr 0 bytes (`e3b0c442…b855`).

Verbatim stdout:

```
k01	P1-pass	segments=8 procedure_count=1
k02	P1-pass	segments=8 procedure_count=2
k03	P1-pass	segments=8 procedure_count=3
k04	P1-pass	segments=8 procedure_count=4
k05	P1-pass	segments=8 procedure_count=1
k06	P1-pass	segments=8 procedure_count=5
k07	P1-pass	segments=8 procedure_count=6
k08	P1-pass	segments=8 procedure_count=2
k09	P1-pass	segments=8 procedure_count=7
k10	P1-pass	segments=8 procedure_count=3
k11	P1-pass	segments=8 procedure_count=8
k12	P1-pass	segments=8 procedure_count=1
carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

The frozen target line `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0, was
met **observed**, once. Per-carrier verdicts match the producer's committed `runs.tsv`
(06:56:33–06:58:38Z, same argv shape `npx -y rea-agents@6.5.0 inspect <path> --format json
--full-output`, pkg_json_sha256 `a5003…b030` — byte-identical to today's
`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`, version `6.5.0`).
Provider env actually used: `node v24.21.0`, `npx 11.19.0`, `openjdk 21.0.12.1+1`,
`GHIDRA_INSTALL_DIR`/`JAVA_HOME` as above (M32-3 corrected: env explicitly set).
The counter strips `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` itself inside `run_rea`
(`clean_env()`); the outer `env -u` additionally protects its own `git` calls.

**Lane-state caveat (witnessed, not caused by this seat):** at run time HEAD had moved to
`bbdd793d55807cfea9193ef5aaf0ae86a5c25a10` (witness-commit retaining the A2PEIndependent
registry/output, parent-announced). `git diff bb0af56c bbdd793d -- corpus/evidence/round-32/c1/
tools/round-32/ PROVINCE.md corpus/knowledge/` is **empty** — the entire C1 read-set is
byte-identical; the counter's rev-pinned reads (`git show bb0af56c:…`) are unaffected.
Two pre-existing tree modifications were present and remain: `M LOG.md`,
`M corpus/lessons/round-32.md` (not mine, not in the C1 read-set). No tracked file changed
through this seat; `cmp` confirmed all 12 working-tree envelopes byte-identical to `bb0af56c`.

## 2. Independent comparison of all 12 committed envelopes (exercised)

Method: my own PE byte parser `pe_own_compare.py` (sha256 `587dadc65d756ccc25d9b05cbbdec0b61fb38b742ee651ebe278e06e1b023251`, 8 245 B — retained in scratch; it does **not** import or call the lane oracle `arm64x_oracle.py`) plus my own `llvm-readobj` 23.1.3 runs
(`llvm-readobj --file-headers --section-headers --coff-exports --coff-load-config`, 12/12 exit 0,
retained `ro-k*.txt`, per-file sha256 below). Envelope copies staged byte-identical from
`git show bb0af56c:…` (`cmp`-verified vs working tree; 12 envelope sha256 listed below).

`python3 -I -B pe_own_compare.py . /fast/scratch/hyaku/kaidoku-r32/carriers env .` →
**`SUMMARY carriers=12 checks=144 fails=0`, `COMPARE_EXIT=0`** (output retained in
`compare-own.json`, sha256 `59725eccf2439cf0c6ef1dc02306375381c779b036ff9a625df25d74b9f4107e`;
copied `carriers.tsv`/`predictions.tsv` into scratch for reproducibility).

| id | env subject sha256 == own sha256 == tsv | ordered segments env == own | #seg env/own/pred | proc env/own/readobj/pred/tsv-native | names env-side order == readobj | hybrid n == tsv ec | codemap own == readobj |
|---|---|---|---|---|---|---|---|
| k01 | ✓ (2f386dde…0989) | ✓ | 8/8/8 | 1 | f1 | 1/1 | ARM64+ARM64EC+AMD64 ranges ✓ |
| k02 | ✓ (a16ba362…d4a1) | ✓ | 8/8/8 | 2 | f1,f2 | 2/2 | ✓ |
| k03 | ✓ (0291e17b…73d1) | ✓ | 8/8/8 | 3 | f1..f3 | 3/3 | ✓ |
| k04 | ✓ (3c783318…b386) | ✓ | 8/8/8 | 4 | f1..f4 | 1/1 | ✓ |
| k05 | ✓ (cc5c644a…60bf) | ✓ | 8/8/8 | 1 | f1 | 4/4 | ✓ |
| k06 | ✓ (6c45a3ce…b7b3) | ✓ | 8/8/8 | 5 | f1..f5 | 5/5 | ✓ |
| k07 | ✓ (84a78b78…fb6f) | ✓ | 8/8/8 | 6 | f1..f6 | 2/2 | ✓ |
| k08 | ✓ (b158eaf7…3215c) | ✓ | 8/8/8 | 2 | f1,f2 | 6/6 | ✓ |
| k09 | ✓ (cf014861…2a87) | ✓ | 8/8/8 | 7 | n1..n7 | 3/3 | ✓ |
| k10 | ✓ (a48499d2…766c7) | ✓ | 8/8/8 | 3 | n1..n3 | 7/7 | ✓ |
| k11 | ✓ (b5e2af7f…d181) | ✓ | 8/8/8 | 8 | f1..f8 | 8/8 | ✓ |
| k12 | ✓ (8c852d07…04fa) | ✓ | 8/8/8 | 1 | n1 | 2/2 | ✓ |

Per-carrier detail (uniform across all 12, observed):

- **Subject digest**: envelope `subject.digest.sha256` == `hashlib.sha256(pinned bytes)` ==
  frozen `carriers.tsv` column == committed `indep.json` `label_sha256`. k01/k12 are 9 216 B,
  the rest 9 728 B, matching `bytes` column.
- **Ordered segments**: envelope `segments` list (name, start, end, length, image_base,
  address_space, in order) equals my byte-derived list exactly: `Headers
  [0x180000000,0x180000400) len 1024` (SizeOfHeaders 0x400) + 7 sections
  (`.text .hexpthk .rdata .data .pdata .a64xrm .reloc`); section `start =
  ImageBase+VirtualAddress`, `length = max(VirtualSize,SizeOfRawData)`, `end = start+length`,
  `address_space "ram"`. `segment_count` 8 = 1+7 = frozen prediction. My readobj
  `--section-headers` section tuples (name, VA, VirtualSize, RawDataSize, PointerToRawData)
  equal my parse for all 12; readobj `SectionCount: 7` + Headers pseudo-segment = 8.
  k04 `.text`: VirtualSize 0x105C < RawDataSize 0x1200 → length 4608 exercises `max` on the
  raw side, as the frozen limits note (no carrier tests VirtualSize > RawDataSize).
- **Procedure counts**: envelope `procedure_count` == my `NumberOfNames` of the primary
  (native-view) export directory == `readobj --coff-exports` primary `Export` block count ==
  frozen `predictions.procedure_count` == `carriers.tsv native_exports`. `NumberOfFunctions
  == NumberOfNames` on all 12 (no ordinal-only exports). Hybrid/EC `Export` block counts
  match `ec_exports`, confirming the native-view count (not union/max) was scored:
  k04 4 native vs 1 EC, k10 3 native vs 7 EC.
- **Beyond the three assigned fields** (same method): `machine` raw bytes 0xAA64 on all 12
  (readobj displays `IMAGE_FILE_MACHINE_ARM64X (0xA64E)` — LLVM display promotion, matching
  A2BuildRecheck §4); `document` == `target-<sha[:12]>.dll` == frozen predictions column;
  `image_base` `0x180000000` (readobj agrees); `subject.format/architecture` `pe`/`arm64`;
  `operation` `binary_overview`; `ok:true`; CHPE code map v2 at load-config +0xC8 decode ==
  readobj `CodeMap [` ranges on all 12 (types: my AMD64 == readobj X64 label).

### Rederived vs merely witnessed

- **Rederived by this seat** (new bytes→values computations, no lane oracle output used):
  subject sha256; every segment field and order; `segment_count`; `procedure_count` and
  export-name identity/order; section-table tuples; COFF machine; ImageBase;
  SizeOfHeaders; load-config presence; CHPE code-map entries/types; doc-name derivation.
  Sources: my parser + my llvm-readobj runs.
- **Witnessed (re-derived by others, compared here, consistent)**: committed `indep.json`
  (`f79b51db…f44f`, working tree == `bbdd793d` blob): `label_sha256`, section_count,
  `exports.name_count`, code-map ranges — all equal my values on all 12. Committed
  `A2BuildRecheck.md` table: native/EC export counts and k04 CHPE ranges — equal.
- **Witnessed only (not re-derived)**: committed↔live envelope equality minus `meta` —
  asserted by the counter's own P1-pass per carrier; measure mode does not retain live
  bytes, so this seat did not byte-diff live vs committed (the counter did). Doc gates
  re-derived cheaply at rev: entry cites S099 (line 1 and line 40) and names all 12
  `ev_*` evidence_ids (sorted lists compared equal); PROVINCE ARM64X row at `:357` sits
  under `## Round-32 additions to Core (verified 2026-10-23)` (`:353`).

## 3. Findings

None blocking, none requiring action. Observed residuals (already disclosed upstream):

- [INFERENCE-level limitation, disclosed] The envelope `procedure_count` equals the export
  **name** count; since `NumberOfFunctions == NumberOfNames` on all 12, "export name count"
  and "export function count" cannot be separated — consistent with the frozen
  claim's stated rule, not a defect.
- The measure run relies on `arm64x_oracle.py`'s own `expected()` for the envelope-equality
  clause; this seat's independent values equal the envelopes, so the oracle's derived
  values are corroborated, but the live-vs-committed byte equality itself is only
  witnessed (counter-asserted), not re-derived (see §2).
- llvm-readobj witnesses share LLVM 23.1.3 with the builder (same caveat as A2BuildRecheck).

## 4. Verification gaps / residual risk

- The rerun's live REA envelopes are not byte-preserved in measure mode (by design); the
  committed-vs-live equality is counter-asserted, consistent with identical digests and
  per-carrier pass reasons.
- One run, one host, one REA pin (6.5.0), one Ghidra build (12.1.4): a provider-side
  nondeterminism could pass one run and fail another; nothing observed suggests this
  (producer and this rerun agree on every verdict 50 min apart).
- Pre-existing uncommitted `LOG.md`/`round-32.md` edits remain — outside the C1 read-set;
  if later committed, the rev-pinned measure is unaffected.

## 5. Retained evidence (scratch hashes, 42 files / 301 226 B)

| artifact | sha256 |
|---|---|
| counter.stdout.txt | e2f194bc2e258fee04830997591148ad9b39d6cb013d58609ed464f529e7cff1 |
| counter.stderr.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| pe_own_compare.py | 587dadc65d756ccc25d9b05cbbdec0b61fb38b742ee651ebe278e06e1b023251 |
| compare-own.json | 59725eccf2439cf0c6ef1dc02306375381c779b036ff9a625df25d74b9f4107e |
| ro-k01..k12.txt | f7a6a913…, 3f50f697…, 2e5a38df…, 04511d0f…, 5ca12503…, 25e006dc…, 2aac82d8…, 56ee565e…, a36b594f…, df9ac5fc…, 944ed613…, 0fb0357c… (full digests in scratch `sha256sum` output; truncated here for width) |
| env/k01..k12.json | c43239a6…, 8023185a…, ca536545…, c9c0c1a3…, 8a945d48…, cf4b0af0…, 6e8c26f1…, 9a997df1…, b32ce2cb…, be6f3864…, 3fc5e5b0…, c7062ab2… |

Exact full digests of the `ro-k*` and `env/k*` files are in the retained `sha256sum`
recorded in this seat's session log; `pe_own_compare.py` + `compare-own.json` + the 12
envelope copies suffice to re-derive every table cell above.

## 6. Conclusion

Observed: the frozen C1 counter at `bb0af56c`, run once read-only with provider env set and
Git routing unset, exits 0 on the frozen target line (12/12 P1-pass, entry_ok=1,
province_ok=1). All 12 committed envelopes independently corroborate — subject digest,
ordered segments, and procedure counts each equal both this seat's own byte parse and this
seat's llvm-readobj rederivation, plus two committed third-party witnesses (`indep.json`,
A2BuildRecheck). 144/144 comparator checks pass; zero mismatches. No findings; verdict
consistent with landed product. Nothing was suppressed: no failed run occurred to report;
write mode was never invoked.

No installs/updates were made (pacman paused; nothing needed). No lane/git writes; no
background processes left; held item `U064N008Hf47eb933` not touched. Deadline 07:55Z met.
