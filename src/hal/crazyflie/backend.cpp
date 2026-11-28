// src/hal/backend.cpp
#include "../../../include/hal/crazyflie/backend.hpp"

#include <stdexcept>

namespace wut_control::hal {

    std::vector<DroneInfo> CrazyflieBackend::scan(uint8_t start_channel, uint8_t end_channel,
                                                  uint64_t address) {
        return connection_.scan(start_channel, end_channel, address);
    }

    void CrazyflieBackend::connect(const std::string& uri) {
        connection_.connect(uri);
    }

    void CrazyflieBackend::disconnect() {
        connection_.disconnect();
    }

    bool CrazyflieBackend::isConnected() const {
        return connection_.isConnected();
    }

    void CrazyflieBackend::startMotors() {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::stopMotors() {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::emergencyStop() {
        connection_.withCrazyflie([](Crazyflie& cf) { cf.emergencyStop(); },
                                  /*require_connected=*/false);
    }

    void CrazyflieBackend::stopAndHover() {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::takeoff(float /*target_height*/, float /*velocity*/) {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::land(float /*velocity*/) {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::goToPosition(float /*x*/, float /*y*/, float /*z*/, float /*yaw*/,
                                        float /*velocity*/) {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::moveByVector(float /*dx*/, float /*dy*/, float /*dz*/, float /*dyaw*/,
                                        float /*velocity*/) {
        throw std::logic_error("Not implemented yet");
    }

    void CrazyflieBackend::rotate(float /*degrees*/, float /*angular_velocity*/) {
        throw std::logic_error("Not implemented yet");
    }

    TelemetryState CrazyflieBackend::getTelemetry() const {
        return TelemetryState{};
    }

}  // namespace wut_control::hal