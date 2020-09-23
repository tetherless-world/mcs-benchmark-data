from mcs_benchmark_data.loaders.composite_loader import CompositeLoader
from mcs_benchmark_data.loaders.rdf_file_loader import RdfFileLoader


class DefaultLoader(CompositeLoader):
    def __init__(self, **kwds):
        CompositeLoader.__init__(self, loaders=(RdfFileLoader(**kwds),), **kwds)