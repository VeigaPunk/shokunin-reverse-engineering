# R41CritC2Draft artifacts — reproducers for the R41-C2 draft attack

Seat: `R41CritC2Draft` (critic, leaf). Report: `.ufo/waves/round-41/w1/R41CritC2Draft.md`.
Nothing here is a lane instrument, a candidate table, or a proposed landing: these are
measurement scripts and their outputs, cited by the report.

Tool versions used: Python 3.14.8, node v24.21.0, npx 11.19.0, REA `rea-agents@6.5.0`
(`package.json` sha256 prefix `a500302319c1214a`), unblob 26.6.4, sasquatch-v4be 4.5.1.
No installs, no upgrades, no pacman transaction. No vendor firmware bytes are stored here;
the only real-firmware data are digest fields read from committed lane receipts.

## Scripts

| file | sha256 | what it measures |
|---|---|---|
| `comboprobe.py` | `2213a56014d450e3627f33d59af210595f84d77f4184b387db49ccc5bb155612` | builds four fresh carriers from the round-40 generator's own writer + damage recipes (in-tree links / both link kinds, `partial` damage) and runs REA `extract-firmware` once each; also runs one deliberately refused call (`--max-output-files 1`) |
| `nested.py` | `5023a08d83bf74008eab2dd6e8cd037264f0b7c2c1cd5c653b08f3d643a44b95` | (a) one lane-built squashfs holding a second squashfs plus an in-tree and an escaping symlink, run at `--max-depth 1,2,3`; (b) four further seeds of "both link kinds + partial damage" |
| `flat.py` | `420b779562dc3d44dd25bdf6601b19354dfeb5051be4138e69729446d921ccfd` | one flat, clean, single-file squashfs (no nesting, no links) at `--max-depth 1,2,3` |
| `precedence-probe.py` | `20d155e64590347e99ee9ea428505693d94c5898ca222e68821c52a09874216d` | the **draft** precedence text (`plans/round-41-claims.md:75-88`) implemented literally, applied to the four committed round-40 C1 receipts and to the probe envelopes; reports the distinct (label, action) pairs it decides and the labels that have no action token in the v2 vocabulary |
| `real-carrier-features.py` | `e29fb854a549fb5492616df98a085464a852df3dc1dcda67c7e963a275db235a` | feature table (with receipt sha256) of the four committed round-40 C1 `after.json` receipts |

Rebuild the carrier generators' inputs: both probes load the lane's own
`tools/round-40/heldout-gen-v2.py` (writer `tools/round-39/gen-squashfs.py`) by path and reuse
its `build_tree` / `corruption_partial` / `rea_env`; they add only the recipe keys named above.

## Data

| file | sha256 | content |
|---|---|---|
| `precedence-real.tsv` | `a749c7cd4f4cec6d68f2b12e2380a7fbf9afb0db78a0809fb8ee02f9a3082af8` | the draft precedence applied to 4 real + 4 probe envelopes (stdout of `precedence-probe.py`) |
| `data/real-carriers.tsv` | `b0fd043d50af49d02ee488048f23f366f099164aa1449d8731b714ca7ea2ee71` | V1/V2/L1/L2 receipt digest + full feature vector |
| `data/probe1-report.json` | `64d53ce8ded5f888b6614ab1eb53ac03b6a53888c8300d2884e14ace5af44ab3` | combined-gap probe: 4 carriers, REA exit/ok, features, envelope sha256; plus the refused-run envelope |
| `data/probe2-report.json` | `4cf8d72c2b22d4f659a075c1fe7e4347d160918796b07773a46719a8348c1312` | nested-depth runs + 4 partial+mixed seeds |
| `data/probe3-report.json` | `540adc248d32a152ea8c8bebf9508a1f418e4113e7b7e890c1c65f594559829a` | flat image at depth 1/2/3 |
| `data/H01..H04/envelope.json`, `run.json` | — | the four combined-set REA envelopes (bare `data` object), with the generator's own run record |

Carrier bytes are **not** stored: each is a pure function of the seed and class, and every
`report*.json` / `run.json` carries its `carrier_sha256`. Rebuild:

```
python3 -I -B comboprobe.py <outdir> 41c2d0ff1cebabe1      # H01..H04 + refused run
python3 -I -B nested.py <outdir>                            # nested depth 1/2/3 + 4 seeds
python3 -I -B flat.py                                       # flat image depth 1/2/3
```

Scratch roots used by the probes were `/fast/scratch/hyaku/kaidoku-r41/R41CritC2Draft` and were
removed after the report was written; the numbers in the report are reproducible from the
commands above with the recorded seeds.
