import time

import manual_navigator


def countdown_seconds(seconds):
    for i in range(seconds):
        print(seconds - i)
        time.sleep(1)


def main():
    navigator = manual_navigator.ManualNavigator()
    countdown_seconds(3)
    try:
        while True:
            navigator.start()
            iter_count = 0
            max_iter_count = 1000
            while not navigator.fallen_over:
                navigator.main_task()

                if iter_count % 100:
                    navigator.pid.update_constants()
                    navigator.print_telemetry()

                iter_count = iter_count % max_iter_count
                time.sleep(0.001)

            input("Angle too big, press enter to continue")

    finally:
        navigator.stop()
        navigator.cleanup()


if __name__ == '__main__':
    main()
