# R30-C2 sequential pre-data controls — CtlC2Sequence

## Result and scope

**Observation — attack verdict: holds for these seven controls. None met the frozen target.** This is a control receipt, not verification of R30-C2 or permission to collect claim data.

- Frozen source revision: `4ee65c6771058284aa947a266475839d196ed4d4`. All seven independently cloned `main` refs started there.
- Expected detector: the unchanged C2 counter must not print the all-success line and exit 0 for any assigned control. Frozen success is `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`, exit 0 (the counter prints explanatory parentheticals).
- Observation: 22 bounded measure invocations ran serially: pristine/control/restored for each clone, plus the requested post-carrier-repair do-nothing rerun. No two C2 counters were started concurrently.
- Mutation-test verdict: **inconclusive**, not killed, against a positive-baseline kill rule: every pristine baseline already exited 1 with zero committed matches. The specified negative-control rejection condition nevertheless held in each measured control.
- Observation: all seven restored trees equal the pristine tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; every scoped file digest and absence marker was restored exactly. Git history is retained, and its behavioral consequence for control 7 is recorded below.
- Carrier incident: this seat did not alter any carrier. No carrier-PIN-blocked run was observed by this seat. The empty-predictions PIN failure was a different, expected input mismatch. The additional rerun below records the requested run after the parent reported carrier repair; no blocked carrier output is invented.
- REA pin: `rea-agents@6.5.0`; already-present package JSON SHA-256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. Runtime version command `timeout 10 node --version` returned `v24.21.0`, exit 0.
- Safety: carriers/mutants were read as bytes only, never executed. Only the assigned counter rebuilt shared mutant files. Sandbox Git writes were confined to the seven private clones, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. Parent environment set `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/tmp`.
- Processes: the harness starts each bounded command in a separate process group and kills any remainder on normal or exceptional return. No long-lived service was started; the private Node compile cache was removed after all counter runs.
- Installs/updates: none initiated by this seat; no pacman transaction. No lane files were written except this report. Existing unrelated lane source changes were not reverted.

| Control | Counter exit | Last counter line | Target met |
|---|---:|---|---|
| do-nothing | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` | no |
| empty-predictions | 2 | `PIN predictions file differs from main` | no |
| all-accept-predictions | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` | no |
| one-generic-message | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` | no |
| rotated-messages | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` | no |
| junk-row | 1 | `mutants=19 matches=0 target=19 entry_ok=1 (ok) skill_ok=1 (ok)` | no |
| predictions-copied-as-observations | 1 | `mutants=19 matches=16 target=19 entry_ok=1 (ok) skill_ok=1 (ok)` | no |

No control met the target, so no target-enabling clause exists to report. The narrower permissive clauses observed without a full pass are recorded separately below.

## 1. do-nothing

Construction: No behavior or evidence change; create an empty sandbox commit.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone`.
- Control commit: `be8521d9d91079c406c6b2d7426c0a3e371d7e5e`; tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: do-nothing'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone --rev main
```

UTC: `2026-10-23T02:44:46+00:00` → `2026-10-23T02:45:03+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nobits	refuse	P2-miss	committed envelope absent or not added after the freeze
r-compressed-flag	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-sections	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-zlib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-trailing-bytes	refuse	P2-miss	committed envelope absent or not added after the freeze
r-over-1mib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-inflate-ratio	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-utf8	refuse	P2-miss	committed envelope absent or not added after the freeze
r-bad-json	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nesting-33	refuse	P2-miss	committed envelope absent or not added after the freeze
r-format-negative	refuse	P2-miss	committed envelope absent or not added after the freeze
r-extra-field	refuse	P2-miss	committed envelope absent or not added after the freeze
r-kind-dev	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-roots	refuse	P2-miss	committed envelope absent or not added after the freeze
r-index-outside	refuse	P2-miss	committed envelope absent or not added after the freeze
mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

`CONTROL do-nothing met_target=no`

Observation: all 19 rows missed because no post-freeze envelope was committed; entry_ok and skill_ok were both 0.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:44:19+00:00 | 2026-10-23T02:44:34+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:45:03+00:00 | 2026-10-23T02:45:18+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `024b15184340bc0dd8fff121352fd310bebeb978`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` |

## 2. empty-predictions

Construction: Replace the predictions TSV with its 46-byte header only; preserve all other tracked bytes. The detector regenerates the working TSV and then refuses its mismatch with the committed header. After capture, remove the regenerated rows again before reverting the control commit.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/clone`.
- Control commit: `fc9b88178821b974ecfbf52b11539e25079910da`; tree `2266b7744efa4f318b44b7a55c8efb8c5e860add`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: empty-predictions'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/clone --rev main
```

