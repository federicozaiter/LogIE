from .registry import register


@register("counts")
def eval(results, ground_truth):
    """ Returns the counts of expected and extracted triples."""
    num_ext = sum(len(results[idx]) for idx in results)
    num_gt = sum(len(ground_truth[idx]) for idx in ground_truth)
    print(f'Expected triples: {num_gt}, Number of extractions: {num_ext}')