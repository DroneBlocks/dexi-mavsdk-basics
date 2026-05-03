#!/usr/bin/env python3
"""
Lesson 8 — solution flight script.

This is the working reference flight for Lesson 8. It imports the helpers
from `solution_dexi_helpers.py` so you can see the lesson work end-to-end
without first filling in your own `dexi_helpers.py`.

When you do the lesson yourself, run `mission.py` instead — it imports
from `dexi_helpers.py`, which you'll write.
"""

import asyncio
from solution_dexi_helpers import connect, takeoff_to, safe_land


async def main():
    drone = await connect("udpin://0.0.0.0:14540")
    try:
        await takeoff_to(drone, 2.5)
        print("Hovering for 5s...")
        await asyncio.sleep(5)
    finally:
        await safe_land(drone)


if __name__ == "__main__":
    asyncio.run(main())
