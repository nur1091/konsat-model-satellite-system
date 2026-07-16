# System Architecture

## Architecture scope

The available PDR and CDR files define KONSAT as a model-satellite concept with payload, sensor, communication and data handling, ground-control, electrical, flight-software, descent-control and structural subsystems. This repository focuses on the communication, ground-station and electrical interfaces that formed Nisanur Kayğusuz's assigned responsibility.

## Telemetry and command path

```mermaid
flowchart LR
    S["Sensors"] -->|I2C/UART| P["Raspberry Pi Zero 2 W"]
    P -->|UART| R1["Payload XBee 3"]
    R1 -->|2.4 GHz| R2["Ground XBee 3"]
    R2 -->|USB serial| Q["Qt GCS"]
    Q --> V["Plots and CSV"]
    Q -->|Commands| R2
```

The baseline calls for one telemetry packet per second. Intended fields include mission time, altitude, pressure, temperature, battery voltage, command echo, GPS latitude, longitude, altitude and satellite count. The ground-station concept also includes calibration, mechanism commands and simulation-profile playback.

## Processing and sensor interfaces

| Interface | Design allocation |
|---|---|
| I2C | BMP280, MPU6050, HMC5883L and RTC concepts |
| UART | XBee telemetry radio and GPS |
| CSI | Raspberry Pi camera concept |
| USB | Second camera and ground XBee adapter |
| Local storage | Flight data and video on microSD |

## Electrical concept

```mermaid
flowchart LR
    B["3S NCR18650GA battery concept"] --> SW["Switch and protection - TBD"]
    SW --> REG["LM2596 5 V rail"]
    REG --> PI["Raspberry Pi Zero 2 W"]
    PI --> LOADS["Sensors, cameras and interfaces"]
```

The design-review material proposes three 3.6 V nominal cells in series and an LM2596-based 5 V supply. It does not contain a complete measured load budget, protection design, thermal result or two-hour endurance record.

## Interface risks

1. **RF connector compatibility:** XB3-24Z8ST-J uses an RPSMA antenna connection, while APARN1204-S2450 is a surface-mount patch antenna. A compatible RF feed/carrier solution or a different antenna must be selected.
2. **Analog measurement:** Raspberry Pi Zero 2 W has no native analog input. The battery-voltage divider requires an external ADC or another defined measurement device.
3. **I2C voltage level:** DS1307 modules are commonly associated with a 5 V rail. Pull-up voltage and Raspberry Pi 3.3 V GPIO compatibility must be verified.
4. **Power distribution:** Supplying every peripheral from Raspberry Pi rails requires a verified current budget, start-up analysis and fault isolation.
5. **Ground antenna identity:** The design uses an AS-2-17 17 dBi value, but the exact manufacturer data and connector/polarization details must be confirmed before procurement.
6. **Simultaneous imaging:** Dual-camera recording must be verified against processor, USB, storage, thermal and power limits.

## Evidence boundary

The architecture above is reconstructed from PDR/CDR design evidence. No surviving schematic, wiring harness, executable flight software, executable GCS project or end-to-end hardware test record was supplied.

