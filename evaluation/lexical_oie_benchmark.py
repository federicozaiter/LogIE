# https://github.com/gabrielStanovsky/oie-benchmark/blob/master/benchmark.py
# https://github.com/gabrielStanovsky/oie-benchmark/blob/master/matcher.py
from .registry import register
from .utils import check_unstructured

LEXICAL_THRESHOLD = 0.25 # Same as theirs

@register("lexical")
def eval(results, ground_truth):
    """ This approach matches two extractions if their predicates 
    overlap in at least one word and if their arguments matching number
    of words percentage is above the lexical threshold."""
    check_unstructured(results)
    check_unstructured(ground_truth)

    num_extractions = 0
    num_gt = 0
    correct_ext = set()
    recalled_gt = set()
    for idx in results:
        num_extractions += len(results[idx])
        num_gt += len(ground_truth[idx])
        for e_idx, result in enumerate(results[idx]):
            for g_idx, gt in enumerate(ground_truth[idx]):
                pred_res = result.pred.strip().split()
                gt_res = gt.pred.strip().split()
                if not set(pred_res).intersection(set(gt_res)):
                    continue
                count_match = 0      
                for w1 in gt.args:
                    for w2 in result.args:
                        if w1 == w2:
                            count_match += 1
                coverage = float(count_match) / len(gt.args)

                # Counting differently for precision than for recall
                # Precision is for the extracted triples and recall is
                # for the ground truth triples
                if coverage > LEXICAL_THRESHOLD:
                    recalled_gt.add(str(idx) + str(g_idx))
                    correct_ext.add(str(idx) + str(e_idx)) 
    num_ok = len(correct_ext)
    num_recalled = len(recalled_gt)

    precision = num_ok / num_extractions
    recall = num_recalled / num_gt
    f1 = 2 * (precision * recall) / (precision + recall)
    f2 = 5 * (precision * recall) / (4 * precision + recall)
    print(f'Precision: {precision}, Recall: {recall}, F1: {f1}, F2: {f2}')