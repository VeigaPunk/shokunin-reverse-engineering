# Exact commands as executed 2026-10-28T15:36Z..15:43Z (UTC), lane root L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
# F=f762b7273e3f6ca3c710bb37d5de92a4a4417aec   B=149133d47aa7e90796f96047afe6d251a3e65b2c   HEAD=faa875bc0eb839d15b83c4afa6078819e5a7b381
# S=/fast/scratch/hyaku/kaidoku-r45/R45W1RevFreezeCommit (TMPDIR=S); frozen interpreter extracted to $S/preflight-frozen.py

# Q1 scope
git -C "$L" diff-tree --no-commit-id --name-status -r "$F"
git -C "$L" diff-tree --no-commit-id --name-status -r -M -C "$F"
git -C "$L" show --numstat --format='' "$F"
git -C "$L" show --no-patch --format='fuller%n---AUTHOR---%n%an%n%ae%n%aI%n---COMMITTER---%n%cn%n%ce%n%cI%n---MSG---%n%s%n%b' "$F"
git -C "$L" cat-file -p "$F"

# Q3 worktree
git -C "$L" status --porcelain
git -C "$L" status --porcelain --untracked-files=no

# Q4 frozen preflight (exact form asked for, then variants)
python3 -I -B "$S/preflight-frozen.py" --root "$L" --freeze "$B" --rev "$F" --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec                                   # A1 exit 1
python3 -I -B "$S/preflight-frozen.py" --root "$L" --freeze "$B" --rev "$F" --pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec   # A2 exit 1
python3 -I -B "$S/preflight-frozen.py" --root "$L" --freeze "$F" --rev "$F" --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec                                   # A3 exit 0
python3 -I -B "$S/preflight-frozen.py" --root "$L" --freeze "$F" --rev "$HEAD" --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty                    # A4 exit 0
python3 -I -B "$S/preflight-frozen.py" --root "$L" --freeze "$F" --rev "$HEAD" --pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec --check-dirty   # A5 exit 0

# Cross-instrument freeze arm on the same (parent-based) range
python3 -I -B "$L/tools/round-45/c1-counter.py" --root "$L" --freeze "$B" --rev "$F"    # B3 exit 2
python3 -I -B "$L/tools/round-45/c2-counter.py" --root "$L" --freeze "$B" --rev "$F"    # B4 exit 2

# Do-nothing before controls, reproduced from frozen bytes
python3 -I -B "$L/tools/round-45/c1-counter.py" --root "$L" --freeze "$F" --rev "$F"    # B1 exit 1, dict-identical to controls/ctl-c1-0-do-nothing.json
python3 -I -B "$L/tools/round-45/c2-counter.py" --root "$L" --freeze "$F" --rev "$F"    # B2 exit 1, dict-identical to controls/ctl-c2-0-do-nothing.json

# Selftests
python3 -I -B "$S/preflight-frozen.py" --selftest            # C1 exit 0, cases=11 failures=0
python3 -I -B "$L/tools/round-45/c1-counter.py" --selftest   # C2 exit 0, cases=9  failures=0
python3 -I -B "$L/tools/round-45/c2-counter.py" --selftest   # C3 exit 0, cases=7  failures=0

# Frozen-byte identity now vs freeze
git -C "$L" diff --stat "$F" -- plans/round-45-claims.md tools/round-45/     # empty
git -C "$L" log --format=%H -1 -- plans/round-45-claims.md                   # f762b727...
git -C "$L" log --format='%h %aI %s' --name-status "$F"..HEAD -- plans/round-45-claims.md tools/round-45/   # empty
