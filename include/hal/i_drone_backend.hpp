#pragma once

#include <string>
#include <vector>

#include "hal/types.hpp"

namespace wut_control::hal {

class IDroneBackend {
public:
    virtual ~IDroneBackend() = default;

    virtual std::vector<DroneInfo> scan(uint8_t start_channel = 0, uint8_t end_channel = 125,
                                        uint64_t address = 0xE7E7E7E7E7ULL) = 0;
    virtual void connect(const std::string& uri) = 0;
    virtual void disconnect() = 0;
    [[nodiscard]] virtual bool isConnected() const = 0;

    virtual void startMotors() = 0;
    virtual void stopMotors() = 0;
    virtual void emergencyStop() = 0;
    virtual void stopAndHover() = 0;

    virtual void takeoff(float target_height, float velocity = 0.2f) = 0;
    virtual void land(float velocity = 0.2f) = 0;
    virtual void goToPosition(float x, float y, float z, float yaw, float velocity = 0.2f) = 0;
    virtual void moveByVector(float dx, float dy, float dz, float dyaw, float velocity = 0.2f) = 0;
    virtual void rotate(float degrees, float angular_velocity = 50.0f) = 0;

    [[nodiscard]] virtual TelemetryState getTelemetry() const = 0;
};

}  // namespace wut_control::hal