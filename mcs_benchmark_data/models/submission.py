from dataclasses import dataclass
from dataclasses_json import LetterCase, dataclass_json
from datetime import datetime
from typing import Tuple, Optional

from rdflib import Graph
from rdflib.resource import Resource
from mcs_benchmark_data.namespace import MCS, SCHEMA, XSD

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
    contributors: Tuple[str, ...]
    contentRating: Tuple[TestScore, DevScore]
    result: Tuple[str, datetime, datetime, str] 
    sample: Optional[Tuple[SubmissionSample, ...]]


    def to_rdf(
        self, *, graph: Graph) -> Resource:
        resource = _Model.to_rdf(
            self, graph=graph
        )

        resource.add(SCHEMA.name, self.name)
        resource.add(XSD.string, self.description)
        resource.add(SCHEMA.date, self.dateCreated)
        resource.add(SCHEMA.isBasedOn, self.isBasedOn)
        for contributor in self.contributors:
            resource.add(SCHEMA.person, contributor)
        
        resource.add(MCS.testScore, self.contentRating[0])
        self.contentRating[0].to_rdf(graph)
        resource.add(MCS.devScore, self.contentRating[1])
        self.contentRating[1].to_rdf(graph)

        resource.add(SCHEMA.resultOf, self.result)
        resource.add(SCHEMA.softwareApplication, self.result[0])
        resource.add(SCHEMA.endTime, self.result[1])
        resource.add(SCHEMA.startTime, self.result[2])
        resource.add(SCHEMA.url, self.result[3])

        if self.sample is not None:
            for smpl in self.sample:
                resource.add(MCS.submissionSample, smpl)
                smpl.to_rdf(graph)

        return resource
