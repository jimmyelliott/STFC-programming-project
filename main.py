from motor import SimpleMotor
from commands import handle_command


def run_cli(motor):
    while True:
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            break
        reply = handle_command(motor, line)
        if reply:                      # set commands like v= and stop reply nothing
            print(reply)


def main():
    motor = SimpleMotor()
    motor.start()                      # starts the 10 Hz update thread
    try:
        run_cli(motor)
    finally:
        motor.stop()                   # always stops the thread, even on Ctrl+C


if __name__ == "__main__":
    main()