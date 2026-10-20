#!/usr/bin/env python3
"""Round-20 immutable controls for no-harm coverage, depth, and history.
Usage: python3 -I -B controls-r20.py BASE SOURCE; --selftest exercises the
control rules without Git, network, target execution, or external writes.
0 controls hold, 1 a control found harm, 2 unusable input. This is not a
semantic audit of the corpus.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = str(pathlib.Path(__file__).resolve().parents[3])
QUALITY_ROWS = 22
RUNS_PREDICTIONS = re.compile(
    r'^\.ufo/waves/round-1[789]/(?:runs|predictions)/')
ROUTED_FIX_FILES = {
    '.ufo/gates/custody-pair/custody-pair.py',
    '.ufo/gates/citation-drift/citation-drift-probe.py',
    '.ufo/gates/c1-census-v10.py',
    '.ufo/waves/round-17/tools/receipt-validate.py',
    '.ufo/waves/round-18/tools/head-rev-lint.py',
    '.ufo/waves/round-18/tools/jj-red-before.py',
    '.ufo/waves/round-19/tools/wave-outcomes.py',
}
SOURCE_MUTABLE_CELLS = {'status', 'recheck', 'used-by'}
CITATION_PATTERN = re.compile(
    r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?')


def git(*args):
    return subprocess.check_output(
        ['git', '--no-optional-locks', '-C', ROOT, *args],
        env={k: v for k, v in os.environ.items()
             if not k.startswith(('GIT_', 'JJ_'))})


def blob(rev, path):
    return git('show', f'{rev}:{path}')


def paths(rev):
    return set(git('ls-tree', '-r', '--name-only', rev).decode().splitlines())


def analyze_coverage(files, readme, skill, read_knowledge):
    coverage_section = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', coverage_section))
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    resolved = 0
    for rule in rules:
        refs = CITATION_PATTERN.findall(rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(read_knowledge('corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except (KeyError, subprocess.CalledProcessError):
                valid = False
        resolved += valid
    if not files or not rules:
        raise ValueError('command_a_empty_denominator')
    return {
        'mapped': len(files & mapped),
        'knowledge_files': len(files),
        'missing': sorted(files - mapped),
        'dangling': sorted(mapped - files),
        'citation_resolved_rules': resolved,
        'rule_blocks': len(rules),
        'coverage_score': round(10 * len(files & mapped) / len(files), 2),
        'depth_score': round(10 * resolved / len(rules), 2),
    }


def command_a(rev, names):
    # Match SCORECARD.md command A: only Git-object reads differ in packaging.
    files = {pathlib.PurePosixPath(p).stem for p in names
             if p.startswith('corpus/knowledge/') and p.endswith('.md')}
    readme = blob(rev, 'corpus/README.md').decode()
    skill = blob(rev, 'SKILL.md').decode()
    return analyze_coverage(
        files, readme, skill, lambda path: blob(rev, path))


def section_rows(data, heading, row_pattern):
    rows = []
    inside = False
    found = False
    for line in data.splitlines(keepends=True):
        body = line.rstrip(b'\r\n')
        if not inside:
            if body == heading:
                inside = True
                found = True
            continue
        if body.startswith(b'## '):
            break
        if row_pattern.match(line):
            rows.append(line)
    if not found:
        raise ValueError('missing_section:' + heading.decode('ascii'))
    return rows


def quality_rows(data):
    return section_rows(data, b'## Admission criteria',
                        re.compile(rb'^\|\s*\d+\s*\|'))


def quality_controls(before, after):
    old_rows = quality_rows(before)
    new_rows = quality_rows(after)
    row_re = re.compile(rb'^\|\s*(\d+)\s*\|')

    def indexed(rows):
        result, duplicates, order = {}, set(), []
        for row in rows:
            match = row_re.match(row)
            if not match:
                continue
            number = int(match.group(1))
            order.append(number)
            if number <= QUALITY_ROWS and number in result:
                duplicates.add(number)
            result[number] = row
        return result, duplicates, order

    old, old_duplicates, old_order = indexed(old_rows)
    new, new_duplicates, new_order = indexed(new_rows)
    expected = list(range(1, QUALITY_ROWS + 1))
    present = (all(number in old for number in expected) and
               all(number in new for number in expected) and
               not old_duplicates and not new_duplicates)
    changed = [number for number in expected
               if old.get(number) != new.get(number)]
    ordered = ([number for number in old_order if number <= QUALITY_ROWS] == expected and
               [number for number in new_order if number <= QUALITY_ROWS] == expected)
    return {
        'required_rows_present_once': present,
        'first_22_ordered': ordered,
        'first_22_byte_identical': present and not changed,
        'changed_rows': changed,
        'before_rows': len(old_rows),
        'after_rows': len(new_rows),
    }


def split_table_row(line):
    text = line.strip()
    if not (text.startswith('|') and text.endswith('|')):
        return []
    cells, current, escaped = [], [], False
    for char in text[1:-1]:
        if char == '|' and not escaped:
            cells.append(''.join(current).strip())
            current = []
            escaped = False
        else:
            current.append(char)
            if char == '\\':
                escaped = not escaped
            else:
                escaped = False
    cells.append(''.join(current).strip())
    return cells


def source_table(data):
    lines = data.decode().splitlines()
    header_index = None
    header = None
    for index, line in enumerate(lines):
        cells = split_table_row(line)
        if cells and cells[0].lower() == 'id':
            header_index, header = index, [cell.lower() for cell in cells]
            break
    if header_index is None:
        raise ValueError('missing_sources_registry_header')
    rows = []
    for line in lines[header_index + 1:]:
        if not line.strip():
            break
        if not line.lstrip().startswith('|'):
            break
        cells = split_table_row(line)
        if not cells:
            if re.match(r'^\s*\|\s*S\d+\b', line):
                raise ValueError('malformed_sources_row')
            break
        if re.fullmatch(r':?-+:?', cells[0]):
            continue
        if not re.fullmatch(r'S\d+', cells[0]):
            break
        if len(cells) != len(header):
            raise ValueError('sources_row_width:' + cells[0])
        rows.append((cells[0], cells))
    required = {'id', 'status', 'recheck', 'used-by'}
    if not required.issubset(header):
        raise ValueError('sources_mutable_columns_missing')
    return header, rows


def compare_sources(before, after):
    old_header, old_rows = source_table(before)
    new_header, new_rows = source_table(after)
    old_ids = [sid for sid, _ in old_rows]
    new_ids = [sid for sid, _ in new_rows]
    old_by_id = {sid: cells for sid, cells in old_rows}
    new_by_id = {sid: cells for sid, cells in new_rows}
    duplicate_ids = (len(set(old_ids)) != len(old_ids) or
                     len(set(new_ids)) != len(new_ids))
    changed_cells = []
    missing_ids = []
    disallowed = []
    allowed_indices = {index for index, name in enumerate(old_header)
                       if name in SOURCE_MUTABLE_CELLS}
    for sid, old_cells in old_rows:
        new_cells = new_by_id.get(sid)
        if new_cells is None:
            missing_ids.append(sid)
            continue
        for index in range(max(len(old_cells), len(new_cells))):
            old_value = old_cells[index] if index < len(old_cells) else None
            new_value = new_cells[index] if index < len(new_cells) else None
            if old_value == new_value:
                continue
            column = old_header[index] if index < len(old_header) else None
            change = {
                'id': sid,
                'column': column,
                'old': old_value,
                'new': new_value,
                'allowed': index in allowed_indices,
            }
            change['display'] = f'{sid}.{column}: {old_value!r} -> {new_value!r}'
            changed_cells.append(change)
            if index not in allowed_indices:
                disallowed.append(change['display'])
    append_only = (not duplicate_ids and
                   new_ids[:len(old_ids)] == old_ids)
    appended_rows = [
        {'id': sid, 'cells': cells}
        for sid, cells in new_rows[len(old_ids):]
    ] if append_only else [
        {'id': sid, 'cells': cells}
        for sid, cells in new_rows if sid not in old_by_id
    ]
    checks = {
        'header_unchanged': old_header == new_header,
        'rows_append_only': append_only,
        'existing_cells_limited_to_status_recheck_used_by':
            not missing_ids and not disallowed,
    }
    details = {
        'before_rows': len(old_rows),
        'after_rows': len(new_rows),
        'missing_ids': missing_ids,
        'appended_rows': appended_rows,
        'changed_cells': changed_cells,
        'disallowed_changes': disallowed,
    }
    return checks, details


def tracked_path_changes(before_paths, after_paths, read_before, read_after):
    added = sorted(after_paths - before_paths)
    deleted = sorted(before_paths - after_paths)
    changed = sorted(path for path in before_paths & after_paths
                     if read_before(path) != read_after(path))
    return {'added': added, 'deleted': deleted, 'changed': changed}


def evaluate(base, source):
    old_paths, new_paths = paths(base), paths(source)
    checks, details = {}, {}

    for path in ('LOG.md', 'SCORECARD.md'):
        old_bytes, new_bytes = blob(base, path), blob(source, path)
        checks['prefix:' + path] = new_bytes.startswith(old_bytes)
        details[path] = {'base_bytes': len(old_bytes), 'source_bytes': len(new_bytes)}

    quality = quality_controls(blob(base, 'corpus/QUALITY.md'),
                               blob(source, 'corpus/QUALITY.md'))
    checks['quality-rows-1-22-present-once'] = quality['required_rows_present_once']
    checks['quality-rows-1-22-order-preserved'] = quality['first_22_ordered']
    checks['quality-rows-1-22-byte-identical'] = quality['first_22_byte_identical']
    details['quality'] = quality

    old_lessons = {p for p in old_paths if p.startswith('corpus/lessons/')}
    lesson_changes = tracked_path_changes(
        old_lessons, old_lessons & new_paths,
        lambda path: blob(base, path), lambda path: blob(source, path))
    checks['prior-lessons-unchanged'] = not (
        lesson_changes['deleted'] or lesson_changes['changed'])
    details['prior_lessons_changed'] = lesson_changes

    old_history = {p for p in old_paths if RUNS_PREDICTIONS.match(p)
                   and p not in ROUTED_FIX_FILES}
    new_history = {p for p in new_paths if RUNS_PREDICTIONS.match(p)
                   and p not in ROUTED_FIX_FILES}
    run_changes = tracked_path_changes(
        old_history, new_history,
        lambda path: blob(base, path), lambda path: blob(source, path))
    checks['prior-round-17-18-19-runs-predictions-unchanged'] = not any(
        run_changes.values())
    details['prior_runs_predictions_changes'] = run_changes

    checks['no-deleted-path'] = not (old_paths - new_paths)
    details['deleted_paths'] = sorted(old_paths - new_paths)
    routed_changes = []
    for path in sorted(ROUTED_FIX_FILES):
        before_exists, after_exists = path in old_paths, path in new_paths
        if (before_exists != after_exists or
                (before_exists and blob(base, path) != blob(source, path))):
            routed_changes.append(path)
    details['routed_fix_tool_changes'] = routed_changes
    details['routed_fix_tool_allowlist'] = sorted(ROUTED_FIX_FILES)

    before_coverage = command_a(base, old_paths)
    after_coverage = command_a(source, new_paths)
    details['command_a'] = {'base': before_coverage, 'source': after_coverage}
    checks['base-map-resolves'] = not (before_coverage['missing'] or
                                       before_coverage['dangling'])
    checks['source-map-resolves'] = not (after_coverage['missing'] or
                                         after_coverage['dangling'])
    checks['coverage-not-harmed'] = (
        after_coverage['coverage_score'] >= before_coverage['coverage_score'])
    checks['depth-not-harmed'] = (
        after_coverage['depth_score'] >= before_coverage['depth_score'])

    source_checks, source_details = compare_sources(
        blob(base, 'corpus/SOURCES.md'), blob(source, 'corpus/SOURCES.md'))
    checks.update({'sources-' + name: passed
                   for name, passed in source_checks.items()})
    details['sources'] = source_details

    failed = [name for name, passed in checks.items() if not passed]
    return {
        'base': base,
        'source': source,
        'checks': checks,
        'details': details,
        'failed': failed,
        'pass': not failed,
    }


def selftest():
    cases = []

    def add(case_id, test):
        cases.append((case_id, test))

    def require(value):
        if not value:
            raise AssertionError('condition_false')

    readme = ('## Coverage map\n| `2026-10-20-a` | one |\n'
              '| `2026-10-20-b` | two |\n## Frontier\n')
    skill = ('## Queue-drain craft (selftest)\n'
             '- **rule** cites corpus/knowledge/2026-10-20-a.md:1-2\n'
             '## Next\n')
    files = {'2026-10-20-a', '2026-10-20-b'}
    knowledge = {'corpus/knowledge/2026-10-20-a.md': b'one\ntwo\n'}
    valid_coverage = analyze_coverage(files, readme, skill, knowledge.__getitem__)
    add('coverage_map_exact', lambda: require(
        not valid_coverage['missing'] and not valid_coverage['dangling']))
    missing_coverage = analyze_coverage(
        files, readme.replace('| `2026-10-20-b` | two |\n', ''), skill,
        knowledge.__getitem__)
    add('coverage_missing_detected', lambda: require(
        missing_coverage['missing'] == ['2026-10-20-b']))
    add('depth_valid_citation_counted', lambda: require(
        valid_coverage['citation_resolved_rules'] == 1 and
        valid_coverage['depth_score'] == 10.0))
    invalid_skill = skill.replace(':1-2', ':1-3')
    invalid_depth = analyze_coverage(files, readme, invalid_skill,
                                     knowledge.__getitem__)
    add('depth_out_of_range_rejected', lambda: require(
        invalid_depth['citation_resolved_rules'] == 0))

    quality = (b'## Admission criteria\n| # | criterion |\n|---|---|\n' +
               b''.join(f'| {n} | stable {n} |\n'.encode()
                        for n in range(1, QUALITY_ROWS + 1)) +
               b'\n## Weak signals\n')
    add('quality_first_22_identical', lambda: require(
        quality_controls(quality, quality)['first_22_byte_identical']))
    altered_quality = quality.replace(b'| 22 | stable 22 |',
                                      b'| 22 | altered 22 |')
    add('quality_row_22_change_rejected', lambda: require(
        not quality_controls(quality, altered_quality)['first_22_byte_identical']))
    add('prefix_append_accepted', lambda: require(
        b'base\n'.startswith(b'base\n') and
        (b'base\nmore\n').startswith(b'base\n')))
    add('prefix_rewrite_rejected', lambda: require(
        not b'changed\n'.startswith(b'base\n')))

    header = ('| id | source | kind | tier | scope | anchor | teaches | status | '
              'opened | recheck | used-by |\n'
              '|---|---|---|---|---|---|---|---|---|---|---|\n')
    row1 = ('| S001 | source | docs | A | scope | anchor | teaches | mined | '
            '2026-10-20 | on-release | old.md |\n')
    row2 = ('| S002 | source2 | docs | A | scope2 | anchor2 | teaches2 | mined | '
            '2026-10-20 | on-release | new.md |\n')
    sources_before = (header + row1).encode()
    sources_allowed = (header + row1.replace(
        '| mined |', '| rechecked |').replace('| on-release |',
        '| 90d |').replace('| old.md |', '| old.md, new.md |') +
        row2).encode()
    allowed_checks, allowed_details = compare_sources(sources_before,
                                                       sources_allowed)
    add('sources_allowed_cells_and_append', lambda: require(
        all(allowed_checks.values()) and
        [c['column'] for c in allowed_details['changed_cells']] ==
        ['status', 'recheck', 'used-by'] and
        allowed_details['appended_rows'][0]['id'] == 'S002'))
    sources_bad = sources_allowed.replace(
        b'| S001 | source | docs | A | scope | anchor |',
        b'| S001 | source | docs | A | scope | changed |', 1)
    bad_checks, _ = compare_sources(sources_before, sources_bad)
    add('sources_evidence_cell_change_rejected', lambda: require(
        not bad_checks['existing_cells_limited_to_status_recheck_used_by']))
    reordered_checks, _ = compare_sources(
        (header + row1).encode(), (header + row2 + row1).encode())
    add('sources_nonappend_rejected', lambda: require(
        not reordered_checks['rows_append_only']))

    path_changes = tracked_path_changes(
        {'old-run', 'same-run'}, {'new-run', 'same-run'},
        {'old-run': b'old', 'same-run': b'same'}.__getitem__,
        {'new-run': b'new', 'same-run': b'same'}.__getitem__)
    add('history_addition_and_deletion_detected', lambda: require(
        path_changes['added'] == ['new-run'] and
        path_changes['deleted'] == ['old-run'] and
        not path_changes['changed']))

    failures = []
    for case_id, test in cases:
        try:
            test()
        except Exception as error:
            failures.append((case_id, str(error)))
            print(f'CASE {case_id}: FAIL {error}')
        else:
            print(f'CASE {case_id}: PASS')
    if failures:
        print(f'SELFTEST: FAILED cases={len(cases)} fails={len(failures)}')
        return 1
    print(f'SELFTEST: CLEAN cases={len(cases)}')
    return 0


def main():
    if sys.argv[1:] == ['--selftest']:
        return selftest()
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        result = evaluate(sys.argv[1], sys.argv[2])
    except (subprocess.CalledProcessError, UnicodeDecodeError,
            ValueError, IndexError, KeyError) as error:
        print(json.dumps({'error': str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
