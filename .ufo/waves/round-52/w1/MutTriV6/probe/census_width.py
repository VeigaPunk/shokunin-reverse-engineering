#!/usr/bin/env python3
"""Probe: is the v6 new row's FAMILY key wider than the reader census it rests on?

The frozen reader census (tools/round-50-c3/sqfs-triage-v5.py:150-156) is
FIXTURE-level: `squashfs_v3_ddwrt` is 6/7 NO-READER -- one of the seven measured ddwrt
fixtures IS reader-backed.  The v6 new row keys on the FAMILY (`squashfs_v3_ddwrt`),
so it prescribes `preserve-unresolved` for EVERY ddwrt FAILED body, including the
reader-backed variant -- a widening the census does not support.

This probe measures:
  (a) how many ddwrt FAILED bodies the corpus carries (the corpus can only witness 1),
  (b) what the v6 row does to a SYNTHETIC ddwrt FAILED body that stands for the
      reader-backed 1/7 variant (the corpus cannot witness this),
  (c) whether the audit's census has the same width problem.
"""
import sys, json, os, datetime

sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6')
import proto_v6 as P

OUT = sys.argv[1]
corpus = P.load_corpus()

ddwrt_failed = [(e, f['HF']) for e, _p, f in corpus
                 if 'extractor-failure' in f['G'] and f['P'] == 0
                 and 'squashfs_v3_ddwrt' in f['HF']]
ddwrt_all = [(e, f['G'], f['P']) for e, _p, f in corpus
              if 'squashfs_v3_ddwrt' in f['F']]

# A synthetic ddwrt FAILED body standing for the reader-backed 1/7 variant.
# The census says 6/7 ddwrt fixtures have NO reader; 1/7 DOES.  A family-level key
# cannot tell them apart (the scored features expose no body variant -- v5 docstring).
synthetic_reader_backed = P.v5._env(handler='squashfs_v3_ddwrt',
                                     gaps=['extractor-failure'], be='-be', files=0)

br, _ = P.parse(P.V6_ROWS)
label, action = P.v5.decision(P.v5.classify(br, P.v5.features(synthetic_reader_backed)))
v5r, _ = P.parse(P.v5.V5_ROWS, P.v5.V5_ACTIONS, P.v5.MARKER_V5)
v5_label, v5_action = P.v5.decision(
    P.v5.classify(v5r, P.v5.features(synthetic_reader_backed)))

out = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'corpus_ddwrt_FAILED_bodies': ddwrt_failed,
    'corpus_ddwrt_envelopes_total': len(ddwrt_all),
    'census_source': 'tools/round-50-c3/sqfs-triage-v5.py:150-156 -- FIXTURE-level: '
                     'squashfs_v3_ddwrt 6/7 NO-READER (one of the seven measured ddwrt '
                     'fixtures IS reader-backed)',
    'synthetic_reader_backed_ddwrt_FAILED_body': {
        'v6_table': [label, action],
        'v5_table': [v5_label, v5_action],
        'note': 'the v6 family key prescribes preserve-unresolved for a body the census '
                'says has a reader -- the census is not narrow enough to justify it, '
                'and the corpus carries only the no-reader variant so it cannot witness '
                'the difference',
    },
    'audit_width': {
        'audit_census_no_reader_set': list(P.NO_VALIDATED_READER),
        'ddwrt_in_audit_no_reader_set': 'squashfs_v3_ddwrt' in P.NO_VALIDATED_READER,
        'note': 'the audit census is also family-level, so it shares the same width: it '
                'would NOT flag a cross-read on the reader-backed 1/7 ddwrt variant',
    },
}
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write('\n')
print(json.dumps(out, indent=1, sort_keys=True))
