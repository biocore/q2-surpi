import unittest

import q2_surpi
from q2_surpi.plugin_setup import plugin as surpi_plugin


class PluginSetupTests(unittest.TestCase):

    def test_plugin_setup(self):
        self.assertEqual(surpi_plugin.name, q2_surpi.__plugin_name__)
