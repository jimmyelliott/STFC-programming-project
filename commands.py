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
        ...

    return "Unknown command"