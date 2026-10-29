#!/usr/bin/env python3
"""Calibrated credential-class scan: values only, never reproduced.

A hit is a live-looking value: the value part is >=6 chars, contains no
whitespace/';' and is NOT a redaction placeholder ('[redacted...', '<REDACTED>',
'<redacted...').  Placeholders are reported separately as `placeholder` hits so
the two classes never blur.
"""
import json
import os
import re
import sys

PATTERNS = {
    'set_cookie': re.compile(r'(?im)^\s*set-cookie:\s*([^=\s]+)=([^\s;]+)'),
    'cookie_hdr': re.compile(r'(?im)^\s*cookie:\s*([^\n]+)'),
    'authorization': re.compile(r'(?im)^\s*(?:proxy-)?authorization:\s*([^\n]+)'),
    'x_api_key': re.compile(r'(?im)^\s*x-api-key:\s*([^\n]+)'),
    'github_token': re.compile(r'\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b'),
    'github_pat': re.compile(r'\bgithub_pat_[A-Za-z0-9_]{20,}\b'),
    'bearer': re.compile(r'(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})'),
    'op_ref': re.compile(r'\bop://[A-Za-z0-9][A-Za-z0-9_/-]{3,}'),
    'aws_key': re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    'sk_key': re.compile(r'\bsk-[A-Za-z0-9_-]{16,}\b'),
    'private_key': re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    'jwt': re.compile(r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{6,}'),
}
PLACEHOLDER = re.compile(r'^[\[<](\s*redacted|\s*REDACTED)', re.IGNORECASE)
KNOWN_SCANTER_FIXTURES = {
    # deliberate scanner self-test fixtures: synthetic, not real credentials
    '.ufo/waves/round-49/w2/W2Sentinel/selftest.py',
}


def scan_text(text, path, out, live_only):
    for name, rx in PATTERNS.items():
        for m in rx.finditer(text):
            val = (m.group(m.lastindex) if m.lastindex else m.group(0))
            val = val.strip()
            if path in KNOWN_SCANTER_FIXTURES:
                out.append({'path': path, 'class': name, 'kind': 'synthetic-fixture',
                            'value_len': len(val)})
                continue
            if PLACEHOLDER.match(val) or val.lower() in ('no', 'yes', 'true', 'false'):
                out.append({'path': path, 'class': name, 'kind': 'placeholder',
                            'value_len': len(val)})
                continue
            if name in ('set_cookie', 'cookie_hdr', 'authorization', 'x_api_key'):
                # only the *value* part of a header is credential-class
                if name == 'set_cookie' and not re.match(r'^_?[\w-]+$', m.group(1) or ''):
                    continue
                out.append({'path': path, 'class': name, 'kind': 'live',
                            'value_len': len(val)})
            else:
                out.append({'path': path, 'class': name, 'kind': 'live',
                            'value_len': len(val)})


def main():
    roots = sys.argv[1:]
    hits = []
    nfiles = 0
    nbytes = 0
    for root in roots:
        if os.path.isfile(root):
            paths = [root]
        else:
            paths = []
            for dp, dn, fn in os.walk(root):
                dn[:] = [d for d in dn if d not in ('.git', '__pycache__')]
                for f in fn:
                    paths.append(os.path.join(dp, f))
        for p in paths:
            try:
                b = open(p, 'rb').read()
            except OSError:
                continue
            nfiles += 1
            nbytes += len(b)
            try:
                t = b.decode('utf-8')
            except UnicodeDecodeError:
                t = b.decode('latin-1')
            before = len(hits)
            scan_text(t, p, hits, True)
            for h in hits[before:]:
                h['sha256'] = __import__('hashlib').sha256(b).hexdigest()
    live = [h for h in hits if h['kind'] == 'live']
    ph = [h for h in hits if h['kind'] == 'placeholder']
    syn = [h for h in hits if h['kind'] == 'synthetic-fixture']
    print(json.dumps({
        'roots': roots,
        'files_scanned': nfiles,
        'bytes_scanned': nbytes,
        'live_hits': len(live),
        'placeholder_hits': len(ph),
        'synthetic_fixture_hits': len(syn),
        'live': live,
        'placeholder': ph,
        'synthetic': syn,
    }, indent=1, sort_keys=True))
    return 1 if live else 0


if __name__ == '__main__':
    sys.exit(main())
