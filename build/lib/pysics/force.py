from .errors import MassOfZeroError

import math

#The gravitational acceleration while on the surface of...
EARTH_G = 9.80665 #m/s^2
"""The gravitational acceleration on the surface of the Earth in m/s^2"""

MOON_G = 1.625 #m/s^2
"""The gravitational acceleration on the surface of the Moon in m/s^2"""

MARS_G = 3.72076 #m/2^2
"""The gravitational acceleration on the surface of Mars in m/s^2"""

def calculate_grav_force(g=EARTH_G, parent_mass=1) -> float:
    """Calculate the gravitational force that would be applied to an object
    with the given mass given a gravitational acceleration.

    Calculation: ``gravitational force = mg``\n
        * ``m`` is the mass of the parent object.\n
        * ``g`` is the gravitational acceleration (the gravitational constant).

    Parameters
    ----------
    g: :class:`float`
        The gravitational acceleration (gravitational constant). This is the resulting acceleration from the force.
        Defaults to :attr:`EARTH_G` (9.80665 m/s^2)

    parent_mass: :class:`float`
        The mass of the object the gravitational force will be applied to. Defaults to 1 kilogram.

    Returns
    -------
    :class:`float`
        The newtons of force that would be required to have a mass of ``parent_mass`` accelerate at ``g`` m/s^2.
        The force you will make from this does not necessarily have to be on the y (vertical) axis. Why not have gravity be sideways?
    """

    return g*parent_mass

class Force():
    """A force that acts upon a :class:`PhysicsObject`.

    The x, y, and z attributes can be used freely by developers (meaning you can use any axis as you wish. For example, you could use the universe's y axis as your z axis).
    If you desire to only have 2D motion, then completely ignore an entire dimension. If you wish to only have 1D motion, the ignore 2 dimensions.

    It is not recommended that the variable that stores a :class:`Force` be called ``force``, because that is also the name of the module :mod:`force`, which could cause naming conflicts.

    Parameters
    ----------
    name: :class:`str`
        The force's name. Used to identify this force when applied to an object.

    x: :class:`float`
        The newtons of force in the x direction. Defaults to ``0.0`` if not supplied.
        East is positive, West is negative.

    y: :class:`float`
        The newtons of force in the x direction. Defaults to ``0.0`` if not supplied.
        Up is positive, Down is negative.

    z: :class:`float`
        The newtons of force in the x direction. Defaults to ``0.0`` if not supplied.
        North is positive, South is negative.

    force_type: :class:`int`
        Represents the type of force this is with the following values:
            * ``0``: Applied Force
            * ``1``: Gravitational Force
            * ``2``: Frictional Force (Not yet implemented)
            * ``3``: Tension (Not yet implemented)
            * ``4``: Air Resistance (Not yet implemented)

        .. note:: 
            :attr:`force_type` is currently unused and will not change (will always stay initial value)

    x_rotation_axis_distance: :class:`float`
        The distance from the axis of rotation on the x-axis in meters. Defaults to ``0.0``.

    y_rotation_axis_distance: :class:`float`
        The distance from the axis of roataion on the y-axis in meters. Defaults to ``0.0``.

    z_rotation_axis_distance: :class:`float`
        The distance from the axis of rotation on the z-axis in meters. Defaults to ``0.0``.

    x_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the x-axis. Defaults to ``0.0``.

    y_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the x-axis. Defaults to ``0.0``.

    z_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the z-axis. Defaults to ``0.0``.

    Attributes
    ----------
    name: :class:`str`
        The name of this force. It cannot be the same as any other force on an object.

    x: :class:`float`
        The newtons of force in the x direction (typically east/west).
        Can be positive or negative, with (+) being east and (-) being west.

    y: :class:`float`
        The newtons of force in the y direction (typically vertical).
        Can be positive or negative, with (+) being up and (-) being down.

    z: :class:`float`
        The newtons of force in the z direction (typically north/south).
        Can be positive or negative, with (+) being north and (-) being south.

    force_type: :class:`int`
        Represents the type of force this force is with the following values:
            * ``0``: Applied Force
            * ``1``: Gravitational Force
            * ``2``: Frictional Force (Not yet implemented)
            * ``3``: Tension (Not yet implemented)
            * ``4``: Air Resistance (Not yet implemented)

        .. note:: Currently unused and not changed (will stay its initial value).

    x_rotation_axis_distance: :class:`float`
        The distance from the axis of rotation on the x-axis in meters.
        Vector quantity.

    y_rotation_axis_distance: :class:`float`
        The distance from the axis of rotation on the y-axis in meters.
        Vector quantity.

    z_rotation_axis_distance: :class:`float`
        The distance from the axis of rotation on the z-axis in meters.
        Vector quantity.

    x_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the x-axis.

    y_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the y-axis.

    z_rot_angle: :class:`float`
        The angle, in radians, from the axis of rotation on the z-axis.

    x_torque: :class:`float`
        The amount of torque on the x axis in newton meters.
        Vector quantity.

    y_torque: :class:`float`
        The amount of torque on the y axis in newton meters.
        Vector quantity.

    z_torque: :class:`float`
        The amount of torque on the z axis in newton meters.
        Vector quantity.

    """

    def __init__(self, name, x=0.0, y=0.0, z=0.0, force_type=0, x_rotation_axis_distance=0.0, y_rotation_axis_distance=0.0, z_rotation_axis_distance=0.0, x_rot_angle=0.0, y_rot_angle=0.0, z_rot_angle=0.0):
        """Create a force with the given name and horizontal and vertical forces in newtons. 
        Each dimension defaults to ``0`` so you only have to deal with what you want. force_type defaults to ``0`` to simply add an applied force.
        Force_type is not currently used."""
        self.name = name

        #Translational
        self.x = x #In newtons
        self.y = y
        self.z = z

        #Rotational force variables

        self.x_rotation_axis_distance = x_rotation_axis_distance
        self.y_rotation_axis_distance = y_rotation_axis_distance
        self.z_rotation_axis_distance = z_rotation_axis_distance

        self.x_rot_angle = x_rot_angle
        self.y_rot_angle = y_rot_angle
        self.z_rot_angle = z_rot_angle

        self.x_torque = 0.0
        self.y_torque = 0.0
        self.y_torque = 0.0

        self.calculate_torque()

        self.force_type = force_type


    def calculate_torque(self) -> tuple:
        """
        Calculate the torque this force applies on the x and y axis.

        Torque for each axis can be calculated using the following equation: ::

            torque = (distance from axis of rotation) * (force) * (sin(angle from axis of rotation))

        Returns
        -------
        tuple( :class:`float`, :class:`float`)
            The torque this force will apply to any object in the form (x_torque, y_torque, z_torque)

        """

        self.x_torque = self.x_rotation_axis_distance*self.x*math.sin(self.x_rot_angle)
        self.y_torque = self.y_rotation_axis_distance*self.y*math.sin(self.y_rot_angle)
        self.z_torque = self.z_rotation_axis_distance*self.z*math.sin(self.z_rot_angle)

        return (self.x_torque, self.y_torque, self.z_torque)
