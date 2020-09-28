import json
from typing import Generator

from pathvalidate import sanitize_filename

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.loaders._file_loader import _FileLoader
from mcs_benchmark_data.loaders.json_utils import json_dump_default, model_to_json_object


class JsonFileLoader(_FileLoader):
    def __init__(self, **kwds):
        _FileLoader.__init__(self, **kwds)
        self.__models = []

    def flush(self):
        file_path = self._file_path
        if file_path is None:
            file_path = self._loaded_data_dir_path / (
                sanitize_filename(self._pipeline_id) + ".json"
            )

        json_objects_by_class_name = {}
        for model in self.__models:
            json_objects_by_class_name.setdefault(model.__class__.__name__, []).append(
                model_to_json_object(model)
            )

        with open(file_path, "w+", newline="\n") as file_:
            json.dump(
                json_objects_by_class_name, file_, indent=4, default=json_dump_default
            )

    def load(self, *, models: Generator[_Model, None, None]):
        self.__models.extend(models)