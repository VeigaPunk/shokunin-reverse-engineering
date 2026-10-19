#!/usr/bin/env bash
# EX-40 scratch fixture builder — recreates /var/tmp/ex40/fix deterministically.
# SCRATCH ONLY: none of these paths is a custody path; the real custody paths are
# never written (hash/stat capture only, in the seat's own evidence files).
# Fixture shapes map 1:1 to the declared classes in edge-cases.md.
set -eu
R=${1:-/var/tmp/ex40/fix}
rm -rf "$(dirname "$R")/fix"
mkdir -p "$R"; cd "$R"
printf 'alpha-content-1\n' > good.txt
printf 'same-bytes\n' > twin_a.txt; cp twin_a.txt twin_b.txt
mkdir dir_target; printf 'x\n' > dir_target/inner.txt
mkdir blocked_dir; printf 'y\n' > blocked_dir/inner.txt
mkfifo pipe.fifo
ln -s good.txt link_ok.txt                 # symlink -> regular (resolves)
ln -s no_such_target.txt link_dangling.txt # symlink -> missing target
ln -s link_loop_b link_loop_a              # symlink cycle (ELOOP on follow)
ln -s link_loop_a link_loop_b
ln -s dir_target link_dir                  # symlink -> directory
ln -s /dev/null link_devnull               # symlink -> character device
ln -s ../fix/good.txt link_relative        # relative symlink target
printf 'hidden\n' > unreadable.txt; chmod 000 unreadable.txt   # EACCES on open
chmod 000 blocked_dir                                          # EACCES on path resolution
echo "fixtures built in $R:"; ls -la "$R"
