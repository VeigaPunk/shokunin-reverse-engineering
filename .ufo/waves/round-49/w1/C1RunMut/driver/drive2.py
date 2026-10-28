#!/usr/bin/env python3
# Confound-free follow-ups: output_directory strings the runner would emit with another segment,
# a nested /kaidoku-r44/…/kaidoku-r49/ string, and a freshness control (freeze := receipt commit).
import sys
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/C1RunMut/mut')
sys.argv = ['drive2']
import drive as D
import json as _json
D.RESULTS.extend(_json.load(open(D.S + '/results.json')))

S = D.S
D.CLONE_XPIN[0] = S + '/clone0/tools/round-27/xpin-attribute.mjs'


def outdir_remint(value_fn):
    def f(d):
        D.after_set_outdir(d, value_fn, True)
    return f


cases = [
    ('P14_outdir_kaidoku_r44_only_remint',
     outdir_remint(lambda cid: '/fast/scratch/hyaku/kaidoku-r44/probe-R49C1Run/c1-run.' + cid + '/rea-out')),
    ('P15_outdir_r49_segment_under_r44_remint',
     outdir_remint(lambda cid: '/fast/scratch/hyaku/kaidoku-r44/kaidoku-r49/probe-R49C1Run/' + cid + '/rea-out')),
]
for name, fn in cases:
    srcs = D.fresh(name)
    for k in D.IDS:
        fn(srcs[k])
    D.scenario(name, srcs)

# freshness control: the receipts' own commit is passed as --freeze; first add == freeze must fail
name = 'CTRL_receipt_commit_as_freeze'
dest, freeze = D.mkclone(name)
srcs = {k: f'{D.BASE_EV}/{k}' for k in D.IDS}
rev = D.stage(dest, name, srcs)
rec = D.score(dest, rev, name)
rec['freeze'] = rev
rec['receipt_commit'] = rev
rec['note'] = 'freeze argument set to the receipts commit itself (expect receipt_fresh false)'
D.record(rec)
D.log('DONE2')
