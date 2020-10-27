import bz2
from io import StringIO

from rdflib import Graph

from mcs_benchmark_data.path import DATA_DIR_PATH
from tests.assertions import assert_valid_rdf_loaded
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_pipeline import (
    SocialIQaBenchmarkPipeline,
)
from mcs_benchmark_data.pipelines.social_iqa.social_iqa_benchmark_file_names import (
    SocialIQaBenchmarkFileNames,
)


def test_extract_transform_load():
    SocialIQaBenchmarkPipeline(
        file_names=SocialIQaBenchmarkFileNames(
            metadata="metadata.json",
            dev_labels="dev-labels.lst",
            dev_samples="dev.jsonl",
            train_labels="train-labels.lst",
            train_samples="train.jsonl",
        ),
    ).extract_transform_load()

    assert_valid_rdf_loaded(SocialIQaBenchmarkPipeline.ID)
