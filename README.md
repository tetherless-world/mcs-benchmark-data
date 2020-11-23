# MCS Benchmark Data

MCS Benchmark Data is a set of scripts that can be used to create and execute pipelines that extract, transform and load information about Machine Commonsense benchmarks into the Commonsense Benchmark Ontology.

For more information about the ontology, refer to:
[Commonsense Benchmark Ontology](https://tetherless-world.github.io/mcs-ontology/docs/index-en.html)
*Henrique O. Santos, Minor Gordon, Zhicheng Liang, Gretchen Forbush, Deborah L. McGuinness*
## One-time Setup

### Create the Python virtual environment

From the current directory:
    python3 -m venv venv


### Activate the virtual environment

On Unix:
    source venv/bin/activate

On Windows:

    venv\Scripts\activate

### Install the dependencies
    pip install -r requirements.txt
## Development: Adding a Pipeline

Adding a new benchmark to the ontology requires adding a pipeline.


### 1. Adding a new benchmark

Activate the virtual environment as above, then run: 

    python3.6 -m cli create_benchmark_pipeline --benchmark_name <benchmark_name> [--using-test-data]

Follow the logging instructions in order to add the appropriate data files and update the transformer file as follows:

#### Transformer File

- Define the `_transform_benchmark_sample` class method, using other pipeline transformers for reference. 
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


#### 2. (Optional) Adding a new benchmark submission

Complete the following steps if using data from a completed benchmark submission.

Activate the virtual environment as above, then run: 

    python3.6 -m cli create_benchmark_pipeline --benchmark_name <benchmark_name> --submission_name <submission_name> [--using-test-data]

Follow the logging instructions in order to add the appropriate data files.


#### Transformer File

You may need to adjust/add functionality based on the submission (as can be seen in the TriAN MCScript transformer). Use the functions in `_SubmissionTransformer` for guidance.



### 3. Test the Functionality

Once the instructions above have been followed, run the following code to test the functionality:

#### Testing the entire test suite
From the root directory:
`pytest`

#### Testing individual benchmarks
From the test directory of the given benchmark (`./tests/mcs_benchmark_data_test/pipelines/<benchmark_name>`):
`pytest`

#### Testing an individual file
From the test directory of the given benchmark (`./tests/mcs_benchmark_data_test/pipelines/<benchmark_name>`):
`pytest <test_file_name>.py`

### 4. File-naming Conventions

Within the `data` and `test_data` directories, files are assumed to be named as follows:
- Benchmark Dataset Samples: `<submission_type>_samples.<ext>`
- Benchmark Dataset Labels (if applicable): `<submission_type>_labels.<ext>`
- Benchmark Submission (if applicable): `<submission_name>_<submission_type>_submission.<ext>`
where `submission_type` is either `dev`, `test`, or `train`.





