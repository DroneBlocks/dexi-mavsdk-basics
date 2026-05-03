#!/usr/bin/env python3
"""
Lesson 7 — When Things Go Wrong (solution)
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw, VelocityBodyYawspeed


async def wait_until_altitude(drone, target_m, tolerance=0.3):
    async for pos in drone.telemetry.position():
        if abs(pos.relative_altitude_m - target_m) < tolerance:
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


async def fly_box(drone):
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    try:
        await drone.offboard.start()
    except OffboardError:
        pass

    waypoints = [(1.0, 0.0, -3.0), (1.0, 1.0, -3.0), (0.0, 1.0, -3.0), (0.0, 0.0, -3.0)]
    for n, e, d in waypoints:
        await drone.offboard.set_position_ned(PositionNedYaw(n, e, d, 0.0))
        await asyncio.sleep(5)

    try:
        await drone.offboard.stop()
    except OffboardError:
        pass


async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            break
    print("Connected!")

    try:
        await takeoff_to(drone, 3.0)
        await fly_box(drone)
    except Exception as e:
        print(f"mission failed: {e}")
    finally:
        print("landing safely")
        await drone.action.land()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
