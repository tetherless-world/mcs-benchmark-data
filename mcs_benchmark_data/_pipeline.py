import logging
from abc import ABC
from typing import Dict, Optional
from pathlib import Path

from configargparse import ArgParser

from mcs_benchmark_data._extractor import _Extractor
from mcs_benchmark_data._loader import _Loader
from mcs_benchmark_data._transformer import _Transformer
from mcs_benchmark_data.loaders.default_loader import DefaultLoader
from mcs_benchmark_data.path import DATA_DIR_PATH


class _Pipeline(ABC):
    def __init__(
        self,
        *,
        extractor: _Extractor,
        id: str,
        transformer: _Transformer,
        loader: Optional[_Loader] = None,
        data_dir_path: Path = DATA_DIR_PATH,
        **kwds
    ):
        """
        Construct an extract-transform-load pipeline.
        :param extractor: extractor implementation
        :param id: unique identifier for this pipeline instance, may be adapted from arguments
        :param loader: optional loader; if not specified, a default loader will be used
        :param transformer: transformer implementation
        """
        self.__extractor = extractor
        self.__id = id
        if loader is None:
            loader = DefaultLoader(pipeline_id=id, data_dir_path=data_dir_path, **kwds)
        self.__loader = loader
        self.__transformer = transformer

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        """
        Add pipeline-specific arguments. The parsed arguments are passed to the constructor as keywords.
        """
        arg_parser.add_argument("-c", is_config_file=True, help="config file path")
        arg_parser.add_argument(
            "--debug", action="store_true", help="turn on debugging"
        )
        arg_parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="force extract and transform, ignoring any cached data",
        )
        arg_parser.add_argument(
            "--force-extract",
            action="store_true",
            help="force extract, ignoring any cached data",
        )
        arg_parser.add_argument(
            "--logging-level",
            help="set logging-level level (see Python logging module)",
        )

    def extract_transform(self, *, force_extract: bool = False):
        extract_kwds = self.extractor.extract(force=force_extract)
        if not extract_kwds:
            extract_kwds = {}
        return self.transformer.transform(**extract_kwds)

    def extract_transform_load(self, *, force_extract: bool = False):
        models = self.extract_transform(force_extract=force_extract)
        self.loader.load(models=models)
        return self.loader.flush()

    @property
    def extractor(self):
        return self.__extractor

    @classmethod
    def main(cls, args: Optional[Dict[str, object]] = None):
        if args is None:
            arg_parser = ArgParser()
            cls.add_arguments(arg_parser)
            args = arg_parser.parse_args()
            args = vars(args).copy()

        if args.get("debug", False):
            logging_level = logging.DEBUG
        elif args.get("logging_level") is not None:
            logging_level = getattr(logging, args["logging_level"].upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s",
            level=logging_level,
        )

        pipeline_kwds = args.copy()
        for key in ("force", "force_extract", "logging_level"):
            try:
                pipeline_kwds.pop(key)
            except KeyError:
                pass
        pipeline = cls(**pipeline_kwds)

        force = bool(args.get("force", False))
        force_extract = force or bool(args.get("force_extract", False))

        pipeline.extract_transform_load(force_extract=force_extract)

    @property
    def id(self):
        return self.__id

    @property
    def loader(self):
        return self.__loader

    @property
    def transformer(self):
        return self.__transformer
