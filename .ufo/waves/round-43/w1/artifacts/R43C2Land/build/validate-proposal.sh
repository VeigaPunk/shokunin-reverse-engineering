#!/usr/bin/env bash
# validate-proposal — apply the F4 gate extension IN A SANDBOX CLONE ONLY and
# check the acceptance criteria stated in proposal/gate-extension-F4.patch.
#
# The lane's tools/round-41/local-source-gate.py is never modified: the patch is
# applied to a copy inside a throwaway clone.
#
# Usage: validate-proposal.sh <pack-dir> <scratch-dir> <receipts-dir>
set -u
P=${1:?pack dir}
S=${2:?scratch dir}
R=${3:?receipts dir}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REV=6b9e64fe7e0de202d9383baad5792fbfe039a743
mkdir -p "$R"
D=$(mktemp -d "$S/fx.XXXX") || exit 1
git clone -q --shared "$LANE" "$D/lane" || exit 1
top=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$top" = "$D/lane" ] || { echo "clone toplevel mismatch: $top"; exit 1; }
cp -a "$P/corpus/." "$D/lane/corpus/" || exit 1
cd "$S" || exit 1
G="$D/lane/tools/round-41/local-source-gate.py"

echo "### 0. the lane's gate is untouched (sha256 before/after the experiment)"
sha256sum "$LANE/tools/round-41/local-source-gate.py" | tee "$R/lane-gate-before.txt"

echo "### 1. apply the extension to the sandbox copy only"
python3 - "$G" <<'PY'
import sys
path = sys.argv[1]
src = open(path, encoding="utf-8").read()

old_keys = ('ENTRY_KEYS = {"copy", "sha256", "sha256_file", "kind", "note", '
            '"source_sha256", "rebuild"}')
new_keys = ('ENTRY_KEYS = {"copy", "sha256", "sha256_file", "kind", "note", '
            '"source_sha256", "rebuild", "encoding", "members"}\n'
            'ENTRY_KINDS = ("file", "tree-archive", "compressed", "member-excerpt")\n'
            'ENTRY_ENCODINGS = ("gzip",)')
assert old_keys in src, "ENTRY_KEYS anchor not found"
src = src.replace(old_keys, new_keys)

old_kind = ('    kind = entry.get("kind")\n'
            '    if kind is not None and kind not in ("file", "tree-archive"):\n'
            '        return fail("map-kind-invalid", copy=copy, kind=kind)')
new_kind = ('    kind = entry.get("kind")\n'
            '    if kind is not None and kind not in ENTRY_KINDS:\n'
            '        return fail("map-kind-invalid", copy=copy, kind=kind)\n'
            '    encoding = entry.get("encoding")\n'
            '    if encoding is not None and encoding not in ENTRY_ENCODINGS:\n'
            '        return fail("map-encoding-invalid", copy=copy, encoding=encoding)\n'
            '    members = entry.get("members")\n'
            '    if members is not None:\n'
            '        if not isinstance(members, list) or not all(isinstance(m, str) for m in members):\n'
            '            return fail("map-members-invalid", copy=copy)\n'
            '    # a shape claim must be self-consistent: a compressed copy names its\n'
            '    # encoding, and a member excerpt names its members\n'
            '    if kind == "compressed" and not encoding:\n'
            '        return fail("map-kind-encoding-mismatch", copy=copy, kind=kind)\n'
            '    if kind == "member-excerpt" and not members:\n'
            '        return fail("map-kind-members-mismatch", copy=copy, kind=kind)\n'
            '    # a named member must actually be present in the copy\n'
            '    if members and kind in ("tree-archive", "member-excerpt"):\n'
            '        import tarfile\n'
            '        try:\n'
            '            with tarfile.open(copy_abs, "r:") as tar:\n'
            '                present = {m.name for m in tar.getmembers()}\n'
            '        except tarfile.TarError:\n'
            '            present = None\n'
            '        if present is not None:\n'
            '            absent = [m for m in members if m not in present]\n'
            '            if absent:\n'
            '                return fail("map-member-absent", copy=copy, absent=absent)')
assert old_kind in src, "kind check anchor not found"
src = src.replace(old_kind, new_kind)

open(path, "w", encoding="utf-8").write(src)
print("patched", path)
PY
echo "patch exit=$?"

echo "### 2. the extended gate still passes its own selftest"
python3 -I -B "$G" --selftest > "$R/proposal-selftest.txt" 2>&1
echo "selftest exit=$?"; tail -1 "$R/proposal-selftest.txt"

echo "### 3. the extended gate still greens the round-43 pack"
python3 -I -B "$G" --root "$D/lane" --rev "$REV" --json > "$R/proposal-gate-green.json" 2>&1
echo "gate exit=$?"
python3 -c "
import json; d=json.load(open('$R/proposal-gate-green.json'))
print('rows_failed', d['rows_failed'], 'rows_total', d['rows_total'])"

echo "### 4. control: kind compressed WITHOUT encoding must be red"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-c.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/data/typeinfo/golang/go1.25.0.json"):
        v["kind"] = "compressed"
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/lane/corpus/evidence/local-sources.json" "$D/map-orig.json"
cp "$D/map-c.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$G" --root "$D/lane" --rev "$REV" --json > "$R/proposal-kind-compressed.json" 2>&1
echo "kind-compressed exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### 5. control: encoding gzip WITH kind compressed must be green"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-e.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/data/typeinfo/golang/go1.25.0.json"):
        v["kind"] = "compressed"
        v["encoding"] = "gzip"
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-e.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$G" --root "$D/lane" --rev "$REV" --json > "$R/proposal-encoding-green.json" 2>&1
echo "encoding-green exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### 6. control: a bogus encoding must be red"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-x.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/data/typeinfo/golang/go1.25.0.json"):
        v["encoding"] = "brotli"
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-x.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$G" --root "$D/lane" --rev "$REV" --json > "$R/proposal-bad-encoding.json" 2>&1
echo "bad-encoding exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### 7. control: a members list naming an absent member must be red"
python3 - "$D/lane/corpus/evidence/local-sources.json" "$D/map-m.json" <<'PY'
import json, sys
doc = json.load(open(sys.argv[1]))
for k, v in doc["sources"].items():
    if k.endswith("/lib/Base-src.zip"):
        v["kind"] = "member-excerpt"
        v["members"] = ["ghidra/app/util/bin/format/golang/rtti/DoesNotExist.java"]
json.dump(doc, open(sys.argv[2], "w"), indent=2, sort_keys=True)
PY
cp "$D/map-m.json" "$D/lane/corpus/evidence/local-sources.json"
python3 -I -B "$G" --root "$D/lane" --rev "$REV" --json > "$R/proposal-bad-members.json" 2>&1
echo "bad-members exit=$?"
cp "$D/map-orig.json" "$D/lane/corpus/evidence/local-sources.json"

echo "### 8. the lane's gate is still untouched (sha256 after)"
sha256sum "$LANE/tools/round-41/local-source-gate.py" | tee "$R/lane-gate-after.txt"
cmp -s "$R/lane-gate-before.txt" "$R/lane-gate-after.txt" && echo "lane-gate-UNCHANGED"

rm -rf "$D"
