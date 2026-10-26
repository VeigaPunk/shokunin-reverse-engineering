# R38ExecEnvelopeRules — envelope identity (R36-CL6) and argv retention on the K1..K4 after-arm receipts

Seat: `R38ExecEnvelopeRules` (executor, leaf). Claim under audit: **R38-C1**. Measured at lane
HEAD `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` (freeze `e059ca93`, counters unchanged since the
freeze: `git diff --stat e059ca93 HEAD -- tools/round-38/c1-counter.py tools/round-38/c2-counter.py
.ufo/waves/round-38/c1/carriers.json` → empty). REA `rea-agents@6.5.0` from
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, unblob 26.6.4
(`~/.local/bin/unblob`), `sasquatch-v4be` from `~/.local/bin`.

Verdict in one line: **the identity rule holds on every round-38 after-arm receipt (identity is
`subject.digest.sha256` = frozen pin, never `local_path`; the counter never reads `local_path`), and
every receipt retains `parameters.path` / `output_directory` / `max_depth` — but the retained
parameters cannot reproduce the run, because the extractor-resolution axis is not recorded and two
carriers produce opposite results from byte-identical parameters; and K2 carries a permanent
`unpublished-entry` gap that makes the frozen target 4 unreachable.**

## 1. Identity (R36-CL6) compliance — K1..K4

Receipts produced by this seat: `artifacts/R38ExecEnvelopeRules/envelope-K{1..4}.json`
(REA `extract-firmware --format json`, carrier argument = the committed lane carrier, fresh output
root under scratch, ambient PATH ⇒ `sasquatch-v4be` resolvable). Identity recomputation uses the
counter's own tool: envelope wrapped as `{"data": <env>}` and run through
`node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0> --pkg67 <same>`.

| carrier | frozen pin (carriers.json) | `subject.digest.sha256` | identity = pin | `subject.local_path` | `parameters.path` | handler | gaps | oracle | `evidence_id` recomputes (xpin, pkg65=pkg67) |
|---|---|---|---|---|---|---|---|---|---|
| K1 | `1cfb6c33…8286117e` | `1cfb6c33…8286117e` | yes | committed lane carrier, resolves | committed lane carrier, resolves | `squashfs_v4_be` | 0 | 5/5 | yes — `ev_25d5ab34e0890e60dec1e31d1309e7608577c8a1e8326da1aee6ae8c6ab349eb` |
| K2 | `403cb0a8…cbc99154` | `403cb0a8…cbc99154` | yes | committed lane carrier, resolves | committed lane carrier, resolves | `squashfs_v4_be` | **1** | 3/3 | yes — `ev_c49ff4ced8532c6b7620512c7de75adb0792884d3d2f9f12443dd80a55f0ba48` |
| K3 | `9c7c523c…b69397c0` | `9c7c523c…b69397c0` | yes | committed lane carrier, resolves | committed lane carrier, resolves | `squashfs_v4_be` | 0 | 4/4 | yes — `ev_e23dbfd922fe450e6bc6315e931b49f5e25d40a7b18181262fee67b81449e54a` |
| K4 | `a29ddc15…dfe956ed` | `a29ddc15…dfe956ed` | yes | committed lane carrier, resolves | committed lane carrier, resolves | `squashfs_v4_be` | 0 | 4/4 | yes — `ev_f9cb9ba33d3fc22c275115703095beff9a61c1de435fe13df67277f4269ce51e` |

Cross-check against the independently produced peer set
`.ufo/waves/round-38/w1/artifacts/R38ExecProvincePatch/after-K{1..4}.json` (same committed carriers,
output roots inside the lane artifacts dir): identical verdicts — K1 `ev_eccca733…` 5/5 gaps 0;
K2 `ev_66d89e96…` 3/3 gaps 1; K3 `ev_05731564…` 4/4 gaps 0; K4 `ev_b62e21b8…` 4/4 gaps 0; all four
`subject.digest.sha256` = pin, all four `subject.local_path` and `parameters.path` = committed lane
paths that resolve, all four recompute under xpin.

So the R36-CL6 fix is *observable* on this round's receipts in the sense that matters: the identity a
reader needs is the digest, the digest is pinned before any run in
`.ufo/waves/round-38/c1/carriers.json`, and the bytes named by `parameters.path` are committed at the
base, so nothing depends on a scratch path. `grep -c local_path tools/round-38/c1-counter.py` → `0`:
the scoring path cannot be steered through `local_path` at all.

## 2. Parameters / argv retention

