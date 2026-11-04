import importlib.util, os, sys, json
CAND = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-87/w1/ExecRepairCases/candidate/upx-magic-repair.py"
spec = importlib.util.spec_from_file_location("rep", CAND); rep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rep)
n = acc = ph = 0; accepted = []; ph_hits = []; magic_files = 0
for root in ("/usr/bin", "/usr/lib"):
    for f in sorted(os.listdir(root)):
        p = os.path.join(root, f)
        if not os.path.isfile(p) or os.path.islink(p): continue
        try:
            with open(p, "rb") as fh:
                if fh.read(4) != b"\x7fELF": continue
                fh.seek(0); d = fh.read()
        except OSError: continue
        n += 1
        if b"UPX!" in d: magic_files += 1
        try:
            rep.find_packheader(d); ph += 1; ph_hits.append(p)
        except rep.Refused: pass
        try:
            rep.repair(d); acc += 1; accepted.append(p)
        except rep.Refused: pass
print(json.dumps({"elf_files": n, "packheader_window_validates": ph, "repair_accepts": acc,
                  "files_containing_UPX!": magic_files, "accepted": accepted, "ph_hits_sample": ph_hits[:20]}))
