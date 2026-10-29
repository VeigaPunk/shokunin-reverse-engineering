#!/usr/bin/env python3
"""DRAFT runner, seat C2AtomCritic. Builds landing overlay G (plan wording, made concrete) and
single-edit forgeries of G; scores each with the probe's naive and tight predicates.
Output: one JSON line per (case, atom) on stdout and a summary. SCR=<scratch> required."""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('c2probe', os.path.join(HERE, 'c2-probe.py'))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
sha, show, BASE = P.sha, P.show, P.BASE
H = P.H
# Marker-aware locator. The frozen helper marks only <h2>/<h3>; the FreeBSD snapshot marks its
# sections with <a id="ERRORS"> (no h2/h3), so a heading check on it cannot bind. This patch
# is a probe-only extension, reported as such.
import html as _html
def marked_norm(b):
    t = b.decode('utf-8', 'replace') if b is not None else ''
    t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', t)
    t = re.sub(r'(?is)<h([1-6])[^>]*>(.*?)</h\1>', lambda m: ' \x01' + re.sub(r'<[^>]+>', ' ', m.group(2)) + '\x02 ', t)
    t = re.sub(r'<a id="([^"]+)"[^>]*>', lambda m: ' \x01' + m.group(1) + '\x02 ', t)
    t = _html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return re.sub(r'\s+', ' ', t)
P.H.html_norm = marked_norm
TIP = '8847042a140b044dbf335210c965bf7b06b09b4f'
R47_LANDING = P.git('rev-parse', '--verify', '1e2c310295^{commit}').stdout.decode().strip()
C1R, C2R = P.C1R, P.C2R
SECTION_HDR = '## Record corrections \u2014 round 50'
H_C2FINAL = sha(show('.ufo/waves/round-49/l1/scores/c2-final.json'))
H_FB = sha(show(P.FB))
H_POP = sha(show(P.POP))


def b5_line(with_sha=True):
    if with_sha:
        return '- B5 tip=%s receipts=%s,%s sha256=%s,%s' % (TIP, C1R, C2R, sha(show(C1R)), sha(show(C2R)))
    return '- B5 tip=%s receipts=%s,%s' % (TIP, C1R, C2R)


def b5_tight(v):
    lines = [l for l in P.vis_section(v.text('SCORECARD.md'), SECTION_HDR) if l.startswith('- B5 ')]
    if len(lines) != 1:
        return False
    if P.git('cat-file', '-e', TIP + '^{commit}').returncode:
        return False
    return lines[0].strip() == b5_line(True)


def section_text(b3=None, b4=None, b5=None):
    lines = [SECTION_HDR, '',
             b3 or '- B3 seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers',
             b4 or '- B4 quality=harmed discernment=improved-decision-level-only source=corpus/lessons/round-48-verifier-spotcheck.md',
             b5 or b5_line(True), '']
    return '\n'.join(lines)


def row_s(sid, src, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby):
    return '| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        sid, src, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby)


S150 = row_s(
    'S150', 'sysexits(3) FreeBSD manual, a second archive \u2014 https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3',
    'docs', 'C', 'the provenance direction of the sysexits header (which archive carries the origin text)',
    'ERRORS heading; "EX_USAGE (64) The command was used incorrectly" (7 words); sha256 %s, snapshot %s' % (H_FB, P.FB),
    'supersedes S149 \u2014 FreeBSD is the origin of the sysexits header and man7 its Linux rendering; status stays rejected: REJECTED: a second mirror of the value S148 already carries; flip: a claim whose verdict needs an independent archive of the header',
    'rejected', '2026-10-28', 'on-request', 'corpus/lessons/round-49.md')
S151 = row_s(
    'S151', 'Stanford Encyclopedia of Philosophy, Karl Popper \u2014 https://plato.stanford.edu/entries/popper/',
    'docs', 'B', 'falsifiability as the demarcation criterion, tiered by the CORPUS tier text',
    '2. Backdrop to Popper\u2019s Thought; "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words); sha256 %s, snapshot %s' % (H_POP, P.POP),
    'supersedes S147 \u2014 tier B: an expert survey of Popper, not a primary or authoritative source for the criterion (CORPUS tier text)',
    'mined', '2026-10-28', 'on-request', 'corpus/lessons/round-49.md')

SKILL_ROWS = ['| `%s` | gate \u2014 R49 frozen counter (round-49 landing) | 0=met; 1=not met; 2=could-not-evaluate | self-test: none (disclosed) | pinned: none |'
              % p for p in P.TARGET_PATHS]


