---
title: Solar Power Basics
source: US DOE Solar Energy Guide, Off-Grid Solar Design Manual, Appropriate Technology Library
license: Proprietary
last_reviewed: 2026-03-30
tags: solar, solar panel, charge controller, battery, wiring, off grid, photovoltaic, inverter, solar power, 12V, energy
---

Solar is the most accessible renewable energy source for off-grid situations. No moving parts, no fuel, minimal maintenance. A single 100-watt panel keeps batteries charged for lighting, radio, and small electronics. Understanding the basics lets you set up, maintain, and troubleshoot a system with salvaged or pre-purchased components.

## How Solar Panels Work

Sunlight hits silicon cells in the panel, knocking electrons loose. Those electrons flow through a circuit as direct current (DC) electricity. More sunlight = more electricity. No sunlight = no electricity. It's that simple.

**Key specs on every panel:**
- **Watts (W):** Maximum power output in ideal conditions (full sun, cool panel). A 100W panel produces 100 watts at peak. Real-world output is typically 70–80% of rated wattage.
- **Voltage (Vmp):** Operating voltage, typically 17–22V for a "12V" panel. This is higher than 12V because the charge controller needs overhead voltage to charge a 12V battery.
- **Current (Imp):** Operating current in amps. Watts = Volts × Amps.

## Basic System Components

### 1. Solar Panel(s)

**Monocrystalline:** Black cells, highest efficiency (20–22%), most expensive. Best for limited space.

**Polycrystalline:** Blue cells, slightly lower efficiency (15–17%), cheaper. Good balance of cost and performance.

**Thin-film/Flexible:** Lightweight, bendable, lowest efficiency (10–13%). Good for portable setups, poor for permanent installations needing maximum output.

**Sizing:** A 100W panel in decent sun (5 peak sun hours/day average) produces roughly 400–500 watt-hours per day. That's enough to charge phones, run LED lights, and power a radio. For more demand, add more panels.

### 2. Charge Controller

Sits between the panels and the batteries. Regulates voltage and current to prevent overcharging (which destroys batteries).

**PWM (Pulse Width Modulation):** Cheaper, simpler. Works well when panel voltage closely matches battery voltage. Less efficient — wastes 20–30% of potential power in some configurations.

**MPPT (Maximum Power Point Tracking):** More expensive, more efficient. Converts excess panel voltage into extra charging current. Gets 15–30% more energy from the same panels compared to PWM. Worth the cost for any serious system.

**Sizing:** The charge controller must handle the maximum current from your panels. A 100W panel at 18V produces about 5.5 amps. A 200W array produces about 11 amps. Size your controller with a 25% safety margin above your maximum array current.

### 3. Battery Bank

Stores energy for use when the sun isn't shining.

