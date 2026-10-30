import json, os, hashlib, datetime, subprocess
S=os.path.dirname(os.path.abspath(__file__))
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
out={'probe':'CritRetry probe4: is the g7581 ENOENT a REPRODUCIBLE-TOCTOU on a symlink REA itself rewrites?',
     'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}

# 1. WHO produced the message? Node readlink error text vs Python os.readlink error text.
node = subprocess.run(['node','-e','const {readlink}=require("fs/promises");readlink("/nope-xyz").catch(e=>console.log(e.message));'],capture_output=True,text=True)
py = subprocess.run(['python3','-c','import os\ntry: os.readlink("/nope-xyz")\nexcept OSError as e: print(e)'],capture_output=True,text=True)
out['error_text_provenance']={
  'node_readlink_message': node.stdout.strip(),
  'python_readlink_message': py.stdout.strip(),
  'committed_receipt_reason': "ENOENT: no such file or directory, readlink '/fast/scratch/.../luacgi'",
  'CONCLUSION': 'the committed reason is the NODE (JS) form, i.e. raised by REA/unblob-JS readlink, NOT python unblob os.readlink'}

# 2. Which readlink call sites exist in REA 6.5.0 that could touch an EXTRACTION-TREE path?
rea='/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
sites=[]
for rel in ('dist/firmware/FirmwareFiles.js','dist/cli-runtime/cli.js','dist/process/capture/FilesystemSnapshot.js'):
    p=os.path.join(rea,rel)
    if not os.path.exists(p): continue
    for i,line in enumerate(open(p,encoding='utf-8',errors='replace'),1):
        if 'readlink(' in line and ('await readlink' in line or '= await readlink' in line):
            sites.append({'file':rel,'line':i,'code':line.strip()[:160]})
out['rea_readlink_sites']=sites

# 3. The critical asymmetry: unblob's fix_symlink does path.unlink() then path.symlink_to() -- a WINDOW
#    in which the path DOES NOT EXIST. REA's FirmwareFiles.js:184 does readlink(path) unguarded.
unblob=os.path.join(os.path.expanduser('~'),'.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/extractor.py')
src=open(unblob,encoding='utf-8').read().splitlines()
seg=[(i+1,l) for i,l in enumerate(src) if 84 <= i+1 <= 95]
out['unblob_fix_symlink_window']={'lines':[{'line':i,'text':l.rstrip()} for i,l in seg],
  'NOTE':'path.unlink() at 89 then path.symlink_to(relative_target) at 91 -> between them the path is ABSENT'}

# 4. Does the committed g7581 receipt show the REWRITTEN (relative) link_target for the very path that ENOENT'd?
rec=json.load(open(os.path.join(LANE,'corpus/evidence/round-50/c1/g7581/after.json')))
nr=rec.get('normalized_result') or {}
tgt='usr/www.myfritz/avme/cgi-bin/luacgi'
hits=[u for u in (nr.get('unpublished_entries') or []) if tgt in (u.get('relative_path') or '')]
out['committed_receipt_the_enoent_path']={
  'path':tgt,
  'present_in_unpublished_entries':len(hits),
  'entry':hits[0] if hits else None,
  'NOTE':'the committed g7581 receipt CONTAINS this symlink with a RELATIVE link_target (../../../www/cgi-bin/luacgi) -> unblob rewrote it; the oracle says the raw target is /usr/www/cgi-bin/luacgi (absolute)'}

# 5. oracle says the raw target is ABSOLUTE
orow=[l.rstrip('\n') for l in open(os.path.join(LANE,'tools/round-50/oracle/g7581.nonregular.tsv'),encoding='utf-8') if l.startswith(tgt+'\t')]
out['oracle_row']=orow
print(json.dumps(out,indent=1,sort_keys=True))
