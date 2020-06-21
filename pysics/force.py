from .errors import MassOfZeroError

class Force():
    """A force that acts upon a :class:`PhysicsObject`.
    If the gravitational constant is provided and nonzero, then a vertical force will calculated from it and the ``parent_mass`` (mass of the owning object).
    Some forces, especially gravitational forces, should not be used on multiple objects at once, but others that are not effected by the owning object's values can be.

    The x, y, and z attributes can be used freely by developers (meaning you can use any axis as you wish. For example, you could use the y axis as the z axis).
    If you desire to only have 2D motion, then completely ignore an entire dimension. If you wish to only have 1D motion, the ignore 2 dimensions.

    Parameters
    ----------
    name: :class:`str`
        The force's name. Used to identify this force when applied to an object.

    x: :class:`float`
        The newtons of force in the x direction. Defaults to 0.0 if not supplied.
        East is positive, West is negative.

    y: :class:`float`
        The newtons of force in the x direction. Defaults to 0.0 if not supplied.
        Up is positive, Down is negative.

    z: :class:`float`
        The newtons of force in the x direction. Defaults to 0.0 if not supplied.
        North is positive, South is negative.

    force_type: :class:`int`
        Represents the type of force this is with the following values:
            * ``0``: Applied Force
            * ``1``: Gravitational Force
            * ``2``: Fricational Force (Not yet implemented)
            * ``3``: Tension (Not yet implemented)
            * ``4``: Air Resistance (Not yet implemented)

        .. note:: 
            Currently unused and will not change (will always stay initial value)

    g: :class:`float`
        Only used on force creation and if this is nonzero.
        The gravitational acceleration of this force. When g is supplied, then the y component of this force is calculated using g and the parent_mass.

        :todo: Add an example for using this.

    parent_mass: :class:`float`
        Only used on force creation and if g is supplied.
        The mass of the object that will own this force.
        .. note:: The force will not be recalculated if the parent object's mass is changed, thus messing up the gravitational force's effect.


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
            * ``2``: Fricational Force (Not yet implemented)
            * ``3``: Tension (Not yet implemented)
            * ``4``: Air Resistance (Not yet implemented)

        .. note:: Currently unused and not changed (will always stay 0)

    g: :class:`float`
        The gravitational acceleration constant this force uses.
        Only used on force creation when supplied and nonzero.

    """
    #If you wish to only to 2 dimentional motion, ignore oneof the dimensions

    name = "force"
    
    # In newtons
    x = 0.0 #The portion of the force on the x axis in Newtons
    y = 0.0 #The portion of the force on the y axis in Newtons
    z = 0.0 #The portion of the force on the z axis in Newtons

    #Types:
    #   0: Applied
    #   1: Gravitational Force (Implement much later)
    #   2: Frictional (Changes based on speed unless its kinetic) ( Implement later)
    #   3: Tension (Implement much later)
    #   4: Air resistance (Implement much later)
    force_type = 0

    g = 9.80665 #Gravitational acceleration. Only applies if this is a gravitational force


    def __init__(self, name, x=0, y=0, z=0, force_type=0, g=0, parent_mass=0):
        """Create a force with the given name and horizontal and vertical forces in newtons. 
        Each dimension defaults to 0 so you only have to deal with what you want. force_type defaults to 0 to simply add an applied force.
        The gravitational constant is different for every force and defaults to 0.
        If you wish to have a specific gravitational acceleration for a gravitational force, supply g instead of vertical force and the
        object's mass (parent_mass). The vertical force will be calculated from them. Forces created this way cannot be used by two different objects."""
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
