import os
import re
import sys

from mcs_benchmark_data.dataset_type import DatasetType


def check_benchmark_name(*, benchmark_name: str):

    is_lowercase = benchmark_name == benchmark_name.lower()

    has_only_letters_underscores_numbers = bool(
        re.match("^[a-z0-9_]*$", benchmark_name)
    )

    prefixed_by_letter = benchmark_name[0].isalpha()

    return is_lowercase and has_only_letters_underscores_numbers and prefixed_by_letter


def make_benchmark_directories(*, benchmark_name: str):

    cwd = os.getcwd()

    for dataset_type in DatasetType:
        os.makedirs(
            os.path.join(cwd, f"data/{benchmark_name}/datasets/{dataset_type.value}")
        )
        os.makedirs(
            os.path.join(
                cwd, f"test_data/{benchmark_name}/datasets/{dataset_type.value}"
            )
        )

    print(
        f"""6 new directories have been made for the dev, train, and test datasets of the new benchmark in the following paths:\n
    -./data/{benchmark_name}/datasets/{dataset_type.value}\n
    -./test_data/{benchmark_name}/datasets/{dataset_type.value}\n
        Please add the proper files to each respective directory. Test_data files should have a smaller subset of data to facilitate expedited testing.\n
        Additionally, copy the metadata.json file from ./data/benchmark_name and fill in the appropriate information about the benchmark.\n
        Then, create a symbolic link of this file for the test data using the command \'ln metadata.json ../../test_data/{benchmark_name}/metadata.json\'"""
    )

    os.makedirs(os.path.join(cwd, f"mcs_benchmark_data/pipelines/{benchmark_name}"))

    open(
        os.path.join(cwd, f"mcs_benchmark_data/pipelines/{benchmark_name}/__init__.py"),
        "w",
    )

    print(
        f"""A new directory has been made for the pipeline files of the new benchmark at the following path:\n
    -./mcs_benchmark_data/pipelines/{benchmark_name}\n
    Please copy the benchmark_* files from ./mcs_benchmark_data/pipelines/benchmark_name and edit them according to the steps specified in the README.md"""
    )

    os.makedirs(
        os.path.join(cwd, f"tests/mcs_benchmark_data_test/pipelines/{benchmark_name}")
    )

    open(
        os.path.join(
            cwd, f"tests/mcs_benchmark_data_test/pipelines/{benchmark_name}/__init__.py"
        ),
        "w",
    )

    print(
        f"""A new directory has been made for the pipeline test files of the new benchmark at the following path:\n
    -./tests/mcs_benchmark_data_test/pipelines/{benchmark_name}\n
    Please copy the benchmark_* test file from ./tests/mcs_benchmark_data_test/pipelines/benchmark_name and edit it according to the steps specified in the README.md"""
    )


def make_submission_directories(*, benchmark_name: str, submission_name: str):

    cwd = os.getcwd()

    data_path = f"data/{benchmark_name}/submissions"

    submission_data_path = os.path.join(cwd, data_path)

    is_first_submission = not bool(
        os.path.exists(os.path.join(submission_data_path, "submissions_metadata.jsonl"))
    )

    print(is_first_submission)

    os.makedirs(os.path.join(submission_data_path, f"{submission_name}"))

    os.makedirs(os.path.join(cwd, f"test_{data_path}/{submission_name}"))

    if is_first_submission:
        print(
            f"""Since this is the first submission for this benchmark, please copy the file from the following path and 
        place it in ./data/{benchmark_name}/submissions:\n
        ./data/benchmark_name/submissions/submissions_metadata.jsonl\n
        Update the information from the skeleton to reflect the information about the new submission.\n 
        Then, create a symbolic link of this file for the test data using the command \'ln submissions_metadata.jsonl ../../../test_data/{benchmark_name}/submissions/submissions_metadata.jsonl\'\n"""
        )
    else:
        print(
            f"""Since this is not the first submission for this benchmark, please edit the file ./data/{benchmark_name}/submissions/submissions_metadata.jsonl.\n
        Edit the file by copying the last entry and pasting it directly below. Edit the entry according to the information from the new submission.\n"""
        )

    print(
        f"""The submission pipeline files need to be added to the following directory:\n
    -./mcs_benchmark_data/pipelines/{benchmark_name}\n
    Please copy the submission_* files from ./mcs_benchmark_data/pipelines/benchmark_name and edit them according to the steps specified in the README.md"""
    )

    print(
        f"""The submission pipeline test files need to be added to the following directory:\n
    -./tests/mcs_benchmark_data_test/pipelines/{benchmark_name}\n
    Please copy the submission_* test file from ./tests/mcs_benchmark_data_test/pipelines/benchmark_name and edit it according to the steps specified in the README.md"""
    )


if __name__ == "__main__":

    args = sys.argv

    if len(args) <= 1 or len(args) > 4:
        print(
            "An incorrect number of arguments was specified. Refer to the README.md file for how to properly execute the script."
        )
        sys.exit()

    option = sys.argv[1]

    if option == "--benchmark":

        benchmark_name = sys.argv[2]

        if not check_benchmark_name(benchmark_name=benchmark_name):
            print(
                "This benchmark name is not in snake_case. See https://medium.com/better-programming/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841 for more information."
            )
            sys.exit()

        make_benchmark_directories(benchmark_name=benchmark_name)

    elif option == "--submission":

        submission_name = sys.argv[2]

        benchmark_name = sys.argv[3]

        if not os.path.exists(os.path.join(os.getcwd(), f"data/{benchmark_name}")):
            print(
                "Please add the benchmark directories/files before adding a submission. Refer to the README.md for further instructions."
            )
            sys.exit()

        make_submission_directories(
            benchmark_name=benchmark_name, submission_name=submission_name
        )

    else:
        print(
            "The first argument must be either '--benchmark' or '--submission'. Please refer to the README.md for further instructions."
        )
