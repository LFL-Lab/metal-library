import unittest

import os

import metal_library
from metal_library.core.reader import Reader

class TestCore(unittest.TestCase):
    """Units test child"""
    
    def setUp(self):
        """Setup unit test."""
        pass

    def tearDown(self):
        """Tie any loose ends."""
        pass
    
    # metal_library attributes tests
    def test_supported_components(self):
        """Test metal_library.supported_components matches those in the library"""
        __library_path__ = metal_library.__library_path__
        directory_names = [d for d in os.listdir(__library_path__) if os.path.isdir(os.path.join(__library_path__, d))]
        component_names = directory_names.remove("__pycache__")

        self.assertEqual(len(metal_library.supported_components), len(component_names))

    # metal_library.core.reader related tests
    def test_reader_instantiate(self):
        """Test if the library will instantiate with all components"""
        for component_name in metal_library.supported_components:
            try:
                Reader(component_name=component_name)
            except Exception:
                self.fail(f"Reader failed on component_name = {component_name}")