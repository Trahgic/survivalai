---
title: Battery Systems
source: Battery University, Off-Grid Solar Design Manual, US Army Technical Manual
license: Proprietary
last_reviewed: 2026-03-30
tags: battery, lead acid, lithium, car battery, series, parallel, wiring, charging, deep cycle, battery safety, 12V, voltage
---

Batteries are the weakest link in any off-grid power system. They're heavy, expensive, have limited lifespans, and fail if mistreated. But they're also the only way to store electricity for use when the sun isn't shining or the wind isn't blowing. Treating your batteries right is the single most impactful thing you can do for your energy system's longevity.

## Battery Types

### Flooded Lead-Acid (FLA)

The oldest rechargeable battery technology. Liquid sulfuric acid electrolyte, lead plates.

**Pros:** Cheapest per amp-hour. Widely available. Repairable (can replace electrolyte). Tolerant of high charge rates. Well-understood technology.

**Cons:** Requires maintenance (checking/adding water). Must be kept upright (liquid spills). Produces hydrogen gas when charging (ventilation required). Heavy. Only 50% usable capacity.

**Types within FLA:**
- **Car/starting batteries:** Designed for short, high-current bursts (starting an engine). Thin plates, high surface area. They CAN be used for off-grid storage in a pinch, but they degrade rapidly with deep cycling. Expect 6–12 months of life used as a deep-cycle battery.
- **Golf cart batteries (6V):** Thick plates designed for deep cycling. Two wired in series give 12V. One of the best value options for off-grid. Lifespan: 3–6 years with care.
- **L16 batteries (6V, ~400Ah):** The commercial standard for off-grid. Heavy (120+ lbs each), high capacity. Lifespan: 5–8 years.

### AGM (Absorbed Glass Mat)

Sealed lead-acid. Electrolyte is absorbed into glass mat separators — no free liquid.

**Pros:** Maintenance-free. Spill-proof. Can mount in any position. Low self-discharge. No hydrogen venting (in normal operation).

**Cons:** More expensive than FLA (2–3x). Less tolerant of overcharging. Not repairable. Same 50% depth of discharge limitation.

### Gel

Sealed lead-acid with gelled electrolyte.

**Pros:** Maintenance-free. Very tolerant of high temperatures. Good cycle life.

**Cons:** Sensitive to overcharging (gelling agent can crack permanently). Requires precise charge settings. Not widely available.

### Lithium Iron Phosphate (LiFePO4)

The modern standard for off-grid storage.

**Pros:** 80–90% usable capacity (vs. 50% for lead-acid). 2,000–5,000 cycle lifespan (vs. 500–1,000 for lead-acid). Half the weight. No maintenance. Flat discharge curve (steady voltage until nearly empty). Fast charging.

**Cons:** High upfront cost (3–5x lead-acid per unit). Requires a Battery Management System (BMS) — usually built in. Won't charge below freezing (some have built-in heating). Harder to salvage or repair in the field.

## Car Battery Repurposing

In a grid-down scenario, car batteries are the most abundant battery resource available. Every abandoned vehicle has one.

### Assessment

1. Check the voltage with a multimeter. A healthy 12V car battery reads 12.4–12.8V. Below 12.0V it's deeply discharged. Below 11.5V it may be damaged.
2. Check for physical damage — cracks, bulging, leaking acid.
3. Load test if possible: connect a 12V light bulb or small load. If voltage drops below 10V under load, the battery is weak.
4. Car batteries that have been sitting discharged for months may be sulfated (lead sulfate crystals coat the plates, reducing capacity). Some can be recovered with a slow, prolonged charge cycle.

### Using Car Batteries Off-Grid

- Wire multiple car batteries in parallel for more capacity at 12V.
- Accept shorter lifespan — car batteries used for deep cycling last 6–18 months.
- Limit discharge to 30% depth (not 50% like deep-cycle). This extends life somewhat.
- They're free and abundant — when one dies, swap it for another from the next abandoned car.
- Always match battery sizes/types when wiring in parallel. Mixing different batteries causes uneven charging and premature failure.

