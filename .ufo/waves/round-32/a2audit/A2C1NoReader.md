# C1 NoReader control — target unmet, full-comparison rejection observed

UTC report: 2026-10-23T06:54:25+00:00  
Seat: A2C1NoReader; new attempt-2 fixture, not an attempt-1 resend.  
Assigned axes: **coverage** (C1 ARM64X Frontier→Core), **calibration** (C2 Capabilities vs pinned non-author closure). This seat exercised C1 only; C2 was not scored or changed.

## Result and counterexample

The requested NoReader forge did **not** meet the frozen target. After resolving the provider environment, every k01–k12 verdict was `P1-fail` at committed-versus-live full-envelope comparison:

```text
k01	P1-fail	committed envelope differs from the live envelope (full comparison)
k02	P1-fail	committed envelope differs from the live envelope (full comparison)
k03	P1-fail	committed envelope differs from the live envelope (full comparison)
k04	P1-fail	committed envelope differs from the live envelope (full comparison)
k05	P1-fail	committed envelope differs from the live envelope (full comparison)
k06	P1-fail	committed envelope differs from the live envelope (full comparison)
k07	P1-fail	committed envelope differs from the live envelope (full comparison)
k08	P1-fail	committed envelope differs from the live envelope (full comparison)
k09	P1-fail	committed envelope differs from the live envelope (full comparison)
k10	P1-fail	committed envelope differs from the live envelope (full comparison)
k11	P1-fail	committed envelope differs from the live envelope (full comparison)
k12	P1-fail	committed envelope differs from the live envelope (full comparison)
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Observed counter exit: **1**. Frozen requested target remains `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0. No shortcut met it; this is not a FALSIFIED finding.

The attempted counterexample is a committed set of twelve plausible inspect envelopes constructed solely from the frozen oracle plus the committed probe's shape. All carrier digests are the frozen correct values. Every forged evidence ID is `ev_` plus 64 zero hexadecimal digits. The entry cites the frozen S099 label and includes that ID; a Core table row points to the entry. The observed documentation gates both passed, but the complete predicate rejected every forged envelope.

[INFERENCE] The resolved-run rejection reason is reachable only after the frozen live-envelope checks have passed, including live exit/ok, ARM64X classification, operation, carrier digest, oracle-projected report and predicted procedure count (`c1-arm64x-positive.py:69–87,198–202`). Thus this run exercised the committed-envelope check, unlike the initial run. The counter does not print the live envelopes or differing keys; rejection cannot be attributed solely to the zero ID rather than another copied non-oracle field. This is evidence about this exact forge, not universal provenance authentication.

[INFERENCE / not exercised] Full-envelope equality establishes record association, not producer authenticity. An oracle-derived record that also reproduced REA's canonical-ID calculation and every remaining non-meta field could theoretically match without having been produced by a reader: the frozen comparison does not inspect construction history. This item did not compute canonical IDs or retain live full envelopes, so the attainability of that conditional match is untested. **Mismatch localization is unknown:** the observed receipt cannot distinguish an ID-only mismatch from additional full-envelope field mismatches. No extra carrier call or changed fixture was used to investigate it.

## Environment failure retained, not counted as discrimination

The first run's Eval subprocess environment contained `GHIDRA_INSTALL_DIR=null` and `JAVA_HOME=null`. Its actual complete counter stdout was:

