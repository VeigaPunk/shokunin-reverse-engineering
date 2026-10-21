# MutateC1 — bounded author-side mutation probe

## Axes and scope

- **Coverage:** challenge whether all six frozen T1 verbs can be marked exercised without six bound witnesses.
- **Calibration:** preserve expected versus observed counts, raw subprocess outputs, exact source hashes, and the author-only boundary.
- **Verdict: killed.** The pristine detector passes, the forced-coverage mutant fails, and the same detector passes again after exact source restoration.
- This is distinct W2 recovery evidence. It does not claim the lost W1 seats returned, judge R22-C1/R22-C2, admit a capability, or supply outside review.
- Declared claim baseline: `7787fea4d6fd718726de92ed20759d11ce7b8b48`. The actual private clone was at `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; this synthetic probe is **not** a measurement of the frozen lane baseline.

## Mutant

Only the private clone's `.ufo/waves/round-22/tools/count-c1.py:73` changed. The behavior-bearing expression `bool(witnesses)` was replaced with `True` inside the T1 loop, so every verb becomes exercised while witness discovery and retained evidence lists remain untouched.

```diff
-        result["targets"][verb]["exercised"] = bool(witnesses)
+        result["targets"][verb]["exercised"] = True
```

The resulting mutant source at that point was:

```python
        result["targets"][verb]["exercised"] = True
        result["targets"][verb]["bound_evidence"] = witnesses[:5]
    exercised = [verb for verb in T1 if result["targets"][verb]["exercised"]]
```

No production fix or contract change was made. No sibling/lane source, index, config, MANIFEST, or state was written.

## Independent input and expected detector

The fixed synthetic Git input mentions all six T1 verbs in one eligible entry and supplies a mined `S051` row opened `2026-10-21` whose `used-by` names that entry. It retains exactly **one** cited Evidence-shaped JSON record: operation `identify_flutter_build` with a matching cited ID. There are no records for the other five operations. The expected outcome is declared independently, without importing candidate T1 values, `c1_files()`, `cases()`, or counter decisions:

- Counter exit **1**, claim `R22-C1`, `t1_exercised_count` **1**, `t1_total` **6**.
- `t1_exercised == ["identify-flutter-build"]` and per-verb flags exactly match that singleton.
- Exactly one bound-witness pair for Flutter and empty witness lists for all five other verbs.
- The existing C1 selftest must exit **0** with finding `counter_controls_clean`.

The detector exits 0 only if all these checks pass. Thus the expected raw counter exit 1 is **not** a failing pristine detector. The same detector source and argv were used in all three phases, on independent input revision `08d00b445d8dfb7176d277491b161e7fed2880d2`.

The JSON record is deliberately synthetic local-binding input, not an executed REA receipt and not authenticated Evidence. No target binary, GDB/Rizin target, device, Frida process, REA CLI/MCP runtime, or remote connection was invoked.

### Exact independent input bytes

`corpus/knowledge/independent-one-of-six.md` — SHA-256 `5c5d57f0e59b0c4f6fcd7bb1eac71bb703b713b3a1239e914f05748d5db43bdb`

```text
source: S051
verified-at: 2026-10-21
recheck: author-side synthetic control

identify-flutter-build
inspect-dart-aot
debug-with-gdb
debug-with-rizin
inspect-signal-decoders
decode-signal-recording

