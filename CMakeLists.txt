cmake_minimum_required(VERSION 2.8.11)
project(soundtouch)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_definitions(
  -DDLL_EXPORTS
)
include_directories(soundtouch/include)
set(SRC
  soundtouch/source/SoundTouch/AAFilter.cpp
  soundtouch/source/SoundTouch/BPMDetect.cpp
  soundtouch/source/SoundTouch/cpu_detect_x86.cpp
  soundtouch/source/SoundTouch/FIFOSampleBuffer.cpp
  soundtouch/source/SoundTouch/FIRFilter.cpp
  soundtouch/source/SoundTouch/InterpolateCubic.cpp
  soundtouch/source/SoundTouch/InterpolateLinear.cpp
  soundtouch/source/SoundTouch/InterpolateShannon.cpp
  soundtouch/source/SoundTouch/mmx_optimized.cpp
  soundtouch/source/SoundTouch/PeakFinder.cpp
  soundtouch/source/SoundTouch/RateTransposer.cpp
  soundtouch/source/SoundTouch/SoundTouch.cpp
  soundtouch/source/SoundTouch/sse_optimized.cpp
  soundtouch/source/SoundTouch/TDStretch.cpp
  soundtouch/source/SoundTouchDLL/SoundTouchDLL.cpp
  soundtouch/source/SoundTouchDLL/SoundTouchDLL.rc
)

add_library(SoundTouch SHARED
  ${SRC}
)