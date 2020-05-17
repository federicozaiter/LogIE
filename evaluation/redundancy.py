from .registry import register
from .utils import check_structured
from .evaluator import BaseEvaluator
from ..oie_extraction.extraction import UnstructuredExtraction
unstructure_extractions = UnstructuredExtraction.unstructure_extractions 
from .utils import check_unstructured


def redundancy(extractions):
    num_partitions = len(set(extractions))
    num_pred = len(extractions)
    return num_partitions, num_pred


class RedundancyEvaluator(BaseEvaluator):
    def single_eval(self, extractions, groundtruth):
        num_partitions, num_pred = redundancy(extractions)
        self.num_recalled += num_partitions
        self.num_extractions += num_pred
        if not (check_unstructured(extractions) and check_unstructured(groundtruth)):
            extractions = unstructure_extractions(extractions)
            groundtruth = unstructure_extractions(groundtruth)
        num_partitions, num_pred = redundancy(extractions)
        self.num_ok += num_partitions
        self.num_gt += num_pred

    def metrics(self):
        redundancy = self.num_extractions / self.num_recalled if self.num_recalled != 0 else 0
        lexical_red = self.num_gt / self.num_ok if self.num_ok != 0 else 0
        return {'Redundancy':redundancy, 'Lexical':lexical_red}


@register("redundancy")
def build_eval(params):
    """ Returns (number of predicted triples / number of partitions)
    as a measure of redundancy. Partitions are obtained using He's 
    approach for equivalent extraction. The higher, the more redundant."""
    return RedundancyEvaluator(params)
