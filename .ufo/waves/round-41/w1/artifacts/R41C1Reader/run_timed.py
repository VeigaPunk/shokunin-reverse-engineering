import os, resource, subprocess, sys, time
t0=time.time()
p=subprocess.run(sys.argv[1:], capture_output=True)
w=time.time()-t0
ru=resource.getrusage(resource.RUSAGE_CHILDREN)
sys.stderr.write("ELAPSED=%.2fs MAXRSS_KB=%d EXIT=%d\n" % (w, ru.ru_maxrss, p.returncode))
sys.stderr.write("STDOUT_TAIL:\n"+p.stdout.decode('utf-8','replace')[-3000:])
sys.stderr.write("STDERR_TAIL:\n"+p.stderr.decode('utf-8','replace')[-3000:])
sys.exit(p.returncode)
