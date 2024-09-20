import pandas
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.feature_data import FeatureData, Taxonomy
from qiime2.plugin import (Plugin, Citations)
import q2_surpi
from q2_surpi._formats_and_types import (
    SurpiCountTable, SurpiCountTableFormat, SurpiCountTableDirectoryFormat,
    SurpiSampleSheet, SurpiSampleSheetFormat, SurpiSampleSheetDirectoryFormat)


plugin = Plugin(
    name=q2_surpi.__plugin_name__,
    version=q2_surpi.__version__,
    website=q2_surpi.__url__,
    package=q2_surpi.__package_name__,
    citations=Citations.load(
        q2_surpi.__citations_fname__, package=q2_surpi.__package_name__),
    description=q2_surpi.__long_description__,
    short_description=q2_surpi.__description__,
)

plugin.register_formats(SurpiCountTableFormat, SurpiCountTableDirectoryFormat)
plugin.register_semantic_types(SurpiCountTable)
plugin.register_semantic_type_to_format(
    SurpiCountTable, SurpiCountTableDirectoryFormat)

plugin.register_semantic_types(SurpiSampleSheet)
plugin.register_formats(SurpiSampleSheetFormat,
                        SurpiSampleSheetDirectoryFormat)
plugin.register_semantic_type_to_format(
    SurpiSampleSheet, SurpiSampleSheetDirectoryFormat)


@plugin.register_transformer
# load a SurpiCountTableFormat into a dataframe
def _1(ff: SurpiCountTableFormat) -> pandas.DataFrame:
    result = pandas.read_csv(str(ff), sep='\t', header=0)
    return result


@plugin.register_transformer
# load a SurpiSampleSheetFormat into a dataframe
def _2(ff: SurpiSampleSheetFormat) -> pandas.DataFrame:
    result = pandas.read_csv(str(ff), sep='\t', header=0)
    return result


# plugin.methods.register_function(
#     function=q2_surpi.extract_test,
#     name='Extract test data',
#     description='Extract test data.',
#     inputs={'test_df': SurpiCountTable},
#     input_descriptions={'test_df': 'Test data.'},
#     parameters={},
#     outputs=[('test_table', FeatureTable[Frequency]),
#              ('test_taxonomy', FeatureData[Taxonomy])],
#     output_descriptions={
#         'test_table': 'Test feature table.',
#         'test_taxonomy': 'Test feature metadata.'},
# )

plugin.methods.register_function(
    function=q2_surpi.extract,
    name='Extract SURPI data for use in QIIME.',
    description=(
        'Extract SURPI data into a feature table and a feature taxonomy.'),
    inputs={'surpi_output': SurpiCountTable,
            'surpi_sample_info': SurpiSampleSheet},
    input_descriptions={
        'surpi_output': "SURPI counts per species per barcode.",
        'surpi_sample_info': 'Info linking sample ids to barcodes.'},
    parameters={},
    outputs=[('table', FeatureTable[Frequency]),
             ('taxonomy', FeatureData[Taxonomy])],
    output_descriptions={
        'table': 'Output feature table.',
        'taxonomy': 'Output feature metadata.'},
)
