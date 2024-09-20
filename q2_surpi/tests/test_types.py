from q2_surpi import (
    SurpiCountTable, SurpiSampleSheet,
    SurpiCountTableDirectoryFormat, SurpiSampleSheetDirectoryFormat,
    __package_name__)

from qiime2.plugin.testing import TestPluginBase


class TestTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_surpicounttable_semantic_types_registration(self):
        self.assertRegisteredSemanticType(SurpiCountTable)
        self.assertSemanticTypeRegisteredToFormat(
            SurpiCountTable,
            SurpiCountTableDirectoryFormat)

    def test_linear_regressions_semantic_types_registration(self):
        self.assertRegisteredSemanticType(SurpiSampleSheet)
        self.assertSemanticTypeRegisteredToFormat(
            SurpiSampleSheet,
            SurpiSampleSheetDirectoryFormat)
