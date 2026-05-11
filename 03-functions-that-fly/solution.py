#!/usr/bin/env python3
"""
Lesson 3 — Functions That Fly (solution)

Refactor the takeoff sequence into a reusable function.
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def takeoff_to(drone, altitude_m):
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

    print(f"Taking off to {altitude_m}m...")
    await drone.action.set_takeoff_altitude(altitude_m)
    await drone.action.takeoff()
    await asyncio.sleep(8)


async def main():
    drone = System()

    print("Connecting...")
    # Connection string — pick one. See README for context.
    #   Simulator (this lesson):   udpin://0.0.0.0:14540
    #   Running on DEXI's Pi:      udpout://127.0.0.1:14540
    #   Host on DEXI's WiFi:       udpout://192.168.4.1:14540
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
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
