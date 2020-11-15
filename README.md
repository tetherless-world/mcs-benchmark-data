# MCS Benchmark Data

MCS Benchmark Data is a set of scripts that can be ued to create and execute Extract, Transform, Load (ETL) pipelines that store information about Machine Commonsense benchmarks into the Commonsense Benchmark Ontology.

For more information about the ontology, refer to:
[Commonsense Benchmark Ontology](https://tetherless-world.github.io/mcs-ontology/docs/index-en.html)
*Henrique O. Santos, Minor Gordon, Zhicheng Liang, Gretchen Forbush, Deborah L. McGuinness*


## Usage: Adding a Pipeline

Adding a new benchmark to the ontology requires adding a pipeline.

### 1. Add the Appropriate Data

Add a folder with the name of the benchmark (snake_case) to the `data` directory. 
```bash
cd data
mkdir <benchmark_name>
```
Within that new directory, add the appropriate file/folder structure.
```bash
cd <benchmark_name>
mkdir -p datasets/dev datasets/test datasets/train
mkdir loaded
```

Add the benchmark files to the corresponding folder based on their dataset type.

Copy `metadata.json` from another benchmark's data folder and fill the file with the appropriate information for the new benchmark.
```bash
cp ../anli/metadata.json
```

Repeat this in the `test_data` directory with smaller subsets of data, if desired. Instead of creating a duplicate metadata file, use symbolic links.

From root directory, once the test_data directory for this benchmark has been produced:
```bash
cd test_data/<benchmark_name>
ln ../../data/<benchmark_name>/metadata.json
```

### 2. Create the Benchmark Pipeline Files

Make a directory for the new benchmark and copy/create the pipeline files.

```bash
cd ../mcs_benchmark_data/pipelines
mkdir <benchmark_name>
cp ../anli/anli_benchmark_pipeline.py <benchmark_name>_benchmark_pipieline.py
touch __init__.py <benchmark_name>_transformer.py
```
Edit the pipeline files to mimic the respective functionality in the other benchmark pipelines. 

#### Pipeline File

Edit the benchmark pipeline to reflect the new benchmark.
- Change the class name to `<BenchmarkName>BenchmarkPipeline` in the definition and the call in main
- Change the class attribute to `ID = "<benchmark_name>"`
- Change the transformer in the _Pipeline initilaization and the import statement to be called `<BenchmarkName>BenchmarkTransformer`


#### Transformer File

Define a class `<BenchmarkName>BenchmarkTransformer` that inherits from `_BenchmarkTransformer`
- Define the `_transform_benchmark_sample` class method using other pipelines for reference. 
```Python
    _transform_benchmark_sample(
        self,
        *,
        dataset_type: DatasetType,
        dataset_uri: URIRef,
        **kwds,
    ) -> Generator[_Model, None, None]
```
- Consider using helper methods in `_BenchmarkTransformer`


### 3. Prepare the Benchmark Submission Data (Optional)

Complete the following steps if using data from a completed benchmark submission.

From the root directory:

```bash
cd data/<benchmark_name>
mkdir -p submissions/<submission_name>
cd submissions
```

If non-existent for the current benchmark, copy the `submissions_metadata.jsonl` file from another benchmark.
```bash
cp ../../commonsense_qa/submissions/submissions_metadata.jsonl
```
Update the information in the file if necessary. If the file already exists for the current benchmark, add a new line with the corresponding information from the new submission.

Place the submission file in the `data/<benchmark_name>/submissions/<submission_name>` directory.

Repeat this in the `test_data` directory with smaller subsets of data, if desired. Instead of creating a duplicate metadata file, use symbolic links.

From root directory, once the test_data directory for this benchmark has been produced:
```bash
cd test_data/<benchmark_name>/submissions
ln ../../data/<benchmark_name>/submissions/submissions_metadata.jsonl
```

### 4. Create the Benchmark Submission Pipeline Files (Optional)

Copy the necessary pipeline files from another benchmark submission to the directory for this submission:

From the root directory:

```bash
cd mcs_benchmark_data/pipelines/<benchmark_name>
cp ../commonsense_qa/kagnet_commonsense_qa_submission_pipeline.py <submission_name>_<benchmark_name>_submission_pipeline.py
cp ../commonsense_qa/kagnet_commonsense_qa_submission_transformer.py <submission_name>_<benchmark_name>_submission_transformer.py
```

#### Pipeline File

Edit the submission pipeline to reflect the new benchmark.
- Change the class name to `<SubmissionName><BenchmarkName>SubmissionkPipeline` in the definition and the call in main
- Change the class attributes to `BENCHMARK_ID = "<benchmark_name>"` and `SUBMISSION_ID = "<submission_name>"`
- Change the transformer in the _Pipeline initilaization and the import statement to be called `<SubmissionName><BenchmarkName>BenchmarkTransformer`


#### Transformer File

Change the name of the class to `<SubmissionName><BenchmarkName>SubmissionTransformer` and update the docstring accordingly. 

You may need to adjust/add functionality based on the submission (as can be seen in the TriAN MCScript transformer). Use the functions in `_SubmissionTransformer` for guidance.

### 5. Test the Functionality

#### Add the appropriate directories/files
From the root directory:
```bash
cd tests/mcs_benchmark_data_test/pipelines
mkdir <benchmark_name>
cd <benchmark_name>
touch __init__.py
```

#### Testing the Benchmark Pipeline

Create your own test file, or copy a benchmark pipeline test file from another benchmark and update it accordingly:
```bash
cp ../anli/anli_pipeline_test.py <benchmark_name>_pipeline_test.py
```
- Change all of the pipeline objects to be `<BenchmarkName>Pipeline`
- Change the parameter `data_dir_path` according to whether you would like to pull from the full dataset (DATA_DIR_PATH) or a truncated dataset (TEST_DATA_DIR_PATH) (if it has been prepared).

#### Testing a Submission Pipeline

Create your own test file, or copy a benchmark submission test file from another benchmark and update it accordingly:
```bash
cp ../commonsense_qa/kagnet_commonsense_qa_submission_pipeline_test.py <submission_name>_<benchmark_name>_pipeline_test.py
```
- Change all of the pipeline objects to be `<BenchmarkName>Pipeline`
- Change the parameter `data_dir_path` according to whether you would like to pull from the full dataset (DATA_DIR_PATH) or a truncated dataset (TEST_DATA_DIR_PATH) (if it has been prepared).


### 4. File-naming Conventions

Within the `data` and `test_data` directories, files are assumed to be named as follows:
- Benchmark Dataset Samples: `<submission_type>_samples.<ext>`
- Benchmark Dataset Labels (if applicable): `<submission_type>_labels.<ext>`
- Benchmark Submission (if applicable): `<submission_name>_<submission_type>_submission.<ext>`
where `submission_type` is either `dev`, `test`, or `train`.