**Lead-acid (flooded):** Cheapest, widely available (car batteries, golf cart batteries, marine deep-cycle). Deep-cycle batteries are designed for repeated discharge/recharge — car batteries are not (they're designed for short high-current bursts). Use deep-cycle if possible. Lifespan: 3–5 years with proper care. Only discharge to 50% capacity — discharging below 50% dramatically shortens lifespan.

**AGM (Absorbed Glass Mat):** Sealed lead-acid. No maintenance, no spills, can mount in any position. More expensive than flooded. Same 50% discharge rule. Lifespan: 4–7 years.

**Lithium (LiFePO4):** Most expensive upfront but longest-lasting (10+ years). Can discharge to 80–90% capacity without damage. Lighter weight. No maintenance. The best option if you can afford it or salvage from electric vehicles.

**Sizing:** Battery capacity is measured in amp-hours (Ah). A 100Ah 12V battery stores 1,200 watt-hours (100Ah × 12V). With the 50% discharge rule for lead-acid, you can use 600Wh before recharging. Match your battery bank to your daily usage plus a reserve for cloudy days.

### 4. Inverter (Optional)

Converts 12V DC (from batteries) to 120V AC (standard household outlets). Needed only if you're running AC appliances.

**Pure sine wave:** Clean power output. Required for sensitive electronics (computers, medical devices, variable-speed motors). More expensive.

**Modified sine wave:** Cheaper, works for simple loads (lights, fans, basic tools). Can damage or malfunction with some electronics.

**Sizing:** The inverter must handle the maximum wattage of everything you'll run simultaneously. A 1000W inverter runs a few lights, a phone charger, and a small tool. For larger loads, size accordingly. An inverter larger than your needs wastes standby power.

## Wiring

### Series vs. Parallel

**Series (+ to -):** Connects panels or batteries in a chain. Voltage adds up, current stays the same. Two 12V 100Ah batteries in series = 24V 100Ah.

**Parallel (+ to +, - to -):** Connects panels or batteries side by side. Current adds up, voltage stays the same. Two 12V 100Ah batteries in parallel = 12V 200Ah.

**Panels:** Wire in series for higher voltage (needed for MPPT controllers and long wire runs). Wire in parallel for higher current at the same voltage (simpler, but requires thicker wires).

### Wire Sizing

Undersized wires lose energy as heat and can start fires. The longer the wire run and the higher the current, the thicker the wire needs to be.

**Rule of thumb for 12V systems:**
- Under 10 feet, 10 amps: 12 AWG wire
- Under 20 feet, 10 amps: 10 AWG wire
- Under 10 feet, 20 amps: 10 AWG wire
- Under 20 feet, 20 amps: 8 AWG wire
- Over 20 feet or over 20 amps: consult a wire sizing chart

Keep wire runs as short as possible. Every foot of wire loses energy.

### Fuses and Protection

**Every connection needs a fuse.** Between panels and controller, between controller and battery, between battery and inverter, and between battery and any load. Fuses prevent fire from short circuits.

Size fuses at 125% of the maximum expected current for that circuit. A circuit carrying 10 amps gets a 12.5 or 15 amp fuse.

## Panel Mounting and Positioning

- **Face panels toward the equator.** In the Northern Hemisphere, face them south. In the Southern Hemisphere, face them north.
- **Tilt angle:** For year-round fixed mounting, set the tilt angle equal to your latitude. At 40° latitude, tilt the panel 40° from horizontal.
- **Seasonal adjustment:** Steeper in winter (latitude + 15°), shallower in summer (latitude - 15°). Adjustable mounts increase annual output by 10–15%.
- **Avoid shade.** Even partial shade on one cell of a panel can reduce output by 50% or more — solar cells are wired in series, so one shaded cell bottlenecks the entire string.
- **Keep panels clean.** Dust, bird droppings, and snow reduce output. Wipe with water periodically.

### Improvised Mounts

- Lean panels against a wall or rock at the correct angle
- Build an A-frame from lumber or poles
- Lay on a south-facing roof surface
- Mount on a pole driven into the ground with adjustable brackets

## Maintenance

- **Check battery water levels monthly** (flooded lead-acid only). Add distilled water to cover the plates. Never add tap water — minerals contaminate the cells.
- **Check connections** for corrosion and tightness quarterly.
- **Monitor voltage.** A healthy 12V battery reads 12.6–12.8V fully charged, 12.0V at 50% discharge, and 11.8V at empty. Below 11.5V, you're damaging the battery.
- **Clean panels** when dirty. Output drops measurably with a film of dust.
- **Equalize flooded batteries** every 1–3 months — a controlled overcharge that evens out cell voltages. Your charge controller may have an equalization mode.

## Quick System Examples

**Minimal (phone charging + LED lights):**
- 1× 50W panel
- 1× PWM charge controller (10A)
- 1× 35Ah AGM battery
- 12V LED lights + USB charging adapter
- Cost (pre-disaster): ~$150

**Basic homestead (lights + radio + small tools):**
- 2× 100W panels (wired in parallel)
- 1× 20A MPPT charge controller
- 2× 100Ah deep-cycle batteries (wired in parallel)
- 1000W pure sine wave inverter
- Cost (pre-disaster): ~$600–800

**Full household (lights + fridge + tools + pumps):**
- 4–8× 100W panels
- 1× 40–60A MPPT controller
- 4–8× 100Ah lithium batteries or 8–16× lead-acid
- 3000W+ inverter
- Cost (pre-disaster): $3,000–6,000+
