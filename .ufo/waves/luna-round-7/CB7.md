## CLAIM
Frozen read-only post-landing census: Command A verbatim 78/78 (9/9 rules, coverage/depth 10.0), six hyphenated entries with house fields and pinned anchors, 12 row-exact README rows, prior-72 byte identity, no Core-promotion reading. At `411175e` it fails closed (no landing); this seat certifies the instrument, not the target.

## METHOD
Read `N1.md`/`N2.md`/`P0.md`, `E1D`–`E6D`, `G3`/`G4`/`G6`, `Z1`–`Z6`, `M1`/`M2`, `K3`/`K4`, `F8`, `SCORECARD.md:92-123`, `corpus/QUALITY.md:7-25`, `protocol/CORPUS.md:17-19`, `receipts/census-pre.txt`. Baselines re-derived read-only at `411175e`: Command A verbatim `{"citation_resolved_rules":9,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":72,"mapped":72,"missing":[],"rule_blocks":9}`; 72-blob digest `3adf3bc2…`; map-token digest `c538284b…` — both reproduce `census-pre.txt:14-15`. The frozen body (sha256 `cedc6e30…`, 489 lines) extracts the Command A fence from `SCORECARD.md` at REV, execs it verbatim, requires it byte-equal to BASE (C0), then runs C1–C20. Attack: 20 in-memory states through the same checker; no repo writes.

## FINDINGS
- Pre-state at `411175e`: `CENSUS RESULT: FINDING` (exit 1); C1/C2/C4–C12/C14 each name the six absent files; C0 and C16–C20 PASS — fail-closed on the real tree.
- Checks: C1 Command A targets; C2 file set + prior-72 digest; C4 tokens = BASE ∪ SIX; C5 six 3-cell map rows (after r14-02, before `## Knowledge`); C6 six 4-cell rows dated `2026-10-16`; C7 README append-only (rev lines minus the 12 new rows == BASE); per entry C8 `source:`/`verified-at:`/`recheck:`, C9 `rea-agents@6.5.0`, C10 observation/inference/unknown, C11 carrier anchors + distinct-carrier phrasing (rulings b/c), C12 resolvable receipt ranges, C14 no un-negated Core promotion, C15 sqlite fixture exclusion; C16 `PROVINCE.md`/C17 SKILL craft unchanged; C13/C18/C19/C20 WARN-only.
- Attack: `SELFTEST PASS (20 states)` — control PASS; 18 mutations caught (underscore stems C2/C4/C5; dropped `recheck:` C8; prior-file edit C2; README edit C7; map-row drop/duplicate/wrong-section C4/C5; 79th file C1/C2; promotion C14; out-of-bounds citation C12; dropped hash C11; A-fixture C15; wrong date C6; dangling token C1/C4; empty entry C8–C11; edited Command A C0; `PROVINCE.md` C16); records-only change WARN C19.
- Run: extract the marker-pair block and execute from the repo root; `CB7_REV` overrides HEAD, `CB7_STRICT_README=0` downgrades C7, `CB7_SELFTEST=1` runs the matrix.

## THREATS
Proxies disclosed: C14 is a sentence-level negation heuristic; ev-id presence is WARN-only (QUALITY 6 admits the exact call); C13 downgrades untracked `SC*.md` citations; C5/C6 encode the house 3/4-cell shapes; C7 can false-fail an intentional baseline edit (knob provided). Uncommitted landing → REV=HEAD reports pre-state (C20 warns). Synthetic PASS proves non-vacuity, not the real admissions; scouts remain untracked at this HEAD.

## VERDICT
FINDING: census frozen (sha256 `cedc6e30…`) and attacked 20/20; fail-closed at `411175e` — 78/78 and the six admissions remain to be earned at the landing revision.

