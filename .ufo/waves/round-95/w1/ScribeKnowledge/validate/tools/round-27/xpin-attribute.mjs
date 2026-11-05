#!/usr/bin/env node
/**
 * R27-C2 capability tool: attribute a saved REA evidence envelope to the
 * evidence-ID rule of rea-agents 6.5.0, 6.7.0, both or neither.
 *
 * Usage:
 *   node xpin-attribute.mjs --pkg65 <6.5.0 package root> --pkg67 <6.7.0 package root> ENVELOPE...
 *   node xpin-attribute.mjs --parse --pkg65 <root> --pkg67 <root> ENVELOPE...
 *
 * Default mode prints one stdout line per envelope:
 *   <path as given> TAB <stored id> TAB <id under 6.5.0 rule> TAB <id under 6.7.0 rule> TAB <6.5.0|6.7.0|both|none>
 *
 * --parse mode prints one stdout line per envelope:
 *   <path as given> TAB <parseEvidence-6.5.0 accept|reject:<first error message>> TAB <parseEvidence-6.7.0 accept|reject:<first error message>>
 *
 * Exit 0 on success, 2 on unreadable input (message on stderr).
 *
 * Neither pin's rule is retyped here. For each pin the tool
 *   1. imports `digestCanonicalValue` from <pkg>/dist/domain/canonicalDigest.js of that pin,
 *   2. extracts the `const semanticProjection = ...;` statement from that pin's
 *      <pkg>/dist/domain/evidence.js source text and evaluates it,
 *   3. hashes `semanticProjection(evidence)` with that pin's own digest code,
 *      giving id = 'ev_' + digestCanonicalValue(projection, 'Evidence').
 *
 * The record handed to a pin's projection is the parsed `.data` object exactly as
 * it appears in the envelope: no field is inserted, defaulted or removed. A record
 * that lacks the `relationship_coverage` key is therefore evaluated with that key
 * absent, which is what each package's own JavaScript does with such a record.
 */

import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import { join, resolve } from "node:path";

const EXIT_OK = 0;
const EXIT_INPUT = 2;

class InputError extends Error {}

/** Parse argv: --pkg65 <root>, --pkg67 <root>, optional --parse, then envelope paths. */
function parseArgs(argv) {
    const pkg65 = [];
    const pkg67 = [];
    const files = [];
    let parseMode = false;
    for (let index = 0; index < argv.length; index += 1) {
        const arg = argv[index];
        if (arg === "--pkg65") {
            const value = argv[index + 1];
            if (value === undefined) throw new InputError("--pkg65 needs a package root");
            pkg65.push(value);
            index += 1;
        } else if (arg === "--pkg67") {
            const value = argv[index + 1];
            if (value === undefined) throw new InputError("--pkg67 needs a package root");
            pkg67.push(value);
            index += 1;
        } else if (arg.startsWith("--pkg65=")) {
            pkg65.push(arg.slice("--pkg65=".length));
        } else if (arg.startsWith("--pkg67=")) {
            pkg67.push(arg.slice("--pkg67=".length));
        } else if (arg === "--parse") {
            parseMode = true;
        } else if (arg === "--") {
            files.push(...argv.slice(index + 1));
            break;
        } else if (arg.startsWith("--")) {
            throw new InputError("unknown option " + arg);
        } else {
            files.push(arg);
        }
    }
    if (pkg65.length !== 1) throw new InputError("--pkg65 must be given exactly once");
    if (pkg67.length !== 1) throw new InputError("--pkg67 must be given exactly once");
    if (files.length === 0) throw new InputError("no envelope paths given");
    return { pkg65: pkg65[0], pkg67: pkg67[0], files, parseMode };
}

/**
 * Extract the `const semanticProjection = ...;` statement from a package's
 * evidence.js source text. The statement ends at the first top-level `;`
 * outside strings, comments and brackets. The returned text is the package's
 * own definition, never a retyped field list.
 */
function extractProjectionStatement(source, label) {
    const marker = "const semanticProjection";
    const start = source.indexOf(marker);
    if (start < 0) {
        throw new InputError(`${label}: no "${marker}" definition in evidence.js`);
    }
    const equals = source.indexOf("=", start + marker.length);
    if (equals < 0) {
        throw new InputError(`${label}: "${marker}" is not an assignment`);
    }
    let depth = 0;
    let index = equals + 1;
    while (index < source.length) {
        const char = source[index];
        const next = source[index + 1];
        if (char === "/" && next === "/") {
            const end = source.indexOf("\n", index);
            index = end < 0 ? source.length : end + 1;
            continue;
        }
        if (char === "/" && next === "*") {
            const end = source.indexOf("*/", index + 2);
            index = end < 0 ? source.length : end + 2;
            continue;
        }
        if (char === "\"" || char === "'" || char === "`") {
            index += 1;
            while (index < source.length) {
                const inner = source[index];
                if (inner === "\\") {
                    index += 2;
                    continue;
                }
                if (inner === char) {
                    index += 1;
                    break;
                }
                index += 1;
            }
            continue;
        }
        if (char === "(" || char === "[" || char === "{") {
            depth += 1;
            index += 1;
            continue;
        }
        if (char === ")" || char === "]" || char === "}") {
            depth -= 1;
            index += 1;
            continue;
        }
        if (char === ";" && depth === 0) {
            const statement = source.slice(start, index + 1);
            if (!statement.includes(marker)) {
                throw new InputError(`${label}: extracted statement does not define ${marker}`);
            }
            return statement;
        }
        index += 1;
    }
    throw new InputError(`${label}: "${marker}" definition is not terminated by ";"`);
}

