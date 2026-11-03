# Kaidoku round 64 — bounded ZIP occurrence craft

Lane: kaidoku. Date: 2026-11-03 UTC.
Final lane HEAD: `98eab3ab559033a452fd07cf1d333e9b0cb85da9`.
Working branch: `train/kaidoku-round64-cloud`.
Base: `c7fe6898e9a8b3ff04486b4a1d672e9db37610c9`.
First and unchanged claim freeze: `300e87a713b3f6f91aed80a29e08ca91228f7f76`.
This report is staged after committed lane work and final clean-head checks.

## Outcome and claim

R64-C1, depth capability acquisition, is independently verified and accepted
by the parent within its declared profile. The new standalone reader retains
central-directory ordinal, local-header offset and per-occurrence payload
digest when ZIP members have duplicate names. It preserves equal-payload
occurrences too. It provides bounded malformed/unsupported refusals without
extracting or executing members. Existing APK occurrence knowledge is
explicitly acknowledged; this is not its first discovery.

All 19 frozen cases matched the independent construction-derived oracle.
Fourteen fixture byte instances changed after freeze and five were identical
boundary re-observations. All six named shortcut readers failed the full
19-case target: collapse-by-name 14/19, physical-order sorting 18/19,
filename lookup 15/19, identity replay 12/19, no-op 0/19, all-false 0/19.
These finite results establish neither universal ZIP validity/security nor
runtime duplicate selection, signature authenticity or statistical accuracy.

The 19 cases are archive budget, central-directory permutation, count
boundary, count budget, CRC failure, deflated duplicates, different-payload
duplicates, empty archive, encryption, local-header name mismatch, member
boundary, member budget, metadata-only paths, NUL name, reversed payloads,
equal-payload duplicates, total budget, truncation and unsupported method.
The accepted input profile is at most 8 MiB, 128 entries, 1 MiB per member
and 4 MiB total, STORE/DEFLATE, ASCII names without NUL truncation and no
encryption. One inert 8 MiB + 1 byte negative was expressly authorized;
the reader refuses it before ZIP parsing. It does not increase the cap.

## Evidence and landed changes

- Declaration/instruments: `47b97eb180e8290f0009aceb4db502a38eb7bf37`.
  `tools/round-64/` contains the reader, independent raw-record fixture
  writer, semantic comparator, shortcut writer and admission wrapper.
  LOG records preparation and its mistakes; SKILL registers the commands.
- Freeze: `300e87a713b3f6f91aed80a29e08ca91228f7f76`, after the actual
  19-case end-to-end scratch-clone dry run. Exact declaration and pins are
  `.ufo/waves/round-64/claims.json` and `plans/round-64-claims.md`.
- Data/craft: `d9a04cd5a72ad82de2f0b9885d70d591628731ca`.
  `.ufo/waves/round-64/data/comparison.json` retains actual argv, UTC,
  stdout/stderr, return codes and semantic comparisons. All fixture bytes,
  expected records and generation custody are committed alongside it.
  `corpus/knowledge/2026-11-03-r64-zip-occurrences.md`, the SKILL table and
  checklist, source S264 and the corpus index provide reusable craft.
- Independent review and original blocked disposition are preserved under
  `.ufo/waves/round-64/review/`, including the exact assessment by
  `/root/judge_kaidoku_round64`, appointed by the parent. This is not author
  self-admission. Fresh shortcut receipts are under `closure/`.
- Closeout metadata: `d6d4363ed39fadb281c34eec90051e97423d8edb` appends the
  current disposition to LOG, SCORECARD and the round lesson. Final
  committed receipts at `98eab3ab559033a452fd07cf1d333e9b0cb85da9` are under
  `.ufo/waves/round-64/final/`. Every change group has an appended LOG entry.

Reader outer-CLI selftest: 2/2. Independent comparator: 8/8. Admission
wrapper: 11/11, including alternate freeze, changed claims, old evidence,
old run time and typed semantic negatives. Independent review preserves
both initial comparator false accepts and their pre-freeze corrections.
Original frozen instruments, cases and expectations were not changed.

## Original block and prospective authority

Original filing really was blocked. Under QUALITY 47 the old mandatory
prefile required both legacy and active-v2 legs. The baseline legacy ledger
already missed rounds 53–63 and included the retired round 35 declaration.
The new round 64 omission was repaired by its actual audited row, but the
historical problem remained. Two bounded Git status attempts first exited
2 on threaded-lstat initialization. A separately authorized same-cap retry
with per-process core.preloadIndex=false reached the real old prefile
failure: clean tree, legacy exit 1, active-v2 exit 0. Those receipts and the
blocked review were preserved, never relabelled successful.

