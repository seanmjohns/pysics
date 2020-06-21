

class NameUsedError(Exception):
    """Raised when user attempts to use a name for a new Force or PhysicsObject that has already been used by another thing of the same type."""
    pass
    

class MassOfZeroError(Exception):
    """Raised when the user attempts to use a mass of 0 for a PhysicsObject (prevents division by 0)."""
    pass
