#!/usr/bin/env python3
"""
Lesson 4 — Telemetry Streams

Print live altitude alongside the current flight mode while the drone hovers.

TODOs:
    1. Write track_flight_mode(drone, live) — keeps live["mode"] up to date.
    2. Write print_altitude(drone, live) — prints altitude AND live["mode"]
       on the same line, throttled to every 10th reading.
    3. After takeoff, create a `live = {"mode": "UNKNOWN"}` dict and run both
       coroutines with asyncio.gather, wrapped in asyncio.wait_for(..., timeout=15).
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


# Two coroutines share a `live` dict. One writes the latest flight mode into it;
# the other reads from it while printing altitude. The dict is the bridge between
# two streams running at the same time.

# TODO 1: write `async def track_flight_mode(drone, live):`
#         stream:  drone.telemetry.flight_mode()
#         body:    `live["mode"] = str(mode)` on every reading

# TODO 2: write `async def print_altitude(drone, live):`
#         stream:  drone.telemetry.position()  — use pos.relative_altitude_m
#         throttle: every 10th reading (count % 10 == 0)
#         print:   altitude AND live["mode"] on the same line


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

    # TODO 3: create `live = {"mode": "UNKNOWN"}`, then run track_flight_mode
    #         and print_altitude together with asyncio.gather, wrapped in
    #         asyncio.wait_for(..., timeout=15).

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
