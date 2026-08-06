// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/combo_image.hpp"


#ifndef INTERFACES__MSG__DETAIL__COMBO_IMAGE__TRAITS_HPP_
#define INTERFACES__MSG__DETAIL__COMBO_IMAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces/msg/detail/combo_image__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'img_rgb'
// Member 'img_depth'
#include "sensor_msgs/msg/detail/image__traits.hpp"

namespace interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ComboImage & msg,
  std::ostream & out)
{
  out << "{";
  // member: cx
  {
    out << "cx: ";
    rosidl_generator_traits::value_to_yaml(msg.cx, out);
    out << ", ";
  }

  // member: cy
  {
    out << "cy: ";
    rosidl_generator_traits::value_to_yaml(msg.cy, out);
    out << ", ";
  }

  // member: fx
  {
    out << "fx: ";
    rosidl_generator_traits::value_to_yaml(msg.fx, out);
    out << ", ";
  }

  // member: fy
  {
    out << "fy: ";
    rosidl_generator_traits::value_to_yaml(msg.fy, out);
    out << ", ";
  }

  // member: img_rgb
  {
    out << "img_rgb: ";
    to_flow_style_yaml(msg.img_rgb, out);
    out << ", ";
  }

  // member: img_depth
  {
    out << "img_depth: ";
    to_flow_style_yaml(msg.img_depth, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ComboImage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cx: ";
    rosidl_generator_traits::value_to_yaml(msg.cx, out);
    out << "\n";
  }

  // member: cy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cy: ";
    rosidl_generator_traits::value_to_yaml(msg.cy, out);
    out << "\n";
  }

  // member: fx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fx: ";
    rosidl_generator_traits::value_to_yaml(msg.fx, out);
    out << "\n";
  }

  // member: fy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fy: ";
    rosidl_generator_traits::value_to_yaml(msg.fy, out);
    out << "\n";
  }

  // member: img_rgb
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_rgb:\n";
    to_block_style_yaml(msg.img_rgb, out, indentation + 2);
  }

  // member: img_depth
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "img_depth:\n";
    to_block_style_yaml(msg.img_depth, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ComboImage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace interfaces

namespace rosidl_generator_traits
{

[[deprecated("use interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces::msg::ComboImage & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const interfaces::msg::ComboImage & msg)
{
  return interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces::msg::ComboImage>()
{
  return "interfaces::msg::ComboImage";
}

template<>
inline const char * name<interfaces::msg::ComboImage>()
{
  return "interfaces/msg/ComboImage";
}

template<>
struct has_fixed_size<interfaces::msg::ComboImage>
  : std::integral_constant<bool, has_fixed_size<sensor_msgs::msg::Image>::value> {};

template<>
struct has_bounded_size<interfaces::msg::ComboImage>
  : std::integral_constant<bool, has_bounded_size<sensor_msgs::msg::Image>::value> {};

template<>
struct is_message<interfaces::msg::ComboImage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__MSG__DETAIL__COMBO_IMAGE__TRAITS_HPP_
