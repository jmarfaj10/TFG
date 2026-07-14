// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:action/Move.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/action/move.hpp"


#ifndef INTERFACES__ACTION__DETAIL__MOVE__BUILDER_HPP_
#define INTERFACES__ACTION__DETAIL__MOVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/action/detail/move__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_Goal_z_goal
{
public:
  explicit Init_Move_Goal_z_goal(::interfaces::action::Move_Goal & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_Goal z_goal(::interfaces::action::Move_Goal::_z_goal_type arg)
  {
    msg_.z_goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_Goal msg_;
};

class Init_Move_Goal_y_goal
{
public:
  explicit Init_Move_Goal_y_goal(::interfaces::action::Move_Goal & msg)
  : msg_(msg)
  {}
  Init_Move_Goal_z_goal y_goal(::interfaces::action::Move_Goal::_y_goal_type arg)
  {
    msg_.y_goal = std::move(arg);
    return Init_Move_Goal_z_goal(msg_);
  }

private:
  ::interfaces::action::Move_Goal msg_;
};

class Init_Move_Goal_x_goal
{
public:
  Init_Move_Goal_x_goal()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_Goal_y_goal x_goal(::interfaces::action::Move_Goal::_x_goal_type arg)
  {
    msg_.x_goal = std::move(arg);
    return Init_Move_Goal_y_goal(msg_);
  }

private:
  ::interfaces::action::Move_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_Goal>()
{
  return interfaces::action::builder::Init_Move_Goal_x_goal();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_Result_z
{
public:
  explicit Init_Move_Result_z(::interfaces::action::Move_Result & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_Result z(::interfaces::action::Move_Result::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_Result msg_;
};

class Init_Move_Result_y
{
public:
  explicit Init_Move_Result_y(::interfaces::action::Move_Result & msg)
  : msg_(msg)
  {}
  Init_Move_Result_z y(::interfaces::action::Move_Result::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Move_Result_z(msg_);
  }

private:
  ::interfaces::action::Move_Result msg_;
};

class Init_Move_Result_x
{
public:
  explicit Init_Move_Result_x(::interfaces::action::Move_Result & msg)
  : msg_(msg)
  {}
  Init_Move_Result_y x(::interfaces::action::Move_Result::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Move_Result_y(msg_);
  }

private:
  ::interfaces::action::Move_Result msg_;
};

class Init_Move_Result_distancia
{
public:
  Init_Move_Result_distancia()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_Result_x distancia(::interfaces::action::Move_Result::_distancia_type arg)
  {
    msg_.distancia = std::move(arg);
    return Init_Move_Result_x(msg_);
  }

private:
  ::interfaces::action::Move_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_Result>()
{
  return interfaces::action::builder::Init_Move_Result_distancia();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_Feedback_y_current
{
public:
  explicit Init_Move_Feedback_y_current(::interfaces::action::Move_Feedback & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_Feedback y_current(::interfaces::action::Move_Feedback::_y_current_type arg)
  {
    msg_.y_current = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_Feedback msg_;
};

class Init_Move_Feedback_x_current
{
public:
  Init_Move_Feedback_x_current()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_Feedback_y_current x_current(::interfaces::action::Move_Feedback::_x_current_type arg)
  {
    msg_.x_current = std::move(arg);
    return Init_Move_Feedback_y_current(msg_);
  }

private:
  ::interfaces::action::Move_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_Feedback>()
{
  return interfaces::action::builder::Init_Move_Feedback_x_current();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_SendGoal_Request_goal
{
public:
  explicit Init_Move_SendGoal_Request_goal(::interfaces::action::Move_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_SendGoal_Request goal(::interfaces::action::Move_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Request msg_;
};

class Init_Move_SendGoal_Request_goal_id
{
public:
  Init_Move_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_SendGoal_Request_goal goal_id(::interfaces::action::Move_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Move_SendGoal_Request_goal(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_SendGoal_Request>()
{
  return interfaces::action::builder::Init_Move_SendGoal_Request_goal_id();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_SendGoal_Response_stamp
{
public:
  explicit Init_Move_SendGoal_Response_stamp(::interfaces::action::Move_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_SendGoal_Response stamp(::interfaces::action::Move_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Response msg_;
};

class Init_Move_SendGoal_Response_accepted
{
public:
  Init_Move_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_SendGoal_Response_stamp accepted(::interfaces::action::Move_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Move_SendGoal_Response_stamp(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_SendGoal_Response>()
{
  return interfaces::action::builder::Init_Move_SendGoal_Response_accepted();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_SendGoal_Event_response
{
public:
  explicit Init_Move_SendGoal_Event_response(::interfaces::action::Move_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_SendGoal_Event response(::interfaces::action::Move_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Event msg_;
};

class Init_Move_SendGoal_Event_request
{
public:
  explicit Init_Move_SendGoal_Event_request(::interfaces::action::Move_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_Move_SendGoal_Event_response request(::interfaces::action::Move_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Move_SendGoal_Event_response(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Event msg_;
};

class Init_Move_SendGoal_Event_info
{
public:
  Init_Move_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_SendGoal_Event_request info(::interfaces::action::Move_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Move_SendGoal_Event_request(msg_);
  }

private:
  ::interfaces::action::Move_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_SendGoal_Event>()
{
  return interfaces::action::builder::Init_Move_SendGoal_Event_info();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_GetResult_Request_goal_id
{
public:
  Init_Move_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::action::Move_GetResult_Request goal_id(::interfaces::action::Move_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_GetResult_Request>()
{
  return interfaces::action::builder::Init_Move_GetResult_Request_goal_id();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_GetResult_Response_result
{
public:
  explicit Init_Move_GetResult_Response_result(::interfaces::action::Move_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_GetResult_Response result(::interfaces::action::Move_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Response msg_;
};

class Init_Move_GetResult_Response_status
{
public:
  Init_Move_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_GetResult_Response_result status(::interfaces::action::Move_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Move_GetResult_Response_result(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_GetResult_Response>()
{
  return interfaces::action::builder::Init_Move_GetResult_Response_status();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_GetResult_Event_response
{
public:
  explicit Init_Move_GetResult_Event_response(::interfaces::action::Move_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_GetResult_Event response(::interfaces::action::Move_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Event msg_;
};

class Init_Move_GetResult_Event_request
{
public:
  explicit Init_Move_GetResult_Event_request(::interfaces::action::Move_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_Move_GetResult_Event_response request(::interfaces::action::Move_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Move_GetResult_Event_response(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Event msg_;
};

class Init_Move_GetResult_Event_info
{
public:
  Init_Move_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_GetResult_Event_request info(::interfaces::action::Move_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Move_GetResult_Event_request(msg_);
  }

private:
  ::interfaces::action::Move_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_GetResult_Event>()
{
  return interfaces::action::builder::Init_Move_GetResult_Event_info();
}

}  // namespace interfaces


namespace interfaces
{

namespace action
{

namespace builder
{

class Init_Move_FeedbackMessage_feedback
{
public:
  explicit Init_Move_FeedbackMessage_feedback(::interfaces::action::Move_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::interfaces::action::Move_FeedbackMessage feedback(::interfaces::action::Move_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::action::Move_FeedbackMessage msg_;
};

class Init_Move_FeedbackMessage_goal_id
{
public:
  Init_Move_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Move_FeedbackMessage_feedback goal_id(::interfaces::action::Move_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Move_FeedbackMessage_feedback(msg_);
  }

private:
  ::interfaces::action::Move_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::action::Move_FeedbackMessage>()
{
  return interfaces::action::builder::Init_Move_FeedbackMessage_goal_id();
}

}  // namespace interfaces

#endif  // INTERFACES__ACTION__DETAIL__MOVE__BUILDER_HPP_
