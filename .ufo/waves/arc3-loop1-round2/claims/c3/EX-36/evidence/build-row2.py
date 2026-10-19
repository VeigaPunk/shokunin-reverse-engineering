#!/usr/bin/env python3
"""EX-36: build the patched SKILL.md (preamble rewrite + appended custody-pair row), rev 2."""
import hashlib
src = open('SKILL.md','rb').read()
body = src.decode('utf-8').split('\n')[:-1]
assert len(body) == 371, len(body)
assert body[363] == "recovery gate and the citation-drift probe. Neither validates REA correctness,", repr(body[363])
assert body[364] == "outside review, canonical judgment, or fleet acceptance. Evidence and limits:", repr(body[364])
assert body[365].startswith("`corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery."), repr(body[365])
assert body[370].startswith('| citation-drift | probe / kaidoku |'), repr(body[370])
new364 = "recovery gate, the citation-drift probe, and the custody-pair tool — none of"
new365 = "them validates REA correctness, outside review, canonical judgment, or fleet"
new366 = "acceptance. Evidence and limits: " + body[365]
ROW = ("| custody-pair | tool / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]` "
 "— read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and "
 "MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; "
 "the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; `paths` prints the canonical five; "
 "`verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), "
 "11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, "
 "extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT; 2 USAGE (bad args, unreadable or unparsable receipt, "
 "refused write); precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, else 13 with the "
 "receipt still written, and it refuses to write a receipt over a custody path; v1 receipts still compare on their sha256 — a sums-form "
 "v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its "
 "sha256 contract intact (5/5)** | same command with `selftest`; 15 fixture cases — capture/receipt shape/sidecar self-hash, "
 "verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, "
 "TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, refuse-to-write-over-custody-path → 2; scratch root "
 "`$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | "
 "the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing "
 "under the custody paths — files opened for reading only, never renamed, mtime never touched; writes only the requested receipt + its "
 "`.sha256` sidecar (outside the custody set) and, under `selftest`, its isolated fixture root; `--paths` exists for fixture runs only** |")
assert ROW.count('|') == 6, ROW.count('|')
assert '\n' not in ROW
out = body[:363] + [new364, new365, new366] + body[366:] + [ROW]
patched = '\n'.join(out) + '\n'
open('/var/tmp/ex36/SKILL.md.patched','w',encoding='utf-8').write(patched)
def sha(b): return hashlib.sha256(b).hexdigest()
print('orig lines:', len(body), 'sha256:', sha(src))
print('patched lines:', len(out), 'sha256:', sha(patched.encode()))
print('row sha256:', sha(ROW.encode()), 'row chars:', len(ROW))
