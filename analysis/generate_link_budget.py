"""Generate a reproducible free-space link-budget profile for KONSAT."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "design_inputs.json"
PROFILE_PATH = ROOT / "data" / "link_budget_profile.csv"
SUMMARY_PATH = ROOT / "results" / "link_budget_summary.json"
FIGURE_PATH = ROOT / "docs" / "images" / "link_budget_profile.png"
SPEED_OF_LIGHT_M_S = 299_792_458.0


def fspl_db(distance_m: float, frequency_hz: float) -> float:
    """Return free-space path loss in dB."""
    if distance_m <= 0 or frequency_hz <= 0:
        raise ValueError("Distance and frequency must be positive.")
    wavelength_m = SPEED_OF_LIGHT_M_S / frequency_hz
    return 20.0 * math.log10(4.0 * math.pi * distance_m / wavelength_m)


def evaluate(distance_m: float, inputs: dict[str, float]) -> dict[str, float]:
    path_loss_db = fspl_db(distance_m, inputs["frequency_hz"])
    received_power_dbm = (
        inputs["tx_power_dbm"]
        + inputs["tx_antenna_gain_dbi"]
        + inputs["rx_antenna_gain_dbi"]
        - path_loss_db
        - inputs["implementation_loss_db"]
    )
    margin_db = received_power_dbm - inputs["receiver_sensitivity_dbm"]
    return {
        "distance_m": distance_m,
        "fspl_db": path_loss_db,
        "received_power_dbm": received_power_dbm,
        "link_margin_db": margin_db,
    }


def main() -> None:
    inputs = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    distances = []
    current = inputs["profile_start_m"]
    while current <= inputs["profile_stop_m"] + 1e-9:
        distances.append(float(current))
        current += inputs["profile_step_m"]

    rows = [evaluate(distance, inputs) for distance in distances]
    reference = evaluate(inputs["reference_distance_m"], inputs)

    with PROFILE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["distance_m", "fspl_db", "received_power_dbm", "link_margin_db"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: f"{value:.6f}" for key, value in row.items()})

    summary = {
        "model": "Ideal free-space analytical baseline",
        "reference_distance_m": reference["distance_m"],
        "frequency_hz": inputs["frequency_hz"],
        "tx_power_dbm": inputs["tx_power_dbm"],
        "tx_antenna_gain_dbi": inputs["tx_antenna_gain_dbi"],
        "rx_antenna_gain_dbi": inputs["rx_antenna_gain_dbi"],
        "implementation_loss_db": inputs["implementation_loss_db"],
        "receiver_sensitivity_dbm": inputs["receiver_sensitivity_dbm"],
        "fspl_db": round(reference["fspl_db"], 6),
        "received_power_dbm": round(reference["received_power_dbm"], 6),
        "link_margin_db": round(reference["link_margin_db"], 6),
        "assumption_note": inputs["assumption_note"],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(
        [row["distance_m"] / 1000.0 for row in rows],
        [row["received_power_dbm"] for row in rows],
        color="#1f4e79",
        linewidth=2.4,
        label="Predicted received power",
    )
    ax.axhline(
        inputs["receiver_sensitivity_dbm"],
        color="#b03a2e",
        linestyle="--",
        linewidth=1.8,
        label="Receiver sensitivity",
    )
    ax.scatter(
        [reference["distance_m"] / 1000.0],
        [reference["received_power_dbm"]],
        color="#138d75",
        zorder=3,
        label=f"1 km margin: {reference['link_margin_db']:.2f} dB",
    )
    ax.set_title("KONSAT 2.4 GHz Ideal Free-Space Link Profile", weight="bold")
    ax.set_xlabel("Separation distance (km)")
    ax.set_ylabel("Received power (dBm)")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=180, metadata={"Software": "KONSAT reproducible analysis"})
    plt.close(fig)


if __name__ == "__main__":
    main()

