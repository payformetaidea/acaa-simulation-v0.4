#!/usr/bin/env node
/** Independent JavaScript implementation for M-P1-v1.1 verification. */
const fs = require("fs");

const PATTERN = /^CAU-[0-9]{6}$/;

function extract(manifest) {
  const records = Array.isArray(manifest.cau_records) ? manifest.cau_records : null;
  if (records === null) return { status: "DATA_INTEGRITY_FAIL", m_p1: null };

  const valid = [];
  let invalid = 0;
  for (const record of records) {
    const raw = record && typeof record === "object" ? record.cau_id : undefined;
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

const manifest = JSON.parse(fs.readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(extract(manifest)) + "\n");
