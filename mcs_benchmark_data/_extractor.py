from abc import abstractmethod
from pathlib import Path
from typing import Dict, Optional
from urllib.request import urlopen

from pathvalidate import sanitize_filename

from mcs_benchmark_data._pipeline_phase import _PipelinePhase
from mcs_benchmark_data.path import DATA_DIR_PATH


class _Extractor(_PipelinePhase):
    def _download(self, from_url: str, force: bool) -> Path:
        """
        Utility method to download a file from a URL to a local file path.
        """
        file_path = self._extracted_data_dir_path / sanitize_filename(from_url)
        if not force and file_path.exists():
            self._logger.info(
                "%s already downloaded to %s and force not specified, skipping download",
                from_url,
                file_path,
            )
            return file_path

        self._logger.info("downloading %s to %s", from_url, file_path)
        try:
            url_ = urlopen(from_url)
            url_contents = url_.read()
        finally:
            url_.close()
        with open(file_path, "w+b") as file_:
            file_.write(url_contents)
        self._logger.info("downloaded %s", from_url)
        return file_path

    @abstractmethod
    def extract(self, *, force: bool) -> Optional[Dict[str, object]]:
        """
        Extract data from a source.
        :param force: force extraction, ignoring any cached data
        :return a **kwds dictionary to merge with kwds to pass to transformer
        """

    @property
    def _extracted_data_dir_path(self) -> Path:
        """
        Directory to use to store extracted data.
        The directory is created on demand when this method is called.
        Paths into this directory can be passed to the transformer via the kwds return from extract.
        """
        extracted_data_dir_path = DATA_DIR_PATH / self._pipeline_id
        extracted_data_dir_path = extracted_data_dir_path.absolute()
        extracted_data_dir_path.mkdir(parents=True, exist_ok=True)
        return extracted_data_dir_path
