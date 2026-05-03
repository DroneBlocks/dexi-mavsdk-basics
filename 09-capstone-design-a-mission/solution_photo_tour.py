#!/usr/bin/env python3
"""
Lesson 9 — Capstone (one possible solution: Photo Tour)

Mission description:
    Fly to four named "landmarks" around the takeoff point at 3m altitude.
    Hover for 3 seconds at each (pretending to take a photo). Return home and land.
    Print battery percentage at each landmark.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-your-own-module"))
# Use the worked solution helpers so this script flies regardless of whether
# the student has filled in their own dexi_helpers.py from Lesson 8.
from solution_dexi_helpers import connect, takeoff_to, safe_land

from mavsdk.offboard import OffboardError, PositionNedYaw


LANDMARKS = {
    "north_overlook": (3.0, 0.0, -3.0),
    "east_garden":    (0.0, 3.0, -3.0),
    "south_meadow":   (-3.0, 0.0, -3.0),
    "west_pond":      (0.0, -3.0, -3.0),
}


async def get_battery_percent(drone):
    async for bat in drone.telemetry.battery():
        return bat.remaining_percent * 100


async def main():
    drone = await connect("udpin://0.0.0.0:14540")
    try:
        await takeoff_to(drone, 3.0)

        await drone.offboard.set_position_ned(PositionNedYaw(0, 0, -3, 0))
        try:
            await drone.offboard.start()
        except OffboardError:
            pass

        for name, (n, e, d) in LANDMARKS.items():
            print(f"flying to {name}...")
            await drone.offboard.set_position_ned(PositionNedYaw(n, e, d, 0))
            await asyncio.sleep(5)
            battery = await get_battery_percent(drone)
            print(f"  arrived at {name}. battery: {battery:.0f}%. snap!")
            await asyncio.sleep(3)

        print("returning home...")
        await drone.offboard.set_position_ned(PositionNedYaw(0, 0, -3, 0))
        await asyncio.sleep(5)

        try:
            await drone.offboard.stop()
        except OffboardError:
            pass
    finally:
        await safe_land(drone)


if __name__ == "__main__":
    asyncio.run(main())
