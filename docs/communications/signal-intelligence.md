---
title: Signal Intelligence — Monitoring and Scanning
source: ARRL Operating Manual, NOAA Weather Radio Guide, Scanner Reference Guides
license: Proprietary
last_reviewed: 2026-03-30
tags: scanning, monitoring, emergency frequencies, NOAA, weather radio, signal intelligence, radio monitoring, situation awareness
---

Listening is often more valuable than transmitting. Monitoring radio frequencies gives you situational awareness — what's happening beyond your immediate area, where help is, where threats are, and what the weather is doing. In a grid-down scenario, the ability to passively gather information by listening is a significant advantage.

## NOAA Weather Radio

The single most valuable radio frequency to monitor continuously.

**Frequencies:** 162.400, 162.425, 162.450, 162.475, 162.500, 162.525, 162.550 MHz. Seven channels, each broadcasting from a different transmitter. One of these will work in your area.

**What it provides:** Continuous weather forecasts, hazardous weather warnings, and emergency alerts (AMBER alerts, tsunami warnings, nuclear facility incidents, chemical spills). Broadcasts 24/7.

**Equipment:** Any VHF receiver, scanner, or HAM radio that covers the 162 MHz range. Dedicated NOAA weather radios ($20–40) have built-in alert functionality — they remain silent until an emergency alert is broadcast, then activate with an alarm tone.

**In a grid-down scenario:** NOAA weather radio is one of the last government broadcasts to go offline. It's powered by dedicated infrastructure with generator backup. As long as NWS facilities are functioning, weather radio broadcasts.

## Scanner Monitoring

A radio scanner automatically cycles through programmed frequencies, stopping when it detects a signal. This lets you monitor dozens or hundreds of channels passively.

### Key Frequencies to Monitor

**Emergency services (if still operational):**
- Local police, fire, and EMS frequencies vary by area. Pre-program your local frequencies before a crisis. Many are available at radioreference.com.
- Note: most urban police/fire have moved to encrypted digital systems (P25 Phase II) that scanners can't decode. Rural agencies often still use analog or unencrypted digital.

**Aviation:**
- 121.500 MHz — international aviation emergency
- 122.750 MHz — general aviation air-to-air
- 123.025 MHz — helicopter emergency medical services
- Aircraft overhead may indicate military operations, rescue flights, or supply movements.

**Marine:**
- 156.800 MHz (Channel 16) — marine distress and calling. If you're coastal, monitor this.

**Railroad:**
- 160–161 MHz range. Rail traffic indicates functioning infrastructure.

**HAM radio:**
- 146.520 MHz — 2-meter simplex calling frequency
- 446.000 MHz — 70-cm simplex calling frequency
- Local repeater frequencies (check local repeater directories)

**FRS/GMRS:**
- 462/467 MHz range. Monitor to detect other groups in your area.

**CB:**
- 27.065 MHz (Channel 9) — emergency
- 27.185 MHz (Channel 19) — highway traffic

### What to Listen For

**Situational intelligence:**
- News and official announcements (if broadcast stations are operating)
- Reports of conditions in nearby areas
- Military or government communications (may indicate evacuation, aid distribution, or enforcement activity)
- HAM emergency nets (organized communication groups sharing situation reports)
- Traffic from other groups (indicates who else is operating in your area)

**Weather:**
- NOAA broadcasts
- HAM weather nets
- Aviation weather (ATIS broadcasts on specific frequencies at airports)

### Equipment

**Handheld scanner:** $100–300. Uniden and Whistler are common brands. Program your local frequencies before a crisis.

**Software-defined radio (SDR):** A USB dongle ($25–35, RTL-SDR) plugged into a laptop covers a massive frequency range (25 MHz to 1.7 GHz). With free software (SDR#, GQRX), you can monitor multiple frequencies simultaneously, record transmissions, and visualize the spectrum. Requires a computer but is the most versatile monitoring tool available.

**HAM radio as scanner:** Most HAM radios can receive outside their transmit bands. A Baofeng UV-5R ($25) receives police, fire, marine, NOAA, FRS, GMRS, and aviation frequencies. It can't transmit on these frequencies legally, but it can listen.

## Passive Information Gathering

### Signal Direction Finding

If you hear a signal and want to know where it's coming from:

1. Use a directional antenna (Yagi or even a handheld with the rubber duck antenna pointed in different directions).
2. Rotate until the signal is strongest. That's the general direction.
3. Move to a different location and take another bearing. Where the two bearings intersect is the approximate source location.

### Traffic Analysis

Even if you can't understand encrypted communications, you can learn from:
- **Volume of traffic** — heavy radio activity may indicate an event or operation
- **Timing patterns** — regular scheduled transmissions indicate organized groups
- **Signal strength** — stronger signals are closer
- **New signals** — a frequency that was silent now has traffic. Something changed.
- **Callsigns and identifiers** — even encrypted transmissions may have unencrypted headers

### Operational Security (OPSEC)

Remember: if you can listen to others, others can listen to you.

- Assume all your transmissions are monitored
- Use encryption where available (Meshtastic encrypted channels, etc.)
- Keep transmissions brief — shorter transmissions are harder to direction-find
- Use low power — the minimum needed to reach your intended recipient
- Change frequencies periodically (pre-arranged schedule with your group)
- Don't transmit information you don't want intercepted — locations, plans, resources, group size

## Emergency Broadcasting

In a prolonged grid-down scenario, establishing a community broadcast serves morale, coordination, and information sharing:

1. Use a HAM radio on an HF frequency (40 or 80 meters reaches regional audiences).
2. Broadcast at scheduled times (e.g., daily at 0800 and 1800 local time).
3. Share weather observations, news from other contacts, safety information, and community announcements.
4. Invite check-ins — let other stations report their situations.
5. Keep a log of contacts, locations, and information shared. Build a picture of the broader situation over time.
