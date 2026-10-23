# CtlC2RewritePred — frozen-input amendment control

CONTROL CtlC2RewritePred: met=no score=0/23

## Result

- **Observation:** the amended control did not meet the frozen C2 target. It exited **1**, reporting `requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)`. The pristine and restored runs produced byte-identical stdout and the same exit code.
- **Observation:** the round-30 prefreeze gate **did not catch** the post-freeze frozen-input amendment. At the control commit it exited **0**, reporting `pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0` and `verdict=CLEAN`. Its pristine and restored comparisons also exited 0.
- **Observation plus source interpretation:** **C2 itself does not detect this frozen-input edit after it is committed and measured with `--rev HEAD`.** Its prediction check compares working-tree text with the prediction blob at the supplied revision, not with the freeze commit. The amended run completed all 23 live requests without a PIN rejection; every miss was `committed envelope absent`.
- **Inference:** the amendment **survived the prefreeze gate's freeze-authenticity boundary**. The relevant gate implementation hashes each pinned path at `freeze`, not at the measured revision. C2 also lacks that boundary check in its prediction loading. This is a coverage finding, not permission to amend the frozen inputs.
- **Mutation verdict:** **survived** against the prefreeze gate; **inconclusive** as a C2 full-target mutation kill, because the pristine baseline already fails for absent records/documents. The amended exit 1 is **not** evidence that the amendment was detected.
- **Unknown:** whether an otherwise complete post-data tree with this amendment could meet the full C2 target. No envelopes or documentation rows were added for this assigned one-cell probe, and no full-target bypass was observed.

The attack was exactly the assigned frozen-input edit. Despite the target's general after-data-message description, the explicit work instruction leaves the message unchanged and changes only `code_pointer`; this probe does not claim to have changed the expected live message.

## Control and containment

Axes: frozen-input identity, attribution of rejection, and exact byte restoration.

Sandbox: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone`, branch `ctl`, initially at freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`.

Only this clone file was mutated:

`/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv`, line 5, row `q-missing-table`.

- Message remained exactly `Selected ordinary table does not exist with that exact name: NoSuchTable`.
- `code_pointer` changed from `dist/sqlite/SqliteDatabaseInspection.js:74,187-189; dist/sqlite/SqliteDatabaseWorkerExecution.js:31-58` to `amended`.
- Control commit: `980bfa7e17d87b861889a467eb0879dc0692c7e6`, created at **2026-10-23T04:11:40Z** with the required `ctl <ctl@local>` identity.
- Producing commit command, exit **0**:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone -c user.name=ctl -c user.email=ctl@local commit -m 'control: amend q-missing-table code pointer after freeze'
```

Exact commit stdout:

```text
[ctl 980bfa7] control: amend q-missing-table code pointer after freeze
 1 file changed, 1 insertion(+), 1 deletion(-)
```

The control commit remains on `ctl` and is retained in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control.bundle`. After the mutated detectors finished, the working-tree prediction file was restored to the exact freeze bytes, without resetting or removing the control commit. Consequently that one working-tree file intentionally differs from the retained control commit.

No lane source, index, fleet repository, sibling seat, immutable carrier, or immutable mutant was edited. The sole lane write is this report. REA ran only through the assigned counter, three bounded counter invocations. No `--write-evidence`, `--build`, selftest, other REA operation, tool installation, or tool update was run.

## Detector execution and capture

All detector commands below ran with working directory `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred` and `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/tmp`, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/run-probe.py` retained stdout/stderr bytes, the exact argument vector, UTC interval, exit code, and output hashes. It launched each bounded command in an owned process group and cleaned that group up before returning. No timeout fired. Every detector's stderr was empty. The private runtime cache was removed after the detectors finished.

Expected detector: an enforcement check for the frozen-input invariant would reject the changed prediction bytes despite their agreement with the later commit. The frozen C2 score target remains `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1`, exit 0; it was not changed for this control.

### Pristine C2 counter

UTC **2026-10-23T04:10:56Z–04:11:20Z**; exit **1**.

Exact counter command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout:

```text
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

### Amended C2 counter

UTC **2026-10-23T04:11:59Z–04:12:20Z**; exit **1**. At this invocation `HEAD` was `980bfa7e17d87b861889a467eb0879dc0692c7e6`, and the working-tree prediction bytes matched that commit.

Exact counter command:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --rev HEAD
```

Full stdout:

```text
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

