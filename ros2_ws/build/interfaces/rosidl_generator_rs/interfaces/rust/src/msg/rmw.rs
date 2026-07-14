#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Goal() -> *const std::ffi::c_void;
}

#[link(name = "interfaces__rosidl_generator_c")]
extern "C" {
    fn interfaces__msg__Goal__init(msg: *mut Goal) -> bool;
    fn interfaces__msg__Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Goal>, size: usize) -> bool;
    fn interfaces__msg__Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Goal>);
    fn interfaces__msg__Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<Goal>) -> bool;
}

// Corresponds to interfaces__msg__Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: i32,

}



impl Default for Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces__msg__Goal__init(&mut msg as *mut _) {
        panic!("Call to interfaces__msg__Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Goal where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces/msg/Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Goal() }
  }
}


#[link(name = "interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__ComboImage() -> *const std::ffi::c_void;
}

#[link(name = "interfaces__rosidl_generator_c")]
extern "C" {
    fn interfaces__msg__ComboImage__init(msg: *mut ComboImage) -> bool;
    fn interfaces__msg__ComboImage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ComboImage>, size: usize) -> bool;
    fn interfaces__msg__ComboImage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ComboImage>);
    fn interfaces__msg__ComboImage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ComboImage>, out_seq: *mut rosidl_runtime_rs::Sequence<ComboImage>) -> bool;
}

// Corresponds to interfaces__msg__ComboImage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ComboImage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub cx: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub cy: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fx: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fy: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_rgb: sensor_msgs::msg::rmw::Image,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_depth: sensor_msgs::msg::rmw::Image,

}



impl Default for ComboImage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces__msg__ComboImage__init(&mut msg as *mut _) {
        panic!("Call to interfaces__msg__ComboImage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ComboImage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__ComboImage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__ComboImage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__ComboImage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ComboImage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ComboImage where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces/msg/ComboImage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__ComboImage() }
  }
}


#[link(name = "interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Request() -> *const std::ffi::c_void;
}

#[link(name = "interfaces__rosidl_generator_c")]
extern "C" {
    fn interfaces__msg__Request__init(msg: *mut Request) -> bool;
    fn interfaces__msg__Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Request>, size: usize) -> bool;
    fn interfaces__msg__Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Request>);
    fn interfaces__msg__Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Request>) -> bool;
}

// Corresponds to interfaces__msg__Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub img: super::super::msg::rmw::ComboImage,


    // This member is not documented.
    #[allow(missing_docs)]
    pub request: rosidl_runtime_rs::String,

}



impl Default for Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces__msg__Request__init(&mut msg as *mut _) {
        panic!("Call to interfaces__msg__Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Request where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces/msg/Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Request() }
  }
}


#[link(name = "interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Response() -> *const std::ffi::c_void;
}

#[link(name = "interfaces__rosidl_generator_c")]
extern "C" {
    fn interfaces__msg__Response__init(msg: *mut Response) -> bool;
    fn interfaces__msg__Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Response>, size: usize) -> bool;
    fn interfaces__msg__Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Response>);
    fn interfaces__msg__Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Response>) -> bool;
}

// Corresponds to interfaces__msg__Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub response: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,

}



impl Default for Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !interfaces__msg__Response__init(&mut msg as *mut _) {
        panic!("Call to interfaces__msg__Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { interfaces__msg__Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Response where Self: Sized {
  const TYPE_NAME: &'static str = "interfaces/msg/Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__interfaces__msg__Response() }
  }
}


