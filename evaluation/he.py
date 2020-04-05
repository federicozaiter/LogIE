from .registry import register


@register("he")
def eval(results, ground_truth):
    """ This approach considers partitioning for each template, both the 
    results and the ground truth in groups that are equivalent according
    to He's approach. Two triples are equivalent if the syntactic heads
    of their predicates and arguments match."""
    num_ok = 0
    num_extractions = 0
    num_gt = 0
    for idx in results:
        extractions = set(results[idx])
        gt = set(ground_truth[idx])
        num_ok += len(gt.intersection(extractions))
        num_extractions += len(extractions)
        num_gt += len(gt)
    precision = num_ok / num_extractions
    recall = num_ok / num_gt
    f1 = 2 * (precision * recall) / (precision + recall)
    f2 = 5 * (precision * recall) / (4 * precision + recall)
    print(f'Precision: {precision}, Recall: {recall}, F1: {f1}, F2: {f2}')