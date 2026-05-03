#!/usr/bin/env python3
"""
Lesson 1 — Hello, DEXI (solution)

Connect to the DEXI Simulator and print "Connected to DEXI!".
"""

import asyncio
from mavsdk import System


async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to DEXI!")
            return


if __name__ == "__main__":
    asyncio.run(main())
