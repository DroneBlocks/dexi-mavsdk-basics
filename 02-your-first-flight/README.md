# Lesson 2 — Your First Flight

**Python concept:** `async def`, `await`, sequential statements.
**You'll end with:** a script that takes off to 2 meters, hovers for 5 seconds, and lands.

## The story

In Lesson 1 you said hello. Now you're going to fly. This is your first complete flight script — under 40 lines, end to end. We'll fly first and ask questions later. Lesson 3 unpacks every line.

## Why every drone call has `await` in front of it

Talking to a drone takes time. A regular Python function returns instantly:

```python
x = 2 + 2   # done immediately
```

A drone command isn't like that. When you say "arm", the drone has to actually arm. That takes a moment. `await` is Python's way of saying "start this, wait for it to actually finish, then continue." Every MAVSDK command is `await`-ed.

## The "boilerplate" you'll see

The first few lines of `starter.py` look complicated:

```python
await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
await drone.offboard.start()
await asyncio.sleep(1.5)
await drone.action.arm()
```

That's because PX4 SITL (the simulator's flight controller) won't let us arm without a continuous "I am in control" signal. Sending a zero-velocity setpoint and starting offboard mode provides that signal. **You don't need to understand it yet.** You'll unpack offboard mode in Lesson 6.

## What to do

1. Open `02-your-first-flight/starter.py`.
2. Find the three `TODO`s and fill them in. The README and Lesson 1 give you everything you need.
3. Save and run:
   ```
   cd ~/dexi-mavsdk-basics/02-your-first-flight
   python3 starter.py
   ```
4. Watch the Unity sim. The drone should:
   - Spin up its rotors
   - Lift off to 2m
   - Hover for 5 seconds
   - Land
5. The terminal will print each step as it happens.

## If something goes wrong

| Problem | Likely cause |
|---|---|
| Drone doesn't arm | SITL probably still booting. Wait 10s and try again. |
| Drone takes off then drifts | Optical flow not locked yet. Restart the sim. |
| Script hangs at "Waiting for drone..." | Connection address is wrong, or SITL isn't running. |

## Stretch challenge

Change the takeoff altitude to 4 meters. Change the hover time to 10 seconds. Run it again. Same code, different flight.

## When you're done

Open Lesson 3: `cd ../03-functions-that-fly`
