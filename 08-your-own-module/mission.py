#!/usr/bin/env python3
"""
Lesson 8 — Your Own Module

Use the helpers from dexi_helpers.py to write a tiny, readable mission.
"""

import asyncio
from dexi_helpers import connect, takeoff_to, safe_land


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
