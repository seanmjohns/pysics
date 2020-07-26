import sys, os

sys.path.insert(0, os.path.abspath('..'))

from pysics.manager import PhysicsManager
from pysics.obj import PhysicsObject
from pysics.force import Force

# The tick_length for this universe should be 1/10 of a second
# For games, it is recommended to have a small tick_length, because this will improve collisions (such as 0.1 or 0.01 seconds per tick). We are using a larger tick length to illustrate how it works.
tick_length = 1 #second
manager = PhysicsManager(tick_length)

# Add an object to the universe to be acted upon

# The ball will have an initial position of (10, 10) (To have physics work on the 3rd dimension, simply utilize it)
# The ball will also have an initial velocity of 10 meters per second to the right. Position and velocity values on each axis will default to 0 if not supplied.
ball = PhysicsObject("ball", xpos=10, ypos=10, xvel=10)
manager.add_object(ball)

print("Initial position: " + str(ball.get_pos()))

# Add an applied force that acts *against* the ball's initial velocity at 5 Newtons
force = Force("my force", x=-5)
ball.apply_force(force)

print(ball.get_pos()) #The ball has not moved! No time has passed.

#Now for the next 5 seconds, lets pass some time.

print("Ball position: (x, y, z)")

for second in range(1,6):
    # Make a second (length of tick_length) pass
    manager.tick()
    print(str(second) + " second(s): " + str(ball.get_pos()))
