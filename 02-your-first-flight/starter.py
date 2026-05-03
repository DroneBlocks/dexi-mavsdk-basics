#!/usr/bin/env python3
"""
Lesson 2 — Your First Flight

Takeoff to 2 meters, hover for 5 seconds, land.

TODOs:
    1. Fill in the SITL connection address.
    2. Set the takeoff altitude (in meters).
    3. Set the hover time (in seconds).
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def main():
    drone = System()

    print("Connecting...")
    # TODO 1: connection address
    await drone.connect(system_address="")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    # --- Boilerplate: SITL needs an offboard signal before arming ---
    print("Sending offboard signal...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print(f"offboard start failed: {e._result.result}")
    await asyncio.sleep(1.5)
    # --- End boilerplate ---

    print("Arming...")
    await drone.action.arm()

    # Stop offboard so we can use action.takeoff()
    try:
        await drone.offboard.stop()
    except OffboardError:
        pass

    # TODO 2: set the takeoff altitude (try 2.0)
    altitude_m = 0.0
    print(f"Taking off to {altitude_m}m...")
    await drone.action.set_takeoff_altitude(altitude_m)
    await drone.action.takeoff()
    await asyncio.sleep(8)  # rough wait for takeoff

    # TODO 3: hover time in seconds (try 5)
    hover_seconds = 0
    print(f"Hovering for {hover_seconds}s...")
    await asyncio.sleep(hover_seconds)

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
