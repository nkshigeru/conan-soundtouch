import os
from conans import ConanFile, tools, MSBuild, AutoToolsBuildEnvironment


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
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def build_id(self):
        if self.settings.os == "Windows":
            self.info_build.options.shared = "Any"

    def source(self):
        url = "https://gitlab.com/soundtouch/soundtouch/-/archive/{version}/soundtouch-{version}.tar.gz".format(version=self.version)
        tools.get(url)
        os.rename("soundtouch-{version}".format(version=self.version), self.source_subfolder)
        tools.replace_in_file(os.path.join(self.source_subfolder, "source/SoundTouchDLL/SoundTouchDLL.rc"),
            "afxres.h", "winres.h")

    def build(self):
        if self.settings.os == "Windows":
            msbuild = MSBuild(self)
            msbuild.build(os.path.join(self.source_subfolder, "source/SoundTouchDLL/SoundTouchDLL.sln"),
                platforms = {'x86': 'Win32', 'x86_64': 'x64'})
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
            self.copy("source/SoundTouchDLL/SoundTouchDLL.h", dst="include", src=self.source_subfolder, keep_path=False)
            self.copy("*.h", dst="include/soundtouch", src=os.path.join(self.source_subfolder, "include"), keep_path=False)
            self.copy("*.lib", dst="lib", src=os.path.join(self.source_subfolder, "lib"), keep_path=False)
            self.copy("*.dll", dst="bin", src=os.path.join(self.source_subfolder, "lib"), keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            lib = "SoundTouch{dll}{debug}{suffix}".format(
                dll = "DLL" if self.options.shared else "",
                debug = "D" if self.settings.build_type == "Debug" else "",
                suffix = "_x64" if self.settings.arch == "x86_64" else ""
            )
            self.cpp_info.libs = [lib]
        else:
            self.cpp_info.libs = ["SoundTouch"]

