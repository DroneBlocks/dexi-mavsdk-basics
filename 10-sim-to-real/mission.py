#!/usr/bin/env python3
"""
Lesson 10 — From Sim to Real DEXI

Run against the sim:
    python3 mission.py

Run against a real DEXI on your WiFi:
    DEXI_ADDRESS=udpout://192.168.4.1:14540 python3 mission.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-your-own-module"))
from dexi_helpers import connect, takeoff_to, safe_land


async def main():
    address = os.environ.get("DEXI_ADDRESS", "udpin://0.0.0.0:14540")
    print(f"using address: {address}")

    drone = await connect(address)
    try:
        await takeoff_to(drone, 2.0)
        print("hovering for 5s...")
        await asyncio.sleep(5)
    finally:
        await safe_land(drone)


if __name__ == "__main__":
    asyncio.run(main())
