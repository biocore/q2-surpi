from q2_surpi import (
    __package_name__, SurpiCountTableFormat, SurpiSampleSheetFormat)
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase


class TestSurpiCountTableFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_surpicounttable_format_valid(self):
        filenames = ['surpi_output.counttable']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = SurpiCountTableFormat(filepath, mode='r')
            test_format.validate()

    def test_surpicounttable_format_invalid(self):
        filenames = ['surpi_missing_cols.counttable',
                     'surpi_missing_samples.counttable',
                     'surpi_empty.counttable']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            with self.assertRaisesRegex(ValidationError, r'Expected '):
                test_format = SurpiCountTableFormat(filepath, mode='r')
                test_format.validate()


class TestSurpiSampleSheetFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_surpisamplesheet_format_valid(self):
        filenames = ['surpi_sample_info.txt']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = SurpiSampleSheetFormat(filepath, mode='r')
            test_format.validate()

    def test_surpisamplesheet_format_invalid(self):
        filenames = [
            # empty
            'surpi_sample_info_empty.txt',
            # missing column "sample"
            'surpi_sample_info_missing_sample.txt',
            # missing column "barcode"
            'surpi_sample_info_missing_barcode.txt'
        ]
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            with self.assertRaisesRegex(ValidationError, r'Expected '):
                test_format = SurpiSampleSheetFormat(filepath, mode='r')
                test_format.validate()