ev_1212121212121212121212121212121212121212121212121212121212121212 .ufo/waves/round-22/evidence/c1/independent-flutter.json
```

`corpus/SOURCES.md` — SHA-256 `f02b05496d6d62186a38b2e6f23df74cbda957c54672603414399a2b73c71828`

```text
# SOURCES
## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S051 | independent synthetic control | own-work | A | fixture | exact | one of six | mined | 2026-10-21 | on-release | corpus/knowledge/independent-one-of-six.md |
```

`.ufo/waves/round-22/evidence/c1/independent-flutter.json` — SHA-256 `0609ad8c50a99d5c8386cc2d16dd4131a55453a0ea1c9e23ac5590e60c6b42ee`

```json
{"evidence_id": "ev_1212121212121212121212121212121212121212121212121212121212121212", "operation": "identify_flutter_build"}
```

## Commands and bounds

Private-clone creation (observed exit 0, no output):

```sh
git -c core.hooksPath=/dev/null clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kaidoku-r22-MutateC1-FnIDYk/repo
```

Preparation (observed exit 0, empty stderr; exact stdout and its setup Git argv are in `MutateC1.json` under `setup`/`setup_normalized`):

```sh
python3 -I -B /tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.mutation-c1/detector.py --prepare
```

Identical bounded detector argv, once per pristine, mutant, and restored phase:

```sh
python3 -I -B /tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.mutation-c1/detector.py
```

All outer detector commands used cwd `/tmp/kaidoku-r22-MutateC1-FnIDYk/repo`, capture-only stdout/stderr, and a 180-second timeout. Inside the detector, the independent counter has a 90-second timeout and the existing selftest a 120-second timeout. Their exact argv are:

```sh
/usr/bin/python3 -I -B /tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.ufo/waves/round-22/tools/count-c1.py --root /tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.mutation-c1/input --rev 08d00b445d8dfb7176d277491b161e7fed2880d2
/usr/bin/python3 -I -B /tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.ufo/waves/round-22/tools/count-c1.py --selftest
```

For both child invocations, `TMPDIR=/tmp/kaidoku-r22-MutateC1-FnIDYk/repo/.mutation-c1/tmp` keeps selftest-generated Git fixtures inside the private clone. `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.hooksPath`, and `GIT_CONFIG_VALUE_0=/dev/null` disable inherited Git hooks. Preparation also disables hooks for each fixture Git command and supplies a synthetic commit identity only in the scratch fixture.

## Observed results

| Source phase | Detector exit | Independent counter exit | Exercised count | Existing selftest exit/finding | Cases matching expectations |
|---|---:|---:|---:|---|---:|
| pristine | 0 | 1 | 1/6 | 0 / `counter_controls_clean` | 6/6 |
| mutant | 1 | 0 | 6/6 | 1 / `counter_controls_failed` | 1/6 |
| restored | 0 | 1 | 1/6 | 0 / `counter_controls_clean` | 6/6 |

The mutant's independent output claimed all six exercised, while five `bound_evidence` arrays were still empty. Its failed detector checks were `counter_exit_is_1`, `count_is_1`, `exercised_list_is_flutter_only`, `per_verb_flags_exact`, and `existing_controls_clean`. The bound-witness check itself still passed, isolating the forced exercised flags as the introduced defect.

For every phase the independent counter, outer detector, existing selftest, and all six selftest case subprocesses had empty stderr. Their complete stdout strings, exact argv, exit codes, case findings, and generated temporary paths are retained without abbreviation in the same-name JSON attachment (`runs.<phase>.stdout` is the exact outer stdout, containing child records). The following table is a projection of those actual selftest results, not substituted stdout:

| Existing selftest case | Expected counter exit/count | Pristine exit/count/pass | Mutant exit/count/pass | Restored exit/count/pass |
|---|---|---|---|---|
| `all_six` | 0 / 6 | 0 / 6 / true | 0 / 6 / true | 0 / 6 / true |
| `missing_source` | 1 / 0 | 1 / 0 / true | 0 / 6 / false | 1 / 0 / true |
| `refusal` | 1 / 0 | 1 / 0 / true | 0 / 6 / false | 1 / 0 / true |
| `split_record` | 1 / 0 | 1 / 0 / true | 0 / 6 / false | 1 / 0 / true |
| `uncited_path` | 1 / 0 | 1 / 0 / true | 0 / 6 / false | 1 / 0 / true |
| `duplicate_json` | 1 / 0 | 1 / 0 / true | 0 / 6 / false | 1 / 0 / true |

The existing `--selftest` is present and runnable; there is no missing-selftest finding. Its five negative controls also kill this mutant. [INFERENCE] The existing six cases declare only 0/6 and 6/6 expected counts; the independent fixture adds an explicit intermediate 1/6 assertion without changing the contract.

## Restoration and calibration limit

| Bytes | SHA-256 |
|---|---|
| Pristine cloned counter | `5fbc68684a1b6d8aa1a29fbd42e3074c9ca6674b69e83d061b0a49d5f947dd61` |
| Mutated cloned counter | `05f2143cb11a3b88481309b133fcc84eeed5731162adabbcd60148c0c6a6485c` |
| Restored cloned counter | `5fbc68684a1b6d8aa1a29fbd42e3074c9ca6674b69e83d061b0a49d5f947dd61` |
| Unchanged detector source, all phases | `8e0bdd65bbd84ade21637418474cdd6df3832edc76b07e3b27befc2ed013f59f` |

The one edited line was restored using the exact original text. The restored counter SHA-256 equals the pre-mutation counter SHA-256, the edit tool returned the original snapshot tag, and the restored detector passed with the original 1/6 result. No mutation remained in the private source.

A separate post-restoration `sha256sum` observed the restored clone hash above and a **different concurrent lane** target hash, `71ce219814e28530d75f58708468a1b8192449144b9450945a881a600700c2cd`. The lane target initially had the tested `5fbc68684a1b6d8aa1a29fbd42e3074c9ca6674b69e83d061b0a49d5f947dd61` hash. A read showed the lane had independently moved to a rebuilt per-target dictionary (129 lines rather than the tested 115). This seat did not write or revert that lane change. **The killed-mutant result is pinned to the tested private snapshot; the later lane version is untested here.**

Fixture helper/catalog hashes are retained in the attachment. The same fixed independent input revision and detector hash were observed in every phase. No additional mutation or re-probe of the moving lane was performed.

## Tooling, blockers, and hand-off

- Existing tools: `Python 3.14.8` and `git version 2.56.0`, observed via `python3 --version` and `git --version`.
- Installs/updates: **none**; no package-manager transaction, service restart, or tooling-channel change.
- Blockers for the assigned snapshot: **none**. The only limit is the explicitly untested later lane source; no domain/provider capability or outside admission is inferred.
- Lane write scope is limited to this report and `MutateC1.json`. Production files and round state remain integration-owner work.
- Full detector source follows so the private control is retained even when temporary directories expire. No integration or production test change was made by this seat.

## Retained detector source

```python
#!/usr/bin/env python3
"""Author-side one-of-six C1 control, independent of candidate fixture builders."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / '.mutation-c1'
FIXTURE = SCRATCH / 'input'
COUNTER = ROOT / '.ufo/waves/round-22/tools/count-c1.py'
VERBS = (
    'identify-flutter-build', 'inspect-dart-aot', 'debug-with-gdb',
    'debug-with-rizin', 'inspect-signal-decoders', 'decode-signal-recording',
)
DEPS = (
    '.ufo/waves/round-20/tools/verb-coverage.py',
    '.ufo/waves/round-21/tools/verb-coverage.py',
    '.ufo/waves/round-20/verify/round20/verb-coverage.json',
)
ENTRY = 'corpus/knowledge/independent-one-of-six.md'
RECEIPT = '.ufo/waves/round-22/evidence/c1/independent-flutter.json'
EVIDENCE_ID = 'ev_' + '12' * 32


def call(argv, timeout=90, env=None):
    proc = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True,
                          text=True, timeout=timeout, check=False)
    return {'argv': argv, 'exit': proc.returncode,
            'stdout': proc.stdout, 'stderr': proc.stderr}


def git(*args):
    argv = ['git', '-c', 'core.hooksPath=/dev/null', '-C', str(FIXTURE), *args]
    row = call(argv)
    if row['exit'] != 0:
        raise RuntimeError(json.dumps(row, sort_keys=True))
    return row


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    FIXTURE.mkdir(parents=True)
    logs = [git('init', '-q')]
    for relative in DEPS:
        target = FIXTURE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    entry = FIXTURE / ENTRY
    entry.parent.mkdir(parents=True, exist_ok=True)
    entry.write_text(
        'source: S051\nverified-at: 2026-10-21\nrecheck: author-side synthetic control\n\n'
        + '\n'.join(VERBS) + '\n\n'
        + EVIDENCE_ID + ' ' + RECEIPT + '\n', encoding='utf-8')
    (FIXTURE / 'corpus/SOURCES.md').write_text(
        '# SOURCES\n## Registry\n'
        '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
        '|---|---|---|---|---|---|---|---|---|---|---|\n'
        '| S051 | independent synthetic control | own-work | A | fixture | exact | one of six | mined | 2026-10-21 | on-release | '
        + ENTRY + ' |\n', encoding='utf-8')
    receipt = FIXTURE / RECEIPT
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps({'evidence_id': EVIDENCE_ID,
                                   'operation': 'identify_flutter_build'},
                                  sort_keys=True) + '\n', encoding='utf-8')
    logs.append(git('add', '--all'))
    logs.append(git('-c', 'user.name=MutateC1 fixture',
                    '-c', 'user.email=mutate-c1@invalid.local',
                    'commit', '-qm', 'Independent one-of-six C1 input'))
    revision = git('rev-parse', 'HEAD')
    logs.append(revision)
    print(json.dumps({'setup_commands': logs, 'fixture_rev': revision['stdout'].strip(),
                      'fixture_files': {
                          rel: {'sha256': sha(FIXTURE / rel),
                                'text': (FIXTURE / rel).read_text(encoding='utf-8')}
                          for rel in (ENTRY, 'corpus/SOURCES.md', RECEIPT)},
                      'dependency_hashes': {rel: sha(FIXTURE / rel) for rel in DEPS}},
                     sort_keys=True))
    return 0


def detect():
    revision = git('rev-parse', 'HEAD')['stdout'].strip()
    env = dict(os.environ)
    env['TMPDIR'] = str(SCRATCH / 'tmp')
    Path(env['TMPDIR']).mkdir(exist_ok=True)
    env['GIT_CONFIG_COUNT'] = '1'
    env['GIT_CONFIG_KEY_0'] = 'core.hooksPath'
    env['GIT_CONFIG_VALUE_0'] = '/dev/null'
    counter = call([sys.executable, '-I', '-B', str(COUNTER), '--root',
                    str(FIXTURE), '--rev', revision], env=env)
    try:
        data = json.loads(counter['stdout'])
    except ValueError:
        data = {}
    expected_flags = {verb: verb == 'identify-flutter-build' for verb in VERBS}
    actual_flags = {verb: data.get('targets', {}).get(verb, {}).get('exercised')
                    for verb in VERBS}
    actual_bounds = {verb: data.get('targets', {}).get(verb, {}).get('bound_evidence')
                     for verb in VERBS}
    expected_bounds = {verb: ([[EVIDENCE_ID, RECEIPT]]
                              if verb == 'identify-flutter-build' else [])
                       for verb in VERBS}
    checks = {
        'counter_exit_is_1': counter['exit'] == 1,
        'claim_is_R22_C1': data.get('claim') == 'R22-C1',
        'count_is_1': data.get('t1_exercised_count') == 1,
        'total_is_6': data.get('t1_total') == 6,
        'exercised_list_is_flutter_only': data.get('t1_exercised') == ['identify-flutter-build'],
        'per_verb_flags_exact': actual_flags == expected_flags,
        'bound_witnesses_exact': actual_bounds == expected_bounds,
    }
    existing = call([sys.executable, '-I', '-B', str(COUNTER), '--selftest'],
                    timeout=120, env=env)
    try:
        selftest = json.loads(existing['stdout'])
    except ValueError:
        selftest = {}
    checks['existing_controls_clean'] = (
        existing['exit'] == 0 and selftest.get('finding') == 'counter_controls_clean')
    result = {
        'scope': 'author-side synthetic counter control, not outside admission',
        'counter_sha256': sha(COUNTER),
        'fixture_rev': revision,
        'detector_sha256': sha(Path(__file__)),
        'expected': {'counter_exit': 1, 'count': 1, 'total': 6,
                     'exercised': ['identify-flutter-build'],
                     'per_verb_flags': expected_flags, 'bound_evidence': expected_bounds,
                     'existing_selftest_exit': 0},
        'checks': checks,
        'independent_counter': counter,
        'existing_selftest': existing,
        'clean': all(checks.values()),
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result['clean'] else 1


if __name__ == '__main__':
    raise SystemExit(prepare() if sys.argv[1:] == ['--prepare'] else detect())
```
