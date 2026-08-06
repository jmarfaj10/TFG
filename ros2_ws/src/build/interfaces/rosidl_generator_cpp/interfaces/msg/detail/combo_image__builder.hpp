// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/combo_image.hpp"


#ifndef INTERFACES__MSG__DETAIL__COMBO_IMAGE__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__COMBO_IMAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/combo_image__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_ComboImage_img_depth
{
public:
  explicit Init_ComboImage_img_depth(::interfaces::msg::ComboImage & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::ComboImage img_depth(::interfaces::msg::ComboImage::_img_depth_type arg)
  {
    msg_.img_depth = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

class Init_ComboImage_img_rgb
{
public:
  explicit Init_ComboImage_img_rgb(::interfaces::msg::ComboImage & msg)
  : msg_(msg)
  {}
  Init_ComboImage_img_depth img_rgb(::interfaces::msg::ComboImage::_img_rgb_type arg)
  {
    msg_.img_rgb = std::move(arg);
    return Init_ComboImage_img_depth(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

class Init_ComboImage_fy
{
public:
  explicit Init_ComboImage_fy(::interfaces::msg::ComboImage & msg)
  : msg_(msg)
  {}
  Init_ComboImage_img_rgb fy(::interfaces::msg::ComboImage::_fy_type arg)
  {
    msg_.fy = std::move(arg);
    return Init_ComboImage_img_rgb(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

class Init_ComboImage_fx
{
public:
  explicit Init_ComboImage_fx(::interfaces::msg::ComboImage & msg)
  : msg_(msg)
  {}
  Init_ComboImage_fy fx(::interfaces::msg::ComboImage::_fx_type arg)
  {
    msg_.fx = std::move(arg);
    return Init_ComboImage_fy(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

class Init_ComboImage_cy
{
public:
  explicit Init_ComboImage_cy(::interfaces::msg::ComboImage & msg)
  : msg_(msg)
  {}
  Init_ComboImage_fx cy(::interfaces::msg::ComboImage::_cy_type arg)
  {
    msg_.cy = std::move(arg);
    return Init_ComboImage_fx(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

class Init_ComboImage_cx
{
public:
  Init_ComboImage_cx()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ComboImage_cy cx(::interfaces::msg::ComboImage::_cx_type arg)
  {
    msg_.cx = std::move(arg);
    return Init_ComboImage_cy(msg_);
  }

private:
  ::interfaces::msg::ComboImage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::ComboImage>()
{
  return interfaces::msg::builder::Init_ComboImage_cx();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__COMBO_IMAGE__BUILDER_HPP_
