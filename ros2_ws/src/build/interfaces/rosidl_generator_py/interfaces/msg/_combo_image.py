# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interfaces:msg/ComboImage.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ComboImage(type):
    """Metaclass of message 'ComboImage'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.msg.ComboImage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__combo_image
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__combo_image
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__combo_image
            cls._TYPE_SUPPORT = module.type_support_msg__msg__combo_image
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__combo_image

            from sensor_msgs.msg import Image
            if Image.__class__._TYPE_SUPPORT is None:
                Image.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ComboImage(metaclass=Metaclass_ComboImage):
    """Message class 'ComboImage'."""

    __slots__ = [
        '_cx',
        '_cy',
        '_fx',
        '_fy',
        '_img_rgb',
        '_img_depth',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'cx': 'double',
        'cy': 'double',
        'fx': 'double',
        'fy': 'double',
        'img_rgb': 'sensor_msgs/Image',
        'img_depth': 'sensor_msgs/Image',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'Image'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'Image'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.cx = kwargs.get('cx', float())
        self.cy = kwargs.get('cy', float())
        self.fx = kwargs.get('fx', float())
        self.fy = kwargs.get('fy', float())
        from sensor_msgs.msg import Image
        self.img_rgb = kwargs.get('img_rgb', Image())
        from sensor_msgs.msg import Image
        self.img_depth = kwargs.get('img_depth', Image())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.cx != other.cx:
            return False
        if self.cy != other.cy:
            return False
        if self.fx != other.fx:
            return False
        if self.fy != other.fy:
            return False
        if self.img_rgb != other.img_rgb:
            return False
        if self.img_depth != other.img_depth:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def cx(self):
        """Message field 'cx'."""
        return self._cx

    @cx.setter
    def cx(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'cx' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'cx' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._cx = value

    @builtins.property
    def cy(self):
        """Message field 'cy'."""
        return self._cy

    @cy.setter
    def cy(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'cy' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'cy' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._cy = value

    @builtins.property
    def fx(self):
        """Message field 'fx'."""
        return self._fx

    @fx.setter
    def fx(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'fx' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'fx' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._fx = value

    @builtins.property
    def fy(self):
        """Message field 'fy'."""
        return self._fy

    @fy.setter
    def fy(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'fy' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'fy' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._fy = value

    @builtins.property
    def img_rgb(self):
        """Message field 'img_rgb'."""
        return self._img_rgb

    @img_rgb.setter
    def img_rgb(self, value):
        if self._check_fields:
            from sensor_msgs.msg import Image
            assert \
                isinstance(value, Image), \
                "The 'img_rgb' field must be a sub message of type 'Image'"
        self._img_rgb = value

    @builtins.property
    def img_depth(self):
        """Message field 'img_depth'."""
        return self._img_depth

    @img_depth.setter
    def img_depth(self, value):
        if self._check_fields:
            from sensor_msgs.msg import Image
            assert \
                isinstance(value, Image), \
                "The 'img_depth' field must be a sub message of type 'Image'"
        self._img_depth = value
