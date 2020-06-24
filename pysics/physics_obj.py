from .force import Force
import pysics

from .errors import MassOfZeroError
from .errors import NameUsedError
from .errors import MomentOfInertiaZeroError

import math

class PhysicsObject():
    """Represents an object in space that will react as forces are applied on it over ticks (time).
    Acceleration is only calculated when the object moves (at the beginning of each tick).
    Acceleration can be manually calculated with :meth:`PhysicsObject.calculate_accel()`.
    Objects have a mass of 1 kilogram by default.

    Parameters
    ----------
    name: :class:`str`
        The name of this object.

    xpos: :class:`float`
        The object's initial position on the x axis. Defaults to ``0.0`` if not provided.
        East is positive, West is negative.

    ypos: :class:`float`
        The object's initial position on the y axis. Defaults to ``0.0`` if not provided.
        Up is positive, Down is negative.

    zpos: :class:`float`
        The object's initial position on the z axis. Defaults to ``0.0`` if not provided.
        North is positive, South is negative.

    xvel: :class:`float`
        The object's velocity on the x axis. Defaults to ``0.0`` if not provided.
        East is positive, West is negative.

    yvel: :class:`float`
        The object's velocity on the y axis. Defaults to ``0.0`` if not provided.
        Up is positive, Down is negative.

    zvel: :class:`float`
        The object's velocity on the z axis. Defaults to ``0.0`` if not provided.
        North is positive, South is negative.

    forces: list[:class:`pysics.force.Force`]
        The forces that will act on this object. Defaults to no forces.
        Useful for creating many PhysicsObjects.

    mass: :class:`float`
        The mass of this object. Defaults to 1 kilogram (in case you don't want to deal with mass)


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

    Raises
    ------
    :exc:`MassOfZeroError` 
        Raised if an object is given a mass of ``0`` on initialization.

    """

    def __init__(self, name, xpos=0.0, ypos=0.0, zpos=0.0, xvel=0.0, yvel=0.0, zvel=0.0, x_orientation=0.0, y_orientation=0.0, z_orientation=0.0, x_angular_vel=0.0, y_angular_vel=0.0, z_angular_vel=0.0, forces=[], mass=1.0, moment_of_inertia=1.0):
        if mass == 0:
            raise MassOfZeroError("PhysicsObjects cannot have a mass of 0.")
        if moment_of_inertia == 0:
            raise MomentOfInertiaZeroError("Physics Objects cannot have a moment of inertia of 0.")
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

        #Rotational
        self.x_orientation = x_orientation #In radians
        self.y_orientation = y_orientation #In radians
        self.z_orientation = z_orientation #In radians

        self.x_angular_vel = x_angular_vel #In m/s
        self.y_angular_vel = y_angular_vel #In m/s
        self.z_angular_vel = z_angular_vel #In m/s

        self.x_angular_accel = 0.0 #In m/s^2
        self.y_angular_accel = 0.0 #In m/s^2
        self.z_angular_accel = 0.0 #In m/s^2


        self.forces = forces
        self.mass = mass #Having altered mass may not be desired in some games, so mass is defaulted to 1 kilogram
        self.moment_of_inertia = moment_of_inertia #In kg*m^2

        self.calculate_accel()
        self.calculate_angular_accel()

    def tick(self, tick_length:float):
        """

        Time passes for this object. 
        
        Forces will be applied and the object will move based on velocity and acceleration.

        Acceleration is recalculated just before the position and velocity are updated.

        Translational position/velocity is calculated first.

        Parameters
        ----------
        tick_length: :class:`float`
            The amount of time that passes this tick.

        """

        if tick_length == 0: return #Literally no time passes.
        self.calculate_accel()
        #x = x(initial) + v(initial)(t) + 1/2(a)(t) - on a single axis
        self.xpos += self.xvel*tick_length + (1/2)*(self.xaccel)*(pow(tick_length,2))
        self.ypos += self.yvel*tick_length + (1/2)*(self.yaccel)*(pow(tick_length,2))
        self.zpos += self.zvel*tick_length + (1/2)*(self.zaccel)*(pow(tick_length,2))


        #v = v(initial) + (a)(t) - on a single axis
        self.xvel += (self.xaccel)*(tick_length)
        self.yvel += (self.yaccel)*(tick_length)
        self.zvel += (self.zaccel)*(tick_length)

        self.calculate_angular_accel()
        #Now for angular stuff (Uses same equations as translational, except uses angular versions of variables)
        self.x_orientation += self.x_angular_vel*tick_length + (1/2)*(self.x_angular_accel)*(pow(tick_length,2))
        self.y_orientation += self.y_angular_vel*tick_length + (1/2)*(self.y_angular_accel)*(pow(tick_length,2))
        self.z_orientation += self.z_angular_vel*tick_length + (1/2)*(self.z_angular_accel)*(pow(tick_length,2))

        print(self.x_orientation)
        

        self.x_angular_vel += (self.x_angular_accel)*(tick_length)
        self.y_angular_vel += (self.y_angular_accel)*(tick_length)
        self.z_angular_vel += (self.z_angular_accel)*(tick_length)

        #acceleration does not change until the net force (or net torque for angular acceleration) changes

    def get_pos(self) -> tuple:
        """
        Returns the object's current position on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's position on the 3 dimensions (x, y, z)
        """
        return(self.xpos, self.ypos, self.zpos)

    def get_orientation(self) -> tuple:
        """
        Returns the object's current orientation on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's position on the 3 dimensions (x, y, z)
        """
        return(self.x_orientation, self.y_orientation, self.z_orientation)

    def get_vel(self) -> tuple:
        """
        Returns the object's current velocity on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's velocity on the 3 dimensions (x, y, z)
        """
        return(self.xvel, self.yvel, self.zvel)

    def get_angular_vel(self) -> tuple:
        """
        Returns the object's current angular velocity on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's velocity on the 3 dimensions (x, y, z)
        """
        return(self.x_angular_vel, self.y_angular_vel, self.z_angular_vel)

    def get_accel(self) -> tuple:
        """
        Returns the object's current translational acceleration on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's translational acceleration on the 3 dimensions (x, y, z)
        """
        return(self.xaccel, self.yaccel, self.zaccel)

    def get_angular_accel(self) -> tuple:
        """
        Returns the object's current angular acceleration on each axis in the form (x, y, z)

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's acceleration on the 3 dimensions (x, y, z)
        """
        return(self.x_angular_accel, self.y_angular_accel, self.z_angular_accel)

    def calculate_accel(self) -> tuple:
        """
        Calculates and sets the object's translational (linear) acceleration for each dimension.

        Adds all the newtons of force for each dimension from :attr:`forces`, then divides each result by the :attr:`mass`.

        This is called when a :meth:`tick` is called. Translational acceleration can be updated manually by calling this function.

        Returns
        -------
        tuple(:class:`float`, :class:`float`, :class:`float`, :class:`float`, :class:`float`)
            Returns a tuple of the object's acceleration on the 3 dimensions (x, y, z)

        Raises
        ------
        :exc:`MassOfZeroError`
            PhysicsObjects cannot have a mass of ``0``. Prevents from dividing by ``0``.
        """

        if self.mass == 0:
            raise MassOfZeroError("PhysicsObjects cannot have a mass of 0.")

        self.xaccel = 0
        self.yaccel = 0
        self.zaccel = 0
        for force in self.forces:
            self.xaccel += force.x*math.cos(force.x_rot_angle)
            self.yaccel += force.y*math.cos(force.y_rot_angle)
            self.zaccel += force.z*math.cos(force.z_rot_angle)
        self.xaccel /= self.mass
        self.yaccel /= self.mass
        self.zaccel /= self.mass
        return (self.xaccel, self.yaccel, self.zaccel)

    def calculate_angular_accel(self) -> tuple:
        """
        Calculates and sets the object's angular acceleration for each dimension.

        Adds all the newtons of force for each dimension from :attr:`forces`, then divides each result by the :attr:`moment_of_inertia`.

        This is called when a :meth:`tick` is called. Angular acceleration can be updated manually by calling this function.

        Returns
        -------
        tuple( :class:`float`, :class:`float`, :class:`float`)
            The angular acceleration of the 3 dimensions in the form: (x, y, z)

        Raises
        ------
        :exc:`MomentOfInertiaZeroError`
            PhysicsObjects cannot have a moment of inertia of ``0``. Prevents from dividing by ``0``.
        """

        if self.moment_of_inertia == 0:
            raise MomentOfInertiaZeroError("PhysicsObjects cannot have a moment of inertia of 0.")

        self.x_angular_accel = 0
        self.y_angular_accel = 0
        self.z_angular_accel = 0
        for force in self.forces:
            force.calculate_torque()
            self.x_angular_accel =+ force.x_torque
            self.y_angular_accel =+ force.y_torque
            self.z_angular_accel =+ force.z_torque

        self.x_angular_accel /= self.moment_of_inertia
        self.y_angular_accel /= self.moment_of_inertia
        self.z_angular_accel /= self.moment_of_inertia

        return (self.x_angular_accel, self.y_angular_accel, self.z_angular_accel)

    def apply_force(self, new_force):
        """
        Applies another force on this object. 

        Parameters
        ----------
        new_force: :class:`new_force`
            The force instance that will be applied to this object.

        Raises
        ------
        :exc:`pysics.errors.NameUsedError`
            You cannot use the same name twice for a force on the same object.
        """
        for force in self.forces: #Make sure its name is not already used
            if force.name == new_force.name:
                raise NameUsedError("You cannot use the same name twice for a force on the same object.")

        self.forces.append(new_force)

    def remove_force(self, force):
        """
        Remove a force from this object so that it is no longer applied (removes from :attr:`forces`).
        Fails silently if there is no force with the given name.

        Parameters
        ----------
        force: :class:`pysics.force.Force`
            The instance of the force to remove.
        """

        if force not in self.forces: return
        self.forces.remove(force)

    def remove_force_by_name(self, name:str):
        """
        Remove a force based on its name so that it is no longer applied to this object (removes from :attr:`forces`). 
        Fails silently if there is no force with the given name.

        Parameters
        ----------
        name: :class:`str`
            The name of the force to be removed.

        """

        for force in forces:
            if force.name == name:
                forces.remove(force)

    def clear_forces(self) -> list:
        """
        Remove all the forces acting on this object (Empties :attr:`forces`).

        Returns
        -------
        list[:class:`pysics.force.Force`]:
            All the forces cleared. Useful for transferring forces to another object.

        """
        forces_copy = self.forces
        self.forces.clear()
        return forces_copy
