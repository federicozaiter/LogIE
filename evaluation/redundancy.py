from .registry import register
from .utils import check_structured


@register("redundancy")
def eval(results, ground_truth):
    """ Returns (number of predicted triples / number of partitions)
    as a measure of redundancy. Partitions are obtained using He's 
    approach for equivalent extraction. The higher, the more redundant."""
    check_structured(results)
    check_structured(ground_truth)

    num_pred = 0
    num_partitions = 0
    for idx in results:
        num_partitions += len(set(results[idx]))
        num_pred += len(results[idx])
    print(f'Redundancy: {num_pred / num_partitions}')