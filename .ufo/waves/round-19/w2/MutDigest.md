# MutDigest — round 19 wave 2 mutation evidence

Seat: `KaidokuR19.MutDigest-3`; author-side mutation tester, not an outside verifier.

## Axes and scope

- **Calibration:** distinguish the requested defect reopening from whole-command health; never call an already-red baseline a killed mutant.
- **Freshness:** freeze an observed `refs/heads/main` commit, not the round's older declaration baseline or an unpinned alias.
- **Depth:** one-nibble valid-hex mutations, revision-scoped detectors on pristine/mutated/restored bytes, retained digest evidence and exact-tree restoration.

**OBSERVATION:** Both requested defect IDs reopened under their respective one-file mutations and closed again after restoration. The retained-copy mutant is **KILLED** (`0 → 1 → 0`). The summary-digest probe is **INCONCLUSIVE as a whole strict-command kill** (`1 → 1 → 1`): its pristine command was already red on `R17-REGISTRY`. Nevertheless the requested `R17-VALIDATE16` reopening is directly observed (`open: false → true → false`, total open count `1 → 2 → 1`). No production fix or admission judgment is made.

References for the assignment: `.ufo/waves/round-19/claims.json:12-13,38` (C1), `claims.json:4` and `contract.md:4` (declaration baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`), `contract.md:17-22,26-30,48-50` (write/revision/report boundaries). This probe does not repeat the B-to-delivery claim measurement.

## Observed revision and isolation

**OBSERVATION:** First, a preliminary read-only command used bare `HEAD` and returned `5e364bd5e6016f030a04b4b8c81830477ebdaf51` (exit 0). That was a process deviation from `contract.md:19`; it was not used as the probe's base. The subsequent explicit main-ref observation below is the frozen base. No Git writes occurred in the production checkout.

```sh
# cwd: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD
# exit 0; stdout: 5e364bd5e6016f030a04b4b8c81830477ebdaf51
git rev-parse refs/heads/main
# exit 0; stdout: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

Scratch was allocated by Python's `tempfile.mkdtemp(prefix="kr19-w2-MutDigest-")`, returning `/tmp/kr19-w2-MutDigest-bg2poo6s`; clone/checkout commands appear in the command ledger below. All detector processes, mutations, staging, commits and restoration ran in that private clone. Both pristine detector invocations ran concurrently before either edit; mutation/restoration cycles were serialized to prevent overlapping writes.

Frozen base: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`.
The supplied `routed-r18.py` was run from this commit's clone, with its bytes unchanged throughout (SHA-256 below), rather than from a concurrently mutable production path.

| State | Scratch commit |
|---|---|
| Pristine | `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` |
| M1 summary digest | `abeec5f5ddaf8eddc5b9685e0cea95a9ea7c678e` |
| M1 restored | `0006b6e435742cfa09fc702cf9ccabd9a599603d` |
| M2 retained copy | `8bfec0186f7ed46b1d6f6330c9ce9b313b5637d1` |
| M2 restored / final | `82c44229adb73793f47ed3ca4cf7809cb65ddd20` |

## M1 — summary declares a well-formed but wrong validator digest

**Mutant:** change only `.ufo/waves/round-18/evidence/validate16/summary.json:82`, first hex nibble `6 → 0`. The other 63 hex characters, `validator_rev` (:81), eight receipt entries and retained stdout remain untouched. Applied with the surgical edit tool:

```diff
-  "validator_sha256": "618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f"
+  "validator_sha256": "018448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f"
```

**Expected detector:** round-18 `routed-defects.py --strict` at the mutation commit must reopen `R17-VALIDATE16`, specifically `validator-sha256-pinned`. Code anchors at the frozen base: `.ufo/waves/round-18/tools/routed-defects.py:402-428` recomputes the pinned blob digest and checks equality, `:431-440` reads the selected revision's summary, and `:497-499` emits the substance check. No detector code was edited.

**OBSERVATION:** The target is closed pristine, reopens on the mutation with a specific unequal-digest detail, and closes after exact restoration. All other checks in `R17-VALIDATE16` stayed true. Its named checks stayed satisfied; the changed digest was not rejected merely as malformed input.

**Calibration caveat / verdict:** **INCONCLUSIVE for whole strict-command mutation killing**, not a killed mutant: pristine and restored strict exits are already 1 due to `R17-REGISTRY / skill-scope-pins`. This does not hide the directly observed target reopening. The baseline failure detail is `scoped paths absent at rev: ['.ufo/waves/round-18/runs/<label>/pins']`. The literal example appears in `SKILL.md:542`; `.ufo/waves/round-18/tools/routed-defects.py:702-708` checks all backticked `.ufo/` tokens in the cell for existence. **INFERENCE:** the registry failure is an unrelated placeholder-example/registry-check interaction; it was not repaired or independently re-probed here.

### Actual detector outputs — M1

The JSON blocks below are selected fields from actual stdout (target's pin check and any other open defect), not new detector implementations or replacement exit codes. Every omitted target check was true. Stderr was empty for each process.

#### Pristine

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 1
```

```json
{
  "defects": [
    {
      "checks": [
        {
          "detail": "validator_sha256=618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f == sha256(.ufo/waves/round-17/tools/receipt-validate.py at 9011581d84527ba34c675f9cf912e54d2e72d470)",
          "name": "validator-sha256-pinned",
          "ok": true,
          "set": "substance"
        }
      ],
      "id": "R17-VALIDATE16",
      "named_open": false,
      "open": false,
      "substance_open": false
    },
    {
      "checks": [
        {
          "detail": "scoped paths absent at rev: ['.ufo/waves/round-18/runs/<label>/pins']",
          "name": "skill-scope-pins",
          "ok": false,
          "set": "substance"
        }
      ],
      "id": "R17-REGISTRY",
      "named_open": false,
      "open": true,
      "substance_open": true
    }
  ],
  "named_open_count": 0,
  "open_count": 1,
  "rev": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41",
  "substance_open_count": 1
}
```

#### Mutated

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev abeec5f5ddaf8eddc5b9685e0cea95a9ea7c678e --strict
# exit 1
```

```json
{
  "defects": [
    {
      "checks": [
        {
          "detail": "validator_sha256=018448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f != sha256(.ufo/waves/round-17/tools/receipt-validate.py at 9011581d84527ba34c675f9cf912e54d2e72d470)=618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f",
          "name": "validator-sha256-pinned",
          "ok": false,
          "set": "substance"
        }
      ],
      "id": "R17-VALIDATE16",
      "named_open": false,
      "open": true,
      "substance_open": true
    },
    {
      "checks": [
        {
          "detail": "scoped paths absent at rev: ['.ufo/waves/round-18/runs/<label>/pins']",
          "name": "skill-scope-pins",
          "ok": false,
          "set": "substance"
        }
      ],
      "id": "R17-REGISTRY",
      "named_open": false,
      "open": true,
      "substance_open": true
    }
  ],
  "named_open_count": 0,
  "open_count": 2,
  "rev": "abeec5f5ddaf8eddc5b9685e0cea95a9ea7c678e",
  "substance_open_count": 2
}
```

#### Restored

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 0006b6e435742cfa09fc702cf9ccabd9a599603d --strict
# exit 1
```

```json
{
  "defects": [
    {
      "checks": [
        {
          "detail": "validator_sha256=618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f == sha256(.ufo/waves/round-17/tools/receipt-validate.py at 9011581d84527ba34c675f9cf912e54d2e72d470)",
          "name": "validator-sha256-pinned",
          "ok": true,
          "set": "substance"
        }
      ],
      "id": "R17-VALIDATE16",
      "named_open": false,
      "open": false,
      "substance_open": false
    },
    {
      "checks": [
        {
          "detail": "scoped paths absent at rev: ['.ufo/waves/round-18/runs/<label>/pins']",
          "name": "skill-scope-pins",
          "ok": false,
          "set": "substance"
        }
      ],
      "id": "R17-REGISTRY",
      "named_open": false,
      "open": true,
      "substance_open": true
    }
  ],
  "named_open_count": 0,
  "open_count": 1,
  "rev": "0006b6e435742cfa09fc702cf9ccabd9a599603d",
  "substance_open_count": 1
}
```

## M2 — alter one retained remap copy without blessing its new digest

**Mutant:** change only `.ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json:7`, one nibble of `carrier.sha256_post`, preserving valid 64-hex syntax. Applied with the surgical edit tool:

```diff
-    "sha256_post": "bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014",
+    "sha256_post": "aab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014",
```

The manifest `.ufo/waves/round-19/evidence/validate16-remap/digests.json:5,8,11` continues to identify that copy, its original digest and `validator_exit: 0`; `:108-109` retains the original validator pin. Neither manifest nor summary was changed in M2. M1 had already been fully restored before this second mutation.

**Expected detector:** `.ufo/waves/round-19/tools/routed-r18.py --strict` at the mutation commit must reopen `R18-VALIDATOR-DIGEST`. Frozen-base code anchors: `:118-143` exercises wrong/true validator-digest behavior; `:144-161` reads and re-hashes the retained copies; `:156-159` must refuse the altered bytes. `:292-312,401-403` defines the open count and strict exit.

**OBSERVATION / verdict: KILLED.** Pristine exit 0 / `open_count: 0`, mutated exit 1 / `open_count: 1`, restored exit 0 / `open_count: 0`. Only `R18-VALIDATOR-DIGEST` reopens. Its named correction stays true while substance becomes false, with exact reason `copy calib-esbuild-0.25.12 missing or does not re-hash`. The file was altered, not deleted; the reason intentionally covers both cases.

### Actual detector outputs — M2

Selected target plus aggregate fields from actual stdout; all six omitted defects stayed named/substance true. Stderr was empty in every process.

#### Pristine

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 0
```

```json
{
  "defects": [
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41",
  "substance_open": 0
}
```

#### Mutated

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 8bfec0186f7ed46b1d6f6330c9ce9b313b5637d1 --strict
# exit 1
```

```json
{
  "defects": [
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": false,
      "why": "copy calib-esbuild-0.25.12 missing or does not re-hash"
    }
  ],
  "named_open": 0,
  "open_count": 1,
  "rev": "8bfec0186f7ed46b1d6f6330c9ce9b313b5637d1",
  "substance_open": 1
}
```

#### Restored

```sh
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 82c44229adb73793f47ed3ca4cf7809cb65ddd20 --strict
# exit 0
```

```json
{
  "defects": [
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "82c44229adb73793f47ed3ca4cf7809cb65ddd20",
  "substance_open": 0
}
```

## Before/after SHA-256 and exact restoration

**OBSERVATION:** `sha256sum` (each invocation exit 0, commands below) returned:

| File | Pristine | M1 | M1 restored / M2 pristine bytes | M2 | Final restored |
|---|---|---|---|---|---|
| `.ufo/waves/round-18/evidence/validate16/summary.json` | `7368afa6cdd0bc7bf40fb2e8102aa423750d58513c170511688e937e9dcb745a` | `0bc959ffe553389679788259c8e1a2ce78395c48bfac43a0f1787401a4147a26` | `7368afa6cdd0bc7bf40fb2e8102aa423750d58513c170511688e937e9dcb745a` | `7368afa6cdd0bc7bf40fb2e8102aa423750d58513c170511688e937e9dcb745a` | `7368afa6cdd0bc7bf40fb2e8102aa423750d58513c170511688e937e9dcb745a` |
| `.ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json` | `28b94aa9749f3e1fc631329cd9b9ce3aeb0e8669903ad28c6fe198e25695265f` | `28b94aa9749f3e1fc631329cd9b9ce3aeb0e8669903ad28c6fe198e25695265f` | `28b94aa9749f3e1fc631329cd9b9ce3aeb0e8669903ad28c6fe198e25695265f` | `f05e6eaa6afa69a6bfd50b656159f934590ae0bac53af51541272dc0b25ed628` | `28b94aa9749f3e1fc631329cd9b9ce3aeb0e8669903ad28c6fe198e25695265f` |

The following stayed identical in all five hash invocations:

```text
cf18918dae5c16e449df5a3fe84acf7a4a77c70ae6e926919f5c53985d52b994  .ufo/waves/round-19/evidence/validate16-remap/digests.json
7d14d59cb1a2b34c3329bbd3207d803a5d8e5540c30e6e59cb338583ef69aef5  .ufo/waves/round-18/tools/routed-defects.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  .ufo/waves/round-19/tools/routed-r18.py
```

Both restoration commits and the observed base have the identical full Git tree `b344427155950539dd93926882071beea28970a4`; the two `rev-parse` commands below each printed that hash twice (exit 0). Thus restoration covered the complete tracked tree, not merely a parsed JSON value. The final detector ran after restoring the physical receipt bytes. Restoration was in `finally` blocks around each mutated detector call; both calls completed normally and both restores succeeded. The private clone is retained at the final restoration commit; no mutation remains in its tracked tree.

## Complete subprocess command ledger

Commands below are the captured invocations and actual exits, including those whose detector stdout is excerpted above. Except for clone source reads and the separately disclosed preliminary ref observations, all writes were confined to the private scratch clone. Commit stdout reported exactly one file changed, one insertion and one deletion for each of the four commits. All captured subprocess stderr was empty.

```sh
# 1
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-MutDigest-bg2poo6s
# exit 0
# 2
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s checkout -q --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# exit 0
# 3
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s rev-parse --verify 'd0690fd44f46d8a7fe9da5f01c6be723d12abd41^{commit}'
# exit 0
# stdout: d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# 4
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && sha256sum .ufo/waves/round-18/evidence/validate16/summary.json .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json .ufo/waves/round-19/evidence/validate16-remap/digests.json .ufo/waves/round-18/tools/routed-defects.py .ufo/waves/round-19/tools/routed-r18.py
# exit 0
# 5
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 1
# 6
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 0
# 7
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && sha256sum .ufo/waves/round-18/evidence/validate16/summary.json .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json .ufo/waves/round-19/evidence/validate16-remap/digests.json .ufo/waves/round-18/tools/routed-defects.py .ufo/waves/round-19/tools/routed-r18.py
# exit 0
# 8
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s add -- .ufo/waves/round-18/evidence/validate16/summary.json
# exit 0
# 9
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=KaidokuR19.MutDigest-3 -c user.email=kaidoku-mutdigest@shokunin.local commit -m 'mutation probe: well-formed wrong validate16 validator digest'
# exit 0
# stdout: [detached HEAD abeec5f] mutation probe: well-formed wrong validate16 validator digest
# stdout:  1 file changed, 1 insertion(+), 1 deletion(-)
# 10
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s log -1 --format=%H
# exit 0
# stdout: abeec5f5ddaf8eddc5b9685e0cea95a9ea7c678e
# 11
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev abeec5f5ddaf8eddc5b9685e0cea95a9ea7c678e --strict
# exit 1
# 12
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s restore --source=d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --staged --worktree -- .ufo/waves/round-18/evidence/validate16/summary.json
# exit 0
# 13
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s add -- .ufo/waves/round-18/evidence/validate16/summary.json
# exit 0
# 14
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=KaidokuR19.MutDigest-3 -c user.email=kaidoku-mutdigest@shokunin.local commit -m 'mutation probe: restore exact validate16 summary bytes'
# exit 0
# stdout: [detached HEAD 0006b6e] mutation probe: restore exact validate16 summary bytes
# stdout:  1 file changed, 1 insertion(+), 1 deletion(-)
# 15
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s log -1 --format=%H
# exit 0
# stdout: 0006b6e435742cfa09fc702cf9ccabd9a599603d
# 16
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && sha256sum .ufo/waves/round-18/evidence/validate16/summary.json .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json .ufo/waves/round-19/evidence/validate16-remap/digests.json .ufo/waves/round-18/tools/routed-defects.py .ufo/waves/round-19/tools/routed-r18.py
# exit 0
# 17
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s rev-parse 'd0690fd44f46d8a7fe9da5f01c6be723d12abd41^{tree}' '0006b6e435742cfa09fc702cf9ccabd9a599603d^{tree}'
# exit 0
# stdout: b344427155950539dd93926882071beea28970a4
# stdout: b344427155950539dd93926882071beea28970a4
# 18
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 0006b6e435742cfa09fc702cf9ccabd9a599603d --strict
# exit 1
# 19
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && sha256sum .ufo/waves/round-18/evidence/validate16/summary.json .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json .ufo/waves/round-19/evidence/validate16-remap/digests.json .ufo/waves/round-18/tools/routed-defects.py .ufo/waves/round-19/tools/routed-r18.py
# exit 0
# 20
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s add -- .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json
# exit 0
# 21
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=KaidokuR19.MutDigest-3 -c user.email=kaidoku-mutdigest@shokunin.local commit -m 'mutation probe: alter one retained remap receipt digest nibble'
# exit 0
# stdout: [detached HEAD 8bfec01] mutation probe: alter one retained remap receipt digest nibble
# stdout:  1 file changed, 1 insertion(+), 1 deletion(-)
# 22
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s log -1 --format=%H
# exit 0
# stdout: 8bfec0186f7ed46b1d6f6330c9ce9b313b5637d1
# 23
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 8bfec0186f7ed46b1d6f6330c9ce9b313b5637d1 --strict
# exit 1
# 24
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s restore --source=d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --staged --worktree -- .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json
# exit 0
# 25
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s add -- .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json
# exit 0
# 26
$ git -C /tmp/kr19-w2-MutDigest-bg2poo6s -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=KaidokuR19.MutDigest-3 -c user.email=kaidoku-mutdigest@shokunin.local commit -m 'mutation probe: restore exact retained remap receipt bytes'
# exit 0
# stdout: [detached HEAD 82c4422] mutation probe: restore exact retained remap receipt bytes
# stdout:  1 file changed, 1 insertion(+), 1 deletion(-)
# 27
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s log -1 --format=%H
# exit 0
# stdout: 82c44229adb73793f47ed3ca4cf7809cb65ddd20
# 28
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && sha256sum .ufo/waves/round-18/evidence/validate16/summary.json .ufo/waves/round-19/evidence/validate16-remap/copies/calib-esbuild-0.25.12.receipt.json .ufo/waves/round-19/evidence/validate16-remap/digests.json .ufo/waves/round-18/tools/routed-defects.py .ufo/waves/round-19/tools/routed-r18.py
# exit 0
# 29
$ git --no-optional-locks -C /tmp/kr19-w2-MutDigest-bg2poo6s rev-parse 'd0690fd44f46d8a7fe9da5f01c6be723d12abd41^{tree}' '82c44229adb73793f47ed3ca4cf7809cb65ddd20^{tree}'
# exit 0
# stdout: b344427155950539dd93926882071beea28970a4
# stdout: b344427155950539dd93926882071beea28970a4
# 30
$ cd /tmp/kr19-w2-MutDigest-bg2poo6s && python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutDigest-bg2poo6s --rev 82c44229adb73793f47ed3ca4cf7809cb65ddd20 --strict
# exit 0
```

## Limits and disposition

- **OBSERVATION:** both assignment-specific reopenings were exercised at committed mutant revisions with the same respective script bytes before, during and after mutation; no surviving mutant was observed in these two scoped perturbations.
- **OBSERVATION:** M1 cannot be advertised as a clean strict-exit kill because of its red pristine baseline. No suppression, contract change, fixture repair, or easier substitute was used.
- **INFERENCE:** these results support only the two tested integrity boundaries, not complete semantic replay of all eight receipts, all of C1, a version-held-out claim, recovery quality, or outside verification.
- Read-only production access except this report; no production code/evidence edits, patch delivery, push, jj, state/config/fleet/sibling edits, REA/MCP calls, Ghidra, carrier execution, build, broad suite, formatter, delegation, or other runtime invocation.
- Tool installs/upgrades: **none**. Host-wide pacman pause respected.

Report: `.ufo/waves/round-19/w2/MutDigest.md`
