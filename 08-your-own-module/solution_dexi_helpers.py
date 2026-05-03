#!/usr/bin/env python3
"""
dexi_helpers — solution reference.

Rename this to dexi_helpers.py if you want to use it directly.
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed


async def connect(address):
    drone = System()
    await drone.connect(system_address=address)
    async for state in drone.core.connection_state():
        if state.is_connected:
            return drone


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


async def safe_land(drone):
    print("landing safely")
    await drone.action.land()
    await asyncio.sleep(10)
    try:
        await drone.action.disarm()
    except Exception:
        pass
