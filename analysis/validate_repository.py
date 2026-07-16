"""Validate KONSAT traceability data and generated RF results."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_REQUIREMENT_STATES = {
    "Design evidence",
    "Analysis evidence",
    "Planned verification",
    "Open",
}
ALLOWED_COMPONENT_STATES = {
    "Design evidence",
    "Analysis evidence",
    "Planned verification",
    "Open",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_unique(rows: list[dict[str, str]], field: str, label: str) -> None:
    values = [row[field].strip() for row in rows]
    if not values or any(not value for value in values):
        raise ValueError(f"{label} contains an empty {field}.")
    if len(values) != len(set(values)):
        raise ValueError(f"{label} contains duplicate {field} values.")


def main() -> None:
    requirements = read_csv(ROOT / "data" / "requirements_traceability.csv")
    validate_unique(requirements, "id", "Requirements matrix")
    invalid_requirements = {
        row["evidence_status"] for row in requirements
    } - ALLOWED_REQUIREMENT_STATES
    if invalid_requirements:
        raise ValueError(f"Invalid requirement evidence states: {sorted(invalid_requirements)}")

    components = read_csv(ROOT / "data" / "component_selection.csv")
    validate_unique(components, "function", "Component table")
    invalid_components = {
        row["evidence_level"] for row in components
    } - ALLOWED_COMPONENT_STATES
    if invalid_components:
        raise ValueError(f"Invalid component evidence states: {sorted(invalid_components)}")

    summary = json.loads(
        (ROOT / "results" / "link_budget_summary.json").read_text(encoding="utf-8")
    )
    expected = {
        "fspl_db": 100.052008,
        "received_power_dbm": -73.052008,
        "link_margin_db": 29.947992,
    }
    for field, expected_value in expected.items():
        actual = float(summary[field])
        if abs(actual - expected_value) > 1e-5:
            raise ValueError(f"Unexpected {field}: {actual} != {expected_value}")

    telemetry_rows = read_csv(ROOT / "data" / "sample_telemetry.csv")
    if len(telemetry_rows) != 121:
        raise ValueError(f"Unexpected telemetry row count: {len(telemetry_rows)}")
    times = [int(row["mission_time_s"]) for row in telemetry_rows]
    packets = [int(row["packet_count"]) for row in telemetry_rows]
    if times != list(range(121)) or packets != list(range(1, 122)):
        raise ValueError("Telemetry time or packet sequence is not continuous at 1 Hz.")

    telemetry_summary = json.loads(
        (ROOT / "results" / "telemetry_demo_summary.json").read_text(encoding="utf-8")
    )
    if telemetry_summary["evidence_type"] != "Simulated portfolio demonstration":
        raise ValueError("Telemetry evidence boundary is missing or incorrect.")

    required_files = [
        ROOT / "README.md",
        ROOT / "docs" / "images" / "link_budget_profile.png",
        ROOT / "docs" / "images" / "telemetry_demo.png",
        ROOT / "docs" / "images" / "original_artifacts" / "communication_chain.png",
        ROOT / "docs" / "images" / "original_artifacts" / "telemetry_fields_1.jpg",
        ROOT / "docs" / "images" / "original_artifacts" / "telemetry_fields_2.jpg",
        ROOT / "data" / "link_budget_profile.csv",
        ROOT / "data" / "telemetry_schema.csv",
        ROOT / "data" / "sample_telemetry.csv",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required repository files: {missing}")

    print(
        f"Validated {len(requirements)} requirements, {len(components)} components, "
        f"{len(telemetry_rows)} telemetry packets and the reference RF analysis."
    )


if __name__ == "__main__":
    main()