Independent diagnosis established deliberate retirement of the round 35
claims path; restoring it would produce another mismatch. The separately
reviewed versioned migration was prospectively adopted in
`4c8a09ebd4f45b7109d32af9d6d802707ee9a772`, with active adoption receipts
committed at `36a297cc1048848036f896fc4e9a1346c543bb8d`. QUALITY 102 now
names `tools/ledger-reconciliation-v1/prefile-check.sh` as current authority.
The migration preserves the original ledger byte prefix and exact retired
source history, checks every live tuple, rejects unknown strays/revivals,
and retains the unchanged active-v2 leg. Sixteen independent adversarial
outcomes support the migration. Its output still includes legacy exit 1.
This is current accounting repair, not retroactive filing success, a waiver,
or an additional technical capability claim for round 64.

## Final verification

After the last corpus metadata append, revision
`d6d4363ed39fadb281c34eec90051e97423d8edb` produced:
- prospective prefile exit 0;
- versioned reconciliation required-clean round 64 exit 0;
- original frozen technical admission: met, 19 cases, exit 0;
- unchanged active-v2 disclosures: 39/39 exact;
- registry: 75/75, exit 0;
- source census: exit 0, 171 rows and 19 standing W04 warnings.

Exact producer commands, timestamps and outputs were committed in
`.ufo/waves/round-64/final/` before this report was staged. At final HEAD
`98eab3ab559033a452fd07cf1d333e9b0cb85da9`, the versioned prefile was run
again at `2026-11-03T02:53:58.067613+00:00`, exit 0. Its stdout reports:

```text
prefile-reconciliation-v1: tree clean
prefile-reconciliation-v1: prospective ledger reconciliation exit=0
prefile-reconciliation-v1: active v2 ledger exit=0
prefile-reconciliation-v1: PASS (prospective only)
```

The exact invocation was `timeout -k 2 180 prlimit --as=536870912
--cpu=160 --fsize=16777216 --nofile=64 sh
/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kaidoku/tools/ledger-reconciliation-v1/prefile-check.sh
/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kaidoku`, with
per-process index.threads=1 and core.preloadIndex=false. Full final-head
stdout/stderr and command record are in the sibling outbox directory
`audit/kaidoku64-closeout/final-head-*`. All source/corpus-input hashes
still matched the committed census receipt, all original instrument pins
matched, and the lane tree was clean. No persistent config or security
setting was changed.

## Sources & frontier

Source rows: 170 → 171, measured by the source-row pattern and maintained
census command in the retained receipts. Added S264: one tier A official
Python documentation row. Tiers A 156 → 157, B 9 and C 5 unchanged;
mined 161 → 162, rejected 9 unchanged. Every old source row is byte-preserved;
no old source-row fields changed. The docs were served as Python 3.12.16;
actual runtime 3.12.14 and its installed module digest are separately pinned.
Source excerpts, quote location and limited support are in the lesson Gate.
No Frontier-to-Core REA promotion or new provider capability is asserted.
Assimilation: none. Mistakes mined: inadequate novelty search, permissive
JSON comparison, caller-selected freeze, and boundary-authorization timing.

## Axes, scope and carried limits

Depth repertoire improves under the independent technical finding.
Coverage/calibration and all numeric axis scores remain unchanged at
10/10/10. Existing archive/package scope is unchanged. No promotion is
claimed. Registry growth is distinguished from expertise: 68 → 73 registered
paths for domain work, then 75 after two separately adopted accounting tools;
the old registry snapshot also caught up 12 previously registered paths.

Historical bare-name receipt findings, D60-1 edge mismatch, 19 W04 warnings
and the historical round 53 L0 question remain carried. Migration only
resolves present ledger accounting under new prospective authority.
Cross-domain evidence: the ledger conformance repair was separately
parent-reviewed; it receives no archive capability credit. No extraction,
unknown shipped-binary execution, credentials/client-config read, install,
new authentication, push, main update or round 65 occurred.

The approved host adaptation used sequential specialist work and an
independent reviewer, not a claim of eight simultaneous workers. All round
64 review work is settled. This manual parent dispatch has no observed
watchdog tick/mission-age channel; no unsupported stale-driver conclusion
is made.

## SHONEN

- [~] SKILL.md has a sourced ZIP decision table, refusal cases and checklist;
  `corpus/knowledge/2026-11-03-r64-zip-occurrences.md` and independent review.
- [~] End-to-end bounded archive analysis executed and logged; committed
  `.ufo/waves/round-64/data/comparison.json` and fresh shortcut receipts.
- [~] Standalone reader and registered commands have reproducible fixtures,
  pins, outer-CLI controls and committed evidence; no oral context required.
- [~] Archive/package scope retained, PROVINCE unchanged, observation,
  inference and unknown separated. Promotion remains a separate decision.
