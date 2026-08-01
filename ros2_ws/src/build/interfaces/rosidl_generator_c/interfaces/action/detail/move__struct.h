// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:action/Move.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/action/move.h"


#ifndef INTERFACES__ACTION__DETAIL__MOVE__STRUCT_H_
#define INTERFACES__ACTION__DETAIL__MOVE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_Goal
{
  float x_goal;
  float y_goal;
  float z_goal;
} interfaces__action__Move_Goal;

// Struct for a sequence of interfaces__action__Move_Goal.
typedef struct interfaces__action__Move_Goal__Sequence
{
  interfaces__action__Move_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_Goal__Sequence;

// Constants defined in the message

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_Result
{
  float distancia;
  float x;
  float y;
  float z;
} interfaces__action__Move_Result;

// Struct for a sequence of interfaces__action__Move_Result.
typedef struct interfaces__action__Move_Result__Sequence
{
  interfaces__action__Move_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_Result__Sequence;

// Constants defined in the message

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_Feedback
{
  float x_current;
  float y_current;
} interfaces__action__Move_Feedback;

// Struct for a sequence of interfaces__action__Move_Feedback.
typedef struct interfaces__action__Move_Feedback__Sequence
{
  interfaces__action__Move_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "interfaces/action/detail/move__struct.h"

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  interfaces__action__Move_Goal goal;
} interfaces__action__Move_SendGoal_Request;

// Struct for a sequence of interfaces__action__Move_SendGoal_Request.
typedef struct interfaces__action__Move_SendGoal_Request__Sequence
{
  interfaces__action__Move_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} interfaces__action__Move_SendGoal_Response;

// Struct for a sequence of interfaces__action__Move_SendGoal_Response.
typedef struct interfaces__action__Move_SendGoal_Response__Sequence
{
  interfaces__action__Move_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  interfaces__action__Move_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  interfaces__action__Move_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  interfaces__action__Move_SendGoal_Request__Sequence request;
  interfaces__action__Move_SendGoal_Response__Sequence response;
} interfaces__action__Move_SendGoal_Event;

// Struct for a sequence of interfaces__action__Move_SendGoal_Event.
typedef struct interfaces__action__Move_SendGoal_Event__Sequence
{
  interfaces__action__Move_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} interfaces__action__Move_GetResult_Request;

// Struct for a sequence of interfaces__action__Move_GetResult_Request.
typedef struct interfaces__action__Move_GetResult_Request__Sequence
{
  interfaces__action__Move_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "interfaces/action/detail/move__struct.h"

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_GetResult_Response
{
  int8_t status;
  interfaces__action__Move_Result result;
} interfaces__action__Move_GetResult_Response;

// Struct for a sequence of interfaces__action__Move_GetResult_Response.
typedef struct interfaces__action__Move_GetResult_Response__Sequence
{
  interfaces__action__Move_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  interfaces__action__Move_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  interfaces__action__Move_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  interfaces__action__Move_GetResult_Request__Sequence request;
  interfaces__action__Move_GetResult_Response__Sequence response;
} interfaces__action__Move_GetResult_Event;

// Struct for a sequence of interfaces__action__Move_GetResult_Event.
typedef struct interfaces__action__Move_GetResult_Event__Sequence
{
  interfaces__action__Move_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "interfaces/action/detail/move__struct.h"

/// Struct defined in action/Move in the package interfaces.
typedef struct interfaces__action__Move_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  interfaces__action__Move_Feedback feedback;
} interfaces__action__Move_FeedbackMessage;

// Struct for a sequence of interfaces__action__Move_FeedbackMessage.
typedef struct interfaces__action__Move_FeedbackMessage__Sequence
{
  interfaces__action__Move_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__action__Move_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__ACTION__DETAIL__MOVE__STRUCT_H_