This did **not** meet the frozen target; therefore no clause was observed letting a complete target pass through. The narrower frozen-input edit was admitted by the tree-versus-`--rev` check at counter lines 279–285. The missing-envelope rule at lines 232–236 and 342–345, plus the absent documentation gates, prevented a score pass. Because `committed_check` is reached only after the live judgment matches, the live-half agreement for all 23 requests is an **inference from that control flow and the actual stdout**, not a claim that this seat retained the live envelopes themselves.

### Prefreeze gate: pristine, amended, restored

Pristine command, UTC **2026-10-23T04:10:56Z**, exit **0**:

```sh
timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-30/prefreeze-gate.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --round 31 --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full pristine stdout:

```text
prefreeze round=round-31 freeze=35ba7c522dba55f9be27eb161d4254eacaa24330 rev=35ba7c522dba55f9be27eb161d4254eacaa24330 claims=.ufo/waves/round-31/claims.json
pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
```

Amended command, run after the amended C2 counter, UTC **2026-10-23T04:12:24Z**, exit **0**:

```sh
timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-30/prefreeze-gate.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --round 31 --rev HEAD
```

Full amended stdout:

```text
prefreeze round=round-31 freeze=35ba7c522dba55f9be27eb161d4254eacaa24330 rev=980bfa7e17d87b861889a467eb0879dc0692c7e6 claims=.ufo/waves/round-31/claims.json
pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
```

Restored command, UTC **2026-10-23T04:12:50Z**, exit **0**:

```sh
timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-30/prefreeze-gate.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --round 31 --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full restored stdout:

```text
prefreeze round=round-31 freeze=35ba7c522dba55f9be27eb161d4254eacaa24330 rev=35ba7c522dba55f9be27eb161d4254eacaa24330 claims=.ufo/waves/round-31/claims.json
pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
```

**Inference:** this gate verifies pins against the original freeze tree. Its clean result says nothing about later amendments of those paths: lines 187–201 call `blob_sha256(root, freeze, path)` and compare the recorded pin to that original blob. The observed amended clean result is consistent with this implementation; it is not a PIN mismatch detector for the measured tree.

### Restored C2 counter

After restoring the exact prediction bytes, the same instrument and the original revision argument were used again. UTC **2026-10-23T04:12:50Z–04:13:21Z**; exit **1**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Its full 1,232-byte stdout is byte-identical to the pristine C2 block above, retained at `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-counter.stdout`, SHA256 `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`. Its final line is exactly:

```text
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

## Byte identity and restoration evidence

| State | Prediction-file SHA256 |
|---|---|
| Before mutation / freeze blob | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` |
| Mutated working tree and control-commit blob | `aa4173a499165872083703d321aab1fee2422c9ac51e4fd6ff88cae8386c8999` |
| Restored working tree | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` |

**Observation:** the initial pre-mutation `timeout 30 sha256sum` output matched the freeze pin. The mutated hash was captured at **2026-10-23T04:11:59Z**, exit **0**, by:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv
```

Exact amended stdout:

```text
aa4173a499165872083703d321aab1fee2422c9ac51e4fd6ff88cae8386c8999  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv
```

The restored hash command at **2026-10-23T04:12:50Z**, exit **0**, also hashed the unchanged counter, gate, claims, and operational references:

```sh
timeout 30 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-31/c2-sqlite-refusals.py /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-30/prefreeze-gate.py /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/.ufo/waves/round-31/claims.json /home/vgpnk/.agents/skills/godspeed/SKILL.md /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md /home/vgpnk/.omp/agent/RULES.md
```

Exact restoration excerpt:

```text
acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv
```

For separately timestamped immutable before/after blob evidence, the following read-only commands both exited **0** at **2026-10-23T04:14:58Z**. Their complete stdout is the respective original/amended prediction file, with SHA256 equal to the first two rows of the table:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone show 35ba7c522dba55f9be27eb161d4254eacaa24330:corpus/evidence/round-31/c2/predictions.tsv
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone show 980bfa7e17d87b861889a467eb0879dc0692c7e6:corpus/evidence/round-31/c2/predictions.tsv
```

## Sources

Access date for every source: **2026-10-23**. Local sources only, opened by ordinary file reads; no HTTP source or access challenge was used. SHA256 values identify complete source-file bytes. Quotes below contain at most 25 contiguous words. Relative paths occurring inside verbatim detector output or Git object specifications above are original output/specification syntax, not alternate filesystem destinations.

| Source URL | SHA256 | Located quote |
|---|---|---|
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-31/c2-sqlite-refusals.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` | L283: `if pred_text != open(os.path.join(root, PRED)).read():` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/tools/round-30/prefreeze-gate.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` | L193: `at_freeze = blob_sha256(root, freeze, path)` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L5: `a miss under them is reported, never amended, never re-scaled.` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone/corpus/evidence/round-31/c2/predictions.tsv` (freeze/restored bytes) | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` | L5: `Selected ordinary table does not exist with that exact name: NoSuchTable` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-predictions.stdout` (control-commit bytes) | `aa4173a499165872083703d321aab1fee2422c9ac51e4fd6ff88cae8386c8999` | L5, final field: `amended` |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` (operational reference) | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L13: `2. **Iterate cheap, in parallel.**` |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` (operational reference) | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | L17: `Run REA through the CLI` |
| `file:///home/vgpnk/.omp/agent/RULES.md` (operational reference) | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L4: `full privilege, without asking first.` |