def build_scorecard(prefix_row=True, cal_extra=None, section=None, trailing=None):
    lines = P.show('SCORECARD.md').decode().split('\n')
    done_cov = done_cal = False
    for i, l in enumerate(lines):
        if not done_cov and l.startswith('| coverage | 9.72 \u2192 10.0 | '):
            pre = '139/139 knowledge files mapped at %s (command A, base); ' % BASE if prefix_row else ''
            lines[i] = l.replace('| coverage | 9.72 \u2192 10.0 | ', '| coverage | 9.72 \u2192 10.0 | ' + pre, 1)
            done_cov = True
        if not done_cal and l.startswith('| calibration | 0 \u2192 10 |'):
            body = l.rstrip()
            sent = cal_extra if cal_extra is not None else (
                ' Round-48 closure verdict `rejected-harmed` (`corpus/lessons/round-48-verifier-spotcheck.md`); '
                'round-49 `c2-final` measure `mismatches 0` (`.ufo/waves/round-49/l1/scores/c2-final.json`, sha256 %s).' % H_C2FINAL)
            lines[i] = body[:-1].rstrip() + sent + ' |'
            done_cal = True
    text = '\n'.join(lines).rstrip('\n') + '\n\n' + (section if section is not None else section_text()) + (trailing or '')
    return text.encode()


def build_sources(s150=S150, s151=S151, extra=''):
    lines = P.show('corpus/SOURCES.md').decode().split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith('| S149 |'))
    lines[i + 1:i + 1] = [s150, s151] + ([extra] if extra else [])
    return '\n'.join(lines).encode()


def build_skill(rows=None, fence=False, heading_new=None):
    t = P.show('SKILL.md').decode().split('\n')
    start = t.index('## Local round-evidence gate registry')
    end = next(k for k in range(start + 1, len(t)) if t[k].startswith('## '))
    last = max(k for k in range(start, end) if t[k].startswith('| '))
    rr = rows if rows is not None else SKILL_ROWS
    if fence:
        rr = ['```'] + rr + ['```']
    t[last + 1:last + 1] = rr
    out = '\n'.join(t)
    if heading_new:
        out = out.rstrip('\n') + '\n\n## Round-49 notes\n\n' + '\n'.join(heading_new) + '\n'
    return out.encode()


def G():
    return {'SCORECARD.md': build_scorecard(), 'corpus/SOURCES.md': build_sources(),
            'SKILL.md': build_skill()}


CASES = []  # (case_id, atom, description, overlay)


def add(cid, atom, desc, over):
    CASES.append((cid, atom, desc, over))


g = G()
CASES.append(('G', 'ALL', 'landing overlay G (plan wording made concrete): every atom must be green', g))
CASES.append(('D0', 'ALL', 'do-nothing: base bytes, no landing (every atom must be red except as noted)', {}))

# ---- B1 coverage fraction
add('F1a', 'B1', 'coverage 139 prefix moved inside an HTML comment in the row; visible row still 138/138',
    {'SCORECARD.md': build_scorecard(prefix_row=False, trailing='')
     .replace(b'| coverage | 9.72', b'| coverage | 9.72', 1)})
_row = build_scorecard(prefix_row=False).decode().replace(
    '| coverage | 9.72 \u2192 10.0 | ', '| coverage | 9.72 \u2192 10.0 | <!-- 139/139 knowledge files mapped at %s -->' % BASE, 1)
CASES[-1] = ('F1a', 'B1', 'coverage 139 prefix placed inside an HTML comment; visible row still 138/138', {'SCORECARD.md': _row.encode()})
add('F1b', 'B1', 'coverage row unchanged (138/138 round-47); "139/139 ... at <base>" as a plain paragraph after the table',
    {'SCORECARD.md': build_scorecard(prefix_row=False, section=section_text(b3='- B3 seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers\n139/139 knowledge files mapped at %s.' % BASE))})
add('F1c', 'B1', 'prefix states 139/139 but names the round-47 landing commit (count there 138)',
    {'SCORECARD.md': build_scorecard(prefix_row=False).replace(
        '| coverage | 9.72 \u2192 10.0 | '.encode(), ('| coverage | 9.72 \u2192 10.0 | 139/139 knowledge files mapped at %s; ' % R47_LANDING).encode(), 1)})

# ---- B2 calibration row
add('F2a', 'B2', 'rejected-harmed + c2-final sentence placed inside an HTML comment within the calibration row',
    {'SCORECARD.md': build_scorecard(cal_extra=' <!-- Round-48 closure verdict `rejected-harmed`; round-49 `c2-final` sha256 %s. -->' % H_C2FINAL)})
add('F2b', 'B2', 'sentence present but the c2-final digest is truncated to 8 hex',
    {'SCORECARD.md': build_scorecard(cal_extra=' Round-48 closure verdict `rejected-harmed` (`corpus/lessons/round-48-verifier-spotcheck.md`); round-49 `c2-final` measure `mismatches 0` (`.ufo/waves/round-49/l1/scores/c2-final.json`, sha256 %s).' % H_C2FINAL[:8])})

# ---- B3 round-48 seat settlement
add('F3a', 'B3', 'plan wording as written: names C1Meaning and ScribeReportNumbers and 72, omits C1Battery',
    {'SCORECARD.md': build_scorecard(section=section_text(b3='- B3 75 results, C1Meaning blocked, ScribeReportNumbers aborted; 72 report artifacts'))})
