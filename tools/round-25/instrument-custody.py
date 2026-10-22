#!/usr/bin/env python3
"""Explicit caller-selected Git instrument-reference custody checker (round 25).

Implements the frozen consumer contract of
corpus/evidence/round-25/oracle/contract.json:

    python3 -I -B tools/round-25/instrument-custody.py \
        --root <repository-top> --request-json <literal-JSON>

The checker reads immutable Git objects of exactly one repository top: tree
entries, blob bytes and commit history metadata.  It never executes an
instrument, never opens a claims file for meaning, and never consults an
oracle, test, ruler, gate, fixture or case-keyed expected answer.  Every
verdict carries scope "explicit_reference_custody_only" plus the primary
finding label fixed by the contract.

Decision order (contract deterministic_primary_order); the first hit decides
the finding and the process exit:

  1 request_invalid                       exit 2
  2 reference_unresolved | reference_unsupported   exit 2
  3 measured_commit_unavailable           exit 2
  4 freeze_parent_unsupported | claims_history_unsupported | freeze_mismatch  exit 2
  5 instrument_absent (exit 1) | instrument_nonregular (exit 2)
  6 instrument_not_prior                  exit 1
  7 pin_mismatch                          exit 1
  8 supersession_commit_unavailable       exit 2
  9 supersession_not_revision             exit 1
 10 supersession_digest_mismatch          exit 1
 11 revision_undisclosed                  exit 1
 12 clean                                 exit 0

A declared freeze commit is classified by its real parent count before any
claims-history or first-add classification, so a two-parent freeze is always
freeze_parent_unsupported and never competes with claims_history_unsupported.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SCOPE = 'explicit_reference_custody_only'
SCHEMA = 'kaidoku-r25-instrument-custody-v1'

EXIT_CODES = {
    'clean': 0,
    'instrument_absent': 1,
    'instrument_not_prior': 1,
    'pin_mismatch': 1,
    'supersession_not_revision': 1,
    'supersession_digest_mismatch': 1,
    'revision_undisclosed': 1,
    'request_invalid': 2,
    'reference_unresolved': 2,
    'reference_unsupported': 2,
    'measured_commit_unavailable': 2,
    'freeze_mismatch': 2,
    'freeze_parent_unsupported': 2,
    'claims_history_unsupported': 2,
    'instrument_nonregular': 2,
    'supersession_commit_unavailable': 2,
    'could_not_evaluate': 2,
}

REQUEST_MEMBERS = frozenset(
    ('claims_file', 'freeze', 'measured', 'reference', 'sha256', 'supersessions'))
SUPERSESSION_MEMBERS = frozenset(('commit', 'sha256', 'reason'))
CLAIMS_FILE_PATTERN = re.compile(r'^\.ufo/waves/round-[0-9]+/claims\.json$')
COMMIT_PATTERN = re.compile(r'^[0-9a-f]{40}$')
DIGEST_PATTERN = re.compile(r'^[0-9a-f]{64}$')
COMPONENT_PATTERN = re.compile(r'^[A-Za-z0-9_.-]+$')
SUPPORTED_PREFIXES = ('./', '<LANE>/', '$LANE/')
SUPPORTED_SUFFIXES = ('.py', '.sh', '.js', '.mjs', '.ts')
REGULAR_MODES = ('100644', '100755')


class Verdict(Exception):
    """Primary precedence stop: the first verdict raised is the reported one."""

    def __init__(self, finding, detail='', extra=None):
        super().__init__(finding)
        self.finding = finding
        self.detail = detail
        self.extra = extra or {}


class GitUnavailable(Exception):
    """A Git read could not be completed, so custody is not evaluable."""


def git_environment():
    """Neutralise every inherited Git variable, then pin read-only settings.

    All GIT_* variables are dropped, not a sampled subset, so inherited
    routing (GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR, GIT_INDEX_FILE,
    GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_NAMESPACE),
    inherited configuration counts and replacement metadata cannot reach any
    Git subprocess.  The retained settings disable system/global
    configuration, hooks, attributes, object replacement, lazy fetch and
    interactive prompts, and force literal pathspecs.
    """
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    environment.update({
        'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_SYSTEM': '/dev/null',
        'GIT_CONFIG_GLOBAL': '/dev/null',
        'GIT_CONFIG_COUNT': '2',
        'GIT_CONFIG_KEY_0': 'core.hooksPath',
        'GIT_CONFIG_VALUE_0': '/dev/null',
        'GIT_CONFIG_KEY_1': 'core.attributesFile',
        'GIT_CONFIG_VALUE_1': '/dev/null',
        'GIT_NO_REPLACE_OBJECTS': '1',
        'GIT_NO_LAZY_FETCH': '1',
        'GIT_LITERAL_PATHSPECS': '1',
        'GIT_OPTIONAL_LOCKS': '0',
        'GIT_TERMINAL_PROMPT': '0',
    })
    return environment


class GitReader:
    """Read-only Git access to one repository top under a neutral environment."""

    def __init__(self, root):
        self.root = root
        self.environment = git_environment()

    def _run(self, arguments, payload=None):
        return subprocess.run(
            ['git', '-C', self.root] + list(arguments),
            env=self.environment,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def _read(self, label, arguments, payload=None):
        completed = self._run(arguments, payload)
        if completed.returncode != 0:
            raise GitUnavailable('git_read_failed:' + label)
        return completed.stdout

    def require_repository_top(self):
        completed = self._run(['rev-parse', '--show-toplevel'])
        if completed.returncode != 0:
            raise GitUnavailable('root_not_repository')
        top = completed.stdout.decode('utf-8', 'replace').strip()
        if not top or os.path.realpath(top) != self.root:
            raise GitUnavailable('root_not_repository_top')

    def commit_exists(self, commit):
        return self._run(['cat-file', '-e', commit + '^{commit}']).returncode == 0

    def commit_parents(self, commit):
        output = self._read('rev-list',
                            ['rev-list', '--parents', '-n', '1', commit])
        parts = output.decode('ascii', 'replace').split()
        return parts[1:] if parts else []

    def is_ancestor(self, ancestor, descendant):
        completed = self._run(['merge-base', '--is-ancestor', ancestor, descendant])
        if completed.returncode not in (0, 1):
            raise GitUnavailable('git_read_failed:merge-base')
        return completed.returncode == 0

    def commit_list(self, start, exclude=None):
        """Ordered (commit, parents) pairs reachable from start."""
        arguments = ['rev-list', '--topo-order', '--reverse', '--parents', start]
        if exclude is not None:
            arguments += ['--not', exclude]
        output = self._read('rev-list', arguments)
        listing = []
        for line in output.decode('ascii', 'replace').splitlines():
            parts = line.split()
            if parts:
                listing.append((parts[0], parts[1:]))
        return listing

    def path_entry(self, commit, path):
        """(mode, type, object id) of the exact path, or None when absent.

        A failed Git read is never absence: it raises GitUnavailable so the
        verdict stays could_not_evaluate instead of a guessed absent or
        clean.  A successful ls-tree with an empty result is a real absence.
        """
        completed = self._run(['ls-tree', '-z', '--full-tree', commit, '--', path])
        if completed.returncode != 0:
            raise GitUnavailable('git_read_failed:ls-tree')
        for record in completed.stdout.split(b'\0'):
            if not record:
                continue
            meta, tab, name = record.partition(b'\t')
            if not tab:
                continue
            fields = meta.split(b' ')
            if len(fields) != 3:
                continue
            if name.decode('utf-8', 'replace') == path:
                return (fields[0].decode('ascii'),
                        fields[1].decode('ascii'),
                        fields[2].decode('ascii'))
        kind = self.object_kind(commit + ':' + path)
        if kind is not None and kind[1] == 'tree':
            return ('040000', 'tree', kind[0])
        return None

    def object_kind(self, expression):
        """(object id, type) of an object expression, or None when absent.

        A failed Git read raises GitUnavailable; a successful batch-check
        reporting 'missing' is a real absence.
        """
        completed = self._run(['cat-file', '--batch-check'],
                               (expression + '\n').encode('ascii'))
        if completed.returncode != 0:
            raise GitUnavailable('git_read_failed:cat-file')
        fields = completed.stdout.decode('utf-8', 'replace').strip().split()
        if len(fields) < 2 or fields[-1] in ('missing', 'ambiguous'):
            return None
        return (fields[0], fields[1])

    def read_blob(self, commit, path):
        return self._read('cat-file', ['cat-file', 'blob', commit + ':' + path])

    def _diff_candidates(self, commits, path):
        """Commits whose tree diff touches the exact path or anything below it."""
        if not commits:
            return set()
        payload = []
        for commit, parents in commits:
            if parents:
                payload.append(commit + ' ' + parents[0])
            else:
                payload.append(commit)
        completed = self._run(
            ['diff-tree', '--stdin', '-r', '--raw', '--no-abbrev',
             '--no-renames', '--', path],
            ('\n'.join(payload) + '\n').encode('ascii'))
        if completed.returncode != 0:
            raise GitUnavailable('git_read_failed:diff-tree')
        candidates = set()
        current = None
        for line in completed.stdout.split(b'\n'):
            if not line:
                continue
            if line.startswith(b':'):
                if current is not None:
                    candidates.add(current)
            else:
                fields = line.split()
                current = fields[0].decode('ascii', 'replace') if fields else None
        return candidates

    def path_changes(self, commits, path):
        """Exact-path changes of the given commits against their first parent.

        Each returned record is (commit, parents, status, parent entry, entry)
        with status 'A', 'D' or 'M'.
        """
        candidates = self._diff_candidates(commits, path)
        changes = []
        for commit, parents in commits:
            if commit not in candidates:
                continue
            entry = self.path_entry(commit, path)
            parent_entry = self.path_entry(parents[0], path) if parents else None
            if entry == parent_entry:
                continue
            if entry is None:
                status = 'D'
            elif parent_entry is None:
                status = 'A'
            else:
                status = 'M'
            changes.append((commit, parents, status, parent_entry, entry))
        return changes


def reject_duplicate_members(pairs):
    """Object hook that rejects duplicate JSON member names."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate_member')
        result[key] = value
    return result


