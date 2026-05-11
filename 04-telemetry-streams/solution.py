#!/usr/bin/env python3
"""
Lesson 4 — Telemetry Streams (solution)
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


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
    await asyncio.sleep(8)


async def track_flight_mode(drone, live):
    async for mode in drone.telemetry.flight_mode():
        live["mode"] = str(mode)


async def print_altitude(drone, live):
    count = 0
    async for pos in drone.telemetry.position():
        count += 1
        if count % 10 == 0:
            print(f"alt: {pos.relative_altitude_m:.2f} m  mode: {live['mode']}")


async def main():
    drone = System()
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

    live = {"mode": "UNKNOWN"}

    try:
        await asyncio.wait_for(
            asyncio.gather(
                track_flight_mode(drone, live),
                print_altitude(drone, live),
            ),
            timeout=15,
        )
    except asyncio.TimeoutError:
        print("Telemetry window done.")

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
