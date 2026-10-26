import * as m from "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js";
import { readFileSync } from "node:fs";
m.init_canonicalDigest();
const digestCanonicalValue = m.digestCanonicalValue;
const semanticProjection = (e) => ({
  subject: e.subject === null ? null : { digest: e.subject.digest, format: e.subject.format, architecture: e.subject.architecture },
  provider: e.provider,
  analysis_profile: e.analysis_profile,
  predicate_type: e.predicate_type,
  operation: e.operation,
  parameters: e.parameters,
  raw_result: e.raw_result,
  normalized_result: e.normalized_result,
  confidence: e.confidence,
  authority: e.authority,
  environment: e.environment,
  limitations: e.limitations,
  ...(e.relationship_coverage === null ? {} : { relationship_coverage: e.relationship_coverage }),
  locations: e.locations,
  evidence_links: e.evidence_links,
});
const computeEvidenceId = (e) => `ev_${digestCanonicalValue(semanticProjection(e), "Evidence")}`;
const ev = JSON.parse(readFileSync(process.argv[2], "utf8"));
const stored = ev.evidence_id, recomputed = computeEvidenceId(ev);
console.log(JSON.stringify({ file: process.argv[2], stored, recomputed, match: stored === recomputed }));