def parse_request(text):
    """Validate the closed request schema; every rejection is request_invalid."""
    try:
        parsed = json.loads(text, object_pairs_hook=reject_duplicate_members)
    except ValueError:
        raise Verdict('request_invalid', 'malformed_json')
    if not isinstance(parsed, dict):
        raise Verdict('request_invalid', 'request_not_object')
    if set(parsed) != REQUEST_MEMBERS:
        raise Verdict('request_invalid', 'request_member_set')
    claims_file = parsed['claims_file']
    if not isinstance(claims_file, str) or not CLAIMS_FILE_PATTERN.fullmatch(claims_file):
        raise Verdict('request_invalid', 'claims_file_path')
    freeze = parsed['freeze']
    if not isinstance(freeze, str) or not COMMIT_PATTERN.fullmatch(freeze):
        raise Verdict('request_invalid', 'freeze_commit')
    measured = parsed['measured']
    if not isinstance(measured, str) or not COMMIT_PATTERN.fullmatch(measured):
        raise Verdict('request_invalid', 'measured_commit')
    reference = parsed['reference']
    if not isinstance(reference, str):
        raise Verdict('request_invalid', 'reference_type')
    digest = parsed['sha256']
    if not isinstance(digest, str) or not DIGEST_PATTERN.fullmatch(digest):
        raise Verdict('request_invalid', 'sha256_digest')
    supersessions = parsed['supersessions']
    if not isinstance(supersessions, list):
        raise Verdict('request_invalid', 'supersessions_type')
    entries = []
    seen = set()
    for item in supersessions:
        if not isinstance(item, dict):
            raise Verdict('request_invalid', 'supersession_type')
        if set(item) != SUPERSESSION_MEMBERS:
            raise Verdict('request_invalid', 'supersession_member_set')
        commit = item['commit']
        if not isinstance(commit, str) or not COMMIT_PATTERN.fullmatch(commit):
            raise Verdict('request_invalid', 'supersession_commit')
        entry_digest = item['sha256']
        if not isinstance(entry_digest, str) or not DIGEST_PATTERN.fullmatch(entry_digest):
            raise Verdict('request_invalid', 'supersession_sha256')
        reason = item['reason']
        if not isinstance(reason, str) or not reason.strip():
            raise Verdict('request_invalid', 'supersession_reason')
        if commit in seen:
            raise Verdict('request_invalid', 'supersession_duplicate_commit')
        seen.add(commit)
        entries.append((commit, entry_digest, reason))
    return {
        'claims_file': claims_file,
        'freeze': freeze,
        'measured': measured,
        'reference': reference,
        'sha256': digest,
        'supersessions': entries,
    }


