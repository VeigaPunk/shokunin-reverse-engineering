set -u
S="$1"; D=$(mktemp -d -p "$S" fx2.XXXXXXXX); git -C "$D" init -q -b main
T=$(git -C "$D" rev-parse --show-toplevel); [ "$T" = "$D" ] || { echo "GUARD FAIL $T"; exit 9; }
export GIT_AUTHOR_NAME=fx GIT_AUTHOR_EMAIL=fx@example.invalid GIT_COMMITTER_NAME=fx GIT_COMMITTER_EMAIL=fx@example.invalid
export GIT_AUTHOR_DATE=2026-10-28T00:00:00Z GIT_COMMITTER_DATE=2026-10-28T00:00:00Z
printf 'a\nb\nc\n' > "$D/f.txt"; printf 'x\n' > "$D/keep.txt"; git -C "$D" add -A; git -C "$D" commit -qm base
git -C "$D" checkout -q -b side; printf 'a\nSIDE\nc\n' > "$D/f.txt"; git -C "$D" commit -qam side
git -C "$D" checkout -q main; printf 'a\nMAIN\nc\n' > "$D/f.txt"; git -C "$D" commit -qam main
git -C "$D" merge --no-ff -q side -m merge 2>/dev/null
printf 'a\nRESOLVED\nc\n' > "$D/f.txt"; git -C "$D" add f.txt; git -C "$D" commit -qm 'merge with resolution'
echo "git_version $(git --version)"
echo "merge_commit $(git -C "$D" rev-parse HEAD) parents $(git -C "$D" rev-list --parents -n1 HEAD)"
for v in "D_plain::--name-status" "A_dmfp:--diff-merges=first-parent:--name-status" "B_m:-m:--name-status" "C_rev:--diff-merges=first-parent:-m:--name-status"; do
  n=${v%%:*}; args=${v#*:}; args=${args//:/ }
  echo "### $n :: git log $args -1"
  # shellcheck disable=SC2086
  git -C "$D" log $args -1 --format='%H %s' | sed 's/^/  /'
  echo "### exit $?"
done
echo "### z_parse first arm (-m --diff-merges=first-parent --name-status -z)"
git -C "$D" log -m --diff-merges=first-parent --name-status -z -1 --format= | od -An -c
