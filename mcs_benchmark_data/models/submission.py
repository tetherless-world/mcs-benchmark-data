from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from datetime import datetime
from typing import Tuple

from rdflib import Graph
from rdflib.resource import Resource
from ..namespace import MCS, RDF

from mcs_benchmark_data._model import _Model
from mcs_benchmark_data.models.dev_score import DevScore
from mcs_benchmark_data.models.test_score import TestScore
from mcs_benchmark_data.models.submission_sample import SubmissionSample

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen = True)
class Submission(_Model):
    '''A submission dataset from a system/model with prediction choices for a benchmark'''
    name: str
    description: str
    dateCreated: datetime
    isBasedOn: str #benchmark name
    contributor: Tuple[str, ...]
    contentRating: Tuple[TestScore, DevScore]
    result: Tuple[str, datetime, datetime, str] #type (e.g. SoftwareAplication), startTime, endTime, url
    sample: Tuple[SubmissionSample, ...]


    def to_rdf(
        self, *, graph: Graph, **kwds) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph, **kwds
        )
        resource.add(RDF.type, MCS[self.__class__.__name__])

        #How to add name? FOAF?
        #How to add description, datecreated, isBasedOn?
        #How to add contributors? FOAF?
        resource.add(MCS.TestScore, self.contentRating[0])
        resource.add(MCS.DevScore, self.contentRating[1])
        #How to add result?
        if self.sample is not None:
            for smpl in self.sample:
                resource.add(MCS.SubmissionSample, smpl)
                #Need to smpl.to_rdf?

        return resource
