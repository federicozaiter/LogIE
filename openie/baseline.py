from .registry import register
from ..oie_extraction.extraction import Extraction
import spacy
__nlp = spacy.load('en_core_web_sm')

def get_triple(sentence):
    doc = __nlp(sentence)
    pred_start = -1
    pred_end = len(doc)

    idx = 0
    idx_token = enumerate(doc)
    pred_tags = ['AUX','VERB','ADP','ADV']
    while pred_start < 0 and idx < len(doc):
        idx, token = next(idx_token)
        if token.pos_ in pred_tags:
            pred_start = idx
    while pred_end == len(doc) and idx < len(doc):
        idx, token = next(idx_token)
        if token.pos_ not in pred_tags:
            pred_end = idx
    tokens = [token.text for token in doc]
    tup = (
        ' '.join(tokens[:pred_start]),
        ' '.join(tokens[pred_start:pred_end]),
        ' '.join(tokens[pred_end:] if pred_end < len(doc) else [])
    )
    return Extraction.fromTuple(tup, sentence=sentence)


@register('baseline')
def extract_triples(input_remaining, params):
    triples = {}
    remaining = {}
    for idx in input_remaining:
        triples[idx] = list(map(get_triple, input_remaining[idx]))
        remaining[idx] = []
    return triples, remaining