| receipt field | K1 | K2 | K3 | K4 | what a reader needs it for |
|---|---|---|---|---|---|
| `parameters.path` | committed carrier | committed carrier | committed carrier | committed carrier | re-run subject |
| `parameters.output_directory` | fresh scratch root | fresh scratch root | fresh scratch root | fresh scratch root | re-run destination (volatile by nature) |
| `parameters.max_depth` | 3 | 3 | 3 | 3 | depth bound |
| `parameters.max_output_bytes` / `max_output_files` | 268435456 / 10000 | same | same | same | budgets |
| `provider.id` / `provider.version` | unblob / 26.6.4 | same | same | same | extractor |
| `raw_result.execution.args` | full unblob argv (depth, report, log, extract-dir, input) | same | same | same | what ran |
| `environment` | **null** | **null** | **null** | **null** | nothing |

All four retain the three required fields, and the unblob argv is retained too. Two retention gaps
remain, both out of the counter's reach (`grep -n parameters tools/round-38/c1-counter.py` → no
match: the counter never validates `parameters` at all, so retention is a report-level obligation,
not a scored one):

1. **The extractor-resolution environment is nowhere in the envelope.** `environment` is `null` on
   every arm; no field names the `unblob` executable, `REA_UNBLOB_COMMAND`, or `PATH`. See §3 —
   this is not cosmetic: it decides whether the run extracts anything.
2. **`evidence_id` is per-run, not per-subject.** Two runs of K1 with the same carrier and the same
   `max_depth` produced different ids (`ev_25d5ab34…` vs `ev_5353626b…`); the peer summary lists the
   volatile inputs (`normalized_result.output_directory`, `parameters.output_directory`,
   `chunks[].provider_id`, `raw_result.execution.args[7,9,11,12]`, staging paths). So "recomputes to
   its stored evidence id" holds for the *stored bytes* (xpin, verified for these four and for the
   twelve peer receipts listed in §5) and never for a fresh re-run. A reader must compare `subject.digest.sha256`, not
   `evidence_id`.

## 3. The unrecorded axis: `sasquatch-v4be` on PATH (falsifies the C1 sentence "no external extractor dependency")

Same four carriers, same argv, same retained parameters, PATH without `~/.local/bin` (`sasquatch-v4be`
unresolvable; `unblob` still reachable via `REA_UNBLOB_COMMAND=/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`).
Envelopes: `artifacts/R38ExecEnvelopeRules/envelope-K{1..4}-clean-path.json`.

| carrier | sasquatch-v4be resolvable | files | gaps | gap dependency | oracle hits | `evidence_id` |
|---|---|---|---|---|---|---|
| K1 | yes | 5 | 0 | — | 5/5 | `ev_25d5ab34…` |
| K1 | no | **0** | **1** `missing-extractor-dependency` | `["sasquatch-v4be"]` | 0/5 | `ev_12d06001…` |
| K2 | yes | 3 | 1 `unpublished-entry` | — | 3/3 | `ev_c49ff4ce…` |
| K2 | no | 0 | 1 `missing-extractor-dependency` | `["sasquatch-v4be"]` | 0/3 | `ev_1f1101ad…` |
| K3 | yes | 4 | 0 | — | 4/4 | `ev_e23dbfd9…` |
| K3 | no | 0 | 1 `missing-extractor-dependency` | `["sasquatch-v4be"]` | 0/4 | `ev_de2fa6ec…` |
| K4 | yes | 4 | 0 | — | 4/4 | `ev_f9cb9ba3…` |
| K4 | no | 0 | 1 `missing-extractor-dependency` | `["sasquatch-v4be"]` | 0/4 | `ev_482857c7…` |

The two arms differ in `PATH` only; every retained field except `output_directory` is identical.
This reproduces the peer finding (`artifacts/R38ExecAfterK1/summary.json`, K1 off-PATH
`ev_fd9baf66…` 0 files / on-PATH `ev_5353626b…` 5 files) on all four carriers, and agrees with
`R38ExecAfterK3/after.json` (`ev_bb5d941f…`, 0 files, 1 gap) being the off-PATH arm while its
post-fix harness run (`ev_fbc3be2e…`, 4 files, ambient PATH) is the on-PATH arm. So the P38-C1
sentence "run with stock unblob 26.6.4; no external extractor dependency" is false for **every**
frozen carrier: unblob 26.6.4 has no in-process BE-v4 extractor and shells out to `sasquatch-v4be`.
A receipt that retains the required parameters but omits the PATH cannot tell a reader which of the
two rows above it is.

## 4. The K2 gap is structural, not an extractor problem

`artifacts/R38ExecEnvelopeRules/envelope-K2.json`, ambient PATH: 3/3 oracle files published,
`extraction_gaps = [{"kind": "unpublished-entry", "relative_path": "firmware.bin_extract/var/lib/run-link"}]`,
`unpublished_entries = [{"relative_path": "…/var/lib/run-link", "kind": "symlink", "link_target": "../../a/run.sh"}]`.

