from datetime import datetime, timezone

import numpy as np
from sgp4.api import Satrec, jday

# Read the saved TLE (name line, line 1, line 2), ignoring blank lines
with open("data/iss_tle.txt") as f:
    name, line1, line2 = [ln.strip() for ln in f if ln.strip()][:3]

sat = Satrec.twoline2rv(line1, line2)

# Current time in UTC, converted to the Julian date format SGP4 expects
now = datetime.now(timezone.utc)
jd, fr = jday(now.year, now.month, now.day,
              now.hour, now.minute, now.second + now.microsecond / 1e6)

err, r, v = sat.sgp4(jd, fr)

radius = np.linalg.norm(r)
speed = np.linalg.norm(v)
tle_age_days = (jd + fr) - (sat.jdsatepoch + sat.jdsatepochF)

print(f"Satellite:   {name}")
print(f"Error code:  {err}  (0 = success)")
print(f"Position:    {r} km (TEME frame)")
print(f"Velocity:    {v} km/s")
print(f"Radius:      {radius:.1f} km")
print(f"Altitude:    {radius - 6378.137:.1f} km (approx, above equatorial radius)")
print(f"Speed:       {speed:.2f} km/s")
print(f"TLE age:     {tle_age_days:.2f} days")