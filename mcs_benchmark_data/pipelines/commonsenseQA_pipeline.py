from typing import Optional

from rdflib import URIRef

from mcs_benchmark_data._pipeline import _Pipeline
from mcs_benchmark_data.extractors.nop_extractor import NopExtractor
from mcs_benchmark_data.transformers.commonsenseQA_transformer import (
    CommonsenseQATransformer
)


class CommonsenseQAPipeline(_Pipeline):
    def __init__(
        self,
        *,
        export_xml_file_path: str,
        owner: Optional[str],
        pipeline_id: str,
        **kwds
    ):
        _Pipeline.__init__(
            self,
            extractor=NopExtractor(),
            id=pipeline_id,
            transformer=CommonsenseQATransformer(
                owner=URIRef(owner) if owner is not None else None,
                pipeline_uri=_Pipeline.id_to_uri(pipeline_id),
            ),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--owner", help="URI of the owner, or public if absent")
        arg_parser.add_argument(
            "--pipeline-id",
            help="unique identifier for this pipeline, used to isolate its cache",
            required=True,
        )


if __name__ == "__main__":
    CommonsenseQAPipeline.main()