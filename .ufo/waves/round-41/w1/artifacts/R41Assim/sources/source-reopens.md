# R41Assim — sources re-opened this round (2026-10-26)

All fetches made from scratch `$S=/fast/scratch/hyaku/kaidoku-r41/R41Assim`, `cd "$S/src"`.
Access instants are the fetched files' UTC mtimes (`datetime.fromtimestamp(st_mtime).astimezone()`).

| # | URL | HTTP outcome | bytes | sha256 | access (UTC) |
|---|---|---|---|---|---|
| A1 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | curl -fsSL exit 0 | 7580 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` | 2026-10-26T20:22:21Z |
| A2 | https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md | curl -fsSL exit 0 | 7580 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` (identical to A1) | 2026-10-26T20:22:21Z |
| A3 | https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md | curl -fsSL exit 0 | 1050 | `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` | 2026-10-26T20:22:21Z |
| B1 | https://raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md | curl -fsSL exit 0 | 1470 | `87b8277efbbbdcdfcaa6518c1d3efed071617214432c81400b9e67ee093a11d4` | 2026-10-26T20:22:21Z |
| B2 | https://api.github.com/repos/ReFirmLabs/binwalk/commits/master | curl -fsSL exit 0 | 223798 | sha of `master` object: `26713972e3f9f52dc37d4a421c4554b0bd9e82ef`, committer date 2026-08-11T15:27:26Z, message `Clippy/fmt fixes` | 2026-10-26T20:24:05Z |
| B3 | https://raw.githubusercontent.com/ReFirmLabs/binwalk/26713972e3f9f52dc37d4a421c4554b0bd9e82ef/README.md | curl -fsSL exit 0; `cmp` B1 B3 exit 0 (identical) | 1470 | `87b8277efbbbdcdfcaa6518c1d3efed071617214432c81400b9e67ee093a11d4` | 2026-10-26T20:24:47Z |

The exact fetch commands:

```sh
curl -fsSL -o unblob-README.md        https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md
curl -fsSL -o unblob-HEAD-README.md   https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md
curl -fsSL -o sasquatch-README.md     https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md
curl -fsSL -o binwalk-README.md       https://raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md
curl -fsSL -o binwalk-master-commit.json https://api.github.com/repos/ReFirmLabs/binwalk/commits/master
curl -fsSL -o binwalk-pinned-README.md \
  https://raw.githubusercontent.com/ReFirmLabs/binwalk/26713972e3f9f52dc37d4a421c4554b0bd9e82ef/README.md
sha256sum *.md ; cmp binwalk-pinned-README.md binwalk-README.md
```

## Located quotes (≤25 words, contiguous, with line and section)

### A. unblob README (A1/A2, sha256 `6544d60f…3716`)
- line 43 (opens the install block): `Then install the required external extractor tools. On Ubuntu/Debian:`
- **line 49, inside that block, section “Installation” → Ubuntu/Debian route:**
  `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):` (7 words)
- Stage candidate A's claim that the `.deb` is a release asset is borne out at line 52:
  `curl -L -o sasquatch_1.0.deb "https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/…"`

### B. devttys0/sasquatch README (A3, sha256 `f09961ee…1fef`)
- line 4, section “About”: `a set of patches to the standard unsquashfs utility (part of squashfs-tools)` (12 words)
- **line 8, section “About”:** `` `sasquatch` will attempt to automatically resolve such customizations via a brute-force method. `` (13 words)
- **line 12, section “About”, standalone line:** `Very beta.` (2 words)
- line 17, section “Prerequisites”: `You need a C/C++ compiler, plus the liblzma, liblzo and zlib development libraries:`
- line 26, section “Installation”: `` The included `build.sh` script will download squashfs-tools v4.3, patch the source, then build and install `sasquatch` `` (18 words)

### C. ReFirmLabs binwalk README (B1 ≡ B3, sha256 `87b8277e…11d4`, commit `26713972…`)
- **line 3, document lead under H1 `# Binwalk v3` (NOT § "What does it do?"):**
  `This is an updated version of the Binwalk firmware analysis tool, re-written in Rust for speed and accuracy.` (20 words)
- **line 9, section `## What does it do?`:**
  `Binwalk can identify, and optionally extract, files and data that have been embedded inside of other files.` (18 words)
- line 11, section `## What does it do?`, per-signature catalogue pointer:
  `a [wide variety](https://github.com/ReFirmLabs/binwalk/wiki/Supported-Signatures) of file and data types` (13 words)

Anchor correction for candidate C: the staged entry cites § "What does it do?" for **both** sentences; the
Rust-rewrite sentence sits in the document lead (line 3) above that heading (heading is line 7).

## Recheck command as staged (reproduces)

```sh
curl -fsSL https://raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md | grep -c 'Binwalk v3'
# -> 1   (only the H1 at line 1; line 5's image alt is lower-case "binwalk v3")
```
