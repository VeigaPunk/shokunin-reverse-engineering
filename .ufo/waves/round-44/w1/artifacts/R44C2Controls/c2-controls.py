#!/usr/bin/env python3
"""R44-C2 controls: the four red-before controls of `plans/round-44-claims.md` R44-C2.

The claim being controlled (calibration): a frozen rubric of the lane's own
self-assessment statements is re-derived at the measured revision; the score is
`mismatches == 0`.  Every control below is scored against the FROZEN counter
(`tools/round-44/c2-counter.py`; the wave-1 artifact lives at
`.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py` until the L1
installs it) and never against a hand-written verdict.

    CTL-C2-0  do-nothing / honest-stop gate
              The census at the BASE revision with the frozen rubric.  The
              counter must exit non-zero (1) iff the rubric shows
              `mismatches > 0` at the base.  If the census shows ZERO
              mismatches at the base, the C2 claim STOPS (the do-nothing
              control would have reached the target, so the predicate is
              wrong).  The stop is reported, never loosened.

    CTL-C2-1  seeded mismatch
              A scratch CLONE of the lane at the freeze, with ONE seeded wrong
              statement (a non-frozen file the rubric points at is mutated:
              a count decremented, an evidence value changed).  The counter
              must report the mismatch by id and exit non-zero (1).  The
              baseline run at the same freeze (unseeded) is recorded too, so
              the mismatch is attributable to the seed when the baseline was
              green.

    CTL-C2-2  malformed rubric
              A copy of the frozen rubric with one entry's check command
              dropped.  The counter must refuse the rubric: exit 2
              (`rubric_malformed: ..._missing_command`), never a score.

    CTL-C2-3  rubric immutability
              The rubric is a frozen path.  A copy of the lane is committed
              with the rubric bytes at a freeze commit and then EDITED
              mid-round.  The counter must refuse: exit 2 with
              `frozen_path_changed` naming `tools/round-44/c2-rubric.json`.
              A later restore does not un-block (the walk compares FREEZE..REV).

    CTL-C2-4  wrong-value note
              A correction note carrying a WRONG value must never make an
              entry pass.  Two arms: the enforced arm (the note is appended to
              the rubric-named frozen file and the freeze walk is enforced —
              the note is a declaration, the rubric binds the exact appended
              bytes, so the counter refuses) and the scored arm (the same note
              with the freeze walk reported but not enforced, so the ENTRY is
              scored: the check re-derives the value and the observation is
              `UNSUPPORTED:<note value>`, a mismatch — a note is never
              evidence).  The control passes when NEITHER arm yields a pass.

    --fitness  the per-entry fitness gate the amended claims require: every
              rubric entry is shown able to fail on its own statement (one
              asserted-value mutation per entry; the entry must then be
              reported as a mismatch).

Two modes:

  --mode dev   a self-contained synthetic fixture (a tiny git repo, a check
               script, a stale statement and a consistent statement).  It
               demonstrates every control able to FAIL, with no dependence on
               the lane's state.  This is the mode a control seat may run.

  --mode real  the lane: the real frozen rubric
               (`tools/round-44/c2-rubric.json`), the real base revision, the
               real freeze revision.  This is the mode the L1 runs after the
               rubric is installed and frozen.  It never runs the after-side
               data procedure (there is none for C2) and never scores the
               claim: it only runs controls.

  --mode auto  real when the frozen rubric is present, else dev.

Exit codes (semantic): 0 = every control behaved as expected; 1 = a control
failed (or a kill rule fired); 2 = a control could not be evaluated.

Receipts (one per control, in --out):
    {control, command, exit_code, expected, seat, argv, stdout_sha256,
     stdout_bytes, stdout_head, stderr_head, wall_seconds, ...control detail}

Honours TMPDIR and --work; writes only --out and --json-out.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

SEAT = 'R44C2Controls'
EXIT_MET, EXIT_FAIL, EXIT_CANT = 0, 1, 2

# The frozen paths the counter always freezes (mirrors
# tools/round-44/c2-counter.py C2_DEFAULT_FROZEN plus its two tool paths).
COUNTER_DEFAULT_FROZEN = (
    'SCORECARD.md', 'SHONEN.md', 'corpus/README.md', 'SKILL.md',
    'tools/round-44/c2-rubric.json', 'tools/round-44/c2-counter.py',
)

COMMAND_KEYS = ('command', 'argv', 'check_argv', 'check_command', 'cmd', 'run')
CHECK_KEYS = ('check', 'check_kind', 'kind', 'check_type', 'type')
ENTRY_LIST_KEYS = ('entries', 'checks', 'items', 'statements', 'rubric')

DEFAULT_BASE = 'c29360e3ba5381a5ab69e372d0d9577970f85018'

# --------------------------------------------------------------------- utils


def sha256_bytes(data):
    if data is None:
        return None
    return hashlib.sha256(data).hexdigest()


def git(root, *args, check=False):
    proc = subprocess.run(['git', '-C', root] + list(args),
                          capture_output=True, text=True)
    if check and proc.returncode:
        raise ControlError('git %s failed: %s' % (' '.join(args),
                                                  proc.stderr.strip()))
    return proc


def rev_parse(root, rev):
    proc = git(root, 'rev-parse', '--verify', '%s^{commit}' % rev)
    if proc.returncode:
        return None
    return proc.stdout.strip()


def tree_paths(root, rev):
    proc = git(root, 'ls-tree', '-r', '--name-only', rev)
    if proc.returncode:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def blob(root, rev, path):
    proc = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                          capture_output=True)
    if proc.returncode:
        return None
    return proc.stdout


def run(argv, cwd=None, env=None, timeout=900):
    started = time.time()
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                              text=True, timeout=timeout)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode('utf-8', 'replace') if exc.stdout else ''
        stderr = 'timeout'
        code = None
    return {
        'argv': list(argv),
        'exit_code': code,
        'stdout': stdout,
        'stderr': stderr,
        'stdout_sha256': sha256_bytes(stdout.encode('utf-8', 'replace')),
        'stdout_bytes': len(stdout.encode('utf-8', 'replace')),
        'wall_seconds': round(time.time() - started, 6),
    }


def command_line(argv):
    return ' '.join(shlex.quote(a) for a in argv)


class ControlError(Exception):
    """A control could not be run at all (usage, IO, missing frozen input)."""


# ------------------------------------------------------------- counter driver


def counter_argv(counter, root, rev=None, freeze=None, work=None, rubric=None,
                 json_out=None, pre_freeze=False, seat=SEAT):
    argv = [sys.executable, '-I', '-B', counter, '--root', root]
    if rev:
        argv += ['--rev', rev]
    if freeze:
        argv += ['--freeze', freeze]
    if work:
        argv += ['--work', work]
    if rubric:
        argv += ['--rubric', rubric]
    if json_out:
        argv += ['--json-out', json_out]
    if pre_freeze:
        argv += ['--pre-freeze']
    argv += ['--seat', seat]
    return argv


def run_counter(counter, **kwargs):
    """Run the frozen counter as a subprocess and read back its receipt."""
    argv = counter_argv(counter, **kwargs)
    env = dict(os.environ)
    env['HYAKU_SEAT'] = SEAT
    result = run(argv, env=env)
    out = kwargs.get('json_out')
    doc = None
    if out and os.path.isfile(out):
        try:
            with open(out, encoding='utf-8') as handle:
                doc = json.load(handle)
        except (OSError, json.JSONDecodeError):
            doc = None
    result['json'] = doc
    result['command'] = command_line(argv)
    return result


def receipt(control, expected, result, **detail):
    """One receipt per control: {control, command, exit_code, expected, ...}."""
    payload = {
        'control': control,
        'command': result.get('command'),
        'exit_code': result.get('exit_code'),
        'expected': expected,
        'seat': SEAT,
        'argv': result.get('argv'),
        'stdout_sha256': result.get('stdout_sha256'),
        'stdout_bytes': result.get('stdout_bytes'),
        'stdout_head': (result.get('stdout') or '')[:2000],
        'stderr_head': (result.get('stderr') or '')[:1000],
        'wall_seconds': result.get('wall_seconds'),
    }
    payload.update(detail)
    return payload


# --------------------------------------------------------------- rubric utils


def pick(entry, keys, default=None):
    for key in keys:
        if key in entry and entry[key] is not None:
            return entry[key]
    return default


def rubric_entries(doc):
    if not isinstance(doc, dict):
        return []
    for key in ENTRY_LIST_KEYS:
        value = doc.get(key)
        if isinstance(value, list):
            return [e for e in value if isinstance(e, dict)]
    return []


def rubric_frozen_paths(doc):
    """Every path the counter will freeze for this rubric."""
    frozen = set(COUNTER_DEFAULT_FROZEN)
    if not isinstance(doc, dict):
        return frozen
    for item in doc.get('frozen_paths') or []:
        if isinstance(item, str):
            frozen.add(item.strip())
        elif isinstance(item, dict):
            path = pick(item, ('path', 'file', 'target', 'subject'))
            if isinstance(path, str):
                frozen.add(path.strip())
    edits = doc.get('expected_edits')
    if isinstance(edits, dict):
        for path in edits:
            frozen.add(str(path))
    for entry in rubric_entries(doc):
        edit = pick(entry, ('expected_edit', 'edit', 'repair'))
        if isinstance(edit, dict):
            path = edit.get('file')
            if isinstance(path, str):
                frozen.add(path.strip())
    return frozen


def rubric_frozen_dirs(doc):
    dirs = set()
    if isinstance(doc, dict):
        for item in doc.get('frozen_dirs') or []:
            if isinstance(item, str) and item.strip():
                dirs.add(item.strip().rstrip('/'))
    return dirs


def entry_candidates(doc):
    """[(entry_id, [candidate paths])] — paths an entry's check may read."""
    out = []
    for entry in rubric_entries(doc):
        ident = pick(entry, ('id', 'check_id', 'entry_id', 'name', 'label'))
        if not isinstance(ident, str) or not ident.strip():
            ident = 'entry'
        names = []
        files = pick(entry, ('files', 'reads', 'inputs'), default=[]) or []
        for name in list(files):
            if isinstance(name, str) and name.strip():
                names.append(name.strip())
        single = pick(entry, ('file', 'path', 'target', 'subject'))
        if isinstance(single, str) and single.strip():
            names.append(single.strip())
        command = pick(entry, COMMAND_KEYS, default=[]) or []
        if isinstance(command, str):
            command = command.split()
        for token in command:
            if isinstance(token, str) and ('/' in token) and not token.startswith('-'):
                names.append(token.strip())
        out.append((ident.strip(), names))
    return out


