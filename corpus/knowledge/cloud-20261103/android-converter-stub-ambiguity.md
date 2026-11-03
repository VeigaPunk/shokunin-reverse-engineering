# A decompiled stub is not recovered behavior

This is an original synthesis of a published study and separate maintainer guidance, not an independent reproduction. The cases below are invented manual reasoning controls, not executed tests. No malware was acquired, executed or installed for this lesson.

## Objective

Distinguish original Dalvik bytecode, conversion to JVM bytecode, decompiler output, reported failure counts and actual semantic fidelity. A downstream decompiler can accurately describe an intermediate artifact that already lost the original method body. A method name and signature surviving conversion do not establish that its behavior survived.

## Sources and attribution

- **[P] Empirical study:** Ulf Kargén, Noah Mauthe and Nahid Shahmehri, “[Android decompiler performance on benign and malicious apps: an empirical study](https://link.springer.com/article/10.1007/s10664-022-10281-9),” *Empirical Software Engineering* 28, article 48 (2023), DOI 10.1007/s10664-022-10281-9, sections 3.1.2–3.1.3 and 4.6. © The Author(s) 2023. The article is available under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). This lesson paraphrases and adapts the study into a new explanatory synthesis and invented controls; no figures, code, samples, or other third-party assets are reproduced. The authors do not endorse this lesson. The source provides the study's results; we did not reproduce them. See the [source article](https://doi.org/10.1007/s10664-022-10281-9) for its notices and the license’s [disclaimer of warranties and limitation of liability](https://creativecommons.org/licenses/by/4.0/legalcode.en#s5).
- **[J] Separate maintainer guidance:** [Jadx, “Troubleshooting Q&A”](https://github.com/skylot/jadx/wiki/Troubleshooting-Q%26A), inspected 2026-11-03. This is general troubleshooting guidance, not evidence of what succeeded on the study's particular sample.

## What the reported case establishes

In the study's manual analysis of one heavily obfuscated Android malware app from the AMD dataset, Jadx had a reported method failure rate of 63%, the highest for an app across the original three datasets. The Java decompilers reported much lower failure rates for that app. This single selected case does not establish a typical or current Jadx failure rate, or current tool behavior. The AMD samples were collected in 2010–2016. [P]

The processing paths differed: Jadx directly decompiled Dalvik bytecode, whereas CFR, Fernflower and Procyon received JVM bytecode after dex2jar conversion. The researchers found that, in some failed method conversions, dex2jar emitted a method with the same signature but replaced its body with an exception-only stub. A warning appeared sometimes, not consistently. A Java decompiler may then successfully produce readable source for that stub, without recovering the original method body. This can make downstream failure reporting look better than actual original-body recovery. The authors spotted this conversion failure mode in one manually analyzed, heavily obfuscated malware app; they did not quantify its frequency. [P]

A throw-only body alone does not prove a conversion failure: an original method may genuinely do nothing else. A specifically linked converter warning or a trustworthy comparison with the original bytecode can corroborate loss. Matching the method's identity, inputs and conversion provenance matters; a warning for another method or artifact cannot establish this method's history. The absence of a warning does not exonerate conversion, given the authors' inconsistent-warning observation. Even a verified conversion failure establishes that the original body was not preserved through that conversion, not what the missing body did.

The authors generally compared failed methods with Dalvik disassembly during manual analysis. In this particular app, baksmali crashed on unrecognized opcodes. Their idea that altered bytecode might be translated by an internal layer at runtime was explicitly a hypothesis, not demonstrated mechanism. The discussed example provides no sample hash in the paper, and neither a working fix nor complete recovery of its original code is established. [P] General Jadx guidance recommends checking suspicious output against Smali or control-flow graphs and cautions that partially decompiled code may be unreliable [J]. That advice does not show that either cross-check succeeded in this case, especially in light of the reported baksmali crash.

## What reported success measures, and what it misses

The study measured decompilation completeness through reported failures, not whether emitted source preserved every original semantic detail. The pipeline used Android SDK apkanalyzer to enumerate method signatures and then matched reported failures to them. The authors note that apkanalyzer sometimes omitted methods or whole classes; apps where it failed outright were excluded. Signature matching and unreported errors introduce further uncertainty. Consequently, a result's denominator and the observed set of failures are bounded by enumeration, matching, conversion, timeout and reporting behavior. [P] A lack of reported failure, a complete listing, syntactically valid output, and faithful behavior are different propositions.

## Hypothetical manual reasoning controls

All scenarios are invented, not observations or executed system tests. Each states the supported conclusion and the tempting overclaim to reject.

1. **Conversion versus decompilation.** A converter logs that it replaced method A's body after a conversion error; a Java decompiler cleanly prints that replacement. Accept clean decompilation of the converted body. Reject recovery of A's original body or a conclusion that the Java decompiler caused the upstream loss.
2. **Same signature, different body.** The original and converted artifacts list the same method name and parameter types, but linked bytecode evidence shows different bodies. Accept signature continuity and the documented body discrepancy. Reject semantic equivalence based on the signature.
3. **Throw-only ambiguity.** A converted method contains only a throw, with no reliable warning or original comparison. Accept that this is what the output shows. Reject the assertion that it is necessarily a converter-generated stub; genuine throw-only methods exist. Seek a method-specific conversion warning or original-bytecode comparison.
4. **No warning.** A log has no converter warning for method B, but an independently matched comparison shows its original body was replaced. Accept the comparison at its documented scope. Reject the inference that silence guarantees conversion fidelity; warnings may be inconsistent.
5. **Reporting versus correctness.** A tool reports zero method failures and emits source for all methods it enumerated. Accept that reported outcome for its configuration and enumerated set. Reject claims that every original method was included or the emitted source is semantically correct. Validate coverage and behavior separately.
6. **Enumeration gap.** An enumerator lists 90 methods while an independently verified original inventory contains 100, and the tool reports no failures for the 90. Accept the 90-method reported result and the inventory discrepancy. Reject a 100-method success rate or an assumed outcome for the missing 10.
7. **Decompiler disagreement.** Direct Dalvik decompilation reports a failure, while a Java decompiler displays a same-signature method after conversion. Accept the two path-specific reports. Reject choosing the clean-looking output as faithful solely because it is readable; examine the conversion and original representation.
8. **Shared intermediate blind spot.** Three Java decompilers agree on a method body, but all consumed the same converted JVM artifact. Accept their agreement about that input. Reject treating them as three independent witnesses to the original Dalvik behavior; an upstream replacement would be shared.
9. **Disassembler crash.** A disassembler crashes on an unfamiliar opcode while another tool produces a partial listing. Accept the crash and the limited output as separate observations. Reject claims that the bytecode is inherently invalid, that a particular runtime translation mechanism was proven, or that the remaining body was recovered.
10. **Hypothesis versus observation.** A researcher suggests runtime translation to explain a static-analysis failure, with no runtime evidence. Record it as the researcher's hypothesis alongside the observed failure. Reject presenting the mechanism as established or prescribing a fix as though validated.
11. **Identity and scope.** A paper describes an unusual sample without a digest; a later file has a similar family label. Accept that the later file may be related. Reject byte-for-byte identity or transfer of the paper's exact failure rate without trustworthy matching evidence.
12. **Successful reasoning is not empirical verification.** A reader correctly answers these scenarios. Accept a documented manual review if actually performed. Reject a claim that the scenarios were executed or that an empirical system test passed solely on that basis.

## Review checklist

- Is the 63% result tied to the one manually examined AMD app and the stated study methodology, not generalized to current tools or the Android ecosystem?
- Are original bytecode, conversion output, decompiled text, reported failures, method enumeration and semantic correctness kept separate?
- Is a throw-only body treated as ambiguous without method-specific corroboration, and is warning silence treated cautiously?
- Are the baksmali crash, unverified runtime-translation hypothesis, missing sample hash, and absence of an established fix or complete recovery preserved?
- Is maintainer advice clearly separate from observations on this sample? Are omitted methods, excluded apps and signature-matching limitations retained?
- Are these controls explicitly hypothetical, with no claim that the scenarios were executed or that an empirical system test passed?

## Independent manual review of the hypothetical controls

An independent reviewer passed the original draft and manually judged all 12 invented controls. The public adaptation rewords control 12 and related review language. The original judgments reviewed written reasoning, not executed tests:

1. Control 1 correctly distinguishes upstream conversion loss from downstream decompilation.
2. Control 2 distinguishes method identity from body preservation.
3. Control 3 preserves the ambiguity of a throw-only body without corroboration.
4. Control 4 does not treat warning silence as proof of conversion fidelity.
5. Control 5 distinguishes reported success from semantic fidelity.
6. Control 6 accounts for the enumerator's denominator gap.
7. Control 7 keeps the different decompiler paths distinct.
8. Control 8 recognizes dependence on a shared intermediate input.
9. Control 9 does not overinterpret the disassembler crash.
10. Control 10 separates the proposed mechanism from observation.
11. Control 11 preserves uncertainty about sample identity; the no-hash observation concerns the paper's discussed example, not the linked dataset generally.
12. The original control 12 did not infer system testing from successful reasoning.
