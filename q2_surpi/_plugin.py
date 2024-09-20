import pandas
from q2_surpi._formats_and_types import FEATURE_ID_KEY, FAMILY_KEY, \
    GENUS_KEY, SPECIES_KEY, BARCODE_KEY, TAG_KEY, SAMPLE_NAME_KEY

SAMPLE_ID_KEY = 'sample-id'
TAXON_KEY = 'Taxon'
FEATURE_KEY = 'Feature ID'


# NB: Because there is a transformer on the plugin that can turn a
# SurpiCountTable (which is what the plugin gets as its first
# argument) into a pandas.DataFrame, and another that can turn a
# SurpiSampleSheet (which is what the plugin gets as its second argument)
# into a pandas.DataFrame, those transformations will be done
# automagically and this will receive pandas.DataFrames as its arguments.
def extract(
        surpi_output: pandas.DataFrame,
        surpi_sample_info: pandas.DataFrame) -> \
        (pandas.DataFrame, pandas.DataFrame):

    """Turn SURPI data into a feature table dataframe and a taxonomy dataframe.

    Parameters
    ----------
    surpi_counts_df : pandas.DataFrame
        A DataFrame containing the content of a SURPI counttable [sic] file.
    surpi_sample_info_df : pandas.DataFrame
        A DataFrame containing the content of a SURPI sample sheet file.

    Returns
    -------
    surpi_feature_table_df : pandas.DataFrame
        A DataFrame containing the SURPI counts linked to sample ids and the
        original surpi taxon-based feature ids.
    surpi_taxonomy_df : pandas.DataFrame
        A DataFrame linking the original surpi taxon-based feature ids to
        the QIIME 2 taxonomy format.
    """

    # Generate the taxonomy result
    taxonomy = surpi_output[[SPECIES_KEY, GENUS_KEY, FAMILY_KEY]].copy()
    taxonomy[TAXON_KEY] = surpi_output.apply(
        lambda x: _generate_taxonomy_str(x), axis=1)
    taxonomy.fillna("", inplace=True)
    taxonomy[FEATURE_ID_KEY] = taxonomy[SPECIES_KEY] + "_" + \
        taxonomy[GENUS_KEY] + "_" + taxonomy[FAMILY_KEY]
    # drop the SPECIES_KEY, GENUS_KEY, and FAMILY_KEY columns
    taxonomy.drop(columns=[SPECIES_KEY, GENUS_KEY, FAMILY_KEY], inplace=True)
    taxonomy = taxonomy.set_index(FEATURE_ID_KEY)
    taxonomy.index.name = FEATURE_KEY

    # Generate the feature table
    surpi_feature_table_df = surpi_output.copy()
    surpi_feature_table_df.drop(
        columns=[SPECIES_KEY, GENUS_KEY, FAMILY_KEY, TAG_KEY], inplace=True)
    surpi_feature_table_df[FEATURE_ID_KEY] = taxonomy.index
    surpi_feature_table_df = surpi_feature_table_df.set_index(FEATURE_ID_KEY)
    surpi_feature_table_df = surpi_feature_table_df.T
    surpi_feature_table_df.index.name = BARCODE_KEY
    surpi_feature_table_df = surpi_feature_table_df.reset_index()
    feature_barcodes = surpi_feature_table_df[BARCODE_KEY].unique()

    # merge the sample info with the feature table
    # TODO: this is speculative code and may need to be adjusted; I don't
    #  know yet what the sample info looks like
    limited_sample_info_df = \
        surpi_sample_info[[BARCODE_KEY, SAMPLE_NAME_KEY]]
    surpi_feature_table_df = surpi_feature_table_df.merge(
        limited_sample_info_df, on=BARCODE_KEY, how='inner',
        validate='one_to_one')
    identified_barcodes = surpi_feature_table_df[BARCODE_KEY].unique()
    unidentified_barcodes = set(feature_barcodes) - set(identified_barcodes)
    if len(unidentified_barcodes) > 0:
        raise ValueError(
            f"The following barcodes were not linked to sample identifiers "
            f"in the sample sheet: {unidentified_barcodes}")

    surpi_feature_table_df.drop(columns=[BARCODE_KEY], inplace=True)
    surpi_feature_table_df.set_index(SAMPLE_NAME_KEY, inplace=True)
    surpi_feature_table_df.index.name = SAMPLE_ID_KEY

    return surpi_feature_table_df, taxonomy


def _generate_taxonomy_str(row):
    fam_str = "" if pandas.isnull(row[FAMILY_KEY]) else \
        "f__" + row[FAMILY_KEY] + "; "
    gen_str = "" if pandas.isnull(row[GENUS_KEY]) else \
        "g__" + row[GENUS_KEY] + "; "
    spc_str = "" if pandas.isnull(row[SPECIES_KEY]) else \
        "s__" + row[SPECIES_KEY] + "; "

    result = fam_str + gen_str + spc_str
    return result.strip()
