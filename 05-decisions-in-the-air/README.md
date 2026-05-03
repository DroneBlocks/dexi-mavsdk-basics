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
2. Find the `TODO` and write the function:
   ```python
   async def wait_until_altitude(drone, target_m, tolerance=0.3):
       async for pos in drone.telemetry.position():
           diff = abs(pos.relative_altitude_m - target_m)
           if diff < tolerance:
               print(f"reached {target_m}m")
               return
   ```
3. In `takeoff_to`, replace the `await asyncio.sleep(8)` with `await wait_until_altitude(drone, altitude_m)`.
4. Run it. The drone takes off and reports as soon as it actually reaches altitude — not 8 seconds, however long it actually takes.

## Read the comparison carefully

```python
diff = abs(pos.relative_altitude_m - target_m)
if diff < tolerance:
```

`abs()` makes the difference positive whether the drone overshoots or undershoots. Without `abs()`, an overshoot would give a negative number that's always less than 0.3, and the function would return too early.

## Stretch challenge

What if the drone *never* reaches that altitude? Right now your script would hang forever. Add a 30-second safety timeout:

```python
async def wait_until_altitude(drone, target_m, tolerance=0.3, timeout_s=30):
    try:
        await asyncio.wait_for(
            _wait_until_altitude_loop(drone, target_m, tolerance),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        print(f"timeout: didn't reach {target_m}m in {timeout_s}s")
```

Move the original loop into `_wait_until_altitude_loop`. The leading underscore is a Python convention for "internal helper."
