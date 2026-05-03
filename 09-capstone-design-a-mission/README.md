# Lesson 9 — Capstone: Design Your Own Mission

**Python concepts:** all of them.
**You'll end with:** a mission you invented, flown autonomously in the simulator.

## The story

You have everything you need now. You can connect, arm, takeoff, fly waypoints, react to telemetry, handle errors, and land safely. The capstone is open-ended on purpose — **you decide what your drone does**.

## Mission ideas

Pick one, modify one, or invent your own. Anything that's a real mission counts.

### Easy

**Photo Tour.** Pick four spots around the takeoff point. Fly to each, hover for 3 seconds (pretend the drone is taking a picture), and return.

**Search Pattern.** Fly a 4×4 grid at 4m altitude. Hover for 1 second at each grid cell. Land back at the start.

### Medium

**Ascending Spiral.** Fly a circle (8 waypoints around a center) while gaining altitude — start at 1m, end at 6m, gaining 0.6m per waypoint.

**Triangle Patrol.** Fly a triangle pattern. Repeat 3 times. Each time, get faster (shorter sleep between waypoints).

### Harder

**Battery-Aware Mission.** Read battery telemetry the whole time. If battery drops below 50%, abort the rest of the mission and land immediately.

**Two-Altitude Survey.** Fly a square at 2m, then the same square at 5m. Print altitude readings throughout.

## Constraints

- **Use your `dexi_helpers.py` from Lesson 8.** Import what you need; don't repeat yourself.
- **Use the `try/finally` pattern from Lesson 7.** Your drone must always land.
- **Read at least one telemetry stream.** Even if it's just printing battery once.
- **Keep `mission.py` under 80 lines.** If it's longer, more should go in helpers.

## What to do

1. Open `09-capstone-design-a-mission/mission.py`. It's a stub.
2. Sketch your mission *in plain English* in a comment at the top of the file. Two or three sentences.
3. Implement it. Use any helpers from Lesson 8 (copy `dexi_helpers.py` into this directory or import from `../08-your-own-module/`).
4. Run it. Watch it fly in the Unity sim.
5. Capture a screenshot of the Unity sim mid-flight, or a short screen recording. Save it next to your `mission.py`.

> **Want to see a working example before you start?** Run `python3 solution_photo_tour.py` — it imports the filled-in helpers from `08-your-own-module/solution_dexi_helpers.py` and flies a four-landmark Photo Tour. Use it as inspiration, not a template to copy.
>
> **Note:** the stub `mission.py` imports from `08-your-own-module/dexi_helpers.py`. If you skipped Lesson 8 (or didn't fill in your helpers), copy them in first: `cp ../08-your-own-module/solution_dexi_helpers.py ../08-your-own-module/dexi_helpers.py`.

## Rubric (for teachers)

- [ ] Mission completes without crashing
- [ ] Always lands (uses `try/finally`)
- [ ] Reads at least one telemetry stream
- [ ] Uses at least one helper from `dexi_helpers.py`
- [ ] Comment at the top describes what the mission does
- [ ] Code is under 80 lines

A 4-out-of-6 is passing. A 6-out-of-6 with a creative mission is exceptional.

## What's next

Lesson 10 — the bridge to real hardware.
