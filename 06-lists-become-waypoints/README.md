# Lesson 6 — Lists Become Waypoints

**Python concept:** lists, `for` loops.
**You'll end with:** a drone that flies a 1-meter square in offboard mode.

## The story

Up to now you've flown one move at a time. A real mission is a **sequence** — a list of places to go. Python lists hold them; a `for` loop walks through them; **offboard mode** flies the drone to each one.

## How drones think about position: NED

Drones use a coordinate system called **NED** — North, East, Down. Picture yourself standing where the drone takes off, looking north:

```
                  N (north)
                  │
                  │
   W (-east) ─────┼───── E (east)
                  │
                  │
                  S (-north)
```

And **down** means *down*. So **up is negative**.

```
   ground level: down =  0
   1 meter up:   down = -1
   3 meters up:  down = -3
```

If that feels weird, it is. Aviation has used NED forever, and PX4 inherited it.

## Your waypoints (a 1m square at 3m altitude)

```python
waypoints = [
    (1.0,  0.0, -3.0),   # 1m north of start
    (1.0,  1.0, -3.0),   # then 1m east
    (0.0,  1.0, -3.0),   # then 1m back south
    (0.0,  0.0, -3.0),   # back to start
]
```

Each tuple is `(north, east, down)`. All down values are `-3.0` because we're staying at 3 meters up.

## What to do

1. Open `06-lists-become-waypoints/starter.py`. Takeoff is already wired up.
2. Find the `TODO` and create the `waypoints` list above.
3. Write a `for` loop that flies to each waypoint:
   ```python
   for north, east, down in waypoints:
       print(f"flying to N={north}, E={east}")
       await drone.offboard.set_position_ned(PositionNedYaw(north, east, down, 0.0))
       await asyncio.sleep(5)   # we'll telemetry-wait in stretch
   ```
4. Run it. Watch the drone fly a square in the Unity sim.

## What's `set_position_ned`?

`PositionNedYaw(north, east, down, yaw)` is one waypoint. We pass it to `drone.offboard.set_position_ned(...)`, and the drone flies there. The fourth argument (`yaw`) is which way the drone faces — `0.0` means "keep facing north."

## ⚠️ The offboard rule you must not break

> **In offboard mode, the drone needs a fresh setpoint at least every 0.5 seconds.** If setpoints stop arriving — your script crashes, hangs in a long calculation, sleeps too long — PX4 assumes your code died, drops out of offboard, and triggers a failsafe (typically a hold or a land). This is a safety feature, not a bug.

In our loop, each call to `set_position_ned(...)` IS a fresh setpoint, and MAVSDK keeps the connection warm in the background while we sleep. That's fine for this lesson. But if you ever extend the script — say, you want to do a long calculation between waypoints — you need to keep streaming setpoints during that work. **A common pattern is a background coroutine that re-sends the current setpoint every 100ms.** You don't need it today; just know the rule exists.

## Two ways drones fly waypoints (a heads-up)

What you're doing here is called **offboard mode** — your code drives the drone, one setpoint at a time. PX4 also supports a second model called **mission mode**, where you upload a *plan* (a list of waypoints with rules like "loiter for 30s here") and tell PX4 to execute it on its own. We use offboard in this course because it's interactive — you can change your mind mid-flight, react to telemetry, build state machines. Mission mode is great for "here are 50 survey points, fly all of them and tell me when you're done." We may cover it in a future course.

## Stretch challenge

`asyncio.sleep(5)` is a guess (sound familiar from Lesson 5?). Write `wait_until_position(drone, n, e, d, tolerance=0.3)` using `drone.telemetry.position_velocity_ned()`. Compare `position.north_m`, `position.east_m`, and `position.down_m` to the target.

## Reference

`~/dexi-mavsdk/missions/box_mission.py` does the same idea but in body frame (forward/right relative to the drone). Compare your script to it once you finish.
