import sys

from qgis.testing import unittest

# from LDMP.test.unit.test_dialog_settings import SettingsUnitSuite
# from LDMP.test.unit.test_calculate_ldn import CalculateLDNUnitSuite
# from LDMP.test.integration.test_calculate_ldn import CalculateLDNIntegrationSuite
# from LDMP.test.integration.test_calculate_urban import CalculateUrbanIntegrationSuite

from LDMP.test.unit.test_reports import ReportsFrameworkTests


def unit_tests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportsFrameworkTests))
    # suite.addTest(SettingsUnitSuite())
    # suite.addTest(CalculateLDNUnitSuite())
    return suite


def integration_tests():
    suite = unittest.TestSuite()
    # suite.addTest(CalculateLDNIntegrationSuite())
    # suite.addTest(CalculateUrbanIntegrationSuite())
    return suite


def run_all():
    # unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(integrationTests())
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(unit_tests())


if __name__ == '__main__':
    run_all()
