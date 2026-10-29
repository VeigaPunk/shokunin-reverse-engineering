// Offline selftest stub of the rea-agents 6.5.0 digest entry point.
// Deterministic, dependency-free; both mint and recompute use THIS stub, so the
// counter's mint-vs-recompute equality is preserved without the real package.
import { createHash } from "node:crypto";

function stable(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value) === undefined ? "null" : JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(stable).join(",") + "]";
  const keys = Object.keys(value).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + stable(value[k])).join(",") + "}";
}

export function digestCanonicalValue(value, prefix) {
  const h = createHash("sha256").update(String(prefix) + "\n" + stable(value)).digest("hex");
  return "ev_" + h;
}
