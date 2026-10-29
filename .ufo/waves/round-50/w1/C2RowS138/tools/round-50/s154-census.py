#!/usr/bin/env python3
"""S154 grounding census: re-derive the 22-member unblob 26.6.4 squashfs v1/v2 `__output__` census.

Inputs (all public, no credentials):
  --git-census  JSON from `census.py` (git ls-tree of tag 26.6.4 + LFS pointer oid/size + media bytes)
  --listing DIR  GitHub contents-API bodies named `<tree-slug>__<dir>.json` (bodies only; headers stripped)

Checks: every regular file of the four endian `__output__` trees appears in exactly one
`.bin_extract` listing; listing name/sha (git blob) equals the git tree blob; the located quote
for each tree is a `name` field of that tree's listing at the printed JSON path; the sorted
digest `sha256("<oid>  <path>\\n" sorted by path)` reproduces the lane's recorded 21cb3a6a....

Exit 0 when every check holds; 1 on any mismatch; 2 on unreadable input.
"""
import argparse, hashlib, json, os, sys

TREES = ["squashfs_v1/big_endian", "squashfs_v1/little_endian",
         "squashfs_v2/big_endian", "squashfs_v2/little_endian"]
DIGEST_RECORDED = "21cb3a6ab67af507f6b4ccaff15d1990567550355a7a4c21ef4111b9efd660ca"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--git-census", required=True)
    ap.add_argument("--listing", required=True)
    a = ap.parse_args()
    try:
        raw = open(a.git_census).read()
        members = json.loads(raw.split("\n", 4)[4])
    except Exception as e:
        print(f"could-not-evaluate: {e}", file=sys.stderr); return 2
    fails = []
    by_tree = {t: [m for m in members if m["tree"] == t] for t in TREES}
    total = len(members)
    if total != 22: fails.append(f"members {total} != 22")
    # listing bodies
    listing_rows = []
    quotes = {}
    for t in TREES:
        slug = t.replace("/", "_")
        seen = []
        for m in by_tree[t]:
            d = os.path.basename(os.path.dirname(m["path"]))   # e.g. squashfs_v2.0_le.bin_extract
            fn = os.path.join(a.listing, f"{slug}__{d}.json")
            try:
                body = open(fn, "rb").read()
            except OSError as e:
                fails.append(f"missing listing {fn}: {e}"); continue
            names = json.loads(body)
            if not isinstance(names, list):
                fails.append(f"listing {fn} is not a JSON array"); continue
            ent = {e["name"]: e for e in names}
            ok = ent.get(os.path.basename(m["path"]), {}).get("sha") == m["git_blob"]
            if not ok: fails.append(f"blob mismatch {m['path']}")
            seen.append(m["path"])
            listing_rows.append(dict(tree=t, dir=d, file=os.path.basename(m["path"]),
                                     sha256_body=hashlib.sha256(body).hexdigest(),
                                     api_blob_eq_git=ok))
        if len(seen) != len(by_tree[t]): fails.append(f"{t}: listed {len(seen)} of {len(by_tree[t])}")
        # located quote: the last regular file of the tree's first .bin_extract listing (JSON array index)
        first_dir = sorted({os.path.basename(os.path.dirname(m["path"])) for m in by_tree[t]})[0]
        fn = os.path.join(a.listing, f"{slug}__{first_dir}.json")
        arr = json.loads(open(fn, "rb").read())
        idx = len(arr) - 1
        quotes[t] = dict(name=arr[idx]["name"], json_path=f"$[{idx}].name",
                         listing=f"{slug}__{first_dir}.json",
                         listing_sha256=hashlib.sha256(open(fn, "rb").read()).hexdigest())
        if arr[idx]["name"] not in {os.path.basename(m["path"]) for m in by_tree[t]}:
            fails.append(f"quote {t} not a member name")
    digest_src = "".join(f"{m['lfs_oid']}  {m['path']}\n" for m in sorted(members, key=lambda m: m["path"]))
    digest = hashlib.sha256(digest_src.encode()).hexdigest()
    if digest != DIGEST_RECORDED: fails.append(f"sorted digest {digest} != recorded")
    out = dict(members=total, bytes=sum(m["lfs_size"] for m in members),
               distinct_sha256=len({m["lfs_oid"] for m in members}),
               sorted_digest=digest, digest_matches_recorded=digest == DIGEST_RECORDED,
               listings=listing_rows, quotes=quotes, failures=fails)
    print(json.dumps(out, indent=1))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
