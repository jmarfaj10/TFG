// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/Request.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/request.hpp"


#ifndef INTERFACES__MSG__DETAIL__REQUEST__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__REQUEST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'img'
#include "interfaces/msg/detail/combo_image__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces__msg__Request __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__Request __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Request_
{
  using Type = Request_<ContainerAllocator>;

  explicit Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : img(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->request = "";
    }
  }

  explicit Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : img(_alloc, _init),
    request(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->request = "";
    }
  }

  // field types and members
  using _img_type =
    interfaces::msg::ComboImage_<ContainerAllocator>;
  _img_type img;
  using _request_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _request_type request;

  // setters for named parameter idiom
  Type & set__img(
    const interfaces::msg::ComboImage_<ContainerAllocator> & _arg)
  {
    this->img = _arg;
    return *this;
  }
  Type & set__request(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->request = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__Request
    std::shared_ptr<interfaces::msg::Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__Request
    std::shared_ptr<interfaces::msg::Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Request_ & other) const
  {
    if (this->img != other.img) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    return true;
  }
  bool operator!=(const Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Request_

// alias to use template instance with default allocator
using Request =
  interfaces::msg::Request_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__REQUEST__STRUCT_HPP_