UTC: `2026-10-23T02:45:53+00:00` → `2026-10-23T02:45:53+00:00`; exit **2**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
PIN predictions file differs from main
```

`CONTROL empty-predictions met_target=no`

Observation: exit 2 with PIN predictions file differs from main. This is a predictions-file mismatch, not a carrier PIN failure.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:45:18+00:00 | 2026-10-23T02:45:33+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:46:16+00:00 | 2026-10-23T02:46:31+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `9b3247653c45c4b52101588228c00d2a37389566`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/clone/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `0f07e94f68fffa4250bff27068eab82fc412b54e74f6d221f99e5efc7daf1ffb` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` |

## 3. all-accept-predictions

Construction: For all 19 prediction rows, set kind to ok and message to the empty string; preserve IDs, digests, sizes, paths and code pointers.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/clone`.
- Control commit: `555936a0512f1095b251a3fa9e2078f717a57223`; tree `c8b0ecca6e53386e46d3eabf6b05b345fd013ae2`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: all-accept-predictions'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/clone --rev main
```

UTC: `2026-10-23T02:47:22+00:00` → `2026-10-23T02:47:37+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	ok	P2-miss	not accepted (exit 1)
r-nobits	ok	P2-miss	not accepted (exit 1)
r-compressed-flag	ok	P2-miss	not accepted (exit 1)
r-two-sections	ok	P2-miss	not accepted (exit 1)
r-not-zlib	ok	P2-miss	not accepted (exit 1)
r-trailing-bytes	ok	P2-miss	not accepted (exit 1)
r-over-1mib	ok	P2-miss	not accepted (exit 1)
r-inflate-ratio	ok	P2-miss	not accepted (exit 1)
r-not-utf8	ok	P2-miss	not accepted (exit 1)
r-bad-json	ok	P2-miss	not accepted (exit 1)
r-nesting-33	ok	P2-miss	not accepted (exit 1)
r-format-negative	ok	P2-miss	not accepted (exit 1)
r-extra-field	ok	P2-miss	not accepted (exit 1)
r-kind-dev	ok	P2-miss	not accepted (exit 1)
r-two-roots	ok	P2-miss	not accepted (exit 1)
r-index-outside	ok	P2-miss	not accepted (exit 1)
mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

`CONTROL all-accept-predictions met_target=no`

Observation: changed predictions were measured, not PIN-refused. All 16 actual refusals missed with not accepted (exit 1); the three actual acceptances still lacked committed envelopes.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:46:31+00:00 | 2026-10-23T02:46:46+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:47:37+00:00 | 2026-10-23T02:47:51+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `57b053c1e3ac2930de528882c2690379eff3b6bc`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/clone/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `0819487f5c5f4d273180e4ef3114be04a9d41b89620bb9d4821a53524f054fdd` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` |

## 4. one-generic-message

Construction: For every refusal row set the message to Dependency section is not a complete zlib stream. Leave the three acceptance rows and every other field unchanged.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/clone`.
- Control commit: `d43cbed9059e1d81ac6db1e05d275d22a8673211`; tree `b6b150e6fb7ab2ec7cb21c2770a466e038366895`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: one-generic-message'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/clone --rev main
```

UTC: `2026-10-23T02:48:36+00:00` → `2026-10-23T02:48:49+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	refuse	P2-miss	predicted message absent
r-nobits	refuse	P2-miss	predicted message absent
r-compressed-flag	refuse	P2-miss	predicted message absent
r-two-sections	refuse	P2-miss	predicted message absent
r-not-zlib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-trailing-bytes	refuse	P2-miss	committed envelope absent or not added after the freeze
r-over-1mib	refuse	P2-miss	predicted message absent
r-inflate-ratio	refuse	P2-miss	predicted message absent
r-not-utf8	refuse	P2-miss	predicted message absent
r-bad-json	refuse	P2-miss	predicted message absent
r-nesting-33	refuse	P2-miss	predicted message absent
r-format-negative	refuse	P2-miss	predicted message absent
r-extra-field	refuse	P2-miss	predicted message absent
r-kind-dev	refuse	P2-miss	predicted message absent
r-two-roots	refuse	P2-miss	predicted message absent
r-index-outside	refuse	P2-miss	predicted message absent
mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

`CONTROL one-generic-message met_target=no`

Observation: changed predictions were measured, not PIN-refused. Fourteen refusal rows missed with predicted message absent. The two genuine zlib-message rows and the three acceptances still lacked committed envelopes.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:47:51+00:00 | 2026-10-23T02:48:08+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:48:49+00:00 | 2026-10-23T02:49:04+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `67c6ee3d194083a3d1eaeee2ef76acaa62ba07b5`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/clone/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `a290bd9396cf4799648c5072032d5ab7443bd8929af07429b7587d758d3ce357` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` |

