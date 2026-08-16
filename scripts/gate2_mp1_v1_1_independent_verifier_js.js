#!/usr/bin/env node
/** Independent JavaScript implementation for M-P1-v1.1 verification. */
const fs = require("fs");

const PATTERN = /^CAU-[0-9]{6}$/;

function extract(artifact) {
  if (artifact === null || typeof artifact !== "object" || Array.isArray(artifact)) {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }

  if (!Object.prototype.hasOwnProperty.call(artifact, "records")) {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }
  const records = artifact.records;
  if (!Array.isArray(records)) return { status: "DATA_INTEGRITY_FAIL", m_p1: null };

  if (!Object.prototype.hasOwnProperty.call(artifact, "aggregate") ||
      artifact.aggregate === null ||
      typeof artifact.aggregate !== "object" ||
      Array.isArray(artifact.aggregate)) {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }
  const cauRecords = artifact.aggregate.cau_records;
  if (!Number.isInteger(cauRecords) || typeof cauRecords === "boolean") {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }
  if (cauRecords !== records.length) {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }

  const valid = [];
  let invalid = 0;
  for (const record of records) {
    const raw = record && typeof record === "object" && !Array.isArray(record)
      ? record.cau_id
      : undefined;
    if (typeof raw !== "string" || raw.trim() === "") {
      invalid += 1;
      continue;
    }
    const candidate = raw.trim().toUpperCase();
    if (PATTERN.test(candidate)) valid.push(candidate);
    else invalid += 1;
  }

  if (records.length > 0 && invalid === records.length) {
    return { status: "DATA_INTEGRITY_FAIL", m_p1: null };
  }
  return { status: "VALID", m_p1: new Set(valid).size };
}

let artifact;
try {
  artifact = JSON.parse(fs.readFileSync(0, "utf8"));
} catch (error) {
  process.stdout.write(JSON.stringify({ status: "DATA_INTEGRITY_FAIL", m_p1: null }) + "\n");
  process.exit(1);
}

process.stdout.write(JSON.stringify(extract(artifact)) + "\n");
