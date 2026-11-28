#include "hal/crazyflie/connection.hpp"

#include <array>
#include <cstdio>
#include <cstring>
#include <stdexcept>

#include "Crazyradio.h"

namespace wut_control::hal::crazyflie {

namespace {

constexpr uint32_t kDefaultRadioDevId = 0;
constexpr uint8_t kMaxChannel = 125;
constexpr uint8_t kCrtpNullPacket = 0xFF;
constexpr uint8_t kScanAutoRetryCount = 1;

struct DatarateSpec {
    Crazyradio::Datarate rate;
    const char* label;
};

constexpr std::array<DatarateSpec, 3> kDatarates{{
    {Crazyradio::Datarate_2MPS, "2M"},
    {Crazyradio::Datarate_1MPS, "1M"},
    {Crazyradio::Datarate_250KPS, "250K"},
}};

struct ParsedRadioUri {
    uint32_t dev_id = 0;
    uint8_t channel = 0;
    Crazyradio::Datarate datarate = Crazyradio::Datarate_2MPS;
    const char* datarate_label = "2M";
    uint64_t address = 0xE7E7E7E7E7ULL;
};

std::optional<ParsedRadioUri> parseRadioUri(const std::string& uri) {
    unsigned int dev_id = 0;
    unsigned int channel = 0;
    int rate_num = 0;
    char rate_unit = 0;
    unsigned long long address = 0xE7E7E7E7E7ULL;

    const int matched = std::sscanf(uri.c_str(), "radio://%u/%u/%d%c/%llx", &dev_id, &channel,
                                    &rate_num, &rate_unit, &address);
    if (matched < 4 || channel > kMaxChannel) {
        return std::nullopt;
    }

    ParsedRadioUri parsed{};
    parsed.dev_id = dev_id;
    parsed.channel = static_cast<uint8_t>(channel);
    parsed.address = (matched == 5) ? static_cast<uint64_t>(address) : 0xE7E7E7E7E7ULL;

    if (rate_num == 2 && rate_unit == 'M') {
        parsed.datarate = Crazyradio::Datarate_2MPS;
        parsed.datarate_label = "2M";
    } else if (rate_num == 1 && rate_unit == 'M') {
        parsed.datarate = Crazyradio::Datarate_1MPS;
        parsed.datarate_label = "1M";
    } else if (rate_num == 250 && rate_unit == 'K') {
        parsed.datarate = Crazyradio::Datarate_250KPS;
        parsed.datarate_label = "250K";
    } else {
        return std::nullopt;
    }

    return parsed;
}

std::string formatRadioUri(uint32_t dev_id, uint8_t channel, const char* datarate_label,
                           uint64_t address) {
    std::array<char, 64> buffer{};
    std::snprintf(buffer.data(), buffer.size(), "radio://%u/%u/%s/%010llX", dev_id,
                  static_cast<unsigned>(channel), datarate_label,
                  static_cast<unsigned long long>(address));
    return std::string(buffer.data());
}

}  // namespace

CrazyflieConnection::~CrazyflieConnection() {
    disconnect();
}

bool CrazyflieConnection::pingRadioEndpoint(uint32_t dev_id, uint8_t channel,
                                            Crazyradio::Datarate datarate, uint64_t address) {
    bool acked = false;
    Crazyflie::withSharedRadio(static_cast<int>(dev_id), [&](Crazyradio& radio) {
        radio.setAddress(address);
        radio.setDatarate(datarate);
        radio.setChannel(channel);
        radio.setAckEnable(true);
        radio.setArc(kScanAutoRetryCount);

        ITransport::Ack ack{};
        radio.sendPacket(&kCrtpNullPacket, 1, ack);
        acked = ack.ack;
    });
    return acked;
}

std::vector<DroneInfo> CrazyflieConnection::scan(uint8_t start_channel, uint8_t end_channel,
                                                 uint64_t address) {
    if (start_channel > end_channel || end_channel > kMaxChannel) {
        throw std::invalid_argument("Invalid channel range (expected 0 <= start <= end <= 125)");
    }

    std::optional<std::string> cached_uri;
    {
        std::lock_guard<std::mutex> lock(mutex_);
        cached_uri = last_uri_;
    }

    try {
        if (cached_uri.has_value()) {
            const auto parsed = parseRadioUri(*cached_uri);
            if (parsed.has_value() && parsed->dev_id == kDefaultRadioDevId &&
                parsed->address == address && parsed->channel >= start_channel &&
                parsed->channel <= end_channel) {
                if (pingRadioEndpoint(parsed->dev_id, parsed->channel, parsed->datarate, address)) {
                    return {DroneInfo{
                        .uri = *cached_uri,
                        .channel = parsed->channel,
                        .address = address,
                    }};
                }
            }
        }

        std::vector<DroneInfo> found;
        for (const auto& dr : kDatarates) {
            for (uint16_t ch = start_channel; ch <= end_channel; ++ch) {
                const auto channel = static_cast<uint8_t>(ch);
                if (pingRadioEndpoint(kDefaultRadioDevId, channel, dr.rate, address)) {
                    const std::string uri =
                        formatRadioUri(kDefaultRadioDevId, channel, dr.label, address);
                    found.push_back(DroneInfo{
                        .uri = uri,
                        .channel = channel,
                        .address = address,
                    });
                }
            }
        }

        if (!found.empty()) {
            std::lock_guard<std::mutex> lock(mutex_);
            last_uri_ = found.front().uri;
        }

        return found;
    } catch (const std::exception&) {
        return {};
    }
}

void CrazyflieConnection::connect(const std::string& uri) {
    std::lock_guard<std::mutex> lock(mutex_);
    if (connected_.load()) {
        if (current_uri_ == uri) {
            return;
        }
        throw std::runtime_error("Already connected to another drone: " + current_uri_);
    }

    auto cf = std::make_unique<Crazyflie>(uri);
    cf->sendPing();
    cf->requestLogToc();
    cf->requestParamToc();

    cf_ = std::move(cf);
    current_uri_ = uri;
    last_uri_ = uri;
    connected_.store(true);
}

void CrazyflieConnection::disconnect() {
    std::lock_guard<std::mutex> lock(mutex_);
    cf_.reset();
    current_uri_.clear();
    connected_.store(false);
}

bool CrazyflieConnection::isConnected() const {
    return connected_.load();
}

std::optional<std::string> CrazyflieConnection::lastKnownUri() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return last_uri_;
}

    void CrazyflieConnection::withCrazyflie(const std::function<void(Crazyflie&)>& fn,
                                            bool require_connected) {
    std::lock_guard<std::mutex> lock(mutex_);
    if (!cf_) {
        if (require_connected) {
            throw std::runtime_error("Drone is not connected");
        }
        return;
    }

    if (require_connected && !connected_.load()) {
        throw std::runtime_error("Drone connection lost");
    }

    try {
        fn(*cf_);
    } catch (...) {
        connected_.store(false);
        if (require_connected) {
            throw;
        }
    }
}

}  // namespace wut_control::hal::crazyflie