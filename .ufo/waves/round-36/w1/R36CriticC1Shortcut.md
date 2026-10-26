# R36CriticC1Shortcut — attack on R36-C1 as frozen

Seat: `R36CriticC1Shortcut` (leaf, advisory). Round 36, wave 1.
Measured lane state while attacking: `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (HEAD), freeze
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`, genuine after receipts `3310d8fa27bfaa95ad858c4aaad6f6377f853982`,
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Counter, predicate, carriers, oracle and harness were
read only; nothing in the lane was written except this report.

## Verdict

**R36-C1 as frozen is structure-blind: `met_target` is reachable with no sasquatch-enabled extraction, no
unblob invocation, no REA process, no carrier image bytes and no network.** The cheapest demonstrated input is
four JSON files totalling **608,835 bytes**, whose `evidence_id` fields are produced by **~25 lines of Python
stdlib** (`json` + `hashlib`) that reproduce REA's own id byte-for-byte. The frozen counter scores that fixture
`met_target: true`, exit 0.

The counter cannot tell the difference: for the genuine receipts committed at `3310d8fa` and for my fabricated
ones, its per-carrier measurement block is **field-for-field identical** (empty diff, §5).

The frozen kill rule cannot fire on this class. `CTL-C1-2`'s recorded outcome is `carriers_matched: 0` with all
bindings true (`ctl-c1-2-forged-oracle-copy.json`), which is the signature of an id mismatch on a forged
oracle copy [INFERENCE: its fixture is gone; the shape is replicated in F4, which scores 0 under the honest
rule and 4 under a substituted one]. Recomputing the id is the one missing step and it costs seconds.

## 1. What I attacked, and on what authority

The frozen counting command was run unmodified (`tools/round-36/c1-counter.py`, no edits), against a fixture
repository built under my scratch, exactly as the frozen control `CTL-C1-2` itself did (its argv root was
`/fast/scratch/hyaku/kaidoku-r36/L1/ctl.5IzfxI`, `.ufo/waves/round-36/controls/ctl-c1-2-forged-oracle-copy.json`).

Fixture provenance (all source bytes read out of the lane with read-only `git show`):

