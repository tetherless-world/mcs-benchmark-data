import string
import stringcase as sc

from dataclasses import dataclass, asdict, fields

from pathlib import Path
from typing import Optional

from mcs_benchmark_data.path import TEMPLATE_DIR_PATH, ROOT_DIR_PATH


class Template:
    @dataclass
    class Context:
        benchmark_name: str
        submission_name: Optional[str] = None

    def __init__(
        self,
        *,
        context: Context,
        dest_file_name: str,
        template_file_name: str,
        dest_file_path_from_root: Path,
    ):
        self.context = context
        self.dest_file_name = dest_file_name
        self.template_file_name = template_file_name
        self.dest_file_path_from_root = dest_file_path_from_root

    def write_new_file(self, file_path: Path, file_data: str):
        if Path(file_path).exists():
            raise FileExistsError(f"The file at {file_path} already exists.")

        with open(file_path, "w") as fp:
            fp.write(file_data)

    def execute(self, *, root_path: Path, data_dir: str, force: Optional[bool] = False):

        format_args = asdict(self.context)

        for field in fields(Template.Context):
            field_value = getattr(self.context, field.name)
            if field_value is not None:
                format_args[sc.pascalcase(field.name)] = sc.pascalcase(field_value)
        format_args["data_dir"] = data_dir
        print(format_args)

        with open(TEMPLATE_DIR_PATH / self.template_file_name) as template_file:
            template_str = template_file.read()

        temp = string.Template(template_str)
        formatted_str = temp.substitute(**format_args)

        self.write_new_file(
            root_path / self.dest_file_path_from_root, file_data=formatted_str
        )

        return formatted_str
