import os,sys
p=sys.argv[1]; st=os.stat(p); d=open(p,'rb').read()
with open(p,'r+b') as fh: fh.write(d)
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))
a=os.stat(p)
print("in-place + mtime restored ns-exact: inode %d (same=%s) mtime_ns restored=%s ctime_ns moved=%s" % (a.st_ino, a.st_ino==st.st_ino, a.st_mtime_ns==st.st_mtime_ns, a.st_ctime_ns!=st.st_ctime_ns))
