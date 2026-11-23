import math


def handle_command(motor, line):
    cmd = line.strip()

    queries = {
        "p?": lambda: f"p={motor.get_position():.1f}",
        "v?": lambda: f"v={motor.get_velocity():.1f}",
    }
    if cmd in queries:
        return queries[cmd]()

    if cmd == "stop":
        motor.stop_motion()
        return None

    if cmd.startswith("v="):
        # parse the number after "v="; if it isn't a valid float, fall through
        try:
            velocity = float(cmd[2:])
        except ValueError:
            velocity = None
        if velocity is not None and math.isfinite(velocity):   # reject nan / inf
            motor.set_velocity(velocity)
            return None

    return "Unknown command"