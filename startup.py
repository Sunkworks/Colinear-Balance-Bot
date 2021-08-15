from indicator import *
import pygame
import time

def find_controller():
    screen = pygame.display.set_mode([10, 10])
    
    search_color = (0, 0, 255)
    heartbeat_state = False
    
    for i in range(0, 50):  # Makes sense to get the controller in pairing mode before searching
        indicate(1, (255, 255, 255))
        time.sleep(0.1)
        indicate(1, (0, 0, 255))
        time.sleep(0.1)
    
    while True:
        try:
            pygame.joystick.init()
            joy = pygame.joystick.Joystick(0)
            joy.init()
            print("Controller Found!")
            break
        except:
            print("Controller not found. Trying again...")
            color = search_color if heartbeat_state else (0, 0, 0)
            heartbeat_state = not heartbeat_state
            indicate(1, color)
            time.sleep(1)
    
    indicate(1, search_color)
    
    ready_for_boot = False
    while not ready_for_boot:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
                if joy.get_button(3):
                    print("Y pressed, proceeding to main")
                    ready_for_boot = True 
    
    pygame.quit()
    
