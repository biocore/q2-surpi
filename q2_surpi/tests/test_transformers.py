import numpy as np
import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase
from q2_surpi import (
    __package_name__, SurpiCountTableFormat, SurpiSampleSheetFormat)
from q2_surpi._formats_and_types import (
    SPECIES_KEY, GENUS_KEY, FAMILY_KEY, TAG_KEY, SAMPLE_NAME_KEY, BARCODE_KEY)


class TestSurpiCountTableFormatTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_surpicounttableformat_to_dataframe(self):
        input_fname = "surpi_output.counttable"

        expected_dict = {
            SPECIES_KEY: ["Dill cryptic virus 1", "Escherichia phage FEC14",
                          "Dickeya phage phiDP10.3", "Dickeya phage phiDP23.1",
                          "Salmonella virus SJ2", "Klebsiella phage May",
                          "Escherichia virus FI", "Escherichia virus Qbeta",
                          "Enterobacteria phage C-1 INW-2012",
                          "Enterobacteria phage Hgal1",
                          "Escherichia virus BZ13", "Escherichia virus MS2",
                          "Acinetobacter phage AP205", "Pseudomonas phage PP7",
                          "Pseudomonas phage PRR1", "*"],
            GENUS_KEY: [np.nan, "Cba120virus", "Limestonevirus",
                        "Limestonevirus", "Vi1virus", np.nan, "Allolevivirus",
                        "Allolevivirus", "Levivirus", "Levivirus", "Levivirus",
                        "Levivirus", np.nan, np.nan, np.nan, np.nan],
            FAMILY_KEY: ["Partitiviridae", "Ackermannviridae",
                         "Ackermannviridae", "Ackermannviridae",
                         "Ackermannviridae", "Ackermannviridae", "Leviviridae",
                         "Leviviridae", "Leviviridae", "Leviviridae",
                         "Leviviridae", "Leviviridae", "Leviviridae",
                         "Leviviridae", "Leviviridae", "Microviridae"],
            TAG_KEY: ["host-apicomplexans|fungi|plants;", "host-bacteria;",
                      "host-bacteria;", "host-bacteria;", "host-bacteria;",
                      "host-bacteria;", "host-bacteria;", "host-bacteria;",
                      "host-bacteria;", "host-bacteria;", "host-bacteria;",
                      "host-bacteria;", "host-bacteria;", "host-bacteria;",
                      "host-bacteria;", "host-bacteria;"],
            "AACCCGCC+GAGGATTT": [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 7, 0, 2, 0],
            "AATCGTCA+AGTTAAAG": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 3, 0, 0, 0],
            "ACTATGAT+TTCGATAG": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "AGTACAAG+CCCATTGC": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "AGTAGTAA+TACTGATA": [0, 0, 5, 1, 0, 0, 1, 5, 0, 1, 10, 1, 10, 4, 3, 0],
            "AGTCCCGG+GCAGAAGT": [0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 6, 0, 3, 0, 0, 0],
            "AGTCTGCT+TCCAGGCT": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "AGTGCGGA+CCGTTGTC": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "CATCTACT+TTCCGTTG": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 11, 0, 1, 0],
            "CATTCGGA+GATGGAAA": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0]
        }

        expected_df = pandas.DataFrame(expected_dict)

        _, obs_df = self.transform_format(
            SurpiCountTableFormat, pandas.DataFrame,
            filename=input_fname)

        assert_frame_equal(obs_df, expected_df)


class TestSurpiSampleSheetFormatTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_surpisamplesheetformat_to_dataframe(self):
        input_fname = "surpi_sample_info.csv"

        expected_dict = {
            SAMPLE_NAME_KEY: [
                "sample-R-A1", "sample-R-B1", "sample-R-C1", "sample-R-D1",
                "sample-R-E1", "sample-R-F1", "sample-R-G1", "sample-R-H1",
                "sample-R-A2", "sample-R-B2", "sample-R-C2", "sample-R-D2",
                "sample-R-E2", "sample-R-F2", "sample-R-G2", "sample-R-H2",
                "sample-D-A1", "sample-D-B1", "sample-D-C1", "sample-D-D1",
                "sample-D-E1", "sample-D-F1", "sample-D-G1", "sample-D-H1",
                "sample-D-A2", "sample-D-B2", "sample-D-C2", "sample-D-D2",
                "sample-D-E2", "sample-D-F2", "sample-D-G2", "sample-D-H2"],
            BARCODE_KEY: ["AGTAGTAA+TACTGATA", "TACTAAGG+CTGACTCG",
                          "CATTCGGA+GATGGAAA", "AATCGTCA+AGTTAAAG",
                          "GCTGATTT+ATAGAGGC", "CGCGAAAG+AAAGGAGG",
                          "TTGCCACT+GGGAACTG", "TTCGTGGA+ACAAGGTA",
                          "AGTCCCGG+GCAGAAGT", "TCCTGGAC+CTGCTTAA",
                          "CTACATGA+GATTTGAT", "CCGGATAG+GACTCAAA",
                          "AACCCGCC+GAGGATTT", "CGAACGTG+CATCTGTA",
                          "CCGTAGAA+TGCGCTTA", "CATCTACT+TTCCGTTG",
                          "AGTCTGCT+TCCAGGCT", "GCCGAATC+CTGTCCTC",
                          "ACTATGAT+TTCGATAG", "CCCTATCT+GTTAGTGA",
                          "CGTTGTCC+CTTATCGA", "TGGAACGG+GAATAAAG",
                          "CCCTTCGG+GAAGGCAG", "TGTCCAAA+TTGGTTGT",
                          "AGTACAAG+CCCATTGC", "TACTGTGA+GTGTCCAG",
                          "CCGGAATT+GCATACTT", "TCGCTCGG+CCATCGGA",
                          "AGTGCGGA+CCGTTGTC", "GCTTCACA+TAAAGCTA",
                          "CCGATCGT+GACTGTTT", "CCGTAAGC+AGTGAGGT"],
        }

        expected_df = pandas.DataFrame(expected_dict)

        _, obs_df = self.transform_format(
            SurpiSampleSheetFormat, pandas.DataFrame,
            filename=input_fname)

        # the only parts of the sample sheet that are used are the sample name
        # and the barcode, so we only compare those columns
        partial_obs_df = obs_df[[SAMPLE_NAME_KEY, BARCODE_KEY]]
        assert_frame_equal(partial_obs_df, expected_df)
