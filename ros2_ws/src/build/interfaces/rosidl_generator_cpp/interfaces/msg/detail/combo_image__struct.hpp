// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/combo_image.hpp"


#ifndef INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'img_rgb'
// Member 'img_depth'
#include "sensor_msgs/msg/detail/image__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces__msg__ComboImage __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__ComboImage __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ComboImage_
{
  using Type = ComboImage_<ContainerAllocator>;

  explicit ComboImage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : img_rgb(_init),
    img_depth(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cx = 0.0;
      this->cy = 0.0;
      this->fx = 0.0;
      this->fy = 0.0;
    }
  }

  explicit ComboImage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : img_rgb(_alloc, _init),
    img_depth(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cx = 0.0;
      this->cy = 0.0;
      this->fx = 0.0;
      this->fy = 0.0;
    }
  }

  // field types and members
  using _cx_type =
    double;
  _cx_type cx;
  using _cy_type =
    double;
  _cy_type cy;
  using _fx_type =
    double;
  _fx_type fx;
  using _fy_type =
    double;
  _fy_type fy;
  using _img_rgb_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _img_rgb_type img_rgb;
  using _img_depth_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _img_depth_type img_depth;

  // setters for named parameter idiom
  Type & set__cx(
    const double & _arg)
  {
    this->cx = _arg;
    return *this;
  }
  Type & set__cy(
    const double & _arg)
  {
    this->cy = _arg;
    return *this;
  }
  Type & set__fx(
    const double & _arg)
  {
    this->fx = _arg;
    return *this;
  }
  Type & set__fy(
    const double & _arg)
  {
    this->fy = _arg;
    return *this;
  }
  Type & set__img_rgb(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->img_rgb = _arg;
    return *this;
  }
  Type & set__img_depth(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->img_depth = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::ComboImage_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::ComboImage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::ComboImage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::ComboImage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::ComboImage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::ComboImage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::ComboImage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::ComboImage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::ComboImage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::ComboImage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__ComboImage
    std::shared_ptr<interfaces::msg::ComboImage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__ComboImage
    std::shared_ptr<interfaces::msg::ComboImage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ComboImage_ & other) const
  {
    if (this->cx != other.cx) {
      return false;
    }
    if (this->cy != other.cy) {
      return false;
    }
    if (this->fx != other.fx) {
      return false;
    }
    if (this->fy != other.fy) {
      return false;
    }
    if (this->img_rgb != other.img_rgb) {
      return false;
    }
    if (this->img_depth != other.img_depth) {
      return false;
    }
    return true;
  }
  bool operator!=(const ComboImage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ComboImage_

// alias to use template instance with default allocator
using ComboImage =
  interfaces::msg::ComboImage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__COMBO_IMAGE__STRUCT_HPP_
