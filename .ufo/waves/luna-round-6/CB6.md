## CLAIM
Frozen, read-only round-6 census: hashes 10 lane-A + 10 lane-B receipts; derives classes from digest-verified stdout blocks; scores both lanes vs the pre-registered classes (gate >=8/10); measures agreement N/10; checks zero drift (frozen HEAD, clean worktree, Command A + token set vs both baselines, 6.5.0 pins). Live run at f0e8cde: PASS.

## METHOD
Parsing is format-agnostic: fenced and marker-bounded blocks; digests by label context; exit codes inline or heading+next-lines; class from JSON-RPC frames/bare payloads in digest-verified blocks first, declared class second (conflict = FAIL). Gates: 20/20 receipts; exit 0 + recomputing digest each; route token allowed + request/response route consistency; no byte-identical A/B receipt; scores >=8; agreement >=8; drift zero. Attacked with 18 mutated wave copies (`/tmp/rea-cb6/mksims.py`; matrix `/tmp/rea-cb6/attack-matrix-final.txt`): 13 fail closed; 4 limit/policy cases below. The command below is the frozen deliverable (script sha256 `cc9f3e78fb9f95f9bff0f35204481840dc26847e14836e39833d72a8afece18d`); run from repo root; read-only; exit 0 = PASS.

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -B - "$PWD" <<'PY'
#!/usr/bin/env python3
"""luna-round-6 final census - CB6 (lane B, freeze v2). Read-only: no writes, no network, no MCP.
Usage: python3 -B census.py <repo-root>          (CB6_WAVE env overrides the wave dir for attack sims)
Pre-registered gates: 20/20 receipts present; per-lane score >=8/10; class agreement >=8/10;
zero drift (frozen HEAD, tracked-clean worktree, Command A + coverage-map token set equal to
receipts/census-pre.txt, every receipt pinning rea-agents@6.5.0); no digest/class/route conflicts.
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
WAVE = Path(os.environ.get('CB6_WAVE') or (ROOT / '.ufo/waves/luna-round-6'))
FROZEN_HEAD = 'f0e8cdecb216d71cf7df974675c0f6b16ba4f82f'
PRED = {1:'RESULT',2:'RESULT',3:'RESULT',4:'RESULT',5:'RESULT',6:'RESULT',7:'RESULT',8:'RESULT',9:'TYPED-REFUSAL',10:'TYPED-REFUSAL'}
ALLOWED = {1:{'--version'},2:{'tools/list'},3:{'inspect_go_binary'},4:{'inspect_rust_binary'},
           5:{'inspect_electron_fuses'},6:{'inspect_sqlite_database'},7:{'search_bytes'},
           8:{'inspect_with_objdump'},9:{'identify_flutter_build'},
           10:{'compare_wasm_interfaces','project_harmony_application_graph','inspect_wasm_artifact'}}
DIVERGENT = {10:{'inspect_wasm_artifact'}}
SCAN = sorted({t for s in ALLOWED.values() for t in s} | {'open_binary','--version'})
HEX = re.compile(r'\b[0-9a-f]{64}\b')
CLS = re.compile(r'\b(RESULT|TYPED-REFUSAL|ERROR-UNEXPECTED)\b')
EXIT = [re.compile(r'(?i)exit[\s_]*code(?:\s+was)?\s*[:=]?\s*`?(\d+)`?'), re.compile(r'(?i)\bexit\s*[:=]\s*(\d+)'), re.compile(r'(?i)\bexit\s+(\d+)\b')]
EXIT_H = re.compile(r'(?i)^\W*(process exit code|mcp server exit code|server exit code|exit code|exit)\W*$')
SUBP = {1:['6.5.0'], 2:['"count":207']}

def sha256(b): return hashlib.sha256(b).hexdigest()

def blocks(text):
    lines = text.split('\n'); out = []; i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith('`'):
            ticks = s[:len(s)-len(s.lstrip('`'))]; buf = []; j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(ticks): buf.append(lines[j]); j += 1
            if j < len(lines): out.append('\n'.join(buf)); i = j + 1; continue
        elif re.match(r'^-{2,}\s*(BEGIN|RAW)\b', s):
            buf = []; j = i + 1
            while j < len(lines) and not re.match(r'^-{2,}\s*END\b', lines[j].strip()): buf.append(lines[j]); j += 1
            if j < len(lines): out.append('\n'.join(buf)); i = j + 1; continue
        i += 1
    return out

def payloads(text):
    lines = text.split('\n'); out = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if 'stdout' not in s.lower() or 'sha' in s.lower() or 'stdin' in s.lower() or 'stderr' in s.lower(): continue
        j = i + 1
        while j < len(lines) and not lines[j].strip(): j += 1
        if j >= len(lines): continue
        if lines[j].strip().startswith('`'):
            ticks = lines[j].strip()[:len(lines[j].strip())-len(lines[j].strip().lstrip('`'))]; buf = []; k = j + 1
            while k < len(lines) and not lines[k].strip().startswith(ticks): buf.append(lines[k]); k += 1
            if k < len(lines): out.append('\n'.join(buf))
        elif lines[j].lstrip().startswith('{'):
            buf = []; k = j
            while k < len(lines):
                if lines[k].lstrip().startswith('{'): buf.append(lines[k].strip()); k += 1
                elif not lines[k].strip(): k += 1
                else: break
            if buf: out.append('\n'.join(buf))
    return out

def cand_hashes(texts):
    C = {}
    for b in texts:
        for c in (b, b + '\n', b.rstrip('\n'), b.rstrip('\n') + '\n'):
            try: C.setdefault(sha256(c.encode('utf-8')), True)
            except UnicodeEncodeError: pass
    return C

def structural_class(frames, bare):
    calls = [f for f in frames if isinstance(f.get('result'), dict) and ('content' in f['result'] or 'isError' in f['result'])]
    if calls:
        r = calls[-1]['result']; inner = None
        c = r.get('content')
        text = c[0].get('text') if isinstance(c, list) and c and isinstance(c[0], dict) else None
        if isinstance(text, str):
            try: inner = json.loads(text)
            except Exception: inner = None
        if isinstance(inner, dict) and isinstance(inner.get('error'), dict) and ('code' in inner['error'] or 'category' in inner['error']) and 'evidence_id' not in inner:
            return 'TYPED-REFUSAL'
        if r.get('isError') is True: return 'ERROR-UNEXPECTED'
        return 'RESULT'
    for d in reversed(bare):
        if not isinstance(d, dict): continue
        if isinstance(d.get('error'), dict) and ('code' in d['error'] or 'category' in d['error']): return 'TYPED-REFUSAL'
        if 'evidence_id' in d or 'normalized_result' in d or 'structuredContent' in d: return 'RESULT'
    res = [f for f in frames if isinstance(f.get('result'), dict)]
    err = [f for f in frames if 'error' in f]
    meaningful = [f for f in res if 'protocolVersion' not in f['result'] or 'tools' in f['result']]
    if err and not meaningful: return 'ERROR-UNEXPECTED'
    if meaningful: return 'RESULT'
    return None

def parse(path, n):
    d = {'present': False, 'leg': n}
    if not path.exists(): return d
    d['present'] = True
    b = path.read_bytes(); text = b.decode('utf-8', 'replace'); lines = text.split('\n')
    d['file_sha256'] = sha256(b)
    exits = []
    for i, ln in enumerate(lines):
        for rx in EXIT:
            for m in rx.finditer(ln): exits.append(int(m.group(1)))
        if EXIT_H.match(ln.strip()):
            for j in range(i + 1, min(i + 5, len(lines))):
                m = re.match(r'^\s*`?(\d+)`?\s*$', lines[j])
                if m: exits.append(int(m.group(1))); break
    d['exit'] = exits[-1] if exits else None; d['exits_all'] = sorted(set(exits))
    texts = blocks(text) + payloads(text)
    C = cand_hashes(texts)
    digs = []
    for i, ln in enumerate(lines):
        hs = HEX.findall(ln)
        if not hs: continue
        if 'sha' not in ' '.join(lines[max(0, i-3):i+2]).lower(): continue
        if re.search(r'(?i)stderr', ln) and not re.search(r'(?i)stdout', ln): continue
        label = 'stdout' if re.search(r'(?i)stdout', ln) else None
        if label is None:
            for j in range(i, max(-1, i - 7), -1):
                if re.search(r'(?i)stdout', lines[j]): label = 'stdout'; break
                if re.search(r'(?i)stderr', lines[j]): break
        if label != 'stdout': continue
        for h in hs[:2]:
            if 'urn:' in ln and re.search(r'sha-?256:' + re.escape(h), ln): continue
            if ('stdout', h) not in digs: digs.append(('stdout', h))
    ds = [h for l, h in digs]
    ded = []
    for h in ds:
        if h not in ded: ded.append(h)
    d['digests'] = ded
    verified = [h for h in ded if h in C]
    prim = [h for l, h in digs if l == 'stdout' and not re.search(r'(?i)raw process|process stdout', l)]
    if verified:
        pref = [h for h in prim if h in verified]
        d['digest'] = (pref or verified)[0]; d['recheck'] = 'match'
    elif ded:
        d['digest'] = (prim or ded)[0]; d['recheck'] = 'mismatch' if C else 'unverified'
    else:
        d['digest'] = None; d['recheck'] = 'absent'
    d['digests_verified'] = len(verified); d['digests_total'] = len(ded)
    d['warns'] = []
    def t_hashes(t):
        out = set()
        for c in (t, t + '\n', t.rstrip('\n'), t.rstrip('\n') + '\n'):
            try: out.add(sha256(c.encode('utf-8')))
            except UnicodeEncodeError: pass
        return out
    trusted = [t for t in texts if t_hashes(t) & set(verified)] if verified else []
    def scan(ts):
        fr = []; ba = []; rq = set(); rp = set(); sv = set()
        for t in ts:
            st = t.strip()
            if st.startswith('{'):
                try:
                    f = json.loads(st)
                    if isinstance(f, dict): ba.append(f)
                except Exception: pass
            for ln in t.split('\n'):
                s = ln.strip()
                if not s.startswith('{'): continue
                try: f = json.loads(s)
                except Exception: continue
                if not (isinstance(f, dict) and f.get('jsonrpc') == '2.0'): continue
                fr.append(f)
                if f.get('method') == 'tools/call' and isinstance(f.get('params'), dict) and f['params'].get('name'):
                    rq.add(f['params']['name'])
                if f.get('method') == 'tools/list': rq.add('tools/list')
                r = f.get('result') if isinstance(f.get('result'), dict) else None
                c = r.get('content') if r else None
                if isinstance(c, list) and c and isinstance(c[0], dict) and isinstance(c[0].get('text'), str):
                    try: inner = json.loads(c[0]['text'])
                    except Exception: inner = None
                    if isinstance(inner, dict) and isinstance(inner.get('operation'), str): rp.add(inner['operation'])
                si = r.get('serverInfo') if r else None
                if isinstance(si, dict) and isinstance(si.get('version'), str): sv.add(si['version'])
        return fr, ba, rq, rp, sv
    tr = scan(trusted); allx = scan(texts)
    st = structural_class(tr[0], tr[1])
    if st is None:
        st2 = structural_class(allx[0], allx[1])
        if st2 and trusted: d['warns'].append(f'class taken from unverified block ({st2}); verified blocks carry no class evidence')
        st = st2
    d['trusted_blocks'] = len(trusted)
    frames = allx[0]; req = allx[2]; resp = allx[3]; srvver = allx[4]
    d['frames'] = len(frames)
    route = set(req) | set(resp); d['route_src'] = 'frames'
    if not route:
        route = {t for t in SCAN if t in text}; d['route_src'] = 'text' + ('-ambiguous' if len(route) > 3 else '')
    d['route'] = sorted(route)
    d['req_route'] = sorted(req); d['resp_route'] = sorted(resp)
    d['route_conflict'] = bool(req and resp and not (req & resp))
    d['route_ok'] = bool(set(route) & ALLOWED[n])
    d['route_divergent'] = d['route_ok'] and not (set(route) & (ALLOWED[n] - DIVERGENT.get(n, set())))
    decl = None
    for ln in lines:
        if re.match(r'(?i)^\W*(outcome\s*class|class|observed|verdict|decision|result class)\b', ln.strip()):
            t = CLS.findall(ln)
            if t: decl = t[-1]
    if decl is None:
        for ln in lines:
            if '→' in ln and not re.search(r'(?i)frozen|pre-?register|predict', ln):
                t = CLS.findall(ln)
                if t: decl = t[-1]
    if d['exit'] not in (0, None): cls, src = 'ERROR-UNEXPECTED', 'exit-code'
    elif st: cls, src = st, 'structural'
    elif decl: cls, src = decl, 'declared'
    elif d['exit'] == 0 and any(t in text for t in SUBP.get(n, [])) and not re.search(r'(?i)capability_unavailable|traceback|command not found|ENOENT', text):
        cls, src = 'RESULT', 'fallback'
    else: cls, src = None, None
    d['cls'] = cls; d['cls_src'] = src; d['declared'] = decl
    d['conflict'] = bool(st and decl and st != decl)
    d['pins'] = sorted(set(re.findall(r'rea-agents@([0-9][A-Za-z0-9.\-]*)', text)))
    d['srvver'] = sorted(srvver)
    d['subpred'] = all(t in text for t in SUBP.get(n, []))
    return d

def command_a(rev):
    g = lambda p: subprocess.check_output(['git', 'show', f'{rev}:{p}'], cwd=ROOT, text=True)
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'], cwd=ROOT, text=True).splitlines()
    files = {Path(p).stem for p in paths if p.endswith('.md')}
    section = g('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    tokens = sorted(set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section)))
    craft = g('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule); valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(g('corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError: valid = False
        resolved += valid
    return {'revision': rev, 'mapped': len(files & set(tokens)), 'knowledge_files': len(files),
            'missing': sorted(files - set(tokens)), 'dangling': sorted(set(tokens) - files),
            'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
            'coverage_score': round(10*len(files & set(tokens))/len(files), 2),
            'depth_score': round(10*resolved/len(rules), 2)}, tokens, '\n'.join(tokens) + '\n'

def main():
    out = []; warns = []; fails = []
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    status = [l for l in subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=ROOT, text=True).split('\n') if l]
    tracked_dirty = [l for l in status if not l.startswith('??')]
    head_ok = head == FROZEN_HEAD; wt_ok = not tracked_dirty
    if not head_ok: fails.append(f'HEAD {head} != frozen {FROZEN_HEAD}')
    if not wt_ok: fails.append('tracked worktree modifications: ' + '; '.join(tracked_dirty[:3]))
    a_ok = tok_ok = None; srcs = 0; cmp_a = []; cmp_t = []
    for bn in ('census-pre.txt', 'census-laneB-pre.txt'):
        bpath = WAVE / 'receipts' / bn
        if not bpath.exists(): continue
        srcs += 1
        bt = bpath.read_text()
        m = re.search(r'^COMMAND_A (\{.*\})$', bt, re.M) or re.search(r'^(\{[^\n]*"revision"[^\n]*"mapped"[^\n]*\})$', bt, re.M)
        base = json.loads(m.group(1)) if m else None
        m = re.search(r'^MAP_TOKEN_SHA256 ([0-9a-f]{64})$', bt, re.M); ftok = m.group(1) if m else None
        m = re.search(r'^MAP_TOKEN_COUNT (\d+)$', bt, re.M); fn = int(m.group(1)) if m else None
        a, tokens, toktext = command_a(FROZEN_HEAD)
        if base is None:
            warns.append(f'{bn}: no parseable Command A record; token set compared only')
        else:
            same = base == a; cmp_a.append(same)
            if not same: fails.append(f'Command A output != {bn} baseline')
        if ftok is None or fn is None:
            warns.append(f'{bn}: no parseable token-set record')
        else:
            same = ftok == sha256(toktext.encode()) and fn == len(tokens); cmp_t.append(same)
            if not same: fails.append(f'coverage-map token set != {bn} baseline')
    a_ok = all(cmp_a) if cmp_a else None
    tok_ok = all(cmp_t) if cmp_t else None
    if srcs == 0:
        fails.append('no census-pre baseline: command A drift unverifiable')
    out_note = f'baselines={srcs} commandA_sources={len(cmp_a)} token_sources={len(cmp_t)}'
    rows = {'A': {}, 'B': {}}
    extras = {'A': 0, 'B': 0}; nodecl = {'A': [], 'B': []}
    for lane in ('A', 'B'):
        for n in range(1, 11):
            d = parse(WAVE / ('receipts' if lane == 'A' else 'receipts-B') / f'leg-{n}.md', n)
            rows[lane][n] = d
            if not d['present']: continue
            if d['exit'] is None: fails.append(f'{lane}{n} no exit code recorded')
            elif d['exit'] != 0: fails.append(f'{lane}{n} exit={d["exit"]}')
            warns += [f'{lane}{n} {w}' for w in d.get('warns', [])]
            if d['digest'] is None: fails.append(f'{lane}{n} no stdout digest recorded')
            if d['recheck'] in ('mismatch', 'absent'): fails.append(f'{lane}{n} stdout digest {d["recheck"]} ({d["digests_verified"]}/{d["digests_total"]} verified)')
            if d['recheck'] == 'unverified': warns.append(f'{lane}{n} digest unverified: no hashable stdout block')
            if d['digests_verified'] < d['digests_total']: extras[lane] += 1
            if d['conflict']: fails.append(f'{lane}{n} class conflict declared={d["declared"]} structural-differs')
            if d['cls'] is None: fails.append(f'{lane}{n} outcome class undeterminable')
            if not d['route_ok']: fails.append(f'{lane}{n} route {d["route"]} not in allowed {sorted(ALLOWED[n])}')
            if d.get('route_conflict'): fails.append(f'{lane}{n} request route {d["req_route"]} vs response route {d["resp_route"]} share no tool')
            if d['route_divergent']: warns.append(f'{lane}{n} route {"+".join(d["route"])} diverges from predicted route')
            if d['declared'] is None: nodecl[lane].append(n)
            if not d['subpred']: warns.append(f'{lane}{n} sub-predicate token missing')
            if any(v != '6.5.0' for v in d['pins']): fails.append(f'{lane}{n} version drift pins={d["pins"]}')
            if any(v != '6.5.0' for v in d['srvver']): fails.append(f'{lane}{n} version drift serverInfo={d["srvver"]}')
            if not d['pins']: warns.append(f'{lane}{n} no rea-agents version pin found')
    for lane in ('A', 'B'):
        if extras[lane]: warns.append(f'lane {lane}: {extras[lane]} receipts carry extra unverified stdout-labeled digests (carrier/mirror hashes)')
        if nodecl[lane]: warns.append(f'lane {lane}: no declared class on legs {nodecl[lane]} (class derived structurally)')
    presA = sum(rows['A'][n]['present'] for n in range(1, 11)); presB = sum(rows['B'][n]['present'] for n in range(1, 11))
    if presA != 10: fails.append(f'lane A receipts {presA}/10')
    if presB != 10: fails.append(f'lane B receipts {presB}/10')
    sA = sum(1 for n in range(1, 11) if rows['A'][n]['present'] and rows['A'][n]['cls'] == PRED[n])
    sB = sum(1 for n in range(1, 11) if rows['B'][n]['present'] and rows['B'][n]['cls'] == PRED[n])
    agree = sum(1 for n in range(1, 11) if rows['A'][n]['present'] and rows['B'][n]['present'] and rows['A'][n]['cls'] and rows['A'][n]['cls'] == rows['B'][n]['cls'])
    if sA < 8: fails.append(f'score A {sA}/10 < 8')
    if sB < 8: fails.append(f'score B {sB}/10 < 8')
    if agree < 8: fails.append(f'class agreement {agree}/10 < 8')
    for n in range(1, 11):
        a, b = rows['A'][n], rows['B'][n]
        if a['present'] and b['present'] and a['file_sha256'] == b['file_sha256']:
            fails.append(f'leg {n}: lane-B receipt byte-identical to lane-A (not independent)')
    def rt(d):
        r = d.get('route') or []
        if len(r) > 3 and (d.get('route_src') or '').startswith('text'): return f'text-scan({len(r)})'
        return '+'.join(r) or '-'
    out.append(f'HEAD {head} frozen={FROZEN_HEAD} ok={head_ok} commandA_ok={a_ok} tokens_ok={tok_ok} tracked_dirty={len(tracked_dirty)} {out_note}')
    out.append('LEG  A-class(src)        B-class(src)        pred           match  agree  digest(A/B)  route(A) -> route(B)')
    for n in range(1, 11):
        a, b = rows['A'][n], rows['B'][n]
        ac, bc = a.get('cls'), b.get('cls')
        fa = f"{(ac or '-'):<10}@{a.get('cls_src')}" if a['present'] else 'MISSING'
        fb = f"{(bc or '-'):<10}@{b.get('cls_src')}" if b['present'] else 'MISSING'
        out.append(f"{n:>2}  {fa:<20} {fb:<20} {PRED[n]:<14} "
                   f"{('Y' if ac==PRED[n] else '.')}{('Y' if bc==PRED[n] else '.')}     "
                   f"{'Y' if ac and ac==bc else '.'}      "
                   f"{(a.get('recheck', '-')[:3] if a['present'] else '-'):<4}{(b.get('recheck', '-')[:3] if b['present'] else '-'):<4} "
                   f"A={rt(a)} -> B={rt(b)}")
    for lane in ('A', 'B'):
        for n in range(1, 11):
            d = rows[lane][n]
            if d['present']: out.append(f'RECEIPT_SHA256 {lane} {n} {d["file_sha256"]}')
    out.append(f'RECEIPTS A={presA}/10 B={presB}/10   SCORE A={sA}/10 B={sB}/10 (gate >=8)   AGREEMENT {agree}/10 (gate >=8)')
    mism = [n for n in range(1, 11) if not (rows['A'][n].get('cls') == rows['B'][n].get('cls') == PRED[n])]
    out.append(f'PREDICTION_MISMATCH_LEGS {mism or "none"}')
    if mism: warns.append(f'prediction mismatch or class disagreement on legs {mism}: adjudicate against frozen classes')
    for w in warns: out.append('WARN ' + w)
    for f_ in fails: out.append('FAIL ' + f_)
    verdict = 'PASS' if not fails else 'FAIL'
    out.append(f'CENSUS RESULT: {verdict}')
    j = {'head': head, 'head_ok': head_ok, 'command_a_ok': a_ok, 'tokens_ok': tok_ok,
         'receipts_sha256': {l: {n: rows[l][n].get('file_sha256') for n in range(1, 11)} for l in ('A', 'B')},
         'classes': {l: {n: rows[l][n].get('cls') for n in range(1, 11)} for l in ('A', 'B')},
         'recheck': {l: {n: rows[l][n].get('recheck') for n in range(1, 11)} for l in ('A', 'B')},
         'score': {'A': sA, 'B': sB}, 'agreement': agree, 'warnings': warns, 'failures': fails, 'verdict': verdict}
    out.append('CENSUS_JSON ' + json.dumps(j, sort_keys=True))
    print('\n'.join(out))
    return 0 if verdict == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
PY
```

## FINDINGS
Measured 2026-10-16T19:18-03:00 (transcript sha256 `75ea5a8f6a735fb820a1759b47a7c3a0ef39323417d1261edfff9d4668fbc32e`):
- `commandA_ok=True tokens_ok=True tracked_dirty=0 baselines=2`; HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`.
- `RECEIPTS A=10/10 B=10/10`; `SCORE A=10/10 B=10/10`; `AGREEMENT 10/10`; `PREDICTION_MISMATCH_LEGS none`; `CENSUS RESULT: PASS` (exit 0); digest `mat` 20/20; 20 file hashes printed.
- Warns: L10 route divergence both lanes (`inspect_wasm_artifact` vs predicted compare/harmony; class matched); 7 A + 6 B receipts carry extra unverified carrier/mirror digests; 9 declare no class (derived structurally); B4's harness digest `84d489f7...` does not recompute (server-raw record does).
- Detected (FAIL with reason): digest/byte tamper, decoy-in-block, declared lie, swap, A-copy, truncation, exit!=0, pin drift, missing receipt, route half-swap, digest removal, half-forgery. Limits: alternate-record or duplicate-occurrence tamper -> warn only; decoy outside digest-bound blocks inert; self-consistent lane forgery passes >=8 but is flagged (`PREDICTION_MISMATCH_LEGS [9]`).

## THREATS
Consistency is not authenticity: a self-consistent forgery (block+digest+declared rewritten in one lane) passes the round's >=8 gate, flagged only (demonstrated on B9). Digest verification is existential (>=1 record), so alternate/duplicate-record tampers degrade to warns. L2 route evidence is a text scan (catalogue names all tools). Receipts may be rewritten after this run; output file hashes pin the snapshot. Reads files only; host drift covered by HEAD, pins, serverInfo, Command A.

## VERDICT
CLEAN: PASS on the live wave (20/20, 10/10 both lanes, agreement 10/10, zero drift vs two baselines); warn/flag-level limits demonstrated - adjudicate L10's divergent route and B4's harness-digest anomaly.
