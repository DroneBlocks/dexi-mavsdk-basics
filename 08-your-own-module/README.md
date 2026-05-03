# Lesson 8 — Your Own Module

**Python concept:** importing across files.
**You'll end with:** a `dexi_helpers.py` you wrote, used from a clean `mission.py`.

## The story

You've now written `wait_until_altitude`, `takeoff_to`, and the offboard preamble three or four times. That's three or four times too many. In real Python projects, helpers live in their own file. You import them.

## How imports actually work

Every `.py` file is a **module**. When you write `import dexi_helpers`, Python finds `dexi_helpers.py` in the same directory, runs it once, and gives you everything inside. After that, `dexi_helpers.takeoff_to(...)` works just like any other function.

The shorter form `from dexi_helpers import takeoff_to` does the same thing but lets you call `takeoff_to(...)` without the `dexi_helpers.` prefix.

## What to do

1. Open `08-your-own-module/`. There's a `dexi_helpers.py` (mostly empty) and a `mission.py` (also mostly empty).
2. Move your helpers into `dexi_helpers.py`:
   - `connect(address)` — returns a connected `drone`
   - `takeoff_to(drone, altitude_m)`
   - `wait_until_altitude(drone, target_m, tolerance=0.3)`
   - `safe_land(drone)`
3. In `mission.py`, write a short flight script that uses them:
   ```python
   from dexi_helpers import connect, takeoff_to, safe_land

   async def main():
       drone = await connect("udpin://0.0.0.0:14540")
       try:
           await takeoff_to(drone, 2.5)
           await asyncio.sleep(5)
       finally:
           await safe_land(drone)
   ```
4. Run `python3 mission.py`. It should look almost like English.

> **Stuck or just want to see it work first?** Run `python3 solution.py` — it imports the filled-in helpers from `solution_dexi_helpers.py` and flies the same mission.

## Why this is a big deal

Compare your `mission.py` to your Lesson 2 `starter.py`. The Lesson 2 script was 50 lines of detail. The Lesson 8 mission is 10 lines of intent. Same flight, completely different to read. **That's what a good module does** — it lets you write code at the level you're thinking, not at the level the drone needs.

You'll keep using `dexi_helpers.py` for the rest of the course (and beyond).

## Stretch challenge

Add type hints to every function in `dexi_helpers.py`:

```python
from mavsdk import System

async def takeoff_to(drone: System, altitude_m: float) -> None:
    ...
```

Type hints don't change how Python runs — they're notes for humans (and tools). Your editor will start helping you more once they're there.

## When you're done

Open Lesson 9: `cd ../09-capstone-design-a-mission`
