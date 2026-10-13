<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/08-java-runtime.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 · 08 — Java runtime for REA/Ghidra

Round-1 curation of the Java toolchain underpinning Ghidra-driven reverse
engineering on this host. All commands run 2026-10-13.

## Candidate: Host JDK is a single OpenJDK 21.0.12.1 install, full JDK (javac present)

- claim: The only Java runtime installed on this host is OpenJDK
  21.0.12.1+1 (64-bit Server VM, build stamped 2026-08-18) at
  `/usr/lib/jvm/java-21-openjdk`; it is a full JDK (`javac 21.0.12.1` exists),
  and `/usr/lib/jvm` contains no other version — only the `default` and
  `default-runtime` symlinks, both pointing at `java-21-openjdk`.
- source: `/usr/lib/jvm/java-21-openjdk/bin/java -version`;
  `javac -version`; `ls -la /usr/lib/jvm/`
- verify: `/usr/lib/jvm/java-21-openjdk/bin/java -version && /usr/lib/jvm/java-21-openjdk/bin/javac -version && ls -la /usr/lib/jvm/`
- verified-at: 2026-10-13
- suggested: admit — hard, independently re-runnable host fact; Ghidra needs a
  JDK (not JRE) so the javac presence is load-bearing.

## Candidate: `java` on PATH and `JAVA_HOME` resolve to the same JDK 21 — no split-brain

- claim: `java -version` on PATH and `$JAVA_HOME/bin/java -version` report the
  identical build: `/usr/bin/java` is a symlink chain ending at
  `/usr/lib/jvm/java-21-openjdk/bin/java`, and `JAVA_HOME` is
  `/usr/lib/jvm/java-21-openjdk`. Any tool resolving Java by PATH or by
  JAVA_HOME gets the same binary.
- source: `java -version`; `which java`; `readlink -f $(which java)`;
  `echo $JAVA_HOME`
- verify: `java -version 2>&1 | head -1; readlink -f "$(which java)"; echo "JAVA_HOME=$JAVA_HOME"`
- verified-at: 2026-10-13
- suggested: admit — eliminates a whole class of "wrong Java picked" failure
  modes for REA tooling; directly falsifiable.

## Candidate: JAVA_HOME is exported twice, in both `~/.bashrc` and `~/.profile`

- claim: `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` is exported at
  `~/.bashrc:24` and `~/.profile:4` — both the interactive-shell and
  login-shell paths set it to the same value, so non-interactive SSH /
  systemd-spawned and terminal shells agree. The duplication means an edit to
  only one file would silently desynchronize the two entry paths.
- source: `grep -rn JAVA_HOME ~/.bashrc ~/.profile ~/.bash_profile`
  (`.bash_profile` absent — no matches, file not present)
- verify: `grep -rn JAVA_HOME ~/.bashrc ~/.profile ~/.bash_profile`
- verified-at: 2026-10-13
- suggested: admit — env wiring is exactly the kind of invisible prerequisite
  a curated record should pin; the dual-export caveat is a real drift hazard.

## Candidate: Ghidra 12.1.4's documented minimum is JDK 21 (64-bit) — installed JDK satisfies it exactly

- claim: The installed Ghidra (`~/.local/opt/ghidra_12.1.4_PUBLIC`, version
  12.1.4_PUBLIC) declares under "Minimum Requirements → Software" in its
  bundled `GettingStarted.md` (line 54): "Java 21 64-bit Runtime and
  Development Kit (JDK)", and `support/launch.properties:4` notes "Ghidra
  requires a JDK to launch." The host's OpenJDK 21.0.12.1 full JDK meets both
  the version floor and the JDK-not-JRE constraint.
- source: `~/.local/opt/ghidra_12.1.4_PUBLIC/GettingStarted.md:54`;
  `~/.local/opt/ghidra_12.1.4_PUBLIC/support/launch.properties`
- verify: `sed -n '46,56p' ~/.local/opt/ghidra_12.1.4_PUBLIC/GettingStarted.md; grep -n "requires a JDK" ~/.local/opt/ghidra_12.1.4_PUBLIC/support/launch.properties`
- verified-at: 2026-10-13
- suggested: admit — the core "prerequisite vs installed" verdict for the
  lane; sourced from the shipped artifact's own docs, not external memory.

