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

    def test_container_at_5_5_to_15_10(self):
        """Test container at coordinates (5,5) to (15,10) as requested"""
        # Override terminal size for this test to accommodate the container
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=20, lines=15)
        d = self.main.Display()
        
        # Create container at (5,5) to (15,10) as specified by user
        d.container(5, 5, 15, 10, "test_box")
        
        # Test text at origin of container (should appear at 5,5)
        d.text("A", 0, 0, container=["test_box"])
        d.render()
        self.assertEqual(d.last_terminal[5][5], "A")
        
    def test_container_at_5_5_to_15_10_with_offset(self):
        """Test text rendering with offset inside container at (5,5) to (15,10)"""
        # Override terminal size for this test to accommodate the container
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=20, lines=15)
        d = self.main.Display()
        d.container(5, 5, 15, 10, "test_box")
        
        # Test text at offset (2,1) within container (should appear at 5+2=7, 5+1=6)
        d.text("Test", 2, 1, container=["test_box"])
        d.render()
        self.assertEqual(d.last_terminal[6][7], "T")
        self.assertEqual(d.last_terminal[6][8], "e")
        self.assertEqual(d.last_terminal[6][9], "s")
        self.assertEqual(d.last_terminal[6][10], "t")
        
    def test_container_at_5_5_to_15_10_clipping(self):
        """Test that text is clipped at container boundaries (5,5) to (15,10)"""
        # Override terminal size for this test to accommodate the container
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=20, lines=15)
        d = self.main.Display()
        d.container(5, 5, 15, 10, "test_box")
        
        # Place text at container position x=6
        # Container spans screen x=5 to x=15 (11 positions total: 5,6,7,8,9,10,11,12,13,14,15)
        # Text at container x=6 maps to screen positions 11-15 (5 chars fit: '01234')
        # Characters '56789X' are clipped as they exceed the container boundary
        d.text("0123456789X", 6, 0, container=["test_box"])
        d.render()
        self.assertEqual(d.last_terminal[5][11], "0")  # container x=6 -> screen x=11
        self.assertEqual(d.last_terminal[5][15], "4")  # container x=10 -> screen x=15 (rightmost)
        # Verify clipped characters don't appear beyond container boundary
        self.assertEqual(d.last_terminal[5][16], " ")
        
    def test_container_at_5_5_to_15_10_vertical_bounds(self):
        """Test that container at (5,5) to (15,10) properly handles vertical bounds"""
        # Override terminal size for this test to accommodate the container
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=20, lines=15)
        d = self.main.Display()
        d.container(5, 5, 15, 10, "test_box")
        
        # Container spans from y=5 to y=10 (6 lines: 5,6,7,8,9,10)
        # Place text at bottom of container (y=5 within container maps to screen y=10)
        d.text("Bottom", 0, 5, container=["test_box"])
        d.render()
        self.assertEqual(d.last_terminal[10][5], "B")
        self.assertEqual(d.last_terminal[10][6], "o")
        self.assertEqual(d.last_terminal[10][7], "t")
        self.assertEqual(d.last_terminal[10][8], "t")
        self.assertEqual(d.last_terminal[10][9], "o")
        self.assertEqual(d.last_terminal[10][10], "m")


if __name__ == "__main__":
    unittest.main(verbosity=2)
