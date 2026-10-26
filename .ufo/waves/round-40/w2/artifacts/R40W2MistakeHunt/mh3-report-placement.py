#!/usr/bin/env python3
"""MH-3 — a wave-1 report can be committed twice, and a retry seat's report can land
inside the artifacts tree under a seat id no registry member carries: two live
authorities for one seat, and one seat whose only report is a copy.

Round-40 bytes (`7fce3086`, one commit adds all of it):
  w1/R40SrcAvmVendor.md            == artifacts/R40SrcAvmVendor.md          (4214 B, identical)
  w1/R40SrcReaOps.md               == artifacts/R40SrcReaOps.md             (13359 B, identical)
  w1/R40ConnSibling.md             == artifacts/R40ConnSibling-2/R40ConnSibling.md
                                     (15535 B, identical; the w1 copy's own
                                      header says `Seat: R40ConnSibling-2`)
The wave-1 sentinel flagged the two top-level copies (`w1/R40Sentinel.md` §2.5) and
not the nested one.

Usage: mh3-report-placement.py --wave W1DIR [--registry swarm-registry.json]
       [--fixture-move DIR] [--json]
Exit 0 = clean; 1 = findings; 2 = usage error.
Green fixture: `--fixture-move` copies W1DIR to DIR with hard links, deletes the
duplicates (the nested copy is kept as w1/R40ConnSibling-2.md) and re-runs the checks
there, so the same code path is red on the lane bytes and green on a repaired tree.
"""
import argparse
import json
import os
import re
import shutil
import sys

SEAT_ID = re.compile(r'^#\s*(R40[-A-Za-z0-9]+)\b')
SEAT_DECL = re.compile(r'Seat:\s*`?(R40[-A-Za-z0-9]+)`?')


def registry_members(path):
    if not path or not os.path.exists(path):
        return set()
    data = json.load(open(path))
    return set((data.get('members') or {}).keys())


def read(path):
    with open(path, 'rb') as fh:
        return fh.read()


def check(wave):
    findings = []
    reg = registry_members(os.path.join(wave, 'swarm-registry.json'))
    reports = {}
    for name in sorted(os.listdir(wave)):
        if name.endswith('.md'):
            reports[name[:-3]] = read(os.path.join(wave, name))
    for seat in sorted(reg):
        if seat not in reports:
            findings.append(('missing-report', seat, 'registry member has no w1/%s.md' % seat))
    for seat, blob in sorted(reports.items()):
        head = blob.decode('utf-8', 'replace')[:4000]
        declared = SEAT_DECL.search(head)
        if declared and declared.group(1) != seat:
            findings.append(('seat-identity', seat,
                             'w1/%s.md declares Seat: %s' % (seat, declared.group(1))))
    arts = os.path.join(wave, 'artifacts')
    if os.path.isdir(arts):
        by_bytes = {}
        for seat, blob in reports.items():
            by_bytes.setdefault(blob, []).append('w1/%s.md' % seat)
        for dirpath, _dirnames, filenames in os.walk(arts):
            for name in sorted(filenames):
                if not name.endswith('.md'):
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, wave)
                blob = read(path)
                if os.path.dirname(rel) == 'artifacts':
                    findings.append(('report-at-artifacts-root', rel,
                                     'a report-shaped md sits at the artifacts root'))
                if blob in by_bytes:
                    findings.append(('duplicate-report', rel,
                                     'byte-identical to %s' % by_bytes[blob]))
                    continue
                first = blob.decode('utf-8', 'replace').splitlines()[:1]
                if first and SEAT_ID.match(first[0]) and SEAT_DECL.search(
                        blob.decode('utf-8', 'replace')[:4000]):
                    findings.append(('report-in-artifacts', rel,
                                     'a seat report is filed under artifacts/'))
    return findings


def build_fixture(wave, dest):
    """Copy only what the gate reads (top-level md, the registry, artifacts/**/*.md),
    so a cross-device scratch dir works and nothing large is duplicated."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for name in sorted(os.listdir(wave)):
        src = os.path.join(wave, name)
        if os.path.isfile(src) and (name.endswith('.md') or name == 'swarm-registry.json'):
            shutil.copy2(src, os.path.join(dest, name))
    arts = os.path.join(wave, 'artifacts')
    if os.path.isdir(arts):
        for dirpath, _dirnames, filenames in os.walk(arts):
            for name in filenames:
                if not name.endswith('.md'):
                    continue
                src = os.path.join(dirpath, name)
                dst = os.path.join(dest, os.path.relpath(src, wave))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    for rel in ('artifacts/R40SrcAvmVendor.md', 'artifacts/R40SrcReaOps.md'):
        p = os.path.join(dest, rel)
        if os.path.exists(p):
            os.unlink(p)
    nested = os.path.join(dest, 'artifacts/R40ConnSibling-2/R40ConnSibling.md')
    if os.path.exists(nested):
        os.replace(nested, os.path.join(dest, 'R40ConnSibling-2.md'))
    # the registered seat's own report gets its own id back, and the retry seat
    # becomes a registry member in its own right
    main_report = os.path.join(dest, 'R40ConnSibling.md')
    if os.path.exists(main_report):
        text = read(main_report).decode('utf-8', 'replace')
        text = text.replace('Seat: `R40ConnSibling-2`', 'Seat: `R40ConnSibling`', 1)
        with open(main_report, 'w', encoding='utf-8') as fh:
            fh.write(text)
    reg_path = os.path.join(dest, 'swarm-registry.json')
    if os.path.exists(reg_path):
        reg = json.loads(read(reg_path))
        members = reg.get('members') or {}
        if 'R40ConnSibling' in members:
            retry = dict(members['R40ConnSibling'])
            retry['kind'] = 'respawn'
            members['R40ConnSibling-2'] = retry
            with open(reg_path, 'w', encoding='utf-8') as fh:
                json.dump(reg, fh, indent=1)
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--wave', required=True)
    ap.add_argument('--fixture-move', default=None)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    if not os.path.isdir(args.wave):
        print('no such wave dir %s' % args.wave)
        return 2
    target = args.fixture_move and build_fixture(args.wave, args.fixture_move) or args.wave
    findings = check(target)
    if args.json:
        print(json.dumps({'dir': target, 'findings': findings}, indent=1))
    else:
        for kind, where, why in findings:
            print('%-26s %-42s %s' % (kind, where, why))
        print('dir=%s findings=%d' % (target, len(findings)))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
