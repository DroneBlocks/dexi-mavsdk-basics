# Lesson 10 — From Sim to Real DEXI

**Python concept:** environment variables, externalized config.
**You'll end with:** the same script, ready to fly a real drone.

## The promise we made

In Lesson 1 we said: code you write in the simulator runs unchanged on a real DEXI. Today you'll see why. **The only difference between sim and real is the connection string** — and we'll move that out of the code so you don't have to touch the script at all.

## What changes between sim and real

| | Sim | Real DEXI |
|---|---|---|
| Connection address | `udpin://0.0.0.0:14540` | `udpout://192.168.4.1:14540` (DEXI's default access-point IP) |
| Where you run the script | code-server in the sim container | A laptop on the same WiFi as the drone |
| Everything else | identical | identical |

That's it. Same `await drone.action.arm()`, same `await drone.offboard.set_position_ned(...)`, same `await drone.action.land()`.

## What to do

### Part 1: read config from the environment

1. Open `10-sim-to-real/mission.py`.
2. Find the line:
   ```python
   address = "udpin://0.0.0.0:14540"
   ```
3. Replace it with:
   ```python
   import os
   address = os.environ.get("DEXI_ADDRESS", "udpin://0.0.0.0:14540")
   ```
4. Run it normally:
   ```
   python3 mission.py
   ```
   Same as before — flies in the sim.

### Part 2: see how you'd target a real drone

You won't actually run this today (no hardware). But this is the command you'd use:

```bash
DEXI_ADDRESS=udpout://192.168.4.1:14540 python3 mission.py
```

The `DEXI_ADDRESS=...` part sets an environment variable just for that command. `os.environ.get(...)` in your script reads it. **Same script. Different drone.**

## The pre-flight checklist

When the day comes that you fly real hardware with code that worked in sim, run through this **every time**:

- [ ] Mission was tested end-to-end in sim **today**, not last week
- [ ] Always-land `finally` block is in place (Lesson 7)
- [ ] Battery > 60%
- [ ] Open space, no people in the flight area
- [ ] You have a Mode switch on the RC ready to take manual control
- [ ] Someone else is watching the drone, not just you

## What's next

You finished the bridge from Python to a real autonomous drone. From here:

- **Hover Lab Unit 3 — Autonomous Missions in Sim.** Bigger missions, state machines, mission planning.
- **Hover Lab Unit 4 — DEXI-3 Indoor Flight.** Real hardware. Optical flow. Range sensor. The exact lessons you wrote here, running on a real drone you can hold.

## You did it

You went from "I just learned Python" to "I just flew an autonomous mission." The same code is ready to fly real hardware. That's the whole bridge.

If you want to learn how to share your work on GitHub — clone, branch, push, collaborate, get code reviewed — take the companion course **Git & GitHub for Drone Developers**.
