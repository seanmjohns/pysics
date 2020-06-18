from pysics.manager import PhysicsManager
from pysics.force import Force
from pysics.physics_obj import PhysicsObject
from pysics import pysics

tick_length = 1 #1 tick = 1 second
pysics.game_mode = True #Do less precise calculations

def main(): #Testing time
    
    #Setup
    manager = PhysicsManager(tick_length=1) #tick_length is 1 by default


    print("Force of 1 Newton on the x-axis on an object with a mass of 1.3 kilograms. 1 second passes.")

    #Create the object for the test
    test_object = PhysicsObject("test object", mass=1.3) #Initial velocity is 0 m/s
    manager.add_object(test_object)

    #Create a force
    force = Force("test force", x=1) #Force of 1 newton in the x direction (will be net force)
    test_object.apply_force(force) #It will accelerate when a tick passes
    
    #See the results 
    manager.tick() #Time passes (1 second)
    print((test_object.xpos, test_object.ypos, test_object.zpos)) #It has moved




    print("\n\n")

    #Now lets test out different gravitational forces with different gravitational accelerations

    manager.clear()
    test_object.clear_forces()

    mars_g = 3.72076
    print("Gravitational force with g=" + str(mars_g) + " (Moon) on an object with a mass of 2 kg. Initial velocity of 1 m/s upwards, 100 meters high.")

    test_object = PhysicsObject("test object", ypos=100, yvel=1, mass=2) #The object is moving upwards at 1 m/s initially
    manager.add_object(test_object)

    force = Force("gravity", g=mars_g, parent_mass=test_object.mass)
    test_object.apply_force(force)

    print("Initial (Pos, Vel):")
    print((test_object.xpos, test_object.ypos, test_object.zpos))
    print((test_object.xvel, test_object.yvel, test_object.zvel))

    for i in range(4):
        manager.tick() #We could change the tick length here (This could allow for slow motion in games)
        print(str(i) + " seconds (Pos, Vel):")
        print((test_object.xpos, test_object.ypos, test_object.zpos))
        print((test_object.xvel, test_object.yvel, test_object.zvel))


    print("\nWhy not apply a negative gravitational acceleration? g=-9.80665 (Earth). Other gravitational force still applied.")

    earth_g = 9.80665
    negative_g_force = Force("negative gravity", g=-earth_g, parent_mass=test_object.mass)
    test_object.apply_force(negative_g_force)

    for i in range(4):
        manager.tick() #We could change the tick length here (This could allow for slow motion in games)
        print(str(i) + " seconds (Pos, Vel):")
        print((test_object.xpos, test_object.ypos, test_object.zpos))
        print((test_object.xvel, test_object.yvel, test_object.zvel))

if __name__ == "__main__":
    main()
