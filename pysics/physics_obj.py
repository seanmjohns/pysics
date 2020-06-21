from .force import Force
import pysics

from .errors import MassOfZeroError
from .errors import NameUsedError

class PhysicsObject():
    """Represents an object in space that will react as forces are applied on it over ticks.
    Acceleration is only calculated when the object moves (at the beginning of each tick).
    Acceleration can be manually calculated with PhysicsObject.calculate_accel().
    Objects have a mass of 1 kilogram by default.

    Parameters
    ----------
    name: :class:`str`
        The name of this object.

    xpos: :class:`float`
        The object's initial position on the x axis. Defaults to 0.0 if not provided.
        East is positive, West is negative.

    ypos: :class:`float`
        The object's initial position on the y axis. Defaults to 0.0 if not provided.
        Up is positive, Down is negative.

    zpos: :class:`float`
        The object's initial position on the z axis. Defaults to 0.0 if not provided.
        North is positive, South is negative.

    xvel: :class:`float`
        The object's velocity on the x axis. Defaults to 0.0 if not provided.
        East is positive, West is negative.

    yvel: :class:`float`
        The object's velocity on the y axis. Defaults to 0.0 if not provided.
        Up is positive, Down is negative.

    zvel: :class:`float`
        The object's velocity on the z axis. Defaults to 0.0 if not provided.
        North is positive, South is negative.

    forces: list[:class:`pysics.force.Force`]
        The forces that will act on this object. Defaults to no forces.
        Useful for creating many PhysicsObjects.

    mass: :class:`float`
        The mass of this object.


    Attributes
    ----------
    name: :class:`str`
        The name of this physics object. It cannot be the same as another object's name in the same universe.

    forces: list[:class:`pysics.force.Force`]
        All the forces that act on this object each tick.

    mass: :class:`float`
        This object's mass.

    xpos: :class:`float`
        This object's position on the x axis in meters.
        East is positive, West is negative.

    ypos: :class:`float`
        This object's position on the y axis in meters.
        Up is positive, Down is negative.

    zpos: :class:`float`
        This object's position on the z axis in meters.
        North is positive, South is negative.

    xvel: :class:`float`
        This object's velocity on the x axis in meters per second.
        East is positive, West is negative.

    yvel: :class:`float`
        This object's velocity on the y xis in meters per second.
        Up is positive, Down is negatives.

    zvel: :class:`float`
        This object's velocity on the z axis in meters per second.
        North is positive, South is negative.

    xaccel: :class:`float`
        This object's acceleration on the x axis in meters per second^2.
        East is positive, West is negaitve.

    yaccel: :class:`float`
        This object's acceleration on the y axis in meters per second^2.
        Up is positive, Down is negaitve.

    zaccel: :class:`float`
        This object's acceleration on the z axis in meters per second^2.
        North is positive, South is negaitve.

    """

    def __init__(self, name, xpos=0.0, ypos=0.0, zpos=0.0, fxvel=0.0, yvel=0.0, zvel=0.0, forces=[], mass=1.0):
        if mass == 0:
            raise MassOfZeroError("PhysicsObjects cannot have a mass of 0.")
        self.name = name

        self.xvel = xvel #Initial velocity in meters per second
        self.yvel = yvel #Initial velocity in meters per second
        self.zvel = zvel #Initial velocity in meters per second

        self.xpos = xpos #in meters
        self.ypos = ypos #in meters
        self.zpos = zpos #in meters

        self.xaccel = 0.0 #In m/s^2
        self.yaccel = 0.0 #In m/s^2
        self.zaccel = 0.0 #In m/s^2

        self.forces = forces
        self.mass = mass #Having altered mass may not be desired in some games, so mass is defaulted to 1 kilogram

        self.calculate_accel()

    def tick(self, tick_length:float):
        """One tick has passed for this object. If tick_length is 0, then nothing happens because no time passes."""
        if tick_length == 0: return #Literally no time passes.
        self.move(tick_length)
        # Update forces

    def move(self, tick_length:float):
        """Move the object on the 3d (or 2D) plane over the time period given.
        If instantaneous, then do not affect the position, just the velocity."""
        self.calculate_accel() #Includes instantaneous forces
        #x = x(initial) + v(initial)(t) + 1/2(a)(t) - on a single axis
        self.xpos += self.xvel*tick_length + (1/2)*(self.xaccel)*(pow(tick_length,2))
        self.ypos += self.yvel*tick_length + (1/2)*(self.yaccel)*(pow(tick_length,2))
        self.zpos += self.zvel*tick_length + (1/2)*(self.zaccel)*(pow(tick_length,2))


        #v = v(initial) + (a)(t) - on a single axis
        self.xvel += (self.xaccel)*(tick_length)
        self.yvel += (self.yaccel)*(tick_length)
        self.zvel += (self.zaccel)*(tick_length)

        #acceleration does not change until the net force changes

    def get_pos(self) -> tuple:
        """
            :return: Returns the 3 dimensional position as (x, y, z).
            :rtype: tuple
            """
        return(self.xpos, self.ypos, self.zpos)

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
        """
        Applies another force on this object. 
            
            .. note:: 
                Currently unused and not changed (will always stay 0)
        """
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