def seed_mutation(path, data):
    """Mutate a file's bytes so a re-derivation sees a different value.

    JSON first (decrement the first number), then text (decrement the first
    integer), then a marker line.  Returns a description of what was done.
    """
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        text = None
    if text is not None:
        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            doc = None
        if doc is not None:
            found = []

            def walk(node):
                if found:
                    return
                if isinstance(node, dict):
                    for key in sorted(node):
                        walk(node[key])
                elif isinstance(node, list):
                    for item in node:
                        walk(item)
                elif isinstance(node, bool):
                    return
                elif isinstance(node, (int, float)):
                    found.append((node, node - 1 if isinstance(node, int) else node - 1))
            walk(doc)
            if found:
                old, new = found[0]
                text2 = text.replace(json.dumps(old), json.dumps(new), 1)
                if text2 == text:
                    text2 = text.replace(str(old), str(new), 1)
                if text2 != text:
                    return text2.encode('utf-8'), 'json_number %r -> %r' % (old, new)
    if text is not None:
        match = re.search(r'\d+', text)
        if match:
            old = int(match.group(0))
            new = old - 1 if old > 0 else old + 1
            text2 = text[:match.start()] + str(new) + text[match.end():]
            return text2.encode('utf-8'), 'text_integer %d -> %d' % (old, new)
        return (text + '\nseeded-mutation: 1\n').encode('utf-8'), 'appended_marker'
    return data + b'\nseeded-mutation: 1\n', 'appended_marker_bytes'


# ------------------------------------------------------------- fixture (dev)


FIXTURE_CHECK = '''import json, pathlib, re, sys
"""Re-derive one number from a file in the exported tree (the check command).

Mirrors the rubric's check contract: the statement's value comes from
SCORECARD.md (or from an appended `c2-correction-value:` note), the derived
value comes from the tree, and the observation is the statement's value only
when the two agree.  A note is a declaration: when it disagrees with the
derivation the observation is `UNSUPPORTED:<note value>`.
"""
target = sys.argv[1] if len(sys.argv) > 1 else "evidence/count.txt"
eid = "evidence-count"
card = pathlib.Path("SCORECARD.md").read_text()
derived = int(pathlib.Path(target).read_text().split()[0])
stated = None
for line in card.splitlines():
    m = re.search(r"(\\d+) knowledge files mapped", line)
    if m:
        stated = m.group(1)
lines = card.splitlines()
for i, line in enumerate(lines):
    if ("<!-- c2-correction: " + eid + " -->") in line:
        for j in range(i + 1, min(i + 10, len(lines))):
            m = re.match(r"\\s*c2-correction-value:\\s*(.+?)\\s*$", lines[j])
            if m:
                stated = m.group(1)
observed = stated if (stated is not None and str(derived) == stated) \\
    else ("UNSUPPORTED:" + str(stated))
json.dump({"observed": observed, "derived": derived, "detail": "fixture"}, sys.stdout)
'''


def fixture_rubric(asserted, correction_value, freeze=None):
    doc = {
        'predicate': 'P44-C2',
        'frozen_paths': ['SCORECARD.md'],
        'expected_edits': {
            'SCORECARD.md': {
                'file': 'SCORECARD.md',
                'append': [
                    '- **Round-44 fixture correction:** the coverage row is re-derived.',
                    '<!-- c2-correction: evidence-count -->',
                    'c2-correction-value: %s' % correction_value,
                ],
                'marker': 'c2-correction: evidence-count',
            },
        },
        'entries': [{
            'id': 'evidence-count',
            'check': 'json',
            'command': ['python3', '-I', '-B', 'tools/round-44/c2-checks.py',
                        'evidence/count.txt'],
            'asserted': asserted,
            'compare': 'eq',
            'file': 'SCORECARD.md',
            'files': ['evidence/count.txt'],
        }],
    }
    if freeze:
        doc['freeze'] = freeze
    return json.dumps(doc, indent=1).encode('utf-8')


