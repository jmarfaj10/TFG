// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Request.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/request.hpp"


#ifndef INTERFACES__MSG__DETAIL__REQUEST__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Request_request
{
public:
  explicit Init_Request_request(::interfaces::msg::Request & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Request request(::interfaces::msg::Request::_request_type arg)
  {
    msg_.request = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Request msg_;
};

class Init_Request_img
{
public:
  Init_Request_img()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Request_request img(::interfaces::msg::Request::_img_type arg)
  {
    msg_.img = std::move(arg);
    return Init_Request_request(msg_);
  }

private:
  ::interfaces::msg::Request msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Request>()
{
  return interfaces::msg::builder::Init_Request_img();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__REQUEST__BUILDER_HPP_
