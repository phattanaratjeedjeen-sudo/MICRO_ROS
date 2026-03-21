#include <Arduino.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

// Global micro-ROS objects
rcl_node_t node;
rclc_support_t support;
rcl_allocator_t allocator;

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  pinMode(2, OUTPUT); // GPIO2 for LED on ESP32

  allocator = rcl_get_default_allocator();

  // Create init_options
  rclc_support_init(&support, 0, NULL, &allocator);

  // Create node (This is the part from your tutorial link)
  const char * node_name = "hardware_control_node";
  const char * node_namespace = ""; 
  rclc_node_init_default(&node, node_name, node_namespace, &support);
}

void loop() {
  digitalWrite(2, HIGH); // Turn the LED on
  delay(1000); // Wait for a second
  digitalWrite(2, LOW); // Turn the LED off
  delay(1000); // Wait for a second
}

