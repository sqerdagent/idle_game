import pygame
import sys
from mobs import TestFairy
from user_settings import *

#TODO: continue user settings


def main():
    #Initializing pygame module see: https://www.pygame.org/docs/ref/pygame.html
    pygame.init()
    print(f"Running Pygame version: {pygame.__version__}")
          

    #creating GUI Window https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    #Helper variables begin:
    fps_time_to_stdout_timer = 0 #Accumulates delta time
    mobs_on_screen = 0

    fairy_list = []

    #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock
    delta_time_clock = pygame.time.Clock()
    dt = 0
    print(f"Inititializing Delta Time Object {delta_time_clock} at dt:{dt}")
    
    while True:
        #get events from the queue https://www.pygame.org/docs/ref/event.html#pygame.event.get
        for event in pygame.event.get():
            #uninitialize all pygame modules https://www.pygame.org/docs/ref/pygame.html#pygame.quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        #Fill Screen: https://www.pygame.org/docs/ref/surface.html#pygame.Surface.fill
        screen.fill((45,45,45))


        #test code to have some fairies on screen
        if mobs_on_screen <= 100:
            fairy_list.append(TestFairy())
            mobs_on_screen += 1

        #Draw the Fairies:
        for fairy in fairy_list:
            fairy.update(dt)  #Change later for every object.
            screen.blit(fairy.image, fairy.rect)

        #Refresh Screen: https://www.pygame.org/docs/ref/display.html#pygame.display.flip
        pygame.display.flip()


        #update the clock https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
        dt = delta_time_clock.tick(60)/1000
        # time.sleep(1) #old method of limiting cpu usage

        #Simple output to stdout to show game is running.
        fps_time_to_stdout_timer += dt
        if fps_time_to_stdout_timer >=5:
            #https://www.pygame.org/docs/ref/time.html?highlight=fps#pygame.time.Clock.get_fps
            print(f"delta_time_clock is: {delta_time_clock} dt is: {dt} for {delta_time_clock.get_fps()} frames per second")
            #print(f"Rotation: {user_player1.rotation}")  #old irrelevent rotation check
            fps_time_to_stdout_timer = 0
    
    pass



main()