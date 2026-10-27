#!/usr/bin/env python3
"""Materialise round-42 C1 carriers into a cache directory, fail-closed at every link.

Round-42 C1 carriers are *published third-party* DSL/router images (DD-WRT, OpenWrt
Kamikaze, vendor rootfs).  Their bytes are never committed, so `carriers.json` pins each
one by a chain and every link of that chain is checked here before a byte is written:

    url
      -> sha256(image) == image_sha256                       link `image_sha256`
      -> [optional container] read the member out of the image
           kind "tar"   : member == container.member (exact name, regular file only)
           kind "range" : image[offset : offset+length]
         sha256(member) == container.member_sha256           link `member_sha256`
         (no container: the whole image is the member)
      -> carve = member[carve.offset : carve.offset+carve.bytes_used]
         the window must lie inside the member                link `carve`
         sha256(carve) == carve.sha256                       link `carve_sha256`
      -> CACHE/<carve.sha256>.bin                            link `cache` / `verify`

`CACHE/<sha256>.bin` is what the C1 counter reads (`--carrier-cache`), holding exactly
the carved bytes: `bytes_used` bytes starting at `carve.offset` of the member.  The
carve offset is new in round 42 (round 41 carved at offset 0); a carrier whose SquashFS
sits behind a boot header is expressed as `carve.offset` instead of a second container
step, so the cache entry stays "the filesystem and nothing else".

Schema (one record per carrier; unknown keys INSIDE `container` and `carve` are a spec
error, so a typo in the frozen table cannot silently skip a check; free metadata such as
`kind`, `product`, `publisher`, `oracle`, `nonregular` lives on the record itself):

    {
      "claim": "R42-C1",
      "carriers": [
        {"id": "TQ", "url": "https://<published image>",
         "image_sha256": "<64 hex>",
         "container": {"kind": "tar", "member": "./firmware.bin",
                       "member_sha256": "<64 hex>"},
         "carve": {"offset": 0, "bytes_used": 3014656, "sha256": "<64 hex>"},
         "kind": "vendor", "product": "DD-WRT v24 ...", "oracle": "..."},
        {"id": "KM", "url": "file:///.../kamikaze-8.09.img", "image_sha256": "<64 hex>",
         "container": {"kind": "range", "offset": 65536, "length": 1900544,
                       "member_sha256": "<64 hex>"},
         "carve": {"offset": 0, "bytes_used": 1900544, "sha256": "<64 hex>"}},
        {"id": "RAW", "url": "https://<raw squashfs>", "image_sha256": "<64 hex>",
         "carve": {"offset": 0, "bytes_used": 1234567, "sha256": "<64 hex>"}}
      ]
    }

Round-41 closure D5 / R41W2C1Chain D1 (symlink-following writes) is fixed here:

  * every component of `--cache` / `--image-cache` is lstat'ed before use; a symlink or
    a non-directory component fails closed (link `cache`) and nothing is written;
  * entries are written to a fresh random `.NAME.tmp-<pid>-<rand>` file opened with
    O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, fsync'ed, then renamed into place: a planted
    `<pin>.bin` symlink is *replaced*, never written through, and a planted
    `<pin>.bin.part` is never touched (no fixed temporary name);
  * after the rename the entry is lstat'ed (must be a regular file), size-checked and
    re-hashed with O_NOFOLLOW; any mismatch unlinks it and fails (link `verify`).

Fail-closed ordering: for each carrier every digest link is checked *before* the next
step, and the cache entry is created only after the carve digest has matched.  A carrier
that fails any link leaves no cache entry (the download staging file is removed too).
Earlier carriers of the same run keep their entries: "nothing cached" is per carrier.

Downloads are staged in `--work` (else $TMPDIR, else the platform default) and removed
on every path, success or failure; nothing is written to /tmp unless TMPDIR says so.

Usage:
  fetch-carrier.py --spec carriers.json --cache DIR [--image-cache DIR] [--work DIR]
  fetch-carrier.py --root LANE --rev REV --cache DIR [--repo-spec PATH]
  fetch-carrier.py --selftest

Exit: 0 every managed carrier materialised and verified; 1 a chain link failed (named in
the JSON receipt as `link`); 2 usage / unreadable spec / unusable work or cache path.
Stdlib only.
"""
import argparse
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

CHUNK = 1 << 20
REPO_SPEC = '.ufo/waves/round-42/c1/carriers.json'
HEX64 = re.compile(r'^[0-9a-f]{64}$')
REV_RE = re.compile(r'^[0-9a-fA-F]{4,64}$')
SCHEME_RE = re.compile(r'^(https?|file)://')
CONTAINER_KEYS = {
    'tar': {'kind', 'member', 'member_sha256'},
    'range': {'kind', 'offset', 'length', 'member_sha256'},
}
CARVE_KEYS = {'offset', 'bytes_used', 'sha256'}


