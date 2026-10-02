import os
import csv
import time
import random
import threading
from xarm.wrapper import XArmAPI

# ---------------- Settings ----------------
IP           = "192.168.1.150"
DRY_RUN      = False     # True = only print the moves, don't move the arm
REPETITIONS  = 200
CALIB_MOVES  = 3         # first N iterations are zero moves (calibration)
PAUSE_S      = 0.5       # pause at the random pose before returning
SPEED_MOVE   = 100       # mm/s for the random move
SPEED_BACK   = 100       # mm/s for the return to home
LOG_DT       = 0.02      # seconds between logged samples
MAX_FAILURES = 5         # stop after this many failed moves in a row

# Max random offset from the home pose, per axis
TRANS_RANGE = [(-30, 30), (-30, 30), (-30, 30)]   # x, y, z in mm
ROT_RANGE   = [(-15, 15), (-15, 15), (-15, 15)]   # roll, pitch, yaw in deg

os.makedirs("Data", exist_ok=True)
CSV_PATH = os.path.join("Data", f"{time.time()}.csv")


# ---------------- Helpers ----------------
def diagnose(what, code):
    """Print everything useful about why a command failed."""
    _, err_warn = arm.get_err_warn_code()
    _, state = arm.get_state()
    _, pos = arm.get_position(is_radian=False)
    print(f"  !! {what} failed: return code {code}, state={state}, "
          f"error/warn from controller={err_warn}, collision_sensitivity={arm.collision_sensitivity}")
    print(f"     current pose: {[round(v, 2) for v in pos] if pos else pos}")


def recover():
    """Clear errors and put the arm back in a ready-to-move state."""
    arm.clean_warn()
    arm.clean_error()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(state=0)
    time.sleep(1.0)


def go_home():
    """Return to the recorded home pose; recover and retry once if needed."""
    for attempt in (1, 2):
        code = arm.set_position(*HOME, speed=SPEED_BACK, wait=True)
        if code == 0:
            return
        diagnose(f"return home (attempt {attempt})", code)
        recover()
    raise RuntimeError("Could not return to home pose, stopping.")


def random_offset(i):
    """Zero for calibration moves, otherwise a random offset from home."""
    if i <= CALIB_MOVES:
        return [0, 0, 0, 0, 0, 0]
    t = [random.randint(lo, hi) for lo, hi in TRANS_RANGE]
    r = [random.randint(lo, hi) for lo, hi in ROT_RANGE]
    return t + r


# ---------------- Logger (runs in background) ----------------
phase = {"name": "init", "iter": 0}
stop_logging = threading.Event()


def logger(path):
    with open(path, mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time", "iteration", "phase",
                    "x_mm", "y_mm", "z_mm", "roll_rad", "pitch_rad", "yaw_rad"])
        while not stop_logging.is_set():
            code, pos = arm.get_position(is_radian=True)
            if code == 0:
                w.writerow([time.time(), phase["iter"], phase["name"]] + list(pos))
            time.sleep(LOG_DT)


# ---------------- Setup ----------------
arm = XArmAPI(IP)
recover()

if not DRY_RUN:
    code = arm.move_gohome(wait=True)
    if code != 0:
        diagnose("move_gohome", code)
        raise SystemExit(1)
    code = arm.set_tool_position(x=100, y=100, z=0, roll=0, pitch=0, yaw=0,
                                 speed=20, wait=True)
    if code != 0:
        diagnose("initial move", code)
        raise SystemExit(1)

# Record the exact home pose (degrees) so we can return to it absolutely
code, HOME = arm.get_position(is_radian=False)
if code != 0:
    raise SystemExit(f"get_position failed with code {code}")
HOME = list(HOME)
print("Home pose:", [round(v, 3) for v in HOME])

log_thread = threading.Thread(target=logger, args=(CSV_PATH,), daemon=True)
log_thread.start()
print("Starting capture")

# ---------------- Main loop ----------------
failures = 0
skipped = []

try:
    for i in range(1, REPETITIONS + 1):
        offset = random_offset(i)
        dx, dy, dz, dr, dp, dyaw = offset
        print(f"[{i}/{REPETITIONS}] offset: {dx} {dy} {dz} | {dr} {dp} {dyaw}")

        if DRY_RUN:
            continue

        # 1) Random move, relative to the tool frame
        phase.update(name="move", iter=i)
        code = arm.set_tool_position(x=dx, y=dy, z=dz, roll=dr, pitch=dp, yaw=dyaw,
                                     speed=SPEED_MOVE, wait=True)
        if code != 0:
            diagnose("random move", code)
            skipped.append((i, offset))
            failures += 1
            if failures >= MAX_FAILURES:
                raise RuntimeError(f"{failures} failed moves in a row, stopping.")
            recover()
            phase.update(name="return")
            go_home()
            continue
        failures = 0

        # 2) Pause at the random pose
        phase.update(name="pause")
        time.sleep(PAUSE_S)

        # 3) Return to the recorded home pose (absolute, so no drift)
        phase.update(name="return")
        go_home()

        # Report how accurately we got back
        _, now = arm.get_position(is_radian=False)
        err = max(abs(a - b) for a, b in zip(now[:3], HOME[:3]))
        print(f"    back home, max position error: {err:.3f} mm")

except KeyboardInterrupt:
    print("Interrupted by user")
    arm.set_state(4)   # stop motion
finally:
    stop_logging.set()
    log_thread.join()
    if skipped:
        print(f"Skipped {len(skipped)} moves that failed:")
        for i, off in skipped:
            print(f"  iteration {i}: {off}")
    arm.disconnect()
    print("finished:", CSV_PATH)
