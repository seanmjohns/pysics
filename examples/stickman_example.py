# Inspired by the stickmen from the Stick Ranger series of games on danball.com

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
floor = 20 #The distance from the bottom of the screen that the bottom boundary is
window = pygame.display.set_mode([400, 400])
pygame.display.set_caption("stickman example")

#FPS
clock = pygame.time.Clock()
desired_fps = 120

x = width/4
y = height*(3/4)
#Note that for pygame, the top of the screen is y=0

#Setup pysics
tick_length = 0.05
wall_bump_tick_length = 0.001
pysics.game_mode = True
manager = PhysicsManager(tick_length=tick_length)
manager2 = PhysicsManager(tick_length=tick_length)

boundary_coef_of_friction = 0.75
background_coef_of_friction = 0.5
body_part_spring_constant = 0.75

class BodyPart(PhysicsObject):

    def __init__(self, name, color=(0,0,0), bpd=10, xpos=0.0, ypos=0.0, zpos=0.0, xvel=0.0, yvel=0.0, zvel=0.0, x_orientation=0.0, y_orientation=0.0, z_orientation=0.0, x_angular_vel=0.0, y_angular_vel=0.0, z_angular_vel=0.0, forces=[], mass=1.0, moment_of_inertia=1.0, time_passed=0.0):
        self.grabbed = False
        self.connected_parts = []
        self.bpd = bpd
        self.color = color
        super().__init__(name, xpos, ypos, zpos, xvel, yvel, zvel, x_orientation, y_orientation, z_orientation, x_angular_vel, y_angular_vel, z_angular_vel, forces, mass, moment_of_inertia, time_passed)

    def set_connected_parts(self, parts=[]):
        self.connected_parts = parts.copy()

    def apply_body_part_forces(self):
        for part in self.connected_parts:
            x_distance = part.xpos-self.xpos
            y_distance = part.ypos-self.ypos
            total_distance = pow(pow(x_distance,2)+pow(y_distance,2),1/2)
            if total_distance > (self.bpd): #If the part is out of body part range, apply a sprint force to pull it back
                theta = math.acos(x_distance/total_distance)
                multiplier = 10 #needed to adequately offset the gravitational force
                stretch_distance = total_distance*multiplier - self.bpd #Prevent jerky movements
                x_force = math.copysign(math.cos(theta)*stretch_distance, x_distance)
                y_force = math.copysign(math.sin(theta)*stretch_distance, y_distance)

                #Spring force: kx^2

                #We need to keep direction, however
                x_squared = math.copysign(pow(x_force,2), x_force)
                y_squared = math.copysign(pow(y_force,2), y_force)

                #Must divide by two because both parts are applied forces (conservation of momentum)
                x_force = (1/2)*(body_part_spring_constant)*x_squared
                y_force = (1/2)*(body_part_spring_constant)*y_squared

                self.remove_force_by_name(part.name + " pull")
                f = Force(name=(part.name + " pull"), x=x_force, y=y_force)
                self.apply_force(f)
                self.tick(wall_bump_tick_length)
                self.remove_force(f)

class Stickman():

    bpd = 10 #body part distance in pixels
    head_radius = 2
    
    def __init__(self, head_pos:tuple, stickman_id):
        self.part_grabbed = False
        self.body_parts = []
        self.stickman_id = stickman_id
        self.head = BodyPart(name="stickman" + str(self.stickman_id) + " head", xpos=head_pos[0], ypos=head_pos[1], color=(0,0,255))
        self.body_parts.append(self.head)

        self.neck = BodyPart(name="stickman" + str(self.stickman_id) + " neck", xpos=self.head.xpos, ypos=self.head.ypos+self.bpd, color=(0,0,255))
        self.body_parts.append(self.neck)

        self.left_hand = BodyPart(name="stickman" + str(self.stickman_id) + " left_hand", xpos=self.neck.xpos-self.bpd, ypos=self.neck.ypos, color=(0,255,0))
        self.body_parts.append(self.left_hand)
        
        self.right_hand = BodyPart(name="stickman" + str(self.stickman_id) + " right_hand", xpos=self.neck.xpos+self.bpd, ypos=self.neck.ypos, color=(255,0,0))
        self.body_parts.append(self.right_hand)

        self.waist = BodyPart(name="stickman" + str(self.stickman_id) + " waist", xpos=self.neck.xpos, ypos=self.neck.ypos+self.bpd, color=(0,0,255))
        self.body_parts.append(self.waist)

        self.left_foot = BodyPart(name="stickman" + str(self.stickman_id) + " left_foot", xpos=self.waist.xpos-math.pow(math.pow(self.bpd,2)/2,1/2), ypos=self.waist.ypos+math.pow(math.pow(self.bpd,2)/2,1/2), color=(0,255,0))
        self.body_parts.append(self.left_foot)

        self.right_foot = BodyPart(name="stickman" + str(self.stickman_id) + " right_foot", xpos=self.waist.xpos+math.pow(math.pow(self.bpd,2)/2,1/2), ypos=self.waist.ypos+math.pow(math.pow(self.bpd,2)/2,1/2), color=(255,0,0))
        self.body_parts.append(self.right_foot)

        """self.head = BodyPart(name="head", xpos=30, ypos=27)
        self.body_parts.append(self.head)

        self.neck = BodyPart(name="neck", xpos=30, ypos=27)
        self.body_parts.append(self.neck)

        self.left_hand = BodyPart(name="left_hand", xpos=191, ypos=27)
        self.body_parts.append(self.left_hand)
        
        self.right_hand = BodyPart(name="right_hand", xpos=39, ypos=27)
        self.body_parts.append(self.right_hand)

        self.waist = BodyPart(name="waist", xpos=30, ypos=27)
        self.body_parts.append(self.waist)

        self.left_foot = BodyPart(name="left_foot", xpos=37, ypos=27)
        self.body_parts.append(self.left_foot)

        self.right_foot = BodyPart(name="right_foot", xpos=23, ypos=27)
        self.body_parts.append(self.right_foot)"""

        #Set what the connected body parts are to each body part
        self.head.set_connected_parts([self.neck])
        self.neck.set_connected_parts([self.head, self.waist, self.left_hand, self.right_hand])
        self.left_hand.set_connected_parts([self.neck])
        self.right_hand.set_connected_parts([self.neck])
        self.waist.set_connected_parts([self.neck, self.left_foot, self.right_foot])
        self.left_foot.set_connected_parts([self.waist])
        self.right_foot.set_connected_parts([self.waist])

    def draw(self):
        for part in self.body_parts:
            if "head" in part.name: #We want only the head to be a circle, and to not draw lines to other parts
                pygame.draw.circle(window, part.color, (int(part.xpos), int(part.ypos)), self.head_radius) #head
                continue
            for p in part.connected_parts: #Draw a line for all other parts
                if "head" in p.name: continue
                pygame.draw.line(window, (0,0,0), (int(p.xpos), int(p.ypos)), (int(part.xpos), int(part.ypos)))
            #Draw a dot representing the body part
            pygame.draw.circle(window, part.color, (int(part.xpos), int(part.ypos)), 1)

