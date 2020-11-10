from mcs_benchmark_data._extractor import _Extractor


class NopExtractor(_Extractor):
    def extract(self, **kwds):
        return {}
