#!/usr/bin/env python3
"""Sandbox simulation: does a candidate rule block 20 keep command A green?
usage: sim-block20.py <sandbox lane clone> ; clone must be a --shared clone of the lane at 49096c7e.
Never touches the real lane; commits only inside the clone (fixture identity)."""
import json, subprocess, sys, re, pathlib
LANE = pathlib.Path(sys.argv[1])
assert subprocess.check_output(['git','-C',str(LANE),'rev-parse','--show-toplevel'],text=True).strip()==str(LANE)
G=['git','-c','user.name=fx','-c','user.email=fx@fx','-C',str(LANE)]
def git(*a): return subprocess.check_output(G+list(a),text=True)
BASE=git('rev-parse','HEAD').strip()
CMD=pathlib.Path(__file__).with_name('command-A-verbose.py')
def cmdA(rev):
    out=subprocess.check_output([sys.executable,str(CMD),rev],cwd=LANE,text=True)
    return json.loads(out)
STEM='2026-10-26-r41-sqfs-triage-v3'
ENTRY=LANE/'corpus/knowledge'/(STEM+'.md')
def reset():
    git('reset','-q','--hard',BASE)
def block(cites, extra=''):
    return ('- **SquashFS `extract-firmware` outcome triage v3 (round 41).** Table v3 labels combined gap sets\n'
            +''.join(f'  (`corpus/knowledge/{n}.md{c}`)\n' for n,c in cites)
            +extra+'\n  <!-- sqfs-triage-table v3 -->\n  | label |\n  | --- |\n  | x |\n')
def insert_block(blk, after_line=375):
    lines=(LANE/'SKILL.md').read_text().split('\n')
    new=lines[:after_line]+['']+blk.rstrip('\n').split('\n')+lines[after_line:]
    (LANE/'SKILL.md').write_text('\n'.join(new))
def readme_row(stem):
    p=LANE/'corpus/README.md'; t=p.read_text().split('\n')
    i=[k for k,l in enumerate(t) if l.startswith('| Genuine AVM-layout big-endian')][0]
    t.insert(i+1,f'| T | `{stem}` | held |')
    p.write_text('\n'.join(t))
def entry(n=60):
    ENTRY.write_text('\n'.join(f'line {i}' for i in range(1,n+1))+'\n')
def commit(): git('add','-A'); git('commit','-q','--allow-empty','-m','fx'); return git('rev-parse','HEAD').strip()
res={}
def run(name, setup):
    reset(); setup(); rev=commit(); r=cmdA(rev)
    res[name]={k:r[k] for k in ('knowledge_files','mapped','missing','dangling','rule_blocks','citation_resolved_rules','bad_rules','coverage_score','depth_score')}
def ok():
    entry(60); insert_block(block([(STEM,':11-18'),(STEM,':19-26')])); readme_row(STEM)
run('P0_baseline', lambda: None)
run('P1_good_block20_and_readme', ok)
def no_readme(): entry(60); insert_block(block([(STEM,':11-18')]))
run('N1_entry_not_in_coverage_map', no_readme)
def beyond(): entry(30); insert_block(block([(STEM,':11-40')])); readme_row(STEM)
run('N2_range_past_end_of_entry', beyond)
def reversed_r(): entry(60); insert_block(block([(STEM,':26-19')])); readme_row(STEM)
run('N3_reversed_range', reversed_r)
def uncommitted_entry():  # entry file absent from the commit
    insert_block(block([(STEM,':11-18')])); readme_row(STEM)
run('N4_entry_file_missing_at_rev', uncommitted_entry)
def nocite(): entry(60); insert_block(block([])); readme_row(STEM)
run('N5_block_without_citation', nocite)
def split_by_bullet(): entry(60); insert_block(block([(STEM,':11-18')], extra='- **a second col-0 bold bullet** with no citation\n')); readme_row(STEM)
run('N6_second_col0_bullet_splits_block', split_by_bullet)
def h2(): entry(60); insert_block(block([(STEM,':11-18')], extra='\n## Not a heading please\n')); readme_row(STEM)
run('N7_h2_inside_block_truncates_craft', h2)
def wrapped(): entry(60); insert_block(block([], extra='  (`corpus/knowledge/\n  '+STEM+'.md:11-18`)\n')); readme_row(STEM)
run('N8_citation_wrapped_across_newline', wrapped)
def uppercase(): entry(60); insert_block(block([('2026-10-26-R41_sqfs','.md:11')])) if False else insert_block('- **x** `corpus/knowledge/'+STEM.upper()+'.md:11-18`\n'); readme_row(STEM)
run('N9_uppercase_name_in_citation', uppercase)
def dangling_map():
    entry(60); insert_block(block([(STEM,':11-18')])); readme_row(STEM); readme_row('2026-10-26-r41-avm-be-squashfs-core')
run('N10_readme_maps_stem_with_no_file', dangling_map)
def shortcite(): entry(60); insert_block('- **x** table cell style `knowledge '+STEM+'.md :11-18` only\n'); readme_row(STEM)
run('N11_table_style_citation_not_counted', shortcite)
def cite_other(): entry(60); insert_block('- **x** cites only `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:11-18`\n'); readme_row(STEM)
run('P2_block_citing_only_existing_entry_ok', cite_other)
reset()
print(json.dumps(res,indent=1,sort_keys=True))
