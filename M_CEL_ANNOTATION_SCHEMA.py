"""Frozen H-AICR ground-truth annotation schema."""
from dataclasses import dataclass

LABELS = ("consumer", "producer", "joint", "uncertain")

@dataclass(frozen=True)
class Annotation:
    record_uuid: str
    annotator_id: str
    label: str
    confidence: float
    rationale: str
    annotated_at_utc: str
    source_version: str

    def validate(self) -> None:
        if self.label not in LABELS:
            raise ValueError("INVALID_ANNOTATION_LABEL")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("INVALID_ANNOTATION_CONFIDENCE")
        if not self.record_uuid or not self.annotator_id:
            raise ValueError("ANNOTATION_ID_MISSING")
        if not self.source_version:
            raise ValueError("ANNOTATION_SOURCE_VERSION_MISSING")

ANNOTATION_SCHEMA_VERSION = "H-AICR-GT-1.0"
