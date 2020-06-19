from pysics.errors import MassOfZeroError

class Force():
    """A force"""
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

    instantaneous=False

    def __init__(self, name, x=0, y=0, z=0, force_type=0, g=0, parent_mass=0, instantaneous=False):
        """Create a force with the given name and horizontal and vertical forces in newtons. 
        Each dimension defaults to 0 so you only have to deal with what you want. force_type defaults to 0 to simply add an applied force.
        The gravitational constant is different for every force and defaults to 0.
        If you wish to have a specific gravitational acceleration for a gravitational force, supply g instead of vertical force and the
        object's mass (parent_mass). The vertical force will be calculated from them. Forces created this way cannot be used by two different objects.
        Instantaneous forces are accounted for when calculating the new velocity over the tick, but not the position. All instantaneous forces are removed each tick (because they are instantaneous)."""
        self.name = name
        self.g = g
        self.x = x
        if g != 0: #Gravitational acceleration supplied
            if parent_mass == 0:
                raise MassOfZeroError("Parent mass cannot be 0")
            self.y += -g*parent_mass #g needs to be negative in this calculation because it goes down
        else: #Gravitational acceleration not supplied
            self.y = y
        self.z = z
        self.force_type = force_type
        self.instantaneous = instantaneous