add('F3b', 'B3', 'looser token: missing= set has two of three seats (C1Battery dropped)',
    {'SCORECARD.md': build_scorecard(section=section_text(b3='- B3 seats=75 reports=72 missing=C1Meaning,ScribeReportNumbers'))})
add('F3c', 'B3', 'correct B3 line wrapped in an HTML comment (only line in the section)',
    {'SCORECARD.md': build_scorecard(section=section_text(b3='<!--\n- B3 seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers\n-->'))})
add('F3d', 'B3', 'correct B3 line plus a contradictory second B3 line (first-match / duplicate)',
    {'SCORECARD.md': build_scorecard(section=section_text() + '- B3 seats=75 reports=75 missing=\n')})

# ---- B4 closure verdicts
add('F4a', 'B4', 'correct B4 line inside a fenced code block',
    {'SCORECARD.md': build_scorecard(section=section_text(b4='```\n- B4 quality=harmed discernment=improved-decision-level-only source=corpus/lessons/round-48-verifier-spotcheck.md\n```'))})
add('F4b', 'B4', 'B4 line with the wrong source row (round-49 closure, which does not carry the round-48 verdicts)',
    {'SCORECARD.md': build_scorecard(section=section_text(b4='- B4 quality=harmed discernment=improved-decision-level-only source=corpus/lessons/round-49-verifier-spotcheck.md'))})

# ---- B5 receipts named
add('F5a', 'B5', 'receipts and tip named, sha256 field dropped',
    {'SCORECARD.md': build_scorecard(section=section_text(b5=b5_line(False)))})
add('F5b', 'B5', 'receipts and tip named in a prose paragraph outside the corrections section; section has no B5 line',
    {'SCORECARD.md': build_scorecard(section=section_text(b5='- B5 see prose'), trailing='\nThe round-48 receipts are %s and %s (tip %s).\n' % (C1R, C2R, TIP))})

# ---- B6/B7 registry supersedes rows
add('F6a', 'B6', 'S150 correction row duplicated verbatim',
    {'corpus/SOURCES.md': build_sources(extra=S150)})
add('F6b', 'B6', 'S150 correction row inside an HTML comment in the registry',
    {'corpus/SOURCES.md': build_sources(s150='<!--\n' + S150 + '\n-->')})
add('F6c', 'B6', 'S150 row indented four spaces (invisible to the census row pattern, still matches plain text)',
    {'corpus/SOURCES.md': build_sources(s150='    ' + S150)})
add('F6d', 'B6', 'S150 anchor says DESCRIPTION, not ERRORS (quote located under the wrong heading)',
    {'corpus/SOURCES.md': build_sources(s150=S150.replace('ERRORS heading', 'DESCRIPTION heading'))})
add('F7a', 'B7', 'S151 tier cell left at A while teaches says tier B (teaches-only tier)',
    {'corpus/SOURCES.md': build_sources(s151=S151.replace('| docs | B |', '| docs | A |'))})
add('F7b', 'B7', 'S151 row inside an HTML comment',
    {'corpus/SOURCES.md': build_sources(s151='<!--\n' + S151 + '\n-->')})

# ---- B9 registry census
add('F9a', 'B9', 'six round-49 registry rows placed inside a fenced block in the registry section',
    {'SKILL.md': build_skill(fence=True)})
add('F9b', 'B9', 'verdict maps with polarity inverted to "0=not met; 1=violation; 2=usage" (round-48 C1Gold shape)',
    {'SKILL.md': build_skill(rows=[r.replace('0=met; 1=not met; 2=could-not-evaluate', '0=not met; 1=violation; 2=usage') for r in SKILL_ROWS])})
add('F9c', 'B9', 'six rows placed under a new "## Round-49 notes" heading, not the registry heading',
    {'SKILL.md': build_skill(rows=[], heading_new=SKILL_ROWS)})

# ---- B11 base agreement (base-only atom)
add('D11', 'B11', 'do-nothing for B11 is the base: all four declarations read decc5697 (expected GREEN; not an atom)', {})


def score(over):
    v = P.View(over)
    res = {}
    for k in ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11'):
        naive_f, tight_f = P.ATOMS[k]
        if k == 'B5':
            tight_f = b5_tight
        if k == 'B8':
            res[k] = {'naive': bool(naive_f(v)), 'tight': None}
        elif k == 'B10':
            res[k] = {'naive': bool(naive_f(v)), 'tight': None}
        else:
            res[k] = {'naive': bool(naive_f(v)), 'tight': bool(tight_f(v))}
    return res


out = []
for cid, atom, desc, over in CASES:
    r = score(over)
    out.append({'case': cid, 'atom_target': atom, 'desc': desc, 'verdicts': r})
    print(json.dumps({'case': cid, 'target': atom, 'desc': desc, 'verdicts': r}, ensure_ascii=False))

with open(os.path.join(os.environ['SCR'], 'probe-out.json'), 'w') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
