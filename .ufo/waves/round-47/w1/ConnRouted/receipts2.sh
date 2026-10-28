#!/usr/bin/env bash
# Second batch (appends): helper identical to receipts.sh, no truncation.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r47/ConnRouted
OUT="$LANE/.ufo/waves/round-47/w1/ConnRouted"
mkdir -p "$OUT"

r() {
  local label="$1"; shift
  local tmp="$S/.s.$$"
  local cmd; cmd=$(printf '%q ' "$@")
  ( cd "$LANE" && "$@" ) > "$tmp" 2>&1
  local code=$?
  local sha; sha=$(sha256sum "$tmp" | awk '{print $1}')
  python3 - "$label" "$code" "$sha" "$tmp" "$cmd" <<'PY' >> "$OUT/receipts.jsonl"
import json, sys, datetime
label, code, sha, path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
cmd = sys.argv[5]
body = open(path).read()
print(json.dumps({"label": label, "exit": code, "stdout_sha256": sha,
                  "utc": datetime.datetime.now(datetime.timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "stdout_tail": body[-300:] if len(body) > 300 else body,
                  "cmd": cmd}, sort_keys=True))
PY
  rm -f "$tmp"
}

r porcelain_split bash -c "git status --porcelain | awk '{print substr(\$0,1,2)}' | sort | uniq -c"
r scorecard_round47_preverdict_line bash -c "grep -n 'all before any claim verdict' SCORECARD.md"
r log_round47_amendments_line bash -c "grep -n 'Four amendments before verdict' LOG.md"
r claims_A2_after_data_line bash -c "grep -n 'first after-data run' plans/round-47-claims.md"
r scorecard_round47_before_cell bash -c "grep -n 'at the freeze exit 1' SCORECARD.md"
r untracked_split bash -c "git ls-files --others --exclude-standard | awk -F/ '{print \$1\"/\"\$2}' | sort | uniq -c | sort -rn | head -6"
r block23_header_line sed -n '614p' SKILL.md
echo "receipts total: $(wc -l < "$OUT/receipts.jsonl")"
