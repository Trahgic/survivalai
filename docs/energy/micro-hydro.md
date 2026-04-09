---
title: Micro-Hydro Power
source: Practical Action Micro-Hydro Guide, US DOE Small Hydro Handbook, Appropriate Technology Library
license: Proprietary
last_reviewed: 2026-03-30
tags: micro hydro, water power, turbine, stream power, head, flow, hydro electric, water wheel, off grid, renewable energy
---

If you have a year-round stream with reasonable flow and some elevation drop, micro-hydro is the best off-grid power source available. It runs 24/7 regardless of weather, producing steady, reliable power that solar and wind can't match. A small system on a modest stream can produce enough electricity to power an entire household — continuously.

## What You Need

Two things determine how much power a stream can produce:

### Head (Vertical Drop)

Head is the vertical distance the water falls from your intake to your turbine. More head = more power. Measured in feet or meters.

**Low head:** Under 10 feet. Requires high flow to produce useful power. Water wheel territory.

**Medium head:** 10–50 feet. Good for most micro-hydro turbines. The sweet spot for small systems.

**High head:** 50+ feet. Excellent power potential even with modest flow. A 100-foot head with a garden-hose-sized flow produces meaningful power.

### Flow (Volume of Water)

Flow is how much water passes a point per unit time, measured in gallons per minute (GPM) or liters per second.

**Measuring flow:**
1. Find a narrow point in the stream.
2. Dam it temporarily or use a natural restriction to channel all water through one point.
3. Time how long it takes to fill a bucket of known volume. 5-gallon bucket fills in 10 seconds = 30 GPM.
4. For larger flows: measure the cross-section of the stream (width × average depth) and measure the speed of the water (float a stick and time how long it takes to travel a measured distance). Flow = cross-section area × speed. Multiply by 0.8 to account for friction (bottom and sides of the stream move slower than the surface).

### Power Formula

**Power (watts) = Head (feet) × Flow (GPM) × 0.18 × efficiency**

Typical turbine efficiency is 50–70%.

**Example:** 50 feet of head × 20 GPM × 0.18 × 0.6 efficiency = **108 watts continuous**

That's 108 watts every hour of every day — over 2,500 watt-hours per day, or roughly 5× what a 100W solar panel produces in average conditions. And it works at night and on cloudy days.

## System Components

### Intake

A screened collection point where water enters your system.

1. Build a small dam or weir across the stream to create a pool. Doesn't need to impound much water — just enough to submerge your intake pipe.
2. Place a screen (hardware cloth, wire mesh) over the intake to keep leaves, debris, and fish out. A screen with holes smaller than ¼ inch stops most debris.
3. Build a settling basin behind the screen — a small pool where sediment drops out before entering the pipe. Sediment destroys turbines.

### Penstock (Pipe)

The pipe that carries water from the intake to the turbine. The penstock converts potential energy (head) into pressure and velocity.

- **PVC pipe** is cheapest and easiest to work with. Use schedule 40 or heavier for higher pressures.
- **Polyethylene pipe** (black plastic roll pipe) is flexible and easy to lay along terrain.
- **Steel pipe** for very high-pressure applications.

**Sizing:** Bigger pipe = less friction loss = more power delivered. For flows under 50 GPM, 2–4 inch pipe is typical. For higher flows, 4–6 inch or larger. The pipe should be as straight as possible — bends, fittings, and length all add friction losses.

**Pressure rating:** At the bottom of a 100-foot head, the pipe sees about 43 PSI. Make sure your pipe is rated for the pressure.

### Turbine

The turbine converts the water's energy into rotating mechanical energy.

**Pelton wheel (high head, low flow):** A wheel with cups around the rim. A jet of water from a nozzle hits the cups and spins the wheel. Best for heads above 30 feet. Simple, efficient (70–90%), easy to improvise. The most practical DIY turbine.

**Turgo (medium head, medium flow):** Similar to Pelton but the jet hits at an angle, allowing more water to pass through. Good for 15–100 foot head.

