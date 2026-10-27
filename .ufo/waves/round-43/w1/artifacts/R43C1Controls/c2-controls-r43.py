#!/usr/bin/env python3
"""R43-C1 controls: build the round-43 control tables and score every control.

Round-43 successor of `tools/round-42/c2-controls.py` (which built and scored the
round-42 C2 control set).  Two things changed and both are load-bearing:

  1. the CONTROL SET is not rebuilt from the live `SKILL.md`.  The round-42
     builder copied the live `SKILL.md` into `CTL-C2-0-base-SKILL.md` ("the
     do-nothing document") and the live table into the reference row set.  At
     round-43 time the live `SKILL.md` already carries the frozen v4 table, so
     a rebuild today makes the do-nothing control the REFERENCE TABLE: it
     scores 78/78 and the kill rule fires on the do-nothing control itself.
     Measured (round-42 builder, `--build`, lane `SKILL.md` as of
     6b9e64fe7e0de202d9383baad5792fbfe039a743):
         CTL-C2-0-base-SKILL.md  exit=0 matched=78/78   kill_rule_fires True
     Here the control tables are copied BYTE-EXACT from the frozen round-42
     documents (sha256-verified), so the do-nothing control stays the v3-era
     document that exits 2 and the reference stays the reference.

  2. the SCORE is computed on the frozen round-42 dev arm and compared with
     the frozen round-42 receipt, and the receipt's DEGENERATE combo column is
     recomputed.  The round-42 receipt (`.ufo/waves/round-42/controls/c2/
     dev-scores-prefreeze.json`) reports `"combo": [0, 0]` for every control
     and `"named": [m, 78]`: the receipt was computed on two scratch slices
     (`/fast/scratch/hyaku/kaidoku-r42/l1-ctl/{named,combo}`) that carried no
     `manifest.json`, so `combo_ids()` found no `combo` carrier and every
     envelope was counted as named.  The `matched` numbers are right (all 14
     documents reproduce exactly on the committed dev arm, missed SETS equal);
     the combo/named SPLIT is wrong.  Here the split is computed from the
     committed dev arm's `manifest.json` (`class == "combo"`), and the
     round-42 receipt is kept as the `matched` reference.

The four controls scored (plans/round-43-claims.md `## R43-C1`, kill rule):

  CTL-C1-0  do-nothing       the counter at the FREEZE exits 2
                              `no_manifest_at_rev` (the held-out evidence does
                              not exist at the freeze; it is added after).
  CTL-C1-1  stale manifest   the round-42 held-out manifest copied byte-exact
                              to the round-43 evidence path, in a sandbox clone
                              whose freeze commit ALREADY carries it, so the
                              counter's `seed_matches_freeze` and
                              `manifest_after_freeze` bindings both go false.
                              The counter must exit non-zero and the receipt
                              must name the bindings that fired.
  CTL-C1-2  refusal red      the round-42 C02 manifest (declared
                              {extractor-failure, unpublished-entry}) fed to the
                              frozen generator's tuple check exits 3
                              `declared_tuple_unobserved` and writes NO
                              manifest.  The GREEN half of the same check (a
                              manifest whose declared tuple equals the observed
                              one) must exit 0 and write no manifest either --
                              it is the tuple check, not the write, that the
                              control exercises.
  CTL-C1-3  shortcut controls the eight round-42 shortcut control documents
                              (catch-all, actions-rotated, exact-gap-sets,
                              no-legacy-row, v4-handler-glob,
                              no-container-residue, and both lookup variants)
                              re-scored on the frozen round-42 dev arm with the
                              frozen round-42 interpreter and evaluator
                              reproduce their round-42 receipts, and NONE of
                              them reaches the target (78 of 78).
  CTL-C1-4  hand-edit         a frozen dev-arm manifest with ONE carrier's
                              `declared_features` edited to a value its committed
                              envelope does not observe (every envelope byte
                              unchanged), scored by the counter, exits non-zero
                              with `observed_features_match_declared` false.  The
                              unedited baseline on the same arm keeps the binding
                              true, so the failure is attributable to the edit —
                              which is what proves the counter derives the
                              observed tuple from envelope bytes and not from the
                              manifest's own `generator.tuple_check` record.

Kill rule (plans/round-43-claims.md): a control that reaches the target stops
C1 before the held-out set is generated.  The reference table
(`CTL-C1-REF-v4-precedence.md`) is the POSITIVE WITNESS, not a control: it must
reach the target, and that is what proves the arm is scoreable at all.

Usage
  c2-controls-r43.py --root LANE --out CTL_DIR --json-out SUMMARY.json
      [--receipts DIR] [--ctl CTL-C1-0,...] [--build]
      [--counter PATH] [--generator PATH] [--interp PATH] [--eval PATH]
      [--dev DIR] [--evidence-dir DIR] [--scratch DIR]

Exit
  0  every selected control behaved as expected and no control reached the
     target (the kill rule did not fire)
  1  a control reached the target (the kill rule fired) or a control's actual
     exit/receipt disagreed with its expected one
  2  usage, IO, or a required frozen tool is absent

Honours TMPDIR and --scratch; never writes outside --out, --receipts and
--json-out; never mutates the lane's VCS (the CTL-C1-1 clone is a sandbox with
fixture identity).
"""
import argparse
import ast
import collections
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

MARK = '<!-- sqfs-triage-table v4 -->'

# --- the frozen round-42 control set (documents copied byte-exact) --------------
# The eight shortcut controls CTL-C1-3 scores, and the reference witness.
# (frozen document name, control id, role)
SHORTCUTS = (
    ('CTL-C2-1-catch-all.md', 'CTL-C1-3a-catch-all', 'control'),
    ('CTL-C2-3-actions-rotated.md', 'CTL-C1-3b-actions-rotated', 'control'),
    ('CTL-C2-4-exact-gap-sets.md', 'CTL-C1-3c-exact-gap-sets', 'control'),
    ('CTL-C2-8-no-legacy-row.md', 'CTL-C1-3d-no-legacy-row', 'control'),
    ('CTL-C2-9-v4-handler-glob.md', 'CTL-C1-3e-v4-handler-glob', 'control'),
    ('CTL-C2-10-no-container-residue.md', 'CTL-C1-3f-no-container-residue', 'control'),
    ('CTL-C2-7-lookup.md', 'CTL-C1-3g-lookup', 'control'),
    ('CTL-C2-7b-lookup-fallback.md', 'CTL-C1-3h-lookup-fallback', 'control'),
)
REFERENCE = ('CTL-C2-REF-v4-precedence.md', 'CTL-C1-REF-v4-precedence', 'witness')
DO_NOTHING = ('CTL-C2-0-base-SKILL.md', 'CTL-C1-0-base-SKILL', 'control')

