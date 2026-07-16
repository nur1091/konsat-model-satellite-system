# Methodology and Assumptions

## Evidence method

The repository was reconstructed from the surviving 60-page PDR and 86-slide CDR files. Each claim is classified as design evidence, analysis evidence, planned verification or open. Planned behavior is not presented as implemented functionality.

## Corrected RF baseline

The free-space path loss is calculated as:

```text
FSPL(dB) = 20 log10(4 pi d / lambda)
lambda = c / f
```

Received power and link margin are calculated as:

```text
Pr(dBm) = Pt + Gt + Gr - FSPL - Limplementation
Margin(dB) = Pr - ReceiverSensitivity
```

The baseline uses:

- Frequency: 2.4 GHz
- Transmit power: +8 dBm for the selected non-PRO XBee 3 design point
- Payload antenna gain: +2 dBi typical peak gain from the selected APARN1204-S2450 concept
- Ground antenna gain: +17 dBi from the PDR/CDR design assumption
- Receiver sensitivity: -103 dBm
- Reference distance: 1 km
- Implementation loss: 0 dB because no measurements are available

The implementation-loss setting makes this an optimistic analytical baseline. It must not be interpreted as expected field performance.

## Why the PDR/CDR calculation was normalized

The original design-review link budget used a correct 1 km free-space path loss of approximately 100.04 dB but combined it with 20 dBm transmit power and 12 dBi payload gain. Those values do not match the selected non-PRO XB3-24Z8ST-J radio (+8 dBm) and APARN1204-S2450 antenna (+2 dBi typical peak gain). The repository therefore regenerates the result from one internally consistent assumption set.

## Excluded losses and effects

- Cable and connector loss
- Polarization mismatch
- Antenna pointing error
- Payload enclosure and structural shadowing
- Ground reflections and multipath
- Fresnel-zone obstruction
- Receiver implementation and interference margin
- Regulatory EIRP constraints for the operating region

These terms require a finalized RF implementation, deployment geometry and measurement plan.

## Reproducibility

`analysis/generate_link_budget.py` reads `data/design_inputs.json` and creates:

- `data/link_budget_profile.csv`
- `results/link_budget_summary.json`
- `docs/images/link_budget_profile.png`

`analysis/validate_repository.py` verifies traceability states, unique identifiers, component evidence classes and the reference RF metrics.

## Telemetry demonstrator

`demo/generate_telemetry_demo.py` reconstructs the documented 1 Hz telemetry and CSV-logging concept as an executable portfolio demonstration. It creates a deterministic 120-second ascent/descent profile with altitude, pressure, temperature, battery, GPS, packet-counter and command-echo fields.

The resulting CSV and plot are synthetic. They demonstrate data handling and traceability only; they are not original flight software, radio-test data or measured mission telemetry.
