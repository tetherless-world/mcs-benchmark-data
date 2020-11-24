import logging
import sys

from configargparse import ArgParser

from mcs_benchmark_data.cli.commands.create_submission_pipeline_command import (
    CreateSubmissionPipelineCommand,
)
from mcs_benchmark_data.cli.commands.create_benchmark_pipeline_command import (
    CreateBenchmarkPipelineCommand,
)


class Cli:
    def __init__(self):
        self.__commands = {
            "create-benchmark-pipeline": CreateBenchmarkPipelineCommand(),
            "create-submission-pipeline": CreateSubmissionPipelineCommand(),
        }

    @staticmethod
    def __add_global_args(arg_parser: ArgParser):
        arg_parser.add_argument(
            "--logging-level",
            help="set logging-level level (see Python logging module)",
        )

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
        args = self.__parse_args()
        self.__commands[args.command](args)

    def __parse_args(self):
        arg_parser = ArgParser()
        subparsers = arg_parser.add_subparsers(title="commands", dest="command")
        self.__add_global_args(arg_parser)
        for command_name, command in self.__commands.items():
            subparser = subparsers.add_parser(command_name)
            self.__add_global_args(subparser)
            command.add_arguments(subparser, self.__add_global_args)

        parsed_args = arg_parser.parse_args()
        if parsed_args.command is None:
            arg_parser.print_usage()
            sys.exit(1)

        return parsed_args


def main():
    Cli().main()


if __name__ == "__main__":
    main()
