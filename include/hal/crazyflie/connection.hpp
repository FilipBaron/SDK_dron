#pragma once

#include <atomic>
#include <cstdint>
#include <functional>
#include <memory>
#include <mutex>
#include <optional>
#include <string>
#include <vector>

#include "Crazyflie.h"
#include "hal/types.hpp"

namespace wut_control::hal::crazyflie {

    class CrazyflieConnection final {
    public:
        CrazyflieConnection() = default;
        ~CrazyflieConnection();

        CrazyflieConnection(const CrazyflieConnection&) = delete;
        CrazyflieConnection& operator=(const CrazyflieConnection&) = delete;
        CrazyflieConnection(CrazyflieConnection&&) = delete;
        CrazyflieConnection& operator=(CrazyflieConnection&&) = delete;

        std::vector<DroneInfo> scan(uint8_t start_channel = 0, uint8_t end_channel = 125,
                                    uint64_t address = 0xE7E7E7E7E7ULL);
        void connect(const std::string& uri);
        void disconnect();
        [[nodiscard]] bool isConnected() const;
        [[nodiscard]] std::optional<std::string> lastKnownUri() const;

        void withCrazyflie(const std::function<void(Crazyflie&)>& fn, bool require_connected = true);

    private:
        static bool pingRadioEndpoint(uint32_t dev_id, uint8_t channel, Crazyradio::Datarate datarate,
                                      uint64_t address);

        mutable std::mutex mutex_;
        std::unique_ptr<Crazyflie> cf_;
        std::atomic<bool> connected_{false};
        std::string current_uri_;
        std::optional<std::string> last_uri_;
    };

}  // namespace wut_control::hal::crazyflie