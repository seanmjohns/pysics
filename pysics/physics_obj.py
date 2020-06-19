from pysics.force import Force
from pysics import pysics

from pysics.errors import MassOfZeroError
from pysics.errors import NameUsedError

class PhysicsObject():
    """Represents an object in space that will react as forces are applied on it over ticks.
    Acceleration is only calculated when the object moves (at the beginning of each tick).
    Acceleration can be manually calculated with PhysicsObject.calculate_accel().
    Objects have a mass of 1 kilogram by default."""

    forces = []

    xvel = 0.0 #In meters per second
    yvel = 0.0 #In meters per second
    zvel = 0.0 #In meters per seconds

    xpos = 0.0 #In meters
    ypos = 0.0 #In meters
    zpos = 0.0 #In meters

    xaccel = 0.0 #In m/s^2
    yaccel = 0.0 #In m/s^2
    zaccel = 0.0 #In m/s^2

    mass = 1.0 #kilograms

    name = "obj"

    def __init__(self, name, xvel=0.0, yvel=0.0, zvel=0.0, xpos=0.0, ypos=0.0, zpos=0.0, forces=[], mass=1.0):
        if mass == 0:
            raise MassOfZeroError("PhysicsObjects cannot have a mass of 0.")
        self.name = name
        self.xvel = xvel #Initial velocity 
        self.yvel = yvel #Initial velocity
        self.zvel = zvel #Initial velocity
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self.forces = forces
        self.mass = mass #Having altered mass may not be desired in some games, so mass is defaulted to 1 kilogram
        self.calculate_accel()

    def tick(self, tick_length:float):
        """One tick has passed for this object."""
        self.move(tick_length)
        # Update forces

    def move(self, tick_length:float):
        """Move the object on the 3d (or 2D) plane over the time period given.
        If instantaneous, then do not affect the position, just the velocity."""
        self.calculate_accel() #Includes instantaneous forces
        if pysics.game_mode: #Gamer mode (not scientific)

            #x = x(initial) + v(initial)(t) + 1/2(a)(t) - on a single axis
            #print("yaccel: " + str(self.yaccel))
            self.xpos += self.xvel*tick_length + (1/2)*(self.xaccel)*(pow(tick_length,2))
            #print("Before: " + str(self.ypos))
            #print("change in y pos: " + str(self.yvel*tick_length + (1/2)*(self.yaccel)*(tick_length)))
            self.ypos += self.yvel*tick_length + (1/2)*(self.yaccel)*(pow(tick_length,2))
            #print("After: " + str(self.ypos))
            self.zpos += self.zvel*tick_length + (1/2)*(self.zaccel)*(pow(tick_length,2))


            #v = v(initial) + (a)(t) - on a single axis
            self.xvel += (self.xaccel)*(tick_length)
            self.yvel += (self.yaccel)*(tick_length)
            #print("change: " + str((self.yaccel)*(tick_length)))
            #print("yvel: " + str(self.yvel))
            self.zvel += (self.zaccel)*(tick_length)

            if abs(self.yvel) < 0.5:
                print("ypos: " + str(self.ypos))
                print("yaccel: " + str(self.yaccel))

            #acceleration does not change until the net force changes

    def calculate_accel(self) -> tuple:
        """Calculates the the object's acceleration for each dimension.
        Returns a tuple of the dimensions. This assumes mass is negligible."""
        if self.mass == 0:
            raise MassOfZeroError("PhysicsObjects cannot have a mass of 0.")
        self.xaccel = 0
        self.yaccel = 0
        self.zaccel = 0
        for force in self.forces:
            self.xaccel =+ force.x
            self.yaccel =+ force.y
            self.zaccel =+ force.z
        self.xaccel /= self.mass
        self.yaccel /= self.mass
        self.zaccel /= self.mass
        return (self.xaccel, self.yaccel, self.zaccel)

    def apply_force(self, new_force):
        """Applies another force on this object. Acceleration is NOT recalculated here."""
        for force in self.forces: #Make sure its name is not already used
            if force.name == new_force.name:
                raise NameUsedError("You cannot use the same name twice for a force on the same object.")

        self.forces.append(new_force)

    def remove_force(self, force):
        if force not in self.forces: return
        self.forces.remove(force)

    def remove_force_by_name(self, name:str):
        """Remove a force based on its name. If the force is not applied to this object, fails silently."""
        for force in forces:
            if force.name == name:
                forces.remove(force)

    def clear_forces(self) -> list:
        """Remove all the forces acting on this object. Returns all the forces that were applied."""
        forces_copy = self.forces
        self.forces.clear()
        return self.forces_copy

