// include/hal/crazyflie/backend.hpp
#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "hal/crazyflie/connection.hpp"
#include "hal/i_drone_backend.hpp"

namespace wut_control::hal {

    class CrazyflieBackend final : public IDroneBackend {
    public:
        CrazyflieBackend() = default;
        ~CrazyflieBackend() override = default;

        CrazyflieBackend(const CrazyflieBackend&) = delete;
        CrazyflieBackend& operator=(const CrazyflieBackend&) = delete;
        CrazyflieBackend(CrazyflieBackend&&) = delete;
        CrazyflieBackend& operator=(CrazyflieBackend&&) = delete;

        std::vector<DroneInfo> scan(uint8_t start_channel = 0, uint8_t end_channel = 125,
                                    uint64_t address = 0xE7E7E7E7E7ULL) override;
        void connect(const std::string& uri) override;
        void disconnect() override;
        [[nodiscard]] bool isConnected() const override;

        void startMotors() override;
        void stopMotors() override;
        void emergencyStop() override;
        void stopAndHover() override;

        void takeoff(float target_height, float velocity = 0.2f) override;
        void land(float velocity = 0.2f) override;
        void goToPosition(float x, float y, float z, float yaw, float velocity = 0.2f) override;
        void moveByVector(float dx, float dy, float dz, float dyaw, float velocity = 0.2f) override;
        void rotate(float degrees, float angular_velocity = 50.0f) override;

        [[nodiscard]] TelemetryState getTelemetry() const override;

    private:
        crazyflie::CrazyflieConnection connection_;
        // crazyflie::CrazyflieMotors motors_{connection_};
        // crazyflie::CrazyflieFlight flight_{connection_};
        // crazyflie::CrazyflieTelemetry telemetry_{connection_};
    };

}  // namespace wut_control::hal