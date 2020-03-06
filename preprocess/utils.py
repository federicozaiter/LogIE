import re
from tqdm import tqdm
from ..decorators import print_step


class Repl:
    def __init__(self, ini=0):
        self.called = ini
    def __call__(self, match):
        self.called += 1
        return f'VAR{self.called}'


@print_step
def process_templates(input_source, output, process_line=None):
    with open(output, "w", encoding='latin-1') as f:
        # counting first to show progress with tqdm
        with open(input_source, 'r', encoding='latin-1') as IN:
            line_count = sum(1 for line in IN)
        with open(input_source, 'r', encoding='latin-1') as IN:
                results = map(process_line, IN)
                f.writelines(tqdm(results, total=line_count))


@print_step
def load_processed_templates(params):
    templates_path = params['processed_templates']
    templates = {}
    with open(templates_path, 'r', encoding='latin-1') as IN:
        line_count = sum(1 for line in IN)
    with open(templates_path, 'r', encoding='latin-1') as IN:
        for line in tqdm(IN, total=line_count):
            line = line.strip()
            idx, template = line.split('\t')
            templates[idx] = template
    return templates
