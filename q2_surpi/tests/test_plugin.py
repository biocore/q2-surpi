import numpy as np
import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase
from q2_surpi import __package_name__
from q2_surpi._formats_and_types import (
    SPECIES_KEY, GENUS_KEY, FAMILY_KEY, TAG_KEY, SAMPLE_NAME_KEY, BARCODE_KEY)
from q2_surpi._plugin import extract, SAMPLE_ID_KEY, TAXON_KEY, FEATURE_KEY


class TestExtractSurpiData(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_extract(self):
        counts_dict = {
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

        sample_info_dict = {
            SAMPLE_NAME_KEY: [
                "sample_1", "sample_2", "sample_3", "sample_4", "sample_5",
                "sample_6", "sample_7", "sample_8", "sample_9", "sample_10",
                "sample_11", "sample_12", "sample_13", "sample_14",
                "sample_15", "sample_16", "sample_17", "sample_18",
                "sample_19", "sample_20", "sample_21", "sample_22",
                "sample_23", "sample_24", "sample_25", "sample_26",
                "sample_27", "sample_28", "sample_29", "sample_30",
                "sample_31", "sample_32"],
            BARCODE_KEY: ["AACCCGCC+GAGGATTT", "AATCGTCA+AGTTAAAG",
                          "ACTATGAT+TTCGATAG", "AGTACAAG+CCCATTGC",
                          "AGTAGTAA+TACTGATA", "AGTCCCGG+GCAGAAGT",
                          "AGTCTGCT+TCCAGGCT", "AGTGCGGA+CCGTTGTC",
                          "CATCTACT+TTCCGTTG", "CATTCGGA+GATGGAAA",
                          "CCCTATCT+GTTAGTGA", "CCCTTCGG+GAAGGCAG",
                          "CCGATCGT+GACTGTTT", "CCGGAATT+GCATACTT",
                          "CCGGATAG+GACTCAAA", "CCGTAAGC+AGTGAGGT",
                          "CCGTAGAA+TGCGCTTA", "CGAACGTG+CATCTGTA",
                          "CGCGAAAG+AAAGGAGG", "CGTTGTCC+CTTATCGA",
                          "CTACATGA+GATTTGAT", "GCCGAATC+CTGTCCTC",
                          "GCTGATTT+ATAGAGGC", "GCTTCACA+TAAAGCTA",
                          "TACTAAGG+CTGACTCG", "TACTGTGA+GTGTCCAG",
                          "TCCTGGAC+CTGCTTAA", "TCGCTCGG+CCATCGGA",
                          "TGGAACGG+GAATAAAG", "TGTCCAAA+TTGGTTGT",
                          "TTCGTGGA+ACAAGGTA", "TTGCCACT+GGGAACTG"],
        }

        feature_ids = [
            "Dill cryptic virus 1__Partitiviridae",
            "Escherichia phage FEC14_Cba120virus_Ackermannviridae",
            "Dickeya phage phiDP10.3_Limestonevirus_Ackermannviridae",
            "Dickeya phage phiDP23.1_Limestonevirus_Ackermannviridae",
            "Salmonella virus SJ2_Vi1virus_Ackermannviridae",
            "Klebsiella phage May__Ackermannviridae",
            "Escherichia virus FI_Allolevivirus_Leviviridae",
            "Escherichia virus Qbeta_Allolevivirus_Leviviridae",
            "Enterobacteria phage C-1 INW-2012_Levivirus_Leviviridae",
            "Enterobacteria phage Hgal1_Levivirus_Leviviridae",
            "Escherichia virus BZ13_Levivirus_Leviviridae",
            "Escherichia virus MS2_Levivirus_Leviviridae",
            "Acinetobacter phage AP205__Leviviridae",
            "Pseudomonas phage PP7__Leviviridae",
            "Pseudomonas phage PRR1__Leviviridae",
            "*__Microviridae"]

        expected_counts_dict = {
            feature_ids[0]: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            feature_ids[1]: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            feature_ids[2]: [1, 0, 0, 0, 5, 0, 0, 0, 0, 0],
            feature_ids[3]: [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            feature_ids[4]: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            feature_ids[5]: [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
            feature_ids[6]: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            feature_ids[7]: [1, 0, 0, 0, 5, 3, 0, 0, 0, 1],
            feature_ids[8]: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            feature_ids[9]: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            feature_ids[10]: [2, 8, 0, 0, 10, 6, 0, 0, 0, 3],
            feature_ids[11]: [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            feature_ids[12]: [7, 3, 0, 0, 10, 3, 0, 0, 11, 0],
            feature_ids[13]: [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
            feature_ids[14]: [2, 0, 0, 0, 3, 0, 0, 0, 1, 0],
            feature_ids[15]: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        expected_taxonomy_dict = {
            TAXON_KEY: ["f__Partitiviridae; s__Dill cryptic virus 1;",
                        "f__Ackermannviridae; g__Cba120virus; s__Escherichia phage FEC14;",
                        "f__Ackermannviridae; g__Limestonevirus; s__Dickeya phage phiDP10.3;",
                        "f__Ackermannviridae; g__Limestonevirus; s__Dickeya phage phiDP23.1;",
                        "f__Ackermannviridae; g__Vi1virus; s__Salmonella virus SJ2;",
                        "f__Ackermannviridae; s__Klebsiella phage May;",
                        "f__Leviviridae; g__Allolevivirus; s__Escherichia virus FI;",
                        "f__Leviviridae; g__Allolevivirus; s__Escherichia virus Qbeta;",
                        "f__Leviviridae; g__Levivirus; s__Enterobacteria phage C-1 INW-2012;",
                        "f__Leviviridae; g__Levivirus; s__Enterobacteria phage Hgal1;",
                        "f__Leviviridae; g__Levivirus; s__Escherichia virus BZ13;",
                        "f__Leviviridae; g__Levivirus; s__Escherichia virus MS2;",
                        "f__Leviviridae; s__Acinetobacter phage AP205;",
                        "f__Leviviridae; s__Pseudomonas phage PP7;",
                        "f__Leviviridae; s__Pseudomonas phage PRR1;",
                        "f__Microviridae; s__*;"]
        }

        input_counts_df = pandas.DataFrame(counts_dict)
        input_sample_info_df = pandas.DataFrame(sample_info_dict)
        expected_counts_df = pandas.DataFrame(
            expected_counts_dict,
            index=sample_info_dict[SAMPLE_NAME_KEY][0:10])
        expected_counts_df.index.name = SAMPLE_ID_KEY
        expected_taxonomy_df = pandas.DataFrame(
            expected_taxonomy_dict, index=feature_ids)
        expected_taxonomy_df.index.name = FEATURE_KEY

        obs_feature_table_df, obs_taxonomy_df = extract(
            input_counts_df, input_sample_info_df)

        assert_frame_equal(obs_feature_table_df, expected_counts_df)
        assert_frame_equal(obs_taxonomy_df, expected_taxonomy_df)
