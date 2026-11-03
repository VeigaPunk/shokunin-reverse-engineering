#!/usr/bin/env python3
"""Write bounded independent shortcut reader controls, no fixture execution; exit0 success.
Controlled source variants of reviewed reader plus inert replay/no-op controls.
"""
import pathlib,sys,json
reader=pathlib.Path(sys.argv[1]); dest=pathlib.Path(sys.argv[2]); dest.mkdir(parents=True,exist_ok=True)
src=reader.read_text()
variants={
 'collapse_by_name':("return dict(identity, finding='inventory_complete', occurrences=records,","return dict(identity, finding='inventory_complete', occurrences=list({r['filename']:r for r in records}.values()),"),
 'local_order':("return dict(identity, finding='inventory_complete', occurrences=records,","return dict(identity, finding='inventory_complete', occurrences=sorted(records,key=lambda r:r['header_offset']),"),
 'name_lookup':("with z.open(info, 'r') as member:","with z.open(info.filename, 'r') as member:")}
for name,(old,new) in variants.items():
    assert src.count(old)==1,(name,'replacement not unique')
    (dest/(name+'.py')).write_text(src.replace(old,new))
(dest/'noop.py').write_text('pass\n')
(dest/'allfalse.py').write_text("print('{}')\n")
# Memorizes dev output by basename; challenge uses fresh payload/name/size vocabulary.
expected=json.loads(pathlib.Path(sys.argv[3]).read_text())
replay="import pathlib,json,sys,hashlib\ntable="+repr(expected)+"\nr=table[pathlib.Path(sys.argv[-1]).stem].copy()\nr.update(schema=1,python=sys.version.split()[0],reader_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())\nif r['exit']!=0:\n r={k:v for k,v in r.items() if k not in ('archive_sha256','archive_size')}\nprint(json.dumps(r))\nsys.exit(r['exit'])\n"
(dest/'identity_replay.py').write_text(replay)
