# Lesson 1 — Hello, DEXI

**Python concept:** imports, running a script.
**You'll end with:** a script that connects to the simulator and prints `Connected to DEXI!`.

## The story

A drone is a computer with rotors. Before you can fly it, you have to talk to it. In this lesson you'll write the smallest possible program that talks to the DEXI Simulator — one that just says hello.

## What is MAVSDK?

**MAVSDK** is a Python library for talking to drones. (It also exists in C++, Swift, and a few other languages — same library, different programming languages.) Underneath, it speaks **MAVLink**, the standard messaging protocol used by autopilots like **PX4** (which DEXI runs) and ArduPilot. Picture the layers:

```
Your Python code
     ↓
MAVSDK         (turns Python calls into MAVLink messages)
     ↓
MAVLink        (the message format flying over UDP)
     ↓
PX4 autopilot  (running in the simulator — or on the real drone)
     ↓
Motors, sensors, the actual flight
```

You only ever touch the top of that stack. MAVSDK does the rest. The exact same Python code talks to a simulated drone today and a real one in Lesson 10 — only the address changes.

## How MAVSDK actually works under the hood

When you call `await drone.connect(...)`, MAVSDK quietly does something cool: it starts a small **C++ helper process called `mavsdk_server`** in the background, and your Python code talks to it over a fast local channel called **gRPC**. That C++ process is what actually speaks MAVLink to the drone.

Why two pieces? Because the heavy lifting — parsing thousands of MAVLink messages per second, keeping the link alive — is faster in C++. The Python library is a thin, friendly wrapper that lets you forget the messy parts.

You'll never start, stop, or talk to `mavsdk_server` directly. But if you ever run `ps` while a script is alive and spot a process with that name, **that's not a stray — it's MAVSDK doing its job.**

## What's in that connection string?

`udpin://0.0.0.0:14540` looks like gibberish. Let's break it down:

- **`udpin`** means "*listen* for incoming UDP messages" — we wait for the drone to talk to us. The opposite is **`udpout`**, meaning "*reach out* to a specific drone." You'll use `udpout` in Lesson 10 when we aim the same code at a real DEXI on your WiFi.
- **`0.0.0.0`** means "listen on every network interface on this computer." The simulator runs on the same machine, so it doesn't matter which interface — `0.0.0.0` is the catch-all.
- **`14540`** is the port number. By PX4 convention, **port 14540 is reserved for offboard / SDK control** — that's where MAVSDK and other developer tools live. Port 14550 is reserved for ground stations like QGroundControl. PX4 happily talks to both at once.

Same string, all the way through Lesson 9. Lesson 10 is the one place it changes.

## What you need

- The DEXI Simulator running (Unity scene + PX4 SITL)
- code-server open in your browser
- A terminal in code-server

## What to do

1. Confirm you cloned the lessons repo (you should be in `~/dexi-mavsdk-basics`).
2. **Install MAVSDK.** In the code-server terminal:
   ```
   pip3 install mavsdk
   ```
   You'll probably see `Requirement already satisfied: mavsdk` — the simulator container ships with it. **That's the success message**, not a problem. It means MAVSDK is ready.

   Confirm the version:
   ```
   python3 -c "import mavsdk; print(mavsdk.__version__)"
   ```
   Any version number is fine. (When you eventually run lessons on your own laptop, this same command tells you whether you need to install it for real.)
3. Open `01-hello-dexi/starter.py` in code-server and read every line. None of it should be a mystery.
4. Find the `TODO` and replace it with the SITL connection string:
   ```
   udpin://0.0.0.0:14540
   ```
5. Save and run:
   ```
   cd ~/dexi-mavsdk-basics/01-hello-dexi
   python3 starter.py
   ```
6. You should see:
   ```
   Waiting for drone...
   Connected to DEXI!
   ```

If you see that, you just had your first conversation with a drone. Press Ctrl+C to stop.

## Two new things you saw

- **`async def`** — this is a function that does work over time. Talking to a drone takes time (you have to wait for it to respond), so MAVSDK uses `async`. Don't worry about the details yet; we'll dig in next lesson.
- **`async for`** — this loops over a stream of data. The drone keeps publishing its state, and we keep reading until it says it's connected.

## Stretch challenge

After "Connected to DEXI!", print the drone's flight controller version. Add this before `return`:

```python
info = await drone.info.get_version()
print(info)
```

## When you're done

Open Lesson 2: `cd ../02-your-first-flight`
