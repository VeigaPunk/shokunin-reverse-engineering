import json, sys
print(json.dumps({"schema":1,"needed":[{"file":"libc.so.6","versions":[{"name":"GLIBC_2.14","flags":0,"other":7,"hash":110530964}]}]}, sort_keys=True, separators=(",",":")))
