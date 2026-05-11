#!/usr/bin/env python3
"""
Lesson 3 — Functions That Fly

Refactor the takeoff sequence into a reusable function.

TODOs:
    1. Write the takeoff_to(drone, altitude_m) function above main().
       Move the offboard/arm/takeoff boilerplate from Lesson 2 into it.
    2. Call takeoff_to from main().
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


# TODO 1: write `async def takeoff_to(drone, altitude_m):` here


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

    # TODO 2: call takeoff_to(drone, 2.5)

    print("Hovering for 5s...")
    await asyncio.sleep(5)

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
