# python util libraries
import sys, os
import math

sys.path.insert(0, os.path.abspath('..')) #You wont need this

#pygame
import pygame
from pygame.locals import *
from pygame import Color

#pysics
from pysics.manager import PhysicsManager
from pysics.obj import PhysicsObject
from pysics.force import Force
from pysics import force
from pysics import pysics

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Sans Serif", 20)

# display
width = 400
height = 400
window = pygame.display.set_mode([400, 400])
pygame.display.set_caption("pysics example")

#FPS
clock = pygame.time.Clock()
desired_fps = 60

x = width/4
y = height*(3/4)
#Note that for pygame, the top of the screen is y=0

#Setup pysics
tick_length_max = 1 #Used for mouse position
tick_length = 0 # Recommended to be low for games so collision works properly (This example, the default is 0, because that is the middle)
tick_length_min = -1
pysics.game_mode = True
manager = PhysicsManager(tick_length=tick_length)

wall_bump_tick_length = 0.0001

boundary_coef_of_friction = 0.5

def main():

    #Create the ball
    ball = PhysicsObject("ball", xpos=x, ypos=y, xvel=10, mass=1, moment_of_inertia=1) #Initial velocity is 0.5 to the right
    ball_color = Color(0, 0, 0)
    ball_radius = 7.5

    ball_image = pygame.image.load("images/ball.png")

    #Apply the gravitational force
    g = force.calculate_grav_force(force.EARTH_G, ball.mass)
    grav_force = Force("gravitational force", y=-g) #Note that you need to make it go downwards, because thats what gravitational forces do.
    ball.apply_force(grav_force)

    #The object must be added to the universe first
    manager.add_object(ball)

    #Create the instructions
    instruction_surface = font.render("Move the cursor up and down", False, (100,100,100))

    while True:
        #To demonstrate how tick_rate can be used for slow-mo (and even backwards-moving time), move mouse up and down
        mouse_pos_y = pygame.mouse.get_pos()[1]
        tick_length = (mouse_pos_y-height/2)/(height/2)*tick_length_max
        if (tick_length < tick_length_min): tick_length = tick_length_min
        if (tick_length > tick_length_max): tick_length = tick_length_max
        manager.tick(tick_length)

        #This should be done after the tick to make sure we are getting the CURRENT position
        ball_screen_y = height - ball.ypos #x pos in pysics is equivalent to the xpos in pygame

        clock.tick(desired_fps)
        #Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        #Determine if the ball has hit a boundary (account for ball radius) - Apply an instantaneous (really its one tiny tick) normal force against it if so
        if ball.xpos <= 0:
            #Impulse = change in momentum
            #Impulse = force*change in time
            #Change in momentum = change in velocity * mass (mass is constant)
            #Since momentum will not be lost (Law of conservation of momentum), and the boundary does not gain momentum, change in velocity will be 2*velocity. 
            #so, by rearranging the variables and substituting:
            #Force = (2v*m)/t, so
            #Force = (2*xvel*mass)/tick_length : The 2 is factored in with  the ball.xvel*elasticity
            #This force is the one we need to apply
            left = None
            if tick_length < 0:
                left = Force("left side normal force", x=(-abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length)
            else:
                left = Force("left side normal force", x=(abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length)
            ball.apply_force(left)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(left)

        if ball.xpos + ball_radius*2 >= width:
            right = None
            if tick_length < 0:
                right = Force("right side normal force", x=(abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length)
            else:
                right = Force("right side normal force", x=(-abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length)
            ball.apply_force(right)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(right)

        #For this example, we don't want the ball to hit the top of the screen
        #if ball_screen_y - ball_raidus <= 0:
        #    ball.apply_force("top side normal force", y=(abs(ball.yvel)*ball.mass/tick_length))

        if ball_screen_y + ball_radius*2 >= height:
            bottom = None
            friction = None
            if tick_length < 0:
                bottom = Force("bottom side normal force", y=(-abs(2*ball.yvel)*ball.mass)/wall_bump_tick_length)
            else:
                bottom = Force("bottom side normal force", y=(abs(2*ball.yvel)*ball.mass)/wall_bump_tick_length)

            if ball.xvel < 0:
                friction = Force("bottom friction force", x=(abs(boundary_coef_of_friction*bottom.y*wall_bump_tick_length)), x_rotation_axis_distance=ball_radius, x_rot_angle=math.pi/2) #Friction = (coefficient of friction)*(normal force)
            else:
                friction = Force("bottom friction force", x=(-abs(boundary_coef_of_friction*bottom.y*wall_bump_tick_length)), x_rotation_axis_distance=ball_radius, x_rot_angle=math.pi/2) #Friction = (coefficient of friction)*(normal force)

            ball.apply_force(bottom)
            ball.apply_force(friction)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(bottom)
            ball.remove_force(friction)

        #Draw the background (white)
        window.fill((255, 255, 255))

        #Draw the instructions
        window.blit(instruction_surface, (10,10))
        tick_length_text = font.render("Tick Length: " + str(tick_length), False, (100,100,100))
        window.blit(tick_length_text, (10, 40))

        #Draw the ball
        window.blit(pygame.transform.rotate(ball_image, math.degrees(ball.x_orientation)), (int(ball.xpos), height-int(ball.ypos))) #y=0 is at the top of the screen

        pygame.display.update()


if __name__ == "__main__":
    main()