def normalize_reference(value):
    """Strip at most one supported prefix and validate the lane-relative path."""
    text = value
    for prefix in SUPPORTED_PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    if not text:
        raise Verdict('reference_unsupported', 'reference_empty')
    components = text.split('/')
    for component in components:
        if not component or component in ('.', '..'):
            raise Verdict('reference_unsupported', 'reference_component')
        if not COMPONENT_PATTERN.fullmatch(component):
            raise Verdict('reference_unsupported', 'reference_component_charset')
        if component.startswith('-'):
            raise Verdict('reference_unsupported', 'reference_component_leading_dash')
    if len(components) < 2:
        raise Verdict('reference_unresolved', 'reference_bare_name')
    if not any(text.lower().endswith(suffix) for suffix in SUPPORTED_SUFFIXES):
        raise Verdict('reference_unsupported', 'reference_suffix')
    return text


def evaluate(git, request_text, evidence):
    """Run the custody checks in the frozen precedence order."""
    request = parse_request(request_text)
    evidence['claims_file'] = request['claims_file']
    evidence['requested_sha256'] = request['sha256']
    reference = normalize_reference(request['reference'])
    evidence['reference'] = reference
    measured = request['measured']
    freeze = request['freeze']

    if not git.commit_exists(measured):
        raise Verdict('measured_commit_unavailable', 'measured_commit_absent')
    evidence['measured'] = measured
    if not git.commit_exists(freeze):
        raise Verdict('freeze_mismatch', 'freeze_commit_absent')
    evidence['freeze'] = freeze

    freeze_parents = git.commit_parents(freeze)
    if len(freeze_parents) != 1:
        raise Verdict('freeze_parent_unsupported', 'freeze_parent_count')

    history = git.commit_list(measured)
    claims_changes = git.path_changes(history, request['claims_file'])
    additions = [change for change in claims_changes if change[2] == 'A']
    merges = [change for change in claims_changes if len(change[1]) > 1]
    if merges or len(additions) != 1:
        raise Verdict('claims_history_unsupported', 'claims_history_shape')
    first_add = additions[0][0]
    evidence['resolved_first_add'] = first_add
    if first_add != freeze:
        raise Verdict('freeze_mismatch', 'freeze_is_not_claims_first_add')
    if not git.is_ancestor(freeze, measured):
        raise Verdict('freeze_mismatch', 'freeze_not_ancestor_of_measured')

    entry = git.path_entry(freeze, reference)
    if entry is None:
        raise Verdict('instrument_absent', 'instrument_absent_at_freeze')
    if entry[0] not in REGULAR_MODES:
        raise Verdict('instrument_nonregular', 'instrument_entry_not_regular')
    evidence['freeze_blob'] = entry[2]
    evidence['freeze_mode'] = entry[0]
    parent_entry = git.path_entry(freeze_parents[0], reference)
    if parent_entry is None:
        raise Verdict('instrument_not_prior', 'instrument_absent_in_freeze_parent')
    if parent_entry[0] != entry[0] or parent_entry[2] != entry[2]:
        raise Verdict('instrument_not_prior', 'instrument_changed_in_freeze')
    evidence['parent_blob'] = parent_entry[2]
    evidence['parent_mode'] = parent_entry[0]

    frozen_sha256 = hashlib.sha256(git.read_blob(freeze, reference)).hexdigest()
    evidence['frozen_sha256'] = frozen_sha256
    if frozen_sha256 != request['sha256']:
        raise Verdict('pin_mismatch', 'frozen_digest_mismatch')

    post_freeze = git.commit_list(measured, exclude=freeze)
    revisions = git.path_changes(post_freeze, reference)
    revision_commits = [change[0] for change in revisions]
    evidence['revision_commits'] = revision_commits

    for commit, digest, reason in request['supersessions']:
        if not git.commit_exists(commit):
            raise Verdict('supersession_commit_unavailable', 'supersession_commit_absent')
    for commit, digest, reason in request['supersessions']:
        if commit not in revision_commits:
            raise Verdict('supersession_not_revision', 'supersession_not_a_path_revision')
    verified = []
    for commit, digest, reason in request['supersessions']:
        post_image = git.path_entry(commit, reference)
        actual = None
        if post_image is not None and post_image[0] in REGULAR_MODES:
            actual = hashlib.sha256(git.read_blob(commit, reference)).hexdigest()
        if actual is None or actual != digest:
            evidence['verified_supersessions'] = verified
            raise Verdict('supersession_digest_mismatch', 'supersession_digest_mismatch')
        verified.append({'commit': commit, 'sha256': actual})
    evidence['verified_supersessions'] = verified

    disclosed = set(supersession[0] for supersession in request['supersessions'])
    undisclosed = [commit for commit in revision_commits if commit not in disclosed]
    if undisclosed:
        raise Verdict('revision_undisclosed', 'post_freeze_revision_not_disclosed',
                      {'undisclosed_commits': undisclosed})
    return 'clean'


