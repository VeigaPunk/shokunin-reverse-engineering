# PrimaryAndroid — primary-source support for Android ABI native-library paths

Seat `KaidokuR22R.PrimaryAndroid-6`, recovery wave W2 (distinct from the lost W1 seats; not a claim they returned). Author-side only; this is not outside admission. Lane read-only except this file and `PrimaryAndroid.json`. No installs. No REA call, no target execution, no device/ADB contact, no account/config inspection.

## Verdict

The source is accessible, so S052 may stay a registry row. The page directly supports the APK path convention `/lib/<abi>/lib<name>.so` for NDK-generated libraries, with `<abi>` drawn from four listed ABIs. It does **not** support the second clause of S052's claim ("so ABI records describe the packaged library rather than an executing device"). That clause is the lane's own inference and must be labelled as such. S052 also lacks the page date and digest that sibling rows (S045, S047) record.

## Primary source

- URL: https://developer.android.com/ndk/guides/abis (final URL identical, no redirect)
- Title: `Android ABIs | Android NDK | Android Developers`
- Page date: footer `Last updated 2026-05-15 UTC.`; HTTP `last-modified: Fri, 15 May 2026 00:27:03 GMT`
- Fetched: HTTP `date: Wed, 21 Oct 2026 13:03:48 GMT` (HEAD); body sha256 `fa4cc619bb3840b6a1d3c2d87c5800fe94307f5b4281c1b731171847fca10858`, 299528 bytes. Devsite HTML embeds per-request markup, so this digest pins this retrieval only and is not a stable content hash.

### Quote (22 words, contiguous in reading order)

Heading path: `ABI management on the Android platform` (h2 `#am`) › `Native code in app packages` (h3 `#native-code-in-app-packages`); page Last updated 2026-05-15 UTC.

> Both the Play Store and Package Manager expect to find NDK-generated libraries on filepaths inside the APK matching the following pattern: /lib/<abi>/lib<name>.so

Markup note: the prose sits in a `<p>` and the pattern in the immediately following `<pre>`. Nothing lies between them, so the quote is contiguous in rendered text but spans two HTML elements.

### Other observed page facts (paraphrased, not quoted)

- `<abi>` is "one of the ABI names listed under Supported ABIs". Table 1 lists `armeabi-v7a`, `arm64-v8a`, `x86`, `x86_64`. armeabi and MIPS were removed in NDK r17. No riscv64 row appears on this revision.
- `<name>` is defined via `LOCAL_MODULE` in `Android.mk`, which is ndk-build framing.
- If the system cannot find libraries where it expects them, it cannot use them, and the app must copy them and `dlopen()` them itself.
- A fat APK example lists `/lib/{armeabi-v7a,arm64-v8a,x86,x86_64}/libfoo.so`.
- Section "Automatic extraction of native code at install time" (h3 `#aen`): the package manager scans `lib/<primary-abi>/lib<name>.so`, then `lib/<secondary-abi>/…`, and copies the matches into the app's `nativeLibraryDir`.

## Relation to the lane targets

- `claims.json` R22-C1 (coverage) lists `identify-flutter-build` and `inspect-dart-aot` in T1. S052 is a round-22 row (S051 onward), and `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` cites it for the path convention. This report only bears on how well S052 is supported; it does not add or count a verb.
- `claims.json` R22-C2 (calibration) is about PROVINCE.md `### Round-22 catalog dispositions` and the evidence under `evidence/c2`. The ADB rows there (`inspect-adb-package`, `list-adb-services`, `inspect-adb-window`, `start-adb-activity`, `stop-adb-app`) are false-client controls. This page says nothing about REA or ADB client behaviour, so it adds no support for those rows. The page's `adb install --abi` line is a device operation and was not run.
- PROVINCE.md `### Round-22 narrowly added static ground` (lines 200–204) records the Godot APK as a parsed negative. The page supports reading that negative narrowly: the APK is laid out by the path convention, and REA's `abis` field is Flutter-scoped (see the control below).
- Baseline check: `git show 7787fea4…:corpus/SOURCES.md | grep -c S052` printed `0`. S052 is therefore new in round 22, at HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.

## Static control: zip listing of the pinned APK (read-only, no execution)

```
$ A=/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_release.apk
$ sha256sum "$A"        # exit 0
6d1bb2cfa126a1b1c87e064a35b3cbd181bef0ec784dec1efd1d64dffa8be6cb  …/android_release.apk
$ unzip -Z1 "$A" | grep -E '^lib/'   # unzip exit 0, grep exit 0
lib/arm64-v8a/libc++_shared.so
lib/arm64-v8a/libgodot_android.so
lib/armeabi-v7a/libc++_shared.so
lib/armeabi-v7a/libgodot_android.so
lib/x86/libc++_shared.so
lib/x86/libgodot_android.so
lib/x86_64/libc++_shared.so
lib/x86_64/libgodot_android.so
$ unzip -Z1 "$A" | grep -c -E '^/lib/'   # prints 0, exit 1 (no match)
```

