# Unit tests for the reporting framework.

import unittest

# from LDMP.utils import qgis_process_path


class ReportsFrameworkTests(unittest.TestCase):
    """Unit tests for the reporting framework."""

    def test_qgis_process_path(self):
        """Path to qgis_process exists."""
        # proc_path = qgis_process_path()
        self.assertEqual('John','Kahiu', 'Names are not equal')

