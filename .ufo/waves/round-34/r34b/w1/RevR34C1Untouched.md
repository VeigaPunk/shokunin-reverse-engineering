# RevR34C1Untouched — inherited-claim audit (R34-C1 inertness)

Seat: `L1Kaidoku34-2.RevR34C1Untouched` (leaf, no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, tip `c79bbe7b0959132b9873ff3431cf5eb313b58b33`
(reflog-free read; no VCS mutation performed by this seat).
Inherited claim: R34-C1 (GNU version-needs), frozen at `54a87a51a865ab931fd355e767303337b05cccf4`,
stopped before production in `claim-stop.json`. Scope of this seat: prove its artifacts are
byte-identical and prove the wave's new instruments and receipts neither execute nor score its
production reader or its twelve carriers.

**Verdict: R34-C1 UNTOUCHED — all five named artifacts byte-identical f432c8e3 → c79bbe7b, all
frozen inputs and twelve carriers still at their pinned digests, zero execution/scoring hits in the
new instruments and receipts. Two adjacent instrument defects (D1 predicate identity, D2 unverified
revision label) recorded for their owners; neither is a C1 hit.**

## 1. Byte identity, five named artifacts (the assignment)

Method A (git object level, independent of the worktree): `git ls-tree -r <rev> -- <paths>` at both
commits; identical OIDs and identical modes. Method B (content level): `git cat-file -p <rev>:<path>`
piped to `sha256sum`, then `cmp -s` between the two revisions (`UTC=2026-10-25T07:23:00Z`,
`cmp_batch_exit=0`).

| path | blob OID (both revs) | mode | bytes | sha256 f432c8e3 = c79bbe7b | worktree |
|---|---|---|---|---|---|
| `.ufo/waves/round-34/claims.json` | `d56fb8d7f3be525bd3dda07bd0d64e2340df5488` | 100644 | 7520 | `bb971710cb17ef775227cceb1b7024b7380e859564a28648709dd1c786a997a4` | `bb9717…` identical |
| `.ufo/waves/round-34/claim-stop.json` | `9e487015544013919b190a2a43e9dd596d301bf7` | 100644 | 11937 | `a00968b047f0b825dd6d5efe5a15a0ffe2ab9c0d67d023b08655ac4c0205a0e6` | `a00968…` identical |
| `tools/round-34/version-needs-counter.py` | `ac89ecd0df6e60011de66c709b91b38107683f5b` | 100755 | 17275 | `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e` | `d7f0a8…` identical |
| `tools/round-34/elf-version-needs.py` | `f69688ed1acee330d4c28576ed7e7d0b2fee549a` | 100644 | 38594 | `ac7d24a546022c7cc8295450a2692c51c07099e42a1aa02fb69c29455dae3f33` | `ac7d24…` identical |
| `.ufo/waves/round-34/w1/CtlLabels-files/size_lookup.pristine.py` | `784fc60ab7bc5d11b2f0742507a940b183cb150c` | 100755 | 15271 | `c68511f7bc2d10b005847139a5ef70331f50634a84d3d1ae63c762c570460b22` | `c68511…` identical |

Range membership: `git log --oneline f432c8e3..c79bbe7b` returns exactly one commit
(`c79bbe7b round-34: freeze R34-C2 …`), so identity across the range is equivalent to identity
across that single commit, checked at both ends.
`git diff --name-status f432c8e3 c79bbe7b -- <the five paths>` → empty. Worktree copies are clean:
`git status --porcelain --untracked-files=all -- <the five paths + all of .ufo/waves/round-34/w1/
+ corpus/evidence/round-34/>` → empty.

Lineage beyond the ask (depth): the same blobs hold from the C1 freeze point itself —
`claims.json`, `version-needs-counter.py`, `elf-version-needs.py` are identical at
`54a87a51`, `d52e2404`, `abbd7604`, `f432c8e3`, `c79bbe7b`; `claim-stop.json` and
`size_lookup.pristine.py` first appear at `abbd7604` (the stop commit) with the digests above and are
unchanged at every later commit. No relabel, no re-freeze, no counter/reader drift.

## 2. Frozen-input and evidence pins still hold

Pins are the values inside the byte-frozen `claims.json` / `claim-stop.json`; observed hashes are of
the worktree files, `UTC 2026-10-25T07:19Z`:

| item | pinned | observed |
|---|---|---|
| `.ufo/waves/round-34/expected.json` (C1 manifest, 12 carriers) | `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d` | same |
| `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` | `d721189c9df0a267c22dd566d488deb3c19e3b1365f1e1f8cfaf0ba2092aa639` | same |
| `.ufo/waves/round-34/approved-skill-section.txt` | `c156effc825c46930bc08309888102a47e7011c5b589a453dceb2e961c8d2ba6` | same |
| `prep/R34SourceNovelty-files/lsb-symversion.html` | `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91` | same |
| `prep/R34SourceNovelty-files/glibc-elf.h` | `fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f` | same |
| `tools/round-34/freeze-integrity.py` | `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138` | same |
| `prep/R34Expected-files/author_expected.py` | `916e066964ebe09c1015ed641621f9ec51354c1399eef65263537cbaf8b9c797` | same |
| `claim-stop.json` `counter_sha256` | `d7f0a8cf…e7c45e` | matches `tools/round-34/version-needs-counter.py` |
| `claim-stop.json` `control_sha256` | `c68511f7…460b22` | matches `size_lookup.pristine.py` |

Twelve carriers `corpus/evidence/round-34/elf/e01..e12.bin`: every sha256 equals its manifest pin
(`claims.json.frozen_inputs`), all mode `644`, all mtimes `2026-10-23 07:43:21–22 -0300`, i.e. pre-freeze
and not rewritten in this wave.
Control tree: `size_lookup.pristine.py` = `size_lookup.py` (the executed copy in the counterexample
argv) = `size_lookup.restored.py` = `c68511f7…`; only `size_lookup.mutated.py` differs
(`4ad7dfcd…`), modes 755, mtimes 2026-10-23 08:02. Retained control and its restoration are intact.
`git diff --name-only f432c8e3 c79bbe7b -- tools/round-34/freeze-integrity.py
.ufo/waves/round-34/prep/ .ufo/waves/round-34/expected.json corpus/evidence/round-34/
corpus/knowledge/2026-10-23-r34-elf-version-needs.md .ufo/waves/round-34/approved-skill-section.txt`
→ empty.

## 3. Grep for execution / scoring of the production reader or its twelve carriers

Scope (the wave's new instruments and receipts):
`tools/round-34/{replay-gate.py,c2-shortcut-gate-counter.py,gate-config-mini.json,gate-config-naive.json,mini-fix/**}`
and `.ufo/waves/round-34/r34b/{claims.json,after/,before/,controls/,assimilation/,w1/}` (all files,
including the four control-gate mutants and the eight synthetic fixtures).

Commands and results (`UTC 2026-10-25T07:19–07:23Z`, exit 0 for every grep below except where the
count is 0; `EXIT=1` on a grep with no match is recorded as "0 hits"):

1. `grep -rnE 'elf-version-needs|version-needs-counter|version_needs|Vernaux|Verneed' <instruments> <r34b/>` →
   **0 hits in instruments**; hits only in `w1-spec.json`, `w1-payload.json`, `w1/prompts/*.md`
   (dispatch text, which *quotes the prohibition* from the shared preamble: "…its production reader and
   twelve carriers must NOT be executed or scored").
2. `grep -rn 'corpus/evidence/round-34' tools/round-34/<new instruments>` → 0
   (consolidated count receipt: `reader_token=0 carrier_token=0`, `UTC=2026-10-25T07:23:00Z`).
3. `grep -rnE 'e0[1-9]\.bin|e1[0-2]\.bin|corpus/evidence/round-34/elf' r34b/{after,before,controls,claims.json}` → 0.
4. Word-boundary `grep -rInE '\be(0[1-9]|1[0-2])\b' r34b/` excluding dispatch text → 0
   (the one `e12=13` count inside a trace was a hash substring `…398e12c9…` in a `/tmp` opaque copy,
   verified in §4).
5. `grep -rnE 'carrier|ELF carrier|production reader' r34b/` excluding dispatch text → only
   `r34b/claims.json:75-76,84`: the declarative notes `no ELF carrier is reused from R34-C1`,
   `the R34-C1 production reader and its twelve carriers are not executed or scored this round`, and
   the retained-claim predicate echo. These are statements of non-use, not execution paths.
6. `grep -rn 'expected.json' <gate/counter/configs/control receipts>` → 0: the C1 manifest
   (`.ufo/waves/round-34/expected.json`) is never referenced; `mini-fix/expected.json` is a distinct
   eight-fixture file.
7. Sibling report `w1/RevClaimsVsInstruments.md:223` independently states the same non-execution;
   not relied on, cited for corroboration only.

Static call-graph check of every subprocess site in the new instruments (line pointers):
`replay-gate.py:79` runs `config["counter"]["argv"]` with `{reader}` substituted;
`replay-gate.py:266` runs a generated mutant of itself; `c2-shortcut-gate-counter.py:45` runs the gate;
`mini-fix/mini-counter.py:116` and `mini-fix/naive-counter.py:48` run `sys.executable -I -B <reader> <target>`.
Both shipped configs name `/usr/bin/python3 -I -B tools/round-34/mini-fix/{mini,naive}-counter.py`
with `{reader}` ∈ the eight files under `mini-fix/readers/`. No config, no default and no receipt
supplies `elf-version-needs.py` or any `.bin`. Fixtures are 512-byte `MREC` objects, zero ELF magic
(`grep -l $'\x7fELF' fixtures/*.mrec` → no match, exit 1), and no fixture `value` equals any C1
record value (0 hits for `100729359`, `2819`, `2912`, `50332424`, `50531585` in the C1 expected.json).

## 4. Dynamic non-execution proof (bounded probe, scratch only)

Scratch root `/fast/scratch/hyaku/kaidoku-r34b/w1/RevR34C1Untouched/probe/` holds **only**
`replay-gate.py`, both configs, `c2-shortcut-gate-counter.py` and `mini-fix/` — the C1 reader, the C1
counter and the twelve carriers are not present in it, so any attempted access would fail loudly.

| UTC | command | exit | observable |
|---|---|---|---|
| 07:20:21Z | `strace -f -qq -e trace=execve,execveat … replay-gate.py --root . --config gate-config-mini.json --json-out green-probe.json` | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7`; 73 `execve`, all `/usr/bin/python3` |
| 07:20:21Z | same with `gate-config-naive.json --json-out red-probe.json` | 2 | `REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization` |
| 07:20:35Z | `strace -f -qq -s 400 -e trace=execve … c2-shortcut-gate-counter.py --root . --rev probe-rev --json-out counter-probe.json` | 0 | `GATE_COUNTER_OK … mutants_killed=3 green_positive_matched=8`; **183 execve, every one `/usr/bin/python3`** |
| 07:21:33Z | same with `-e trace=openat,open --json-out counter-probe2.json` | 0 | 16455 traced opens; **0** containing `elf-version-needs`, `version-needs-counter`, `corpus/evidence`, `/e01…/e12`; 0 `*.bin`; 104 opens of `mini-fix/fixtures/*.mrec` only |

Executed program set for the full counter run (histogram from `trace-all-exec.txt`): the gate (3),
the two mini counters (8 each), the eight `mini-fix/readers/*.py` (18 each), the three mutants (1
each), the counter itself (1), and the selftest's temporary `/tmp/kaidoku-r34-gate-*/{counter,pos,s1,s2,s3}.py`.
Nothing else. The only `e12`-looking string anywhere in the traces is the hex substring inside
`opaque-398e12c9767796a63c77.data`, a temp copy of a 512-byte fixture.

Probe receipt parity with the lane's production receipt: `clauses`, `met_target`, `finding`, `exit`,
`mutants_killed`, `selftest_failures` compare equal to `.ufo/waves/round-34/r34b/after/c2-at-instruments.json`
(boolean comparison printed `True` for all six keys). This is a byproduct corroboration only;
ExecRecountC2 owns the recount.

## 5. Findings

**F1 (adjacent, C2-owned, major) — the frozen "predicate identity" assertion is false.**
`r34b/claims.json.claims[0].predicate_identity` states: "The same sentence is the gate config's
`predicate` field, the C2 counter's PREDICATE constant and the receipt label". Measured with an AST
read of the constant and a JSON read of the receipt:
`claim.predicate == config.predicate: True`; `claim.predicate == receipt.predicate: False`;
`counter_PREDICATE == receipt: True`; `counter_PREDICATE == claim: False` (351 vs 237 characters).
- claim/config: "P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does."
- counter/receipt: "P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, clears the identity-defeating counter on the same eight fixtures where every registered shortcut class stays below target, and its selftest kills every mutant of its own refusal, positive-control and shortcut-floor branches."
Consequence: the receipt's `predicate` is not the frozen claim predicate, so "the receipt label is the
predicate" cannot be asserted as-is. Not a C1 hit; routed to RevPredicateIdentity / the L1.

**F2 (adjacent, C2-owned, medium) — `measured_revision` is an unverified label.**
`c2-shortcut-gate-counter.py` writes `measured_revision = args.rev` and resolves the gate/config/readers
against `--root`'s worktree; nothing binds the executed bytes to the named commit. Proven by probe:
`--rev probe-rev2` (a revision that does not exist) still yields `finding=shortcut_gate_discriminates`,
`met_target: true`, `exit 0`, and `"measured_revision": "probe-rev2"`
(`probe/counter-probe2.json`). So the receipt's `c79bbe7b…` is an operator attestation, not an
instrument-verified fact. (The bytes were independently verified against `c79bbe7b` in §1, so the
production receipt is not thereby falsified — but the counter cannot carry that claim alone.)

**O1 (observation, attribution unknown) — a lane-side `__pycache__` appeared after the freeze.**
`tools/round-34/mini-fix/__pycache__/mini-counter.cpython-314.pyc`, 10625 bytes, mtime
`2026-10-25 04:19:33 -0300` = `07:19:33Z`, dir `mini-fix/` mtime likewise 04:19; not a symlink
(`readlink -f` = the lane path). It is gitignored (`.gitignore:1:__pycache__/`), so
`git status --porcelain --untracked-files=all -- tools/round-34/` is empty and VCS is untouched.
Every pinned run passes `-B` (both configs and the gate's own invocations), which cannot produce a
`.pyc`, so some process imported/ran `mini-counter.py` from the lane worktree without `-B` after the
freeze. It does not touch any C1 artifact (mtimes and digests in §1–§2 unchanged). Recorded for the
containment seats; the wave rule is to run counters on copies, not in the lane.

## 6. Residual risk and verification gaps

- Absence-of-execution is proven to three layers: frozen bytes (§1), static argv/config closure (§3),
  and one full `strace` run of the wave's counter (§4). It is **not** a host-wide audit: a C1 execution
  by some other process after the freeze would leave no lane trace. Mitigating evidence: the reader,
  counter, manifest and all twelve carriers are byte-identical with pre-freeze mtimes, and no receipt
  anywhere in `r34b/` carries a carrier path or a carrier-shaped row.
- I did not run, import or score `elf-version-needs.py`, `version-needs-counter.py` or any carrier:
  none of them exist in my probe root. The C1 counterexample itself is not re-executed (prohibited);
  its integrity is argued from the byte-frozen receipt plus the control-tree digests in §2.
- Text `grep` was used only for token presence; the semantic claim (what was executed/opened) rests on
  the strace sets, not on grep. No `lsp` device exists in this seat's toolset and the audit changes no
  source, so caller/definition/diagnostics queries were not applicable; this is stated rather than
  substituted with grep.
- Fixture namespace note (not a defect, affects how "separable" should be read): the eight fixtures
  use shared-library *names* that also occur in the C1 carriers' version-needs records
  (`libc.so.6` appears 11× and `libm.so.6` 1× in the C1 `expected.json`), while none of the fixture
  `value`/`flags` triples or bytes are copied from C1. `claims.json`'s literal claim ("no ELF carrier
  is reused", "never domain evidence") holds; the C2 surface is not domain-disjoint, so no
  fixture-derived pass can be read as C1 evidence.

## 7. Tooling

No installs or upgrades. Used: `/usr/bin/python3` 3.14.8, `git` 2.56.0, `strace` 7.2. All writes went
to this report and to `/fast/scratch/hyaku/kaidoku-r34b/w1/RevR34C1Untouched/` (probe copy, four
receipts `green-probe.json`, `red-probe.json`, `counter-probe.json`, `counter-probe2.json`, traces
`trace-green-exec.txt`, `trace-red-exec.txt`, `trace-all-exec.txt`, `trace-open.txt`).

Verdict: **R34-C1 untouched and inert — byte-identical f432c8e3 → c79bbe7b on all five named
artifacts, all pins and twelve carriers intact, zero execution or scoring hits; no C1 defect found.**
