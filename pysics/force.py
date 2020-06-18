
class Force():
    #If you wish to only to 2 dimentional motion, ignore oneof the dimensions
    
    # In newtons
    x = 0.0 #The portion of the force on the x axis in Newtons
    y = 0.0 #The portion of the force on the y axis in Newtons
    z = 0.0 #The portion of the force on the z axis in Newtons

    coefficient_of_friction = 0.0 # Does not matter if the force is not friction
    static_friction = False # Whether or not the object the force is applied on is static (not moving) or not (only applies to frictional forces)

    #Types:
    #   0: Applied
    #   1: Gravitational Force (Implement much later)
    #   2: Frictional (Changes based on speed unless its kinetic) ( Implement later)
    #   3: Tension (Implement much later)
    #   4: Air resistance (Implement much later)
    force_type = 0

    g = 9.80665 #Gravitational acceleration. Only applies if this is a gravitational force

    name = "force"

    def __init__(self, name, x=0, y=0, z=0, force_type=0, g=0.80665):
        """Create a force with the given name and horizontal and vertical forces in newtons. 
        Each dimension defaults to 0 so you only have to deal with what you want. force_type defaults to 0 to simply add an applied force.
        The gravitational constant is different for every force and defaults to the configured value."""
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.force_type = force_type
        self.g = g
