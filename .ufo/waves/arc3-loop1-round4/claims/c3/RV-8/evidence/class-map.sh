#!/usr/bin/env bash
# RV-8 class-map — exercise every declared exit class on any revision of the
# custody-pair tool, and print a stable one-line-per-class transcript.
# usage: class-map.sh <tool.py> <workroot> <tag>
set -u
TOOL="$1"; W="$2"; TAG="$3"
F="$W/fixtures"; rm -rf "$W"; mkdir -p "$F" "$W/st"
sha256sum "$TOOL" | sed "s|^|[$TAG] tool |"
echo "[$TAG] lines=$(wc -l < "$TOOL")"

run() { # run <id> <expected-rc> <args...>
  local id="$1"; shift
  local exp="$1"; shift
  local out rc line
  out=$(cd "$F" && python3 "$TOOL" "$@" 2>&1); rc=$?
  line=$(printf '%s\n' "$out" | grep -E "^(CUSTODY_PAIR_(VERIFY|CAPTURE|SELFTEST)|VERDICT|USAGE|REFERENCE-COVERAGE)" | tail -1)
  printf '%-24s rc=%-3s exp=%-3s %s\n' "$id" "$rc" "$exp" "${line:0:140}"
}

# --- class 0 MATCH ---------------------------------------------------------
printf 'alpha\n' > "$F/a.conf"
run cap-0 0 capture --paths "$F/a.conf" --out "$F/a.txt" --label t
run verify-live-0 0 verify "$F/a.txt" --live

# --- class 10 CONTENT-DRIFT ------------------------------------------------
printf 'beta-ORIG\n' > "$F/b.conf"
run cap-b0 0 capture --paths "$F/b.conf" --out "$F/b-pre.txt"
printf 'beta-EVIL\n' > "$F/b.conf"
run verify-10 10 verify "$F/b-pre.txt" --live

# --- class 11 REWRITE-DRIFT (same content, new inode) -----------------------
printf 'gamma\n' > "$F/c.conf"
run cap-c0 0 capture --paths "$F/c.conf" --out "$F/c-pre.txt"
rm -f "$F/c.conf"; printf 'gamma\n' > "$F/c.conf"
run verify-11 11 verify "$F/c-pre.txt" --live

# --- class 12 METADATA-DRIFT (chmod) ---------------------------------------
printf 'delta\n' > "$F/d.conf"
run cap-d0 0 capture --paths "$F/d.conf" --out "$F/d-pre.txt"
chmod 640 "$F/d.conf"
run verify-12 12 verify "$F/d-pre.txt" --live

# --- class 13 ABSENT (reference exists, candidate absent) -------------------
printf 'eps\n' > "$F/g.conf"
run cap-g0 0 capture --paths "$F/g.conf" --out "$F/g-pre.txt"
rm -f "$F/g.conf"
run verify-13 13 verify "$F/g-pre.txt" --live

# --- class 14 UNEVALUABLE (blocked parent dir) -----------------------------
mkdir -p "$F/blk"; printf 'x\n' > "$F/blk/z.conf"; chmod 000 "$F/blk"
run cap-14 14 capture --paths "$F/blk/z.conf" --out "$F/f.txt"
run verify-14 14 verify "$F/f.txt" --live
chmod 755 "$F/blk"

# --- class 2 USAGE: write-guard, coverage gate, scratch guard ---------------
run guard-2 2 capture --paths "$F/a.conf" --out "$F/a.conf"
run gate-2 2 verify "$F/a.txt" --live --require-paths 5
run scratch-2 2 selftest --scratch "$F/does-not-exist"

# --- the four r4 residual vectors ------------------------------------------
# (a) sidecar scope: --paths X.sha256 --out X  → sidecar lands on measured file
printf 'meas\n' > "$F/v.sha256"
run sidecar-a "$?" capture --paths "$F/v.sha256" --out "$F/v"
printf '%-24s measured-file-after: size=%s head=%s\n' sidecar-a "$(stat -c%s "$F/v.sha256")" "$(head -c 24 "$F/v.sha256" | tr '\n' '|')"
# (a2) the r3-literal spelling: --out X.sha256 --paths X → sidecar is neighbour
printf 'meas2\n' > "$F/w"
run sidecar-a2 "$?" capture --paths "$F/w" --out "$F/w.sha256"
printf '%-24s neighbour-after: size=%s head=%s\n' sidecar-a2 "$(stat -c%s "$F/w.sha256")" "$(head -c 24 "$F/w.sha256" | tr '\n' '|')"
# (b) mkdir outside the guarded try
printf 'plain\n' > "$F/notadir"
run mkdir-b 2 capture --paths "$F/a.conf" --out "$F/notadir/sub/r.txt"
run mkdir-b2 2 capture --paths "$F/a.conf" --out ""
# (c) coverage gate counts stanzas, not distinct paths
python3 "$TOOL" capture --paths "$F/a.conf" "$F/a.conf" "$F/a.conf" "$F/a.conf" "$F/a.conf" --out "$F/dupe5.txt" >/dev/null 2>&1
run dupe-gate 2 verify "$F/dupe5.txt" --live --require-paths 5
# (d) both-sides-absent semantics: capture an ABSENT path, then verify --live
run cap-absent 13 capture --paths "$F/never-was.conf" --out "$F/h-absent.txt"
run both-absent 0 verify "$F/h-absent.txt" --live

# --- selftest ---------------------------------------------------------------
run selftest-0 0 selftest --scratch "$W/st"