Direct unblob check (`~/.local/bin/unblob --extract-dir … --report … carrier.sqsh`, exit 0): unblob
*does* extract `var/lib/run-link` as a symlink (`lrwxrwxrwx run-link -> ../../a/run.sh`). The gap is
REA 6.5.0's publication policy — symlinks land in `unpublished_entries` and are surfaced as an
`unpublished-entry` extraction gap — not an extraction failure. K1's own symlink
(`link-to-hello -> ../hello.txt`, escaping the extraction root) takes a different path: it is removed
with a `MaliciousSymlinkRemoved` WARNING diagnostic and leaves **no** gap.

Consequence measured with the frozen counter, on a fixture repo built from committed bytes plus my
four draft receipts as `corpus/evidence/round-38/c1/K*/after.json` (`/fast/scratch/…/fx.KBgm`,
single commit `f28904a8abeda7fe081207d35532da84e65651e3`; receipt
`artifacts/R38ExecEnvelopeRules/counter-fixture-four-receipts.json`):

```
carriers_matched 3   met_target False
K1 matched True  (subject ok, handler ok, gaps 0, oracle 5/5, evidence id ok)
K2 matched False (subject ok, handler ok, gaps 1 -> after_gaps_empty False, oracle 3/3, evidence id ok)
K3 matched True  (… 4/4 …)      K4 matched True (… 4/4 …)
```

`met_target` is false in the fixture for the unrelated reason that PROVINCE/knowledge/SOURCES/README
bindings are absent there; the per-carrier block is the measurement. **As frozen, P38-C1 cannot reach
`carriers_matched == 4`: K2's carrier contains a legitimate internal symlink, and the frozen predicate
demands `extraction_gaps == []`.** I changed nothing — carrier, predicate and counter are frozen; this
is reported for the L1.

## 5. Receipts whose `local_path` is (or was) load-bearing

Ledger over 29 receipts: `artifacts/R38ExecEnvelopeRules/audit-after-receipts.json`. Classification:
a receipt's `local_path` is load-bearing when its `subject.digest.sha256` has **no committed carrier
in the lane** and the path it names no longer resolves.

| receipt(s) | `subject.digest.sha256` | committed carrier with that digest | `local_path` / `parameters.path` | load-bearing? |
|---|---|---|---|---|
| `corpus/evidence/round-36/c1/K3/{after,before}.json` | `b644d034…c35f29fb` (nvim x86_64 AppImage) | **none** (no AppImage committed; run receipts hold the digest only, no URL) | dead scratch | **yes** |
| `corpus/evidence/round-36/c1/K4/{after,before}.json` | `8efcec73…c9efe1c2` (nvim arm64 AppImage) | **none** | dead scratch | **yes** |
| `corpus/evidence/round-36/c1/K{1,2}/{after,before}.json` | `93802938…` / `ce5bf60e…` | `corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh`, `k2-le-gzip.sqsh` (sha256 equal) | dead scratch | no (digest resolves in-repo) |
| `.ufo/waves/round-37/probes/rea-k3.json` | `9c7c523c…` | round-38 carrier K3 | committed path, resolves | no |
| `R38ExecAfterK1/{after,after.repro.*,after.sasquatch-on-path}.json`, `R38ExecAfterK2/after.json`, `R38ExecAfterK3/after.json`, `R38ExecAfterK4/after-scratchcopy-crosscheck.json` | the four frozen pins | yes (round-38 carriers) | scratch copies (`R38ExecAfterK2/K2-after/carrier.sqsh` is now **gone**; the other copies still exist) | no — the digest still resolves to the committed carrier, so the dead path costs a re-run, not identity |
| `R38ExecAfterK4/after.json`, `R38ExecProvincePatch/after-K{1..4}.json`, this seat's `envelope-K{1..4}.json` | the four frozen pins | yes | committed lane carrier, resolves | no |

So the R36-CL6 residue is exactly round-36 **K3/K4** (both arms, four receipts): their identity is
stored as a digest but the only thing that ever named those bytes was the dead scratch path. The
SKILL limit 4 sentence (`SKILL.md:1277`) already says this for K3/K4; it is still true today. Every
round-38 receipt is clean on this axis.

## 6. Instrument defect found while producing the receipts (reported, not repaired)

`tools/round-38/c1-run.sh` after mode at HEAD `cb4326b2` (`sha256 08609e73…cb3c9a83`) does
`rm -rf "$OUT"` but never creates `$OUT`'s parent, while REA's own contract is
`rea extract-firmware --help` → `outputDirectory  Absent output directory; parent must exist`.
A fresh `OUTDIR` tree therefore fails:

```
bash tools/round-38/c1-run.sh after corpus/evidence/round-37/c1/K4/carrier.bin "$S/hfresh/nested/K4" "$S/hfresh-scratch"
exit=1  {"code":"execution_failure", … "reason":"Extraction output parent is unavailable"}
```

