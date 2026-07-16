"""Generate a deterministic 1 Hz KONSAT telemetry-processing demonstration.

This is a portfolio reconstruction based on the documented PDR/CDR telemetry
interface. It is not original flight software or measured flight data.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sample_telemetry.csv"
SUMMARY_PATH = ROOT / "results" / "telemetry_demo_summary.json"
FIGURE_PATH = ROOT / "docs" / "images" / "telemetry_demo.png"
MISSION_DURATION_S = 120


def pressure_from_altitude(altitude_m: float) -> float:
    return 101_325.0 * (1.0 - altitude_m / 44_330.0) ** 5.255


def build_row(second: int) -> dict[str, str | int | float]:
    altitude_m = 500.0 * math.sin(math.pi * second / MISSION_DURATION_S)
    phase = "ASCENT" if second < MISSION_DURATION_S / 2 else "DESCENT"
    return {
        "mission_time_s": second,
        "packet_count": second + 1,
        "mode": "FLIGHT",
        "state": phase,
        "altitude_m": round(altitude_m, 3),
        "pressure_pa": round(pressure_from_altitude(altitude_m), 3),
        "temperature_c": round(22.0 - 0.0065 * altitude_m, 3),
        "battery_v": round(11.1 - 0.0025 * second, 3),
        "latitude_deg": round(37.866 + second * 0.000002, 6),
        "longitude_deg": round(32.420 + second * 0.000003, 6),
        "gps_altitude_m": round(altitude_m + 2.0, 3),
        "satellites": 10,
        "command_echo": "CALIBRATE" if second == 0 else "NONE",
    }


def main() -> None:
    rows = [build_row(second) for second in range(MISSION_DURATION_S + 1)]
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "evidence_type": "Simulated portfolio demonstration",
        "sample_rate_hz": 1,
        "duration_s": MISSION_DURATION_S,
        "packet_count": len(rows),
        "maximum_altitude_m": max(row["altitude_m"] for row in rows),
        "minimum_battery_v": min(row["battery_v"] for row in rows),
        "note": "Generated data; not measured flight telemetry.",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    times = [row["mission_time_s"] for row in rows]
    fig, axes = plt.subplots(3, 1, figsize=(9, 7.2), sharex=True)
    axes[0].plot(times, [row["altitude_m"] for row in rows], color="#1f4e79", linewidth=2.2)
    axes[0].set_ylabel("Altitude (m)")
    axes[1].plot(times, [row["pressure_pa"] / 1000 for row in rows], color="#5b8c5a", linewidth=2.2)
    axes[1].set_ylabel("Pressure (kPa)")
    axes[2].plot(times, [row["battery_v"] for row in rows], color="#b26a2e", linewidth=2.2)
    axes[2].set_ylabel("Battery (V)")
    axes[2].set_xlabel("Mission time (s)")
    for axis in axes:
        axis.grid(True, alpha=0.25)
    fig.suptitle("KONSAT 1 Hz Telemetry Processing Demonstration", weight="bold")
    fig.text(0.5, 0.005, "Simulated portfolio data - not measured flight telemetry", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.025, 1, 0.97))
    fig.savefig(FIGURE_PATH, dpi=180, metadata={"Software": "KONSAT telemetry demo"})
    plt.close(fig)


if __name__ == "__main__":
    main()

