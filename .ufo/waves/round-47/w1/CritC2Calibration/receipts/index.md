# Receipts — CritC2Calibration (round 47, wave 1)

Exact command, exit code (0 = ran and reproduced; 1 = the counter's not-met verdict; 2 =
could-not-evaluate), sha256 of the file's bytes, and the UTC time the receipt records (else its
mtime). `receipts/tip/` is the re-measurement at `b1a058f3`; the rest were taken at `09a9f912`
or earlier, and each names its revision.

## Measurements at `09a9f912` and earlier

| receipt | command | subject | sha256 | UTC |
|---|---|---|---|---|
| `receipts/c2-at-base.json` | `python3 -I -B tools/round-47/record.py --root <lane> --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 --no-battery --json-out <this file>` | rev 13a9e9e1f7ca | `b80145e20a2a99026819848acb4cdf27c214f6c5326e55bcbf553e9e13a6a5cb` | 2026-10-28T17:58:01Z |
| `receipts/c2-at-head.json` | `python3 -I -B tools/round-47/record.py --root <lane> --rev 2e4ae43463aabdae707f8c8a4daa41441ad67a71 --json-out <this file>` | rev 2e4ae43463aa | `553be365645d8fe69adfac6a1888c67dacd72f12e608ebe71784ea9467d88fc0` | 2026-10-28T17:53:46Z |
| `receipts/c2-at-live.json` | `python3 -I -B tools/round-47/record.py --root . --rev 09a9f912f4a639b91bce7dcd3711d8f391969d4f --json-out <this file>` | rev 09a9f912f4a6 | `bda3988f7c7d67f2b41df5d7a1e4a675cc7fa72efeae6c8848c27203da5c8b19` | 2026-10-28T18:01:48Z |
| `receipts/c2-atom-census.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/probes.py --lane <lane> --rev 09a9f912 --out-dir <receipts>` | rev 09a9f912f4a6 | `f2601536059d86fad1675a7a5c9f9dd50531d7b1eb4702c89949bc0b15926b92` | 2026-10-28T18:10:34Z |
| `receipts/c2-attack-cases.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/c2-attack.py --lane <lane>` | 0 | `bad16bd8f892372d7eb8c975e02d9d73dd1e6f81f332f9f12a727981e71bb59b` | 2026-10-28T18:00:52Z |
| `receipts/c2-timeline.json` | `same probes.py run (09a9f912)` | head 09a9f912f4a6 | `0b4233d232f4a1db2d29d6aa70c9326ca0cfd867fa607e81fdd60bcbae524754` | 2026-10-28T18:10:38Z |
| `receipts/command-a-09a9f912.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py 09a9f912` | rev 09a9f912f4a6 | `0165c5eaf71bb56e463691d4e79da7275c0d1ed8b56b0ca945e16db118b9ab07` | 2026-10-28T18:04:06Z |
| `receipts/command-a-13a9e9e1.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py 13a9e9e1` | rev 13a9e9e1 | `8f350aff52a992400891282cb92d7ee58d54fb9bf047b1c026eb5195a7a28135` | 2026-10-28T17:59:43Z |
| `receipts/command-a-2e4ae434.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py 2e4ae434` | rev 2e4ae434 | `1bba2db928a345db41d9c7240f0211a538294d16aea83e9c5b80ccdffe1fbe77` | 2026-10-28T17:59:43Z |
| `receipts/command-a-58eb04b6.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py 58eb04b6` | rev 58eb04b6 | `909d80f6b8688059ba3110f836c32d077e9177a3892079bac6c06c8440cbe16f` | 2026-10-28T17:59:43Z |
| `receipts/command-a-repair-demo.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py 2e4ae434 --repair-demo` | rev 2e4ae434 | `00e618dbc741083e3cdec175c9f5b009e21a48f6fc8a92749120984698024420` | 2026-10-28T18:07:18Z |
| `receipts/ledger-vs-receipt.json` | `same probes.py run (09a9f912)` | head 09a9f912f4a6 | `07e6db60cd3fb14e4c89a9e865c026ca434e7a85404d8008dc67e0ca65ef87af` | 2026-10-28T18:10:38Z |
| `receipts/record-open-defects.json` | `same probes.py run (09a9f912)` | 0 | `30a39f58c6448510d442295e2e8d04f0b4bd4b3df0e08edb0769a3b7a515db04` | 2026-10-28T18:10:38Z |
| `receipts/record-selftest.txt` | `python3 -I -B tools/round-47/record.py --selftest --root . --rev 09a9f912` | 0 | `de00da68efe13f902d8754335bee3432eead675c3fb002235d1a96aab50ac5e8` | 2026-10-28T18:03:16Z |
| `receipts/tool-pinning.txt` | `same probes.py run (09a9f912)` | 0 | `d218f68200a30ced5076f26801f631367d7170b93e2e29ded513da401490ba48` | 2026-10-28T18:10:38Z |

## Re-measurement at the tip `b1a058f3`

| receipt | command | subject | sha256 | UTC |
|---|---|---|---|---|
| `receipts/tip/c2-at-tip.json` | `python3 -I -B tools/round-47/record.py --root . --rev b1a058f32c6908a6b92248052f151d0b0e2c76b1 --json-out <this file>` | rev b1a058f32c69 | `3092e068b13f1d653fcbe7059e6b1b644b594aecd3b29f7e35e24d7f3fc333f9` | 2026-10-28T18:11:29Z |
| `receipts/tip/c2-atom-census.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/probes.py --lane . --rev b1a058f3 --out-dir <receipts/tip>` | rev b1a058f32c69 | `4f02d708c250f60dd347f644f515e2d398075c219ec7478d20c5c62544b4aa9c` | 2026-10-28T18:11:29Z |
| `receipts/tip/c2-timeline.json` | `same probes.py run (tip)` | head b1a058f32c69 | `89f6bfef1e1421275502db8e31349d99bf535f375c86d753d577d495b76ce76e` | 2026-10-28T18:11:32Z |
| `receipts/tip/command-a-tip.json` | `python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py b1a058f3` | rev b1a058f32c69 | `7fff68f91fb3099a9ad94d0476f6052443c3e9ef88f957c4ecac502c4caea3a7` | 2026-10-28T18:11:32Z |
| `receipts/tip/ledger-vs-receipt.json` | `same probes.py run (tip)` | head b1a058f32c69 | `bfefd849c0379e5cd8741ff935a4174f50bdc8c262f03403615ceb4b46ddf483` | 2026-10-28T18:11:32Z |
| `receipts/tip/record-open-defects.json` | `same probes.py run (tip)` | 0 | `4a96fada2998276e06dc6d51b70e59167e7328a9762540fea65fe18f3e781f8a` | 2026-10-28T18:11:32Z |
| `receipts/tip/tool-pinning.txt` | `same probes.py run (tip)` | 0 | `52b8a71945147d3b6870469bf968e0f77bc8003a7b4ded057a077cc7314b31bd` | 2026-10-28T18:11:32Z |

## Drivers

- `fixtures/c2-attack.py` — 14-case fixture battery over the exemption machinery (9 green-by-defect, 3 controls, 1 honest green, 1 honest-pair rejection).
- `fixtures/command-a.py` — command A verbatim from `SCORECARD.md`'s recipe, by revision; `--repair-demo` shows the depth arithmetic of one added citation.
- `fixtures/probes.py` — census, timeline, ledger-vs-receipt, open-defect and pinning receipts.

All three read the lane only; they write only what `--out-dir` names.
