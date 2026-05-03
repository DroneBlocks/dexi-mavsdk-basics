#!/usr/bin/env python3
"""
Lesson 2 — Your First Flight (solution)

Takeoff to 2 meters, hover for 5 seconds, land.
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def main():
    drone = System()

    print("Connecting...")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    print("Sending offboard signal...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print(f"offboard start failed: {e._result.result}")
    await asyncio.sleep(1.5)

    print("Arming...")
    await drone.action.arm()

    try:
        await drone.offboard.stop()
    except OffboardError:
        pass

    altitude_m = 2.0
    print(f"Taking off to {altitude_m}m...")
    await drone.action.set_takeoff_altitude(altitude_m)
    await drone.action.takeoff()
    await asyncio.sleep(8)

    hover_seconds = 5
    print(f"Hovering for {hover_seconds}s...")
    await asyncio.sleep(hover_seconds)

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
