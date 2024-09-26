import io
import pandas
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model

FEATURE_ID_KEY = 'feature-id'
SPECIES_KEY = "species"
GENUS_KEY = "genus"
FAMILY_KEY = "family"
TAG_KEY = "tag"
SAMPLE_NAME_KEY = 'Sample_Name'
SS_SAMPLE_ID_KEY = "Sample_ID"
INDEX_1_KEY = "index"
INDEX_2_KEY = "index2"
BARCODE_KEY = 'barcode'


# Types
SurpiCountTable = SemanticType("SurpiCountTable")
SurpiSampleSheet = SemanticType("SurpiSampleSheet")


# Formats
class SurpiCountTableFormat(model.TextFileFormat):
    """Represents a tab-delimited count file produced by SURPI+."""

    def _validate_(self, level):
        # Validate that the file is a tsv and that it has the expected columns
        # for those that are fixed. Note that we don't validate the values in
        # the columns, as we don't know what they should be.
        with self.path.open("r") as f:
            df = pandas.read_csv(f, header=0, sep='\t')

        if (len(df.columns) < 5) or (df.columns[0] != SPECIES_KEY) or \
                (df.columns[1] != GENUS_KEY) or (df.columns[2] != FAMILY_KEY) \
                or (df.columns[3] != TAG_KEY):
            raise ValidationError(
                f"Expected columns for {SPECIES_KEY}, {GENUS_KEY}, "
                f"{FAMILY_KEY}, {TAG_KEY}, and at least one sample, but got "
                f"{df.columns}")

        if len(df) == 0:
            raise ValidationError("Expected at least one row, but got none")


class SurpiSampleSheetFormat(model.TextFileFormat):
    """Represents a csv-delimited sample sheet file used by SURPI+."""

    def _validate_(self, level):
        _ = surpi_sample_sheet_fp_to_df(self.path)


def surpi_sample_sheet_fp_to_df(fp: str) -> pandas.DataFrame:
    # open the file and count each line until we find one that starts with
    # [Data]

    data_table_lines = []
    is_data = False
    with open(fp, "r") as f:
        for line in f:
            if line.startswith("[Data]"):
                is_data = True
                continue
            # endif line.startswith("[Data]")

            if is_data:
                if line.startswith("["):
                    # if we've reached the beginning of the next section, stop
                    break

                if not line.startswith(','):
                    # add non-empty lines to the data table
                    data_table_lines.append(line)
            # endif is_data and not line.startswith(',')
        # endfor line in f
    # endwith self.path.open("r") as f

    if len(data_table_lines) == 0:
        raise ValidationError(
            "Expected section starting with '[Data]', but didn't find one")

    # create a streamio object from the list of lines
    data_table_stream = io.StringIO("\n".join(data_table_lines))

    # Validate that the file is a tsv and that it has the expected columns
    # for those that are fixed. Note that we don't validate the values in
    # the columns, as we don't know what they should be.
    df = pandas.read_csv(data_table_stream, header=0, sep=',')

    if ((SAMPLE_NAME_KEY not in df.columns) or
            (INDEX_1_KEY not in df.columns) or
            (INDEX_2_KEY not in df.columns)):
        raise ValidationError(
            f"Expected at least '{SAMPLE_NAME_KEY}', '{INDEX_1_KEY}', and "
            f"'{INDEX_2_KEY}' columns, but got {df.columns}")

    if len(df) == 0:
        raise ValidationError("Expected at least one row, but got none")

    df[BARCODE_KEY] = df[INDEX_1_KEY] + "+" + df[INDEX_2_KEY]
    return df


SurpiCountTableDirectoryFormat = model.SingleFileDirectoryFormat(
    'SurpiCountTableDirectoryFormat', 'surpi_output.counttable',
    SurpiCountTableFormat)

SurpiSampleSheetDirectoryFormat = model.SingleFileDirectoryFormat(
    'SurpiSampleSheetDirectoryFormat', 'surpi_sample_info.txt',
    SurpiSampleSheetFormat)
