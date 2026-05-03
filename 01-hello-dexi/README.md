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
