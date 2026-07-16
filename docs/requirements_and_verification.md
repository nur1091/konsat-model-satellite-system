# Requirements and Verification Plan

## Traceability approach

The matrix in `data/requirements_traceability.csv` focuses on communication, ground control, electrical interfaces and the corrected RF analysis. It does not reproduce every competition requirement from the source reviews.

## Verification levels

| Evidence state | Meaning |
|---|---|
| Design evidence | The architecture or selection is documented in PDR/CDR material. |
| Analysis evidence | A repeatable calculation supports the requirement. |
| Planned verification | A method is defined but no result is available. |
| Open | A gap, conflict or missing evidence prevents closure. |

## Recommended test sequence

1. **Interface inspection** - confirm part numbers, supply voltages, RF connectors, I2C levels and UART pin allocation.
2. **Unit tests** - exercise the RTC, XBee radio, serial link and telemetry-storage functions independently.
3. **Telemetry schema test** - inject known values and verify every packet field, engineering unit and command echo.
4. **Simulation-mode test** - stream a pressure-profile CSV at 1 Hz and verify state transitions and altitude response.
5. **End-to-end radio test** - record distance, RSSI, packet delivery ratio, missed packet count and latency.
6. **Power test** - measure every operating mode, regulator efficiency, peak current and two-hour endurance.
7. **Integrated functional test** - verify commands, live plots, CSV output and reset recovery.

## Minimum telemetry test record

A defensible telemetry test should record:

- UTC and mission time
- Transmitted and received packet counters
- RSSI or available radio-quality indicator
- Packet delivery ratio and consecutive losses
- Command, command echo and response latency
- Telemetry values and expected injected values
- Test distance, antenna orientation, obstacles and weather
- Payload and ground-station power state

## Current closure status

The available files support PDR/CDR design evidence. They do not support closure of communication range, power endurance or end-to-end ground-station verification.
