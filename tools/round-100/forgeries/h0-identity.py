import argparse, shutil, sys
ap = argparse.ArgumentParser()
ap.add_argument('--in', dest='inp', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
shutil.copyfile(a.inp, a.out)
print('ok intact')
