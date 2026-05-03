# Lesson 4 — Telemetry Streams

**Python concept:** `async for`, iterating over a stream; sharing state between coroutines with a dict.
**You'll end with:** a script that prints the drone's altitude and current flight mode on one line, live, while it flies.

## The story

In Lesson 1 you used `async for` to wait for the connection state. That was an **async iterator** — it produces values one at a time, forever, as the drone publishes them. Telemetry works the same way. The drone publishes its position about 20 times a second; you subscribe and read.

This is how you find out what's actually happening on the drone. Without telemetry, you're flying blind.

In this lesson you'll subscribe to **two** streams at once — altitude and flight mode — and combine them on a single output line.

## What you'll build

Two coroutines that share a dict:

- `track_flight_mode(drone, live)` reads the flight-mode stream and stores the latest value in `live["mode"]`.
- `print_altitude(drone, live)` reads the position stream and prints altitude **plus** whatever mode is currently in `live["mode"]`.

```python
async def track_flight_mode(drone, live):
    async for mode in drone.telemetry.flight_mode():
        live["mode"] = str(mode)


async def print_altitude(drone, live):
    count = 0
    async for pos in drone.telemetry.position():
        count += 1
        if count % 10 == 0:
            print(f"alt: {pos.relative_altitude_m:.2f} m  mode: {live['mode']}")
```

Then run them at the same time using `asyncio.gather`:

```python
live = {"mode": "UNKNOWN"}

await asyncio.gather(
    track_flight_mode(drone, live),
    print_altitude(drone, live),
)
```

## Why a shared dict?

Each `async for` loop is locked onto one stream. To combine data from two streams on a single line, one coroutine has to leave a "note" the other can read. A dict is a great note: passed by reference, so when `track_flight_mode` updates `live["mode"]`, `print_altitude` sees the new value on its very next print.

## Why throttle?

The position stream fires 10–20 times a second. Print every reading and the terminal is unreadable. The `count % 10 == 0` pattern prints once every ten readings — about twice a second — which is the sweet spot for human eyes.

We don't throttle `track_flight_mode` because it doesn't print anything. It just keeps `live["mode"]` fresh, as fast as the drone tells it to.

## What you'll see

Roughly twice a second:

```
alt: 2.48 m  mode: HOLD
alt: 2.48 m  mode: HOLD
alt: 2.48 m  mode: HOLD
```

> Note: the landing happens *after* the telemetry window closes, so you won't see `mode: LAND` in the output. That's a fun thing to fix in Lesson 5 once you know how to wait for events.

## What to do

1. Open `04-telemetry-streams/starter.py`. It connects, takes off, and lands — using your `takeoff_to` function from Lesson 3.
2. Find TODO 1 and write `track_flight_mode(drone, live)`.
3. Find TODO 2 and write `print_altitude(drone, live)` — make sure it prints altitude AND `live["mode"]` on the same line, every 10th reading.
4. Find TODO 3 in `main()`. Create `live = {"mode": "UNKNOWN"}` and run both coroutines with `asyncio.gather(...)`, wrapped in `asyncio.wait_for(..., timeout=15)`.
5. Run it.

## Why `asyncio.wait_for`?

`async for` over telemetry is **infinite** — the drone never stops publishing. If you don't put a timeout on it, your script hangs forever. `asyncio.wait_for` gives you a polite "stop after N seconds."

## Stretch challenge

Add **battery** to the same line. You already have the pattern:

1. Add another coroutine `track_battery(drone, live)` that updates `live["battery"]` on every reading.
2. Add it to the `asyncio.gather(...)` call.
3. Update the print in `print_altitude` to include `live['battery']`.

Tip: the simulator pins battery near 100% — it doesn't drain. The real drone does.
