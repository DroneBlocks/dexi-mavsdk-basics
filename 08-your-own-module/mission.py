#!/usr/bin/env python3
"""
Lesson 8 — Your Own Module

Use the helpers from dexi_helpers.py to write a tiny, readable mission.
"""

import asyncio
from dexi_helpers import connect, takeoff_to, safe_land


async def main():
    # Connection string — pick one. See README for context.
    #   Simulator (this lesson):   udpin://0.0.0.0:14540
    #   Running on DEXI's Pi:      udpout://127.0.0.1:14540
    #   Host on DEXI's WiFi:       udpout://192.168.4.1:14540
    drone = await connect("udpin://0.0.0.0:14540")
    try:
        await takeoff_to(drone, 2.5)
        print("Hovering for 5s...")
        await asyncio.sleep(5)
    finally:
        await safe_land(drone)


if __name__ == "__main__":
    asyncio.run(main())
