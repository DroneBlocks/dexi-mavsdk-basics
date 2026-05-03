# Lesson 7 — When Things Go Wrong

**Python concept:** `try` / `except` / `finally`.
**You'll end with:** a mission that always lands, even if your code crashes.

## The story

A drone in flight when your script crashes is *not* okay. It will hold position, drain battery, and eventually fall. The `finally` block is the most important keyword in drone programming: it runs **no matter what** — whether the code finished cleanly, hit an exception, or got Ctrl+C'd.

This lesson is short. The pattern is small. But this is the difference between a hobby script and one you'd trust in the air.

## The pattern

```python
try:
    await takeoff_to(drone, 3.0)
    await fly_my_mission(drone)
except Exception as e:
    print(f"mission failed: {e}")
finally:
    print("landing safely")
    await drone.action.land()
```

- **`try`** — the risky stuff (takeoff, mission)
- **`except`** — runs only if something blew up; we log it
- **`finally`** — runs *always*; we land

## What to do

1. Open `07-when-things-go-wrong/starter.py`. It's your Lesson 6 mission.
2. Wrap the body of `main()` (after the connection wait) in `try` / `except` / `finally`.
3. Move the `await drone.action.land()` into the `finally` block.
4. Run it. Confirm it still lands cleanly.
5. **Now break it on purpose.** Right after takeoff, add `raise RuntimeError("simulated failure")`. Run it again. Confirm:
   - The error message prints
   - The drone *still lands*

That second test is the important one.

## Stretch challenge

What happens if the **connection drops** mid-mission? Try catching the specific exception type:

```python
from mavsdk.offboard import OffboardError

except OffboardError as e:
    print(f"offboard error: {e._result.result}")
except Exception as e:
    print(f"unexpected error: {e}")
```

Two `except` blocks, most-specific first. This is a Python pattern you'll see in every robust program.

## Why "Exception" and not just `except:`?

A bare `except:` catches *everything*, including Ctrl+C. That means you couldn't even stop your script. `except Exception:` catches programming errors but lets the user always interrupt. Use the named version.
