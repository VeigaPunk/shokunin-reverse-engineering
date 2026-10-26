#!/usr/bin/env node
// Direct probe of rea-agents@6.5.0 `inventoryFirmwareOutput` (the staged-entry
// budget).  Builds a staging-like tree with one of every name kind REA can meet
// (directory, regular file, symlink, fifo, unix socket, character device) and
// reports (a) what the function returns and (b) the exact budget at which it
// throws, so the counting rule is measured rather than read.
//
// Usage: node count-entries-probe.mjs <fixture-root>
//        (the caller creates the tree; this script never runs an extractor)
import { inventoryFirmwareOutput } from "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/firmware/FirmwareFiles.js";

const root = process.argv[2];
if (!root) {
    console.error("usage: node count-entries-probe.mjs <fixture-root>");
    process.exit(2);
}
const op = "extract_firmware";

let failAt = null;
const failures = [];
const tryBudget = async (maxEntries) => {
    try {
        const entries = await inventoryFirmwareOutput(root, 1 << 30, maxEntries, op, undefined);
        return { ok: true, entries };
    } catch (cause) {
        failures.push({
            maxEntries,
            tag: cause?._tag ?? null,
            code: cause?.message ?? String(cause),
            reason: cause?.reason ?? null,
            operation: cause?.operation ?? null,
        });
        if (failAt === null) failAt = maxEntries;
        return { ok: false };
    }
};

// Smallest budget that succeeds, found from below; also reports one above.
let success = null;
for (let n = 1; n <= 32; n++) {
    const r = await tryBudget(n);
    if (r.ok) {
        success = { maxEntries: n, entries: r.entries };
        break;
    }
}
const above = success === null ? null : await tryBudget(success.maxEntries + 1);

const shape = success === null
    ? null
    : success.entries.map((e) => ({ rel: e.relativePath, kind: e.kind, size: e.size, link: e.linkTarget }));

console.log(JSON.stringify({
    root,
    budget_that_first_succeeds: success === null ? null : success.maxEntries,
    entries_returned: shape === null ? null : shape.length,
    kinds_returned: shape === null ? null : [...new Set(shape.map((s) => s.kind))].sort(),
    returned: shape,
    budget_plus_one_ok: above === null ? null : above.ok,
    budget_plus_one_entries: above === null || !above.ok ? null : above.entries.length,
    failures,
}, null, 1));
