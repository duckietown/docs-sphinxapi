.. _docs-build:

Building the documentation
==========================

Documenting ROS Nodes can be tricky, especially when done across multiple repositories. You don't
need to build the documentation in order to use it. You can use the pre-built official
documentation, which happens to be exactly the page you are currently on! However, in case
you want to contribute a change to the documentation, or if you wish to implement a
similar documentation system to your own project, this is the place to be.

Here we will discuss how to build the ``html`` files that constitute this webpage if all the
backend has already been setup for you. This is the workflow you need to follow if you want
to test how the changes that you propose would look like.

If you wish to setup your own workflow, make bigger changes, or understand the magic (and hacks)
behind this webpage, check out :ref:`docs-build-details`.

Where are the docs sources?
---------------------------

The sources that generate the documentation of the repositories here is intertwined with the code.
Every ROS node has its documentation implemented as docstrings. Every library in the ``include``
directory is structured and documented as a Python module. Then to link the pages together
a dedicated documentation page is added in ``docs/source/packages`` for each package in the
repository. The standard structure of these pages is as follows::

   led\_emitter package
   ====================

   .. contents::

   The ``led_emitter`` package provides the drivers that control the LEDs of a Duckiebot.
   It provides a convenient API for turning the LEDs on and off, changing their color and making
   them blink with various frequencies. You can see examples how to do that in the description
   of the ``LEDEmitterNode`` class bellow.

   LEDEmitterNode
   --------------

   .. autoclass:: nodes.LEDEmitterNode

   Included libraries
   ------------------

   rgb_led
   ^^^^^^^

   .. automodule:: rgb_led

It always must be titled with the package name and "package" and start with a table of contents
of the page. This must be followed by a short description of the package. After that a list of
all nodes (if any) should be provided, followed by the documentation of the libraries (if any).
These files must be **manually** updated at this moment. The generation of the documentation
from the libraries and the ROS nodes source files is **automatic**.

.. _docs-build-individual:

Building an individual repository
---------------------------------

This webpage combines the documentations of multiple repositories. Typically, you would need to
only build the one that you make changes to. Once your changes are merged into the main branch,
this webpage will automatically update. Therefore, this section would focus on building the
documentation of a single repository.

This documentation system is based on the Python documentation generator
`Sphinx <http://www.sphinx-doc.org/en/master/index.html>`_. Sphinx is great
when one tries to load a Python module and has all the dependencies installed.
When your code is not structured as a Python module, or if you are missing some
dependencies, than you need to hack your way around it. In our case, we face both
challenges.

In order to ensure that all dependencies are accounted for we build the documentation
on top of the Docker container containing all the code. So, first build the main Docker image
by running ``dts devel build`` in the main directory of the repository. This will ensure that you
have a local image corresponding to the changes you have made.

Now you can add the documentation-specific files and dependencies on top of that, build
the documentation in the new container and copy it to your host system. Here is everything
combined neatly in a single command::

  docker run -it --rm -v $(pwd):/code/catkin_ws/src/dt-car-interface/ $(docker build -q docs/)  bash -c "cd /code/catkin_ws/src/dt-car-interface/docs; rm -r build; make html"

The resulting ``html`` files are in ``docs/build/html``. If you experience an issue with a Python
module (e.g. some hardware drivers that exist on the robot but not on your computer), you can
add it to the ``docs/source/mock_imports`` file. `Mock imports <http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_mock_imports>`_ are
Python modules that Sphinx will pretend to be available even when they are not.

Warning:
   Always make sure to delete the  ``docs/build`` directory before you build
   the documentation. If you fail to do so, your changes might not be incorporated in the build.

Building the combined documentation
-----------------------------------

If you want to make a change to any of the pages outside the code repositories (e.g. to the
pages in the *Contribute* section such as this one) then you need to make a pull request in
the repository that combines everything together. The combined documentation source is hosted `here <https://github.com/duckietown/docs-sphinxapi>`_.

Clone the ``docs-sphinxapi`` repository and run the following command::

  rm -r output; docker create --name docs-sphinxapi-temp $(docker build -q .); docker cp docs-sphinxapi-temp:/output output; docker rm docs-sphinxapi-temp

This will clone all the other relevant repositories and will arrange for building
everything together. The resulting ``html`` files should be in the ``output`` directory.
For more details, check :ref:`docs-build-details`.

Warning:
   Always make sure to delete the ``output`` directory before you build
   the documentation. If you fail to do so, your changes might not be incorporated in the build.

