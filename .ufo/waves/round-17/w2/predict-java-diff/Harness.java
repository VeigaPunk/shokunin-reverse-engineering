// PredictJavaDiff harness — Kaidoku round 17 wave 2.
// Drives the REAL extracted Ghidra sources GoVer.java / GoVerRange.java
// (Base-src.zip, ghidra/app/util/bin/format/golang/) over escaped test
// strings from stdin and prints one result line per input.
//
// Escapes on stdin: "\\", "n", "r", "t" after a backslash, and 'u' + 4 hex
// digits (UTF-16 units, so astral chars are sent as a surrogate pair).
//
// The "go" prefix strip replicates GoBuildInfo.java:488-489 verbatim:
//   if (versionString.startsWith("go")) versionString = versionString.substring(2);
//
// Output line format (TAB separated):
//   <idx>\tVALID\t<major>\t<minor>\t<patch>\t<toString>\t<inRange>
//   <idx>\tINVALID
// where inRange = GoVerRange.parse("1.15-1.25").contains(ver)
// (the SUPPORTED_VERSIONS literal of GoRttiMapper.java:79).

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

import ghidra.app.util.bin.format.golang.GoVer;
import ghidra.app.util.bin.format.golang.GoVerRange;

public class Harness {

	static String unescape(String line) {
		StringBuilder sb = new StringBuilder(line.length());
		for (int i = 0; i < line.length(); i++) {
			char c = line.charAt(i);
			if (c != '\\') {
				sb.append(c);
				continue;
			}
			char e = line.charAt(++i);
			switch (e) {
				case 'n': sb.append('\n'); break;
				case 'r': sb.append('\r'); break;
				case 't': sb.append('\t'); break;
				case '\\': sb.append('\\'); break;
				case 'u':
					sb.append((char) Integer.parseInt(line.substring(i + 1, i + 5), 16));
					i += 4;
					break;
				default:
					throw new IllegalArgumentException("bad escape \\" + e);
			}
		}
		return sb.toString();
	}

	public static void main(String[] args) throws Exception {
		GoVerRange supported = GoVerRange.parse("1.15-1.25");
		BufferedReader in =
			new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
		String line;
		int idx = 0;
		while ((line = in.readLine()) != null) {
			String raw = unescape(line);
			// GoBuildInfo.java:488-489
			String versionString = raw;
			if (versionString.startsWith("go")) {
				versionString = versionString.substring(2);
			}
			// GoBuildInfo.getGoVer -> GoVer.parse(version) (GoBuildInfo.java:238)
			GoVer ver = GoVer.parse(versionString);
			if (ver.isInvalid()) {
				System.out.printf("%d\tINVALID%n", idx);
			}
			else {
				System.out.printf("%d\tVALID\t%d\t%d\t%d\t%s\t%b%n",
					idx, ver.getMajor(), ver.getMinor(), ver.getPatch(),
					ver.toString(), supported.contains(ver));
			}
			idx++;
		}
	}
}
