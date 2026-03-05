# Simple Reflex Agent — AQI Monitor

**AI Programming Assignment 2 — Group Assignment**

## What is a Simple Reflex Agent?

A simple reflex agent acts only on **current sensor input** — it has no memory of past states. It reads the environment, applies rules, and produces an output.
Sensors → Percept → Condition-Action Rules → Action

In this project:
- **Sensors** → CSV file with pollutant readings (PM2.5, PM10, CO, NO2, SO2, O3)
- **Percept** → Current pollution levels for a location
- **Rules** → EPA AQI breakpoint formulas
- **Action** → Report AQI value + health category + advice


## What is AQI?

The **Air Quality Index (AQI)** is a number from 0–500 that tells how clean or polluted the air is.

| AQI Range | Category | Health Implication |
|---|---|---|
| 0 – 50 | Good | Satisfactory, no risk |
| 51 – 100 | Moderate | Acceptable quality |
| 101 – 150 | Unhealthy for Sensitive Groups | Sensitive people affected |
| 151 – 200 | Unhealthy | Everyone may feel effects |
| 201 – 300 | Very Unhealthy | Health alert for all |
| 301 – 500 | Hazardous | Emergency conditions |

---

## Pollutants Monitored

| Pollutant | Unit | Description |
|---|---|---|
| PM2.5 | µg/m³ | Fine particulate matter |
| PM10 | µg/m³ | Coarse particulate matter |
| CO | ppm | Carbon monoxide |
| NO2 | ppb | Nitrogen dioxide |
| SO2 | ppb | Sulfur dioxide |
| O3 | ppb | Ozone |

---

## How to Run

### Requirements
No external libraries needed — pure Python 3.

### Steps
1. Make sure `sensor_data.csv` is in the same folder as `aqi_agent.py`
2. Run:
```bash
python aqi_agent.py
```

## Sample Output

```
============================================================
  SIMPLE REFLEX AGENT — AQI Monitor
============================================================

  Location : Hyderabad_Center
  AQI      : 125
  Category : Unhealthy for Sensitive Groups
  Advice   : Sensitive people may be affected.
  Dominant : PM2.5 (sub-index: 125)
  Sub-indices: PM2.5:125  |  PM10:63  |  CO:9  |  NO2:30  |  SO2:18  |  O3:52
  --------------------------------------------------------

  Location : Hyderabad_Market
  AQI      : 206
  Category : Very Unhealthy
  Advice   : Health alert: serious effects for everyone.
  Dominant : PM2.5 (sub-index: 206)
  --------------------------------------------------------

============================================================
  SUMMARY
============================================================
  Location                    AQI  Category
  --------------------------------------------------------
  Hyderabad_Center            125  Unhealthy for Sensitive Groups
  Hyderabad_Industrial        185  Unhealthy
  Hyderabad_Suburbs            95  Moderate
  Hyderabad_Highway           172  Unhealthy
  Hyderabad_Market            206  Very Unhealthy
  Hyderabad_Lake_Area         142  Unhealthy for Sensitive Groups
  ...
============================================================
```

---

## How the Agent Works

1. **Reads** each row from `sensor_data.csv` (one row = one location's sensor data)
2. **Calculates** a sub-index AQI for each of the 6 pollutants using EPA breakpoint formulas
3. **Takes the maximum** sub-index as the overall AQI (EPA standard)
4. **Maps** the AQI to a health category and advice message
5. **Reports** results for every location

---

## Dataset Format

The `sensor_data.csv` file should have these columns:
```
location, pm25, pm10, co, no2, so2, o3
```
You can add more rows for more locations — the agent handles any number of entries.

## Files

| File | Description |
|---|---|
| `aqi_agent.py` | Simple reflex agent implementation |
| `sensor_data.csv` | Sample sensor dataset (10 Hyderabad locations) |
| `README.md` | This file |

---

## References
- [US EPA AQI Basics](https://www.airnow.gov/aqi/aqi-basics/)
- [AQI Calculation Tutorial](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
