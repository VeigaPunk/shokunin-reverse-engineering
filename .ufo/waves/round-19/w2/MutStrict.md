# MutStrict — strict-baseline receipt mutation probe

Author-side leaf probe: `KaidokuR19.MutStrict-3`. No outside-verifier or integration verdict is claimed.

## Findings

**Observation: four negative-control mutants were killed; an invented, hash-consistent, never-executed run survived.** The same `routed-r18.py --strict` command was clean on pristine bytes, reopened only `R18-STRICT-BASELINE` for exit/argv/stdout corruption and for a re-hashed zero count, then returned fully clean for the fabricated positive-count transcript. All touched bytes were restored exactly and the restored detector was clean. No inconclusive result.

**Boundary:** this check establishes selected receipt fields and Git-byte/digest consistency, not execution authenticity. Its clean result does not establish that the retained argv ran, that the referenced tool generated stdout, or that its claimed exit was observed. The survivor is a coverage finding, not permission to change the contract and not evidence that the existing historical receipts were fabricated.

## Axes and freshness

- **Calibration:** distinguish four exercised rejection controls from the surviving producer-authenticity gap; observation and inference are labelled below.
- **Freshness:** main was observed before cloning and after restoration as `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (both reads exit 0). The detector, tools and evidence were tested in a `tempfile.mkdtemp(prefix="kr19-w2-MutStrict-")` clone detached at that exact tip, not at a floating HEAD and not in a sibling source.
- **Depth:** independently alter exit, the strict argv token, and stdout; separate a byte-hash failure from the semantic zero-count failure by updating the stdout digest; then author a complete synthetic run record while preserving a real tool-blob commitment.

Clone: `/tmp/kr19-w2-MutStrict-mduxjr5e`. Declared round-19 red baseline **B19** is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. The retained strict run being tested is for the distinct round-18 **B18** `9011581d84527ba34c675f9cf912e54d2e72d470`.

## Exact source anchors

Paths below are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Detector/receipt/stdout anchors were read in the isolated clone at the pinned tip unless a mutant revision is stated; claims, contract and the routed requirement were read from the lane working tree as declarations, not used as executable evidence.

- `.ufo/waves/round-19/claims.json:10-14`: C1 names the routed fixes and the 7-to-0 counting claim. `.ufo/waves/round-19/contract.md:17-30,46-50`: no lane Git writes, revision-scoped Git objects, explicit command exits and observation/inference reporting.
- `corpus/lessons/round-18-verifier-spotcheck.md:195`: the actual routed requirement is to retain the strict red baseline run, not merely its non-strict output.
- `.ufo/waves/round-19/tools/routed-r18.py:165-175`: only the `9011581d8452` receipt is selected; the receipt must claim B18, contain the exact `--strict` argv token, and claim exit 1.
- `.ufo/waves/round-19/tools/routed-r18.py:176-182`: stdout/stderr re-hash to the receipt, and the tool blob at the receipt-supplied `tool_rev` re-hashes to `tool_sha256`.
- `.ufo/waves/round-19/tools/routed-r18.py:183-189`: stdout must parse as JSON and its `open_count` must be truthy. This function does not run the recorded argv.
- `.ufo/waves/round-19/tools/routed-r18.py:284-312,401-403`: named corrections and substance jointly determine each open defect; `--strict` exits 1 if the total open count is nonzero.
- `.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json:2-20`: original argv (`--strict` at line 11), exit (line 14), output hashes (lines 17-18) and tool commitment (lines 19-20). `.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt:292-295`: original counts are 6 and stdout revision is B18.

## Mutants and expected detector

Every mutant is confined to that receipt/stdout pair in the scratch clone. The detector source and stderr bytes were never mutated. Expected negative-control outcome: `named=true`, `substance=false` for `R18-STRICT-BASELINE`, aggregate `open_count=1`, `named_open=0`, `substance_open=1`, process exit 1, with the other six defects closed.

| Probe | Smallest change relative to pristine | Expected | Observed | Verdict |
|---|---|---|---|---|
| M1 exit | Receipt line 14: `"exit": 1` → `0`; argv/stdout untouched | Reopen | Exit 1; only STRICT-BASELINE open | **Killed** |
| M2 argv | Receipt line 11: `"--strict"` → `"--no-strict"`; exit/stdout untouched | Reopen | Exit 1; only STRICT-BASELINE open | **Killed** |
| M3 stdout | Stdout line 293: `"open_count": 6` → `0`; receipt digest untouched | Reopen at byte binding | Exit 1; hash-mismatch reason | **Killed** |
| M4 zero + re-hash | Keep the M3 zero and set receipt line 18 to the actual new stdout SHA-256 | Reopen even though the bytes re-hash | Exit 1; semantic zero-count reason | **Killed** |
| M5 fabricated run | Replace stdout with a newly authored one-defect transcript, and replace receipt argv/timestamps/output hash while preserving B18, exit 1, `--strict`, empty-stderr hash and a real tool commitment | Authenticity challenge: reopen if execution is authenticated | Exit 0; all seven defects closed | **Survived** |

M1 and M2 each had an intervening pristine restoration commit and clean detector. M3→M4 deliberately changes only the digest after testing the same zero stdout; both are compared to the original clean baseline and share the exact pristine R3 restoration/control. M5 starts after R3 and ends with exact pristine R4 restoration.

### Actual detector outputs (selected JSON fields)

The table is a projection of the captured JSON stdout, not a different detector. All 11 detector runs had empty stderr. Counts are the outer routed-r18 counts, not the count inside the retained/fabricated round-18 stdout.

| Stage | Full evaluated revision | Exit | open / named-open / substance-open | STRICT-BASELINE named / substance | Exact `why` |
|---|---|---:|---|---|---|
| B19 declared red baseline | `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` | 1 | 7 / 7 / 7 | false / false | `strict-baseline receipt for 9011581d8452 absent` |
| pristine observed main | `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 6), bytes and tool bound` |
| MutStrict M1 receipt exit 1 to 0 | `ec94605da1a4d0f09dba6d8641196d92d87a96d3` | 1 | 1 / 0 / 1 | true / false | `receipt is not a --strict run at 9011581d84527ba34c675f9cf912e54d2e72d470 with exit 1` |
| MutStrict R1 restore exact pristine receipt | `3c4972127275fa4c541cad28b45b87b3ffe055a4` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 6), bytes and tool bound` |
| MutStrict M2 argv strict token absent | `f9b72d12f685655a47023887f8124f0b1097d0ec` | 1 | 1 / 0 / 1 | true / false | `receipt is not a --strict run at 9011581d84527ba34c675f9cf912e54d2e72d470 with exit 1` |
| MutStrict R2 restore exact pristine argv | `de196c1268ce26becbd5f7f75f685b8f46a80b55` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 6), bytes and tool bound` |
| MutStrict M3 stdout zero without rehash | `634699289f6d2cc62e8e7a786ecea89aaab7f67a` | 1 | 1 / 0 / 1 | true / false | `retained stdout/stderr do not re-hash to the receipt` |
| MutStrict M4 stdout zero with matching digest | `84eb7fbe33d5e7bd84e60c2360fa7cbc774d6724` | 1 | 1 / 0 / 1 | true / false | `retained strict stdout reports open_count 0 (red baseline needs >0)` |
| MutStrict R3 restore exact pristine stdout and receipt | `9b0f6a511ad9f325dd5476596a32bac8306b7620` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 6), bytes and tool bound` |
| MutStrict M5 invented self-consistent unexecuted run | `e48c99872f23203bfbc7937120c6209534d4ed68` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 1), bytes and tool bound` |
| MutStrict R4 restore exact pristine after fabrication | `229f7d6a6fb5e0590c4de71e868dc37b926da4a7` | 0 | 0 / 0 / 0 | true / true | `strict run at 9011581 exit 1 (open 6), bytes and tool bound` |

## Surviving fabrication and its precise boundary

**Observation (M5, `e48c99872f23203bfbc7937120c6209534d4ed68`):** I wrote the following stdout from scratch; I did not execute the recorded argv. Its lone invented defect and all three counts agree internally. It is not the original six-defect stdout.

```json
{
  "defects": [
    {
      "checks": [],
      "id": "R17-INVENTED-MutStrict",
      "named_open": true,
      "open": true,
      "substance_open": true
    }
  ],
  "named_open_count": 1,
  "open_count": 1,
  "rev": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "substance_open_count": 1
}
```

The M5 retained stdout path is `.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt@e48c99872f23203bfbc7937120c6209534d4ed68:4-14` (invented id at line 5, positive count at line 12). The entire fabricated receipt was:

```json
{
  "argv": [
    "python3",
    "-I",
    "-B",
    "/tmp/kr19-MutStrict-fabricated-never-executed/routed-defects.py",
    "--root",
    "/tmp/kr19-w2-MutStrict-mduxjr5e",
    "--rev",
    "9011581d84527ba34c675f9cf912e54d2e72d470",
    "--strict"
  ],
  "ended_utc": "2000-01-01T00:00:01Z",
  "exit": 1,
  "rev": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "started_utc": "2000-01-01T00:00:00Z",
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "stdout_sha256": "f449f897c9965cc7f9431aff896c5af7014801d7f161adb98d9716b31e8516a2",
  "tool_rev": "a245bb00c581ae3423a10a055c77d4bc873918df",
  "tool_sha256": "b004c3ed76fd72aca7667e85d335c8296257e8b7e4891ef53113043950e72b03"
}
```

The M5 receipt anchor is `.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json@e48c99872f23203bfbc7937120c6209534d4ed68:6-20`: invented script pathname at line 6, invented timestamps at lines 13 and 16, claimed exit/revision at 14-15, matching output hashes at 17-18, real Git tool identity at 19-20. The timestamps are deliberately invented and are not validated by the checker; “self-consistent” here means field/JSON/hash consistency, not historically possible provenance. The actual tool blob commitment is reused, not forged cryptographically. Empty stderr is byte-identical to pristine.

Actual successful defect row from the M5 routed detector:

```json
{
  "id": "R18-STRICT-BASELINE",
  "named": true,
  "substance": true,
  "why": "strict run at 9011581 exit 1 (open 1), bytes and tool bound"
}
```

**Observation:** M4 proves that replacing the stdout digest does not by itself defeat the semantic zero guard. M5 proves that replacing the transcript with a positive, internally matching claim does defeat any interpretation of this gate as execution authentication. No historical round-18 command was invoked to create M5; only the assigned bounded routed-r18 detector was executed.

**Inference from `.ufo/waves/round-19/tools/routed-r18.py:174-189`:** the implementation trusts the claimed exit and timestamp/argv provenance, validates only membership of `--strict` rather than the rest of argv, and re-hashes whatever parseable stdout the receipt author supplies. It never compares this stdout with output generated by the committed tool. It also does not compare stdout `rev` or defect details with the claimed baseline. These unchecked fields explain the survivor; M5 alone does not separately measure every omitted binding.

**Inference, not an exercised additional mutant:** line 187 tests truthiness rather than an integer count `> 0`; no negative-number/string/bool count probe was run. No claim about those cases is counted among the four kills or the one survivor. The source also selects only the red B18 stem, so these results do not certify the paired `454dee6` green receipt.

**Scope of conclusion:** the existing retained receipt passes the selected consistency checks at the observed tip. This probe does not establish or refute its historical authenticity, does not judge the round, and makes no production fix or contract amendment.

## Before / mutant / restored hashes

Full SHA-256 values are from immutable Git blobs at the listed commits. The original snapshots were read with `git --no-optional-locks -C <clone> show <rev>:<path>` and hashed in the Eval Python process; every Git read returned 0. Each restoration additionally compared the bytes themselves with the saved pristine bytes (`==`), not only digests.

| State | Receipt SHA-256 | Retained stdout SHA-256 |
|---|---|---|
| Pristine d0690fd44f46d8a7fe9da5f01c6be723d12abd41 | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict M1 receipt exit 1 to 0 (`ec94605da1a4d0f09dba6d8641196d92d87a96d3`) | `db2bb215c046be909d903e5a29b2d1291cd3fe61535ad5f949885d76d262ab22` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict R1 restore exact pristine receipt (`3c4972127275fa4c541cad28b45b87b3ffe055a4`) | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict M2 argv strict token absent (`f9b72d12f685655a47023887f8124f0b1097d0ec`) | `ac3a3474f341220b34a7a4f6a17f80ec06af2df47290561c8f83462a5c818dde` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict R2 restore exact pristine argv (`de196c1268ce26becbd5f7f75f685b8f46a80b55`) | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict M3 stdout zero without rehash (`634699289f6d2cc62e8e7a786ecea89aaab7f67a`) | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `ef64cdf21f3a6956994d866c5ebccbd91e9c705bf420c61ef7aa08b34dea0b58` |
| MutStrict M4 stdout zero with matching digest (`84eb7fbe33d5e7bd84e60c2360fa7cbc774d6724`) | `1725bbb89903ee4e01d02a4a6d649ef43d09b5277822a4e492bd97f7af7c5d7a` | `ef64cdf21f3a6956994d866c5ebccbd91e9c705bf420c61ef7aa08b34dea0b58` |
| MutStrict R3 restore exact pristine stdout and receipt (`9b0f6a511ad9f325dd5476596a32bac8306b7620`) | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| MutStrict M5 invented self-consistent unexecuted run (`e48c99872f23203bfbc7937120c6209534d4ed68`) | `6ad354fc6617550ca6bfa3eb7d30bc4fb5e2aafb52250dde42cc7ed3a9ca8560` | `f449f897c9965cc7f9431aff896c5af7014801d7f161adb98d9716b31e8516a2` |
| MutStrict R4 restore exact pristine after fabrication (`229f7d6a6fb5e0590c4de71e868dc37b926da4a7`) | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |

Unchanged at every mutation and restoration:

- Retained stderr: 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Detector `.ufo/waves/round-19/tools/routed-r18.py`: 18741 bytes; SHA-256 `dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b`.

Final scratch commit: `229f7d6a6fb5e0590c4de71e868dc37b926da4a7`. Receipt/stdout/stderr/detector at this commit all compared byte-equal to pristine (`true` for all four). The final worktree `sha256sum` command independently returned those same four pristine hashes, exit 0. Restored detector: exit 0, `open_count=0`, STRICT-BASELINE substance true, original `open 6` reason.

## Commands and exits

Commands below are the actual argv executed via subprocess (shell quoting is for readability). Every detector used the same immutable detector bytes and `--strict`. Actual detector stdout is summarized above; no shell pipeline masked its exit. No shell mutation script was used: M1/M2/M3/M4 used successful `functions.edit` hashline patches to the exact lines listed above; M5 used successful whole-file `functions.write` calls. Restoration used inverse patches for M1/M2/M3-M4, then whole-file writes of the saved pristine Git bytes after M5. Those editor operations have tool-success results, not fabricated OS exit codes.

Initial main observation (read-only):
```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
# exit 0; d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

