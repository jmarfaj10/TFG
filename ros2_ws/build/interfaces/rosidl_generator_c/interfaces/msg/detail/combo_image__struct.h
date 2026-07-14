// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/combo_image.h"


#ifndef INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_H_
#define INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'img_rgb'
// Member 'img_depth'
#include "sensor_msgs/msg/detail/image__struct.h"

/// Struct defined in msg/ComboImage in the package interfaces.
typedef struct interfaces__msg__ComboImage
{
  double cx;
  double cy;
  double fx;
  double fy;
  sensor_msgs__msg__Image img_rgb;
  sensor_msgs__msg__Image img_depth;
} interfaces__msg__ComboImage;

// Struct for a sequence of interfaces__msg__ComboImage.
typedef struct interfaces__msg__ComboImage__Sequence
{
  interfaces__msg__ComboImage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__ComboImage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_H_
