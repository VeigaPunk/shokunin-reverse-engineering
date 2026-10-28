import json,subprocess,sys
R=sys.argv[1]
for cid in ["v1le","v1be","v2le","v2be"]:
    p=f"corpus/evidence/round-49/c1/{cid}/after.json"
    d=json.loads(subprocess.run(['git','show',f'{R}:{p}'],capture_output=True,text=True).stdout)
    print(cid, sorted(d.keys()))
    print("  top-level sample:", {k:d[k] for k in d if k in ('carrier_id','handler','failing','gaps','unpublished_entries','carrier_pin','subject_digest','evidence_id','semantic_projection','chunks','oracle_match','published')} )