# The frozen round-42 control directory (a frozen path of the round-43 claim).
R42_CONTROLS = '.ufo/waves/round-42/controls/c2'
# The frozen round-42 receipt that the round-43 score is compared with.
R42_RECEIPT = R42_CONTROLS + '/dev-scores-prefreeze.json'
# The frozen round-42 dev arm (a frozen path of the round-43 claim).
R42_DEV = 'corpus/evidence/round-42/c2/dev'
# The frozen round-42 held-out set (the CTL-C1-2 input).
R42_HELDOUT = 'corpus/evidence/round-42/c2/heldout'

# The round-43 evidence path the counter reads and the control plants into.
R43_EVIDENCE = 'corpus/evidence/round-43/c1/heldout'

# The bindings CTL-C1-1 requires to go false.
CTL1_REQUIRED_FALSE = ('seed_matches_freeze', 'manifest_after_freeze')

# The candidate CLIs for the generator's tuple check (probed, not assumed).
# Each entry is (flag,): the directory argument is appended by the caller.
TUPLE_CHECK_CLIS = (
    ('--tuple-check',),
    ('--check-tuples',),
    ('--verify-declared',),
)


class ControlError(Exception):
    """A control could not be run at all (usage, IO, missing frozen tool)."""


# ------------------------------------------------------------------ small helpers
def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def git(root, *args, **kw):
    p = subprocess.run(['git', '-C', root] + list(args),
                       capture_output=True, text=True, **kw)
    return p


def read_text(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def envelope_id(path):
    base = os.path.basename(path)
    parent = os.path.basename(os.path.dirname(path))
    if base in ('envelope.json', 'rea-full.json'):
        return parent
    return os.path.splitext(base)[0]


def collect_envs(devdir):
    """Envelope paths under a dev arm, in directory order (C* before H*)."""
    envs = []
    if not os.path.isdir(devdir):
        raise ControlError('dev arm not found: %s' % devdir)
    for name in sorted(os.listdir(devdir)):
        sub = os.path.join(devdir, name)
        if not os.path.isdir(sub):
            continue
        for cand in ('envelope.json', 'rea-full.json'):
            p = os.path.join(sub, cand)
            if os.path.isfile(p):
                envs.append(p)
                break
    if not envs:
        raise ControlError('no envelopes under %s' % devdir)
    return envs


# ------------------------------------------------------------------ scoring core
def expected_pairs(evaluator, devdir, scratch):
    """(label, action) per envelope id, from the frozen independent evaluator."""
    out = os.path.join(scratch, 'eval-dev.json')
    p = subprocess.run([sys.executable, '-I', '-B', evaluator,
                        '--envelopes', devdir, '--out', out],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise ControlError('evaluator failed on %s (exit %d): %s'
                           % (devdir, p.returncode, p.stderr.strip()[-400:]))
    doc = json.load(open(out))
    pairs = {}
    if isinstance(doc.get('results'), list):
        for rec in doc['results']:
            pairs[rec['id']] = (rec['label'], rec['action'])
    else:
        pairs.update(doc['labels'])
    if not pairs:
        raise ControlError('evaluator returned no labels for %s' % devdir)
    return pairs


def run_interpreter(interp, skill, envs):
    p = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', skill] + envs,
                       capture_output=True, text=True)
    got = {}
    for line in p.stdout.splitlines():
        parts = line.rstrip('\n').split('\t')
        if len(parts) == 3:
            got[envelope_id(parts[0])] = (parts[1], parts[2])
    return p.returncode, got, p.stderr.strip()[-400:]


def combo_ids(devdir):
    """Carrier ids whose manifest class is `combo` (the round-42 receipt lost this)."""
    out = set()
    path = os.path.join(devdir, 'manifest.json')
    if os.path.isfile(path):
        for c in json.load(open(path)).get('carriers') or []:
            if isinstance(c, dict) and c.get('class') == 'combo':
                out.add(c.get('id'))
    return out


# ------------------------------------------------------------------ control bodies
def ctl_c1_0(args, scratch):
    """CTL-C1-0 do-nothing: the counter at the freeze has no held-out manifest."""
    counter = args.counter
    if not os.path.isfile(counter):
        raise ControlError('counter not found: %s' % counter)
    receipt = os.path.join(scratch, 'ctl-c1-0.json')
    cmd = [sys.executable, '-I', '-B', counter, '--root', args.root,
           '--rev', args.freeze, '--freeze', args.freeze, '--json-out', receipt]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=scratch)
    doc = {}
    if os.path.isfile(receipt):
        doc = json.load(open(receipt))
    exit_code = doc.get('exit_code', p.returncode)
    unevaluable = doc.get('unevaluable')
    ok = exit_code == 2 and unevaluable == 'no_manifest_at_rev'
    return {
        'control': 'CTL-C1-0',
        'title': 'do-nothing: the counter at the freeze',
        'argv': cmd,
        'counter_exit': exit_code,
        'process_exit': p.returncode,
        'unevaluable': unevaluable,
        'counter_path': doc.get('counter_path'),
        'counter_sha256': doc.get('counter_sha256'),
        'counter_sha256_at_freeze': doc.get('counter_sha256_at_freeze'),
        'counter_sha256_at_freeze_present':
            doc.get('counter_sha256_at_freeze') is not None,
        'bindings_present': bool(doc.get('bindings')),
        'expected_exit': 2,
        'expected_unevaluable': 'no_manifest_at_rev',
        'expected_counter_sha256_at_freeze': 'present (amended freeze-integrity rule)',
        'ok': ok,
        'note': ('the held-out evidence does not exist at the freeze; the counter '
                 'must refuse to score a revision that has no manifest.  on this '
                 'path the round-42 counter reports an EMPTY `bindings` map, so '
                 'no binding may be read from this receipt; the amended '
                 'freeze-integrity rule additionally requires '
                 '`counter_sha256_at_freeze` here, which the round-42 counter '
                 'omits (it assigns the field after its Unevaluable raise) and '
                 'the round-43 counter provides'),
    }


