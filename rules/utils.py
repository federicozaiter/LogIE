import re
import os


not_word_digit_pattern = re.compile(r'^[^\w\d]+|[^\w\d]+$')
def power_strip(string):
    return re.sub(not_word_digit_pattern, '', string)


def save_remaining(extractions, output_dir):
    remaining = os.path.join(output_dir, 'remaining.txt')
    with open(remaining, 'w') as remaining_f:
        for idx in extractions:
            remaining_idx = extractions[idx]
            # remaining_idx = [f'{idx}\t{line}' for line in remaining_idx]
            remaining_f.writelines('\n'.join((*remaining_idx,'')))
    return remaining
