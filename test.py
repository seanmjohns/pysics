from pysics.manager import PhysicsManager
from pysics.force import Force
from pysics.physics_obj import PhysicsObject
from pysics import pysics

tick_length = 1 #1 tick = 1 second
pysics.game_mode = True #Do less precise calculations

def main(): #Testing time
    
    #Setup
    manager = PhysicsManager(tick_length=1)

    #Create the object for the test
    test_object = PhysicsObject("test object", mass=1.3) #Initial velocity is 0 m/s
    print(test_object.xpos)
    manager.add_object(test_object)

    #Create a force
    force = Force("test force", x=1) #Force of 1 newton in the x direction (will be net force)
    manager.objects[0].apply_force(force) #It will accelerate when a tick passes
    
    #See the results 
    print(test_object.xpos) #Nothing has happened yet because no time has passed
    manager.tick() #Time passes (1 second)
    print(test_object.xpos) #It has moved to 0.5 meters over the 1 second

if __name__ == "__main__":
    main()