def _envelope_digests(directory):
    """{carrier id: sha256} of every committed envelope under `directory`."""
    out = {}
    for name in sorted(os.listdir(directory)):
        sub = os.path.join(directory, name)
        if not os.path.isdir(sub):
            continue
        for cand in ('rea-full.json', 'run.json', 'envelope.json'):
            p = os.path.join(sub, cand)
            if os.path.isfile(p):
                out[name] = {'file': cand, 'sha256': sha256_file(p)}
                break
    return out


def _flip_one_declared_field(manifest_bytes):
    """Hand-edit ONE carrier's declared tuple so it cannot match its envelope.

    The edit is manifest-only: no envelope byte is touched.  `published` is
    flipped ('nonzero' <-> 'zero'), which the observed tuple derives from the
    published-file count, so the edited carrier is guaranteed to disagree.
    Returns (new bytes, edit record).
    """
    man = json.loads(manifest_bytes.decode())
    for c in man.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        feats = c.get('declared_features')
        if not isinstance(feats, dict):
            continue
        cur = feats.get('published')
        if cur == 'nonzero':
            feats['published'] = 'zero'
        elif cur == 'zero':
            feats['published'] = 'nonzero'
        else:
            continue
        new = (json.dumps(man, indent=2) + '\n').encode('utf-8')
        return new, {'carrier': c.get('id'), 'class': c.get('class'),
                     'field': 'published', 'declared_before': cur,
                     'declared_after': feats['published']}
    raise ControlError('no carrier carries a flippable declared tuple')


