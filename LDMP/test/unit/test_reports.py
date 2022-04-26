# Unit tests for the reporting framework.

import subprocess
import unittest

from LDMP.utils import qgis_process_path


class ReportsFrameworkTests(unittest.TestCase):
    """Unit tests for the reporting framework."""

    def test_qgis_process_path(self):
        # Assert path to qgis_process exists.
        proc_path = qgis_process_path()
        self.assertIsNot(proc_path, '', 'Path to qgis_process not found.')

    def test_exec_qgis_process(self):
        # Assert qgis_process can be executed.
        proc_path = qgis_process_path()
        completed_process = subprocess.run([proc_path, 'list'])

        self.assertEqual(
            completed_process.returncode,
            0,
            'Execute qgis_process failed'
        )


