// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "interfaces/msg/detail/combo_image__struct.h"
#include "interfaces/msg/detail/combo_image__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool sensor_msgs__msg__image__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * sensor_msgs__msg__image__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool sensor_msgs__msg__image__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * sensor_msgs__msg__image__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool interfaces__msg__combo_image__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[39];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("interfaces.msg._combo_image.ComboImage", full_classname_dest, 38) == 0);
  }
  interfaces__msg__ComboImage * ros_message = _ros_message;
  {  // cx
    PyObject * field = PyObject_GetAttrString(_pymsg, "cx");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->cx = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // cy
    PyObject * field = PyObject_GetAttrString(_pymsg, "cy");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->cy = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // fx
    PyObject * field = PyObject_GetAttrString(_pymsg, "fx");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->fx = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // fy
    PyObject * field = PyObject_GetAttrString(_pymsg, "fy");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->fy = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // img_rgb
    PyObject * field = PyObject_GetAttrString(_pymsg, "img_rgb");
    if (!field) {
      return false;
    }
    if (!sensor_msgs__msg__image__convert_from_py(field, &ros_message->img_rgb)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // img_depth
    PyObject * field = PyObject_GetAttrString(_pymsg, "img_depth");
    if (!field) {
      return false;
    }
    if (!sensor_msgs__msg__image__convert_from_py(field, &ros_message->img_depth)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * interfaces__msg__combo_image__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ComboImage */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("interfaces.msg._combo_image");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ComboImage");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  interfaces__msg__ComboImage * ros_message = (interfaces__msg__ComboImage *)raw_ros_message;
  {  // cx
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->cx);
    {
      int rc = PyObject_SetAttrString(_pymessage, "cx", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // cy
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->cy);
    {
      int rc = PyObject_SetAttrString(_pymessage, "cy", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fx
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->fx);
    {
      int rc = PyObject_SetAttrString(_pymessage, "fx", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fy
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->fy);
    {
      int rc = PyObject_SetAttrString(_pymessage, "fy", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // img_rgb
    PyObject * field = NULL;
    field = sensor_msgs__msg__image__convert_to_py(&ros_message->img_rgb);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "img_rgb", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // img_depth
    PyObject * field = NULL;
    field = sensor_msgs__msg__image__convert_to_py(&ros_message->img_depth);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "img_depth", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
