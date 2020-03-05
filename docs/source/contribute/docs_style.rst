Documentation style guide
=========================

In order to ensure consistent and helpful documentation, adhere to the following style requirements.

* The API documentation follows the reStructuredText markup syntax. A list of the available directives can be found `here <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_.

* General description about ROS nodes (and classes in general) should happen in the class docstring,
  not the init method. The init method **should not** have a docstring. If it has, it will not
  be shown in the documentation

* Arguments, topics, services, parameters, etc. should always be written in the local namespace (i.e. starting with ``~``).

* External links can be added like that::

    `Picamera <https://picamera.readthedocs.io/>`_

* Values, names of variables, errors, messages, etc, should be in grave accent quotes::

    ``like that``

* Every class, method or function should have a docstring describing at least its inputs and outputs.

* Always indicate the type of the input or output. If it is a message, use the message type. If a list, a dictionary, or a tuple, you can use expressions like ``(:obj:`list` of :obj:`float`)``

* The following section names have special use: ``Examples``, ``Raises``, ``Configuration``, ``Subscribers``, ``Subscriber``, ``Publishers``, ``Publisher``, ``Services``, ``Service``, ``Fields``, ``inputs``, ``input``, ``outputs``, ``output``.

* You can add a link to a different package, node, method, or object like that::

  :py:mod:`duckietown`
  :py:class:`duckietown.DTROS`
  :py:meth:`duckietown.DTROS.publisher`
  :py:attr:`duckietown.DTROS.switch`

Examples:

.. code-block:: rest    

   class CameraNode(DTROS):
       """Handles the imagery.

       The node handles the image stream, initializing it, publishing frames
       according to the required frequency and stops it at shutdown.
       `Picamera <https://picamera.readthedocs.io/>`_ is used for handling the image stream.

       Note that only one :obj:`PiCamera` object should be used at a time. If another node
       tries to start an instance while this node is running, it will likely fail with an
       `Out of resource` exception.

       The configuration parameters can be changed dynamically while the node is running
       via `rosparam set` commands.

       Args:
           node_name (:obj:`str`): a unique, descriptive name for the node that ROS will use

       Configuration:
           ~framerate (:obj:`float`): The camera image acquisition framerate, default is 30.0 fps
           ~res_w (:obj:`int`): The desired width of the acquired image, default is 640px
           ~res_h (:obj:`int`): The desired height of the acquired image, default is 480px
           ~exposure_mode (:obj:`str`): PiCamera exposure mode, one of
           `these <https://picamera.readthedocs.io/en/latest/api_camera.html?highlight=sport#picamera.PiCamera.exposure_mode>`_, default is `sports`

       Publisher:
           ~image/compressed (:obj:`CompressedImage`): The acquired camera images

       Service:
           ~set_camera_info:
               Saves a provided camera info to
               `/data/config/calibrations/camera_intrinsic/HOSTNAME.yaml`.

               input:
                   camera_info (`CameraInfo`): The camera information to save

               outputs:
                   success (`bool`): `True` if the call succeeded
                   status_message (`str`): Used to give details about success

       """

       def __init__(self, node_name):

           # Initialize the DTROS parent class
           super(CameraNode, self).__init__(node_name=node_name)


           [ ... ]

       def loadCameraInfo(self, filename):
           """Loads the camera calibration files.

           Loads the intrinsic and extrinsic camera matrices.

           Args:
               filename (:obj:`str`): filename of calibration files.

           Returns:
               :obj:`CameraInfo`: a CameraInfo message object

           """
           stream = file(filename, 'r')
           calib_data = yaml.load(stream)
           cam_info = CameraInfo()