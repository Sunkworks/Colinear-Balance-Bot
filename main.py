import time
import multiprocessing as mp
from multiprocessing import Process
import math

import simple_navigator
import os
import neopixel
import board
from remote import RemoteController
from indicator import indicate
from startup import find_controller

def main():
    find_controller()
    #p1 = mp.Process(target=find_controller, args=())
    #p1.start()

    heartbeat_color = (255, 0, 255)
    heartbeat_state = True

    indicate(2, (255, 255, 0))
    navigator = simple_navigator.ManualNavigator()
    
    indicate(0, (255, 255, 255))
    while not navigator.get_button(1):
        time.sleep(0.1)

    try:
        while True:
            navigator.start()
            #p2 = mp.Process(target=navigator.start, args=())
            #p2.start()
          
            indicate(0,(0, 255, 0))
            iter_count = 0
            max_iter_count = 1000
            while not navigator.fallen_over:
                navigator.main_task()
                #p3 = mp.Process(target=navigator.main_task.start, args=())
                #p3.start()
                
                
                if not iter_count % 32:
                    color = heartbeat_color if heartbeat_state else (255, 255, 255)
                    indicate(0, color)
                    heartbeat_state = not heartbeat_state
                    navigator.update_constants()
                    navigator.print_telemetry()
                    if navigator.get_button(0):
                        break

                iter_count += 1
                iter_count = iter_count % max_iter_count
                time.sleep(0.001)

            navigator.stop()
            indicate(0, (255, 0, 0))
            print("Manual halt or angle threshold reached, press x to enable motors")
            while not navigator.get_button(1):
                time.sleep(0.1)

    finally:
        navigator.stop()
        navigator.cleanup()
        for i in range(3):
            indicate(i, (255, 0, 0))


if __name__ == '__main__':
    main()
"""
    processes = []

    for i in range(os.cpu_count()):
        print('registering process %d' % i)
        processes.append(Process(target=calc))

    for process in processes:
        process.start()

    for process in processes:
        process.join()
    

#p1 = mp.Process(target=navigator.start, args=())
#Test

"""