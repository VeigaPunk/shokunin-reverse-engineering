#!/usr/bin/env python3
"""Read-only inventory of installed Ghidra Go API snapshot resources (round 15 C1).

Inventories the installed Base module data directory
`Ghidra/Features/Base/data/typeinfo/golang`:

  go<major>.<minor>.<patch>.json          base snapshots
  patchverdiffs/go<major>.<minor>.<patch>.json.diff
                                          jd patch diffs applied to the
                                          matching `<major>.<minor>.0` base

For every base JSON the script records filename, absolute path, byte size,
SHA-256, and the parsed top-level structure: sorted top-level container keys
(the GoApiSnapshot OS/architecture/feature map keys) with each container's
field names and `Funcs` / `Types` entry counts. Each base entry also carries an
`all_bucket` summary with the `all` container's `Funcs` / `Types` counts.

For every patch diff it records filename, absolute path, byte size, SHA-256,
the numeric patch component (`patch`), and the parsed top-level structure
(`patch_structure`): number of `@ [path]` sections, per-container section
counts, and `+ ` / `- ` line counts. Diffs are parsed, never applied.

A selection list (default `1.25.0` and `1.26.0`) reports, explicitly for each
requested version: base filename/presence/path/size/digest, the base's OS/arch
map keys, every patch diff present for that major.minor, and whether the exact
patch diff filename exists. Absent entries are reported as explicit `false` /
`null`, never inferred.

For each selected version whose base JSON is present, `bootstrap_types` reports
the two non-primitive bootstrap definitions `runtime.moduledata` and
`runtime.pcHeader` by top-level container key: presence, container list, field
counts, entry key names, a canonical SHA-256 of each entry, and the exact parsed
`Types` entry per container. Only these two named entries are copied; the full
`Types`/`Funcs` maps are never dumped.

OUTPUT
  One deterministic JSON document on stdout (`sort_keys=True`, no timestamps,
  absolute paths). Lists are version-ordered.

EXIT
  0  inventory complete
  2  could not evaluate: unusable --ghidra root, missing/ambiguous resource
     directory, invalid --select token, unreadable/undecodable file, malformed
     base JSON or diff header. A JSON document is still emitted with `errors`.

LIMITS
  - Presence, sizes and digests are filename/byte observations only. They are
    not a statement that a version is supported, compatible, or sufficient.
  - `json` parsing does not report duplicate object keys.
  - Patch diffs are not applied; section/line counts are structural metadata.
  - Only non-symlink regular directory entries are read; other matching entries
    are reported under `skipped_non_regular` and excluded.
  - No network, subprocess, Ghidra launch, target/provider execution, or write.
"""
import argparse
import functools
import hashlib
import json
import os
import re
import stat
import sys

DEFAULT_GHIDRA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
RESOURCE_REL = ("Ghidra", "Features", "Base", "data", "typeinfo", "golang")
DEFAULT_SELECT = ("1.25.0", "1.26.0")

BASE_RE = re.compile(r"^go(\d+)\.(\d+)\.(\d+)\.json$")
DIFF_RE = re.compile(r"^go(\d+)\.(\d+)\.(\d+)\.json\.diff$")
VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$")

BOOTSTRAP_TYPES = ("runtime.moduledata", "runtime.pcHeader")

SCHEMA = "kaidoku-go-snapshot-inventory-v1"

LIMITS = [
    "Read-only bytes/structure inventory; no patch application and no Ghidra execution.",
    "Presence, size and digest are observations, not version support or recovery evidence.",
    "Digest and parsed structure come from one read of each file.",
    "Base JSON uses Python json parsing; duplicate object keys are not reported and non-finite constants are rejected.",
    "Diff '@ ' paths and '+ ' / '- ' line prefixes are counted; patch semantics are not validated.",
    "Matching entries are opened once with O_NOFOLLOW and accepted only if fstat reports a regular file.",
    "Directory path components are not symlink-checked; resource_dir_realpath is reported.",
    "Only the installed Base module data directory is inspected.",
    "bootstrap_types copies only runtime.moduledata and runtime.pcHeader; full Types/Funcs maps are never dumped.",
    "Diff section/line counts are structural only; JsonPatch validity and '+ ' value semantics are not evaluated.",
]


