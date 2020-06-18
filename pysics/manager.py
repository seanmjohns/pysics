from pysics.physics_obj import PhysicsObject

from pysics.errors import NameUsedError

class PhysicsManager():
    """Represents a universe in which physics works the way it does in that universe.
    Time (ticks) passes individually in each universe."""

    objects=[]

    tick_length = 1 #Second - For scientific calculations, use milliseconds (1000th)

    gravitational_acceleration = 9.80665 

    game_mode = True #Whether or not to use less precise and optimised calculations for games, but not for scientific simulations

    def __init__(self, tick_length=1, gravitational_constant=9.80665, game_mode=True):
        self.tick_length = tick_length
        self.gravitational_constant = gravitational_constant
        self.game_mode = game_mode

    def tick(self, tick_length=tick_length):
        """Make a single physics tick pass for all objects in this universe.
        This is not recommended if you are creating a game. In the case of game creation, you should tick each object manually."""
        for obj in self.objects:
            obj.tick(self.tick_length)

    def tick_object(self, obj: PhysicsObject):
        """Make a single physics tick pass for a single object."""
        obj.tick(self.tick_length)

    def tick_length(self) -> float:
        """Returns the tick_length (in seconds)."""
        return self.tick_length
    
    def add_object(self, obj:PhysicsObject):
        """Add an object to this universe."""
        for obj in self.objects:
            if obj.name == name:
                raise NameUsedError(name, "PhysicsObject")
                return

        self.objects.append(obj)

    def remove_object(self, obj:PhysicsObject):
        self.objects.remove(obj)

    def remove_object_by_name(name:str):
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)