```text
k01	P1-fail	exit 1 ok False
k02	P1-fail	exit 1 ok False
k03	P1-fail	exit 1 ok False
k04	P1-fail	exit 1 ok False
k05	P1-fail	exit 1 ok False
k06	P1-fail	exit 1 ok False
k07	P1-fail	exit 1 ok False
k08	P1-fail	exit 1 ok False
k09	P1-fail	exit 1 ok False
k10	P1-fail	exit 1 ok False
k11	P1-fail	exit 1 ok False
k12	P1-fail	exit 1 ok False
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Initial counter exit: **1**. That receipt is **unevaluable for NoReader discrimination**: the live calls failed before committed-envelope comparison. No precise underlying provider error is claimed: the unchanged counter captures each REA stdout/stderr but does not publish or persist it in measure mode. Its retained original error text is exactly `exit 1 ok False` for each carrier; the counter's own stderr was empty.

A separate Bash `printenv GHIDRA_INSTALL_DIR JAVA_HOME` returned the two configured absolute paths. Following the resolved-prerequisite instruction, exactly one additional scoring run used the **same frozen counter, same committed fixture, same revision and same argv**, with only these explicit environment additions:

```json
{
  "GHIDRA_INSTALL_DIR": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
  "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk"
}
```

No unchanged retry, direct REA inspection, REA write mode, counter/input/predicate/target edit, or model switch was used.

## Evidence and smallest safe correction

- **Counterexample tested:** oracle-only forged records with correct carrier hashes, probe-derived data, zero evidence IDs, S099 entry and Core row.
- **Evidence:** the resolved run gives twelve full-comparison failures, documentation gates 1/1, pass 0/12 and exit 1; the initial environment-failure receipt is retained separately below.
- **Impacted axes:** false persisted provenance would undermine C1 coverage evidence. Misreading the initial provider failures as discrimination would undermine calibration of this audit. No finding or measurement is made about C2.
- **Smallest safe correction:** retain the frozen full-envelope comparison; no production counter correction is established by this control. Supply and record the two resolved provider variables, and exclude provider-failure receipts from discrimination evidence. No axis tradeoff, claim-admission decision, or canonical Rust-judge verdict is supplied.

Source was re-opened 2026-10-23 at `file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone/tools/round-32/c1-arm64x-positive.py`; revision `f7ba512dd9244df02773378cb0f66f22abac32fb`; SHA-256 `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a`. At line 122, the returned reason is: “committed envelope differs from the live envelope (full comparison)” (9 words). The branch is at lines 121–122; its caller is at 198–202. The oracle projection was re-opened at `tools/round-32/arm64x_oracle.py:112–135`, SHA-256 `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686`.

## Sandbox custody and bounds

- Lane production content and Git/jj state were read-only. The only lane write is this assigned Report; all fixture/Git writes are inside `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader`. No sibling-seat path or held item was inspected or changed.
- Start revision: `f382e3b7978e6091a19ca93277c15a75c0016b43`; assigned C1 freeze: `9a73680a`; C2 v3 freeze: `f382e3b7`; base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- Exactly one sandbox fixture commit: `f7ba512dd9244df02773378cb0f66f22abac32fb`, author and committer `ctl <ctl@local>`. Its complete diff is embedded below: 14 files, 40 insertions. No lane/fleet commit or push was made.
- Report construction made no REA call. Its generator imported only the frozen Python oracle and read carrier bytes as data; carriers were never executed. The counter itself made the scoring REA calls at the frozen 6.5.0 pin.
- Generator limits: 4 GiB address space, 1 MiB per file and aggregate envelope-write guard. It wrote 62,964 envelope bytes (5,247 each); no recursion. The counter's Ghidra subprocesses were not subject to the fixture address-space limit. Each launched fixture/score command used timeout 900 seconds; the frozen inner REA timeout is 600 seconds per call. No build or carrier rebuild was performed.
- Each scoring process was launched in its own process group. Cleanup recorded `owned score process group absent after counter completion` for the initial run and `owned score process group absent after counter completion` for the resolved run. No owned scoring group remained at return from either run.
- Tools installed/updated: **none**. Existing Python 3.14.8, Git 2.56.0, GNU timeout 9.12, cached npm `rea-agents` 6.5.0. The Bash version pipeline's `timeout --version` wrapper returned usage/125; the direct `/usr/bin/timeout --version` returned 0 and identified GNU coreutils 9.12. These are diagnostic command observations, not a verification rerun.
- Existing REA package JSON SHA-256: `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`. Resolved Ghidra `Ghidra/application.properties`: `e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67`; Java `release`: `16b1bf12d3d42d3386bbef4c145613a9ef5ab18b1e0e011d6127f4431229e482`.
- Scratch full diff: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/fixture-control.patch`, SHA-256 `89c165238ea5f20bdf0d89169d8322dd7231bc14922e28cc6df7b7d9707f7a07`. Scratch receipts and all fixture/source hashes are retained below, so L1 can preserve this complete control before data without importing the forged fixture as production evidence.

## Exact preflight and checkout receipt

