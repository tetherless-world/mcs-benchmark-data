from pathlib import Path

ROOT_DIR_PATH = Path(__file__).parent.parent.absolute()

DATA_DIR_PATH = ROOT_DIR_PATH / "data"

TEST_DATA_DIR_PATH = ROOT_DIR_PATH / "test_data"

TEMPLATE_DIR_PATH = ROOT_DIR_PATH / "mcs_benchmark_data" / "cli" / "templates"