## 5. rotated-messages

Construction: Read the 16 refusal rows in TSV order and give each the next refusal row's message, wrapping the final row to the first. Duplicate adjacent messages remain equal by construction; acceptances and all non-message fields are unchanged.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/clone`.
- Control commit: `4279ca98e8165bca03129807b0a91bdc92311a82`; tree `e90bccebf61eb5ba1b9276a14a2b42d62c65e667`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: rotated-messages'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/clone --rev main
```

UTC: `2026-10-23T02:49:46+00:00` → `2026-10-23T02:50:01+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nobits	refuse	P2-miss	predicted message absent
r-compressed-flag	refuse	P2-miss	predicted message absent
r-two-sections	refuse	P2-miss	predicted message absent
r-not-zlib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-trailing-bytes	refuse	P2-miss	predicted message absent
r-over-1mib	refuse	P2-miss	predicted message absent
r-inflate-ratio	refuse	P2-miss	predicted message absent
r-not-utf8	refuse	P2-miss	predicted message absent
r-bad-json	refuse	P2-miss	predicted message absent
r-nesting-33	refuse	P2-miss	predicted message absent
r-format-negative	refuse	P2-miss	predicted message absent
r-extra-field	refuse	P2-miss	committed envelope absent or not added after the freeze
r-kind-dev	refuse	P2-miss	predicted message absent
r-two-roots	refuse	P2-miss	predicted message absent
r-index-outside	refuse	P2-miss	predicted message absent
mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

`CONTROL rotated-messages met_target=no`

Observation: changed predictions were measured, not PIN-refused. Thirteen refusal rows missed with predicted message absent; the three duplicate-message rows and the three acceptances still lacked committed envelopes.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:49:05+00:00 | 2026-10-23T02:49:19+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:50:01+00:00 | 2026-10-23T02:50:16+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `db37719b47fa9fbe8fc6a56df6e3943ce9528f61`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/clone/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | `e43ef9c8a3255eb5de061197b029c3b4e7869fa37bb2b52405180dacc81fb4e6` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` |

## 6. junk-row

Construction: Keep the true frozen predictions. Add one SKILL.md line naming inspect-rust-binary and the assigned entry; create the entry with first line source: S090; add a junk | S090 | registry row. Commit no envelopes.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone`.
- Control commit: `21a9d50de660d67e737c365a22db2207dd5c2883`; tree `eae18e4b2fdb926d8f401b530c44275322d8d1b7`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: junk-row'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone --rev main
```

UTC: `2026-10-23T02:50:53+00:00` → `2026-10-23T02:51:09+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nobits	refuse	P2-miss	committed envelope absent or not added after the freeze
r-compressed-flag	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-sections	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-zlib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-trailing-bytes	refuse	P2-miss	committed envelope absent or not added after the freeze
r-over-1mib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-inflate-ratio	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-utf8	refuse	P2-miss	committed envelope absent or not added after the freeze
r-bad-json	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nesting-33	refuse	P2-miss	committed envelope absent or not added after the freeze
r-format-negative	refuse	P2-miss	committed envelope absent or not added after the freeze
r-extra-field	refuse	P2-miss	committed envelope absent or not added after the freeze
r-kind-dev	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-roots	refuse	P2-miss	committed envelope absent or not added after the freeze
r-index-outside	refuse	P2-miss	committed envelope absent or not added after the freeze
mutants=19 matches=0 target=19 entry_ok=1 (ok) skill_ok=1 (ok)
```

`CONTROL junk-row met_target=no`

Observation: the junk documentation met entry_ok=1 and skill_ok=1, but every envelope was absent and matches remained 0.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:50:16+00:00 | 2026-10-23T02:50:30+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:51:09+00:00 | 2026-10-23T02:51:23+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `3cc1b9451677e756b42910e28a6a2102455d661b`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone/SKILL.md` | `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` | `00ffe146e746e01217672fe5c50b3f35f6364913268458d23157e0b25623af42` | `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone/corpus/SOURCES.md` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | `4e6b29cba82915760ef756366acf2d95b905f3fda3b548a1ad83b2e936041a4e` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` | `absent` | `fa27ed6a95c265ee6154ca75580686fbff6d7829ecc6a3e032989ad011861a42` | `absent` |

## 7. predictions-copied-as-observations

Construction: Make the same three junk documentation changes as junk-row, preserve true predictions, and add 19 fabricated envelope JSON files. Refusals contain only ok:false and error.message copied from the prediction. The three ok envelopes use the independent oracle's packages, section offset/size and mutant digest, with evidence_id set to ev_ plus SHA-256 of the UTF-8 mutant ID. No captured REA output is read by the fabricator.

- Clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone`.
- Control commit: `71cadd52377c9ce1951ee521cbf79c5ca644bdfe`; tree `52fda2e11aa4daa61de8417d39682a38ca6c86c0`.
- Exact construction diff: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control.patch` (SHA-256 in artifact inventory). Existing-file mutations were hashline edits; new entry/envelope files were created only in this clone.
- Commit command (actual):
```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone -c user.name=ctl -c user.email=ctl@sandbox commit --allow-empty -m 'R30-C2 control: predictions-copied-as-observations'
```

Counter command (actual, with the environment above):
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone --rev main
```

