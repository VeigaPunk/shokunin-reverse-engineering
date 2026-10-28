R=/fast/scratch/hyaku/kaidoku-r49
for e in $(ls -A "$R"); do
  hits=0; procs=""
  for d in /proc/[0-9]*; do
    c=$(readlink "$d/cwd" 2>/dev/null)
    case "$c" in "$R/$e"|"$R/$e"/*) procs="$procs ${d#/proc/}";; esac
    for f in "$d"/fd/*; do
      l=$(readlink "$f" 2>/dev/null)
      case "$l" in "$R/$e"|"$R/$e"/*) hits=$((hits+1));; esac
    done
  done 2>/dev/null
  echo "$e | open_fd_hits=$hits | cwd_pids=[$procs ]"
done
