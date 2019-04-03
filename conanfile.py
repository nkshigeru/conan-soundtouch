import os
from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment


class SoundtouchConan(ConanFile):
    name = "soundtouch"
    version = "2.1.1"
    license = "LGPL-2.1"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Soundtouch here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = []
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "soundtouch"

    def source(self):
        url = "https://gitlab.com/soundtouch/soundtouch/-/archive/{version}/soundtouch-{version}.tar.gz".format(version=self.version)
        tools.get(url)
        os.rename("soundtouch-{version}".format(version=self.version), self.source_subfolder)
        tools.replace_in_file("soundtouch/source/SoundTouchDLL/SoundTouchDLL.rc",
            "afxres.h", "winres.h")

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
        else:
            with tools.chdir(self.source_subfolder):
                self.run("sh bootstrap")
                env_build = AutoToolsBuildEnvironment(self)
                def option_value(b):
                    return "yes" if b else "no"
                args = [
                    "--enable-shared=" + option_value(self.options.shared),
                    "--enable-static=" + option_value(not self.options.shared),
                ]
                env_build.configure(args=args)
                env_build.make()
                env_build.install()

    def package(self):
        if self.settings.os == "Windows":
            #self.copy("soundtouch/include/SoundTouch.h", dst="include", keep_path=False)
            self.copy("soundtouch/source/SoundTouchDLL/SoundTouchDLL.h", dst="include", keep_path=False)
            self.copy("lib/SoundTouch.lib", dst="lib", keep_path=False)
            self.copy("bin/SoundTouch.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SoundTouch"]

