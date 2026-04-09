---
title: Antenna Building
source: ARRL Antenna Book, Practical Antenna Handbook, Emergency Antenna Designs
license: Proprietary
last_reviewed: 2026-03-30
tags: antenna, dipole, vertical, yagi, wire antenna, SWR, radio antenna, building, frequency, ham radio
---

The antenna is the most important part of any radio system. A $25 radio with a good antenna outperforms a $2,000 radio with a bad antenna. In an emergency, you can build effective antennas from wire, coax, and basic hardware.

## Core Concept: Wavelength

Antenna dimensions are determined by the frequency you're using. The relationship: wavelength (in feet) = 984 / frequency (in MHz).

**Common wavelengths:**
- 2 meters (146 MHz): ~6.7 feet per wavelength
- 70 cm (446 MHz): ~2.2 feet per wavelength
- 20 meters HF (14 MHz): ~70 feet per wavelength
- 40 meters HF (7 MHz): ~140 feet per wavelength

Most antennas are sized as fractions of the wavelength — ½ wave, ¼ wave, or 5/8 wave are most common.

## Half-Wave Dipole — The Foundation Antenna

The simplest effective antenna for any frequency. Two wires, each ¼ wavelength long, connected to the feedline (coax cable) at the center.

### Formula

Total dipole length (feet) = 468 / frequency (MHz)

Each leg = half the total length.

### Examples

- **2 meters (146 MHz):** Total = 38.4 inches. Each leg = 19.2 inches.
- **20 meters (14.2 MHz):** Total = 33 feet. Each leg = 16.5 feet.
- **40 meters (7.2 MHz):** Total = 65 feet. Each leg = 32.5 feet.

### Construction

1. Cut two pieces of wire to the calculated leg length. Any copper or aluminum wire works — electrical wire, speaker wire, even coat hangers for VHF.
2. At the center, connect one leg to the center conductor of the coax cable. Connect the other leg to the shield (braid) of the coax.
3. Insulate the center connection — tape, hot glue, or a commercial center insulator.
4. Attach insulators at the far end of each leg (any non-conductive material — plastic, wood, glass).
5. Hang the antenna as high as possible, ideally in an inverted-V shape (center high, ends angling down at 45 degrees). The higher, the better the performance.

### Performance

A dipole hung at 30+ feet is an excellent antenna for its design frequency. It's directional (stronger broadside to the wire, weaker off the ends) which can be useful for targeting communication in a specific direction. Rotate the antenna by repositioning end supports.

## Quarter-Wave Ground Plane — Best for VHF/UHF Base Station

A vertical antenna with radials. Omnidirectional — radiates equally in all directions.

### Construction (2-Meter Example)

1. **Vertical element:** A 19.5-inch piece of stiff wire or rod (copper, brass, coat hanger, brazing rod) mounted vertically.
2. **Radials:** Four pieces of wire, each 19.5 inches, mounted horizontally (or angled downward at 45 degrees) from the base of the vertical element, pointing in four directions like a plus sign.
3. **Connection:** Vertical element connects to the center conductor of the coax. All four radials connect to the coax shield.
4. **Mount on a mast, pole, or pipe** as high as possible.

This antenna is simple to build and performs excellently for VHF/UHF repeater access and simplex communication.

## J-Pole — Excellent VHF/UHF Antenna

A half-wave antenna with a built-in matching section. No radials needed. Higher gain than a ground plane.

### Construction from 300-Ohm Twin-Lead (TV Antenna Wire)

1. Cut a piece of 300-ohm twin-lead wire (the flat, ribbon-like wire used for old TV antennas) to 56 inches total for 2 meters.
2. At one end, separate the two conductors for a length of 19 inches. Short the remaining conductors together at the bottom.
3. At the junction where the separation begins (19 inches from the bottom), connect the coax: center conductor to one wire, shield to the other.
4. The longer section (top 37 inches) is the radiator. The shorter section (bottom 19 inches) is the matching stub.
5. Hang vertically. Performance is excellent — comparable to commercial antennas costing $50+.

