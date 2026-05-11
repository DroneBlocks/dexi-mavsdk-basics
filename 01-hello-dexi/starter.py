#!/usr/bin/env python3
"""
Lesson 1 — Hello, DEXI

Connect to the DEXI Simulator and print "Connected to DEXI!".

TODO:
    Replace the empty string with the SITL connection address.
    See the README for what to use.
"""

import asyncio
from mavsdk import System


async def main():
    drone = System()

    # TODO: replace "" with a connection string from the list below.
    #   Simulator (start here):    udpin://0.0.0.0:14540
    #   Running on DEXI's Pi:      udpout://127.0.0.1:14540
    #   Host on DEXI's WiFi:       udpout://192.168.4.1:14540
    await drone.connect(system_address="")

    print("Waiting for drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to DEXI!")
            return


if __name__ == "__main__":
    asyncio.run(main())