The directory was created with `mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader` before the isolated clone. Every Git invocation had `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset; `git -C` used absolute paths. The clone command was wrapped by `timeout 900`.

```json
{
  "utc_observed": "2026-10-23T06:45:23Z",
  "argv": [
    "df",
    "-h",
    "/fast"
  ],
  "exit": 0,
  "stdout": "Filesystem      Size  Used Avail Use% Mounted on\n/dev/nvme1n1p2  804G  559G  245G  70% /fast\n",
  "clone_argv": [
    "git",
    "-C",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader",
    "clone",
    "--no-hardlinks",
    "--no-checkout",
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone"
  ],
  "clone_exit": 0,
  "clone_output": "Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone'...\ndone.\n",
  "checkout_argv": [
    "git",
    "-C",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
    "checkout",
    "--detach",
    "f382e3b7"
  ],
  "checkout_exit": 0,
  "checkout_output": "HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) \u2014 anchored evidence and description, before receipts\n",
  "git_environment_unset": [
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE"
  ]
}
```

## Complete generation receipt

```json
{
  "utc_start": "2026-10-23T06:47:29+00:00",
  "utc_end": "2026-10-23T06:47:30+00:00",
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader",
  "argv": [
    "timeout",
    "900",
    "python3",
    "-I",
    "-B",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/forge-fixture.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone"
  ],
  "exit": 0,
  "stdout": "utc_start=2026-10-23T06:47:30+00:00\nmethod=committed-probe-shape + frozen-oracle expected fields; no REA invocation\nevidence_id=ev_0000000000000000000000000000000000000000000000000000000000000000\n{\"bytes\": 5247, \"carrier_sha256\": \"2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989\", \"envelope_sha256\": \"0ab09200da988ecaae183d9ffa0e4e7fb03d91b0225c8803f3703d23f6984dfb\", \"id\": \"k01\", \"procedure_count\": 1, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4\", \"envelope_sha256\": \"f208b629d7d51673f82bd4e946399a1842352a5a428b18d1694e3cfb9bb527d6\", \"id\": \"k02\", \"procedure_count\": 2, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d\", \"envelope_sha256\": \"8d418257f9910c59d2bd2d583e81d3947f80e69c65c20964e8bcd79ddf4ca737\", \"id\": \"k03\", \"procedure_count\": 3, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386\", \"envelope_sha256\": \"0babfba3dc0dfd3594512d34438ee391584df7ffe30e631eee6bc7a251f2afbd\", \"id\": \"k04\", \"procedure_count\": 4, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf\", \"envelope_sha256\": \"c224fabc7cc951a421c42d7461153cce7ca87141060d07a85eae0bc8b82794f9\", \"id\": \"k05\", \"procedure_count\": 1, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c\", \"envelope_sha256\": \"1c545cd05715c50ec1d3ac5c94d58cbbfdd421714487401d0722edca28cf696f\", \"id\": \"k06\", \"procedure_count\": 5, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f\", \"envelope_sha256\": \"6cd125e7d17e00e4481344ff83799009d759c935d4d94d846a029fd1aa10a641\", \"id\": \"k07\", \"procedure_count\": 6, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c\", \"envelope_sha256\": \"54964f2f94950b10b6f36e4203db4ffd4726fb7be27684bb03279036b480c302\", \"id\": \"k08\", \"procedure_count\": 2, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87\", \"envelope_sha256\": \"471ef80fa21c93159f2feef92aad4cc18d9b8dc44170e6163fe86b4fc93cd50d\", \"id\": \"k09\", \"procedure_count\": 7, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7\", \"envelope_sha256\": \"1e9d1ccfaf90dd287234d92d81e139950cdfe614564c04d6aed19d9c8c6339cb\", \"id\": \"k10\", \"procedure_count\": 3, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181\", \"envelope_sha256\": \"d8d102225f5f789f2c3088f7b1e262a4632167c27c0a22bf834e1a1dcb1e5ae5\", \"id\": \"k11\", \"procedure_count\": 8, \"segment_count\": 8}\n{\"bytes\": 5247, \"carrier_sha256\": \"8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa\", \"envelope_sha256\": \"d9b7b0c0741f68350219e191814140649db399a1d7e4c578a1c141c4482611b0\", \"id\": \"k12\", \"procedure_count\": 1, \"segment_count\": 8}\nfixture_bytes=62964\nutc_end=2026-10-23T06:47:30+00:00\n",
  "stderr": ""
}
```

## Complete sandbox commit receipt

```json
{
  "identity": "ctl <ctl@local>",
  "git_environment_unset": [
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE"
  ],
  "commands": [
    {
      "utc_start": "2026-10-23T06:47:55+00:00",
      "utc_end": "2026-10-23T06:47:55+00:00",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "commit.gpgsign=false",
        "add",
        "--",
        "PROVINCE.md",
        "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md",
        "corpus/evidence/round-32/c1/envelopes/k01.json",
        "corpus/evidence/round-32/c1/envelopes/k02.json",
        "corpus/evidence/round-32/c1/envelopes/k03.json",
        "corpus/evidence/round-32/c1/envelopes/k04.json",
        "corpus/evidence/round-32/c1/envelopes/k05.json",
        "corpus/evidence/round-32/c1/envelopes/k06.json",
        "corpus/evidence/round-32/c1/envelopes/k07.json",
        "corpus/evidence/round-32/c1/envelopes/k08.json",
        "corpus/evidence/round-32/c1/envelopes/k09.json",
        "corpus/evidence/round-32/c1/envelopes/k10.json",
        "corpus/evidence/round-32/c1/envelopes/k11.json",
        "corpus/evidence/round-32/c1/envelopes/k12.json"
      ],
      "exit": 0,
      "stdout": "",
      "stderr": ""
    },
    {
      "utc_start": "2026-10-23T06:47:55+00:00",
      "utc_end": "2026-10-23T06:47:55+00:00",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "--no-gpg-sign",
        "-m",
        "control: round-32 attempt-2 C1 NoReader oracle-only synthetic evidence"
      ],
      "exit": 0,
      "stdout": "[detached HEAD f7ba512d] control: round-32 attempt-2 C1 NoReader oracle-only synthetic evidence\n 14 files changed, 40 insertions(+)\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k01.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k02.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k03.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k04.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k05.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k06.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k07.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k08.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k09.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k10.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k11.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k12.json\n create mode 100644 corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\n",
      "stderr": ""
    }
  ],
  "revision_argv": [
    "git",
    "-C",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
    "rev-parse",
    "HEAD"
  ],
  "revision_exit": 0,
  "revision_stdout": "f7ba512dd9244df02773378cb0f66f22abac32fb\n",
  "revision_stderr": ""
}
```

## Complete original scoring receipt — environment failure

```json
{
  "utc_start": "2026-10-23T06:48:25+00:00",
  "utc_end": "2026-10-23T06:48:37+00:00",
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
  "argv": [
    "timeout",
    "--kill-after=5s",
    "900s",
    "python3",
    "-I",
    "-B",
    "tools/round-32/c1-arm64x-positive.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
    "--rev",
    "f7ba512dd9244df02773378cb0f66f22abac32fb"
  ],
  "sandbox_revision": "f7ba512dd9244df02773378cb0f66f22abac32fb",
  "pid": 3293299,
  "exit": 1,
  "stdout": "k01\tP1-fail\texit 1 ok False\nk02\tP1-fail\texit 1 ok False\nk03\tP1-fail\texit 1 ok False\nk04\tP1-fail\texit 1 ok False\nk05\tP1-fail\texit 1 ok False\nk06\tP1-fail\texit 1 ok False\nk07\tP1-fail\texit 1 ok False\nk08\tP1-fail\texit 1 ok False\nk09\tP1-fail\texit 1 ok False\nk10\tP1-fail\texit 1 ok False\nk11\tP1-fail\texit 1 ok False\nk12\tP1-fail\texit 1 ok False\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
  "stderr": "",
  "process_cleanup": [
    "owned score process group absent after counter completion"
  ],
  "original_provider_environment": {
    "GHIDRA_INSTALL_DIR": null,
    "JAVA_HOME": null
  }
}
```

## Complete resolved-environment scoring receipt

```json
{
  "utc_start": "2026-10-23T06:50:02+00:00",
  "utc_end": "2026-10-23T06:51:49+00:00",
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
  "argv": [
    "timeout",
    "--kill-after=5s",
    "900s",
    "python3",
    "-I",
    "-B",
    "tools/round-32/c1-arm64x-positive.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone",
    "--rev",
    "f7ba512dd9244df02773378cb0f66f22abac32fb"
  ],
  "sandbox_revision": "f7ba512dd9244df02773378cb0f66f22abac32fb",
  "pid": 3980532,
  "original_provider_environment": {
    "GHIDRA_INSTALL_DIR": null,
    "JAVA_HOME": null
  },
  "environment_overrides": {
    "GHIDRA_INSTALL_DIR": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
    "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk"
  },
  "exit": 1,
  "stdout": "k01\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk02\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk03\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk04\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk05\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk06\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk07\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk08\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk09\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk10\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk11\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk12\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
  "stderr": "",
  "process_cleanup": [
    "owned score process group absent after counter completion"
  ]
}
```

## File hashes

Paths prefixed `clone/` are relative to the unique scratch directory, not lane paths.

```text
a4bd78d12f65d755002127cb6be1709899948962be9c379b376e7230b9f48b2b  clone/PROVINCE.md
f922df3036dc048a05b337e506bccc9f165bfa71133e8d428015f321430a54f0  clone/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
0ab09200da988ecaae183d9ffa0e4e7fb03d91b0225c8803f3703d23f6984dfb  clone/corpus/evidence/round-32/c1/envelopes/k01.json
f208b629d7d51673f82bd4e946399a1842352a5a428b18d1694e3cfb9bb527d6  clone/corpus/evidence/round-32/c1/envelopes/k02.json
8d418257f9910c59d2bd2d583e81d3947f80e69c65c20964e8bcd79ddf4ca737  clone/corpus/evidence/round-32/c1/envelopes/k03.json
0babfba3dc0dfd3594512d34438ee391584df7ffe30e631eee6bc7a251f2afbd  clone/corpus/evidence/round-32/c1/envelopes/k04.json
c224fabc7cc951a421c42d7461153cce7ca87141060d07a85eae0bc8b82794f9  clone/corpus/evidence/round-32/c1/envelopes/k05.json
1c545cd05715c50ec1d3ac5c94d58cbbfdd421714487401d0722edca28cf696f  clone/corpus/evidence/round-32/c1/envelopes/k06.json
6cd125e7d17e00e4481344ff83799009d759c935d4d94d846a029fd1aa10a641  clone/corpus/evidence/round-32/c1/envelopes/k07.json
54964f2f94950b10b6f36e4203db4ffd4726fb7be27684bb03279036b480c302  clone/corpus/evidence/round-32/c1/envelopes/k08.json
471ef80fa21c93159f2feef92aad4cc18d9b8dc44170e6163fe86b4fc93cd50d  clone/corpus/evidence/round-32/c1/envelopes/k09.json
1e9d1ccfaf90dd287234d92d81e139950cdfe614564c04d6aed19d9c8c6339cb  clone/corpus/evidence/round-32/c1/envelopes/k10.json
d8d102225f5f789f2c3088f7b1e262a4632167c27c0a22bf834e1a1dcb1e5ae5  clone/corpus/evidence/round-32/c1/envelopes/k11.json
d9b7b0c0741f68350219e191814140649db399a1d7e4c578a1c141c4482611b0  clone/corpus/evidence/round-32/c1/envelopes/k12.json
7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a  clone/tools/round-32/c1-arm64x-positive.py
17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686  clone/tools/round-32/arm64x_oracle.py
8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e  clone/corpus/evidence/round-32/c1/carriers.tsv
fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b  clone/corpus/evidence/round-32/c1/predictions.tsv
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  clone/.ufo/waves/round-32/claims.json
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  clone/.ufo/waves/round-32/claims-v3.json
4eabbb60e11610f915c3e649f6c2afe8261fe25972f0f0cf2a623d6b165e1b15  clone/.ufo/waves/round-32/before/probe/insp.json
4a04457d9de160641c6a36da50f6793b3d47c626ffdbffb565358acc7a919332  forge-fixture.py
fce41402590a3830e87c6660e060f5499a665fd2cb8df2e604fdc4c417b278b8  fixture-generation-receipt.json
e62e2e67436c5296c3a4268d323c66596797ba62409e0c29b79db256795a0a19  sandbox-commit-receipt.json
89c165238ea5f20bdf0d89169d8322dd7231bc14922e28cc6df7b7d9707f7a07  fixture-control.patch
a3f75aa1161b9d6dfd501f22394adaeaaa79b7df2ab57d465a5f2695f2e5f2b7  c1-noreader-receipt.json
5f08e6854480518fd70fcbddf0e3553f77f1e001f21b68c128660dabed804bc2  c1-noreader.stdout.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  c1-noreader.stderr.txt
5f1ee140970a4d4e3da3d9eefc55c334994497b9f7b3616ba788dff5cc9e54f6  c1-noreader-resolved-env-receipt.json
17187881b7bb1a48edf739e22d5db380309615db3ef264903ff6743ed8e0ced2  c1-noreader-resolved-env.stdout.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  c1-noreader-resolved-env.stderr.txt
```

## Generator used (scratch only, not a production change)

```python
#!/usr/bin/env python3
"""Create a bounded NoReader control; never invoke REA or execute a carrier."""
import argparse
import copy
import csv
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys

