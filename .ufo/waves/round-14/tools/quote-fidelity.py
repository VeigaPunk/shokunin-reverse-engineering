#!/usr/bin/env python3
"""quote-fidelity gate (round 14, C2).

Verifies that every manifest quote is a located, contiguous, <=25-word excerpt
of a locally captured source. The gate is read-only: no network, no subprocess,
no writes outside the self-test's TemporaryDirectory.

VERDICT
  exit 0 clean, 1 failed, 2 could-not-evaluate.

USAGE
  quote-fidelity.py --manifest PATH
  quote-fidelity.py --frozen EXPECTED.json
  quote-fidelity.py --selftest

MANIFEST
  {"sources": {ID: {"path": REL, "sha256": HEX64}},
   "quotes": [{"id": ID, "source": SRC, "section": SEC, "quote": TEXT}]}
  Paths are relative to the manifest file and must resolve inside its directory.
  Duplicate JSON keys, duplicate quote ids, unknown sources, empty sources or
  empty quotes are invalid_manifest. Every declared source is hashed before any
  quote is graded; only after all digests match are quotes evaluated.

SECTION
  Markdown ATX selector: the literal heading line including '#', trailing
  whitespace trimmed, e.g. "## Usage". An HTML h1..h6 element on one line is
  selected either by its visible label (attributes and inline tags stripped,
  entities decoded, whitespace collapsed, e.g. "Introduction") or by its literal
  trimmed element line, e.g. "<h1 class=\"wp-block-heading\">Introduction</h1>".
  Both forms are compared by exact string equality, never substring. The body
  runs to the next heading of the same or higher level. ATX-looking lines inside
  ```/~~~ fences are ignored.

QUOTE
  An exact contiguous substring of the section body; no whitespace, tag or
  punctuation normalization is applied to the quote or the source.

FINDINGS
  quote_too_long            more than 25 whitespace-separated words
  quote_not_contiguous      quote absent from the whole source
  quote_location_mismatch   section absent, or quote outside the declared section
  invalid_manifest          malformed manifest, duplicate heading, unsafe path
  source_tampered           source bytes differ from the manifest pin
  snapshot_tampered         --frozen pinned input missing or altered
  expected_verdict_mismatch --frozen observed exit/IDs differ from the pin

FROZEN EXPECTATIONS (--frozen)
  {"manifests": [{"path": REL, "sha256": HEX64, "exit": N, "findings": ["class@id"]}],
   "sources": [{"path": REL, "sha256": HEX64}]}
  Every pinned manifest and source is hashed before any evaluation; a missing or
  altered input is snapshot_tampered (exit 2). Every source a pinned manifest
  references must itself be pinned in "sources", else invalid_manifest (exit 2).
  Each manifest is then run and its exit code and sorted finding ids are compared
  with the pin; any difference is expected_verdict_mismatch (exit 1).

SELF-TEST
  Fixtures are created and removed by TemporaryDirectory under /var/tmp, never
  in the repository; override the parent with QUOTE_FIDELITY_SELFTEST_DIR.
  Every case launches this CLI as `sys.executable -I <script>` and asserts the
  real return code plus the parsed stable class@id lines, not helper returns.
"""
import argparse
import hashlib
import html
import json
import os
import re
import stat
import sys
import tempfile

CLEAN, FAILED, CNE = 0, 1, 2
MAX_WORDS = 25
HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")
MD_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*\Z")
HTML_HEADING = re.compile(r"^<h([1-6])(?:\s[^>]*)?>(.*?)</h\1>[ \t]*\Z", re.IGNORECASE)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CNE_FINDINGS = frozenset({"invalid_manifest", "source_tampered", "snapshot_tampered"})
SELFTEST_ROOT = os.environ.get("QUOTE_FIDELITY_SELFTEST_DIR", "/var/tmp")


class ManifestError(Exception):
    """A could-not-evaluate problem in a manifest or frozen expectations file."""


