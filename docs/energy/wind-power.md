---
title: Wind Power
source: US DOE Small Wind Guide, Practical Action Wind Energy Guide, Hugh Piggott's Wind Turbine Design
license: Proprietary
last_reviewed: 2026-03-30
tags: wind power, wind turbine, small wind, blade design, tower, charge regulation, wind energy, off grid, alternator
---

Wind power supplements solar nicely — wind often blows strongest at night and in winter when solar output is lowest. But wind is the most variable renewable source. A site that averages 10 mph produces 8x more power than a site averaging 5 mph (power scales with the cube of wind speed). If your site isn't windy, don't invest in wind.

## Is Your Site Viable?

### Minimum Wind Speed

You need an average annual wind speed of at least 9–10 mph (4–4.5 m/s) to justify a small wind turbine. Below that, solar is more cost-effective.

### How to Assess

- **Observation:** If trees are permanently bent, flags fly straight most of the time, or wind is a constant annoyance, you probably have enough wind.
- **Beaufort Scale quick assessment:** If leaves and small branches move constantly (Beaufort 3–4, roughly 8–18 mph), the site is viable.
- **Measurement:** Ideally, mount an anemometer at your planned tower height for several months. At minimum, monitor for the windiest and calmest seasons to understand the range.
- **Terrain:** Hilltops, ridgelines, and open plains are windiest. Valleys, forests, and areas behind buildings create turbulence and reduce effective wind.
- **Height matters enormously.** Wind speed increases with height above ground. At 30 feet, wind is typically 20–30% faster than at 10 feet. At 60 feet, it's 30–50% faster. A taller tower is always worth the investment.

### The Cube Rule

Wind power is proportional to the cube of wind speed. Doubling the wind speed increases power by 8x (2³).

- 5 mph wind: ~15 watts from a small turbine
- 10 mph wind: ~125 watts (8× more)
- 15 mph wind: ~420 watts (27× more)
- 20 mph wind: ~1,000 watts (64× more)

This means a few mph difference in average wind speed makes a massive difference in annual energy production.

## Small Turbine Components

### Blades

Most small turbines use 3 blades. More blades produce more torque at low speeds but have lower maximum RPM (and thus lower peak power).

**Materials:** Carved wood (traditional), PVC pipe (cut lengthwise into airfoil shapes), fiberglass, or carved foam covered in fiberglass.

**Blade diameter** determines how much wind energy you capture. The swept area (the circle the blades trace) is what matters. A turbine with 6-foot blades has a swept area of about 113 square feet. Double the diameter = 4× the swept area = 4× the power.

**Pitch and twist:** Each blade should be thicker and flatter near the hub (where it moves slower) and thinner with more twist at the tips (where it moves faster). This aerodynamic profile maximizes energy extraction. The angle of attack changes along the blade length.

### Generator/Alternator

Converts rotation to electricity.

**Permanent magnet alternator (PMA):** The standard for small wind. Magnets mounted on a rotor spin past copper coils on a stator. Produces AC which is rectified to DC. Can be built from scratch using neodymium magnets and hand-wound coils — Hugh Piggott's designs are widely used and well-documented.

**Car alternator:** Works but is inefficient for wind. Car alternators need 2,000+ RPM to produce useful power — most small wind turbines spin at 200–600 RPM. You'd need a gearbox or pulley system to step up the speed, which adds complexity and friction losses.

**Treadmill motor (permanent magnet DC motor):** Excellent for DIY turbines. These are permanent magnet motors that produce DC directly when spun. They start producing usable voltage at low RPM. Find them on discarded treadmills.

### Tower

The tower gets the turbine above ground-level turbulence into cleaner, faster wind.

**Rule of thumb:** The bottom of the blade sweep should be at least 30 feet above any obstacle within 500 feet. Trees, buildings, and terrain features create turbulence that reduces power and stresses the turbine.

**Tower types:**
- **Guyed pole:** A steel pole or pipe supported by wire guy cables. Cheapest and most practical for DIY. Three or four sets of guys anchored at 60–75% of the tower height work well.
- **Tilt-up tower:** A guyed pole with a hinge at the base. The entire tower tilts down for maintenance. Eliminates climbing. Highly recommended for DIY installations.
- **Freestanding:** A heavy, self-supporting structure. Expensive and requires engineering. Not practical for DIY.

### Charge Controller / Regulation

Wind turbines can't be "turned off" — the wind keeps blowing. You need:

1. **Charge controller:** Regulates charging to prevent battery damage. Many wind charge controllers include a dump load (a resistance heater that absorbs excess power when batteries are full).
2. **Brake/furling system:** In high winds, a mechanism to reduce blade speed and prevent turbine damage. Options include:
   - **Furling tail:** The turbine pivots sideways to the wind, reducing the area presented. Most common on small turbines — works passively.
   - **Blade pitch change:** Blades rotate to spill wind. More complex.
   - **Manual brake:** A switch that short-circuits the generator, stopping the blades electromagnetically. Essential for maintenance.

> **WARNING:** Never disconnect a spinning wind turbine from its load (batteries or dump load) without first braking it. An unloaded turbine overspeeds and self-destructs. Always engage the brake before disconnecting wires.

## DIY Turbine — Basic Approach

A simple, functional wind turbine using salvaged components:

1. **Blades:** Cut 3 blades from 6-inch PVC pipe (each pipe section creates 2 blades). Shape into a rough airfoil. Each blade 2–4 feet long. Bolt to a hub made from a flange or heavy plate.
2. **Generator:** Treadmill motor or purpose-built PMA. Mount behind the blade hub on a frame.
3. **Tail vane:** A flat piece of sheet metal or plywood on a boom behind the generator. Keeps the turbine pointed into the wind. Mount so it can pivot — the tail acts as a furling mechanism in high winds.
4. **Mount on a pipe that fits inside the tower pipe** — the turbine needs to freely rotate (yaw) to track wind direction. Use a bearing or smooth pipe-in-pipe joint.
5. **Tower:** Guyed steel pipe, 20–40 feet tall. Three sets of guy wires at 120-degree spacing.
6. **Wiring:** Run wire from the turbine down the tower (with a drip loop) to the charge controller, then to batteries. Use slip rings or a coiled wire loop at the yaw joint so the turbine can rotate without tangling wires.

## Realistic Expectations

A well-built small turbine (6-foot blade diameter) in a good wind site (12 mph average) produces roughly 100–200 kWh per month. That's enough for basic lighting, communication, phone charging, and small appliances.

In marginal wind (8 mph average), the same turbine produces 30–60 kWh/month — barely worth the effort.

**Wind + solar is the optimal combination** for most off-grid situations. Solar carries the daytime load, wind fills in at night and in storms. Together, they reduce the battery storage needed compared to either alone.