def main():

    cursor_grab_distance = 8; #pixels
    grabbed_stickman = False

    num_stickmen = 2

    stickmen = []
    for i in range(1,num_stickmen+1): #Create as many stickmen as you want
        stickmen.append(Stickman((20*i, 20), i))

    #Apply a gravitational force to all the body parts
    grav_force = force.calculate_grav_force(g=force.EARTH_G, parent_mass=1)

    #All the body parts will have the same mass (1 kg), so this can be applied to all body parts
    for stickman in stickmen:
        for part in stickman.body_parts:
            part.apply_force(Force("grav", y=grav_force)) #apply force
            manager.add_object(part) #Add object to the universe

    while True:
        manager.tick(tick_length)

        clock.tick(desired_fps)
        mouse_y = pygame.mouse.get_pos()[1]
        mouse_x = pygame.mouse.get_pos()[0]
        if pygame.mouse.get_pressed()[0]:
            for stickman in stickmen:
                if not grabbed_stickman:
                    for part in stickman.body_parts:
                        distance = pow(pow(mouse_y-part.ypos,2)+pow(mouse_x-part.xpos,2),1/2)
                        if distance <= cursor_grab_distance:
                            part.grabbed = True
                            stickman.part_grabbed = True
                            grabbed_stickman = True
                            break #only one part can be grabbed at a time
                else: break

        else:
            grabbed_stickman = False
            for stickman in stickmen:
                stickman.part_grabbed = False
                for part in stickman.body_parts:
                    part.grabbed = False

        #Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

    
        for stickman in stickmen:
            for part in stickman.body_parts:
                #Apply grab forces so that the body parts will go towards the mouse
                if part.grabbed:
                    part.remove_force_by_name("grabbed")
                    x_force = 10*(mouse_x-part.xpos)
                    y_force = 10*(mouse_y-part.ypos)
                    part.apply_force(Force("grabbed", x=x_force, y=y_force))
                else:
                    part.remove_force_by_name("grabbed")

            #apply air resistance (proportional to velocity, and thus creates terminal velocity)
            #Air Resistance Force = (-1/2)*(air constant)*(velocity of obj)*(density of air)*(Cross-sectional area of object)
            #Drag coefficient for spheres is about 0.47 (with reynolds number of 10^4)
            #Air density at 15 degrees celcius at sea level is about 1.225 kg/m^3
            #Cross-sectional area is assumed to be 1 square meter
            for part in stickman.body_parts:
                part.remove_force_by_name("air_resistance")
                x_force = (1/2)*(0.47)*(-part.xvel)*(1.225)*(1)
                y_force = (1/2)*(0.47)*(-part.yvel)*(1.225)*(1)
                part.apply_force(Force("air_resistance", x=x_force, y=y_force))

            #Make the body parts go towards each other if they are too far apart
            for part in stickman.body_parts:
                part.apply_body_part_forces()

            #Apply friction when the bodies hit the walls (and stop them on their opposite axes)
            #(2*xvel*mass)/tick_length
            for part in stickman.body_parts:
                part.remove_force_by_name("left wall friction")
                if part.xpos <= 0:
                    part.xpos = 0
                    if part.xvel < 0:
                        part.xvel = 0
                elif part.xpos >= width:
                    part.xpos = width
                    if part.xvel > 0:
                        part.xvel = 0
                if part.ypos <= 0:
                    part.ypos = 0
                    if part.yvel < 0:
                        part.yvel = 0
                elif part.ypos >= height-floor:
                    part.ypos = height-floor
                    if part.yvel > 0: #we should allow it to escape the boundary
                        part.yvel = 0
                    friction = Force("left wall friction", x=(boundary_coef_of_friction)*(2*-part.xvel)*part.mass)
                    part.apply_force(friction)

        #Draw the background (white)
        window.fill((255, 255, 255))

        #Draw the stickmen
        for stickman in stickmen:
            stickman.draw()

        pygame.display.update()

if __name__ == "__main__":
    main()
