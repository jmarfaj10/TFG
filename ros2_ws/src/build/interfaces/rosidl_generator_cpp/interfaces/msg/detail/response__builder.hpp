// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Response.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/response.hpp"


#ifndef INTERFACES__MSG__DETAIL__RESPONSE__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__RESPONSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/response__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Response_z
{
public:
  explicit Init_Response_z(::interfaces::msg::Response & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Response z(::interfaces::msg::Response::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Response msg_;
};

class Init_Response_y
{
public:
  explicit Init_Response_y(::interfaces::msg::Response & msg)
  : msg_(msg)
  {}
  Init_Response_z y(::interfaces::msg::Response::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Response_z(msg_);
  }

private:
  ::interfaces::msg::Response msg_;
};

class Init_Response_x
{
public:
  explicit Init_Response_x(::interfaces::msg::Response & msg)
  : msg_(msg)
  {}
  Init_Response_y x(::interfaces::msg::Response::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Response_y(msg_);
  }

private:
  ::interfaces::msg::Response msg_;
};

class Init_Response_object
{
public:
  explicit Init_Response_object(::interfaces::msg::Response & msg)
  : msg_(msg)
  {}
  Init_Response_x object(::interfaces::msg::Response::_object_type arg)
  {
    msg_.object = std::move(arg);
    return Init_Response_x(msg_);
  }

private:
  ::interfaces::msg::Response msg_;
};

class Init_Response_response
{
public:
  Init_Response_response()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Response_object response(::interfaces::msg::Response::_response_type arg)
  {
    msg_.response = std::move(arg);
    return Init_Response_object(msg_);
  }

private:
  ::interfaces::msg::Response msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Response>()
{
  return interfaces::msg::builder::Init_Response_response();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__RESPONSE__BUILDER_HPP_
