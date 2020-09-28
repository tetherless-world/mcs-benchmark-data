from mcs_benchmark_data._extractor import _Extractor


class CommonsenseQaBenchmarkExtractor(_Extractor):
    def extract(self, **kwds):
        return {
            "benchmark_json_file_path": self._extracted_data_dir_path / "metadat.json",
            "dev_jsonl_file_path": self._extracted_data_dir_path
            / "dev_rand_split.jsonl",
            "test_jsonl_file_path": self._extracted_data_dir_path
            / "test_rand_split_no_answers.jsonl",
            "train_jsonl_file_path": self._extracted_data_dir_path
            / "train_rand_split.jsonl",
        }