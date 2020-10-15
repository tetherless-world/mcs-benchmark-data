from mcs_benchmark_data._extractor import _Extractor

from mcs_benchmark_data.path import DATA_DIR_PATH


class KagnetCommonsenseQaSubmissionExtractor(_Extractor):
    def __init__(self, submission_jsonl_file_name: str, **kwds):
        self.__submission_jsonl_file_name = submission_jsonl_file_name

    def extract(self, **kwds):
        extracted_data_dir_path = DATA_DIR_PATH / "extracted" / "CommonsenseQA"
        # return {
        #     "submission_data_jsonl_file_path": self._extracted_data_dir_path
        #     / "CommonsenseQA_dev_submissions.jsonl",
        #     "submission_jsonl_file_path": self._extracted_data_dir_path
        #     / self.__submission_jsonl_file,
        # }
        return {
            "submission_data_jsonl_file_path": extracted_data_dir_path
            / "CommonsenseQA_dev_submissions.jsonl",
            "submission_jsonl_file_path": extracted_data_dir_path
            / self.__submission_jsonl_file_name,
        }
