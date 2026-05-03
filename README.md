# DEXI MAVSDK Basics

The intro course in the DEXI MAVSDK series. A 10-lesson bridge from "I just learned Python" to "I just flew an autonomous mission in the DEXI Simulator."

Each lesson is a small Python script (under 40 lines) that runs against PX4 SITL today and unchanged on real DEXI hardware tomorrow. That sim-to-real promise is the whole point.

## Who this is for

Middle school and up. You should already know Python basics: variables, functions, loops, conditionals, lists. If those are unfamiliar, take *Python In 14 Days* or *Python Unpacked: Coding for Teachers* in the DroneBlocks portal first.

## Before you start

1. Open the DEXI Simulator. Wait for the Unity scene and PX4 SITL to come up.
2. Open code-server in your browser at `https://<your-sim-host>:9999` (password: `droneblocks`).
3. In code-server, open a terminal: **Terminal → New Terminal**.
4. Verify MAVSDK is installed:
   ```
   python3 -c "import mavsdk; print(mavsdk.__version__)"
   ```
   You should see a version number. If you see an error, ask your teacher.
5. Get the lessons:
   ```
   cd ~
   git clone https://github.com/DroneBlocks/dexi-mavsdk-basics.git
   cd dexi-mavsdk-basics
   ```
   No GitHub account needed — anyone can clone a public repo. We won't push anything in this course.

## The 10 lessons

| # | Lesson | What you'll learn |
|---|--------|-------------------|
| 1 | Hello, DEXI | Connect to the simulator |
| 2 | Your First Flight | Takeoff, hover, land |
| 3 | Functions That Fly | Reusable helpers |
| 4 | Telemetry Streams | Watch the drone live |
| 5 | Decisions in the Air | Wait for evidence, not for time |
| 6 | Lists Become Waypoints | Fly a 1m square |
| 7 | When Things Go Wrong | Always land safely |
| 8 | Your Own Module | Build `dexi_helpers.py` |
| 9 | Capstone | Design and fly your own mission |
| 10 | From Sim to Real | One connection string from a real drone |

## How each lesson is laid out

Every lesson directory contains:

- `README.md` — the lesson itself: what to learn, what to do, and the git task
- `starter.py` — a script with `TODO` comments where you'll write code
- `solution.py` — a working reference. Try the lesson first; peek if you're stuck.

## Reference code

The DEXI team maintains working examples at `~/dexi-mavsdk` in your sim environment. These lessons rebuild some of those scripts from scratch so you understand every line.

## Want to save your work to GitHub?

This course doesn't cover that on purpose — it would distract from the drone code. If you (or your students) want to learn how to clone, branch, push, and collaborate, take the companion course **Git & GitHub for Drone Developers**.
