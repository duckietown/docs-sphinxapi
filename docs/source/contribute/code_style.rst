ROS nodes code style guide
==========================

In order to ensure consistent and helpful code that is easy to understand and extend we follow the general guidelines outline here.

* The :py:class:`duckietown.DTROS` class should be inherited by all Duckietown ROS nodes.

* All node parameters should be dynamically configurable unless there is a very good reason why not. :py:class:`duckietown.DTROS`’s framework should be used for handling these.

* The beginning of the ``__init__`` method of the ROS node class should be structured like that::

    def __init__(self, node_name):

        # Initialize the DTROS parent class
        super(CoolNode, self).__init__(node_name=node_name)

        # Add the node parameters to the parameters dictionary and load their default values
        self.parameters['~important_parameter'] = None
        self.parameters['~even_more_important_parameter'] = None
        self.updateParameters()

  The :py:meth:`duckietown.DTROS.updateParameters()` method loads the parameters from the parameter server and starts a process that regularly checks if they are changed. Do not forget to add it. Otherwise the parameters will never be loaded.

  If the parameters are changed the :py:attr:`duckietown.DTROS.parametersChanged` property will be set to ``True``. Your node should detect that, adjust anything that depends on these parameters, adn then set it back to ``False``.

* The parameters of each node should be stored under ``config/NODE_NAME/default.yaml``.

* The default values should be only stored in the config files, no default values should be hard-coded in the code.

* Logging should be done through the :py:meth:`duckietown.DTROS.log` method. You can read more on this in the documentation of the method.

* Node shutdown should use the :py:meth:`duckietown.DTROS.onShutdown` method inherited from :py:class:`duckietown.DTROS` unless there’s a good reason to customize it. See :py:class:`wheels_driver.WheelsDriverNode` for an example of redefining the :py:meth:`duckietown.DTROS.onShutdown` method.

* The nodes should accept their name as an initialization argument called ``node_name``.

* Nodes should be defined as classes, and launched like that::

   if __name__ == '__main__':
       # Initialize the node with rospy
       node = WheelsDriverNode(node_name='wheels_driver_node')
       # Keep it spinning to keep the node alive
       rospy.spin()

* Make sure you initialize the callbacks only after you’ve defined all the class attributes
  that they are using. Otherwise you risk getting a AttributeError when you try to access a
  yet undefined attribute.

  **Wrong**::

   class CoolNode(DTROS):
      def __init__(...):
          sub_a = self.subscriber(..., callback=mycallback, ...)
          self.important_variable = 3.1415

      def mycallback(self):
          self.important_variable *= 1.0

  **Correct**::

    class CoolNode(DTROS):
        def __init__(...):
            self.important_variable = 3.1415
            sub_a = self.subscriber(..., callback=mycallback, ...)

        def mycallback(self):
            self.important_variable *= 1.0

* :py:class:`duckietown.DTROS` provides a :py:attr:`duckietown.DTROS.switch` property for each
  ROS Node Class. In case that the output or actions of this node are not required it can be
  set to `False`. This will automatically prevent your node from receiving any messages and
  hence executing callbacks. If you need some  special treatment fo such cases, make sure to implement it.

* Always use :py:meth:`duckietown.DTROS.publisher` and :py:meth:`duckietown.DTROS.subscriber` to initialize Publishers and Subscribers. **Never** use ``rospy.Subscriber`` or ``rospy.Publisher``. The APIs are identical.

* The names of all callback methods should start with ``cb``, e.g. ``cbWheelsCmd``.

* camelCase should be used for naming methods.

* In Python code, **never ever** do universal imports like ``from somepackage import *``. This is
  an extremely bad practice. Instead, specify exactly what you are importing, i.e.
  ``from somepackage import somefunction``.  It is fine if you do it in ``__init__.py`` files
  but even then try to avoid it if possible.

* When using a package that has a common practice alias, use it,
  e.g. ``import numpy as np``, ``import matplotlib.pyplot as plt``, etc. However, refrain from
  defining your own aliases.