UTC: `2026-10-23T02:52:06+00:00` → `2026-10-23T02:52:19+00:00`; exit **1**. Counter stderr: empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed evidence_id differs
g-recompressed	ok	P2-miss	committed evidence_id differs
g-no-root	ok	P2-miss	committed evidence_id differs
r-empty	refuse	P2-match	refused with predicted message
r-nobits	refuse	P2-match	refused with predicted message
r-compressed-flag	refuse	P2-match	refused with predicted message
r-two-sections	refuse	P2-match	refused with predicted message
r-not-zlib	refuse	P2-match	refused with predicted message
r-trailing-bytes	refuse	P2-match	refused with predicted message
r-over-1mib	refuse	P2-match	refused with predicted message
r-inflate-ratio	refuse	P2-match	refused with predicted message
r-not-utf8	refuse	P2-match	refused with predicted message
r-bad-json	refuse	P2-match	refused with predicted message
r-nesting-33	refuse	P2-match	refused with predicted message
r-format-negative	refuse	P2-match	refused with predicted message
r-extra-field	refuse	P2-match	refused with predicted message
r-kind-dev	refuse	P2-match	refused with predicted message
r-two-roots	refuse	P2-match	refused with predicted message
r-index-outside	refuse	P2-match	refused with predicted message
mutants=19 matches=16 target=19 entry_ok=1 (ok) skill_ok=1 (ok)
```

`CONTROL predictions-copied-as-observations met_target=no`

Observation: all 16 fabricated refusal envelopes counted as P2-match; all three oracle-fabricated acceptances missed with committed evidence_id differs. Result: matches=16, not 19.

**Observation — control verdict: holds. Mutation-kill verdict: inconclusive (pristine baseline already failed).**

Pristine/restored detector evidence (same exact counter command; the `main` ref identifies each stage's committed state):

| Stage | UTC start | UTC end | Exit | Exact last stdout line |
|---|---|---|---:|---|
| pristine | 2026-10-23T02:51:23+00:00 | 2026-10-23T02:51:37+00:00 | 1 | `mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |
| restored | 2026-10-23T02:52:19+00:00 | 2026-10-23T02:52:33+00:00 | 1 | `mutants=19 matches=16 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)` |

Full stdout, empty stderr, command, exit and UTC receipts for those stages are retained and individually hashed in the artifact inventory.

Restoration: `9b198c114cf1c816e37515a1ca0e005933702a50`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; `exact_tree_restored=true`, `exact_scoped_files_restored=true`.

Before/control/restored SHA-256 (`absent` is exact file absence):

