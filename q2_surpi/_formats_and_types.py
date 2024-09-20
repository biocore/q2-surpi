import pandas
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model

FEATURE_ID_KEY = 'feature-id'
SPECIES_KEY = "species"
GENUS_KEY = "genus"
FAMILY_KEY = "family"
TAG_KEY = "tag"
SAMPLE_NAME_KEY = 'sample'
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


# TODO: this is speculative code and may need to be adjusted; I don't
#  know yet what the sample info looks like
class SurpiSampleSheetFormat(model.TextFileFormat):
    """Represents a tab-delimited sample sheet file used by SURPI+."""

    def _validate_(self, level):
        # Validate that the file is a tsv and that it has the expected columns
        # for those that are fixed. Note that we don't validate the values in
        # the columns, as we don't know what they should be.
        with self.path.open("r") as f:
            df = pandas.read_csv(f, header=0, sep='\t')

        if ((SAMPLE_NAME_KEY not in df.columns) or
                (BARCODE_KEY not in df.columns)):
            raise ValidationError(
                f"Expected '{SAMPLE_NAME_KEY}' and '{BARCODE_KEY}' columns, "
                f"but got {df.columns}")

        if len(df) == 0:
            raise ValidationError("Expected at least one row, but got none")


SurpiCountTableDirectoryFormat = model.SingleFileDirectoryFormat(
    'SurpiCountTableDirectoryFormat', 'surpi_output.counttable',
    SurpiCountTableFormat)

SurpiSampleSheetDirectoryFormat = model.SingleFileDirectoryFormat(
    'SurpiSampleSheetDirectoryFormat', 'surpi_sample_info.txt',
    SurpiSampleSheetFormat)
