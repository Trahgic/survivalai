---
title: Electrical Repair
source: US Army Technical Manual, Ugly's Electrical References, Practical Electrical Wiring Guides
license: Proprietary
last_reviewed: 2026-03-30
tags: electrical, wiring, repair, wire splicing, outlet, breaker, multimeter, 12V, 120V, voltage, circuit, fuse, troubleshooting
---

Basic electrical knowledge lets you maintain power systems, repair damaged wiring, and safely work with both low-voltage (12V DC) and household-voltage (120V AC) systems. This isn't about becoming an electrician — it's about understanding enough to fix things safely and not electrocute yourself.

## 12V DC vs. 120V AC — Know the Difference

### 12V DC (Direct Current)

Found in: car electrical systems, solar/battery setups, RV systems, most off-grid installations.

**Danger level:** Low. 12V DC can't push enough current through dry human skin to cause electrocution. You can touch both terminals of a 12V battery without feeling it. HOWEVER: 12V batteries can deliver hundreds of amps through a short circuit — enough to weld metal, start fires, and cause explosions. The danger is fire and burns, not electrocution.

### 120V AC (Alternating Current)

Found in: household wiring, generator output, standard wall outlets in North America.

**Danger level:** High. 120V AC can kill you. As little as 50 milliamps through the heart causes fibrillation (cardiac arrest). Wet skin, metal contact, or a hand-to-hand current path through the chest dramatically increases risk. Treat 120V with serious respect.

> **CRITICAL:** Before working on any 120V circuit, disconnect the power source. Turn off the breaker, unplug the generator, or disconnect the inverter. Verify the circuit is dead with a multimeter or voltage tester before touching any wire. Test the tester on a known live circuit first to confirm it's working. People die from "dead" circuits that weren't actually off.

## Essential Tool: Multimeter

A multimeter measures voltage, current, and resistance. It's the most important diagnostic tool for electrical work. Even a cheap $10 multimeter is invaluable.

### Measuring Voltage (Volts)

1. Set the dial to V (DC for batteries, AC for household).
2. Touch the red probe to the positive/hot wire, black probe to the negative/neutral wire.
3. Read the voltage. For 12V systems: 12.6V = full battery, 12.0V = half, 11.5V = nearly dead. For 120V AC: you should read 115–125V.

### Measuring Continuity (Is the Wire Broken?)

1. Set the dial to the continuity/diode symbol (looks like a sound wave or arrow).
2. Touch both probes to each end of the wire (disconnect the wire from power first).
3. If you get a beep and near-zero reading, the wire is intact. If no beep and infinite reading, the wire is broken somewhere.

### Measuring Resistance (Ohms)

1. Set to Ω (ohms).
2. Touch probes to both ends of the component.
3. A fuse should read near zero (intact) or infinite/OL (blown). A heating element should read some resistance (10–50 ohms typically). An open circuit reads OL or infinite.

## Wire Splicing

When a wire is cut or broken, you need to rejoin it.

### Twist and Tape (Field Method)

1. Strip ½ inch of insulation from each wire end. Use a knife — score around the insulation lightly and pull it off. Don't nick the conductor.
2. Twist the stripped ends together tightly. Twist clockwise. The twisted section should be at least 3–4 full turns.
3. Wrap with electrical tape — at least 3 layers, extending ½ inch past the stripped area on each side. Pull the tape tight.
4. This is not a permanent solution but works for field repairs.

### Wire Nut (Preferred for AC)

1. Strip ½ inch from each wire.
2. Hold the stripped ends parallel.
3. Thread a wire nut (twist-on connector) clockwise over both ends until tight.
4. Tug on each wire to verify it's secure.
5. Wrap electrical tape over the wire nut for extra security.

### Crimp Connector (Best for DC/Automotive)

1. Strip the wire. Insert into the crimp connector (butt connector, ring terminal, or spade terminal).
2. Squeeze with a crimping tool (or pliers in a pinch). The connector deforms and grips the wire.
3. Tug to verify.
4. Heat-shrink tubing over the connection is ideal. If you don't have heat shrink, use tape.