## Series and Parallel Wiring

### Series (Increases Voltage)

Connect positive terminal of one battery to negative terminal of the next.

- 2× 6V batteries in series = 12V
- 2× 12V batteries in series = 24V
- Capacity (Ah) stays the same

### Parallel (Increases Capacity)

Connect positive to positive, negative to negative.

- 2× 12V 100Ah batteries in parallel = 12V 200Ah
- Voltage stays the same

### Series-Parallel (Both)

Combine both methods for higher voltage AND capacity. Common in larger systems.

Example: Four 6V 200Ah batteries → two series strings of two (making two 12V 200Ah strings) → wire the two strings in parallel (12V 400Ah total).

> **WARNING:** Only wire identical batteries together. Same type, same brand, same age, same capacity. Mismatched batteries charge and discharge unevenly, and the weakest battery drags the entire bank down.

## Charging

### From Solar

Use a charge controller (see solar-basics.md). The controller manages the charging stages automatically.

### From a Generator

A generator produces AC power. You need either a battery charger (AC to DC converter) or a charge controller designed for generator input. Don't connect a generator directly to batteries — you'll overcharge and destroy them.

### From a Vehicle Alternator

A running vehicle alternator outputs 13.5–14.5V DC — perfect for charging 12V batteries. Connect the house battery to the vehicle battery with appropriate wire gauge and a fuse. Run the engine for 1–2 hours to significantly charge the house battery. An isolator or manual switch prevents the house battery from draining the starting battery when the engine is off.

### Charging Stages

Proper charging has three stages:

1. **Bulk:** Full current until battery reaches about 80% charge (voltage reaches ~14.4V for 12V lead-acid). This is the fast-charge phase.
2. **Absorption:** Voltage is held constant at 14.4V while current gradually decreases as the battery fills. Continues until current drops to about 2% of battery capacity.
3. **Float:** Voltage drops to 13.2–13.6V and holds. This maintains full charge without overcharging. Batteries can stay on float indefinitely.

**Overcharging** boils the electrolyte (FLA), damages plates, and shortens life. A proper charge controller prevents this.

**Undercharging** (never reaching full charge) causes sulfation in lead-acid batteries — progressive capacity loss that's eventually irreversible. Fully charge your batteries at least once every 2 weeks.

## Safety

- **Lead-acid batteries produce hydrogen gas during charging.** Hydrogen is explosive. Charge in ventilated areas. No sparks, no open flame near charging batteries.
- **Battery acid (sulfuric acid) burns skin and destroys clothing.** Wear eye protection when working with flooded batteries. If acid contacts skin, flush with large amounts of water. For eye contact, flush for 15+ minutes.
- **Short circuits across battery terminals produce enormous current** — enough to weld metal, start fires, and cause explosions. Remove metal jewelry before working on batteries. Use insulated tools. Cover terminal connections with tape or boots when not working on them.
- **Batteries are heavy.** A standard car battery weighs 40+ lbs. L16 batteries weigh 120+ lbs. Lift with your legs, not your back.
- **Lithium battery safety:** LiFePO4 batteries are inherently safer than other lithium chemistries, but damaged or shorted lithium cells can still catch fire. Never puncture, crush, or short-circuit any lithium battery.

## Monitoring

Check your battery bank regularly:

- **Voltage** (daily): 12.6V+ = full, 12.2V = 50%, 12.0V = near empty, below 11.8V = damage territory
- **Specific gravity** (FLA only, monthly): use a hydrometer. Each cell should read 1.265–1.280 when fully charged. Cells more than 0.025 apart indicate a failing cell.
- **Water level** (FLA only, monthly): plates must be submerged. Add distilled water after charging, not before.
- **Temperature:** Batteries lose capacity in cold. A battery at 32°F (0°C) has about 70% of its rated capacity. At 0°F (-18°C), about 50%. Insulate battery banks in cold climates.
- **Connections:** Check for corrosion (white/green fuzzy buildup on terminals). Clean with a wire brush and apply petroleum jelly or dielectric grease to prevent recurrence.