| Absolute clone path | Pristine | Control before detector | Restored |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/SKILL.md` | `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` | `00ffe146e746e01217672fe5c50b3f35f6364913268458d23157e0b25623af42` | `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/SOURCES.md` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | `4e6b29cba82915760ef756366acf2d95b905f3fda3b548a1ad83b2e936041a4e` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/g-no-root.json` | `absent` | `4b7c5dea68054555a768f97986af90ea7859edd1fd1bd6eff0a9c67b4a799959` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/g-recompressed.json` | `absent` | `f9257a28840df274aa16a9ad4fd688eba847b4edbc83eec4ac29cdbea42471cb` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/g-relocated.json` | `absent` | `c2952251936dcfb833adcfb27cf8117f4e34682932895c5f9f527555d17eb131` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-bad-json.json` | `absent` | `f5addb2607a5ef707e51241ead89f1684a7aae38b56d4bebfd02f0004d6e7967` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-compressed-flag.json` | `absent` | `c1666d35e26ff92f0943dcbc4abfc7e95828c650a762863b322fbcfb2ce7442d` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-empty.json` | `absent` | `e725c572fd91584a8f29f66e8cd3d781c33f8b05ea2bd4241c7b089affb33a0f` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-extra-field.json` | `absent` | `edcf15d577bccb091fdc8ee5c47755e3e4ca3d107623371b5cbcb4ffdb7955ca` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-format-negative.json` | `absent` | `ee8e5809cbc03af8fc0e0ddc5321ea4fe97d465fb1aedeeea891aa7fcb631e65` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-index-outside.json` | `absent` | `20bf1d2a52643aa0aa443ca1cdcf7420a8377f71b9fe038c4228b0468c568f99` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-inflate-ratio.json` | `absent` | `7ad95aa1a0ba21de04cb1ce6c55daa2633facf5a6231be9c7d80dad31ce89244` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-kind-dev.json` | `absent` | `edcf15d577bccb091fdc8ee5c47755e3e4ca3d107623371b5cbcb4ffdb7955ca` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-nesting-33.json` | `absent` | `c963773b7920db3a8677d7171255d81ba088040948effe6c2e90f244c4b88102` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-nobits.json` | `absent` | `e725c572fd91584a8f29f66e8cd3d781c33f8b05ea2bd4241c7b089affb33a0f` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-not-utf8.json` | `absent` | `ebd9056e99a87f1d22bfe9cb22d81698a9223769b962d9615fc096ddb641cb6c` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-not-zlib.json` | `absent` | `0f1cf49dc3d64d6d5e704ea417ecdddc491c3b5424b8c2d3c97769ad29344125` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-over-1mib.json` | `absent` | `b6b14a5a7eeb58e51180ea9cda5c6993370c27299fc3a13a564ae7c87c2860bd` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-trailing-bytes.json` | `absent` | `0f1cf49dc3d64d6d5e704ea417ecdddc491c3b5424b8c2d3c97769ad29344125` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-two-roots.json` | `absent` | `d775a95c6e02b59eba8fd935e3baf05238136247ad945431a945d607975d271e` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/evidence/round-30/c2/envelopes/r-two-sections.json` | `absent` | `7b84a915beb196d549621219ea3489e671059ecf1a392d0a6e9cb9a9ec19e696` | `absent` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` | `absent` | `fa27ed6a95c265ee6154ca75580686fbff6d7829ecc6a3e032989ad011861a42` | `absent` |

## Narrow findings and limits

### Altered predictions were not always freeze-refused

**Observation:** controls 3–5 exited 1 after measurement, rather than exit 2 at the predictions pin. Their producing commands, UTCs and complete stdout are above. **Inference from the frozen counter:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py:324-328` compares working predictions with the requested revision, not with the freeze commit or frozen SHA-256. Sandbox-committing changed predictions therefore passes that comparison. The behavioral and committed-envelope conditions still prevented the target. This report does not amend the frozen contract.

### Fabricated committed refusals counted, while acceptance IDs stopped the full shortcut

**Observation:** control 7's command at `2026-10-23T02:52:06+00:00` exited 1 and printed `mutants=19 matches=16 target=19 entry_ok=1 (ok) skill_ok=1 (ok)`. Sixteen rows were `P2-match`; the three positive rows printed `committed evidence_id differs`.

**Inference from the frozen counter:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py:246-255` checks the committed evidence ID only when the live envelope is ok. For a live refusal it compares boolean ok only after checking first-add time. Thus the minimal fabricated refusal objects satisfy committed agreement; this is a subpredicate coverage finding, not a full target pass.

### Exact byte restoration did not undo Git-history observations

**Observation:** the restored control-7 command at `2026-10-23T02:52:19+00:00` exited 1 but still printed 16 matches, despite restored tree equality and all 19 envelope paths absent. The three acceptance rows instead printed `committed ok False != live ok True`. Full restored stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed ok False != live ok True
g-recompressed	ok	P2-miss	committed ok False != live ok True
g-no-root	ok	P2-miss	committed ok False != live ok True
r-empty	refuse	P2-match	refused with predicted message
r-nobits	refuse	P2-match	refused with predicted message
r-compressed-flag	refuse	P2-match	refused with predicted message
r-two-sections	refuse	P2-match	refused with predicted message
r-not-zlib	refuse	P2-match	refused with predicted message
r-trailing-bytes	refuse	P2-match	refused with predicted message
r-over-1mib	refuse	P2-match	refused with predicted message
r-inflate-ratio	refuse	P2-match	refused with predicted message
r-not-utf8	refuse	P2-match	refused with predicted message
r-bad-json	refuse	P2-match	refused with predicted message
r-nesting-33	refuse	P2-match	refused with predicted message
r-format-negative	refuse	P2-match	refused with predicted message
r-extra-field	refuse	P2-match	refused with predicted message
r-kind-dev	refuse	P2-match	refused with predicted message
r-two-roots	refuse	P2-match	refused with predicted message
r-index-outside	refuse	P2-match	refused with predicted message
mutants=19 matches=16 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

**Inference from the frozen counter:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py:240-255` retains the earlier add timestamp in `git log --diff-filter=A`, while absent `show` data becomes null and therefore committed ok=false. A null committed value and a live refusal both map to false. The explicit byte-restoration requirement is met; the restored behavioral result is not falsely described as the pristine result. No second mutation was introduced to test or repair this.

