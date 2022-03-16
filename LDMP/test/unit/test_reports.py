# Unit tests for the reporting framework.

import unittest

from LDMP.utils import qgis_process_path


class ReportsFrameworkTests(unittest.TestCase):
    """Unit tests for the reporting framework."""

    def test_qgis_process_path(self):
        """Path to qgis_process exists."""
        proc_path = qgis_process_path()
        self.assertIsNot(proc_path, '')


if __name__ == '__main__':
    suite = unittest.makeSuite(ReportsFrameworkTests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)