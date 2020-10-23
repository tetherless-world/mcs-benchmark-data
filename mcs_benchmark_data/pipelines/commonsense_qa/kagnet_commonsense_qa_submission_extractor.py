from mcs_benchmark_data._extractor import _Extractor

from mcs_benchmark_data.path import DATA_DIR_PATH

from mcs_benchmark_data.pipelines.commonsense_qa.kagnet_commonsense_qa_submission_file_names import (
    KagnetCommonsenseQaSubmissionFileNames,
)


class KagnetCommonsenseQaSubmissionExtractor(_Extractor):
    def __init__(
        self,
        file_names: KagnetCommonsenseQaSubmissionFileNames,
        **kwds,
    ):
        _Extractor.__init__(self, **kwds)
        self.__file_names = file_names

    def extract(self, **kwds):

        return {
            "extracted_path": self._extracted_data_dir_path,
            "file_names": self.__file_names,
        }
