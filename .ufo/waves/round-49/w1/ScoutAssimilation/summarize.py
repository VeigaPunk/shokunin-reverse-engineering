#!/usr/bin/env python3
import json
d = json.load(open("/fast/scratch/hyaku/kaidoku-r49/ScoutAssimilation/inventory.json"))
keys = [
    "package_file_count", "knowledge_md_count", "json_entry_count", "accepted_rows",
    "refused_rows", "missing_entry_files", "amendment_paths", "v1_v2_mentions",
    "lane_knowledge_count", "lane_source_ids_count", "lane_source_id_min",
    "lane_source_id_max", "staged_source_ids_count", "staged_source_id_min",
    "staged_source_id_max", "id_collision_count", "id_collision_min",
    "id_collision_max", "considerthese_exists", "avm_le_tsv_exists",
    "overlap_count", "evidence_name_hits",
]
for k in keys:
    print(f"{k}={d[k]}")
print("---OVERLAP---")
for e in d["entries"]:
    if e["squashfs_firmware_overlap"]:
        held = e["known_held"] or ("name" if e["stem_in_lane_knowledge_name"] else "")
        print(
            f"{e['target']}\theld={held}\treadme={e['stem_in_readme']}"
            f"\tlocal_src={e['campaign_local_source_lines']}\thttps={e['https_source_lines']}"
            f"\tbytes={e['bytes']}"
        )
print("---UNHELD---")
n = 0
for e in d["entries"]:
    held = bool(e["known_held"] or e["stem_in_lane_knowledge_name"] or e["stem_in_readme"])
    if not held:
        n += 1
        print(
            f"{e['target']}\toverlap={e['squashfs_firmware_overlap']}"
            f"\tlocal={e['campaign_local_source_lines']}\thttps={e['https_source_lines']}"
            f"\t{e['title']}"
        )
print("unheld_count", n)
print("---PACKAGE_FILES---")
for f in d["package_files"]:
    if not f.startswith("knowledge/"):
        print(f)
