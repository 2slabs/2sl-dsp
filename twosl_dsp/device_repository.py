"""Where a plugin repository's device sources are (its src/), for the in-memory patch its plugin build reads.

    <plugin repo>/
      2sl-dsp/                     this kit, as a git submodule
      src/                         the device's Python, its brain template, its preset book and
        live-parameters.lock.json  the Live parameter lock (twosl_dsp/live_parameter_identity.py)

architecture/device-repository.md has the reasoning.
"""
import os

import twosl_dsp
from twosl_dsp.build_error import BuildError

KIT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(twosl_dsp.__file__)))


class DeviceRepository:
    def __init__(self, root_directory):
        """A repository rooted at `root_directory`, which must have src/ and must not be the kit."""
        self.root_directory = os.path.abspath(root_directory)
        self.source_directory = os.path.join(self.root_directory, "src")
        # the kit first: it is refused whatever it holds (it has no src/, and must not get one by accident)
        if os.path.realpath(self.root_directory) == os.path.realpath(KIT_DIRECTORY):
            raise BuildError(f"{self.root_directory} is the kit itself: a device is built from its own repository, "
                             "with the kit as its 2sl-dsp submodule")
        if not os.path.isdir(self.source_directory):
            raise BuildError(f"{self.root_directory} is no device repository: it has no src/ (see 2sl-dsp "
                             "architecture/device-repository.md)")

    def source_path(self, file_name):
        return os.path.join(self.source_directory, file_name)
