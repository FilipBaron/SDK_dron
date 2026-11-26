cmake_minimum_required(VERSION 3.16)
project(wut_control LANGUAGES CXX C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_compile_definitions(_USE_MATH_DEFINES)

find_package(Threads REQUIRED)

include(FetchContent)

FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG        v2.12.0
)
FetchContent_MakeAvailable(pybind11)

find_package(libusb CONFIG QUIET)
if(NOT libusb_FOUND)
    FetchContent_Declare(
            libusb_cmake
            GIT_REPOSITORY https://github.com/libusb/libusb-cmake.git
            GIT_TAG        v1.0.27-0
    )
    FetchContent_MakeAvailable(libusb_cmake)
    add_library(libusb::libusb ALIAS usb-1.0)

    file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/generated_include/libusb-1.0")
    file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/generated_include/libusb-1.0/libusb.h"
            "#include \"${libusb_cmake_SOURCE_DIR}/libusb/libusb/libusb.h\"\n")
endif()

add_library(crazyflie_cpp STATIC
        third_party/crazyflie_cpp/src/Crazyflie.cpp
        third_party/crazyflie_cpp/src/CrazyflieUSB.cpp
        third_party/crazyflie_cpp/src/Crazyradio.cpp
        third_party/crazyflie_cpp/src/crtp.cpp
        third_party/crazyflie_cpp/src/ITransport.cpp
        third_party/crazyflie_cpp/src/USBDevice.cpp
)
target_include_directories(crazyflie_cpp PUBLIC
        third_party/crazyflie_cpp/include
        third_party/crazyflie_cpp/include/crazyflie_cpp
        "${CMAKE_CURRENT_BINARY_DIR}/generated_include"
)
target_link_libraries(crazyflie_cpp PUBLIC
        libusb::libusb
        Threads::Threads
)

if(MSVC)
    target_compile_options(crazyflie_cpp PRIVATE
            /FI"${CMAKE_CURRENT_SOURCE_DIR}/third_party/crazyflie_cpp/msvc_compat.h"
            /wd4103
    )
endif()

file(GLOB_RECURSE WUT_SDK_SOURCES CONFIGURE_DEPENDS
        "src/core/*.cpp"
        "src/backends/*.cpp"
)
add_library(wut_sdk_core STATIC ${WUT_SDK_SOURCES})
target_include_directories(wut_sdk_core PUBLIC
        include
)
target_link_libraries(wut_sdk_core PUBLIC
        crazyflie_cpp
)

if(MSVC)
    target_compile_options(wut_sdk_core PRIVATE /W4)
else()
    target_compile_options(wut_sdk_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

pybind11_add_module(_core src/bindings/bindings.cpp)
target_link_libraries(_core PRIVATE wut_sdk_core)

if(MINGW)
    target_link_options(_core PRIVATE -static-libgcc -static-libstdc++ -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive)
endif()

if(MSVC)
    target_compile_options(_core PRIVATE /W4)
else()
    target_compile_options(_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

set_target_properties(_core PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_core"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
        RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
        RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
        LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
        LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/wut_control"
)