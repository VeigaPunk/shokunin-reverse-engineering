#!/bin/sh
# R45W2Src141 fixture battery: does the frozen commit arm see what S141 says it sees?
# Every call names -C "$D"; toplevel asserted before the first commit.
set -u
S=${1:?scratch dir}
GATE=${2:?preflight copy}
UTC() { date -u +%Y-%m-%dT%H:%M:%SZ; }

mk() {  # $1=dir suffix; echoes the repo dir
    d=$(mktemp -d -p "$S" "fx.$1.XXXX") || exit 2
    git -C "$d" init -q
    git -C "$d" config user.email r45w2@selftest
    git -C "$d" config user.name r45w2
    top=$(git -C "$d" rev-parse --show-toplevel)
    [ "$top" = "$d" ] || { echo "TOPLEVEL_MISMATCH $top != $d"; exit 2; }
    echo "$d"
}

run() { # $1=label $2=repo $3=freeze $4=rev $5=pathspec $6=freeze-path ; prints receipt
    echo "### $1  utc=$(UTC)"
    python3 "$GATE" --root "$2" --freeze "$3" --rev "$4" \
        --pathspec "$5" --freeze-path "$6" --check-dirty
    echo "exit=$?"
}

# --- case A: ASCII frozen file modified (the round's actual path shape) -----
D=$(mk ascii)
mkdir -p "$D/frozen"; printf 'alpha\n' > "$D/frozen/a.txt"; printf 'o\n' > "$D/other.txt"
git -C "$D" add -A; git -C "$D" commit -qm freeze; F=$(git -C "$D" rev-parse HEAD)
printf 'beta\n' > "$D/frozen/a.txt"; git -C "$D" add -A; git -C "$D" commit -qm touch; R=$(git -C "$D" rev-parse HEAD)
run A-ascii-touched "$D" "$F" "$R" frozen/ frozen

# --- case B: nothing frozen touched (green control) -------------------------
D=$(mk green); mkdir -p "$D/frozen"; printf 'alpha\n' > "$D/frozen/a.txt"; printf 'o\n' > "$D/other.txt"
git -C "$D" add -A; git -C "$D" commit -qm freeze; F=$(git -C "$D" rev-parse HEAD)
printf 'o2\n' > "$D/other.txt"; git -C "$D" add -A; git -C "$D" commit -qm unrelated; R=$(git -C "$D" rev-parse HEAD)
run B-ascii-clean "$D" "$F" "$R" frozen/ frozen

# --- case C: frozen file whose name git C-quotes ---------------------------
D=$(mk uni); mkdir -p "$D/frozen"; printf 'alpha\n' > "$D/frozen/ü.txt"
git -C "$D" add -A; git -C "$D" commit -qm freeze; F=$(git -C "$D" rev-parse HEAD)
printf 'beta\n' > "$D/frozen/ü.txt"; git -C "$D" add -A; git -C "$D" commit -qm touch; R=$(git -C "$D" rev-parse HEAD)
echo "### C-quoted frozen name, utc=$(UTC)"
echo "-- plain git log --name-status (bytes) --"
git -C "$D" log -m --diff-merges=first-parent --name-status --format='%x00%H' "$F..$R" | od -c
echo "-- status of rev-parse on the receipt's own path --"
git -C "$D" rev-parse "$F:\"frozen/\\303\\274.txt\"" >/dev/null 2>&1; echo "rev-parse-quoted-exit=$?"
git -C "$D" rev-parse "$F:frozen/ü.txt" >/dev/null 2>&1; echo "rev-parse-raw-exit=$?"
run C-quoted-touched "$D" "$F" "$R" frozen/ frozen

# --- case D: -z form (the flag the arm does not pass) ----------------------
echo "### D -z output, utc=$(UTC)"
git -C "$D" log -m --diff-merges=first-parent --name-status -z --format='%x00%H' "$F..$R" | od -c
echo "exit=$?"

# --- case E: frozen path with a literal newline in its name ---------------
D=$(mk nl); mkdir -p "$D/frozen"; N=$(printf 'a\nb.txt'); printf 'x\n' > "$D/frozen/$N"
git -C "$D" add -A; git -C "$D" commit -qm freeze; F=$(git -C "$D" rev-parse HEAD)
printf 'y\n' > "$D/frozen/$N"; git -C "$D" add -A; git -C "$D" commit -qm touch; R=$(git -C "$D" rev-parse HEAD)
echo "### E newline name, plain name-status, utc=$(UTC)"
git -C "$D" log --name-status --format='%x00%H' "$F..$R" | cat -A
echo "-- -z --"
git -C "$D" log --name-status -z --format='%x00%H' "$F..$R" | od -c
run E-newline-touched "$D" "$F" "$R" frozen/ frozen

# --- case F: quoted name touched then restored (the restored[] row) --------
D=$(mk restore); mkdir -p "$D/frozen"; printf 'alpha\n' > "$D/frozen/ü.txt"
git -C "$D" add -A; git -C "$D" commit -qm freeze; F=$(git -C "$D" rev-parse HEAD)
printf 'tamper\n' > "$D/frozen/ü.txt"; git -C "$D" add -A; git -C "$D" commit -qm tamper
printf 'alpha\n' > "$D/frozen/ü.txt"; git -C "$D" add -A; git -C "$D" commit -qm restore; R=$(git -C "$D" rev-parse HEAD)
run F-quoted-restored "$D" "$F" "$R" frozen/ frozen
