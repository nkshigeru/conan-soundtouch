import os
from conans import ConanFile, CMake, tools


class SoundtouchConan(ConanFile):
    name = "soundtouch"
    version = "2.1.1"
    license = "LGPL-2.1"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Soundtouch here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    exports = []
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    def source(self):
        url = "https://gitlab.com/soundtouch/soundtouch/-/archive/{version}/soundtouch-{version}.tar.gz".format(version=self.version)
        tools.get(url)
        os.rename("soundtouch-{version}".format(version=self.version), "soundtouch")
        tools.replace_in_file("soundtouch/source/SoundTouchDLL/SoundTouchDLL.rc",
            "afxres.h", "winres.h")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        #self.copy("soundtouch/include/SoundTouch.h", dst="include", keep_path=False)
        self.copy("soundtouch/source/SoundTouchDLL/SoundTouchDLL.h", dst="include", keep_path=False)
        self.copy("lib/SoundTouch.lib", dst="lib", keep_path=False)
        self.copy("bin/SoundTouch.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SoundTouch"]

