// Compile-only stub for GoVer.java's fromProgramProperties signature.
// Real signature: ghidra.program.model.listing.Program with static
// PROGRAM_INFO String constant and getOptions(String) accessor.
// No parsing behavior lives here.
package ghidra.program.model.listing;

import ghidra.framework.options.Options;

public interface Program {
	String PROGRAM_INFO = "Program Information";

	Options getOptions(String propertyListName);
}