receipt: `artifacts/R38ExecEnvelopeRules/harness-after-fresh-parent-failure.json`. The documented
form `c1-run.sh after CARRIER OUTDIR` names no parent precondition, so the harness still cannot
generate claim data on a clean scratch tree; the already-reported defect it fixed was the
mirror-image one (`mkdir -p "$OUT"` → "Extraction output root already exists", reproduced by this
seat at the freeze bytes before the fix). A one-line `mkdir -p "$(dirname "$OUT")"` is what the REA
contract needs. Oracle mode was unaffected.

## 7. Evidence index

All paths relative to the lane root; all are untracked wave artifacts (L1 integrates).

| file | sha256 |
|---|---|
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/compliance-K1-K4.json` | `473951c450f069940e710888942420f0685a2319bc41f3ff83caf7af1a6d0b5a` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/audit-after-receipts.json` | `0d52eaf4209e8650ba8ef30a8a3d240cf328f74f6ca37e2edd8061164ed6104f` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K1.json` | `c43b38f36d5f6d6369f1cd879529dc37668967045e706bacaf7c3ae62005f0e3` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K2.json` | `3c9a0d7906901737b5c307ed578073c77d9e7cb6daa866ecb7b54a788e4961ca` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K3.json` | `3ac5f923d1c96829b296c81898ee60e03992cadd219cf79113cc346e69da9b45` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K4.json` | `fe6e3c80f42caf4c9622296bb7ba82747a2d1ba9869a02a76fac958a15317122` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K1-clean-path.json` | `13c3f0219beefbe415586156abafabe00949eed5b29959649f0400517260933b` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K2-clean-path.json` | `4d14c6ed61cc2ce13fb964d73edaaba86fefa0396cc2ae87421c72c98773ba39` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K3-clean-path.json` | `dc863cffe5f57d6cd94da4bbf13fcbb88849755ea8b927909ed6b034667735d2` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/envelope-K4-clean-path.json` | `1423d0af8f746009a1da455330596373beebd285a90957db0cc8b6fd9cdfba6d` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/counter-fixture-four-receipts.json` | `45532930249be2e4bf69905edd7f458426f4eb91af694312f182ff329ecd030f` |
| `.ufo/waves/round-38/w1/artifacts/R38ExecEnvelopeRules/harness-after-fresh-parent-failure.json` | `dddf10b87358e08ef26eed5612b4e6f5eebd08ab22ceb7cd00a0e9963258d0e4` |

Exact re-run argv (output roots must be absent with an existing parent):

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json \
  <lane>/corpus/evidence/round-37/c1/K{1,2}/carrier.sqsh <FRESH>/K{1,2} > envelope-K{1,2}.json
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json \
  <lane>/corpus/evidence/round-37/c1/K{3,4}/carrier.bin <FRESH>/K{3,4} > envelope-K{3,4}.json
```

## 8. Tooling, limits

- No tool installed or upgraded by this seat (npx cache, unblob 26.6.4 and `sasquatch-v4be` were
  already in place; pacman untouched). Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ExecEnvelopeRules`
  is removed on exit; every byte this report cites is copied into the artifact dir above.
- No VCS mutation, no write outside the artifact dir and this report, no write into
  `corpus/evidence/round-38`, `corpus/knowledge`, `PROVINCE.md`, `corpus/SOURCES.md`,
  `corpus/README.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`.
- `[INFERENCE]` The K2 `unpublished-entry` gap is a deliberate REA publication policy (it also
  records the link in `unpublished_entries`, so the information is not lost) rather than an
  oversight; either way the frozen counter counts it.
- `[INFERENCE]` Whether "no extraction gap" in P38-C1 was intended to exclude symlink-only gaps is
  not decidable from the frozen text; measured as written, K2 fails.
- I did not run the selftest, build, lint, or any gate: this wave's editing phase leaves that to the
  L1. The only counter execution here is the fixture scoring in §4, which writes nothing into the
  lane. It ran the **committed freeze bytes** (`git show HEAD:tools/round-38/c1-counter.py`, sha256
  `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`); I touched neither the counter
  nor the claims doc.
- **Observed, not mine:** while this report was being written the lane working tree gained
  uncommitted edits to `tools/round-38/c1-counter.py` (working sha256
  `1b4dc73003bc0f295884207d94ca5ae4888d77542f6f7f69c951c12268df9a14`, mtime 03:26:29) and
  `plans/round-38-claims.md` (`320f2f08…`, mtime 03:25:45) that move P38-C1 to a paired
  before/after form (before = `sasquatch-v4be` unavailable, after = available). Every number in this
  report was measured against the frozen bytes above; nothing here evaluates the in-flight revision.
