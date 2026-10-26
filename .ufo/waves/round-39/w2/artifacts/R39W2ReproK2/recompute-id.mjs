import { readFileSync } from "node:fs";
import { digestCanonicalValue } from "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js";

const path = process.argv[2];
const evidence = JSON.parse(readFileSync(path, "utf8"));

// semanticProjection, transcribed from rea-agents 6.5.0 dist/domain/evidence.js:156-180
const semanticProjection = (e) => ({
  subject: e.subject === null ? null : {
    digest: e.subject.digest,
    format: e.subject.format,
    architecture: e.subject.architecture,
  },
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

const id = `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`;
process.stdout.write(JSON.stringify({
  stored: evidence.evidence_id,
  recomputed: id,
  match: id === evidence.evidence_id,
}) + "\n");
