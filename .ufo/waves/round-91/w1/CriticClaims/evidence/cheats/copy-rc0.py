#!/usr/bin/env python3
import shutil, sys
a = sys.argv[sys.argv.index("--in")+1]; b = sys.argv[sys.argv.index("--out")+1]
shutil.copyfile(a, b)
sys.exit(0)