- Observed: the digest equals the target SHA-256 in the knowledge entry. The APK has 8 entries matching `lib/<abi>/lib<name>.so` across all four Table 1 ABIs. No zip entry begins with `/`.
- Inference: `identify-flutter-build`'s `abis:[]` (ev_3458b996…) is the Flutter-carrier ABI list, not the APK's native-library ABI set. This confirms the knowledge entry's row "ABI list empty → Do not infer the absence of all native code". The page's leading `/` is notation for the archive root; actual zip entry names start with `lib/`. The page itself also writes `lib/<primary-abi>/…` without the slash.

## Unsupported or over-reaching inferences

1. **S052 claim, second clause** ("so ABI records describe the packaged library rather than an executing device"). The page describes the device-side choice (primary/secondary ABI from system properties) and extraction into `nativeLibraryDir`. It says nothing about REA ABI records. The packaged-not-device reading is the lane's inference and is reasonable for a static zip parse, but it should be marked `[INFERENCE]` rather than attributed to S052.
2. **The convention as a guarantee.** The page says "expect" and documents the alternative where the app copies libraries and calls `dlopen()`. Nonconforming layouts are possible, so the path is a convention, not an invariant of every APK.
3. **Coverage of non-ndk-build or non-NDK libraries.** `<name>` is defined through `Android.mk` `LOCAL_MODULE`. That Flutter's `libapp.so`/`libflutter.so` or Godot's `libgodot_android.so` follow the same pattern is observed (Godot) or inferred (Flutter), not stated by the page.
4. **Modern install behaviour.** The page describes copying into `nativeLibraryDir`. Whether libraries are extracted or loaded directly from the APK on current Android releases (for example under the `extractNativeLibs` manifest attribute) is not covered by this page and was not examined.
5. **ABI set completeness.** Table 1 has four ABIs on this revision. Any claim about riscv64 or other ABIs is unsupported by this source.

## Drafted registry row (proposal for L1; replaces the S052 text, same id)

| S052 | Android NDK ABI guide — https://developer.android.com/ndk/guides/abis | docs | A | NDK-generated library path convention inside APKs and the four Table 1 ABIs; not a guarantee for every APK, not Flutter-specific, not modern extraction/loading behaviour, not REA record semantics | Last updated 2026-05-15 UTC (HTTP last-modified Fri, 15 May 2026 00:27:03 GMT); fetched 2026-10-21T13:03:48Z, retrieval sha256 `fa4cc619bb3840b6a1d3c2d87c5800fe94307f5b4281c1b731171847fca10858` (299528 bytes, per-request markup); ABI management on the Android platform › Native code in app packages | Play Store and Package Manager expect NDK libraries at `/lib/<abi>/lib<name>.so` (archive entries `lib/<abi>/…`); that static ABI records describe packaged libraries rather than a device is [INFERENCE]. | mined | 2026-10-21 | 90d | corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md, corpus/lessons/round-22.md |

## Commands and exits

| argv | exit | observed |
|---|---|---|
| `curl -sS -L -o /tmp/abis.html -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n' https://developer.android.com/ndk/guides/abis` | 0 | `http=200 size=299528 url=https://developer.android.com/ndk/guides/abis` |
| `curl -sS -I -L https://developer.android.com/ndk/guides/abis` | 0 | `HTTP/2 200`, `last-modified: Fri, 15 May 2026 00:27:03 GMT`, `date: Wed, 21 Oct 2026 13:03:48 GMT` |
| `sha256sum /tmp/abis.html` | 0 | `fa4cc619…0858` |
| python3 HTML→text extraction (local, `/tmp/abis.txt`) | 0 | title, `Last updated 2026-05-15 UTC.`, heading ids `am`, `native-code-in-app-packages`, `aen`, `sa` |
| `git log -1 --format='%H %s'` (lane) | 0 | `2ee3d9f5… round-22: retain static frontier evidence and calibrated catalog dispositions` |
| `git show 7787fea4…:corpus/SOURCES.md \| grep -c S052` | 0 (pipeline) | `0` |
| `sha256sum <godot apk>` | 0 | `6d1bb2cf…a8be6cb` |
| `unzip -Z1 <godot apk> \| grep -E '^lib/'` | 0 / 0 | 8 entries listed above |
| `unzip -Z1 <godot apk> \| grep -c -E '^/lib/'` | 1 | `0` |

## Unknowns and blockers

- Blockers: none. The source was accessible.
- Not examined: Flutter APK layouts, the `extractNativeLibs` and direct-load behaviour, other Android docs (for example Play App Bundle ABI splits), and any device-side `nativeLibraryDir` value. No device was contacted.
- `corpus/lessons/round-22.md` was not read; S052's citation there is unverified by this seat.
- Tool installs: none.
