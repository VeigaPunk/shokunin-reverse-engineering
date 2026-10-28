#!/usr/bin/env python3
"""Read-only inventory of merge/kaidoku vs the lane corpus. Writes JSON to stdout."""
import hashlib, json, os, re
from pathlib import Path

PKG = Path("/home/vgpnk/Projects/shokuknow/merge/kaidoku")
LANE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
KW = re.compile(r"squashfs|sasquatch|unblob|avm|firmware|binwalk", re.I)

report = json.loads((PKG / "MERGE-REPORT.json").read_text())
entries = report["entries"]

files = sorted(p.relative_to(PKG).as_posix() for p in PKG.rglob("*") if p.is_file())
knowledge = sorted(
    p.relative_to(PKG).as_posix()
    for p in (PKG / "knowledge").rglob("*.md")
    if p.is_file()
)

lane_know = sorted(p.name for p in (LANE / "corpus" / "knowledge").glob("*.md"))
lane_stems = set()
for name in lane_know:
    stem = name[:-3]
    lane_stems.add(stem)
    # drop a leading date prefix
    m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)", stem)
    if m:
        lane_stems.add(m.group(1))

readme = (LANE / "corpus" / "README.md").read_text(errors="replace")
sources = (LANE / "corpus" / "SOURCES.md").read_text(errors="replace")
lane_ids = sorted(set(re.findall(r"^\| (S\d+) \|", sources, re.M)))
# also indented rows
lane_ids2 = sorted(set(re.findall(r"^\s*\| (S\d+) \|", sources, re.M)))

append = (PKG / "SOURCES.append.md").read_text(errors="replace")
staged_ids = sorted(set(re.findall(r"^\| (S\d+) \|", append, re.M)))
staged_ids_indented = sorted(set(re.findall(r"^\s*\| (S\d+) \|", append, re.M)))

def idn(s):
    return int(s[1:])

lane_set = set(lane_ids2)
staged_set = set(staged_ids_indented or staged_ids)
collisions = sorted(lane_set & staged_set, key=idn)

HELD = {
    "unblob-sasquatch-dependency": "corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md (r36)",
    "unblob-format-matrix": "corpus/knowledge/2026-10-26-unblob-format-matrix.md (r38)",
    "firmware-region-vocabulary": "corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md (r41, renamed)",
    "avm-image-extraction": "absorbed into corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md (r40 lineage)",
    "sasquatch-prebuilt-package-inventory": "corpus/knowledge/2026-10-27-sasquatch-release-matrix.md (r43, re-grounded)",
}

rows = []
missing_files = []
for e in entries:
    target = e["target"]
    stem = Path(target).name[:-3] if target.endswith(".md") else Path(target).name
    staged_path = PKG / "knowledge" / target
    exists = staged_path.is_file()
    if not exists:
        missing_files.append(target)
    text = staged_path.read_text(errors="replace") if exists else ""
    sources_lines = [ln.strip() for ln in text.splitlines() if ln.startswith("source:")]
    local = [ln for ln in sources_lines if "lanes/kaidoku" in ln or ln.startswith("source: S") and "http" not in ln and "://" not in ln]
    https = [ln for ln in sources_lines if "http://" in ln or "https://" in ln]
    overlap = bool(KW.search(stem) or KW.search(e.get("title") or "") or KW.search(text[:2500]))
    name_held = stem in lane_stems or any(stem in n for n in lane_know)
    readme_hit = stem in readme
    rows.append({
        "target": target,
        "staged_file": str(staged_path) if exists else None,
        "bytes": staged_path.stat().st_size if exists else None,
        "round": e.get("round"),
        "kind": e.get("kind"),
        "title": e.get("title"),
        "squashfs_firmware_overlap": overlap,
        "stem_in_lane_knowledge_name": name_held,
        "stem_in_readme": readme_hit,
        "known_held": HELD.get(stem),
        "source_line_count": len(sources_lines),
        "https_source_lines": len(https),
        "campaign_local_source_lines": len(local),
        "first_source": sources_lines[0][:240] if sources_lines else None,
    })

# package tree extras
amend = [f for f in files if f.startswith("amendments/") or "/amend" in f]
v1 = []
for rel in knowledge:
    t = (PKG / rel).read_text(errors="replace")
    if re.search(r"squashfs_v1|squashfs_v2|SquashFS v1|SquashFS v2", t):
        v1.append(rel)

# evidence names
ev_hits = []
ev = LANE / "corpus" / "evidence"
if ev.is_dir():
    for p in ev.rglob("*"):
        if p.is_file() and re.search(r"avm.?le|genuine", p.name, re.I):
            ev_hits.append(str(p.relative_to(LANE)))

tsv = Path("/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv")
consid = LANE / "considerthese"

out = {
    "package_file_count": len(files),
    "package_files": files,
    "knowledge_md_count": len(knowledge),
    "json_entry_count": len(entries),
    "accepted_rows": report.get("accepted"),
    "refused_rows": report.get("refused"),
    "missing_entry_files": missing_files,
    "amendment_paths": amend,
    "v1_v2_mentions": v1,
    "lane_knowledge_count": len(lane_know),
    "lane_source_ids_count": len(lane_set),
    "lane_source_id_min": min(lane_set, key=idn) if lane_set else None,
    "lane_source_id_max": max(lane_set, key=idn) if lane_set else None,
    "staged_source_ids_count": len(staged_set),
    "staged_source_id_min": min(staged_set, key=idn) if staged_set else None,
    "staged_source_id_max": max(staged_set, key=idn) if staged_set else None,
    "id_collision_count": len(collisions),
    "id_collision_min": collisions[0] if collisions else None,
    "id_collision_max": collisions[-1] if collisions else None,
    "considerthese_exists": consid.exists(),
    "avm_le_tsv_exists": tsv.is_file(),
    "avm_le_tsv": str(tsv),
    "evidence_name_hits": ev_hits[:40],
    "overlap_count": sum(1 for r in rows if r["squashfs_firmware_overlap"]),
    "entries": rows,
}
print(json.dumps(out, indent=2))