<!-- CB7-FROZEN-CMD-BEGIN -->
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -B - "$PWD" <<'PY'
#!/usr/bin/env python3
"""luna-round-7 final census - CB7 (lane B, coverage round). Read-only: Git objects only; no writes,
network, REA/MCP.  Usage: python3 -B - <repo-root>  (REV from env CB7_REV, default HEAD).
Env: CB7_SELFTEST=1 attack matrix; CB7_STRICT_README=0 downgrades the append-only README gate to WARN.
Exit 0 PASS / 1 FINDING / 2 harness error."""
import contextlib, hashlib, io, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
os.chdir(ROOT)
BASE = '411175e337c0725ae9bee3fd478ae9bf05bedf3f'
SIX = ['2026-10-16-l7-01-inspect-go-binary',
       '2026-10-16-l7-02-inspect-rust-binary',
       '2026-10-16-l7-03-inspect-electron-fuses',
       '2026-10-16-l7-04-inspect-sqlite-database',
       '2026-10-16-l7-05-search-bytes',
       '2026-10-16-l7-06-inspect-with-objdump']
BASE_FILES_SHA = '3adf3bc2f0e59646cf8d77dc9d06646d7690e24168b89f9b4607cdfdad75adbf'
BASE_TOKENS_SHA = 'c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0'
A_TARGET = {'knowledge_files': 78, 'mapped': 78, 'missing': [], 'dangling': [],
            'citation_resolved_rules': 9, 'rule_blocks': 9,
            'coverage_score': 10.0, 'depth_score': 10.0}
ANCHOR = {SIX[0]: ['70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9', '/usr/bin/docker'],
          SIX[1]: ['1b44ed531f404f5358ee0618a423560463819534a38db5176bb1064b9d14d1f7',
                   'd006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42',
                   '/usr/bin/rg', 'libsignal-client.node'],
          SIX[2]: ['f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a',
                   '/usr/lib/signal-desktop/signal-desktop'],
          SIX[3]: ['3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728', 'sc4-index.db'],
          SIX[4]: ['8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d', '/usr/bin/true'],
          SIX[5]: ['e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806', '/usr/bin/jq']}
A_FIXTURE = '71ac0b8ea43d2f841d019e97fac0f621d0b2dc600ab6fd1314cee831d3e5872b'
EXCLUDE_RE = re.compile(r'(?i)(exclud|not admit|no retained|without .{0,24}(recipe|bytes)|not included)')
NEG_RE = re.compile(r'(?i)\b(not|no|never|without|non)\b')
PROMO_RE = re.compile(r'(?i)(promot|elevat|admit)')
CORE_RE = re.compile(r'(?i)\bcore\b')
RECEIPT_RE = re.compile(r'(\.ufo/waves/luna-round-6/receipts(?:-B)?/leg-\d+\.md)((?::\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)?)')
ANY_CITE_RE = re.compile(r'((?:\.ufo|corpus)/[A-Za-z0-9._/-]+\.md)')
FIELD_PATS = {'source': re.compile(r'(?m)^[ \t]*(?:[->*][ \t]+)?source:'),
              'verified-at': re.compile(r'(?m)^[ \t]*(?:[->*][ \t]+)?verified-at:'),
              'recheck': re.compile(r'(?m)^[ \t]*(?:[->*][ \t]+)?recheck:')}

def git(*args):
    return subprocess.check_output(['git', *args], text=True, stderr=subprocess.DEVNULL)

def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def make_reader(rev):
    cache = {}
    def read(path):
        if path not in cache:
            cache[path] = git('show', f'{rev}:{path}')
        return cache[path]
    return read

def make_tree(rev):
    cache = {}
    def tree_of(prefix):
        if prefix not in cache:
            cache[prefix] = [l for l in git('ls-tree', '-r', '--name-only', rev, '--', prefix).splitlines() if l]
        return cache[prefix]
    return tree_of

def cmd_a_body(read):
    lines = read('SCORECARD.md').splitlines()
    start = end = None
    for i, l in enumerate(lines):
        if l.strip().startswith('python3 - "$REV"'):
            start = i + 1
            break
    if start is not None:
        for j in range(start, len(lines)):
            if lines[j].strip() == 'PY':
                end = j
                break
    if start is None or end is None or end <= start:
        raise RuntimeError('SCORECARD.md Command A here-doc block not found')
    return '\n'.join(lines[start:end])

def run_cmd_a(rev):
    body = cmd_a_body(make_reader(rev))
    buf = io.StringIO()
    saved = sys.argv[:]
    sys.argv = ['commandA', rev]
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(body, 'SCORECARD.md:CommandA', 'exec'), {'__name__': '__main__'})
    finally:
        sys.argv = saved
    return json.loads(buf.getvalue())

