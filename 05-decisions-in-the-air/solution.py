#!/usr/bin/env python3
"""
Lesson 5 — Decisions in the Air (solution)
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def wait_until_altitude(drone, target_m, tolerance=0.3):
    async for pos in drone.telemetry.position():
        diff = abs(pos.relative_altitude_m - target_m)
        if diff < tolerance:
            print(f"reached {target_m}m")
            return


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
    await wait_until_altitude(drone, altitude_m)


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