def verdict_payload(finding, detail='', evidence=None, extra=None):
    payload = {
        'schema': SCHEMA,
        'finding': finding,
        'scope': SCOPE,
    }
    if detail:
        payload['error'] = detail
    if evidence:
        payload.update(evidence)
    if extra:
        payload.update(extra)
    return payload


def emit(payload, code):
    sys.stdout.write(json.dumps(payload, sort_keys=True) + '\n')
    sys.stdout.flush()
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Check the Git custody of one explicit instrument reference.')
    parser.add_argument('--root', required=True,
                        help='repository top to read, verified as the real top')
    parser.add_argument('--request-json', required=True,
                        help='literal request JSON for one custody question')
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as exit_request:
        if exit_request.code == 0:
            raise
        return emit(verdict_payload('request_invalid', 'invalid_invocation'), 2)

    evidence = {}
    try:
        git = GitReader(os.path.realpath(arguments.root))
        git.require_repository_top()
        finding = evaluate(git, arguments.request_json, evidence)
    except Verdict as stop:
        payload = verdict_payload(stop.finding, stop.detail, evidence, stop.extra)
        return emit(payload, EXIT_CODES.get(stop.finding, 2))
    except GitUnavailable as unavailable:
        payload = verdict_payload('could_not_evaluate', str(unavailable), evidence)
        return emit(payload, EXIT_CODES['could_not_evaluate'])
    except (OSError, ValueError, UnicodeError, RecursionError,
            subprocess.SubprocessError) as failure:
        payload = verdict_payload('could_not_evaluate', type(failure).__name__, evidence)
        return emit(payload, EXIT_CODES['could_not_evaluate'])
    return emit(verdict_payload(finding, '', evidence), EXIT_CODES[finding])


if __name__ == '__main__':
    raise SystemExit(main())
