// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from interfaces:msg/Goal.idl
// generated code does not contain a copyright notice

#include "interfaces/msg/detail/goal__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_interfaces
const rosidl_type_hash_t *
interfaces__msg__Goal__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdc, 0x6d, 0x9a, 0xb5, 0x2b, 0xd9, 0xdb, 0xa4,
      0x86, 0xe1, 0x7d, 0x30, 0xef, 0xea, 0xa4, 0x69,
      0x3d, 0xaf, 0x7a, 0x49, 0x35, 0x3f, 0xb0, 0xb5,
      0xef, 0x45, 0x3d, 0x40, 0xe0, 0x08, 0xc0, 0xc8,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char interfaces__msg__Goal__TYPE_NAME[] = "interfaces/msg/Goal";

// Define type names, field names, and default values
static char interfaces__msg__Goal__FIELD_NAME__x[] = "x";
static char interfaces__msg__Goal__FIELD_NAME__y[] = "y";
static char interfaces__msg__Goal__FIELD_NAME__z[] = "z";

static rosidl_runtime_c__type_description__Field interfaces__msg__Goal__FIELDS[] = {
  {
    {interfaces__msg__Goal__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Goal__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Goal__FIELD_NAME__z, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
interfaces__msg__Goal__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {interfaces__msg__Goal__TYPE_NAME, 19, 19},
      {interfaces__msg__Goal__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int32 x\n"
  "int32 y\n"
  "int32 z";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
interfaces__msg__Goal__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {interfaces__msg__Goal__TYPE_NAME, 19, 19},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 23, 23},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
interfaces__msg__Goal__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *interfaces__msg__Goal__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
