import csv

#AQI Breakpoints (US EPA Standard)

PM25_BREAKPOINTS = [
    (0.0,  12.0,   0,  50),
    (12.1, 35.4,  51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4,151, 200),
    (150.5,250.4,201, 300),
    (250.5,500.4,301, 500),
]
PM10_BREAKPOINTS = [
    (0,   54,   0,  50),
    (55,  154,  51, 100),
    (155, 254, 101, 150),
    (255, 354, 151, 200),
    (355, 424, 201, 300),
    (425, 604, 301, 500),
]
CO_BREAKPOINTS = [
    (0.0,  4.4,   0,  50),
    (4.5,  9.4,  51, 100),
    (9.5,  12.4, 101, 150),
    (12.5, 15.4, 151, 200),
    (15.5, 30.4, 201, 300),
    (30.5, 50.4, 301, 500),
]
NO2_BREAKPOINTS = [
    (0,   53,   0,  50),
    (54,  100,  51, 100),
    (101, 360, 101, 150),
    (361, 649, 151, 200),
    (650, 1249,201, 300),
    (1250,2049,301, 500),
]
SO2_BREAKPOINTS = [
    (0,   35,   0,  50),
    (36,  75,  51, 100),
    (76,  185, 101, 150),
    (186, 304, 151, 200),
    (305, 604, 201, 300),
    (605, 1004,301, 500),
]
O3_BREAKPOINTS = [
    (0,   54,   0,  50),
    (55,  70,  51, 100),
    (71,  85, 101, 150),
    (86,  105,151, 200),
    (106, 200,201, 300),
]

# AQI Category
def get_category(aqi):
    if aqi <= 50:  return "Good",                            "Air quality is satisfactory."
    if aqi <= 100: return "Moderate",                        "Acceptable air quality."
    if aqi <= 150: return "Unhealthy for Sensitive Groups",  "Sensitive people may be affected."
    if aqi <= 200: return "Unhealthy",                       "Everyone may begin to feel effects."
    if aqi <= 300: return "Very Unhealthy",                  "Health alert: serious effects for everyone."
    return               "Hazardous",                        "Emergency conditions. Everyone is affected."

# Calculate Sub-Index
def calc_aqi(concentration, breakpoints):
    for (c_lo, c_hi, aqi_lo, aqi_hi) in breakpoints:
        if c_lo <= concentration <= c_hi:
            aqi = ((aqi_hi - aqi_lo) / (c_hi - c_lo)) * (concentration - c_lo) + aqi_lo
            return round(aqi)
    return 500

# Simple Reflex Agent
def reflex_agent(sensor_reading):
    """
    Reads current sensor percepts and returns AQI decision.
    No memory or history — pure reflex based on current state.
    """
    pm25 = float(sensor_reading["pm25"])
    pm10 = float(sensor_reading["pm10"])
    co   = float(sensor_reading["co"])
    no2  = float(sensor_reading["no2"])
    so2  = float(sensor_reading["so2"])
    o3   = float(sensor_reading["o3"])

    sub_indices = {
        "PM2.5": calc_aqi(pm25, PM25_BREAKPOINTS),
        "PM10":  calc_aqi(pm10, PM10_BREAKPOINTS),
        "CO":    calc_aqi(co,   CO_BREAKPOINTS),
        "NO2":   calc_aqi(no2,  NO2_BREAKPOINTS),
        "SO2":   calc_aqi(so2,  SO2_BREAKPOINTS),
        "O3":    calc_aqi(o3,   O3_BREAKPOINTS),
    }

    overall_aqi = max(sub_indices.values())
    dominant    = max(sub_indices, key=sub_indices.get)
    category, advice = get_category(overall_aqi)

    return overall_aqi, category, advice, dominant, sub_indices

# Read Sensor File & Run Agent
def run(filename="sensor_data.csv"):
    print("=" * 60)
    print("  SIMPLE REFLEX AGENT — AQI Monitor")
    print("=" * 60)

    with open(filename, newline="") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        aqi, category, advice, dominant, sub_indices = reflex_agent(row)
        print(f"\n  Location : {row['location']}")
        print(f"  AQI      : {aqi}")
        print(f"  Category : {category}")
        print(f"  Advice   : {advice}")
        print(f"  Dominant : {dominant} (sub-index: {sub_indices[dominant]})")
        print(f"  Sub-indices: " + "  |  ".join([f"{k}:{v}" for k, v in sub_indices.items()]))
        print(f"  {'-'*56}")

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Location':<25} {'AQI':>5}  Category")
    print(f"  {'-'*56}")
    for row in rows:
        aqi, category, _, _, _ = reflex_agent(row)
        print(f"  {row['location']:<25} {aqi:>5}  {category}")
    print(f"{'='*60}")

if __name__ == "__main__":
    run("sensor_data.csv")
