#!/usr/bin/env python3
"""
Lesson 6 — Lists Become Waypoints

Fly a 1m square at 3m altitude using offboard position setpoints.

TODOs:
    1. Define a `waypoints` list of (north, east, down) tuples.
    2. Write a for-loop that calls drone.offboard.set_position_ned for each one.
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


async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            break
    print("Connected!")

    await takeoff_to(drone, 3.0)

    # Re-enter offboard mode for waypoint flying
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print(f"offboard failed: {e._result.result}")

    # TODO 1: define waypoints — list of (north, east, down) tuples for a 1m square at 3m up

    # TODO 2: for loop that flies to each waypoint
    # for north, east, down in waypoints:
    #     ...

    try:
        await drone.offboard.stop()
    except OffboardError:
        pass

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