class Findings:
    def __init__(self):
        self.rows = []
        self.quotes = 0

    def add(self, finding, ident, detail=""):
        self.rows.append((finding, ident, detail))

    def ids(self):
        return sorted("%s@%s" % (finding, ident) for finding, ident, _ in self.rows)

    def exit_code(self):
        if any(finding in CNE_FINDINGS for finding, _, _ in self.rows):
            return CNE
        return FAILED if self.rows else CLEAN


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def read_regular(path, label):
    """Open nonblocking once, require a regular file, and return the bytes."""
    try:
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError as exc:
        raise ManifestError("%s unreadable (%s)" % (label, exc.strerror or type(exc).__name__))
    try:
        if not stat.S_ISREG(os.fstat(handle).st_mode):
            raise ManifestError("%s is not a regular file" % label)
        chunks = []
        while True:
            chunk = os.read(handle, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError as exc:
        raise ManifestError("%s unreadable (%s)" % (label, exc.strerror or type(exc).__name__))
    finally:
        os.close(handle)


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ManifestError("duplicate JSON key %r" % key)
        out[key] = value
    return out


def load_json(path, label):
    blob = read_regular(path, label)
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError:
        raise ManifestError("%s is not valid UTF-8" % label)
    try:
        return json.loads(text, object_pairs_hook=unique_pairs)
    except ManifestError:
        raise
    except ValueError as exc:
        raise ManifestError("%s is not valid JSON (%s)" % (label, exc))


def resolve_relative(base_real, rel, label):
    if not isinstance(rel, str) or not rel.strip():
        raise ManifestError("%s path must be a non-empty string" % label)
    if os.path.isabs(rel):
        raise ManifestError("%s path must be relative: %s" % (label, rel))
    path = os.path.realpath(os.path.join(base_real, rel))
    try:
        inside = os.path.commonpath([base_real, path]) == base_real
    except ValueError:
        inside = False
    if not inside:
        raise ManifestError("%s path escapes the base directory: %s" % (label, rel))
    return path


def pinned_digest(value, label):
    if not isinstance(value, str) or not HEX64.fullmatch(value):
        raise ManifestError("%s sha256 must be 64 hex characters" % label)
    return value.lower()


def parse_manifest(data, base_real):
    if not isinstance(data, dict):
        raise ManifestError("manifest must be a JSON object")
    sources = data.get("sources")
    quotes = data.get("quotes")
    if not isinstance(sources, dict) or not sources:
        raise ManifestError("sources must be a non-empty object")
    if not isinstance(quotes, list) or not quotes:
        raise ManifestError("quotes must be a non-empty array")
    pins = {}
    for source_id, spec in sources.items():
        if not isinstance(source_id, str) or not source_id.strip():
            raise ManifestError("source ids must be non-empty strings")
        if not isinstance(spec, dict):
            raise ManifestError("source %s must be an object" % source_id)
        pins[source_id] = (
            resolve_relative(base_real, spec.get("path"), "source %s" % source_id),
            pinned_digest(spec.get("sha256"), "source %s" % source_id),
        )
    parsed = []
    seen = set()
    for index, entry in enumerate(quotes):
        if not isinstance(entry, dict):
            raise ManifestError("quote #%d must be an object" % index)
        fields = {}
        for key in ("id", "source", "section", "quote"):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ManifestError("quote #%d field %r must be a non-empty string" % (index, key))
            fields[key] = value
        if fields["id"] in seen:
            raise ManifestError("duplicate quote id %r" % fields["id"])
        seen.add(fields["id"])
        if fields["source"] not in pins:
            raise ManifestError("quote %s names unknown source %s" % (fields["id"], fields["source"]))
        parsed.append(fields)
    return pins, parsed


def scan_headings(text):
    """Return (lines, headings); headings are (line index, level, selectors)."""
    lines = text.splitlines(keepends=True)
    heads = []
    fence = None
    for index, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        marker = FENCE.match(line)
        if fence is not None:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= fence[1]:
                fence = None
            continue
        if marker:
            fence = (marker.group(1)[0], len(marker.group(1)))
            continue
        markdown = MD_HEADING.match(line)
        if markdown:
            heads.append((index, len(markdown.group(1)), (line.rstrip(),)))
            continue
        element = HTML_HEADING.match(line)
        if element:
            label = html.unescape(re.sub(r"<[^>]*>", "", element.group(2)))
            heads.append((index, int(element.group(1)),
                          (" ".join(label.split()), line.rstrip())))
    return lines, heads


def section_body(lines, heads, position):
    start = heads[position][0] + 1
    level = heads[position][1]
    end = len(lines)
    for later in heads[position + 1:]:
        if later[1] <= level:
            end = later[0]
            break
    return "".join(lines[start:end])


def grade_quote(quote, text, findings):
    ident = quote["id"]
    if len(quote["quote"].split()) > MAX_WORDS:
        findings.add("quote_too_long", ident, "more than %d whitespace words" % MAX_WORDS)
        return
    lines, heads = scan_headings(text)
    if quote["quote"] not in text:
        findings.add("quote_not_contiguous", ident, "no contiguous occurrence in source")
        return
    matches = [position for position, head in enumerate(heads)
               if quote["section"] in head[2]]
    if len(matches) > 1:
        findings.add("invalid_manifest", ident, "duplicate exact heading %r" % quote["section"])
        return
    if not matches:
        findings.add("quote_location_mismatch", ident, "section not found")
        return
    if quote["quote"] not in section_body(lines, heads, matches[0]):
        findings.add("quote_location_mismatch", ident, "quote lies outside the declared section")


def evaluate_manifest(path):
    findings = Findings()
    try:
        base_real = os.path.realpath(os.path.dirname(os.path.abspath(path)))
        pins, quotes = parse_manifest(load_json(path, "manifest"), base_real)
    except ManifestError as exc:
        findings.add("invalid_manifest", "manifest", str(exc))
        return findings
    texts = {}
    for source_id, (source_path, pinned) in pins.items():
        try:
            blob = read_regular(source_path, "source %s" % source_id)
        except ManifestError as exc:
            findings.add("invalid_manifest", source_id, str(exc))
            return findings
        if sha256(blob) != pinned:
            findings.add("source_tampered", source_id, "sha256 differs from manifest pin")
            return findings
        try:
            texts[source_id] = blob.decode("utf-8")
        except UnicodeDecodeError:
            findings.add("invalid_manifest", source_id, "source is not valid UTF-8")
            return findings
    for quote in quotes:
        findings.quotes += 1
        grade_quote(quote, texts[quote["source"]], findings)
    return findings


def parse_frozen(data, base_real):
    if not isinstance(data, dict):
        raise ManifestError("frozen expectations must be a JSON object")
    manifests = data.get("manifests")
    sources = data.get("sources")
    if not isinstance(manifests, list) or not manifests:
        raise ManifestError("manifests must be a non-empty array")
    if not isinstance(sources, list):
        raise ManifestError("sources must be an array")
    pinned_manifests = []
    seen = set()
    for index, entry in enumerate(manifests):
        if not isinstance(entry, dict):
            raise ManifestError("manifest pin #%d must be an object" % index)
        rel = entry.get("path")
        path = resolve_relative(base_real, rel, "manifest pin #%d" % index)
        if path in seen:
            raise ManifestError("duplicate pinned manifest path %r" % rel)
        seen.add(path)
        want_exit = entry.get("exit")
        if isinstance(want_exit, bool) or not isinstance(want_exit, int) or want_exit not in (CLEAN, FAILED, CNE):
            raise ManifestError("manifest pin %s exit must be 0, 1 or 2" % rel)
        want_ids = entry.get("findings")
        if not isinstance(want_ids, list) or not all(isinstance(item, str) and item.strip() for item in want_ids):
            raise ManifestError("manifest pin %s findings must be an array of strings" % rel)
        pinned_manifests.append({
            "path": path,
            "rel": rel,
            "sha256": pinned_digest(entry.get("sha256"), "manifest pin %s" % rel),
            "exit": want_exit,
            "findings": sorted(want_ids),
        })
    pinned_sources = []
    seen = set()
    for index, entry in enumerate(sources):
        if not isinstance(entry, dict):
            raise ManifestError("source pin #%d must be an object" % index)
        rel = entry.get("path")
        path = resolve_relative(base_real, rel, "source pin #%d" % index)
        if path in seen:
            raise ManifestError("duplicate pinned source path %r" % rel)
        seen.add(path)
        pinned_sources.append({
            "path": path,
            "rel": rel,
            "sha256": pinned_digest(entry.get("sha256"), "source pin %s" % rel),
        })
    return pinned_manifests, pinned_sources


def evaluate_frozen(expected_path):
    findings = Findings()
    try:
        base_real = os.path.realpath(os.path.dirname(os.path.abspath(expected_path)))
        pinned_manifests, pinned_sources = parse_frozen(
            load_json(expected_path, "frozen expectations"), base_real)
    except ManifestError as exc:
        findings.add("invalid_manifest", "frozen", str(exc))
        return findings, []
    for pin in pinned_manifests + pinned_sources:
        try:
            blob = read_regular(pin["path"], "pinned %s" % pin["rel"])
        except ManifestError:
            findings.add("snapshot_tampered", pin["rel"], "pinned input is missing or unreadable")
            return findings, []
        if sha256(blob) != pin["sha256"]:
            findings.add("snapshot_tampered", pin["rel"], "sha256 differs from frozen pin")
            return findings, []
    covered = {pin["path"] for pin in pinned_sources}
    for pin in pinned_manifests:
        try:
            manifest_pins, _ = parse_manifest(
                load_json(pin["path"], "pinned manifest"),
                os.path.realpath(os.path.dirname(pin["path"])))
        except ManifestError:
            continue  # a structurally invalid manifest has no inventory to cover
        for source_id, (source_path, _) in manifest_pins.items():
            if source_path not in covered:
                findings.add("invalid_manifest", "frozen",
                             "manifest %s source %s is not pinned in sources"
                             % (pin["rel"], source_id))
                return findings, []
    rows = []
    for pin in pinned_manifests:
        observed = evaluate_manifest(pin["path"])
        got_exit = observed.exit_code()
        got_ids = observed.ids()
        rows.append((pin["rel"], pin["exit"], pin["findings"], got_exit, got_ids))
        if got_exit != pin["exit"] or got_ids != pin["findings"]:
            findings.add("expected_verdict_mismatch", pin["rel"],
                         "expected exit=%d ids=%s actual exit=%d ids=%s"
                         % (pin["exit"], ids_text(pin["findings"]), got_exit, ids_text(got_ids)))
    return findings, rows


def ids_text(ids):
    return ",".join(ids) if ids else "none"


def label_for(code):
    return {CLEAN: "clean", FAILED: "failed", CNE: "could-not-evaluate"}[code]


def emit_row(finding, ident, detail):
    line = "QUOTE_FIDELITY: %s ident=%s" % (finding, ident)
    if detail:
        line += " " + detail
    print(line)


def run_manifest(path):
    findings = evaluate_manifest(path)
    print("QUOTE_FIDELITY_MANIFEST: %s" % os.path.abspath(path))
    for row in findings.rows:
        emit_row(*row)
    code = findings.exit_code()
    print("QUOTE_FIDELITY_VERDICT: %s quotes=%d findings=%d exit=%d"
          % (label_for(code), findings.quotes, len(findings.rows), code))
    return code


def run_frozen(path):
    findings, rows = evaluate_frozen(path)
    print("QUOTE_FIDELITY_FROZEN: %s" % os.path.abspath(path))
    for rel, want_exit, want_ids, got_exit, got_ids in rows:
        state = "match" if (want_exit == got_exit and want_ids == got_ids) else "mismatch"
        print("QUOTE_FIDELITY_PIN: manifest=%s expected=exit:%d,ids:%s actual=exit:%d,ids:%s %s"
              % (rel, want_exit, ids_text(want_ids), got_exit, ids_text(got_ids), state))
    for row in findings.rows:
        emit_row(*row)
    code = findings.exit_code()
    print("QUOTE_FIDELITY_VERDICT: %s mode=frozen manifests=%d findings=%d exit=%d"
          % (label_for(code), len(rows), len(findings.rows), code))
    return code


# --------------------------------------------------------------------------
# self-test: isolated fixtures under TemporaryDirectory, never the repository
# --------------------------------------------------------------------------
CLEAN_QUOTE = ("Replace address-derived function identifiers with deterministic "
               "names based on parse order.")
SPLICE_QUOTE = ("Use --normalize to replace address-derived function names with "
                "deterministic names based on parse order.")
LOCATION_QUOTE = ("The goal is not perfect source recovery — V8 compilation is lossy, "
                  "and the output of decompilation remains pseudocode.")

MARKDOWN_SOURCE = (
    "# Doc\n"
    "\n"
    "## Usage\n"
    "\n" + CLEAN_QUOTE + "\n"
    "\n"
    "## Notes\n"
    "\n" + LOCATION_QUOTE + "\n"
)

HTML_SOURCE = (
    "<h1>View8</h1>\n"
    "<h2>Usage</h2>\n"
    "<h3>Command-Line Arguments</h3>\n"
    "<ul>\n"
    "<li><code>--normalize</code>: " + CLEAN_QUOTE + "</li>\n"
    "</ul>\n"
    "<h3>Deterministic Function Names and Mapping CSV</h3>\n"
    "<p>Use <code>--normalize</code> to replace address-derived function names "
    "with deterministic identifiers.</p>\n"
)

HTML_ATTRIBUTE_SOURCE = (
    '<h1 class="wp-block-heading">Introduction</h1>\n'
    '<p class="wp-block-paragraph">' + LOCATION_QUOTE + '</p>\n'
    '<h1 class="wp-block-heading">Decompiled output</h1>\n'
    "<p>Other text.</p>\n"
)

FENCE_SOURCE = (
    "## Usage\n"
    "\n"
    "```\n"
    "# pseudo heading\n"
    "```\n"
    "\n" + CLEAN_QUOTE + "\n"
    "\n"
    "## Next\n"
    "\n"
    "Other text.\n"
)

DUPLICATE_HEADING_SOURCE = (
    "## Usage\n" + CLEAN_QUOTE + "\n"
    "## Usage\n" + CLEAN_QUOTE + "\n"
)


def write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def write_bytes(path, blob):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(blob)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def read_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def fixture_manifest(root, source_text, section, quote, quote_id="q1",
                     source_id="S1", source_rel="src/doc.md", manifest_rel="manifest.json"):
    source_path = os.path.join(root, source_rel)
    write_text(source_path, source_text)
    manifest = {
        "sources": {source_id: {"path": source_rel, "sha256": sha256(source_text.encode("utf-8"))}},
        "quotes": [{"id": quote_id, "source": source_id, "section": section, "quote": quote}],
    }
    manifest_path = os.path.join(root, manifest_rel)
    write_json(manifest_path, manifest)
    return manifest_path


def pin_of(path):
    return sha256(read_regular(path, "fixture"))


def observe(args):
    """Run this gate as a subprocess; return (exit, sorted ids, stdout, stderr)."""
    import subprocess
    command = [sys.executable, "-I", os.path.abspath(__file__)] + args
    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8", errors="replace", timeout=60, check=False)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return 2, [], "", "%s: %s" % (type(exc).__name__, exc)
    ids = []
    prefix = "QUOTE_FIDELITY: "
    for line in proc.stdout.splitlines():
        if not line.startswith(prefix) or " ident=" not in line:
            continue
        finding, rest = line[len(prefix):].split(" ", 1)
        ident = rest.split("ident=", 1)[1].split(" ", 1)[0]
        ids.append("%s@%s" % (finding, ident))
    return proc.returncode, sorted(ids), proc.stdout, proc.stderr


def selftest():
    results = []

    def check(name, want_exit, want_ids, observed):
        code, ids, _stdout, _stderr = observed
        ok = code == want_exit and ids == sorted(want_ids)
        print("SELFTEST_CASE: %s case=%s exit=%d expected=%d ids=%s"
              % ("CLEAN" if ok else "FAILED", name, code, want_exit, ids_text(ids)))
        results.append(ok)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-markdown-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        check("markdown_clean", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-html-") as root:
        path = fixture_manifest(root, HTML_SOURCE, "Command-Line Arguments", CLEAN_QUOTE)
        check("html_label_clean", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-html-attr-") as root:
        path = fixture_manifest(root, HTML_ATTRIBUTE_SOURCE, "Introduction", LOCATION_QUOTE)
        check("html_attributes_clean", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-html-token-") as root:
        token = '<h1 class="wp-block-heading">Introduction</h1>'
        path = fixture_manifest(root, HTML_ATTRIBUTE_SOURCE, token, LOCATION_QUOTE,
                                quote_id="q-token")
        check("html_element_token_clean", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-fence-") as root:
        path = fixture_manifest(root, FENCE_SOURCE, "## Usage", CLEAN_QUOTE)
        check("fenced_pseudo_heading_ignored", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-splice-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", SPLICE_QUOTE,
                                quote_id="q-splice")
        check("splice_absent_everywhere", 1,
              ["quote_not_contiguous@q-splice"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-elsewhere-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", LOCATION_QUOTE,
                                quote_id="q-loc")
        check("quote_elsewhere", 1,
              ["quote_location_mismatch@q-loc"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-nosection-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Missing", CLEAN_QUOTE,
                                quote_id="q-sec")
        check("section_absent", 1,
              ["quote_location_mismatch@q-sec"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-substring-") as root:
        source = "## Basic Usage\n\n" + CLEAN_QUOTE + "\n"
        path = fixture_manifest(root, source, "## Usage", CLEAN_QUOTE,
                                quote_id="q-exact")
        check("heading_exact_not_substring", 1,
              ["quote_location_mismatch@q-exact"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-dupheading-") as root:
        path = fixture_manifest(root, DUPLICATE_HEADING_SOURCE, "## Usage", CLEAN_QUOTE,
                                quote_id="q-dup")
        check("duplicate_heading", 2,
              ["invalid_manifest@q-dup"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-long-") as root:
        words = " ".join("w%d" % n for n in range(1, 27))
        path = fixture_manifest(root, "## Usage\n\n" + words + "\n", "## Usage", words,
                                quote_id="q-long")
        check("quote_too_long", 1, ["quote_too_long@q-long"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-boundary-") as root:
        words = " ".join("w%d" % n for n in range(1, 26))
        path = fixture_manifest(root, "## Usage\n\n" + words + "\n", "## Usage", words,
                                quote_id="q-bound")
        check("word_limit_boundary", 0, [], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-tamper-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        manifest = read_json(path)
        manifest["quotes"].append({"id": "q-bad", "source": "S1",
                                   "section": "## Usage", "quote": SPLICE_QUOTE})
        write_json(path, manifest)
        write_text(os.path.join(root, "src/doc.md"), MARKDOWN_SOURCE + "changed\n")
        check("source_tampered_precedes_quotes", 2,
              ["source_tampered@S1"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-invalid-json-") as root:
        path = os.path.join(root, "manifest.json")
        write_text(path, "{ not json")
        check("invalid_json", 2, ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-dup-quote-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE,
                                quote_id="q-dup")
        manifest = read_json(path)
        manifest["quotes"].append(dict(manifest["quotes"][0]))
        write_json(path, manifest)
        check("duplicate_quote_id", 2,
              ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-dup-source-") as root:
        write_text(os.path.join(root, "src/doc.md"), MARKDOWN_SOURCE)
        digest = sha256(MARKDOWN_SOURCE.encode("utf-8"))
        text = ('{"sources":{"S1":{"path":"src/doc.md","sha256":"%s"},'
                '"S1":{"path":"src/doc.md","sha256":"%s"}},'
                '"quotes":[{"id":"q1","source":"S1","section":"## Usage","quote":"%s"}]}'
                % (digest, digest, CLEAN_QUOTE))
        path = os.path.join(root, "manifest.json")
        write_text(path, text)
        check("duplicate_source_key", 2,
              ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-missing-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        os.remove(os.path.join(root, "src/doc.md"))
        check("source_missing", 2, ["invalid_manifest@S1"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-utf8-") as root:
        blob = b"\xff\xfe\x00"
        write_bytes(os.path.join(root, "src/doc.md"), blob)
        manifest = {
            "sources": {"S1": {"path": "src/doc.md", "sha256": sha256(blob)}},
            "quotes": [{"id": "q1", "source": "S1", "section": "## Usage",
                        "quote": CLEAN_QUOTE}],
        }
        path = os.path.join(root, "manifest.json")
        write_json(path, manifest)
        check("source_not_utf8", 2, ["invalid_manifest@S1"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-fifo-") as root:
        os.makedirs(os.path.join(root, "src"))
        os.mkfifo(os.path.join(root, "src/doc.md"))
        manifest = {
            "sources": {"S1": {"path": "src/doc.md", "sha256": "0" * 64}},
            "quotes": [{"id": "q1", "source": "S1", "section": "## Usage",
                        "quote": CLEAN_QUOTE}],
        }
        path = os.path.join(root, "manifest.json")
        write_json(path, manifest)
        check("source_not_regular", 2, ["invalid_manifest@S1"],
              observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-escape-") as root:
        base = os.path.join(root, "md")
        os.makedirs(base)
        write_text(os.path.join(root, "outside.md"), MARKDOWN_SOURCE)
        manifest = {
            "sources": {"S1": {"path": "../outside.md",
                               "sha256": sha256(MARKDOWN_SOURCE.encode("utf-8"))}},
            "quotes": [{"id": "q1", "source": "S1", "section": "## Usage",
                        "quote": CLEAN_QUOTE}],
        }
        path = os.path.join(base, "manifest.json")
        write_json(path, manifest)
        check("path_escape", 2, ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-absolute-") as root:
        outside = os.path.join(root, "outside.md")
        write_text(outside, MARKDOWN_SOURCE)
        manifest = {
            "sources": {"S1": {"path": outside,
                               "sha256": sha256(MARKDOWN_SOURCE.encode("utf-8"))}},
            "quotes": [{"id": "q1", "source": "S1", "section": "## Usage",
                        "quote": CLEAN_QUOTE}],
        }
        path = os.path.join(root, "manifest.json")
        write_json(path, manifest)
        check("absolute_path", 2, ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-empty-") as root:
        write_text(os.path.join(root, "src/doc.md"), MARKDOWN_SOURCE)
        manifest = {
            "sources": {"S1": {"path": "src/doc.md",
                               "sha256": sha256(MARKDOWN_SOURCE.encode("utf-8"))}},
            "quotes": [],
        }
        path = os.path.join(root, "manifest.json")
        write_json(path, manifest)
        check("empty_quotes", 2, ["invalid_manifest@manifest"], observe(["--manifest", path]))

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-ok-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        expected = {
            "manifests": [{"path": "manifest.json", "sha256": pin_of(path),
                           "exit": 0, "findings": []}],
            "sources": [{"path": "src/doc.md",
                         "sha256": pin_of(os.path.join(root, "src/doc.md"))}],
        }
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, expected)
        observed = observe(["--frozen", expected_path])
        check("frozen_reproduces_clean", 0, [], observed)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-mismatch-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        expected = {
            "manifests": [{"path": "manifest.json", "sha256": pin_of(path),
                           "exit": 1, "findings": ["quote_not_contiguous@q1"]}],
            "sources": [{"path": "src/doc.md",
                         "sha256": pin_of(os.path.join(root, "src/doc.md"))}],
        }
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, expected)
        observed = observe(["--frozen", expected_path])
        check("frozen_verdict_mismatch", 1,
              ["expected_verdict_mismatch@manifest.json"], observed)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-tamper-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        expected = {
            "manifests": [{"path": "manifest.json", "sha256": pin_of(path),
                           "exit": 0, "findings": []}],
            "sources": [{"path": "src/doc.md",
                         "sha256": pin_of(os.path.join(root, "src/doc.md"))}],
        }
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, expected)
        write_text(os.path.join(root, "src/doc.md"), MARKDOWN_SOURCE + "changed\n")
        observed = observe(["--frozen", expected_path])
        check("frozen_source_tampered", 2,
              ["snapshot_tampered@src/doc.md"], observed)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-missing-") as root:
        expected = {
            "manifests": [{"path": "absent.json", "sha256": "0" * 64,
                           "exit": 0, "findings": []}],
            "sources": [],
        }
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, expected)
        observed = observe(["--frozen", expected_path])
        check("frozen_input_missing", 2,
              ["snapshot_tampered@absent.json"], observed)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-coverage-") as root:
        path = fixture_manifest(root, MARKDOWN_SOURCE, "## Usage", CLEAN_QUOTE)
        expected = {
            "manifests": [{"path": "manifest.json", "sha256": pin_of(path),
                           "exit": 0, "findings": []}],
            "sources": [],
        }
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, expected)
        observed = observe(["--frozen", expected_path])
        check("frozen_missing_source_pin", 2, ["invalid_manifest@frozen"], observed)

    with tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix="qf-frozen-invalid-") as root:
        expected_path = os.path.join(root, "expected.json")
        write_json(expected_path, {"manifests": "nope", "sources": []})
        observed = observe(["--frozen", expected_path])
        check("frozen_invalid", 2, ["invalid_manifest@frozen"], observed)

    passed = sum(results)
    failed = len(results) - passed
    print("QUOTE_FIDELITY_SELFTEST: %s cases=%d passed=%d failed=%d exit=%d"
          % ("CLEAN" if failed == 0 else "FAILED", len(results), passed, failed,
             0 if failed == 0 else 1))
    return 0 if failed == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="quote-location fidelity gate")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--manifest", metavar="PATH")
    group.add_argument("--frozen", metavar="EXPECTED")
    group.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        if args.frozen is not None:
            return run_frozen(args.frozen)
        return run_manifest(args.manifest)
    except Exception as exc:  # preserve the 0/1/2 contract, never a traceback exit
        print("QUOTE_FIDELITY: invalid_manifest ident=gate detail=internal:%s"
              % type(exc).__name__)
        print("QUOTE_FIDELITY_VERDICT: could-not-evaluate findings=1 exit=2")
        return CNE


if __name__ == "__main__":
    sys.exit(main())
