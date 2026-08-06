// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces:msg/ComboImage.idl
// generated code does not contain a copyright notice
#include "interfaces/msg/detail/combo_image__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `img_rgb`
// Member `img_depth`
#include "sensor_msgs/msg/detail/image__functions.h"

bool
interfaces__msg__ComboImage__init(interfaces__msg__ComboImage * msg)
{
  if (!msg) {
    return false;
  }
  // cx
  // cy
  // fx
  // fy
  // img_rgb
  if (!sensor_msgs__msg__Image__init(&msg->img_rgb)) {
    interfaces__msg__ComboImage__fini(msg);
    return false;
  }
  // img_depth
  if (!sensor_msgs__msg__Image__init(&msg->img_depth)) {
    interfaces__msg__ComboImage__fini(msg);
    return false;
  }
  return true;
}

void
interfaces__msg__ComboImage__fini(interfaces__msg__ComboImage * msg)
{
  if (!msg) {
    return;
  }
  // cx
  // cy
  // fx
  // fy
  // img_rgb
  sensor_msgs__msg__Image__fini(&msg->img_rgb);
  // img_depth
  sensor_msgs__msg__Image__fini(&msg->img_depth);
}

bool
interfaces__msg__ComboImage__are_equal(const interfaces__msg__ComboImage * lhs, const interfaces__msg__ComboImage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // cx
  if (lhs->cx != rhs->cx) {
    return false;
  }
  // cy
  if (lhs->cy != rhs->cy) {
    return false;
  }
  // fx
  if (lhs->fx != rhs->fx) {
    return false;
  }
  // fy
  if (lhs->fy != rhs->fy) {
    return false;
  }
  // img_rgb
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->img_rgb), &(rhs->img_rgb)))
  {
    return false;
  }
  // img_depth
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->img_depth), &(rhs->img_depth)))
  {
    return false;
  }
  return true;
}

bool
interfaces__msg__ComboImage__copy(
  const interfaces__msg__ComboImage * input,
  interfaces__msg__ComboImage * output)
{
  if (!input || !output) {
    return false;
  }
  // cx
  output->cx = input->cx;
  // cy
  output->cy = input->cy;
  // fx
  output->fx = input->fx;
  // fy
  output->fy = input->fy;
  // img_rgb
  if (!sensor_msgs__msg__Image__copy(
      &(input->img_rgb), &(output->img_rgb)))
  {
    return false;
  }
  // img_depth
  if (!sensor_msgs__msg__Image__copy(
      &(input->img_depth), &(output->img_depth)))
  {
    return false;
  }
  return true;
}

interfaces__msg__ComboImage *
interfaces__msg__ComboImage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__ComboImage * msg = (interfaces__msg__ComboImage *)allocator.allocate(sizeof(interfaces__msg__ComboImage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces__msg__ComboImage));
  bool success = interfaces__msg__ComboImage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces__msg__ComboImage__destroy(interfaces__msg__ComboImage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces__msg__ComboImage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces__msg__ComboImage__Sequence__init(interfaces__msg__ComboImage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__ComboImage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(interfaces__msg__ComboImage)) {
      return false;
    }
    data = (interfaces__msg__ComboImage *)allocator.zero_allocate(size, sizeof(interfaces__msg__ComboImage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces__msg__ComboImage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces__msg__ComboImage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
interfaces__msg__ComboImage__Sequence__fini(interfaces__msg__ComboImage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      interfaces__msg__ComboImage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

interfaces__msg__ComboImage__Sequence *
interfaces__msg__ComboImage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces__msg__ComboImage__Sequence * array = (interfaces__msg__ComboImage__Sequence *)allocator.allocate(sizeof(interfaces__msg__ComboImage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces__msg__ComboImage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces__msg__ComboImage__Sequence__destroy(interfaces__msg__ComboImage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces__msg__ComboImage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces__msg__ComboImage__Sequence__are_equal(const interfaces__msg__ComboImage__Sequence * lhs, const interfaces__msg__ComboImage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces__msg__ComboImage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces__msg__ComboImage__Sequence__copy(
  const interfaces__msg__ComboImage__Sequence * input,
  interfaces__msg__ComboImage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(interfaces__msg__ComboImage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(interfaces__msg__ComboImage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces__msg__ComboImage * data =
      (interfaces__msg__ComboImage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces__msg__ComboImage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces__msg__ComboImage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces__msg__ComboImage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
