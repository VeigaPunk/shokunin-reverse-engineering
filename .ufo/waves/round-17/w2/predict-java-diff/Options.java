// Compile-only stub for GoVer.java's program-properties accessors.
// Covers ONLY the two members GoVer.java references
// (getString / setString); no parsing behavior lives here.
// Real signature: ghidra.framework.options.Options.
package ghidra.framework.options;

public interface Options {
	String getString(String name, String defaultValue);
	void setString(String name, String value);
}
