.. _docs-build-details:

Documentation backend
=====================

This section is for advanced users who want to understand how the backend of this
documentation works. If you haven't already, please read :ref:`docs-build` first.

Adding documentation
--------------------

To add documentation to an existing repository, you can simply copy the ``docs`` directory from one of the repos that you see on the side and make a few small edits. In particular:

* Update ``docs/source/conf.py``. This is the main file where all the magic happens. In particular, you
  will want to change the ``project``, ``copyright``, ``author``, and ``version`` variables. If you
  need to add new sections for the autodocs, you can do that in the ``napoleon_custom_sections``
  list.

* Update ``docs/source/mock_imports``. As mentioned in :ref:`docs-build-individual` the mock imports are used for emulating packages which cannot be installed in the Docker image used to build the docs. If you end up having an issue with an external Python module which you do not want to document, you can try adding it there.

* Update ``docs/Dockerfile``. You will have to change the base image to be the one that you are
  documenting. Depending on what you are working with, you might need to change the entry point
  as well. It is highly recommended not to change the other commands.

* Update ``docs/source/index.rst``. This is the title page and you will have to change the heading and update the content.

* Update ``docs/source/packages``. Each package must have its own page here. Remove the existing ones and add ones for the packages in your repository.

Then you should be able to build it by following the instructions in :ref:`docs-build-individual`.

Understanding the individual build process
------------------------------------------
`Sphinx <http://www.sphinx-doc.org/en/master/index.html>`_ expects the structure of a Python module and not a bunch of loose Python files. That is why, what is happening behind the scenes is that we are building a Python module calld ``nodes`` that contains all the node classes in the repository. This is done in ``docs/source/conf.py``.

All the node source files are copied from the ``package_name/src`` directory to a temporary   directory and an appropriate ``__init__.py`` file is generated. This procedure is senstitvie to   the structure of the repository and the naming of the source directory (should always be called  ``src``). Moreover, if duplicate names exist across the packages, these will be overwritten  which would lead to unexpected results.

The libraries, on the other hand can directly be processed by Sphinx but that is done on a   stand-alone basis. In other words, as far as Sphinx is concerned, these libraries have nothing   to do with the nodes. Again, duplicate names would result un unexpected behavior.

In order to enable a more natural documentation of ROS nodes, we have also added a few custom   sections to `Napoleon <http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_,   the Sphinx extension we use for processing the docstrings. This requires a custom version of   Napoleon as can be seen in ``docs/Dockerfile``. These custom sections can be edited in the   ``napoleon_custom_sections`` list in ``docs/source/conf.py``. Also note that the Sphinx version is currently fixed to ``1.7.0`` because Python 2 compatibility was necessary due to all the ROS code running on our robots is still in Python 2.


Understanding the combined build process
----------------------------------------

Building the combined documentation requires an extra level of moving files around. This is done by the ``launch.sh`` file in `docs-sphinxapi <https://github.com/duckietown/docs-sphinxapi>`_. It clones all the repositories listed in ``docs/source/repositories.txt``. Then, when building the ``nodes`` module, the source files from all the cloned directories are aggregated. Hence, there should be no name reuse across the combined repositories as well. If you wish to add a new repository the the combined documentation, edit the ``repositories.txt`` file and the ``index.rst``.

The combined documentation also hosts non-code related pages such as this one. These can also be found under ``docs/source`` in the `docs-sphinxapi <https://github.com/duckietown/docs-sphinxapi>`_ repository.