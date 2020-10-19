import json
import xmltodict

from mcs_benchmark_data._extractor import _Extractor

from mcs_benchmark_data.path import DATA_DIR_PATH


class PhysicalIQaBenchmarkExtractor(_Extractor):
    def __init__(
        self,
        dev_jsonl_file_name: str,
        dev_labels_file_name: str,
        test_jsonl_file_name: str,
        train_jsonl_file_name: str,
        train_labels_file_name: str,
        **kwds,
    ):
        self.__dev_jsonl_file_name = dev_jsonl_file_name
        self.__dev_labels_file_name = dev_labels_file_name
        self.__test_jsonl_file_name = test_jsonl_file_name
        self.__train_jsonl_file_name = train_jsonl_file_name
        self.__train_labels_file_name = train_labels_file_name

    def extract(self, **kwds):

        extracted_data_dir_path = DATA_DIR_PATH / "extracted" / "PhysicalIQA"
        return {
            "benchmark_json_file_path": extracted_data_dir_path / "metadata.json",
            "dev_jsonl_file_path": extracted_data_dir_path / self.__dev_jsonl_file_name,
            "dev_labels_file_path": extracted_data_dir_path
            / self.__dev_labels_file_name,
            "test_jsonl_file_path": extracted_data_dir_path
            / self.__test_jsonl_file_name,
            "train_jsonl_file_path": extracted_data_dir_path
            / self.__train_jsonl_file_name,
            "train_labels_file_path": extracted_data_dir_path
            / self.__train_labels_file_name,
        }
