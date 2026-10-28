import json, os, hashlib
S = '/fast/scratch/hyaku/kaidoku-r49/CritFreeze'
L = lambda n: json.load(open(os.path.join(S, n)))
w1, w2, w3, w4, w5, w6, mx = (L('results-walk.json'), L('results-walk2.json'), L('results-walk3.json'),
    L('results-walk4.json'), L('results-walk5.json'), L('results-walk6.json'), L('matrix.json'))
rows = []
def c1s(r):
    return ('touched ' + str(r['touched'])) if 'touched' in r else ('error ' + r.get('error', ''))
def c2s(r):
    return 'exit %s reason=%s mismatches=%s' % (r['exit'], r['reason'], r['mismatches'])
def add(label, rev, c1walk, c2walk, cli=None, note=''):
    if cli is None:
        for key in mx:
            if key.split('_')[0] == label.split('_')[0] and mx[key]['rev'][:12] == rev[:12] and key != 'x':
                m = mx[key]['c1_cli']; cli = 'exit %s reason=%s (matrix)' % (m['exit'], m['reason']); break
    rows.append((label, rev[:12], c1s(c1walk), c2s(c2walk), cli or 'not run', note))
for k in ['S0_benign_nonfrozen','S1a_touch_restore_c1counter','S1b_touch_restore_c2mismatch','S1c_touch_restore_c1controls',
          'S1d_touch_restore_carriers','S1e_touch_restore_c1oracle','S2a_new_file_tools','S2b_new_file_nested',
          'S3a_merge_commit_edits_carriers','S3b_side_edit_reverted_in_merge','S3c_side_new_tool_merged','S4_rename_inside',
          'S5_rename_out','S6_rename_in_nonfrozen','S7_mode_change','S8_symlink_swap','S9_delete_file']:
    v = w1[k]; m = mx[k]
    cli = 'exit %s reason=%s' % (m['c1_cli']['exit'], m['c1_cli']['reason'])
    add(k, v['rev'], v['c1_walk'], v['c2_walk'], cli)
for k in ['S3d_side_edit_revert_on_side','S10_rev_is_base','S11_sibling_readd','S12_quoted_name_edit','S13_refreeze_operator_freeze','S14_plain_copy_add']:
    v = w2[k]; add(k, v['rev'], v['c1_walk'], v['c2_walk'], note='freeze=%s' % v['freeze'][:12])
v = w4['S15b_replace_touch']
add('S15b_replace_on (X replaced by tree=FREEZE commit)', v['rev'], v['walk_replace_on']['c1'], v['walk_replace_on']['c2'])
v = w6['S15b_no_replace_env']; add('S15b_GIT_NO_REPLACE_OBJECTS=1 (mitigation probe)', w4['S15b_replace_touch']['rev'], v['c1'], v['c2'], 'not run (walk probe only, env set)')
v = w6['S27_squash']; add('S27_squash (one commit, FREEZE tree)', v['rev'], v['c1'], v['c2'])
v = w3['S16_grafts']; add('S16_grafts (.git/info/grafts cuts touching commit)', v['rev'], v['c1_walk'], v['c2_walk'])
v = w5['S24_plan_edit']; add('S24_plan_edit', v['rev'], v['c1_walk'], v['c2_walk'])
v = w5['S25_round42_frozen_tool_edit']; add('S25_round42_fixtures_edit (plan: byte-frozen)', v['rev'], v['c1_walk'], v['c2_walk'])
v = w5['S26_round44_oracle_edit']; add('S26_round44_oracle_edit (plan: byte-frozen)', v['rev'], v['c1_walk'], v['c2_walk'])
hdr = '| manoeuvre | REV | C1 freeze walk | C2 freeze walk | C1 CLI (full counter) | note |\n|---|---|---|---|---|---|\n'
body = ''.join('| %s | %s | %s | %s | %s | %s |\n' % (a, b, c, d, e, f) for a, b, c, d, e, f in rows)
open(os.path.join(S, 'matrix.md'), 'w').write(hdr + body)
print(hdr + body)
