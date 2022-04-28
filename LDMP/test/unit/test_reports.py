# Unit tests for the reporting framework.

import subprocess
import unittest

import qgis.utils
from qgis.core import QgsApplication

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
        completed_process = subprocess.run([proc_path, 'plugins'])

        self.assertEqual(
            completed_process.returncode,
            0,
            'Execute qgis_process failed'
        )

    def test_plugin_entry(self):
        pt = '/root/.local/share/QGIS/QGIS3/profiles/default/QGIS/QGIS3.ini'
        plugin_path = QgsApplication.pluginPath()
        raise NameError(plugin_path)



