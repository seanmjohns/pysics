#pygame
import pygame
from pygame.locals import *
from pygame import Color

#pysics
from pysics.manager import PhysicsManager
from pysics.physics_obj import PhysicsObject
from pysics.force import Force
from pysics import pysics

# python util libraries
import sys
import math

pygame.init()

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
print(y)
#Note that for pygame, the top of the screen is y=0

#Setup pysics
tick_length = 0.1 # Recommended to be low for games so collision works properly
pysics.game_mode = True
manager = PhysicsManager(tick_length=tick_length)

earth_g = 9.80665

wall_bump_tick_length = 0.0001

def main():

    #Create the ball
    ball = PhysicsObject("ball", xpos=x, ypos=y, xvel=10, mass=1) #Initial velocity is 0.5 to the right
    ball_color = Color(0, 0, 0)
    ball_radius = 5

    #Apply the gravitational force
    grav_force = Force("gravitational force", g=earth_g, parent_mass=ball.mass)
    ball.apply_force(grav_force)

    #The object must be added to the universe first
    manager.add_object(ball)

    while True:
        #print("\n")
        manager.tick()
        #This should be done after the tick to make sure we are getting the CURRENT position
        ball_screen_y = height - ball.ypos #x pos in pysics is equivalent to the xpos in pygame

        clock.tick(desired_fps)
        #Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        #Determine if the ball has hit a boundary (account for ball radius) - Apply an instantaneous (really its one tick) normal force against it if so (removed next frame)
        if ball.xpos - ball_radius <= 0:
            #Impulse = change in momentum
            #Impulse = force*change in time
            #Change in momentum = change in velocity * mass (mass is constant)
            #Since momentum will not be lost (Law of conservation of momentum), and the boundary does not gain momentum, change in velocity will be 2*velocity. 
            #so, by rearranging the variables and substituting:
            #Force = (2v*m)/t, so
            #Force = (2*xvel*mass)/tick_length : The 2 is factored in with  the ball.xvel*elasticity
            #This force is the one we need to apply
            left = Force("left side normal force", x=(abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length, instantaneous=True)
            ball.apply_force(left)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(left)

        if ball.xpos + ball_radius >= width:
            right = Force("right side normal force", x=(-abs(2*ball.xvel)*ball.mass)/wall_bump_tick_length, instantaneous=True) #Going to the negative direction, so xvel needs to be negative
            ball.apply_force(right)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(right)

        #For this example, we don't want the ball to hit the top of the screen
        #if ball_screen_y - ball_raidus <= 0:
        #    ball.apply_force("top side normal force", y=(abs(ball.yvel)*ball.mass/tick_length))

        #print(ball_screen_y + ball_radius)
        if ball_screen_y + ball_radius >= height:
            bottom = Force("bottom side normal force", y=(abs(2*ball.yvel)*ball.mass)/wall_bump_tick_length, instantaneous=True)
            ball.apply_force(bottom)
            ball.tick(wall_bump_tick_length)
            ball.remove_force(bottom)

        #Draw the background (white)
        window.fill((255, 255, 255))

        #Draw the ball
        pygame.draw.circle(window, ball_color, (int(ball.xpos), height-int(ball.ypos)), 5) #y=0 is at the top of the screen

        pygame.display.update()


if __name__ == "__main__":
    main()
