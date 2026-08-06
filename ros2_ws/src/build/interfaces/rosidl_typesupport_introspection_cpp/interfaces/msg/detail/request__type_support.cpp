// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from interfaces:msg/Request.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "interfaces/msg/detail/request__functions.h"
#include "interfaces/msg/detail/request__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) interfaces::msg::Request(_init);
}

void Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<interfaces::msg::Request *>(message_memory);
  typed_message->~Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Request_message_member_array[2] = {
  {
    "img",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<interfaces::msg::ComboImage>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces::msg::Request, img),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "request",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces::msg::Request, request),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Request_message_members = {
  "interfaces::msg",  // message namespace
  "Request",  // message name
  2,  // number of fields
  sizeof(interfaces::msg::Request),
  false,  // has_any_key_member_
  Request_message_member_array,  // message members
  Request_init_function,  // function to initialize message memory (memory has to be allocated)
  Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Request_message_members,
  get_message_typesupport_handle_function,
  &interfaces__msg__Request__get_type_hash,
  &interfaces__msg__Request__get_type_description,
  &interfaces__msg__Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<interfaces::msg::Request>()
{
  return &::interfaces::msg::rosidl_typesupport_introspection_cpp::Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, interfaces, msg, Request)() {
  return &::interfaces::msg::rosidl_typesupport_introspection_cpp::Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
