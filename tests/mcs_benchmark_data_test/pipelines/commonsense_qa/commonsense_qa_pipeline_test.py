from mcs_benchmark_data.path import DATA_DIR_PATH
from mcs_benchmark_data.pipelines.commonsense_qa.commonsense_qa_benchmark_pipeline import (
    CommonsenseQaBenchmarkPipeline,
)


def test_extract_transform_load(tmp_path):
    CommonsenseQaBenchmarkPipeline().extract_transform_load()
    loaded_data_dir_path = DATA_DIR_PATH / "loaded" / CommonsenseQaBenchmarkPipeline.ID
    assert loaded_data_dir_path.is_dir()
    rdf_file_path = loaded_data_dir_path / (CommonsenseQaBenchmarkPipeline.ID + ".ttl")
    assert rdf_file_path.is_file()
    # TODO: load the RDF file into a Graph and test its contents
