import os
import json
from .oie_extraction.extraction import Extraction, UnstructuredExtraction


def file_handling(params):
    if "templates" in params:
        if not os.path.exists(params['templates']):
            raise FileNotFoundError(
                f"File {params['templates']} doesn't exist. "
                + "Please provide the log templates path."
            )


def print_params(params):
    print("{:-^80}".format("params"))
    print("Beginning extraction "
          + "using the following configuration:\n")
    for param, value in params.items():
        print("\t{:>13}: {}".format(param, value))
    print()
    print("-" * 80)


def combine_extractions(one, two):
    all_keys = set(one).union(set(two))
    combined = {}
    for key in all_keys:
        combined[key] = one.get(key, []) + two.get(key, [])
    return combined


def unstructure_extractions(extractions):
    for idx in extractions:
        unstructured = []
        for ext in extractions[idx]:
            if hasattr(ext, 'args'):
                unstructured.append(ext)
            else:
                unstructured.append(UnstructuredExtraction.fromExtraction(ext))
        extractions[idx] = unstructured