**Unknown:** these controls do not establish that the detector rejects every possible shortcut, that the frozen predictions are sufficient knowledge, or that a passing positive claim can be measured from the lane. No integration or claim-data collection was performed.

## Requested post-carrier-repair rerun

Counter command:
```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone --rev main
```

UTC: `2026-10-23T02:53:09+00:00` → `2026-10-23T02:53:24+00:00`; exit **1**; stderr empty.

Full counter stdout:
```text
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-miss	committed envelope absent or not added after the freeze
g-recompressed	ok	P2-miss	committed envelope absent or not added after the freeze
g-no-root	ok	P2-miss	committed envelope absent or not added after the freeze
r-empty	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nobits	refuse	P2-miss	committed envelope absent or not added after the freeze
r-compressed-flag	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-sections	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-zlib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-trailing-bytes	refuse	P2-miss	committed envelope absent or not added after the freeze
r-over-1mib	refuse	P2-miss	committed envelope absent or not added after the freeze
r-inflate-ratio	refuse	P2-miss	committed envelope absent or not added after the freeze
r-not-utf8	refuse	P2-miss	committed envelope absent or not added after the freeze
r-bad-json	refuse	P2-miss	committed envelope absent or not added after the freeze
r-nesting-33	refuse	P2-miss	committed envelope absent or not added after the freeze
r-format-negative	refuse	P2-miss	committed envelope absent or not added after the freeze
r-extra-field	refuse	P2-miss	committed envelope absent or not added after the freeze
r-kind-dev	refuse	P2-miss	committed envelope absent or not added after the freeze
r-two-roots	refuse	P2-miss	committed envelope absent or not added after the freeze
r-index-outside	refuse	P2-miss	committed envelope absent or not added after the freeze
mutants=19 matches=0 target=19 entry_ok=0 (entry absent at rev) skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)
```

`CONTROL do-nothing met_target=no`

Observation: no carrier pin blocked either the initial do-nothing run or this rerun. This seat was not the carrier writer. The parent's carrier repair/immutability statement is contextual information, not a finding independently re-verified here.

## Opened local primary sources

Access date for every entry: **2026-10-23**. These are local-file URLs opened by ordinary reads, not browser sessions or access-control workarounds. Quotes are at most 25 contiguous words. Source details and read provenance are retained in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/source-receipts.json`.

| URL | SHA-256 | Located quote |
|---|---|---|
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | line 253: `if l_ok and (committed.get("data") or {}).get("evidence_id") != (live.get("data") or {}).get("evidence_id"):` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | line 3: `Shares no code with REA. It parses the container section tables itself` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | line 6: `Counters, predicates, labels, targets, carrier list and predictions below are fixed from that commit;` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | line 1: `id	format	arch	wheel	wheel_sha256	member	sha256	size	path` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | line 1: `id	kind	message	sha256	size	path	code_pointer` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md | `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` | line 68: `## Error patterns (typed refusals)` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | line 1: `# SOURCES — where kaidoku learns` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | line 4: `"version": "6.5.0",` |
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 14: `Record every install or update — tool, version, channel, reason — in your report or handoff.` |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 12: `**Name the axes.**` |
| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 11: `Use REA when a claim depends on a shipped binary or package, decompilation,` |

The source-registry receipt describes the bytes opened before unrelated lane edits; its byte-identical retained snapshot is `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/clone/corpus/SOURCES.md`.

## Artifact inventory

