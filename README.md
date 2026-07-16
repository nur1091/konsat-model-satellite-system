# KONSAT Model Satellite System Design

[![Validate design](https://github.com/nur1091/konsat-model-satellite-system/actions/workflows/validate.yml/badge.svg)](https://github.com/nur1091/konsat-model-satellite-system/actions/workflows/validate.yml)

Systems-engineering portfolio for a 2.4 GHz XBee-based CanSat concept covering telemetry, ground control, electrical interfaces, requirements traceability and reproducible RF link-budget analysis.

## Overview

KONSAT was developed as a 2024-2025 academic spacecraft-system-design project. The team advanced the concept through Preliminary Design Review (PDR) and Critical Design Review (CDR), addressing the payload, descent-control mechanism, sensors, communication and data handling, ground control, electrical power and flight-software concepts.

This repository converts the surviving design-review material into a concise and reviewable engineering portfolio. It intentionally separates documented design evidence from planned verification work.

## My contribution

As the team member responsible for the **communication system, ground station and electrical systems**, I contributed to:

- The 2.4 GHz XBee telemetry architecture and component trade studies.
- Payload-to-ground-station interfaces and data flow.
- Telemetry-field, command and 1 Hz reporting concepts.
- Ground-station visualization, CSV logging and simulation-mode requirements.
- Electrical distribution and subsystem-interface definition.
- PDR/CDR documentation and requirements-based design reviews.

## Project objectives

- Define a model-satellite architecture traceable to competition requirements.
- Transmit sensor and mission data to a portable ground station at 1 Hz.
- Support command exchange, real-time visualization and CSV recording.
- Select compatible communication, processing, sensing and power components.
- Evaluate the line-of-sight RF link with a transparent, reproducible model.
- Establish verification methods before implementation and flight testing.

## System architecture

```mermaid
flowchart TD
    SENS["Sensors and cameras"] --> PI["Raspberry Pi Zero 2 W"]
    RTC["RTC and mission time"] --> PI
    PI --> SD["Onboard storage"]
    PI -->|UART| XB1["Payload XBee 3"]
    XB1 -->|2.4 GHz link| XB2["Ground XBee 3"]
    XB2 -->|USB serial| GCS["Qt ground station"]
    GCS --> OUT["Live plots, commands and CSV"]
```

The architecture is a design baseline, not an as-flown configuration. Hardware-interface risks and unverified assumptions are listed in [System Architecture](docs/system_architecture.md).

## Original PDR/CDR design artifacts

The following visuals are preserved from the original Preliminary and Critical Design Reviews and are limited to my assigned responsibility: communication, ground station and electrical systems. The original Turkish labels are retained for authenticity; the images are design evidence, not hardware-test or flight-test evidence.

| Preliminary Design Review | Critical Design Review |
|---|---|
| ![PDR communication and data-handling architecture](docs/images/design_review/pdr_communication_architecture.png)<br><sub>Communication and data-handling architecture</sub> | ![CDR communication architecture](docs/images/design_review/cdr_communication_architecture.png)<br><sub>Communication and data-handling architecture</sub> |
| ![PDR payload and ground-station data flow](docs/images/design_review/pdr_ground_station_data_flow.png)<br><sub>Payload and ground-station data flow</sub> | ![CDR ground-station interfaces](docs/images/design_review/cdr_ground_station_interfaces.png)<br><sub>Ground-station interfaces</sub> |
| ![PDR electrical power distribution](docs/images/design_review/pdr_power_distribution.png)<br><sub>Electrical power-distribution concept</sub> | *No finalized CDR electrical power-distribution visual survives in the supplied deck.* |

## Selected design baseline

| Function | Selected element | Primary interface |
|---|---|---|
| Main processing | Raspberry Pi Zero 2 W | I2C, UART, SPI, USB, CSI |
| Telemetry radio | Digi XBee 3 XB3-24Z8ST-J | UART / 2.4 GHz Zigbee 3.0 |
| Payload antenna concept | Abracon APARN1204-S2450 | 2.4 GHz RF interface |
| Mission time | DS1307 RTC concept | I2C |
| Pressure and temperature | BMP280 | I2C |
| Motion sensing | MPU6050 + HMC5883L | I2C |
| Position | GY-NEO6MV2 GPS | UART |
| Power conversion | LM2596 buck converter concept | 10.8 V nominal to 5 V |
| Energy storage | Three NCR18650GA cells in series | 3S battery concept |
| Ground software | Qt / C++ concept | USB serial, live plots, CSV |

See [Component Selection](data/component_selection.csv) for the complete design table and known interface risks.

## Reproducible RF analysis

The PDR/CDR material contained a valid 1 km free-space path-loss result but combined it with transmit-power and antenna-gain values that did not match the selected radio and payload antenna. This repository normalizes the calculation to the selected design baseline:

| Parameter | Baseline value |
|---|---:|
| Frequency | 2.4 GHz |
| Distance | 1.0 km |
| XBee transmit power | +8 dBm |
| Payload antenna gain | +2 dBi |
| Ground antenna gain | +17 dBi |
| Free-space path loss | 100.05 dB |
| Predicted received power | -73.05 dBm |
| Receiver sensitivity | -103 dBm |
| Ideal link margin | 29.95 dB |

![RF link profile](docs/images/link_budget_profile.png)

The result is an **ideal line-of-sight analytical value**. It excludes cable, connector, polarization, pointing, enclosure, multipath and implementation losses because these were not measured. It is not a range-test or flight-test result. See [Methodology and Assumptions](docs/methodology.md).

## Requirements and verification

The traceability dataset distinguishes four states:

- `Design evidence`: addressed in the PDR/CDR architecture.
- `Analysis evidence`: supported by a reproducible calculation in this repository.
- `Planned verification`: a test method is defined but no result is available.
- `Open`: the available evidence shows a gap or unresolved interface.

Review the [Requirements Traceability Matrix](data/requirements_traceability.csv) and [Verification Plan](docs/requirements_and_verification.md).

## Repository structure

```text
.github/workflows/   Automated design validation
analysis/            RF calculation and repository checks
data/                Inputs, component selections and traceability
docs/                Architecture, methodology and design-review notes
  images/design_review/  Curated original PDR/CDR artifacts
results/             Generated RF summary
```

The original PDR and CDR files are not redistributed because they contain student identifiers, team information and draft material. Their relevant engineering content is summarized here without presenting the full files as implementation evidence.

## Reproduce the analysis

```bash
python -m pip install -r requirements.txt
python analysis/generate_link_budget.py
python analysis/validate_repository.py
```

The GitHub Actions workflow regenerates the link-budget dataset and checks the committed requirements, component and result files on every push.

## Key engineering findings

- The corrected ideal 1 km link closes analytically with approximately 29.95 dB margin before implementation losses.
- The selected XBee variant uses an RPSMA RF port, while the APARN1204-S2450 is a surface-mount patch antenna; the final RF feed and carrier-board implementation therefore remain open.
- The two-hour operating-duration requirement is not verified because a measured load profile and complete power budget are absent.
- The DS1307/Raspberry Pi I2C voltage interface requires hardware-level verification before integration.
- Live telemetry, CSV logging and simulation mode are defined as ground-station requirements but no executable GCS source or test record survives in the supplied files.

## Verification boundary

- Completed: PDR/CDR design definition, component trade studies, interface concept and corrected analytical RF model.
- Not evidenced: assembled flight hardware, environmental qualification, end-to-end telemetry test, measured power endurance or flight validation.
- The repository must therefore be read as a **design and analysis portfolio**, not a flight-qualified CanSat implementation.

## Future work

- Select and validate an antenna/feed implementation compatible with the XBee RPSMA interface.
- Build an end-to-end XBee range-test setup and record RSSI, packet delivery and packet loss.
- Implement the Qt ground station with serial parsing, live plots, commands and CSV logging.
- Complete a measured power budget and a two-hour endurance test.
- Verify I2C voltage compatibility and power-rail current limits.
- Run functional, vibration, shock, deployment and recovery tests against the traceability matrix.

## Tools and technologies

Raspberry Pi Zero 2 W, Digi XBee 3, Zigbee 3.0, UART, I2C, SPI, Qt/C++, Python, telemetry, ground-station design, requirements traceability, PDR/CDR and RF link-budget analysis.

## Author

**Nisanur Kayğusuz**  
Aerospace Engineer  
Necmettin Erbakan University  

[LinkedIn](https://www.linkedin.com/in/nisanur-kay%C4%9Fusuz-62569b1ba/) · [Email](mailto:nisanurkaygusuz0625@gmail.com)
