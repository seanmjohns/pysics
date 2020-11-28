==================
Accuracy of Pysics
==================

As you might know, computers are limited in how accurate they can be with simulations (although they can be pretty accurate!).

Collision Accuracy
==================
When a tick passes for a universe (or individual object), pysics simply teleports all affected objects to their new positions and updates their velocities.
Due to this teleportation, objects might "jump" (teleport past) boundaries or other objects that they are supposed to collide with, decreasing the accuracy of pysics. The teleportation distance is proportional to ``tick_length`` and velocity.

Below is a `graph <https://www.desmos.com/calculator/xs1dpo8twj>`_ relating collision accuracy to ``tick_length`` with pysics (It also models collision accuracy related to object velocity):

.. image::
    /images/collision_accuracy_ticks.png
    :alt: collision accuracy relative to ``tick_length``
    :align: center
    :scale: 30%

In the graph, as ``tick_length`` approaches 0, accuracy approaches unbounded infinity (it gets better and better). Unfortunately, computers only have so much computational power, so our games will slow as we decrease the ``tick_lenght`` (assuming ``tick()`` is called faster to compensate).

Additionally if ``tick_length`` were swapped with velocity, as velocity approaches 0, accuracy approaches unbounded infinity (the model would not change), because objects would not teleport as far (assuming ``tick_length`` stays constant).

.. note::
    ``tick_length`` cannot be 0, because then no time would pass.

General Accuracy
================

Although smaller ``tick_length`` s lead to improved *collision* accuracy, it decreases the *general* accuracy of Pysics' calculations by a very small fraction (over the same total time) due to `decimal rounding and estimation <https://softwareengineering.stackexchange.com/questions/101163/what-causes-floating-point-rounding-errors>`_. This should **by no means** discourage you from using a smaller ``tick_length``, as the decimal rounding is very small and should not be an issue in most cases, and, as mentioned before, smaller ``tick_length`` s improve accuracy in other situations.

Below is a `graph <https://www.desmos.com/calculator/vaza9cycsk>`_ relating the general accuracy of pysics' calculations to ``tick_length``:

.. image::
    /images/general_accuracy.png
    :alt: Pysics' general accuracy relative to ``tick length``.
    :align: center
    :scale: 30%

As shown in the graph, as ``tick_length`` approaches 0, accuracy worsens. As more ticks pass (more passing ticks over the same period of time with a smaller ``tick_length``), there are more calculations, so the positions and velcocities of objects are rounded more often.

