from .registry import register


@register("redundancy")
def eval(results, ground_truth):
    """ Returns (number of predicted triples / number of partitions)
    as a measure of redundancy. Partitions are obtained using He's 
    approach for equivalent extraction. The higher, the more redundant."""
    num_pred = 0
    num_partitions = 0
    for idx in results:
        num_partitions += len(set(results[idx]))
        num_pred += len(results[idx])
    print(f'Redundancy: {num_pred / num_partitions}')