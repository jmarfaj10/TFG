// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from interfaces:msg/Response.idl
// generated code does not contain a copyright notice

#include "interfaces/msg/detail/response__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_interfaces
const rosidl_type_hash_t *
interfaces__msg__Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb6, 0x00, 0xe6, 0xcf, 0x19, 0xf9, 0x9e, 0x75,
      0xf6, 0x41, 0x9c, 0x03, 0x54, 0x6d, 0xef, 0xe9,
      0xed, 0x44, 0xad, 0x30, 0xcd, 0x2b, 0x3f, 0x8f,
      0xd1, 0xda, 0xbb, 0x98, 0x29, 0xb9, 0x40, 0x4a,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char interfaces__msg__Response__TYPE_NAME[] = "interfaces/msg/Response";

// Define type names, field names, and default values
static char interfaces__msg__Response__FIELD_NAME__response[] = "response";
static char interfaces__msg__Response__FIELD_NAME__object[] = "object";
static char interfaces__msg__Response__FIELD_NAME__x[] = "x";
static char interfaces__msg__Response__FIELD_NAME__y[] = "y";
static char interfaces__msg__Response__FIELD_NAME__z[] = "z";

static rosidl_runtime_c__type_description__Field interfaces__msg__Response__FIELDS[] = {
  {
    {interfaces__msg__Response__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Response__FIELD_NAME__object, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Response__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Response__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {interfaces__msg__Response__FIELD_NAME__z, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
interfaces__msg__Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {interfaces__msg__Response__TYPE_NAME, 23, 23},
      {interfaces__msg__Response__FIELDS, 5, 5},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string response\n"
  "string object\n"
  "float32 x\n"
  "float32 y\n"
  "float32 z\n"
  "";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
interfaces__msg__Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {interfaces__msg__Response__TYPE_NAME, 23, 23},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 61, 61},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
interfaces__msg__Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *interfaces__msg__Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
