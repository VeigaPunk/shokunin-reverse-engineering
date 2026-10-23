# ExecSettleGate — tools/round-30/settle-gate.py (seat-settlement gate, round-29 routed defect 4 / M29-1)

Seat: `KaidokuR30.ExecSettleGate` (executor, round-30 wave 1). Lane read-only; the only lane write is
this report. No REA, no subagent, no tool installs, no git/jj writes.

## 1. What was built

`settle-gate.py` — a seat-settlement gate for filing time, written for integration as
`tools/round-30/settle-gate.py` (scratch source: see §6). It answers M29-1's open question: *is every
seat of the round settled before filing, and are the settled report bytes the ones on disk?*

    python3 -I -B settle-gate.py --root <LANE> --round <N>      # N = 29 or round-29
    python3 -I -B settle-gate.py --selftest

It reads (filesystem only — no git, no subprocess, no writes, no network):

- every `.ufo/waves/round-<N>/*/swarm-registry.json` member list (the dispatched seats); the
  registry's `reportDir` names the wave's report directory (absent → the registry's own directory);
  a member's report is `<reportDir>/<name>.md`;
- the ledger `.ufo/waves/round-<N>/settle.tsv`: required header, columns read by header name
  (`name`, `status`, `utc`, `report_sha256`, optional `note`); `status` ∈ `returned|cancelled|dead`;
  a row key is the bare member name or `<wave>/<name>` (the wave is the registry directory name,
  e.g. `w1`) when a round re-uses a name across waves; blank lines and `#` lines ignored.

Findings (exit 1):

| code | condition |
|---|---|
| `MISSING_LEDGER` | the ledger file does not exist — nothing is settled |
| `MISSING_ROW` | a registry member has no ledger row |
| `REPORT_ABSENT` | a returned member's report file is absent (or unreadable) |
| `REPORT_SHA_MISMATCH` | a returned member's report bytes differ from the settled sha256 — a seat that rewrote its report after settling |
| `REPORT_WITHOUT_NOTE` | a cancelled/dead member left a report and its row carries no note |

Exit 0 when there are no findings; 1 when there are; 2 on usage errors or unevaluable input (round
directory absent, no registry, unreadable/malformed registry or ledger: unknown status, malformed
sha256 or utc, duplicate row key, ambiguous bare row key for a name used in more than one registry
of the round — such a row must be qualified `<wave>/<name>`). A ledger row that settles no member
prints `WARN STRAY_ROW` and does not fail the gate.

Name collisions across waves are real in the lane (round-23 `CoverageMap` in w1+w2; round-28 has
30+ names shared by w1/a2/a2w — scanned over all 29 committed registries), hence the qualified-key
form; a single row cannot carry two different report shas. [observation]

Limits stated in the tool docstring: the ledger is author-written (agreement with the bytes on
disk, not honesty of a settlement); reads the working tree only, so a report rewritten after the
gate run is not caught — run it last, immediately before the filing commit, like
`tools/round-29/prefile-check.sh`; `utc` values are recorded, not authenticated.

## 2. Selftest — `--selftest` with fixtures

Command (from the scratch seat dir, `TMPDIR` under it):

    TMPDIR=…/ExecSettleGate/tmp timeout 300 python3 -I -B settle-gate.py --selftest

Full stdout, exit 0 (`selftest.txt`, sha256 `21dbce5f…`):

```
ok green-clean got=0 want=0 code='settle: PASS'
ok red-missing-row got=1 want=1 code='MISSING_ROW w1/ScoutD'
ok red-returned-report-absent got=1 want=1 code='REPORT_ABSENT w1/ExecA'
ok red-r28-report-changed-after-filing got=1 want=1 code='REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix'
ok red-cancelled-report-without-note got=1 want=1 code='REPORT_WITHOUT_NOTE w1/CriticC'
ok green-cancelled-report-with-note got=0 want=0 code='settle: PASS'
ok red-no-ledger got=1 want=1 code='MISSING_LEDGER'
ok green-qualified-keys-two-waves got=0 want=0 code='settle: PASS'
ok error-ambiguous-bare-key got=2 want=2 code='is ambiguous'
ok error-bad-status got=2 want=2 code='status'
ok error-bad-sha got=2 want=2 code='not a sha256'
ok error-duplicate-row got=2 want=2 code='duplicate ledger row'
ok green-stray-row-warns got=0 want=0 code='WARN STRAY_ROW Ghost'
selftest cases=13 failures=0
```

13/13, exit 0, 2026-10-23T02:45Z. The round-28 shape case is fixture
`red-r28-report-changed-after-filing`: ledger carries the sha of the filing-time bytes
(`19:25:35Z` marker) while the file on disk carries the later rewrite (`19:26:31Z` marker) →
exit 1, `REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix`. Fixtures are built under `TMPDIR` and removed
on success; the selftest needs no lane.

## 3. Round-29 run on a clone (acceptance)

Sandbox clone (contract form), HEAD `4ee65c6771058284aa947a266475839d196ed4d4`; receipt
`round29-clone.txt`, sha256 `8561cf1f…`:

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin clone
$ git -C clone rev-parse HEAD
4ee65c6771058284aa947a266475839d196ed4d4
$ timeout 300 python3 -I -B settle-gate.py --root clone --round 29
settle: round-29 root=…/ExecSettleGate/clone registries=1 members=44 ledger=.ufo/waves/round-29/settle.tsv rows=0
settle: MISSING_LEDGER .ufo/waves/round-29/settle.tsv
settle: FAIL (1 findings)
exit=1
```

Exit 1 as required: no ledger exists, so none of round-29's 44 dispatched seats is settled.
[observation] 2026-10-23T02:45Z. The same run against the live lane (read-only, `lane-live-readonly.txt`)
prints the identical result, exit 1.

## 4. Shown able to fail — and to pass — on real round-28 data

Round-28's defect is real and still in the lane: `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md`
is `fcb8e28061bcdacae2daa7702c134bb754a6fc4410496705e39ee928c47705e5` at the filing commit
`242b0d8b` and `7ed676593a0b3c85719eb6718ea454d2bae4d29422256d59b49c38c8dfa960bb` at HEAD
(`git show 242b0d8b:… | sha256sum` vs `sha256sum`; read-only). [observation]

In the clone, `make-demo-ledger.py` writes `.ufo/waves/round-28/settle.tsv` with one qualified row
per member of all three round-28 registries (142 rows; `returned` + current sha where a report
exists, `cancelled` otherwise; utc is the fixture constant `2026-10-22T19:25:35Z`). Receipt
`round28-demo.txt`, sha256 `669288c9…`, 2026-10-23T02:45Z:

```
$ python3 -I -B settle-gate.py --root clone --round 28        (variant head: shas of the clone's bytes)
settle: round-28 … registries=3 members=142 ledger=.ufo/waves/round-28/settle.tsv rows=142
settle: PASS
exit=0

$ python3 -I -B settle-gate.py --root clone --round 28        (variant filed: ExecR27SelftestFix pinned to the 242b0d8b bytes)
settle: round-28 … registries=3 members=142 ledger=.ufo/waves/round-28/settle.tsv rows=142
settle: REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix ledger=fcb8e28061bcdacae2daa7702c134bb754a6fc4410496705e39ee928c47705e5 file=7ed676593a0b3c85719eb6718ea454d2bae4d29422256d59b49c38c8dfa960bb
settle: FAIL (1 findings)
exit=1
```

[observation] The head variant passes (the gate is not red by construction on real round-28 data);
the filed variant exits 1 with exactly one finding — the real rewritten report, named, with both
shas. A round-29 synthetic green ledger (44 rows: 43 `returned` + `CriticAxisFit` `cancelled`, it
filed no report) gives `settle: PASS` exit 0, and removing that ledger returns to exit 1
(`round29-demo.txt`, sha256 `756bd848…`). [observation]

## 5. Edge cases (receipt `edge-cases.txt`, sha256 `49814222…`, 2026-10-23T02:46Z)

- `--round 25` (no registry under that round): `settle: ERROR no swarm-registry.json under .ufo/waves/round-25`, exit 2.
- `--help`: exit 0. No args: `error: --root required`, exit 2.

## 6. Scratch artifacts (all under /fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecSettleGate/)

| artifact | sha256 |
|---|---|
| `settle-gate.py` (the tool; L1 integrates to `tools/round-30/settle-gate.py`, mode 0755) | `1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5` |
| `make-demo-ledger.py` (demo ledger generator) | `f1b83301ff117c3ea2e3984e8a52528eceacc416f986ffeceaeeda515c775bc2` |
| `run-receipts.sh` (runs §3–§5) | `feeec9bbfb8dd5ef337cb95b7cf6cbed4bcee5f0618ce8962075de6441b21bd1` |
| `selftest.txt` | `21dbce5fbd528f7487d0626eb78635023ff887cc01c37d9248708fa81911bea5` |
| `round29-clone.txt` | `8561cf1ff3cf41165f612ef66666394325966d8a4de617e7fd77d2cca333a1e5` |
| `round28-demo.txt` | `669288c9a0eefe738d48b876da24ddc5385904384883a8c65c8274807974093d` |
| `round29-demo.txt` | `756bd848e85c1edaccbfacba2988925b6b915894aa8b3a54e769b9ef4d8153ed` |
| `lane-live-readonly.txt` | `f0854dc53589254cdd0c54d752dc6c5ee38ebebae2f321adae48b7a6b8806655` |
| `edge-cases.txt` | `49814222aef75d41e767a970660fd4753e2a58b3a2446dc4cb398fc23b8e95ad` |
| `clone/` (sandbox clone at `4ee65c67`; holds the demo `settle.tsv` fixtures in its round-28 dir) | n/a |

No process left running; every command was capped with `timeout` ≤ 600 s.

## 7. Integration notes, risks, blockers

- Run `python3 -I -B tools/round-30/settle-gate.py --root <LANE> --round 29` **last** in the filing
  sequence (it reads the working tree; a later write is invisible to it). It is read-only: no git
  invocation, no writes, no locks.
- The gate is red on round 29 until the L1 writes `.ufo/waves/round-29/settle.tsv` (44 rows for
  `w1`; `CriticAxisFit` filed no report). That red state is correct and expected — it is the M29-1
  condition that no tool previously checked.
- Ambiguous bare ledger keys are refused (exit 2), not silently applied, when a name appears in
  more than one registry of the round; use `<wave>/<name>` there.
- Not checked (out of scope): honesty of a settlement, wall-clock ordering of `utc` against report
  content, and reports of seats that are in no registry.
- Blockers: none. No tool installs were needed; no REA was run; no subagent was spawned.
