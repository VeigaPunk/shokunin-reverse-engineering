# Proposed change (PATCH TEXT — not applied) — EX-02 / chain c1

Target: new file `receipts/solc-install.txt` (parent lands at integration; the c1 claim
requires the install receipt "committed under `receipts/`").

## New file: receipts/solc-install.txt

```text
solc install receipt — arc3-loop1-round1, seat EX-02 (installer), 2026-10-19
repo HEAD at install: e845c2b524ad2e59871e004c51a1386e192a74ab
host node: v26.12.0 (mise) | npm: 11.20.0

package:            solc
exact version:      0.8.37  (0.8.37+commit.f401782d.Emscripten.clang)
tarball:            https://registry.npmjs.org/solc/-/solc-0.8.37.tgz
tarball sha256:     0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51
tarball size:       6476046 bytes
tarball sha512:     sha512-ieUYdPDRGNKMsZpCfi9tY64Q+ASoL8tyhLuvf9cFiqDs+6ijlx8Wn2CRi0N71AlCvRx0V092rlUYu3b3PuxWlA==
registry shasum:    1aacd7601aec858b2f4ba78d0427c9e582e92b6c  (sha1, dist.shasum)
registry time.modified: 2026-09-10T10:02:55.025Z

install command:    npm install --prefix .ufo/waves/arc3-loop1-round1/tools/solc-prefix solc@0.8.37
install path:       .ufo/waves/arc3-loop1-round1/tools/solc-prefix/
bin path:           .ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/.bin/solcjs
npm cache path:     /home/vgpnk/.npm
cache content file: /home/vgpnk/.npm/_cacache/content-v2/sha512/89/e5/1874f0d118d28cb19a427e2f6d63ae10f804a82fcb7284bbaf7fd7058aa0ecfba8a3971f169f60918b437bd40942bd1c74574f76ae5518bb76f73eec5694
cache index entry:  /home/vgpnk/.npm/_cacache/index-v5/83/d6/551073c673831c2405f12184ab4a154657fa67da9fc869d2c0720b4a03b7

dep tree (npm ls --all): solc@0.8.37 + command-exists@1.2.9, commander@8.3.0,
  follow-redirects@1.16.1, js-sha3@0.8.0, memorystream@0.3.1, semver@5.7.2, tmp@0.2.6
verification:       solcjs --version -> "0.8.37+commit.f401782d.Emscripten.clang", exit 0
cross-check:        byte-identical to pre-existing ambient global install (fnm node v24.21.0):
  soljson.js sha256 221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c (both trees)
  solc.js    sha256 188c3fdca72bbb8ec1c70373427ad4536e117341c48944dae9185f9cf035146f (both trees)
custody:            5-path sha256 identical pre/post install (no drift)
full evidence:      .ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt
```