Capture / commit / detector transcript (Git object reads are grouped separately below):

```sh
git --no-optional-locks clone --quiet --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-MutStrict-mduxjr5e
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e checkout --quiet --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout d0690fd44f46d8a7fe9da5f01c6be723d12abd41
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# exit 1
# stdout JSON projection {"named_open": 7, "open_count": 7, "rev": "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": false, "substance": false, "why": "strict-baseline receipt for 9011581d8452 absent"}, "substance_open": 7}
# stderr empty
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"}, "substance_open": 0}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict M1 receipt exit 1 to 0'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout ec94605da1a4d0f09dba6d8641196d92d87a96d3
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev ec94605da1a4d0f09dba6d8641196d92d87a96d3 --strict
# exit 1
# stdout JSON projection {"named_open": 0, "open_count": 1, "rev": "ec94605da1a4d0f09dba6d8641196d92d87a96d3", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": false, "why": "receipt is not a --strict run at 9011581d84527ba34c675f9cf912e54d2e72d470 with exit 1"}, "substance_open": 1}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict R1 restore exact pristine receipt'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout 3c4972127275fa4c541cad28b45b87b3ffe055a4
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 3c4972127275fa4c541cad28b45b87b3ffe055a4 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "3c4972127275fa4c541cad28b45b87b3ffe055a4", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"}, "substance_open": 0}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict M2 argv strict token absent'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout f9b72d12f685655a47023887f8124f0b1097d0ec
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev f9b72d12f685655a47023887f8124f0b1097d0ec --strict
# exit 1
# stdout JSON projection {"named_open": 0, "open_count": 1, "rev": "f9b72d12f685655a47023887f8124f0b1097d0ec", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": false, "why": "receipt is not a --strict run at 9011581d84527ba34c675f9cf912e54d2e72d470 with exit 1"}, "substance_open": 1}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict R2 restore exact pristine argv'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout de196c1268ce26becbd5f7f75f685b8f46a80b55
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev de196c1268ce26becbd5f7f75f685b8f46a80b55 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "de196c1268ce26becbd5f7f75f685b8f46a80b55", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"}, "substance_open": 0}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict M3 stdout zero without rehash'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout 634699289f6d2cc62e8e7a786ecea89aaab7f67a
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 634699289f6d2cc62e8e7a786ecea89aaab7f67a --strict
# exit 1
# stdout JSON projection {"named_open": 0, "open_count": 1, "rev": "634699289f6d2cc62e8e7a786ecea89aaab7f67a", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": false, "why": "retained stdout/stderr do not re-hash to the receipt"}, "substance_open": 1}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict M4 stdout zero with matching digest'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout 84eb7fbe33d5e7bd84e60c2360fa7cbc774d6724
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 84eb7fbe33d5e7bd84e60c2360fa7cbc774d6724 --strict
# exit 1
# stdout JSON projection {"named_open": 0, "open_count": 1, "rev": "84eb7fbe33d5e7bd84e60c2360fa7cbc774d6724", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": false, "why": "retained strict stdout reports open_count 0 (red baseline needs >0)"}, "substance_open": 1}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict R3 restore exact pristine stdout and receipt'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout 9b0f6a511ad9f325dd5476596a32bac8306b7620
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 9b0f6a511ad9f325dd5476596a32bac8306b7620 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "9b0f6a511ad9f325dd5476596a32bac8306b7620", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"}, "substance_open": 0}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict M5 invented self-consistent unexecuted run'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout e48c99872f23203bfbc7937120c6209534d4ed68
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev e48c99872f23203bfbc7937120c6209534d4ed68 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "e48c99872f23203bfbc7937120c6209534d4ed68", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 1), bytes and tool bound"}, "substance_open": 0}
# stderr empty
git -C /tmp/kr19-w2-MutStrict-mduxjr5e add -- .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# exit 0
git -C /tmp/kr19-w2-MutStrict-mduxjr5e -c 'user.name=MutStrict probe' -c user.email=mutstrict@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet -m 'MutStrict R4 restore exact pristine after fabrication'
# exit 0
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e rev-parse HEAD
# exit 0
# stdout 229f7d6a6fb5e0590c4de71e868dc37b926da4a7
python3 -I -B /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutStrict-mduxjr5e --rev 229f7d6a6fb5e0590c4de71e868dc37b926da4a7 --strict
# exit 0
# stdout JSON projection {"named_open": 0, "open_count": 0, "rev": "229f7d6a6fb5e0590c4de71e868dc37b926da4a7", "strict_baseline": {"id": "R18-STRICT-BASELINE", "named": true, "substance": true, "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"}, "substance_open": 0}
# stderr empty
sha256sum /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py
# exit 0
# dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50  /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json
# 48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316  /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt
# e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutStrict-mduxjr5e/.ufo/waves/round-19/tools/routed-r18.py
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
# exit 0
# stdout d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

Committed-blob hash reads: the following is the actual command pattern, instantiated for each of the four paths and each of the nine scratch commits in the output table; all 36 calls returned exit 0. Their stdout was captured as bytes and SHA-256/byte equality recorded rather than printed as text. The four pristine snapshot calls used the same pattern at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` and also returned exit 0.

```sh
git --no-optional-locks -C /tmp/kr19-w2-MutStrict-mduxjr5e show <FULL_REV>:<PATH>
# PATH: .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.receipt.json
# PATH: .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stdout.txt
# PATH: .ufo/waves/round-19/evidence/strict-baseline/9011581d8452.stderr.txt
# PATH: .ufo/waves/round-19/tools/routed-r18.py
# all instantiated exits: 0
```

## Safety and handoff

- The only lane write is this report. All Git writes and evidence mutations were inside the named scratch clone. No sibling source, fleet state, client config, lane production source, or historical retained bytes in the lane were changed.
- Scratch is retained with restored worktree and immutable mutant/restoration commits for audit; it was not declared disposable and no damaged bytes remain at its final checkout.
- No delegation, runtime orchestration, REA/MCP/Ghidra call, carrier execution, builds, broad suite, formatter, or installation/update. **Tool installations/updates: none.**
- Assigned mutation probe complete. No integration/ship/round judgement; four exercised kills and one execution-authenticity survivor are the scoped findings.

Report generated UTC: 2026-10-20T19:19:18.935786+00:00
