#!/usr/bin/env python3
"""RV-4: mechanically summarize the round-3 map-token verification into
measurements.json + artifact-identity.txt (no hand-transcribed numbers)."""
import hashlib
import json
import pathlib
import re
import sys

D = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/RV-4')
ART = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/map-token-patch.md')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def fields(path):
    out = {}
    for line in pathlib.Path(path).read_text().splitlines():
        if ': ' in line:
            k, v = line.split(': ', 1)
            out[k.strip()] = v.strip()
    # combined lines: "coverage_section_lines: 11-69  hunk_starts: [38]  scope_ok: True"
    comb = out.get('coverage_section_lines', '')
    mm = re.search(r'hunk_starts: (\[[^\]]*\])', comb)
    if mm:
        out['hunk_starts'] = mm.group(1)
    ms = re.search(r'scope_ok: (\w+)', comb)
    if ms:
        out['scope_ok'] = ms.group(1)
    return out


def main():
    m = {
        'seat': 'RV-4', 'chain': 'c1', 'wave': 'arc3-loop1-round3',
        'producer_artifact': {
            'path': str(ART.relative_to(D.parents[5])),
            'sha256': sha(ART),
            'mtime': pathlib.Path(ART).stat().st_mtime_ns,
            'bytes': ART.stat().st_size,
        },
        'baseline': {
            'readme_sha256': sha(D / 'README.before.md'),
            'readme_lines': len((D / 'README.before.md').read_text().splitlines()),
            'coverage_map_unique_tokens': 82,
            'coverage_map_occurrences': 84,
            'command_a_before': (D / 'command-A-before.txt').read_text().strip(),
        },
        'variants': {},
    }
    for v in ('primary', 'honest-stop', 'caller-option-strict-additive'):
        f = fields(D / f'{v}-verification.out')
        m['variants'][v] = {
            'patch_sha256': sha(D / f'{v}.patch'),
            'after_readme_sha256': sha(D / f'{v}.README.md'),
            'after_lines': len((D / f'{v}.README.md').read_text().splitlines()),
            'apply_method': f.get('apply_method'),
            'line_neutral': f.get('line_neutral'),
            'unique_tokens_after': f.get('token_occurrences_after', '').split('unique_after:')[-1].strip(),
            'prior_tokens_byte_identical': f.get('prior_tokens_byte_identical'),
            'prior_token_occurrence_sequence_identical': f.get('prior_token_occurrence_sequence_identical'),
            'new_tokens': f.get('new_tokens'),
            'hunks': f.get('hunks'),
            'hunk_starts': f.get('hunk_starts'),
            'scope_ok': f.get('scope_ok'),
            'files_touched': f.get('files_touched_by_patch'),
            'occurrence_delta': f.get('coverage_map_occurrence_delta'),
            'strict_additive_only': f.get('STRICT_additive_only (r1 form; prose rewrite not allowed)'),
            'verdict_seat_criteria': f.get('VERDICT_SEAT_CRITERIA (line-neutral | 82->83 | prior-82 identical)'),
        }
    m['coupling_rehearsal'] = (D / 'coupling-rehearsal.out').read_text().strip().splitlines()
    m['probe_rehearsal'] = (D / 'probe-rehearsal.txt').read_text().strip().splitlines()
    m['probe_rehearsal_v2_current_table'] = (D / 'probe-rehearsal-v2.txt').read_text().strip().splitlines()
    m['selftests'] = {p.stem: fields(p).get('VERDICT_SEAT_CRITERIA (line-neutral | 82->83 | prior-82 identical)')
                      for p in sorted(D.glob('selftest-*.out'))}
    (D / 'measurements.json').write_text(json.dumps(m, indent=2, sort_keys=True) + '\n')
    print(json.dumps(m, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()