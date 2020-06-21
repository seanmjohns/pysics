==========
The Basics
==========

PhysicsManager
==============

``PhysicsManager`` s represent a universe in which physics works a specific way based on its configuration. It is possible to have multiple universes that are used at the same time for different things. These "universes" operate on their own "ticks" (time). Each manager has a list of all the objects within its universe. When a tick passes for a universe, a tick passes for each object within it, and the forces for each object act on them.

Ticks
=====

"Ticks" are the amount of time that passes. The ``tick_length`` of a manager is configurable on the fly and is specific to each manager. It is common to change the tick length for an individual tick, sometimes to have a specific force to act over a smaller or instantaneous time interval (allowing for things like collisions). 

A tick passes when ``PhysicsManager.tick(tick_length)`` is called (the ``tick_length`` will default to the ``PhysicsManager``'s configured tick length). The default ``tick_length`` for a manager is 1 second (python value of 1). Velocity, acceleration, and position in pysics are measured in meters per second, meters per second^2, and meters, respectively (they all are in relation to seconds).

It is also common to make a tick pass for a specific object (``PhysicsObject.tick(tick_length)``; ``tick_length`` must be given). Time will then only pass for that object. 

Ticks do not go by automatically, but instead pass every time ``PhysicsManager.tick()`` is called (typically done every frame in a game loop). In other words, time only passes when ``tick()`` is called, and time is frozen at all other times. This provides the advantage of not relying on the CPU clock for passing time when implementing physics into your game. If you were to rely on how much real time had passed to determine when an object should move, they could become inconsistent because it takes time for the rest of your code to run, too, and that could cause issues for slower PCs.

Having a tick pass is simple. First set up a ``PhysicsManager``, then call ``tick()``: ::

    from pysics.manager import PhysicsManager

    manager = PhysicsManager(tick_length=0.1) #tick_length will be the manager's default tick length
    manager.tick()

In the above example, exactly 0.1 seconds has passed, because that is how long one tick for the ``manager`` is. In this case, calling tick was virtually pointless because there were no ``PhysicsObject`` s within the manager's universe to be acted upon, however it still qualifies as a good starting example.

PhysicsObject
=============

``PhysicsObject`` s are objects within a ``PhysicsManager`` universe. Every time a tick passes within a universe, a tick passes for a ``PhysicsObject``, and the forces applied to this object will take effect. 

As mentioned above, ticks can pass individually for a single object, and forces will only act on said object during the time interval. Each object contains a list of all the forces acting on it. An object's velocity and position can be manipulated directly without the use of forces, and can be useful in some situations. Each ``PhysicsObject`` has its own ``mass``.

Although objects *can* be within multiple universes, it is *not* recommended, because each universe will affect the object as ticks pass for that universe, making it difficult to understand what is happening. Certain game scenarios and effects may warrant such an action, but that is very rare. 

Force
=====

``Force`` s are exactly what they sound like: forces that act on a ``PhysicsObject``, and they are a part of their parent ``PhysicsObject``. Forces are in Newtons. They act on their parent objects based on how long an object is "ticked" (it is possible to tick an object individually, however in most cases, programmers tick in them unison with all other objects in their manager's universe). 

Example
=======

Below is an example in which an applied force will act on an object for a few ticks. We will break it down afterwards: ::

    from pysics.manager import PhysicsManager
    from pysics.physics_obj import PhysicsObject
    from pysics.force import Force

    tick_length = 1 #second
    manager = PhysicsManager(tick_length)

    ball = PhysicsObject("ball", xpos=10, ypos=10, xvel=10)
    manager.add_object(ball)

    print("Initial position: " + str(ball.get_pos()))

    force = Force("my force", x=-5)
    ball.apply_force(force)

    print("Position after applying force: " + str(ball.get_pos()))

    print("Ball position: (x, y, z)")

    for second in range(5):
        manager.tick()
        print(str(string_second) + " second(s): " + str(ball.get_pos()))

Now lets break it down: ::

    tick_length = 1 #second
    manager = PhysicsManager(tick_length)

These two lines set up and configure the manager and its universe. For this manager, each time ``tick()`` is called, 1 second will pass.

::
    
    ball = PhysicsObject("ball", x=10, y=10, xvel=10)
    manager.add_object(ball)

This will create a ball object and add it to the universe we created earlier. This new "ball" object will have an initial position of (10, 10) and an initial velocity of 10 meters per second to the right.

If we wanted to work in the third dimension, all we would have to do is use the ``z`` argument (ex: ``z=10``). This would make the ball's initial position on the z axis 10 meters from the "origin". For 2D games, the third dimension in pysics is generally not dealt with (and can be kept out of mind). Any position and velocity arguments that are not provided default to 0 meters or meters per second, respectively.

Lets move on to the next chunk of code. ::

    print("Initial position: " + str(ball.get_pos()))

    force = Force("my force", x=-5)
    ball.apply_force(force)

    print("Position after applying force: " + str(ball.get_pos()))

The first line just gives us the initial position of the ball for this example.

The next line creates a 5 newton force, "my force", that is directed in the **negative-x direction** (If you did not know this already, it is suggested that you take a physics mechanics recap/course). The following line applies our new force to the ball.

The last line in this chunk prints the ball's position. Lets take a look at the output from this bit of code: ::

    Initial position: (10.0, 10.0, 0)
    Position after applying force: (10.0, 10.0, 0)

"Hold up, but didn't we just apply a force to the ball? Why didn't it move?"

No time has passed. Velocity and acceleration only work over a time interval (remember the units? meters per **second** and meters per **second^2**). Time only passes when we call ``PhysicsManager.tick()`` (Time can also pass for an individual ``PhysicsObject`` if we call ``PhysicsObject.tick()``, but we'll get into that later).

Now for the final block: ::

    print("Ball position: (x, y, z)")

    for second in range(1,6):
        manager.tick()
        print(str(string_second) + " second(s): " + str(ball.get_pos()))   

The first line just prints out what form the ball's position will be (and has been) displayed in.

Within the for loop, exactly 5 ticks pass because ``manager.tick()`` is called 5 times. The total amount of time that passes within our ``manager``'suniverse is 5 seconds because the ``tick_length`` configured for it is 1 second. For each second, the position of the ball is printed in the form displayed by the first ``print()``. Let's look at what it outputs: ::

    Ball position: (x, y, z)
    1 second(s): (17.5, 10.0, 0.0)
    2 second(s): (20.0, 10.0, 0.0)
    3 second(s): (17.5, 10.0, 0.0)
    4 second(s): (10.0, 10.0, 0.0)
    5 second(s): (-2.5, 10.0, 0.0)

The first line is the form the ball's position is displayed in, as mentioned before.

The following lines are the ball's position for each second. Notice how the ball moves every time ``tick()`` is called. Within these 5 seconds, the ball has turned around and passed its starting position.

This example can also be found at the root of the repository (basic_example.py)

