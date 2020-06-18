

class NameUsedError(Exception):
    """Raised when user attempts to use a name for a new Force or PhysicsObject that has already been used by another thing of the same type."""
    pass
    

class MassOfZeroError(Exception):
    """Raised when the user attempts to use a mass of 0 for an object.
    If this were allowed, then acceleration would be infinite (we would really get a divide by 0 error)."""
    pass
