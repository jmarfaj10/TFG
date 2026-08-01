// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Goal.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/goal.hpp"


#ifndef INTERFACES__MSG__DETAIL__GOAL__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__GOAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/goal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Goal_z
{
public:
  explicit Init_Goal_z(::interfaces::msg::Goal & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Goal z(::interfaces::msg::Goal::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Goal msg_;
};

class Init_Goal_y
{
public:
  explicit Init_Goal_y(::interfaces::msg::Goal & msg)
  : msg_(msg)
  {}
  Init_Goal_z y(::interfaces::msg::Goal::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Goal_z(msg_);
  }

private:
  ::interfaces::msg::Goal msg_;
};

class Init_Goal_x
{
public:
  Init_Goal_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Goal_y x(::interfaces::msg::Goal::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Goal_y(msg_);
  }

private:
  ::interfaces::msg::Goal msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Goal>()
{
  return interfaces::msg::builder::Init_Goal_x();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__GOAL__BUILDER_HPP_