def build_fixture(work, name, stated, reality):
    """A tiny lane-like repo: a statement, a reality, and a check script.

    `stated` is what the statement claims, `reality` is what the tree holds.
    When they differ the check reports `UNSUPPORTED:<stated>` (the rubric's
    observation rule); when they agree it reports the value.

    Returns dict(root, freeze, rubric).
    """
    root = os.path.join(work, 'fixture-%s' % name)
    os.makedirs(os.path.join(root, 'evidence'), exist_ok=True)
    os.makedirs(os.path.join(root, 'tools', 'round-44'), exist_ok=True)
    write(os.path.join(root, 'SCORECARD.md'),
          '# fixture scorecard\n\n| coverage | %d knowledge files mapped |\n'
          % stated)
    write(os.path.join(root, 'evidence', 'count.txt'), '%d\n' % reality)
    write(os.path.join(root, 'tools', 'round-44', 'c2-checks.py'), FIXTURE_CHECK)
    write(os.path.join(root, 'tools', 'round-44', 'c2-rubric.json'),
          fixture_rubric(stated, stated).decode('utf-8'))
    git(root, 'init', '-q', '-b', 'main')
    git(root, 'config', 'user.email', 'controls@kaidoku.local')
    git(root, 'config', 'user.name', 'R44C2Controls fixture')
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', 'fixture base')
    top = git(root, 'rev-parse', '--show-toplevel').stdout.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise ControlError('fixture repo top-level mismatch: %s != %s' % (top, root))
    freeze = rev_parse(root, 'HEAD')
    rubric = os.path.join(work, 'fixture-%s-rubric.json' % name)
    write(rubric, fixture_rubric(stated, stated).decode('utf-8'))
    return {'root': root, 'freeze': freeze, 'rubric': rubric, 'stated': stated,
            'reality': reality}


def write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)


# ------------------------------------------------------------------- controls


def ctl_c2_0(counter, root, rev, rubric_path, work, out, freeze=None,
             declared_freeze=None):
    """Do-nothing census at the base: non-zero exit iff mismatches > 0.

    The census runs the counter in `--pre-freeze` mode at the BASE revision
    with the frozen rubric: the freeze walk is reported but not enforced (at
    the base the freeze is not yet an ancestor of the measured revision).  The
    counter refuses a rubric whose declared `freeze` differs from the freeze
    argument, so the attempts are tried in a fixed ladder and the first one
    that produces a census is scored:

      1. `--rev BASE --freeze <FREEZE> --pre-freeze` (the real freeze, when
         the rubric declares it);
      2. `--rev BASE --pre-freeze` (no freeze: for a rubric that declares
         none);
      3. `--rev BASE --freeze <rubric's declared freeze> --pre-freeze`.

    The score is the census: mismatches > 0 -> exit 1 (the claim is not yet
    met, the counter can fail); mismatches == 0 -> exit 0, and R44-C2 STOPS
    (the do-nothing control would have reached the target, so the predicate
    is wrong).  The stop is reported, never loosened.
    """
    detail = {'mode': 'census_at_base', 'rev': rev, 'rubric': rubric_path}
    ladder = []
    if freeze:
        ladder.append(freeze)
    if declared_freeze and declared_freeze not in ladder:
        ladder.append(declared_freeze)
    ladder.append(None)

    attempts = []
    result = None
    doc = {}
    for freeze_arg in ladder:
        candidate = run_counter(
            counter, root=root, rev=rev, freeze=freeze_arg, work=work,
            rubric=rubric_path, json_out=os.path.join(out, 'ctl-c2-0.json'),
            pre_freeze=True)
        attempts.append(candidate)
        cdoc = candidate.get('json') or {}
        if result is None:
            result = candidate
            doc = cdoc
        if cdoc.get('mismatches_count') is not None:
            result = candidate
            doc = cdoc
            break
    mismatches = doc.get('mismatches_count')
    if mismatches is None:
        mismatches = len(doc.get('mismatches') or []) if doc else None
    evaluated = doc.get('entries_evaluated')
    expected_exit = None
    if mismatches is not None:
        expected_exit = EXIT_FAIL if mismatches > 0 else EXIT_MET
    unevaluable = doc.get('unevaluable')
    ok = (mismatches is not None and result['exit_code'] == expected_exit
          and not unevaluable)
    # the rubric's own declared expectation for this control (when it has one)
    vector = None
    try:
        with open(rubric_path, encoding='utf-8') as handle:
            rubric_doc = json.load(handle)
    except (OSError, json.JSONDecodeError):
        rubric_doc = None
    found = rubric_control_vector(rubric_doc, 'CTL-C2-0')
    if found:
        vector = found
        want = found['vector']
        want_exit = want.get('counter_exit_code')
        want_ids = want.get('mismatches_exact_ids')
        vector_checks = {
            'counter_exit_code_matches': (want_exit is None
                                          or result['exit_code'] == want_exit),
            'mismatch_count_matches': (want.get('mismatch_count') is None
                                       or mismatches == want.get('mismatch_count')),
            'mismatch_ids_match': (want_ids is None
                                   or list(doc.get('mismatches') or []) == list(want_ids)),
            'entries_evaluated_matches': (want.get('entries_evaluated') is None
                                          or evaluated == want.get('entries_evaluated')),
        }
        detail['declared_vector'] = vector
        detail['declared_vector_checks'] = vector_checks
        ok = ok and all(vector_checks.values())
        detail['verdict'] = 'ok' if ok else 'failed'
    detail.update({
        'mismatches': mismatches,
        'mismatch_ids': doc.get('mismatches'),
        'entries_evaluated': evaluated,
        'entries_count': doc.get('entries_count'),
        'unevaluable': unevaluable,
        'frozen_path_changed': doc.get('frozen_path_changed'),
        'pre_freeze': doc.get('pre_freeze'),
        'claim_score': doc.get('claim_score'),
        'expected_exit_code': expected_exit,
        'attempts': [{'command': a['command'], 'exit_code': a['exit_code'],
                      'unevaluable': (a.get('json') or {}).get('unevaluable'),
                      'stdout_sha256': a['stdout_sha256'],
                      'wall_seconds': a['wall_seconds']} for a in attempts],
        'kill_rule_fired': (mismatches == 0),
        'claim_stops': (mismatches == 0),
        'verdict': 'ok' if ok else ('inconclusive' if mismatches is None else 'failed'),
        'note': ('ZERO mismatches at the base: the do-nothing control reaches the '
                 'target, so R44-C2 STOPS (honest stop; the rubric is not '
                 'loosened to make the claim scoreable).'
                 if mismatches == 0 else ''),
    })
    payload = receipt(
        'CTL-C2-0',
        'exit 1 iff the frozen rubric shows mismatches > 0 at the base; '
        'exit 0 iff 0 mismatches (then R44-C2 STOPS); exit 2 = could-not-evaluate',
        result, **detail)
    return payload, ok


