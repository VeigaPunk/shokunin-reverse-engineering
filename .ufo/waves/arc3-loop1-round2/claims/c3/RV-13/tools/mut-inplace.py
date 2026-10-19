import os,sys
p=sys.argv[1]; st=os.stat(p); d=open(p,'rb').read()
with open(p,'r+b') as fh: fh.write(d)
print("in-place rewrite of %d identical bytes; inode=%d mtime_ns was=%d ctime_ns was=%d" % (len(d), st.st_ino, st.st_mtime_ns, st.st_ctime_ns))