## Candidate: Ghidra's Java resolution prefers JAVA_HOME over PATH; override knob exists but is unset

- claim: Per Ghidra's bundled Java Notes (`GettingStarted.md` lines 98–105),
  Ghidra locates Java on PATH or via `JAVA_HOME`, with `JAVA_HOME` taking
  precedence; if no supported JDK is found it prompts for a Java home path.
  Additionally `support/launch.properties` exposes `JAVA_HOME_OVERRIDE`
  (currently empty) to force a Java home. Because `JAVA_HOME` is exported in
  both `.bashrc` and `.profile` and points at a supported JDK 21, `ghidraRun`
  binds the correct JDK non-interactively on this host.
- source: `~/.local/opt/ghidra_12.1.4_PUBLIC/GettingStarted.md:98-105`;
  `~/.local/opt/ghidra_12.1.4_PUBLIC/support/launch.properties:5`
  (`JAVA_HOME_OVERRIDE=` empty); `ghidraRun` → `support/launch.sh bg jdk`
- verify: `sed -n '98,106p' ~/.local/opt/ghidra_12.1.4_PUBLIC/GettingStarted.md; grep -n "JAVA_HOME_OVERRIDE" ~/.local/opt/ghidra_12.1.4_PUBLIC/support/launch.properties; grep -n "launch.sh" ~/.local/opt/ghidra_12.1.4_PUBLIC/ghidraRun`
- verified-at: 2026-10-13
- suggested: admit — explains *why* the env wiring above is sufficient and
  documents the supported remediation knob if it ever isn't.

## Candidate: Single-Java host is a latent fragility — JDK removal/upgrade would strand Ghidra

- claim: `/usr/lib/jvm` contains exactly one Java. Since Ghidra 12.1.4 pins a
  supported-version check (launch.sh fails closed: "ERROR: Failed to find a
  supported JDK"), a distro upgrade that replaced or removed
  `java-21-openjdk` without leaving a supported JDK on PATH/JAVA_HOME would
  break every Ghidra-backed REA workflow with no graceful fallback — the only
  recovery path is installing a new JDK or setting `JAVA_HOME_OVERRIDE`.
- source: `ls -la /usr/lib/jvm/` (sole entry `java-21-openjdk`);
  `support/launch.sh` lines ~153–165 (fail-closed JDK discovery)
- verify: `ls /usr/lib/jvm/ | wc -l; sed -n '147,166p' ~/.local/opt/ghidra_12.1.4_PUBLIC/support/launch.sh`
- verified-at: 2026-10-13
- suggested: admit — falsifiable (count the jvm dir, read the fail path) and
  operationally relevant; flagged as risk, not as a defect requiring action.

## Candidate: REA skill enumerates Ghidra/Java as expected host tooling — consistent with what is installed

- claim: The REA skill loaded for this lane
  (`~/.agents/skills/reverse-engineer-anything/SKILL.md` line 40) lists "Java,
  Ghidra, IDA, JADX, Binwalk or Unblob" among the host runtimes it may
  require; on this host the Java+Ghidra pair is present and version-compatible,
  while IDA/JADX were not verified in this pass.
- source: `grep -in "java\|ghidra" ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verify: `grep -n "Java, Ghidra" ~/.agents/skills/reverse-engineer-anything/SKILL.md; command -v jadx ida64 2>&1`
- verified-at: 2026-10-13
- suggested: admit — ties the Java finding back to the lane's declared
  toolchain contract; explicitly scoped to Java+Ghidra so no overclaim.

## Summary
Host runs a single full OpenJDK 21.0.12.1 at `/usr/lib/jvm/java-21-openjdk` with `JAVA_HOME` redundantly exported in `.bashrc:24` and `.profile:4` and PATH resolving to the same binary — exactly satisfying Ghidra 12.1.4's "Java 21 64-bit JDK" minimum; the only latent risk is that there is no second Java if JDK 21 is ever removed or upgraded away.
