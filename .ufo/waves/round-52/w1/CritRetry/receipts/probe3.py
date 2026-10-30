import importlib.util, json, os, sys, hashlib, datetime
S=os.path.dirname(os.path.abspath(__file__))
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
COUNTER=os.path.join(LANE,'tools/round-50/c1-counter.py')
spec=importlib.util.spec_from_file_location('c50',COUNTER); m=importlib.util.module_from_spec(spec); sys.modules['c50']=m; spec.loader.exec_module(m)

def env_with(link_target, drop=False):
    e={'normalized_result':{'files':[{'relative_path':'firmware.bin_extract/usr/www/cgi-bin/luacgi','sha256':'a'*64,'size':10,'mime_type':'application/octet-stream'}],
        'chunks':[{'handler':'squashfs_v4_le','range':{'offset':0,'length':100},'extraction_failed':False}],
        'extraction_gaps':[],
        'unpublished_entries':([] if drop else [{'kind':'symlink','relative_path':'firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi','link_target':link_target}]),
        'diagnostics':[],
        'derivations':[],'engine':{'name':'unblob','version':'26.6.4'},'published_bytes':10,'coverage':'partial'},
        'subject':{'digest':{'sha256':'b'*64}},'parameters':{}}
    return e

out={'probe':'CritRetry probe3: is the frozen projection sensitive to the symlink link_target and to a dropped symlink?',
     'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'projection_profile_in_receipt':'plus-extractor',
     'PROJECTION_KEYS_BY_PROFILE':{k:list(v) for k,v in m.PROJECTION_KEYS_BY_PROFILE.items()}}

a=m.projection(env_with('../../../www/cgi-bin/luacgi'),'plus-extractor')
b=m.projection(env_with('/usr/www/cgi-bin/luacgi'),'plus-extractor')
eq,keys,detail=m.projection_diff(a,b,'plus-extractor')
out['link_target_changed_absolute_vs_rewritten']={'projection_equal':eq,'differing_keys':keys,
   'NOTE':'the two envelopes differ ONLY in unpublished_entries[0].link_target (the value unblob writes after its unlink+relink rewrite) -> the projection is BLIND to it'}
c=m.projection(env_with('../../../www/cgi-bin/luacgi',drop=True),'plus-extractor')
eq2,keys2,detail2=m.projection_diff(a,c,'plus-extractor')
out['symlink_entry_dropped_entirely']={'projection_equal':eq2,'differing_keys':keys2,'detail':detail2}
out['summary']=['link_target is NOT in the projection (unpub rows are [kind, relative_path] only) -> a run whose symlink rewrite landed differently projects EQUAL',
                'dropping the symlink entry entirely DOES change the projection (unpublished_entries) -> the projection catches a LOST entry but not a REWRITTEN one']
print(json.dumps(out,indent=1,sort_keys=True))
