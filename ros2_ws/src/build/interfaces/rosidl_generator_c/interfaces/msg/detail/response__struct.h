// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Response.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/response.h"


#ifndef INTERFACES__MSG__DETAIL__RESPONSE__STRUCT_H_
#define INTERFACES__MSG__DETAIL__RESPONSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'response'
// Member 'object'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Response in the package interfaces.
typedef struct interfaces__msg__Response
{
  rosidl_runtime_c__String response;
  rosidl_runtime_c__String object;
  float x;
  float y;
  float z;
} interfaces__msg__Response;

// Struct for a sequence of interfaces__msg__Response.
typedef struct interfaces__msg__Response__Sequence
{
  interfaces__msg__Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__RESPONSE__STRUCT_H_