class ChainError(Exception):
    """A broken chain link: ``link`` names it, ``detail`` says what was seen."""

    def __init__(self, link, detail=''):
        super().__init__('%s: %s' % (link, detail) if detail else link)
        self.link = link
        self.detail = detail


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b''):
            h.update(chunk)
    return h.hexdigest()


def _isint(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _hex64(v, what):
    s = v.lower() if isinstance(v, str) else ''
    if not HEX64.match(s):
        raise ChainError('spec', '%s is not 64 hex characters: %r' % (what, v))
    return s


# --------------------------------------------------------------------------- spec

def parse_chain(entry):
    """Validate one record and return its normalised chain (or raise ChainError)."""
    url = entry.get('url')
    if not isinstance(url, str) or not SCHEME_RE.match(url):
        raise ChainError('spec', 'url missing or not http(s)/file: %r' % (url,))
    chain = {'url': url,
             'image_sha256': _hex64(entry.get('image_sha256'), 'image_sha256')}

    cont = entry.get('container')
    if cont is None:
        chain['container'] = None
    elif not isinstance(cont, dict):
        raise ChainError('spec', 'container is not an object')
    else:
        kind = cont.get('kind')
        if kind not in CONTAINER_KEYS:
            raise ChainError('spec', 'container.kind %r is not tar|range' % (kind,))
        extra = set(cont) - CONTAINER_KEYS[kind]
        if extra:
            raise ChainError('spec', 'container has unknown keys: %s'
                             % ', '.join(sorted(extra)))
        out = {'kind': kind,
               'member_sha256': _hex64(cont.get('member_sha256'),
                                       'container.member_sha256')}
        if kind == 'tar':
            member = cont.get('member')
            if not isinstance(member, str) or not member:
                raise ChainError('spec', 'container.member missing')
            out['member'] = member
        else:
            off, length = cont.get('offset'), cont.get('length')
            if not _isint(off) or off < 0:
                raise ChainError('spec', 'container.offset must be an integer >= 0')
            if not _isint(length) or length <= 0:
                raise ChainError('spec', 'container.length must be an integer > 0')
            out['offset'], out['length'] = off, length
        chain['container'] = out

    carve = entry.get('carve')
    if not isinstance(carve, dict):
        raise ChainError('spec', 'carve is not an object')
    extra = set(carve) - CARVE_KEYS
    if extra:
        raise ChainError('spec', 'carve has unknown keys: %s' % ', '.join(sorted(extra)))
    off = carve.get('offset', 0)
    used = carve.get('bytes_used')
    if not _isint(off) or off < 0:
        raise ChainError('spec', 'carve.offset must be an integer >= 0')
    if not _isint(used) or used <= 0:
        raise ChainError('spec', 'carve.bytes_used must be an integer > 0')
    chain['carve'] = {'offset': off, 'bytes_used': used,
                      'sha256': _hex64(carve.get('sha256'), 'carve.sha256')}
    return chain


def load_spec(a):
    if a.spec:
        try:
            with open(a.spec, 'rb') as fh:
                return json.load(fh)
        except (OSError, ValueError) as e:
            raise ChainError('spec', 'cannot read %s: %s' % (a.spec, e))
    if not REV_RE.match(a.rev or ''):
        raise ChainError('spec', 'revision is not a hex object name: %r' % (a.rev,))
    p = subprocess.run(['git', '-C', a.root, 'show', '%s:%s' % (a.rev, a.repo_spec)],
                       capture_output=True)
    if p.returncode != 0:
        raise ChainError('spec', 'git show %s:%s failed: %s'
                         % (a.rev, a.repo_spec, p.stderr.decode('utf-8', 'replace').strip()))
    try:
        return json.loads(p.stdout)
    except ValueError as e:
        raise ChainError('spec', 'spec at %s is not JSON: %s' % (a.rev, e))


# ------------------------------------------------------------------- safe paths

def _components(path):
    """Yield every component of ``path`` from the root down (literal, not resolved)."""
    path = os.path.abspath(path)
    parts = []
    head = path
    while True:
        head, tail = os.path.split(head)
        if not tail:
            break
        parts.append(tail)
    cur = head or os.sep
    for part in reversed(parts):
        cur = os.path.join(cur, part)
        yield cur


def _check_path(path, create=False):
    """Validate a directory path component by component.

    A symlink component is refused (the round-41 write primitive), as is a
    non-directory component.  With ``create`` missing components are made; without it
    a missing component simply ends the walk (nothing can be planted beneath it).
    """
    for cur in _components(path):
        try:
            st = os.lstat(cur)
        except FileNotFoundError:
            if not create:
                return os.path.abspath(path)
            try:
                os.mkdir(cur, 0o755)
            except OSError as e:
                raise ChainError('cache', 'cannot create %s: %s' % (cur, e))
            st = os.lstat(cur)
        if stat.S_ISLNK(st.st_mode):
            raise ChainError('cache', 'path component is a symlink: %s' % cur)
        if not stat.S_ISDIR(st.st_mode):
            raise ChainError('cache', 'path component is not a directory: %s' % cur)
    return os.path.abspath(path)


def _drop(path):
    try:
        os.unlink(path)
    except OSError:
        pass


def atomic_write(dirpath, name, writer, want_sha):
    """Write ``name`` inside ``dirpath`` without ever following a symlink.

    Fresh O_EXCL|O_NOFOLLOW temporary file, fsync, rename over the final name (which
    replaces a planted symlink instead of writing through it), then lstat + re-hash the
    entry with O_NOFOLLOW.  Returns ``(path, replaced_symlink)``.
    """
    _check_path(dirpath, create=True)
    final = os.path.join(dirpath, name)
    replaced = os.path.islink(final)
    tmp = None
    fd = None
    for _ in range(5):
        cand = os.path.join(dirpath, '.%s.tmp-%d-%s'
                            % (name, os.getpid(), os.urandom(6).hex()))
        try:
            fd = os.open(cand, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
        except FileExistsError:
            continue
        except OSError as e:
            raise ChainError('cache', 'cannot create a temporary file in %s: %s'
                             % (dirpath, e))
        tmp = cand
        break
    if tmp is None:
        raise ChainError('cache', 'cannot create a temporary file in %s' % dirpath)
    try:
        with os.fdopen(fd, 'wb') as fh:
            fd = None
            writer(fh)
            fh.flush()
            os.fsync(fh.fileno())
        try:
            os.replace(tmp, final)
        except OSError as e:
            raise ChainError('cache', 'cannot replace %s: %s' % (final, e))
        tmp = None
    finally:
        if fd is not None:
            os.close(fd)
        if tmp is not None:
            _drop(tmp)
    st = os.lstat(final)
    if not stat.S_ISREG(st.st_mode):
        _drop(final)
        raise ChainError('verify', 'cache entry is not a regular file: %s' % final)
    h = hashlib.sha256()
    rfd = os.open(final, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        while True:
            b = os.read(rfd, CHUNK)
            if not b:
                break
            h.update(b)
    finally:
        os.close(rfd)
    if h.hexdigest() != want_sha:
        _drop(final)
        raise ChainError('verify', 'cache entry digest %s, want %s'
                         % (h.hexdigest(), want_sha))
    return final, replaced


# ------------------------------------------------------------------------- fetch

def _download(url, fh):
    """Stream ``url`` into ``fh``; a short read against Content-Length is a failure."""
    with urllib.request.urlopen(url, timeout=300) as r:
        headers = getattr(r, 'headers', None)
        clen = headers.get('Content-Length') if headers is not None else None
        status = getattr(r, 'status', None)
        n = 0
        while True:
            b = r.read(CHUNK)
            if not b:
                break
            fh.write(b)
            n += len(b)
    want = int(clen) if clen and clen.strip().isdigit() else None
    if want is not None and want != n:
        raise ChainError('url', 'short read from %s: %d of %d bytes' % (url, n, want))
    # file:// URLs report no status; the image digest check below is the real gate.
    return 'http %d' % status if status is not None else 'read'


def workdir(explicit):
    w = explicit or os.environ.get('TMPDIR') or tempfile.gettempdir()
    if not os.path.isdir(w):
        raise ChainError('work', 'work directory is not a directory: %s' % w)
    return w


def obtain_image(url, want, image_cache, work, fetcher):
    """Return ``(how, path, owned)`` for the image at ``url``, verified by digest."""
    if image_cache and os.path.isdir(image_cache):
        _check_path(image_cache, create=False)
        fp = os.path.join(image_cache, want + '.image')
        if os.path.lexists(fp):
            if os.path.islink(fp):
                raise ChainError('cache', 'image-cache entry is a symlink: %s' % fp)
            if os.path.isfile(fp):
                if sha256_file(fp) == want:
                    return 'cache', fp, False
            else:
                raise ChainError('cache', 'image-cache entry is not a file: %s' % fp)
    try:
        fd, tmp = tempfile.mkstemp(dir=work, prefix='fetch-carrier-', suffix='.img')
        os.close(fd)
    except OSError as e:
        raise ChainError('work', 'cannot stage a download in %s: %s' % (work, e))
    try:
        with open(tmp, 'wb') as fh:
            how = fetcher(url, fh) or 'read'
    except ChainError:
        _drop(tmp)
        raise
    except Exception as e:  # transport error is a broken link, not a pass
        _drop(tmp)
        raise ChainError('url', '%s: %s' % (type(e).__name__, e))
    return how, tmp, True


def _chunks(fh, limit=None):
    left = limit
    while left is None or left > 0:
        chunk = fh.read(CHUNK if left is None else min(CHUNK, left))
        if not chunk:
            return
        if left is not None:
            left -= len(chunk)
        yield chunk


def digest_and_slice(chunks, off, length):
    """Return ``(sha256, carve_window, total)`` over ``chunks`` in a single pass."""
    h = hashlib.sha256()
    buf = bytearray()
    pos = 0
    end = off + length
    for chunk in chunks:
        h.update(chunk)
        lo, hi = pos, pos + len(chunk)
        if hi > off and lo < end:
            buf += chunk[max(off, lo) - lo:min(end, hi) - lo]
        pos = hi
    return h.hexdigest(), bytes(buf), pos


def _bounds(carve, size, where):
    if carve['offset'] + carve['bytes_used'] > size:
        raise ChainError('carve', 'carve %d+%d runs past the %d-byte %s'
                         % (carve['offset'], carve['bytes_used'], size, where))


def _tar_member(tf, name):
    try:
        members = tf.getmembers()
    except (tarfile.TarError, OSError) as e:
        raise ChainError('member', 'image is not a readable tar: %s' % e)
    by_name = {m.name: m for m in members}
    m = by_name.get(name) or by_name.get('./' + name.lstrip('./'))
    if m is None:
        raise ChainError('member', 'tar member %r absent' % name)
    if not m.isfile():
        raise ChainError('member', 'tar member %r is not a regular file' % name)
    return m


# ---------------------------------------------------------------------- pipeline

def _materialise(chain, rec, cache, image_cache, work, fetcher):
    want = chain['image_sha256']
    carve = chain['carve']
    tmp = None
    owned = False
    try:
        how, path, owned = obtain_image(chain['url'], want, image_cache, work, fetcher)
        rec['fetch'] = how
        got = sha256_file(path)
        rec['image_sha256'] = got
        if got != want:
            raise ChainError('image_sha256', 'image %s, want %s' % (got, want))
        if image_cache and owned:
            # Cache the image as soon as its digest matched: the carrier entry below is
            # the only thing this run must not leave behind on a later link failure.
            icache = _check_path(image_cache, create=True)
            fp = os.path.join(icache, want + '.image')
            if not os.path.isfile(fp) or sha256_file(fp) != want:
                atomic_write(icache, want + '.image',
                             lambda fh, src=path: _copy(src, fh), want)

        cont = chain['container']
        if cont is None:
            size = os.stat(path).st_size
            _bounds(carve, size, 'image')
            with open(path, 'rb') as fh:
                msha, body, total = digest_and_slice(
                    _chunks(fh), carve['offset'], carve['bytes_used'])
            if total != size:
                raise ChainError('member', 'image changed size while reading: %d != %d'
                                 % (total, size))
            rec['container'] = {'kind': 'none', 'bytes': size}
        elif cont['kind'] == 'tar':
            with tarfile.open(path, mode='r:') as tf:
                m = _tar_member(tf, cont['member'])
                _bounds(carve, m.size, 'tar member')
                msha, body, total = digest_and_slice(
                    _chunks(tf.extractfile(m)), carve['offset'], carve['bytes_used'])
                if total != m.size:
                    raise ChainError('member', 'tar member short: %d of %d bytes'
                                     % (total, m.size))
            rec['container'] = {'kind': 'tar', 'member': cont['member'], 'bytes': m.size}
            rec['member_sha256'] = msha
            if msha != cont['member_sha256']:
                raise ChainError('member_sha256', 'member %s, want %s'
                                 % (msha, cont['member_sha256']))
        else:
            size = os.stat(path).st_size
            if cont['offset'] + cont['length'] > size:
                raise ChainError('member', 'range %d+%d runs past the %d-byte image'
                                 % (cont['offset'], cont['length'], size))
            with open(path, 'rb') as fh:
                fh.seek(cont['offset'])
                msha, body, total = digest_and_slice(
                    _chunks(fh, cont['length']), carve['offset'], carve['bytes_used'])
            if total != cont['length']:
                raise ChainError('member', 'range short: %d of %d bytes'
                                 % (total, cont['length']))
            rec['container'] = {'kind': 'range', 'offset': cont['offset'],
                                'bytes': cont['length']}
            rec['member_sha256'] = msha
            if msha != cont['member_sha256']:
                raise ChainError('member_sha256', 'member %s, want %s'
                                 % (msha, cont['member_sha256']))

        if len(body) != carve['bytes_used']:
            raise ChainError('carve', 'carve window is %d bytes, want %d'
                             % (len(body), carve['bytes_used']))
        got = sha256(body)
        if got != carve['sha256']:
            raise ChainError('carve_sha256', 'carve %s, want %s' % (got, carve['sha256']))
        rec['carve'] = {'offset': carve['offset'],
                        'bytes_used': carve['bytes_used'], 'sha256': got}

        target, replaced = atomic_write(cache, got + '.bin',
                                        lambda fh: fh.write(body), got)
        rec.update(path=target, bytes=len(body))
        if replaced:
            rec['cache_entry'] = 'symlink-replaced'
    finally:
        if owned and path:
            _drop(path)


def _copy(src, fh):
    with open(src, 'rb') as fsrc:
        for chunk in iter(lambda: fsrc.read(CHUNK), b''):
            fh.write(chunk)


def materialise(entry, cache, image_cache, work, fetcher):
    rec = {'id': entry.get('id'), 'url': entry.get('url'), 'ok': False}
    try:
        chain = parse_chain(entry)
        _materialise(chain, rec, cache, image_cache, work, fetcher)
        rec['ok'] = True
    except ChainError as e:
        rec.update(ok=False, link=e.link, detail=e.detail)
    return rec


def run(spec, cache, image_cache=None, work=None, fetcher=_download):
    """Return ``(records, exit_code)``; only records carrying a url are managed."""
    work = work or workdir(None)
    recs = []
    managed = 0
    for entry in spec.get('carriers') or []:
        if not isinstance(entry, dict):
            continue
        if 'url' not in entry:
            recs.append({'id': entry.get('id'), 'ok': True, 'skipped': 'not-external',
                         'detail': 'no url: lane-built or unmanaged record'})
            continue
        managed += 1
        recs.append(materialise(entry, cache, image_cache, work, fetcher))
    ok = managed > 0 and all(r['ok'] for r in recs if 'skipped' not in r)
    return recs, (0 if ok else 1)


# ---------------------------------------------------------------------- selftest

def selftest():
    """Offline chain tests: inline fixtures, injected fetcher, real filesystem writes."""
    base = tempfile.mkdtemp(prefix='fetch-carrier-selftest-')
    cases = []

    def tar_of(items):
        bio = io.BytesIO()
        with tarfile.open(fileobj=bio, mode='w') as tf:
            for name, body, kind in items:
                ti = tarfile.TarInfo(name)
                if kind == 'file':
                    ti.size = len(body)
                    tf.addfile(ti, io.BytesIO(body))
                elif kind == 'dir':
                    ti.type = tarfile.DIRTYPE
                    tf.addfile(ti)
                elif kind == 'symlink':
                    ti.type = tarfile.SYMTYPE
                    ti.linkname = body.decode()
                    tf.addfile(ti)
                elif kind == 'hardlink':
                    ti.type = tarfile.LNKTYPE
                    ti.linkname = body.decode()
                    tf.addfile(ti)
        return bio.getvalue()

    payload = b'hsqs' + bytes(range(256)) * 3
    head = b'DD-WRT-IMAGE-HEADER' * 5
    member = head + payload + b'PADDING!' * 4
    pin = sha256(payload)
    member_pin = sha256(member)

    tar_image = tar_of([
        ('./firmware.bin', member, 'file'),
        ('./notes.txt', b'read the draft\n', 'file'),
        ('./dir', b'', 'dir'),
        ('./link', b'firmware.bin', 'symlink'),
        ('./linkdir', b'firmware.bin', 'symlink'),
        ('./hard.bin', b'./firmware.bin', 'hardlink'),
    ])
    tar_sha = sha256(tar_image)
    range_head = b'KM-HEADER' * 7
    range_image = range_head + payload + b'END-PAD'
    range_sha = sha256(range_image)
    raw_image = payload

    def spec(image_sha, container, carve, **meta):
        e = {'id': 'T', 'url': 'https://fixture.invalid/image', 'image_sha256': image_sha}
        if container is not None:
            e['container'] = container
        if carve is not None:
            e['carve'] = carve
        e.update(meta)
        return {'carriers': [e]}

    def carve(offset, used, sha):
        c = {'bytes_used': used, 'sha256': sha}
        if offset is not None:
            c['offset'] = offset
        return c

    tar_cont = {'kind': 'tar', 'member': './firmware.bin', 'member_sha256': member_pin}
    range_cont = {'kind': 'range', 'offset': len(range_head),
                  'length': len(payload), 'member_sha256': sha256(payload)}

    def fetcher(data=None, exc=None, keep=None):
        def f(url, fh):
            if exc is not None:
                raise exc
            b = data if keep is None else data[:keep]
            fh.write(b)
            return 'fake'
        return f
    green_tar = spec(tar_sha, tar_cont, carve(len(head), len(payload), pin))
    green = fetcher(tar_image)

    def case(name, sp, fetch, want_rc, want_link=None, want_cache=None,
             image_cache=None, prepare=None, post=None, cache_rel='cache'):
        d = os.path.join(base, name)
        os.makedirs(d)
        cache = os.path.join(d, cache_rel)
        ctx = prepare(d, cache) if prepare else None
        recs, rc = run(sp, cache, image_cache, base, fetch)
        link = None if rc == 0 else (recs[0].get('link') if recs else 'none')
        listed = sorted(os.listdir(cache)) if os.path.isdir(cache) else []
        ok = rc == want_rc
        if want_link is not None:
            ok = ok and link == want_link
        if want_cache is not None:
            ok = ok and listed == want_cache
        if ok and post:
            ok = post(cache, recs, ctx)
        cases.append((name, ok, rc, link, ','.join(listed)))

    # --- green chains -------------------------------------------------------
    case('01-tar-green', green_tar, green, 0, want_cache=[pin + '.bin'],
         post=lambda c, r, x: (sha256_file(os.path.join(c, pin + '.bin')) == pin
                               and os.stat(os.path.join(c, pin + '.bin')).st_size
                               == len(payload)
                               and not os.path.islink(os.path.join(c, pin + '.bin'))))
    case('02-tar-carve-whole-member',
         spec(tar_sha, tar_cont, carve(None, len(member), member_pin)),
         green, 0, want_cache=[member_pin + '.bin'])
    case('03-range-green', spec(range_sha, range_cont, carve(0, len(payload), pin)),
         fetcher(range_image), 0, want_cache=[pin + '.bin'])
    case('04-raw-green', spec(sha256(raw_image), None, carve(0, len(payload), pin)),
         fetcher(raw_image), 0, want_cache=[pin + '.bin'])

    # --- broken digest links ------------------------------------------------
    case('05-image-sha-mismatch',
         spec('0' * 64, tar_cont, carve(len(head), len(payload), pin)),
         green, 1, 'image_sha256', [])
    case('06-partial-download-partial',
         green_tar, fetcher(tar_image, keep=len(tar_image) * 6 // 10),
         1, 'image_sha256', [])
    case('07-partial-download-empty', green_tar, fetcher(b''), 1, 'image_sha256', [])
    case('08-member-sha-mismatch',
         spec(tar_sha, dict(tar_cont, member_sha256='1' * 64),
              carve(len(head), len(payload), pin)), green, 1, 'member_sha256', [])
    case('09-member-sha-omitted',
         spec(tar_sha, {'kind': 'tar', 'member': './firmware.bin'},
              carve(len(head), len(payload), pin)), green, 1, 'spec', [])
    case('10-member-absent',
         spec(tar_sha, dict(tar_cont, member='./nope.bin'),
              carve(len(head), len(payload), pin)), green, 1, 'member', [])
    case('11-member-is-symlink',
         spec(tar_sha, dict(tar_cont, member='./link'),
              carve(len(head), len(payload), pin)), green, 1, 'member', [])
    case('12-member-is-dir',
         spec(tar_sha, dict(tar_cont, member='./dir'),
              carve(0, 1, pin)), green, 1, 'member', [])
    case('13-carve-sha-mismatch',
         spec(tar_sha, tar_cont, carve(len(head), len(payload), '2' * 64)),
         green, 1, 'carve_sha256', [])
    case('13b-member-is-hardlink',
         spec(tar_sha, dict(tar_cont, member='./hard.bin'),
              carve(len(head), len(payload), pin)), green, 1, 'member', [])
    case('13c-member-name-without-dot-slash',
         spec(tar_sha, dict(tar_cont, member='firmware.bin'),
              carve(len(head), len(payload), pin)), green, 0,
         want_cache=[pin + '.bin'])
    case('14-carve-overrun',
         spec(tar_sha, tar_cont, carve(len(head), len(member), pin)),
         green, 1, 'carve', [])
    case('15-carve-zero-length',
         spec(tar_sha, tar_cont, carve(len(head), 0, pin)), green, 1, 'spec', [])
    case('16-carve-unknown-key',
         spec(tar_sha, tar_cont, dict(carve(len(head), len(payload), pin), length=1)),
         green, 1, 'spec', [])
    case('17-carve-offset-not-integer',
         spec(tar_sha, tar_cont, carve('0', len(payload), pin)), green, 1, 'spec', [])
    case('18-range-overrun',
         spec(range_sha, dict(range_cont, length=len(range_image)),
              carve(0, len(payload), pin)), fetcher(range_image), 1, 'member', [])
    case('19-container-unknown-key',
         spec(tar_sha, dict(tar_cont, length=4), carve(len(head), len(payload), pin)),
         green, 1, 'spec', [])
    case('20-url-unreachable', green_tar,
         fetcher(exc=OSError('unreachable')), 1, 'url', [])
    case('21-pin-not-hex',
         spec(tar_sha, tar_cont, carve(len(head), len(payload), 'z' * 64)),
         green, 1, 'spec', [])
    sp = spec(tar_sha, tar_cont, carve(len(head), len(payload), pin))
    sp['carriers'][0]['url'] = 'ftp://host/image'
    case('22-url-scheme', sp, green, 1, 'spec', [])
    case('23-no-carriers', {'carriers': []}, green, 1, None, [])

    # --- symlink / cache-surface cases (round-41 D5) ------------------------
    def prep_entry_symlink(d, cache):
        os.makedirs(cache)
        victim = os.path.join(d, 'victim.txt')
        with open(victim, 'wb') as fh:
            fh.write(b'do not touch me\n')
        os.symlink(victim, os.path.join(cache, pin + '.bin'))
        return victim

    def post_entry_symlink(cache, recs, victim):
        entry = os.path.join(cache, pin + '.bin')
        with open(victim, 'rb') as fh:
            untouched = fh.read() == b'do not touch me\n'
        return (untouched and not os.path.islink(entry)
                and sha256_file(entry) == pin
                and recs[0].get('cache_entry') == 'symlink-replaced')

    case('24-cache-entry-symlink-replaced', green_tar, green, 0,
         want_cache=[pin + '.bin'], prepare=prep_entry_symlink,
         post=post_entry_symlink)

    def prep_part_symlink(d, cache):
        os.makedirs(cache)
        victim = os.path.join(d, 'victim2.txt')
        with open(victim, 'wb') as fh:
            fh.write(b'partial plant\n')
        os.symlink(victim, os.path.join(cache, pin + '.bin.part'))
        return victim

    def post_part_symlink(cache, recs, victim):
        with open(victim, 'rb') as fh:
            untouched = fh.read() == b'partial plant\n'
        return untouched and os.path.islink(os.path.join(cache, pin + '.bin.part'))

    case('25-cache-part-symlink-ignored', green_tar, green, 0,
         want_cache=[pin + '.bin', pin + '.bin.part'],
         prepare=prep_part_symlink, post=post_part_symlink)

    def prep_parent_symlink(d, cache):
        real = os.path.join(d, 'real')
        os.makedirs(real)
        os.symlink(real, os.path.join(d, 'link'))
        return real

    def post_parent_symlink(cache, recs, real):
        return os.listdir(real) == []

    case('26-cache-parent-symlink-refused', green_tar, green, 1, 'cache', [],
         prepare=prep_parent_symlink, post=post_parent_symlink,
         cache_rel='link/cache')

    def prep_cache_is_file(d, cache):
        victim = os.path.join(d, 'cachefile')
        with open(victim, 'wb') as fh:
            fh.write(b'x')
        os.symlink(victim, cache)
        return victim

    def post_cache_is_file(cache, recs, victim):
        with open(victim, 'rb') as fh:
            return fh.read() == b'x'

    case('27-cache-entrypoint-is-symlink', green_tar, green, 1, 'cache', None,
         prepare=prep_cache_is_file, post=post_cache_is_file)

    def prep_icache_symlink(d, cache):
        ic = os.path.join(d, 'ic')
        os.makedirs(ic)
        victim = os.path.join(d, 'victim3.txt')
        with open(victim, 'wb') as fh:
            fh.write(b'image plant\n')
        os.symlink(victim, os.path.join(ic, tar_sha + '.image'))
        return victim

    def post_icache_symlink(cache, recs, victim):
        with open(victim, 'rb') as fh:
            return fh.read() == b'image plant\n'

    case('28-image-cache-symlink-refused', green_tar, green, 1, 'cache', [],
         image_cache=os.path.join(base, '28-image-cache-symlink-refused', 'ic'),
         prepare=prep_icache_symlink, post=post_icache_symlink)

    # --- image cache hit ----------------------------------------------------
    def prep_icache(d, cache):
        ic = os.path.join(d, 'ic')
        os.makedirs(ic)
        with open(os.path.join(ic, tar_sha + '.image'), 'wb') as fh:
            fh.write(tar_image)
        return ic

    def post_icache_hit(cache, recs, ic):
        return recs[0].get('fetch') == 'cache'

    case('29-image-cache-hit', green_tar, fetcher(exc=OSError('must not fetch')), 0,
         want_cache=[pin + '.bin'],
         image_cache=os.path.join(base, '29-image-cache-hit', 'ic'),
         prepare=prep_icache, post=post_icache_hit)

    def prep_poisoned_entry(d, cache):
        os.makedirs(cache)
        with open(os.path.join(cache, pin + '.bin'), 'wb') as fh:
            fh.write(b'not the carrier' * 100)
        return cache

    def post_poisoned_entry(cache, recs, ctx):
        entry = os.path.join(cache, pin + '.bin')
        return sha256_file(entry) == pin and not os.path.islink(entry)

    case('31-poisoned-regular-entry-replaced', green_tar, green, 0,
         want_cache=[pin + '.bin'], prepare=prep_poisoned_entry,
         post=post_poisoned_entry)

    def prep_cache_dir_symlink(d, cache):
        real = os.path.join(d, 'realdir')
        os.makedirs(real)
        os.symlink(real, cache)
        return real

    def post_cache_dir_symlink(cache, recs, real):
        return os.listdir(real) == []

    case('32-cache-entrypoint-dir-symlink-refused', green_tar, green, 1, 'cache', [],
         prepare=prep_cache_dir_symlink, post=post_cache_dir_symlink)

    def prep_entry_dir(d, cache):
        os.makedirs(os.path.join(cache, pin + '.bin'))
        return cache

    def post_entry_dir(cache, recs, ctx):
        entries = sorted(os.listdir(cache))
        return entries == [pin + '.bin'] and os.path.isdir(os.path.join(cache, pin + '.bin'))

    case('33-cache-entry-is-directory', green_tar, green, 1, 'cache', None,
         prepare=prep_entry_dir, post=post_entry_dir)

    def prep_entry_hardlink(d, cache):
        os.makedirs(cache)
        victim = os.path.join(d, 'victim4.txt')
        with open(victim, 'wb') as fh:
            fh.write(b'hardlink plant\n')
        os.link(victim, os.path.join(cache, pin + '.bin'))
        return victim

    def post_entry_hardlink(cache, recs, victim):
        entry = os.path.join(cache, pin + '.bin')
        with open(victim, 'rb') as fh:
            intact = fh.read() == b'hardlink plant\n'
        return (intact and os.stat(victim).st_nlink == 1
                and os.stat(entry).st_ino != os.stat(victim).st_ino
                and sha256_file(entry) == pin)

    case('34-cache-entry-hardlink-plant', green_tar, green, 0,
         want_cache=[pin + '.bin'], prepare=prep_entry_hardlink,
         post=post_entry_hardlink)

    # --- staging hygiene ----------------------------------------------------
    leftovers = [n for n in os.listdir(base) if n.startswith('fetch-carrier-')]
    cases.append(('30-no-leftover-staging', not leftovers, 0, None,
                  ','.join(leftovers)))

    import shutil
    shutil.rmtree(base, ignore_errors=True)

    for name, ok, rc, link, cached in cases:
        print('%s\t%s\trc=%s\tlink=%s\tcache=%s'
              % ('PASS' if ok else 'FAIL', name, rc, link, cached))
    total = len(cases)
    passed = sum(1 for c in cases if c[1])
    print('SELFTEST cases=%d pass=%d fail=%d' % (total, passed, total - passed))
    return 0 if passed == total else 1


# -------------------------------------------------------------------------- main

USAGE = ('usage: fetch-carrier.py --spec FILE --cache DIR [--image-cache DIR] [--work DIR]\n'
         '       fetch-carrier.py --root LANE --rev REV --cache DIR [--repo-spec PATH]\n'
         '       fetch-carrier.py --selftest')


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, usage=USAGE)
    ap.add_argument('--spec')
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--repo-spec', default=REPO_SPEC)
    ap.add_argument('--cache')
    ap.add_argument('--image-cache')
    ap.add_argument('--work')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.cache or not (a.spec or (a.root and a.rev)):
        print(USAGE, file=sys.stderr)
        return 2
    try:
        spec = load_spec(a)
        if not isinstance(spec, dict):
            raise ChainError('spec', 'top level is not an object')
        work = workdir(a.work)
        cache = _check_path(a.cache, create=False)
        if a.image_cache:
            _check_path(a.image_cache, create=False)
    except ChainError as e:
        print('fetch-carrier: %s: %s' % (e.link, e.detail), file=sys.stderr)
        return 2
    recs, rc = run(spec, cache, a.image_cache, work)
    out = {'carriers': recs, 'exit_code': rc}
    print(json.dumps(out, indent=1, sort_keys=True))
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write('\n')
    return rc


if __name__ == '__main__':
    sys.exit(main())
