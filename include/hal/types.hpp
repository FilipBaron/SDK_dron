#pragma once

#include <cstdint>
#include <string>

namespace wut_control::hal {

struct Pose3D {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float yaw = 0.0f;
};

struct LidarReadings {
    float front = 0.0f;
    float back = 0.0f;
    float left = 0.0f;
    float right = 0.0f;
    float up = 0.0f;
    float down = 0.0f;
};

struct SensorStatus {
    bool imu_ok = false;
    bool flow_or_lighthouse_ok = false;
    bool multiranger_ok = false;
};

struct TelemetryState {
    Pose3D pose{};
    LidarReadings lidars{};
    SensorStatus sensors{};
    float battery_voltage = 0.0f;
    float battery_percentage = 0.0f;
    uint64_t last_ack_ms = 0;
};

struct DroneInfo {
    std::string uri;
    uint8_t channel = 0;
    uint64_t address = 0;
};

}  // namespace wut_control::hal