"""The kit's brain blocks in node (tests/kit-scripts.test.js), in the fixture's brain and patch as the kit makes them
in memory. Needs node on PATH (or NODE=/path/to/node): fails, saying so, without it."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixture_device  # noqa: E402
from twosl_dsp.preset_book import PresetBook  # noqa: E402

NODE = os.environ.get("NODE") or shutil.which("node")


class KitScriptTests(unittest.TestCase):
    def test_the_generated_brain_blocks_in_node(self):
        if NODE is None:
            self.fail("node isn't on PATH (set NODE=/path/to/node): the kit's script tests need it")
        patch = fixture_device.fixture_patch(PresetBook(fixture_device.FIXTURE_PRESET_BOOK, "the fixture's book"))
        folder = tempfile.mkdtemp(prefix="kit-scripts-")
        try:
            brain_path, patch_path = os.path.join(folder, "brain.js"), os.path.join(folder, "patch.json")
            with open(brain_path, "w", encoding="utf-8") as brain_file:
                brain_file.write(patch.fixture_brain)
            with open(patch_path, "w", encoding="utf-8") as patch_file:
                json.dump(patch.patch(), patch_file)
            run = subprocess.run([NODE, os.path.join(HERE, "kit-scripts.test.js"), brain_path, patch_path],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main(verbosity=2)