**Crossflow (medium head, variable flow):** Water passes through a drum-shaped runner twice. Efficient across a range of flows. Good for 5–100 foot head. Can be built from scratch with basic metalworking.

**Propeller/Kaplan (low head, high flow):** A submerged propeller in a tube. Works with as little as 3 feet of head but needs significant flow. Harder to build from scratch.

### Generator

The turbine spins a generator to produce electricity. Options:

- **Permanent magnet alternator:** Produces AC power at variable frequency (depends on speed). Needs a rectifier to convert to DC for battery charging. Common in small hydro. Can be salvaged from cars (alternators), wind turbines, or purpose-built.
- **Induction motor run as generator:** A standard AC induction motor (from a washing machine, pump, or fan) can work backward as a generator when spun by the turbine. Requires excitation capacitors to establish the magnetic field. Produces standard AC at whatever speed the motor is rated for.
- **Car alternator:** The easiest generator to source. Produces 12V DC directly. Limited to about 500–700 watts. Needs to spin at 3,000+ RPM — may need a belt/pulley speed-up from the turbine.

### Controls

- **Charge controller:** If charging batteries, same as solar — regulates voltage and current.
- **Load diversion controller:** Micro-hydro can't be "turned off" like solar — water keeps flowing. If the batteries are full, excess power needs somewhere to go. A diversion load (a water heater element, resistance heater, or dump load) absorbs excess power. Without this, overcharging destroys batteries.
- **Voltage regulator:** If running AC loads directly (no batteries), a regulator maintains stable voltage despite flow variations.

## DIY Pelton Turbine

The simplest effective micro-hydro turbine to build:

1. **Runner (wheel):** Cut cups from PVC pipe (halved 3–4 inch pipe sections work) and bolt them around the perimeter of a circular plate (plywood, metal plate, or repurposed wheel hub). Space cups evenly. 8–16 cups is typical.
2. **Nozzle:** Reduce the penstock output to a small, focused jet. A reducer fitting (4 inch to 1 inch, for example) accelerates the water. The jet should hit the cups at the centerline, tangent to the wheel.
3. **Shaft:** Mount the runner on a shaft supported by bearings. Shaft connects to the generator (direct drive or belt/pulley).
4. **Housing:** An enclosure that catches the spent water and directs it away. Can be an open frame — the housing doesn't need to be sealed.

**Nozzle sizing:** The nozzle diameter controls how much water flows and therefore how much power you produce. Start small and increase if you have more flow available. A 1-inch nozzle at 50 feet of head passes about 30 GPM.

## Site Assessment Checklist

Before investing time in a micro-hydro system:

1. Is the stream year-round? Seasonal streams leave you without power in dry months.
2. Measure the flow at its lowest point (late summer in most climates). Design for the minimum flow — anything above that is bonus.
3. Measure the head. Walk the stream and note elevation changes. Even 10 feet of head is usable with adequate flow.
4. Check the distance from the turbine site to where you need the power. Long wire runs lose energy. Keep the turbine as close to the batteries/house as practical, or use higher voltage to reduce losses.
5. Assess debris load. Streams with heavy leaf fall, sediment, or ice need more robust intake screening and more maintenance.
6. Legal considerations: in normal times, water rights and permits may apply. In a survival scenario, this matters less.

## Advantages Over Solar and Wind

- **24/7 production.** A 100-watt micro-hydro system produces 2,400 watt-hours per day. A 100-watt solar panel produces 400–500 watt-hours per day. Hydro produces 5–6x more energy from the same wattage rating.
- **Consistent output.** No cloudy days, no calm days. Stream flow is the most predictable renewable energy source.
- **Smaller battery bank needed.** Because production is continuous, you need less storage to bridge gaps.
- **Works at night.** Obvious but significant — your loads don't have to match daylight hours.

**Main disadvantage:** You need a specific site — a stream with adequate head and flow. You can put solar panels anywhere. Hydro requires the right geography.