sys.dont_write_bytecode = True
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
resource.setrlimit(resource.RLIMIT_FSIZE, (1024**2, 1024**2))
parser = argparse.ArgumentParser()
parser.add_argument('--root', required=True)
a = parser.parse_args()
root = Path(a.root).resolve()
assert root == Path('/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone')
probe_rel = '.ufo/waves/round-32/before/probe/insp.json'
probe = json.loads((root / probe_rel).read_bytes())
spec = importlib.util.spec_from_file_location('r32_frozen_oracle', root / 'tools/round-32/arm64x_oracle.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
rows = list(csv.DictReader((root / 'corpus/evidence/round-32/c1/carriers.tsv').open(), delimiter='\t'))
assert len(rows) == 12
outdir = root / 'corpus/evidence/round-32/c1/envelopes'
outdir.mkdir(parents=True, exist_ok=False)
eid = 'ev_' + '0' * 64
writes = []
total = 0
print('utc_start=' + datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
print('method=committed-probe-shape + frozen-oracle expected fields; no REA invocation')
print('evidence_id=' + eid)
for row in rows:
    path = Path(row['path'])
    actual = oracle.sha256_file(str(path))
    assert actual == row['sha256'], (row['id'], actual)
    expected = oracle.expected(str(path))
    envelope = copy.deepcopy(probe)
    data = envelope['data']
    data['evidence_id'] = eid
    data['subject'].update(name=path.name, local_path=str(path), format=expected['format'], architecture=expected['architecture'])
    data['subject']['digest']['sha256'] = actual
    data['normalized_result'].update({k: v for k, v in expected.items() if k not in ('format', 'architecture')})
    assert oracle.comparable(data) == expected
    encoded = (json.dumps(envelope, separators=(',', ':'), ensure_ascii=False) + '\n').encode()
    total += len(encoded)
    assert len(encoded) <= 1024**2 and total <= 1024**2
    destination = outdir / (row['id'] + '.json')
    with destination.open('xb') as f:
        f.write(encoded)
    result = {'id': row['id'], 'carrier_sha256': actual, 'bytes': len(encoded), 'envelope_sha256': hashlib.sha256(encoded).hexdigest(), 'procedure_count': expected['procedure_count'], 'segment_count': expected['segment_count']}
    writes.append(result)
    print(json.dumps(result, sort_keys=True))
print('fixture_bytes=' + str(total))
print('utc_end=' + datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
```

## Complete control fixture diff

The following is synthetic fixture data, not admitted knowledge or source-authority prose. Exact extraction argv:

```text
git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1NoReader/clone show --format=fuller --binary --no-ext-diff f7ba512dd9244df02773378cb0f66f22abac32fb -- PROVINCE.md corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md corpus/evidence/round-32/c1/envelopes/k01.json corpus/evidence/round-32/c1/envelopes/k02.json corpus/evidence/round-32/c1/envelopes/k03.json corpus/evidence/round-32/c1/envelopes/k04.json corpus/evidence/round-32/c1/envelopes/k05.json corpus/evidence/round-32/c1/envelopes/k06.json corpus/evidence/round-32/c1/envelopes/k07.json corpus/evidence/round-32/c1/envelopes/k08.json corpus/evidence/round-32/c1/envelopes/k09.json corpus/evidence/round-32/c1/envelopes/k10.json corpus/evidence/round-32/c1/envelopes/k11.json corpus/evidence/round-32/c1/envelopes/k12.json
```

Observed exit `0`, stderr empty; full stdout follows. Diff bytes: `69722`; SHA-256 `89c165238ea5f20bdf0d89169d8322dd7231bc14922e28cc6df7b7d9707f7a07`.

```diff
commit f7ba512dd9244df02773378cb0f66f22abac32fb
Author:     ctl <ctl@local>
AuthorDate: Fri Oct 23 03:47:55 2026 -0300
Commit:     ctl <ctl@local>
CommitDate: Fri Oct 23 03:47:55 2026 -0300

    control: round-32 attempt-2 C1 NoReader oracle-only synthetic evidence

diff --git a/PROVINCE.md b/PROVINCE.md
index d9d4cf4c..5dcc7c3d 100644
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -41,6 +41,7 @@ Surfaces owned now — each verified on this host 2026-10-13.
 
 | Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |
 |---|---|---|---|
+| ARM64X hybrid PE — NoReader negative control, not admitted | `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` | Frozen-oracle reports forged without REA write mode | Synthetic `ev_0000000000000000000000000000000000000000000000000000000000000000`; control only |
 | REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `evidence/doctor/`; historical readiness probe 2026-10-13 |
 | `rea` CLI | npx cache `~/.npm/_npx/*/node_modules/rea-agents` — no `rea` on PATH; 153 commands on the 6.5.0/6.7.0 pins, 127 on 6.4.0 (historical) | `npx -y rea-agents@6.4.0 --version` → `6.4.0` (2026-10-13 receipt) | wave 01/02/03 catalogs |
 | Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 34 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
diff --git a/corpus/evidence/round-32/c1/envelopes/k01.json b/corpus/evidence/round-32/c1/envelopes/k01.json
new file mode 100644
index 00000000..c1520d7e
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k01.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k01.dll","digest":{"sha256":"2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-2f386dde73a2.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":1,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k02.json b/corpus/evidence/round-32/c1/envelopes/k02.json
new file mode 100644
index 00000000..bcd8a44c
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k02.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k02.dll","digest":{"sha256":"a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-a16ba36205f5.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":2,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k03.json b/corpus/evidence/round-32/c1/envelopes/k03.json
new file mode 100644
index 00000000..ba94717b
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k03.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k03.dll","digest":{"sha256":"0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-0291e17bd517.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":3,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k04.json b/corpus/evidence/round-32/c1/envelopes/k04.json
new file mode 100644
index 00000000..a3f176f7
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k04.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k04.dll","digest":{"sha256":"3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-3c783318ea3a.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":4,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k05.json b/corpus/evidence/round-32/c1/envelopes/k05.json
new file mode 100644
index 00000000..f43f9122
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k05.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k05.dll","digest":{"sha256":"cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-cc5c644a515b.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":1,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k06.json b/corpus/evidence/round-32/c1/envelopes/k06.json
new file mode 100644
index 00000000..479e7bc3
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k06.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k06.dll","digest":{"sha256":"6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-6c45a3ce1c3e.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":5,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k07.json b/corpus/evidence/round-32/c1/envelopes/k07.json
new file mode 100644
index 00000000..1e7871ed
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k07.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k07.dll","digest":{"sha256":"84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-84a78b7894fa.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":6,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k08.json b/corpus/evidence/round-32/c1/envelopes/k08.json
new file mode 100644
index 00000000..8b8d9661
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k08.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k08.dll","digest":{"sha256":"b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-b158eaf7c741.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":2,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k09.json b/corpus/evidence/round-32/c1/envelopes/k09.json
new file mode 100644
index 00000000..cd874004
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k09.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k09.dll","digest":{"sha256":"cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-cf0148615fce.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":7,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k10.json b/corpus/evidence/round-32/c1/envelopes/k10.json
new file mode 100644
index 00000000..f38204b2
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k10.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k10.dll","digest":{"sha256":"a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-a48499d2df92.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":3,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k11.json b/corpus/evidence/round-32/c1/envelopes/k11.json
new file mode 100644
index 00000000..d22064b6
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k11.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k11.dll","digest":{"sha256":"b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-b5e2af7f2b96.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004600","length":1536,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":8,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/evidence/round-32/c1/envelopes/k12.json b/corpus/evidence/round-32/c1/envelopes/k12.json
new file mode 100644
index 00000000..394be2bb
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k12.json
@@ -0,0 +1 @@
+{"ok":true,"data":{"evidence_id":"ev_0000000000000000000000000000000000000000000000000000000000000000","subject":{"name":"k12.dll","digest":{"sha256":"8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa"},"local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll","format":"pe","architecture":"arm64"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"pe","executable_role":"shared-library","managed":false,"native_aot_metadata":{"contract_revision":"rtr-9.1-x64-pe-read-only-v3","source_bytes":134217728,"work_units":67108864,"working_memory_bytes":67108864,"report_bytes":4194304},"architecture":"arm64","available_architectures":["arm64"],"import_mode":"ephemeral-source-immutable","pdb_observations":"program-info-v1","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","call_relationship_coverage":"function-body-call-coverage-v5","function_dossier_coverage":"observed-facets-and-call-relationships-v1","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","procedure_file_offset_resolution":"address-first-unique-target-source-mapping-v2","instruction_flow_evidence":"decoded-return-pcode-v1","instruction_references":"exact-address-incoming-v1","function_boundary_observations":"ghidra-function-boundary-limitations-v3","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"3c95bcaaac626b69803b92205bbe7643b4d9062fd3174f253a1d19a8a9977eef"},"workflow_revision":3},"digest":"f29702889a5ab0bd7d664b1cb885e541f0066ec520e8da9b68c93c3365cfee59"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-8c852d075fab.dll","image_base":"0x180000000","segments":[{"name":"Headers","start":"0x180000000","end":"0x180000400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".text","start":"0x180001000","end":"0x180002200","length":4608,"image_base":"0x180000000","address_space":"ram"},{"name":".hexpthk","start":"0x180003000","end":"0x180003200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".rdata","start":"0x180004000","end":"0x180004400","length":1024,"image_base":"0x180000000","address_space":"ram"},{"name":".data","start":"0x180005000","end":"0x180005200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".pdata","start":"0x180006000","end":"0x180006200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".a64xrm","start":"0x180007000","end":"0x180007200","length":512,"image_base":"0x180000000","address_space":"ram"},{"name":".reloc","start":"0x180008000","end":"0x180008200","length":512,"image_base":"0x180000000","address_space":"ram"}],"segment_count":8,"procedure_count":1,"string_count":3},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow.","A headless Ghidra session contains exactly one imported Program, unlike Hopper's multi-document GUI session.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Charset is reported, while a non-missing terminator cannot distinguish a present terminator from a fixed or Pascal layout.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","External functions and local thunks are distinct; procedure metadata identifies both and preserves a thunk target when Ghidra resolves one.","Memory-block end addresses are exclusive; permissions come from Ghidra MemoryBlock flags rather than inference from section names.","Only Ghidra-defined string Data is observed; packed or undefined string bytes may be absent. Completeness applies to that inventory, and an empty search does not establish that text is absent from the artifact. If an address is known, use read_bytes and xrefs to inspect bytes and references.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results."],"relationship_coverage":null,"locations":[],"evidence_links":[]},"meta":{"command":"inspect","duration":"6802ms"}}
diff --git a/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
new file mode 100644
index 00000000..67e839e5
--- /dev/null
+++ b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
@@ -0,0 +1,27 @@
+source: S099 (frozen claim label only); tools/round-32/arm64x_oracle.py; .ufo/waves/round-32/before/probe/insp.json
+verified-at: 2026-10-23; NoReader negative control, not a capability claim
+recheck: frozen tools/round-32/c1-arm64x-positive.py at this sandbox commit
+
+# Round 32 ARM64X NoReader control — not admitted
+
+These reports were forged from the committed probe shape and the frozen oracle.
+No REA write mode or carrier execution produced them. Their subject digests
+are the correct frozen carrier digests, but all evidence IDs are deliberately
+synthetic: ev_0000000000000000000000000000000000000000000000000000000000000000.
+The S099 label and Core table row exercise the frozen documentation gates;
+they do not establish source grounding, capability acquisition, or promotion.
+
+| Carrier | Deliberately forged committed envelope |
+|---|---|
+| k01 | corpus/evidence/round-32/c1/envelopes/k01.json |
+| k02 | corpus/evidence/round-32/c1/envelopes/k02.json |
+| k03 | corpus/evidence/round-32/c1/envelopes/k03.json |
+| k04 | corpus/evidence/round-32/c1/envelopes/k04.json |
+| k05 | corpus/evidence/round-32/c1/envelopes/k05.json |
+| k06 | corpus/evidence/round-32/c1/envelopes/k06.json |
+| k07 | corpus/evidence/round-32/c1/envelopes/k07.json |
+| k08 | corpus/evidence/round-32/c1/envelopes/k08.json |
+| k09 | corpus/evidence/round-32/c1/envelopes/k09.json |
+| k10 | corpus/evidence/round-32/c1/envelopes/k10.json |
+| k11 | corpus/evidence/round-32/c1/envelopes/k11.json |
+| k12 | corpus/evidence/round-32/c1/envelopes/k12.json |
```

Report: .ufo/waves/round-32/a2audit/A2C1NoReader.md
