# Lesson 3 — Functions That Fly

**Python concept:** function parameters and return values.
**You'll end with:** a reusable `takeoff_to(drone, altitude)` function — and a script that uses it twice with different altitudes.

## The story

Look at your Lesson 2 script. The takeoff section is six lines of detail: send offboard signal, sleep, arm, stop offboard, set altitude, takeoff. If you wanted to take off to a different altitude in another script, you'd copy all six lines and remember to change the right number.

Real programmers wrap details in **functions**. In this lesson you'll write `takeoff_to(drone, altitude_m)` — once. Then every future lesson will just call `await takeoff_to(drone, 2.5)`.

## What to do

### Part 1: refactor

1. Open `03-functions-that-fly/starter.py`. It's the same flow as Lesson 2, but the takeoff lines are gone — replaced with a single `# TODO: call takeoff_to(...)`.
2. Above `main()`, write the function:
   ```python
   async def takeoff_to(drone, altitude_m):
       # send offboard signal
       # arm
       # stop offboard
       # set altitude and takeoff
       # wait
   ```
   Move the boilerplate from Lesson 2 into the function body.
3. In `main()`, call it: `await takeoff_to(drone, 2.5)`.
4. Run it. Same flight, cleaner code.

### Part 2: try it twice

Add a second flight after landing:

```python
await takeoff_to(drone, 4.0)
await asyncio.sleep(3)
await drone.action.land()
```

Now you've reused the function with a different altitude. **That's the win.** One function, two flights, no copy-paste.

## Why this matters

Every helper you write in this course will look exactly like `takeoff_to`: an `async def`, a few `await`s inside, called from `main()`. By Lesson 8 you'll have a small library of these helpers, and your missions will read like English.

## Stretch challenge

Write a second helper: `async def safe_land(drone)`. It should call `drone.action.land()` and then `drone.action.disarm()` after a 10-second wait. Use it instead of the bare `await drone.action.land()` in `main()`.

## When you're done

Open Lesson 4: `cd ../04-telemetry-streams`