### Soldering (Best Quality)

1. Strip ½ inch from each wire.
2. Twist or hook the ends together.
3. Heat the joint (not the solder) with a soldering iron or heated piece of metal.
4. Touch solder to the heated joint — it should flow into and around the twisted wires (this is called "wetting"). Don't apply solder to the iron and drip it on — the joint needs to be hot enough to melt solder itself.
5. Let cool. The joint should be shiny and smooth.
6. Cover with heat-shrink tubing or tape.

Soldered joints are mechanically stronger and have lower resistance than twisted or crimped connections.

## Breaker Panels

### When a Breaker Trips

A tripped breaker means the circuit drew more current than the breaker is rated for (overload) or a short circuit occurred.

1. Unplug or turn off everything on that circuit.
2. Reset the breaker: push it firmly to the OFF position, then back to ON.
3. If it trips again immediately: there's a short circuit. Don't keep resetting — find the short.
4. If it holds: plug things back in one at a time. The last thing you plug in before it trips is the problem.

### Finding a Short Circuit

1. With the breaker off, use the multimeter's continuity mode.
2. Disconnect all loads (unplug everything).
3. Test between hot (black) and neutral (white) wires at the panel. You should read infinite resistance (open circuit). If you read near zero (continuity), there's a short in the wiring itself.
4. If the wiring tests open, one of the plugged-in devices has an internal short. Test each device separately.

## Common Repairs

### Replacing an Outlet

1. **Turn off the breaker.** Verify dead with a tester.
2. Remove the cover plate (1 screw).
3. Remove the outlet from the box (2 screws).
4. Note wire connections before disconnecting: black (hot) goes to brass-colored screws, white (neutral) goes to silver-colored screws, green or bare (ground) goes to the green screw.
5. Disconnect wires from old outlet. Connect to new outlet in the same configuration.
6. Push outlet back into box, screw in place, replace cover.

### Fixing a Broken Extension Cord

1. Cut out the damaged section.
2. Strip the outer jacket from both cut ends (2 inches).
3. Strip individual conductor insulation (½ inch each).
4. Splice each conductor separately (twist, wire nut, or crimp). Black to black, white to white, green to green.
5. Stagger the splices — don't put all three splices at the same point (they can short against each other). Offset each splice by ½ inch.
6. Tape each splice individually, then wrap the entire repair with tape.

## 12V System Troubleshooting

Most 12V problems are one of three things:

**Bad connections:** Corrosion, loose terminals, broken wires. Clean connections with a wire brush, tighten terminals, check continuity in wires.

**Dead battery:** Measure voltage. Below 11.5V, the battery is dead or dying. Charge it. If it won't hold a charge, it's failed (sulfated or cell shorted).

**Blown fuse:** Find the fuse box (in vehicles, usually under the dashboard or in the engine compartment). Pull fuses and inspect — a blown fuse has a broken metal strip visible through the clear body. Replace with the same amperage rating. If the new fuse blows immediately, there's a short — find it before replacing again.

## Safety Rules

1. **Always disconnect power before working on wiring.** Every time. No exceptions.
2. **One hand rule:** When working on circuits that might be live, keep one hand in your pocket. Current flowing hand-to-hand passes through the heart. Hand-to-foot or hand-to-ground is less likely to cause cardiac arrest.
3. **Don't work on electrical in wet conditions.** Water reduces skin resistance from ~100,000 ohms (dry) to ~1,000 ohms (wet), dramatically increasing the current that flows through you at any given voltage.
4. **Fuse everything.** Every circuit needs a fuse rated for the wire size. Wire without a fuse is a fire waiting for a short circuit.
5. **Don't overload circuits.** A 15-amp household circuit handles about 1,800 watts. A 20-amp circuit handles 2,400 watts. Plugging more into a circuit than it's rated for overheats wires inside walls — a leading cause of house fires.
6. **Respect stored energy.** Even after disconnecting a power source, large capacitors (in inverters, microwaves, TVs) can hold a lethal charge for minutes to hours. Don't reach inside electronic equipment you don't understand.
