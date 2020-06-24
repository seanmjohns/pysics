from .obj import PhysicsObject

from .errors import NameUsedError

class PhysicsManager():
    """Represents a universe in which physics works the way it does in that universe.
    Time (ticks) passes individually in each universe.

    Parameters
    ----------
    tick_length: :class:`float`
        The amount of time, in seconds, a tick is for this universe. This can be changed after initialization.
        Time can move backwards.

    Attributes
    ----------
    objects: List[:class:`pysics.physics_obj.PhysicsObject`]
        All the objects within this universe. 
        Ticks pass for all objects when :meth:`tick` is called.

    tick_length: :class:`double`
        The configured value of how many seconds a tick is.
        Recommended to be small for games to reduce/prevent collision issues.
        Yes, time can move backwards.

    """

    def __init__(self, tick_length=1):
        self.objects = []
        self.tick_length = tick_length

    def tick(self, tick_length=None):
        """Make a single physics tick pass for all objects in this universe. 

        If tick_length is not supplied, then use the universe's tick length.

        Parameters
        ----------
        tick_length: :class:`float`
            The amount of time this tick lasts. 
            
            .. note::

                Time *can* move backwards.

        """
        
        if tick_length is None: tick_length = self.tick_length #If tick length is 0, that means no tick length was given
        for obj in self.objects:
            obj.tick(tick_length)

    def tick_object(self, obj: PhysicsObject):
        """
        Make a single physics tick pass for a single object. The tick_length is this manager's configured length.

        This can be achieved by calling :meth:`pysics.physics_obj.PhysicsObject.tick` and providing the configured tick_length.

        Parameters
        ----------
        obj: :class:`pysics.physics_obj.PhysicsObject`
            The object that is to be ticked.

        """
        obj.tick(self.tick_length)

    def add_object(self, ph_obj:PhysicsObject):
        """

        Add an object to this universe. Adds the object to the end of the ``objects`` list.

        Parameters
        ----------
        ph_obj: :class:`pysics.physics_obj.PhysicsObject`
            The object to be added to this universe.

        Raises
        ------
        :exc:`pysics.errors.NameUsedError`
            There cannot be two objects in one universe with the same name.

        """
        for obj in self.objects: #Make sure its name is not already used
            if obj.name == ph_obj.name:
                raise NameUsedError("There cannot be two objects within the same universe with the same name.")

        self.objects.append(ph_obj)

    def remove_object(self, obj:PhysicsObject):
        """
        Remove a physics object using the instance itself.

        Parameters
        ----------
        obj: :class:`pysics.physics_obj.PhysicsObject`
            The object to remove from this universe (the instance itself).

        """
        self.objects.remove(obj)

    def remove_object_by_name(name:str):
        """

        Remove a physics object using its name.

        If there is no object with the given name, fails silently.

        Parameters
        ----------
        name: :class:`str`
            The name of the object to be removed.

        """
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)

    def clear(self) -> tuple:
        """

        Remove all physics objects from the universe. Clears the objects list.

        Returns
        -------
        List[:class:`pysics.physics_obj.PhysicsObject`]
            All the objects that were previously a part of this universe.
            Useful for transferring all objects to a different universe.

        """
        objects_copy = self.objects
        self.objects.clear()
        return objects_copy
