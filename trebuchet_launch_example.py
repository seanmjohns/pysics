# pygame
import pygame
from pygame.locals import *

# Python libraries
import sys
import math

# pysics
from pysics.manager import PhysicsManager
from pysics.force import Force
from pysics.physics_obj import PhysicsObject
from pysics import force

# Setting up pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Sans Serif", 20)

# Setup the window
width = 800
height = 400

window = pygame.display.set_mode([width, height])
pygame.display.set_caption("Trebuchet")

#Set up pysics
tick_length = 0.1
manager = PhysicsManager(tick_length)

clock = pygame.time.Clock()
fps = 120

trebuchet_image = pygame.image.load("images/trebuchet.png")

#configured stuff
rock_color = pygame.Color(0,0,0)
rock_radius = 5

starting_pos = 10

# Will be inputted in 
rock_mass = 3
launch_angle = 45 #degrees from the vertical
launch_velocity = 50 #m/s
starting_height = 10 #meters

def draw_rock(rock):

    pygame.draw.circle(window, rock_color, (int(rock.xpos), height-int(rock.ypos)), rock_radius) #y=0 is at the top of the screen

def main():

    if len(sys.argv) < 5:
        print("usage - python3 trebuchet_launch.py <rock_mass> <launch_angle> <launch_velocity> <starting_height>")
        print("    rock_mass - the rock's mass in kilograms")
        print("    launch_angle - the angle of launch from the vertical in degrees")
        print("    launch_velocity - the rock's initial velocity in meters per second")
        print("    starting_height - The rock's initial height in meters")
        return
    
    rock_mass = float(sys.argv[1])
    if rock_mass <= 0:
        print("Rock mass must be positive")
        return
    launch_angle = float(sys.argv[2])
    launch_velocity = float(sys.argv[3])
    starting_height = float(sys.argv[4])
    if starting_height <= 0:
        print("Starting_height must be above ground")
        return

    print("Rock mass: " + str(rock_mass) + " kg.")
    print("Launch angle: " + str(launch_angle) + " degrees.")
    print("Launch velocity: " + str(launch_velocity) + " m/s.")
    print("Starting height: " + str(starting_height) + " meters.")

    rock = PhysicsObject("rock", xpos = starting_pos, ypos = starting_height, mass=rock_mass)
    manager.add_object(rock)


    # Draw everything to the screen (We dont want to do that while waiting because that is a waste of power)

    window.fill([255,255,255])

    draw_rock(rock)

    window.blit(trebuchet_image, (10, height-10))

    start_message = font.render("Press Space to start", False, (0, 0, 0))
    window.blit(start_message, (10, 10))

    pygame.display.update()

    # Waiting to start simulation
    start = False
    while True:
        if start: break
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True #Start the simulation
        clock.tick(fps)
        

    # Apply the grav force
    grav_force = force.calculate_grav_force(g=force.EARTH_G, parent_mass=rock.mass)
    rock.apply_force(Force("grav force", y=-grav_force))

    # Apply the initial velocity
    rock.yvel = launch_velocity*math.sin(launch_angle)
    rock.xvel = launch_velocity*math.cos(launch_angle)

    # Simulation is running
    rock_landed = False
    while True:
        clock.tick(fps)
        if not rock_landed: manager.tick()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        window.fill([255,255,255])

        window.blit(trebuchet_image, (10, height-10))

        draw_rock(rock)

        distance_message = font.render("Distance: " + str(rock.xpos-starting_pos), False, (0, 0, 0))
        window.blit(distance_message, (10, 10))

        #Determine if it hit the ground
        if rock.ypos - rock_radius <= 0:
            rock_landed = True

        pygame.display.update()

if __name__ == "__main__":
    main()
