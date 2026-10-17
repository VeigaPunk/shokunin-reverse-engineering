# XB1 — census canonical (lane B, luna-round-7)

## CLAIM

The runnable canonical census text below consolidates N1's post-integration gate, C4's content checks, and round-6 CB7's wrong-version hunt into one read-only command. Verified: pre-state fails closed (six entries absent); a simulated post-state exits 0 with Command A `{"knowledge_files": 78, "mapped": 78, "missing": [], "dangling": [], "citation_resolved_rules": 9, "coverage_score": 10.0}`; four adversarial mutations each exit 1.

## METHOD

- Recomputed N2's baseline pins at `411175e`: 72 map tokens, digest `c538284b...` (`'\n'.join(sorted(set(tokens)))+'\n'`); 72-file aggregate `3adf3bc2...`. Command A extracted verbatim from the SCORECARD blob and run: 72/72, 9/9.
- Receipt pins: all 12 leg-3...8 receipts are tracked at HEAD, so the census reads them as Git objects at REV; every `rea-agents@<ver>` token is `6.5.0` (bare prose mentions in B leg-4/5/8 reported, not gated — CB7's adjudication).
- Pre-state from repo root: exit 1, `CENSUS RESULT: FAIL`, `command A knowledge_files=72 != 78`, six `absent`.
- Post-state rehearsal `/tmp/xb1/sim` (clone + six entries composed from Z1/G2/G4/G5/E6D with the metadata trio added + README rows, commit `c4edcf3`): exit 0, PASS.
- Sim mutations, committed then reverted: promotion line -> FAIL; underscore stem -> FAIL; prior-entry byte change -> FAIL; receipt pin `6.4.0` -> FAIL.

## FINDINGS

- Verified gate mechanics: hyphenated stems (ruling a), prior-72 byte identity vs `411175e`, prior-token digest, 1x occurrence per new stem in both README tables, per-entry markers (metadata trio, pin, labels, path+sha256 line, leg-A/leg-B citations), non-negated promotion language, receipt pins.
- The gate caught a real omission in my first sim draft: entry 4 lacked its leg-6 A citation (G4 keeps A as the excluded comparator) — required, since ruling (b) excludes A's result, not its receipt record.
- `SCn` citation and Evidence ID are warn-only (QUALITY criterion 6 admits the exact reproducing call); semantic QUALITY judgment stays with the parent.

## THREATS

- The sim's entries are XB1 rehearsals, not the parent's integrated texts; real post-integration PASS remains a projection.
- Census reads Git objects: commit first or pass `REV=<commit>`. Command A extraction depends on SCORECARD's `**A — source-derived controls.**` marker + first bash fence; if moved it fails closed.
- The pin stage gates versioned `rea-agents@` tokens only; unpinned `npx rea-agents` would surface as `bare`, not FAIL.

## VERDICT

CLEAN — runnable canonical census text delivered and verified pre/post-state; four mutations fail closed.

## CANONICAL CENSUS TEXT (runnable, read-only; exit 0 = PASS)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -B - "${REV:-HEAD}" <<'PY'
#!/usr/bin/env python3
"""luna-round-7 XB1 canonical census — coverage gate for the six l7 entries.

Run from the kaidoku-shokunin repo root:
    python3 -B - <<'PY'   ...   PY        (this file's body, fenced in XB1.md)
Read-only: Git objects (REV vs the pinned pre-state BASELINE) plus the cited
round-6 receipt files on disk; no network, MCP, or repo writes. Exit 0 = PASS.

Consolidates three round designs (cited, not copied):
- N1.md (lane A round-7 gate design): Command A fields, six exact stems,
  prior-72 byte identity, one Coverage-map + one Knowledge-table occurrence.
- C4.md: entry-body checks Command A cannot make (kept mechanical only).
- round-6 CB7.md (wrong-version hunter): every versioned `rea-agents@<ver>`
  token in the round-6 receipts the six entries cite must be exactly 6.5.0.
Run: commit the integration first, or pass REV=<commit>.
"""
import hashlib, json, os, re, subprocess, sys

BASELINE = '411175e337c0725ae9bee3fd478ae9bf05bedf3f'   # N2 pre-state (72/72; SCORECARD Command A)
TOKEN_DIGEST_72 = 'c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0'   # N2 / round-5 P0
KNOWLEDGE_72_DIGEST = '3adf3bc2f0e59646cf8d77dc9d06646d7690e24168b89f9b4607cdfdad75adbf'  # N2
NEW = [  # (stem per ruling (a) hyphenated, lane A leg, lane B leg, scout)
    ('2026-10-16-l7-01-inspect-go-binary', 3, 1),
    ('2026-10-16-l7-02-inspect-rust-binary', 4, 2),
    ('2026-10-16-l7-03-inspect-electron-fuses', 5, 3),
    ('2026-10-16-l7-04-inspect-sqlite-database', 6, 4),
    ('2026-10-16-l7-05-search-bytes', 7, 5),
    ('2026-10-16-l7-06-inspect-with-objdump', 8, 6),
]
TOKEN_RE = r'2026-10-\d{2}-[a-z0-9-]+'
RECEIPT_DIR = '.ufo/waves/luna-round-6'

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def show(rev, path):
    r = run(['git', 'show', f'{rev}:{path}'])
    if r.returncode != 0:
        raise RuntimeError(f'git show {rev}:{path}: {r.stderr.strip()}')
    return r.stdout

def try_show(rev, path):
    r = run(['git', 'show', f'{rev}:{path}'])
    return r.stdout if r.returncode == 0 else None

def stems_at(rev):
    out = run(['git', 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'])
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return {os.path.basename(p)[:-3] for p in out.stdout.splitlines() if p.endswith('.md')}

def map_section(readme):
    return readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]

def know_section(readme):
    if '\n## Knowledge\n' not in readme:
        return ''
    return readme.split('\n## Knowledge\n', 1)[1].split('\n## ', 1)[0]

def token_digest(tokens):
    return hashlib.sha256(('\n'.join(sorted(set(tokens))) + '\n').encode()).hexdigest()

def blob_hex(rev, path):
    return hashlib.sha256(show(rev, path).encode()).hexdigest()

def agg_digest(rev, stems):
    recs = [f'{s} {blob_hex(rev, "corpus/knowledge/" + s + ".md")}\n' for s in sorted(stems)]
    return hashlib.sha256(''.join(recs).encode()).hexdigest()

def command_a(rev):
    """Extract recipe A from the REV SCORECARD blob and run it verbatim."""
    sc = show(rev, 'SCORECARD.md')
    i = sc.index('**A — source-derived controls.**')
    m = re.search(r'```bash\n(.*?)\n```', sc[i:], re.S)
    body = m.group(1)
    r = run(['bash', '-c', body], env=dict(os.environ, REV=rev))
    if r.returncode != 0:
        return None, f'command A exit {r.returncode}: {r.stderr.strip()[:200]}'
    return json.loads(r.stdout.strip().splitlines()[-1]), None

def entry_checks(rev, stem, leg, scout):
    fails, warns = [], []
    path = f'corpus/knowledge/{stem}.md'
    body = show(rev, path)
    if len(body.encode()) < 400:
        fails.append(f'size<400B ({len(body.encode())}B)')
    for marker in ('source:', 'verified-at:', 'recheck:'):
        if marker not in body:
            fails.append(f'missing {marker}')
    if 'rea-agents@6.5.0' not in body:
        fails.append('missing pin rea-agents@6.5.0')
    if re.search(r'rea-agents@(?!6\.5\.0)\d', body):
        fails.append('non-6.5.0 rea-agents pin present')
    absent = [l for l in ('observation', 'inference', 'unknown') if l not in body.lower()]
    if absent:
        fails.append('missing labels: ' + ','.join(absent))
    if not any(re.search(r'/[A-Za-z0-9._@+/-]{3,}', l) and re.search(r'[0-9a-f]{64}', l)
               for l in body.splitlines()):
        fails.append('no line with absolute path + 64-hex sha256')
    for lane, tag in (('receipts', 'A'), ('receipts-B', 'B')):
        pat = rf'(?:\.ufo/waves/luna-round-6/)?{lane}/leg-{leg}\.md'
        if not re.search(pat, body):
            fails.append(f'missing leg-{leg} {tag} citation')
    if not re.search(rf'SC{scout}\.md', body):
        warns.append(f'no SC{scout} citation')
    if not re.search(r'ev_[0-9a-f]{8,64}', body):
        warns.append('no Evidence ID (ev_...)')
    neg = re.compile(r'not|never|no |without|deny|denies|excluded|outside|beyond', re.I)
    bad = [l.strip()[:80] for l in body.splitlines()
           if (re.search(r'promot', l, re.I) or re.search(r'\bCore\b', l)) and not neg.search(l)]
    if bad:
        fails.append('non-negated promotion/Core language: ' + ' | '.join(bad))
    return fails, warns

def pins(rev):
    rep, missing, disk = {}, [], []
    for num in range(3, 9):
        for lane in ('receipts', 'receipts-B'):
            rel = f'{RECEIPT_DIR}/{lane}/leg-{num}.md'
            text = try_show(rev, rel)
            if text is None:
                if os.path.exists(rel):
                    text = open(rel, encoding='utf-8', errors='replace').read()
                    disk.append(rel)
                else:
                    missing.append(rel)
                    continue
            vers = re.findall(r'rea-agents@([0-9A-Za-z._-]+)', text)
            rep[f'{lane}/leg-{num}'] = {
                'versioned': len(vers),
                'bad': sorted({v for v in vers if v != '6.5.0'}),
                'bare': len(re.findall(r'rea-agents(?!@)', text)),
            }
    return rep, missing, disk

def main():
    if not os.path.isdir('.git'):
        print('FAIL: run from the kaidoku-shokunin repo root'); return 1
    rev = run(['git', 'rev-parse',
               sys.argv[1] if len(sys.argv) > 1 else os.environ.get('REV', 'HEAD')]).stdout.strip()
    fails, warns, out = [], [], {}
    ca, ca_err = command_a(rev)
    if ca_err:
        fails.append(ca_err)
        out['command_a'] = None
    else:
        out['command_a'] = ca
        want = {'knowledge_files': 78, 'mapped': 78, 'missing': [], 'dangling': [],
                'citation_resolved_rules': 9, 'rule_blocks': 9,
                'coverage_score': 10.0, 'depth_score': 10.0}
        for k, v in want.items():
            if ca.get(k) != v:
                fails.append(f'command A {k}={ca.get(k)!r} != {v!r}')

    pre_stems, pre_readme = stems_at(BASELINE), show(BASELINE, 'corpus/README.md')
    pre_tokens = re.findall(TOKEN_RE, map_section(pre_readme))
    if token_digest(pre_tokens) != TOKEN_DIGEST_72 or len(pre_tokens) != 72:
        fails.append('baseline token census drifted from N2 pin')
    if agg_digest(BASELINE, pre_stems) != KNOWLEDGE_72_DIGEST or len(pre_stems) != 72:
        fails.append('baseline knowledge census drifted from N2 pin')

    stems, readme = stems_at(rev), show(rev, 'corpus/README.md')
    new_stems = {n for n, _, _ in NEW}
    prior = stems - new_stems
    out['revision'], out['baseline'] = rev, BASELINE
    out['knowledge_count'] = len(stems)
    diff = [s for s in sorted(prior & pre_stems) if blob_hex(rev, f'corpus/knowledge/{s}.md')
            != blob_hex(BASELINE, f'corpus/knowledge/{s}.md')]
    out['prior_stems_missing'] = sorted(pre_stems - stems)
    out['prior_files_changed'] = diff
    if len(stems) != 78 or stems != pre_stems | new_stems:
        fails.append(f'knowledge stems: {len(stems)} (want 78, pre72+6 exactly)')
    if diff or (prior != pre_stems):
        fails.append('prior-72 entries not byte-identical to baseline')
    if agg_digest(rev, prior) != KNOWLEDGE_72_DIGEST:
        fails.append('prior-72 aggregate digest != N2 pin')

    toks = re.findall(TOKEN_RE, map_section(readme))
    uniq = set(toks)
    occ = {t: toks.count(t) for t in sorted(set(toks) | new_stems)}
    out['token_count'], out['token_unique'] = len(toks), len(uniq)
    out['token_digest_full'] = token_digest(toks)
    out['token_digest_prior72'] = token_digest(uniq & pre_stems)
    if len(toks) != 78 or len(uniq) != 78 or uniq != pre_stems | new_stems:
        fails.append(f'coverage-map tokens: {len(toks)} occ / {len(uniq)} unique (want 78/78 = pre72+6)')
    if out['token_digest_prior72'] != TOKEN_DIGEST_72:
        fails.append('prior-72 map-token digest != N2 pin')
    bad_occ = {t: occ[t] for t in new_stems if occ.get(t, 0) != 1}
    if bad_occ:
        fails.append(f'new tokens not 1x in Coverage map: {bad_occ}')

    know = re.findall(TOKEN_RE, know_section(readme))
    kocc = {t: know.count(t) for t in new_stems}
    mis_kt = {t: kocc[t] for t in new_stems if kocc[t] != 1}
    if mis_kt:
        fails.append(f'new stems not 1x in Knowledge table: {mis_kt}')

    out['entries'] = {}
    for stem, leg, scout in NEW:
        if stem not in stems:
            out['entries'][stem] = {'content_failures': ['file absent']}
            fails.append(f'{stem}: absent')
            continue
        f, w = entry_checks(rev, stem, leg, scout)
        out['entries'][stem] = {'content_failures': f, 'warnings': w}
        fails += [f'{stem}: {x}' for x in f]
        warns += [f'{stem}: {x}' for x in w]

    rep, missing, disk = pins(rev)
    out['pins'] = rep
    out['pin_files_missing'] = missing
    out['pin_read_via_worktree'] = disk
    pin_bad = {k: v['bad'] for k, v in rep.items() if v['bad']}
    out['pin_bad'] = pin_bad
    if pin_bad:
        fails.append(f'receipts with non-6.5.0 rea-agents pin: {pin_bad}')
    if missing:
        warns.append(f'receipts not at REV and not on disk (pin check skipped): {missing}')
    if disk:
        warns.append(f'receipts read from worktree, not REV objects: {disk}')

    out['failures'], out['warnings'] = fails, warns
    out['verdict'] = 'PASS' if not fails else 'FAIL'
    print(f'BASELINE {BASELINE} pre-stems={len(pre_stems)} pre-tokens={len(pre_tokens)}')
    print(f'REVISION {rev} knowledge_files={len(stems)} map_tokens={len(toks)}')
    if ca:
        print('COMMAND_A ' + json.dumps(ca, sort_keys=True))
    for stem, f, w in [(s, out['entries'][s].get('content_failures'), out['entries'][s].get('warnings'))
                       for s, _, _ in NEW]:
        print(f'ENTRY {stem}: ' + ('OK' if not f else 'FAIL ' + '; '.join(f)))
    pinsum = ', '.join(f'{k}={v["versioned"]}x6.5.0' + (f' BAD{v["bad"]}' if v['bad'] else '')
                       for k, v in rep.items())
    print('PINS ' + (pinsum or 'none'))
    print(f'CENSUS RESULT: {out["verdict"]}')
    print('CENSUS_JSON ' + json.dumps(out, sort_keys=True))
    return 0 if out['verdict'] == 'PASS' else 1

try:
    sys.exit(main())
except Exception as exc:  # fail closed, never traceback-only
    print(f'CENSUS RESULT: FAIL (runner error: {exc})')
    sys.exit(1)
PY
```
