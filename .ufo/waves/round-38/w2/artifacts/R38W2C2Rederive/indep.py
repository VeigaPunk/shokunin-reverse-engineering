#!/usr/bin/env python3
"""Independent rederivation of P38-C2 (does NOT import the frozen counter)."""
import json, re, subprocess, sys, collections

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'

def show(rev, path):
    p = subprocess.run(['git','-C',ROOT,'show',f'{rev}:{path}'],capture_output=True)
    return p.stdout.decode() if p.returncode==0 else None

def exists(rev, path):
    return subprocess.run(['git','-C',ROOT,'cat-file','-e',f'{rev}:{path}'],capture_output=True).returncode==0

def sect(text, heading):
    lines = text.splitlines()
    try: i = lines.index(heading)
    except ValueError: return []
    out=[]
    for l in lines[i+1:]:
        if l.startswith('## '): break
        out.append(l)
    return out

def table_rows(lines):
    rows=[]; started=False
    for l in lines:
        if l.lstrip().startswith('|'):
            started=True
            if re.match(r'^\s*\|[\s\-|:]+\|\s*$', l): continue
            rows.append(l)
        elif started: break
    return [r for r in rows if r.strip().strip('|').split('|')[0].strip() not in ('Axis','Capability','Surface')]

def units(rev):
    sc, sh, pv = show(rev,'SCORECARD.md'), show(rev,'SHONEN.md'), show(rev,'PROVINCE.md')
    u = collections.OrderedDict()
    for r in table_rows(sect(sc,'## Owned axes')):
        u['owned:'+r.strip().strip('|').split('|')[0].strip()] = [(r,'row')]
    for r in table_rows(sect(sc,'## Capabilities')):
        u['cap:'+r.strip().strip('|').split('|')[0].strip()] = [(r,'row')]
    for r in table_rows(sect(pv,'## Core')):
        u['core:'+r.strip().strip('|').split('|')[0].strip()] = [(r,'row')]
    # FRONTIER: the predicate says "rows"; the section is a bullet list -> each bullet is a row
    cur=None
    for l in sect(pv,'## Frontier'):
        if re.match(r'^- ', l):
            cur='frontier:'+l[2:60]
            u[cur]=[(l,'bullet')]
        elif cur and (l.startswith('  ') or l.strip()==''):
            if l.strip(): u[cur].append((l,'cont'))
        else:
            cur=None
    cur=None
    for l in sh.splitlines():
        m=re.match(r'^- \[[ x~]\] (.*)$', l)
        if m:
            cur='shonen:'+m.group(1).strip()
            u[cur]=[(l,'box')]
        elif cur and l.startswith('  '):
            u[cur].append((l,'cont'))
        else:
            cur=None
    return u

LANE = re.compile(r'^(corpus/|tools/|plans/|evidence/|scripts/|considerthese/|kaidoku-r26/|\.ufo/|SCORECARD\.md|SHONEN\.md|SKILL\.md|PROVINCE\.md|LOG\.md|README\.md|MINT\.md|AGENTS\.md)')
TOK = re.compile(r'`([^`\n]+)`')
PTR = re.compile(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$')

def ptrs(pieces):
    out=[]
    for text,_ in pieces:
        for tok in TOK.findall(text):
            tok=tok.strip()
            m=PTR.match(tok)
            if not m: continue
            p=m.group(1)
            if tok.startswith(('/', '~')): continue
            if not LANE.match(p): continue
            out.append((tok,p,m.group(2),m.group(3)))
    return out

cache={}
def nlines(rev,p):
    k=(rev,p)
    if k not in cache:
        t=show(rev,p); cache[k]=len(t.splitlines()) if t is not None else 0
    return cache[k]

def resolve(rev,tok,p,a,b):
    pp=p.rstrip('/')
    # a bare '.md' token at repo root that the pointer set accepts
    if not pp or not exists(rev,pp): return False
    if a is None:
        return True
    if b is not None and int(b)<int(a): return False
    hi=int(b or a); lo=int(a)
    return 1<=lo and hi<=nlines(rev,pp)

def scan(rev, label, U):
    total=0; bad=[]
    for k,pieces in U.items():
        for tok,p,a,b in ptrs(pieces):
            total+=1
            if not resolve(rev,tok,p,a,b): bad.append([k,tok])
    print(f'--- {label} rev={rev[:12]} units={len(U)} pointers={total} unresolved={len(bad)}')
    for k,t in bad: print('   UNRESOLVED',k,'::',t)
    return total,bad

UB = units('77091b492cc53f8743bd0701b1e7d5e66123dd84')
UR = units('0fc6113376a156fddc3ec385386d71c3a4a9f690')
tb,bb = scan('77091b492cc53f8743bd0701b1e7d5e66123dd84','BASE',UB)
tr,br = scan('0fc6113376a156fddc3ec385386d71c3a4a9f690','REV ',UR)
print('units dropped:', [k for k in UB if k not in UR])
print('pointers base->rev:', tb, '->', tr)