### Construction from Copper Pipe

A copper pipe J-pole is more durable and commonly built from ½ or ¾ inch copper pipe and fittings. Dimensions for 2 meters: long element 58 inches, short element 19 inches, spacing between elements ¾ inch, connected at the bottom with a U-shaped fitting. Feed point is approximately 3 inches up from the bottom on the long element.

## Yagi — Directional High-Gain Antenna

A Yagi antenna focuses energy in one direction, like a flashlight beam. Higher gain = greater range in the pointed direction, but you must aim it at the station you want to communicate with.

### Elements

- **Driven element:** A dipole at the center, connected to the coax. Same dimensions as a standalone dipole.
- **Reflector:** A wire 5% longer than the driven element, positioned behind it (away from the target direction). Spaced about 0.2 wavelengths behind.
- **Director(s):** Wires 5% shorter than the driven element, positioned in front (toward the target). Spaced about 0.15–0.2 wavelengths apart. More directors = more gain = narrower beam.

### Simple 3-Element Yagi for 2 Meters

1. **Boom:** A non-conductive pole (wood, PVC) about 36 inches long.
2. **Reflector:** 40.2 inches of wire or rod, mounted at one end of the boom.
3. **Driven element:** 38.4 inches total (two 19.2-inch halves with coax connection at center), mounted at the center of the boom.
4. **Director:** 36.6 inches, mounted at the other end of the boom.
5. All elements are parallel, centered on the boom.
6. Point the director end toward the station you want to reach.

Gain: approximately 6–7 dBi (roughly 4x the effective power of a dipole).

## Emergency Wire Antennas for HF

### Random Wire

In an emergency, ANY wire of ANY length connected to an HF radio's antenna port will radiate. It won't be efficient, but it works.

1. Connect one end of any wire (20–100 feet) to the antenna connection of your radio.
2. Run the wire up and away from the radio — drape over a tree branch, stretch to another building, run along a ridgeline.
3. Use the radio's built-in tuner (if equipped) to match the antenna. If no tuner, just try it — many radios tolerate moderate mismatch.
4. This is not optimal but in an emergency, getting any signal out beats waiting for perfect antenna design.

### Long Wire with Counterpoise

Better than a random wire: a wire ¼ wavelength or longer for your desired band, with a counterpoise (a second wire of the same length laid on the ground or running in the opposite direction from the antenna wire).

## SWR (Standing Wave Ratio)

SWR measures how well the antenna is matched to the radio. Perfect match = 1:1 (all power goes to the antenna). Acceptable = under 2:1. Above 3:1, the radio may reduce power or refuse to transmit. Above 5:1, you risk damaging the radio.

If you have an SWR meter (worth carrying in a radio kit):
1. Connect it between the radio and the antenna.
2. Transmit briefly at low power.
3. Read the SWR. If it's above 2:1, adjust the antenna length. Shorter = moves the resonance higher in frequency. Longer = moves it lower.
4. Trim or extend in small increments (½ inch for VHF, 6 inches for HF) and re-check.

If you don't have an SWR meter, cut the antenna to the calculated length and accept the result. It'll be close enough for emergency use.

## Feedline (Coax Cable)

**RG-58:** Thin, flexible, cheap. Works for short runs (under 25 feet) on VHF/UHF. Significant loss on HF over long runs.

**RG-8/RG-213:** Thicker, lower loss. Better for longer runs and HF use. The standard for most permanent installations.

**Key rule:** Keep the coax as short as possible. Every foot of coax loses signal. Run just enough to reach from the radio to the antenna, no more.

## Height is Everything

For VHF and UHF, antenna height is the single most important factor. Doubling the height roughly doubles your effective range. Get the antenna up — on a pole, in a tree, on a roof, on a hilltop. Every foot of height counts.

For HF, height matters less than antenna length and orientation, but higher is still generally better. An HF dipole at 50 feet outperforms one at 15 feet significantly.
