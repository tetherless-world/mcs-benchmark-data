from typing import Dict, Optional

from mcs-benchmark-data._extractor import _Extractor
from mcs-benchmark-data.paths import DATA_DIR, PROJECT_ROOT
from mcs-benchmark-data.pipeline_storage import PipelineStorage


class CommonsenseQAExtractor(_Extractor):
    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        jsonl_paths = []
        benchmark_source_path = (
            PROJECT_ROOT.parent / "data" / "CommonsenseQA" / "converted"
        )
        assert (
            benchmark_source_path.exists()
        ), f"Could not find benchmark source directory: {benchmark_source_path}"

        for benchmark_path in benchmark_source_path.iterdir():
            for benchmark_jsonl_path in benchmark_path.glob("*.jsonl"):
                jsonl_paths.append(benchmark_jsonl_path)
        assert (
            len(jsonl_paths) > 0
        ), f"No benchmark jsonl files found in {benchmark_source_path}"

        return {
            "benchmark_jsonl_paths": tuple(jsonl_paths),
        }