import os
import json


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


def save_output_triples(triples, params):
    with open(params["templates"], 'r') as f:
        gt = json.load(f)
    
    # "index":["sentence", ["triple1", "triple2",]]
    result = {idx:[gt[idx][0], [str(triple) for triple in triples[idx]]] for idx in triples}
    output_file_name = f"{params['templates_type']}_{params['openie']}.json"
    with open(output_file_name, 'w') as out:
        json.dump(result, out, indent=4, sort_keys=False)
