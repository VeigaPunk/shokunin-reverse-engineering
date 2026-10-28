import subprocess, sys
R='29883d4ec35a31a8393c4ffb220888c44c0bb022'
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def blob(path, rev=R):
    return subprocess.run(['git','-C',LANE,'show',f'{rev}:{path}'],capture_output=True).stdout