def map_section(readme):
    return readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]

def knowledge_section(readme):
    return readme.split('## Knowledge\n', 1)[1].split('\n## ', 1)[0]

def census(read_rev, read_base, tree_rev, tree_base, a_json, strict_readme=True,
           changed_paths=(), dirty=''):
    res = []
    def chk(cid, ok, detail, warn=False):
        res.append({'cid': cid, 'level': 'PASS' if ok else ('WARN' if warn else 'FAIL'), 'detail': detail})
    def warn(cid, detail):
        res.append({'cid': cid, 'level': 'WARN', 'detail': detail})
    counts = {}
    # C0 canonical Command A body unchanged
    try:
        b_rev, b_base = cmd_a_body(read_rev), cmd_a_body(read_base)
        chk('C0', b_rev == b_base, 'Command A here-doc body identical to BASE (%d lines)' % len(b_rev.splitlines()))
    except Exception as e:
        chk('C0', False, 'Command A body extraction failed: %r' % e)
    # C1 Command A result targets
    got = {k: a_json.get(k) for k in A_TARGET}
    bad = [k for k in A_TARGET if a_json.get(k) != A_TARGET[k]]
    counts.update(got)
    chk('C1', not bad, 'Command A %s' % (json.dumps(got, sort_keys=True) if not bad else 'mismatch: ' + json.dumps({k: got[k] for k in bad}, sort_keys=True)))
    # C2 knowledge file set + prior-72 blob identity
    try:
        tf = tree_rev('corpus/knowledge'); tb = tree_base('corpus/knowledge')
        st_rev = [Path(p).stem for p in tf if p.endswith('.md')]
        st_base = [Path(p).stem for p in tb if p.endswith('.md')]
        new = sorted(set(st_rev) - set(st_base)); gone = sorted(set(st_base) - set(st_rev))
        nonmd = [p for p in tf if not p.endswith('.md') and p not in set(tb)]
        recs = ''.join('%s %s\n' % (s, sha(read_rev('corpus/knowledge/%s.md' % s))) for s in st_base)
        digest = sha(recs)
        ok = (new == sorted(SIX)) and not gone and not nonmd and len(st_rev) == 78 and digest == BASE_FILES_SHA
        counts['files'] = len(st_rev)
        chk('C2', ok, 'files=%d new=%s gone=%s new_nonmd=%d prior72_sha=%s' % (len(st_rev), new, gone, len(nonmd), digest[:16]))
    except Exception as e:
        chk('C2', False, 'file-set check failed: %r' % e)
    # C4 map tokens
    try:
        toks_rev = re.findall(r'2026-10-\d{2}-[a-z0-9-]+', map_section(read_rev('corpus/README.md')))
        toks_base = re.findall(r'2026-10-\d{2}-[a-z0-9-]+', map_section(read_base('corpus/README.md')))
        base_digest = sha('\n'.join(sorted(set(toks_base))) + '\n')
        added = sorted(set(toks_rev) - set(toks_base)); lost = sorted(set(toks_base) - set(toks_rev))
        ok = (base_digest == BASE_TOKENS_SHA and added == sorted(SIX) and not lost and len(set(toks_rev)) == 78)
        counts['tokens'] = len(set(toks_rev))
        chk('C4', ok, 'tokens=%d added=%s lost=%s base_sha_ok=%s' % (len(set(toks_rev)), added, lost, base_digest == BASE_TOKENS_SHA))
    except Exception as e:
        chk('C4', False, 'token check failed: %r' % e)
    # C5 six 3-cell map rows
    hits_map = {}
    try:
        rl = read_rev('corpus/README.md').splitlines()
        map_hdr = [i for i, l in enumerate(rl) if l.strip() == '## Coverage map'][0]
        kn_hdr = [i for i, l in enumerate(rl) if l.strip() == '## Knowledge'][0]
        for s in SIX:
            pat = re.compile(r'^\| `knowledge/' + re.escape(s) + r'` \|')
            hits_map[s] = [i for i, l in enumerate(rl) if pat.match(l)]
        ok = True
        for s in SIX:
            if len(hits_map[s]) != 1:
                ok = False
            else:
                i = hits_map[s][0]
                ok = ok and (rl[i].count('|') == 4) and (map_hdr < i < kn_hdr)
        chk('C5', ok, 'map rows ' + ' '.join('%s:%d' % (s[-12:], len(hits_map[s])) for s in SIX))
    except Exception as e:
        chk('C5', False, 'map-row check failed: %r' % e)
    # C6 six 4-cell Knowledge rows
    hits_kn = {}
    try:
        rl = read_rev('corpus/README.md').splitlines()
        kn_hdr = [i for i, l in enumerate(rl) if l.strip() == '## Knowledge'][0]
        ls_hdr = [i for i, l in enumerate(rl) if l.strip() == '## Lessons']
        ls_end = ls_hdr[0] if ls_hdr else len(rl)
        row_pat = re.compile(r'^\| `2026-10-\d{2}-[a-z0-9-]+` \|')
        for s in SIX:
            pat = re.compile(r'^\| `' + re.escape(s) + r'` \|')
            hits_kn[s] = [i for i, l in enumerate(rl) if pat.match(l)]
        ok = True
        for s in SIX:
            if len(hits_kn[s]) != 1:
                ok = False
            else:
                i = hits_kn[s][0]; cells = rl[i].split('|')
                ok = ok and (rl[i].count('|') == 5) and (kn_hdr < i < ls_end) and ('2026-10-16' in cells[-2])
        base_rows = [l for l in knowledge_section(read_base('corpus/README.md')).splitlines() if row_pat.match(l)]
        rev_rows = [l for l in knowledge_section(read_rev('corpus/README.md')).splitlines() if row_pat.match(l)]
        chk('C6', ok and len(rev_rows) == len(base_rows) + 6,
            'knowledge rows %d->%d ' % (len(base_rows), len(rev_rows)) + ' '.join('%s:%d' % (s[-12:], len(hits_kn[s])) for s in SIX))
    except Exception as e:
        chk('C6', False, 'knowledge-row check failed: %r' % e)
    # C7 README append-only
    try:
        rl = read_rev('corpus/README.md').splitlines()
        bl = read_base('corpus/README.md').splitlines()
        rowlines = []; found = True
        for s in SIX:
            for pat in (re.compile(r'^\| `knowledge/' + re.escape(s) + r'` \|'), re.compile(r'^\| `' + re.escape(s) + r'` \|')):
                hits = [l for l in rl if pat.match(l)]
                if len(hits) != 1:
                    found = False
                else:
                    rowlines.append(hits[0])
        if not found:
            chk('C7', False, 'cannot identify the 12 new row lines uniquely', warn=not strict_readme)
        else:
            remain = list(rl)
            for l in rowlines:
                remain.remove(l)
            ok = remain == bl
            chk('C7', ok, 'README minus 12 new rows == BASE' if ok else 'README diverges (remain %d vs base %d lines)' % (len(remain), len(bl)), warn=not strict_readme)
    except Exception as e:
        chk('C7', False, 'append-only check failed: %r' % e)
    # C8-C15 per entry
    for s in SIX:
        path = 'corpus/knowledge/%s.md' % s
        try:
            txt = read_rev(path)
        except Exception:
            for cid in ('C8', 'C9', 'C10', 'C11', 'C12', 'C14'):
                chk(cid, False, '%s: entry file missing' % s)
            continue
        missing = [k for k, p in FIELD_PATS.items() if not p.search(txt)]
        badf = []
        if not missing:
            m = FIELD_PATS['verified-at'].search(txt)
            line = txt[m.start():txt.find('\n', m.start()) if '\n' in txt[m.start():] else len(txt)]
            if '2026-10-16' not in line:
                badf.append('verified-at value lacks 2026-10-16')
            m2 = FIELD_PATS['recheck'].search(txt)
            line2 = txt[m2.start():txt.find('\n', m2.start()) if '\n' in txt[m2.start():] else len(txt)]
            if len(line2.split(':', 1)[1].strip()) < 4:
                badf.append('recheck value empty')
        chk('C8', not missing and not badf, '%s: metadata fields %s' % (s, 'ok' if not (missing or badf) else 'missing=%s %s' % (missing, badf)))
        chk('C9', 'rea-agents@6.5.0' in txt, '%s: rea pin %s' % (s, 'ok' if 'rea-agents@6.5.0' in txt else 'MISSING'))
        lab = [l for l in ('observation', 'inference', 'unknown') if not re.search(r'(?i)\b' + l, txt)]
        chk('C10', not lab, '%s: labels %s' % (s, 'ok' if not lab else 'missing %s' % lab))
        miss = [a for a in ANCHOR[s] if a not in txt]
        chk('C11', not miss, '%s: anchors %s' % (s, 'ok' if not miss else 'MISSING %s' % miss))
        if s == SIX[1] and re.search(r'(?i)\b(same|shared|identical)\b[^.\n]{0,24}\b(carrier|target|artifact)', txt):
            warn('C11', '%s: possible merged-carrier phrasing — verify the two carriers stay distinct' % s)
        cites = RECEIPT_RE.findall(txt); bounds_bad = []; have_line = False
        for pth, rngspec in cites:
            try:
                n = len(read_rev(pth).splitlines())
            except Exception:
                bounds_bad.append(pth + ':unresolvable'); continue
            if not rngspec:
                continue
            have_line = True
            for part in rngspec.lstrip(':').split(','):
                a, _, b = part.partition('-'); st, en = int(a), int(b or a)
                if not (1 <= st <= en <= n):
                    bounds_bad.append('%s:%s(oob n=%d)' % (pth, part, n))
        if not cites:
            chk('C12', False, '%s: no round-6 receipt citation' % s)
        else:
            chk('C12', not bounds_bad, '%s: %d receipt citations %s' % (s, len(cites), 'ranges ok' if not bounds_bad else 'bad ' + str(bounds_bad)))
            if not have_line:
                warn('C12', '%s: receipt citations carry no :line range' % s)
        unres = []
        for pth in sorted(set(ANY_CITE_RE.findall(txt))):
            if RECEIPT_RE.match(pth):
                continue
            try:
                read_rev(pth)
            except Exception:
                unres.append(pth)
        if unres:
            warn('C13', '%s: unresolvable non-receipt citations %s' % (s, unres))
        promo = []
        for sent in re.split(r'(?<=[.;!?])\s+|\n', txt):
            if CORE_RE.search(sent) and PROMO_RE.search(sent) and not NEG_RE.search(sent):
                promo.append(sent.strip()[:70])
        chk('C14', not promo, '%s: not-core %s' % (s, 'ok' if not promo else 'POSITIVE: %s' % promo))
        if not re.search(r'\bRESULT\b', txt):
            warn('C14', '%s: no RESULT marker' % s)
        if s == SIX[3]:
            if A_FIXTURE in txt and not EXCLUDE_RE.search(txt):
                chk('C15', False, '%s: lane-A fixture hash present without exclusion wording' % s)
            else:
                chk('C15', True, '%s: lane-A fixture not admitted (A-hash %s)' % (s, 'present+excluded' if A_FIXTURE in txt else 'absent'))
    # C16-C18 surface immutability
    for cid, p, warn_only in (('C16', 'PROVINCE.md', False), ('C18', 'corpus/QUALITY.md', True)):
        try:
            same = read_rev(p) == read_base(p)
            chk(cid, same, '%s %s' % (p, 'unchanged' if same else 'CHANGED vs BASE'), warn=warn_only)
        except Exception as e:
            chk(cid, False, '%s unreadable: %r' % (p, e), warn=warn_only)
    try:
        craft_rev = read_rev('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
        craft_base = read_base('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
        chk('C17', craft_rev == craft_base, 'SKILL.md Queue-drain craft block %s' % ('unchanged' if craft_rev == craft_base else 'CHANGED vs BASE'))
    except Exception as e:
        chk('C17', False, 'SKILL.md craft block check failed: %r' % e)
    # C19 changed paths
    expected = {'corpus/README.md'} | {'corpus/knowledge/%s.md' % s for s in SIX}
    extra = sorted(set(changed_paths) - expected)
    if extra:
        warn('C19', 'tracked changes outside the coverage landing (adjudicate): %s' % extra)
    else:
        res.append({'cid': 'C19', 'level': 'PASS', 'detail': 'tracked changes inside the coverage landing'})
    # C20 worktree
    if dirty:
        warn('C20', 'checked paths dirty in worktree (verdict is REV-scoped): %s' % dirty.replace('\n', '; '))
    else:
        res.append({'cid': 'C20', 'level': 'PASS', 'detail': 'checked paths clean in worktree'})
    fails = sorted(set(r['cid'] for r in res if r['level'] == 'FAIL'))
    warns = sorted(set(r['cid'] for r in res if r['level'] == 'WARN'))
    return res, ('PASS' if not fails else 'FINDING'), fails, warns, counts

def emul_cmd_a(read, tree_of, rev):
    files = {Path(p).stem for p in tree_of('corpus/knowledge') if p.endswith('.md')}
    section = read('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    craft = read('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule); valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(read('corpus/knowledge/' + name).splitlines())
                st, en = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= st <= en <= count
            except Exception:
                valid = False
        resolved += valid
    n = len(files)
    return {'revision': rev, 'mapped': len(files & mapped), 'knowledge_files': n,
            'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
            'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
            'coverage_score': round(10 * len(files & mapped) / n, 2),
            'depth_score': round(10 * resolved / len(rules), 2)}

def synth_entry(stem):
    hashes = [a for a in ANCHOR[stem] if re.fullmatch(r'[0-9a-f]{64}', a)]
    toks = [a for a in ANCHOR[stem] if a not in hashes]
    leg = 'leg-%d' % (SIX.index(stem) + 3)
    return '\n'.join(['# %s' % stem, '',
        'source: `.ufo/waves/luna-round-6/receipts/%s.md:1-2`' % leg,
        'verified-at: 2026-10-16',
        'recheck: rerun the pinned call and compare the Evidence ID', '',
        'REA pin: `rea-agents@6.5.0`.', '',
        '- Observation: pinned carriers %s by hash.' % ', '.join(toks + hashes),
        '- Inference: bounded to the pinned inputs.', '- Unknown: other inputs untested.',
        'Not a Core promotion; RESULT-class exercise only.', ''])

def selftest():
    base_read = make_reader(BASE); base_tree = make_tree(BASE)
    texts = {}
    for p in base_tree('corpus/knowledge') + base_tree('.ufo/waves/luna-round-6/receipts') + base_tree('.ufo/waves/luna-round-6/receipts-B'):
        if p.endswith('.md'):
            texts[p] = base_read(p)
    for p in ('corpus/README.md', 'SCORECARD.md', 'SKILL.md', 'PROVINCE.md', 'corpus/QUALITY.md'):
        texts[p] = base_read(p)
    def build(mut=None):
        txt = dict(texts); tree = list(base_tree('corpus/knowledge'))
        changed = ['corpus/README.md'] + ['corpus/knowledge/%s.md' % s for s in SIX]
        for s in SIX:
            p = 'corpus/knowledge/%s.md' % s
            txt[p] = synth_entry(s); tree.append(p)
        rl = txt['corpus/README.md'].splitlines()
        i14 = next(i for i, l in enumerate(rl) if '2026-10-14-r14-02-final-sweep' in l)
        maprows = ['| `knowledge/%s` | synthetic observation line | REA 6.5.0; round-6 receipts |' % s for s in SIX]
        rl[i14 + 1:i14 + 1] = maprows
        ils = next(i for i, l in enumerate(rl) if l.strip() == '## Lessons')
        knrows = ['| `%s` | synthetic topic | round-6 receipts A/B | 2026-10-16 |' % s for s in SIX]
        rl[ils:ils] = knrows
        txt['corpus/README.md'] = '\n'.join(rl)
        if mut:
            mut(txt, tree, changed)
        def rd(p): return txt[p]
        def tr(prefix):
            return list(tree) if prefix == 'corpus/knowledge' else base_tree(prefix)
        a = emul_cmd_a(rd, tr, 'SYNTH')
        return census(rd, base_read, tr, base_tree, a, strict_readme=True, changed_paths=changed, dirty='')
    def uplit(s): return s[:17] + s[17:].replace('-', '_')
    def firstbase(tree): return next(p for p in base_tree('corpus/knowledge') if p.endswith('.md'))
    def m_underscore(txt, tree, changed):
        for s in SIX:
            u = uplit(s); old = 'corpus/knowledge/%s.md' % s
            txt['corpus/knowledge/%s.md' % u] = txt.pop(old); tree.remove(old); tree.append('corpus/knowledge/%s.md' % u)
            txt['corpus/README.md'] = txt['corpus/README.md'].replace('knowledge/%s' % s, 'knowledge/%s' % u).replace('| `%s` |' % s, '| `%s` |' % u)
    def m_recheck(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[2]; txt[p] = txt[p].replace('recheck:', 're-check:')
    def m_baseedit(txt, tree, changed):
        p = firstbase(tree); txt[p] = txt[p] + '\npatched line\n'
    def m_readmeedit(txt, tree, changed):
        rl = txt['corpus/README.md'].splitlines()
        i = next(i for i, l in enumerate(rl) if 'held —' in l)
        rl[i] = rl[i].replace('held —', 'held — patched', 1)
        txt['corpus/README.md'] = '\n'.join(rl)
    def m_maprowdrop(txt, tree, changed):
        rl = txt['corpus/README.md'].splitlines()
        i = next(i for i, l in enumerate(rl) if l.startswith('| `knowledge/%s`' % SIX[0]))
        del rl[i]; txt['corpus/README.md'] = '\n'.join(rl)
    def m_extrafile(txt, tree, changed):
        p = 'corpus/knowledge/2026-10-16-l7-07-extra.md'; txt[p] = '# extra\n'; tree.append(p)
    def m_promo(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[0]; txt[p] = txt[p] + 'Status: promoted to Core this round.\n'
    def m_oob(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[1]; txt[p] = txt[p].replace(':1-2`', ':3-9999`')
    def m_hashdel(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[0]; txt[p] = txt[p].replace(ANCHOR[SIX[0]][0], '')
    def m_sqlitea(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[3]; txt[p] = txt[p] + 'Also admits lane-A synthetic fixture %s with sampled rows.\n' % A_FIXTURE
    def m_rustdrop(txt, tree, changed):
        p = 'corpus/knowledge/%s.md' % SIX[1]; txt[p] = txt[p].replace(ANCHOR[SIX[1]][1], '')
    def m_kndate(txt, tree, changed):
        txt['corpus/README.md'] = txt['corpus/README.md'].replace('| `%s` | synthetic topic | round-6 receipts A/B | 2026-10-16 |' % SIX[4],
                                                                  '| `%s` | synthetic topic | round-6 receipts A/B | 2026-10-15 |' % SIX[4])
    def m_wrongsec(txt, tree, changed):
        rl = txt['corpus/README.md'].splitlines()
        i = next(i for i, l in enumerate(rl) if l.startswith('| `knowledge/%s`' % SIX[1]))
        row = rl.pop(i)
        j = next(i for i, l in enumerate(rl) if l.strip() == '## Knowledge')
        rl.insert(j + 1, row); txt['corpus/README.md'] = '\n'.join(rl)
    def m_dangling(txt, tree, changed):
        rl = txt['corpus/README.md'].splitlines()
        i = next(i for i, l in enumerate(rl) if l.startswith('| `knowledge/%s`' % SIX[5]))
        rl.insert(i + 1, '| `knowledge/2026-10-16-l7-99-ghost` | dangling | none |')
        txt['corpus/README.md'] = '\n'.join(rl)
    def m_dupmap(txt, tree, changed):
        rl = txt['corpus/README.md'].splitlines()
        i = next(i for i, l in enumerate(rl) if l.startswith('| `knowledge/%s`' % SIX[0]))
        rl.insert(i + 1, rl[i]); txt['corpus/README.md'] = '\n'.join(rl)
    def m_empty(txt, tree, changed):
        txt['corpus/knowledge/%s.md' % SIX[0]] = ''
    def m_scorcard(txt, tree, changed):
        txt['SCORECARD.md'] = txt['SCORECARD.md'].replace('import json, pathlib, re, subprocess, sys', 'import json, pathlib, re, subprocess, sys  # patched')
    def m_province(txt, tree, changed):
        txt['PROVINCE.md'] = txt['PROVINCE.md'] + '\n# patched\n'
    def m_log(txt, tree, changed):
        changed.append('LOG.md')
    matrix = [('conforming (control)', None, set()),
              ('underscore stems', m_underscore, {'C2', 'C4', 'C5'}),
              ('entry missing recheck:', m_recheck, {'C8'}),
              ('prior entry edited', m_baseedit, {'C2'}),
              ('README baseline line edited', m_readmeedit, {'C7'}),
              ('map row dropped', m_maprowdrop, {'C4', 'C5'}),
              ('extra 79th knowledge file', m_extrafile, {'C1', 'C2'}),
              ('promotion claim in entry', m_promo, {'C14'}),
              ('receipt range out of bounds', m_oob, {'C12'}),
              ('carrier hash removed', m_hashdel, {'C11'}),
              ('sqlite lane-A fixture admitted', m_sqlitea, {'C15'}),
              ('rust 2nd carrier dropped', m_rustdrop, {'C11'}),
              ('knowledge-row wrong date', m_kndate, {'C6'}),
              ('map row in wrong section', m_wrongsec, {'C5'}),
              ('dangling token', m_dangling, {'C1', 'C4'}),
              ('duplicate map row', m_dupmap, {'C5'}),
              ('empty entry body', m_empty, {'C8', 'C9', 'C10', 'C11'}),
              ('Command A body edited', m_scorcard, {'C0'}),
              ('PROVINCE edited', m_province, {'C16'}),
              ('records-only change (WARN)', m_log, set())]
    bad = 0
    for name, mut, expect in matrix:
        res, verdict, fails, warns, counts = build(mut)
        if name.startswith('conforming'):
            ok = verdict == 'PASS' and not fails
            print('%-36s control verdict=%s %s' % (name, verdict, 'OK' if ok else '<<CONTROL-BROKEN>>'))
        elif 'WARN' in name:
            ok = not fails and 'C19' in warns
            print('%-36s WARN-only fails=%s C19warn=%s %s' % (name, fails, 'C19' in warns, 'OK' if ok else '<<MISS>>'))
        else:
            missed = sorted(expect - set(fails))
            ok = verdict == 'FINDING' and not missed
            print('%-36s caught=%s %s' % (name, fails, 'OK' if ok else '<<MISS %s>>' % missed))
        bad += 0 if ok else 1
    print('SELFTEST %s (%d states)' % ('PASS' if bad == 0 else 'FAIL(%d)' % bad, len(matrix)))
    return 0 if bad == 0 else 2

def main():
    if os.environ.get('CB7_SELFTEST') == '1':
        return selftest()
    rev = os.environ.get('CB7_REV') or git('rev-parse', 'HEAD').strip()
    read_rev, read_base = make_reader(rev), make_reader(BASE)
    tree_rev, tree_base = make_tree(rev), make_tree(BASE)
    a_json = run_cmd_a(rev)
    changed = [l for l in git('diff', '--name-only', BASE, rev).splitlines() if l]
    dirty = git('status', '--porcelain', '--', 'corpus/README.md', 'corpus/knowledge', 'SCORECARD.md', 'SKILL.md', 'PROVINCE.md').strip()
    strict = os.environ.get('CB7_STRICT_README', '1') != '0'
    res, verdict, fails, warns, counts = census(read_rev, read_base, tree_rev, tree_base, a_json,
                                                strict_readme=strict, changed_paths=changed, dirty=dirty)
    print('CB7 FINAL CENSUS rev=%s base=%s' % (rev[:12], BASE[:12]))
    for r in res:
        print('%-4s %-4s %s' % (r['level'], r['cid'], r['detail']))
    print('CENSUS RESULT: %s%s' % (verdict, '' if verdict == 'PASS' else ' — FAIL %s' % fails))
    print('CENSUS_JSON ' + json.dumps({'revision': rev, 'base': BASE, 'verdict': verdict, 'fail': fails, 'warn': warns, 'counts': counts}, sort_keys=True))
    return 0 if verdict == 'PASS' else 1

sys.exit(main())
PY
```
<!-- CB7-FROZEN-CMD-END -->
