from qgis.testing import unittest

import sys
from queue import Queue
from time import sleep

from LDMP.calculate_prod import DlgCalculateProd

from LDMP.test.unit.test_dialog_settings import SettingsUnitSuite
from LDMP.test.unit.test_calculate_ldn import CalculateLDNUnitSuite
from LDMP.test.unit.test_reports import ReportsFrameworkTests
from LDMP.test.integration.test_calculate_ldn import CalculateLDNIntegrationSuite
from LDMP.test.integration.test_calculate_urban import CalculateUrbanIntegrationSuite

def unitTests():
    suite = unittest.TestSuite()
    suite.addTest(SettingsUnitSuite())
    suite.addTest(CalculateLDNUnitSuite())
    return suite


def integrationTests():
    suite = unittest.TestSuite()
    suite.addTest(CalculateLDNIntegrationSuite())
    suite.addTest(CalculateUrbanIntegrationSuite())
    return suite


def run_all():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportsFrameworkTests))

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    runner.run(suite)


if __name__ == '__main__':
    run_all()

