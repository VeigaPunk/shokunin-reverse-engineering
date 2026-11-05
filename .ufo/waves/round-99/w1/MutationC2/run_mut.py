import os, subprocess, json, shutil, sys
from concurrent.futures import ThreadPoolExecutor
S = "/fast/scratch/hyaku/kaidoku-r99/MutationC2"
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE = L + "/.ufo/waves/round-99/w1/MutationC2"
REV = "01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f"
src = subprocess.run(["git", "-C", L, "show", REV + ":tools/round-99/upx-pe-repair.py"],
                     capture_output=True, text=True, check=True).stdout
for sub in ("mut", "rcpt", "work"):
    os.makedirs(f"{S}/{sub}", exist_ok=True)
os.makedirs(WAVE + "/mutants", exist_ok=True)
os.makedirs(WAVE + "/receipts", exist_ok=True)

M = [
 ("M00", "control: unmutated L", []),
 ("M01", "drop ALIGN_UP in truncation end", [('end = (last["rptr"] + last["rsize"] + falign - 1) // falign * falign', 'end = last["rptr"] + last["rsize"]')]),
 ("M02", "truncation test < -> <=", [("if len(b) < end:", "if len(b) <= end:")]),
 ("M03", "last header = section 0", [('last = secs[-1]', 'last = secs[0]')]),
 ("M04", "last header = max raw end", [('last = secs[-1]', 'last = max(secs, key=lambda s: s["rptr"] + s["rsize"])')]),
 ("M05", "drop filealign-zero refusal", [('raise Refuse("filealign-zero")', 'pass')]),
 ("M06", "FileAlignment read at SectionAlignment offset", [('falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]', 'falign = struct.unpack_from("<I", b, pe + 24 + 32)[0]')]),
 ("M07", "drop output-is-directory refusal", [('return refuse("output-is-directory", a.json)', 'pass')]),
 ("M08", "fixed temp name instead of mkstemp", [('fd, tmp = tempfile.mkstemp(dir=outdir, prefix=os.path.basename(a.out) + ".tmp-")', 'tmp = os.path.join(outdir, os.path.basename(a.out) + ".tmp"); fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)')]),
 ("M09", "drop PackHeader uniqueness (min of candidates)", [("if len(found) != 1:", "if not found:"), ("return found.pop()", "return min(found)")]),
 ("M10", "drop PackHeader checksum validation", [("if sum(h[4:31]) % 251 != h[31]:", "if False:")]),
 ("M11", "gate window start rptr-63", [('(secs[1]["rptr"] - 64, secs[2]["rptr"])', '(secs[1]["rptr"] - 63, secs[2]["rptr"])')]),
 ("M12", "scan window one byte short (+1023)", [("max(0, s) + 1024):", "max(0, s) + 1023):")]),
 ("M13", "too-few-sections bound n<3 -> n<2", [("if n < 3 or st + 40 * n > len(b):", "if n < 2 or st + 40 * n > len(b):")]),
 ("M14", "drop chmod 0644 on output", [("os.chmod(tmp, 0o644)", "pass")]),
 ("M15", "drop fsync of output", [("os.fsync(fh.fileno())", "pass")]),
 ("M16", "drop PackHeader magic rewrite", [("b[i:i + 4] = MAGIC", "pass")]),
 ("M17", "section 2 always UPX2 (no .rsrc branch)", [('want = b".rsrc" if rsrc_rva and inside else b"UPX2"', 'want = b"UPX2"')]),
 ("M18", "resource dir offset 96 for PE32+ too", [("(96 if magic == 0x10B else 112)", "96")]),
 ("M19", "drop c_len <= file size check", [("return 0 < c_len < u_len and c_len <= len(b)", "return 0 < c_len < u_len")]),
 ("M20", "drop truncation refusal", [("if len(b) < end:", "if False:")]),
 ("M21", "version upper bound 14 -> 15", [("not 10 <= version <= 14", "not 10 <= version <= 15")]),
 ("M22", "drop PackHeader bounds check", [("if i < 0 or i + PH_LEN > len(b):", "if i < 0:")]),
 ("M23", "c_len < u_len -> <=", [("0 < c_len < u_len", "0 < c_len <= u_len")]),
 ("M24", "skip UPX-name repair of sections 0/1", [('if not secs[k]["name"].startswith(b"UPX"):', "if False:")]),
 ("M25", "skip section-2 rename", [('if not (s2["name"].rstrip(b"\\0") == b".rsrc" or s2["name"].startswith(b"UPX2")):', "if False:")]),
]


def score(mid, desc, subs):
    d = f"{S}/m/{mid}"
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", L, d], check=True)
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", REV], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    text = src
    for old, new in subs:
        n = text.count(old)
        assert n == 1, (mid, old, n)
        text = text.replace(old, new)
    with open(f"{d}/tools/round-99/upx-pe-repair.py", "w") as fh:
        fh.write(text)
    with open(f"{S}/mut/{mid}.py", "w") as fh:
        fh.write(text)
    shutil.copyfile(f"{S}/mut/{mid}.py", f"{WAVE}/mutants/{mid}.py")
    pc = subprocess.run(["python3", "-I", "-B", "-c", "import ast,sys; ast.parse(open(sys.argv[1]).read())", f"{S}/mut/{mid}.py"], capture_output=True, text=True)
    jout = f"{S}/rcpt/{mid}.json"
    if os.path.exists(jout):
        os.unlink(jout)
    W = f"{S}/work/{mid}"
    p = subprocess.run(["python3", "-I", "-B", f"{d}/tools/round-99/pe-upx-trunc-battery.py", "--root", d,
                        "--repair", "tools/round-99/upx-pe-repair.py", "--rev", "worktree", "--work", W, "--json-out", jout],
                       capture_output=True, text=True, timeout=3000)
    lab = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    rc = json.load(open(jout)) if os.path.exists(jout) else {}
    if os.path.exists(jout):
        shutil.copyfile(jout, f"{WAVE}/receipts/{mid}.json")
    shutil.rmtree(W, ignore_errors=True)
    r = {"id": mid, "desc": desc, "compiles": pc.returncode == 0, "exit": p.returncode,
         "label": lab, "met": rc.get("met"), "repair_sha256": rc.get("repair_sha256", "")[:12],
         "stderr": p.stderr[-200:]}
    print(json.dumps(r), flush=True)
    return r


with ThreadPoolExecutor(max_workers=3) as ex:
    res = list(ex.map(lambda t: score(*t), M))
json.dump(res, open(f"{S}/summary.json", "w"), indent=1)
shutil.copyfile(f"{S}/summary.json", f"{WAVE}/summary.json")
print("DONE", flush=True)
