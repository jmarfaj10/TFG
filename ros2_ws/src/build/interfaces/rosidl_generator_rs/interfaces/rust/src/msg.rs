#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to interfaces__msg__Goal

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Goal::default())
  }
}

impl rosidl_runtime_rs::Message for Goal {
  type RmwMsg = super::msg::rmw::Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
    }
  }
}


// Corresponds to interfaces__msg__ComboImage

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub img_rgb: sensor_msgs::msg::Image,


    // This member is not documented.
    #[allow(missing_docs)]
    pub img_depth: sensor_msgs::msg::Image,

}



impl Default for ComboImage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ComboImage::default())
  }
}

impl rosidl_runtime_rs::Message for ComboImage {
  type RmwMsg = super::msg::rmw::ComboImage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        cx: msg.cx,
        cy: msg.cy,
        fx: msg.fx,
        fy: msg.fy,
        img_rgb: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Owned(msg.img_rgb)).into_owned(),
        img_depth: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Owned(msg.img_depth)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      cx: msg.cx,
      cy: msg.cy,
      fx: msg.fx,
      fy: msg.fy,
        img_rgb: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Borrowed(&msg.img_rgb)).into_owned(),
        img_depth: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Borrowed(&msg.img_depth)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      cx: msg.cx,
      cy: msg.cy,
      fx: msg.fx,
      fy: msg.fy,
      img_rgb: sensor_msgs::msg::Image::from_rmw_message(msg.img_rgb),
      img_depth: sensor_msgs::msg::Image::from_rmw_message(msg.img_depth),
    }
  }
}


// Corresponds to interfaces__msg__Request

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub img: super::msg::ComboImage,


    // This member is not documented.
    #[allow(missing_docs)]
    pub request: std::string::String,

}



impl Default for Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Request::default())
  }
}

impl rosidl_runtime_rs::Message for Request {
  type RmwMsg = super::msg::rmw::Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        img: super::msg::ComboImage::into_rmw_message(std::borrow::Cow::Owned(msg.img)).into_owned(),
        request: msg.request.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        img: super::msg::ComboImage::into_rmw_message(std::borrow::Cow::Borrowed(&msg.img)).into_owned(),
        request: msg.request.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      img: super::msg::ComboImage::from_rmw_message(msg.img),
      request: msg.request.to_string(),
    }
  }
}


// Corresponds to interfaces__msg__Response

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub response: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object: std::string::String,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Response::default())
  }
}

impl rosidl_runtime_rs::Message for Response {
  type RmwMsg = super::msg::rmw::Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        response: msg.response.as_str().into(),
        object: msg.object.as_str().into(),
        x: msg.x,
        y: msg.y,
        z: msg.z,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        response: msg.response.as_str().into(),
        object: msg.object.as_str().into(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      response: msg.response.to_string(),
      object: msg.object.to_string(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
    }
  }
}


