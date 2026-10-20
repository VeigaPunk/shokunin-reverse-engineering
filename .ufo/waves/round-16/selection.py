#!/usr/bin/env python3
"""Source-law selection preview for Ghidra's installed Go API snapshot data.

Models the file selection performed by
ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java (source S003,
Base-src.zip member of the installed Ghidra 12.1.4 tree). Mirrors, in order:

  - get() (lines 102-116): base snapshot lookup; EMPTY when absent; the arch
    search order List.of(goOS+"-"+goArch, goOS, unix?"unix":"", goArch, "all")
    at lines 108-109.
  - getApiSnapshotJsonFile() (118-146): base file is always the patch-0 file
    go<major>.<minor>.0.json (122-123); when no patch diff is found the base
    file itself is the result (129-130); otherwise base+diff would be merged
    at runtime (134-144). This preview NEVER merges: patch_applied is always
    false and reported digests are the raw stored bytes.
  - getPatchVerDiffFile() (148-166): scan patchverdiffs/go<M.m.p>.json.diff
    downward from the requested patch, first present wins; patch 0 or no
    present diff => null => base only.
  - getApiSnapshotFile() (168-178): filenames are
    "typeinfo/golang/<subdir>go<M.m.p>.json<suffix>" under the supplied root;
    the getApiFile() (183-192) "goM.m.json" two-part filename fallback is
    intentionally NOT reproduced.
  - IS_GOOS_UNIX set (180-181).

Request parsing is deliberately stricter than GoVer.parse (GoVer.java 62-81):
only a stable "M.m.p" form with three canonical non-negative integer
components is accepted; the two-part shorthand, wildcard patch, trailing
decorations ("1.22.8 X:rangefunc"), pre-release suffixes and leading zeros
are rejected, and (0,0,*) is rejected as INVALID.

Stdlib only; read-only; no target/source execution.
"""

import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

# GoApiSnapshot.java:180-181
IS_GOOS_UNIX = frozenset((
    "aix", "android", "darwin", "dragonfly", "freebsd", "hurd",
    "illumos", "ios", "linux", "netbsd", "openbsd", "solaris",
))

# Strict stable M.m.p: canonical decimal components only, no leading zeros,
# each component fitting a Java int (<= 2147483647). fullmatch is required:
# with $ a trailing newline would still match.
_VERSION_RE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
_JAVA_INT_MAX = 2147483647

# patchverdiffs file names produced by getApiSnapshotFile("%sgo%s.json%s"):
# canonical GoVer.toString() components, no leading zeros.
_DIFF_NAME_RE = re.compile(
    r"go(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.json\.diff")

_PATCH_SUBDIR = "patchverdiffs"


class RequestError(ValueError):
    """Invalid request version or selector arguments (CLI exit 2)."""


class UnreadableError(OSError):
    """Root or selected file is missing/unreadable where reading is required
    (CLI exit 2)."""


def parse_request(request):
    """Parse a strict stable "M.m.p" request into (major, minor, patch).

    Raises RequestError for anything else. Stricter than GoVer.parse: no
    two-part form, no wildcard (-1), no trailing text, no leading zeros, and
    (0,0,*) is rejected as GoVer.INVALID. Components must fit a Java int.
    """
    if not isinstance(request, str):
        raise RequestError("request must be a string")
    m = _VERSION_RE.fullmatch(request)
    if not m:
        raise RequestError(
            "invalid request version %r: expected stable M.m.p" % (request,))
    groups = (m.group(1), m.group(2), m.group(3))
    # Length check BEFORE int(): >10-digit canonical components can never fit
    # a Java int, and int() itself raises ValueError past Python's
    # int-string digit limit (~4300).
    if any(len(g) > 10 for g in groups):
        raise RequestError(
            "invalid request version %r: component exceeds Java int range"
            % (request,))
    major, minor, patch = (int(g) for g in groups)
    if major > _JAVA_INT_MAX or minor > _JAVA_INT_MAX \
            or patch > _JAVA_INT_MAX:
        raise RequestError(
            "invalid request version %r: component exceeds Java int range"
            % (request,))
    if major == 0 and minor == 0:
        # GoVer.isInvalid(): major==0 && minor==0 is the INVALID sentinel.
        raise RequestError(
            "invalid request version %r: 0.0.x is the INVALID sentinel"
            % (request,))
    return major, minor, patch


