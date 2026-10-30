# Round-52 fetcher draft

Draft: `fetch-vendor.py` (byte-port intended from round-50; see notes below).

Network guards in source:

```python
# Initial request scheme guard (fetch)
if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
    raise ValueError('url outside https://%s: %s' % (ALLOWED_HOST, url))

# Initial request pinned-host guard (same conditional; independent clause)
if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
    raise ValueError('url outside https://%s: %s' % (ALLOWED_HOST, url))

# Redirect scheme guard (_AvmOnlyRedirect.redirect_request)
if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
    raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)

# Redirect pinned-host guard (same conditional; independent clause)
if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
    raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)
```

Selftest covers offline checks for an initial HTTP URL, initial host confusion (`download.avm.de.evil.example`), redirect downgrade, and redirect off-host. The required deletion-site fixture copies (one deleted guard at a time) and their observed red results have **not been run**; current draft therefore does not yet satisfy that acceptance condition. The current implementation is a reduced reconstruction, not a faithful full byte-port: it uses SquashFS helper APIs that have not been checked against round-41, and it omits portions of the original materialisation receipt behavior. Do not integrate without repairing this gap.
