from mcs_benchmark_data._extractor import _Extractor

from mcs_benchmark_data.path import DATA_DIR_PATH


class CommonsenseQaBenchmarkExtractor(_Extractor):
    def __init__(
        self,
        dev_jsonl_file_name: str,
        test_jsonl_file_name: str,
        train_jsonl_file_name: str,
        **kwds
    ):
        self.__dev_jsonl_file_name = dev_jsonl_file_name
        self.__test_jsonl_file_name = test_jsonl_file_name
        self.__train_jsonl_file_name = train_jsonl_file_name

    def extract(self, **kwds):
        # return {
        #     "benchmark_json_file_path": self._extracted_data_dir_path / "metadata.json",
        #     "dev_jsonl_file_path": self._extracted_data_dir_path
        #     / self.__dev_jsonl_file,
        #     "test_jsonl_file_path": self._extracted_data_dir_path
        #     / self.__test_jsonl_file,
        #     "train_jsonl_file_path": self._extracted_data_dir_path
        #     / self.__train_jsonl_file,
        # }
        extracted_data_dir_path = DATA_DIR_PATH / "extracted" / "CommonsenseQA"
        return {
            "benchmark_json_file_path": extracted_data_dir_path / "metadata.json",
            "dev_jsonl_file_path": extracted_data_dir_path / self.__dev_jsonl_file_name,
            "test_jsonl_file_path": extracted_data_dir_path
            / self.__test_jsonl_file_name,
            "train_jsonl_file_path": extracted_data_dir_path
            / self.__train_jsonl_file_name,
        }
