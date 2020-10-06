from mcs_benchmark_data._extractor import _Extractor


class RobertaCommonsenseQaSubmissionExtractor(_Extractor):
    def extract(self, **kwds):
        return {
            "submission_data_jsonl_file_path": self._extracted_data_dir_path
            / "CommonsenseQA_dev_submissions.jsonl",
            "submission_jsonl_file_path": self._extracted_data_dir_path
            / "dev_rand_split_roberta_submission.jsonl",
        }
