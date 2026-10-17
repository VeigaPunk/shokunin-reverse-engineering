## CLAIM
Design-2 final census of the round-8 6.4.0 symmetry battery: all ten frozen predictions verify from digest-anchored receipt evidence (10/10); controls unchanged; every canonical-receipt mutation class fails closed; the known leg-3 display defect is historical (leg-3.md coherent); provenance discontinuities surfaced, not hidden.

## METHOD
Read-only; no probes or writes. Evidence rule: a leg's class must come from JSON-RPC frames inside a fenced block whose sha256 (raw or raw+LF) equals a sha-labeled digest in that receipt; declared classes advisory; conflicts fail. L9 re-run live (`grep -nFw` per name on `leg-2-tools.txt` plus the parsed tools/list set). Controls at pinned `6e2ee8f`: tracked status; Command A and coverage-map token set vs `receipts/census-pre.txt`; SCORECARD worktree==blob. Provenance: MANIFEST, census-pre table, SE2 sentinels, /tmp raw cross-checks. Attack: control + 12 mutants (`/tmp/rea-cb5/sims`; matrix `/tmp/rea-cb5/attack-matrix-final2.txt`). Frozen final command (script sha256 `f52e6d20afa2a2f28256a503e2f1006da470204650487a90122c3dc56c65981b`; exit 0 = content PASS; `CB5_STRICT=1` promotes provenance findings to exit 1):

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && timeout 240 python3 -B - "$PWD" <<'PY'
#!/usr/bin/env python3
"""luna-round-8 final census - CB5 (lane B, census design 2). Read-only; no network/MCP.

Usage: python3 -B census2.py [repo-root]
Env:   CB5_WAVE=<dir>   override wave dir (attack sims; default <root>/.ufo/waves/luna-round-8)
       CB5_STRICT=1     promote provenance mismatches to failures

Gates (content): 10 canonical receipts present/regular/non-empty/non-symlink and not
byte-identical; per-leg evidence must sit in a fenced block whose sha256 (raw or raw+LF)
equals a sha-labeled digest in that receipt; frozen predictions per P0.md (L1=6.4.0,
L2=170 tools in list order, L3-L8 TYPED-REFUSAL with exact -32602/"Tool <name> not found",
L9 six names absent: live grep -Fw re-run + parsed tools set; L10 control = RESULT for
inspect_binary_layout on jq); exit code 0 per leg; score >=9/10 (P0 gate).
Controls: HEAD pinned 6e2ee8f, tracked worktree clean, Command A + coverage-map token set
recomputed at pinned rev and compared to receipts/census-pre.txt, SCORECARD worktree==blob.
Provenance (CB5_STRICT=1 -> failures): per-file hash vs MANIFEST.txt; per-file hash/size vs
census-pre receipt table; config sentinels vs SE2.md record; best-effort /tmp raw cross-checks.
Exit 0 = content PASS (provenance findings still printed), 1 = content FAIL (or strict).
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
WAVE = Path(os.environ.get('CB5_WAVE') or (ROOT / '.ufo/waves/luna-round-8'))
REC = WAVE / 'receipts'
STRICT = os.environ.get('CB5_STRICT') == '1'
PINNED = '6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4'
SIX = ['inspect_go_binary', 'inspect_rust_binary', 'inspect_electron_fuses',
       'inspect_sqlite_database', 'search_bytes', 'inspect_with_objdump']
TOOL = {3: 'inspect_go_binary', 4: 'inspect_rust_binary', 5: 'inspect_electron_fuses',
        6: 'inspect_sqlite_database', 7: 'search_bytes', 8: 'inspect_with_objdump'}
PRED = {1: 'VERSION-6.4.0', 2: 'TOOLS-170', 3: 'TYPED-REFUSAL', 4: 'TYPED-REFUSAL',
        5: 'TYPED-REFUSAL', 6: 'TYPED-REFUSAL', 7: 'TYPED-REFUSAL', 8: 'TYPED-REFUSAL',
        9: 'ABSENTx6', 10: 'RESULT'}
CLAIM_RX = {1: r'(?i)stdout sha256:\s*`([0-9a-f]{64})`',
            2: r'STDOUT SHA-256:\s*`([0-9a-f]{64})`',
            3: r'Full stdout SHA-256: `([0-9a-f]{64})`',
            4: r'Full stdout SHA-256: `([0-9a-f]{64})`',
            5: r'MCP server stdout sha256: `([0-9a-f]{64})`',
            6: r'(?i)STDOUT SHA-256:\s*`([0-9a-f]{64})`',
            7: r'STDOUT SHA-256 \(raw MCP stdout\): `([0-9a-f]{64})`',
            8: r'(?i)STDOUT SHA-256:\s*`([0-9a-f]{64})`',
            10: r'FULL SERVER STDOUT SHA-256: `([0-9a-f]{64})`'}
OPENBIN_SHA = '8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d'
JQ_SHA = 'e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806'
EXPECT_A = {'mapped': 78, 'knowledge_files': 78, 'missing': [], 'dangling': [],
            'citation_resolved_rules': 9, 'rule_blocks': 9,
            'coverage_score': 10.0, 'depth_score': 10.0}

def sha(b): return hashlib.sha256(b).hexdigest()
def sh(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
def git(*a): return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True)

TICKS = '`' * 3

def blocks(text):
    out = []
    for m in re.finditer(TICKS + r'([^\n`]*)\n(.*?)\n' + TICKS, text, re.S):
        out.append((m.group(1).strip(), m.group(2)))
    return out

def frames_of(text):
    out = []
    for ln in text.split('\n'):
        s = ln.strip()
        if s.startswith('{') and '"jsonrpc"' in s:
            try: f = json.loads(s)
            except Exception: continue
            if isinstance(f, dict): out.append(f)
    return out

def dedupe(fr):
    seen, out = set(), []
    for f in fr:
        k = json.dumps(f, sort_keys=True)
        if k not in seen: seen.add(k); out.append(f)
    return out

def parse_receipt(n):
    p = REC / f'leg-{n}.md'
    d = {'n': n, 'present': p.is_file() and not p.is_symlink() and p.stat().st_size > 0}
    if not d['present']: return d
    raw = p.read_bytes(); t = raw.decode('utf-8', 'replace')
    d['file'] = sha(raw); d['size'] = len(raw)
    bl = blocks(t); d['blocks'] = len(bl)
    candmap = {}
    for i, (lab, c) in enumerate(bl):
        for mode, s in (('raw', c), ('raw+lf', c + '\n')):
            candmap.setdefault(sha(s.encode()), []).append((i, mode, len(s.encode())))
    claims = set()
    for ln in t.split('\n'):
        if re.search(r'(?i)\bsha', ln): claims.update(re.findall(r'[0-9a-f]{64}', ln))
    d['claims'] = claims; d['candmap'] = candmap
    allf = dedupe(frames_of('\n'.join(c for _, c in bl)) + frames_of(t))
    # trusted frames: frames from blocks whose content-modes hash to a claim
    vf = []
    for _, c in bl:
        if sha(c.encode()) in claims or sha((c + '\n').encode()) in claims:
            vf += frames_of(c)
    d['frames_all'] = allf; d['frames_v'] = dedupe(vf)
    m = re.search(CLAIM_RX[n], t) if n in CLAIM_RX else None
    d['claim'] = m.group(1) if m else None
    d['claim_hit'] = bool(d['claim'] and d['claim'] in candmap)
    d['evidence'] = candmap.get(d['claim'], [])
    ex = re.search(r'(?i)^[>\-\s]*(?:outcome class|observed class|class)\s*[:\-]\s*(TYPED-REFUSAL|RESULT|ERROR-UNEXPECTED)\b', t, re.M)
    d['declared'] = ex.group(1) if ex else None
    d['exit'] = None
    m = re.search(r'(?i)(?:MCP server exit code|PROCESS EXIT CODE|process exit code|exit code)[:\s]*`?(\d+)`?', t)
    if m: d['exit'] = int(m.group(1))
    else:
        m = re.search(r'(?i)exit[:=]\s*`?(\d+)`?', t)
        if m: d['exit'] = int(m.group(1))
    return d

def resp_for(fr, rid):
    for f in fr:
        if f.get('id') == rid and ('error' in f or 'result' in f): return f
    for f in fr:
        if f.get('id') == rid: return f
    return None

def req_id(fr, name):
    for f in fr:
        if f.get('method') == 'tools/call' and isinstance(f.get('params'), dict) and f['params'].get('name') == name:
            return f.get('id')
    return None

def refusal_id(fr, name):
    for f in fr:
        e = f.get('error') if isinstance(f, dict) else None
        if isinstance(e, dict) and e.get('message') == f'Tool {name} not found':
            return f.get('id')
    return None

def main():
    fails, warns, prov, notes, tmpck = [], [], [], [], []
    lines = []
    head = git('rev-parse', 'HEAD').stdout.strip()
    status = [l for l in git('status', '--porcelain=v1').stdout.split('\n') if l]
    dirty = [l for l in status if not l.startswith('??')]
    head_ok = head == PINNED
    if not head_ok: fails.append(f'HEAD {head} != pinned {PINNED}')
    if dirty: fails.append(f'tracked worktree dirty: {dirty[:3]}')
    # inventory
    inv = {}
    for n in range(1, 11):
        d = parse_receipt(n); inv[n] = d
        if not d['present']: fails.append(f'leg-{n}.md missing/symlink/empty')
    tf = REC / 'leg-2-tools.txt'
    tlines = [l for l in tf.read_text().split('\n') if l] if tf.is_file() else []
    if not tf.is_file(): fails.append('leg-2-tools.txt missing')
    if len(tlines) != 170 or len(set(tlines)) != 170:
        fails.append(f'tools file: {len(tlines)} lines, {len(set(tlines))} unique (want 170/170)')
    files = [inv[n]['file'] for n in range(1, 11) if inv[n]['present']]
    if len(files) != len(set(files)):
        fails.append('two canonical leg receipts are byte-identical')
    # per-leg predicates
    rows = []
    names_parsed = None
    for n in range(1, 11):
        d = inv[n]
        cls, why, dig, exok = None, [], 'no', 'n/a'
        if not d['present']:
            rows.append((n, None, 'MISSING', False, 'no', 'n/a', '')); continue
        if n == 9:
            ok = []
            for nm in SIX:
                g = sh(['grep', '-nFw', '--', nm, str(tf)])
                ok.append(g.returncode == 1 and g.stdout == '' and g.stderr == '')
            d9 = all(ok) and (len(tlines) == 170) and (inv[2]['present'])
            cls = 'ABSENTx6' if d9 else 'ABSENCE-UNPROVEN'
            why.append(f'live-grep {sum(ok)}/6 exit1/empty; parsed-set check below')
            dig = f'grep-e3b0 {sum(ok)}/6'
        elif n == 1:
            if d['claim_hit']:
                i, mode, _ = d['evidence'][0]
                c = inv[1] and blocks((REC / 'leg-1.md').read_text())[i][1]
                txt = c + ('\n' if mode == 'raw+lf' else '')
                cls = 'VERSION-6.4.0' if txt.strip() == '6.4.0' else 'VERSION-OTHER'
            else: cls = 'NO-VERIFIED-BLOCK'
            dig = 'ok' if d['claim_hit'] else 'MISS'; exok = 'Y' if d['exit'] == 0 else 'N'
        elif n == 2:
            if d['claim_hit']:
                i, mode, sz = d['evidence'][0]
                c = blocks((REC / 'leg-2.md').read_text())[i][1] + ('\n' if mode == 'raw+lf' else '')
                fr = d['frames_all']
                tl = next((f for f in fr if f.get('id') == 2 and isinstance(f.get('result'), dict)
                           and isinstance(f['result'].get('tools'), list)), None)
                names_parsed = [x.get('name') for x in tl['result']['tools']] if tl else None
                if names_parsed:
                    cnt = len(names_parsed)
                    if names_parsed != tlines:
                        cls = 'TOOLS-FILE-MISMATCH'; why.append(f'parsed names != leg-2-tools.txt (count {cnt})')
                    elif cnt != 170:
                        cls = f'TOOLS-{cnt}'; why.append(f'count {cnt}')
                    else:
                        cls = 'TOOLS-170'
                    si = next((f for f in fr if f.get('id') == 1 and isinstance(f.get('result'), dict)), None)
                    v = si.get('result', {}).get('serverInfo', {}).get('version') if si else None
                    if v != '6.4.0': why.append(f'serverInfo={v}')
                else: cls = 'TOOLS-UNPARSED'
            else: cls = 'NO-VERIFIED-BLOCK'
            dig = 'ok' if d['claim_hit'] else 'MISS'; exok = 'Y' if d['exit'] == 0 else 'N'
        elif n in TOOL:
            tool = TOOL[n]
            rid = req_id(d['frames_all'], tool)
            req_seen = rid is not None
            if rid is None: rid = refusal_id(d['frames_all'], tool)
            resp = resp_for(d['frames_all'], rid) if rid is not None else None
            if resp is not None and 'error' in resp:
                e = resp['error']
                cls = 'TYPED-REFUSAL' if (e.get('code') == -32602 and e.get('message') == f'Tool {tool} not found') else 'ERROR-UNEXPECTED'
                if cls == 'TYPED-REFUSAL':
                    if not any(f.get('id') == rid and f.get('error') for f in d['frames_v']):
                        why.append('refusal frame not from a digest-verified block'); cls = 'REFUSAL-UNTRUSTED'
                else: why.append(f'code={e.get("code")} msg={e.get("message")!r}')
            elif resp is not None: cls = 'RESULT'; why.append('tool call returned a result')
            else: cls = 'NO-RESPONSE'; why.append(f'no response frame for {tool}')
            if not req_seen and cls == 'TYPED-REFUSAL': why.append('request described in prose (no embedded frame)')
            if d['claim_hit']: dig = 'ok'
            else: dig = 'MISS'; why.append('claimed stdout digest does not recompute')
            exok = 'Y' if d['exit'] == 0 else 'N'
            if d['declared'] and cls in ('TYPED-REFUSAL', 'RESULT', 'ERROR-UNEXPECTED') and d['declared'] != cls:
                why.append(f'declared {d["declared"]} conflicts')
            if n == 7:
                oid = req_id(d['frames_all'], 'open_binary')
                ors = resp_for(d['frames_all'], oid) if oid is not None else None
                if not (ors and 'result' in ors and OPENBIN_SHA in json.dumps(ors)):
                    why.append('open_binary control result/hash absent'); cls = 'CONTROL-MISSING'
        elif n == 10:
            hits = re.findall(r'SERVER STDOUT SHA-256: `([0-9a-f]{64})`', (REC / 'leg-10.md').read_text())
            missing = [h for h in set(hits) if h not in d['candmap']]
            d10 = d['claim_hit'] and not missing
            main_ok = any('inspect_analysis_view' in json.dumps(f) and 'inspect_binary_layout' in json.dumps(f)
                          and JQ_SHA in json.dumps(f) for f in d['frames_v'])
            exa = [h for h in hits if h != d['claim']]
            exa_ok = all(any('"Tool analyze not found"' in c for _, c in blocks((REC / 'leg-10.md').read_text()))
                         for h in []) or True
            cls = 'RESULT' if (d10 and main_ok) else ('CLAIM-MISS' if not d10 else 'NO-CONTROL-EVIDENCE')
            if missing: why.append(f'referenced hashes not embedded: {len(missing)}')
            dig = 'ok' if d10 else 'MISS'; exok = 'Y' if d['exit'] == 0 else 'N'
        rows.append((n, cls, PRED[n], cls == PRED[n], dig, exok, '; '.join(why)))
    if names_parsed is not None:
        miss = [x for x in SIX if x in names_parsed]
        if miss: fails.append(f'L9 names present in parsed tools list: {miss}')
    score = sum(1 for (n, cls, pred, ok, _, _, _) in rows if ok)
    for (n, cls, pred, ok, dig, exok, why) in rows:
        if not ok: fails.append(f'L{n} class {cls or "absent"} != {pred}' + (f' ({why})' if why else ''))
        if dig == 'MISS': fails.append(f'L{n} digest verification failed')
        if exok == 'N': fails.append(f'L{n} exit code != 0')
    if score < 9: fails.append(f'score {score}/10 < gate 9')
    # controls: Command A + tokens vs census-pre
    a_ok = tok_ok = kf_ok = scorecard_ok = None
    cp = (REC / 'census-pre.txt')
    if cp.is_file():
        cpt = cp.read_text()
        m = re.search(r'^COMMAND_A_STDOUT=(\{.*\})$', cpt, re.M)
        base_a = json.loads(m.group(1)) if m else None
        m = re.search(r'^MAP_TOKEN_SHA256=([0-9a-f]{64})$', cpt, re.M); base_tsha = m.group(1) if m else None
        m = re.search(r'^MAP_TOKEN_COUNT=(\d+)$', cpt, re.M); base_tn = int(m.group(1)) if m else None
        m = re.search(r'^KNOWLEDGE_MD_COUNT=(\d+)$', cpt, re.M); base_kf = int(m.group(1)) if m else None
        sc = git('show', f'{PINNED}:SCORECARD.md').stdout
        fence = re.search(r'(?s)## Measurement recipes.*?' + TICKS + r'bash\n(.*?)\n' + TICKS, sc)
        recipe = fence.group(1).split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0] if fence else None
        ra = sh([sys.executable, '-', PINNED], input=recipe, cwd=ROOT) if recipe else None
        cur_a = json.loads(ra.stdout) if ra and ra.returncode == 0 else None
        okf = ('mapped', 'knowledge_files', 'missing', 'dangling',
               'citation_resolved_rules', 'rule_blocks', 'coverage_score', 'depth_score')
        a_ok = bool(cur_a and cur_a.get('revision') == PINNED
                    and all(cur_a.get(k) == EXPECT_A[k] for k in okf) and base_a == cur_a)
        readme = git('show', f'{PINNED}:corpus/README.md').stdout
        sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
        toks = sorted(set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', sec)))
        cur_tsha = sha(('\n'.join(toks) + '\n').encode())
        tok_ok = (cur_tsha == base_tsha and len(toks) == base_tn)
        kpaths = git('ls-tree', '-r', '--name-only', PINNED, '--', 'corpus/knowledge').stdout.split('\n')
        kf_ok = len([p for p in kpaths if p.endswith('.md')]) == base_kf
        sc_wt = (ROOT / 'SCORECARD.md').read_bytes()
        sc_blob = git('show', f'{PINNED}:SCORECARD.md').stdout.encode()
        scorecard_ok = sha(sc_wt) == sha(sc_blob)
        if not a_ok: fails.append('Command A drift vs census-pre/expected')
        if not tok_ok: fails.append('coverage-map token set drift vs census-pre')
        if not kf_ok: fails.append('knowledge file count drift vs census-pre')
        if not scorecard_ok: fails.append('worktree SCORECARD.md != pinned blob')
    else:
        fails.append('census-pre.txt missing: controls unverifiable')
    # provenance
    mf = REC / 'MANIFEST.txt'
    if mf.is_file():
        for ln in mf.read_text().split('\n'):
            m = re.match(r'(leg-\d+\.md) ([0-9a-f]{64})$', ln.strip())
            if not m: continue
            name, h = m.groups(); nm = int(re.search(r'\d+', name).group())
            cur = inv[nm]['file'] if inv[nm]['present'] else None
            if cur != h:
                prov.append(f'MANIFEST {name}: manifest {h[:12]} vs current {str(cur)[:12]}')
    else:
        warns.append('MANIFEST.txt missing')
    if cp.is_file():
        m = re.search(r'^RECEIPT_LEG_FILES=(.*)$', cp.read_text(), re.M)
        if m:
            for part in m.group(1).split(' | '):
                mm = re.match(r'(leg-\d+\.md): regular size=(\d+) sha256=([0-9a-f]{64})', part)
                if not mm: continue
                name, sz, h = mm.groups(); nm = int(re.search(r'\d+', name).group())
                cur = inv[nm]
                if cur['present'] and (cur['size'] != int(sz) or cur['file'] != h):
                    prov.append(f'census-pre {name}: {sz}/{h[:12]} vs current {cur["size"]}/{cur["file"][:12]}')
    cat = cp.read_text() if cp.is_file() else ''
    for name in [f'leg-{i}.md' for i in range(1, 11)]:
        if not re.search(re.escape(name) + r'[:\s]', cat):
            prov.append(f'census-pre record absent for {name}')
    for mm in re.finditer(r'^CONFIG (\S+): regular size=(\d+) sha256=([0-9a-f]{64})$', cat, re.M):
        p = Path(mm.group(1))
        cur = sha(p.read_bytes()) if p.is_file() else 'ABSENT'
        if cur != mm.group(3): prov.append(f'config(census-pre) {p.name}: {mm.group(3)[:12]} vs current {cur[:12]}')
    # config sentinels vs SE2.md record (hash on the label's own line)
    se2 = WAVE / 'SE2.md'
    if se2.is_file():
        t2 = se2.read_text()
        paths = [('Devin', Path.home() / '.config/devin/mcp_config.json'),
                 ('OMP', Path.home() / '.omp/agent/mcp.json'),
                 ('Kimi', Path.home() / '.kimi-code/config.toml'),
                 ('.bashrc', Path.home() / '.bashrc')]
        for label, p in paths:
            exp = None
            for ln in t2.split('\n'):
                mh = re.search(r'([0-9a-f]{64})', ln)
                if mh and label in ln: exp = mh.group(1); break
            cur = sha(p.read_bytes()) if p.is_file() else 'ABSENT'
            if exp is None: warns.append(f'SE2 sentinel for {label} unparsable')
            elif cur != exp: prov.append(f'config {label}: SE2 {exp[:12]} vs current {cur[:12]}')
    else:
        warns.append('SE2.md missing: config sentinels unavailable')
    # /tmp raw cross-checks (notes only; ephemeral)
    x3 = Path('/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout')
    if x3.is_file() and inv[3]['present']:
        h = sha(x3.read_bytes())
        tmpck.append(('leg-3 raw /tmp stdout == claim', h == inv[3]['claim'], h))
    x10a = Path('/tmp/kaidoku-luna-round-8-leg10.stdout')
    x10b = Path('/tmp/kaidoku-luna-round-8-leg10-summary.stdout')
    for lbl, p in (('leg-10 tools-session raw', x10a), ('leg-10 summary raw', x10b)):
        if p.is_file():
            h = sha(p.read_bytes())
            tmpck.append((lbl + ' referenced in leg-10.md', h in inv[10]['candmap'] or h in inv[10]['claims'], h))
    # report
    W = lines.append
    W(f'CB5 luna-round-8 FINAL CENSUS (design 2)  ROOT={ROOT} WAVE={WAVE}')
    W(f'PINNED_HEAD={PINNED} OBSERVED_HEAD={head} HEAD_MATCH={head_ok} TRACKED_DIRTY={len(dirty)}')
    W(f'COMMAND_A_OK={a_ok} TOKEN_SET_OK={tok_ok} KFILES_OK={kf_ok} SCORECARD_WT_EQ_PINNED={scorecard_ok}')
    if tok_ok is not None:
        W(f'MAP_TOKEN_COUNT={len(toks)} MAP_TOKEN_SHA256={cur_tsha}')
    W('LEG CLASS                  PRED                 MATCH DIGEST EXIT NOTE')
    for (n, cls, pred, ok, dig, exok, why) in rows:
        W(f'{n:>3} {str(cls):<22} {pred:<20} {"Y" if ok else "."}     {dig:<6} {exok:<4} {why}')
    W(f'SCORE {score}/10 (P0 gate >=9)')
    for n in range(1, 11):
        if inv[n]['present']: W(f'RECEIPT_SHA256 {n} {inv[n]["file"]}')
    for name, ok, h in tmpck:
        W(f'TMP_CROSSCHECK {name}: {"match" if ok else "NO-MATCH"} {h[:16]}')
    for p in prov: W('PROVENANCE FINDING ' + p)
    for w in warns: W('WARN ' + w)
    for f_ in fails: W('FAIL ' + f_)
    content_ok = not fails
    prov_ok = not prov
    verdict = 'PASS' if content_ok else 'FAIL'
    if STRICT and not prov_ok: verdict = 'FAIL'
    W(f'CENSUS RESULT: {verdict} (content={"PASS" if content_ok else "FAIL"}, provenance={"PASS" if prov_ok else "FINDINGS"}{", strict" if STRICT else ""})')
    j = {'head': head, 'head_ok': head_ok, 'command_a_ok': a_ok, 'tokens_ok': tok_ok,
         'classes': {str(n): cls for (n, cls, *_ ) in rows},
         'score': score, 'receipts_sha256': {str(n): inv[n].get('file') for n in range(1, 11)},
         'provenance': prov, 'warnings': warns, 'failures': fails, 'verdict': verdict}
    W('CENSUS_JSON ' + json.dumps(j, sort_keys=True))
    print('\n'.join(lines))
    return 0 if (content_ok and (not STRICT or prov_ok)) else 1

if __name__ == '__main__':
    sys.exit(main())
PY
```

## FINDINGS
- Live run exit 0, **SCORE 10/10**, stdout sha256 `5a9cd053b69366de0e1ee3074393d2b463501b99eeb1513f565fa94adc54c84d`: L1 `6.4.0`; L2 170 names order-identical to `leg-2-tools.txt`; L3–L8 `-32602` `Tool <name> not found` in digest-verified blocks; L9 6/6 absent (grep exit 1, empty stdout `e3b0c442…`); L10 jq `inspect_binary_layout` RESULT. Controls: HEAD match, tracked-clean; Command A 78/78–9/9–10.0, tokens 78/c6c025f3…, configs == sentinels.
- Known defect resolved: leg-3.md (1be7e4f9, 1448B) block+LF = 5c6820 = claim = /tmp raw; broken variant (`/tmp/zb3-broken-sim.md`, d641e3d3, 1430B, drops `prompts.listChanged`) reproduces census-pre's record and is caught (sim a2 → FAIL). Non-reproducing now.
- Provenance findings (4): `leg-10.md` current 6cd389e9 ≠ MANIFEST c89eea7a (later rewrite; internally coherent; /tmp raws 23e94d0b/61450b92 match); census-pre leg-3/leg-4 entries stale vs current (==MANIFEST, coherent); census-pre has no leg-10. `CB5_STRICT=1` → exit 1.
- Attack: control PASS; 12/12 mutants fail closed (11 content FAIL: byte tamper, historical leg-3 defect, swap, missing, exit, L9 insert, tools-order, re-hash, claim, duplicate, census-pre tamper; manifest = strict FAIL). leg-4's superseded bytes unattested.

## THREATS
Digest gates are existential and in-receipt: a fully coherent forgery passes (re-hash died only on its class lie). L3–L5 requests are prose-only. Mtimes were preserved during leg-3/4/10 edits; leg-4's superseded bytes unattested. Config sentinels lack a round-8 pre-L1 pair; /tmp cross-checks are ephemeral — the stdout sha pins this snapshot.

## VERDICT
FINDING: 10/10 predictions and all current receipt claims verify (content PASS, exit 0); leg-3 display defect repaired and non-reproducing; residual provenance discontinuities (leg-10 vs MANIFEST; leg-3/leg-4 vs census-pre) remain for parent adjudication — `CB5_STRICT=1` fails closed on them.
