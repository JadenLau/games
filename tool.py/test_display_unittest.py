import os
import sys
import io
import types
import unittest
import importlib


TOOL_DIR = "/workspaces/games/tool.py"


class DisplayTests(unittest.TestCase):
    def setUp(self):
        # Patch terminal size to be deterministic for tests
        self._orig_get_terminal_size = os.get_terminal_size
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=20, lines=10)

        # Capture stdout so tests don't spam the terminal
        self._orig_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Ensure we can import the module by file path directory
        if TOOL_DIR not in sys.path:
            sys.path.insert(0, TOOL_DIR)

        # Re-import fresh module each test to pick up patched get_terminal_size
        if "main" in sys.modules:
            del sys.modules["main"]
        self.main = importlib.import_module("main")

    def tearDown(self):
        # Restore stdout
        sys.stdout = self._orig_stdout
        # Restore terminal size function
        os.get_terminal_size = self._orig_get_terminal_size
        # Clean sys.path (optional; keep for isolation)
        if TOOL_DIR in sys.path:
            try:
                sys.path.remove(TOOL_DIR)
            except ValueError:
                pass

    def test_plain_text_renders_at_coordinates(self):
        d = self.main.Display()
        d.text("Hi", 2, 1)
        d.render()
        self.assertEqual(d.last_terminal[1][2], "H")
        self.assertEqual(d.last_terminal[1][3], "i")

    def test_text_within_container(self):
        d = self.main.Display()
        d.container(5, 3, 15, 8, "box")
        d.text("OK", 1, 1, container=["box"])  # expect at (5+1, 3+1) => (6,4)
        d.render()
        self.assertEqual(d.last_terminal[4][6], "O")
        self.assertEqual(d.last_terminal[4][7], "K")

    def test_nested_containers(self):
        d = self.main.Display()
        d.container(2, 2, 18, 9, "outer")
        d.container(4, 3, 10, 6, "inner")
        d.text("N", 1, 1, container=["outer", "inner"])  # expect at (4+1, 3+1) => (5,4)
        d.render()
        self.assertEqual(d.last_terminal[4][5], "N")

    def test_horizontal_clipping_in_container(self):
        d = self.main.Display()
        # inclusive right edge at x=5 allows positions [0..5]
        d.container(0, 0, 5, 2, "small")
        d.text("abcdefg", 0, 0, container=["small"])  # 'g' should be clipped
        d.render()
        self.assertEqual(d.last_terminal[0][0], "a")
        self.assertEqual(d.last_terminal[0][5], "f")
        # ensure the clipped character didn't spill
        self.assertNotEqual(d.last_terminal[0][5], "g")

    def test_missing_container_raises(self):
        d = self.main.Display()
        d.text("X", 0, 0, container=["missing"])
        with self.assertRaises(self.main.ContainerNotFoundError):
            d.render()


if __name__ == "__main__":
    unittest.main(verbosity=2)
