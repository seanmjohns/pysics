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

    def tick(self, tick_length=-1):
        """Make a single physics tick pass for all objects in this universe. If tick_length is 0, then use the universe's tick length.
        This is not recommended if you are creating a game. In the case of game creation, you should tick each object manually."""
        
        if tick_length < 0: tick_length = self.tick_length #If tick length is 0, that means no tick length was given
        for obj in self.objects:
            obj.tick(tick_length)

    def tick_object(self, obj: PhysicsObject):
        """Make a single physics tick pass for a single object."""
        obj.tick(self.tick_length)

    def tick_length(self) -> float:
        """Returns the tick_length (in seconds)."""
        return self.tick_length
    
    def add_object(self, ph_obj:PhysicsObject):
        """Add an object to this universe."""
        for obj in self.objects: #Make sure its name is not already used
            if obj.name == ph_obj.name:
                raise NameUsedError(name, "PhysicsObject")

        self.objects.append(ph_obj)

    def remove_object(self, obj:PhysicsObject):
        """Remove a physics object using the instance itself"""
        self.objects.remove(obj)

    def remove_object_by_name(name:str):
        """Remove a physics object using its name"""
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)

    def clear(self):
        """Remove all physics objects from the universe."""
        self.objects.clear()
