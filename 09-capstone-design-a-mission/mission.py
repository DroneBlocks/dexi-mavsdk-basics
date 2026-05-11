#!/usr/bin/env python3
"""
Lesson 9 — Capstone

Mission description (in plain English):
    TODO: write 2-3 sentences describing what your drone does.

Reuses helpers from Lesson 8.
"""

import asyncio
import sys
from pathlib import Path

# Pull in helpers from Lesson 8
sys.path.insert(0, str(Path(__file__).parent.parent / "08-your-own-module"))
from dexi_helpers import connect, takeoff_to, safe_land


async def main():
    # Connection string — pick one. See README for context.
    #   Simulator (this lesson):   udpin://0.0.0.0:14540
    #   Running on DEXI's Pi:      udpout://127.0.0.1:14540
    #   Host on DEXI's WiFi:       udpout://192.168.4.1:14540
    drone = await connect("udpin://0.0.0.0:14540")
    try:
        # TODO: your mission code here
        await takeoff_to(drone, 2.0)
        await asyncio.sleep(3)
    finally:
        await safe_land(drone)


if __name__ == "__main__":
    asyncio.run(main())
