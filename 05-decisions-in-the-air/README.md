# Lesson 5 — Decisions in the Air

**Python concept:** `if` / `else`, comparisons.
**You'll end with:** a `wait_until_altitude(drone, target)` helper that uses real telemetry.

## The story

In Lesson 3 you wrote `await asyncio.sleep(8)` to wait for takeoff. **That was a guess.** Real flight code waits for *evidence* — actual telemetry that the drone reached its target.

This lesson replaces the guess with a check: keep reading altitude, and return as soon as the drone is close enough to where we asked it to go.

## Why this matters

A `sleep()` is a lie. It tells your script "the drone definitely got there" when it might not have — maybe the battery is low, maybe there's wind, maybe takeoff failed. A telemetry-driven wait tells the truth. **Every real drone program is built this way.** Internalize this pattern; you'll use it for the rest of the course.

## What to do

1. Open `05-decisions-in-the-air/starter.py`.
2. Find the `TODO` and write the function. We're going to do **two** things at once: read telemetry until the drone arrives, AND give up gracefully if it never does.
   ```python
   async def wait_until_altitude(drone, target_m, tolerance=0.3, timeout_s=30):
       async def _loop():
           async for pos in drone.telemetry.position():
               if abs(pos.relative_altitude_m - target_m) < tolerance:
                   print(f"reached {target_m}m")
                   return
       try:
           await asyncio.wait_for(_loop(), timeout=timeout_s)
       except asyncio.TimeoutError:
           print(f"timeout: didn't reach {target_m}m in {timeout_s}s")
   ```
3. In `takeoff_to`, replace the `await asyncio.sleep(8)` with `await wait_until_altitude(drone, altitude_m)`.
4. Run it. The drone takes off and reports as soon as it actually reaches altitude — not 8 seconds, however long it actually takes.

## Read the comparison carefully

```python
if abs(pos.relative_altitude_m - target_m) < tolerance:
```

`abs()` makes the difference positive whether the drone overshoots or undershoots. Without `abs()`, an overshoot would give a negative number that's always less than 0.3, and the function would return too early.

## Why the timeout matters

What if the drone *never* reaches that altitude? Without `asyncio.wait_for(...)`, your script would hang **forever** — battery dies, the drone is stuck in offboard mode, you have to Ctrl+C. **Always put a timeout on a wait.** This is a habit, not a stretch goal.

The pattern is `async def _loop(): ...` (the inner work) wrapped in `await asyncio.wait_for(_loop(), timeout=...)` (the safety net). The leading underscore on `_loop` is a Python convention for "internal helper, don't call me directly."

## Stretch challenge

Try `wait_until_altitude(drone, 99.0, timeout_s=5)` after takeoff. You're asking the drone to reach 99m in 5 seconds — impossible. Confirm:

1. The function prints the timeout message after 5 seconds.
2. Your script keeps running (the rest of the flight still happens).
3. The drone lands cleanly because the rest of `main()` — and the `land()` call — still gets to run.

This is the difference between a `sleep` and a real wait: a real wait can fail without crashing your program.
