#!/usr/bin/env python3
"""Control: does adding the C2 craft rule block move the depth axis recipe 17/17 -> 18/18, or regress it?"""
import re, subprocess, sys
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; REV=sys.argv[1] if len(sys.argv)>1 else 'a2f64e1da78afcf8cc39287106604dbcc270844c'
def show(p): return subprocess.run(['git','-C',LANE,'show',f'{REV}:{p}'],capture_output=True,text=True,check=True).stdout
skill=show('SKILL.md'); craft=skill.split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
NEW="""- **SquashFS extract-firmware outcomes are separated by typed envelope fields, not by counts (round 39 draft control).** Table rows key on chunk count, `extraction_failed`, gap `kind`, diagnostic `__typename__`, and the `-be` token in the retained extractor command; see unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py:39-54` and rea-agents 6.5.0 `dist/firmware/FirmwarePublication.js:276-308`.
"""
pat=re.compile(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?')
def score(c):
    rules=re.split(r'(?m)^- \*\*',c)[1:]; resolved=0; bad=[]
    for i,r in enumerate(rules,1):
        refs=pat.findall(r); valid=bool(refs)
        for name,first,last in refs:
            try:
                n=len(show('corpus/knowledge/'+name).splitlines()); s,e=int(first or 1),int(last or first or 1)
                valid = valid and 1<=s<=e<=n
            except subprocess.CalledProcessError: valid=False
        resolved+=valid
        if not valid: bad.append(i)
    return dict(rule_blocks=len(rules),resolved=resolved,depth_score=round(10*resolved/len(rules),2),unresolved=bad)
print('base craft                        ', score(craft))
print('base + 18th block, external cites ', score(craft.rstrip('\n')+'\n'+NEW+'\n'))
print('base + 18th block, + knowledge cite', score(craft.rstrip('\n')+'\n'+NEW.rstrip('\n')+' Rows: `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:1-20`.\n'))