The lane copies used for initial source inspection were the frozen sources; the executed sandbox instruments retained the SHA256 values above. The counter was not patched. The original freeze and control-commit prediction bytes are retained separately so source identity does not depend on the final working-tree state.

## Retained artifact inventory

The repository directory `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/clone` is retained with the control commit and restored working-tree prediction file. Its portable committed-history representation is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control.bundle` (SHA256 below); the restored file's separate SHA256 is recorded above. A directory itself is not being represented as a single file hash.

Every retained probe-created standalone file is listed below. The JSON files contain exact producing commands, UTC times, exit codes, and output sizes/hashes. Empty stderr files are retained rather than omitted.

```text
59040b34bdf570679dbe691def3655299eee0599dacbc96cb38c484265772078  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/run-probe.py
2fdfd0aa611529f9de8e7aa636a4d585086018901cdf35e2aad615f6aaf5eb56  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control.bundle
6e4233a74eb0d90704c845faa18489443608146bf295cbeb8d03d8863bec035e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-counter.json
cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-counter.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-counter.stderr
a66312419047de6a330974d0252b84f6123e52356fcf98dca1f51f69ceceb04e  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-gate.json
76f26969311c9c9f6ef2372da5ade21ae1c0dde68577069b5672479629903be5  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-gate.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/baseline-gate.stderr
50769bff51af12cd0cff3222def17feead495da92f74fce2257f0960d02f5165  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-commit.json
b326ddc6fb60c832350f56873f3e9abace84981e0079fd816c9cd07499ef9163  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-commit.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-commit.stderr
d579a85744abd330e2eb2be71aaf4e1ca2bd13111374285931d8d171a12d7100  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-patch.json
30334fb7a0674a56bee17dff3344f0127dc19f7e36c3a221557ce94bfcf7ab66  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-patch.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/control-patch.stderr
ec29f70d4d4d2329e1e8abd901cdaef319838efb7094e4b06b707737260d65bc  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-hash.json
3782d3534eac3d60116b51e0e89db3fe7e7e9474d6f79f652d177f818af509d1  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-hash.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-hash.stderr
5c676bd45c9b53fdd7e24e534a2cb741737d7debc3cc37243bb4b25fde674879  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-counter.json
cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-counter.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-counter.stderr
5fc04aabce53d5a1ba171870c965cfd38c9cd001c0df92b451b97102991ae59d  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-gate.json
61fc29289397f49b8b1731ec217b858df5ca3fd78b16a65fb44c28118a12ac74  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-gate.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-gate.stderr
1321ff85c520d7601edfe5ec06097c41dc0e90bf3eaa00225f1e3d9cfcb303ab  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-counter.json
cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-counter.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-counter.stderr
7b9962bfc56982440f2c8b1f6c2d190071416864bde2ad4f091851974352815d  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-gate.json
76f26969311c9c9f6ef2372da5ade21ae1c0dde68577069b5672479629903be5  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-gate.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-gate.stderr
e50ba55172dc72a6324001c54cbe76224f96fbe676d192750f63b6586e43c094  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-hashes.json
fc1e8a9f6f3e06955c93926bd55fa3dbc800f83cc11018fff968e4cc14f65beb  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-hashes.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/restored-hashes.stderr
a9d7a506f9d53346cac68b4ba8c746b87403b5aa3832d5fcb763525ff222118c  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/frozen-predictions.json
acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/frozen-predictions.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/frozen-predictions.stderr
8004cf28a58ab5e597775569c76b321ef685663f4aac62495d3695e69bb6bcdf  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-predictions.json
aa4173a499165872083703d321aab1fee2422c9ac51e4fd6ff88cae8386c8999  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-predictions.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2RewritePred/amended-predictions.stderr
```
