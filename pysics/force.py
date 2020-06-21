from .errors import MassOfZeroError

class Force():
    """A force that acts upon a :class:`PhysicsObject`.

    The x, y, and z attributes can be used freely by developers (meaning you can use any axis as you wish. For example, you could use the universe's y axis as your z axis).
    If you desire to only have 2D motion, then completely ignore an entire dimension. If you wish to only have 1D motion, the ignore 2 dimensions.

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

    Attributes
    ----------
    name: :class:`str`
        The name of this force. It cannot be the same as any other force on an object.

    x: :class:`float`
        The newtons of force in the x direction (typically left/right).
        Can be positive or negative, with (+) being right and (-) being left.

    y: :class:`float`
        The newtons of force in the y direction (typically vertical).
        Can be positive or negative, with (+) being up and (-) being down.

    z: :class:`float`
        The newtons of force in the z direction (typically forwards/backwards).
        Can be positive or negative, with (+) being forwards and (-) being backwards.

    force_type: :class:`int`
        Represents the type of force this force is with the following values:
            * ``0``: Applied Force
            * ``1``: Gravitational Force
            * ``2``: Frictional Force (Not yet implemented)
            * ``3``: Tension (Not yet implemented)
            * ``4``: Air Resistance (Not yet implemented)

        .. note:: Currently unused and not changed (will stay its initial value).

    """

    def __init__(self, name, x=0, y=0, z=0, force_type=0):
        """Create a force with the given name and horizontal and vertical forces in newtons. 
        Each dimension defaults to ``0`` so you only have to deal with what you want. force_type defaults to ``0`` to simply add an applied force.
        Force_type is not currently used."""
        self.name = name
        self.x = x #In newtons
        self.y = y
        self.z = z
        self.force_type = force_type