def arch_search_order(goos, goarch):
    """Effective arch-name search order from GoApiSnapshot.get (108-109).

    The Java list literal contains "" in the unix slot for non-unix GOOS;
    "" is filtered downstream by read() (230-232), so it is dropped here.
    """
    if not isinstance(goos, str) or not goos:
        raise RequestError("goos must be a non-empty string")
    if not isinstance(goarch, str) or not goarch:
        raise RequestError("goarch must be a non-empty string")
    return [name for name in (
        goos + "-" + goarch,
        goos,
        "unix" if goos in IS_GOOS_UNIX else "",
        goarch,
        "all",
    ) if name]


def _describe_file(path, root):
    """Return {path, size, sha256} for a regular file, or None if absent.

    One stat() call decides presence: FileNotFoundError/NotADirectoryError
    (or a non-regular file) mean "not a snapshot file" => None; any other
    OSError (e.g. EACCES) is unreadable input => UnreadableError, matching
    the contract's exit-2 requirement rather than is_file()'s silent False.
    path is reported relative to root (POSIX separators) so output is stable
    across roots.
    """
    try:
        st = path.stat()
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError as e:
        raise UnreadableError("cannot stat %s: %s" % (path, e)) from e
    if not stat.S_ISREG(st.st_mode):
        return None
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    except OSError as e:
        raise UnreadableError("cannot read %s: %s" % (path, e)) from e
    return {
        "path": path.relative_to(root).as_posix(),
        "size": st.st_size,
        "sha256": h.hexdigest(),
    }


def _top_level_keys(path):
    """Return names of top-level base-snapshot buckets with non-null values.

    Mirrors read() (205-240): keys are filtered by the arch-name set
    (218-223), each value is deserialized as GoArch, and the ordered result
    map retains a bucket only when the deserialized GoArch is non-null
    (233-235) — a JSON `"all": null` is therefore NOT a matching bucket.
    This is not a full GoArch schema validation: a non-null non-object value
    (e.g. an array) still counts as present here, a names-only limitation.
    Non-object documents and unparseable JSON raise UnreadableError so the
    bucket preview never claims membership for a document the Java reader
    could not open (read() requires a top-level object).
    """
    try:
        with path.open("rb") as f:
            doc = json.load(f)
    except RecursionError as e:
        # Deeply nested JSON exceeds json.load's recursion budget.
        raise UnreadableError(
            "cannot parse base snapshot %s: recursion limit" % (path,)) from e
    except (OSError, ValueError) as e:
        raise UnreadableError("cannot parse base snapshot %s: %s" % (path, e)) \
            from e
    if not isinstance(doc, dict):
        raise UnreadableError(
            "base snapshot %s is not a JSON object" % (path,))
    return [k for k, v in doc.items() if v is not None]


