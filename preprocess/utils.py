import re
from tqdm import tqdm
from ..decorators import print_step
import json
from ..oie_extraction.extraction import Extraction


class Repl:
    def __init__(self, ini=0):
        self.called = ini
    def __call__(self, match):
        self.called += 1
        return f'VAR{self.called}'


@print_step
def process_templates_json(input_source, process_line=None):
    with open(input_source, 'r') as f:
        gt = json.load(f)
    templates = {}
    for idx in gt:
        sentence = process_line(gt[idx][0])
        triples = gt[idx][1]
        if triples:
            triples = [Extraction.fromTuple(tup, sentence=sentence)
            for tup in triples]
        gt[idx] = triples
        templates[idx] = sentence
    return templates, gt


brackets = re.compile(r'[\[\]\{\}]') # \(\)
def remove_brackets(line):
    return re.sub(brackets, ' ', line).strip()


# Some variables use underscores which we want to keep so we only remove
# the ones from longer sentences
underscores = re.compile(r'([\w\d]+_[\w\d]+){3,}')
def remove_underscores(match):
    group = match.group()
    return group.replace('_', ' ')
