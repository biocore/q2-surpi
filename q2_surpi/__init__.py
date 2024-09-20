from ._plugin import extract
from ._formats_and_types import (
    SurpiCountTable, SurpiCountTableFormat, SurpiCountTableDirectoryFormat,
    SurpiSampleSheet, SurpiSampleSheetFormat, SurpiSampleSheetDirectoryFormat)
from . import _version
__version__ = _version.get_versions()['version']

__name__ = 'q2-surpi'
__plugin_name__ = 'surpi'
__package_name__ = 'q2_surpi'
__description__ = 'Plugin to import SURPI results into QIIME 2.'
__long_description__ = ('This QIIME 2 plugin imports SURPI results into '
                        'artifacts for use in QIIME 2.')
__license__ = 'BSD-3-Clause'
__author__ = 'Amanda Birmingham'
__email__ = 'abirmingham@ucsd.edu'
__url__ = 'https://github.com/AmandaBirmingham/q2-surpi'
__citations_fname__ = 'citations.bib'

__all__ = ['extract', 'SurpiCountTable', 'SurpiCountTableFormat',
           'SurpiCountTableDirectoryFormat', 'SurpiSampleSheet',
           'SurpiSampleSheetFormat', 'SurpiSampleSheetDirectoryFormat']