def select_snapshot(root, request, goos, goarch):
    """Source-law selection preview.

    Args:
        root: pathlib.Path (or str) of the golang typeinfo directory, i.e. the
            directory containing go<M.m.p>.json files and patchverdiffs/.
        request: strict stable "M.m.p" version string.
        goos, goarch: GOOS/GOARCH selector strings.

    Returns a dict with keys: requested, status, base, selected_diff,
    selected_patch, arch_search_order, base_matching_buckets, patch_applied,
    evidence_class; plus informational request_raw, goos, goarch and
    base_matching_buckets_source.

    status is one of: missing_base, base_only, exact_diff, fallback_diff.
    """
    root = Path(root)
    major, minor, patch = parse_request(request)
    order = arch_search_order(goos, goarch)
    normalized = "%d.%d.%d" % (major, minor, patch)

    if not root.is_dir():
        raise UnreadableError("root %s is not a directory" % (root,))

    # getApiSnapshotJsonFile lines 122-123: base is always patch 0.
    base_rel = "go%d.%d.%d.json" % (major, minor, 0)
    base_info = _describe_file(root / base_rel, root)
    if base_info is None:
        # lines 124-126: no base file => GoApiSnapshot.EMPTY.
        return {
            "requested": normalized,
            "request_raw": request,
            "goos": goos,
            "goarch": goarch,
            "status": "missing_base",
            "base": None,
            "selected_diff": None,
            "selected_patch": None,
            "arch_search_order": order,
            "base_matching_buckets": [],
            "base_matching_buckets_source": None,
            "patch_applied": False,
            "evidence_class": "source_model",
        }

    # getPatchVerDiffFile lines 148-166: nearest present diff <= request
    # within the same minor. The Java while-loop only probes when patch > 0
    # (patch==0 exits with null without touching patchverdiffs/), so the
    # listing is skipped for patch 0 entirely. Equivalent to listing once and
    # taking the max canonical same-minor patch <= request, without a
    # per-patch countdown probe. A missing diff directory is the valid "no
    # diffs" case; any other OSError is unreadable input (exit 2).
    diff_info = None
    diff_patch = None
    if patch > 0:
        diff_dir = root / _PATCH_SUBDIR
        try:
            entries = list(diff_dir.iterdir())
        except (FileNotFoundError, NotADirectoryError):
            entries = []
        except OSError as e:
            raise UnreadableError(
                "cannot list %s: %s" % (diff_dir, e)) from e
        candidates = []
        for entry in entries:
            m = _DIFF_NAME_RE.fullmatch(entry.name)
            if m and int(m.group(1)) == major and int(m.group(2)) == minor:
                cand = int(m.group(3))
                if 0 < cand <= patch:
                    candidates.append((cand, entry))
        for cand, entry in sorted(candidates, reverse=True):
            cand_info = _describe_file(entry, root)
            if cand_info is not None:
                diff_info = cand_info
                diff_patch = cand
                break

    # Base top-level buckets matching the arch search order, order-preserved
    # and deduplicated exactly like read()'s LinkedHashMap build (228-237):
    # a Set membership test plus ordered iteration skips "" and repeats.
    keys = set(_top_level_keys(root / base_rel))
    buckets = []
    seen = set()
    for name in order:
        if name in keys and name not in seen:
            buckets.append(name)
            seen.add(name)

    if diff_info is None:
        # lines 128-131: no diff file (patch==0 or none present) => base only.
        status = "base_only"
    elif diff_patch == patch:
        status = "exact_diff"
    else:
        status = "fallback_diff"

    return {
        "requested": normalized,
        "request_raw": request,
        "goos": goos,
        "goarch": goarch,
        "status": status,
        "base": base_info,
        "selected_diff": diff_info,
        # 0 when no diff is selected: the patch-0 base file is the byte source.
        "selected_patch": diff_patch if diff_patch is not None else 0,
        "arch_search_order": order,
        # Buckets are computed on the raw base file even when a diff is
        # selected; the patched document is never constructed.
        "base_matching_buckets": buckets,
        "base_matching_buckets_source": "unpatched_base_file",
        "patch_applied": False,
        "evidence_class": "source_model",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Source-law selection preview of Ghidra's Go API snapshot "
            "files; never applies patches."))
    parser.add_argument("--root", required=True,
                        help="golang typeinfo directory")
    parser.add_argument("--request", required=True,
                        help="stable Go version M.m.p")
    parser.add_argument("--goos", required=True, help="GOOS selector")
    parser.add_argument("--goarch", required=True, help="GOARCH selector")
    args = parser.parse_args(argv)

    try:
        result = select_snapshot(
            Path(args.root), args.request, args.goos, args.goarch)
    except (RequestError, UnreadableError) as e:
        kind = "invalid_request" if isinstance(e, RequestError) \
            else "unreadable_input"
        json.dump({"status": kind, "error": str(e)}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        print("error: %s" % e, file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
