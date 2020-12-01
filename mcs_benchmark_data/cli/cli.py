import logging
import sys

from configargparse import ArgParser

from mcs_benchmark_data.path import ROOT_DIR_PATH
from mcs_benchmark_data.cli.commands.create_submission_pipeline_command import (
    CreateSubmissionPipelineCommand,
)
from mcs_benchmark_data.cli.commands.create_benchmark_pipeline_command import (
    CreateBenchmarkPipelineCommand,
)


class Cli:
    __COMMAND_CLASSES = {
        "create-benchmark-pipeline": CreateBenchmarkPipelineCommand,
        "create-submission-pipeline": CreateSubmissionPipelineCommand,
    }

    def __init__(self):
        self.__arg_parser = ArgParser()
        self.__logger = logging.getLogger(self.__class__.__name__)

    def __add_arguments(self):
        arg_parsers = [self.__arg_parser]
​
        subparsers = self.__arg_parser.add_subparsers(dest="command")
        for command_name, command_class in self.__COMMAND_CLASSES.items():
            command_arg_parser = subparsers.add_parser(command_name)
            command_class.add_arguments(command_arg_parser)
            arg_parsers.append(command_arg_parser)
​
        for arg_parser in arg_parsers:
            arg_parser.add_argument("-c", is_config_file=True, help="config file path")
            arg_parser.add_argument("--root-path",
                                           help="path to the mcs-benchmark-data directory")
            arg_parser.add_argument(
                "--benchmark-name",
                help="name of the benchmark the submission was tested against (in snake_case)",
            )
            arg_parser.add_argument(
                "--submission-name",
                help="name of the model that the submission was made from (in snake_case)",
            )
            arg_parser.add_argument(
                "--using-test-data",
                help="true if using truncated data for testing (in the test_data directory)\nalters the test file input path",
            )
            arg_parser.add_argument(
                '--debug',
                action='store_true',
                help='turn on debugging'
            )
            arg_parser.add_argument(
                '--logging-level',
                help='set logging-level level (see Python logging module)'
            )
            arg_parser.add_argument("-f", "--force", action="store_true")

    def __configure_logging(self, args):
        if args.debug:
            logging_level = logging.DEBUG
        elif args.logging_level is not None:
            logging_level = getattr(logging, args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format="%(asctime)s:%(processName)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s",
            level=logging_level,
        )

    def main(self):
        self.__add_arguments()
        args = self.__arg_parser.parse_args()
        self.__configure_logging(args)
​
        root_path = args.root_path
        if root_path is not None:
            root_path = Path(root_path)
        else:
            root_path = ROOT_DIR_PATH 
        if not root_path.is_dir():
            raise ValueError(root_path + " does not exist or is not a directory")
        args.root_path = root_path
​
        command_class = self.__COMMAND_CLASSES[args.command]
        command_kwds = vars(args).copy()
        command_kwds.pop("c")
        command_kwds.pop("logging_level")
        command = command_class(**command_kwds)
​
        command()


def main():
    Cli().main()


if __name__ == "__main__":
    main()