/** Evaluate the package's own semanticProjection statement and return the function. */
function evaluateProjection(statement, label) {
    try {
        const factory = new Function(`${statement}\nreturn semanticProjection;`);
        const projection = factory();
        if (typeof projection !== "function") {
            throw new Error("semanticProjection is not a function");
        }
        return projection;
    } catch (error) {
        throw new InputError(`${label}: cannot evaluate semanticProjection: ${error.message}`);
    }
}

/** Load one pin: its own digest code, its own projection source text, its own parser. */
async function loadPin(root, label) {
    const packageRoot = resolve(root);
    const digestPath = join(packageRoot, "dist", "domain", "canonicalDigest.js");
    const evidencePath = join(packageRoot, "dist", "domain", "evidence.js");
    let digestModule;
    let evidenceModule;
    let evidenceSource;
    try {
        digestModule = await import(pathToFileURL(digestPath).href);
        evidenceModule = await import(pathToFileURL(evidencePath).href);
        evidenceSource = await readFile(evidencePath, "utf8");
    } catch (error) {
        throw new InputError(`${label}: cannot read package files under ${packageRoot}: ${error.message}`);
    }
    const digestCanonicalValue = digestModule.digestCanonicalValue;
    if (typeof digestCanonicalValue !== "function") {
        throw new InputError(`${label}: ${digestPath} does not export digestCanonicalValue`);
    }
    const parseEvidence = evidenceModule.parseEvidence;
    if (typeof parseEvidence !== "function") {
        throw new InputError(`${label}: ${evidencePath} does not export parseEvidence`);
    }
    const statement = extractProjectionStatement(evidenceSource, label);
    const semanticProjection = evaluateProjection(statement, label);
    return { label, packageRoot, digestCanonicalValue, semanticProjection, parseEvidence };
}

/** The Evidence record of a saved envelope: the record lives under `.data`. */
function evidenceRecord(envelope, path) {
    if (envelope === null || typeof envelope !== "object" || Array.isArray(envelope)) {
        throw new InputError(`${path}: envelope is not a JSON object`);
    }
    const record = envelope.data;
    if (record === null || typeof record !== "object" || Array.isArray(record)) {
        throw new InputError(`${path}: envelope has no ".data" evidence record`);
    }
    return record;
}

/** id = 'ev_' + digestCanonicalValue(semanticProjection(evidence), 'Evidence') under one pin. */
function idUnderPin(pin, evidence) {
    let digest;
    try {
        digest = pin.digestCanonicalValue(pin.semanticProjection(evidence), "Evidence");
    } catch (error) {
        throw new InputError(`${pin.label}: cannot digest projection: ${error.message}`);
    }
    return `ev_${digest}`;
}

function attribute(stored, id65, id67) {
    if (stored === id65 && stored === id67) return "both";
    if (stored === id65) return "6.5.0";
    if (stored === id67) return "6.7.0";
    return "none";
}

/** Run one pin's own parseEvidence on a record and describe the outcome. */
function parseUnderPin(pin, evidence) {
    try {
        pin.parseEvidence(evidence);
        return "accept";
    } catch (error) {
        const issues = error && Array.isArray(error.issues) ? error.issues : [];
        let message = issues.length > 0 ? String(issues[0].message) : String(error && error.message ? error.message : error);
        message = message.replace(/[\t\r\n]+/g, " ").trim();
        return `reject:${message}`;
    }
}

async function main() {
    const { pkg65, pkg67, files, parseMode } = parseArgs(process.argv.slice(2));
    const pin65 = await loadPin(pkg65, "6.5.0");
    const pin67 = await loadPin(pkg67, "6.7.0");
    const lines = [];
    for (const path of files) {
        let envelope;
        try {
            envelope = JSON.parse(await readFile(path, "utf8"));
        } catch (error) {
            throw new InputError(`${path}: cannot read envelope: ${error.message}`);
        }
        const evidence = evidenceRecord(envelope, path);
        if (parseMode) {
            const result65 = parseUnderPin(pin65, evidence);
            const result67 = parseUnderPin(pin67, evidence);
            lines.push([path, `parseEvidence-6.5.0 ${result65}`, `parseEvidence-6.7.0 ${result67}`].join("\t"));
            continue;
        }
        const stored = typeof evidence.evidence_id === "string" ? evidence.evidence_id : "";
        const id65 = idUnderPin(pin65, evidence);
        const id67 = idUnderPin(pin67, evidence);
        lines.push([path, stored, id65, id67, attribute(stored, id65, id67)].join("\t"));
    }
    process.stdout.write(`${lines.join("\n")}\n`);
    return EXIT_OK;
}

try {
    process.exitCode = await main();
} catch (error) {
    const message = error instanceof InputError ? error.message : `unexpected failure: ${error.stack ?? error}`;
    process.stderr.write(`xpin-attribute: ${message}\n`);
    process.exitCode = EXIT_INPUT;
}