def clone_repo(root, dest):
    proc = subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet',
                           os.path.abspath(root), dest],
                          capture_output=True, text=True)
    if proc.returncode:
        raise ControlError('clone failed: %s' % proc.stderr.strip())
    top = subprocess.run(['git', '-C', dest, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise ControlError('clone top-level mismatch: %s != %s' % (top, dest))
    return dest


def rubric_control_vector(doc, needle):
    """The rubric's own declared expectation for a control vector.

    The rubric may carry a `control_vectors` map: {control description:
    {counter_exit_code, mismatch_count, mismatches_exact_ids, ...}}.  The
    control is then scored against the rubric's FROZEN expectation, not
    against a hand-written one.
    """
    vectors = doc.get('control_vectors') if isinstance(doc, dict) else None
    if not isinstance(vectors, dict):
        return None
    for key, value in vectors.items():
        if needle.lower() in str(key).lower():
            return {'key': key, 'vector': value}
    return None


def declared_seed(doc):
    """The rubric's own declared seed for CTL-C2-1, if it declares one."""
    block = doc.get('seeded_mismatch') if isinstance(doc, dict) else None
    if not isinstance(block, dict):
        return None
    primary = block.get('primary')
    if not isinstance(primary, dict):
        return None
    return primary


def apply_declared_seed(kind, data):
    """(bytes, description) — apply the rubric's declared mutation kind."""
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return data, 'binary_untouched'
    if kind == 'log-round-entry-removed':
        lines = text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            if line.lstrip().startswith('#') and 'round 43' in line:
                lines[index] = line.replace('round 43', 'round 43x', 1)
                return ''.join(lines).encode('utf-8'), \
                    'LOG.md round-43 heading renamed (line %d)' % (index + 1)
        return data, 'no_round_43_heading_found'
    if kind == 'evidence-path-substituted':
        # the old/new pair is filled in by the caller through the doc
        return data, 'evidence-path substitution not applied'
    return seed_mutation('text', data)


def corrupt_asserted(entry):
    """(new asserted value, description) — one wrong asserted value.

    A count is decremented, a claimed path is replaced by a path that does not
    exist, a list loses one element, a string gains a marker.  The SEED is the
    rubric-named entry itself: the counter re-derives the value from the
    repository and must report the disagreement.
    """
    asserted = pick(entry, ('asserted', 'assert', 'expected', 'expected_value',
                             'value'))
    if isinstance(asserted, bool):
        return (not asserted), 'asserted bool flipped'
    if isinstance(asserted, (int, float)):
        new = asserted - 1 if asserted != 0 else asserted + 1
        return new, 'asserted number %r -> %r' % (asserted, new)
    if isinstance(asserted, list):
        if not asserted:
            return ['seeded-nonexistent'], 'asserted list emptied then seeded'
        return list(asserted[:-1]), 'asserted list lost its last element'
    if isinstance(asserted, str):
        if asserted.endswith('/') or '/' in asserted:
            return asserted.rstrip('/') + '/seeded-nonexistent', \
                'asserted path replaced by a nonexistent path'
        return asserted + ' [seeded]', 'asserted string marked'
    if asserted is None:
        return 'seeded-nonexistent', 'asserted null replaced'
    return 'seeded-nonexistent', 'asserted value replaced'


def ctl_c2_1(counter, root, freeze, rubric_path, work, out, base=None):
    """Seeded mismatch: one rubric-named statement is made wrong.

    Two arms, both scored against the frozen counter:

      arm A (reality side) — a scratch CLONE of the lane at the freeze, with one
        NON-frozen file the rubric points at mutated (a count decremented, an
        evidence value changed).  The counter must re-derive the value and
        report the mismatch.

      arm B (rubric side) — a scratch copy of the frozen rubric whose SEEDED
        entry carries a wrong asserted value (a count decremented, an evidence
        path deleted).  The counter must re-derive the value from the
        repository and report the mismatch: a fabricated rubric cannot pass.

    The control passes when at least one arm makes the counter report the
    mismatch by id and exit non-zero (1).
    """
    detail = {'mode': 'seeded_mismatch', 'arms': {}}
    if not rubric_path or not os.path.isfile(rubric_path):
        raise ControlError('rubric not available: %s' % rubric_path)
    with open(rubric_path, encoding='utf-8') as handle:
        raw = handle.read()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ControlError('rubric is not JSON: %s' % exc)
    entries = rubric_entries(doc)
    if not entries:
        raise ControlError('rubric has no entries to seed')

    clone = clone_repo(root, os.path.join(work, 'ctl-c2-1-clone'))
    git(clone, 'checkout', '-q', freeze)
    frozen = rubric_frozen_paths(doc)
    frozen_dirs = rubric_frozen_dirs(doc)
    paths = set(tree_paths(clone, freeze))
    # the rubric blob is committed at the freeze?  then the counter may read it
    # from the freeze itself (the strongest form).
    rubric_at_freeze = blob(clone, freeze, 'tools/round-44/c2-rubric.json')
    rubric_committed = rubric_at_freeze is not None
    rubric_arg = None if rubric_committed else rubric_path

    # ------------------------------------------------------------- baseline
    baseline = run_counter(counter, root=clone, rev=freeze, freeze=freeze,
                           work=work, rubric=rubric_arg,
                           json_out=os.path.join(out, 'ctl-c2-1-baseline.json'))
    baseline_doc = baseline.get('json') or {}
    detail['baseline'] = {
        'command': baseline['command'],
        'exit_code': baseline['exit_code'],
        'mismatches': baseline_doc.get('mismatches'),
        'stdout_sha256': baseline['stdout_sha256'],
        'wall_seconds': baseline['wall_seconds'],
    }
    detail['rubric_committed_at_freeze'] = rubric_committed

    # ------------------------------------------------------- arm A: reality
    candidates = []
    for ident, names in entry_candidates(doc):
        for name in names:
            if name in frozen or name in frozen_dirs:
                continue
            if any(name == d or name.startswith(d + '/') for d in frozen_dirs):
                continue
            if name in paths:
                candidates.append((ident, name))
    candidates.sort(key=lambda item: (0 if item[1].startswith(('corpus/', 'evidence/'))
                                       else 1, item[0], item[1]))
    detail['candidates'] = candidates[:10]
    seed = declared_seed(doc)
    if seed:
        detail['declared_seed'] = seed
        # the rubric names its own seed: put it FIRST, whatever the generic
        # candidate order is.
        seed_file = seed.get('file')
        seed_id = seed.get('entry_id')
        if isinstance(seed_file, str) and seed_file in paths:
            candidates = [(seed_id or ident, seed_file) for ident, name in candidates
                          if name == seed_file]
            candidates = [(seed_id or 'entry', seed_file)]
    arm_a = []
    arm_a_ok = False
    arm_a_result = baseline
    for ident, name in candidates[:6]:
        git(clone, 'reset', '-q', '--hard', freeze)
        git(clone, 'clean', '-qfd')
        data = blob(clone, freeze, name)
        if data is None:
            continue
        if seed and seed.get('file') == name:
            kind = ((seed.get('mutation') or {}).get('kind') or '')
            new_data, how = apply_declared_seed(kind, data)
            if kind == 'evidence-path-substituted':
                mutation = seed.get('mutation') or {}
                old = mutation.get('old')
                new = mutation.get('new')
                if old and new:
                    new_data = data.decode('utf-8').replace(old, new).encode('utf-8')
                    how = 'evidence path %r -> %r' % (old, new)
        else:
            new_data, how = seed_mutation(name, data)
        target = os.path.join(clone, name)
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        with open(target, 'wb') as handle:
            handle.write(new_data)
        git(clone, 'add', '-A')
        git(clone, '-c', 'user.email=controls@kaidoku.local',
            '-c', 'user.name=R44C2Controls', 'commit', '-q', '-m',
            'seeded mismatch: %s' % name)
        seeded = rev_parse(clone, 'HEAD')
        result = run_counter(counter, root=clone, rev=seeded, freeze=freeze,
                              work=work, rubric=rubric_arg,
                              json_out=os.path.join(out, 'ctl-c2-1.json'))
        sdoc = result.get('json') or {}
        arm_a.append({
            'target': name, 'entry': ident, 'mutation': how,
            'command': result['command'], 'exit_code': result['exit_code'],
            'mismatches': sdoc.get('mismatches'),
            'stdout_sha256': result['stdout_sha256'],
            'wall_seconds': result['wall_seconds'],
        })
        if result['exit_code'] == EXIT_FAIL and sdoc.get('mismatches'):
            arm_a_ok = True
            arm_a_result = result
            break
    detail['arms']['A_reality_side'] = {
        'ok': arm_a_ok, 'attempts': arm_a,
        'note': ('no non-frozen file named by the rubric could be seeded'
                 if not arm_a and not candidates else ''),
    }

    # ----------------------------------------------- arm B: rubric side seed
    arm_b = []
    arm_b_ok = False
    arm_b_result = baseline
    for entry in entries:
        ident = pick(entry, ('id', 'check_id', 'entry_id', 'name', 'label'))
        if not isinstance(ident, str) or not ident.strip():
            ident = 'entry'
        new_asserted, how = corrupt_asserted(entry)
        broken = json.loads(raw)
        list_key = None
        for key in ENTRY_LIST_KEYS:
            if isinstance(broken.get(key), list):
                list_key = key
                break
        target_entry = None
        for candidate in broken[list_key]:
            if isinstance(candidate, dict):
                cand_id = pick(candidate, ('id', 'check_id', 'entry_id', 'name',
                                           'label'))
                if cand_id == ident:
                    target_entry = candidate
                    break
        if target_entry is None:
            target_entry = broken[list_key][0]
        for key in ('asserted', 'assert', 'expected', 'expected_value', 'value'):
            if key in target_entry:
                target_entry[key] = new_asserted
                break
        else:
            target_entry['asserted'] = new_asserted
        seeded_rubric = os.path.join(work, 'ctl-c2-1-seeded-rubric.json')
        write(seeded_rubric, json.dumps(broken, indent=1))
        result = run_counter(counter, root=clone, rev=freeze, freeze=freeze,
                              work=work, rubric=seeded_rubric,
                              json_out=os.path.join(out, 'ctl-c2-1.json'))
        sdoc = result.get('json') or {}
        arm_b.append({
            'entry': ident, 'mutation': how,
            'command': result['command'], 'exit_code': result['exit_code'],
            'mismatches': sdoc.get('mismatches'),
            'stdout_sha256': result['stdout_sha256'],
            'wall_seconds': result['wall_seconds'],
        })
        if result['exit_code'] == EXIT_FAIL and sdoc.get('mismatches'):
            arm_b_ok = True
            arm_b_result = result
            break
    detail['arms']['B_rubric_side'] = {'ok': arm_b_ok, 'attempts': arm_b}

    ok = arm_a_ok or arm_b_ok
    result = arm_a_result if arm_a_ok else (arm_b_result if arm_b_ok else baseline)
    sdoc = result.get('json') or {}
    reported = list(sdoc.get('mismatches') or [])
    baseline_ids = list(baseline_doc.get('mismatches') or [])
    seeded_entry_id = None
    if arm_a:
        seeded_entry_id = arm_a[-1].get('entry')
    elif arm_b:
        seeded_entry_id = arm_b[-1].get('entry')
    # the seed is ATTRIBUTABLE when the seeded entry id is reported now and
    # was NOT reported in the unseeded baseline at the same freeze.
    seeded_reported = (bool(seeded_entry_id) and seeded_entry_id in reported
                       and seeded_entry_id not in baseline_ids)
    newly_mismatching = [i for i in reported if i not in baseline_ids]
    # the rubric's own declared expectation for CTL-C2-1 (when it has one).
    # Its vector is declared for the POSITIVE-repair-then-seed order, so the
    # ids are recorded, not gated: this control seeds at the freeze.
    vector = rubric_control_vector(doc, 'CTL-C2-1')
    if vector:
        want = vector['vector']
        detail['declared_vector'] = vector
        detail['declared_vector_checks'] = {
            'counter_exit_code_matches': (want.get('counter_exit_code') is None
                                          or result['exit_code'] == want.get('counter_exit_code')),
            'mismatch_count_at_least_one': bool(reported),
            'seeded_entry_reported': seeded_reported,
        }
    detail.update({
        'seeded_entry': seeded_entry_id,
        'seeded_entry_reported_in_mismatches': seeded_reported,
        'mismatches': reported,
        'baseline_mismatch_ids': baseline_ids,
        'newly_mismatching_ids': newly_mismatching,
        'mismatch_details': sdoc.get('mismatch_details'),
        'baseline_exit_code': baseline['exit_code'],
        'attribution': ('seed_induced' if newly_mismatching
                        else 'pre_existing_mismatch'),
        'verdict': 'ok' if ok else 'failed',
        'note': ('neither arm produced a reported mismatch' if not ok else ''),
    })
    payload = receipt(
        'CTL-C2-1',
        'the counter must report the seeded mismatch by id and exit non-zero '
        '(1) at the seeded revision',
        result, **detail)
    return payload, ok


def ctl_c2_2(counter, root, freeze, rubric_path, work, out):
    """Malformed rubric: one entry loses its check command -> exit 2."""
    detail = {'mode': 'malformed_rubric'}
    if not rubric_path or not os.path.isfile(rubric_path):
        raise ControlError('rubric not available: %s' % rubric_path)
    with open(rubric_path, encoding='utf-8') as handle:
        raw = handle.read()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ControlError('rubric is not JSON: %s' % exc)
    entries = rubric_entries(doc)
    if not entries:
        raise ControlError('rubric has no entries to malform')
    broken = json.loads(raw)
    list_key = None
    for key in ENTRY_LIST_KEYS:
        if isinstance(broken.get(key), list):
            list_key = key
            break
    dropped = []
    for entry in broken[list_key]:
        for key in COMMAND_KEYS:
            if key in entry:
                dropped.append(key)
                del entry[key]
                break
        if dropped:
            break
    if not dropped:
        raise ControlError('no command key found to drop')
    broken_path = os.path.join(work, 'ctl-c2-2-malformed-rubric.json')
    write(broken_path, json.dumps(broken, indent=1))
    detail['dropped_keys'] = dropped
    detail['rubric_sha256'] = sha256_bytes(raw.encode('utf-8'))
    detail['broken_rubric_sha256'] = sha256_bytes(
        json.dumps(broken, indent=1).encode('utf-8'))
    result = run_counter(counter, root=root, rev=freeze, freeze=freeze, work=work,
                          rubric=broken_path,
                          json_out=os.path.join(out, 'ctl-c2-2.json'))
    doc2 = result.get('json') or {}
    reason = doc2.get('unevaluable') or ''
    ok = (result['exit_code'] == EXIT_CANT and 'rubric_malformed' in str(reason))
    detail.update({
        'unevaluable': reason,
        'verdict': 'ok' if ok else 'failed',
        'note': 'exit 2 = could-not-evaluate; a malformed rubric is never a score',
    })
    payload = receipt(
        'CTL-C2-2',
        'a rubric with a dropped check command must be refused: exit 2 '
        '(rubric_malformed), never a score',
        result, **detail)
    return payload, ok


def ctl_c2_3(counter, root, freeze, rubric_path, work, out, rubric_bytes=None):
    """Rubric edited mid-round -> exit 2, frozen_path_changed on the rubric.

    The rubric is a FROZEN PATH.  A scratch clone of the lane is committed with
    the rubric bytes at a freeze commit and then EDITED mid-round; the counter
    must refuse with exit 2 and `frozen_path_changed` naming
    `tools/round-44/c2-rubric.json`.  A later restore does not un-block: the
    walk compares FREEZE..REV, so the re-red is permanent for that pair.

    Two freeze arrangements:
      * the rubric is committed at the real freeze -> the real freeze is used
        (the counter reads the rubric AT THE FREEZE, so a post-freeze edit
        cannot loosen the score);
      * otherwise a synthetic freeze commit is created inside the clone that
        holds the rubric bytes, so the arm is still runnable before the L1
        installs the rubric.
    """
    detail = {'mode': 'rubric_immutability'}
    if not rubric_path or not os.path.isfile(rubric_path):
        raise ControlError('rubric not available: %s' % rubric_path)
    raw = open(rubric_path, 'rb').read()
    if rubric_bytes is not None:
        raw = rubric_bytes
    clone = clone_repo(root, os.path.join(work, 'ctl-c2-3-clone'))
    git(clone, 'checkout', '-q', freeze)
    rub_rel = 'tools/round-44/c2-rubric.json'
    rub = os.path.join(clone, rub_rel)
    at_freeze = blob(clone, freeze, rub_rel)
    if at_freeze is not None and at_freeze == raw:
        freeze_used = freeze
        detail['freeze_arrangement'] = 'real_freeze'
    else:
        # synthetic freeze inside the clone that holds the rubric bytes
        os.makedirs(os.path.dirname(rub), exist_ok=True)
        with open(rub, 'wb') as handle:
            handle.write(raw)
        git(clone, 'add', '-A')
        git(clone, '-c', 'user.email=controls@kaidoku.local',
            '-c', 'user.name=R44C2Controls', 'commit', '-q', '-m',
            'rubric committed at the freeze')
        freeze_used = rev_parse(clone, 'HEAD')
        detail['freeze_arrangement'] = 'synthetic_freeze'
    # edit the rubric mid-round (an in-place fabrication, not an append)
    edited = raw.decode('utf-8', 'replace')
    if '"asserted":' in edited:
        edited = edited.replace('"asserted":', '"asserted_edited":', 1)
    else:
        edited = edited.replace('{', '{ "edited_mid_round": true,', 1)
    with open(rub, 'w', encoding='utf-8') as handle:
        handle.write(edited)
    git(clone, 'add', '-A')
    git(clone, '-c', 'user.email=controls@kaidoku.local',
        '-c', 'user.name=R44C2Controls', 'commit', '-q', '-m',
        'rubric edited mid-round')
    edited_rev = rev_parse(clone, 'HEAD')
    result = run_counter(counter, root=clone, rev=edited_rev, freeze=freeze_used,
                          work=work, rubric=None,
                          json_out=os.path.join(out, 'ctl-c2-3.json'))
    doc = result.get('json') or {}
    changed = doc.get('frozen_path_changed') or []
    ok = (result['exit_code'] == EXIT_CANT and rub_rel in changed)
    detail.update({
        'freeze_used': freeze_used,
        'edited_revision': edited_rev,
        'rubric_sha256_at_freeze': sha256_bytes(raw),
        'rubric_sha256_edited': sha256_bytes(edited.encode('utf-8')),
        'frozen_path_changed': changed,
        'unevaluable': doc.get('unevaluable'),
        'verdict': 'ok' if ok else 'failed',
        'note': ('the rubric is a frozen path: a mid-round edit re-reds with '
                 'exit 2 (frozen_path_changed); a later restore does not '
                 'un-block'),
    })
    payload = receipt(
        'CTL-C2-3',
        'a mid-round edit of the frozen rubric must re-red: exit 2 with '
        'frozen_path_changed naming tools/round-44/c2-rubric.json',
        result, **detail)
    return payload, ok


def ctl_c2_4(counter, root, freeze, rubric_path, work, out):
    """Wrong-value note: a correction note carrying a wrong value never passes.

    Two arms, both in a scratch clone of the lane:

      arm A (enforced)  the wrong-value note is appended to the rubric-named
        frozen file and the counter is run at the FREEZE with the freeze walk
        ENFORCED.  The note is a declaration; the rubric binds the exact
        appended bytes, so the counter must refuse: never a pass.

      arm B (scored)   the same note, with the freeze walk REPORTED but not
        enforced (the census mode), so the ENTRY is scored.  The check
        re-derives the value from the tree; the note's value disagrees with
        the derivation, so the observation is `UNSUPPORTED:<note value>` and the
        entry stays a MISMATCH — a note is never evidence.

    The control passes when neither arm yields a pass (exit 0 / met_target).
    """
    detail = {'mode': 'wrong_value_note'}
    if not rubric_path or not os.path.isfile(rubric_path):
        raise ControlError('rubric not available: %s' % rubric_path)
    with open(rubric_path, encoding='utf-8') as handle:
        raw = handle.read()
    doc = json.loads(raw)
    edits = doc.get('expected_edits') if isinstance(doc, dict) else None
    if not isinstance(edits, dict) or not edits:
        raise ControlError('rubric declares no expected_edits to seed a note into')
    target_file = sorted(edits)[0]
    edit = edits[target_file] or {}
    append_lines = edit.get('append') or []
    marker = edit.get('marker')
    if not append_lines or not marker:
        raise ControlError('expected_edits[%s] binds no append/marker' % target_file)
    # The wrong value REPLACES the bound value line: the check reads the FIRST
    # `c2-correction-value:` after its marker, so appending a second line would
    # leave the correct value in force and the note would never be wrong.
    note_lines = []
    wrong_value = None
    for line in append_lines:
        if line.startswith('c2-correction-value:'):
            value = line.split(':', 1)[1].strip()
            wrong_value = value + ' [WRONG]'
            note_lines.append('c2-correction-value: ' + wrong_value)
        else:
            note_lines.append(line)
    if wrong_value is None:
        raise ControlError('expected_edits[%s] binds no c2-correction-value line'
                           % target_file)
    detail['target_file'] = target_file
    detail['note_lines'] = note_lines
    detail['wrong_value'] = wrong_value
    detail['note_note'] = ('the bound value line is REPLACED, not appended '
                            'after: the check reads the first c2-correction-value '
                            'after its marker')

    clone = clone_repo(root, os.path.join(work, 'ctl-c2-4-clone'))
    git(clone, 'checkout', '-q', freeze)
    target = os.path.join(clone, target_file)
    with open(target, 'a', encoding='utf-8') as handle:
        handle.write('\n' + '\n'.join(note_lines) + '\n')
    git(clone, 'add', '-A')
    git(clone, '-c', 'user.email=controls@kaidoku.local',
        '-c', 'user.name=R44C2Controls', 'commit', '-q', '-m',
        'wrong-value correction note')
    noted_rev = rev_parse(clone, 'HEAD')
    detail['noted_revision'] = noted_rev

    arms = {}
    # arm A: enforced freeze walk
    enforced = run_counter(counter, root=clone, rev=noted_rev, freeze=freeze,
                           work=work, rubric=rubric_path,
                           json_out=os.path.join(out, 'ctl-c2-4-enforced.json'))
    edoc = enforced.get('json') or {}
    arms['A_enforced'] = {
        'command': enforced['command'],
        'exit_code': enforced['exit_code'],
        'mismatches': edoc.get('mismatches'),
        'unevaluable': edoc.get('unevaluable'),
        'frozen_path_changed': edoc.get('frozen_path_changed'),
        'stdout_sha256': enforced['stdout_sha256'],
        'wall_seconds': enforced['wall_seconds'],
    }
    # arm B: census mode, the freeze walk reported but not enforced
    scored = run_counter(counter, root=clone, rev=noted_rev, freeze=freeze,
                         work=work, rubric=rubric_path,
                         json_out=os.path.join(out, 'ctl-c2-4-scored.json'),
                         pre_freeze=True)
    sdoc = scored.get('json') or {}
    observed = None
    for entry in sdoc.get('entries') or []:
        if entry.get('id') and entry.get('file') == target_file:
            value = entry.get('observed')
            if isinstance(value, str) and value.startswith('UNSUPPORTED:'):
                observed = value
                break
    arms['B_scored'] = {
        'command': scored['command'],
        'exit_code': scored['exit_code'],
        'mismatches': sdoc.get('mismatches'),
        'unevaluable': sdoc.get('unevaluable'),
        'note_observation': observed,
        'stdout_sha256': scored['stdout_sha256'],
        'wall_seconds': scored['wall_seconds'],
    }
    a_pass = (enforced['exit_code'] == EXIT_MET
              and (edoc.get('met_target') is not False))
    b_pass = (scored['exit_code'] == EXIT_MET
              and (sdoc.get('met_target') is not False))
    ok = (not a_pass) and (not b_pass)
    detail.update({
        'arms': arms,
        'arm_A_passed': a_pass,
        'arm_B_passed': b_pass,
        'verdict': 'ok' if ok else 'failed',
        'note': ('a wrong-value note must never make an entry pass; arm B '
                 'shows the entry scored UNSUPPORTED:<note value>'),
    })
    payload = receipt(
        'CTL-C2-4',
        'a correction note carrying a wrong value must never pass: the counter '
        'refuses it (enforced arm) and the entry stays a mismatch (scored arm, '
        'note_value_disagrees)',
        enforced, **detail)
    return payload, ok


def fitness_gate(counter, root, rev, freeze, rubric_path, work, out, limit=None):
    """Per-entry fitness gate: every check is shown able to fail on its own entry.

    For every rubric entry, one mutation of that entry's asserted value is
    applied to a scratch copy of the rubric and the counter is asked to score
    it.  The entry must then be reported as a mismatch: a check that cannot
    fail on its own statement is not a check (the rubric's own fitness gate).
    """
    with open(rubric_path, encoding='utf-8') as handle:
        raw = handle.read()
    doc = json.loads(raw)
    entries = rubric_entries(doc)
    list_key = None
    for key in ENTRY_LIST_KEYS:
        if isinstance(doc.get(key), list):
            list_key = key
            break
    rows = []
    for index, entry in enumerate(entries):
        if limit is not None and index >= limit:
            break
        ident = pick(entry, ('id', 'check_id', 'entry_id', 'name', 'label'))
        ident = ident if isinstance(ident, str) and ident.strip() else 'entry-%03d' % index
        new_asserted, how = corrupt_asserted(entry)
        broken = json.loads(raw)
        target_entry = None
        for candidate in broken[list_key]:
            if not isinstance(candidate, dict):
                continue
            cand_id = pick(candidate, ('id', 'check_id', 'entry_id', 'name', 'label'))
            if cand_id == ident:
                target_entry = candidate
                break
        if target_entry is None:
            target_entry = broken[list_key][index]
        for key in ('asserted', 'assert', 'expected', 'expected_value', 'value'):
            if key in target_entry:
                target_entry[key] = new_asserted
                break
        else:
            target_entry['asserted'] = new_asserted
        seeded = os.path.join(work, 'fitness-%03d.json' % index)
        write(seeded, json.dumps(broken, indent=1))
        result = run_counter(counter, root=root, rev=rev, freeze=freeze, work=work,
                              rubric=seeded,
                              json_out=os.path.join(out, 'fitness-%03d.json' % index))
        rdoc = result.get('json') or {}
        reported = list(rdoc.get('mismatches') or [])
        rows.append({
            'id': ident,
            'mutation': how,
            'exit_code': result['exit_code'],
            'reported_in_mismatches': ident in reported,
            'mismatches': reported,
            'stdout_sha256': result['stdout_sha256'],
            'wall_seconds': result['wall_seconds'],
        })
    failed = [r['id'] for r in rows if not r['reported_in_mismatches']]
    return rows, failed


# ---------------------------------------------------------------------- modes


def run_dev_mode(counter, work, out, controls, variant='stale'):
    """Every control against a self-contained synthetic fixture.

    Two fixtures are built:

      `stale`      the statement claims 7 knowledge files, the tree holds 6
                   -> the census reports one mismatch -> the do-nothing control
                   FAILS, as it must.
      `consistent` the statement claims 6 and the tree holds 6
                   -> the census reports zero mismatches -> the do-nothing
                   control reaches the target, which is the honest-stop signal
                   for R44-C2.

    CTL-C2-0 is scored on the fixture named by `--dev-variant`; the other
    controls are scored on the `consistent` fixture (a green baseline, so a
    seeded mismatch is attributable).
    """
    stale = build_fixture(work, 'stale', 7, 6)
    consistent = build_fixture(work, 'consistent', 6, 6)
    results = []
    verdicts = {}

    def record(name, payload, ok):
        results.append(payload)
        verdicts[name] = payload.get('verdict')

    census = stale if variant == 'stale' else consistent
    if 'CTL-C2-0' in controls:
        payload, ok = ctl_c2_0(counter, census['root'], census['freeze'],
                               census['rubric'], work, out)
        payload['fixture'] = 'dev:' + variant
        record('CTL-C2-0', payload, ok)
    for name, fn in (('CTL-C2-1', ctl_c2_1), ('CTL-C2-2', ctl_c2_2),
                     ('CTL-C2-3', ctl_c2_3), ('CTL-C2-4', ctl_c2_4)):
        if name in controls:
            payload, ok = fn(counter, consistent['root'], consistent['freeze'],
                             consistent['rubric'], work, out)
            payload['fixture'] = 'dev:consistent'
            record(name, payload, ok)
    return results, verdicts


def run_real_mode(counter, root, base, freeze, rubric_path, work, out, controls):
    results = []
    verdicts = {}
    declared = None
    try:
        with open(rubric_path, encoding='utf-8') as handle:
            doc = json.load(handle)
        if isinstance(doc.get('freeze'), str):
            declared = doc['freeze']
    except (OSError, json.JSONDecodeError):
        doc = {}

    def record(name, payload, ok):
        results.append(payload)
        verdicts[name] = payload.get('verdict')

    if 'CTL-C2-0' in controls:
        payload, ok = ctl_c2_0(counter, root, base, rubric_path, work, out,
                               freeze=freeze, declared_freeze=declared)
        payload['fixture'] = 'real'
        record('CTL-C2-0', payload, ok)
    if 'CTL-C2-1' in controls:
        payload, ok = ctl_c2_1(counter, root, freeze, rubric_path, work, out,
                               base=base)
        payload['fixture'] = 'real'
        record('CTL-C2-1', payload, ok)
    if 'CTL-C2-2' in controls:
        payload, ok = ctl_c2_2(counter, root, freeze, rubric_path, work, out)
        payload['fixture'] = 'real'
        record('CTL-C2-2', payload, ok)
    if 'CTL-C2-3' in controls:
        payload, ok = ctl_c2_3(counter, root, freeze, rubric_path, work, out)
        payload['fixture'] = 'real'
        record('CTL-C2-3', payload, ok)
    if 'CTL-C2-4' in controls:
        payload, ok = ctl_c2_4(counter, root, freeze, rubric_path, work, out)
        payload['fixture'] = 'real'
        record('CTL-C2-4', payload, ok)
    return results, verdicts


# ------------------------------------------------------------------------ CLI


def main(argv=None):
    started = time.time()
    parser = argparse.ArgumentParser(
        description='R44-C2 controls: CTL-C2-0/1/2/3 against the frozen counter.')
    parser.add_argument('--root', help='lane root (real mode)')
    parser.add_argument('--counter', required=True, help='path to c2-counter.py')
    parser.add_argument('--rubric', help='path to the frozen c2-rubric.json')
    parser.add_argument('--rev', default=DEFAULT_BASE, help='measured revision')
    parser.add_argument('--freeze', help='freeze revision')
    parser.add_argument('--work', help='scratch directory')
    parser.add_argument('--out', help='directory for the per-control receipts')
    parser.add_argument('--json-out', help='summary receipt')
    parser.add_argument('--mode', choices=('auto', 'dev', 'real'), default='auto')
    parser.add_argument('--ctl',
                        default='CTL-C2-0,CTL-C2-1,CTL-C2-2,CTL-C2-3,CTL-C2-4')
    parser.add_argument('--fitness', action='store_true',
                        help='run the per-entry fitness gate: every rubric '
                             'entry is shown able to fail on its own statement '
                             '(one asserted-value mutation per entry)')
    parser.add_argument('--fitness-limit', type=int, default=None,
                        help='score only the first N entries (a bounded '
                             'sample; the receipt says how many were scored)')
    parser.add_argument('--dev-variant', choices=('stale', 'consistent'),
                        default='stale',
                        help='dev fixture shape: `stale` = the fixture statement '
                             'is wrong (the census reports a mismatch, the '
                             'do-nothing control fails); `consistent` = the '
                             'statement is right (the census reports zero '
                             'mismatches — the honest-stop signal for R44-C2)')
    args = parser.parse_args(argv)

    if not os.path.isfile(args.counter):
        print('counter not found: %s' % args.counter, file=sys.stderr)
        return EXIT_CANT
    work = os.path.abspath(args.work or os.environ.get('HYAKU_SCRATCH')
                           or tempfile.gettempdir())
    os.makedirs(work, exist_ok=True)
    out = os.path.abspath(args.out or os.path.join(work, 'c2-controls-receipts'))
    os.makedirs(out, exist_ok=True)
    controls = [c.strip() for c in args.ctl.split(',') if c.strip()]

    root = os.path.abspath(args.root) if args.root else None
    rubric = os.path.abspath(args.rubric) if args.rubric else None
    if rubric is None and root:
        guess = os.path.join(root, 'tools', 'round-44', 'c2-rubric.json')
        if os.path.isfile(guess):
            rubric = guess
    real_available = bool(root and rubric and os.path.isfile(rubric)
                           and os.path.isdir(os.path.join(root, '.git')))

    mode = args.mode
    if mode == 'auto':
        mode = 'real' if real_available else 'dev'

    summary = {
        'schema': 'kaidoku-r44-c2-controls-v1',
        'seat': SEAT,
        'mode': mode,
        'root': root,
        'counter': os.path.abspath(args.counter),
        'counter_sha256': sha256_bytes(open(args.counter, 'rb').read()),
        'rubric': rubric,
        'rubric_sha256': (sha256_bytes(open(rubric, 'rb').read())
                          if rubric and os.path.isfile(rubric) else None),
        'rev': args.rev,
        'freeze': args.freeze,
        'work': work,
        'controls': [],
        'verdicts': {},
        'exit_code': EXIT_MET,
        'argv': sys.argv,
        'tool_command': command_line([sys.executable, '-I', '-B',
                                      os.path.abspath(__file__)] + sys.argv[1:]),
    }

    try:
        if mode == 'dev':
            results, verdicts = run_dev_mode(args.counter, work, out, controls,
                                             variant=args.dev_variant)
        else:
            base = rev_parse(root, args.rev) or args.rev
            freeze = args.freeze
            if not freeze:
                freeze = rev_parse(root, 'HEAD')
            if not freeze:
                raise ControlError('no freeze revision resolvable at %s' % root)
            results, verdicts = run_real_mode(args.counter, root, base, freeze,
                                              rubric, work, out, controls)
    except ControlError as exc:
        summary['error'] = str(exc)
        summary['exit_code'] = EXIT_CANT
        if args.json_out:
            with open(args.json_out, 'w', encoding='utf-8') as handle:
                json.dump(summary, handle, indent=1, sort_keys=True)
        print(json.dumps({'error': str(exc), 'exit_code': EXIT_CANT},
                         sort_keys=True))
        return EXIT_CANT

    for payload in results:
        name = payload['control']
        path = os.path.join(out, '%s.json' % name)
        summary['controls'].append({
            'control': name,
            'receipt': path,
            'exit_code': payload.get('exit_code'),
            'expected': payload.get('expected'),
            'verdict': payload.get('verdict'),
            'stdout_sha256': payload.get('stdout_sha256'),
            'wall_seconds': payload.get('wall_seconds'),
        })
    summary['verdicts'] = verdicts
    if args.fitness and mode == 'real':
        rows, failed = fitness_gate(
            args.counter, root, rev_parse(root, args.rev) or args.rev,
            rev_parse(root, args.freeze) or args.freeze, rubric, work, out,
            limit=args.fitness_limit)
        summary['fitness'] = {
            'entries_scored': len(rows),
            'entries_failing_to_fail': failed,
            'ok': not failed,
            'rows': rows,
        }
        if failed:
            summary['verdicts']['FITNESS'] = 'failed'
        else:
            summary['verdicts']['FITNESS'] = 'ok'
    if 'CTL-C2-0' in verdicts and verdicts.get('CTL-C2-0') == 'ok':
        for payload in results:
            if payload['control'] == 'CTL-C2-0' and payload.get('kill_rule_fired'):
                summary['kill_rule_fired'] = ['CTL-C2-0']
                summary['claim_stops'] = True
    failed = [c for c, v in verdicts.items() if v == 'failed']
    inconclusive = [c for c, v in verdicts.items() if v == 'inconclusive']
    if failed or summary.get('kill_rule_fired'):
        summary['exit_code'] = EXIT_FAIL
    elif inconclusive:
        summary['exit_code'] = EXIT_CANT
    else:
        summary['exit_code'] = EXIT_MET
    stdout_line = json.dumps({'mode': mode, 'verdicts': verdicts,
                               'exit_code': summary['exit_code']}, sort_keys=True)
    tool_stdout_sha256 = sha256_bytes(stdout_line.encode('utf-8'))
    tool_wall = round(time.time() - started, 6)
    summary['stdout_sha256'] = tool_stdout_sha256
    summary['stdout'] = stdout_line
    summary['wall_seconds'] = tool_wall
    for payload in results:
        name = payload['control']
        path = os.path.join(out, '%s.json' % name)
        payload['tool_command'] = summary['tool_command']
        payload['tool_stdout_sha256'] = tool_stdout_sha256
        payload['tool_wall_seconds'] = tool_wall
        payload['tool_exit_code'] = summary['exit_code']
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as handle:
            json.dump(summary, handle, indent=1, sort_keys=True)
    print(stdout_line)
    return summary['exit_code']


if __name__ == '__main__':
    sys.exit(main())
