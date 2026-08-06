// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Request.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/request.h"


#ifndef INTERFACES__MSG__DETAIL__REQUEST__STRUCT_H_
#define INTERFACES__MSG__DETAIL__REQUEST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'img'
#include "interfaces/msg/detail/combo_image__struct.h"
// Member 'request'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Request in the package interfaces.
typedef struct interfaces__msg__Request
{
  interfaces__msg__ComboImage img;
  rosidl_runtime_c__String request;
} interfaces__msg__Request;

// Struct for a sequence of interfaces__msg__Request.
typedef struct interfaces__msg__Request__Sequence
{
  interfaces__msg__Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Request__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__REQUEST__STRUCT_H_
