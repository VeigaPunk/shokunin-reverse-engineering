cd '/home/vgpnk/Projects/shokunin/kaidoku-shokunin' && awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
