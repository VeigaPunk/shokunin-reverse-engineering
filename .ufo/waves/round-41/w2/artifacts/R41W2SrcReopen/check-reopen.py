#!/usr/bin/env python3
"""R41W2SrcReopen: re-derive every checkable claim of SOURCES rows S127/S128 from
independently fetched AVM bytes.

Usage (scratch S, after the fetches in commands.sh):
  python3 check-reopen.py --sources "$S/SOURCES-e9a24d07.md" --dir "$S" --carriers <lane>/.ufo/waves/round-41/c1/carriers.json

Every check prints PASS/FAIL plus the observed value; exit 1 if any check fails.
No network access: it reads the files the fetch commands saved.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

fails = []


def check(tag, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + tag + ((" | " + detail) if detail else ""))
    if not ok:
        fails.append(tag)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cells_of(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--carriers", required=True)
    a = ap.parse_args()
    D = a.dir

    rows = {}
    for line in open(a.sources, encoding="utf-8").read().split("\n"):
        if line.startswith("| S127 |") or line.startswith("| S128 |"):
            c = cells_of(line)
            rows[c[0]] = c
    check("rows present S127+S128", set(rows) == {"S127", "S128"}, str(sorted(rows)))

    table = {  # row -> facts asserted in the row
        "S127": dict(model="5490", carrier="V3",
                     image_size=33269760, etag=("64f592ae", "1fba800"),
                     info_en=(50653, "e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18"),
                     info_de=(56125, "519e5038d4e28935f6c356333d0d48062e770125b11f2092600486b6b174a5c9"),
                     listing=(574, "88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4"),
                     im_lm="Mon, 04 Sep 2023 08:17:50 GMT",
                     en_lm="Mon, 18 Nov 2024 14:01:57 GMT",
                     improv=29, sig_line=672, sig="DHA 2023/09/04",
                     lic=(663, 670), utf8_fail=17974, image_sha=None),
        "S128": dict(model="5491", carrier="V4",
                     image_size=36392960, etag=("64f5a91e", "22b5000"),
                     info_en=(53166, "ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4"),
                     info_de=(47098, "dc663791cbb0499e69d0be097a844ed105772c2c7ad8e33d6e9b8397292c745e"),
                     listing=(574, "badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7"),
                     im_lm="Mon, 04 Sep 2023 09:53:34 GMT",
                     en_lm="Mon, 18 Nov 2024 14:01:04 GMT",
                     improv=30, sig_line=695, sig="HKR 2021/11/17",
                     lic=(686, 693), utf8_fail=None, image_sha=None),
    }

    for rid, t in table.items():
        row = rows[rid]
        d = os.path.join(D, "s127" if t["model"] == "5490" else "s128")
        pref = rid + " "

        # --- shape / registry columns -------------------------------------
        check(pref + "11 cells", len(row) == 11, "cells=%d" % len(row))
        raw = "\n".join(l for l in open(a.sources, encoding="utf-8").read().split("\n")
                        if l.startswith("| %s |" % rid))
        check(pref + "12 pipes", raw.count("|") == 12, "pipes=%d" % raw.count("|"))
        check(pref + "kind=dataset", row[2] == "dataset", row[2])
        check(pref + "tier=A", row[3] == "A", row[3])
        check(pref + "status=mined", row[7] == "mined", row[7])
        check(pref + "recheck=180d", row[9] == "180d", row[9])
        check(pref + "used-by names round-41 entry",
              row[10] == "corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md", row[10])
        check(pref + "URL is the 549x fritz.os directory",
              ("fritzbox-%s/other/fritz.os/" % t["model"]) in row[1], row[1].split(" — ")[1][:70])

        # --- listing ------------------------------------------------------
        lb = open(os.path.join(d, "listing.html"), "rb").read()
        check(pref + "listing size %d" % t["listing"][0], len(lb) == t["listing"][0], str(len(lb)))
        check(pref + "listing sha256", sha(lb) == t["listing"][1], sha(lb))
        txt = lb.decode()
        imgs = re.findall(r'href="([^"]+\.image)"', txt)
        check(pref + "listing has exactly one .image entry", len(imgs) == 1, str(imgs))
        check(pref + "image name FRITZ.Box_%s-07.31.image" % t["model"],
              imgs == ["FRITZ.Box_%s-07.31.image" % t["model"]], str(imgs))
        m = re.search(r'href="(FRITZ\.Box_[^"]+\.image)"[^>]*>\S+</a>\s+(\S+ \S+)\s+(\d+)', txt)
        check(pref + "listing image size %d" % t["image_size"], m and int(m.group(3)) == t["image_size"],
              m.group(3) if m else "no match")
        check(pref + "listing image mtime in row's Last-Modified date",
              m and m.group(2).startswith("04-Sep-2023"), m.group(2) if m else "-")
        for f, claimed in (("info_en.txt", t["info_en"]), ("info_de.txt", t["info_de"])):
            mm = re.search(r'href="%s"[^>]*>\S+</a>\s+(\S+ \S+)\s+(\d+)' % f, txt)
            check(pref + "listing %s size %d" % (f, claimed[0]),
                  mm and int(mm.group(2)) == claimed[0], mm.group(2) if mm else "no match")

        # --- info files ---------------------------------------------------
        for f in ("info_en.txt", "info_de.txt"):
            b = open(os.path.join(d, f), "rb").read()
            want = t["info_en"] if f == "info_en.txt" else t["info_de"]
            check(pref + "%s size %d" % (f, want[0]), len(b) == want[0], str(len(b)))
            check(pref + "%s sha256" % f, sha(b) == want[1], sha(b[:0]) or sha(b))
            check(pref + "%s CRLF only" % f,
                  b.count(b"\r\n") > 0 and b.count(b"\n") == b.count(b"\r\n"),
                  "crlf=%d barelf=%d" % (b.count(b"\r\n"), b.count(b"\n") - b.count(b"\r\n")))
            try:
                b.decode("utf-8")
                ok = False
                det = "strict UTF-8 decodes (claim says it must not)"
            except UnicodeDecodeError as e:
                ok = True
                det = "strict UTF-8 fails at byte %d" % e.start
            if f == "info_en.txt" and t["utf8_fail"] is not None:
                ok = ok and det.endswith(str(t["utf8_fail"]))
            check(pref + "%s not UTF-8 (Latin-1 text)" % f, ok, det)

        en = open(os.path.join(d, "info_en.txt"), "rb").read().decode("latin-1").split("\r\n")
        de = open(os.path.join(d, "info_de.txt"), "rb").read().decode("latin-1").split("\r\n")

        # --- quoted lines -------------------------------------------------
        check(pref + 'info_en L8 "Product: FRITZ!Box %s"' % t["model"],
              en[7].replace("\t", " ").strip() == "Product: FRITZ!Box %s" % t["model"], en[7])
        check(pref + 'info_en L10 "Version: FRITZ!OS 7.31"',
              "FRITZ!OS 7.31" in en[9], en[9])
        check(pref + 'info_en L14 "Release date: 09/04/2023"',
              "Release date:" in en[13] and "09/04/2023" in en[13], en[13])
        check(pref + 'info_en L%d "# Further Improvements of FRITZ!OS 7.31"' % t["improv"],
              en[t["improv"] - 1].strip() == "# Further Improvements of FRITZ!OS 7.31",
              en[t["improv"] - 1])
        check(pref + "info_en L%d signature %r" % (t["sig_line"], t["sig"]),
              en[t["sig_line"] - 1].strip().rstrip(".") == t["sig"], en[t["sig_line"] - 1])
        lo, hi = t["lic"]
        block = " ".join(en[lo - 1:hi])
        check(pref + "info_en L%d-%d licence notice (no redistribution / no reverse engineering)" % (lo, hi),
              "reverse engineered" in block and "propagated" in block, block[:60] + "...")
        check(pref + 'info_de L14 "Release-Datum: 04.09.2023"',
              "Release-Datum:" in de[13] and "04.09.2023" in de[13], de[13])
        check(pref + "info_en L1 names only the xx.xx template image",
              "FRITZ.Box_%s-xx.xx.image" % t["model"] in en[0], en[0][:70])
        joined = " ".join(en) + " " + " ".join(de)
        check(pref + "no Build number in either info file",
              "build" not in joined.lower(), "occurrences=%d" % joined.lower().count("build"))
        check(pref + "no SquashFS/filesystem layout claim in either info file",
              "squash" not in joined.lower() and "filesystem" not in joined.lower(),
              "squash=%d filesystem=%d" % (joined.lower().count("squash"), joined.lower().count("filesystem")))

        # --- image HEAD / ETag arithmetic --------------------------------
        hdr = open(os.path.join(d, "image.head"), "rb").read().decode("latin-1")
        cl = int(re.search(r"(?i)content-length:\s*(\d+)", hdr).group(1))
        et = re.search(r'(?i)etag:\s*"([0-9a-f]+)-([0-9a-f]+)"', hdr)
        lm = re.search(r"(?i)last-modified:\s*(.+)", hdr).group(1).strip()
        check(pref + "image HEAD content-length %d" % t["image_size"], cl == t["image_size"], str(cl))
        check(pref + "image HEAD ETag %s-%s" % t["etag"], (et.group(1), et.group(2)) == t["etag"], et.group(0))
        check(pref + "ETag size field == Content-Length", int(et.group(2), 16) == cl,
              "%d vs %d" % (int(et.group(2), 16), cl))
        check(pref + "ETag mtime field == Last-Modified",
              datetime.datetime.fromtimestamp(int(et.group(1), 16), datetime.UTC)
              .strftime("%a, %d %b %Y %H:%M:%S GMT") == lm, lm)
        check(pref + "image Last-Modified as recorded", lm == t["im_lm"], lm)
        en_lm = re.search(r"(?i)last-modified:\s*(.+)",
                          open(os.path.join(d, "info_en.hdr"), "rb").read().decode("latin-1")).group(1).strip()
        check(pref + "info_en Last-Modified as recorded", en_lm == t["en_lm"], en_lm)

        # --- second fetch stability --------------------------------------
        for f, second in (("info_en.txt", "info_en.2.txt"), ("listing.html", "listing.2.html")):
            p = os.path.join(d, second)
            if os.path.exists(p):
                check(pref + "second fetch byte-identical: " + f,
                      open(p, "rb").read() == open(os.path.join(d, f), "rb").read(), second)
            else:
                print("SKIP " + pref + "second fetch for " + f + " (file absent)")

    # --- carrier binding: vendor image sha256 == the lane's carrier pin ----
    car = json.load(open(a.carriers))
    pin = {c["id"]: (c.get("external") or {}).get("image_sha256") for c in car["carriers"]}
    dig = {}
    for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "vendor-image-digests.txt"), encoding="utf-8"):
        parts = line.split()
        if len(parts) == 2 and parts[1].endswith(".bin"):
            dig[parts[1]] = parts[0]
        elif len(parts) == 2 and parts[1].isdigit():
            pass
    sizes = {}
    for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "vendor-image-digests.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) == 2 and p[1].isdigit():
            sizes[p[0]] = int(p[1])
    check("V3 vendor image sha256 == carriers.json image_sha256",
          dig.get("img-5490.bin") == pin.get("V3"),
          "%s vs %s" % (dig.get("img-5490.bin"), pin.get("V3")))
    check("V4 vendor image sha256 == carriers.json image_sha256",
          dig.get("img-5491.bin") == pin.get("V4"),
          "%s vs %s" % (dig.get("img-5491.bin"), pin.get("V4")))
    check("V3 downloaded size == listing size 33269760", sizes.get("img-5490.bin") == 33269760,
          str(sizes.get("img-5490.bin")))
    check("V4 downloaded size == listing size 36392960", sizes.get("img-5491.bin") == 36392960,
          str(sizes.get("img-5491.bin")))

    print("\n%d checks failed" % len(fails))
    if fails:
        for f in fails:
            print("  - " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
