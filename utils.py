import os
import json
from .oie_extraction.extraction import Extraction


def file_handling(params):
    if "templates" in params:
        if not os.path.exists(params['templates']):
            raise FileNotFoundError(
                f"File {params['templates']} doesn't exist. "
                + "Please provide the log templates path."
            )
        templates_directory = os.path.dirname(params['processed_templates'])
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)
    else:
        # Checks if preprocessed templates exist as input
        if not os.path.exists(params['processed_templates']):
            raise FileNotFoundError(
                f"File {params['processed_templates']} doesn't exist. "
                + "Preprocess target logs first and provide their path."
            )


def print_params(params):
    print("{:-^80}".format("params"))
    print("Beginning extraction "
          + "using the following configuration:\n")
    for param, value in params.items():
        print("\t{:>13}: {}".format(param, value))
    print()
    print("-" * 80)


def load_ground_truth(filepath):
    with open(filepath, 'r') as f:
        gt = json.load(f)
    for idx in gt:
        sentence = gt[idx][0]
        triples = gt[idx][1]
        if triples:
            triples = [Extraction.fromTuple(tup, sentence=sentence)
            for tup in triples]
        gt[idx] = triples
    return gt


def combine_extractions(one, two):
    all_keys = set(one) or set(two)
    combined = {}
    for key in all_keys:
        combined[key] = one.get(key, []) + two.get(key, [])
    return combined