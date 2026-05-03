#!/usr/bin/env python3
"""
Lesson 5 — Decisions in the Air

Replace the rough sleep-based takeoff wait with a real telemetry check.

TODOs:
    1. Write wait_until_altitude(drone, target_m, tolerance=0.3).
    2. Use it inside takeoff_to() instead of asyncio.sleep(8).
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


# TODO 1: write `async def wait_until_altitude(drone, target_m, tolerance=0.3):`


async def takeoff_to(drone, altitude_m):
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
    try:
        await drone.offboard.start()
    except OffboardError:
        pass
    await asyncio.sleep(1.5)
    await drone.action.arm()
    try:
        await drone.offboard.stop()
    except OffboardError:
        pass
    await drone.action.set_takeoff_altitude(altitude_m)
    await drone.action.takeoff()
    # TODO 2: replace this sleep with await wait_until_altitude(drone, altitude_m)
    await asyncio.sleep(8)


async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    await takeoff_to(drone, 2.5)
    print("Hovering for 5s...")
    await asyncio.sleep(5)

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