def file_version(filename, regex):
    match = regex.match(filename)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def reject_constant(text):
    raise ValueError("non-finite JSON constant %r is not accepted" % text)


def read_regular(path):
    flags = os.O_RDONLY
    for name in ("O_CLOEXEC", "O_NOFOLLOW", "O_NONBLOCK"):
        if hasattr(os, name):
            flags |= getattr(os, name)
    descriptor = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise OSError("not a regular file: %s" % path)
        chunks = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def canonical_digest(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_base(path, filename, errors, selected_minors):
    entry = {
        "filename": filename,
        "path": path,
        "size": None,
        "sha256": None,
        "top_level": None,
    }
    version = file_version(filename, BASE_RE)
    entry["major"], entry["minor"], entry["patch"] = version
    entry["version"] = "%d.%d.%d" % version
    try:
        raw = read_regular(path)
    except OSError as exc:
        errors.append({"kind": "read_error", "path": path, "detail": str(exc)})
        return entry
    entry["size"] = len(raw)
    entry["sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        document = json.loads(raw, parse_constant=reject_constant)
    except (ValueError, RecursionError) as exc:
        errors.append({"kind": "base_parse_error", "path": path, "detail": str(exc)})
        return entry
    if not isinstance(document, dict):
        errors.append({
            "kind": "base_shape_error",
            "path": path,
            "detail": "top-level JSON value is %s, expected object" % type(document).__name__,
        })
        return entry

    keys = sorted(document)
    containers = {}
    for key in keys:
        value = document[key]
        if not isinstance(value, dict):
            errors.append({
                "kind": "container_shape_error",
                "path": path,
                "detail": "container %r is %s, expected object" % (key, type(value).__name__),
            })
            containers[key] = {"fields": None, "funcs": None, "types": None}
            continue
        fields = sorted(value)
        funcs = value.get("Funcs")
        types = value.get("Types")
        containers[key] = {
            "fields": fields,
            "funcs": len(funcs) if isinstance(funcs, dict) else None,
            "types": len(types) if isinstance(types, dict) else None,
        }
    entry["top_level"] = {
        "key_count": len(keys),
        "keys": keys,
        "containers": containers,
    }
    all_container = document.get("all")
    entry["all_bucket"] = {
        "present": isinstance(all_container, dict),
        "funcs": (len(all_container.get("Funcs"))
                  if isinstance(all_container, dict)
                  and isinstance(all_container.get("Funcs"), dict) else None),
        "types": (len(all_container.get("Types"))
                  if isinstance(all_container, dict)
                  and isinstance(all_container.get("Types"), dict) else None),
    }

    if (entry["major"], entry["minor"]) in selected_minors:
        bootstrap = {}
        for type_name in BOOTSTRAP_TYPES:
            hits = []
            for key in keys:
                container = document[key]
                types = container.get("Types") if isinstance(container, dict) else None
                if isinstance(types, dict) and type_name in types:
                    hits.append((key, types[type_name]))
            bootstrap[type_name] = {
                "present": bool(hits),
                "container_count": len(hits),
                "containers": [key for key, _ in hits],
                "field_counts": {
                    key: (len(value.get("Fields"))
                          if isinstance(value, dict) and isinstance(value.get("Fields"), list)
                          else None)
                    for key, value in hits
                },
                "entry_keys": {
                    key: (sorted(value) if isinstance(value, dict) else None)
                    for key, value in hits
                },
                "entry_sha256": {
                    key: canonical_digest(value) for key, value in hits
                },
                "entries": {key: value for key, value in hits},
            }
        entry["bootstrap_types"] = bootstrap
    return entry


def parse_diff(path, filename, errors):
    entry = {
        "filename": filename,
        "path": path,
        "size": None,
        "sha256": None,
    }
    version = file_version(filename, DIFF_RE)
    entry["major"], entry["minor"], entry["patch"] = version
    entry["version"] = "%d.%d.%d" % version
    try:
        raw = read_regular(path)
    except OSError as exc:
        errors.append({"kind": "read_error", "path": path, "detail": str(exc)})
        return entry
    entry["size"] = len(raw)
    entry["sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        lines = raw.decode("utf-8").split("\n")
    except UnicodeDecodeError as exc:
        errors.append({"kind": "diff_parse_error", "path": path, "detail": str(exc)})
        return entry

    sections = 0
    added = 0
    removed = 0
    container_counts = {}
    for line_number, line in enumerate(lines, 1):
        if line.startswith("@ "):
            try:
                path_array = json.loads(line[2:], parse_constant=reject_constant)
            except (ValueError, RecursionError) as exc:
                errors.append({
                    "kind": "diff_header_error",
                    "path": path,
                    "detail": "line %d: %s" % (line_number, exc),
                })
                continue
            if (not isinstance(path_array, list) or not path_array
                    or not isinstance(path_array[0], str)):
                errors.append({
                    "kind": "diff_header_error",
                    "path": path,
                    "detail": "line %d: header is not a non-empty array with a string root"
                              % line_number,
                })
                continue
            sections += 1
            root = path_array[0]
            container_counts[root] = container_counts.get(root, 0) + 1
        elif line.startswith("+ "):
            added += 1
        elif line.startswith("- "):
            removed += 1
    entry["patch_structure"] = {
        "section_count": sections,
        "container_key_counts": container_counts,
        "added_line_count": added,
        "removed_line_count": removed,
    }
    return entry


def scan_directory(directory, regex, parser, errors):
    entries = []
    skipped = []
    unrecognized = []
    try:
        with os.scandir(directory) as iterator:
            listing = list(iterator)
    except OSError as exc:
        errors.append({"kind": "directory_error", "path": directory, "detail": str(exc)})
        return entries, skipped, unrecognized

    for dir_entry in sorted(listing, key=lambda item: item.name):
        if regex.match(dir_entry.name) is None:
            unrecognized.append(dir_entry.name)
            continue
        try:
            is_regular = dir_entry.is_file(follow_symlinks=False)
        except OSError as exc:
            errors.append({
                "kind": "stat_error",
                "path": os.path.join(directory, dir_entry.name),
                "detail": str(exc),
            })
            continue
        if not is_regular:
            skipped.append(dir_entry.name)
            continue
        entries.append(parser(
            os.path.join(directory, dir_entry.name),
            dir_entry.name,
            errors,
        ))
    entries.sort(key=lambda item: (item["major"], item["minor"], item["patch"]))
    return entries, sorted(skipped), sorted(unrecognized)


def parse_selection(tokens):
    requested = []
    seen = set()
    for token in tokens:
        version = parse_selection_token(token)
        if version not in seen:
            seen.add(version)
            requested.append((token, version))
    return requested


def parse_selection_token(token):
    text = token.strip()
    if text.startswith("go"):
        text = text[2:]
    for suffix in (".json.diff", ".json"):
        if text.endswith(suffix):
            text = text[:-len(suffix)]
            break
    match = VERSION_RE.match(text)
    if match is None:
        raise ValueError("invalid version token: %r" % token)
    major, minor, patch = match.groups()
    return (int(major), int(minor), int(patch) if patch is not None else 0)


def build_selection(requested, base_by_minor, diffs_by_minor, diff_filenames):
    entries = []
    for token, (major, minor, patch) in requested:
        base_filename = "go%d.%d.0.json" % (major, minor)
        base_entry = base_by_minor.get((major, minor))
        exact_diff_filename = "go%d.%d.%d.json.diff" % (major, minor, patch)
        minor_diffs = diffs_by_minor.get((major, minor), [])
        entries.append({
            "requested": token,
            "major": major,
            "minor": minor,
            "patch": patch,
            "base_filename": base_filename,
            "base_present": base_entry is not None,
            "base_path": base_entry["path"] if base_entry else None,
            "base_size": base_entry["size"] if base_entry else None,
            "base_sha256": base_entry["sha256"] if base_entry else None,
            "top_level_container_count": (
                base_entry["top_level"]["key_count"]
                if base_entry and base_entry["top_level"] else None
            ),
            "os_arch_map_keys": (
                base_entry["top_level"]["keys"]
                if base_entry and base_entry["top_level"] else None
            ),
            "patch_diffs_for_minor": [
                name for name in sorted(minor_diffs, key=lambda name: file_version(name, DIFF_RE))
            ],
            "exact_patch_diff_filename": exact_diff_filename,
            "exact_patch_diff_present": exact_diff_filename in diff_filenames,
            "all_bucket": (
                base_entry.get("all_bucket") if base_entry else None
            ),
            "bootstrap_types": (
                base_entry.get("bootstrap_types") if base_entry else None
            ),
        })
    return {"requested": [token for token, _ in requested], "entries": entries}


def resource_directory(root, errors):
    canonical = os.path.join(root, *RESOURCE_REL)
    if os.path.isdir(canonical):
        return canonical, "canonical", [canonical]
    errors.append({
        "kind": "resource_dir_missing",
        "path": canonical,
        "detail": "expected Base module data directory is absent or not a directory",
    })
    return None, "missing", []


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only inventory of installed Ghidra Go API snapshot JSON resources.")
    parser.add_argument(
        "--ghidra",
        default=DEFAULT_GHIDRA,
        metavar="ROOT",
        help="Ghidra installation root (default: %(default)s)")
    parser.add_argument(
        "--select",
        nargs="+",
        default=list(DEFAULT_SELECT),
        metavar="VERSION",
        help="versions whose base presence and map keys are reported "
             "(default: %s)" % " ".join(DEFAULT_SELECT))
    args = parser.parse_args(argv)

    root = os.path.abspath(os.path.expanduser(args.ghidra))
    document = {
        "schema": SCHEMA,
        "ghidra_root": root,
        "resource_dir": None,
        "resource_dir_realpath": None,
        "resource_discovery": None,
        "resource_dir_candidates": [],
        "base_json": {"count": 0, "files": []},
        "patch_diffs": {"count": 0, "files": []},
        "patch_diff_histogram": {},
        "patch_diff_dir_present": None,
        "selection": {"requested": [], "entries": []},
        "skipped_non_regular": [],
        "unrecognized_files": [],
        "limits": LIMITS,
        "errors": [],
    }
    errors = document["errors"]

    try:
        requested = parse_selection(args.select)
    except ValueError as exc:
        requested = []
        errors.append({
            "kind": "select_token_error",
            "path": None,
            "detail": str(exc),
        })
    selected_minors = {(major, minor) for _, (major, minor, _) in requested}

    directory = None
    if not os.path.isdir(root):
        errors.append({
            "kind": "ghidra_root_missing",
            "path": root,
            "detail": "not a directory",
        })
    else:
        directory, discovery, candidates = resource_directory(root, errors)
        document["resource_dir"] = directory
        document["resource_dir_realpath"] = (
            os.path.realpath(directory) if directory else None)
        document["resource_discovery"] = discovery
        document["resource_dir_candidates"] = candidates

    if directory is not None:
        base_entries, skipped, unrecognized = scan_directory(
            directory, BASE_RE,
            functools.partial(parse_base, selected_minors=selected_minors),
            errors)
        diff_dir = os.path.join(directory, "patchverdiffs")
        if os.path.isdir(diff_dir):
            diff_entries, diff_skipped, diff_unrecognized = scan_directory(
                diff_dir, DIFF_RE, parse_diff, errors)
            document["patch_diff_dir_present"] = True
        else:
            diff_entries, diff_skipped, diff_unrecognized = [], [], []
            document["patch_diff_dir_present"] = False
        document["base_json"] = {"count": len(base_entries), "files": base_entries}
        document["patch_diffs"] = {"count": len(diff_entries), "files": diff_entries}
        histogram = {}
        for entry in diff_entries:
            label = "%d.%d" % (entry["major"], entry["minor"])
            histogram[label] = histogram.get(label, 0) + 1
        document["patch_diff_histogram"] = histogram
        document["skipped_non_regular"] = sorted(skipped + diff_skipped)
        document["unrecognized_files"] = sorted(unrecognized + diff_unrecognized)

        base_by_minor = {}
        for entry in base_entries:
            base_by_minor.setdefault((entry["major"], entry["minor"]), entry)
        diffs_by_minor = {}
        diff_filenames = set()
        for entry in diff_entries:
            diffs_by_minor.setdefault((entry["major"], entry["minor"]), []).append(
                entry["filename"])
            diff_filenames.add(entry["filename"])

        document["selection"] = build_selection(
            requested, base_by_minor, diffs_by_minor, diff_filenames)

    # Emit even on failure so the caller gets a deterministic, inspectable document.
    json.dump(document, sys.stdout, indent=2, sort_keys=True, allow_nan=False)
    sys.stdout.write("\n")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
