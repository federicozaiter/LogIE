import os
import json
import pandas as pd
import shutil


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


def save_global_output_triples(triples, params):
    with open(params["templates"], 'r') as f:
        gt = json.load(f)
    
    # "index":["sentence", ["triple1", "triple2",]]
    result = {idx:[gt[idx][0], [str(triple) for triple in triples[idx]]] for idx in triples}
    output_file_name = f"{params['templates_type']}_{params['openie']}.json"
    output_file = os.path.join(
        params['results_dir'],
        output_file_name,
    )
    with open(output_file, 'w') as out:
        json.dump(result, out, indent=4, sort_keys=False)


def save_log_triples(log_idx, triples, params):
    output_file_name = f"{params['templates_type']}_{params['openie']}.tsv"
    output_file = os.path.join(
        params['results_dir'],
        output_file_name
    )
    apend_write = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, apend_write) as f:
        for triple in triples:
            f.write(f'{params["id"]}\t{log_idx}\t{triple}\n')


def save_results(eval_metric, eval_result, params, file_name):
    record = [(params['templates_type'],
        params['openie'],
        eval_metric,
        eval_result['Precision'],
        eval_result['Recall'],
        eval_result['F1'],
        eval_result['F2'],
        )]
    df = pd.DataFrame(
        record,
        columns=['Logs',
            'OIE',
            'Metric',
            'Precision',
            'Recall',
            'F1',
            'F2',
            ]
        )  
    output_file_name =\
        f"metrics_{params['templates_type']}_{params['openie']}.csv"
    with open(output_file_name, 'a') as f:
        df.to_csv(f, mode='a', header=not f.tell())
        if not os.path.isfile(output_file_name):
            df.to_csv(output_file_name, header=True)
        else:
            df.to_csv(output_file_name, mode='a', header=False)


import re
varx_pattern = re.compile(r'VAR\d+') 
def remove_varx(triples_result):
    for idx in triples_result:
        for triple in triples_result[idx]:
                triple.pred = re.sub(varx_pattern, 'VARX', triple.pred)
                if hasattr(triple, 'arg1'):
                    triple.arg1 = re.sub(varx_pattern, 'VARX', triple.arg1)
                    triple.arg2 = re.sub(varx_pattern, 'VARX', triple.arg2)
                else:
                    triple.args = map(
                        lambda x: re.sub(varx_pattern, 'VARX', x),
                        triple.args,
                        )


def file_handling(params):
    if "templates" in params:
        if not os.path.exists(params['templates']):
            raise FileNotFoundError(
                f"File {params['templates']} doesn't exist. "
                + "Please provide the templates path."
            )
    else:
        raise FileNotFoundError(
            "Input templates are necesary to run LogIE. "
            + "Please provide the log templates path."
        )
    if "raw_logs" in params:
        if not os.path.exists(params['raw_logs']):
            raise FileNotFoundError(
                f"File {params['raw_logs']} doesn't exist. "
                + "Please provide the raw logs path."
            )

    if params['save_output']:
        # Checks if the experiment id already exists
        if os.path.exists(params["id_dir"]) and not params["force"]:
            raise FileExistsError(
                f"directory '{params['id_dir']} already exists. "
                + "Run with --force to overwrite."
                + f"If --force is used, you could lose your training results."
            )
        if os.path.exists(params["id_dir"]):
            shutil.rmtree(params["id_dir"])
        for target_dir in ['id_dir', 'results_dir']:
            os.makedirs(params[target_dir])