def _plant_arm(args, scratch, placement, tag='ctl-c1-1', src_rel=None,
               mutate=None):
    """One sandbox arm: plant a committed evidence tree at the counter's path.

    `placement` is 'at-freeze' (the tree is already in place when the freeze is
    cut: the manifest was NOT first added after the freeze) or 'after-freeze'
    (the tree is committed after the freeze, as if it were the held-out data).
    `mutate` optionally rewrites the manifest bytes (CTL-C1-4's hand edit); with
    no `mutate` the manifest must be byte-exact.
    """
    counter = args.counter
    src_rel = src_rel or args.r42_heldout
    src_dir = os.path.join(args.root, src_rel)
    src_manifest = os.path.join(src_dir, 'manifest.json')
    src_bytes = open(src_manifest, 'rb').read()
    src_envelopes = _envelope_digests(src_dir)

    clone = os.path.join(scratch, '%s-%s-clone' % (tag, placement))
    p = subprocess.run(['git', 'clone', '-q', '--shared', args.root, clone],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise ControlError('clone failed: %s' % p.stderr.strip()[-300:])
    top = git(clone, 'rev-parse', '--show-toplevel').stdout.strip()
    if top != os.path.abspath(clone):
        raise ControlError('clone toplevel mismatch: %s != %s' % (top, clone))
    if git(clone, 'rev-parse', '--verify', args.freeze).returncode != 0:
        raise ControlError('freeze %s is not in the clone' % args.freeze)
    git(clone, 'checkout', '-q', args.freeze)

    # Where does the counter READ the manifest?  Ask it: one run at the freeze
    # answers with `manifest_path` in its receipt.  The planted path is then the
    # counter's own, not a guess.
    probe = os.path.join(scratch, '%s-%s-probe.json' % (tag, placement))
    pcmd = [sys.executable, '-I', '-B', counter, '--root', clone,
            '--rev', args.freeze, '--freeze', args.freeze, '--json-out', probe]
    subprocess.run(pcmd, capture_output=True, text=True, cwd=scratch)
    evidence_dir = args.evidence_dir
    if os.path.isfile(probe):
        pdoc = json.load(open(probe))
        if pdoc.get('manifest_path'):
            evidence_dir = os.path.dirname(pdoc['manifest_path'])
    evidence_dir = evidence_dir.strip('/')

    # Plant the whole committed tree at that path: the envelopes so the counter
    # reaches the binding stage instead of stopping on an empty evaluator run,
    # and the manifest as the control's subject.
    dst_dir = os.path.join(clone, evidence_dir)
    if os.path.abspath(dst_dir) != os.path.abspath(src_dir):
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        os.makedirs(dst_dir)
        for name in sorted(os.listdir(src_dir)):
            s = os.path.join(src_dir, name)
            d = os.path.join(dst_dir, name)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copyfile(s, d)
    planted = open(os.path.join(dst_dir, 'manifest.json'), 'rb').read()
    edit = None
    if mutate is None:
        if planted != src_bytes:
            raise ControlError('planted manifest is not byte-exact')
    else:
        edited, edit = mutate(planted)
        with open(os.path.join(dst_dir, 'manifest.json'), 'wb') as fh:
            fh.write(edited)
        planted = edited
    planted_envelopes = _envelope_digests(dst_dir)
    envelopes_untouched = planted_envelopes == src_envelopes
    planted_seed = json.loads(planted.decode()).get('seed')

    env = dict(os.environ)
    env.update({
        'GIT_AUTHOR_NAME': 'fx', 'GIT_AUTHOR_EMAIL': 'fx@fx',
        'GIT_COMMITTER_NAME': 'fx', 'GIT_COMMITTER_EMAIL': 'fx@fx',
    })
    git(clone, 'add', '-A', evidence_dir)
    p = subprocess.run(['git', '-C', clone, '-c', 'user.name=fx', '-c',
                        'user.email=fx@fx', 'commit', '-q', '-m',
                        '%s control (%s): plant the committed evidence tree at '
                        'the %s path' % (tag, placement, evidence_dir)],
                       capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise ControlError('fixture commit failed: %s' % p.stderr.strip()[-300:])
    plant_commit = git(clone, 'rev-parse', 'HEAD').stdout.strip()

    if placement == 'at-freeze':
        freeze = plant_commit
        rev = plant_commit
    else:
        freeze = args.freeze
        rev = plant_commit

    receipt = os.path.join(scratch, '%s-%s.json' % (tag, placement))
    cmd = [sys.executable, '-I', '-B', counter, '--root', clone,
           '--rev', rev, '--freeze', freeze, '--json-out', receipt]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=scratch)
    doc = {}
    if os.path.isfile(receipt):
        doc = json.load(open(receipt))
    exit_code = doc.get('exit_code', p.returncode)
    bindings = doc.get('bindings') or {}
    fired = sorted(k for k, v in bindings.items() if v is not True)
    missing = [k for k in CTL1_REQUIRED_FALSE if bindings.get(k) is not False]
    return {
        'placement': placement,
        'argv': cmd,
        'probe_argv': pcmd,
        'evidence_dir': evidence_dir,
        'sandbox_freeze': freeze,
        'sandbox_rev': rev,
        'plant_commit': plant_commit,
        'planted_manifest_seed': planted_seed,
        'planted_manifest_sha256': sha256_bytes(planted),
        'source_manifest_sha256': sha256_bytes(src_bytes),
        'planted_byte_exact': planted == src_bytes,
        'manifest_hand_edit': edit,
        'envelopes_untouched': envelopes_untouched,
        'envelope_count': len(planted_envelopes),
        'counter_exit': exit_code,
        'process_exit': p.returncode,
        'unevaluable': doc.get('unevaluable'),
        'bindings': bindings,
        'bindings_false': doc.get('bindings_false'),
        'bindings_fired': fired,
        'observed_features_match_declared':
            bindings.get('observed_features_match_declared'),
        'required_false': list(CTL1_REQUIRED_FALSE),
        'required_false_missing': missing,
    }


def ctl_c1_1(args, scratch):
    """CTL-C1-1 stale manifest: the round-42 manifest planted in a sandbox."""
    counter = args.counter
    if not os.path.isfile(counter):
        raise ControlError('counter not found: %s' % counter)
    src_manifest = os.path.join(args.root, args.r42_heldout, 'manifest.json')
    if not os.path.isfile(src_manifest):
        raise ControlError('round-42 held-out manifest not found: %s' % src_manifest)

    arms = {}
    for placement in ('at-freeze', 'after-freeze'):
        arms[placement] = _plant_arm(args, scratch, placement)
    primary = arms['at-freeze']
    ok = (primary['counter_exit'] != 0
          and not primary['required_false_missing']
          and arms['after-freeze']['counter_exit'] != 0)
    return {
        'control': 'CTL-C1-1',
        'title': 'stale manifest: the round-42 manifest at the round-43 path',
        'arms': arms,
        'primary_placement': 'at-freeze',
        'planted_manifest_sha256': primary['planted_manifest_sha256'],
        'source_manifest_sha256': primary['source_manifest_sha256'],
        'planted_byte_exact': primary['planted_byte_exact'],
        'counter_exit': primary['counter_exit'],
        'bindings_fired': primary['bindings_fired'],
        'required_false': list(CTL1_REQUIRED_FALSE),
        'required_false_missing': primary['required_false_missing'],
        'expected_exit': 'non-zero',
        'ok': ok,
        'note': ('the manifest is present at the sandbox freeze, so the counter '
                 'must reject it: its seed is the round-42 freeze and it was '
                 'not first added after the freeze.  the after-freeze arm is the '
                 'other placement of the same stale manifest and shows which '
                 'binding fires there instead'),
    }


def ctl_c1_4(args, scratch):
    """CTL-C1-4 counter-side hand-edit rejection.

    A frozen dev-arm manifest is planted at the counter's evidence path with one
    carrier's `declared_features` edited to a value its committed envelope does
    not observe; every envelope byte is unchanged.  The counter must exit
    non-zero with `observed_features_match_declared` false, which it can only do
    if it DERIVES the observed tuple from the envelope bytes — a counter that
    read the manifest's own `generator.tuple_check` record would pass the edited
    manifest.

    The `baseline` arm (the same tree, unedited) is run beside it: the dev arm's
    declarations agree with their envelopes in every carrier, so the baseline
    must have `observed_features_match_declared` true.  Baseline true -> hand-edit
    false is the red/green of the binding itself, and it is what makes the
    failure attributable to the edit rather than to a pre-existing mismatch.
    """
    counter = args.counter
    if not os.path.isfile(counter):
        raise ControlError('counter not found: %s' % counter)
    if not os.path.isfile(os.path.join(args.root, args.r42_dev, 'manifest.json')):
        raise ControlError('frozen dev-arm manifest not found under %s'
                           % os.path.join(args.root, args.r42_dev))

    baseline = _plant_arm(args, scratch, 'at-freeze', tag='ctl-c1-4-baseline',
                          src_rel=args.r42_dev, mutate=None)
    hand_edit = _plant_arm(args, scratch, 'at-freeze', tag='ctl-c1-4-hand-edit',
                           src_rel=args.r42_dev, mutate=_flip_one_declared_field)

    base_binding = baseline.get('observed_features_match_declared')
    edit_binding = hand_edit.get('observed_features_match_declared')
    edit = hand_edit.get('manifest_hand_edit') or {}
    ok = (base_binding is True
          and edit_binding is False
          and hand_edit['counter_exit'] != 0
          and baseline['envelopes_untouched']
          and hand_edit['envelopes_untouched']
          and edit.get('declared_before') != edit.get('declared_after'))
    return {
        'control': 'CTL-C1-4',
        'title': 'counter-side hand-edit rejection: a fabricated declaration',
        'dev_arm': args.r42_dev,
        'baseline': baseline,
        'hand_edit': hand_edit,
        'edit_target': edit,
        'baseline_observed_features_match_declared': base_binding,
        'hand_edit_observed_features_match_declared': edit_binding,
        'envelopes_untouched': (baseline['envelopes_untouched']
                                and hand_edit['envelopes_untouched']),
        'counter_exit': hand_edit['counter_exit'],
        'bindings_fired': hand_edit['bindings_fired'],
        'expected_exit': 'non-zero; observed_features_match_declared false',
        'ok': ok,
        'note': ('the edit is manifest-only (%s.%s: %r -> %r) and every envelope '
                 'byte is unchanged, so the binding can only fail if the counter '
                 'computes the observed tuple from the envelope; the unedited '
                 'baseline on the same arm keeps the binding true'
                 % (edit.get('carrier'), edit.get('field'),
                    edit.get('declared_before'), edit.get('declared_after'))),
    }


def _tuple_check_interfaces(generator, directory):
    """Yield (interface_name, argv) for each candidate tuple-check CLI."""
    for (flag,) in TUPLE_CHECK_CLIS:
        yield flag, [flag, directory]


def _module_tuple_check(generator, directory):
    """Call the generator's own check FUNCTION, in-process.

    The generator's refusal is a function over a committed directory; a control
    needs to reach it without REA and without the generator's `--run` state.
    When the CLI does not expose it, the function is imported and called with
    the same inputs the CLI would have passed.  Exit codes are mapped onto the
    generator's own vocabulary: 0 = every observed tuple equals its declared
    one, 3 = a refusal (R43's `declared_tuple_unobserved`), 2 = unusable input.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location('r43_gen_under_test', generator)
    if spec is None or spec.loader is None:
        raise ControlError('cannot import the generator as a module: %s' % generator)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    path = os.path.join(directory, 'manifest.json')
    manifest = json.load(open(path))
    carriers = manifest.get('carriers') or []
    for name in ('run_tuple_check', 'tuple_check'):
        fn = getattr(mod, name, None)
        if fn is None:
            continue
        rc = fn(directory)
        return {'interface': 'module:%s' % name, 'exit': int(rc)}
    fn = getattr(mod, 'refusal_check', None)
    if fn is None:
        raise ControlError('the generator exposes no tuple-check entry point '
                           '(no run_tuple_check/tuple_check/refusal_check)')
    verdict = fn(directory, carriers)
    missing = verdict.get('missing') or []
    unparsable = verdict.get('unparsable') or []
    if missing or unparsable:
        rc = 2
    else:
        rc = 0 if verdict.get('ok') else 3
    rows = verdict.get('rows') or []
    diffs = [{'id': r.get('id'), 'class': r.get('class'),
              'diff': r.get('diff')} for r in rows if r.get('verdict') != 'match']
    return {'interface': 'module:refusal_check', 'exit': rc,
            'mismatched': verdict.get('mismatched'),
            'carriers_checked': verdict.get('carriers_checked'),
            'diffs': diffs}


def _run_tuple_check(generator, directory):
    """Run the generator's tuple check over `directory`.

    Two interfaces are probed, in order: a CLI flag, then the generator's own
    function.  Returns (interface, exit code, detail dict, attempts).
    """
    attempts = []
    for flag, tail in _tuple_check_interfaces(generator, directory):
        argv = [sys.executable, '-I', '-B', generator] + tail
        p = subprocess.run(argv, capture_output=True, text=True, cwd=directory)
        attempts.append({'interface': 'cli:%s' % flag, 'argv': argv,
                         'exit': p.returncode,
                         'stdout_tail': p.stdout[-800:], 'stderr_tail': p.stderr[-400:]})
        if p.returncode not in (0, 1, 2, 3):
            continue
        # argparse rejects an unknown flag with exit 2 and a usage block on
        # stderr; that is "this interface does not exist", not a refusal.
        if ('unrecognized arguments' in p.stderr or 'invalid choice' in p.stderr
                or 'the following arguments are required' in p.stderr
                or p.stderr.lstrip().startswith('usage:')):
            continue
        return ('cli:%s' % flag, p.returncode,
                {'stdout_tail': p.stdout[-800:], 'stderr_tail': p.stderr[-400:]},
                attempts)
    try:
        detail = _module_tuple_check(generator, directory)
    except Exception as exc:
        attempts.append({'interface': 'module', 'error': repr(exc)})
        raise ControlError('the generator exposes no usable tuple-check '
                           'interface; attempts: %s' % json.dumps(attempts))
    attempts.append({'interface': detail['interface'], 'exit': detail['exit']})
    return (detail['interface'], detail['exit'], detail, attempts)


def _parse_check_rows(stdout):
    """Per-carrier declared/observed diffs from the check's own stdout.

    Two shapes are read:
      `REFUSE C02  combo  gap_kinds: declared [...] observed [...]`  (the
        generator's own wording: a verb, the carrier id, the class, the field)
      `C02  combo  MISMATCH` followed by an indented
        `    gap_kinds: declared [...] observed [...]`  (the standalone
        prototype's wording).

    Parsing the check's OWN output is what makes the green half independent of
    which file the check reads its observation from (`run.json` or the emitted
    `rea-full.json`).
    """
    rows = {}
    pending_id = None
    field_re = re.compile(r'([A-Za-z_]+)\s*:\s*declared\s+(.+?)\s+observed\s+(.+?)\s*$')
    for line in (stdout or '').splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        head = stripped.split()
        if len(head) >= 2 and head[-1].upper() in ('MISMATCH', 'REFUSE'):
            # `<id> <class> MISMATCH` -> the id is the first token
            pending_id = head[0]
            continue
        m = field_re.search(stripped)
        if not m:
            continue
        field, declared_raw, observed_raw = m.group(1), m.group(2), m.group(3)
        try:
            declared = ast.literal_eval(declared_raw)
            observed = ast.literal_eval(observed_raw)
        except (ValueError, SyntaxError):
            continue
        cid = None
        # `<...> <id> <class> <field>:` -- the carrier is two tokens before the
        # field token (`REFUSE C02 combo gap_kinds:`) or, when the line carries
        # only the field, the id the preceding MISMATCH/REFUSE line named.
        fi = None
        for i, tok in enumerate(head):
            if tok.split(':')[0] == field:
                fi = i
                break
        if fi is not None and fi >= 2:
            cid = head[fi - 2]
        if cid is None:
            cid = pending_id
        if cid is None:
            continue
        rows.setdefault(cid, {})[field] = (declared, observed)
    return rows


def _manifest_state(directory):
    """(manifest present, sha256) of `directory/manifest.json`."""
    path = os.path.join(directory, 'manifest.json')
    if not os.path.isfile(path):
        return False, None
    return True, sha256_file(path)


def ctl_c1_2(args, scratch):
    """CTL-C1-2 refusal red/green: the tuple check refuses an unobserved tuple."""
    generator = args.generator
    if not os.path.isfile(generator):
        raise ControlError('generator not found: %s' % generator)
    heldout = os.path.join(args.root, args.r42_heldout)
    if not os.path.isfile(os.path.join(heldout, 'manifest.json')):
        raise ControlError('round-42 held-out manifest not found under %s' % heldout)

    # RED: the committed round-42 manifest declares C02 as
    # {extractor-failure, unpublished-entry}; the envelope shows depth-limited
    # as well.  The check must refuse (exit 3) and write no manifest.
    before_present, before_sha = _manifest_state(heldout)
    iface, rc, detail, attempts = _run_tuple_check(generator, heldout)
    after_present, after_sha = _manifest_state(heldout)
    red_ok = (rc == 3 and before_sha == after_sha)
    red = {
        'interface': iface, 'exit': rc,
        'stdout_tail': detail.get('stdout_tail'),
        'stderr_tail': detail.get('stderr_tail'),
        'mismatched': detail.get('mismatched'),
        'diffs': detail.get('diffs'),
        'manifest_present_before': before_present,
        'manifest_sha256_before': before_sha,
        'manifest_present_after': after_present,
        'manifest_sha256_after': after_sha,
        'manifest_unchanged': before_sha == after_sha,
        'expected_exit': 3,
        'ok': red_ok,
    }

    # GREEN: the same check over a copy whose declared tuples equal the
    # observed ones.  The correction is taken from the CHECK'S OWN output (the
    # observed values it reported), so the green half does not depend on which
    # file the check reads its observation from.  The check must pass (exit 0).
    green_dir = os.path.join(scratch, 'ctl-c1-2-green')
    if os.path.isdir(green_dir):
        shutil.rmtree(green_dir)
    shutil.copytree(heldout, green_dir)
    gman_path = os.path.join(green_dir, 'manifest.json')
    gman = json.load(open(gman_path))
    rows = _parse_check_rows(detail.get('stdout_tail'))
    source = 'check stdout'
    if not rows:
        rows = {}
        for c in gman.get('carriers') or []:
            cid = c.get('id')
            kinds = _observed_gap_kinds(heldout).get(cid)
            if kinds is not None:
                rows.setdefault(cid, {})['gap_kinds'] = (
                    list((c.get('declared_features') or {}).get('gap_kinds') or []),
                    list(kinds))
        source = 're-derived from the emitted envelope'
    changed = []
    for c in gman.get('carriers') or []:
        cid = c.get('id')
        diff = rows.get(cid)
        if not diff:
            continue
        feats = c.get('declared_features')
        if not isinstance(feats, dict):
            continue
        for field, (_declared, observed_value) in diff.items():
            if field in feats and feats[field] != observed_value:
                feats[field] = observed_value
                changed.append('%s.%s' % (cid, field))
    with open(gman_path, 'w', encoding='utf-8') as fh:
        json.dump(gman, fh, indent=2)
        fh.write('\n')
    giface, grc, gdetail, gattempts = _run_tuple_check(generator, green_dir)
    gpresent, gsha = _manifest_state(green_dir)
    green = {
        'interface': giface, 'exit': grc,
        'stdout_tail': gdetail.get('stdout_tail'),
        'stderr_tail': gdetail.get('stderr_tail'),
        'mismatched': gdetail.get('mismatched'),
        'diffs': gdetail.get('diffs'),
        'correction_source': source,
        'declared_tuples_corrected': changed,
        'manifest_sha256_after': gsha,
        'expected_exit': 0,
        'ok': grc == 0,
    }
    return {
        'control': 'CTL-C1-2',
        'title': 'refusal: the tuple check rejects an unobserved declared tuple',
        'red': red,
        'green': green,
        'interface_attempts': attempts + gattempts,
        'expected_exit': 3,
        'ok': red_ok and green['ok'],
        'note': ('red: the committed round-42 C02 manifest declares a gap set '
                 'its own envelope does not show; the generator must refuse '
                 'with exit 3 and write no manifest.  green: the same check over '
                 'a manifest whose declared tuple equals the observed one passes '
                 '(the green the held-out run itself must produce).'),
    }


def _observed_gap_kinds(directory):
    """Observed gap kinds per carrier, re-derived from the emitted envelope.

    `rea-full.json` first (the bytes the run emitted, the source the
    generator's own check reads), `run.json` only as a fallback.
    """
    out = {}
    for name in sorted(os.listdir(directory)):
        sub = os.path.join(directory, name)
        if not os.path.isdir(sub):
            continue
        full = os.path.join(sub, 'rea-full.json')
        if os.path.isfile(full):
            try:
                doc = json.load(open(full))
            except ValueError:
                doc = None
            if isinstance(doc, dict):
                data = doc.get('data') or {}
                norm = data.get('normalized_result') or {}
                kinds = sorted({g.get('kind') for g in norm.get('extraction_gaps') or []
                                if g.get('kind')})
                if kinds:
                    out[name] = kinds
                    continue
        run = os.path.join(sub, 'run.json')
        if os.path.isfile(run):
            try:
                doc = json.load(open(run))
            except ValueError:
                continue
            if doc.get('gap_kinds') is not None:
                out[name] = list(doc['gap_kinds'])
    return out


def build_tables(args):
    """Copy the frozen round-42 control documents byte-exact into --out.

    The round-42 builder copied the LIVE `SKILL.md` into the do-nothing
    document and rebuilt the lookup rows from the dev arm.  At round-43 the live
    `SKILL.md` already carries the frozen v4 table, so a rebuild would make the
    do-nothing control the reference table (78/78) and fire the kill rule on
    the control set itself.  The documents are therefore COPIED, sha256-checked,
    and their provenance recorded.
    """
    ctl_dir = os.path.join(args.root, args.r42_controls)
    if not os.path.isdir(ctl_dir):
        raise ControlError('round-42 control directory not found: %s' % ctl_dir)
    os.makedirs(args.out, exist_ok=True)
    copied = []
    for frozen, cid, role in list(SHORTCUTS) + [REFERENCE, DO_NOTHING]:
        src = os.path.join(ctl_dir, frozen)
        if not os.path.isfile(src):
            raise ControlError('frozen control document missing: %s' % src)
        dst = os.path.join(args.out, frozen)
        shutil.copyfile(src, dst)
        if sha256_file(dst) != sha256_file(src):
            raise ControlError('copy of %s is not byte-exact' % frozen)
        copied.append({'id': cid, 'frozen_document': frozen, 'role': role,
                       'sha256': sha256_file(dst),
                       'source': '%s/%s' % (args.r42_controls, frozen)})
    return copied


def ctl_c1_3(args, scratch):
    """CTL-C1-3 shortcut controls: re-score the frozen round-42 control set."""
    receipt_path = os.path.join(args.root, args.r42_receipt)
    if not os.path.isfile(receipt_path):
        raise ControlError('round-42 receipt not found: %s' % receipt_path)
    r42 = json.load(open(receipt_path))
    devdir = os.path.join(args.root, args.r42_dev)
    envs = collect_envs(devdir)
    pairs = expected_pairs(args.eval, devdir, scratch)
    combos = combo_ids(devdir)

    ids = [envelope_id(p) for p in envs]
    n = len(ids)
    scores = {}
    for frozen, cid, role in list(SHORTCUTS) + [REFERENCE, DO_NOTHING]:
        path = os.path.join(args.out, frozen)
        if not os.path.isfile(path):
            raise ControlError('control document not built: %s' % path)
        rc, got, err = run_interpreter(args.interp, path, envs)
        matched = [i for i in ids if got.get(i) == pairs.get(i)]
        missed = [i for i in ids if i not in matched]
        old = (r42.get('scores') or {}).get(frozen) or {}
        combo_hit = sum(1 for i in ids if i in combos and got.get(i) == pairs.get(i))
        named_hit = sum(1 for i in ids if i not in combos and got.get(i) == pairs.get(i))
        entry = {
            'id': cid, 'role': role, 'document': frozen,
            'interp_exit': rc, 'matched': len(matched), 'n': n,
            'label_hits': sum(1 for i in ids
                              if got.get(i, ('', ''))[0] == pairs.get(i, ('', ''))[0]),
            'action_hits': sum(1 for i in ids
                               if got.get(i, ('', ''))[1] == pairs.get(i, ('', ''))[1]),
            'combo': [combo_hit, len(combos)],
            'named': [named_hit, n - len(combos)],
            'r42_receipt_matched': old.get('matched'),
            'r42_receipt_n': old.get('n'),
            'r42_receipt_combo': old.get('combo'),
            'r42_receipt_named': old.get('named'),
            'r42_receipt_missed_set_equal':
                old.get('missed') is not None and set(old['missed']) == set(missed),
            'reproduces_r42_receipt': (old.get('matched') == len(matched)
                                       and old.get('n') == n),
            'missed': missed,
            'reaches_target': len(matched) == n,
            'stderr_tail': err if rc else '',
        }
        scores[cid] = entry

    controls = [cid for cid, e in scores.items() if e['role'] == 'control'
                and cid != DO_NOTHING[1]]
    witness = [cid for cid, e in scores.items() if e['role'] == 'witness']
    at_target = [cid for cid in controls if scores[cid]['reaches_target']]
    witness_at_target = [cid for cid in witness if scores[cid]['reaches_target']]
    not_reproduced = [cid for cid in controls
                      if not scores[cid]['reproduces_r42_receipt']]
    # the do-nothing document must still refuse the v4 grammar (exit 2)
    donothing = scores[DO_NOTHING[1]]
    donothing_ok = donothing['interp_exit'] == 2 and donothing['matched'] == 0
    ok = (not at_target and not not_reproduced and witness_at_target
          and donothing_ok)
    return {
        'control': 'CTL-C1-3',
        'title': 'shortcut controls re-scored on the frozen round-42 dev arm',
        'dev_arm': args.r42_dev,
        'n': n,
        'combo_carriers': len(combos),
        'named_carriers': n - len(combos),
        'r42_receipt': args.r42_receipt,
        'r42_receipt_combo_column_degenerate': all(
            (v.get('combo') or [0, 0]) == [0, 0]
            for v in (r42.get('scores') or {}).values()),
        'scores': scores,
        'controls': controls,
        'witness': witness,
        'controls_at_target': at_target,
        'witness_at_target': witness_at_target,
        'controls_not_reproducing_r42_receipt': not_reproduced,
        'do_nothing_still_refuses': donothing_ok,
        'expected_exit': 'no control at the target; the witness at the target',
        'ok': ok,
        'note': ('the round-42 receipt was computed on two scratch slices with no '
                 'manifest.json, so its combo/named split is degenerate ([0,0] / '
                 '[m,78]); the matched numbers reproduce exactly and the split is '
                 'recomputed here from the committed dev arm manifest'),
    }


# ------------------------------------------------------------------ driver
CONTROLS = {
    'CTL-C1-0': ctl_c1_0,
    'CTL-C1-1': ctl_c1_1,
    'CTL-C1-2': ctl_c1_2,
    'CTL-C1-3': ctl_c1_3,
    'CTL-C1-4': ctl_c1_4,
}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='R43-C1 controls: build the round-43 control tables and '
                    'score every control.')
    ap.add_argument('--root', required=True, help='lane root')
    ap.add_argument('--out', required=True, help='control table directory')
    ap.add_argument('--json-out', required=True, help='summary receipt')
    ap.add_argument('--receipts', default=None,
                    help='per-control receipt directory (default: <out>/receipts)')
    ap.add_argument('--ctl', default=None,
                    help='comma separated control ids to run (default: all)')
    ap.add_argument('--build', action='store_true',
                    help='build the control tables (the controls themselves copy '
                         'the frozen round-42 documents byte-exact)')
    ap.add_argument('--counter', default=None,
                    help='the round-43 counter (default: tools/round-43/c1-counter.py)')
    ap.add_argument('--generator', default=None,
                    help='the round-43 generator (default: '
                         'tools/round-43/heldout-gen-v4r43.py)')
    ap.add_argument('--interp', default=None,
                    help='the frozen interpreter (default: '
                         'tools/round-42/sqfs-triage-v4.py)')
    ap.add_argument('--eval', default=None,
                    help='the frozen evaluator (default: '
                         'tools/round-42/indep-eval-v4.py)')
    ap.add_argument('--dev', default=None,
                    help='the frozen dev arm (default: %s)' % R42_DEV)
    ap.add_argument('--r42-dev', default=R42_DEV)
    ap.add_argument('--r42-controls', default=R42_CONTROLS)
    ap.add_argument('--r42-receipt', default=R42_RECEIPT)
    ap.add_argument('--r42-heldout', default=R42_HELDOUT)
    ap.add_argument('--evidence-dir', default=R43_EVIDENCE,
                    help='the evidence path the counter reads and the control '
                         'plants into')
    ap.add_argument('--freeze', required=True,
                    help='the freeze commit the controls are scored against')
    ap.add_argument('--scratch', default=None,
                    help='scratch directory (default: a temporary directory under '
                         'TMPDIR)')
    a = ap.parse_args(argv)

    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        raise ControlError('lane root not found: %s' % root)
    a.root = root
    a.counter = a.counter or os.path.join(root, 'tools/round-43/c1-counter.py')
    a.generator = a.generator or os.path.join(root, 'tools/round-43/heldout-gen-v4r43.py')
    a.interp = a.interp or os.path.join(root, 'tools/round-42/sqfs-triage-v4.py')
    a.eval = a.eval or os.path.join(root, 'tools/round-42/indep-eval-v4.py')
    a.dev = a.dev or os.path.join(root, a.r42_dev)
    a.out = os.path.abspath(a.out)
    a.json_out = os.path.abspath(a.json_out)
    a.receipts = os.path.abspath(a.receipts) if a.receipts \
        else os.path.join(a.out, 'receipts')
    for p in (a.interp, a.eval):
        if not os.path.isfile(p):
            raise ControlError('frozen tool not found: %s' % p)

    os.makedirs(a.out, exist_ok=True)
    os.makedirs(a.receipts, exist_ok=True)
    os.makedirs(os.path.dirname(a.json_out) or '.', exist_ok=True)

    scratch = a.scratch
    tmp = None
    if not scratch:
        tmp = tempfile.mkdtemp(prefix='r43-c1-controls-')
        scratch = tmp
    else:
        scratch = os.path.abspath(scratch)
        os.makedirs(scratch, exist_ok=True)

    selected = [c.strip() for c in a.ctl.split(',')] if a.ctl else list(CONTROLS)
    unknown = [c for c in selected if c not in CONTROLS]
    if unknown:
        raise ControlError('unknown control id(s): %s' % ', '.join(unknown))

    summary = {
        'tool': 'c2-controls-r43.py',
        'round': 43,
        'claim': 'R43-C1',
        'lane_root': root,
        'freeze': a.freeze,
        'controls_selected': selected,
        'counter': a.counter,
        'generator': a.generator,
        'interpreter': a.interp,
        'evaluator': a.eval,
        'dev_arm': a.dev,
        'out': a.out,
        'receipts': a.receipts,
        'control_tables': [],
        'controls': {},
        'errors': [],
    }
    try:
        # the control tables are the frozen round-42 documents, copied
        # byte-exact; they are built whether or not CTL-C1-3 is selected.
        summary['control_tables'] = build_tables(a)
        for cid in selected:
            try:
                summary['controls'][cid] = CONTROLS[cid](a, scratch)
            except ControlError as exc:
                summary['errors'].append({'control': cid, 'error': str(exc)})
                summary['controls'][cid] = {'control': cid, 'ok': False,
                                           'error': str(exc)}
            summary['controls'][cid]['receipt'] = os.path.join(
                a.receipts, '%s.json' % cid)
            with open(summary['controls'][cid]['receipt'], 'w') as fh:
                json.dump(summary['controls'][cid], fh, indent=1, sort_keys=True)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)

    ok_all = all(summary['controls'][c].get('ok') for c in selected)
    at_target = []
    for cid, entry in summary['controls'].items():
        at_target.extend(entry.get('controls_at_target') or [])
    summary['controls_at_target'] = at_target
    summary['kill_rule_fires'] = bool(at_target)
    summary['ok'] = ok_all and not at_target
    with open(a.json_out, 'w') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)

    for cid in selected:
        e = summary['controls'][cid]
        if 'error' in e:
            print('%-10s ERROR %s' % (cid, e['error']))
            continue
        print('%-10s ok=%s  %s' % (cid, e.get('ok'), e.get('title')))
        if cid == 'CTL-C1-1':
            print('           counter_exit=%s  bindings_fired=%s'
                  % (e.get('counter_exit'), e.get('bindings_fired')))
        if cid == 'CTL-C1-2':
            print('           red exit=%s (manifest unchanged=%s)  green exit=%s'
                  % ((e.get('red') or {}).get('exit'),
                     (e.get('red') or {}).get('manifest_unchanged'),
                     (e.get('green') or {}).get('exit')))
        if cid == 'CTL-C1-3':
            for k, v in sorted(e.get('scores', {}).items()):
                print('           %-26s exit=%d matched=%d/%d combo=%s named=%s '
                      'reproduces_r42=%s at_target=%s'
                      % (k, v['interp_exit'], v['matched'], v['n'], v['combo'],
                         v['named'], v['reproduces_r42_receipt'],
                         v['reaches_target']))
    print('kill_rule_fires', summary['kill_rule_fires'])
    if summary['errors']:
        return 2
    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except ControlError as exc:
        sys.stderr.write('c2-controls-r43.py: %s\n' % exc)
        sys.exit(2)
