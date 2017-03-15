cmake_minimum_required(VERSION 3.6)
project(HopeRF_LoRa_Receiver)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp RFM95registers.h AES_config.h AES.cpp AES.h Labp_RFM95.cpp Labp_RFM95.h)
add_executable(HopeRF_LoRa_Receiver ${SOURCE_FILES})