All raw stdout/stderr and command logs are retained below. The seven clone working trees are restored reproduction copies, identified by Git tree IDs and scoped SHA-256 manifests above; control bytes remain recoverable from their sandbox commits and exact binary diffs. Runtime compile-cache files were disposable and removed, not evidence.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control-manifest.json` | `6e6897f36d40d378a490edcdba4481dac78835f2f22bc2b436e57f1b25431b02` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control-receipt.json` | `b73938ecd372ac04f1fb19f517320e735eb4a16442e31bdfadb0445ca052ee11` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control.patch` | `67c61dd394344984103b5a2b56e8526a88d0e7fbd99b4bc4f3206c364350951b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/control.stdout` | `ad516db518786523c92ae4c19965a5da05a7583ef818bd66def14fe2f45b691c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/pristine-manifest.json` | `ef2e835fdee2c622ede44822cdb4b22e0cdda03585b7456119ce63f648930324` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/pristine-receipt.json` | `2f4dc8edac251bae55b61d378844fd81d11c06863f5b8258024749887b839e43` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/restored-manifest.json` | `86181a84787cd69a46c00dff759444a7c95bafa93d37380c65d74018eaa41b7c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/restored-receipt.json` | `0dd2a6708c5d71f04e7ddc5423846c1d902c5bd10288e1964ac22ba66f5a8160` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/all-accept-predictions/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/artifact-manifest.sha256` | `1435bf5802ed0bdba185a32821584aa01e198a228d4d87a442e46ee6954cf52f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/commands.jsonl` | `5561caf220e833f54d0c135f6df0a643da6d4fa64305bf4dc9ca9b36776dab3f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/control_harness.py` | `2b4965fd73cad1de088aec252f0278ee8d5d792b0f616ce18cbe921c53f85e41` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control-manifest.json` | `7356e1087d4cb2d1f4f7ecfdeeaac9acf7bb9f9777125a366a9364228f6e6c21` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control-receipt.json` | `cfc37ecae683a652a0eebea1bc55e092b5fc77a901a3dc07abaf26414bc87033` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control.patch` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/control.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/post-carrier-repair-receipt.json` | `35f4f8e51c2a9ca06772285f15f1fca28aa30664e07ae8e1eb21cbd72be6508a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/post-carrier-repair.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/post-carrier-repair.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/pristine-manifest.json` | `7c0d5c1759e4d30124cdb6b1e217b202ac44050ee709b2a0a36f9fc527b98750` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/pristine-receipt.json` | `8ed433b14bb5342fd0d7c44548d819c9d7f8feb292b49929dfe27006214cf7eb` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/restored-manifest.json` | `5779527c0e2bb0caa4a7b7ff27e86d24644098e77d5e16d60c08a85cdb50bf11` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/restored-receipt.json` | `c95b6e0b96a9f8a732366ab6acdd1ed1f2e978e83e7eb5db74a66341e837a958` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/do-nothing/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control-manifest.json` | `0e3f116d17956665d68b67de2f235f581ca5029cb7df4dac0d83f86d9976750d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control-receipt.json` | `dd55113d600b91217111b2e59c626cc8a6d7d6651744429b53f3c58bc59f253c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control.patch` | `5129c31747a0b552b00b2ab7a6be1f67fec3d4becd36919c6e0444ace0fa0a36` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/control.stdout` | `ee41a30cb1c04d84a016efff19377631a818a7c88a3cc59a096cc303f9198ce6` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/pristine-manifest.json` | `eb74fcf60c9ef65d6c038f58cbb7a6fbbab8dcfff50e8cc5612aec3ec3eb2095` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/pristine-receipt.json` | `6392a1d634d8f741addf12659849caade04add7864e518f8966b11405bbe5bc6` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/restored-manifest.json` | `8d112d057dc92360a1c989bb5ba4454181ae0d3caa986cb252bf7658f1662d1d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/restored-receipt.json` | `bef2dd623e39d31b1408a7220d0d09433fdf7ca9bdc3e81f33c3434b247df691` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/empty-predictions/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control-manifest.json` | `e6f26867fbb36bebfbd62cae9890e117aab153c5c32c7ba2d41d9e131578e1dc` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control-receipt.json` | `e448bc67d7e8b0a20a607ccf558501558cb61a9ce905c293d3d2f6ba7d2971c2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control.patch` | `4537b57a97b883dda31daeb09172424344416fb86b972fb45a4c3d9739f2e3aa` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/control.stdout` | `11a38aa53d299aa1ea6e3f4f6ac02d5cf65c87c5a901b08abec0bdc0a807db56` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/pristine-manifest.json` | `eb3f7c830896314f81fa928a124b5505d2bd0f9d7efa725bf5523af42ca9c82e` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/pristine-receipt.json` | `8b9e65938c91c241ad39626bc07fa31ff0e764c5c0109bed3fe54abc3255bbb5` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/restored-manifest.json` | `664013e5fb68a3c10e1687146095651780387b8ab4fd723ac4eba4a56e91d289` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/restored-receipt.json` | `b1cd1b765909bbb53997fd448ec27875296d4ef7d417fe2abe7aa0939ce25ace` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/junk-row/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control-manifest.json` | `7023ec5966e8c2938b318c92518bfae60fccc44565d4d3680b8df42f75bc4774` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control-receipt.json` | `9a0907c3b58b68367062c7b5be5107f8cfebfe5b2fb95ade8eec71fcad7689b0` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control.patch` | `dfcd6a92fb8fc2808d312a16ca8727ce6d61cf626483548963bab24434916937` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/control.stdout` | `43e2615f49773a80edbf0d64b24a8d0cc6ffd610bdbcbde664ce3a62fe97019a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/pristine-manifest.json` | `00c3a26480b82e2eb4ac5e8dd7378a83f442da52f83cfabb0cf8ab5dde3a9bee` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/pristine-receipt.json` | `280f3cea8b35cac09300b195a8fce747ec21e58504e4c0ec91c272be5189ea59` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/restored-manifest.json` | `8d9df96d13c810636227e17cf6c2e98f4f065a200b354aaa2535532d5f66a864` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/restored-receipt.json` | `06391048afea2b6c9e68a8a335c08cf52551a1d49c5f200451c8026b90b04e8a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/one-generic-message/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control-manifest.json` | `1bbb3ecff6f81d27efc788d5c5cfe3f52318fa14615f16a87f89c87e586ab525` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control-receipt.json` | `24ce4903217291d9faca817f65287d258f29a03cdac83d295b3276141205b631` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control.patch` | `c538876fef6027dbc0749107edb42ac779d3fee045635978f8d1bd5cd80f08ee` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/control.stdout` | `7d8d104d41af5fbe8e44e409cd6525f0913c12ddf2144201773028d30fe982e8` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/pristine-manifest.json` | `eb3f7c830896314f81fa928a124b5505d2bd0f9d7efa725bf5523af42ca9c82e` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/pristine-receipt.json` | `35759043872aff91374979568922484e8aeaa691cdeb55e559b690175fddb7f2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/restored-manifest.json` | `9483dcebceabea659aead2c3a8a6e2650f459f54c59f10db601879542f35c0c1` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/restored-receipt.json` | `289299d33757606c0ba6e119875e2263fff73950e0b2d55525c017ce81c73e03` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/predictions-copied-as-observations/restored.stdout` | `dccd3f61600018e4d39f878848d7e028c6a2fb9eec9916ad8cbb753e220c3a70` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/preparation.json` | `cc85a2b8a3019617b5948f7492e2f8107c2b13456b2257bd2d780f9c903293e0` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control-manifest.json` | `528b149678b79a346c6c4ff71acdb2729034bbe7c363f36f73f522625bfd8e2f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control-receipt.json` | `5977039873076a926e02074b3206b831a040ea013599ee1800d0f77cf39163d7` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control.patch` | `70d3f7f3e89c2a959212c46404641c145d7997ba664a1d322141867f7df35aac` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/control.stdout` | `7c6f89a2c7f79aec9599c4e4b7cfc3e4ccfb1c238410e0ef844e6fe35c6b747c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/pristine-manifest.json` | `71f5245532a7f1e11568f1d40ebe541bf68aa5ee09dfc8736f15d514f327f891` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/pristine-receipt.json` | `4680675ad18e232ef7000d9d5f5b8d43349aa59c4fdf98c68f6418a1b7964927` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/pristine.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/restored-manifest.json` | `86bc0af248c63504cb68d755484be42a8a446f5eb3faa159b07e64ccb86d8a0a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/restored-receipt.json` | `53871dd86495419b0f4f7f44b2fe05b8054babb5117251e8d3979b14f8caaad5` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/rotated-messages/restored.stdout` | `9d5cc4e057b2eafe548abc1f299f448d37cdd0ecbbe1b35a291d3456b9ec3325` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/source-receipts.json` | `f63ecfaece24b1682f7a95457de6488f79d91346174a70c41ca8d4c14f482e80` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/summary.json` | `a4c69dfef9f02d02fb13890c98edf99aa2407e4e1e545d61b3c897e505d59831` |

Draft artifact: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC2Sequence/report-draft.md`; SHA-256 `deaf3a343be41ed958af39ea232ee147b21ec0047204305ba2e8aa19544c766e`. The draft is excluded from its own internal inventory to avoid a self-referential digest.
