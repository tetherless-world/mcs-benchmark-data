from mcs_benchmark_data.path import DATA_DIR_PATH
from rdflib import Graph
from pathlib import Path
import bz2
import py_compile
import json
from typing import Optional, Tuple

from mcs_benchmark_data.models.submission_sample import SubmissionSample
from mcs_benchmark_data.dataset_type import DatasetType


def assert_valid_rdf_loaded(*, pipeline_id: str, data_dir_path: Path):

    loaded_data_dir_path = data_dir_path / pipeline_id / "loaded"
    assert loaded_data_dir_path.is_dir()
    rdf_bz2_file_path = loaded_data_dir_path / (pipeline_id + ".ttl.bz2")
    assert rdf_bz2_file_path.is_file()

    new_graph = Graph()
    with open(rdf_bz2_file_path, "rb") as rdf_bz2_file:
        with bz2.open(rdf_bz2_file, "rb") as rdf_file:
            new_graph.parse(source=rdf_file, format="ttl")


def assert_submission_models(*, benchmark_id: str, submission_id: str, models):
    assert models

    submissions = [model for model in models if not isinstance(model, SubmissionSample)]
    assert submissions
    submission = submissions[0]
    print(f"{benchmark_id}-{submission_id}")
    print(submission.name)
    assert submission.name == f"{benchmark_id}-{submission_id}"

    samples = [model for model in models if isinstance(model, SubmissionSample)]
    assert len(samples) > 3
    assert all(sample.submission_uri == submission.uri for sample in samples)


def check_py(path: Path):
    py_compile.compile(path, doraise=True)


def check_json(path: Path):

    with open(path, "r") as fp:
        json.loads(fp)


def assert_benchmark_pipeline_compiles(*, root_path: Path, benchmark_name: str):

    paths = [
        (
            Path(root_path / "data" / benchmark_name / "datasets" / dataset_type.value),
            None,
        )
        for dataset_type in DatasetType
    ]

    paths += [
        (
            Path(
                root_path
                / "test_data"
                / benchmark_name
                / "datasets"
                / dataset_type.value
            ),
            None,
        )
        for dataset_type in DatasetType
    ]
    path_to_pipeline = Path(
        root_path
        / "mcs_benchmark_data"
        / "pipelines"
        / benchmark_name
        / f"{benchmark_name}_benchmark_pipeline.py"
    )
    path_to_transformer = Path(
        root_path
        / "mcs_benchmark_data"
        / "pipelines"
        / benchmark_name
        / f"{benchmark_name}_benchmark_transformer.py"
    )
    path_to_test = Path(
        root_path
        / "tests"
        / "mcs_benchmark_data_test"
        / "pipelines"
        / benchmark_name
        / f"{benchmark_name}_pipeline_test.py"
    )
    path_to_metadata = Path(root_path / "data" / Path(benchmark_name) / "metadata.json")
    paths.append((path_to_pipeline, check_py))
    paths.append((path_to_transformer, check_py))
    paths.append((path_to_test, check_py))
    paths.append((path_to_metadata, check_json))
    for path, callable_check in paths:
        assert path.exists()
        if callable_check:
            callable_check(path)


def assert_submission_pipeline_compiles(
    *, root_path: Path, benchmark_name: str, submission_name: str
):

    paths = []

    submission_data_path = Path(
        root_path / "data" / benchmark_name / "submissions" / submission_name
    )

    submission_test_data_path = Path(
        root_path / "test_data" / benchmark_name / "submissions" / submission_name
    )

    path_to_metadata = Path(
        root_path
        / "data"
        / benchmark_name
        / "submissions"
        / "submissions_metadata.jsonl"
    )

    path_to_pipeline = Path(
        root_path / "mcs_benchmark_data" / "pipelines" / benchmark_name
    )
    path_to_tests = Path(
        root_path / "tests" / "mcs_benchmark_data_test" / "pipelines" / benchmark_name
    )

    paths.append(path_to_pipeline)
    paths.append(path_to_tests)

    paths.append(submission_data_path)
    paths.append(submission_test_data_path)

    for path in paths:
        assert path.exists()
        if path == path_to_pipeline:
            py_compile.compile(
                path / f"{submission_name}_{benchmark_name}_submission_pipeline.py",
                doraise=True,
            )
            py_compile.compile(
                path / f"{submission_name}_{benchmark_name}_submission_transformer.py",
                doraise=True,
            )
        elif path == path_to_tests:
            py_compile.compile(
                path / f"{submission_name}_{benchmark_name}_pipeline_test.py",
                doraise=True,
            )
        elif path == path_to_metadata:
            py_compile.compile(path, doraise=True)
