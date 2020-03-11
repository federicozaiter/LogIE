from .registry import register
from ..oie_extraction.extraction import Extraction


@register("he")
def eval(results, ground_truth):
    """ This approach considers partitioning for each template, both the 
    results and the ground truth in groups that are equivalent according
    to He's approach. Two triples are equivalent if the syntactic heads
    of their predicates and arguments match."""
    precision = 0.0
    recall = 0.0
    for idx in results:
        num_ok = 0
        extractions = set(results[idx])
        if extractions:
            gt = set(ground_truth[idx])
            num_ok = len(gt and extractions)
            precision += num_ok/len(extractions)
            if gt:
                recall += num_ok/len(gt)
    precision /= len(results)
    recall /= len(results)
    f1 = 2 * (precision * recall) / (precision + recall)
    return precision, recall, f1