import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";

const entry = process.env.REA_ENTRY;
const outFile = process.env.REA_OUT;
const closeFile = process.env.REA_CLOSE_OUT;
const toolsFile = process.env.REA_TOOLS_OUT;
const errFile = process.env.REA_ERR;

const child = spawn(process.execPath, [entry, "--mcp"], { stdio: ["pipe", "pipe", "pipe"], env: { ...process.env } });
const stderrChunks = [];
child.stderr.on("data", (d) => stderrChunks.push(d));

let buffer = "";
const responses = new Map();
let pendingResolve = null;

child.stdout.on("data", (d) => {
  buffer += d.toString("utf8");
  let idx;
  while ((idx = buffer.indexOf("\n")) >= 0) {
    const line = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!line) continue;
    let msg; try { msg = JSON.parse(line); } catch { continue; }
    if (msg.id !== undefined) { responses.set(msg.id, msg); if (pendingResolve) { const r = pendingResolve; pendingResolve = null; r(msg); } }
  }
});

const send = (obj) => child.stdin.write(JSON.stringify(obj) + "\n");
const waitFor = (id, timeoutMs = 120000) => {
  if (responses.has(id)) return Promise.resolve(responses.get(id));
  return new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error("timeout waiting for id " + id)), timeoutMs);
    pendingResolve = (msg) => { clearTimeout(t); resolve(msg); };
  });
};

const main = async () => {
  send({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "e25-census", version: "0.1.0" } } });
  const init = await waitFor(1);
  console.error("INIT", JSON.stringify({ protocolVersion: init.result?.protocolVersion, serverInfo: init.result?.serverInfo, capabilities: Object.keys(init.result?.capabilities ?? {}) }));
  send({ jsonrpc: "2.0", method: "notifications/initialized" });

  send({ jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "binary_session", arguments: {} } });
  const call = await waitFor(2);
  writeFileSync(outFile, JSON.stringify(call, null, 2));
  console.error("CALL2 isError:", call.result?.isError ?? false);

  send({ jsonrpc: "2.0", id: 4, method: "tools/call", params: { name: "close_binary", arguments: {} } });
  const close = await waitFor(4, 30000).catch((e) => ({ error: { message: String(e) } }));
  writeFileSync(closeFile, JSON.stringify(close, null, 2));
  console.error("CALL4(close_binary) isError:", close.result?.isError ?? "n/a", "err:", close.error ? JSON.stringify(close.error) : "none");

  const tools = [];
  let cursor; let pageId = 3;
  do {
    send({ jsonrpc: "2.0", id: pageId, method: "tools/list", params: cursor ? { cursor } : {} });
    const page = await waitFor(pageId);
    if (page.error) { console.error("tools/list error", JSON.stringify(page.error)); break; }
    tools.push(...(page.result?.tools ?? []));
    cursor = page.result?.nextCursor;
    pageId++;
  } while (cursor);
  writeFileSync(toolsFile, JSON.stringify({ count: tools.length, tools: tools.map((t) => t.name).sort() }, null, 2));

  writeFileSync(errFile, Buffer.concat(stderrChunks).toString("utf8"));
  console.log(JSON.stringify({ initProtocol: init.result?.protocolVersion, serverInfo: init.result?.serverInfo, toolsListCount: tools.length }));
  child.stdin.end();
  child.kill("SIGTERM");
  const code = await new Promise((r) => child.on("exit", (c, s) => r({ code: c, signal: s })));
  console.log("child exit:", JSON.stringify(code));
  process.exit(0);
};

main().catch((e) => { console.error("FAIL", e); try { child.kill("SIGKILL"); } catch {} process.exit(1); });
