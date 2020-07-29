======================
Collisions with Pysics
======================

Creating collisions with Pysics requires some background physics knowledge (we'll discuss that knowledge here for applications).

Vertical or Horizontal Boundary Collisions
==========================================

We are assuming here that these collisions are perfectly elastic, meaning no kinetic energy is lost (KE is a scalar, meaning direction does not apply).

First, we need to understand how collision physics works (at least in an ideal universe). When an object collides with another object, an impulse force is applied to both forces, typically in opposite directions, over a very small amount of time. Impulse can be calculated by the following equation: ::

    Impulse = (force)(time)

Additionally, according to the `Law of Conservation of Momentum <https://en.wikipedia.org/wiki/Momentum>`_, we know that in *all* collisions, the net momentum between the two-object system must stay the same (so ``(momentum in) = (momemntum out)``. The change in momentum can be calculated using the following equation: ::

    Change in Momentum = (Final velocity)*(System Mass) - (Initial velocity)*(System Mass)

We *also* know that ``Impulse = Change in Momentum`` in a collision, so: ::

    (force)*(time) = (Final velocity)*(System mass) - (Initial velocity)*(System mass)

Using the ``Impulse`` and ``Change in Momentum`` equations, we will be able to solve for the force we need to bounce the object: ::

    force = ((Final velocity)*(System mass) - (Initial velocity)*(System mass))/(time)
    force = (mass*(change in net velocity))/time


Since the object is colliding with a boundary that was not moving and will not move, we know that it had ``0`` momentum beforehand, and it will have ``0`` momentum after the collision. Because the boundary has no momentum before and after, the object must account for all the momentum in the system. The ``change in system velocity`` will therefore be the object's change in velocity (and the ``system mass`` will just be the object's mass, because we are assuming the boundary has no mass).

Since no momentum is lost, the object must be moving at the same velocity magnitude as it was before the collision, so the change in velocity will be ``velocity*2``.

What is the time period of the impulse? The amount of time we will be applying our collision force over. This should be an extremely small period of time (like 1/1000 of normal ``tick_length``). To apply this force: ::

    collision_force = ("collision force", y=(abs(2*ball.yvel)*ball.mass)/wall_bounce_tick_length)
    object.apply_force(collision_force)
    object.tick(wall_bounce_tick_length)
    object.remove_force(collision_force)

Notice how the time from our equation is the amount of time the force is applied.

Now we can use our knowledge of impulse and momentum to make a ball bounce off the ground: ::

    tick_length = 0.1 #A good tick lenght for games.
    manager = PhysicsManager(tick_length)

    wall_bounce_tick_length = 0.0001 #This needs to be much less than the normal tick length

    #... Creating the ball, adding gravitational force to it, etc.

    while True:
        #... Make the stuff run at desired fps
        manager.tick()
        if ball.ypos <= 0: #If the ball hits the floor
            collision_force = ("collision force", y=(abs(2*ball.yvel)*ball.mass)/wall_bounce_tick_length)
            ball.apply_force(collision_force)
            ball.tick(wall_bounce_tick_length) #Extremely small amount of time
            ball.remove_force(collision_force)

        #... Draw the stuff to the screen
        #... Events, blah, blah, blah

This can be seen in action in graphical_example.py