- fixture freeze commit `6d7f3fd0bfded8b425578b132063acad8bde47d8` = the lane's frozen bytes:
  `tools/round-27/xpin-attribute.mjs`, `corpus/evidence/round-36/c1/carriers.json`
  (sha256 `2ebcf15ad3fe7e53251b15396074e2cae003ab824a1ccf6ac4f636b07e69ca81`, equal to the lane's),
  the four `K*/oracle.tsv`, the four `K*/before.json`;
- fixture attack commit `ddadb78448b09a3d55e1968ceee127e1f67dc824` = 4 fabricated `K*/after.json`
  + 4 binding files (`PROVINCE.md` round-36 Core row, the knowledge entry, `SOURCES.md` row `S107`,
  `corpus/README.md` coverage-map row). The four `before.json` are **byte-identical to the freeze**
  (verified per carrier), i.e. the no-sasquatch half is the lane's own frozen material, not mine.

The fixture contains **no carrier image at all** — `git ls-files` is 18 paths, none `.sqsh`/`.appimage`;
`find` for `*.sqsh` / `*.appimage` returns nothing. The counter still reported `carriers_matched: 4`.

The counter reads only `git -C <root> show <rev>:<path>` for these paths, so the same four `after.json` bytes
committed at the lane's `corpus/evidence/round-36/c1/K*/after.json` are measured identically. (The binding
files are ordinary authoring that C1 needs anyway; they are not part of the cheat's marginal cost.)

## 2. Class table (cost → result, all observed)

| # | class | marginal input | counter result |
|---|---|---|---|
| F1 | fabricate `after.json` per carrier from the frozen oracle, then recompute `evidence_id` with REA's own rule | 608,835 B JSON, python3 stdlib only | **exit 0, `met_target: true`, `carriers_matched: 4`** |
| F2 | same, but 5-key envelopes (`subject`, `provider`, `operation`, `normalized_result`, `evidence_id`) that REA's own `parseEvidence` **rejects** | same bytes | **green** — the counter never calls `parseEvidence` |
| F3 | edit the genuine frozen `before.json` copies into `after.json` (schema-valid, `raw_result` intact), recompute id | 4 edited receipts, ≈8.8 MB | **green**, although internally contradictory: `raw_result` still names the sasquatch gap while `normalized_result.extraction_gaps` is `[]`, and a fabricated `size: 1` sits next to oracle size 59 |
| F4 | substitute the digest-rule implementation via `--pkg65` (patched copy of rea-agents 6.5.0: `semanticProjection` → identity, `digestCanonicalValue` → returns the record's own `evidence_id`) and keep the **stale** id | copy of a 25.6 MB package + 2 line edits | **green** — the `CTL-C1-2` shape (forged oracle copy, stale id) flips from `carriers_matched 0` to `4` |
| F5 | rule selection without edits: run the frozen command with a genuine `rea-agents@6.7.0` root as `--pkg65` | `npm pack rea-agents@6.7.0` | `before_evidence_id_ok` false for **all four authentic receipts** (0/4); a minimal forgery stays green under either root. The "rea-agents 6.5.0 rule" is not pinned to a version |
| F6 | fabricate the `before.json` too (5 keys, one `missing-extractor-dependency` gap naming sasquatch) | 382 B × 4 | **green** — `before.json` is read at `--rev`, never compared to the freeze |
| F7 | label a genuine `before.json` with an `environment`/`parameters` object claiming sasquatch present, recompute id | 0 extra files | **green**, although `xpin --parse` rejects that record under both pins (`environment` is a `strictObject{id,platform,architecture,isolation}`, `dist/domain/evidence.js:92-97`). Not a route to green by itself (the gap check still guards the class), but it shows the counter accepts records the pinned package refuses |
| F8 | replay: K1 `after.json` := the genuine K3 `after.json` | 0 | **red** (3/4): `after_subject_ok` false, `after_oracle_hits` 0 — subject binding works |
| F9 | near miss: K3 `after.json` with 2129 of 2130 oracle rows | 0 | **red** (3/4): `after_oracle_hits 2129 != oracle_files 2130` |
| F10 | oracle row collapse (duplicate sha / path-suffix) to cover N rows with fewer files | 0 | **no collapse**: K3/K4 census = 2 duplicate-sha groups (13 and 3 rows, all distinct paths) and exactly 1 suffix pair (`nvim.desktop` ⊂ `usr/share/applications/nvim.desktop`) whose shas **differ** (`b407dc89…` vs `0b297403…`), so `matched()` still needs 2130 distinct (path, sha) hits. K1/K2 have no duplicates and no suffix pairs |
| F11 | carriers.json / oracle identity | network | **honest, not a hole** (§6) |

## 3. Primary counterexample (F1/F2), complete recipe

The whole attack is: take the frozen oracle, emit one `published` entry per oracle row, take the carrier sha
out of the frozen `carriers.json` for the subject, recompute the id, commit. No extractor, no extraction.

```python
# python3, stdlib only; reproduces tools/round-27/xpin-attribute.mjs's id for both forged and genuine records
import json, hashlib
def proj(e):                                   # rea-agents 6.5.0 semanticProjection, same field set
    out = {}
    out['subject'] = None if e.get('subject') is None else {
        k: e['subject'][k] for k in ('digest','format','architecture') if k in e['subject']}
    for k in ('provider','analysis_profile','predicate_type','operation','parameters','raw_result',
              'normalized_result','confidence','authority','environment','limitations','locations','evidence_links'):
        if k in e: out[k] = e[k]
    if e.get('relationship_coverage') is not None:
        out['relationship_coverage'] = e['relationship_coverage']
    return out
def evid(e):
    canon = json.dumps(proj(e), sort_keys=True, separators=(',',':'), ensure_ascii=False)
    return 'ev_' + hashlib.sha256(canon.encode()).hexdigest()

for k, carrier_sha in [('K1','93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589'), ...]:
    rows = [l.split('\t') for l in open(f'corpus/evidence/round-36/c1/{k}/oracle.tsv').read().splitlines() if l]
    env = {'subject': {'digest': {'sha256': carrier_sha}},
           'provider': {'id': 'unblob'}, 'operation': 'extract_firmware',
           'normalized_result': {'files': [{'relative_path': r[0], 'sha256': r[1]} for r in rows],
                                 'extraction_gaps': []}}
    env['evidence_id'] = evid(env)
    open(f'corpus/evidence/round-36/c1/{k}/after.json','w').write(json.dumps(env))
```

Id fidelity of that 25-line function, checked against REA's own code (`xpin-attribute.mjs` + the 6.5.0 package
at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`):

| record | REA-computed id | python-stdlib id |
|---|---|---|
| forged K1 `after.json` | `ev_3557629bd4ff959a30405831de165b7fa5bfcd126728cce055248f40083728d7` | same |
| forged K3 `after.json` | `ev_71e923dc5904ca3…` | same |
| genuine K1 `before.json` (lane) | `ev_df7bef526779b306…` | same |
| genuine K1 `after.json` (lane) | `ev_b5bd2e7f0ea0b9f6…` | same |
| genuine K4 `after.json` (lane) | `ev_ff0fdb798eea077d…` | same |

Cost accounting (observed): `after.json` sizes 647 B (K1), 796 B (K2), 303,696 B (K3), 303,696 B (K4) —
608,835 B total, 197,019 B gzipped (422 + 482 + 98,055 + 98,060), whole fixture worktree+`.git`
1,779,070 B, zero external programmes.
For scale, the genuine after set at `3310d8fa` is 8,757,164 B (K3/K4 are 4,362,742/4,362,857 B), i.e. the
forgery is 14.4× smaller than the receipts it replaces.

The counter invocation (mine differed from the frozen one only in `--root`/`--rev`/`--freeze`):

```
HYAKU_SCRATCH=<scratch>/base python3 -I -B \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-36/c1-counter.py \
  --root <fixture> --rev ddadb78448b09a3d55e1968ceee127e1f67dc824 --freeze 6d7f3fd0bfded8b425578b132063acad8bde47d8 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <receipt>
```

stdout (exit 0):

```json
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107"], "opened_source_rows": ["S107"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "ddadb78448b09a3d55e1968ceee127e1f67dc824"}
```

## 4. Why each guard the counter does have is satisfied without an execution

`measure()` reduces the predicate's operative clause ("the committed REA extract-firmware receipt run with
sasquatch on PATH …") to five byte-level tests, all of which a claimant writes by hand:

1. `subject.digest.sha256 == carriers.json sha` — a field copied from the frozen `carriers.json`;
2. `operation == 'extract_firmware'` and `provider.id == 'unblob'` — two literals;
3. `normalized_result.files` covering the oracle exactly — the oracle is **unsquashfs** output, not unblob
   output; `matched()` accepts `fp == rel or fp.endswith('/'+rel)`, so one plain `{relative_path, sha256}`
   pair per row suffices (size, mime, `path`, `analysis_depth`, `reported_sha256` are all ignored);
4. `before_sasquatch_gap is True`, `after_sasquatch_gap is False` — one JSON object present or absent;
5. `stored == recomputed evidence id` — a canonical-JSON sha256 of the record itself, i.e. a checksum.

No test touches `K*/after-run.json` (which records the actual `sasquatch` path/`sha256`/version, REA exit
code and carrier path — all present and committed), no test calls `parseEvidence`, no test inspects
`environment`, and no test executes anything but `git` and `node xpin`. `grep` over the counter confirms the
only `subprocess.run` calls outside the selftest are `git` (line 41) and `node xpin` (line 95).

## 5. Indistinguishability of genuine and forged states (observed)

Comparing the per-carrier block from the run at lane HEAD over the **genuine** receipts with the block from my
**fabricated** fixture: `diffs == []` for every field of K1/K2/K3/K4 (`after_evidence_id_ok`,
`after_operation_ok`, `after_oracle_hits`, `after_present`, `after_sasquatch_gap`, `after_subject_ok`,
`before_*`, `oracle_files`, `oracle_frozen`, `matched`). Example K3, identical on both sides:

```json
{"after_evidence_id_ok": true, "after_operation_ok": true, "after_oracle_hits": 2130, "after_present": true,
 "after_sasquatch_gap": false, "after_subject_ok": true, "before_evidence_id_ok": true,
 "before_operation_ok": true, "before_oracle_hits": 0, "before_present": true, "before_sasquatch_gap": true,
 "before_subject_ok": true, "id": "K3", "matched": true, "oracle_files": 2130, "oracle_frozen": true}
```

The only difference between the two lane-level runs was the `bindings` block, because C1's entry has not
landed at `d2e46ef5`; my fixture supplies it. In other words: **once C1 lands its entry/rows, the counter's
output for a fabricated after set is identical to its output for the real one.**

## 6. Checks that held (so the report does not overclaim)

- **Subject binding is real.** Cross-carrier replay (F8) fails: `after_subject_ok false`, `after_oracle_hits 0`.
- **Exact coverage is real.** One missing oracle row (F9) → `2129 != 2130` → red. The duplicate-sha and
  path-suffix census (F10) shows no way to cover two rows with one published file for any frozen carrier.
- **Carrier identity is honest.** The two live release assets were fetched and hashed:
  `nvim-linux-x86_64.appimage` 11,454,968 B → `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb`,
  `nvim-linux-arm64.appimage` 11,356,680 B → `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2`,
  both equal to `carriers.json`. The committed K1/K2 fixture images hash to their declared shas.
- **The oracle is honest.** `/usr/bin/unsquashfs` 4.7.5 at offset 944632 (K3) / 936456 (K4) (`hsqs` magic
  confirmed) reproduces `K3/oracle.tsv` and `K4/oracle.tsv` **byte-identically** (`cmp` clean, 2130 rows each).
  So the two cheap-input hypotheses the seat listed for *these* artefacts — fabricated carriers, fabricated
  oracle — are refuted: the attack surface is the receipt layer, not the reference layer.
- **The frozen selftest still passes**: `--selftest` → `{"cases": 14, "green_ok": 1, "red_ok": 13,
  "failures": []}`, exit 0, while F1 passes. The 13 red cases cover do-nothing, stale-id edits
  (`after := before`, forged oracle copy, `before := after`), post-freeze changes to the oracle or
  `carriers.json`, and binding/label mistakes. None of them is a self-consistent forgery — the one variant the
  frozen control family does not cover.

## 7. All counters/receipts produced by this seat

| tag | fixture rev | `--pkg65` | met | matched |
|---|---|---|---|---|
| F1/F2 fabricated after | `ddadb784` | 6.5.0 (frozen path) | true | 4 |
| F3 schema-valid edited before→after | `d76b345b` | 6.5.0 | true | 4 |
| F4 stale id, honest rule | `0916fab6` | 6.5.0 | false | 0 |
| F4 stale id, substituted rule | `0916fab6` | patched copy | true | 4 |
| F9 near miss (K3 −1 file) | `ebc2d8d5` | 6.5.0 | false | 3 |
| F6 both receipts fabricated | `68b5ee38` | 6.5.0 | true | 4 |
| F7 before labelled sasquatch-present | `77b645b5` | 6.5.0 | true | 4 |
| F8 replay K3→K1 | `e9700116` | 6.5.0 | false | 3 |
| F8 subject relabel K3→K1, stale id | `0548d216` | 6.5.0 | false | 3 |
| F8 subject relabel, stale id, substituted rule | `0548d216` | patched copy | false | 3 |
| F5 6.7.0 ids, 6.7.0 root | `5dc3d255` | rea-agents 6.7.0 | false | 0 |
| F5 6.7.0 ids, 6.5.0 root | `5dc3d255` | 6.5.0 | true | 4 |

Each row came from its own fresh fixture repo (`git -C <fixture> init`), so the freeze commit hash differs per
fixture (for the F1/F2 repo it is `6d7f3fd0bfded8b425578b132063acad8bde47d8`); every one of them contains the
same frozen bytes taken from `790561d4`. These fixture hashes are recorded for traceability only — the repos
lived under scratch and were removed; the receipts' content is quoted here and reproducible from §3.

The last two rows are the rule-pinning result: minimal forged records are id-stable across the two pins, while
the four **authentic** receipts fail the "6.5.0 rule" the moment the package root changes (F5 run: all
`before_evidence_id_ok: false`, 0/4). The stored id is therefore bound to a *path the caller supplies*, not to
a version or a byte image.

## 8. Root cause and smallest safe correction

Root cause, stated exactly: P36-C1 mixes a capability claim ("ran with sasquatch on PATH and published these
files") with a data claim ("these committed bytes say so"). The counter can only test the second: every input
it examines is writable by the claimant, and the one field that names the capability (`extraction_gaps`) is
itself claimant-authored. A canonical-JSON hash does not change that — it authenticates *what the record says*,
not *that it happened*.

Because the predicate, counter, carriers and oracle are frozen, no edit is admissible this round. The smallest
safe corrections, in order:

1. **Do not accept C1 on the counter receipt alone.** Pair the receipt with an out-of-band witness recorded in
   the round report: a second party re-running `tools/round-36/c1-run.sh after K? <tmp>` with sasquatch on
   `PATH` at the measured revision, plus the same for `before`. This closes the fabrication gap for the
   capability question (it still does not authenticate the committed bytes, but the two together do).
2. **For a machine check, it must execute.** The only input a claimant cannot author is a fresh extraction.
   A round-37 counter that runs `unblob` twice per carrier (sasquatch present / stripped) and compares against
   the committed receipts and the oracle is the only form of this predicate that is falsifiable at all.
3. **If a data-only counter is kept anyway** (raises cost, does not close the hole): pin the rule
   implementation by state — record `sha256(dist/domain/canonicalDigest.js)` and
   `sha256(dist/domain/evidence.js)` and `package.json` name/version `rea-agents@6.5.0` in the freeze and
   reject anything else (kills F4, F5); require `parseEvidence` acceptance and attribution `6.5.0` only
   (kills F2, F6, F7); compare `before.json` bytes to the freeze (kills F6, and any post-freeze relabelling);
   require `raw_result` present and free of a `missing-extractor-dependency` naming sasquatch anywhere in it
   (kills F3, the internally contradictory edit); require the already-committed `K*/after-run.json` to agree
   with the envelope (`exit 0`, `sasquatch_sha256` non-empty, `carrier_sha256 == carriers.json`, engine hash
   equal) — cost-raising only. None of these makes F1 hard: a determined fabricator can synthesize
   `raw_result` and `after-run.json` too, because they are the same kind of bytes.

The honest summary for the close: **C1's counter measures repository content, not the capability.** A green
C1 receipt is exactly as strong as the claimant's assertion that the run happened — which is what a verifier
re-run or an executable counter is for.

## 9. Impacted axes

- **coverage (C1's own axis):** C1 claims the squashfs-recursion capability moves Frontier → Core. The counter
  cannot establish that move: a `carriers_matched == 4` state is producible with the capability absent. If C1
  lands on the counter alone, coverage is asserted, not shown.
- **calibration:** the counter emits the same per-carrier block for genuine and fabricated input (§5), and its
  verdict also depends on unpinned local state — an authentic receipt set goes 0/4 under a different but
  genuine package root (F5). Verdict depends on machine state, not only on the repo.
- **depth:** not touched; no claim here bears on it.
- **falsifiability (round-level):** the frozen control family has no case for a self-consistent forgery, so the
  kill rule cannot fire on the cheapest attack class. This is a control-coverage gap, not a counter bug: F4
  shows the `CTL-C1-2` shape going green when only the rule implementation is substituted.

## 10. Disclosure, tooling, cleanliness

- Installs: none. No pacman, no `uv tool`, no `~/.local/bin` change. sasquatch and unblob were not touched.
- Network: two neovim v0.12.6 AppImage downloads (11,454,968 B and 11,356,680 B) and `npm pack
  rea-agents@6.7.0` (6,276,963 B) — all into scratch, none executed, none installed. Records:
  version 6.7.0, channel npm registry, reason: test whether the counter's "6.5.0 rule" is pinned.
- REA: no `extract-firmware` invocation, no `npx rea-agents` run, no REA MCP device. The only REA code executed
  was the lane's frozen `xpin-attribute.mjs`, which imports the pinned packages' own `dist/domain/` modules —
  exactly what the frozen counter itself does — plus the same tool pointed at a 6.7.0 root for F5.
- VCS: read-only (`git show`, `log`, `rev-list`, `rev-parse`, `ls-files`, `cat-file`). Fixtures were created with
  `git -C <fixture> init` in scratch and every later call named `-C <fixture>`; `rev-parse --show-toplevel` was
  asserted equal to the fixture path before the first commit. The lane was never mutated.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36CriticC1Shortcut` was removed before this report was finished;
  every command, output, byte count and id cited above is inline here, not a scratch path.
